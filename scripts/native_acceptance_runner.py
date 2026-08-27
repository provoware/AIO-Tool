#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import VERSION
from app.loopback_security import allowed_local_request
from app.native_acceptance import NativeAcceptanceError, NativeAcceptanceStore, STEPS
from app.persistence import PersistenceError

HOST = "127.0.0.1"
WEB = ROOT / "web"
RUNTIME = ROOT / "runtime"
STORE = NativeAcceptanceStore(RUNTIME / "native_acceptance.json", VERSION)
REPORT_DIR = RUNTIME / "reports"
BROWSER_COMMANDS = {"firefox": ("firefox",), "chromium": ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")}


def _browser_executable(name: str) -> str | None:
    for command in BROWSER_COMMANDS.get(name, ()):
        found = shutil.which(command)
        if found:
            return found
    return None


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_args) -> None:
        pass

    @property
    def app_port(self) -> int:
        return int(self.server.server_address[1])

    def _headers(self, status: int, content_type: str, length: int) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(length))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'")
        self.end_headers()

    def _json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self._headers(status, "application/json; charset=utf-8", len(body))
        self.wfile.write(body)

    def _read(self) -> dict:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise NativeAcceptanceError("Ungültige Anfragegröße.") from exc
        if length <= 0 or length > 128 * 1024:
            raise NativeAcceptanceError("Ungültige Anfragegröße.")
        value = json.loads(self.rfile.read(length).decode("utf-8"))
        if not isinstance(value, dict):
            raise NativeAcceptanceError("JSON-Objekt erwartet.")
        return value

    def _origin_ok(self) -> bool:
        return allowed_local_request(self.headers.get("Host", ""), self.headers.get("Origin"), self.app_port)

    def do_GET(self) -> None:
        if not self._origin_ok():
            self._json(HTTPStatus.FORBIDDEN, {"ok": False, "error": "Nur der lokale Runner-Port ist erlaubt."})
            return
        path = urlparse(self.path).path
        if path == "/api/session":
            self._json(HTTPStatus.OK, {"ok": True, "report": STORE.report(), "steps": STEPS, "browsers": {name: bool(_browser_executable(name)) for name in BROWSER_COMMANDS}})
            return
        if path == "/api/report":
            self._json(HTTPStatus.OK, {"ok": True, "report": STORE.report()})
            return
        if path == "/report.txt":
            _, txt = STORE.write_reports(REPORT_DIR)
            body = txt.read_bytes()
            self._headers(HTTPStatus.OK, "text/plain; charset=utf-8", len(body))
            self.wfile.write(body)
            return
        static = {
            "/": ("native-acceptance.html", "text/html; charset=utf-8"),
            "/native-acceptance.js": ("native-acceptance.js", "application/javascript; charset=utf-8"),
            "/helper-ui.css": ("helper-ui.css", "text/css; charset=utf-8"),
        }
        if path in static:
            name, content_type = static[path]
            body = (WEB / name).read_bytes()
            self._headers(HTTPStatus.OK, content_type, len(body))
            self.wfile.write(body)
            return
        self._json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "Nicht gefunden."})

    def do_POST(self) -> None:
        if not self._origin_ok():
            self._json(HTTPStatus.FORBIDDEN, {"ok": False, "error": "Nur der lokale Runner-Port ist erlaubt."})
            return
        path = urlparse(self.path).path
        try:
            payload = self._read()
            if path == "/api/session/new":
                STORE.start_new(); STORE.write_reports(REPORT_DIR); self._json(HTTPStatus.OK, {"ok": True, "report": STORE.report()}); return
            if path == "/api/result":
                STORE.record(str(payload.get("step_id", "")), str(payload.get("status", "")), str(payload.get("note", "")), payload.get("observed", {})); STORE.write_reports(REPORT_DIR); self._json(HTTPStatus.OK, {"ok": True, "report": STORE.report()}); return
            if path == "/api/open-browser":
                name = str(payload.get("browser", "")); executable = _browser_executable(name)
                if not executable:
                    raise NativeAcceptanceError("Gewählter Browser wurde nicht gefunden.")
                url = f"http://{HOST}:{self.app_port}/"
                subprocess.Popen([executable, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
                self._json(HTTPStatus.OK, {"ok": True, "browser": name}); return
            self._json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "Unbekannte Aktion."})
        except (NativeAcceptanceError, PersistenceError, OSError, ValueError, json.JSONDecodeError) as exc:
            self._json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(exc)})


def main() -> int:
    parser = argparse.ArgumentParser(description="AIO-Tool Native Acceptance Runner")
    parser.add_argument("--port", type=int, default=8778)
    parser.add_argument("--no-open", action="store_true")
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        raise SystemExit("Port muss zwischen 1024 und 65535 liegen.")
    RUNTIME.mkdir(parents=True, exist_ok=True)
    STORE.write_reports(REPORT_DIR)
    server = ThreadingHTTPServer((HOST, args.port), Handler)
    url = f"http://{HOST}:{server.server_address[1]}/"
    print(f"AIO-Tool Native Acceptance Runner · {VERSION}")
    print(f"Lokal: {url}")
    print("Berichte: runtime/reports/native-acceptance-latest.json/.txt")
    if not args.no_open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

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
from app.safe_file_sim import EXECUTION_ENABLED, SIMULATION_ONLY, SafeFileSimulationError, build_preview, failure_matrix

HOST = "127.0.0.1"
WEB = ROOT / "web"


def selector_capabilities() -> dict:
    return {"kdialog": bool(shutil.which("kdialog")), "zenity": bool(shutil.which("zenity"))}


def select_path(kind: str) -> str:
    if kind not in {"source", "target"}:
        raise SafeFileSimulationError("Unbekannte Auswahlart.")
    title = "Quelldatei auswählen" if kind == "source" else "Zielordner auswählen"
    start = str(Path.home())
    if shutil.which("kdialog"):
        command = ["kdialog", "--getopenfilename", start, "--title", title] if kind == "source" else ["kdialog", "--getexistingdirectory", start, "--title", title]
    elif shutil.which("zenity"):
        command = ["zenity", "--file-selection", "--title", title]
        if kind == "target":
            command.append("--directory")
    else:
        raise SafeFileSimulationError("Kein unterstützter Auswahldialog gefunden (kdialog/zenity).")
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else ""


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
            raise SafeFileSimulationError("Ungültige Anfragegröße.") from exc
        if length <= 0 or length > 64 * 1024:
            raise SafeFileSimulationError("Ungültige Anfragegröße.")
        value = json.loads(self.rfile.read(length).decode("utf-8"))
        if not isinstance(value, dict):
            raise SafeFileSimulationError("JSON-Objekt erwartet.")
        return value

    def _origin_ok(self) -> bool:
        return allowed_local_request(self.headers.get("Host", ""), self.headers.get("Origin"), self.app_port)

    def do_GET(self) -> None:
        if not self._origin_ok():
            self._json(HTTPStatus.FORBIDDEN, {"ok": False, "error": "Nur der lokale Simulator-Port ist erlaubt."})
            return
        path = urlparse(self.path).path
        if path == "/api/capabilities":
            self._json(HTTPStatus.OK, {"ok": True, "version": VERSION, "simulation_only": SIMULATION_ONLY, "execution_enabled": EXECUTION_ENABLED, "selectors": selector_capabilities(), "failure_matrix": failure_matrix()})
            return
        static = {
            "/": ("safe-file-sim.html", "text/html; charset=utf-8"),
            "/safe-file-sim.js": ("safe-file-sim.js", "application/javascript; charset=utf-8"),
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
            self._json(HTTPStatus.FORBIDDEN, {"ok": False, "error": "Nur der lokale Simulator-Port ist erlaubt."})
            return
        path = urlparse(self.path).path
        try:
            payload = self._read()
            if path == "/api/select":
                self._json(HTTPStatus.OK, {"ok": True, "path": select_path(str(payload.get("kind", "")))})
                return
            if path == "/api/preview":
                self._json(HTTPStatus.OK, {"ok": True, "preview": build_preview(str(payload.get("source", "")), str(payload.get("target", "")), str(payload.get("conflict_policy", "skip")))})
                return
            self._json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "Keine Ausführungsaktion vorhanden. SAFE-FILE ist Simulation-only."})
        except (SafeFileSimulationError, OSError, ValueError, json.JSONDecodeError) as exc:
            self._json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(exc)})


def main() -> int:
    parser = argparse.ArgumentParser(description="AIO-Tool SAFE-FILE Simulation")
    parser.add_argument("--port", type=int, default=8779)
    parser.add_argument("--no-open", action="store_true")
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        raise SystemExit("Port muss zwischen 1024 und 65535 liegen.")
    server = ThreadingHTTPServer((HOST, args.port), Handler)
    url = f"http://{HOST}:{server.server_address[1]}/"
    print(f"AIO-Tool SAFE-FILE Simulation · {VERSION}")
    print("SIMULATION ONLY · Es existiert keine Copy-/Move-/Delete-Ausführung.")
    print(f"Lokal: {url}")
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

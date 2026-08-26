from __future__ import annotations

import argparse
import json
import mimetypes
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from . import ROOT_DIR, VERSION
from .config import ConfigError, ConfigStore

WEB_DIR = ROOT_DIR / "web"
RUNTIME_DIR = ROOT_DIR / "runtime"
CONFIG_STORE = ConfigStore(RUNTIME_DIR / "config.json")
MAX_BODY_BYTES = 64 * 1024
ALLOWED_CONFIG_KEYS = {"theme", "font_scale", "expert_visible", "setup_complete", "active_project", "favorites"}


def allowed_host(host: str, port: int) -> bool:
    host = (host or "").strip().lower()
    return host in {f"127.0.0.1:{port}", f"localhost:{port}", "127.0.0.1", "localhost"}


def allowed_origin(origin: str | None, port: int) -> bool:
    if not origin:
        return True
    try:
        parsed = urlparse(origin)
    except ValueError:
        return False
    return parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "localhost"} and (parsed.port or 80) == port


class AIORequestHandler(BaseHTTPRequestHandler):
    server_version = "AIO-Tool"

    @property
    def app_port(self) -> int:
        return int(self.server.server_address[1])

    def log_message(self, fmt: str, *args: object) -> None:
        RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
        line = "%s [HTTP] %s\n" % (self.log_date_time_string(), fmt % args)
        with (RUNTIME_DIR / "server.log").open("a", encoding="utf-8") as handle:
            handle.write(line)

    def _security_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'")
        self.send_header("Cache-Control", "no-store")

    def _reject_if_untrusted(self, mutating: bool = False) -> bool:
        if not allowed_host(self.headers.get("Host", ""), self.app_port):
            self._json(HTTPStatus.FORBIDDEN, {"ok": False, "error": "Ungültiger Host."})
            return True
        if mutating and not allowed_origin(self.headers.get("Origin"), self.app_port):
            self._json(HTTPStatus.FORBIDDEN, {"ok": False, "error": "Ungültige Herkunft."})
            return True
        return False

    def _json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._security_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ConfigError("Ungültige Anfragegröße.") from exc
        if length <= 0 or length > MAX_BODY_BYTES:
            raise ConfigError("Anfrage ist leer oder zu groß.")
        try:
            value = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ConfigError("Ungültiges JSON.") from exc
        if not isinstance(value, dict):
            raise ConfigError("JSON muss ein Objekt sein.")
        return value

    def do_GET(self) -> None:
        if self._reject_if_untrusted():
            return
        path = urlparse(self.path).path
        if path == "/api/status":
            try:
                config = CONFIG_STORE.load()
            except ConfigError as exc:
                self._json(HTTPStatus.INTERNAL_SERVER_ERROR, {"ok": False, "error": str(exc)})
                return
            self._json(HTTPStatus.OK, {
                "ok": True,
                "version": VERSION,
                "ready": True,
                "bind": "127.0.0.1",
                "internet_required": False,
                "external_python_packages": [],
                "config": config,
            })
            return
        if path == "/api/config":
            try:
                self._json(HTTPStatus.OK, {"ok": True, "config": CONFIG_STORE.load()})
            except ConfigError as exc:
                self._json(HTTPStatus.INTERNAL_SERVER_ERROR, {"ok": False, "error": str(exc)})
            return
        self._serve_static(path)

    def do_POST(self) -> None:
        if self._reject_if_untrusted(mutating=True):
            return
        path = urlparse(self.path).path
        if path != "/api/config":
            self._json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "Unbekannter API-Pfad."})
            return
        try:
            changes = self._read_json()
            unknown = set(changes) - ALLOWED_CONFIG_KEYS
            if unknown:
                raise ConfigError("Nicht erlaubte Einstellung: " + ", ".join(sorted(unknown)))
            config = CONFIG_STORE.update(changes)
        except ConfigError as exc:
            self._json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(exc)})
            return
        self._json(HTTPStatus.OK, {"ok": True, "config": config})

    def _serve_static(self, request_path: str) -> None:
        relative = "index.html" if request_path in {"", "/"} else request_path.lstrip("/")
        candidate = (WEB_DIR / relative).resolve()
        try:
            candidate.relative_to(WEB_DIR.resolve())
        except ValueError:
            self.send_error(HTTPStatus.FORBIDDEN)
            return
        if not candidate.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        body = candidate.read_bytes()
        content_type = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
        self.send_response(HTTPStatus.OK)
        self._security_headers()
        self.send_header("Content-Type", content_type + ("; charset=utf-8" if content_type.startswith("text/") or "javascript" in content_type else ""))
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def create_server(port: int = 8765) -> ThreadingHTTPServer:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    return ThreadingHTTPServer(("127.0.0.1", port), AIORequestHandler)


def main() -> None:
    parser = argparse.ArgumentParser(description="AIO-Tool lokales Backend")
    parser.add_argument("--port", type=int, default=int(os.environ.get("AIO_PORT", "8765")))
    args = parser.parse_args()
    server = create_server(args.port)
    print(f"AIO-Tool {VERSION} bereit: http://127.0.0.1:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
import mimetypes
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from . import ROOT_DIR, VERSION
from .config import ConfigError, ConfigStore
from .event_registry import EventRegistry, EventRegistryError
from .todo_store import TodoStore, TodoStoreError
from .version_registry import VersionRegistry, VersionRegistryError

WEB_DIR = ROOT_DIR / "web"
RUNTIME_DIR = ROOT_DIR / "runtime"
CONFIG_STORE = ConfigStore(RUNTIME_DIR / "config.json")
VERSION_REGISTRY = VersionRegistry(RUNTIME_DIR / "versions.json")
EVENT_REGISTRY = EventRegistry(RUNTIME_DIR / "events.json")
TODO_STORE = TodoStore(RUNTIME_DIR / "todos.json")
MAX_BODY_BYTES = 64 * 1024
ALLOWED_CONFIG_KEYS = {"theme", "font_scale", "expert_visible", "setup_complete", "active_project", "favorites"}
TODO_ALLOWED_KEYS = {"title", "category", "due_date", "due_time", "priority", "note", "calendar_event_id"}


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


def ensure_core_state() -> None:
    known = {item["version"] for item in VERSION_REGISTRY.load()["versions"]}
    VERSION_REGISTRY.ensure_current(
        VERSION,
        summary="VersionRegistry, EventRegistry und persistenter TODO-Kern.",
        changes=[
            "VersionRegistry mit Evidenzvertrag",
            "menschenlesbare EventRegistry",
            "TODO-Kern mit Titelgedächtnis und Erledigt-Archiv",
        ],
    )
    if VERSION not in known:
        try:
            EVENT_REGISTRY.add(
                kind="version_registered",
                area="Versionierung",
                level="info",
                message=f"Version {VERSION} wurde als neuer Entwicklungsstand registriert.",
                details={"version": VERSION},
            )
        except EventRegistryError:
            pass


def _safe_event(**kwargs: object) -> str | None:
    try:
        EVENT_REGISTRY.add(**kwargs)
        return None
    except EventRegistryError:
        return "Aktion wurde gespeichert, das Ereignisprotokoll konnte aber nicht aktualisiert werden."


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

    def _read_json(self, *, required: bool = True) -> dict:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ConfigError("Ungültige Anfragegröße.") from exc
        if length == 0 and not required:
            return {}
        if length <= 0 or length > MAX_BODY_BYTES:
            raise ConfigError("Anfrage ist leer oder zu groß.")
        try:
            value = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ConfigError("Ungültiges JSON.") from exc
        if not isinstance(value, dict):
            raise ConfigError("JSON muss ein Objekt sein.")
        return value

    def _query_limit(self, parsed, default: int, maximum: int) -> int:
        raw = parse_qs(parsed.query).get("limit", [str(default)])[0]
        try:
            limit = int(raw)
        except ValueError as exc:
            raise ConfigError("limit muss eine Zahl sein.") from exc
        if limit < 1 or limit > maximum:
            raise ConfigError(f"limit muss zwischen 1 und {maximum} liegen.")
        return limit

    def do_GET(self) -> None:
        if self._reject_if_untrusted():
            return
        parsed = urlparse(self.path)
        path = parsed.path
        try:
            if path == "/api/status":
                config = CONFIG_STORE.load()
                versions = VERSION_REGISTRY.consistency(VERSION)
                todos = TODO_STORE.load()
                self._json(HTTPStatus.OK, {
                    "ok": True,
                    "version": VERSION,
                    "ready": True,
                    "bind": "127.0.0.1",
                    "internet_required": False,
                    "external_python_packages": [],
                    "config": config,
                    "core": {
                        "version_registry": versions,
                        "events": EVENT_REGISTRY.count(),
                        "todos_open": len(todos["items"]),
                        "todos_archived": len(todos["archive"]),
                    },
                })
                return
            if path == "/api/config":
                self._json(HTTPStatus.OK, {"ok": True, "config": CONFIG_STORE.load()})
                return
            if path == "/api/versions":
                self._json(HTTPStatus.OK, {
                    "ok": True,
                    "registry": VERSION_REGISTRY.load(),
                    "consistency": VERSION_REGISTRY.consistency(VERSION),
                    "previous_version": VERSION_REGISTRY.previous_version(),
                })
                return
            if path == "/api/events":
                limit = self._query_limit(parsed, 5, 100)
                self._json(HTTPStatus.OK, {"ok": True, "events": EVENT_REGISTRY.latest(limit)})
                return
            if path == "/api/todos":
                data = TODO_STORE.load()
                self._json(HTTPStatus.OK, {
                    "ok": True,
                    "items": data["items"],
                    "next": TODO_STORE.next_items(3),
                    "archive_count": len(data["archive"]),
                })
                return
            if path == "/api/todos/archive":
                limit = self._query_limit(parsed, 100, 500)
                self._json(HTTPStatus.OK, {"ok": True, "items": TODO_STORE.list_archive(limit)})
                return
            if path == "/api/todos/suggestions":
                limit = self._query_limit(parsed, 12, 50)
                self._json(HTTPStatus.OK, {"ok": True, "titles": TODO_STORE.title_suggestions(limit)})
                return
        except (ConfigError, VersionRegistryError, EventRegistryError, TodoStoreError) as exc:
            self._json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(exc)})
            return
        self._serve_static(path)

    def do_POST(self) -> None:
        if self._reject_if_untrusted(mutating=True):
            return
        path = urlparse(self.path).path
        try:
            if path == "/api/config":
                changes = self._read_json()
                unknown = set(changes) - ALLOWED_CONFIG_KEYS
                if unknown:
                    raise ConfigError("Nicht erlaubte Einstellung: " + ", ".join(sorted(unknown)))
                config = CONFIG_STORE.update(changes)
                self._json(HTTPStatus.OK, {"ok": True, "config": config})
                return

            if path == "/api/todos":
                payload = self._read_json()
                unknown = set(payload) - TODO_ALLOWED_KEYS
                if unknown:
                    raise TodoStoreError("Nicht erlaubtes TODO-Feld: " + ", ".join(sorted(unknown)))
                if "title" not in payload:
                    raise TodoStoreError("Titel fehlt.")
                item = TODO_STORE.create(**payload)
                warning = _safe_event(
                    kind="todo_created",
                    area="TODO",
                    level="green",
                    message=f"TODO „{item['title']}“ wurde angelegt.",
                    details={"todo_id": item["id"]},
                )
                response = {"ok": True, "item": item}
                if warning:
                    response["warning"] = warning
                self._json(HTTPStatus.CREATED, response)
                return

            if path.startswith("/api/todos/") and path.endswith("/complete"):
                todo_id = path.removeprefix("/api/todos/").removesuffix("/complete").strip("/")
                if not todo_id:
                    raise TodoStoreError("TODO-ID fehlt.")
                self._read_json(required=False)
                item = TODO_STORE.complete(todo_id)
                warning = _safe_event(
                    kind="todo_completed",
                    area="TODO",
                    level="green",
                    message=f"TODO „{item['title']}“ wurde erledigt und ins Archiv verschoben.",
                    details={"todo_id": item["id"], "completed_at": item["completed_at"]},
                )
                response = {"ok": True, "item": item}
                if warning:
                    response["warning"] = warning
                self._json(HTTPStatus.OK, response)
                return
        except (ConfigError, VersionRegistryError, EventRegistryError, TodoStoreError) as exc:
            self._json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(exc)})
            return

        self._json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "Unbekannter API-Pfad."})

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
    ensure_core_state()
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

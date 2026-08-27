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
from .calendar_store import CalendarStore, CalendarStoreError, local_now
from .config import ConfigError, ConfigIntegrityError, ConfigStore
from .error_advisor import ErrorAdvisor
from .event_registry import EventRegistry, EventRegistryError
from .persistence import PersistenceError
from .todo_store import TodoStore, TodoStoreError
from .version_registry import VersionRegistry, VersionRegistryError, validate_registry

WEB_DIR = ROOT_DIR / "web"
RUNTIME_DIR = ROOT_DIR / "runtime"
VERSION_SEED_PATH = ROOT_DIR / "VERSION_REGISTRY.json"
CONFIG_STORE = ConfigStore(RUNTIME_DIR / "config.json")
VERSION_SEED = validate_registry(json.loads(VERSION_SEED_PATH.read_text(encoding="utf-8")))
VERSION_REGISTRY = VersionRegistry(RUNTIME_DIR / "versions.json", default=VERSION_SEED)
EVENT_REGISTRY = EventRegistry(RUNTIME_DIR / "events.json")
TODO_STORE = TodoStore(RUNTIME_DIR / "todos.json")
CALENDAR_STORE = CalendarStore(RUNTIME_DIR / "calendar.json")
ERROR_ADVISOR = ErrorAdvisor()
TEXTS = ERROR_ADVISOR.catalog
MAX_BODY_BYTES = 64 * 1024
ALLOWED_CONFIG_KEYS = {"theme", "font_scale", "expert_visible", "setup_complete", "active_project", "favorites"}
TODO_ALLOWED_KEYS = {"title", "category", "due_date", "due_time", "priority", "note", "calendar_event_id"}
CALENDAR_ALLOWED_KEYS = {"title", "date", "start_time", "end_time", "category", "description", "reminders", "todo_id"}


class RequestError(ValueError):
    """Invalid HTTP input supplied by the local UI/client."""


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
        summary="Kalender-Core mit persistenten Terminen, Ansichten, Titelgedächtnis und Reminder-Quittierung.",
        changes=[
            "persistenter Kalender-Core",
            "Monats-, Wochen- und Jahresperioden",
            "Erinnerungs-Presets und fällige Reminder",
            "optionale TODO-Verknüpfung",
            "Kalender-Vorlagen und negative Testdaten",
        ],
    )
    if VERSION not in known:
        try:
            EVENT_REGISTRY.add(
                kind="version_registered",
                area="Versionierung",
                level="info",
                message=TEXTS.get("event.version_registered", version=VERSION),
                details={"version": VERSION},
            )
        except (EventRegistryError, PersistenceError):
            pass


def _safe_event(**kwargs: object) -> str | None:
    try:
        EVENT_REGISTRY.add(**kwargs)
        return None
    except (EventRegistryError, PersistenceError):
        return TEXTS.get("server.event_warning")


def _advice_for(exc: Exception, *, area: str) -> dict:
    try:
        return ERROR_ADVISOR.advise(exc, area=area)
    except Exception:
        return {
            "rule_id": "ERR-ADVISOR-FALLBACK",
            "category": "unknown",
            "severity": "red",
            "message": "Fehlerhilfe konnte nicht sicher geladen werden.",
            "action": "Keine Nutzerdaten automatisch verändern; Diagnose öffnen.",
            "template_path": None,
            "retry_safe": False,
            "area": area,
        }


def _todo_exists(todo_id: str) -> bool:
    data = TODO_STORE.load()
    return any(item["id"] == todo_id for item in data["items"]) or any(item["id"] == todo_id for item in data["archive"])


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
            self._json(HTTPStatus.FORBIDDEN, {"ok": False, "error": TEXTS.get("server.invalid_host")})
            return True
        if mutating and not allowed_origin(self.headers.get("Origin"), self.app_port):
            self._json(HTTPStatus.FORBIDDEN, {"ok": False, "error": TEXTS.get("server.invalid_origin")})
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
            raise RequestError("Ungültige Anfragegröße.") from exc
        if length == 0 and not required:
            return {}
        if length <= 0 or length > MAX_BODY_BYTES:
            raise RequestError("Anfrage ist leer oder zu groß.")
        try:
            value = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RequestError("Ungültiges JSON.") from exc
        if not isinstance(value, dict):
            raise RequestError("JSON muss ein Objekt sein.")
        return value

    def _query_limit(self, parsed, default: int, maximum: int) -> int:
        raw = parse_qs(parsed.query).get("limit", [str(default)])[0]
        try:
            limit = int(raw)
        except ValueError as exc:
            raise RequestError("limit muss eine Zahl sein.") from exc
        if limit < 1 or limit > maximum:
            raise RequestError(f"limit muss zwischen 1 und {maximum} liegen.")
        return limit

    def _respond_error(self, exc: Exception, *, area: str, default_status: int) -> None:
        help_info = _advice_for(exc, area=area)
        status = HTTPStatus.INTERNAL_SERVER_ERROR if help_info.get("category") == "integrity" else default_status
        self._json(status, {
            "ok": False,
            "error": help_info["message"],
            "detail": str(exc),
            "help": help_info,
        })

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
                calendar_data = CALENDAR_STORE.load()
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
                        "calendar_events": len(calendar_data["events"]),
                        "error_help": ERROR_ADVISOR.metadata(),
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
            if path == "/api/calendar":
                query = parse_qs(parsed.query)
                view = query.get("view", ["month"])[0]
                anchor = query.get("date", [local_now().date().isoformat()])[0]
                self._json(HTTPStatus.OK, {"ok": True, "calendar": CALENDAR_STORE.period(view, anchor)})
                return
            if path == "/api/calendar/suggestions":
                limit = self._query_limit(parsed, 12, 50)
                self._json(HTTPStatus.OK, {"ok": True, "titles": CALENDAR_STORE.title_suggestions(limit)})
                return
            if path == "/api/calendar/reminders/due":
                query = parse_qs(parsed.query)
                now = query.get("now", [None])[0]
                limit = self._query_limit(parsed, 100, 500)
                self._json(HTTPStatus.OK, {"ok": True, "reminders": CALENDAR_STORE.due_reminders(now, limit)})
                return
            if path == "/api/help/meta":
                self._json(HTTPStatus.OK, {"ok": True, "help": ERROR_ADVISOR.metadata()})
                return
        except RequestError as exc:
            self._respond_error(exc, area="API", default_status=HTTPStatus.BAD_REQUEST)
            return
        except CalendarStoreError as exc:
            self._respond_error(exc, area="Kalender", default_status=HTTPStatus.BAD_REQUEST)
            return
        except (ConfigError, PersistenceError, VersionRegistryError, EventRegistryError, TodoStoreError, OSError) as exc:
            self._respond_error(exc, area="Persistenz", default_status=HTTPStatus.INTERNAL_SERVER_ERROR)
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
                    raise RequestError("Nicht erlaubte Einstellung: " + ", ".join(sorted(unknown)))
                config = CONFIG_STORE.update(changes)
                self._json(HTTPStatus.OK, {"ok": True, "config": config})
                return

            if path == "/api/todos":
                payload = self._read_json()
                unknown = set(payload) - TODO_ALLOWED_KEYS
                if unknown:
                    raise RequestError("Nicht erlaubtes TODO-Feld: " + ", ".join(sorted(unknown)))
                if "title" not in payload:
                    raise RequestError("Titel fehlt.")
                item = TODO_STORE.create(**payload)
                warning = _safe_event(
                    kind="todo_created",
                    area="TODO",
                    level="green",
                    message=TEXTS.get("event.todo_created", title=item["title"]),
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
                    raise RequestError("TODO-ID fehlt.")
                self._read_json(required=False)
                item = TODO_STORE.complete(todo_id)
                warning = _safe_event(
                    kind="todo_completed",
                    area="TODO",
                    level="green",
                    message=TEXTS.get("event.todo_completed", title=item["title"]),
                    details={"todo_id": item["id"], "completed_at": item["completed_at"]},
                )
                response = {"ok": True, "item": item}
                if warning:
                    response["warning"] = warning
                self._json(HTTPStatus.OK, response)
                return

            if path == "/api/calendar":
                payload = self._read_json()
                unknown = set(payload) - CALENDAR_ALLOWED_KEYS
                if unknown:
                    raise RequestError("Nicht erlaubtes Kalender-Feld: " + ", ".join(sorted(unknown)))
                if "title" not in payload:
                    raise RequestError("Titel fehlt.")
                if "date" not in payload:
                    raise RequestError("Datum fehlt.")
                todo_id = payload.get("todo_id")
                if todo_id is not None and (not isinstance(todo_id, str) or not todo_id.strip() or not _todo_exists(todo_id.strip())):
                    raise RequestError("Das ausgewählte TODO wurde nicht gefunden.")
                event = CALENDAR_STORE.create(**payload)
                warning = _safe_event(
                    kind="calendar_created",
                    area="Kalender",
                    level="green",
                    message=TEXTS.get("event.calendar_created", title=event["title"], date=event["date"]),
                    details={"calendar_event_id": event["id"], "todo_id": event["todo_id"]},
                )
                response = {"ok": True, "event": event}
                if warning:
                    response["warning"] = warning
                self._json(HTTPStatus.CREATED, response)
                return

            parts = [part for part in path.split("/") if part]
            if len(parts) == 6 and parts[0:2] == ["api", "calendar"] and parts[3] == "reminders" and parts[5] == "ack":
                event_id = parts[2]
                try:
                    minutes = int(parts[4])
                except ValueError as exc:
                    raise RequestError("Erinnerungswert muss eine Zahl sein.") from exc
                payload = self._read_json(required=False)
                unknown = set(payload) - {"when"}
                if unknown:
                    raise RequestError("Nicht erlaubtes Erinnerungs-Feld: " + ", ".join(sorted(unknown)))
                event = CALENDAR_STORE.acknowledge_reminder(event_id, minutes, when=payload.get("when"))
                warning = _safe_event(
                    kind="calendar_reminder_ack",
                    area="Kalender",
                    level="info",
                    message=TEXTS.get("event.reminder_ack", title=event["title"]),
                    details={"calendar_event_id": event["id"], "minutes_before": minutes},
                )
                response = {"ok": True, "event": event}
                if warning:
                    response["warning"] = warning
                self._json(HTTPStatus.OK, response)
                return
        except RequestError as exc:
            self._respond_error(exc, area="Eingabe", default_status=HTTPStatus.BAD_REQUEST)
            return
        except ConfigIntegrityError as exc:
            self._respond_error(exc, area="Konfiguration", default_status=HTTPStatus.INTERNAL_SERVER_ERROR)
            return
        except CalendarStoreError as exc:
            self._respond_error(exc, area="Kalender", default_status=HTTPStatus.BAD_REQUEST)
            return
        except (ConfigError, TodoStoreError) as exc:
            self._respond_error(exc, area="Eingabe", default_status=HTTPStatus.BAD_REQUEST)
            return
        except (PersistenceError, VersionRegistryError, EventRegistryError, OSError) as exc:
            self._respond_error(exc, area="Persistenz", default_status=HTTPStatus.INTERNAL_SERVER_ERROR)
            return

        self._json(HTTPStatus.NOT_FOUND, {"ok": False, "error": TEXTS.get("server.unknown_api")})

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

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from .persistence import AtomicJsonStore, PersistenceError

SCHEMA_VERSION = 1
EVENT_LEVELS = {"green", "yellow", "orange", "red", "info"}
MAX_EVENTS = 500

DEFAULT_EVENTS: dict[str, Any] = {
    "schema_version": SCHEMA_VERSION,
    "events": [],
}


class EventRegistryError(PersistenceError):
    pass


def _text(value: Any, field: str, *, allow_empty: bool = False, max_length: int = 500) -> str:
    if not isinstance(value, str):
        raise EventRegistryError(f"{field} muss Text sein.")
    result = value.strip()
    if not result and not allow_empty:
        raise EventRegistryError(f"{field} darf nicht leer sein.")
    if len(result) > max_length:
        raise EventRegistryError(f"{field} ist zu lang.")
    return result


def validate_events(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict) or value.get("schema_version") != SCHEMA_VERSION:
        raise EventRegistryError("Unbekanntes EventRegistry-Schema.")
    events = value.get("events")
    if not isinstance(events, list):
        raise EventRegistryError("events muss eine Liste sein.")

    clean: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in events[-MAX_EVENTS:]:
        if not isinstance(raw, dict):
            raise EventRegistryError("Ereignis muss ein Objekt sein.")
        event_id = _text(raw.get("id"), "id", max_length=80)
        if event_id in seen:
            raise EventRegistryError("Ereignis-ID ist doppelt vorhanden.")
        seen.add(event_id)
        level = _text(raw.get("level", "info"), "level", max_length=20)
        if level not in EVENT_LEVELS:
            raise EventRegistryError(f"Unbekannte Ereignisstufe: {level}")
        details = raw.get("details", {})
        if not isinstance(details, dict):
            raise EventRegistryError("details muss ein Objekt sein.")
        clean.append({
            "id": event_id,
            "time": _text(raw.get("time"), "time", max_length=80),
            "kind": _text(raw.get("kind"), "kind", max_length=80),
            "area": _text(raw.get("area", "Allgemein"), "area", max_length=100),
            "level": level,
            "message": _text(raw.get("message"), "message", max_length=500),
            "details": deepcopy(details),
        })
    return {"schema_version": SCHEMA_VERSION, "events": clean}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class EventRegistry:
    def __init__(self, path: Path):
        self.store = AtomicJsonStore(path, DEFAULT_EVENTS, validate_events)

    def load(self) -> dict[str, Any]:
        return self.store.load()

    def add(
        self,
        *,
        kind: str,
        message: str,
        area: str = "Allgemein",
        level: str = "info",
        details: dict[str, Any] | None = None,
        when: str | None = None,
    ) -> dict[str, Any]:
        kind = _text(kind, "kind", max_length=80)
        message = _text(message, "message", max_length=500)
        area = _text(area, "area", max_length=100)
        if level not in EVENT_LEVELS:
            raise EventRegistryError(f"Unbekannte Ereignisstufe: {level}")
        if details is not None and not isinstance(details, dict):
            raise EventRegistryError("details muss ein Objekt sein.")
        event = {
            "id": uuid4().hex[:16],
            "time": when or utc_now(),
            "kind": kind,
            "area": area,
            "level": level,
            "message": message,
            "details": deepcopy(details or {}),
        }

        def mutate(data: dict[str, Any]) -> dict[str, Any]:
            data["events"].append(event)
            data["events"] = data["events"][-MAX_EVENTS:]
            return data

        self.store.update(mutate)
        return deepcopy(event)

    def latest(self, limit: int = 5) -> list[dict[str, Any]]:
        if not isinstance(limit, int) or limit < 1 or limit > 100:
            raise EventRegistryError("limit muss zwischen 1 und 100 liegen.")
        events = self.load()["events"]
        return deepcopy(list(reversed(events[-limit:])))

    def count(self) -> int:
        return len(self.load()["events"])

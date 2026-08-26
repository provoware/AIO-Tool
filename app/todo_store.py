from __future__ import annotations

from copy import deepcopy
from datetime import date, datetime, time, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from .persistence import AtomicJsonStore, PersistenceError

SCHEMA_VERSION = 1
PRIORITIES = {"low", "normal", "high"}
MAX_TITLE_MEMORY = 100

DEFAULT_TODOS: dict[str, Any] = {
    "schema_version": SCHEMA_VERSION,
    "items": [],
    "archive": [],
    "title_memory": [],
}


class TodoStoreError(PersistenceError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _text(value: Any, field: str, *, allow_empty: bool = False, max_length: int = 500) -> str:
    if not isinstance(value, str):
        raise TodoStoreError(f"{field} muss Text sein.")
    result = value.strip()
    if not result and not allow_empty:
        raise TodoStoreError(f"{field} darf nicht leer sein.")
    if len(result) > max_length:
        raise TodoStoreError(f"{field} ist zu lang.")
    return result


def _optional_text(value: Any, field: str, max_length: int = 500) -> str | None:
    if value is None:
        return None
    result = _text(value, field, allow_empty=True, max_length=max_length)
    return result or None


def _validate_date(value: Any) -> str | None:
    result = _optional_text(value, "due_date", 10)
    if result is None:
        return None
    try:
        date.fromisoformat(result)
    except ValueError as exc:
        raise TodoStoreError("due_date muss YYYY-MM-DD sein.") from exc
    return result


def _validate_time(value: Any) -> str | None:
    result = _optional_text(value, "due_time", 5)
    if result is None:
        return None
    try:
        parsed = time.fromisoformat(result)
    except ValueError as exc:
        raise TodoStoreError("due_time muss HH:MM sein.") from exc
    return parsed.strftime("%H:%M")


def _validate_item(raw: Any, *, archived: bool) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise TodoStoreError("TODO-Eintrag muss ein Objekt sein.")
    priority = _text(raw.get("priority", "normal"), "priority", max_length=20)
    if priority not in PRIORITIES:
        raise TodoStoreError(f"Unbekannte Priorität: {priority}")
    item = {
        "id": _text(raw.get("id"), "id", max_length=80),
        "title": _text(raw.get("title"), "title", max_length=160),
        "created_at": _text(raw.get("created_at"), "created_at", max_length=80),
        "updated_at": _text(raw.get("updated_at"), "updated_at", max_length=80),
        "category": _optional_text(raw.get("category"), "category", 80),
        "due_date": _validate_date(raw.get("due_date")),
        "due_time": _validate_time(raw.get("due_time")),
        "priority": priority,
        "note": _optional_text(raw.get("note"), "note", 2000),
        "calendar_event_id": _optional_text(raw.get("calendar_event_id"), "calendar_event_id", 100),
    }
    if archived:
        item["completed_at"] = _text(raw.get("completed_at"), "completed_at", max_length=80)
    return item


def validate_todos(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict) or value.get("schema_version") != SCHEMA_VERSION:
        raise TodoStoreError("Unbekanntes TODO-Schema.")
    items = value.get("items")
    archive = value.get("archive")
    memory = value.get("title_memory")
    if not isinstance(items, list) or not isinstance(archive, list) or not isinstance(memory, list):
        raise TodoStoreError("TODO-Listen fehlen oder sind ungültig.")

    clean_items = [_validate_item(item, archived=False) for item in items]
    clean_archive = [_validate_item(item, archived=True) for item in archive]
    ids = [item["id"] for item in clean_items + clean_archive]
    if len(ids) != len(set(ids)):
        raise TodoStoreError("TODO-ID ist doppelt vorhanden.")

    clean_memory: list[dict[str, Any]] = []
    seen_titles: set[str] = set()
    for raw in memory[-MAX_TITLE_MEMORY:]:
        if not isinstance(raw, dict):
            raise TodoStoreError("title_memory-Eintrag muss ein Objekt sein.")
        title = _text(raw.get("title"), "title_memory.title", max_length=160)
        key = title.casefold()
        if key in seen_titles:
            raise TodoStoreError("Titel ist mehrfach in title_memory vorhanden.")
        seen_titles.add(key)
        count = raw.get("count", 1)
        if not isinstance(count, int) or count < 1:
            raise TodoStoreError("title_memory.count muss eine positive Zahl sein.")
        clean_memory.append({
            "title": title,
            "count": count,
            "last_used_at": _text(raw.get("last_used_at"), "last_used_at", max_length=80),
        })

    return {
        "schema_version": SCHEMA_VERSION,
        "items": clean_items,
        "archive": clean_archive,
        "title_memory": clean_memory,
    }


class TodoStore:
    def __init__(self, path: Path):
        self.store = AtomicJsonStore(path, DEFAULT_TODOS, validate_todos)

    def load(self) -> dict[str, Any]:
        return self.store.load()

    def create(
        self,
        *,
        title: str,
        category: str | None = None,
        due_date: str | None = None,
        due_time: str | None = None,
        priority: str = "normal",
        note: str | None = None,
        calendar_event_id: str | None = None,
    ) -> dict[str, Any]:
        now = utc_now()
        raw = {
            "id": uuid4().hex[:16],
            "title": title,
            "created_at": now,
            "updated_at": now,
            "category": category,
            "due_date": due_date,
            "due_time": due_time,
            "priority": priority,
            "note": note,
            "calendar_event_id": calendar_event_id,
        }
        item = _validate_item(raw, archived=False)

        def mutate(data: dict[str, Any]) -> dict[str, Any]:
            data["items"].append(item)
            self._remember_title(data, item["title"], now)
            return data

        self.store.update(mutate)
        return deepcopy(item)

    def complete(self, todo_id: str, *, when: str | None = None) -> dict[str, Any]:
        todo_id = _text(todo_id, "todo_id", max_length=80)
        completed_at = when or utc_now()
        completed: dict[str, Any] | None = None

        def mutate(data: dict[str, Any]) -> dict[str, Any]:
            nonlocal completed
            index = next((i for i, item in enumerate(data["items"]) if item["id"] == todo_id), None)
            if index is None:
                raise TodoStoreError("TODO wurde nicht gefunden oder ist bereits erledigt.")
            item = data["items"].pop(index)
            item["updated_at"] = completed_at
            item["completed_at"] = completed_at
            data["archive"].append(item)
            completed = deepcopy(item)
            return data

        self.store.update(mutate)
        assert completed is not None
        return completed

    def list_active(self) -> list[dict[str, Any]]:
        return deepcopy(self.load()["items"])

    def list_archive(self, limit: int | None = None) -> list[dict[str, Any]]:
        archive = list(reversed(self.load()["archive"]))
        if limit is not None:
            if not isinstance(limit, int) or limit < 1 or limit > 500:
                raise TodoStoreError("limit muss zwischen 1 und 500 liegen.")
            archive = archive[:limit]
        return deepcopy(archive)

    def next_items(self, limit: int = 3) -> list[dict[str, Any]]:
        if not isinstance(limit, int) or limit < 1 or limit > 100:
            raise TodoStoreError("limit muss zwischen 1 und 100 liegen.")
        priority_rank = {"high": 0, "normal": 1, "low": 2}

        def key(item: dict[str, Any]) -> tuple[str, int, str, str]:
            due = item["due_date"] or "9999-12-31"
            due_time = item["due_time"] or "23:59"
            return (due, priority_rank[item["priority"]], due_time, item["created_at"])

        return deepcopy(sorted(self.load()["items"], key=key)[:limit])

    def title_suggestions(self, limit: int = 12) -> list[dict[str, Any]]:
        if not isinstance(limit, int) or limit < 1 or limit > 50:
            raise TodoStoreError("limit muss zwischen 1 und 50 liegen.")
        memory = self.load()["title_memory"]
        ranked = sorted(memory, key=lambda item: (item["count"], item["last_used_at"]), reverse=True)
        return deepcopy(ranked[:limit])

    @staticmethod
    def _remember_title(data: dict[str, Any], title: str, when: str) -> None:
        key = title.casefold()
        existing = next((item for item in data["title_memory"] if item["title"].casefold() == key), None)
        if existing is None:
            data["title_memory"].append({"title": title, "count": 1, "last_used_at": when})
        else:
            existing["title"] = title
            existing["count"] += 1
            existing["last_used_at"] = when
        data["title_memory"] = sorted(
            data["title_memory"], key=lambda item: item["last_used_at"]
        )[-MAX_TITLE_MEMORY:]

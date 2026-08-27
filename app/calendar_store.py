from __future__ import annotations

import calendar as calendar_lib
import os
from copy import deepcopy
from datetime import date, datetime, time, timedelta, tzinfo
from pathlib import Path
from typing import Any
from uuid import uuid4
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .persistence import AtomicJsonStore, PersistenceError

SCHEMA_VERSION = 1
ALLOWED_REMINDERS = {0, 10, 30, 60, 1440}
MAX_TITLE_MEMORY = 100
MAX_EVENTS = 10000

DEFAULT_CALENDAR: dict[str, Any] = {
    "schema_version": SCHEMA_VERSION,
    "events": [],
    "title_memory": [],
}


class CalendarStoreError(PersistenceError):
    pass


def system_timezone() -> tzinfo:
    """Best effort IANA system timezone with a safe local-offset fallback."""
    candidates: list[str] = []
    env_tz = os.environ.get("TZ")
    if env_tz:
        candidates.append(env_tz)
    timezone_file = Path("/etc/timezone")
    if timezone_file.is_file():
        try:
            value = timezone_file.read_text(encoding="utf-8").strip()
            if value:
                candidates.append(value)
        except OSError:
            pass
    try:
        resolved = Path("/etc/localtime").resolve().as_posix()
        marker = "/zoneinfo/"
        if marker in resolved:
            candidates.append(resolved.split(marker, 1)[1])
    except OSError:
        pass
    for key in candidates:
        try:
            return ZoneInfo(key)
        except ZoneInfoNotFoundError:
            continue
    return datetime.now().astimezone().tzinfo or ZoneInfo("UTC")


def local_now() -> datetime:
    return datetime.now(system_timezone())


def iso_now() -> str:
    return local_now().isoformat(timespec="seconds")


def _text(value: Any, field: str, *, allow_empty: bool = False, max_length: int = 500) -> str:
    if not isinstance(value, str):
        raise CalendarStoreError(f"{field} muss Text sein.")
    result = value.strip()
    if not result and not allow_empty:
        raise CalendarStoreError(f"{field} darf nicht leer sein.")
    if len(result) > max_length:
        raise CalendarStoreError(f"{field} ist zu lang.")
    return result


def _optional_text(value: Any, field: str, max_length: int = 500) -> str | None:
    if value is None:
        return None
    result = _text(value, field, allow_empty=True, max_length=max_length)
    return result or None


def _date(value: Any, field: str = "date") -> str:
    result = _text(value, field, max_length=10)
    try:
        return date.fromisoformat(result).isoformat()
    except ValueError as exc:
        raise CalendarStoreError(f"{field} muss YYYY-MM-DD sein.") from exc


def _time(value: Any, field: str, *, optional: bool = True) -> str | None:
    if optional and value is None:
        return None
    result = _optional_text(value, field, 5) if optional else _text(value, field, max_length=5)
    if result is None:
        return None
    try:
        parsed = time.fromisoformat(result)
    except ValueError as exc:
        raise CalendarStoreError(f"{field} muss HH:MM sein.") from exc
    return parsed.strftime("%H:%M")


def _timestamp(value: Any, field: str, *, optional: bool = False) -> str | None:
    if optional and value is None:
        return None
    result = _optional_text(value, field, 80) if optional else _text(value, field, max_length=80)
    if result is None:
        return None
    try:
        datetime.fromisoformat(result)
    except ValueError as exc:
        raise CalendarStoreError(f"{field} muss ein ISO-Zeitstempel sein.") from exc
    return result


def _reminders(value: Any, *, start_time: str | None) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise CalendarStoreError("reminders muss eine Liste sein.")
    if value and start_time is None:
        raise CalendarStoreError("Erinnerungen benötigen eine Startzeit.")
    clean: list[dict[str, Any]] = []
    seen: set[int] = set()
    for raw in value:
        if isinstance(raw, int):
            minutes = raw
            notified_at = None
        elif isinstance(raw, dict):
            minutes = raw.get("minutes_before")
            notified_at = _timestamp(raw.get("notified_at"), "reminder.notified_at", optional=True)
        else:
            raise CalendarStoreError("Erinnerung muss Zahl oder Objekt sein.")
        if not isinstance(minutes, int) or minutes not in ALLOWED_REMINDERS:
            raise CalendarStoreError("Unbekannte Erinnerung. Erlaubt: 0, 10, 30, 60 oder 1440 Minuten vorher.")
        if minutes in seen:
            raise CalendarStoreError("Erinnerung ist doppelt vorhanden.")
        seen.add(minutes)
        clean.append({"minutes_before": minutes, "notified_at": notified_at})
    return sorted(clean, key=lambda item: item["minutes_before"], reverse=True)


def _validate_event(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise CalendarStoreError("Kalendertermin muss ein Objekt sein.")
    start_time = _time(raw.get("start_time"), "start_time")
    end_time = _time(raw.get("end_time"), "end_time")
    if end_time is not None and start_time is None:
        raise CalendarStoreError("Eine Endzeit benötigt eine Startzeit.")
    if start_time is not None and end_time is not None and end_time <= start_time:
        raise CalendarStoreError("Endzeit muss nach der Startzeit liegen.")
    timezone_mode = _text(raw.get("timezone", "local"), "timezone", max_length=20)
    if timezone_mode != "local":
        raise CalendarStoreError("timezone muss derzeit 'local' sein.")
    return {
        "id": _text(raw.get("id"), "id", max_length=80),
        "title": _text(raw.get("title"), "title", max_length=160),
        "date": _date(raw.get("date")),
        "start_time": start_time,
        "end_time": end_time,
        "category": _optional_text(raw.get("category"), "category", 80),
        "description": _optional_text(raw.get("description"), "description", 2000),
        "todo_id": _optional_text(raw.get("todo_id"), "todo_id", 100),
        "timezone": timezone_mode,
        "reminders": _reminders(raw.get("reminders", []), start_time=start_time),
        "created_at": _timestamp(raw.get("created_at"), "created_at"),
        "updated_at": _timestamp(raw.get("updated_at"), "updated_at"),
    }


def validate_calendar(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict) or value.get("schema_version") != SCHEMA_VERSION:
        raise CalendarStoreError("Unbekanntes Kalender-Schema.")
    events = value.get("events")
    memory = value.get("title_memory")
    if not isinstance(events, list) or not isinstance(memory, list):
        raise CalendarStoreError("Kalenderlisten fehlen oder sind ungültig.")
    if len(events) > MAX_EVENTS:
        raise CalendarStoreError("Zu viele Kalendertermine in einer Datei.")

    clean_events = [_validate_event(item) for item in events]
    ids = [item["id"] for item in clean_events]
    if len(ids) != len(set(ids)):
        raise CalendarStoreError("Kalendertermin-ID ist doppelt vorhanden.")

    clean_memory: list[dict[str, Any]] = []
    seen_titles: set[str] = set()
    for raw in memory[-MAX_TITLE_MEMORY:]:
        if not isinstance(raw, dict):
            raise CalendarStoreError("title_memory-Eintrag muss ein Objekt sein.")
        title = _text(raw.get("title"), "title_memory.title", max_length=160)
        key = title.casefold()
        if key in seen_titles:
            raise CalendarStoreError("Kalendertitel ist mehrfach im Titelgedächtnis vorhanden.")
        seen_titles.add(key)
        count = raw.get("count", 1)
        if not isinstance(count, int) or count < 1:
            raise CalendarStoreError("title_memory.count muss eine positive Zahl sein.")
        clean_memory.append({
            "title": title,
            "count": count,
            "last_used_at": _timestamp(raw.get("last_used_at"), "title_memory.last_used_at"),
        })

    return {"schema_version": SCHEMA_VERSION, "events": clean_events, "title_memory": clean_memory}


class CalendarStore:
    def __init__(self, path: Path):
        self.store = AtomicJsonStore(path, DEFAULT_CALENDAR, validate_calendar)

    def load(self) -> dict[str, Any]:
        return self.store.load()

    def create(
        self,
        *,
        title: str,
        date: str,
        start_time: str | None = None,
        end_time: str | None = None,
        category: str | None = None,
        description: str | None = None,
        reminders: list[int] | list[dict[str, Any]] | None = None,
        todo_id: str | None = None,
    ) -> dict[str, Any]:
        now = iso_now()
        event = _validate_event({
            "id": uuid4().hex[:16],
            "title": title,
            "date": date,
            "start_time": start_time,
            "end_time": end_time,
            "category": category,
            "description": description,
            "todo_id": todo_id,
            "timezone": "local",
            "reminders": reminders or [],
            "created_at": now,
            "updated_at": now,
        })

        def mutate(data: dict[str, Any]) -> dict[str, Any]:
            data["events"].append(event)
            self._remember_title(data, event["title"], now)
            return data

        self.store.update(mutate)
        return deepcopy(event)

    def get(self, event_id: str) -> dict[str, Any]:
        event_id = _text(event_id, "event_id", max_length=80)
        event = next((item for item in self.load()["events"] if item["id"] == event_id), None)
        if event is None:
            raise CalendarStoreError("Kalendertermin wurde nicht gefunden.")
        return deepcopy(event)

    def title_suggestions(self, limit: int = 12) -> list[dict[str, Any]]:
        if not isinstance(limit, int) or limit < 1 or limit > 50:
            raise CalendarStoreError("limit muss zwischen 1 und 50 liegen.")
        ranked = sorted(self.load()["title_memory"], key=lambda item: (item["count"], item["last_used_at"]), reverse=True)
        return deepcopy(ranked[:limit])

    def period(self, view: str, anchor: str) -> dict[str, Any]:
        view = _text(view, "view", max_length=20).casefold()
        anchor_date = date.fromisoformat(_date(anchor, "anchor"))
        if view == "month":
            start = anchor_date.replace(day=1)
            end = anchor_date.replace(day=calendar_lib.monthrange(anchor_date.year, anchor_date.month)[1])
        elif view == "week":
            start = anchor_date - timedelta(days=anchor_date.weekday())
            end = start + timedelta(days=6)
        elif view == "year":
            start = date(anchor_date.year, 1, 1)
            end = date(anchor_date.year, 12, 31)
        else:
            raise CalendarStoreError("view muss month, week oder year sein.")

        events = [item for item in self.load()["events"] if start.isoformat() <= item["date"] <= end.isoformat()]
        events.sort(key=lambda item: (item["date"], item["start_time"] or "00:00", item["title"].casefold()))
        by_date: dict[str, list[dict[str, Any]]] = {}
        for event in events:
            by_date.setdefault(event["date"], []).append(deepcopy(event))
        return {"view": view, "anchor": anchor_date.isoformat(), "start": start.isoformat(), "end": end.isoformat(), "events": deepcopy(events), "by_date": by_date}

    def due_reminders(self, now: str | None = None, limit: int = 100) -> list[dict[str, Any]]:
        if not isinstance(limit, int) or limit < 1 or limit > 500:
            raise CalendarStoreError("limit muss zwischen 1 und 500 liegen.")
        current = local_now() if now is None else self._parse_local_datetime(now, "now")
        due: list[dict[str, Any]] = []
        for event in self.load()["events"]:
            if event["start_time"] is None:
                continue
            event_start = self._event_datetime(event)
            for reminder in event["reminders"]:
                if reminder["notified_at"] is not None:
                    continue
                trigger = event_start - timedelta(minutes=reminder["minutes_before"])
                if trigger <= current:
                    due.append({
                        "event_id": event["id"],
                        "title": event["title"],
                        "date": event["date"],
                        "start_time": event["start_time"],
                        "minutes_before": reminder["minutes_before"],
                        "trigger_at": trigger.isoformat(timespec="minutes"),
                    })
        due.sort(key=lambda item: (item["trigger_at"], item["event_id"], -item["minutes_before"]))
        return deepcopy(due[:limit])

    def acknowledge_reminder(self, event_id: str, minutes_before: int, *, when: str | None = None) -> dict[str, Any]:
        event_id = _text(event_id, "event_id", max_length=80)
        if not isinstance(minutes_before, int) or minutes_before not in ALLOWED_REMINDERS:
            raise CalendarStoreError("Unbekannte Erinnerung.")
        notified_at = when or iso_now()
        _timestamp(notified_at, "notified_at")
        updated: dict[str, Any] | None = None

        def mutate(data: dict[str, Any]) -> dict[str, Any]:
            nonlocal updated
            event = next((item for item in data["events"] if item["id"] == event_id), None)
            if event is None:
                raise CalendarStoreError("Kalendertermin wurde nicht gefunden.")
            reminder = next((item for item in event["reminders"] if item["minutes_before"] == minutes_before), None)
            if reminder is None:
                raise CalendarStoreError("Erinnerung wurde für diesen Termin nicht gefunden.")
            if reminder["notified_at"] is None:
                reminder["notified_at"] = notified_at
                event["updated_at"] = notified_at
            updated = deepcopy(event)
            return data

        self.store.update(mutate)
        assert updated is not None
        return updated

    @staticmethod
    def _parse_local_datetime(value: str, field: str) -> datetime:
        value = _text(value, field, max_length=80)
        try:
            parsed = datetime.fromisoformat(value)
        except ValueError as exc:
            raise CalendarStoreError(f"{field} muss ein ISO-Zeitstempel sein.") from exc
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=system_timezone())
        return parsed

    @staticmethod
    def _event_datetime(event: dict[str, Any]) -> datetime:
        naive = datetime.fromisoformat(f"{event['date']}T{event['start_time']}:00")
        return naive.replace(tzinfo=system_timezone())

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
        data["title_memory"] = sorted(data["title_memory"], key=lambda item: item["last_used_at"])[-MAX_TITLE_MEMORY:]

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = 1
STATUSES = {"active", "retired"}


class LearningMemoryError(ValueError):
    """Fehler in der Entwicklungs-Lerndatei."""


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LearningMemoryError(f"{field} fehlt oder ist leer.")
    return value.strip()


def validate_entry(raw: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(raw, dict) or raw.get("schema_version") != SCHEMA_VERSION:
        raise LearningMemoryError("Unbekanntes Learning-Memory-Schema.")
    applies_to = raw.get("applies_to", [])
    if not isinstance(applies_to, list) or not all(isinstance(item, str) and item.strip() for item in applies_to):
        raise LearningMemoryError("applies_to muss eine Liste aus nichtleeren Texten sein.")
    status = _text(raw.get("status"), "status")
    if status not in STATUSES:
        raise LearningMemoryError(f"Unbekannter Learning-Status: {status}")
    return {
        "schema_version": SCHEMA_VERSION,
        "id": _text(raw.get("id"), "id"),
        "created_at": _text(raw.get("created_at"), "created_at"),
        "area": _text(raw.get("area"), "area"),
        "trigger": _text(raw.get("trigger"), "trigger"),
        "lesson": _text(raw.get("lesson"), "lesson"),
        "rule": _text(raw.get("rule"), "rule"),
        "regression": _text(raw.get("regression"), "regression"),
        "status": status,
        "applies_to": [item.strip() for item in applies_to],
    }


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    path = Path(path)
    entries: list[dict[str, Any]] = []
    seen: set[str] = set()
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise LearningMemoryError(f"Learning Memory '{path}' ist nicht lesbar.") from exc
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            raw = json.loads(line)
        except json.JSONDecodeError as exc:
            raise LearningMemoryError(f"Ungültiges JSON in Learning Memory, Zeile {number}.") from exc
        entry = validate_entry(raw)
        if entry["id"] in seen:
            raise LearningMemoryError(f"Learning-ID '{entry['id']}' ist doppelt.")
        seen.add(entry["id"])
        entries.append(entry)
    if not entries:
        raise LearningMemoryError("Learning Memory enthält keine Einträge.")
    return entries


def active_entries(entries: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    return [entry for entry in entries if entry.get("status") == "active"]


def relevant(entries: Iterable[dict[str, Any]], areas: Iterable[str]) -> list[dict[str, Any]]:
    wanted = {area.casefold() for area in areas}
    result: list[dict[str, Any]] = []
    for entry in active_entries(entries):
        scopes = {scope.casefold() for scope in entry["applies_to"]}
        if "*" in scopes or scopes.intersection(wanted):
            result.append(entry)
    return result

from __future__ import annotations

import json
import os
import shutil
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .calendar_store import DEFAULT_CALENDAR, validate_calendar
from .config import DEFAULT_CONFIG, validate_config
from .event_registry import DEFAULT_EVENTS, validate_events
from .todo_store import DEFAULT_TODOS, validate_todos
from .version_registry import validate_registry

Validator = Callable[[dict[str, Any]], dict[str, Any]]


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("JSON-Wurzel muss ein Objekt sein.")
    return value


def _atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".selfheal.tmp")
    payload = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    try:
        with temp.open("wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        try:
            temp.unlink(missing_ok=True)
        except OSError:
            pass


def _quarantine(path: Path, quarantine_root: Path, *, label: str) -> Path | None:
    """Preserve a suspicious file before any replacement."""
    if not path.exists():
        return None
    destination = quarantine_root / f"{_utc_stamp()}-{label}-{path.name}"
    destination.parent.mkdir(parents=True, exist_ok=True)
    counter = 1
    while destination.exists():
        destination = destination.with_name(f"{destination.stem}-{counter}{destination.suffix}")
        counter += 1
    shutil.move(str(path), str(destination))
    return destination


def _validated(path: Path, validator: Validator) -> dict[str, Any]:
    return validator(_load_json(path))


def repair_json_state(path: Path, *, default: dict[str, Any], validator: Validator, quarantine_root: Path) -> dict[str, Any]:
    """Repair JSON state without silently discarding an original file."""
    path = Path(path)
    backup = path.with_suffix(path.suffix + ".bak")
    quarantined: list[str] = []
    if not path.exists():
        clean = validator(deepcopy(default))
        _atomic_write_json(path, clean)
        return {"status": "initialized", "quarantined": quarantined, "value": clean}
    try:
        clean = _validated(path, validator)
        return {"status": "healthy", "quarantined": quarantined, "value": clean}
    except Exception:
        pass
    if backup.exists():
        try:
            clean_backup = _validated(backup, validator)
            moved = _quarantine(path, quarantine_root, label="corrupt-main")
            if moved:
                quarantined.append(str(moved))
            _atomic_write_json(path, clean_backup)
            return {"status": "backup-restored", "quarantined": quarantined, "value": clean_backup}
        except Exception:
            pass
    moved = _quarantine(path, quarantine_root, label="corrupt-main")
    if moved:
        quarantined.append(str(moved))
    moved = _quarantine(backup, quarantine_root, label="corrupt-backup")
    if moved:
        quarantined.append(str(moved))
    clean = validator(deepcopy(default))
    _atomic_write_json(path, clean)
    return {"status": "reset-safe", "quarantined": quarantined, "value": clean}


def repair_runtime_state(runtime_dir: Path, version_seed: dict[str, Any]) -> dict[str, Any]:
    """Repair all persisted core stores before the HTTP server imports them."""
    runtime_dir = Path(runtime_dir)
    runtime_dir.mkdir(parents=True, exist_ok=True)
    quarantine = runtime_dir / "quarantine"
    contracts: list[tuple[str, dict[str, Any], Validator]] = [
        ("config.json", DEFAULT_CONFIG, validate_config),
        ("events.json", DEFAULT_EVENTS, validate_events),
        ("todos.json", DEFAULT_TODOS, validate_todos),
        ("calendar.json", DEFAULT_CALENDAR, validate_calendar),
        ("versions.json", version_seed, validate_registry),
    ]
    results: dict[str, Any] = {}
    for filename, default, validator in contracts:
        results[filename] = repair_json_state(runtime_dir / filename, default=default, validator=validator, quarantine_root=quarantine)
    repaired = [name for name, result in results.items() if result["status"] not in {"healthy", "initialized"}]
    initialized = [name for name, result in results.items() if result["status"] == "initialized"]
    return {"ok": True, "runtime_dir": str(runtime_dir), "repaired": repaired, "initialized": initialized, "files": {name: {k: v for k, v in result.items() if k != "value"} for name, result in results.items()}}

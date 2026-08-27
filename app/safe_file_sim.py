from __future__ import annotations

import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
SIMULATION_ONLY = True
EXECUTION_ENABLED = False
CONFLICT_POLICIES = {"skip", "rename", "replace-preview"}

FAILURE_MATRIX = [
    {"id": "SF-001", "case": "source_missing", "severity": "red", "effect": "Simulation blockiert"},
    {"id": "SF-002", "case": "source_not_file", "severity": "red", "effect": "Simulation blockiert"},
    {"id": "SF-003", "case": "source_symlink", "severity": "red", "effect": "Simulation blockiert"},
    {"id": "SF-004", "case": "target_missing", "severity": "red", "effect": "Simulation blockiert"},
    {"id": "SF-005", "case": "target_not_directory", "severity": "red", "effect": "Simulation blockiert"},
    {"id": "SF-006", "case": "target_symlink", "severity": "red", "effect": "Simulation blockiert"},
    {"id": "SF-007", "case": "target_not_writable", "severity": "red", "effect": "Simulation blockiert"},
    {"id": "SF-008", "case": "insufficient_space", "severity": "red", "effect": "Simulation blockiert"},
    {"id": "SF-009", "case": "destination_exists", "severity": "orange", "effect": "Explizite Konfliktentscheidung nötig"},
    {"id": "SF-010", "case": "same_source_destination", "severity": "red", "effect": "Simulation blockiert"}
]


class SafeFileSimulationError(ValueError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _check(check_id: str, ok: bool, label: str, detail: str) -> dict[str, Any]:
    return {"id": check_id, "ok": bool(ok), "status": "green" if ok else "red", "label": label, "detail": detail}


def _unique_destination(target: Path, name: str) -> Path:
    candidate = target / name
    if not candidate.exists():
        return candidate
    stem = Path(name).stem
    suffix = Path(name).suffix
    for number in range(1, 10000):
        candidate = target / f"{stem} ({number}){suffix}"
        if not candidate.exists():
            return candidate
    raise SafeFileSimulationError("Kein freier Vorschlagsname gefunden.")


def validate_preview_contract(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict) or value.get("schema_version") != SCHEMA_VERSION:
        raise SafeFileSimulationError("SAFE-FILE-Vorschau-Schema ist ungültig.")
    if value.get("simulation_only") is not True or value.get("execution_enabled") is not False:
        raise SafeFileSimulationError("SAFE-FILE-Simulation darf keine Ausführung freigeben.")
    if value.get("mutation_performed") is not False:
        raise SafeFileSimulationError("SAFE-FILE-Simulation darf keine Mutation melden.")
    recovery = value.get("recovery_contract")
    if not isinstance(recovery, dict) or recovery.get("current_mode") != "no-mutation" or recovery.get("rollback_required") is not False:
        raise SafeFileSimulationError("Recovery-Vertrag der Simulation ist ungültig.")
    return value


def build_preview(source_path: str | Path, target_path: str | Path, conflict_policy: str = "skip", *, free_bytes: int | None = None) -> dict[str, Any]:
    if conflict_policy not in CONFLICT_POLICIES:
        raise SafeFileSimulationError("Unbekannte Konfliktoption.")
    source = Path(source_path).expanduser()
    target = Path(target_path).expanduser()
    checks: list[dict[str, Any]] = []
    source_exists = source.exists()
    checks.append(_check("source_exists", source_exists, "Quelle gefunden", str(source)))
    source_symlink = source.is_symlink() if source_exists else False
    checks.append(_check("source_not_symlink", source_exists and not source_symlink, "Quelle ist kein symbolischer Link", "Symlinks sind im ersten Sicherheits-Slice gesperrt."))
    source_file = source.is_file() if source_exists else False
    checks.append(_check("source_regular_file", source_file and not source_symlink, "Quelle ist eine normale Datei", "Verzeichnisse folgen erst in einem späteren Vertrag."))
    source_readable = source_file and os.access(source, os.R_OK)
    checks.append(_check("source_readable", source_readable, "Quelle ist lesbar", "Nur Leserechte werden geprüft; nichts wird verändert."))
    target_exists = target.exists()
    checks.append(_check("target_exists", target_exists, "Zielordner gefunden", str(target)))
    target_symlink = target.is_symlink() if target_exists else False
    checks.append(_check("target_not_symlink", target_exists and not target_symlink, "Ziel ist kein symbolischer Link", "Symlink-Ziele sind im ersten Sicherheits-Slice gesperrt."))
    target_dir = target.is_dir() if target_exists else False
    checks.append(_check("target_directory", target_dir and not target_symlink, "Ziel ist ein Ordner", ""))
    target_writable = target_dir and os.access(target, os.W_OK)
    checks.append(_check("target_writable", target_writable, "Ziel ist beschreibbar", "Es wird trotzdem nicht geschrieben; dies ist nur eine Vorprüfung."))
    size = source.stat().st_size if source_file else 0
    reserve = max(10 * 1024 * 1024, int(size * 0.05))
    free = shutil.disk_usage(target).free if free_bytes is None and target_dir else int(free_bytes or 0)
    enough = target_dir and free >= size + reserve
    checks.append(_check("free_space", enough, "Genügend freier Speicher", f"Datei {size} Byte · Reserve {reserve} Byte · frei {free} Byte"))
    destination = target / source.name if source.name else target
    same = False
    if source_exists and target_exists:
        try:
            same = source.resolve() == destination.resolve(strict=False)
        except OSError:
            same = False
    checks.append(_check("different_destination", not same, "Quelle und Ziel sind verschieden", str(destination)))
    conflict_exists = destination.exists() if target_dir and source.name else False
    selected_destination = destination
    if conflict_exists and conflict_policy == "rename":
        selected_destination = _unique_destination(target, source.name)
    conflict = {"exists": conflict_exists, "destination": str(destination), "policy": conflict_policy, "selected_destination": str(selected_destination), "replace_is_preview_only": conflict_policy == "replace-preview", "decision_required": conflict_exists and conflict_policy == "skip"}
    hard_checks_ok = all(item["ok"] for item in checks)
    would_copy = hard_checks_ok and (not conflict_exists or conflict_policy in {"rename", "replace-preview"})
    if conflict_exists and conflict_policy == "skip":
        would_copy = False
    preview = {
        "schema_version": SCHEMA_VERSION, "created_at": _now(), "mode": "simulation-only", "simulation_only": SIMULATION_ONLY, "execution_enabled": EXECUTION_ENABLED, "operation": "copy-preview",
        "source": {"path": str(source), "size_bytes": size}, "target": {"directory": str(target), "free_bytes": free, "reserve_bytes": reserve}, "checks": checks, "conflict": conflict,
        "would_copy_if_execution_existed": would_copy, "mutation_performed": False,
        "recovery_contract": {"current_mode": "no-mutation", "rollback_required": False, "future_execution_requires_persistent_journal": True, "future_done_requires_postvalidation": True, "future_undo_must_verify_destination_unchanged": True}
    }
    return validate_preview_contract(preview)


def failure_matrix() -> list[dict[str, str]]:
    return [dict(item) for item in FAILURE_MATRIX]

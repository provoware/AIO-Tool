#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.version_registry import validate_registry

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
PROVEN_STATUSES = {"tested", "release-candidate", "released"}


def validate_release_evidence(row: dict[str, Any], registry_row: dict[str, Any]) -> dict[str, Any]:
    version = registry_row["version"]
    if not isinstance(row, dict) or row.get("schema_version") != 1 or row.get("version") != version:
        raise ValueError(f"Evidenzdatei ungültig für {version}.")
    if row.get("registry_commit") != registry_row.get("commit_sha"):
        raise ValueError(f"Registry-Commit driftet für {version}.")
    runs = row.get("ci_runs")
    if not isinstance(runs, list) or not runs or any(not isinstance(run, int) or run <= 0 for run in runs):
        raise ValueError(f"CI-Runs fehlen für {version}.")
    artifact = row.get("artifact")
    if not isinstance(artifact, dict) or artifact.get("status") not in {"recorded", "not-recorded"}:
        raise ValueError(f"Artefaktstatus ungültig für {version}.")
    if artifact["status"] == "recorded":
        if not isinstance(artifact.get("sha256"), str) or not SHA256_RE.fullmatch(artifact["sha256"]):
            raise ValueError(f"SHA256 fehlt/ist ungültig für {version}.")
    elif artifact.get("sha256") is not None:
        raise ValueError(f"Nicht aufgezeichneter Hash muss null sein: {version}.")
    matrix = row.get("browser_matrix")
    if not isinstance(matrix, dict) or matrix.get("status") not in {"passed", "not-recorded", "not-applicable"}:
        raise ValueError(f"Browsermatrix ungültig für {version}.")
    if registry_row.get("regression_status") == "passed-ci-cross-browser":
        if matrix.get("status") != "passed":
            raise ValueError(f"Cross-Browser-Evidenz fehlt für {version}.")
        for browser in ("chromium", "firefox"):
            item = matrix.get(browser)
            if not isinstance(item, dict) or item.get("status") != "passed" or not item.get("scenarios"):
                raise ValueError(f"Browser-Evidenz fehlt für {version}/{browser}.")
    gates = row.get("open_l4_gates")
    if not isinstance(gates, list) or any(not isinstance(item, str) or not item for item in gates):
        raise ValueError(f"open_l4_gates ungültig für {version}.")
    return row


def validate_evidence_index(index: dict[str, Any], registry: dict[str, Any], *, root: Path = ROOT) -> dict[str, Any]:
    if not isinstance(index, dict) or index.get("schema_version") != 1:
        raise ValueError("Evidenzindex-Schema muss 1 sein.")
    entries = index.get("entries")
    if not isinstance(entries, list):
        raise ValueError("Evidenzindex entries muss eine Liste sein.")
    expected = {item["version"]: item for item in registry["versions"] if item["status"] in PROVEN_STATUSES}
    indexed: dict[str, str] = {}
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("version"), str) or not isinstance(entry.get("file"), str):
            raise ValueError("Ungültiger Indexeintrag.")
        version = entry["version"]
        if version in indexed:
            raise ValueError(f"Doppelter Indexeintrag: {version}")
        file_path = entry["file"]
        if not file_path.startswith("evidence/releases/") or not file_path.endswith(".json"):
            raise ValueError(f"Ungültiger Evidenzpfad: {file_path}")
        indexed[version] = file_path
    if set(indexed) != set(expected):
        raise ValueError(f"Evidenzindex driftet. Fehlend={sorted(set(expected)-set(indexed))}, zusätzlich={sorted(set(indexed)-set(expected))}")
    for version, registry_row in expected.items():
        path = root / indexed[version]
        if not path.is_file():
            raise ValueError(f"Evidenzdatei fehlt: {indexed[version]}")
        row = json.loads(path.read_text(encoding="utf-8"))
        validate_release_evidence(row, registry_row)
    return index


def main() -> int:
    registry = validate_registry(json.loads((ROOT / "VERSION_REGISTRY.json").read_text(encoding="utf-8")))
    index = json.loads((ROOT / "evidence" / "RELEASE_EVIDENCE_INDEX.json").read_text(encoding="utf-8"))
    validate_evidence_index(index, registry)
    print(f"EVIDENCE GUARD PASS: {len(index['entries'])} bewiesene Versionen mit Einzeldatei indexiert")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

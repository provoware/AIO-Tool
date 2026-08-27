#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import VERSION
from app.version_registry import validate_registry
from scripts.release import status_label

DOCS_REQUIRING_CURRENT_VERSION = [
    "README.md",
    "TODO.md",
    "CHANGELOG.md",
    "MANIFEST.md",
    "REGRESSIONSINFOS.md",
    "LAIEN-ANLEITUNG.md",
    "TOOLBESCHREIBUNG.md",
]


def fail(message: str) -> None:
    raise SystemExit("DOCUMENTATION GUARD FEHLER: " + message)


def main() -> None:
    registry = validate_registry(json.loads((ROOT / "VERSION_REGISTRY.json").read_text(encoding="utf-8")))
    if registry["current_version"] != VERSION:
        fail("VERSION und VERSION_REGISTRY.json weichen voneinander ab.")
    current = next(item for item in registry["versions"] if item["version"] == VERSION)
    label = status_label(current)

    for rel in DOCS_REQUIRING_CURRENT_VERSION:
        path = ROOT / rel
        if not path.is_file():
            fail(f"Pflichtdokument fehlt: {rel}")
        text = path.read_text(encoding="utf-8")
        if VERSION not in text:
            fail(f"{rel} kennt die aktuelle Version {VERSION} nicht.")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    expected_artifact_marker = f"{VERSION}-{label}"
    if expected_artifact_marker not in readme:
        fail(f"README zeigt den Registry-Status nicht korrekt: erwartet {expected_artifact_marker}.")

    manifest = (ROOT / "MANIFEST.md").read_text(encoding="utf-8")
    if current["status"] not in manifest or current["release_status"] not in manifest:
        fail("MANIFEST zeigt aktuellen Versions-/Release-Status nicht an.")

    print(f"DOCUMENTATION GUARD PASS: {VERSION} / {current['status']} / {current['release_status']} / {label}")


if __name__ == "__main__":
    main()

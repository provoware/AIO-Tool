#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import VERSION
from app.version_registry import validate_registry
from scripts.evidence_guard import PROVEN_STATUSES, validate_evidence_index
from scripts.manifest_guard import load_and_validate
from scripts.release import status_label


def fail(message: str) -> None:
    raise SystemExit("DOCUMENTATION GUARD FEHLER: " + message)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _current_evidence(index: dict, version: str) -> dict | None:
    matches = [entry for entry in index["entries"] if entry["version"] == version]
    if not matches:
        return None
    if len(matches) != 1:
        fail(f"Evidenzindex kennt aktuelle Version nicht eindeutig: {version}")
    return _load_json(ROOT / matches[0]["file"])


def main() -> None:
    _, development = load_and_validate(root=ROOT)
    registry = validate_registry(_load_json(ROOT / "VERSION_REGISTRY.json"))
    if registry["current_version"] != VERSION:
        fail("VERSION und VERSION_REGISTRY.json weichen voneinander ab.")
    current = next(item for item in registry["versions"] if item["version"] == VERSION)
    label = status_label(current)

    index = _load_json(ROOT / "evidence" / "RELEASE_EVIDENCE_INDEX.json")
    validate_evidence_index(index, registry, root=ROOT)
    evidence = _current_evidence(index, VERSION)
    proven = current["status"] in PROVEN_STATUSES
    if proven and evidence is None:
        fail(f"Bewiesene Version ohne Einzelevidenz: {VERSION}")
    if not proven and evidence is not None:
        fail(f"Development-Version darf keine vorweggenommene Release-Evidenz beanspruchen: {VERSION}")

    status_docs = development["status_documents"]
    evidence_docs = development["evidence_summary_documents"]
    texts: dict[str, str] = {}
    for rel in status_docs:
        path = ROOT / rel
        if not path.is_file():
            fail(f"Pflichtdokument fehlt: {rel}")
        text = path.read_text(encoding="utf-8")
        texts[rel] = text
        if VERSION not in text:
            fail(f"{rel} kennt die aktuelle Version {VERSION} nicht.")

    readme = texts["README.md"]
    expected_artifact_marker = f"{VERSION}-{label}"
    if expected_artifact_marker not in readme:
        fail(f"README zeigt den Registry-Status nicht korrekt: erwartet {expected_artifact_marker}.")

    manifest = texts["MANIFEST.md"]
    if current["status"] not in manifest or current["release_status"] not in manifest:
        fail("MANIFEST zeigt aktuellen Versions-/Release-Status nicht an.")

    if proven and evidence is not None:
        artifact = evidence.get("artifact", {})
        digest = artifact.get("sha256") if artifact.get("status") == "recorded" else None
        main_commit = evidence.get("main_commit")
        if digest:
            for rel in evidence_docs:
                if digest not in texts[rel]:
                    fail(f"{rel} enthält nicht den kanonischen Runtime-SHA256 aus Release-Evidenz.")
        if main_commit:
            for rel in evidence_docs:
                if main_commit not in texts[rel]:
                    fail(f"{rel} enthält nicht den kanonischen Runtime-Baseline-Commit aus Release-Evidenz.")

    for rel in ("README.md", "MANIFEST.md", "TOOLBESCHREIBUNG.md"):
        if "Runtime-Baseline" not in texts[rel]:
            fail(f"{rel} trennt Runtime-Baseline und Repository-Metadaten nicht ausdrücklich.")

    # Native L4 bleibt eine reale Feldbeobachtung. Development-Versionen dürfen
    # sie niemals aus CI als bestanden ableiten.
    for rel in status_docs:
        upper = texts[rel].upper()
        if "L4" not in upper or "OFFEN" not in upper:
            fail(f"{rel} muss die reale L4-Grenze ausdrücklich als OFFEN kennzeichnen.")
    progress = re.search(r"Native Kubuntu L4[^\n]*?(\d+)\s*%", readme, re.IGNORECASE)
    if progress and int(progress.group(1)) != 0:
        fail("README darf für vollständig offene Native-L4-Schritte keinen Fortschritt > 0 % anzeigen.")

    print(f"DOCUMENTATION GUARD PASS: {VERSION} / {current['status']} / {current['release_status']} / {label} / evidence-policy-consistent")


if __name__ == "__main__":
    main()

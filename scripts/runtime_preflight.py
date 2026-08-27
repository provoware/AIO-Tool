#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))

from app import ROOT_DIR, VERSION
from app.config import ConfigStore, DEFAULT_CONFIG
from app.error_advisor import ErrorAdvisor
from app.loopback_security import allowed_local_request
from app.native_acceptance import NativeAcceptanceStore, STEPS
from app.safe_file_sim import build_preview
from app.server import WEB_DIR, allowed_host, allowed_origin
from app.version_registry import validate_registry

MANIFEST_PATH = ROOT_DIR / "manifests" / "RUNTIME_MANIFEST.json"


def check(condition: bool, label: str) -> None:
    if not condition: raise SystemExit(f"FEHLER: {label}")
    print(f"OK: {label}")


def load_manifest() -> dict:
    try: data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc: raise SystemExit("FEHLER: Runtime-Manifest ist nicht lesbar.") from exc
    if data.get("schema_version") != 1 or not isinstance(data.get("files"), list): raise SystemExit("FEHLER: Runtime-Manifest hat ein unbekanntes Schema.")
    files = data["files"]
    if len(files) != len(set(files)) or not all(isinstance(item, str) and item for item in files): raise SystemExit("FEHLER: Runtime-Manifest enthält ungültige oder doppelte Dateipfade.")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Sichere Runtime-Vorprüfung"); parser.add_argument("--quick", action="store_true", help="kompakte Startprüfung"); parser.parse_args()
    manifest = load_manifest()
    for rel in manifest["files"]: check((ROOT_DIR / rel).is_file(), f"Basisdatei {rel} vorhanden")
    check(bool(VERSION), "Version vorhanden")
    registry = validate_registry(json.loads((ROOT_DIR / "VERSION_REGISTRY.json").read_text(encoding="utf-8"))); check(registry["current_version"] == VERSION, "VERSION und Registry stimmen überein")
    check(WEB_DIR.is_dir(), "Weboberfläche vorhanden"); check(allowed_host("127.0.0.1:8765", 8765), "Loopback-Host erlaubt"); check(not allowed_host("example.com", 8765), "Fremdhost blockiert"); check(allowed_origin("http://127.0.0.1:8765", 8765), "lokale Origin erlaubt"); check(not allowed_origin("https://example.com", 8765), "fremde Origin blockiert")
    check(allowed_local_request("127.0.0.1:8778", "http://127.0.0.1:8778", 8778), "Native Runner gleicher Loopback-Port erlaubt"); check(not allowed_local_request("127.0.0.1:8778", "http://127.0.0.1:9999", 8778), "Native Runner Cross-Port blockiert")
    advisor = ErrorAdvisor(); check(advisor.metadata()["rule_count"] >= 1, "Fehlerhilfe und Referenzvorlagen lesbar")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp); store = ConfigStore(root / "config.json"); saved = store.save(DEFAULT_CONFIG); check(store.load() == saved, "atomare Konfiguration funktioniert")
        native = NativeAcceptanceStore(root / "native.json", VERSION); check(native.report()["counts"]["pending"] == len(STEPS) == 18, "Native Acceptance startet mit 18 offenen Schritten")
        source = root / "source.txt"; source.write_text("preview", encoding="utf-8"); target = root / "target"; target.mkdir(); preview = build_preview(source, target, free_bytes=100 * 1024 * 1024); check(preview["simulation_only"] is True and preview["execution_enabled"] is False and preview["mutation_performed"] is False, "SAFE-FILE-Runtime bleibt reine Simulation")
    print("RUNTIME PREFLIGHT PASS")


if __name__ == "__main__": main()

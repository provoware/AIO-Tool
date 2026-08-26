#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from app import ROOT_DIR, VERSION
from app.config import ConfigStore, DEFAULT_CONFIG
from app.server import WEB_DIR, allowed_host, allowed_origin

REQUIRED = [
    "README.md", "TODO.md", "AGENTS.md", "CHANGELOG.md", "LAIEN-ANLEITUNG.md",
    "TOOLBESCHREIBUNG.md", "MANIFEST.md", "REGRESSIONSINFOS.md", "VERSION",
    "start_tool.sh", "app/config.py", "app/server.py", "web/index.html", "web/app.js", "web/styles.css",
]


def check(condition: bool, label: str) -> None:
    if not condition:
        raise SystemExit(f"FEHLER: {label}")
    print(f"OK: {label}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="Kurze Startprüfung")
    args = parser.parse_args()

    check(bool(VERSION), "Version vorhanden")
    for rel in REQUIRED:
        check((ROOT_DIR / rel).is_file(), f"{rel} vorhanden")
    check(WEB_DIR.is_dir(), "Web-Verzeichnis vorhanden")
    check(allowed_host("127.0.0.1:8765", 8765), "Loopback-Host erlaubt")
    check(not allowed_host("example.com", 8765), "Fremdhost blockiert")
    check(allowed_origin("http://127.0.0.1:8765", 8765), "lokale Origin erlaubt")
    check(not allowed_origin("https://example.com", 8765), "fremde Origin blockiert")

    with tempfile.TemporaryDirectory() as tmp:
        store = ConfigStore(Path(tmp) / "config.json")
        saved = store.save(DEFAULT_CONFIG)
        loaded = store.load()
        check(saved == loaded, "Konfiguration atomar speichern/laden")
        json.loads((Path(tmp) / "config.json").read_text(encoding="utf-8"))

    if not args.quick:
        check((ROOT_DIR / "tests").is_dir(), "Test-Verzeichnis vorhanden")
        check((ROOT_DIR / "scripts" / "release.py").is_file(), "Release-Builder vorhanden")

    print("VALIDATION PASS")


if __name__ == "__main__":
    main()

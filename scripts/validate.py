#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import ROOT_DIR, VERSION
from app.config import ConfigStore, DEFAULT_CONFIG
from app.event_registry import EventRegistry
from app.server import WEB_DIR, allowed_host, allowed_origin
from app.todo_store import TodoStore
from app.version_registry import VersionRegistry, validate_registry

REQUIRED = [
    "README.md", "TODO.md", "AGENTS.md", "CHANGELOG.md", "LAIEN-ANLEITUNG.md",
    "TOOLBESCHREIBUNG.md", "MANIFEST.md", "REGRESSIONSINFOS.md", "VERSION", "VERSION_REGISTRY.json",
    "start_tool.sh", "app/config.py", "app/persistence.py", "app/version_registry.py",
    "app/event_registry.py", "app/todo_store.py", "app/server.py",
    "web/index.html", "web/app.js", "web/styles.css",
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

    tracked_registry = validate_registry(
        json.loads((ROOT_DIR / "VERSION_REGISTRY.json").read_text(encoding="utf-8"))
    )
    check(tracked_registry["current_version"] == VERSION, "VERSION und getrackte Registry stimmen überein")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        config = ConfigStore(root / "config.json")
        saved = config.save(DEFAULT_CONFIG)
        loaded = config.load()
        check(saved == loaded, "Konfiguration atomar speichern/laden")
        json.loads((root / "config.json").read_text(encoding="utf-8"))

        versions = VersionRegistry(root / "versions.json", default=tracked_registry)
        check(versions.consistency(VERSION)["ok"], "Versions-Registry konsistent")
        check(len(versions.load()["versions"]) >= 3, "Versionshistorie auf frischer Runtime vorhanden")

        events = EventRegistry(root / "events.json")
        events.add(kind="validation", area="System", message="Validierung wurde ausgeführt.")
        check(len(events.latest(1)) == 1, "EventRegistry speichern/lesen")

        todos = TodoStore(root / "todos.json")
        item = todos.create(title="Validierung prüfen")
        check(todos.title_suggestions(1)[0]["title"] == "Validierung prüfen", "TODO-Titel merken")
        todos.complete(item["id"])
        check(len(todos.list_archive()) == 1, "TODO ins Erledigt-Archiv verschieben")

    if not args.quick:
        check((ROOT_DIR / "tests").is_dir(), "Test-Verzeichnis vorhanden")
        check((ROOT_DIR / "scripts" / "release.py").is_file(), "Release-Builder vorhanden")

    print("VALIDATION PASS")


if __name__ == "__main__":
    main()

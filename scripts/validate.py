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
from app.calendar_store import CalendarStore, validate_calendar
from app.config import ConfigStore, DEFAULT_CONFIG, validate_config
from app.error_advisor import ErrorAdvisor
from app.event_registry import EventRegistry, validate_events
from app.learning_memory import active_entries, load_jsonl
from app.server import WEB_DIR, allowed_host, allowed_origin
from app.todo_store import TodoStore, validate_todos
from app.version_registry import VersionRegistry, validate_registry

REQUIRED = [
    "README.md", "TODO.md", "AGENTS.md", "CHANGELOG.md", "LAIEN-ANLEITUNG.md",
    "TOOLBESCHREIBUNG.md", "MANIFEST.md", "REGRESSIONSINFOS.md", "VERSION", "VERSION_REGISTRY.json",
    "LEARNING_MEMORY.jsonl", "start_tool.sh",
    "app/config.py", "app/persistence.py", "app/version_registry.py", "app/event_registry.py", "app/todo_store.py",
    "app/calendar_store.py", "app/text_catalog.py", "app/error_advisor.py", "app/learning_memory.py", "app/server.py",
    "resources/texts/de/v1.json", "resources/error_rules/v1.json", "resources/templates/README.md",
    "resources/templates/config/config.v1.example.json",
    "resources/templates/version_registry/version_registry.v1.example.json",
    "resources/templates/events/events.v1.example.json",
    "resources/templates/todos/todos.v1.example.json",
    "resources/templates/calendar/calendar.v1.example.json",
    "scripts/learning_guard.py", "web/index.html", "web/app.js", "web/styles.css", "web/dashboard-texts.de.v1.json",
    "tests/test_dashboard_contract.py",
    "testdata/valid/config.v1.json", "testdata/valid/version_registry.v1.json",
    "testdata/valid/events.v1.json", "testdata/valid/todos.v1.json", "testdata/valid/calendar.v1.json",
    "testdata/invalid/config.invalid-theme.v1.json", "testdata/invalid/config.corrupt-json.txt",
    "testdata/invalid/version_registry.duplicate.v1.json", "testdata/invalid/events.empty-message.v1.json",
    "testdata/invalid/todos.duplicate-title-memory.v1.json",
    "testdata/invalid/calendar.end-before-start.v1.json",
    "testdata/invalid/calendar.reminder-without-time.v1.json",
]


def check(condition: bool, label: str) -> None:
    if not condition:
        raise SystemExit(f"FEHLER: {label}")
    print(f"OK: {label}")


def load_json(rel: str) -> dict:
    return json.loads((ROOT_DIR / rel).read_text(encoding="utf-8"))


def validate_dashboard_contract() -> None:
    dashboard_texts = load_json("web/dashboard-texts.de.v1.json")
    check(dashboard_texts.get("schema_version") == 1, "Dashboard-Textschema bekannt")
    check(dashboard_texts.get("language") == "de", "Dashboard-Texte deutsch")
    check(isinstance(dashboard_texts.get("catalog_version"), str) and bool(dashboard_texts["catalog_version"].strip()), "Dashboard-Textkatalog versioniert")
    messages = dashboard_texts.get("messages")
    check(isinstance(messages, dict) and len(messages) >= 60, "Dashboard-Textkatalog ausreichend befüllt")
    check(all(isinstance(value, str) and value.strip() for value in messages.values()), "Dashboard-Texte nicht leer")

    html = (ROOT_DIR / "web" / "index.html").read_text(encoding="utf-8")
    js = (ROOT_DIR / "web" / "app.js").read_text(encoding="utf-8")
    for element_id in ("monthGrid", "todoList", "eventList", "reminderRegion", "systemSummary", "developerPanel", "settingsPanel"):
        check(f'id="{element_id}"' in html, f"Dashboard-Bereich {element_id} vorhanden")
    for endpoint in ("/api/status", "/api/todos", "/api/events?limit=5", "/api/calendar?view=month", "/api/calendar/reminders/due"):
        check(endpoint in js, f"Dashboard nutzt getestete API {endpoint}")
    check("document.visibilityState!=='visible'" in js, "Reminder werden im unsichtbaren Tab nicht quittiert")
    check("button.addEventListener('click',()=>ackReminder" in js, "Reminder-Quittierung verlangt sichtbare Nutzeraktion")


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

    tracked_registry = validate_registry(load_json("VERSION_REGISTRY.json"))
    check(tracked_registry["current_version"] == VERSION, "VERSION und getrackte Registry stimmen überein")

    advisor = ErrorAdvisor()
    help_meta = advisor.metadata()
    declared_rules = load_json("resources/error_rules/v1.json")["rules_version"]
    declared_texts = load_json("resources/texts/de/v1.json")["catalog_version"]
    check(help_meta["rule_count"] >= 8, "versionierte Fehlerregeln inkl. Kalender geladen")
    check(help_meta["rules_version"] == declared_rules, "Fehlerregeln-Metadaten entsprechen ihrer Quelldatei")
    check(help_meta["text_catalog"]["catalog_version"] == declared_texts, "Textkatalog-Metadaten entsprechen ihrer Quelldatei")
    check(help_meta["text_catalog"]["language"] == "de", "deutscher Core-Textkatalog geladen")

    learnings = load_jsonl(ROOT_DIR / "LEARNING_MEMORY.jsonl")
    check(len(active_entries(learnings)) >= 9, "Entwicklungs-Lerngedächtnis inkl. Metadatenregel validiert")

    validate_config(load_json("resources/templates/config/config.v1.example.json"))
    validate_registry(load_json("resources/templates/version_registry/version_registry.v1.example.json"))
    validate_events(load_json("resources/templates/events/events.v1.example.json"))
    validate_todos(load_json("resources/templates/todos/todos.v1.example.json"))
    validate_calendar(load_json("resources/templates/calendar/calendar.v1.example.json"))
    print("OK: versionierte Mustervorlagen entsprechen den Produktvalidatoren")

    validate_dashboard_contract()

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        config = ConfigStore(root / "config.json")
        saved = config.save(DEFAULT_CONFIG)
        loaded = config.load()
        check(saved == loaded, "Konfiguration atomar speichern/laden")
        json.loads((root / "config.json").read_text(encoding="utf-8"))

        versions = VersionRegistry(root / "versions.json", default=tracked_registry)
        check(versions.consistency(VERSION)["ok"], "Versions-Registry konsistent")
        check(len(versions.load()["versions"]) >= 5, "Versionshistorie auf frischer Runtime vorhanden")

        events = EventRegistry(root / "events.json")
        events.add(kind="validation", area="System", message="Validierung wurde ausgeführt.")
        check(len(events.latest(1)) == 1, "EventRegistry speichern/lesen")

        todos = TodoStore(root / "todos.json")
        item = todos.create(title="Validierung prüfen")
        check(todos.title_suggestions(1)[0]["title"] == "Validierung prüfen", "TODO-Titel merken")
        todos.complete(item["id"])
        check(len(todos.list_archive()) == 1, "TODO ins Erledigt-Archiv verschieben")

        calendar_store = CalendarStore(root / "calendar.json")
        appointment = calendar_store.create(
            title="Kalender prüfen",
            date="2026-08-27",
            start_time="10:00",
            reminders=[10],
        )
        check(calendar_store.get(appointment["id"])["title"] == "Kalender prüfen", "Kalendertermin persistent speichern")
        check(calendar_store.period("month", "2026-08-15")["end"] == "2026-08-31", "Kalender-Monatsperiode korrekt")
        check(calendar_store.title_suggestions(1)[0]["title"] == "Kalender prüfen", "Kalendertitel merken")

    if not args.quick:
        check((ROOT_DIR / "tests").is_dir(), "Test-Verzeichnis vorhanden")
        check((ROOT_DIR / "scripts" / "release.py").is_file(), "Release-Builder vorhanden")

    print("VALIDATION PASS")


if __name__ == "__main__":
    main()

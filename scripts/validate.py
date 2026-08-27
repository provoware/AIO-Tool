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
from app.config import ConfigStore, DEFAULT_CONFIG, THEMES, validate_config
from app.error_advisor import ErrorAdvisor
from app.event_registry import EventRegistry, validate_events
from app.instance_identity import UI_CONTRACT_VERSION
from app.learning_memory import active_entries, load_jsonl
from app.loopback_security import allowed_local_request
from app.native_acceptance import NativeAcceptanceStore, STEPS, validate_session
from app.safe_file_sim import build_preview, validate_preview_contract
from app.server import WEB_DIR, allowed_host, allowed_origin
from app.todo_store import TodoStore, validate_todos
from app.version_registry import VersionRegistry, validate_registry
from scripts.evidence_guard import validate_evidence_index
from scripts.manifest_guard import load_and_validate as validate_manifest_pair

REQUIRED = [
    "README.md", "TODO.md", "AGENTS.md", "CHANGELOG.md", "LAIEN-ANLEITUNG.md", "TOOLBESCHREIBUNG.md", "MANIFEST.md", "REGRESSIONSINFOS.md", "VERSION", "VERSION_REGISTRY.json", "LEARNING_MEMORY.jsonl",
    "start_tool.sh", "start_tool.desktop", "start_native_acceptance.sh", "native_acceptance.desktop", "start_safe_file_simulation.sh", "safe_file_simulation.desktop",
    "app/config.py", "app/persistence.py", "app/version_registry.py", "app/event_registry.py", "app/todo_store.py", "app/calendar_store.py", "app/text_catalog.py", "app/error_advisor.py", "app/learning_memory.py", "app/loopback_security.py", "app/native_acceptance.py", "app/safe_file_sim.py", "app/server.py",
    "resources/texts/de/v1.json", "resources/error_rules/v1.json", "resources/templates/README.md", "resources/templates/config/config.v1.example.json", "resources/templates/version_registry/version_registry.v1.example.json", "resources/templates/events/events.v1.example.json", "resources/templates/todos/todos.v1.example.json", "resources/templates/calendar/calendar.v1.example.json", "resources/templates/native_acceptance/native_acceptance.v1.example.json", "resources/templates/safe_file_sim/safe_file_preview.v1.example.json",
    "scripts/learning_guard.py", "scripts/manifest_guard.py", "scripts/evidence_guard.py", "scripts/documentation_guard.py", "scripts/runtime_preflight.py", "scripts/native_acceptance_runner.py", "scripts/safe_file_simulator.py", "scripts/aux_ui_acceptance.py",
    "web/index.html", "web/app.js", "web/styles.css", "web/acceptance.css", "web/helper-ui.css", "web/dashboard-texts.de.v1.json", "web/native-acceptance.html", "web/native-acceptance.js", "web/safe-file-sim.html", "web/safe-file-sim.js",
    "evidence/RELEASE_EVIDENCE_INDEX.json", "evidence/releases/0.4.3-integrity-hardening.json", "tests/test_dashboard_contract.py", "tests/test_helper_ui_contract.py", "tests/test_native_acceptance.py", "tests/test_safe_file_sim.py", "tests/test_safe_file_simulator_contract.py", "tests/test_evidence_index.py", "tests/test_manifest_guard.py", "tests/test_loopback_security.py",
    "testdata/valid/config.v1.json", "testdata/valid/version_registry.v1.json", "testdata/valid/events.v1.json", "testdata/valid/todos.v1.json", "testdata/valid/calendar.v1.json", "testdata/invalid/config.invalid-theme.v1.json", "testdata/invalid/config.corrupt-json.txt", "testdata/invalid/version_registry.duplicate.v1.json", "testdata/invalid/events.empty-message.v1.json", "testdata/invalid/todos.duplicate-title-memory.v1.json", "testdata/invalid/calendar.end-before-start.v1.json", "testdata/invalid/calendar.reminder-without-time.v1.json", "testdata/native_acceptance/invalid_status.json", "testdata/safe_file_sim/invalid_preview.json",
    "manifests/RUNTIME_MANIFEST.json", "manifests/DEVELOPMENT_MANIFEST.json", "manifests/README.md",
]


def check(condition, label):
    if not condition:
        raise SystemExit(f"FEHLER: {label}")
    print(f"OK: {label}")


def load_json(rel):
    return json.loads((ROOT_DIR / rel).read_text(encoding="utf-8"))


def validate_dashboard_contract():
    dashboard_texts = load_json("web/dashboard-texts.de.v1.json")
    check(dashboard_texts.get("schema_version") == 1, "Dashboard-Textschema bekannt")
    check(dashboard_texts.get("language") == "de", "Dashboard-Texte deutsch")
    check(isinstance(dashboard_texts.get("catalog_version"), str) and bool(dashboard_texts["catalog_version"].strip()), "Dashboard-Textkatalog versioniert")
    messages = dashboard_texts.get("messages")
    check(isinstance(messages, dict) and len(messages) >= 60, "Dashboard-Textkatalog ausreichend befüllt")
    check(all(isinstance(v, str) and v.strip() for v in messages.values()), "Dashboard-Texte nicht leer")

    html = (ROOT_DIR / "web" / "index.html").read_text(encoding="utf-8")
    js = (ROOT_DIR / "web" / "app.js").read_text(encoding="utf-8")
    css = (ROOT_DIR / "web" / "styles.css").read_text(encoding="utf-8")
    for element_id in ("monthGrid", "todoList", "eventList", "reminderRegion", "systemSummary", "developerPanel", "settingsPanel", "bootGuard"):
        check(f'id="{element_id}"' in html, f"Dashboard-Bereich {element_id} vorhanden")
    for endpoint in ("/api/status", "/api/todos", "/api/events?limit=5", "/api/calendar?view=month", "/api/calendar/reminders/due"):
        check(endpoint in js, f"Dashboard nutzt getestete API {endpoint}")
    check(UI_CONTRACT_VERSION in html, "UI-Vertrag entspricht Runtime-Vertrag")
    check(THEMES == {"aurora-glass", "trash-neon", "steel-night", "clean-light", "high-contrast"}, "Theme-Vertrag vollständig")
    check(all(f'data-theme="{theme}"' in html for theme in THEMES), "Alle Themes im Auswahldialog vorhanden")
    check("innerHTML" not in js, "Dashboard baut dynamische Inhalte ohne innerHTML")
    check("boot().catch" in js, "Bootfehler werden sichtbar abgefangen")
    check("state.calendar=result?.calendar||null" in js, "Kalenderfehler können keine Altanzeige wiederverwenden")
    check("prefers-reduced-motion:reduce" in css, "Bewegungsreduktion respektiert")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()
    check(bool(VERSION), "Version vorhanden")

    for rel in REQUIRED:
        check((ROOT_DIR / rel).is_file(), f"{rel} vorhanden")

    validate_manifest_pair(root=ROOT_DIR)
    print("OK: Runtime-/Development-Manifest konsistent")

    check(WEB_DIR.is_dir(), "Web-Verzeichnis vorhanden")
    check(allowed_host("127.0.0.1:8765", 8765), "Loopback-Host mit exaktem Port erlaubt")
    check(not allowed_host("127.0.0.1", 8765), "Loopback-Host ohne Port blockiert")
    check(not allowed_host("example.com", 8765), "Fremdhost blockiert")
    check(allowed_origin("http://127.0.0.1:8765", 8765), "lokale Origin erlaubt")
    check(not allowed_origin("http://127.0.0.1:9999", 8765), "Cross-Port-Origin blockiert")
    check(allowed_local_request("127.0.0.1:8778", "http://127.0.0.1:8778", 8778), "Hilfsserver erlaubt identischen Loopback-Port")
    check(not allowed_local_request("127.0.0.1:8778", "http://127.0.0.1:9999", 8778), "Hilfsserver blockiert Cross-Port-Origin")

    tracked = validate_registry(load_json("VERSION_REGISTRY.json"))
    check(tracked["current_version"] == VERSION, "VERSION und Registry stimmen überein")
    validate_evidence_index(load_json("evidence/RELEASE_EVIDENCE_INDEX.json"), tracked, root=ROOT_DIR)
    print("OK: Release-Evidenzindex konsistent")

    advisor = ErrorAdvisor()
    meta = advisor.metadata()
    check(meta["rules_version"] == load_json("resources/error_rules/v1.json")["rules_version"], "Fehlerregeln-Metadaten konsistent")
    check(meta["text_catalog"]["catalog_version"] == load_json("resources/texts/de/v1.json")["catalog_version"], "Textkatalog-Metadaten konsistent")
    check(len(active_entries(load_jsonl(ROOT_DIR / "LEARNING_MEMORY.jsonl"))) >= 20, "Entwicklungs-Lerngedächtnis validiert")

    validate_config(load_json("resources/templates/config/config.v1.example.json"))
    validate_registry(load_json("resources/templates/version_registry/version_registry.v1.example.json"))
    validate_events(load_json("resources/templates/events/events.v1.example.json"))
    validate_todos(load_json("resources/templates/todos/todos.v1.example.json"))
    validate_calendar(load_json("resources/templates/calendar/calendar.v1.example.json"))
    validate_session(load_json("resources/templates/native_acceptance/native_acceptance.v1.example.json"))
    validate_preview_contract(load_json("resources/templates/safe_file_sim/safe_file_preview.v1.example.json"))
    print("OK: Mustervorlagen entsprechen Produktvalidatoren")
    validate_dashboard_contract()

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        config = ConfigStore(root / "config.json")
        saved = config.save(DEFAULT_CONFIG)
        check(saved == config.load(), "Konfiguration atomar speichern/laden")
        versions = VersionRegistry(root / "versions.json", default=tracked)
        check(versions.consistency(VERSION)["ok"], "Versions-Registry konsistent")
        events = EventRegistry(root / "events.json")
        events.add(kind="validation", area="System", message="Validierung wurde ausgeführt.")
        check(len(events.latest(1)) == 1, "EventRegistry speichern/lesen")
        todos = TodoStore(root / "todos.json")
        item = todos.create(title="Validierung prüfen")
        todos.complete(item["id"])
        check(len(todos.list_archive()) == 1, "TODO archivieren")
        calendar = CalendarStore(root / "calendar.json")
        appointment = calendar.create(title="Kalender prüfen", date="2026-08-27", start_time="10:00", reminders=[10])
        check(calendar.get(appointment["id"])["title"] == "Kalender prüfen", "Kalender persistent")
        native = NativeAcceptanceStore(root / "native.json", VERSION)
        check(native.report()["counts"]["pending"] == len(STEPS) == 18, "Native Acceptance startet offen")
        source = root / "source.txt"
        source.write_text("preview", encoding="utf-8")
        target = root / "target"
        target.mkdir()
        preview = build_preview(source, target, free_bytes=100 * 1024 * 1024)
        check(preview["execution_enabled"] is False and preview["mutation_performed"] is False, "SAFE-FILE mutationsfrei")

    if not args.quick:
        check((ROOT_DIR / "tests").is_dir(), "Test-Verzeichnis vorhanden")
        check((ROOT_DIR / "scripts" / "release.py").is_file(), "Release-Builder vorhanden")
    print("VALIDATION PASS")


if __name__ == "__main__":
    main()

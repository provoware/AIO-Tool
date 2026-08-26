# MANIFEST

## Projekt

- **Name:** AIO-Tool
- **Repository:** `provoware/AIO-Tool`
- **Phase:** P1 — Robustheits- und Datenkern
- **Version:** `0.2.1-robustness`
- **Stand:** 2026-08-27

## Verbindlicher Projektbestand

### Root

`README.md`, `TODO.md`, `AGENTS.md`, `CHANGELOG.md`, `LAIEN-ANLEITUNG.md`, `TOOLBESCHREIBUNG.md`, `MANIFEST.md`, `REGRESSIONSINFOS.md`, `VERSION`, `VERSION_REGISTRY.json`, `LEARNING_MEMORY.jsonl`, `start_tool.sh`, `start_tool.desktop`, `.gitignore`.

### Anwendung

- `app/config.py` — validierte Config-Persistenz.
- `app/persistence.py` — atomarer JSON-Speicher.
- `app/version_registry.py` — Versionen/Evidenz/Drift.
- `app/event_registry.py` — menschenlesbare Ereignisse.
- `app/todo_store.py` — TODOs/Titelgedächtnis/Archiv.
- `app/text_catalog.py` — versionierte Nutztexte.
- `app/error_advisor.py` — regelbasierte Fehlerhilfe.
- `app/learning_memory.py` — validiertes Entwicklungs-Lerngedächtnis.
- `app/server.py` — Loopback-HTTP/API.
- `web/` — Browser-Dashboard-Shell.

### Ressourcen

- `resources/texts/de/v1.json` — deutscher Textkatalog, Katalogversion 1.0.0.
- `resources/error_rules/v1.json` — Fehlerregeln, Regelversion 1.0.0.
- `resources/templates/` — geprüfte Config-/Registry-/Event-/TODO-Referenzen.

### Testdaten

- `testdata/valid/` — muss von den Produktvalidatoren akzeptiert werden.
- `testdata/invalid/` — muss für die jeweils dokumentierte Fehlerklasse abgelehnt werden.
- Testdaten werden niemals automatisch nach `runtime/` kopiert.

### Qualität / Release

- bestehende Config/Server/Persistenz/Registry/Event/TODO-Tests.
- `tests/test_text_catalog.py`.
- `tests/test_error_advisor.py`.
- `tests/test_learning_memory.py`.
- `tests/test_templates.py`.
- erweiterte `tests/test_core_api.py`.
- `scripts/validate.py`.
- `scripts/learning_guard.py`.
- `scripts/release.py`.
- `.github/workflows/foundation-ci.yml`.

## Laufzeitvoraussetzungen

Linux/Kubuntu primär, Python 3.12 angestrebt, nur Standardbibliothek, `python3-venv`, lokaler Browser. Keine externen Python-/JS-Pakete, keine CDN-/Remote-Font-Abhängigkeiten.

## Persistenz

Lokale Nutzerdaten bleiben unter `runtime/` und sind aus Git/Release ausgeschlossen. Atomare Hauptdatei + Backup-Fallback gilt für neue Domänenmodelle.

Aktuelle persistente Schemata:

- VersionRegistry: 1
- EventRegistry: 1
- TODO-Core: 1
- Textkatalog: 1
- Fehlerregeln: 1
- Learning Memory: 1 pro JSONL-Eintrag

Schemaänderung benötigt Validator, Vorlage, Testdaten und Regression/Migration gemeinsam.

## Fehlerhilfe-Vertrag

Fehlerantworten können liefern: `rule_id`, Kategorie, Schweregrad/Ampel, verständliche Meldung, sichere Handlung, optional `template_path`, `retry_safe` und Bereich.

Mustervorlagen sind reine Referenzen. Keine Regel darf sie ohne ausdrückliche Aktion über echte Nutzerdaten schreiben.

## Learning-Memory-Vertrag

`LEARNING_MEMORY.jsonl` enthält Entwicklungslektionen, keine Nutzerdaten. CI prüft eindeutige IDs, Schema, Pflichtfelder und aktive Regeln. Bestätigte strukturelle Fehler sollen eine dauerhafte Lektion und Regression erzeugen.

## Netzwerk

Backend ausschließlich `127.0.0.1`, Standardport 8765, kein Internetzwang, keine Telemetrie, Host-/Origin-Guard, keine CORS-Freigabe.

## Release-Ausschlüsse

`.venv/`, `runtime/*` außer `.gitkeep`, `__pycache__`, Testcache, `dist/`, `build/`, Logs, lokale Profile/Pfade, reale TODO-/Event-/spätere Kalender-/Recovery-Daten, Secrets/PINs/Passwörter.

**Nicht ausgeschlossen** werden dokumentierte `resources/templates/`, `testdata/` und Tests: sie sind Teil des vollständigen Entwicklungs-/Releaseprojekts und enthalten ausschließlich künstliche Beispieldaten.

## Testkommandos

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate.py
python3 scripts/learning_guard.py
bash -n start_tool.sh
node --check web/app.js
python3 scripts/release.py --check
```

GitHub Actions lädt nach grünem Build das vollständige Release-ZIP als Artefakt hoch.

## Status

`0.2.1-robustness` ist automatisiert **GEPRÜFT** durch Run `33024919165`, bleibt jedoch `draft`. Reale Kubuntu-/Browser-/Zoom-Gates sind weiterhin offen.

## Nächster Manifest-Schritt

`0.3.0-calendar-core`: `app/calendar_store.py`, Kalender-Mustervorlage/Testdaten, Termin-/Reminder-Datenvertrag, Monats-/Wochen-/Jahresperioden, Kalender-API, Tests und optionale TODO-Verknüpfung.

# MANIFEST

## Projekt

- **Name:** AIO-Tool
- **Repository:** `provoware/AIO-Tool`
- **Phase:** P1 — Kalender-/Organisationskern
- **Version:** `0.3.0-calendar-core`
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
- `app/calendar_store.py` — persistente Kalendertermine, Perioden, Titelgedächtnis und Reminder-Quittierung.
- `app/text_catalog.py` — versionierte Nutztexte.
- `app/error_advisor.py` — regelbasierte Fehlerhilfe.
- `app/learning_memory.py` — validiertes Entwicklungs-Lerngedächtnis.
- `app/server.py` — Loopback-HTTP/API inkl. Kalenderendpunkte.
- `web/` — Browser-Dashboard-Shell; Dashboard V2 folgt als eigener UI-Slice.

### Ressourcen

- `resources/texts/de/v1.json` — deutscher Textkatalog, Katalogversion `1.1.0`.
- `resources/error_rules/v1.json` — Fehlerregeln, Regelversion `1.1.0`.
- `resources/templates/config/` — Config-Referenz.
- `resources/templates/version_registry/` — Registry-Referenz.
- `resources/templates/events/` — Event-Referenz.
- `resources/templates/todos/` — TODO-Referenz.
- `resources/templates/calendar/` — Kalender-Referenz.

### Testdaten

- `testdata/valid/` — muss von den jeweiligen Produktvalidatoren akzeptiert werden.
- `testdata/invalid/` — muss für die jeweils dokumentierte Fehlerklasse abgelehnt werden.
- Kalender-Negativfälle umfassen mindestens Ende vor Beginn und Reminder ohne Startzeit.
- Testdaten werden niemals automatisch nach `runtime/` kopiert.

### Qualität / Release

Zusätzlich zu den bisherigen Tests gehören zum aktuellen Gate:

- `tests/test_calendar_store.py` — Persistenz, Perioden, Titelgedächtnis, Reminder und DST.
- `tests/test_calendar_api.py` — HTTP-Vertrag, TODO-Link, Reminder-Abfrage/Quittierung.
- `tests/test_templates.py` — Kalender-Muster-/Negativdaten inklusive.
- `tests/test_error_advisor.py` — Kalender-Fehlerhilfe inklusive.
- `tests/test_core_api.py` — Metadaten-/Core-Vertrag ohne redundante Versionskonstanten.
- `scripts/validate.py` — Foundation-/Core-/Kalender-Vorprüfung.
- `scripts/learning_guard.py`.
- `scripts/release.py`.
- `.github/workflows/foundation-ci.yml`.

## Laufzeitvoraussetzungen

Linux/Kubuntu primär, Python 3.12 angestrebt, nur Standardbibliothek, `python3-venv`, lokaler Browser. Keine externen Python-/JS-Pakete, keine CDN-/Remote-Font-Abhängigkeiten.

## Persistenz

Lokale Nutzerdaten bleiben unter `runtime/` und sind aus Git/Release ausgeschlossen. Atomare Hauptdatei + Backup-Fallback gilt für persistente Domänenmodelle.

Aktuelle persistente Schemata:

- VersionRegistry: 1
- EventRegistry: 1
- TODO-Core: 1
- Calendar-Core: 1
- Textkatalog: 1
- Fehlerregeln: 1
- Learning Memory: 1 pro JSONL-Eintrag

Schemaänderung benötigt Validator, Vorlage, positive/negative Testdaten und Regression/Migration gemeinsam.

## Kalendervertrag

Ein Kalendertermin kann Titel, Datum, optionale Start-/Endzeit, Kategorie, Beschreibung, optionale TODO-ID, Zeitzonenmodus und Reminder enthalten.

- Endzeit ohne Startzeit ist ungültig.
- Endzeit muss nach Startzeit liegen.
- Reminder benötigen eine Startzeit.
- erlaubte Reminder: 0, 10, 30, 60, 1440 Minuten vorher.
- fällige Reminder bleiben offen, bis `notified_at` atomar persistiert wurde.
- lokale zukünftige Termine verwenden die System-IANA-Zeitzone via `zoneinfo`, nicht einen festen aktuellen UTC-Offset.
- TODO-Verknüpfung ist optional; bei Angabe muss die TODO-ID existieren.

## Fehlerhilfe-Vertrag

Fehlerantworten können liefern: `rule_id`, Kategorie, Schweregrad/Ampel, verständliche Meldung, sichere Handlung, optional `template_path`, `retry_safe` und Bereich.

Mustervorlagen sind reine Referenzen. Keine Regel darf sie ohne ausdrückliche Aktion über echte Nutzerdaten schreiben.

## Learning-Memory-Vertrag

`LEARNING_MEMORY.jsonl` enthält Entwicklungslektionen, keine Nutzerdaten. CI prüft eindeutige IDs, Schema, Pflichtfelder und aktive Regeln. Aktuell sind zusätzlich DST-/Reminder-/Metadatenversions-Lektionen verbindlich.

## Netzwerk

Backend ausschließlich `127.0.0.1`, Standardport 8765, kein Internetzwang, keine Telemetrie, Host-/Origin-Guard, keine CORS-Freigabe.

## Release-Ausschlüsse

`.venv/`, `runtime/*` außer `.gitkeep`, `__pycache__`, Testcache, `dist/`, `build/`, Logs, lokale Profile/Pfade, reale TODO-/Event-/Kalender-/Recovery-Daten, Secrets/PINs/Passwörter.

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

`0.3.0-calendar-core` ist automatisiert **GEPRÜFT** durch Run `33026180855`, bleibt `draft`. Reale Kubuntu-/Browser-/Zoom-Gates und die sichtbare Reminder-Darstellung sind weiterhin offen.

## Nächster Manifest-Schritt

Dashboard V2: vorhandene Version-/TODO-/Calendar-/Event-APIs sichtbar integrieren, Reminder-Anzeige sicher quittieren, Monatskalender und nächste Termine darstellen, Debugzugang und responsive Dichteführung ergänzen — ohne Domänenlogik in JavaScript zu duplizieren.

# MANIFEST

## Projekt

- **Name:** AIO-Tool
- **Repository:** `provoware/AIO-Tool`
- **Version:** `0.4.0-dashboard-v2`
- **Phase:** P1 — Dashboard-Integration
- **Stand:** 2026-08-27
- **Backend:** Python-Standardbibliothek, Loopback-only
- **Internetpflicht:** nein

## Verbindlicher Root-Bestand

`README.md`, `TODO.md`, `AGENTS.md`, `CHANGELOG.md`, `LAIEN-ANLEITUNG.md`, `TOOLBESCHREIBUNG.md`, `MANIFEST.md`, `REGRESSIONSINFOS.md`, `VERSION`, `VERSION_REGISTRY.json`, `LEARNING_MEMORY.jsonl`, `start_tool.sh`, `start_tool.desktop`, `.gitignore`.

## Anwendung

- `app/config.py` — validierte Konfiguration.
- `app/persistence.py` — atomarer JSON-Speicher.
- `app/version_registry.py` — Versions-/Evidenzvertrag.
- `app/event_registry.py` — menschenlesbare Ereignisse.
- `app/todo_store.py` — TODOs, Titelgedächtnis, Archiv.
- `app/calendar_store.py` — Kalender, Perioden, Reminder, zoneinfo/DST.
- `app/text_catalog.py` — versionierte Core-Texte.
- `app/error_advisor.py` — regelbasierte Fehlerhilfe.
- `app/learning_memory.py` — Entwicklungs-Lerngedächtnis.
- `app/server.py` — lokale Core-API.

## Dashboard V2

- `web/index.html` — semantische Dashboardstruktur.
- `web/app.js` — dünne API-/Darstellungsschicht; keine Kopie der Domänenlogik.
- `web/styles.css` — Themes, Kontrast, Fokus, responsive Dichte.
- `web/dashboard-texts.de.v1.json` — versionierte deutsche Dashboardtexte, Schema 1 / Katalog 1.0.0.

### Sichtbare Kernbereiche

- Monatskalender,
- kommende Termine,
- nächste drei TODOs,
- letzte fünf Ereignisse,
- System-/Registry-/Versionsstatus,
- fällige Reminder,
- Schnellmodule Häufig/Alle,
- optionaler Entwicklerbereich,
- Darstellungseinstellungen.

## Reminder-UI-Vertrag

- Pollingintervall: 60 Sekunden.
- Polling quittiert keinen Reminder.
- unsichtbarer Tab quittiert keinen Reminder.
- ACK erst über sichtbaren Reminder + explizite Nutzeraktion `Gesehen`.
- Backend persistiert erst dann `notified_at`.

## Ressourcen und Testdaten

`resources/templates/` enthält geprüfte Referenzen für Config, VersionRegistry, Events, TODO und Kalender.  
`testdata/valid/` muss von Produktvalidatoren akzeptiert werden.  
`testdata/invalid/` hält reproduzierbare Negativfälle.  
Mustervorlagen dürfen niemals automatisch echte Runtime-Daten überschreiben.

## Qualität / Tests

Zusätzlich zum bisherigen Core gehören verbindlich:

- `tests/test_dashboard_contract.py`
- Dashboard-Textkatalogprüfung,
- erforderliche DOM-Bereiche,
- API-Vertragsmarker,
- Reminder-Visibility-/ACK-Vertrag,
- sichere Textausgabe von Nutzertiteln,
- Diagnose-Datensparsamkeit,
- Responsive-/A11y-Schutzmarker.

`scripts/validate.py` prüft diese Verträge zusätzlich außerhalb des Unit-Test-Laufs.

## Persistenzschemata

- VersionRegistry: 1
- EventRegistry: 1
- TODO: 1
- Calendar: 1
- Core-Textkatalog: 1
- Fehlerregeln: 1
- Learning Memory: 1 pro JSONL-Zeile
- Dashboard-Textkatalog: 1

## Netzwerk / Datenschutz

- Bind ausschließlich `127.0.0.1`.
- Host-/Origin-Guard.
- keine Telemetrie.
- keine externen Python-/JS-Pakete.
- keine CDN-/Remote-Fonts.
- Entwicklerdiagnose zeigt keine vollständige Config, `active_project` oder Favoritenliste.

## Release-Ausschlüsse

`.venv/`, produktive `runtime/*` außer `.gitkeep`, `__pycache__`, Testcache, lokale Logs, `dist/`/`build/` als Eingabe, lokale Profile/Pfade sowie reale Nutzer-/Kalender-/TODO-/Recovery-Daten.

Tests, künstliche Testdaten und Referenzvorlagen bleiben Teil des vollständigen Projekt-ZIPs.

## Automatisierter Nachweis

Code-Gate `33026823914`: **SUCCESS** mit 77 Tests, Validierung, Learning Guard, Launcher, JavaScript, Release-Builder und ZIP-Upload.

Release-Builder-Ausgabe: `AIO-Tool-0.4.0-dashboard-v2.zip`  
SHA256: `104c361caf65c484626cd24812272e0781c151d2afcbcb933b5fc393a3e9e946`.

## Noch offene reale Gates

Kubuntu, Firefox, Chrome/Chromium, 125–200 % Zoom, echte Tastatur-/Fokusnavigation und verschiedene Displaygrößen.

## Nächster Manifest-Schritt

Nach realer Dashboard-Abnahme: SAFE-FILE-CORE mit Copy, Vorprüfung, Vorschau, persistenter Jobausführung, Nachprüfung und Undo-/Recovery-Datensatz.

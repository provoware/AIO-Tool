# MANIFEST

## Projekt

- **Name:** AIO-Tool
- **Repository:** `provoware/AIO-Tool`
- **Phase:** P1 — gemeinsamer persistenter Kern
- **Version:** `0.2.0-core`
- **Stand:** 2026-08-27

## Verbindlicher Projektbestand

### Root

| Pfad | Rolle |
|---|---|
| `README.md` | Einstieg, Status, Start und Projektüberblick |
| `TODO.md` | priorisierte Arbeit und Gates |
| `AGENTS.md` | verbindliche Entwicklungs- und Sicherheitsregeln |
| `CHANGELOG.md` | Versionshistorie in menschenlesbarer Form |
| `LAIEN-ANLEITUNG.md` | einfache Nutzererklärung |
| `TOOLBESCHREIBUNG.md` | Produktvision und Funktionsrahmen |
| `MANIFEST.md` | definierter Projekt-/Releasebestand |
| `REGRESSIONSINFOS.md` | Regressionen, Tests und Evidenz |
| `VERSION` | aktuelle Versionsquelle |
| `VERSION_REGISTRY.json` | getrackte maschinenlesbare Projekt-Versionshistorie |
| `start_tool.sh` | primärer Linux/Kubuntu-Launcher |
| `start_tool.desktop` | Desktop-Starter-Vorlage |
| `.gitignore` | lokale/releasefremde Ausschlüsse |

### Anwendung

| Pfad | Rolle |
|---|---|
| `app/__init__.py` | Root-/Versionszugriff |
| `app/config.py` | bestehende validierte Konfigurationspersistenz |
| `app/persistence.py` | gemeinsamer atomarer JSON-Speicher für neue Domänenmodelle |
| `app/version_registry.py` | Versionshistorie, Status, Evidenz und Driftprüfung |
| `app/event_registry.py` | menschenlesbare Ereignishistorie |
| `app/todo_store.py` | persistente TODOs, Titelgedächtnis und Erledigt-Archiv |
| `app/server.py` | lokaler HTTP/API-Server und Core-API |
| `web/index.html` | Dashboard-Shell |
| `web/app.js` | UI-Zustand und lokale API-Anbindung |
| `web/styles.css` | Themes, Kontrast und responsive Darstellung |

### Qualität / Release

| Pfad | Rolle |
|---|---|
| `tests/test_config.py` | bestehender Konfigurationsvertrag |
| `tests/test_server.py` | Loopback-/Origin-Sicherheitsvertrag |
| `tests/test_persistence.py` | atomarer JSON-Speicher + Backup-Fallback |
| `tests/test_version_registry.py` | Versionsstatus, Evidenz, Seed-Historie und Drift |
| `tests/test_event_registry.py` | Ereignisvalidierung und newest-first-Abruf |
| `tests/test_todo_store.py` | Titelgedächtnis, nächste TODOs und Erledigt-Archiv |
| `tests/test_core_api.py` | integrierter Version/Event/TODO-API- und Fehlerklassen-Flow |
| `scripts/validate.py` | Foundation-/Core-Vorprüfung inkl. Registry-Driftcheck |
| `scripts/release.py` | reproduzierbarer ZIP-Builder |
| `.github/workflows/foundation-ci.yml` | automatisierte CI-Gates auf `main` und `feature/**` |
| `runtime/.gitkeep` | Platzhalter; reale Runtime-Inhalte ausgeschlossen |

## Laufzeitvoraussetzungen

- Linux/Kubuntu als primäres Zielsystem.
- Python 3.12 angestrebt; Code nutzt nur Standardbibliothek.
- `python3-venv` für die lokale `.venv`.
- Firefox und Chrome/Chromium als Zielbrowser.
- `xdg-open` bevorzugt; Browser-Fallbacks im Launcher.

## Abhängigkeiten

### Python

**Keine externen Python-Pakete.**

### Browser

- keine externen JavaScript-Bibliotheken,
- keine CDN-Abhängigkeit,
- keine Remote-Fonts.

## Versionsverwaltung

### Getrackte Projekthistorie

`VERSION_REGISTRY.json` ist Teil des Repository- und Releasebestands. Sie enthält den bekannten offiziellen Versionsstamm und wird per CI gegen `VERSION` validiert.

### Lokale Runtime-Registry

`runtime/versions.json` wird bei frischer Runtime aus der getrackten Historie initialisiert und kann anschließend lokalen Laufzeitstatus führen. Sie ist kein Git-/Releasebestand.

Diese Trennung verhindert, dass eine frische Installation die Projektgeschichte verliert oder lokale Zustände die offizielle Historie still überschreiben.

## Lokale Persistenz

Zur Laufzeit:

```text
runtime/config.json
runtime/config.json.bak
runtime/versions.json
runtime/versions.json.bak
runtime/events.json
runtime/events.json.bak
runtime/todos.json
runtime/todos.json.bak
runtime/server.log
runtime/launcher.log
runtime/server.pid
```

### Schemata

- Config: bestehender Konfigurationsvertrag.
- VersionRegistry: `schema_version = 1`.
- EventRegistry: `schema_version = 1`.
- TODO-Core: `schema_version = 1`.

Schemaänderungen benötigen eine explizite Migration und Regressionstests.

## Datenvertrag

### VersionRegistry

Persistiert Versionsnummer, Zeit, Status, Release-Status, optional Commit-SHA, Zusammenfassung, Änderungen, bekannte Probleme, Regressionstatus und Evidenz.

### EventRegistry

Persistiert kurze menschenlesbare Ereignisse mit Zeit, Art, Bereich, Statusstufe und optionalen technischen Details. Die Eventliste wird auf 500 Einträge begrenzt.

### TODO-Core

Persistiert aktive TODOs, Erledigt-Archiv und Titelgedächtnis. Ein Kalenderbezug ist optional vorbereitet und darf nicht Voraussetzung für normale TODOs werden.

## Netzwerk- und Fehlervertrag

- Backend ausschließlich `127.0.0.1`.
- Standardport `8765`.
- kein Internetzwang.
- keine Telemetrie.
- Host-/Origin-Prüfung auf lokale Herkunft.
- keine CORS-Freigabe.
- ungültige Abfrageparameter: HTTP 400.
- beschädigte lokale Lesepersistenz: HTTP 500 mit verständlicher Integritätsmeldung.
- sekundäres Eventlogging darf eine bereits persistierte Hauptaktion nicht rückwirkend als fehlgeschlagen darstellen.

## Release-Ausschlüsse

- `.venv/`
- `runtime/*` außer `.gitkeep` im Repository
- `__pycache__/`
- Testcache
- `dist/`, `build/`
- lokale Logs
- lokale Profile/Pfade
- reale TODO-/Kalender-/Event-/Recovery-Daten
- Secrets/PINs/Passwörter

## Testkommandos

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate.py
bash -n start_tool.sh
node --check web/app.js
python3 scripts/release.py --check
```

## Statusvertrag

`0.2.0-core` bleibt bis zum finalen grünen CI-Head **UMGESETZT**. Reale Kubuntu-/Browser-Gates bleiben separat offen.

## Nächster Manifest-Schritt

Mit Kalender-Core ergänzen:

- `app/calendar_store.py`,
- Kalender-Schema/Migration,
- Reminder-Datenvertrag,
- Kalender-API,
- Tests für Monat/Woche/Jahr und Persistenz,
- optionale TODO-Verknüpfung.

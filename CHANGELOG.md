# CHANGELOG

Alle wesentlichen Änderungen an AIO-Tool werden nachvollziehbar dokumentiert.

## [Unreleased]

### Geplant

- Dashboard V2 mit Monatskalender, nächsten Terminen, nächsten drei TODOs, letzten fünf Ereignissen, Versions-/Gesundheitsstatus und Debugzugang.
- sichtbare Reminder-Anzeige im Browser auf Basis des bereits getesteten Reminder-Cores.
- danach reale Kubuntu-/Browser-/Zoom-Gates und SAFE-FILE-CORE.

## [0.3.0-calendar-core] — 2026-08-27

### Added

- `app/calendar_store.py` als persistenter Kalender-Core auf `AtomicJsonStore`.
- Terminmodell mit Titel, Datum, optionaler Start-/Endzeit, Kategorie, Beschreibung und optionaler TODO-Verknüpfung.
- Titelgedächtnis für wiederkehrende Kalendertitel.
- Erinnerungs-Presets 0 / 10 / 30 / 60 / 1440 Minuten vorher.
- Abfrage fälliger, noch nicht quittierter Erinnerungen.
- persistente Reminder-Quittierung über `notified_at`.
- Monats-, Wochen- und Jahresperioden.
- System-Zeitzone über Python `zoneinfo` für korrekte zukünftige Sommer-/Winterzeitberechnung.
- Kalender-Mustervorlage sowie gültige und absichtlich ungültige Kalender-Testdaten.
- Kalender-Fehlerregeln und laienfreundliche Kalender-/Remindertexte.
- lokale Kalender-API für Anlegen, Perioden, Vorschläge, fällige Reminder und Quittierung.
- Integrationstests für optionale TODO-Verknüpfung.
- Learning-Memory-Einträge für DST, Reminder-Quittierung und versionierte Testmetadaten.

### Changed

- Fehlerregelversion und Textkatalog wurden für Kalenderfälle erweitert.
- `/api/status` enthält Kalenderinformationen.
- `scripts/validate.py` prüft Kalender-Vorlage, Testdaten und Kalender-Persistenz.
- Metadaten-API-Test liest erwartete Regel-/Textversionen aus den jeweiligen versionierten Quelldateien statt aus redundanten harten Konstanten.

### Fixed

- erster Kalender-CI-Stand scheiterte ausschließlich an einem veralteten harten Testwert für `rules_version` (`1.0.0` statt `1.1.0`).
- Regressionstest wurde strukturell repariert: Quelle der Wahrheit ist nun die versionierte Regeldatei.

### Safety

- Reminder ohne Startzeit werden abgelehnt.
- Endzeit muss nach Startzeit liegen.
- unbekannte TODO-Verknüpfung wird nicht still akzeptiert.
- Reminder werden nicht automatisch als angezeigt markiert; Quittierung ist ein separater persistenter Schritt.
- Kalenderdaten bleiben lokal und werden nicht in Runtime-Form in Release-ZIPs übernommen.

### Verified

GitHub Actions Run `33026180855`: **SUCCESS**.

Erfolgreich: Python-Syntax, 69 Unit-/Integrationstests, Foundation-/Kalender-Validierung, Learning Guard, Launcher-Syntax, JavaScript-Syntax, Release-Builder und Upload des vollständigen Release-ZIPs.

### Not yet verified

- sichtbare Browser-/Desktop-Reminderanzeige,
- realer Kubuntu-Klick-&-Start,
- Firefox/Chrome/Chromium auf Zielsystem,
- 125–200 % Browserzoom.

## [0.2.1-robustness] — 2026-08-27

### Added

- versionierte Config-/JSON-Mustervorlagen unter `resources/templates/`.
- positive und absichtlich negative Testdaten unter `testdata/`.
- versionierter deutscher Textkatalog `resources/texts/de/v1.json`.
- versionierte Fehlerregeln `resources/error_rules/v1.json`.
- `ErrorAdvisor` mit Regel-ID, Kategorie, Ampelstufe, einfacher Handlung, optionalem Vorlagenhinweis und `retry_safe`.
- `GET /api/help/meta` für Fehlerregel-/Textkatalog-Metadaten.
- `LEARNING_MEMORY.jsonl` als Entwicklungs-Lerngedächtnis.
- `scripts/learning_guard.py` als zusätzliches CI-Gate.
- CI-Upload des vollständigen Release-ZIPs als GitHub-Actions-Artefakt.

### Changed

- wiederkehrende Core-Systemtexte sind aus `server.py` in den versionierten Textkatalog ausgelagert.
- API-Fehlerantworten enthalten strukturierte, laienverständliche Hilfe.
- `scripts/validate.py` prüft Vorlagen, Text-/Fehlerregeln und Learning Memory.
- AGENTS.md verlangt künftig Vorlage + Negativtest pro persistentem Datenformat und gezielte Patchstellen vor Großumbauten.

### Fixed

- Fehlerregeln matchten zunächst nur exakte Klassennamen; spezialisierte Unterklassen wie `ConfigIntegrityError` wurden dadurch nicht als Integritätsfehler erkannt. Matcher nutzt jetzt die Klassenhierarchie; direkter Regressionstest ergänzt.

### Verified

GitHub Actions Run `33025238585`: **SUCCESS** inklusive Release-ZIP-Upload.

## [0.2.0-core] — 2026-08-27

### Added

- gemeinsamer `AtomicJsonStore`.
- getrackte `VERSION_REGISTRY.json` + lokale Runtime-Registry.
- VersionRegistry mit Evidenz-/Driftvertrag.
- EventRegistry für menschenlesbare Ereignisse.
- persistenter TODO-Core mit Titelgedächtnis und Erledigt-Archiv.
- API und Regressionstests für Versionen, Events und TODOs.

### Verified

Feature-/Merge-Kandidat Run `33022569880`: **SUCCESS**. Squash-Merge auf `main`: `a110132acc4104e0f0c48c736a3fd4bc98a9c290`.

## [0.1.1-foundation] — 2026-08-27

- ausführbarer Foundation-Kern mit Klick-&-Start, Loopback-Backend, atomarer Config, Dashboard-Shell, Tests, CI und Release-Builder.

## [0.1.0-foundation] — 2026-08-27

- saubere Projektgrundlage ohne Altcode und verbindliche Basisdokumentation.

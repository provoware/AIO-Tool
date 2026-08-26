# CHANGELOG

Alle wesentlichen Änderungen an AIO-Tool werden nachvollziehbar dokumentiert.

## [Unreleased]

### Geplant

- `0.3.0-calendar-core`: persistenter Kalender, Erinnerungsmodell, Monats-/Wochen-/Jahresdaten und optionale TODO-Verknüpfung.
- danach Dashboard V2 mit nächsten drei TODOs, Terminen, letzten fünf Ereignissen und Debugzugang.

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

### Safety

- Mustervorlagen werden niemals automatisch über Nutzerdaten geschrieben.
- Fehlerhilfe kennzeichnet sichere Wiederholbarkeit explizit.
- unbekannte Fehler behaupten keine automatische Recovery.
- sekundäres Eventlogging kann eine bereits gespeicherte TODO-Aktion weiterhin nicht zurückrollen.

### Verified

GitHub Actions Run `33024919165`: **SUCCESS**.

Erfolgreich: Python-Syntax, Unit-/Integrationstests, Foundation-/Core-Validierung, Learning Guard, Launcher-Syntax, JavaScript-Syntax, Release-Builder und Upload des vollständigen Release-ZIPs.

### Not yet verified

- realer Kubuntu-Klick-&-Start,
- Firefox/Chrome/Chromium auf Zielsystem,
- 125–200 % Browserzoom.

## [0.2.0-core] — 2026-08-27

### Added

- gemeinsamer `AtomicJsonStore`.
- getrackte `VERSION_REGISTRY.json` + lokale Runtime-Registry.
- VersionRegistry mit Evidenz-/Driftvertrag.
- EventRegistry für menschenlesbare Ereignisse.
- persistenter TODO-Core mit Titelgedächtnis und Erledigt-Archiv.
- API und Regressionstests für Versionen, Events und TODOs.

### Fixed

- optionales `commit_sha=null` korrekt unterstützt und regressionsgesichert.
- Nutzerfehler (400) von lokalen Integritätsfehlern (500) getrennt.

### Verified

Feature-/Merge-Kandidat Run `33022569880`: **SUCCESS**. Squash-Merge auf `main`: `a110132acc4104e0f0c48c736a3fd4bc98a9c290`.

## [0.1.1-foundation] — 2026-08-27

- ausführbarer Foundation-Kern mit Klick-&-Start, Loopback-Backend, atomarer Config, Dashboard-Shell, Tests, CI und Release-Builder.

## [0.1.0-foundation] — 2026-08-27

- saubere Projektgrundlage ohne Altcode und verbindliche Basisdokumentation.

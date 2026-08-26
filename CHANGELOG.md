# CHANGELOG

Alle wesentlichen Änderungen an AIO-Tool werden hier nachvollziehbar dokumentiert.

## [Unreleased]

### Geplant

- Foundation-CI auf `main` verifizieren.
- frischen Zielsystemstart unter Kubuntu prüfen.
- danach SAFE-FILE-CORE mit Copy als erster realer Dateioperation beginnen.

## [0.1.1-foundation] — 2026-08-27

### Added

- ausführbare Clean-Foundation-Projektstruktur mit `app/`, `web/`, `scripts/`, `tests/` und `runtime/`.
- `start_tool.sh` als Klick-&-Start-Launcher.
- lokale `.venv` ohne externe Python-Pakete.
- Mehrfachstartschutz: vorhandene valide Instanz wird wieder geöffnet.
- Python-Backend auf `127.0.0.1`.
- Host-/Origin-Prüfung für lokale API-Zugriffe.
- Security-Header für die Browser-Oberfläche.
- atomare JSON-Konfiguration mit Backup-Fallback.
- responsive Dashboard-Shell mit sichtbarem nächsten Schritt.
- vier Themes: Trash Neon, Steel Night, Clean Light und High Contrast.
- Schriftgrößen-Presets 90–140 % über Buttons.
- standardmäßig verborgener Expertenbereich.
- `scripts/validate.py` für Foundation-Vorprüfung.
- `scripts/release.py` für reproduzierbares, bereinigtes ZIP.
- Standardbibliothek-Unit-Tests für Persistenz- und Loopback-Sicherheitsvertrag.
- GitHub-Actions-Workflow `foundation-ci`.

### Changed

- Status von reiner Dokumentationsbasis auf ausführbaren Foundation-Kern angehoben.
- nächster Entwicklungs-Slice auf „Copy zuerst“ innerhalb SAFE-FILE-CORE präzisiert.

### Security

- keine Bindung an externe Interfaces.
- keine CORS-Freigabe.
- mutierende API-Aufrufe nur mit gültigem lokalem Host/Origin-Vertrag.
- Anfragegröße für JSON-Schreibzugriffe begrenzt.
- Konfigurationsfelder serverseitig auf erlaubte Schlüssel beschränkt.

### Not yet verified

- tatsächlicher frischer Start auf dem Kubuntu-Zielsystem.
- Firefox- und Chrome/Chromium-Gate auf Zielsystem.
- GitHub-CI-Ergebnis dieses Commits.

## [0.1.0-foundation] — 2026-08-27

### Added

- vollständige saubere Projektgrundlage ohne Altcode.
- `README.md`, `TODO.md`, `AGENTS.md`, `LAIEN-ANLEITUNG.md`, `TOOLBESCHREIBUNG.md`, `MANIFEST.md`, `REGRESSIONSINFOS.md`.

### Changed

- Repository inhaltlich vollständig auf CLEAN FOUNDATION zurückgesetzt.
- Produktphilosophie auf „Auswahl vor Zeicheneingabe“, offline-first, Recovery und transparente Prozesse festgelegt.

### Removed

- alter Projektinhalt der vorherigen Repository-Struktur.
- alte Platzhalterdateien und frühere Frontend-Dateinamen.

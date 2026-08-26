# CHANGELOG

Alle wesentlichen Änderungen an AIO-Tool werden hier nachvollziehbar dokumentiert.

## [Unreleased]

### Geplant

- `0.2.0-core` per CI abnehmen.
- Kalender-Core auf dem neuen Persistenzvertrag aufbauen.
- danach TODO/Kalender/Ereignisse ins kompaktere responsive Dashboard integrieren.
- SAFE-FILE-CORE weiterhin erst nach stabilem Daten-/Dashboardkern beginnen.

## [0.2.0-core] — 2026-08-27

### Added

- gemeinsamer `AtomicJsonStore` für neue persistente Domänenmodelle.
- `VersionRegistry` mit Schema-Version, Versionshistorie, Status, Release-Status, Commit-SHA, Änderungen, bekannten Problemen, Regressionstatus und Evidenz.
- Schutzregel: `tested`, `release-candidate` und `released` benötigen vorher Evidenz.
- Erkennung von Drift zwischen `VERSION` und VersionRegistry.
- Abruf der letzten registrierten Vorgängerversion.
- `EventRegistry` für kurze menschenlesbare Ereignisse mit Bereich und Ampel-/Statusstufe.
- Event-Historie auf 500 Einträge begrenzt; letzte Ereignisse newest-first abrufbar.
- persistenter TODO-Kern mit Titel, Kategorie, optionalem Termin, Priorität, Notiz und optionaler zukünftiger Kalenderverknüpfung.
- persistentes TODO-Titelgedächtnis mit Häufigkeit und letzter Verwendung.
- Erledigt-Archiv: Abhaken verschiebt statt zu löschen und speichert `completed_at`.
- serverseitige Ermittlung der nächsten drei TODOs.
- APIs für Versionen, Ereignisse, TODOs, Archiv und Titelvorschläge.
- Integrationstest für VersionRegistry → TODO anlegen → Titelvorschlag → abhaken → EventRegistry.
- zusätzliche Unit-Tests für Persistenz, VersionRegistry, EventRegistry und TODO-Core.

### Changed

- `/api/status` liefert zusätzlich Registry-Konsistenz sowie Anzahl offener/archivierter TODOs und Ereignisse.
- Foundation-Validierung prüft nun auch Versions-Registry, Ereignisspeicherung, TODO-Titelgedächtnis und Erledigt-Archiv.
- Entwicklungsreihenfolge auf Datenkern → Kalender-Core → Dashboard-Integration → SAFE-FILE-CORE präzisiert.

### Security / Integrity

- neue Registry-/TODO-Dateien nutzen atomisches Replace mit Backup-Fallback.
- schreibende TODO-Endpunkte bleiben an den bestehenden lokalen Host-/Origin-Vertrag gebunden.
- Versionen können nicht ohne Evidenz fälschlich als getestet/freigegeben markiert werden.
- TODOs werden beim Erledigen nicht still gelöscht.
- Event-Protokollierung ist sekundär: eine bereits sicher gespeicherte TODO-Aktion wird bei einem Event-Fehler nicht fälschlich als fehlgeschlagen gemeldet; stattdessen wird eine Warnung zurückgegeben.

### Verification status

- Code und Tests: **UMGESETZT**.
- GitHub-CI für diesen Slice: **noch ausstehend**, bis der Pull Request gelaufen ist.
- reale Kubuntu-/Browser-Gates: weiterhin offen.

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
- Bootstrap-/Release-Skripte importieren den Repository-Root explizit.

### Security

- keine Bindung an externe Interfaces.
- keine CORS-Freigabe.
- mutierende API-Aufrufe nur mit gültigem lokalem Host/Origin-Vertrag.
- Anfragegröße für JSON-Schreibzugriffe begrenzt.
- Konfigurationsfelder serverseitig auf erlaubte Schlüssel beschränkt.

### Verified

- GitHub-Actions `foundation-ci`: **SUCCESS**.
- Python-Syntax, Unit-Tests, Foundation-Validierung, Launcher-Syntax, JavaScript-Syntax und Release-Builder: grün.

### Not yet verified

- tatsächlicher frischer Start auf dem Kubuntu-Zielsystem.
- Firefox- und Chrome/Chromium-Gate auf Zielsystem.

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

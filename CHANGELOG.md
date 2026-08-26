# CHANGELOG

Alle wesentlichen Änderungen an AIO-Tool werden hier nachvollziehbar dokumentiert.

## [Unreleased]

### Geplant

- `0.2.0-core` per finalem CI-Head abnehmen und mergen.
- Kalender-Core auf dem neuen Persistenzvertrag aufbauen.
- danach TODO/Kalender/Ereignisse ins kompaktere responsive Dashboard integrieren.
- SAFE-FILE-CORE weiterhin erst nach stabilem Daten-/Dashboardkern beginnen.

## [0.2.0-core] — 2026-08-27

### Added

- gemeinsamer `AtomicJsonStore` für neue persistente Domänenmodelle.
- getrackte `VERSION_REGISTRY.json` als projektweite Versionshistorie.
- lokale `runtime/versions.json`, die bei frischer Installation aus der getrackten Historie initialisiert wird.
- `VersionRegistry` mit Schema-Version, Versionshistorie, Status, Release-Status, Commit-SHA, Änderungen, bekannten Problemen, Regressionstatus und Evidenz.
- Schutzregel: `tested`, `release-candidate` und `released` benötigen vorher Evidenz.
- Erkennung von Drift zwischen `VERSION` und getrackter VersionRegistry.
- Abruf der letzten registrierten Vorgängerversion.
- `EventRegistry` für kurze menschenlesbare Ereignisse mit Bereich und Ampel-/Statusstufe.
- Event-Historie auf 500 Einträge begrenzt; letzte Ereignisse newest-first abrufbar.
- persistenter TODO-Kern mit Titel, Kategorie, optionalem Termin, Priorität, Notiz und optionaler zukünftiger Kalenderverknüpfung.
- persistentes TODO-Titelgedächtnis mit Häufigkeit und letzter Verwendung.
- Erledigt-Archiv: Abhaken verschiebt statt zu löschen und speichert `completed_at`.
- serverseitige Ermittlung der nächsten drei TODOs.
- APIs für Versionen, Ereignisse, TODOs, Archiv und Titelvorschläge.
- Integrationstests für VersionRegistry → TODO anlegen → Titelvorschlag → abhaken → EventRegistry.
- zusätzliche Unit-Tests für Persistenz, VersionRegistry, EventRegistry und TODO-Core.

### Changed

- `/api/status` liefert zusätzlich Registry-Konsistenz sowie Anzahl offener/archivierter TODOs und Ereignisse.
- Foundation-Validierung prüft nun auch die getrackte Versionshistorie, deren Übereinstimmung mit `VERSION`, Ereignisspeicherung, TODO-Titelgedächtnis und Erledigt-Archiv.
- Feature-Branches unter `feature/**` werden bereits beim Push durch die vollständige CI geprüft.
- ungültige GET-Abfrageparameter werden als 400/Nutzereingabe behandelt; beschädigte lokale Registry-/TODO-Lesedaten als 500/Integritätsfehler.
- Entwicklungsreihenfolge auf Datenkern → Kalender-Core → Dashboard-Integration → SAFE-FILE-CORE präzisiert.

### Fixed

- optionales `commit_sha=null` wurde in der ersten Registry-Implementierung fälschlich abgelehnt; CI hat den Fehler entdeckt und ein direkter Regressionstest sichert ihn nun ab.
- Seed-/Default-Persistenz wird jetzt ebenfalls validiert und nicht ungeprüft übernommen.
- ein Fehler im sekundären Ereignisprotokoll darf eine bereits sicher gespeicherte TODO-Aktion nicht mehr fälschlich als fehlgeschlagen erscheinen lassen.

### Security / Integrity

- neue Registry-/TODO-Dateien nutzen atomisches Replace mit Backup-Fallback.
- schreibende TODO-Endpunkte bleiben an den lokalen Host-/Origin-Vertrag gebunden.
- Versionen können nicht ohne Evidenz fälschlich als getestet/freigegeben markiert werden.
- TODOs werden beim Erledigen nicht still gelöscht.
- offizielle Projekt-Historie und lokale Laufzeit-Registry sind getrennt, damit lokale Zustände nicht still die getrackte Historie überschreiben.

### Verification status

- Zwischenlauf nach Fix des optionalen Commit-SHA: **SUCCESS**.
- finaler CI-Head mit Registry-Seed und Integritätsklassifizierung: noch abzunehmen.
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

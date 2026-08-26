# CHANGELOG

Alle wesentlichen Änderungen an AIO-Tool werden nachvollziehbar dokumentiert.

## [Unreleased]

### Geplant

- Kalender-Core auf dem gemeinsamen Persistenzvertrag aufbauen.
- danach TODO/Kalender/Ereignisse ins kompaktere responsive Dashboard integrieren.
- SAFE-FILE-CORE erst nach stabilem Daten-/Dashboardkern beginnen.

## [0.2.0-core] — 2026-08-27

### Added

- gemeinsamer `AtomicJsonStore` für persistente Domänenmodelle.
- getrackte `VERSION_REGISTRY.json` als offizielle Projekt-Versionshistorie.
- lokale `runtime/versions.json`, die bei frischer Installation aus dieser Historie initialisiert wird.
- `VersionRegistry` mit Status, Release-Status, Commit-SHA, Änderungen, Problemen, Regressionstatus und Evidenz.
- Evidenzpflicht für `tested`, `release-candidate` und `released`.
- Driftprüfung `VERSION` ↔ getrackte Registry und Abruf der Vorgängerversion.
- `EventRegistry` für kurze menschenlesbare Ereignisse; maximal 500, newest-first.
- persistenter TODO-Core mit Titel, Kategorie, optionalem Termin, Priorität, Notiz und optionaler Kalenderverknüpfung.
- TODO-Titelgedächtnis mit Häufigkeit und letzter Verwendung.
- Erledigt-Archiv mit `completed_at` statt Löschen.
- serverseitige Ermittlung der nächsten drei TODOs.
- APIs für Versionen, Ereignisse, TODOs, Archiv und Titelvorschläge.
- Unit- und Integrationstests für Persistenz, Registry, Events, TODOs und HTTP-Fehlerklassen.

### Changed

- `/api/status` enthält Registry-Konsistenz sowie TODO-/Event-Zähler.
- `scripts/validate.py` prüft getrackte Versionshistorie, `VERSION`-Übereinstimmung und frische Runtime-Initialisierung.
- `feature/**`-Branches laufen bereits beim Push durch die vollständige CI.
- ungültige Anfrageparameter/Einstellungen → HTTP 400; beschädigte lokale Persistenz → HTTP 500 mit Integritätsmeldung.
- Entwicklungsreihenfolge: Datenkern → Kalender-Core → Dashboard-Integration → SAFE-FILE-CORE.

### Fixed

- optionales `commit_sha=null` wurde in der ersten Registry-Implementierung fälschlich abgelehnt; CI entdeckte den Fehler, direkter Regressionstest ergänzt.
- Seed-/Default-Persistenz wird vor Verwendung validiert.
- sekundärer Eventfehler kann eine bereits gespeicherte TODO-Aktion nicht rückwirkend als fehlgeschlagen darstellen.
- Config-Eingabefehler und beschädigte Config werden im API-Vertrag getrennt klassifiziert.

### Integrity

- atomisches Replace + Backup-Fallback für neue Registry-/TODO-Dateien.
- TODOs werden beim Erledigen archiviert, nicht still gelöscht.
- offizielle Projekt-Historie und lokale Runtime-Registry sind getrennt.
- schreibende TODO-Endpunkte bleiben an Host-/Origin-Guard gebunden.

### Verified

GitHub Actions Run `33022569880`: **SUCCESS**.

Erfolgreich:
- Python-Syntax,
- Unit-/Integrationstests,
- Core-/Foundation-Validierung,
- Launcher-Syntax,
- JavaScript-Syntax,
- Release-Builder.

### Not yet verified

- frischer realer Kubuntu-Klick-&-Start,
- Firefox und Chrome/Chromium auf Zielsystem,
- 125–200 % Browserzoom auf Zielsystem.

Der Stand ist deshalb **tested / draft**, nicht `released`.

## [0.1.1-foundation] — 2026-08-27

### Added

- ausführbarer Foundation-Kern mit Klick-&-Start, Loopback-Backend, atomarer Config, Dashboard-Shell, Themes, Schriftgrößen-Presets, Tests, CI und Release-Builder.

### Verified

GitHub Actions Run `33020484403`: **SUCCESS**.

### Not yet verified

- reale Kubuntu-/Browser-Zielsystemgates.

## [0.1.0-foundation] — 2026-08-27

### Added

- saubere Projektgrundlage ohne Altcode.
- README, TODO, AGENTS, LAIEN-ANLEITUNG, TOOLBESCHREIBUNG, MANIFEST und REGRESSIONSINFOS.

### Changed

- Repository inhaltlich auf CLEAN FOUNDATION zurückgesetzt.

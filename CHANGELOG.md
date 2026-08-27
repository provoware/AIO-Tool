# CHANGELOG — AIO-Tool

## [Unreleased / 0.5.1-audit-modern-ui] — DEVELOPMENT — 2026-08-27

### Fixed

- Thread-Race in gemeinsam genutzter JSON-Persistenz durch serialisierte Read→Mutate→Write-Transaktionen geschlossen.
- Backup-Erneuerung ebenfalls atomar gemacht.
- `ConfigStore` von eigener doppelter Persistenzlogik auf den gemeinsamen Persistence-Core umgestellt.
- Hauptbackend auf denselben exakten Loopback-Host-/Port-Vertrag wie die Hilfsserver gebracht.
- Threaded Serverlog-Schreibzugriffe serialisiert.
- veralteten Kalender-/Termininhalt nach fehlgeschlagenem Reload entfernt.
- gespeicherten TODO-Aktionsfehler nach erfolgreichem Retry zurückgesetzt.
- sichtbaren Boot-Guard für READY und Startfehler verdrahtet.
- veraltete Kalender-Core-Beschreibung aus generischer Versionsregistrierung entfernt.

### Improved

- neues modernes Theme `Aurora Glass`.
- Steel Night, Trash Neon, Clean Light und High Contrast auf gemeinsamen semantischen Surface-/Accent-Vertrag überarbeitet.
- stärkere visuelle Hierarchie, ruhigere Schatten/Glasflächen, klarere Hover-/Focus-Zustände.
- Theme-, Schrift- und Modulwahl mit `aria-pressed`.
- Settings-Fokusführung und Kalender-Tabreihenfolge verbessert.
- dynamische Dashboard-/Helper-Inhalte ohne `innerHTML` aufgebaut.
- Native Runner und SAFE-FILE Simulator teilen nun `web/helper-ui.css`.
- Helper-CSP benötigt kein `unsafe-inline` für Styles mehr.

### Verification status

Aktuell **DEVELOPMENT / DEV**. Finale Unit-/Release-/Chromium-/Firefox-Gates für `0.5.1-audit-modern-ui` stehen aus.

## [0.5.0-native-acceptance-safe-file-sim] — TESTED (L0–L3) — 2026-08-27

- Native Acceptance Runner mit 18 realen L4-Prüfschritten.
- Release-Evidenz-Masterindex + versionierte Einzelevidenzdateien.
- SAFE-FILE Copy-Simulation mit `execution_enabled=false`.
- Failure-Matrix `SF-001` bis `SF-010` und Recovery-Vorvertrag.
- finaler Main-Commit `a4906e40648cec3fd6ddbeeb133bc41e02790aa4`, Main-CI `33040664746` erfolgreich.
- Native L4 bleibt separat offen; echte Datei-Ausführung bleibt gesperrt.

## [0.4.3-integrity-hardening] — TESTED

- Launcher-Instanzidentität, Runtime-Preflight, fail-closed Statusmodell, Documentation Guard, Release-End-to-End-Preflight und Cross-Browser-Gate.
- finaler Main-Commit `c8b80161e1770f8636d3e77d72b57f9c24723078`.
- Main-CI Run `33036217621` erfolgreich.

## Frühere Stände

Siehe `VERSION_REGISTRY.json` und `evidence/releases/*.json`.

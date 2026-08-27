# CHANGELOG — AIO-Tool

## [0.5.1-audit-modern-ui] — TESTED / BEWIESEN (L0–L3 auf main) — 2026-08-27

### Fixed

- Thread-Race in gemeinsam genutzter JSON-Persistenz durch serialisierte Read→Mutate→Write-Transaktionen geschlossen.
- Backup-Erneuerung atomar gemacht.
- `ConfigStore` auf den gemeinsamen Persistence-Core umgestellt.
- Hauptbackend auf denselben exakten Loopback-Host-/Port-Vertrag wie die Hilfsserver gebracht.
- Threaded Serverlog-Schreibzugriffe serialisiert.
- veralteten oder scheinbar leeren Kalender-/Termin-/TODO-/Ereignisinhalt nach fehlgeschlagenem Reload verhindert.
- gespeicherten TODO-Aktionsfehler nach erfolgreichem Retry zurückgesetzt.
- sichtbaren Boot-Guard für READY, Hinweise und Startfehler verdrahtet.
- Browser-Acceptance von doppelter CI-Implementierung auf einen kanonischen Harness reduziert.

### Improved

- neues modernes Theme `Aurora Glass` sowie überarbeitete Steel Night, Trash Neon, Clean Light und High Contrast Themes.
- stärkere visuelle Hierarchie, klarere Hover-/Focus-Zustände und `aria-pressed` für Auswahlzustände.
- Settings-Fokusführung und Kalender-Tabreihenfolge verbessert.
- dynamische Dashboard-/Helper-Inhalte ohne `innerHTML` aufgebaut.
- Native Runner und SAFE-FILE Simulator teilen `web/helper-ui.css`; Helper-CSP benötigt kein `unsafe-inline` für Styles.
- Refresh und Config-Speichern laufen single-flight mit sichtbarem `aria-busy`-Feedback.
- lokale Backendanfragen besitzen einen 8-Sekunden-Timeout mit verständlicher Fehlerhilfe.
- Theme-Vorschau rollt bei Speicherfehler auf den bestätigten Stand zurück.
- UI unterscheidet erfolgreich leer geladene Daten von technisch nicht verfügbaren Bereichen.
- Learning Memory auf 21 aktive strukturelle Regeln erweitert.

### Verification / Main-Beweis

- DEV-Run `33045348341`: Core/Release + Chromium + Firefox + Helper-UIs PASS.
- TESTED-Promotion `33045669222`: **138/138 Tests**, Guards, Runtime-ZIP/Preflight + Chromium + Firefox + Helper-UIs PASS.
- finaler Evidence-Sync `33047743876`: PASS.
- PR #9 Integrationsgate `33047885115`: PASS.
- Squash-Main-Commit: `ee6adcfd3427e8328920edaceb804e7b6655cdb8`.
- Main-CI `33048070879`: Core/Release + Chromium + Firefox + Native Runner + SAFE-FILE Helper-UI PASS.

Der frühe Promotion-ZIP-Hash `a7ab6d64…` wurde durch den anschließenden finalen Runtime-Metadaten-Sync der `VERSION_REGISTRY.json` erwartbar abgelöst. Der eingefrorene finale Feature-Head und der Squash-Main-Commit erzeugen identisch:

`SHA256 f8ffd88e2f3e40416f0d76b20786aa168cebb4e11fe3ef9d0eefa6dcf93b19ee`

Damit ist `0.5.1` für L0–L3 auf `main` **BEWIESEN**. Native Kubuntu L4 bleibt separat offen; echte SAFE-FILE-Dateimutation bleibt technisch gesperrt.

## [0.5.0-native-acceptance-safe-file-sim] — TESTED (L0–L3) — 2026-08-27

- Native Acceptance Runner mit 18 realen L4-Prüfschritten.
- Release-Evidenz-Masterindex + versionierte Einzelevidenzdateien.
- SAFE-FILE Copy-Simulation mit `execution_enabled=false`.
- Failure-Matrix `SF-001` bis `SF-010` und Recovery-Vorvertrag.
- finaler Main-Commit `a4906e40648cec3fd6ddbeeb133bc41e02790aa4`, Main-CI `33040664746` erfolgreich.

## [0.4.3-integrity-hardening] — TESTED

- Launcher-Instanzidentität, Runtime-Preflight, fail-closed Statusmodell, Documentation Guard, Release-End-to-End-Preflight und Cross-Browser-Gate.
- finaler Main-Commit `c8b80161e1770f8636d3e77d72b57f9c24723078`, Main-CI `33036217621` erfolgreich.

## Frühere Stände

Siehe `VERSION_REGISTRY.json` und `evidence/releases/*.json`.

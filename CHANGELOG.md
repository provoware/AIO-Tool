# CHANGELOG — AIO-Tool

## Repository-Metadaten / Manifest-Härtung — 2026-08-27

Diese Änderungen betreffen **keine Runtime-Datei** der eingefrorenen `0.5.1-audit-modern-ui`-Baseline. Produktversion, Runtime-Baseline-Commit und Runtime-ZIP-SHA256 bleiben unverändert.

### Fixed

- Begriffsdrift zwischen „Main-Commit“, aktuellem Repository-Head und tatsächlichem Runtime-Baseline-Commit beseitigt.
- irreführenden Native-L4-Fortschritt korrigiert: solange kein manueller Schritt bestätigt wurde, gilt **0/18 = 0 %**.
- doppelte manuelle Commit-/Hash-Wahrheiten in Statusdokumenten durch evidenzgetriebene Prüfung reduziert.
- semantische Unschärfe des historischen `generated_files`-Feldes aus Runtime-Manifest 1.3.0 dokumentiert, ohne die bewiesene Runtime nachträglich zu verändern.

### Improved

- `manifests/DEVELOPMENT_MANIFEST.json` auf `1.2.0` erweitert: Authority-Matrix, Statusdokumente, Evidenzdokumente, Policy-Dokumente und Invarianten.
- `manifests/README.md` als klare Erklärung der Manifest-/Wahrheitsebenen ergänzt.
- `scripts/manifest_guard.py` ergänzt, um Runtime-/repo-only-Überlappungen und Manifestdrift fail-closed zu erkennen.
- Release-Evidenz für 0.5.1 um `main_ci_run`, finalen Runtime-Source-Commit, Reproduzierbarkeitsnachweis und abgelöstes Vorartefakt präzisiert.
- `scripts/evidence_guard.py` validiert zusätzlich Wrapper-Digest, Main-CI-Zuordnung, Reproduzierbarkeitsdaten und abgelöste Artefakte.
- `scripts/documentation_guard.py` bezieht Pflichtdokumente aus dem Development-Manifest und prüft kanonischen Runtime-Commit/SHA gegen Release-Evidenz.
- Statusdokumente verwenden einheitlich **Runtime-Baseline**, **Repository-Metadaten**, **L0–L3 BEWIESEN**, **L4 OFFEN** und **SAFE-FILE GESPERRT**.

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

### Verification / Runtime-Baseline

Die kanonische Beweiskette liegt in `evidence/releases/0.5.1-audit-modern-ui.json`.

- Runtime-Baseline-Commit: `ee6adcfd3427e8328920edaceb804e7b6655cdb8`.
- Main-CI: `33048070879`.
- Runtime-ZIP SHA256: `f8ffd88e2f3e40416f0d76b20786aa168cebb4e11fe3ef9d0eefa6dcf93b19ee`.
- Chromium + Firefox + Helper-UIs: PASS.

Der frühere Promotion-ZIP-Hash `a7ab6d64…` ist als abgelöstes Vorartefakt dokumentiert. Der finale Feature-Runtime-Head und der Squash-Main-Commit erzeugen identisch den oben genannten Runtime-SHA256.

Damit ist die Runtime-Baseline für L0–L3 **BEWIESEN**. Native Kubuntu L4 bleibt **OFFEN**; echte SAFE-FILE-Ausführung bleibt **GESPERRT**.

## [0.5.0-native-acceptance-safe-file-sim] — TESTED (L0–L3) — 2026-08-27

- Native Acceptance Runner mit 18 realen L4-Prüfschritten.
- Release-Evidenz-Masterindex + versionierte Einzelevidenzdateien.
- SAFE-FILE Simulation mit `execution_enabled=false`.
- Failure-Matrix `SF-001` bis `SF-010` und Recovery-Vorvertrag.
- finaler Runtime-/Main-Commit `a4906e40648cec3fd6ddbeeb133bc41e02790aa4`, Main-CI `33040664746` erfolgreich.

## [0.4.3-integrity-hardening] — TESTED

- Launcher-Instanzidentität, Runtime-Preflight, fail-closed Statusmodell, Documentation Guard, Release-End-to-End-Preflight und Cross-Browser-Gate.
- finaler Runtime-/Main-Commit `c8b80161e1770f8636d3e77d72b57f9c24723078`, Main-CI `33036217621` erfolgreich.

## Frühere Stände

Siehe `VERSION_REGISTRY.json` und `evidence/releases/*.json`.

# MANIFEST — AIO-Tool

## Projekt

- **Name:** AIO-Tool
- **Aktueller automatisiert bewiesener Stand:** `0.5.0-native-acceptance-safe-file-sim` — 🟢 `tested / draft` für L0–L3
- **Native L4:** 🟡 offen und nur über reale Nutzerabnahme beweisbar
- **Backend:** Python-Standardbibliothek, Loopback-only
- **Telemetrie:** keine
- **SAFE-FILE-Ausführung:** technisch gesperrt (`EXECUTION_ENABLED=False`)

## Runtime-Architektur

### Produktkern

- `app/persistence.py` — atomare JSON-Persistenz.
- `app/version_registry.py` — Version/Status/Evidenzpflicht.
- `app/event_registry.py`, `app/todo_store.py`, `app/calendar_store.py` — bestehender Kern.
- `app/loopback_security.py` — Host/Origin müssen Loopback und denselben Port verwenden.

### Native Acceptance

- `app/native_acceptance.py` — 18-Schritt-Modell, Validierung, persistente Sitzung, Berichte.
- `scripts/native_acceptance_runner.py` — lokaler Runner auf Standardport 8778.
- `web/native-acceptance.html` + `.js` — geführte Oberfläche.
- `start_native_acceptance.sh` + `native_acceptance.desktop` — Laienstart.
- lokale Berichte unter `runtime/`.
- kein Auto-PASS; nur explizites PASS/FAIL/SKIP.

### SAFE-FILE Simulation

- `app/safe_file_sim.py` — rein lesende Vorprüfung, Failure-Matrix, Recovery-Vertrag.
- `scripts/safe_file_simulator.py` — lokaler Simulator auf Standardport 8779 mit kdialog/zenity.
- `web/safe-file-sim.html` + `.js` — Quelle → Ziel → Konflikt → Vorschau.
- `start_safe_file_simulation.sh` + `.desktop` — Laienstart.
- **keine Ausführungs-API und keine Copy-/Move-/Delete-Primitive**.

## SAFE-FILE-Sicherheitsvertrag

- `SIMULATION_ONLY=True`
- `EXECUTION_ENABLED=False`
- `mutation_performed=false`
- Symlink-Quellen/-Ziele gesperrt.
- einzelne normale Datei als simuliertes Quellmodell.
- Standard-Konfliktpolicy `skip`.
- spätere echte Copy benötigt Journal, Staging, Postvalidation, Crash-Recovery und verifiziertes Undo.

## Failure-Matrix

`SF-001` source_missing · `SF-002` source_not_file · `SF-003` source_symlink · `SF-004` target_missing · `SF-005` target_not_directory · `SF-006` target_symlink · `SF-007` target_not_writable · `SF-008` insufficient_space · `SF-009` destination_exists · `SF-010` same_source_destination.

## Release-Evidenz

Repository-only:

- `evidence/RELEASE_EVIDENCE_INDEX.json`
- `evidence/releases/<version>.json`
- `scripts/evidence_guard.py`

Jede TESTED-/höhere Registry-Version besitzt exakt eine Evidenzdatei. Historisch fehlende Werte werden `not-recorded`, niemals geraten.

## Transportvertrag

`manifests/RUNTIME_MANIFEST.json` Version **1.2.1** ist die positive Runtime-Allowlist.

Transportiert werden die neuen Native-Acceptance- und SAFE-FILE-Simulationsmodule, Starter, Webdateien und Referenzvorlagen. Nicht transportiert werden `evidence/`, Tests/Testdaten, Repository-Dokumentation, CI-Evidenz oder lokale Reports.

## Qualitätsebenen / Evidenz

- **L0:** Syntax/Schema — 🟢
- **L1:** Unit/Contract/Failure-Matrix/Evidence Guard — 🟢 DEV-Run `33038051967`, 113 Tests
- **L2:** Runtime-ZIP + frischer Runtime-Preflight — 🟢 DEV-Run `33038051967`
- **L3:** Dashboard + Native Runner + SAFE-FILE in Chromium/Firefox — 🟢 DEV-Run `33038051967`
- **L4:** echtes Kubuntu/Zoom/DPI/Tastatur — 🟡 offen

## Aktuell offen

- TESTED-Promotion-Commit erneut durch L0–L3,
- reale L4-Sitzung,
- persistentes Copy-Jobjournal,
- Staging/Postvalidation/Undo für echte Copy,
- jede echte Dateioperation.

# MANIFEST — AIO-Tool

## Projekt

- **Name:** AIO-Tool
- **Aktuelle Entwicklung:** `0.5.0-native-acceptance-safe-file-sim` — 🟠 `development / draft`
- **Letzter bewiesener Stand:** `0.4.3-integrity-hardening` — 🟢 `tested / draft`
- **Backend:** Python-Standardbibliothek, Loopback-only
- **Telemetrie:** keine
- **SAFE-FILE-Ausführung:** technisch gesperrt

## Runtime-Architektur

### Produktkern

- `app/persistence.py` — atomare JSON-Persistenz.
- `app/version_registry.py` — Version/Status/Evidenzpflicht.
- `app/event_registry.py`, `app/todo_store.py`, `app/calendar_store.py` — bestehender Kern.
- `app/loopback_security.py` — Host/Origin müssen Loopback **und denselben Port** verwenden.

### Native Acceptance

- `app/native_acceptance.py` — 18-Schritt-Modell, Validierung, persistente Sitzung, Berichte.
- `scripts/native_acceptance_runner.py` — eigener lokaler Runner auf Standardport 8778.
- `web/native-acceptance.html` + `.js` — Button-/Dialog-geführte Oberfläche.
- `start_native_acceptance.sh` + `native_acceptance.desktop` — Laienstart.
- lokale Daten: `runtime/native_acceptance.json`, `runtime/reports/native-acceptance-latest.*`.

### SAFE-FILE Simulation

- `app/safe_file_sim.py` — rein lesende Vorprüfung, Failure-Matrix, Recovery-Vertrag.
- `scripts/safe_file_simulator.py` — lokaler Simulator auf Standardport 8779, kdialog/zenity-Auswahl.
- `web/safe-file-sim.html` + `.js` — Quelle → Ziel → Konflikt → Vorschau.
- `start_safe_file_simulation.sh` + `.desktop` — Laienstart.
- **keine Ausführungs-API**.

## SAFE-FILE-Sicherheitskonstanten

- `SIMULATION_ONLY = True`
- `EXECUTION_ENABLED = False`
- `mutation_performed = false`
- Symlink-Quellen/-Ziele gesperrt.
- einzelne normale Datei als einziges simuliertes Quellmodell.
- Standard-Konfliktpolicy: `skip`.

## Failure-Matrix

`SF-001` source_missing · `SF-002` source_not_file · `SF-003` source_symlink · `SF-004` target_missing · `SF-005` target_not_directory · `SF-006` target_symlink · `SF-007` target_not_writable · `SF-008` insufficient_space · `SF-009` destination_exists · `SF-010` same_source_destination.

## Release-Evidenz

Repository-only:

- `evidence/RELEASE_EVIDENCE_INDEX.json`
- `evidence/releases/<version>.json`
- `scripts/evidence_guard.py`

Jede TESTED-/höhere Registry-Version muss exakt eine Evidenzdatei besitzen. Felder: Commit(s), CI-Runs, Artefakthashstatus, Browsermatrix, offene L4-Gates.

## Transportvertrag

`manifests/RUNTIME_MANIFEST.json` Version **1.2.1** ist die positive Runtime-Allowlist.

Neu transportiert werden die Native-Acceptance- und SAFE-FILE-Simulationsmodule, Starter und Weboberflächen. **Nicht** transportiert werden `evidence/`, Tests, Testdaten, Dokumentation, CI-Evidenz oder lokale Reports.

## Qualitätsebenen

- L0 Syntax/Schema
- L1 Unit/Contract/Failure-Matrix/Evidence Guard
- L2 gebautes Runtime-ZIP + frischer Runtime-Preflight
- L3 Chromium + Firefox
- L4 reale Native-Acceptance-Sitzung auf Kubuntu

## Aktuell offen

- finale automatisierte 0.5.0-Evidenz,
- reale L4-Sitzung,
- persistentes Copy-Jobjournal,
- Staging/Postvalidation/Undo für echte Copy,
- jede echte Dateioperation.

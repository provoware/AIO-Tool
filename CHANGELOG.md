# CHANGELOG — AIO-Tool

## [0.5.0-native-acceptance-safe-file-sim] — TESTED (L0–L3) — 2026-08-27

### Added

- Native Acceptance Runner mit 18 realen L4-Prüfschritten für Kubuntu, Anzeige, Tastatur und Firefox/Chromium × 100/125/150/175/200 %.
- persistente gemeinsame Abnahmesitzung und automatisch aktualisierte JSON-/TXT-Berichte.
- Release-Evidenz-Masterindex plus genau eine maschinenlesbare Datei je TESTED-/höherer Version.
- `scripts/evidence_guard.py` als blockierendes CI-Gate.
- SAFE-FILE Copy-Simulation mit kdialog-/zenity-Auswahladapter.
- Failure-Matrix `SF-001` bis `SF-010` und Recovery-Vorvertrag.
- versionierte Mustervorlagen/Negativfixtures für Native Acceptance und SAFE-FILE.
- zentrale exakte Loopback-Host-/Origin-/Port-Prüfung für lokale Hilfsserver.
- eigener Chromium-/Firefox-L3-Gate für Native Runner und SAFE-FILE-Oberfläche.

### Safety

- SAFE-FILE bleibt `simulation_only=true` und `execution_enabled=false`.
- kein `/api/execute` und keine Copy-/Move-/Delete-Primitive.
- Preview-Vertrag verlangt `mutation_performed=false`.
- Native Acceptance setzt keinen Schritt automatisch auf PASS.
- historische Evidenzlücken bleiben `not-recorded` statt erfunden.

### Verification

DEV-Head `6cf6754dcf5da88edb13ee34f2e99b4e22bca593`, GitHub Actions Run `33038051967`:

- 113/113 Unit-/Contracttests PASS,
- Foundation/Learning/Evidence/Documentation Guards PASS,
- Runtime-ZIP + frischer Runtime-Preflight PASS,
- Dashboard Chromium+Firefox PASS,
- Native Runner Chromium+Firefox PASS,
- SAFE-FILE Simulation Chromium+Firefox PASS.

Registry wurde deshalb auf `tested / draft` promoviert. **L4 bleibt separat offen** und echte Datei-Ausführung bleibt gesperrt. Der Promotion-Commit muss anschließend nochmals dieselben L0–L3-Gates bestehen.

## [0.4.3-integrity-hardening] — TESTED

- Launcher-Instanzidentität, Runtime-Preflight, fail-closed Statusmodell, Documentation Guard, Release-End-to-End-Preflight und Cross-Browser-Gate.
- finaler Main-Commit `c8b80161e1770f8636d3e77d72b57f9c24723078`.
- Main-CI Run `33036217621` erfolgreich.

## Frühere Stände

Siehe `VERSION_REGISTRY.json` und `evidence/releases/*.json`.

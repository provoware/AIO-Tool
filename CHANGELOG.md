# CHANGELOG — AIO-Tool

## [Unreleased / 0.5.0-native-acceptance-safe-file-sim] — 2026-08-27

### Added

- Native Acceptance Runner mit eigenem Loopback-Webassistenten.
- 18 reale L4-Prüfschritte für Kubuntu, Anzeige, Tastatur sowie Firefox/Chromium × 100/125/150/175/200 %.
- persistente Native-Acceptance-Sitzung und automatisch aktualisierte JSON-/TXT-Berichte.
- Browser-Öffnen über feste, shell-freie Kommandoliste.
- `evidence/RELEASE_EVIDENCE_INDEX.json` plus einzelne Evidenzdatei je TESTED-Version.
- `scripts/evidence_guard.py` als CI-Gate.
- SAFE-FILE Copy-Simulation mit kdialog-/zenity-Auswahladapter.
- zehnteilige Failure-Matrix `SF-001` bis `SF-010`.
- Recovery-Vorvertrag für späteres Journal, Postvalidation und geschütztes Undo.
- Mustervorlagen und negative Testdaten für Native Acceptance und SAFE-FILE-Simulation.
- zentrale `app/loopback_security.py` für exakten Host-/Origin-/Port-Vertrag der neuen lokalen Assistenten.

### Safety

- SAFE-FILE bleibt `simulation_only=true` und `execution_enabled=false`.
- kein `/api/execute`-Endpunkt.
- keine Copy-/Move-/Delete-Primitive im Simulator.
- Preview-Vertrag verlangt `mutation_performed=false`.
- Native Acceptance setzt keinen Schritt automatisch auf PASS.
- historische Evidenzlücken werden ausdrücklich `not-recorded` statt erfunden.

### Verification status

Aktuell **DEVELOPMENT / DEV**. Automatisierte Evidenz für diesen neuen Slice ist noch ausstehend.

## [0.4.3-integrity-hardening] — TESTED

- Launcher-Instanzidentität, Runtime-Preflight, fail-closed Statusmodell, Documentation Guard, Release-End-to-End-Preflight und Cross-Browser-Gate.
- finaler Main-Commit `c8b80161e1770f8636d3e77d72b57f9c24723078`.
- Main-CI Run `33036217621` erfolgreich.

## Frühere Stände

Siehe `VERSION_REGISTRY.json` und `evidence/releases/*.json`.

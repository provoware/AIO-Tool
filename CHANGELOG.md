# CHANGELOG — AIO-Tool

## [0.6.0-autostart-selfheal] — DEVELOPMENT / DRAFT — 2026-08-27

**Runtime-Baseline:** Die zuletzt bereits bewiesene Basis bleibt `0.5.1-audit-modern-ui`. Dieser Abschnitt beschreibt den neuen Entwicklungsslice `0.6.0-autostart-selfheal`; Native L4 bleibt **OFFEN**, SAFE-FILE-Ausführung **GESPERRT**.

### Added

- autonome `app.autostart`-Startroutine mit neun sichtbaren Checkpoints,
- automatische Portnormalisierung und freie Loopback-Portwahl,
- stale-PID-Bereinigung und Instanzprüfung,
- `app.runtime_health` für datensichere lokale Zustandsreparatur,
- Quarantäne beschädigter Haupt-/Backupdateien vor Wiederherstellung oder Reset,
- `app.runtime_recovery` für hashgebundene Reparatur unveränderlicher Release-Dateien,
- `RECOVERY_BASIS.zip` als deterministisches Build-Artefakt,
- Source-Checkout-Sperre gegen unbemerkte Recovery-Mutationen,
- Read-only-Spiegelung in einen benutzereigenen Zustandsbereich,
- `scripts/portable_entry.py` + gepinntes PyInstaller-Buildsystem,
- `scripts/failure_matrix.py`, `scripts/build_recovery_basis.py`, `scripts/build_portable.py`, `scripts/portable_smoke.py`,
- neue Unit-/Regressionstests für Self-Healing, Recovery und Pipelinevertrag.

### Changed

- Runtime-Manifest auf `2.0.0`: transportierte Basis, Build-Recovery und lokal erzeugter Zustand werden klar getrennt.
- Dokumentations-Guard unterscheidet nun korrekt `development` von bewiesenen Releasezuständen; Release-Evidenz wird nicht vorweggenommen.
- GitHub Actions ist strikt sequenziell: Core-CI → Failure-Matrix → Source-ZIP → RECOVERY_BASIS → Portable-Build → Portable-Smoke → Chromium → Firefox.

### Safety

- keine Systempaketreparatur, kein `sudo`, keine Paketmanager-Automation,
- Nutzerdaten werden vor Ersatz erhalten,
- Source-Checkouts werden durch Runtime-Recovery nicht verändert,
- Native Kubuntu L4 bleibt **OFFEN** und kann nicht durch CI simuliert werden,
- SAFE-FILE reale Ausführung bleibt technisch **GESPERRT**.

## [0.5.1-audit-modern-ui] — TESTED / BEWIESEN L0–L3 — 2026-08-27

Der letzte bereits bewiesene Runtime-Stand vor 0.6.0. Kanonische Details liegen in `evidence/releases/0.5.1-audit-modern-ui.json` und `VERSION_REGISTRY.json`.

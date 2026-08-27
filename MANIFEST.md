# MANIFEST — AIO-Tool

## Projekt

- **Name:** AIO-Tool
- **Aktueller Kandidat:** `0.5.1-audit-modern-ui` — 🟢 `tested / draft` für L0–L3; Promotion-CI noch offen
- **Letzter auf `main` bewiesener Stand:** `0.5.0-native-acceptance-safe-file-sim` — 🟢 `tested / draft` für L0–L3
- **Native L4:** 🟡 weiterhin real offen
- **Backend:** Python-Standardbibliothek, Loopback-only
- **Telemetrie:** keine
- **SAFE-FILE-Ausführung:** technisch gesperrt (`EXECUTION_ENABLED=False`)

## Audit-Härtung 0.5.1

- `app/persistence.py` — atomare und innerhalb eines Prozesses thread-sichere JSON-Transaktionen; atomarer Backup-Refresh.
- `app/config.py` — gemeinsame Persistence-Implementierung statt duplizierter Schreiblogik; fünf Theme-IDs inkl. `aurora-glass`.
- `app/loopback_security.py` + `app/server.py` — ein kanonischer exakter Loopback-Host-/Port-Vertrag.
- `web/styles.css` — semantische Surface-/Accent-Tokens und fünf moderne Themes.
- `web/helper-ui.css` — gemeinsame moderne Oberfläche für Native Runner und SAFE-FILE Simulator.
- `web/app.js` — Timeout, Single-Flight, Nicht-verfügbar-/Leer-Trennung, Retry-, Boot-, Fokus- und ARIA-Härtung.
- `scripts/ui_acceptance.py` — einzige kanonische Browser-Acceptance-Implementierung mit Produktasset-Erkennung.
- `scripts/ui_acceptance_ci.py` — absichtlich nur dünner CI-Entry-Point.
- `tests/test_persistence.py` — parallele Update-Regression.
- `tests/test_dashboard_contract.py`, `tests/test_helper_ui_contract.py`, `tests/test_ui_acceptance_harness.py` — UI-/A11y-/DOM-/Theme-/Harness-Verträge.

## Runtime-Transport

Verbindliche positive Allowlist: `manifests/RUNTIME_MANIFEST.json` Version `1.3.0`. Dokumentation, Tests, Evidenz und Logs bleiben Repo-/lokal. Das Runtime-ZIP enthält weiterhin nur die vollständige Betriebsbasis plus generiertes `MANIFEST_RELEASE.json`.

## Statusgrenzen

DEV-Head `e9803086da790f30f8155946539569dd33c395b5` hat Run `33045348341` vollständig bestanden: Core/Release, Chromium, Firefox, Native Runner und SAFE-FILE-Hilfsoberfläche. Deshalb wurde `0.5.1-audit-modern-ui` auf `tested / draft` promoviert. **Der Promotion-Commit muss denselben vollständigen Gate erneut bestehen**, bevor Artefakthash und Merge-Evidenz als abgeschlossen gelten. Native L4 wird daraus nicht abgeleitet. SAFE-FILE Copy/Move/Delete bleibt gesperrt.

# MANIFEST — AIO-Tool

## Projekt

- **Name:** AIO-Tool
- **Aktueller Kandidat:** `0.5.1-audit-modern-ui` — 🟢 `tested / draft` für L0–L3
- **TESTED-Evidenz:** DEV `33045348341`, Promotion `33045669222`
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

## TESTED-Artefakt

- Runtime-ZIP: `AIO-Tool-0.5.1-audit-modern-ui-TESTED.zip`
- SHA256: `a7ab6d64e978e27c1fa550c549e12dc7ee21e24a17a55fd9c160c19cd3001b72`
- GitHub-Artefakt-Digest: `62cc0787280328c1bfe5ff08628ea87ed1ec251bf718bf82178e2cfca88a85e0`

## Statusgrenzen

`0.5.1-audit-modern-ui` ist für L0–L3 **GEPRÜFT / tested / draft**. Der aktuelle verbleibende Abschlussweg enthält ausschließlich Metadaten- und Integrationsschritte: Evidence-/Dokumentations-Sync prüfen, PR per Squash nach `main`, Main-CI und abschließenden Main-Runtime-ZIP-Hashvergleich. Native L4 wird daraus ausdrücklich nicht abgeleitet. SAFE-FILE Copy/Move/Delete bleibt gesperrt.

# MANIFEST — AIO-Tool

## Projekt

- **Name:** AIO-Tool
- **Aktuelle Entwicklung:** `0.5.1-audit-modern-ui` — 🟠 `development / draft`
- **Letzter bewiesener Stand:** `0.5.0-native-acceptance-safe-file-sim` — 🟢 `tested / draft` für L0–L3
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
- `web/app.js` — stale-state-, Retry-, Boot-, Fokus- und ARIA-Härtung.
- `tests/test_persistence.py` — parallele Update-Regression.
- `tests/test_dashboard_contract.py` / `tests/test_helper_ui_contract.py` — UI-/A11y-/DOM-/Theme-Verträge.

## Runtime-Transport

Verbindliche positive Allowlist: `manifests/RUNTIME_MANIFEST.json` Version `1.3.0`. Dokumentation, Tests, Evidenz und Logs bleiben Repo-/lokal. Das Runtime-ZIP enthält weiterhin nur die vollständige Betriebsbasis plus generiertes `MANIFEST_RELEASE.json`.

## Statusgrenzen

`0.5.1-audit-modern-ui` bleibt **DEV**, bis Core-/Release-, Evidence-/Documentation- und Chromium-/Firefox-Gates auf demselben Commit erfolgreich sind. Native L4 wird daraus nicht abgeleitet. SAFE-FILE Copy/Move/Delete bleibt gesperrt.

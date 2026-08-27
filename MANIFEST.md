# MANIFEST — AIO-Tool

## Projekt

- **Name:** AIO-Tool
- **Aktueller Main-Stand:** `0.5.1-audit-modern-ui` — 🟢 `tested / draft`, **BEWIESEN L0–L3 auf main**
- **Main-Commit:** `ee6adcfd3427e8328920edaceb804e7b6655cdb8`
- **Main-CI:** `33048070879` — vollständig grün
- **Native L4:** 🟡 weiterhin real offen
- **Backend:** Python-Standardbibliothek, Loopback-only
- **Telemetrie:** keine
- **SAFE-FILE-Ausführung:** technisch gesperrt (`EXECUTION_ENABLED=False`)

## Audit-Härtung 0.5.1

- `app/persistence.py` — atomare, thread-sichere JSON-Transaktionen und atomarer Backup-Refresh.
- `app/config.py` — gemeinsame Persistence-Implementierung und fünf Theme-IDs inkl. `aurora-glass`.
- `app/loopback_security.py` + `app/server.py` — kanonischer exakter Loopback-Host-/Port-Vertrag.
- `web/styles.css` — semantische Surface-/Accent-Tokens und fünf moderne Themes.
- `web/helper-ui.css` — gemeinsame moderne Oberfläche für Native Runner und SAFE-FILE Simulator.
- `web/app.js` — Timeout, Single-Flight, Nicht-verfügbar-/Leer-Trennung, Retry-, Boot-, Fokus- und ARIA-Härtung.
- `scripts/ui_acceptance.py` — einzige kanonische Browser-Acceptance-Implementierung.
- `scripts/ui_acceptance_ci.py` — ausschließlich dünner CI-Entry-Point.
- Regressionstests sichern Persistenzparallelität, Dashboard-/A11y-/Theme-Verträge und Harness-Single-Source.

## Runtime-Transport

Verbindliche positive Allowlist: `manifests/RUNTIME_MANIFEST.json` Version `1.3.0`. Dokumentation, Tests und `evidence/` sind ausdrücklich repo-only und verändern das Runtime-ZIP nicht.

## Finales Main-Artefakt

- Runtime-ZIP: `AIO-Tool-0.5.1-audit-modern-ui-TESTED.zip`
- finaler Runtime-SHA256: `f8ffd88e2f3e40416f0d76b20786aa168cebb4e11fe3ef9d0eefa6dcf93b19ee`
- Main-GitHub-Artefakt-Digest: `95238af6cae63091262fbaf2aea6ce267c71fd16eeefcebde56d97f3b482d71b`

Der Hash ist reproduzierbar: der eingefrorene finale Feature-Head `3dec31d22110f738c9964b937a53ddfe251a4d79` und der Squash-Main-Commit erzeugen denselben Runtime-SHA256. Der ältere Promotion-Hash `a7ab6d64…` stammt vom Stand vor dem letzten Runtime-Metadaten-Sync der `VERSION_REGISTRY.json` und ist deshalb nicht der finale Main-Artefakthash.

## Statusgrenzen

`0.5.1-audit-modern-ui` ist für L0–L3 **BEWIESEN**. Native L4 wird daraus ausdrücklich nicht abgeleitet. SAFE-FILE Copy/Move/Delete bleibt gesperrt. Der nächste aktive Qualitätsweg ist ausschließlich die reale Kubuntu-L4-Abnahme.

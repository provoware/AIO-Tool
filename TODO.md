# TODO — AIO-Tool

## Aktueller Stand

**🟠 `0.5.1-audit-modern-ui` — DEVELOPMENT / DEV**

Letzter vollständig bewiesener Stand: **🟢 `0.5.0-native-acceptance-safe-file-sim-TESTED`**.

## Fortschritt

```text
Projektweiter Audit              ████████████████████ 100 % durchgeführt
Persistenz-/Thread-Härtung       ████████████████████ 100 % umgesetzt
Loopback-Vertragskonsolidierung  ████████████████████ 100 % umgesetzt
Dashboard-Zustandshärtung        ████████████████████ 100 % umgesetzt
Moderne Theme-Architektur        ████████████████████ 100 % umgesetzt
Helper-UI Modernisierung         ████████████████████ 100 % umgesetzt
Neue Regressionstests            ████████████████████ 100 % umgesetzt
Finale CI / Cross-Browser        ░░░░░░░░░░░░░░░░░░░░ offen
Native Kubuntu L4                ░░░░░░░░░░░░░░░░░░░░ real offen
SAFE-FILE echte Copy             ░░░░░░░░░░░░░░░░░░░░ gesperrt
```

## P0/P1 — aktueller Slice

- [x] neue Version nach eingefrorenem `0.5.0-TESTED` angelegt.
- [x] AtomicJsonStore gegen parallele Thread-Updates gehärtet.
- [x] ConfigStore auf gemeinsamen Persistence-Core konsolidiert.
- [x] Hauptbackend auf kanonischen exakten Loopback-Port-Vertrag umgestellt.
- [x] Serverlog im Threading-Backend serialisiert.
- [x] stale Kalender-/Upcoming-Darstellung bei Ladefehlern verhindert.
- [x] klebenden TODO-Aktionsfehler nach erfolgreichem Retry entfernt.
- [x] Boot-Guard mit READY-/ERROR-Pfad umgesetzt.
- [x] Theme-/Font-/Modulauswahl mit `aria-pressed` ergänzt.
- [x] Aurora Glass + vier überarbeitete Themes umgesetzt.
- [x] Native Runner und SAFE-FILE Simulator auf gemeinsames modernes Helper-UI umgestellt.
- [x] `unsafe-inline` aus Helper-CSP entfernt.
- [x] neue Persistenz-, Theme-, Helper-UI- und A11y-Regressionen angelegt.
- [ ] kompletter DEV-Gate grün.
- [ ] Chromium + Firefox grün.
- [ ] erst danach TESTED-Promotion mit Evidenzdatei.

## Danach

1. **Native L4 real auf Kubuntu** mit dem Acceptance Runner durchführen.
2. **SAFE-FILE Recovery-Simulation** vertiefen; echte Copy bleibt bis zu eigenem evidenzgebundenen Slice gesperrt.

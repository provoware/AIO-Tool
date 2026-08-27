# TODO — AIO-Tool

## Aktueller Stand

**🟢 `0.5.1-audit-modern-ui` — TESTED / draft für L0–L3**

Promotion-Evidenz: DEV-Run `33045348341`, TESTED-Promotion `33045669222`. Evidence-Sync/Main-Merge sind noch offen.

## Fortschritt

```text
Projektweiter Audit              ████████████████████ 100 % 🟢
Persistenz-/Thread-Härtung       ████████████████████ 100 % 🟢
Loopback-Vertragskonsolidierung  ████████████████████ 100 % 🟢
Dashboard-Zustand/Feedback       ████████████████████ 100 % 🟢
Moderne Theme-Architektur        ████████████████████ 100 % 🟢
Helper-UI Modernisierung         ████████████████████ 100 % 🟢
Code-/Harness-Konsolidierung     ████████████████████ 100 % 🟢
138 Unit-/Contracttests          ████████████████████ 100 % 🟢
Chromium + Firefox               ████████████████████ 100 % 🟢
TESTED-Promotion                 ████████████████████ 100 % 🟢
Evidence-Sync / Main-Merge       ████████████████░░░░  80 % 🟡
Native Kubuntu L4                ░░░░░░░░░░░░░░░░░░░░ real offen 🟡
SAFE-FILE echte Copy             ░░░░░░░░░░░░░░░░░░░░ gesperrt 🔒
```

## Erledigt in 0.5.1

- [x] neue Version nach eingefrorenem `0.5.0-TESTED` angelegt.
- [x] AtomicJsonStore gegen parallele Thread-Updates gehärtet.
- [x] ConfigStore auf gemeinsamen Persistence-Core konsolidiert.
- [x] Hauptbackend auf kanonischen exakten Loopback-Port-Vertrag umgestellt.
- [x] Serverlog im Threading-Backend serialisiert.
- [x] stale/uneindeutige Kalender-, Termin-, TODO- und Ereigniszustände verhindert.
- [x] Refresh/Config single-flight + `aria-busy` + 8-s-Timeout umgesetzt.
- [x] Theme-Vorschau mit Rollback bei Speicherfehler umgesetzt.
- [x] Boot-Guard mit READY-/Hinweis-/ERROR-Pfad umgesetzt.
- [x] Theme-/Font-/Modulauswahl mit `aria-pressed` ergänzt.
- [x] Aurora Glass + vier überarbeitete Themes umgesetzt.
- [x] Native Runner und SAFE-FILE Simulator auf gemeinsames modernes Helper-UI umgestellt.
- [x] `unsafe-inline` aus Helper-CSP entfernt.
- [x] Browser-Harness auf eine kanonische Implementierung reduziert.
- [x] 21 strukturelle Learning-Regeln aktiv.
- [x] kompletter DEV-Gate grün (`33045348341`).
- [x] Chromium + Firefox grün.
- [x] TESTED-Promotion vollständig grün (`33045669222`).
- [x] TESTED-ZIP SHA256 aufgezeichnet: `a7ab6d64e978e27c1fa550c549e12dc7ee21e24a17a55fd9c160c19cd3001b72`.
- [ ] reinen Evidence-Sync erneut grün prüfen.
- [ ] PR per Squash nach `main` und Main-CI abschließen.

## Danach

1. **Native L4 real auf Kubuntu** mit dem Acceptance Runner durchführen.
2. **SAFE-FILE Recovery-Simulation** vertiefen; echte Copy bleibt bis zu eigenem evidenzgebundenen Slice gesperrt.

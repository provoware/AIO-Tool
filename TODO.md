# TODO — AIO-Tool

## Aktueller Stand

**🟢 `0.5.1-audit-modern-ui` — BEWIESEN / TESTED / draft für L0–L3 auf `main`**

Main-Commit: `ee6adcfd3427e8328920edaceb804e7b6655cdb8`  
Main-CI: `33048070879` — vollständig grün.

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
Evidence-Sync                    ████████████████████ 100 % 🟢
PR / Squash-Merge                ████████████████████ 100 % 🟢
Main-CI / Runtime-Reproduktion   ████████████████████ 100 % 🟢
Native Kubuntu L4                ░░░░░░░░░░░░░░░░░░░░ real offen 🟡
SAFE-FILE echte Copy             ░░░░░░░░░░░░░░░░░░░░ gesperrt 🔒
```

## Erledigt in 0.5.1

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
- [x] TESTED-Promotion grün (`33045669222`).
- [x] finaler Evidence-Sync grün (`33047743876`).
- [x] PR-Integrationsgate grün (`33047885115`).
- [x] PR #9 per Squash nach `main` gemergt.
- [x] Main-CI vollständig grün (`33048070879`).
- [x] finaler Runtime-ZIP reproduzierbar: Feature-Head und Main jeweils SHA256 `f8ffd88e2f3e40416f0d76b20786aa168cebb4e11fe3ef9d0eefa6dcf93b19ee`.

## Jetzt — Native L4

1. **Native Acceptance Runner auf echtem Kubuntu starten.**
2. Firefox und Chromium/Chrome real prüfen.
3. Browserzoom 100–200 %, Display-/KDE-Skalierung und Tastaturbedienung nach Runner-Schritten bestätigen.
4. Jeden Schritt ausschließlich nach echter Beobachtung als `pass`, `fail` oder `skip` markieren.
5. FAIL-Befunde erhalten und vor einer Statusverbesserung analysieren.

## Sicherheitsgrenze

SAFE-FILE bleibt unverändert Simulation. **Keine echte Copy/Move/Delete-Ausführung freischalten**, bevor ein eigener evidenzgebundener Recovery-/Execution-Slice dafür angelegt wurde.

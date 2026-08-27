# TODO — AIO-Tool

## Aktueller Stand

**🟠 `0.5.0-native-acceptance-safe-file-sim` — DEVELOPMENT / DEV**

Letzter vollständig bewiesener Stand: **🟢 `0.4.3-integrity-hardening-TESTED`**.

### Fortschritt

```text
Native Acceptance Runner       ████████████████████ 100 % umgesetzt
Release Evidence Index         ████████████████████ 100 % umgesetzt
Evidence Guard                 ████████████████████ 100 % umgesetzt
SAFE-FILE Simulation           ████████████████████ 100 % umgesetzt
Failure-Matrix SF-001..010      ████████████████████ 100 % umgesetzt
Recovery-Vorvertrag            ████████████████████ 100 % umgesetzt
Automatisierte Tests/CI        ░░░░░░░░░░░░░░░░░░░░   0 % final offen
Native Kubuntu L4              ░░░░░░░░░░░░░░░░░░░░   0 % real offen
Copy-Ausführung                ░░░░░░░░░░░░░░░░░░░░   0 % gesperrt
```

## P0/P1 — aktueller Slice

- [x] neue Version nach eingefrorenem `0.4.3-TESTED` angelegt.
- [x] Native Acceptance Runner mit 18 Prüfschritten.
- [x] PASS/FAIL/SKIP nur durch explizite Nutzerentscheidung.
- [x] gemeinsame persistente Sitzung für Firefox/Chromium.
- [x] automatische JSON-/TXT-Abnahmeberichte.
- [x] browserbezogene Umgebungsdaten erfassen, ohne Zoom automatisch vorzutäuschen.
- [x] lokale Host-/Origin-Prüfung inklusive exaktem Port.
- [x] Evidence Masterindex + Einzeldatei pro TESTED-Version.
- [x] historische Evidenzlücken als `not-recorded`, nicht erfunden.
- [x] Evidence Guard gegen Versionsregistry.
- [x] SAFE-FILE Quelle/Ziel über Dialogadapter.
- [x] Copy-Vorschau mit Speicherplatz, Konflikt, Symlink- und Same-Target-Prüfung.
- [x] Failure-Matrix SF-001 bis SF-010.
- [x] Recovery-Vorvertrag.
- [x] `execution_enabled=false` und kein Execute-Endpunkt.
- [ ] finale Unit-/Contract-/Failure-/Evidence-Tests grün.
- [ ] Runtime-ZIP End-to-End-Preflight grün.
- [ ] Chromium + Firefox L3 auf finalem Head grün.
- [ ] erst dann `0.5.0` zu TESTED promoten, falls der Slice vollständig bewiesen ist.

## L4 — reale Native-Abnahme

Nach grünem DEV-/TESTED-Build mit `native_acceptance.desktop`:

- [ ] Kubuntu Desktop-Starter.
- [ ] Shell-Starter.
- [ ] passende Instanz wiederverwenden.
- [ ] Fremdport/Fallback.
- [ ] kleine Anzeige.
- [ ] Full-HD.
- [ ] große Anzeige.
- [ ] Tastatur-only.
- [ ] Firefox 100/125/150/175/200 %.
- [ ] Chrome/Chromium 100/125/150/175/200 %.
- [ ] JSON-/TXT-Bericht sichern.
- [ ] reale FAIL-Befunde jeweils als Regression + Learning Memory übernehmen.

## SAFE-FILE — Freigabebedingungen für echte Copy

Vor einem späteren `execution_enabled=true` müssen in **neuem Versionsslice** bewiesen sein:

- [ ] alle SF-001..010 Tests grün auf finalem Head.
- [ ] persistentes Jobjournal vor Mutation.
- [ ] Staging-/Partial-Copy-Konzept.
- [ ] Nachvalidierung Größe + optional Hash.
- [ ] `DONE` erst nach persistierter Nachvalidierung.
- [ ] Crash-/Abbruch-/Neustarttests.
- [ ] Undo nur wenn Ziel seit Copy unverändert.
- [ ] echte Copy zunächst nur einzelne normale Datei.
- [ ] Move/Rename/Delete weiterhin gesperrt.

## Nächster Schritt

**Jetzt keine echte Dateioperation hinzufügen. Zuerst den vollständigen `0.5.0`-DEV-Slice automatisiert prüfen und jeden roten Befund minimal beheben.**

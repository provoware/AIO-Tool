# TODO — AIO-Tool

## Aktueller Stand

**🟢 `0.5.0-native-acceptance-safe-file-sim` — TESTED / draft (L0–L3)**

Automatisierte DEV-Evidenz: GitHub Actions Run `33038051967`, DEV-Head `6cf6754dcf5da88edb13ee34f2e99b4e22bca593`.

```text
Native Acceptance Runner       ████████████████████ 100 % 🟢
Release Evidence Index         ████████████████████ 100 % 🟢
Evidence Guard                 ████████████████████ 100 % 🟢
SAFE-FILE Simulation           ████████████████████ 100 % 🟢
Failure-Matrix SF-001..010     ████████████████████ 100 % 🟢
Recovery-Vorvertrag            ████████████████████ 100 % 🟢
DEV L0–L3 CI                   ████████████████████ 100 % 🟢
TESTED-Promotion-CI            ░░░░░░░░░░░░░░░░░░░░   0 % 🟠 läuft als nächster Gate
Native Kubuntu L4              ░░░░░░░░░░░░░░░░░░░░   0 % 🟡 real offen
Copy-Ausführung                ░░░░░░░░░░░░░░░░░░░░   0 % 🔒 gesperrt
```

## Automatisiert umgesetzt und DEV-geprüft

- [x] 18 Native-Acceptance-Schritte ohne Auto-PASS.
- [x] persistente gemeinsame Sitzung für Firefox/Chromium.
- [x] JSON-/TXT-Berichte.
- [x] exakter Loopback-Host-/Origin-/Portvertrag.
- [x] eine Evidenzdatei je bewiesener Version + Masterindex.
- [x] historische Evidenzlücken explizit `not-recorded`.
- [x] SAFE-FILE Quelle/Ziel über kdialog/zenity.
- [x] Speicherplatz-/Symlink-/Konflikt-/Same-Target-Vorprüfung.
- [x] Failure-Matrix SF-001..010.
- [x] Recovery-Vorvertrag.
- [x] `execution_enabled=false`, kein Execute-Endpunkt, keine Copy-/Move-/Delete-Primitive.
- [x] 113 Unit-/Contracttests im DEV-Gate.
- [x] Native-/SAFE-FILE-UI in Chromium + Firefox auf 1280/360 CSS-px.
- [ ] TESTED-Promotion-Commit erneut L0–L3 vollständig grün.

## L4 — danach real auf Kubuntu

- [ ] Desktop-Starter und Shell-Starter.
- [ ] passende Instanz wiederverwenden.
- [ ] fremd belegter Port / Fallback.
- [ ] kleine / Full-HD / große Anzeige.
- [ ] Tastatur-only.
- [ ] Firefox 100/125/150/175/200 %.
- [ ] Chrome/Chromium 100/125/150/175/200 %.
- [ ] JSON-/TXT-Bericht sichern.
- [ ] jeden realen FAIL-Befund als Regression + Learning Memory behandeln.

## Vor echter Copy zwingend

- [ ] L4-Befunde ausgewertet.
- [ ] persistentes Jobjournal vor Mutation.
- [ ] Staging-/Partial-Copy-Vertrag.
- [ ] Postvalidation vor `DONE`.
- [ ] Crash/Abbruch/Neustart-Recovery.
- [ ] Undo nur bei unverändertem erzeugtem Ziel.
- [ ] neuer Versionsslice für Copy-only.
- [ ] Move/Rename/Delete weiterhin gesperrt.

## Nächster Schritt

**TESTED-Promotion vollständig erneut prüfen. Danach reale L4-Abnahme mit dem Native Acceptance Runner; noch keine echte Dateioperation implementieren.**

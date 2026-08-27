# TODO — AIO-Tool

## Aktueller Stand

**🟠 `0.4.3-integrity-hardening` — DEVELOPMENT**

Letzter vollständig bewiesener Vorgänger: **🟢 `0.4.2-ui-acceptance-TESTED`** mit Core-/Release-Gate und Chromium+Firefox-Acceptance in GitHub Actions Run `33032999752`.

### Fortschritt 0.4.3

```text
Audit / Befundaufnahme          ████████████████████ 100 %
Launcher-Instanzhärtung         ████████████████████ 100 %
Runtime-Transportvertrag        ████████████████████ 100 %
Statusmodell                    ████████████████████ 100 %
Regressionstests                ████████████████████ 100 %
Dokumentationssynchronisierung  ████████████████████ 100 %
Finale CI / Browser-Evidenz     ░░░░░░░░░░░░░░░░░░░░   0 %
TESTED-Promotion                ░░░░░░░░░░░░░░░░░░░░   0 %
```

## P0/P1 — vor jeder neuen Funktion

- [x] `0.4.2-TESTED` als historischen evidenzgebundenen Stand einfrieren.
- [x] neuen Patchstand als `0.4.3-integrity-hardening / development` registrieren.
- [x] Launcher darf nicht mehr jedes HTTP 200 als eigene Instanz übernehmen.
- [x] konkrete Installationskennung + Version + Ready/Loopback prüfen.
- [x] fremd belegten Standardport transparent auf freien Loopback-Port umleiten.
- [x] normaler Runtime-Start nutzt `runtime_preflight.py`, nicht Repo-`validate.py`.
- [x] Launcher-/Eventlogs lokal begrenzen/rotieren.
- [x] Status- und Releasevokabular vereinheitlichen und widersprüchliche Paare ablehnen.
- [x] gebautes Runtime-ZIP als End-to-End-Test entpacken und darin Preflight starten.
- [x] README/AGENTS auf aktuellen Vertrag umbauen.
- [x] TODO/CHANGELOG/MANIFEST/REGRESSIONS/LAIEN-ANLEITUNG/TOOLBESCHREIBUNG synchronisiert.
- [ ] komplette GitHub-CI auf finalem 0.4.3-Head grün.
- [ ] Chromium + Firefox auf finalem 0.4.3-Head grün.
- [ ] erst danach Evidenz in Registry eintragen und auf `tested / draft` setzen.
- [ ] Promotion-Commit erneut komplett grün prüfen.

## Bereits bewiesene Basis

- [x] atomare Config + Backup-Fallback.
- [x] Loopback Host-/Origin-Schutz.
- [x] VersionRegistry + Evidenzpflicht.
- [x] EventRegistry.
- [x] TODO-Core + Titelgedächtnis + Erledigt-Archiv.
- [x] Calendar-Core + Monat/Woche/Jahr + Reminder + `zoneinfo`/DST.
- [x] Dashboard V2 mit Monatskalender, nächsten TODOs/Terminen und letzten Ereignissen.
- [x] Reminder nur nach sichtbarer Nutzerquittierung.
- [x] 12-Spalten-Raster + Browser-Reflow bis 320 CSS-px.
- [x] Chromium-/Firefox-Acceptance-Pipeline.
- [x] positive Runtime-Allowlist + `MANIFEST_RELEASE.json`.
- [x] Status im Release-Dateinamen.
- [x] versionierte Texte/Fehlerregeln und Mustervorlagen.
- [x] `LEARNING_MEMORY.jsonl` + Guard.

## Native Zielsystemabnahme — danach

- [ ] TESTED-ZIP in frischen Ordner auf Kubuntu entpacken.
- [ ] `start_tool.desktop` und `start_tool.sh` real prüfen.
- [ ] vorhandene passende Instanz wiederverwenden.
- [ ] fremd belegten Port / sicheren Ausweichport real prüfen.
- [ ] Firefox + Chrome/Chromium: Start, Kalender, TODO, Reminder, Einstellungen.
- [ ] 100 / 125 / 150 / 175 / 200 % Browserzoom.
- [ ] KDE-/DPI-Skalierung und kleine / Full-HD / große Fenster.
- [ ] reiner Tastaturdurchlauf und Fokusreihenfolge.
- [ ] reale Befunde als Regression + Learning Memory aufnehmen.

## SAFE-FILE-CORE — erst nach Zielsystemgate

- [ ] Copy als erste reale Dateioperation.
- [ ] Quelle/Ziel möglichst über Auswahl statt Pfadeingabe.
- [ ] Existenz, Lesbarkeit, Schreibbarkeit, freier Speicher und Konflikte vorab prüfen.
- [ ] Vorschau und klare Auswirkung vor Änderung.
- [ ] persistenter Jobstatus.
- [ ] Nachprüfung gegen erwartetes Ergebnis.
- [ ] Undo-/Recovery-Datensatz.
- [ ] Abbruch/Neustart robust behandeln.
- [ ] erst danach Move, Rename und Papierkorb/Delete.

## Job & Recovery — später

- [ ] persistente Job-Queue.
- [ ] `DONE` erst nach Persistenz + Nachprüfung.
- [ ] Pause / Abbruch / Wiederaufnahme.
- [ ] Recovery Center mit Checkpoints.

## Empfohlener nächster Schritt

**Keine neue Nutzfunktion. Jetzt den vollständigen Core-/Release-/Browser-Gate auf dem finalen 0.4.3-Entwicklungshead ausführen und nur bei grünem Ergebnis zu TESTED promovieren.**

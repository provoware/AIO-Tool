# TODO — AIO-Tool

## Aktueller Stand

**🟢 `0.4.3-integrity-hardening` — TESTED / DRAFT**

Finaler Entwicklungshead: GitHub Actions Run `33034359454` — **Core/Release + Chromium + Firefox SUCCESS**.

### Fortschritt 0.4.3

```text
Audit / Befundaufnahme          ████████████████████ 100 %
Launcher-Instanzhärtung         ████████████████████ 100 %
Runtime-Transportvertrag        ████████████████████ 100 %
Statusmodell                    ████████████████████ 100 %
Regressionstests                ████████████████████ 100 %
Dokumentationssynchronisierung  ████████████████████ 100 %
Finale CI / Browser-Evidenz     ████████████████████ 100 %
TESTED-Promotion                ████████████████░░░░  80 %  Promotion-Revalidierung läuft
```

## P0/P1 — Integritätshärtung

- [x] `0.4.2-TESTED` als historischen Evidenzstand einfrieren.
- [x] neuen Patchstand als `0.4.3-integrity-hardening` führen.
- [x] Launcher übernimmt nicht mehr jedes HTTP 200 als eigene Instanz.
- [x] Version + Ready/Loopback + konkrete Installationskennung prüfen.
- [x] fremd belegten Standardport transparent auf freien Loopback-Port umleiten.
- [x] ungültigen Port / unbekannten Probe-Status fail-closed behandeln.
- [x] normaler Runtime-Start nutzt `runtime_preflight.py`, nicht Repo-`validate.py`.
- [x] Launcher-/Eventlogs lokal begrenzen/rotieren.
- [x] Status-/Releasevokabular vereinheitlichen und widersprüchliche Paare ablehnen.
- [x] Runtime-ZIP bauen → entpacken → Preflight aus dem ZIP ausführen.
- [x] Documentation Guard gegen Versions-/Statusdrift.
- [x] README/AGENTS/TODO/CHANGELOG/MANIFEST/REGRESSIONS/LAIEN-ANLEITUNG/TOOLBESCHREIBUNG synchronisieren.
- [x] Core-/Release-Gate auf finalem Entwicklungshead grün.
- [x] Chromium + Firefox auf finalem Entwicklungshead grün.
- [x] Evidenz Run `33034359454` in Registry eintragen und auf `tested / draft` setzen.
- [ ] Promotion-Commit erneut vollständig grün prüfen.

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

## Native Zielsystemabnahme — nächster Slice

- [ ] `AIO-Tool-0.4.3-integrity-hardening-TESTED.zip` in frischen Ordner auf Kubuntu entpacken.
- [ ] `start_tool.desktop` und `start_tool.sh` real prüfen.
- [ ] passende laufende Instanz wiederverwenden.
- [ ] fremd belegten Port / sicheren Ausweichport real prüfen.
- [ ] Firefox + Chrome/Chromium: Start, Kalender, TODO, Reminder, Einstellungen.
- [ ] 100 / 125 / 150 / 175 / 200 % Browserzoom.
- [ ] KDE-/DPI-Skalierung und kleine / Full-HD / große Fenster.
- [ ] reiner Tastaturdurchlauf und Fokusreihenfolge.
- [ ] reale Befunde als Regression + Learning Memory aufnehmen.

## SAFE-FILE-CORE — erst danach

- [ ] Copy als erste reale Dateioperation.
- [ ] Quelle/Ziel möglichst über Auswahl statt Pfadeingabe.
- [ ] Existenz, Lesbarkeit, Schreibbarkeit, freier Speicher und Konflikte vorab prüfen.
- [ ] Vorschau und klare Auswirkung vor Änderung.
- [ ] persistenter Jobstatus.
- [ ] Nachprüfung gegen erwartetes Ergebnis.
- [ ] Undo-/Recovery-Datensatz.
- [ ] Abbruch/Neustart robust behandeln.
- [ ] erst danach Move, Rename und Papierkorb/Delete.

## Empfohlener nächster Schritt

**Promotion-Commit vollständig durch Core/Release + Chromium/Firefox laufen lassen. Danach ohne neue Funktion direkt die native Kubuntu-/Zoom-/Tastaturabnahme aus dem TESTED-ZIP durchführen.**

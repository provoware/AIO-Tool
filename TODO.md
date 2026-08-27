# TODO — AIO-Tool

## Status

**P1 DASHBOARD V2 / 0.4.0-dashboard-v2 — CODE-GATE GRÜN**

GitHub Actions Run `33026823914`: 77 Tests + Validierung + Learning Guard + Launcher + JavaScript + Release-Builder + ZIP-Upload erfolgreich. Finaler Dokumentations-/Registry-Head wird separat erneut geprüft.

## Foundation

- [x] Klick-&-Start, lokale `.venv`, Loopback-Backend.
- [x] atomare Config + Backup-Fallback.
- [x] Host-/Origin-/Security-Header.
- [x] vier Themes und Schriftgrößen-Presets.
- [x] CI + reproduzierbarer ZIP-Builder.
- [ ] sauber entpacktes Release real auf Kubuntu starten.
- [ ] Firefox + Chrome/Chromium prüfen.
- [ ] 125–200 % Zoom und Tastaturfokus real prüfen.

## Persistenter Kern

- [x] VersionRegistry + Evidenzpflicht.
- [x] EventRegistry.
- [x] TODO-Core + Titelgedächtnis + Erledigt-Archiv.
- [x] Calendar-Core + Monats/Wochen/Jahr + Reminder-Quittierung + zoneinfo/DST.
- [x] versionierte Muster-/Testdaten.
- [x] versionierte Core-Texte/Fehlerregeln.
- [x] `LEARNING_MEMORY.jsonl` + CI-Guard.
- [ ] VERSION/Registry-Drift zusätzlich automatisiert gegen CHANGELOG/MANIFEST prüfen.

## Dashboard V2

- [x] Monatskalender dauerhaft sichtbar.
- [x] nächste Termine kompakt.
- [x] nächste drei TODOs aus Serverreihenfolge.
- [x] TODO direkt abhaken.
- [x] letzte fünf Ereignisse.
- [x] Version/Registry/Backend/Fremdpaket-Status.
- [x] fällige Reminder sichtbar anzeigen.
- [x] Reminder erst nach Klick auf „Gesehen“ quittieren.
- [x] unsichtbarer Tab quittiert Reminder nicht.
- [x] Entwicklerbereich klein und persistent ein-/ausblendbar.
- [x] Diagnose ohne vollständige Config, Projektpfad oder Favoriten.
- [x] Module in „Häufig“ und „Alle“ trennen.
- [x] linker modularer Schnellzugriff.
- [x] vier Themes + 90–140 % Schriftgröße.
- [x] automatische Dichte `kompakt / normal / weit` aus Fenster/Schriftgröße.
- [x] responsive Breakpoints 1180 / 920 / 720 / 430 px.
- [x] Skip-Link, Fokusindikator, ARIA-Live und Reduced-Motion-Vertrag.
- [x] versionierter Dashboard-Textkatalog.
- [x] statischer Dashboard-Regressionsvertrag.
- [x] 77 Tests im Code-Gate `33026823914`.
- [ ] echte Browserdarstellung auf Zielsystem visuell/bedienseitig abnehmen.

## P0 vor SAFE-FILE-CORE

- [ ] vollständiges `0.4.0-dashboard-v2` Release aus CI entpacken.
- [ ] `start_tool.sh` auf Kubuntu aus sauberem Ordner starten.
- [ ] Firefox: Start, Kalender, TODO-Abhaken, Reminder, Einstellungen, Fokus, Zoom.
- [ ] Chrome/Chromium: denselben Vertrag prüfen.
- [ ] 100 / 125 / 150 / 175 / 200 % Zoom prüfen.
- [ ] Bildschirmbreiten klein / Full-HD / groß prüfen.
- [ ] gefundene reale UI-Fehler jeweils als Regression + Learning Memory übernehmen.

## SAFE-FILE-CORE danach

- [ ] Copy als erste Dateioperation.
- [ ] Quelle/Ziel nur über sichere Auswahl.
- [ ] Vorprüfung: Existenz, Lesbarkeit, Schreibbarkeit, freier Speicher, Konflikte.
- [ ] Vorschau vor Änderung.
- [ ] persistenter Jobstatus.
- [ ] Nachprüfung gegen erwartetes Ergebnis.
- [ ] Undo-/Recovery-Datensatz.
- [ ] Abbruch/Neustart robust behandeln.
- [ ] erst danach Move, Rename und Papierkorb/Delete.

## Job & Recovery

- [ ] persistente Job-Queue.
- [ ] `DONE` erst nach erfolgreicher Persistenz + Nachprüfung.
- [ ] Pause / Abbruch / Wiederaufnahme.
- [ ] Checkpoints und Recovery Center.

## Aktuell empfohlener nächster Schritt

**Dashboard V2 finalen Dokumentations-/Registry-Gate grün machen und mergen. Danach keine neue Funktion: zuerst reale Kubuntu-/Firefox-/Chrome-/Zoom-Abnahme aus dem erzeugten ZIP.**

# TODO — AIO-Tool

## Status

**CLEAN FOUNDATION / 0.1.1-foundation**

Neue Funktionen werden nicht aufgenommen, solange höhere Sicherheits- oder Integritätsgates offen sind.

## P0 — Fundament festziehen

- [x] Projektstruktur für Anwendung, Tests, Dokumentation und Runtime definiert.
- [x] Klick-&-Start-Launcher mit lokaler `.venv`, Vorprüfung und Mehrfachstartschutz implementiert.
- [x] Persistenz-Grundvertrag umgesetzt: atomare Konfiguration + Backup-Fallback.
- [x] lokales Sicherheitsmodell umgesetzt: Bindung an `127.0.0.1`, Host-/Origin-Prüfung, Security-Header.
- [x] UI-Grundvertrag umgesetzt: Laienmodus, Expertenbereich, 4 Themes, Schriftgrößen-Presets, responsive Dashboard-Shell.
- [x] Release-/Validierungsstruktur implementiert: Unit-Tests, `validate.py`, CI, reproduzierbarer ZIP-Builder.
- [ ] GitHub-CI für `0.1.1-foundation` tatsächlich grün bestätigen.
- [ ] frischen Klick-&-Start auf Kubuntu aus sauberem Checkout prüfen.
- [ ] Firefox- und Chrome/Chromium-Grundgate auf Zielsystem prüfen.

## P1 — SAFE-FILE-CORE / Copy zuerst

- [ ] Quellenwahl über Auswahldialog statt Pfadeingabe definieren und implementieren.
- [ ] Zielwahl über Auswahldialog und zuletzt verwendete sichere Ziele.
- [ ] Datei-/Ordnerauswahl vor Aktion validieren.
- [ ] Copy-Vorschau: Quelle, Ziel, Anzahl, Größe, Konflikte.
- [ ] freien Speicher vor Copy prüfen.
- [ ] Namenskonflikte über Auswahl lösen: überspringen / umbenennen / ersetzen nur nach ausdrücklicher Freigabe.
- [ ] Copy als persistente Job-Operation implementieren.
- [ ] Ergebnis nach Copy validieren.
- [ ] zentralen Undo-/Recovery-Datensatz für Copy erzeugen.
- [ ] Abbruch während Copy sicher behandeln.
- [ ] große Datenmengen ohne UI-Blockade prüfen.

### Erst nach belastbarer Copy-Evidenz

- [ ] Move ergänzen.
- [ ] Rename mit Konfliktvorschau und Undo ergänzen.
- [ ] Löschaktionen ausschließlich über Papierkorb-/Recovery-Vertrag ergänzen.

## P1 — Job & Recovery

- [ ] persistente Job-Queue definieren.
- [ ] Zustände: geplant / läuft / pausiert / abgebrochen / unterbrochen / fehlgeschlagen / fertig.
- [ ] `DONE` erst nach erfolgreicher Persistenz melden.
- [ ] Pause, Abbruch und Wiederaufnahme regressionssicher testen.
- [ ] Checkpoint vor kritischen Änderungen.
- [ ] Recovery-Center mit verständlicher Auswahl statt Dateipfaden.

## P1 — Laienführung

- [ ] Jede reale Hauptaktion mit Zweck, Auswirkung und sicherer Alternative erklären.
- [x] Nächsten Schritt in Foundation-UI sichtbar gemacht.
- [x] Ampellogik als UI-Grundvertrag vorbereitet.
- [ ] „Weiß ich nicht“ in zukünftigen Dialogen ohne Blockade umsetzen.
- [ ] wiederkehrende sichere Eingaben als Auswahl merken.
- [ ] Entwicklerinfo-Titel als Presets + zuletzt verwendet anbieten.

## P2 — Projekt & Dashboard

- [x] Dashboard-Shell vorhanden.
- [ ] Projektordner-Prüfung und -Erstellung.
- [ ] Projektwechsel ohne stillen Statusverlust.
- [ ] Notizen / Entwicklerinfos projektbezogen speichern.
- [ ] Ergebnisberichte und Verlauf.

## P2 — Accessibility & Darstellung

- [x] 4 Themes einschließlich High Contrast vorbereitet.
- [x] Schriftgrößen 90–140 % per Buttons.
- [x] sichtbare Fokuszustände und native Tastaturbedienung im Foundation-Shell.
- [ ] 125–200 % Browserzoom auf realem Zielsystem prüfen.
- [x] Status nicht ausschließlich über Farbe dargestellt.

## P3 — Erweiterungen

- [ ] Kalender und Aufgaben.
- [ ] Presets / wiederholbare Workflows.
- [ ] Plugin-/Modul-Registry.
- [ ] Suchmodul.
- [ ] Import/Export.
- [ ] optionale Automatisierungen.

## Quality Gates

Ein Slice gilt erst als abgeschlossen, wenn:

1. Vorbedingungen dokumentiert sind.
2. relevante Tests vorliegen.
3. Fehlerpfade geprüft sind.
4. Dokumentation angepasst ist.
5. Regressionen aktualisiert sind.
6. Manifest und Changelog stimmen.
7. keine temporären Entwicklungsartefakte im Release verbleiben.
8. Zielsystem-Gates nicht als bestanden behauptet werden, solange sie nicht tatsächlich ausgeführt wurden.

## Aktuell empfohlener nächster Schritt

**Foundation-CI + frischer Kubuntu-Start verifizieren. Danach P1 SAFE-FILE-CORE ausschließlich mit Copy beginnen.**

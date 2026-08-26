# TODO — AIO-Tool

## Status

**CLEAN FOUNDATION / 0.1.0-foundation**

Ziel dieser Datei ist eine priorisierte, überprüfbare Entwicklungsreihenfolge. Neue Funktionen werden nicht aufgenommen, solange höhere Sicherheits- oder Integritätsgates offen sind.

## P0 — Fundament festziehen

- [ ] Projektstruktur für Anwendung, Tests, Dokumentation und Runtime definieren.
- [ ] Start-/Bootstrap-Vertrag festlegen: Klick-&-Start, Abhängigkeitsprüfung, lokale virtuelle Umgebung, verständliche Fehlerausgabe.
- [ ] Persistenzvertrag definieren: Konfiguration, Profile, Recovery-Daten, Lern-/Regressionseinträge.
- [ ] Sicherheitsmodell für lokale Backend-Bindung, Host-/Origin-Prüfung und Dateizugriffe definieren.
- [ ] UI-Grundvertrag festlegen: Laienmodus, Expertenbereich, 4 Themes, Schriftgröße, Kontrast, Tastaturbedienung.
- [ ] Release-/Validierungsstruktur definieren: Vorprüfung, Nachprüfung, Regression, Manifest, reproduzierbares ZIP.

## P1 — SAFE-FILE-CORE

- [ ] Quelle über Auswahldialog statt Pfadeingabe wählen.
- [ ] Datei-/Ordnerauswahl sicher validieren.
- [ ] Copy als erste reale Operation implementieren.
- [ ] Move erst nach Copy-Validierung ergänzen.
- [ ] Rename mit Konfliktvorschau und Undo ergänzen.
- [ ] Löschaktionen ausschließlich über Papierkorb-/Recovery-Vertrag planen.
- [ ] Vorschau vor jeder verändernden Operation.
- [ ] freien Speicher und Zielkonflikte vor Ausführung prüfen.
- [ ] Ergebnis nach Ausführung validieren.
- [ ] zentralen Undo-Datensatz erzeugen.

## P1 — Job & Recovery

- [ ] persistente Job-Queue definieren.
- [ ] Zustände: geplant / läuft / pausiert / abgebrochen / unterbrochen / fehlgeschlagen / fertig.
- [ ] DONE erst nach erfolgreicher Persistenz melden.
- [ ] Pause, Abbruch und Wiederaufnahme regressionssicher testen.
- [ ] Checkpoint vor kritischen Änderungen.
- [ ] Recovery-Center mit verständlicher Auswahl statt Dateipfaden.

## P1 — Laienführung

- [ ] Jede Hauptaktion mit Zweck, Auswirkung und sicherer Alternative erklären.
- [ ] Nächsten Schritt permanent sichtbar halten.
- [ ] Ampellogik definieren: grün bereit, gelb optional, orange prüfen, rot Eingriff/Risiko.
- [ ] „Weiß ich nicht“ darf keinen Workflow blockieren.
- [ ] wiederkehrende sichere Eingaben als Auswahl merken.
- [ ] Entwicklerinfo-Titel als Presets + zuletzt verwendet anbieten.

## P2 — Projekt & Dashboard

- [ ] Dashboard-Shell mit Modulen, Favoriten und Projektstatus.
- [ ] Projektordner-Prüfung und -Erstellung.
- [ ] Projektwechsel ohne stillen Statusverlust.
- [ ] Notizen / Entwicklerinfos projektbezogen speichern.
- [ ] Ergebnisberichte und Verlauf.

## P2 — Accessibility & Darstellung

- [ ] 4 Themes einschließlich High Contrast.
- [ ] Schriftgrößen per Buttons / Presets.
- [ ] Fokuszustände und Tastaturnavigation.
- [ ] 125–200 % Browserzoom ohne Funktionsverlust prüfen.
- [ ] Informationen nicht ausschließlich über Farbe vermitteln.

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

## Aktuell empfohlener nächster Schritt

**P0-Projektstruktur + SAFE-FILE-CORE-Vertrag**, danach erst Implementierung der ersten Copy-Operation.

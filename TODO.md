# TODO — AIO-Tool

## Status

**P1 CALENDAR CORE / 0.3.0-calendar-core — AUTOMATISIERT GEPRÜFT**

Neue Funktionen werden nur in klar abgegrenzeten Slices ergänzt. Sicherheits-, Persistenz-, Fehler- und Learning-Gates bleiben vorrangig.

## P0 — Foundation

- [x] Projektstruktur, Klick-&-Start, lokale `.venv`, Loopback-Backend.
- [x] atomare Config + Backup-Fallback.
- [x] Host-/Origin-/Security-Header-Vertrag.
- [x] Dashboard-Shell, 4 Themes, Schriftgrößen-Presets.
- [x] CI und reproduzierbarer Release-Builder.
- [ ] frischen Klick-&-Start auf Kubuntu aus sauberem Release prüfen.
- [ ] Firefox und Chrome/Chromium auf Zielsystem prüfen.
- [ ] 125–200 % Browserzoom auf Zielsystem prüfen.

## P1 — Persistenter Kern

### VersionRegistry
- [x] getrackte Projekt-Historie + lokale Runtime-Registry.
- [x] Status/Evidenz/Commit-SHA/Regressionstatus.
- [x] Vorgängerversion und VERSION-Driftprüfung.
- [ ] Drift zusätzlich gegen CHANGELOG/MANIFEST automatisieren.

### EventRegistry
- [x] persistente menschenlesbare Events, newest-first, max. 500.
- [ ] Dashboard rechts: letzte fünf Ereignisse.
- [ ] „Alle Ereignisse“ + Debug-Zugang.

### TODO-Core
- [x] persistente TODOs, Priorität, optionaler Termin/Notiz/Kalenderbezug.
- [x] Titelgedächtnis ohne case-sensitive Dubletten.
- [x] Abhaken → Erledigt-Archiv mit Zeitstempel.
- [x] nächste drei TODOs serverseitig.
- [ ] TODO-UI und Archivansicht.
- [ ] Dashboard: nächste drei TODOs anzeigen/abhaken.

## P1 — Robustheits- und Entwicklungs-Guard

- [x] versionierte Musterdateien und positive/negative Testdaten.
- [x] versionierter deutscher Textkatalog.
- [x] versionierte Fehlerregeln + `ErrorAdvisor`.
- [x] Integritätsfehler und Nutzereingabefehler getrennt.
- [x] Exception-Hierarchie-Matching.
- [x] `LEARNING_MEMORY.jsonl` + `scripts/learning_guard.py`.
- [x] CI lädt vollständiges Release-ZIP als Artefakt hoch.
- [x] versionierte Metadaten in Tests gegen ihre Quelldatei statt redundante harte Versionsnummer prüfen.

## P1 — Kalender-Core

- [x] persistentes Kalender-Schema auf `AtomicJsonStore`.
- [x] Termin: Titel, Datum, Startzeit optional, Ende optional, Kategorie, Beschreibung optional.
- [x] Titelgedächtnis und Vorschläge.
- [x] Erinnerungen: Terminzeit / 10 min / 30 min / 1 h / 1 Tag vorher.
- [x] Reminder nur mit Startzeit zulassen.
- [x] persistente Reminder-Quittierung gegen Doppelmeldung.
- [x] Monatsperiode mit echten Monatsgrenzen.
- [x] Wochenperiode Montag–Sonntag.
- [x] Jahresperiode.
- [x] lokale Systemzeitzone via `zoneinfo`; DST-Regressionsschutz.
- [x] optionale TODO-Verknüpfung; unbekannte TODO-ID wird abgelehnt.
- [x] Kalender-Mustervorlage + gültige/ungültige Testdaten.
- [x] Kalender-Fehlerregeln und Laienhinweise.
- [x] Kalender-API + API-Regressionen.
- [x] automatisierte Kalender-CI Run `33026180855`: SUCCESS.
- [ ] sichtbare Browser-/Desktop-Reminderanzeige — gehört zu Dashboard V2.

## P1 — Dashboard V2 / NÄCHSTER SLICE

- [ ] Informationsarchitektur auf getestete Core-APIs umstellen.
- [ ] Monatskalender dauerhaft sichtbar, optional einklappbare Details.
- [ ] nächste Termine kompakt anzeigen.
- [ ] nächste drei TODOs anzeigen und abhaken.
- [ ] letzte fünf Ereignisse in einfacher Sprache.
- [ ] Version + Registry-/Gesundheitsstatus sichtbar.
- [ ] fällige Reminder sichtbar anzeigen und erst nach bestätigter Darstellung quittieren.
- [ ] Debug-/Diagnose-Button dauerhaft erreichbar.
- [ ] Entwicklungsbereich klein anwählbar/versteckbar.
- [ ] häufig genutzte Funktionen getrennt von „Alle“.
- [ ] linker modularer Kachelbereich für weitere Funktionen.
- [ ] Start-Erkennung von Fenster/Bildschirm und Dichte-Modus.
- [ ] kleine Displays, Full-HD, große Displays und 125–200 % Zoom regressionssicher berücksichtigen.
- [ ] Tastaturnavigation, Fokusindikatoren und ARIA-Live-Status prüfen.

## P1 — SAFE-FILE-CORE / danach

- [ ] Copy zuerst: Quelle → Ziel → Vorprüfung → Vorschau → Konflikte → Kopieren → Nachprüfung → Undo-Datensatz.
- [ ] erst danach Move, Rename und Papierkorb/Delete.

## P1 — Job & Recovery

- [ ] persistente Job-Queue.
- [ ] `DONE` erst nach erfolgreicher Persistenz.
- [ ] Pause/Abbruch/Wiederaufnahme.
- [ ] Checkpoints und Recovery-Center.

## Quality Gates

Ein Slice gilt erst als abgeschlossen, wenn Code, positive/negative Testdaten, Tests, Learning Memory falls relevant, Dokumentation, Regressionen, Manifest und Changelog konsistent sind. Zielsystem-Gates dürfen nicht aus CI-Erfolg abgeleitet werden.

## Aktuell empfohlener nächster Schritt

**Dashboard V2 ausschließlich auf den jetzt getesteten Version-/TODO-/Kalender-/Event-APIs aufbauen. Keine neue Domänenlogik in die UI kopieren. Danach reale Browser-/Zoom-Abnahme, erst anschließend SAFE-FILE-CORE.**

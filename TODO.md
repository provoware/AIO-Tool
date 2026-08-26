# TODO — AIO-Tool

## Status

**P1 ROBUSTNESS CORE / 0.2.1-robustness — AUTOMATISIERT GEPRÜFT**

Neue Funktionen werden nur in klar abgegrenzten Slices ergänzt. Sicherheits-, Persistenz- und Integritätsgates bleiben vorrangig.

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
- [ ] Dashboard rechts unten: letzte fünf Ereignisse.
- [ ] „Alle Ereignisse“ + Debug-Button.

### TODO-Core
- [x] persistente TODOs, Priorität, optionaler Termin/Notiz/Kalenderbezug.
- [x] Titelgedächtnis ohne case-sensitive Dubletten.
- [x] Abhaken → Erledigt-Archiv mit Zeitstempel.
- [x] nächste drei TODOs serverseitig.
- [ ] TODO-UI und Archivansicht.
- [ ] Dashboard: nächste drei TODOs anzeigen/abhaken.

## P1 — Robustheits- und Entwicklungs-Guard

- [x] `resources/templates/` mit gültigen, versionierten Musterdateien.
- [x] `testdata/valid/` nutzt dieselben Validatoren wie Produktdaten.
- [x] `testdata/invalid/` bildet bekannte Fehler reproduzierbar ab.
- [x] Textkatalog `resources/texts/de/v1.json` mit eigener Version.
- [x] Fehlerregeln `resources/error_rules/v1.json` mit eigener Version.
- [x] intelligente Fehlerhilfe mit Kategorie, Ampel, Handlung, Vorlagenhinweis und `retry_safe`.
- [x] Fehlerregeln berücksichtigen Klassenhierarchie statt nur exakte Fehlerklasse.
- [x] Integritätsfehler und Nutzereingabefehler getrennt.
- [x] `LEARNING_MEMORY.jsonl` als validiertes Entwicklungs-Lerngedächtnis.
- [x] `scripts/learning_guard.py` als CI-Gate.
- [x] AGENTS-Regel: Datenformat → Vorlage + Negativtest; wiederkehrende Texte → Katalog; bestätigte Strukturfehler → Learning Memory.
- [x] CI lädt vollständiges Release-ZIP als Artefakt hoch.
- [x] Robustheits-CI Run `33024919165`: SUCCESS.

## P1 — Kalender-Core / NÄCHSTER SLICE

- [ ] persistentes Kalender-Schema auf `AtomicJsonStore`.
- [ ] Termin: Titel, Datum, Startzeit optional, Ende optional, Kategorie, Beschreibung optional.
- [ ] Titelgedächtnis und Preset-/Auswahllogik vorbereiten.
- [ ] Erinnerungen: Terminzeit / 10 min / 30 min / 1 h / 1 Tag vorher.
- [ ] Monatsansicht: Periodengrenzen und nach Datum gruppierte Termine.
- [ ] Wochenansicht: Montag–Sonntag.
- [ ] Jahresansicht: 12 Monate / Monatsgruppen.
- [ ] optionale TODO-Verknüpfung; TODO bleibt ohne Kalender voll funktionsfähig.
- [ ] Kalender-Mustervorlage + gültige/ungültige Testdaten.
- [ ] Kalender-API + Regressionstests.

## P1 — Dashboard & Debug DANACH

- [ ] kompakter/informativer Dashboardaufbau.
- [ ] Version + Registrystatus sichtbar.
- [ ] nächste drei TODOs.
- [ ] nächste Termine / optionaler Kalenderblock.
- [ ] rechte Spalte: letzte fünf Ereignisse in einfacher Sprache.
- [ ] Debug-/Diagnose-Button.
- [ ] Start-Erkennung von Fenster/Bildschirm und Dichte-Modus.
- [ ] kleine Displays, Full-HD, große Displays, hohe DPI/Zoom berücksichtigen.

## P1 — SAFE-FILE-CORE / später

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

**Kalender-Core als separates Daten-/API-Modul umsetzen. Danach Dashboard V2 ausschließlich auf den bereits getesteten Registries aufbauen.**

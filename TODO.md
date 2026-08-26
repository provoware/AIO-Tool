# TODO — AIO-Tool

## Status

**P1 PERSISTENT CORE / 0.2.0-core**

Neue Funktionen werden nur in klar abgegrenzten Slices ergänzt. Sicherheits-, Persistenz- und Integritätsgates bleiben vorrangig.

## P0 — Foundation

- [x] Projektstruktur für Anwendung, Tests, Dokumentation und Runtime.
- [x] Klick-&-Start mit lokaler `.venv`, Vorprüfung und Mehrfachstartschutz.
- [x] atomare Konfigurationspersistenz + Backup-Fallback.
- [x] Loopback-, Host-/Origin- und Security-Header-Vertrag.
- [x] UI-Grundvertrag mit Laienmodus, Expertenbereich, 4 Themes und Schriftgrößen-Presets.
- [x] Unit-Tests, Vorvalidierung, CI und reproduzierbarer ZIP-Builder.
- [ ] frischen Klick-&-Start auf Kubuntu aus sauberem Checkout prüfen.
- [ ] Firefox- und Chrome/Chromium-Grundgate auf Zielsystem prüfen.
- [ ] 125–200 % Browserzoom auf Zielsystem prüfen.

## P1 — Gemeinsamer persistenter Kern

### VersionRegistry

- [x] zentrales Registry-Schema implementiert.
- [x] getrackte Projekt-Historie in `VERSION_REGISTRY.json` angelegt.
- [x] lokale Runtime-Registry wird auf frischer Installation aus der Projekt-Historie initialisiert.
- [x] aktuelle und bekannte Versionen persistent speichern.
- [x] Statuswerte development / tested / release-candidate / released / deprecated.
- [x] Release-Status und Regressionstatus speichern.
- [x] Commit-SHA optional vorsehen.
- [x] Änderungen und bekannte Probleme speichern.
- [x] Evidenznachweise speichern.
- [x] getestete/freigegebene Zustände ohne Evidenz blockieren.
- [x] Drift zwischen `VERSION` und getrackter Registry automatisch prüfen.
- [x] Vorgängerversion abrufbar machen.
- [ ] Drift zusätzlich gegen CHANGELOG/MANIFEST automatisch prüfen.

### EventRegistry

- [x] persistentes Event-Schema implementiert.
- [x] kurze menschenlesbare Ereignistexte als Pflichtfeld.
- [x] Bereich und Ampel-/Statusstufe speichern.
- [x] letzte Ereignisse newest-first abrufbar machen.
- [x] Registry auf 500 Ereignisse begrenzen.
- [x] TODO-Anlegen und TODO-Erledigen automatisch protokollieren.
- [ ] Dashboard rechts unten: letzte fünf Ereignisse anzeigen.
- [ ] Button „Alle Ereignisse“.
- [ ] Button zum Debug-/Diagnosemodul.

### TODO-Core

- [x] persistentes TODO-Schema implementiert.
- [x] Titel, Kategorie, Termin, Priorität und Notiz als Datenvertrag.
- [x] Kalenderverknüpfung optional vorbereitet.
- [x] Titel persistent merken.
- [x] gleiche Titel ohne Groß-/Kleinschreibungs-Dubletten zusammenführen.
- [x] Titel nach Nutzungshäufigkeit und letzter Verwendung wieder anbieten.
- [x] Abhaken verschiebt ins Erledigt-Archiv statt zu löschen.
- [x] Erledigt-Zeitstempel speichern und Erstellungszeit erhalten.
- [x] nächste drei TODOs serverseitig ermitteln.
- [ ] TODO-UI mit Auswahl vor Zeicheneingabe.
- [ ] Dashboard: nächste drei TODOs kompakt anzeigen und direkt abhaken.
- [ ] Archivansicht für erledigte TODOs.

### Core-Integrität

- [x] gemeinsamer `AtomicJsonStore` mit atomarem Replace und Backup-Fallback.
- [x] Seed-/Default-Daten werden vor Verwendung validiert.
- [x] API für Versionen, Ereignisse, TODOs, Archiv und Titelvorschläge.
- [x] ungültige Abfrageparameter als 400/Nutzereingabe klassifizieren.
- [x] beschädigte lokale Lesedaten als 500/Integritätsfehler klassifizieren.
- [x] sekundärer Eventfehler darf bereits gespeicherte TODO-Aktion nicht als fehlgeschlagen darstellen.
- [x] Unit-/Integrationstests im Branch ergänzt.
- [x] Foundation-Validierung auf neue Persistenzmodelle erweitert.
- [ ] GitHub-CI für finalen `0.2.0-core`-Head grün bestätigen.

## P1 — Kalender-Core / nächster Slice

- [ ] persistentes Kalender-Schema mit Schema-Version und Recovery-Vertrag.
- [ ] Termin: Titel, Datum, Uhrzeit optional, Ende optional, Kategorie, Beschreibung optional.
- [ ] Monats-, Wochen- und Jahresansicht.
- [ ] Termin-Titel merken und als Auswahl anbieten.
- [ ] Erinnerungen: Terminzeit / 10 min / 30 min / 1 h / 1 Tag vorher.
- [ ] TODO-Verknüpfung optional; TODO ohne Kalender muss vollständig funktionieren.
- [ ] Kalender im Dashboard optional ein-/ausblendbar.

## P1 — Dashboard & Debug danach

- [ ] Dashboard kompakter und informativer strukturieren.
- [ ] Tool-Version und Registry-Status sichtbar machen.
- [ ] nächste drei TODOs anzeigen.
- [ ] nächste Termine anzeigen, wenn Kalender aktiviert ist.
- [ ] rechte Spalte: letzte fünf Ereignisse in einfacher Sprache.
- [ ] Debug-Button dauerhaft erreichbar.
- [ ] Bildschirm-/Fenstergröße beim Start erfassen und Dichte-Modus ableiten.
- [ ] kleine Displays, Full-HD, große Displays und hohe DPI berücksichtigen.

## P1 — SAFE-FILE-CORE / erst nach Daten-/Dashboardkern

- [ ] Quellenwahl über Auswahldialog statt Pfadeingabe.
- [ ] Zielwahl über Auswahldialog und zuletzt verwendete sichere Ziele.
- [ ] Datei-/Ordnerauswahl vor Aktion validieren.
- [ ] Copy-Vorschau: Quelle, Ziel, Anzahl, Größe, Konflikte.
- [ ] freien Speicher vor Copy prüfen.
- [ ] Konflikte über Auswahl lösen.
- [ ] Copy als persistente Job-Operation.
- [ ] Ergebnis nach Copy validieren.
- [ ] Undo-/Recovery-Datensatz.
- [ ] Abbruch sicher behandeln.

### Erst nach belastbarer Copy-Evidenz

- [ ] Move.
- [ ] Rename.
- [ ] Löschaktionen über Papierkorb-/Recovery-Vertrag.

## P1 — Job & Recovery

- [ ] persistente Job-Queue.
- [ ] Zustände geplant / läuft / pausiert / abgebrochen / unterbrochen / fehlgeschlagen / fertig.
- [ ] `DONE` erst nach erfolgreicher Persistenz.
- [ ] Pause, Abbruch und Wiederaufnahme regressionssicher.
- [ ] Checkpoint vor kritischen Änderungen.
- [ ] Recovery-Center über verständliche Auswahl.

## P1 — Laienführung

- [ ] Jede reale Hauptaktion mit Zweck, Auswirkung und sicherer Alternative erklären.
- [x] nächster Schritt im Foundation-Dashboard sichtbar.
- [x] Ampellogik als UI-Grundvertrag.
- [ ] „Weiß ich nicht“ ohne Workflow-Blockade.
- [x] TODO-Titel als wiederkehrende sichere Eingaben persistent merken.
- [ ] Entwicklerinfo-Titel als Presets + zuletzt verwendet anbieten.

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

**Zuerst den finalen `0.2.0-core`-Head durch CI abnehmen und mergen. Danach Kalender-Core auf denselben Persistenzvertrag aufsetzen; anschließend TODO/Kalender/Ereignisse ins responsive Dashboard integrieren.**

# TODO — AIO-Tool

## Status

**P1 PERSISTENT CORE / 0.2.0-core — AUTOMATISIERT GEPRÜFT**

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
- [x] zentrales Registry-Schema.
- [x] getrackte Projekt-Historie in `VERSION_REGISTRY.json`.
- [x] frische Runtime wird aus Projekt-Historie initialisiert.
- [x] Versions-, Release- und Regressionstatus.
- [x] Commit-SHA optional.
- [x] Änderungen, bekannte Probleme und Evidenz.
- [x] tested/release-candidate/released ohne Evidenz blockiert.
- [x] Drift `VERSION` ↔ getrackte Registry geprüft.
- [x] Vorgängerversion abrufbar.
- [ ] Drift zusätzlich gegen CHANGELOG/MANIFEST automatisieren.

### EventRegistry
- [x] persistentes Event-Schema.
- [x] menschenlesbarer Meldungstext Pflicht.
- [x] Bereich und Ampel-/Statusstufe.
- [x] newest-first-Abruf.
- [x] maximal 500 Ereignisse.
- [x] TODO-Anlegen und -Erledigen protokollieren.
- [ ] Dashboard rechts unten: letzte fünf Ereignisse.
- [ ] „Alle Ereignisse“.
- [ ] Debug-/Diagnose-Button.

### TODO-Core
- [x] persistentes TODO-Schema.
- [x] Titel, Kategorie, optionaler Termin, Priorität, Notiz.
- [x] Kalenderverknüpfung optional vorbereitet.
- [x] Titel persistent merken.
- [x] case-insensitive Dubletten verhindern.
- [x] Titel nach Häufigkeit/letzter Nutzung anbieten.
- [x] Abhaken → Erledigt-Archiv.
- [x] `completed_at` plus ursprüngliches `created_at`.
- [x] nächste drei TODOs serverseitig.
- [ ] TODO-UI mit Auswahl vor Zeicheneingabe.
- [ ] Dashboard: nächste drei TODOs anzeigen und abhaken.
- [ ] Archivansicht.

### Core-Integrität
- [x] gemeinsamer `AtomicJsonStore`.
- [x] Seed-/Default-Daten validieren.
- [x] API für Versionen, Ereignisse, TODOs, Archiv und Titelvorschläge.
- [x] ungültige Parameter/Eingaben → HTTP 400.
- [x] beschädigte lokale Persistenz → HTTP 500/Integritätsmeldung.
- [x] sekundärer Eventfehler zerstört Erfolg einer bereits gespeicherten TODO-Aktion nicht.
- [x] Unit-/Integrationstests.
- [x] Foundation-/Core-Validierung erweitert.
- [x] finaler Merge-Kandidat durch GitHub-CI grün: Run `33022569880`.

## P1 — Kalender-Core / nächster Slice

- [ ] persistentes Kalender-Schema mit Schema-Version und Recovery-Vertrag.
- [ ] Termin: Titel, Datum, Uhrzeit optional, Ende optional, Kategorie, Beschreibung optional.
- [ ] Monats-, Wochen- und Jahresansicht.
- [ ] Termin-Titel merken und als Auswahl anbieten.
- [ ] Erinnerungen: Terminzeit / 10 min / 30 min / 1 h / 1 Tag vorher.
- [ ] TODO-Verknüpfung optional; TODO ohne Kalender vollständig funktionsfähig.
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

## P1 — SAFE-FILE-CORE / später

- [ ] Quellen- und Zielwahl über Auswahldialog.
- [ ] Copy-Vorschau mit Quelle, Ziel, Anzahl, Größe, Konflikten.
- [ ] Speicher-/Konfliktprüfung.
- [ ] Copy als persistente Job-Operation.
- [ ] Nachprüfung und Undo-/Recovery-Datensatz.
- [ ] Abbruch sicher behandeln.
- [ ] erst danach Move, Rename und Papierkorb-/Delete-Vertrag.

## P1 — Job & Recovery

- [ ] persistente Job-Queue.
- [ ] Zustände geplant / läuft / pausiert / abgebrochen / unterbrochen / fehlgeschlagen / fertig.
- [ ] `DONE` erst nach erfolgreicher Persistenz.
- [ ] Pause, Abbruch und Wiederaufnahme regressionssicher.
- [ ] Checkpoint und Recovery-Center.

## Quality Gates

Ein Slice gilt erst als abgeschlossen, wenn Tests, Fehlerpfade, Dokumentation, Regressionen, Manifest und Changelog konsistent sind. Zielsystem-Gates dürfen nicht aus CI-Erfolg abgeleitet werden.

## Aktuell empfohlener nächster Schritt

**Kalender-Core auf denselben Persistenzvertrag aufsetzen. Danach TODO/Kalender/EventRegistry in das responsive Dashboard integrieren.**

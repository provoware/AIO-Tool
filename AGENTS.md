# AGENTS.md — Verbindliche Entwicklungsregeln

Diese Regeln gelten für Menschen, KI-Agenten und automatisierte Entwicklungswerkzeuge im Repository.

## 1. Arbeitsprinzip

**Besprechen → klar abgrenzen → gezielt ändern → automatisch prüfen → Fehler beheben → Regression sichern → dokumentieren → nächsten unabhängigen Schritt wählen.**

Keine großflächigen Umbauten ohne nachgewiesenen Nutzen. Bestehende funktionierende Bereiche werden möglichst lokal gepatcht.

## 2. Laien zuerst

- Standardsprache der Nutzeroberfläche: Deutsch.
- Alltagssprache vor Fachsprache.
- Fachbegriffe nur ergänzend und verständlich erklärt.
- Pro Ansicht möglichst 3–6 Hauptentscheidungen.
- Ein klarer nächster Schritt muss sichtbar sein.
- Expertenoptionen standardmäßig einklappen.

## 3. Auswahl vor Zeicheneingabe

Neue Eingabefelder sind begründungspflichtig.

Reihenfolge:

1. Button
2. Auswahldialog
3. Preset / zuletzt verwendet
4. intelligente Empfehlung
5. erst dann Freitext-Fallback

Ausnahmen: Inhalte, die naturgemäß frei eingegeben werden müssen, z. B. Notiztext oder PIN.

Wiederkehrende sichere Eingaben sollen gespeichert und später als Auswahl angeboten werden. Keine sensiblen Inhalte automatisch als Vorschläge übernehmen.

## 4. Sicherheit

- Keine destruktive Dateiaktion ohne Vorschau und klare Auswirkung.
- Kritische Operationen benötigen Vorvalidierung und Nachvalidierung.
- Undo/Recovery ist Teil des Funktionsvertrags, nicht spätere Kosmetik.
- Endgültiges Löschen ist nie Standard.
- Kein stiller Zielwechsel bei Laufwerks-/Pfadproblemen.
- Fehler dürfen keinen falschen Erfolg melden.
- `DONE` erst nach erfolgreicher Persistenz des Abschlusszustands.

## 5. Offline-first und Datenschutz

- Kernfunktionen funktionieren ohne Internet.
- Keine Telemetrie ohne ausdrücklich dokumentierte Produktentscheidung.
- Lokales Backend nur auf Loopback binden, sofern kein anderer Vertrag beschlossen wurde.
- So wenig personenbezogene oder nutzerspezifische Daten speichern wie möglich.
- Keine Secrets, PINs oder Passwörter im Klartext protokollieren.

## 6. Architektur

- Module mit klaren Verantwortlichkeiten.
- UI, Domänenlogik, Persistenz und Transport nicht unnötig koppeln.
- Lange Dateien frühzeitig modularisieren; Zielwert für zentrale Quellmodule: möglichst unter ca. 800 Zeilen.
- Keine Abhängigkeit hinzufügen, wenn Standardbibliothek oder bestehende Abhängigkeit die Aufgabe robust erfüllt.
- Externe Abhängigkeiten müssen begründet, geprüft und im Manifest dokumentiert werden.

## 7. Persistenz

- Zustände atomar schreiben, wo Datenverlust relevant ist.
- Unterbrochene Prozesse dürfen nach Neustart nicht als „läuft“ erscheinen.
- Backups/Recovery-Metadaten konsistent halten.
- Konfigurationsänderungen dürfen nicht als Nebeneffekt einer reinen Prüfung entstehen.

## 8. Tests und Regression

Jeder bestätigte Fehler erhält möglichst:

- reproduzierbaren Test,
- erwartetes Verhalten,
- tatsächliches Fehlverhalten,
- Fix-Nachweis,
- dauerhaftes Regression-Gate.

Keine Aussage „behoben“ ohne erneute Prüfung.

## 9. Release-Regeln

Vor einem Release:

- Tests grün.
- Changelog aktualisiert.
- TODO konsistent.
- Manifest aktuell.
- Regressionseinträge aktuell.
- Laienanleitung auf tatsächliches Verhalten geprüft.
- keine `.venv`, Caches, temporären Logs, Testprofile oder lokalen Nutzerdaten im Release.
- erzeugtes Release erneut aus sauber entpacktem Zustand prüfen.

## 10. Statussprache

`UMGESETZT` bedeutet Code/Artefakt vorhanden.

`GEPRÜFT` bedeutet Test tatsächlich ausgeführt.

`BEWIESEN` bedeutet reproduzierbare Evidenz vorhanden.

Nicht geprüfte Zielsysteme ausdrücklich als offen kennzeichnen.

## 11. Dokumentationspflicht

Änderungen mit Auswirkung auf Verhalten, Architektur, Sicherheit oder Bedienung müssen mindestens in den relevanten Dateien aus README, TODO, CHANGELOG, MANIFEST, REGRESSIONSINFOS und LAIEN-ANLEITUNG nachgezogen werden.

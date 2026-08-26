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

## 8. Tests, Musterdateien und Regression

Jeder bestätigte Fehler erhält möglichst reproduzierbaren Test, erwartetes Verhalten, tatsächliches Fehlverhalten, Fix-Nachweis und dauerhaftes Gate.

Für jedes persistente JSON-/Config-Format gilt zusätzlich:

- mindestens eine gültige versionierte Mustervorlage,
- relevante absichtlich ungültige Testdaten,
- dieselben Validatoren für Produktdaten, Vorlage und Tests,
- Vorlagen niemals ungefragt über Nutzerdaten schreiben,
- Schemaänderung → Validator + Vorlage + Testdaten + Regression gemeinsam aktualisieren.

Keine Aussage „behoben“ ohne erneute Prüfung.

## 9. Versionierte Nutztexte und Fehlerhilfe

Wiederkehrende sichtbare Systemtexte werden aus versionierten Textkatalogen geladen statt an vielen Stellen hart codiert.

Fehlerhilfe muss unterscheiden:

- ungültige Nutzereingabe,
- Integritäts-/Persistenzfehler,
- unbekannter Fehler.

Eine Hilferegel darf eine geprüfte Mustervorlage empfehlen, aber keine Nutzerdaten automatisch ersetzen. `retry_safe=true` darf nur gesetzt werden, wenn ein erneuter Versuch ohne zusätzliche Datengefährdung vertretbar ist.

## 10. Entwicklungs-Lerngedächtnis

`LEARNING_MEMORY.jsonl` hält bestätigte Entwicklungslektionen dauerhaft fest.

Ein Eintrag soll enthalten: Auslöser, Erkenntnis, neue Regel, Regression und Geltungsbereich. Wiederkehrende oder strukturelle Fehler müssen dort aufgenommen werden. CI validiert die Datei; widersprüchliche oder ungültige Lerndaten dürfen keinen Release passieren.

## 11. Codesparendes Patchen

Vor einem größeren Fix zuerst die kleinste verantwortliche Codezone bestimmen: **Datei → Funktion/Klasse → Zeilenbereich → zugehöriger Test**.

Bevorzugt wird ein lokaler Patch mit passender Regression statt breitem Refactor. Größere Umbauten nur, wenn die lokale Reparatur strukturell unvertretbar wäre. Abschlussberichte nennen bei relevanten offenen Punkten konkrete Patchstellen mit Zeilenangaben.

## 12. Release-Regeln

Vor einem Release:

- Tests grün,
- Learning Guard grün,
- Changelog/TODO/Manifest/Regressionen aktuell,
- Laienanleitung auf tatsächliches Verhalten geprüft,
- Muster-/Testdaten mit Validatoren konsistent,
- keine `.venv`, Caches, temporären Logs, Testprofile oder lokalen Nutzerdaten im Release,
- erzeugtes Release erneut prüfen.

## 13. Statussprache

`UMGESETZT` = Code/Artefakt vorhanden.  
`GEPRÜFT` = Test tatsächlich ausgeführt.  
`BEWIESEN` = reproduzierbare Evidenz vorhanden.

Nicht geprüfte Zielsysteme ausdrücklich als offen kennzeichnen.

## 14. Dokumentationspflicht

Änderungen mit Auswirkung auf Verhalten, Architektur, Sicherheit oder Bedienung müssen mindestens in den relevanten Dateien aus README, TODO, CHANGELOG, MANIFEST, REGRESSIONSINFOS und LAIEN-ANLEITUNG nachgezogen werden.

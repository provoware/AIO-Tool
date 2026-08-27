# LAIEN-ANLEITUNG

## Was ist AIO-Tool?

AIO-Tool bündelt wiederkehrende Aufgaben in einer gemeinsamen, lokalen Oberfläche. Die Bedienung soll einfach, sichtbar und sicher bleiben.

## Aktueller Stand: 0.3.0-calendar-core

Der bisherige Versions-, Ereignis-, TODO- und Robustheitskern wurde um einen getesteten Kalender-Kern erweitert.

Neu vorhanden sind:

- Termine lokal und dauerhaft speichern,
- Kalendertitel merken und wieder anbieten,
- Monats-, Wochen- und Jahresbereiche erzeugen,
- Erinnerungen vorbereiten,
- bereits angezeigte Erinnerungen merken,
- optional einen Termin mit einem TODO verknüpfen,
- Sommer-/Winterzeit automatisch korrekt berücksichtigen.

Die sichtbare Kalenderoberfläche folgt im nächsten Entwicklungsschritt.

## Einen Termin verstehen

Ein Termin kann enthalten:

- Titel,
- Datum,
- Startzeit optional,
- Endzeit optional,
- Kategorie optional,
- Beschreibung optional,
- Erinnerung optional,
- TODO-Verknüpfung optional.

Ein TODO ist **keine Pflicht**. Kalender und TODO funktionieren auch unabhängig voneinander.

## Erinnerungen

Zur Auswahl sind vorbereitet:

- zum Terminzeitpunkt,
- 10 Minuten vorher,
- 30 Minuten vorher,
- 1 Stunde vorher,
- 1 Tag vorher.

Eine Erinnerung braucht eine Uhrzeit. Ohne Startzeit kann das Tool nicht eindeutig wissen, wann erinnert werden soll und lehnt diese Kombination deshalb verständlich ab.

### Warum gibt es eine Quittierung?

Die Oberfläche darf eine Erinnerung erst als „angezeigt“ markieren, wenn sie tatsächlich sichtbar dargestellt wurde.

Vereinfacht:

`Reminder fällig → Oberfläche zeigt ihn → erst dann quittieren → nicht erneut anzeigen`

Dadurch soll dieselbe Erinnerung nicht bei jeder neuen Abfrage wieder erscheinen.

## Sommer- und Winterzeit

Das Tool verwendet die lokale System-Zeitzone. Dadurch wird für einen zukünftigen Termin geprüft, welche Zeitregel **an diesem zukünftigen Datum** gilt.

Das ist wichtig, weil ein heute gültiger UTC-Abstand nach einem Sommer-/Winterzeitwechsel falsch sein kann.

## Monats-, Wochen- und Jahresansicht

Der Datenkern kann bereits berechnen:

- Monat vom ersten bis zum letzten echten Kalendertag,
- Woche von Montag bis Sonntag,
- komplettes Kalenderjahr.

Dashboard V2 macht diese Daten anschließend sichtbar.

## Mustervorlagen und Fehlerhilfe

Auch der Kalender besitzt eine geprüfte Musterdatei und gezielte Fehler-Testdateien.

Beispiele für automatisch geprüfte Fehler:

- Endzeit liegt vor der Startzeit,
- Erinnerung wurde gewählt, aber keine Startzeit gesetzt,
- unbekannte Kalenderoption,
- nicht vorhandene TODO-Verknüpfung.

Eine Mustervorlage dient nur zum Vergleichen. Sie wird **nicht automatisch über deine echten Daten geschrieben**.

## Entwicklungs-Lerngedächtnis

Das Toolprojekt merkt sich inzwischen auch Entwicklungslektionen. Neu hinzugekommen sind unter anderem:

- zukünftige Zeitberechnung muss echte Zeitzonenregeln berücksichtigen,
- Reminder brauchen einen gespeicherten Quittierungszustand,
- Tests dürfen versionierte Nummern nicht unnötig doppelt hart speichern.

Diese Datei enthält keine privaten Nutzerdaten.

## TODOs und Ereignisse

TODOs bleiben nach Neustart erhalten. Verwendete Titel können wieder angeboten werden. Erledigte TODOs wandern mit Zeitstempel ins Archiv statt gelöscht zu werden.

Wichtige Ereignisse werden mit einem kurzen verständlichen Satz gespeichert. Dashboard V2 zeigt davon standardmäßig die letzten fünf.

## Datenschutz

- kein Internetzwang,
- Backend nur lokal auf `127.0.0.1`,
- keine Telemetrie,
- keine externen Python-Pakete,
- lokale Config-/TODO-/Event-/Kalenderdaten nicht im Release-ZIP.

## Bedienprinzip

**Button → Auswahldialog → gemerkte Auswahl → Preset/Empfehlung → erst dann eigene Texteingabe.**

## Ampelsystem

- 🟢 bereit / erfolgreich
- 🟡 optional / Hinweis
- 🟠 prüfen / Entscheidung nötig
- 🔴 Fehler / Risiko / Eingriff nötig

Farbe wird immer zusätzlich durch Text erklärt.

## Was kommt als Nächstes?

Als nächstes wird **Dashboard V2** gebaut. Dort sollen die bereits getesteten Daten einfach sichtbar werden:

- Monatskalender,
- nächste Termine,
- nächste drei TODOs,
- letzte fünf Ereignisse,
- Versions-/Gesundheitsstatus,
- Reminder-Hinweise,
- Debug-/Diagnosezugang.

Danach werden die reale Kubuntu-/Browser-/Zoom-Bedienung geprüft und anschließend die ersten sicheren Dateioperationen aufgebaut.

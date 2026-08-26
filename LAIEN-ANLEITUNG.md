# LAIEN-ANLEITUNG

## Was ist AIO-Tool?

AIO-Tool bündelt wiederkehrende Aufgaben in einer gemeinsamen, lokalen Oberfläche. Die Bedienung soll einfach, sichtbar und sicher bleiben.

## Aktueller Stand: 0.2.1-robustness

Der bisherige Versions-, Ereignis- und TODO-Kern wurde um zusätzliche Schutzschichten ergänzt:

- geprüfte Musterdateien,
- Testdateien für typische Fehler,
- verständliche und versionierte Hilfetexte,
- intelligente Fehlerhinweise,
- ein Entwicklungs-Lerngedächtnis, damit bekannte Fehlerarten nicht immer wieder neu entstehen.

## Was sind Mustervorlagen?

Eine Mustervorlage zeigt, wie eine gültige Config- oder JSON-Datei aussehen soll. Sie dient als **Vergleich**, nicht als automatischer Ersatz.

Wenn deine lokale Datei beschädigt ist, darf das Tool die Musterdatei nicht einfach darüberkopieren. Stattdessen soll es erklären, was nicht stimmt und welche sichere Möglichkeit du hast.

## Intelligente Fehlerhilfe

Bei bekannten Fehlern kann das Backend jetzt zusätzlich angeben:

- 🔴/🟠/🟡 wie kritisch das Problem ist,
- was wahrscheinlich passiert ist,
- was du als Nächstes tun kannst,
- ob ein erneuter Versuch sicher ist,
- welche geprüfte Mustervorlage zum Vergleichen passt.

Technische Details bleiben für Diagnosezwecke vorhanden, stehen aber nicht an erster Stelle.

## Versionierte Texte

Wiederkehrende Meldungen werden zentral gespeichert. Dadurch können sie gemeinsam verbessert und geprüft werden, statt an vielen Stellen leicht unterschiedlich zu werden.

## Entwicklungs-Lerngedächtnis

`LEARNING_MEMORY.jsonl` enthält **keine privaten Nutzerdaten**. Dort stehen Entwicklungslektionen wie:

- optionale Werte ausdrücklich testen,
- Eingabefehler und beschädigte Dateien unterscheiden,
- Prüfungen dürfen nichts verändern,
- eine Version niemals ohne Prüfnachweis als getestet markieren.

Die automatische Prüfung kontrolliert auch diese Datei.

## TODOs und Ereignisse

TODOs bleiben nach Neustart erhalten. Verwendete Titel können wieder angeboten werden. Ein erledigtes TODO wird mit Zeitstempel ins Archiv verschoben statt gelöscht.

Wichtige Ereignisse werden mit einem kurzen verständlichen Satz gespeichert. Später zeigt das Dashboard davon standardmäßig die letzten fünf.

## Datenschutz

- kein Internetzwang,
- Backend nur lokal auf `127.0.0.1`,
- keine Telemetrie,
- keine externen Python-Pakete,
- lokale TODO-/Event-/Config-Daten nicht im Release-ZIP.

## Bedienprinzip

**Button → Auswahldialog → gemerkte Auswahl → Preset/Empfehlung → erst dann eigene Texteingabe.**

## Ampelsystem

- 🟢 bereit / erfolgreich
- 🟡 optional / Hinweis
- 🟠 prüfen / Entscheidung nötig
- 🔴 Fehler / Risiko / Eingriff nötig

Farbe wird immer zusätzlich durch Text erklärt.

## Was kommt als Nächstes?

Als nächstes wird der **Kalender-Core** gebaut: Termine persistent speichern, Erinnerungszeiten verwalten, Monats-/Wochen-/Jahresdaten erzeugen und eine TODO-Verknüpfung nur optional anbieten.

Danach folgt das kompaktere Dashboard mit den nächsten drei TODOs, Terminen, den letzten fünf Ereignissen und einem direkten Debug-Zugang.

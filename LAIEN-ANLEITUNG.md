# LAIEN-ANLEITUNG

## Was ist AIO-Tool?

AIO-Tool soll viele wiederkehrende Aufgaben in einer gemeinsamen Oberfläche bündeln. Der Schwerpunkt liegt auf einfacher Bedienung, klaren Schritten und sicheren Änderungen.

## Aktueller Stand

Das Repository befindet sich bewusst in der Phase **CLEAN FOUNDATION**. Es gibt noch kein fertiges Programm zum Starten. Zuerst werden Regeln, Aufbau, Sicherheit und Entwicklungsreihenfolge sauber festgelegt.

## Wie soll die spätere Bedienung funktionieren?

1. Tool starten.
2. Projekt oder Aufgabe über Buttons auswählen.
3. Das Tool prüft Voraussetzungen.
4. Passende Aktion auswählen.
5. Vor einer Änderung erscheint eine verständliche Vorschau.
6. Kritische Änderungen werden bestätigt.
7. Während der Arbeit zeigt das Tool Fortschritt und aktuellen Schritt.
8. Danach wird das Ergebnis kontrolliert.
9. Falls möglich, kann die Änderung rückgängig gemacht oder ein Recovery-Stand genutzt werden.

## Wichtiges Bedienprinzip

Du sollst möglichst wenig technische Zeichen oder Pfade eintippen müssen.

Bevorzugt werden:

- große Buttons,
- verständliche Auswahldialoge,
- empfohlene Standards,
- zuletzt verwendete sichere Auswahlmöglichkeiten,
- Presets,
- kurze Erklärungen.

Freitext wird nur verwendet, wenn er wirklich nötig ist, zum Beispiel für eine Notiz.

## Ampelsystem

- 🟢 **bereit** – alles in Ordnung.
- 🟡 **optional** – kann sinnvoll sein, ist aber nicht zwingend.
- 🟠 **prüfen** – eine Entscheidung oder ein möglicher Konflikt ist offen.
- 🔴 **Eingriff** – Risiko, Fehler oder wichtige Schutzmaßnahme.

Die Farbe wird immer zusätzlich durch Text oder Symbol erklärt.

## Sicherheit

AIO-Tool soll Änderungen nicht einfach im Hintergrund durchführen.

Bei wichtigen Dateiaktionen ist vorgesehen:

`Auswählen → prüfen → Vorschau → bestätigen → ausführen → nachprüfen → bei Bedarf rückgängig`

Endgültiges Löschen soll nicht der normale Standard sein.

## Wenn etwas schiefgeht

Das spätere Tool soll verständlich zeigen:

- was passiert ist,
- welcher Schritt betroffen ist,
- ob Daten verändert wurden,
- ob weitergearbeitet werden kann,
- welche sichere Lösung empfohlen wird.

Längere Aufgaben sollen nach Möglichkeit pausiert, abgebrochen oder später fortgesetzt werden können.

## Datenschutz

Die Kernfunktionen sind offline-first geplant. Es soll keine versteckte Telemetrie geben. Internetfunktionen werden nur ergänzt, wenn ihr Zweck klar dokumentiert ist.

## Für Entwickler

Die technischen Regeln stehen in `AGENTS.md`. Offene Arbeit steht in `TODO.md`. Bekannte Regressionen und Prüfregeln stehen in `REGRESSIONSINFOS.md`.

# TOOLBESCHREIBUNG

## Produktname

**AIO-Tool**

## Produktidee

AIO-Tool ist ein lokales, modulares All-in-One-Werkzeug für wiederkehrende Datei-, Projekt-, Organisations- und Automatisierungsaufgaben. Häufige Abläufe sollen in einer einheitlichen, sicheren und laienfreundlichen Oberfläche zusammengeführt werden.

## Leitidee der Bedienung

**Keine Zeicheneingabe, wenn eine Auswahl ausreicht.**

Reihenfolge: Button → Auswahldialog → Preset/zuletzt verwendet → Empfehlung → Freitext nur als Fallback.

## Aktueller technischer Kern

### VersionRegistry

Getrackte Projekt-Historie und lokale Runtime-Registry mit Status, Commit-SHA, Änderungen, bekannten Problemen, Regressionstatus und Evidenz. Getestet/freigegeben darf nicht ohne Prüfnachweis vergeben werden.

### EventRegistry

Persistente wichtige Ereignisse mit eigenem verständlichem Meldungstext und getrennten technischen Details. Dashboard V2 zeigt davon standardmäßig die letzten fünf.

### TODO-Core

Persistente TODOs mit Titelgedächtnis, optionalem Datum/Kalenderbezug und Erledigt-Archiv mit Zeitstempel. Die nächsten drei offenen TODOs können serverseitig ermittelt werden.

### Calendar-Core 0.3.0

Persistente Kalendertermine auf demselben atomaren Datenvertrag wie die übrigen Domänenmodelle.

Unterstützt werden:

- Titel und Datum,
- optionale Start-/Endzeit,
- optionale Kategorie und Beschreibung,
- optionale TODO-Verknüpfung,
- Titelgedächtnis,
- Monats-/Wochen-/Jahresperioden,
- Reminder 0/10/30/60/1440 Minuten vorher,
- fällige Reminder mit separater persistenter Quittierung,
- lokale Systemzeitzone via `zoneinfo` für korrekte DST-Berechnung.

Die sichtbare Kalender-/Reminderdarstellung wird bewusst im nachfolgenden Dashboard-Slice implementiert. Domänenlogik bleibt im Backend.

## Robustheitskern

AIO-Tool schützt nicht nur Nutzerdaten, sondern zunehmend auch den Entwicklungsprozess selbst.

### Mustervorlagen und Testdaten

Jedes langlebige JSON-/Config-Format besitzt eine geprüfte Referenzdatei. Positive Testdaten müssen akzeptiert, bekannte negative Testfälle gezielt abgelehnt werden. Der Kalender folgt demselben Vertrag.

Mustervorlagen sind Vergleichshilfen und dürfen niemals still über Nutzerdaten geschrieben werden.

### Versionierte Texte

Wiederkehrende Nutzer- und Systemmeldungen werden in einem versionierten deutschen Textkatalog gepflegt. Dadurch lassen sich Sprache, Verständlichkeit und Konsistenz zentral testen und erweitern.

### Intelligente Fehlerhilfe

Versionierte Fehlerregeln ordnen bekannte Fehlerfamilien einer verständlichen Erklärung, Ampelstufe und sicheren nächsten Handlung zu. Kalenderfehler wie ungültiges Datum, Reminder ohne Uhrzeit oder unzulässige Terminzeiten sind darin integriert.

### Entwicklungs-Lerngedächtnis

`LEARNING_MEMORY.jsonl` bewahrt bestätigte Entwicklungslektionen. Der Learning Guard validiert diese Datei in CI. Aktuelle Strukturlektionen betreffen unter anderem optionale Felder, Fehlerklassifikation, Zeit-/DST-Verträge, Reminder-Quittierung und versionierte Metadaten.

### Codesparendes Patchen

Vor breiten Umbauten wird die kleinste verantwortliche Codezone bestimmt: Datei, Funktion/Klasse, Zeilenbereich und passender Test. Lokale Fixes mit Regression werden bevorzugt.

## Nächster Organisationsschritt: Dashboard V2

Der nächste Slice verändert möglichst keine Domänenlogik, sondern macht die vorhandenen getesteten Daten nutzbar sichtbar:

- Monatskalender als dauerhafte Übersicht,
- nächste Termine,
- nächste drei TODOs,
- letzte fünf Ereignisse,
- Version/Registry-/Gesundheitsstatus,
- fällige Reminder mit Quittierung erst nach sichtbarer Darstellung,
- direkter Debug-/Diagnosezugang,
- kleiner ein-/ausblendbarer Entwicklungsbereich,
- häufig genutzte Funktionen getrennt von „Alle“,
- linker modularer Kachelbereich,
- responsive Dichte und Zoom-/Tastaturfreundlichkeit.

## Sicherheitsphilosophie

Für verändernde Operationen gilt grundsätzlich:

`Vorprüfung → Vorschau → Bestätigung → Aktion → Nachprüfung → Protokoll → Undo/Recovery`

Prüfungen bleiben seiteneffektfrei. Ein sekundärer Protokollfehler darf eine bereits sicher gespeicherte Hauptaktion nicht rückwirkend als fehlgeschlagen darstellen.

Für Reminder gilt zusätzlich:

`fällig → sichtbar darstellen → erst danach quittieren`

## Technische Richtung

- Linux/Kubuntu zuerst,
- lokale Browseroberfläche,
- Loopback-Backend,
- Standardbibliothek bevorzugt,
- keine Telemetrie,
- atomare Persistenz,
- `zoneinfo` für lokale zukünftige Zeitregeln,
- versionierte Schemata/Text-/Fehlerverträge,
- reproduzierbare Tests und Releases,
- Release-ZIP als automatisch geprüftes CI-Artefakt.

## Definition eines guten Workflows

Ein Laie soll jederzeit beantworten können:

1. Wo bin ich?
2. Was passiert gerade?
3. Was soll ich als Nächstes tun?
4. Was wird verändert?
5. Kann ich es rückgängig machen?
6. Was ist das Ergebnis?

Wenn eine Hauptansicht diese Fragen nicht beantwortet, ist sie noch nicht fertig optimiert.

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

Persistente wichtige Ereignisse mit eigenem verständlichem Meldungstext und getrennten technischen Details. Das spätere Dashboard zeigt davon standardmäßig die letzten fünf.

### TODO-Core

Persistente TODOs mit Titelgedächtnis, optionalem Datum/Kalenderbezug und Erledigt-Archiv mit Zeitstempel. Die nächsten drei offenen TODOs können serverseitig ermittelt werden.

## Robustheitskern 0.2.1

AIO-Tool schützt nicht nur Nutzerdaten, sondern zunehmend auch den Entwicklungsprozess selbst.

### Mustervorlagen und Testdaten

Jedes langlebige JSON-/Config-Format soll eine geprüfte Referenzdatei besitzen. Positive Testdaten müssen akzeptiert, bekannte negative Testfälle gezielt abgelehnt werden. Mustervorlagen sind Vergleichshilfen und dürfen niemals still über Nutzerdaten geschrieben werden.

### Versionierte Texte

Wiederkehrende Nutzer- und Systemmeldungen werden in einem versionierten deutschen Textkatalog gepflegt. Dadurch lassen sich Sprache, Verständlichkeit und Konsistenz zentral testen und später erweitern.

### Intelligente Fehlerhilfe

Versionierte Fehlerregeln ordnen bekannte Fehlerfamilien einer verständlichen Erklärung, Ampelstufe und sicheren nächsten Handlung zu. Optional kann eine passende Mustervorlage genannt werden. Ein unbekannter Fehler behauptet keine automatische Recovery.

### Entwicklungs-Lerngedächtnis

`LEARNING_MEMORY.jsonl` bewahrt bestätigte Entwicklungslektionen. Der Learning Guard validiert diese Datei in CI. Strukturelle Fehler sollen künftig nicht nur lokal repariert, sondern als Regel + Regression dauerhaft gegen Wiederholung abgesichert werden.

### Codesparendes Patchen

Vor breiten Umbauten wird die kleinste verantwortliche Codezone bestimmt: Datei, Funktion/Klasse, Zeilenbereich und passender Test. Lokale Fixes mit Regression werden bevorzugt.

## Geplanter Organisationsbereich

Als nächster Schritt entsteht der Kalender-Core:

- Termine persistent speichern,
- Titel merken und wieder anbieten,
- Erinnerungen verwalten,
- Monats-/Wochen-/Jahresdaten erzeugen,
- TODO-Verknüpfung optional halten.

Danach folgt Dashboard V2 mit nächsten drei TODOs, Terminen, letzten fünf Ereignissen und Debug-Zugang.

## Sicherheitsphilosophie

Für verändernde Operationen gilt grundsätzlich:

`Vorprüfung → Vorschau → Bestätigung → Aktion → Nachprüfung → Protokoll → Undo/Recovery`

Prüfungen bleiben seiteneffektfrei. Ein sekundärer Protokollfehler darf eine bereits sicher gespeicherte Hauptaktion nicht rückwirkend als fehlgeschlagen darstellen.

## Technische Richtung

- Linux/Kubuntu zuerst,
- lokale Browseroberfläche,
- Loopback-Backend,
- Standardbibliothek bevorzugt,
- keine Telemetrie,
- atomare Persistenz,
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

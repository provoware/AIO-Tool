# TOOLBESCHREIBUNG

## Produktname

**AIO-Tool**

## Produktidee

AIO-Tool ist ein lokales, modulares All-in-One-Werkzeug für wiederkehrende Datei-, Projekt-, Organisations- und Automatisierungsaufgaben. Häufige Abläufe sollen in einer einheitlichen, sicheren und laienfreundlichen Oberfläche zusammengeführt werden.

## Zielgruppe

Primär:

- Nutzer ohne technisches Spezialwissen,
- Nutzer, die klare visuelle Führung bevorzugen,
- Nutzer, die lokale/offline Arbeitsweisen möchten,
- Nutzer mit wiederkehrenden Datei- und Projektabläufen.

Sekundär:

- fortgeschrittene Nutzer über einen bewusst eingeblendeten Expertenbereich.

## Leitidee der Bedienung

**Keine Zeicheneingabe, wenn eine Auswahl ausreicht.**

Das Tool bietet zuerst Buttons, Dialoge, Presets, Favoriten und zuletzt verwendete sichere Eingaben. Eigene Texteingabe bleibt ein gezielter Fallback.

## Technischer Grundkern

Seit `0.2.0-core` besitzt AIO-Tool einen gemeinsamen persistenten Datenkern.

### VersionRegistry

Die Versionierung wird nicht nur über eine sichtbare Versionsnummer dargestellt, sondern über eine persistente Registry mit:

- Versionsnummer,
- Erstellungszeit,
- Entwicklungs-/Test-/Release-Status,
- optionalem Commit-SHA,
- Zusammenfassung und Änderungen,
- bekannten Problemen,
- Regressionstatus,
- Evidenznachweisen.

Ein Prüf-/Release-Status darf nicht ohne Evidenz vergeben werden.

### EventRegistry

Wichtige Ereignisse werden in einer separaten Registry in verständlicher Sprache festgehalten. Technische Details bleiben optional getrennt.

Die spätere Standardansicht im Dashboard zeigt höchstens die letzten fünf relevanten Ereignisse, neuestes zuerst.

### TODO-Core

TODOs sind persistent und bleiben auch nach einem Neustart erhalten.

Ein TODO kann enthalten:

- Titel,
- Kategorie optional,
- Datum/Uhrzeit optional,
- Priorität,
- Notiz optional,
- optionale Kalenderverknüpfung.

Wiederkehrende Titel werden lokal gemerkt und als spätere Auswahl vorbereitet. Abgehakte TODOs werden mit Zeitstempel in ein Erledigt-Archiv verschoben statt gelöscht.

## Geplanter Startablauf

1. Klick-&-Start.
2. System- und Abhängigkeitsprüfung.
3. fehlende lokale Voraussetzungen verständlich auflösen.
4. Projektordner auswählen oder anlegen.
5. Berechtigungen transparent klären.
6. Profil auswählen.
7. Einstellungen und persistente Daten laden.
8. Dashboard öffnen.

## Hauptoberfläche

Geplant bzw. teilweise vorbereitet sind:

- kompaktes Dashboard mit klaren Statusinformationen,
- adaptive Navigation,
- Favoriten / Schnellaktionen,
- sichtbarer nächster Schritt,
- aktiver Vorgang mit Fortschritt,
- Ampelstatus,
- Projektkontext,
- nächste drei TODOs,
- optionaler Kalenderbereich,
- letzte fünf Ereignisse in einfacher Sprache,
- direkter Debug-/Diagnosezugang,
- optionaler Expertenbereich,
- mehrere Farbthemes und veränderbare Schriftgröße.

## Funktionsbereiche

### Projekte

Projektordner prüfen, anlegen, wechseln und den aktuellen Kontext sichtbar halten.

### Sichere Dateioperationen

Suchen, kopieren, verschieben, umbenennen und später weitere Operationen – jeweils mit Vorschau, Konfliktbehandlung, Prüfung und Recovery-Vertrag.

### Organisation

TODOs, Kalender, Notizen und projektbezogene Informationen. TODOs dürfen vollständig ohne Kalender funktionieren; Kalenderverknüpfung ist optional.

### Entwicklerinformationen

Notizen zu Fehlern, Schwachstellen, Aufgaben, Optimierungen, Entscheidungen und Regressionen. Wiederverwendbare Titel sollen gemerkt und als Auswahl angeboten werden.

### Verlauf und Reports

Nachvollziehbar zeigen, was ausgeführt, geprüft oder geändert wurde. Die EventRegistry bildet dafür den ersten persistenten Kern.

### Versionierung

Versionsstand, Vorgängerversion, Status, Evidenz und bekannte Probleme sollen zentral verwaltet werden. Widersprüche zwischen Registry, VERSION, CHANGELOG und Manifest werden schrittweise automatisiert erkannt.

### Presets und Automatisierung

Wiederkehrende Abläufe speichern und kontrolliert automatisieren. Kritische Aktionen bleiben absicherbar.

## Sicherheitsphilosophie

Eine Funktion ist nicht allein deshalb fertig, weil der Normalfall funktioniert. Relevante Fehler- und Abbruchfälle gehören zum Funktionsvertrag.

Für verändernde Operationen gilt grundsätzlich:

`Vorprüfung → Vorschau → Bestätigung → Aktion → Nachprüfung → Protokoll → Undo/Recovery`

## Technische Richtung

- Linux/Kubuntu zuerst.
- lokale browserbasierte Oberfläche.
- lokales Backend nur auf Loopback.
- möglichst wenige externe Abhängigkeiten.
- modulare Architektur.
- persistent, aber datensparsam.
- Schema-Versionen und Migrationen für langlebige lokale Daten.
- reproduzierbare Tests und Releases.

## Nicht-Ziele der ersten Version

- keine Cloud-Pflicht,
- keine Telemetrieplattform,
- kein ungeprüfter Funktionssammler,
- keine automatische endgültige Löschung,
- keine Expertenoberfläche als Standard,
- keine große Plugin-Landschaft vor stabilem Kern.

## Definition eines guten AIO-Tool-Workflows

Ein Laie soll jederzeit beantworten können:

1. Wo bin ich?
2. Was passiert gerade?
3. Was soll ich als Nächstes tun?
4. Was wird verändert?
5. Kann ich es rückgängig machen?
6. Was ist das Ergebnis?

Wenn eine Hauptansicht diese Fragen nicht ausreichend beantwortet, ist sie noch nicht fertig optimiert.

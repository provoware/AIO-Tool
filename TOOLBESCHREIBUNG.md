# TOOLBESCHREIBUNG

## Produktname

**AIO-Tool**

## Produktidee

AIO-Tool ist als lokales, modulares All-in-One-Werkzeug für wiederkehrende Datei-, Projekt-, Organisations- und Automatisierungsaufgaben geplant. Statt viele Spezialprogramme einzeln bedienen zu müssen, sollen häufige Abläufe in einer einheitlichen, sicheren und laienfreundlichen Oberfläche zusammengeführt werden.

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

Das Tool soll zuerst Buttons, Dialoge, Presets, Favoriten und zuletzt verwendete sichere Eingaben anbieten. Eigene Texteingabe bleibt als gezielter Fallback erhalten.

## Geplanter Startablauf

1. Klick-&-Start.
2. System- und Abhängigkeitsprüfung.
3. fehlende lokale Voraussetzungen verständlich auflösen.
4. Projektordner auswählen oder anlegen.
5. Berechtigungen transparent klären.
6. Profil auswählen.
7. Einstellungen laden.
8. Dashboard öffnen.

## Hauptoberfläche

Geplant sind:

- Dashboard mit klaren Statusinformationen,
- linke oder adaptive Navigation,
- Favoriten / Schnellaktionen,
- sichtbarer nächster Schritt,
- aktiver Vorgang mit Fortschritt,
- Ampelstatus,
- Projektkontext,
- optionaler Expertenbereich,
- mehrere Farbthemes und veränderbare Schriftgröße.

## Funktionsbereiche

### Projekte

Projektordner prüfen, anlegen, wechseln und den aktuellen Kontext sichtbar halten.

### Sichere Dateioperationen

Suchen, kopieren, verschieben, umbenennen und später weitere Operationen – jeweils mit Vorschau, Konfliktbehandlung, Prüfung und Recovery-Vertrag.

### Organisation

Aufgaben, Kalender, Notizen und projektbezogene Informationen.

### Entwicklerinformationen

Notizen zu Fehlern, Schwachstellen, Aufgaben, Optimierungen, Entscheidungen und Regressionen. Wiederverwendbare Titel werden gemerkt und als Auswahl angeboten.

### Verlauf und Reports

Nachvollziehbar zeigen, was ausgeführt, geprüft oder geändert wurde.

### Presets und Automatisierung

Wiederkehrende Abläufe speichern und kontrolliert automatisieren. Kritische Aktionen bleiben absicherbar.

## Sicherheitsphilosophie

Eine Funktion ist nicht allein deshalb fertig, weil der Normalfall funktioniert. Relevante Fehler- und Abbruchfälle gehören zum Funktionsvertrag.

Für verändernde Operationen gilt grundsätzlich:

`Vorprüfung → Vorschau → Bestätigung → Aktion → Nachprüfung → Protokoll → Undo/Recovery`

## Technische Richtung

- Linux/Kubuntu zuerst.
- lokale, browserbasierte Oberfläche ist bevorzugt, sofern sie den Funktionsvertrag erfüllt.
- lokales Backend nur auf Loopback.
- möglichst wenige externe Abhängigkeiten.
- modulare Architektur.
- persistent, aber datensparsam.
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

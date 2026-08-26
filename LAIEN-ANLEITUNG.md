# LAIEN-ANLEITUNG

## Was ist AIO-Tool?

AIO-Tool bündelt wiederkehrende Aufgaben in einer gemeinsamen Oberfläche. Die Bedienung soll einfach, sichtbar und sicher bleiben.

## Aktueller Entwicklungsstand

Die Version `0.2.0-core` erweitert den startbaren Grundkern um eine sichere lokale Datenbasis.

Neu vorbereitet sind:

- professionelle Versionsverwaltung,
- verständliche Ereignishistorie,
- persistente TODOs,
- gemerkte TODO-Titel,
- Erledigt-Archiv mit Zeitstempel.

Die sichtbare Kalender- und TODO-Oberfläche folgt im nächsten Entwicklungsschritt.

## Was bedeutet „persistent“?

Das bedeutet einfach:

> Das Tool kann Informationen lokal speichern und nach einem Neustart wiederfinden.

Die neuen Daten liegen nur im lokalen `runtime`-Bereich. Sie werden nicht ins Internet übertragen und nicht in ein Release-ZIP übernommen.

## TODO-Grundprinzip

Ein TODO kann später bequem über Buttons und Auswahldialoge angelegt werden.

Gespeichert werden können:

- Titel,
- Kategorie optional,
- Datum/Uhrzeit optional,
- Priorität,
- Notiz optional.

Ein Kalender ist **nicht Pflicht**.

### Bereits verwendete Titel

Wenn du denselben oder einen ähnlichen TODO-Titel mehrfach nutzt, merkt das Tool den Titel lokal.

Beispiel:

`Backup prüfen`

Beim nächsten Mal kann dieser Titel als Auswahl angeboten werden. Dadurch musst du weniger tippen.

### TODO abhaken

Ein erledigtes TODO wird nicht einfach gelöscht.

Stattdessen:

`Offen → abhaken → Archiv / Erledigt`

Dabei bleibt erhalten:

- ursprünglicher Titel,
- Erstellungszeit,
- weitere Angaben,
- Zeitpunkt der Erledigung.

## Ereignisse

Wichtige Aktionen werden in einfacher Sprache vorbereitet.

Beispiele:

- „TODO „Backup prüfen“ wurde angelegt.“
- „TODO „Backup prüfen“ wurde erledigt und ins Archiv verschoben.“
- „Version 0.2.0-core wurde als neuer Entwicklungsstand registriert.“

Technische Rohdaten sollen später nicht die normale Ereignisanzeige überladen. Das Dashboard wird standardmäßig nur die letzten fünf verständlichen Ereignisse zeigen.

## Versionierung

Das Tool besitzt jetzt eine eigene Versions-Registry.

Sie unterscheidet unter anderem:

- Entwicklung,
- getestet,
- Release Candidate,
- freigegeben,
- veraltet.

Wichtig:

> Eine Version darf nicht einfach als getestet oder freigegeben markiert werden, wenn kein Prüfnachweis vorhanden ist.

## Start unter Kubuntu/Linux

1. Öffne den AIO-Tool-Ordner.
2. Starte `start_tool.sh`.
3. Beim ersten Start richtet das Tool automatisch `.venv` ein.
4. Danach läuft eine kurze Vorprüfung.
5. Das Backend startet nur lokal auf deinem Rechner.
6. Die Oberfläche öffnet sich im Browser.

Falls nötig:

```bash
chmod +x start_tool.sh
./start_tool.sh
```

## Datenschutz

- Kernfunktionen brauchen kein Internet.
- Backend nur auf `127.0.0.1`.
- keine Telemetrie als Standard.
- keine externen Python-Pakete.
- TODOs, Ereignisse und Registry-Daten bleiben lokal.

## Bedienprinzip

Du sollst möglichst wenig technische Zeichen oder Pfade eintippen müssen.

Reihenfolge:

1. Buttons,
2. Auswahldialoge,
3. zuletzt verwendete sichere Auswahl,
4. Presets / Empfehlungen,
5. Freitext nur wenn wirklich nötig.

## Ampelsystem

- 🟢 **bereit** – alles in Ordnung.
- 🟡 **optional** – kann sinnvoll sein.
- 🟠 **prüfen** – Entscheidung oder Prüfung offen.
- 🔴 **Eingriff** – Fehler, Risiko oder Schutzmaßnahme nötig.

Farbe wird immer zusätzlich mit Text oder Symbol erklärt.

## Was kommt als Nächstes?

Als nächster Slice wird das **Kalendermodul** auf dieselbe sichere Datenbasis gesetzt.

Danach werden im Dashboard integriert:

- die nächsten drei TODOs,
- optionale Kalenderinformationen,
- die letzten fünf Ereignisse,
- direkter Zugang zum Debug-/Diagnosemodul.

Echte Dateioperationen folgen erst danach kontrolliert mit Copy als erstem SAFE-FILE-CORE-Schritt.

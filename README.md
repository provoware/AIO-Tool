# AIO-Tool

> Modulares, laienfreundliches, offline-first All-in-One-Tool mit lokalem Backend.

## Status

- **Phase:** P1 — gemeinsamer persistenter Kern
- **Version:** `0.2.0-core`
- **Datum:** 2026-08-27
- **Zielsystem:** primär Linux/Kubuntu
- **Oberfläche:** Browser-UI
- **Backend:** Python-Standardbibliothek, ausschließlich Loopback
- **Externe Python-Pakete:** keine

## Was ist bereits vorhanden?

Die Clean Foundation bleibt erhalten und wurde um den ersten gemeinsamen Datenkern erweitert:

- Klick-&-Start über `start_tool.sh`,
- lokale `.venv` ohne Fremdpakete,
- idempotenter Mehrfachstartschutz,
- lokales Backend auf `127.0.0.1`,
- Host-/Origin-Prüfung und Security-Header,
- atomare Konfiguration mit Backup-Fallback,
- responsive Dashboard-Shell mit 4 Themes und Schriftgrößen-Presets,
- **VersionRegistry** mit Status-, Release- und Evidenzvertrag,
- **EventRegistry** für kurze menschenlesbare Ereignisse,
- **TODO-Datenmodell** mit aktiven Einträgen, Titelgedächtnis und Erledigt-Archiv,
- API für Versionen, Ereignisse, TODOs, Titelvorschläge und Abhaken,
- automatische Tests, Vorvalidierung und reproduzierbarer Release-Builder.

## Persistenter Kern

### VersionRegistry

`runtime/versions.json`

Speichert:

- aktuelle Version,
- bekannte Versionen,
- Entwicklungs-/Test-/Release-Status,
- Commit-SHA optional,
- Änderungen,
- bekannte Probleme,
- Regressionstatus,
- Evidenznachweise.

Wichtig: Ein Stand darf nicht auf `tested`, `release-candidate` oder `released` gesetzt werden, solange kein Evidenznachweis hinterlegt ist.

### EventRegistry

`runtime/events.json`

Speichert wichtige Ereignisse in einfacher Sprache, z. B.:

> TODO „Dashboard prüfen“ wurde erledigt und ins Archiv verschoben.

Die Registry ist auf die letzten 500 Ereignisse begrenzt. Das Dashboard wird später standardmäßig die letzten fünf anzeigen.

### TODO-Core

`runtime/todos.json`

Ein TODO kann enthalten:

- Titel,
- Kategorie optional,
- Datum/Uhrzeit optional,
- Priorität,
- Notiz optional,
- optionale spätere Kalenderverknüpfung.

Beim Erledigen wird ein TODO **nicht gelöscht**, sondern mit Zeitstempel ins Archiv verschoben. Bereits verwendete Titel werden lokal gemerkt und können später wieder als Buttons/Auswahl angeboten werden.

## API-Grundvertrag

Lesend:

- `GET /api/status`
- `GET /api/versions`
- `GET /api/events?limit=5`
- `GET /api/todos`
- `GET /api/todos/archive`
- `GET /api/todos/suggestions`

Schreibend:

- `POST /api/config`
- `POST /api/todos`
- `POST /api/todos/<id>/complete`

Schreibende Aufrufe bleiben an den bestehenden lokalen Host-/Origin-Vertrag gebunden.

## Schnellstart unter Kubuntu/Linux

1. Repository herunterladen oder klonen.
2. `start_tool.sh` ausführbar machen, falls nötig: `chmod +x start_tool.sh`.
3. `./start_tool.sh` starten.
4. Beim ersten Start wird lokal `.venv` erzeugt.
5. Das Backend bindet ausschließlich an `127.0.0.1:8765` und die Oberfläche öffnet sich im Browser.

Es werden keine externen Python-Pakete installiert.

## Produktprinzipien

1. **Auswahl vor Zeicheneingabe** – Buttons, Presets und Auswahldialoge vor Freitext.
2. **Laien zuerst** – Alltagssprache, sichtbarer nächster Schritt, kurze Hilfen.
3. **Offline-first** – kein Internetzwang, keine Telemetrie als Standard.
4. **Sicherheit vor Bequemlichkeit** – Vorschau, Vor-/Nachprüfung, Undo/Recovery für verändernde Operationen.
5. **Transparenz** – Fortschritt, Fehler, Ergebnis und Auswirkungen sichtbar.
6. **Modularität** – UI, Backend, Persistenz und Domänenlogik getrennt.
7. **Datensparsamkeit** – nur notwendige lokale Daten.
8. **Wartbarkeit** – kleine überprüfbare Slices statt Großumbauten.
9. **Regression vor Wiederholung** – bestätigte Fehler als dauerhaftes Gate.
10. **Beweisbarer Status** – `UMGESETZT`, `GEPRÜFT`, `BEWIESEN` werden getrennt verwendet.

## Projektstruktur

```text
app/                    # Backend, Persistenz und Datenmodelle
web/                    # Browser-Oberfläche
scripts/                # Validierung und Release-Builder
tests/                  # automatisierte Regression-/Vertragstests
runtime/                # lokale Laufzeitdaten; nicht im Release
.github/workflows/      # CI-Gates
start_tool.sh           # Klick-&-Start
start_tool.desktop      # Desktop-Starter-Vorlage
VERSION                 # Versionsquelle
```

## Entwicklung / Prüfung

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate.py
bash -n start_tool.sh
node --check web/app.js
python3 scripts/release.py --check
```

## Noch nicht enthalten

- Kalenderdatenmodell und Kalender-UI,
- Dashboard-Anzeige der letzten fünf Ereignisse,
- sichtbare TODO-Verwaltung im Dashboard,
- persistente Job-Queue,
- Copy-/Move-/Rename-/Delete-Operationen,
- Undo-/Recovery-Datensatz für reale Dateiaktionen.

Diese Trennung ist Absicht: Erst ein stabiler gemeinsamer Datenkern, dann Kalender/Dashboard und anschließend SAFE-FILE-CORE.

## Nächster Slice

Nach grünem Registry-/TODO-Core-Gate:

**Kalender-Core + Dashboard-Integration auf Basis der vorhandenen Registries.**

Danach folgt SAFE-FILE-CORE mit Copy als erster realer Dateioperation.

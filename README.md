# AIO-Tool

> Modulares, laienfreundliches, offline-first All-in-One-Tool mit lokalem Backend.

## Status

- **Phase:** CLEAN FOUNDATION — ausführbarer Kern
- **Version:** `0.1.1-foundation`
- **Datum:** 2026-08-27
- **Zielsystem:** primär Linux/Kubuntu
- **Oberfläche:** Browser-UI
- **Backend:** Python-Standardbibliothek, ausschließlich Loopback
- **Externe Python-Pakete:** keine

## Was ist bereits vorhanden?

Der erste ausführbare Foundation-Slice enthält bewusst noch keine verändernden Dateioperationen. Vorhanden sind:

- `start_tool.sh` als Klick-&-Start-Launcher,
- lokale `.venv` ohne Fremdpakete,
- idempotenter Start: vorhandene Instanz öffnen statt zweites Backend starten,
- lokales Python-Backend auf `127.0.0.1`,
- Host-/Origin-Prüfung für API-Schreibzugriffe,
- atomare JSON-Konfiguration mit Backup-Fallback,
- responsive Dashboard-Shell,
- 4 Themes,
- Schriftgrößen 90–140 % über Buttons,
- standardmäßig verborgener Expertenbereich,
- automatische Foundation-Validierung,
- Standardbibliothek-Unit-Tests,
- reproduzierbarer Release-Builder,
- GitHub-Actions-CI.

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
app/                    # Backend und Persistenz
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

Die CI führt diese Gates bei Push und Pull Request aus.

## Was ist ausdrücklich noch nicht enthalten?

- keine Copy-/Move-/Rename-/Delete-Operation,
- noch keine persistente Job-Queue,
- noch kein Undo-Datensatz für Dateiaktionen,
- noch kein Recovery-Center für reale Dateioperationen,
- noch keine produktive Projektverwaltung.

Diese Trennung ist Absicht: SAFE-FILE-CORE beginnt erst nach grünem Foundation-Gate.

## Nächster Slice

**P1 — SAFE-FILE-CORE: Copy zuerst**

`Quelle wählen → Ziel wählen → Vorprüfung → Vorschau → bestätigen → kopieren → nachprüfen → Undo-Datensatz`

Move, Rename und Löschen folgen erst nach belastbarer Copy-Evidenz.

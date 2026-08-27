# AIO-Tool

> Modulares, laienfreundliches, offline-first All-in-One-Tool mit lokalem Backend.

## Status

- **Phase:** P1 — Kalender-/Organisationskern
- **Version:** `0.3.0-calendar-core`
- **Status:** automatisiert getestet / `draft`
- **Datum:** 2026-08-27
- **Zielsystem:** primär Linux/Kubuntu
- **Oberfläche:** Browser-UI
- **Backend:** Python-Standardbibliothek, ausschließlich Loopback
- **Externe Python-Pakete:** keine

## Aktueller Kern

AIO-Tool besitzt inzwischen einen getesteten gemeinsamen Daten- und Robustheitskern:

- Klick-&-Start mit lokalem Loopback-Backend,
- atomare Config-Persistenz + Backup-Fallback,
- VersionRegistry mit Evidenzpflicht,
- EventRegistry mit verständlichen Ereignissen,
- persistenter TODO-Core mit Titelgedächtnis und Erledigt-Archiv,
- versionierte Muster-/Testdaten,
- versionierter deutscher Textkatalog,
- regelbasierte Fehlerhilfe,
- `LEARNING_MEMORY.jsonl` + CI-Learning-Guard,
- reproduzierbarer Release-Builder + vollständiges CI-ZIP,
- **persistenter Kalender-Core mit Erinnerungen, Perioden und optionaler TODO-Verknüpfung**.

## Kalender-Core 0.3.0

`app/calendar_store.py` verwaltet lokale Termine auf demselben atomaren Persistenzvertrag wie die übrigen Domänenmodelle.

Ein Termin unterstützt:

- Titel,
- Datum,
- optionale Startzeit,
- optionale Endzeit,
- optionale Kategorie,
- optionale Beschreibung,
- optionale TODO-Verknüpfung,
- lokale Zeitzone,
- Erinnerungen 0 / 10 / 30 / 60 / 1440 Minuten vorher.

### Kalenderansichten als Datenvertrag

Der Core liefert getestete Perioden für:

- **Monat** — echte Monatsgrenzen,
- **Woche** — Montag bis Sonntag,
- **Jahr** — vollständiges Kalenderjahr.

Die sichtbare Monats-/Wochen-/Jahresoberfläche folgt in Dashboard V2. Der Core selbst ist davon bewusst getrennt.

### Erinnerungen

Fällige Erinnerungen werden nur geliefert, solange sie noch nicht quittiert wurden. Die Quittierung speichert `notified_at` atomar, damit Polling denselben Reminder nicht immer wieder meldet.

Für zukünftige lokale Termine wird die echte System-Zeitzone über Python `zoneinfo` verwendet. Damit bleiben Sommer-/Winterzeitwechsel korrekt; ein fester aktueller UTC-Offset wird ausdrücklich nicht verwendet.

Eine sichtbare Browser-/Desktop-Benachrichtigung ist **noch kein Bestandteil des getesteten Core-Vertrags**. Dashboard V2 bindet diese Anzeige später an den vorhandenen Reminder-Core an.

## Kalender-API

Der lokale API-Vertrag umfasst unter anderem:

- Kalenderstatus / Terminanzahl,
- Termine anlegen,
- Monats-/Wochen-/Jahresperiode lesen,
- Titelvorschläge,
- fällige Reminder lesen,
- Reminder quittieren,
- optionale TODO-Verknüpfung validieren.

Kalender-Eingabefehler werden über die versionierte Fehlerhilfe mit verständlicher Erklärung und sicherer nächster Handlung beantwortet.

## Musterdateien und Testdaten

Geprüfte Referenzen unter `resources/templates/` umfassen jetzt:

- Config,
- VersionRegistry,
- EventRegistry,
- TODOs,
- Kalender.

`testdata/valid/` muss von denselben Produktvalidatoren akzeptiert werden. `testdata/invalid/` enthält gezielte Negativfälle, darunter Ende vor Beginn und Erinnerung ohne Startzeit.

**Mustervorlagen überschreiben niemals automatisch Nutzerdaten.**

## Entwicklungs-Lerngedächtnis

Das Learning Memory enthält inzwischen zusätzlich Regeln für:

- DST-/Zeitzonenberechnung,
- persistente Reminder-Quittierung,
- versionierte Metadaten ohne redundant hart codierte Testversionen.

Der CI-Schritt `python scripts/learning_guard.py` validiert diese Regeln bei jeder Änderung.

## Sicherheit und Datenschutz

- kein Internetzwang,
- keine Telemetrie,
- Backend nur `127.0.0.1`,
- Host-/Origin-Guard,
- keine externen Python-Pakete,
- atomare Persistenz + Backup-Fallback,
- Runtime/Nutzerdaten nicht im Release-ZIP.

## Entwicklung / Prüfung

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate.py
python3 scripts/learning_guard.py
bash -n start_tool.sh
node --check web/app.js
python3 scripts/release.py --check
```

Letzter getesteter Kalender-Codehead: GitHub Actions Run `33026180855` — **SUCCESS** inklusive Release-ZIP-Upload.

## Noch offen

- Dashboard V2: Kalender/TODO/Event/Version sichtbar integrieren,
- sichtbare Reminder-Anzeige im Browser,
- Debug-/Diagnosebereich,
- reale Kubuntu-/Firefox-/Chrome-/Zoom-Gates,
- anschließend SAFE-FILE-CORE.

## Nächster Slice

**Dashboard V2** — nächste drei TODOs, nächste Termine, Monatskalender, letzte fünf Ereignisse, Versions-/Gesundheitsstatus, Debugzugang und responsive Dichteführung auf Basis der bereits getesteten Core-APIs.

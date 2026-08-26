# AIO-Tool

> Modulares, laienfreundliches, offline-first All-in-One-Tool mit lokalem Backend.

## Status

- **Phase:** P1 — Robustheits- und Datenkern
- **Version:** `0.2.1-robustness`
- **Datum:** 2026-08-27
- **Zielsystem:** primär Linux/Kubuntu
- **Oberfläche:** Browser-UI
- **Backend:** Python-Standardbibliothek, ausschließlich Loopback
- **Externe Python-Pakete:** keine

## Aktueller Kern

Vorhanden sind Klick-&-Start, lokales Backend, atomare Konfiguration, VersionRegistry, EventRegistry und persistenter TODO-Core. Zusätzlich schützt `0.2.1-robustness` die Entwicklung selbst stärker:

- versionierte Config-/JSON-Mustervorlagen,
- gültige und absichtlich ungültige Testdaten,
- versionierter deutscher Textkatalog,
- regelbasierte Fehlerhilfe mit Ampelstufe und sicherer Handlungsempfehlung,
- `LEARNING_MEMORY.jsonl` für bestätigte Entwicklungslektionen,
- eigener Learning-Guard in CI,
- vollständiges Release-ZIP als CI-Artefakt.

## Versionierung

`VERSION_REGISTRY.json` enthält die getrackte Projektgeschichte; `runtime/versions.json` führt den lokalen Laufzustand. `tested`, `release-candidate` und `released` benötigen Evidenz. `VERSION` und Registry werden automatisch gegeneinander geprüft.

## Musterdateien und Testdaten

Geprüfte Referenzen liegen unter `resources/templates/`:

- Config,
- VersionRegistry,
- EventRegistry,
- TODOs.

`testdata/valid/` muss von den aktuellen Validatoren akzeptiert werden. `testdata/invalid/` bildet bekannte Fehlerklassen reproduzierbar ab.

**Wichtig:** Musterdateien sind Vergleichs- und Testgrundlagen. Sie überschreiben niemals automatisch lokale Nutzerdaten.

## Versionierte Texte und intelligente Fehlerhilfe

Wiederkehrende Systemtexte liegen unter `resources/texts/de/v1.json`. Fehlerregeln liegen getrennt unter `resources/error_rules/v1.json`.

Eine Fehlerantwort kann dadurch zusätzlich enthalten:

- Regel-ID,
- Kategorie,
- Ampel-/Schweregrad,
- einfache Erklärung,
- sichere nächste Handlung,
- optional passende Mustervorlage,
- Information, ob ein erneuter Versuch als sicher gilt.

`GET /api/help/meta` liefert die verwendeten Regel- und Textversionen.

## Entwicklungs-Lerngedächtnis

`LEARNING_MEMORY.jsonl` speichert keine Nutzerdaten, sondern bestätigte Entwicklungslektionen. Beispiele: optionale Felder explizit testen, Nutzerfehler von Persistenzfehlern trennen, Prüfungen seiteneffektfrei halten und Qualitätsstatus nie ohne Evidenz erhöhen.

Der CI-Schritt `python scripts/learning_guard.py` validiert diese Regeln bei jeder Änderung.

## TODO-Core

TODOs werden persistent gespeichert, Titel gemerkt und wieder angeboten. Abhaken verschiebt einen Eintrag mit `completed_at` ins Archiv statt ihn zu löschen. Ein Kalenderbezug ist optional vorbereitet. Die nächsten drei TODOs können serverseitig ermittelt werden.

## Ereignisse

Die EventRegistry speichert maximal 500 wichtige Ereignisse mit kurzem verständlichem `message`-Text. Technische Details bleiben getrennt. Die spätere Dashboard-Spalte verwendet standardmäßig die letzten fünf Ereignisse.

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

CI lädt bei vollständig grünem Lauf zusätzlich das komplette Release-ZIP als Artefakt hoch.

## Noch offen

- Kalender-Core und Erinnerungsmodell,
- Monats-/Wochen-/Jahresansicht,
- Dashboard V2 mit nächsten drei TODOs und letzten fünf Ereignissen,
- Debugmodul,
- reale Kubuntu-/Firefox-/Chrome-/Zoom-Gates,
- später SAFE-FILE-CORE.

## Nächster Slice

**`0.3.0-calendar-core` — Kalenderdaten, Erinnerungen, Titelgedächtnis und optionale TODO-Verknüpfung.**

Danach folgt Dashboard V2 auf Basis von TODO-, Kalender-, Event- und Versionsdaten.

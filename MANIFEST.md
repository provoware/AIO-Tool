# MANIFEST — AIO-Tool

## Projekt

- **Name:** AIO-Tool
- **Aktuelle Entwicklung:** `0.4.3-integrity-hardening` — 🟠 `development / draft`
- **Letzter bewiesener Stand:** `0.4.2-ui-acceptance` — 🟢 `tested / draft`
- **Repository:** `provoware/AIO-Tool`
- **Backend:** Python-Standardbibliothek, Loopback-only
- **Internetpflicht:** nein
- **Telemetrie:** nein

## Architektur

### Runtime-Core

- `app/config.py` — validierte Konfiguration.
- `app/persistence.py` — atomare JSON-Persistenz + Backup-Fallback.
- `app/version_registry.py` — kanonischer Versions-/Status-/Evidenzvertrag.
- `app/event_registry.py` — menschenlesbare Ereignisse.
- `app/todo_store.py` — TODOs, Titelgedächtnis, Archiv.
- `app/calendar_store.py` — Kalender, Perioden, Reminder, `zoneinfo`/DST.
- `app/text_catalog.py` — versionierte Core-Texte.
- `app/error_advisor.py` — regelbasierte Fehlerhilfe.
- `app/instance_identity.py` — stabile lokale Installationskennung.
- `app/server.py` — lokale Core-API.

### Start / Diagnose

- `start_tool.sh` — 9-Checkpoint-Startroutine mit Ampel, Fehler-IDs und lokaler Logrotation.
- `start_tool.desktop` — sichtbarer Desktopstart; Fehlerkonsole bleibt bei Abbruch offen.
- `scripts/launcher_probe.py` — prüft passende vorhandene Instanz und sucht bei Fremdbelegung sicheren Loopback-Ausweichport.
- `scripts/runtime_preflight.py` — einzige Vorprüfung, die ein Runtime-ZIP zum normalen Start benötigt.

### Dashboard

- `web/index.html` — semantische Dashboardstruktur.
- `web/app.js` — dünne API-/Darstellungsschicht.
- `web/styles.css` — Themes und Basislayout.
- `web/acceptance.css` — harte Raster-/Reflow-/Mindestzielgrößen-Verträge.
- `web/dashboard-texts.de.v1.json` — versionierte deutsche UI-Texte.
- `ui/layout-contract.v1.json` — maschinenlesbarer UI-Acceptance-Vertrag, nur Repository/Testschicht.

## Persistenzschemata

- VersionRegistry: 1
- EventRegistry: 1
- TODO: 1
- Calendar: 1
- Core-Textkatalog: 1
- Fehlerregeln: 1
- Learning Memory: 1 je JSONL-Zeile
- Dashboard-Textkatalog: 1

## Transportvertrag

### Quelle der Wahrheit

`manifests/RUNTIME_MANIFEST.json` ist die **positive Allowlist** für das Nutzer-/Runtime-ZIP.

Aktuelle Manifestversion: **1.1.0**.

### Runtime-ZIP enthält

- `VERSION` + `VERSION_REGISTRY.json`,
- Startdateien,
- benötigten `app/`-Runtime-Code,
- `scripts/runtime_preflight.py` und `scripts/launcher_probe.py`,
- produktive Weboberfläche,
- notwendige Text-/Fehlerdaten,
- geprüfte Referenzvorlagen,
- `manifests/RUNTIME_MANIFEST.json`,
- generiertes `MANIFEST_RELEASE.json`.

### Nicht im Runtime-ZIP

- README / AGENTS / TODO / CHANGELOG / LAIEN-ANLEITUNG / TOOLBESCHREIBUNG,
- REGRESSIONSINFOS / LEARNING_MEMORY,
- Tests und Testdaten,
- `.github/`, CI-Konfiguration,
- `requirements-ui.txt`, Playwright,
- Browserreports/Screenshots,
- `.venv/`, Caches, lokale Logs,
- produktive Config/TODO/Kalender/Event-/Recovery-Daten.

## Generierte lokale Daten

Nicht versioniert und nicht transportiert:

- `runtime/**`,
- `web/.aio-instance-id` — lokale Installationskennung, wird beim Start passend zur Installation/Version erzeugt.

## Statusvertrag

Erlaubte Paare:

| Versionsstatus | Release-Status | ZIP-Suffix |
|---|---|---|
| `development` | `draft` | `DEV` |
| `tested` | `draft` | `TESTED` |
| `release-candidate` | `candidate` | `RC` |
| `released` | `released` | `RELEASED` |
| `blocked` | `blocked` | `BLOCKED` |
| `deprecated` | `deprecated` | `ARCHIVED` |

Widersprüchliche/unbekannte Paare werden vom Validator abgelehnt.

## Qualitätsebenen

- **L0:** Syntax/Schema.
- **L1:** Unit-/Contracttests.
- **L2:** Runtime-ZIP bauen, verifizieren, frisch entpacken, Runtime-Preflight darin ausführen.
- **L3:** Chromium + Firefox über Raster-/Reflow-/Interaktionsmatrix.
- **L4:** echtes Kubuntu/DPI/Zoom/Tastatur-Zielsystem.

Eine niedrigere Ebene darf keine höhere als bestanden behaupten.

## Aktuelle Evidenz

`0.4.2-ui-acceptance`:

- GitHub Actions Run `33032999752` — Core/Release + Chromium/Firefox **SUCCESS**.
- TESTED-ZIP SHA256: `57c461b56abd024775de8a38d8edf216066c8fd11631d4d266e4572a6d58a6cc`.

`0.4.3-integrity-hardening`:

- Status: **DEVELOPMENT**.
- Finale CI-/Browser-Evidenz wird erst nach Abschluss des Audit-/Dokumentationsslices eingetragen.

## Noch offen

- native Kubuntu-Klick-&-Start-Abnahme,
- KDE-/DPI-Skalierung,
- 100–200 % Browserzoom auf Zielsystem,
- realer Tastatur-/Screenreader-Durchlauf,
- SAFE-FILE-CORE,
- persistente Job-/Recovery-Queue.

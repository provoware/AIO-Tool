# MANIFEST — AIO-Tool

## Projekt

- **Name:** AIO-Tool
- **Aktuelle Version:** `0.4.3-integrity-hardening` — 🟢 `tested / draft`
- **Evidenzlauf:** GitHub Actions Run `33034359454` — Core/Release + Chromium/Firefox SUCCESS
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

- `start_tool.sh` — 9-Checkpoint-Startroutine mit Ampel, Fehler-IDs und Logrotation.
- `start_tool.desktop` — sichtbarer Desktopstart; Fehlerkonsole bleibt bei Abbruch offen.
- `scripts/launcher_probe.py` — verifiziert vorhandene Instanz und findet bei Fremdbelegung sicheren Loopback-Ausweichport.
- `scripts/runtime_preflight.py` — einzige Vorprüfung, die ein Runtime-ZIP zum normalen Start benötigt.

### Dashboard / UI

- `web/index.html` — semantische Dashboardstruktur.
- `web/app.js` — dünne API-/Darstellungsschicht.
- `web/styles.css` — Themes und Basislayout.
- `web/acceptance.css` — harte Raster-/Reflow-/Mindestzielgrößen-Verträge.
- `web/dashboard-texts.de.v1.json` — versionierte deutsche UI-Texte.
- `ui/layout-contract.v1.json` — maschinenlesbarer UI-Acceptance-Vertrag, nur Repository/Testschicht.

## Transportvertrag

`manifests/RUNTIME_MANIFEST.json` ist die **positive Allowlist** für das Nutzer-/Runtime-ZIP.

Runtime-ZIP enthält ausschließlich:

- `VERSION` + `VERSION_REGISTRY.json`,
- Startdateien,
- benötigten `app/`-Runtime-Code,
- `scripts/runtime_preflight.py` + `scripts/launcher_probe.py`,
- produktive Weboberfläche,
- notwendige Text-/Fehlerdaten,
- geprüfte Referenzvorlagen,
- `manifests/RUNTIME_MANIFEST.json`,
- generiertes `MANIFEST_RELEASE.json`.

Nicht im Runtime-ZIP:

- README / AGENTS / TODO / CHANGELOG / LAIEN-ANLEITUNG / TOOLBESCHREIBUNG,
- REGRESSIONSINFOS / LEARNING_MEMORY,
- Tests und Testdaten,
- `.github/`, CI, Playwright,
- Browserreports/Screenshots,
- `.venv/`, Caches, lokale Logs,
- produktive Nutzer-/Kalender-/TODO-/Eventdaten.

## Lokale generierte Daten

Nicht versioniert und nicht transportiert:

- `runtime/**`
- `web/.aio-instance-id` — lokale Installationskennung

## Statusvertrag

| Versionsstatus | Release-Status | ZIP-Suffix |
|---|---|---|
| `development` | `draft` | `DEV` |
| `tested` | `draft` | `TESTED` |
| `release-candidate` | `candidate` | `RC` |
| `released` | `released` | `RELEASED` |
| `blocked` | `blocked` | `BLOCKED` |
| `deprecated` | `deprecated` | `ARCHIVED` |

Widersprüchliche oder unbekannte Paare werden fail-closed abgelehnt.

## Qualitätsebenen

- **L0:** Syntax / Schema
- **L1:** Unit-/Contracttests
- **L2:** Runtime-ZIP bauen, verifizieren, frisch entpacken und Preflight darin ausführen
- **L3:** Chromium + Firefox über Raster-/Reflow-/Interaktionsmatrix
- **L4:** echtes Kubuntu/DPI/Zoom/Tastatur-Zielsystem

Eine niedrigere Ebene darf keine höhere als bestanden behaupten.

## Aktuelle Evidenz 0.4.3

GitHub Actions Run `33034359454`:

- Core-/Release-Job: **SUCCESS**
- Documentation Guard: **SUCCESS**
- Runtime-ZIP-End-to-End-Vertrag: **SUCCESS**
- Chromium + Firefox UI-Acceptance: **SUCCESS**

Registry-Status: **`tested`**  
Release-Status: **`draft`**  
Erwarteter Runtime-Dateiname: **`AIO-Tool-0.4.3-integrity-hardening-TESTED.zip`**

Der Promotion-Commit wird anschließend erneut durch dieselbe Pipeline geprüft; erst dann ist die Promotion selbst vollständig bewiesen.

## Persistenzschemata

- VersionRegistry: 1
- EventRegistry: 1
- TODO: 1
- Calendar: 1
- Core-Textkatalog: 1
- Fehlerregeln: 1
- Learning Memory: 1 je JSONL-Zeile
- Dashboard-Textkatalog: 1

## Noch offene L4-Gates

- native Kubuntu-Klick-&-Start-Abnahme
- KDE-/DPI-Skalierung
- 100/125/150/175/200 % Browserzoom auf Zielsystem
- realer Tastatur-/Screenreader-Durchlauf
- verschiedene reale Displaygrößen

## Danach

Erst nach L4-Abnahme: SAFE-FILE-CORE mit Copy, Vorprüfung, Vorschau, persistenter Jobausführung, Nachprüfung und Undo-/Recovery-Datensatz.

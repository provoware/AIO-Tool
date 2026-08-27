# AIO-Tool

> **Lokales, modulares und laienfreundliches All-in-One-Tool.** Es läuft mit einem Python-Backend ausschließlich auf deinem eigenen Rechner und öffnet seine Oberfläche im Browser.

## 🧭 Projektstatus auf einen Blick

| Bereich | Zustand | Bedeutung |
|---|---|---|
| Letzter bewiesener Stand | 🟢 `0.4.2-ui-acceptance-TESTED` | Core + Runtime-ZIP + Chromium + Firefox erfolgreich geprüft |
| Aktuelle Entwicklung | 🟠 `0.4.3-integrity-hardening-DEV` | Robustheits-/Wartbarkeitshärtung; neue Evidenz läuft separat |
| Internet für Kernfunktionen | 🟢 nicht nötig | offline-first |
| Backend | 🟢 nur `127.0.0.1` | nicht im LAN/Internet veröffentlicht |
| Telemetrie | 🟢 keine | keine automatische Nutzungsübertragung |
| Externe Runtime-Pakete | 🟢 keine | Python-Standardbibliothek |
| Native Kubuntu-/DPI-Abnahme | 🟡 offen | automatisierte Browser-CI ersetzt kein echtes Zielsystem |
| SAFE-FILE-CORE | ⚪ noch nicht begonnen | echte Dateioperationen bleiben bis zum Sicherheits-Slice gesperrt |

### Fortschritt

```text
Foundation / Persistenz       ████████████████████ 100 %  🟢
Kalender / TODO / Ereignisse  ████████████████████ 100 %  🟢
Dashboard V2                  ████████████████████ 100 %  🟢
Browser-Acceptance            ████████████████████ 100 %  🟢
Runtime-Transport             ████████████████████ 100 %  🟢
Integritätshärtung 0.4.3      ███████████████░░░░░  75 %  🟠 CI/Promotion noch offen
Native Kubuntu-Abnahme        ██████░░░░░░░░░░░░░░  30 %  🟡 automatisiert vorbereitet
SAFE-FILE-CORE                ░░░░░░░░░░░░░░░░░░░░   0 %  ⚪ später
```

> **Wichtig:** Die Prozentwerte sind Roadmap-/Arbeitsfortschritt. Ein grüner Status entsteht nur durch den jeweiligen Test-/Evidenzvertrag.

---

## ▶️ Start für Laien

1. ZIP vollständig in einen eigenen Ordner entpacken.
2. `start_tool.desktop` doppelklicken oder `start_tool.sh` starten.
3. Die Startkonsole zeigt **9 Checkpoints** mit Ampelstatus.
4. Bei Erfolg öffnet sich die Oberfläche automatisch.
5. Bei einem Fehler bleibt die Konsole offen und zeigt Fehler-ID, Ursache, Logs und den nächsten sinnvollen Prüfschritt.

### Ampel beim Start

- 🟢 **PASS** — geprüft und bestanden
- 🟡 **WARN** — Start möglich, Hinweis beachten
- 🔴 **FAIL** — sicherer Abbruch; Ursache wird erklärt
- 🔵 **INFO** — normaler Zwischenzustand

Die Startkonsole trennt verständliche Nutzerinformation von technischen Logs. Lokale Logs liegen unter `runtime/` und gehören **nicht** zum Releasepaket.

---

## 🧩 Was kann das Tool aktuell?

### Dashboard

- dauerhaft sichtbarer Monatskalender,
- kommende Termine,
- nächste drei TODOs,
- TODO direkt abhaken → wird mit Zeitstempel ins Erledigt-Archiv verschoben,
- letzte fünf Ereignisse in verständlicher Sprache,
- Versions-/Registry-/Systemstatus,
- fällige Erinnerungen mit explizitem **„Gesehen“**,
- Schnellmodule **Häufig / Alle**,
- optionaler Entwickler-/Diagnosebereich,
- vier Themes,
- Schriftgrößen-Presets,
- automatische Darstellungsdichte.

### Kalender

- Monats-, Wochen- und Jahresperioden im Backend,
- Termin-Titelgedächtnis,
- Erinnerungs-Presets,
- Sommer-/Winterzeit über `zoneinfo`,
- optionale TODO-Verknüpfung.

### TODOs

- persistente Aufgaben,
- Titel werden für spätere Auswahl gemerkt,
- nächste drei Aufgaben automatisch priorisiert,
- Erledigt-Archiv mit Zeitstempel.

### Robustheitskern

- atomare JSON-Speicherung,
- Backup-Fallback,
- VersionRegistry mit Evidenzpflicht,
- EventRegistry,
- versionierte Text-/Fehlerkataloge,
- positive und negative Testdaten,
- Entwicklungs-Lerngedächtnis,
- reproduzierbarer Release-Builder.

---

## 🛡️ Warum die Startroutine jetzt sicherer ist

Eine Antwort `200 OK` reicht **nicht** mehr, um eine bereits laufende Instanz zu übernehmen.

Der Launcher prüft:

`Version → Loopback → Ready-Zustand → konkrete Installationskennung`

Ist der Standardport durch eine andere oder alte lokale Instanz belegt, wird sie **nicht** übernommen. Stattdessen wählt die Startroutine transparent einen freien lokalen Ausweichport.

Außerdem verwendet der normale Start nur:

`scripts/runtime_preflight.py`

und **nicht** die Repository-Vollprüfung `scripts/validate.py`. Dadurch bleibt das Runtime-ZIP wirklich unabhängig von README, Tests und Entwicklungsdateien.

---

## 📦 Runtime-ZIP und Repository sind bewusst getrennt

### Im Runtime-ZIP

Nur Dateien aus `manifests/RUNTIME_MANIFEST.json` plus das automatisch erzeugte `MANIFEST_RELEASE.json`:

- Startdateien,
- benötigter Python-Code,
- Browseroberfläche,
- notwendige Text-/Fehlerdaten,
- geprüfte Referenzvorlagen,
- Runtime-Preflight,
- Instanzprüfung.

### Nur im Repository / lokal

- README, AGENTS, TODO, CHANGELOG,
- Regressionen und Learning Memory,
- Tests/Testdaten,
- CI-Konfiguration,
- Browser-Screenshots und Reports,
- lokale Logs und Nutzerdaten.

Der Release-Builder arbeitet mit einer **positiven Allowlist**. Neue Repository-Dateien gelangen deshalb nicht automatisch ins Nutzerpaket.

---

## 🏷️ Was bedeuten die Dateinamen?

| Suffix | Bedeutung |
|---|---|
| `-DEV.zip` | 🟠 Entwicklung, noch nicht vollständig bewiesen |
| `-TESTED.zip` | 🟢 automatisiert geprüft |
| `-RC.zip` | 🟡 Release Candidate |
| `-RELEASED.zip` | 🟢 offiziell freigegeben |
| `-BLOCKED.zip` | 🔴 bekannter Blocker |
| `-ARCHIVED.zip` | ⚪ historischer Stand |

Der Name wird aus der validierten Versionsregistry abgeleitet. Unbekannte oder widersprüchliche Statuskombinationen werden abgelehnt.

---

## 🧪 Wie wird geprüft?

### L0 — Syntax / Schema

- Python-Kompilierung
- Bash-Syntax
- JavaScript-Syntax
- JSON-/Schema-Validatoren

### L1 — Unit / Verträge

Persistenz, Kalender, TODO, Versionierung, Fehlerhilfe, Launcher, UI-Verträge.

### L2 — echtes Runtime-ZIP

CI baut das ZIP, prüft Manifest + SHA256, entpackt es in einen frischen Ordner und startet dort den **Runtime-Preflight**.

### L3 — echte Browser

Chromium und Firefox prüfen über mehrere Viewports:

- 12-Spalten-Raster,
- Reflow bis 320 CSS-px,
- horizontale Überbreite,
- Überlappungen,
- Mindest-Bediengrößen,
- Kalender-7-Spalten,
- TODO-/Reminder-/Einstellungsinteraktionen.

Screenshots und JSON-Report werden als Evidenz erzeugt.

### L4 — echtes Zielsystem

Noch offen: Kubuntu, reale KDE-/DPI-Skalierung, 100–200 % Browserzoom und vollständiger Tastaturdurchlauf. Dieser Status wird nicht aus CI abgeleitet.

---

## 🔧 Entwicklerprüfung

Im Repository:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate.py
python3 scripts/learning_guard.py
bash -n start_tool.sh
node --check web/app.js
python3 scripts/release.py --check
```

Nur Runtime-Vertrag:

```bash
python3 scripts/runtime_preflight.py --quick
```

Browser-Acceptance:

```bash
python3 scripts/ui_acceptance_ci.py --browser chromium --browser firefox --strict
```

---

## 🧠 Entwicklungsdisziplin

Die wichtigsten verbindlichen Regeln stehen in `AGENTS.md`:

- bewiesene Version nicht nachträglich verändern,
- Status nur mit Evidenz erhöhen,
- UI-Renderaussagen nur mit echten Browserläufen,
- Runtime strikt vom Repository trennen,
- Fehler als Regression sichern,
- zuerst kleinste verantwortliche Codezone patchen,
- keine neue Funktion bei rotem P0/P1-Gate.

---

## ⚠️ Was ist bewusst noch nicht fertig?

- native Kubuntu-Klick-&-Start-Abnahme,
- echte KDE-/HiDPI-Skalierung,
- 100/125/150/175/200 % Browserzoom auf dem Zielsystem,
- kompletter Tastatur-/Screenreader-Praxistest,
- SAFE-FILE-CORE,
- persistente Job-/Recovery-Queue.

## ➜ Nächste logische Reihenfolge

1. **`0.4.3-integrity-hardening` vollständig grün prüfen und erst danach zu TESTED hochstufen.**
2. **Native Kubuntu-/Zoom-/Tastaturabnahme aus dem erzeugten TESTED-ZIP.**
3. Danach **SAFE-FILE-CORE**, zunächst ausschließlich sichere Copy-Operationen.

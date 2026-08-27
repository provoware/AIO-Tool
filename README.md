# AIO-Tool

> **Lokales, modulares und laienfreundliches All-in-One-Tool.** Python-Backend nur auf dem eigenen Rechner, Browseroberfläche ohne Internetzwang.

## 🧭 Status auf einen Blick

| Bereich | Zustand | Bedeutung |
|---|---|---|
| Aktuelle Version | 🟢 `0.4.3-integrity-hardening-TESTED` | vollständiger Entwicklungshead hat Core/Release + Chromium + Firefox bestanden |
| Evidenzlauf | 🟢 Run `33034359454` | beide CI-Jobs erfolgreich |
| Release-Status | 🟢 `tested / draft` | automatisiert geprüft, noch keine offizielle Freigabe |
| Internet | 🟢 nicht nötig | offline-first |
| Backend | 🟢 `127.0.0.1` | nicht im LAN/Internet veröffentlicht |
| Telemetrie | 🟢 keine | keine automatische Nutzungsübertragung |
| Externe Runtime-Pakete | 🟢 keine | Python-Standardbibliothek |
| Native Kubuntu-/DPI-Abnahme | 🟡 offen | automatisierte Browser-CI ersetzt kein echtes Zielsystem |
| SAFE-FILE-CORE | ⚪ noch nicht begonnen | echte Dateioperationen bleiben gesperrt |

### Fortschritt

```text
Foundation / Persistenz       ████████████████████ 100 % 🟢
Kalender / TODO / Ereignisse  ████████████████████ 100 % 🟢
Dashboard V2                  ████████████████████ 100 % 🟢
Browser-Acceptance            ████████████████████ 100 % 🟢
Runtime-Transport             ████████████████████ 100 % 🟢
Integritätshärtung 0.4.3      ████████████████████ 100 % 🟢
Promotion-Revalidierung       ████████████████░░░░  80 % 🟡 läuft auf TESTED-Status
Native Kubuntu-Abnahme        ██████░░░░░░░░░░░░░░  30 % 🟡 vorbereitet
SAFE-FILE-CORE                ░░░░░░░░░░░░░░░░░░░░   0 % ⚪
```

> Prozentwerte zeigen Arbeitsfortschritt. **TESTED** entsteht nur durch den zugehörigen Evidenzvertrag.

---

## ▶️ Start für Laien

1. TESTED-ZIP vollständig in einen eigenen Ordner entpacken.
2. `start_tool.desktop` doppelklicken oder `start_tool.sh` starten.
3. Die Konsole zeigt **9 Checkpoints** mit Ampelstatus.
4. Bei Erfolg öffnet sich die Browseroberfläche automatisch.
5. Bei Fehler bleibt die Konsole offen und zeigt Fehler-ID, Ursache, Logs und nächsten Prüfschritt.

### Ampel

- 🟢 **PASS** — geprüft und bestanden
- 🟡 **WARN** — Start möglich, Hinweis beachten
- 🔴 **FAIL** — sicherer Abbruch mit Diagnose
- 🔵 **INFO** — normaler Zwischenzustand

---

## 🛡️ Was wurde in 0.4.3 gehärtet?

### Sichere Instanzprüfung

Ein bloßes `HTTP 200` reicht nicht mehr zur Wiederverwendung einer laufenden Instanz.

Geprüft werden:

`Version → Loopback → Ready → konkrete Installationskennung`

Eine alte/fremde lokale Instanz wird nicht übernommen. Bei belegtem Standardport sucht das Tool transparent einen freien lokalen Ausweichport.

### Runtime bleibt unabhängig vom Repository

Der normale Start verwendet nur:

`scripts/runtime_preflight.py`

Repository-Dokumente, Tests und `scripts/validate.py` sind für ein Nutzer-ZIP nicht erforderlich.

### Release-End-to-End-Vertrag

CI prüft nicht nur das ZIP-Manifest, sondern:

`bauen → Hashes prüfen → entpacken → Runtime-Preflight aus dem entpackten ZIP`

### Dokumentationsschutz

`scripts/documentation_guard.py` stoppt CI, wenn VERSION, Registry, README, TODO, CHANGELOG, MANIFEST, REGRESSIONSINFOS, LAIEN-ANLEITUNG oder TOOLBESCHREIBUNG auseinanderlaufen.

### Logwartung

Launcherlogs werden lokal begrenzt/rotiert und gehören nie ins Runtime-ZIP.

---

## 🧩 Aktuell nutzbare Bereiche

- Monatskalender sowie Backend-Perioden für Monat/Woche/Jahr
- Termine + Reminder
- nächste drei TODOs + Erledigt-Archiv
- Titelgedächtnis
- letzte fünf verständliche Ereignisse
- Versions-/Registry-/Systemstatus
- vier Themes + Schriftgrößen-Presets
- responsive 12-Spalten-Struktur mit Reflow bis 320 CSS-px
- optionaler Diagnosebereich

Echte Dateioperationen sind weiterhin bewusst deaktiviert.

---

## 📦 Runtime-ZIP vs. Repository

### Im Runtime-ZIP

Nur die positive Allowlist aus `manifests/RUNTIME_MANIFEST.json` plus `MANIFEST_RELEASE.json`:

- Startdateien
- notwendiger Python-Code
- Weboberfläche
- Runtime-Preflight + Instanzprobe
- notwendige Text-/Fehlerdaten
- geprüfte Referenzvorlagen

### Nur im Repository/lokal

- README / AGENTS / TODO / CHANGELOG
- Regressionen / Learning Memory
- Tests / Testdaten
- CI-Konfiguration
- Browser-Screenshots und Reports
- lokale Logs und Nutzerdaten

---

## 🏷️ Dateinamenstatus

| Suffix | Bedeutung |
|---|---|
| `-DEV.zip` | 🟠 Entwicklung |
| `-TESTED.zip` | 🟢 automatisiert geprüft |
| `-RC.zip` | 🟡 Release Candidate |
| `-RELEASED.zip` | 🟢 offiziell freigegeben |
| `-BLOCKED.zip` | 🔴 Blocker |
| `-ARCHIVED.zip` | ⚪ historisch |

Der Suffix wird ausschließlich aus der validierten Versionsregistry abgeleitet.

---

## 🧪 Prüfstufen

- **L0:** Syntax / Schema
- **L1:** Unit-, Integrations- und Vertragsprüfungen
- **L2:** echtes Runtime-ZIP inklusive Preflight aus frischer Entpackung
- **L3:** Chromium + Firefox, Raster, Reflow und Interaktionen
- **L4:** echtes Kubuntu-Zielsystem, DPI/Zoom/Tastatur — noch offen

Run `33034359454` hat den finalen Entwicklungshead von `0.4.3-integrity-hardening` auf L0–L3 vollständig bestanden. Danach wurde der Status regelkonform auf `tested / draft` promoviert. Der Promotion-Commit wird erneut durch dieselbe Pipeline geprüft.

---

## 🔧 Entwicklerprüfung

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate.py
python3 scripts/learning_guard.py
python3 scripts/documentation_guard.py
bash -n start_tool.sh
node --check web/app.js
python3 scripts/release.py --check
```

Browser-Gate:

```bash
python3 scripts/ui_acceptance_ci.py --browser chromium --browser firefox --strict
```

---

## ⚠️ Noch offen

- native Kubuntu-Klick-&-Start-Abnahme
- KDE-/HiDPI-Skalierung
- 100 / 125 / 150 / 175 / 200 % Browserzoom auf dem Zielsystem
- kompletter Tastatur-/Screenreader-Praxistest
- SAFE-FILE-CORE
- persistente Job-/Recovery-Queue

## ➜ Nächste logische Reihenfolge

1. **Promotion-Commit von `0.4.3-integrity-hardening-TESTED` nochmals vollständig grün prüfen.**
2. **Danach TESTED-ZIP auf echtem Kubuntu mit Zoom/DPI/Tastatur abnehmen.**
3. Erst danach **SAFE-FILE-CORE**, zunächst ausschließlich Copy mit Vorschau, Nachprüfung und Recovery.

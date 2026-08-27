# AIO-Tool

> **Aktuelle Entwicklung:** 🟠 `0.5.1-audit-modern-ui-DEV`  
> **Letzter vollständig bewiesener Stand:** 🟢 `0.5.0-native-acceptance-safe-file-sim-TESTED`  
> **Betrieb:** lokal · offline-first · keine Telemetrie · Loopback-only

AIO-Tool bündelt Kalender, TODOs, Erinnerungen, Ereignisse, Diagnose, Zielsystemabnahme und die weiterhin **nur simulierte** SAFE-FILE-Vorprüfung in einer laienfreundlichen lokalen Oberfläche.

## 🚦 Was bedeutet der aktuelle Zustand?

| Bereich | Status | Bedeutung |
|---|---|---|
| 0.5.0 Baseline | 🟢 TESTED | L0–L3 automatisiert bewiesen |
| 0.5.1 Audit | 🟠 DEV | Verbesserungen implementiert, finaler CI-/Browsernachweis offen |
| Native Kubuntu L4 | 🟡 OFFEN | muss real auf dem Zielsystem bestätigt werden |
| SAFE-FILE echte Copy | 🔒 GESPERRT | Simulation kann keine Dateien verändern |

**Wichtig:** TESTED bedeutet nicht automatisch „auf jeder realen Kubuntu-/DPI-/Zoom-Kombination manuell abgenommen“. Diese L4-Evidenz bleibt getrennt.

## 📊 Entwicklungsfortschritt

```text
Foundation / Persistenz         ████████████████████ 100 % 🟢
Kalender / TODO / Ereignisse    ████████████████████ 100 % 🟢
Dashboard / Browser-Gates       ████████████████████ 100 % 🟢 Baseline
Native Acceptance Runner        ████████████████████ 100 % 🟢
Release-Evidenzsystem           ████████████████████ 100 % 🟢
SAFE-FILE Simulation            ████████████████████ 100 % 🟢
0.5.1 Robustheitsaudit          ███████████████████░  95 % 🟠 finaler Gate offen
Native Kubuntu L4               ██████░░░░░░░░░░░░░░  30 % 🟡 real offen
SAFE-FILE Copy-Ausführung       ░░░░░░░░░░░░░░░░░░░░   0 % 🔒
```

## ✨ Neu im 0.5.1-Audit

### Robustheit

- `AtomicJsonStore` serialisiert parallele Thread-Zugriffe; `update()` ist ein zusammenhängender Read→Mutate→Write-Vertrag.
- Backup-Dateien werden ebenfalls atomar ersetzt.
- `ConfigStore` nutzt jetzt denselben Persistence-Core statt eigener doppelter Schreiblogik.
- Hauptbackend und Hilfsserver verwenden denselben strengen Loopback-Host-/Port-Vertrag.
- Serverlog-Schreibvorgänge sind im Threading-Backend serialisiert.
- Versions-Fallbacktexte sind nicht mehr fälschlich an den alten Kalender-Slice gekoppelt.

### Nutzerfreundlichkeit

- Fehlerhafte Kalender-/Terminabfragen zeigen keine veralteten Daten unter einer neuen Überschrift.
- Ein später erfolgreicher TODO-Versuch entfernt einen zuvor gespeicherten Aktionsfehler.
- Der sichtbare Boot-Guard unterscheidet Start, READY und Startfehler.
- Theme-, Schrift- und Modulwahl verwenden zusätzlich `aria-pressed`.
- Einstellungen erhalten zuverlässigen Tastaturfokus und geben ihn beim Schließen zurück.
- Kalenderzellen erzeugen nicht mehr Dutzende unnötige Tabstopps.

### Moderneres Erscheinungsbild

Fünf klar getrennte Themes verwenden denselben semantischen Komponentenvertrag:

- **Aurora Glass** — modernes Cyan/Violett mit ruhigen Glasflächen.
- **Steel Night** — sachlich-technisch, dunkel und klar.
- **Trash Neon** — kräftige Subkultur-/Neonwirkung.
- **Clean Light** — helle, ruhige Arbeitsoberfläche.
- **High Contrast** — maximaler Kontrast, ohne dekorative Schatten.

Farbe ist nie die einzige Statusinformation; Status bleibt zusätzlich durch Text/Icon erkennbar. `prefers-reduced-motion` bleibt verbindlich.

## ▶️ Start

### Normales Dashboard

```bash
./start_tool.sh
```

oder per `start_tool.desktop`.

### Reale Zielsystemabnahme

```bash
./start_native_acceptance.sh
```

Der Assistent führt durch 18 echte L4-Schritte. Kein Schritt wird automatisch auf PASS gesetzt.

### SAFE-FILE Simulation

```bash
./start_safe_file_simulation.sh
```

Die Oberfläche darf nur lesen/prüfen/vorschlagen. Der Vertrag bleibt:

```text
simulation_only=true
execution_enabled=false
mutation_performed=false
```

## 🛡️ Sicherheitsprinzipien

1. Nur Loopback, keine Netzwerkfreigabe.
2. Host und Origin müssen zum exakten lokalen Port passen.
3. Keine Telemetrie.
4. Persistente JSON-Zustände werden validiert, atomar geschrieben und mit Backup-Fallback gelesen.
5. Runtime-ZIP enthält nur die positive Allowlist aus `manifests/RUNTIME_MANIFEST.json`.
6. Dokumentation, Tests, Logs und Evidenz bleiben im Repository bzw. lokal.
7. Eine TESTED-Version wird nach ihrer Evidenz nicht weiter verändert; Produktpatches beginnen als neue DEV-Version.

## 🧪 Qualitätspyramide

- **L0:** Syntax / Schema
- **L1:** Unit-, Contract- und Regressionstests
- **L2:** gebautes Runtime-ZIP frisch entpacken und selbst prüfen
- **L3:** echte Chromium-/Firefox-Render-, Reflow- und Interaktionsgates
- **L4:** reale Kubuntu-/Browser-/Zoom-/Tastaturabnahme

Ein niedrigeres Level darf niemals als Beweis für ein höheres ausgegeben werden.

## 🗂️ Wichtige Projektdateien

- `AGENTS.md` — verbindlicher Entwicklungsvertrag
- `VERSION` / `VERSION_REGISTRY.json` — Versions-/Statuswahrheit
- `manifests/RUNTIME_MANIFEST.json` — transportierte Runtime-Allowlist
- `evidence/RELEASE_EVIDENCE_INDEX.json` — bewiesene Release-Evidenz
- `REGRESSIONSINFOS.md` — bekannte Fehlerverträge
- `LEARNING_MEMORY.jsonl` — bestätigte Entwicklungslektionen
- `TODO.md` — aktueller nächster Entwicklungsweg

## ➜ Nächster Gate

`0.5.1-audit-modern-ui` darf erst von DEV auf TESTED wechseln, wenn Unit-/Contracttests, Foundation-/Documentation-/Evidence-Gates, Runtime-ZIP und **Chromium + Firefox inklusive der beiden Hilfsoberflächen** auf demselben Commit grün sind.

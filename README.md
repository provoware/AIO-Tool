# AIO-Tool

> **Aktueller Kandidat:** 🟢 `0.5.1-audit-modern-ui-TESTED` — Registry `tested / draft`; Promotion-CI noch offen  
> **Letzter auf `main` vollständig bewiesener Stand:** 🟢 `0.5.0-native-acceptance-safe-file-sim-TESTED`  
> **Betrieb:** lokal · offline-first · keine Telemetrie · Loopback-only

AIO-Tool bündelt Kalender, TODOs, Erinnerungen, Ereignisse, Diagnose, Zielsystemabnahme und die weiterhin **nur simulierte** SAFE-FILE-Vorprüfung in einer laienfreundlichen lokalen Oberfläche.

## 🚦 Was bedeutet der aktuelle Zustand?

| Bereich | Status | Bedeutung |
|---|---|---|
| 0.5.0 Main-Baseline | 🟢 BEWIESEN | L0–L3 auf `main` vollständig grün |
| 0.5.1 Audit | 🟢 TESTED-Kandidat | DEV-Gate `33045348341` vollständig grün; Promotion-Commit muss nochmals dieselben Gates bestehen |
| Native Kubuntu L4 | 🟡 OFFEN | muss real auf dem Zielsystem bestätigt werden |
| SAFE-FILE echte Copy | 🔒 GESPERRT | Simulation kann keine Dateien verändern |

**Wichtig:** TESTED bedeutet nicht automatisch „auf jeder realen Kubuntu-/DPI-/Zoom-Kombination manuell abgenommen“. Diese L4-Evidenz bleibt getrennt.

## 📊 Entwicklungsfortschritt

```text
Foundation / Persistenz         ████████████████████ 100 % 🟢
Kalender / TODO / Ereignisse    ████████████████████ 100 % 🟢
Dashboard / Browser-Gates       ████████████████████ 100 % 🟢
Native Acceptance Runner        ████████████████████ 100 % 🟢
Release-Evidenzsystem           ████████████████████ 100 % 🟢
SAFE-FILE Simulation            ████████████████████ 100 % 🟢
0.5.1 Code-/Robustheitsaudit    ████████████████████ 100 % 🟢 DEV-Gate
0.5.1 Promotion                 ████████████████░░░░  80 % 🟡 Promotion-CI offen
Native Kubuntu L4               ██████░░░░░░░░░░░░░░  30 % 🟡 real offen
SAFE-FILE Copy-Ausführung       ░░░░░░░░░░░░░░░░░░░░   0 % 🔒
```

## ✨ Verbesserungen in 0.5.1

### Codequalität und Robustheit

- `AtomicJsonStore` serialisiert parallele Thread-Zugriffe über den vollständigen Read→Mutate→Write-Zyklus.
- Backup-Dateien werden ebenfalls atomar ersetzt.
- `ConfigStore` nutzt denselben Persistence-Core statt eigener doppelter Schreiblogik.
- Hauptbackend und Hilfsserver verwenden denselben strengen Loopback-Host-/Port-Vertrag.
- Serverlog-Schreibvorgänge sind im Threading-Backend serialisiert.
- Browser-Acceptance besitzt **nur noch eine** kanonische Implementierung; der CI-Einstieg ist ein dünner Wrapper.
- UI-Testassets werden aus dem aktuellen `index.html` abgeleitet statt Contract-Versionen doppelt zu hardcodieren.
- Entwicklungs-Lerngedächtnis umfasst nun 21 aktive strukturelle Regeln.

### Nutzerfreundlichkeit und Feedback

- Backend-Anfragen haben einen klaren 8-Sekunden-Timeout mit Hinweis auf die Startkonsole.
- „Neu prüfen“ läuft single-flight, zeigt `Prüfe …`, sperrt parallele Wiederholungen und setzt `aria-busy`.
- Theme-/Schriftänderungen zeigen sofort eine Vorschau, werden serialisiert gespeichert und bei Fehler auf den letzten bestätigten Stand zurückgesetzt.
- **Leer** und **nicht verfügbar** sind getrennte Zustände: Ladefehler werden nicht mehr als „keine TODOs/Termine/Ereignisse“ ausgegeben.
- Fehlerhafte Kalender-/Terminabfragen zeigen keine veralteten Daten unter einer neuen Überschrift.
- Ein später erfolgreicher TODO-Versuch entfernt einen zuvor gespeicherten Aktionsfehler.
- Der sichtbare Boot-Guard unterscheidet Start, READY, READY mit Hinweisen und Startfehler.
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
4. Persistente JSON-Zustände werden validiert, atomar und thread-sicher geschrieben und mit Backup-Fallback gelesen.
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

Der aktuelle Promotion-Commit muss erneut **Core/Release + Chromium + Firefox + Native Runner + SAFE-FILE-Hilfsoberfläche** vollständig grün durchlaufen. Erst danach wird der echte TESTED-Artefakthash in die Evidenzdatei eingetragen und der Merge nach `main` vorbereitet.

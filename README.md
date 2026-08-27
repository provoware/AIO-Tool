# AIO-Tool

> **Aktueller Kandidat:** 🟢 `0.5.1-audit-modern-ui-TESTED` — Registry `tested / draft`, L0–L3 vollständig grün  
> **Letzter auf `main` vollständig bewiesener Stand:** 🟢 `0.5.0-native-acceptance-safe-file-sim-TESTED`  
> **Betrieb:** lokal · offline-first · keine Telemetrie · Loopback-only

AIO-Tool bündelt Kalender, TODOs, Erinnerungen, Ereignisse, Diagnose, Zielsystemabnahme und die weiterhin **nur simulierte** SAFE-FILE-Vorprüfung in einer laienfreundlichen lokalen Oberfläche.

## 🚦 Aktueller Zustand

| Bereich | Status | Bedeutung |
|---|---|---|
| 0.5.0 Main-Baseline | 🟢 BEWIESEN | L0–L3 auf `main` vollständig grün |
| 0.5.1 Audit | 🟢 TESTED | DEV-Run `33045348341` und Promotion-Run `33045669222` vollständig grün |
| Evidence-Sync / Main-Merge | 🟡 OFFEN | letzter Metadaten-Gate, PR, Squash-Merge und Main-CI fehlen noch |
| Native Kubuntu L4 | 🟡 OFFEN | muss real auf dem Zielsystem bestätigt werden |
| SAFE-FILE echte Copy | 🔒 GESPERRT | Simulation besitzt weiterhin keine Dateimutation |

**Wichtig:** TESTED bedeutet hier L0–L3. Es ersetzt keine reale Kubuntu-/DPI-/Browserzoom-/Tastaturabnahme L4.

## 📊 Entwicklungsfortschritt

```text
Foundation / Persistenz         ████████████████████ 100 % 🟢
Kalender / TODO / Ereignisse    ████████████████████ 100 % 🟢
Dashboard / Browser-Gates       ████████████████████ 100 % 🟢
Native Acceptance Runner        ████████████████████ 100 % 🟢
Release-Evidenzsystem           ████████████████████ 100 % 🟢
SAFE-FILE Simulation            ████████████████████ 100 % 🟢
0.5.1 Code-/Robustheitsaudit    ████████████████████ 100 % 🟢
0.5.1 TESTED-Promotion          ████████████████████ 100 % 🟢
Evidence-Sync / Main-Merge      ████████████████░░░░  80 % 🟡
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
- Entwicklungs-Lerngedächtnis umfasst 21 aktive strukturelle Regeln.

### Nutzerfreundlichkeit und Feedback

- Backend-Anfragen haben einen klaren 8-Sekunden-Timeout mit Hinweis auf die Startkonsole.
- „Neu prüfen“ läuft single-flight, zeigt `Prüfe …`, sperrt parallele Wiederholungen und setzt `aria-busy`.
- Theme-/Schriftänderungen zeigen sofort eine Vorschau, werden serialisiert gespeichert und bei Fehler auf den letzten bestätigten Stand zurückgesetzt.
- **Leer** und **nicht verfügbar** sind getrennte Zustände.
- Fehlerhafte Kalender-/Terminabfragen zeigen keine veralteten Daten unter einer neuen Überschrift.
- Ein später erfolgreicher TODO-Versuch entfernt einen zuvor gespeicherten Aktionsfehler.
- Der Boot-Guard unterscheidet Start, READY, READY mit Hinweisen und Startfehler.
- Theme-, Schrift- und Modulwahl verwenden `aria-pressed`.
- Einstellungen besitzen zuverlässige Tastaturfokusführung; Kalenderzellen erzeugen keine unnötigen Tabstopps.

### Moderneres Erscheinungsbild

Fünf Themes verwenden denselben semantischen Komponentenvertrag:

- **Aurora Glass** — Cyan/Violett, ruhig und modern.
- **Steel Night** — technisch, dunkel und klar.
- **Trash Neon** — kräftiger Subkultur-/Neonstil.
- **Clean Light** — helle, sachliche Arbeitsansicht.
- **High Contrast** — maximaler Kontrast ohne dekorative Schatten.

Farbe ist nie die einzige Statusinformation; Text/Icon bleiben zusätzlich erhalten. `prefers-reduced-motion` wird respektiert.

## 🧪 TESTED-Evidenz 0.5.1

- DEV-Gate: `33045348341` — Core/Release + Chromium + Firefox + Helper-UIs PASS.
- TESTED-Promotion: `33045669222` — **138/138 Tests**, Guards, Runtime-ZIP/Preflight, Chromium + Firefox + Helper-UIs PASS.
- Runtime-ZIP SHA256: `a7ab6d64e978e27c1fa550c549e12dc7ee21e24a17a55fd9c160c19cd3001b72`.
- GitHub-Artefakt-Digest: `62cc0787280328c1bfe5ff08628ea87ed1ec251bf718bf82178e2cfca88a85e0`.

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

Der Sicherheitsvertrag bleibt:

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
7. Eine TESTED-Version wird nach ihrer Evidenz nicht mehr durch Produktpatches verändert; neue Produktänderungen beginnen in einer neuen DEV-Version.

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

Keine neue Produktfunktion. Zuerst: **reinen Evidence-/Dokumentations-Sync vollständig prüfen → PR → Squash-Merge nach `main` → Main-CI → Main-Runtime-ZIP gegen den bewiesenen TESTED-Hash vergleichen.** Danach folgt Native L4 auf echtem Kubuntu.

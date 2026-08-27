# AIO-Tool

> **Aktueller Main-Stand:** 🟢 `0.5.1-audit-modern-ui-TESTED` — **BEWIESEN für L0–L3 auf `main`**  
> **Main-Commit:** `ee6adcfd3427e8328920edaceb804e7b6655cdb8`  
> **Main-CI:** `33048070879` — Core/Release + Chromium + Firefox + Helper-UIs erfolgreich  
> **Betrieb:** lokal · offline-first · keine Telemetrie · Loopback-only

AIO-Tool bündelt Kalender, TODOs, Erinnerungen, Ereignisse, Diagnose, Zielsystemabnahme und die weiterhin **nur simulierte** SAFE-FILE-Vorprüfung in einer laienfreundlichen lokalen Oberfläche.

## 🚦 Aktueller Zustand

| Bereich | Status | Bedeutung |
|---|---|---|
| `0.5.1` auf `main` | 🟢 BEWIESEN L0–L3 | 138 Tests, Guards, Runtime-Preflight und Cross-Browser-Gates bestanden |
| Runtime-Reproduzierbarkeit | 🟢 BEWIESEN | finaler Feature-Head und Squash-Main erzeugen denselben ZIP-SHA256 |
| Native Kubuntu L4 | 🟡 OFFEN | muss real auf dem Zielsystem bestätigt werden |
| SAFE-FILE echte Copy | 🔒 GESPERRT | Simulation besitzt weiterhin keine Dateimutation |

**Wichtig:** L0–L3 ersetzen keine reale Kubuntu-/DPI-/Browserzoom-/Tastaturabnahme L4.

## 📊 Entwicklungsfortschritt

```text
Foundation / Persistenz         ████████████████████ 100 % 🟢
Kalender / TODO / Ereignisse    ████████████████████ 100 % 🟢
Dashboard / Browser-Gates       ████████████████████ 100 % 🟢
Native Acceptance Runner        ████████████████████ 100 % 🟢
Release-Evidenzsystem           ████████████████████ 100 % 🟢
SAFE-FILE Simulation            ████████████████████ 100 % 🟢
0.5.1 Code-/Robustheitsaudit    ████████████████████ 100 % 🟢
0.5.1 Main-Integration          ████████████████████ 100 % 🟢
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
- Browser-Acceptance besitzt nur noch **eine kanonische Implementierung**; der CI-Einstieg ist ein dünner Wrapper.
- UI-Testassets werden aus dem aktuellen `index.html` abgeleitet statt Contract-Versionen mehrfach zu hardcodieren.
- Das Entwicklungs-Lerngedächtnis umfasst 21 aktive strukturelle Regeln.

### Nutzerfreundlichkeit und Feedback

- Backend-Anfragen haben einen klaren 8-Sekunden-Timeout mit verständlicher Hilfe.
- „Neu prüfen“ läuft single-flight, zeigt einen Busy-Zustand und verhindert parallele Doppelstarts.
- Theme-/Schriftänderungen werden serialisiert gespeichert; eine fehlgeschlagene Vorschau wird zurückgerollt.
- **Leer** und **nicht verfügbar** sind getrennte Zustände.
- Fehlgeschlagene Kalender-/Terminabfragen zeigen keine veralteten Daten als aktuell an.
- Erfolgreiche Wiederholungen entfernen alte Aktionsfehler.
- Bootstatus unterscheidet Start, READY, Hinweise und Fehler.
- Theme-, Schrift- und Modulwahl verwenden `aria-pressed`; Fokusführung und Tastaturbedienung wurden gehärtet.

### Erscheinungsbild

Fünf Themes verwenden denselben semantischen Komponentenvertrag:

- **Aurora Glass** — Cyan/Violett, ruhig und modern.
- **Steel Night** — technisch, dunkel und klar.
- **Trash Neon** — kräftiger Subkultur-/Neonstil.
- **Clean Light** — helle, sachliche Arbeitsansicht.
- **High Contrast** — maximaler Kontrast ohne dekorative Schatten.

Farbe ist nie die einzige Statusinformation; Text/Icon bleiben erhalten. `prefers-reduced-motion` wird respektiert.

## 🧪 Beweiskette 0.5.1

- DEV-Gate `33045348341` — PASS.
- TESTED-Promotion `33045669222` — **138/138 Tests**, Guards, Runtime-ZIP/Preflight, Chromium + Firefox + Helper-UIs PASS.
- finaler Evidence-Sync `33047743876` — PASS.
- PR-Integrationsgate `33047885115` — PASS.
- Squash-Main-Commit `ee6adcfd3427e8328920edaceb804e7b6655cdb8`.
- Main-CI `33048070879` — Core/Release + Chromium + Firefox + Native Runner + SAFE-FILE Helper-UI PASS.

### Reproduzierbarer Runtime-Hash

Der frühe Promotion-Hash `a7ab6d64…` entstand **vor** dem letzten Runtime-Metadaten-Sync der `VERSION_REGISTRY.json`. Da die Registry zur Runtime-Allowlist gehört, änderte dieser Sync berechtigt den ZIP-Inhalt.

Der eingefrorene finale Feature-Head `3dec31d22110f738c9964b937a53ddfe251a4d79` und der Squash-Main-Commit erzeugen dagegen **bytegenau denselben** Runtime-ZIP-SHA256:

`f8ffd88e2f3e40416f0d76b20786aa168cebb4e11fe3ef9d0eefa6dcf93b19ee`

Damit ist die Main-Reproduzierbarkeit nach dem finalen Runtime-Sync bewiesen.

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

oder per `native_acceptance.desktop`. Der Assistent führt durch 18 echte L4-Schritte. Kein Schritt wird automatisch auf PASS gesetzt.

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
7. Eine TESTED-Version wird nach ihrer Evidenz nicht durch weitere Produktpatches verändert; neue Produktänderungen benötigen eine neue DEV-Version.

## 🧪 Qualitätspyramide

- **L0:** Syntax / Schema
- **L1:** Unit-, Contract- und Regressionstests
- **L2:** gebautes Runtime-ZIP frisch entpacken und selbst prüfen
- **L3:** echte Chromium-/Firefox-Render-, Reflow- und Interaktionsgates
- **L4:** reale Kubuntu-/Browser-/Zoom-/Tastaturabnahme

## ➜ Nächster Schritt

`0.5.1` ist auf `main` für L0–L3 abgeschlossen. **Als Nächstes ausschließlich Native L4 real auf Kubuntu durchführen.** SAFE-FILE Copy/Move/Delete bleibt dabei technisch gesperrt.

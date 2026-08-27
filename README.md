# AIO-Tool

> **Lokales, modulares und laienfreundliches All-in-One-Tool für Kubuntu/Linux.** Kernfunktionen laufen offline auf dem eigenen Rechner; das Backend bindet ausschließlich an Loopback.

## 🧭 Status auf einen Blick

| Bereich | Zustand | Bedeutung |
|---|---|---|
| Aktueller automatisiert bewiesener Stand | 🟢 `0.5.0-native-acceptance-safe-file-sim-TESTED` | L0–L3: Core/Release + Chromium + Firefox erfolgreich |
| Native Kubuntu-Abnahme | 🟡 offen | L4 muss real über den neuen Prüfassistenten bestätigt werden |
| Internet für Kernfunktionen | 🟢 nicht nötig | offline-first |
| Telemetrie | 🟢 keine | keine automatische Nutzungsübertragung |
| SAFE-FILE-Ausführung | 🔒 gesperrt | getestet wurde die Simulation; echte Copy/Move/Delete existiert nicht |

### Fortschritt

```text
Native-Acceptance-Datenmodell      ████████████████████ 100 %  🟢
Native-Acceptance-UI/Runner        ████████████████████ 100 %  🟢
Release-Evidenzdateien             ████████████████████ 100 %  🟢
Evidence Guard                     ████████████████████ 100 %  🟢
SAFE-FILE-Vorprüfung               ████████████████████ 100 %  🟢
Failure-Matrix SF-001..010         ████████████████████ 100 %  🟢
Recovery-Vorvertrag                ████████████████████ 100 %  🟢
Automatisierte L0–L3-Gates         ████████████████████ 100 %  🟢
Native L4 auf echtem Kubuntu       ░░░░░░░░░░░░░░░░░░░░   0 %  🟡
Echte Copy-Ausführung              ░░░░░░░░░░░░░░░░░░░░   0 %  🔒
```

> **TESTED bedeutet hier:** Der implementierte Funktionsumfang wurde automatisiert bis L3 bewiesen. Es bedeutet **nicht**, dass die noch offene reale Kubuntu-L4-Abnahme automatisch bestanden wäre.

---

## ▶️ Drei Startwege

### 1. AIO-Tool normal

`start_tool.desktop` oder `start_tool.sh`

Die 9-Checkpoint-Startroutine prüft Runtime, Instanzidentität, Backend und Browserstart.

### 2. Native Acceptance Runner

`native_acceptance.desktop` oder `start_native_acceptance.sh`

Der Assistent führt durch **18 reale L4-Prüfschritte**:

- Kubuntu Desktop-Starter,
- Shell-Starter,
- passende Instanz wiederverwenden,
- fremd belegten Standardport behandeln,
- kleines / Full-HD / großes Fenster,
- reiner Tastaturdurchlauf,
- Firefox bei 100 / 125 / 150 / 175 / 200 %,
- Chrome/Chromium bei 100 / 125 / 150 / 175 / 200 %.

Jeder Schritt startet **🟡 OFFEN**. Nur du kannst ihn als 🟢 PASS, 🔴 FAIL oder ⚪ SKIP markieren. Es gibt kein Auto-PASS.

Die gemeinsame Sitzung liegt lokal in `runtime/native_acceptance.json`. Automatisch entstehen:

- `runtime/reports/native-acceptance-latest.json`
- `runtime/reports/native-acceptance-latest.txt`

Browserdaten wie Viewport, Bildschirmgröße und Device-Pixel-Ratio werden zur Diagnose gespeichert. Der Zielzoom wird dokumentiert, aber nicht fälschlich als automatisch sicher erkannt ausgegeben.

### 3. SAFE-FILE Simulation

`safe_file_simulation.desktop` oder `start_safe_file_simulation.sh`

Ablauf:

**Quelldatei auswählen → Zielordner auswählen → Konfliktoption → sichere Vorschau**

Geprüft werden Quelle, Symlinks, Dateityp, Lesbarkeit, Zielordner, Schreibbarkeit, freier Speicher + Reserve, Quelle/Ziel-Gleichheit und bestehende Zieldatei.

Der Sicherheitsvertrag ist technisch hart:

- `SIMULATION_ONLY=True`
- `EXECUTION_ENABLED=False`
- kein `/api/execute`
- keine Copy-/Move-/Delete-Primitive im Simulator
- `mutation_performed=false`

Damit hängt die Sperre nicht nur an einem deaktivierten Button.

---

## 🧯 SAFE-FILE Failure-Matrix

- `SF-001` Quelle fehlt
- `SF-002` Quelle ist keine normale Datei
- `SF-003` Quelle ist Symlink
- `SF-004` Ziel fehlt
- `SF-005` Ziel ist kein Ordner
- `SF-006` Ziel ist Symlink
- `SF-007` Ziel nicht beschreibbar
- `SF-008` zu wenig freier Speicher
- `SF-009` Zieldatei existiert
- `SF-010` Quelle entspricht dem Ziel

Alle zehn Fälle sind automatisiert getestet. Eine spätere echte Copy benötigt trotzdem einen **neuen Versionsslice** mit Jobjournal, Staging, Postvalidation, Crash-/Recoverytests und geschütztem Undo.

---

## 🧾 Release-Evidenz

Masterindex:

`evidence/RELEASE_EVIDENCE_INDEX.json`

Für jede TESTED-/höhere Version existiert genau eine Datei:

`evidence/releases/<version>.json`

Sie enthält Commit(s), CI-Runs, Artefakthashstatus, Browsermatrix und offene L4-Gates. `scripts/evidence_guard.py` blockiert Registry-/Evidenzdrift. Historisch nicht aufgezeichnete Werte bleiben ausdrücklich `not-recorded`; sie werden nicht erfunden.

---

## 🧪 Automatischer Nachweis für 0.5.0

Der DEV-Head `6cf6754dcf5da88edb13ee34f2e99b4e22bca593` bestand GitHub Actions Run `33038051967`:

- **113/113** Unit-/Contracttests,
- Foundation Validation,
- **18/18** Learning-Memory-Regeln,
- Release Evidence Guard,
- Documentation Guard,
- Bash-/JavaScript-Syntax,
- Runtime-ZIP + frischer Runtime-Preflight,
- Hauptdashboard in Chromium + Firefox,
- Native Acceptance Runner in Chromium + Firefox,
- SAFE-FILE-Simulation in Chromium + Firefox,
- Reflow-/Bedienzielprüfung der neuen Hilfsoberflächen bei 1280 und 360 CSS-px.

Die anschließende TESTED-Promotion wird erneut durch dieselbe komplette CI geprüft.

---

## 🛡️ Datenschutz / lokale Sicherheit

- Keine Telemetrie.
- Hauptbackend und beide Hilfsserver nur Loopback.
- Hilfsserver verlangen Host und Origin auf **demselben lokalen Port**.
- Native Berichte bleiben unter `runtime/` lokal.
- `evidence/` bleibt Repository-only und wird nicht ins Runtime-ZIP transportiert.
- SAFE-FILE liest nur für die Vorschau notwendige Metadaten und verändert keine Datei.

---

## Qualitätsebenen

- **L0:** Syntax / Schema
- **L1:** Unit / Contract / Failure-Matrix / Evidence Guard
- **L2:** echtes Runtime-ZIP frisch entpacken + Runtime-Preflight
- **L3:** echte Chromium-/Firefox-Render-/Interaktionstests
- **L4:** reales Kubuntu / Zoom / DPI / Tastatur über Native Acceptance Runner

Eine niedrigere Ebene darf keine höhere als bestanden behaupten.

## ➜ Nächste Reihenfolge

1. TESTED-Promotion-Commit erneut vollständig durch L0–L3 prüfen.
2. Danach Native Acceptance Runner **real auf Kubuntu** durchführen und den L4-Bericht sichern.
3. Nur bei ausgewerteter Failure-/Recovery-Matrix einen **neuen** Slice für echte Copy einer einzelnen normalen Datei planen.
4. Move, Rename und Delete bleiben weiterhin gesperrt.

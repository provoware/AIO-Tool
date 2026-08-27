# AIO-Tool

> **Lokales, modulares und laienfreundliches All-in-One-Tool für Kubuntu/Linux.** Kernfunktionen laufen offline auf dem eigenen Rechner; das Backend bindet ausschließlich an Loopback.

## 🧭 Status auf einen Blick

| Bereich | Zustand | Bedeutung |
|---|---|---|
| Letzter vollständig bewiesener Stand | 🟢 `0.4.3-integrity-hardening-TESTED` | Core/Release + Chromium + Firefox + Main-CI grün |
| Aktuelle Entwicklung | 🟠 `0.5.0-native-acceptance-safe-file-sim-DEV` | Native Abnahme, Evidenzindex und SAFE-FILE-Simulation werden neu geprüft |
| Internet für Kernfunktionen | 🟢 nicht nötig | offline-first |
| Telemetrie | 🟢 keine | keine automatische Nutzungsübertragung |
| SAFE-FILE-Ausführung | 🔒 gesperrt | aktuelle Version simuliert nur; keine Copy-/Move-/Delete-Funktion vorhanden |

### Fortschritt des aktuellen Slices

```text
Native-Acceptance-Datenmodell      ████████████████████ 100 %  🟢 umgesetzt
Native-Acceptance-UI/Runner        ████████████████████ 100 %  🟢 umgesetzt
Release-Evidenzdateien             ████████████████████ 100 %  🟢 umgesetzt
Evidence Guard                     ████████████████████ 100 %  🟢 umgesetzt
SAFE-FILE-Vorprüfung               ████████████████████ 100 %  🟢 umgesetzt
Failure-Matrix                     ████████████████████ 100 %  🟢 umgesetzt
Recovery-Vertrag                   ████████████████████ 100 %  🟢 umgesetzt
Echte Datei-Ausführung             ░░░░░░░░░░░░░░░░░░░░   0 %  🔒 absichtlich gesperrt
Finale CI / Browser-Evidenz        ░░░░░░░░░░░░░░░░░░░░   0 %  🟠 noch auszuführen
Native L4-Ergebnisse auf Kubuntu   ░░░░░░░░░░░░░░░░░░░░   0 %  🟡 müssen real bestätigt werden
```

> Prozentwerte zeigen Arbeitsfortschritt. **TESTED** entsteht ausschließlich durch den definierten Evidenzvertrag.

---

## ▶️ Die drei Startdateien

### 1. Normales AIO-Tool

`start_tool.desktop` oder `start_tool.sh`

Die bekannte 9-Checkpoint-Startroutine prüft Runtime, Instanzidentität, Backend und Browserstart.

### 2. Native Acceptance Runner

`native_acceptance.desktop` oder `start_native_acceptance.sh`

Der Assistent führt durch **18 reale L4-Prüfschritte**:

- Kubuntu Desktop-Starter,
- Shell-Starter,
- Wiederverwendung einer passenden Instanz,
- fremd belegter Standardport,
- kleines / Full-HD / großes Fenster,
- reiner Tastaturdurchlauf,
- Firefox bei 100 / 125 / 150 / 175 / 200 %,
- Chrome/Chromium bei 100 / 125 / 150 / 175 / 200 %.

### Ganz wichtig

Der Runner setzt **nichts automatisch auf PASS**.

Jeder Schritt startet als **🟡 OFFEN** und wird nur durch eine ausdrückliche Auswahl:

- 🟢 PASS,
- 🔴 FAIL,
- ⚪ SKIP

bewertet.

Die gemeinsame Sitzung liegt lokal in `runtime/native_acceptance.json`. Dadurch können Firefox und Chromium dieselbe Abnahme fortsetzen. Nach jeder Bewertung werden automatisch aktualisiert:

- `runtime/reports/native-acceptance-latest.json`
- `runtime/reports/native-acceptance-latest.txt`

Der Bericht enthält auch gemessene Browserdaten wie Viewport, Bildschirmgröße und Device-Pixel-Ratio. Er behauptet aber **nicht**, einen Zoomwert automatisch sicher erkannt zu haben; der Zielzoom muss real eingestellt und bestätigt werden.

### 3. SAFE-FILE Simulation

`safe_file_simulation.desktop` oder `start_safe_file_simulation.sh`

Ablauf:

1. **Quelldatei auswählen** – auf Kubuntu bevorzugt über `kdialog`.
2. **Zielordner auswählen**.
3. Konfliktverhalten nur für die Vorschau wählen:
   - sicher überspringen,
   - neuen Namen vorschlagen,
   - Ersetzen nur simulieren.
4. **Sichere Vorschau erstellen**.

Geprüft werden unter anderem:

- Quelle vorhanden/lesbar/normale Datei,
- Symlinks gesperrt,
- Ziel vorhanden/Ordner/beschreibbar,
- freier Speicher plus Reserve,
- Quelle und Ziel verschieden,
- bestehende Zieldatei / Konflikt.

### 🔒 Warum wirklich nichts kopiert werden kann

Der aktuelle SAFE-FILE-Slice besitzt absichtlich:

- `simulation_only = true`,
- `execution_enabled = false`,
- **keinen `/api/execute`-Endpunkt**,
- keine Copy-/Move-/Delete-Primitive im Simulator,
- `mutation_performed = false` im Vorschauvertrag.

Damit hängt die Sperre nicht nur an einem deaktivierten Button.

---

## 🧯 Failure-Matrix SAFE-FILE

Der erste Sicherheitsvertrag enthält zehn definierte Fehlerklassen:

`SF-001` Quelle fehlt · `SF-002` Quelle keine Datei · `SF-003` Source-Symlink · `SF-004` Ziel fehlt · `SF-005` Ziel kein Ordner · `SF-006` Target-Symlink · `SF-007` Ziel nicht beschreibbar · `SF-008` zu wenig Speicher · `SF-009` Zielkonflikt · `SF-010` Quelle = Ziel.

Eine spätere echte Copy-Funktion darf erst entstehen, wenn diese Matrix und der Recovery-Vertrag vollständig grün sind.

---

## ↩️ Recovery-Vertrag für die spätere Copy-Stufe

Da die aktuelle Simulation **nichts verändert**, ist heute kein Rollback notwendig. Sie definiert aber bereits verbindlich, was vor einer echten Copy-Freigabe vorhanden sein muss:

- persistentes Journal/Jobprotokoll **vor** der ersten Mutation,
- `DONE` erst nach Nachvalidierung,
- Undo darf ein Ziel nur entfernen, wenn verifiziert wurde, dass es seit der Copy nicht verändert wurde,
- unterbrochene `.part`-/Staging-Zustände müssen als Recovery-Fall sichtbar werden.

---

## 🧾 Release-Evidenzindex

Repository-only:

`evidence/RELEASE_EVIDENCE_INDEX.json`

Dieser verweist auf **genau eine Datei je bewiesener Version**, zum Beispiel:

`evidence/releases/0.4.3-integrity-hardening.json`

Jede Datei enthält maschinenlesbar:

- Registry-Commit,
- Promotion-/Main-Commit soweit vorhanden,
- CI-Run-IDs,
- Artefakt-SHA256 bzw. ausdrücklich `not-recorded`,
- Chromium-/Firefox-Matrix,
- weiterhin offene L4-Gates.

`scripts/evidence_guard.py` vergleicht den Index mit `VERSION_REGISTRY.json`. Eine TESTED-Version ohne Evidenzdatei macht CI rot.

Historische Lücken werden **nicht erfunden**. Ein nicht mehr belegbarer alter Artefakthash wird als `not-recorded` dokumentiert.

---

## 🛡️ Datenschutz und Sicherheit

- Kernbackend nur `127.0.0.1` / `localhost`.
- Native Runner und SAFE-FILE-Simulator verlangen zusätzlich **denselben lokalen Port** für Host/Origin.
- Keine Telemetrie.
- Native Abnahmeberichte bleiben lokal unter `runtime/`.
- Release-Evidenz bleibt im Repository und wird nicht ins Runtime-ZIP gepackt.
- SAFE-FILE liest nur Metadaten/Dateigröße und führt keine Mutation aus.

---

## 🧪 Qualitätsebenen

- **L0:** Syntax / Schema
- **L1:** Unit / Contract / Failure-Matrix
- **L2:** vollständiges Runtime-ZIP frisch entpacken und Preflight daraus starten
- **L3:** echte Chromium-/Firefox-Render-/Interaktionsmatrix
- **L4:** reale Kubuntu-/Zoom-/DPI-/Tastaturabnahme über den neuen Runner

Eine niedrigere Ebene darf niemals eine höhere als bestanden darstellen.

---

## 📦 Runtime vs. Repository

Im Nutzer-ZIP liegen nur Dateien aus `manifests/RUNTIME_MANIFEST.json` plus `MANIFEST_RELEASE.json`.

Der Runtime-Bestand enthält jetzt zusätzlich die beiden lokalen Assistenten und ihre benötigten Module/Webseiten. Nicht transportiert werden weiterhin:

- README / AGENTS / TODO / Changelog,
- Tests/Testdaten,
- `evidence/`,
- Learning Memory,
- CI-Dateien,
- Screenshots/Reports,
- lokale Runtime-/Nutzerdaten.

---

## ➜ Nächste logische Reihenfolge

1. `0.5.0-native-acceptance-safe-file-sim` vollständig durch Unit/Failure-/Evidence-/Release-/Cross-Browser-Gates prüfen.
2. Danach Native Acceptance Runner **real auf Kubuntu** ausführen und L4-Bericht erzeugen.
3. Nur wenn SAFE-FILE Failure-Matrix + Recovery + reale Basisgates grün sind, einen neuen Versionsslice für echte **Copy-only**-Ausführung beginnen.
4. Move, Rename und Delete bleiben weiterhin später.

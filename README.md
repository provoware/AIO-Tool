# AIO-Tool

> **Runtime-Baseline:** 🟢 `0.5.1-audit-modern-ui-TESTED` — `tested / draft`, **L0–L3 BEWIESEN**  
> **Runtime-Baseline-Commit:** `ee6adcfd3427e8328920edaceb804e7b6655cdb8`  
> **Runtime-ZIP SHA256:** `f8ffd88e2f3e40416f0d76b20786aa168cebb4e11fe3ef9d0eefa6dcf93b19ee`  
> **Native L4:** 🟡 **OFFEN · 0/18 real bestätigt**  
> **SAFE-FILE-Ausführung:** 🔒 **GESPERRT**

AIO-Tool ist ein lokales, offline-first Werkzeug mit Python-Loopback-Backend und Browseroberfläche. Es bündelt Kalender, TODOs, Erinnerungen, Ereignisse, Diagnose, geführte Zielsystemabnahme und eine weiterhin ausschließlich simulationsfähige SAFE-FILE-Vorprüfung.

## 🚦 Status auf einen Blick

| Bereich | Status | Bedeutung |
|---|---|---|
| Runtime-Baseline 0.5.1 | 🟢 BEWIESEN L0–L3 | 138 Tests, Guards, Runtime-Preflight und Cross-Browser-Gates bestanden |
| Runtime-Reproduzierbarkeit | 🟢 BEWIESEN | finaler Feature-Runtime-Head und Squash-Main erzeugen denselben ZIP-SHA256 |
| Native Kubuntu L4 | 🟡 OFFEN | 0 von 18 manuellen Prüfschritten bestätigt |
| SAFE-FILE echte Ausführung | 🔒 GESPERRT | Simulation besitzt weiterhin keine Ausführungsfähigkeit |

**Wichtig:** L0–L3 beweisen automatisierbare Qualität. L4 ist eine davon getrennte reale Kubuntu-/Browser-/Zoom-/Tastaturabnahme und darf niemals aus CI abgeleitet werden.

## 📊 Fortschritt

```text
Foundation / Persistenz         ████████████████████ 100 % 🟢
Kalender / TODO / Ereignisse    ████████████████████ 100 % 🟢
Dashboard / Browser-Gates       ████████████████████ 100 % 🟢
Native Acceptance Runner        ████████████████████ 100 % 🟢 implementiert
Release-Evidenzsystem           ████████████████████ 100 % 🟢
SAFE-FILE Simulation            ████████████████████ 100 % 🟢
0.5.1 Runtime/Main-Integration  ████████████████████ 100 % 🟢
Manifest-/Info-Konsistenz       ████████████████████ 100 % 🟢 strukturell gehärtet
Native Kubuntu L4               ░░░░░░░░░░░░░░░░░░░░   0 % 🟡 0/18 bestätigt
SAFE-FILE Ausführung            ░░░░░░░░░░░░░░░░░░░░   0 % 🔒
```

## 🧭 Welche Datei sagt was?

| Wahrheitsebene | Kanonische Quelle | Zweck |
|---|---|---|
| Version / Status | `VERSION` + `VERSION_REGISTRY.json` | Welche Produktversion und welcher Releasezustand gelten? |
| Runtime-Transport | `manifests/RUNTIME_MANIFEST.json` | Welche Dateien gehören tatsächlich in das Runtime-ZIP? |
| Release-Beweis | `evidence/RELEASE_EVIDENCE_INDEX.json` + versionierte Einzelevidenz | Welcher Commit, CI-Lauf und Artefakt-Hash wurden wirklich bewiesen? |
| Repository-Bestand | `manifests/DEVELOPMENT_MANIFEST.json` | Welche Doku-, Test-, Evidenz- und Entwicklungsdateien bleiben repo-only? |
| Menschenlesbarer Überblick | `MANIFEST.md` | Kompakte Zusammenfassung der obigen Wahrheitsquellen |

Ein **Repository-Head** kann nach der eingefrorenen Runtime-Baseline noch reine Dokumentations-/Evidenzänderungen enthalten. Er ist deshalb nicht automatisch ein neuer Produkt- oder Runtime-Commit.

## ✨ Kernverbesserungen der Runtime-Baseline 0.5.1

### Robustheit

- `AtomicJsonStore` serialisiert parallele Read→Mutate→Write-Transaktionen.
- Backups werden atomar erneuert.
- `ConfigStore` nutzt denselben Persistence-Core.
- Hauptbackend und Hilfsserver verwenden denselben exakten Loopback-Host-/Port-Vertrag.
- Serverlog-Schreibvorgänge sind im Threading-Backend serialisiert.
- Browser-Acceptance besitzt nur eine kanonische Harness-Implementierung.

### Nutzerführung

- lokale API-Anfragen besitzen einen begrenzten Timeout mit verständlicher Hilfe,
- Refresh und Config-Speichern laufen single-flight mit sichtbarem Busy-Zustand,
- **leer**, **nicht verfügbar** und **veraltet** werden getrennt behandelt,
- fehlgeschlagene Theme-Vorschau rollt auf den bestätigten Stand zurück,
- Bootstatus, Fokus und Auswahlzustände sind auch assistiven Technologien eindeutig zugänglich.

### Erscheinungsbild

Fünf Themes verwenden denselben semantischen Komponentenvertrag: **Aurora Glass**, **Steel Night**, **Trash Neon**, **Clean Light** und **High Contrast**. Farbe ist nie das einzige Statussignal; `prefers-reduced-motion` wird berücksichtigt.

## 🧪 Kanonische Beweiskette

Die vollständige maschinenlesbare Evidenz liegt in:

`evidence/releases/0.5.1-audit-modern-ui.json`

Dort sind unter anderem festgehalten:

- Runtime-Baseline-Commit `ee6adcfd3427e8328920edaceb804e7b6655cdb8`,
- Main-CI `33048070879`,
- finaler Runtime-SHA256 `f8ffd88e2f3e40416f0d76b20786aa168cebb4e11fe3ef9d0eefa6dcf93b19ee`,
- Chromium-/Firefox-Matrix,
- weiterhin offene L4-Gates.

Der ältere Promotion-Hash `a7ab6d64…` ist dort ausdrücklich als **abgelöstes Vorartefakt** dokumentiert. Er entstand vor dem letzten Runtime-Metadaten-Sync und ist nicht der finale Main-Artefakthash.

## 📦 Manifest-System

- Runtime-Manifest: `1.3.0` — für die bewiesene 0.5.1-Runtime **eingefroren**.
- Development-Manifest: `1.2.0` — klassifiziert repo-only Inhalte und die Dokumentationspflicht.
- `MANIFEST_RELEASE.json` — wird reproduzierbar beim Build erzeugt und enthält Dateigrößen und Einzel-SHA256.
- `scripts/manifest_guard.py` — verhindert Überschneidungen und Klassifikationsdrift.

Details: `manifests/README.md`.

## ▶️ Start

Normales Dashboard:

```bash
./start_tool.sh
```

Reale Zielsystemabnahme:

```bash
./start_native_acceptance.sh
```

SAFE-FILE Simulation:

```bash
./start_safe_file_simulation.sh
```

## 🛡️ Unveränderte Sicherheitsgrenzen

1. Backend nur auf Loopback; keine Netzwerkfreigabe.
2. Keine Telemetrie.
3. Persistente JSON-Zustände werden validiert, atomar und thread-sicher geschrieben.
4. Runtime-ZIP entsteht ausschließlich aus der positiven Runtime-Allowlist plus generiertem Release-Manifest.
5. Dokumentation, Tests, Release-Evidenz und Entwicklungslogs bleiben repo-only.
6. Eine bewiesene Runtime-Version wird nicht nachträglich durch Produktpatches verändert.
7. SAFE-FILE bleibt bis zu einem eigenen evidenzgebundenen Ausführungsslice ohne reale Ausführungsfähigkeit.

## 🧪 Qualitätspyramide

- **L0:** Syntax / Schema
- **L1:** Unit-, Contract- und Regressionstests
- **L2:** echtes gebautes und frisch geprüftes Runtime-ZIP
- **L3:** Chromium-/Firefox-Render-, Reflow- und Interaktionsgates
- **L4:** reale Kubuntu-/Browser-/Zoom-/Tastaturabnahme

## ➜ Nächster Schritt

Die Runtime-Baseline bleibt `0.5.1`. Als nächstes wird **Native L4 real auf Kubuntu** durchgeführt. Bis dahin bleiben alle 18 L4-Schritte OFFEN und SAFE-FILE unverändert gesperrt.

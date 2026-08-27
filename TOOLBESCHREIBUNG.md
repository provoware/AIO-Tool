# TOOLBESCHREIBUNG — AIO-Tool

## Aktueller Qualitätsstand

**Runtime-Baseline:** `0.5.1-audit-modern-ui` — 🟢 `tested / draft`, **L0–L3 BEWIESEN**  
**Runtime-Baseline-Commit:** `ee6adcfd3427e8328920edaceb804e7b6655cdb8`  
**Runtime-ZIP SHA256:** `f8ffd88e2f3e40416f0d76b20786aa168cebb4e11fe3ef9d0eefa6dcf93b19ee`  
**Native L4:** 🟡 **OFFEN · 0/18 real bestätigt**  
**SAFE-FILE-Ausführung:** 🔒 **GESPERRT**

AIO-Tool ist ein lokales, offline-first Werkzeug mit Python-Loopback-Backend und Browseroberfläche. Die Runtime-Baseline 0.5.1 fokussiert Robustheit, Wartbarkeit, verständliches Nutzerfeedback, Barrierefreiheit und ein modernes Theme-System, ohne die SAFE-FILE-Simulation in eine reale Ausführungsfunktion umzuwandeln.

## Architektur in Kurzform

```text
Launcher
   ↓
Loopback-Backend
   ↓
Domänen-Stores / Persistenz
   ↓
Browser-Dashboard
   ↓
separate Test- und Evidence-Schichten
```

Runtime, Entwicklung, Release-Evidenz und lokale Nutzerdaten sind bewusst getrennte Ebenen.

## Wahrheitsebenen

| Thema | Kanonische Quelle |
|---|---|
| Produktversion / Status | `VERSION` + `VERSION_REGISTRY.json` |
| Runtime-Dateimenge | `manifests/RUNTIME_MANIFEST.json` |
| Release-Beweis | `evidence/RELEASE_EVIDENCE_INDEX.json` + `evidence/releases/*.json` |
| Repository-only Bestand | `manifests/DEVELOPMENT_MANIFEST.json` |
| Menschenlesbarer Status | `MANIFEST.md` |

Der **Runtime-Baseline-Commit** ist der bewiesene Programm-/Transportstand. Ein späterer **Repository-Head** kann zusätzliche reine Dokumentations- oder Evidenzänderungen enthalten und ist deshalb nicht automatisch eine neue Runtime-Version.

## Persistenz und Robustheit

`AtomicJsonStore` serialisiert parallele Read→Mutate→Write-Zyklen über einen gemeinsamen reentranten Lock. Hauptdatei und Backup werden atomar ersetzt. `ConfigStore` verwendet denselben Persistence-Core statt einer zweiten Schreibimplementierung.

Wichtige Zustandsregeln:

- beschädigte Persistenz ist kein normaler Eingabefehler,
- fehlgeschlagene Reloads dürfen keine alten Werte als aktuell anzeigen,
- **leer**, **nicht verfügbar** und **veraltet** bleiben getrennte Zustände,
- konkurrierende Refresh-/Config-Aktionen laufen single-flight,
- Wartevorgänge besitzen einen begrenzten Timeout und eine verständliche nächste Handlung.

## Lokale Sicherheit

Hauptbackend, Native Runner und SAFE-FILE Simulator verwenden denselben exakten Loopback-Host-/Port-Vertrag. Fremde Hosts und Cross-Port-Origin-Anfragen gelten nicht als vertrauenswürdig. Es gibt keine Telemetrie.

## Dashboard und Barrierefreiheit

- Boot-Guard für Start, READY, Hinweise und Fehler,
- sichtbare Busy-Zustände mit `aria-busy`,
- `aria-pressed` für Auswahlzustände,
- Fokusführung und logische Tastaturreihenfolge,
- dynamische Inhalte ohne `innerHTML`,
- Farbe nie als einziges Statussignal,
- `prefers-reduced-motion` wird respektiert.

## Theme-System

Fünf Themes nutzen denselben semantischen Tokenvertrag:

- Aurora Glass
- Steel Night
- Trash Neon
- Clean Light
- High Contrast

Oberflächenebenen, Akzent, Fokus, Status, Schatten und Kontrast sind getrennt definiert.

## Browser-Acceptance

`scripts/ui_acceptance.py` ist die einzige kanonische Browser-Acceptance-Implementierung. Der CI-Einstieg bleibt ein dünner Wrapper. Produktassets werden aus dem aktuellen HTML-Vertrag abgeleitet; Fixture-Reihenfolge und Ready-Zustand sind regressionsgesichert.

L3 umfasst echte Chromium-/Firefox-Render-, Reflow- und Interaktionsgates. L4 wird davon ausdrücklich getrennt.

## Native Acceptance L4

Der Native Runner enthält 18 manuelle Prüfschritte für:

- Kubuntu-Startpfade und Instanzverhalten,
- fremd belegten Port,
- kleine / Full-HD / große Anzeige,
- reine Tastaturbedienung,
- Firefox 100–200 %,
- Chrome/Chromium 100–200 %.

Jeder Schritt startet OFFEN. `pass`, `fail` und `skip` werden ausschließlich nach realer Nutzerbeobachtung gespeichert. Solange kein Schritt bestätigt wurde, gilt **0/18 = 0 %**.

## SAFE-FILE-Grenze

Unverändert gilt:

- `SIMULATION_ONLY=True`
- `EXECUTION_ENABLED=False`
- kein Execute-Endpunkt
- keine reale Ausführungsprimitive in der Simulationsstufe

Eine spätere reale Ausführung benötigt eine neue Produktversion mit Jobjournal, Staging, Postvalidation, Crash-/Recoverytests und Guarded Undo.

## Manifest-System

### Runtime-Manifest 1.3.0

`manifests/RUNTIME_MANIFEST.json` ist die positive Transport-Allowlist der bewiesenen 0.5.1-Runtime und deshalb eingefroren.

### Development-Manifest 1.2.0

`manifests/DEVELOPMENT_MANIFEST.json` klassifiziert Repository-only Dokumentation, Tests, Evidenz, CI-/Build-Hilfen, lokale Reports und die Manifest-Policy.

### Manifest Guard

`scripts/manifest_guard.py` verhindert insbesondere:

- Überschneidung von Runtime- und repo-only Klassifikation,
- fehlende Pflichtdokumente im Development-Inventar,
- unzulässige Runtime-Dateien unter verbotenen Präfixen,
- Fehlinterpretation der historischen `generated_files`-Semantik.

Details stehen in `manifests/README.md`.

## Release-Evidenz

Kanonische Quelle für 0.5.1:

`evidence/releases/0.5.1-audit-modern-ui.json`

Darin sind festgehalten:

- Runtime-Baseline-Commit `ee6adcfd3427e8328920edaceb804e7b6655cdb8`,
- Main-CI `33048070879`,
- Runtime-ZIP SHA256 `f8ffd88e2f3e40416f0d76b20786aa168cebb4e11fe3ef9d0eefa6dcf93b19ee`,
- Cross-Browser-Matrix,
- Reproduzierbarkeit zwischen finalem Runtime-Feature-Head und Main,
- abgelöstes Promotion-Artefakt,
- offene L4-Gates.

## Nächster Qualitätsweg

Die Runtime-Baseline bleibt unverändert. Als nächstes wird ausschließlich **Native L4 real auf Kubuntu** durchgeführt. Vor Abschluss dieser realen Abnahme wird kein höherer L4-Status behauptet und SAFE-FILE bleibt technisch gesperrt.

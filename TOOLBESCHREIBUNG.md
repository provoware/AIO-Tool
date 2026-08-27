# TOOLBESCHREIBUNG — AIO-Tool

## Qualitätsstand

**Aktueller Entwicklungsslice:** `0.6.0-autostart-selfheal` — `development / draft`  
**Runtime-Baseline:** `0.5.1-audit-modern-ui` — letzter bereits bewiesener L0–L3-Stand  
**Native L4:** 🟡 **OFFEN · 0 % automatisch aufgewertet**  
**SAFE-FILE-Ausführung:** 🔒 **GESPERRT**

AIO-Tool ist ein lokales, offline-first Werkzeug mit Python-Loopback-Backend und Browseroberfläche. Version 0.6.0 erweitert den Startpfad um autonome Vorprüfung, begrenzte Selbstreparatur, Release-Recovery und einen selbstenthaltenen Linux-x86_64-Build.

## Architektur 0.6.0

```text
start_tool.sh / AIO-Tool-Start
          ↓
      app.autostart
          ↓
 ┌────────┼─────────┐
 │        │         │
Preflight Self-Heal Recovery
 │        │         │
 └────────┼─────────┘
          ↓
 freie Loopback-Instanz
          ↓
 Backend-READY
          ↓
 Browser-/Dashboard-Handshake
```

## Autostart

`app/autostart.py` ist der kanonische Startkoordinator. Er besitzt sichtbare Checkpoints und behandelt Portwahl, stale PID, Runtime-Recovery, Persistenzgesundheit, Preflight, Backend-Start und Browser-Handshake in einer reproduzierbaren Reihenfolge.

## Self-Healing

`app/runtime_health.py` prüft die lokalen Kernstores vor dem Serverstart. Reihenfolge pro Datei:

1. Hauptdatei validieren.
2. Bei Fehler gültiges Backup prüfen.
3. Beschädigte Hauptdatei vor Ersatz quarantänisieren.
4. Bei brauchbarem Backup dieses atomar wiederherstellen.
5. Sind Hauptdatei und Backup unbrauchbar, beide quarantänisieren und nur dann einen validierten sicheren Standard erzeugen.

Damit wird ein kaputter Zustand repariert, ohne das ursprüngliche Beweismaterial still zu vernichten.

## Release-Recovery

`app/runtime_recovery.py` arbeitet nur, wenn **beide** Buildmarker vorhanden sind:

- `MANIFEST_RELEASE.json`
- `RECOVERY_BASIS.zip`

Ein Source-Checkout ohne diese Marker wird nicht automatisch verändert. Die Recovery-Basis enthält für jede Runtime-Allowlist-Datei Größe und SHA256. Eine beschädigte Runtime-Datei wird vor Ersatz in die Runtime-Quarantäne verschoben.

## Read-only-Quelle

Ist die Installationsbasis tatsächlich nicht schreibbar, wird sie in einen benutzereigenen Zustandsbereich gespiegelt. Die Installation selbst bleibt unangetastet; anschließend startet dieselbe Version aus dem beschreibbaren Spiegel.

## Portable Linux x86_64

- Entry-Point: `scripts/portable_entry.py`
- Builder: `scripts/build_portable.py`
- Build-Abhängigkeit: `requirements-build.txt`
- Technik: PyInstaller onedir
- Starter im Paket: `AIO-Tool-Start`
- zusätzlicher Laienstart: `start_tool.sh`
- eingebettet: `MANIFEST_RELEASE.json` + `RECOVERY_BASIS.zip`

## Qualitätskette

1. **Core-CI:** Syntax, Unit-/Integrationstests, Guards, Runtime-Release.
2. **Failure-Matrix:** künstliche Port-, PID-, Persistenz- und Recovery-Fehler.
3. **Source-ZIP:** exaktes `git archive` desselben Commits.
4. **RECOVERY_BASIS:** deterministische Hash-/Dateimengenprüfung.
5. **Portable-Build:** gepinnter PyInstaller-Build.
6. **Portable-Smoke:** normaler Start plus Read-only-Quellspiegelung.
7. **Chromium:** striktes UI-Gate.
8. **Firefox:** striktes UI-Gate.

Die Jobs sind hart sequenziell voneinander abhängig.

## Manifest-System

`manifests/RUNTIME_MANIFEST.json` ist in 0.6.0 auf Version `2.0.0` angehoben. Es trennt Runtime-Allowlist, Build-generierte Dateien (`MANIFEST_RELEASE.json`, `RECOVERY_BASIS.zip`) und erst lokal entstehende Zustände (`runtime/**`, Instanzmarker).

`manifests/DEVELOPMENT_MANIFEST.json` klassifiziert Tests, Build-/CI-Helfer und Dokumentation als repository-only.

## Evidenzgrenze

`0.6.0-autostart-selfheal` ist während dieses Slices noch nicht bewiesen und besitzt deshalb bewusst noch keine vorweggenommene Release-Evidenz. Der Documentation Guard unterscheidet nun Entwicklung und bewiesene Zustände korrekt. Native L4 bleibt **OFFEN**.

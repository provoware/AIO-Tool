# AIO-Tool

> **Aktueller Entwicklungsslice:** 🟡 `0.6.0-autostart-selfheal` — `development / draft`  
> **Artefaktmarker:** `0.6.0-autostart-selfheal-DEV`  
> **Bewiesene Runtime-Baseline:** 🟢 `0.5.1-audit-modern-ui` — L0–L3 BEWIESEN  
> **Native Kubuntu L4:** 🟡 **OFFEN · 0 % automatisch aufgewertet**  
> **SAFE-FILE-Ausführung:** 🔒 **GESPERRT**

AIO-Tool ist ein lokales, offline-first Werkzeug mit Python-Loopback-Backend und Browseroberfläche. Der Entwicklungsslice `0.6.0-autostart-selfheal` erweitert die bewiesene 0.5.1-Basis um eine autonome Klick-&-Start-Routine, datensichere Selbstreparatur, eine Build-Recovery-Basis und ein portables Linux-x86_64-Paket.

## 🚦 Was 0.6.0 neu macht

- automatische freie Loopback-Portwahl statt Startabbruch bei Portkonflikt,
- Erkennung und Entfernung veralteter eigener PID-Dateien,
- sichere Reparatur beschädigter lokaler JSON-Zustände,
- Originale werden vor Ersatz in `runtime/quarantine/` erhalten,
- `RECOVERY_BASIS.zip` repariert beschädigte **immutable Runtime-Dateien** nur in gebauten Releases,
- Source-Checkouts werden durch Recovery niemals heimlich überschrieben,
- Browser-Ready-/Backend-Handshake statt bloßem „Prozess wurde gestartet“,
- bei schreibgeschützter Programmbasis wird in einen benutzereigenen Bereich gespiegelt,
- Portable Linux x86_64 enthält den Python-Interpreter; kein `sudo`, kein `pip`, kein venv nötig.

## 🧪 Atomare Prüfkette

Der Slice gilt erst dann als geprüft, wenn **alle Gates in dieser Reihenfolge** grün sind:

```text
01 Core-CI
   ↓
02 Failure-Matrix
   ↓
03 Source-ZIP
   ↓
04 RECOVERY_BASIS
   ↓
05 Portable-Build
   ↓
06 Portable-Smoke
   ↓
07 Chromium
   ↓
08 Firefox
```

Ein späteres Gate darf ein früheres nicht überspringen. Der Branch-Commit ist die einzige Eingangsquelle für alle acht Gates.

## ▶️ Start

### Quell-/Runtime-Paket

```bash
./start_tool.sh
```

Die Startroutine sucht selbstständig einen kompatiblen Python-Interpreter ab 3.10 und startet anschließend `app.autostart`.

### Portable Linux x86_64

```bash
./start_tool.sh
```

Im Portable-Paket erkennt derselbe Starter `AIO-Tool-Start` und verwendet automatisch den gebündelten Interpreter.

### Automatischer Prüflauf ohne Browser

```bash
./start_tool.sh --no-browser --preflight-only
```

## 🛡️ Datensicherheit

1. Reparaturen an Nutzerdaten ersetzen ein beschädigtes Original nie kommentarlos.
2. Verwertbare Backups werden bevorzugt wiederhergestellt.
3. Nicht verwertbare Haupt-/Backupdateien werden vor einem sicheren Reset quarantänisiert.
4. `RECOVERY_BASIS.zip` ist hashgebunden und repariert nur die im Runtime-Manifest geführte Basis.
5. Die Recovery-Funktion ist in Source-Checkouts ohne `MANIFEST_RELEASE.json` deaktiviert.
6. Backend und Hilfsoberflächen bleiben Loopback-only; keine Telemetrie.
7. SAFE-FILE bleibt simulationsgebunden und besitzt keine reale Datei-Ausführungsfunktion.

## 📦 Manifest- und Build-Vertrag

- `manifests/RUNTIME_MANIFEST.json` — Runtime-Allowlist, Manifest-Version `2.0.0`.
- `manifests/DEVELOPMENT_MANIFEST.json` — Repository-only Dateien und Prüfinfrastruktur.
- `MANIFEST_RELEASE.json` — beim Runtime-Build erzeugte Datei-/Hashliste.
- `RECOVERY_BASIS.zip` — deterministisch erzeugte Recovery-Kopie der Runtime-Allowlist.
- `requirements-build.txt` — exakt gepinnter PyInstaller für den Portable-Build.

## 🧭 Wahrheitsebenen

Die **Runtime-Baseline** `0.5.1-audit-modern-ui` bleibt der letzte bereits bewiesene Produktstand. `0.6.0-autostart-selfheal` ist während dieses Branch-Slices ausdrücklich `development / draft`. Erst ein vollständig grüner Pipeline-Lauf darf eine spätere Statuspromotion begründen; CI macht Native L4 nicht automatisch zu PASS.

## 📊 Entwicklungsstatus 0.6.0

```text
Runtime-/Self-Heal-Code          ████████████████████ 100 % 🟢 vorbereitet
Test-/Build-/Doku-Vertrag        ████████████████████ 100 % 🟢 im atomaren Tree
Atomarer Branch-Commit           ░░░░░░░░░░░░░░░░░░░░   0 % bis Commit/Ref-Verifikation
8-stufige CI-Beweiskette         ░░░░░░░░░░░░░░░░░░░░   0 % bis GitHub Actions
Native Kubuntu L4                ░░░░░░░░░░░░░░░░░░░░   0 % 🟡 OFFEN
SAFE-FILE Ausführung             ░░░░░░░░░░░░░░░░░░░░   0 % 🔒 GESPERRT
```

Weitere technische Details: `docs/0.6.0-AUTOSTART-SELFHEAL.md`.

# MANIFEST — AIO-Tool

## 1. Projektstatus

- **Produkt:** AIO-Tool
- **Aktuelle Produktversion im Repository:** `0.6.0-autostart-selfheal`
- **Status:** `development`
- **Release-Status:** `draft`
- **Artefaktmarker:** `0.6.0-autostart-selfheal-DEV`
- **Runtime-Baseline:** `0.5.1-audit-modern-ui` bleibt der letzte bereits bewiesene L0–L3-Stand.
- **Native Kubuntu L4:** 🟡 **OFFEN · 0 % automatisch aufgewertet**
- **SAFE-FILE-Ausführung:** 🔒 **GESPERRT**

`0.6.0-autostart-selfheal` wird erst nach der vollständigen achtstufigen Pipeline zur Promotion bewertet. Ein `development`-Datensatz besitzt bewusst noch keine vorweggenommene Release-Evidenz.

## 2. Wahrheitsebenen

| Ebene | Kanonische Quelle | Aussage |
|---|---|---|
| Version / Status | `VERSION` + `VERSION_REGISTRY.json` | aktueller Produkt-/Entwicklungszustand |
| Runtime-Transport | `manifests/RUNTIME_MANIFEST.json` | positive Runtime-Allowlist |
| Release-Beweis | `evidence/RELEASE_EVIDENCE_INDEX.json` + Einzelevidenz | nur bewiesene Versionen |
| Repository-Bestand | `manifests/DEVELOPMENT_MANIFEST.json` | repo-only Doku, Tests, Build, CI, Evidenz |
| Menschenlesbarer Status | `MANIFEST.md` | Zusammenfassung ohne Parallelwahrheit |

## 3. Runtime-Manifest 2.0.0

Die 0.6.0-Runtime enthält zusätzlich den autonomen Start-/Recovery-Vertrag:

- `app/autostart.py`
- `app/preflight.py`
- `app/runtime_health.py`
- `app/runtime_recovery.py`
- `app/startup_progress.py`
- `scripts/portable_entry.py`

Build-generiert und deshalb nicht als feste Quelldatei geführt:

- `MANIFEST_RELEASE.json`
- `RECOVERY_BASIS.zip`

Lokal erzeugt und nicht transportiert:

- `runtime/**`
- `web/.aio-instance-id`

## 4. Development-Inventar

Repository-only bleiben unter anderem:

- `.github/`
- `tests/`
- `testdata/`
- `docs/`
- `evidence/`
- `requirements-ui.txt`
- `requirements-build.txt`
- Release-/Failure-/Recovery-/Portable-Buildhelper.

## 5. Atomare Gate-Kette

```text
01 Core-CI
02 Failure-Matrix
03 Source-ZIP
04 RECOVERY_BASIS
05 Portable-Build
06 Portable-Smoke
07 Chromium
08 Firefox
```

Jeder Job benötigt den vorherigen Job. Das verhindert, dass ein visuelles PASS einen fehlerhaften Core-/Buildzustand verdeckt.

## 6. Invarianten

1. Ein Slice wird aus genau einem Git-Tree und einem Commit geprüft.
2. Source-ZIP und alle Builds stammen aus exakt diesem Commit.
3. Runtime-Recovery arbeitet nur in einem gebauten Release mit `MANIFEST_RELEASE.json` und `RECOVERY_BASIS.zip`.
4. Beschädigte Nutzerdaten werden vor Ersatz quarantänisiert.
5. Repo-only Dateien gelangen nicht in das Runtime-ZIP.
6. `development` darf keine Release-Evidenz vortäuschen.
7. Native L4 bleibt **OFFEN**, bis reale Zielsystembeobachtung vorliegt.
8. SAFE-FILE-Ausführung bleibt **GESPERRT**.

## 7. Automatische Prüfer

- `scripts/manifest_guard.py`
- `scripts/evidence_guard.py`
- `scripts/documentation_guard.py`
- `scripts/release.py --check`
- `scripts/failure_matrix.py`
- `scripts/build_recovery_basis.py --check`
- `scripts/build_portable.py --check`
- `scripts/portable_smoke.py`

## 8. Evidenzgrenze

Die **Runtime-Baseline** 0.5.1 besitzt kanonische Release-Evidenz. `0.6.0-autostart-selfheal` ist im vorliegenden Tree `development / draft`; CI-Ergebnisse werden erst nach erfolgreichem Lauf in einen späteren Promotion-/Evidenzschritt überführt.

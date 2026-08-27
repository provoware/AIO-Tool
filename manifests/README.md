# Manifest-System — AIO-Tool

Dieses Verzeichnis trennt Runtime-Transport, Repository-Inhalt, Build-Recovery, lokale Laufzeitdaten und Release-Evidenz.

## Ebenen

| Ebene | Quelle | Bedeutung |
|---|---|---|
| Versions-/Statuswahrheit | `VERSION` + `VERSION_REGISTRY.json` | Aktuelle Produktversion und Statuspaar. |
| Runtime-Transport | `manifests/RUNTIME_MANIFEST.json` | Positive Allowlist aller transportierten Betriebsdateien. |
| Repository-Bestand | `manifests/DEVELOPMENT_MANIFEST.json` | Dokumentation, Tests, Evidenz, CI, Build-Helfer und lokale Entwicklungsdaten. |
| Build-Inventar | `MANIFEST_RELEASE.json` | Reproduzierbar erzeugte Datei-/Größen-/SHA256-Liste des Runtime-ZIPs. |
| Build-Recovery | `RECOVERY_BASIS.zip` | Hashgebundene Wiederherstellungsbasis exakt für die Runtime-Allowlist. |
| Release-Evidenz | `evidence/RELEASE_EVIDENCE_INDEX.json` + `evidence/releases/*.json` | Belegt ausschließlich TESTED-/höhere Stände. |

## Aktueller Vertrag 0.6.0

`0.6.0-autostart-selfheal` ist `development / draft`. Die zuletzt bereits bewiesene **Runtime-Baseline** bleibt `0.5.1-audit-modern-ui`. Development ist kein Beweisstatus und erhält deshalb noch keine vorweggenommene Release-Evidenz.

`RUNTIME_MANIFEST.json` steht in diesem Slice auf **2.0.0**. Es trennt:

1. `files` — feste positive Runtime-Allowlist,
2. `generated_files` — explizit nach Build/Start erzeugte Dateien wie `MANIFEST_RELEASE.json`, `RECOVERY_BASIS.zip`, Instanzmarker und `runtime/**`,
3. `forbidden_prefixes` — Bereiche, die niemals in das Runtime-ZIP gelangen dürfen,
4. `repo_only_root_files` — Root-Dateien für Entwicklung, Tests und Buildsystem.

## RECOVERY_BASIS

`scripts/build_recovery_basis.py` erzeugt `RECOVERY_BASIS.zip` deterministisch aus exakt derselben `files`-Allowlist. `RECOVERY_MANIFEST.json` enthält pro Datei Pfad, Größe und SHA256. Die Runtime-Recovery ist nur aktiv, wenn im gebauten Paket sowohl `MANIFEST_RELEASE.json` als auch `RECOVERY_BASIS.zip` vorhanden sind. Ein Source-Checkout wird dadurch nicht automatisch verändert.

## Development-Manifest 1.3.0

`DEVELOPMENT_MANIFEST.json` klassifiziert unter anderem:

- Status-/Policy-Dokumentation,
- Tests und Fixtures,
- `.github/` und CI,
- `requirements-ui.txt` und `requirements-build.txt`,
- Failure-Matrix, Recovery-, Portable- und Release-Builder,
- lokale `artifacts/`, `dist/`, `build/` und `runtime/`-Ausgaben.

## Atomare Prüfkette

Für 0.6.0 gilt verbindlich:

`Core-CI → Failure-Matrix → Source-ZIP → RECOVERY_BASIS → Portable-Build → Portable-Smoke → Chromium → Firefox`.

Alle Stufen müssen exakt denselben Commit prüfen. `git archive HEAD` bindet das Source-ZIP direkt an diesen Commit. Ein späteres PASS kann ein vorheriges FAIL nicht ersetzen.

## Begriffe

- **Runtime-Baseline:** letzter bereits bewiesener Programm-/Transportstand.
- **Repository-Head:** aktuellster Commit eines Branches.
- **Registry-Commit:** Commit, der einen Versionsdatensatz begründet.
- **Release-Evidenz:** Nachweis erst nach erfolgreicher Prüfkette eines beweisfähigen Status.

Diese Begriffe sind nicht austauschbar. Native L4 bleibt separat **OFFEN**, bis eine reale Zielsystembeobachtung vorliegt.

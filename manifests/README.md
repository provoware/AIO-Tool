# Manifest-System — AIO-Tool

Dieses Verzeichnis trennt Transport, Repository-Inhalt, Build-Inventar und Release-Evidenz.

## Ebenen

| Ebene | Quelle | Bedeutung |
|---|---|---|
| Runtime-Transport | `manifests/RUNTIME_MANIFEST.json` | Positive Allowlist der Betriebsdateien im Runtime-ZIP. |
| Repository-Bestand | `manifests/DEVELOPMENT_MANIFEST.json` | Klassifiziert Dokumentation, Tests, Evidenz, CI und lokale Entwicklungsdaten. |
| Build-Inventar | `MANIFEST_RELEASE.json` im ZIP | Wird reproduzierbar erzeugt und enthält Version, Status, Dateien, Größen und SHA256. |
| Release-Evidenz | `evidence/RELEASE_EVIDENCE_INDEX.json` und `evidence/releases/*.json` | Belegt Commit, CI, Browsermatrix und Artefakt-Hash eines geprüften Stands. |

## Begriffe

- **Runtime-Baseline:** eingefrorener Programm- und Transportstand einer bewiesenen Version.
- **Repository-Head:** neuester Commit eines Branches; er kann nach der Runtime-Baseline noch reine Repository-Metadaten enthalten.
- **Registry-Commit:** Commit, der den Versionsdatensatz in `VERSION_REGISTRY.json` begründet.
- **Main-Commit in Release-Evidenz:** geprüfter Runtime-/Produktstand nach Integration auf `main`.

Diese Begriffe sind nicht austauschbar.

## Grenze für 0.5.1

`0.5.1-audit-modern-ui` ist als Runtime-Baseline eingefroren. `RUNTIME_MANIFEST.json` Version `1.3.0` bleibt deshalb in dieser Repository-Metadaten-Härtung unverändert.

Das historische Feld `generated_files` in Runtime-Manifest 1.3.0 vereint zwei Bedeutungen: `MANIFEST_RELEASE.json` entsteht beim Build und wird in das ZIP aufgenommen; `web/.aio-instance-id` und `runtime/**` entstehen erst lokal nach dem Start und werden nicht transportiert. Der Manifest-Guard prüft diese Semantik explizit. Eine strukturelle Feldaufteilung ist erst in einer neuen Runtime-Version zulässig.

## Änderungsregel

Repo-only Änderungen dürfen die eingefrorene Runtime-Baseline nicht verändern. Änderungen an einer Runtime-Allowlist-Datei oder am Runtime-Manifest selbst benötigen dagegen eine neue `development`-Version und die vollständige L0–L3-Prüfkette.

Bei Widersprüchen gilt die Quellenhierarchie aus `AGENTS.md`; unklare Zustände bleiben OFFEN.

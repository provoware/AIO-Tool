# MANIFEST — AIO-Tool

## 1. Projektstatus

- **Produkt:** AIO-Tool
- **Runtime-Baseline:** `0.5.1-audit-modern-ui` — 🟢 `tested / draft`, **L0–L3 BEWIESEN**
- **Runtime-Baseline-Commit:** `ee6adcfd3427e8328920edaceb804e7b6655cdb8`
- **Runtime-ZIP:** `AIO-Tool-0.5.1-audit-modern-ui-TESTED.zip`
- **Runtime-SHA256:** `f8ffd88e2f3e40416f0d76b20786aa168cebb4e11fe3ef9d0eefa6dcf93b19ee`
- **Native L4:** 🟡 **OFFEN · 0/18 real bestätigt**
- **SAFE-FILE-Ausführung:** 🔒 **GESPERRT**
- **Backend:** Python-Standardbibliothek · Loopback-only
- **Telemetrie:** keine

Die maschinenlesbare kanonische Release-Evidenz liegt unter `evidence/releases/0.5.1-audit-modern-ui.json`.

## 2. Wahrheitsebenen

| Ebene | Kanonische Quelle | Aussage |
|---|---|---|
| Versions-/Releasezustand | `VERSION` + `VERSION_REGISTRY.json` | Produktversion und Statuspaar |
| Runtime-Transport | `manifests/RUNTIME_MANIFEST.json` | positive Allowlist des Runtime-ZIPs |
| Release-Beweis | `evidence/RELEASE_EVIDENCE_INDEX.json` + Einzeldatei | Commit, CI, Browsermatrix, Hash, offene L4-Gates |
| Repository-Bestand | `manifests/DEVELOPMENT_MANIFEST.json` | repo-only Doku-, Test-, Evidenz- und Entwicklungsbestand |
| Menschenlesbare Zusammenfassung | `MANIFEST.md` | komprimierte Sicht auf die obigen Quellen |

### Begriffsregel

- **Runtime-Baseline-Commit** = der bewiesene Programm-/Transportstand.
- **Repository-Head** = der neueste Commit eines Branches; er darf danach reine repo-only Metadaten enthalten.
- **Registry-Commit** = Commit, der den Versionsdatensatz begründet.

Diese drei Commit-Arten dürfen nicht als Synonyme verwendet werden.

## 3. Manifestfamilie

### `manifests/RUNTIME_MANIFEST.json`

- Manifest-Version: **`1.3.0`**
- Status für 0.5.1: **eingefroren**
- Aufgabe: positive Runtime-Allowlist plus Transportverbote
- Änderung daran würde den Runtime-ZIP-Hash verändern und benötigt deshalb eine **neue Produktversion**.

### `manifests/DEVELOPMENT_MANIFEST.json`

- Manifest-Version: **`1.2.0`**
- Scope: **repository-only**
- Aufgabe: Dokumentation, Tests, Release-Evidenz, CI-/Build-Hilfen, lokale Reports und Manifest-Policy klassifizieren.
- Definiert zusätzlich Statusdokumente, Evidenz-Zusammenfassungen, Authority-Matrix und Invarianten.

### `MANIFEST_RELEASE.json`

Wird vom Release-Builder reproduzierbar in das Runtime-ZIP erzeugt und enthält:

- Toolversion und Status,
- Runtime-Manifest-Version,
- Archivname,
- Dateizahl,
- Pfad, Größe und SHA256 jeder Runtime-Basisdatei.

### `manifests/README.md`

Erklärt die Rollen, Änderungsregeln und die bewusste Trennung zwischen Runtime-Baseline und Repository-Metadaten.

## 4. Bekannte historische Manifest-Semantik

Runtime-Manifest `1.3.0` verwendet noch das gemeinsame Feld `generated_files` für zwei Arten:

- `MANIFEST_RELEASE.json` — beim Build erzeugt und transportiert,
- `web/.aio-instance-id` sowie `runtime/**` — erst lokal nach dem Start erzeugt und **nicht** transportiert.

Diese Semantik wird durch `scripts/manifest_guard.py` explizit geprüft. Das Feld wird in 0.5.1 nicht nachträglich strukturell geändert, weil dadurch die eingefrorene Runtime-Baseline verändert würde. Eine Feldaufspaltung gehört in eine spätere neue Runtime-Version.

## 5. Runtime-Invarianten

1. Das Runtime-ZIP wird ausschließlich aus der positiven Allowlist plus generiertem `MANIFEST_RELEASE.json` gebaut.
2. Repo-only Dokumentation, Tests, Release-Evidenz und lokale Reports dürfen nicht in das Runtime-ZIP gelangen.
3. Eine repo-only Metadatenänderung darf den Runtime-SHA256 der eingefrorenen Baseline nicht verändern.
4. Statusdokumente dürfen keinen höheren Status behaupten als Registry + reale Evidenz.
5. Offene Native-L4-Schritte bleiben OFFEN; CI ersetzt keine reale Nutzerbeobachtung.
6. SAFE-FILE-Ausführung bleibt bis zu einem eigenen neuen Versionsslice gesperrt.

## 6. Automatische Konsistenzgates

- `scripts/manifest_guard.py` — Runtime-/Development-Manifest, Überschneidungen, Policy und Legacy-generated-files-Semantik.
- `scripts/evidence_guard.py` — Release-Evidenz, Commit-/CI-/Hash-Provenienz und Browsermatrix.
- `scripts/documentation_guard.py` — aktuelle Version, Status, kanonischer Runtime-Commit/SHA und L4-Grenze in Statusdokumenten.
- `scripts/release.py --check` — reproduzierbarer Build, Dateimengen- und Einzelhashprüfung.

## 7. Runtime-Beweis 0.5.1

- **Runtime-Baseline-Commit:** `ee6adcfd3427e8328920edaceb804e7b6655cdb8`
- **Main-CI:** `33048070879`
- **Runtime-SHA256:** `f8ffd88e2f3e40416f0d76b20786aa168cebb4e11fe3ef9d0eefa6dcf93b19ee`
- **GitHub-Artefakt-Wrapper-Digest:** `95238af6cae63091262fbaf2aea6ce267c71fd16eeefcebde56d97f3b482d71b`

Der finale Feature-Runtime-Head `3dec31d22110f738c9964b937a53ddfe251a4d79` und die Runtime-Baseline auf `main` erzeugen bytegleich denselben Runtime-SHA256.

Der frühere Promotion-Hash `a7ab6d64…` ist in der Release-Evidenz als abgelöstes Vorartefakt vermerkt und **nicht** der finale Runtime-Baseline-Hash.

## 8. Offene Gates

### Native L4 — OFFEN

- 18 manuelle Schritte vorhanden,
- 0 real bestätigt,
- Kubuntu, Anzeige, Tastatur sowie Firefox/Chromium 100–200 % real zu prüfen.

### SAFE-FILE-Ausführung — GESPERRT

Die Runtime enthält weiterhin nur die Simulation. Eine reale Ausführungsfähigkeit erfordert eine neue Version mit eigenem Recovery-/Execution-Nachweis.

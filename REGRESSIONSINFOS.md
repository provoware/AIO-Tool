# REGRESSIONSINFOS — AIO-Tool

## Grundsatz

**Bestätigter Fehler → reproduzierbarer Auslöser → minimaler Fix → Regressionstest → erneute Prüfung → Evidenz → Learning Memory bei strukturellem Fehler.**

Statussprache: **OFFEN / UMGESETZT / GEPRÜFT / BEWIESEN**.

## Historische Kernverträge REG-001 bis REG-044

Foundation-, Persistenz-, Versions-, TODO-, Fehlerhilfe-, Kalender- und Dashboard-Verträge bleiben verbindlich. Besonders relevant:

- REG-009/010 — Fremdhost/Fremd-Origin blockieren.
- REG-017 — sichtbares Ereignis braucht verständlichen Text.
- REG-024 — wiederkehrende sichtbare Texte zentral/versioniert.
- REG-029 — Reminder nach Quittierung nicht erneut ausliefern.
- REG-030 — lokale Zukunftszeit via `zoneinfo`/DST.
- REG-034 — Metadatenversionen nicht redundant hart codieren.
- REG-035/036/037 — Reminder erst nach tatsächlicher Sichtbarkeit + Nutzeraktion quittieren.
- REG-038 — Dashboard-Textschlüssel vollständig/versioniert.
- REG-039 — Kernbereiche des Dashboards dürfen nicht unbemerkt verschwinden.
- REG-040 — UI dupliziert keine Backend-Domänenlogik.
- REG-041 — Nutzertitel als Text, nicht HTML.
- REG-042 — Diagnose gibt keine unnötigen Nutzerdaten aus.
- REG-043 — Responsive-/A11y-Schutzmarker bleiben vorhanden.
- REG-044 — Monatsraster Montag bis Sonntag.

## UI-Acceptance / Transport / Integrität

### REG-045 — Statische UI-Prüfung meldet „grün“, obwohl Renderfehler existiert

- **Risiko:** Überlappung, Überbreite oder zu kleine Bedienelemente bleiben unentdeckt.
- **Vertrag:** echte Chromium-/Firefox-Geometrie + Interaktionen über definierte Viewports.
- **Evidenz:** `scripts/ui_acceptance_ci.py`, Screenshot-/JSON-Artefakt.
- **Status:** BEWIESEN für `0.4.2` in Run `33032999752`.

### REG-046 — 320-CSS-px-Reflow erzeugt horizontalen Overflow

- **Vertrag:** kein unzulässiger horizontaler Overflow; Hauptbereiche 12/12/12.
- **Gate:** Browser-Acceptance `wcag-reflow-320`.
- **Status:** BEWIESEN in Chromium + Firefox für `0.4.2`.

### REG-047 — wichtiges Bedienelement unter Mindestzielgröße

- **Auslöser:** Einstellungsbutton `⚙` war bei 320 px zu klein.
- **Vertrag:** interaktive Kernziele mindestens 44 CSS-px gemäß Projektvertrag.
- **Status:** BEWIESEN in Chromium + Firefox für `0.4.2`.

### REG-048 — Browser-Fixture startet nach Produkt-JavaScript

- **Risiko:** Testharness erzeugt falsche Bootfehler/Flakes.
- **Vertrag:** deterministische Fixtures vor `app.js`; Ready-Zustand messbar; Fehlerartefakt auch bei rotem Gate.
- **Status:** BEWIESEN für `0.4.2`.

### REG-049 — Repo-/Testdateien gelangen in Runtime-ZIP

- **Vertrag:** ausschließlich positive Allowlist aus `manifests/RUNTIME_MANIFEST.json` + generiertes Release-Manifest.
- **Test:** `ReleaseContractTests` + `scripts/release.py --check`.
- **Status:** GEPRÜFT im aktuellen 0.4.3-Slice, finale CI noch offen.

### REG-050 — Runtime-ZIP ist formal korrekt, aber nicht selbst startprüfbar

- **Risiko:** Launcher erwartet Repo-Datei, die absichtlich nicht transportiert wird.
- **Vertrag:** ZIP bauen → frisch entpacken → `scripts/runtime_preflight.py --quick` darin erfolgreich ausführen.
- **Test:** `test_built_runtime_zip_is_self_contained_and_preflightable`.
- **Status:** UMGESETZT; finale 0.4.3-CI ausstehend.

### REG-051 — Launcher übernimmt fremde/alte lokale Instanz durch HTTP 200

- **Risiko:** HTML/JS/API bzw. Nutzerdaten verschiedener Installation werden vermischt.
- **Vertrag:** Version + Loopback/Ready + konkrete Installationskennung müssen übereinstimmen.
- **Tests:** `LauncherProbeTests`, `test_launcher_verifies_instance_and_uses_safe_fallback_port`.
- **Status:** UMGESETZT; finale 0.4.3-CI ausstehend.

### REG-052 — fremd belegter Standardport führt zu falscher Wiederverwendung oder hartem Startfehler

- **Vertrag:** fremde Instanz nicht übernehmen; freien Loopback-Ausweichport suchen und Nutzer transparent informieren.
- **Test:** Launcher-Contract + Probe-Logik.
- **Status:** UMGESETZT.

### REG-053 — Launcher benötigt Repository-Vollprüfung zum normalen Runtime-Start

- **Vertrag:** normaler Start ruft `runtime_preflight.py`; `validate.py` bleibt Repo-only.
- **Test:** `test_runtime_start_does_not_require_repository_validator` + Release-End-to-End-Test.
- **Status:** UMGESETZT.

### REG-054 — Statusvokabular driftet zwischen Registry und Release-Builder

- **Auslöser:** unerreichbare Varianten wie `release_candidate`/`rc`/`blocked` im Builder gegenüber anderem Registryvokabular.
- **Vertrag:** eine kanonische Statussprache; zulässige Statuspaare zentral validieren; unknown = Fehler.
- **Tests:** `VersionRegistryTests` Statuspaar-/Blocked-/RC-Tests + `ReleaseContractTests`.
- **Status:** UMGESETZT.

### REG-055 — bewiesene Version wird nach TESTED weiter verändert

- **Risiko:** Evidenz verweist nicht mehr eindeutig auf denselben Produktstand.
- **Vertrag:** jeder Produktpatch nach TESTED/RC/RELEASED startet neue Version als development.
- **Nachweis:** `0.4.2` bleibt als evidenzgebundener Stand erhalten; aktueller Slice ist `0.4.3-integrity-hardening`.
- **Status:** UMGESETZT.

### REG-056 — Launcher-/Ereignislogs wachsen unbegrenzt

- **Vertrag:** lokale Launcherlogs werden ab definierter Größe rotiert; Release enthält keine Runtime-Logs.
- **Test:** Launcher-Contract prüft Rotationsvertrag; Runtime-Allowlist schließt `runtime/` aus.
- **Status:** UMGESETZT.

## Evidenzhistorie

- Foundation: Run `33020484403`.
- Core: Run `33022569880`.
- Robustness: Run `33025238585`.
- Calendar: Run `33026380907`.
- Dashboard V2: Main-Run `33027125428`.
- UI-Acceptance/TESTED `0.4.2`: Run `33032999752`, Core/Release + Chromium/Firefox SUCCESS.

## Aktueller 0.4.3-Gate

Noch **OFFEN** bis der finale Code-/Doku-Head vollständig geprüft wurde. Keine TESTED-Promotion vor:

1. Unit/Contract/Validation/Learning/Launcher/JS/Release grün,
2. frisch entpacktes Runtime-ZIP + Preflight grün,
3. Chromium + Firefox Acceptance grün,
4. Registry-Evidenz eingetragen,
5. Promotion-Commit erneut vollständig grün.

## Native Gates weiterhin offen

- Kubuntu-Klick-&-Start aus sauberem TESTED-ZIP.
- KDE-/DPI-Skalierung.
- 100/125/150/175/200 % Browserzoom.
- realer Tastatur-/Screenreader-Durchlauf.
- verschiedene reale Displaygrößen.

Diese Punkte dürfen nicht aus CI als bestanden abgeleitet werden.

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

### REG-045 — Statische UI-Prüfung übersieht Renderfehler
- **Vertrag:** echte Chromium-/Firefox-Geometrie + Interaktionen über definierte Viewports.
- **Status:** BEWIESEN seit `0.4.2`, erneut erfolgreich in Run `33034359454`.

### REG-046 — 320-CSS-px-Reflow erzeugt horizontalen Overflow
- **Vertrag:** kein unzulässiger horizontaler Overflow; Hauptbereiche 12/12/12.
- **Status:** BEWIESEN in Chromium + Firefox.

### REG-047 — wichtiges Bedienelement unter Mindestzielgröße
- **Vertrag:** interaktive Kernziele mindestens 44 CSS-px gemäß Projektvertrag.
- **Status:** BEWIESEN in Chromium + Firefox.

### REG-048 — Browser-Fixture startet nach Produkt-JavaScript
- **Vertrag:** deterministische Fixtures vor `app.js`; Ready-Zustand messbar; Fehlerartefakt auch bei rotem Gate.
- **Status:** BEWIESEN.

### REG-049 — Repo-/Testdateien gelangen in Runtime-ZIP
- **Vertrag:** positive Allowlist aus `manifests/RUNTIME_MANIFEST.json` + generiertes Release-Manifest.
- **Status:** BEWIESEN in Run `33034359454`.

### REG-050 — Runtime-ZIP ist formal korrekt, aber nicht selbst startprüfbar
- **Vertrag:** ZIP bauen → frisch entpacken → `scripts/runtime_preflight.py --quick` darin erfolgreich ausführen.
- **Test:** `test_built_runtime_zip_is_self_contained_and_preflightable`.
- **Status:** BEWIESEN in Run `33034359454`.

### REG-051 — Launcher übernimmt fremde/alte lokale Instanz durch HTTP 200
- **Vertrag:** Version + Loopback/Ready + konkrete Installationskennung müssen übereinstimmen.
- **Tests:** `LauncherProbeTests`, Launcher-Contract.
- **Status:** BEWIESEN durch automatisierte Probe-/Contracttests in Run `33034359454`; native Kubuntu-Praxisprüfung bleibt L4-offen.

### REG-052 — fremd belegter Standardport führt zu falscher Wiederverwendung oder hartem Startfehler
- **Vertrag:** fremde Instanz nicht übernehmen; freien Loopback-Ausweichport suchen und Nutzer transparent informieren.
- **Status:** GEPRÜFT automatisiert; native L4-Abnahme offen.

### REG-053 — Launcher benötigt Repository-Vollprüfung zum normalen Runtime-Start
- **Vertrag:** normaler Start ruft `runtime_preflight.py`; `validate.py` bleibt Repo-only.
- **Status:** BEWIESEN durch Runtime-ZIP-End-to-End-Test.

### REG-054 — Statusvokabular driftet zwischen Registry und Release-Builder
- **Vertrag:** eine kanonische Statussprache; zulässige Statuspaare zentral validieren; unknown = Fehler.
- **Status:** BEWIESEN durch Statuspaar-/Release-Regressionen.

### REG-055 — bewiesene Version wird nach TESTED weiter verändert
- **Vertrag:** jeder Produktpatch nach TESTED/RC/RELEASED startet neue Version als `development`.
- **Nachweis:** `0.4.2` blieb eingefroren; Integritätsänderungen wurden als `0.4.3` geführt.
- **Status:** BEWIESEN als Prozessvertrag.

### REG-056 — Launcher-/Ereignislogs wachsen unbegrenzt
- **Vertrag:** lokale Launcherlogs werden ab definierter Größe rotiert; Release enthält keine Runtime-Logs.
- **Status:** GEPRÜFT durch Launcher-Contract + Runtime-Allowlist.

## Evidenzhistorie

- Foundation: Run `33020484403`.
- Core: Run `33022569880`.
- Robustness: Run `33025238585`.
- Calendar: Run `33026380907`.
- Dashboard V2: Main-Run `33027125428`.
- UI-Acceptance/TESTED `0.4.2`: Run `33032999752`.
- **Integrity Hardening `0.4.3`: Run `33034359454` — Core/Release + Chromium/Firefox SUCCESS.**

## Aktueller 0.4.3-Status

`0.4.3-integrity-hardening` wurde nach grünem finalem Entwicklungshead auf **`tested / draft`** promoviert.

Der Promotion-Commit muss danach erneut dieselben Gates bestehen. Erst dieser zweite grüne Lauf beweist, dass auch die Status-/Dokumentationspromotion selbst keinen Drift eingeführt hat.

## Native L4-Gates weiterhin offen

- Kubuntu-Klick-&-Start aus sauberem TESTED-ZIP.
- KDE-/DPI-Skalierung.
- 100/125/150/175/200 % Browserzoom.
- realer Tastatur-/Screenreader-Durchlauf.
- verschiedene reale Displaygrößen.

Diese Punkte dürfen nicht aus CI als bestanden abgeleitet werden.

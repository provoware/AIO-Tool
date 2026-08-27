# REGRESSIONSINFOS — AIO-Tool

Grundsatz: **Fehler → reproduzierbarer Auslöser → kleinste Codezone → Fix → Regression → Evidenz → Learning Memory bei strukturellem Befund.**

Statussprache: **OFFEN / UMGESETZT / GEPRÜFT / BEWIESEN**.

Historische Verträge **REG-001 bis REG-066** bleiben verbindlich. Die Runtime-Baseline `0.5.1-audit-modern-ui` ist für L0–L3 BEWIESEN; Native L4 bleibt OFFEN.

## Repository-/Manifest-Härtung nach Runtime-Baseline 0.5.1

### REG-081 — Runtime-Baseline-Commit und Repository-Head werden verwechselt
- **Risiko:** Repo-only Dokumentationscommits nach einem Squash-Merge lassen die Formulierung „Main-Commit“ mehrdeutig werden.
- **Vertrag:** Statusdokumente verwenden **Runtime-Baseline-Commit** für den bewiesenen Programm-/Transportstand. `Repository-Head` und `Registry-Commit` sind davon getrennte Begriffe.
- **Schutz:** `AGENTS.md`, `manifests/README.md`, `MANIFEST.md`, evidenzgetriebener Documentation Guard.
- **Status:** **UMGESETZT** — Branch-Gate steht noch aus.

### REG-082 — manuell duplizierte CI-/Hashdaten erzeugen selbstreferenziellen Dokumentationsdrift
- **Risiko:** Ein Doku-Sync trägt „letzten CI-Lauf“ ein, erzeugt dadurch einen neuen Commit und einen neuen CI-Lauf und macht sich sofort wieder veraltet.
- **Vertrag:** Kanonische Produkt-/Runtime-Evidenz liegt in `evidence/releases/<version>.json`. Statusdokumente dürfen stabile Baseline-Fakten wiedergeben, aber keinen flüchtigen Repository-Head als neue Produktwahrheit behandeln.
- **Schutz:** `scripts/documentation_guard.py` prüft Runtime-Commit und Runtime-SHA direkt gegen die Release-Evidenz.
- **Status:** **UMGESETZT** — Branch-Gate steht noch aus.

### REG-083 — Runtime- und Development-Manifest klassifizieren dieselbe Datei widersprüchlich
- **Risiko:** Eine Datei wird gleichzeitig transportiert und als repo-only geführt; oder ein repo-only Root-Dokument fehlt im Development-Inventar.
- **Vertrag:** Runtime-Allowlist und Development-Klassifikation dürfen sich nicht überschneiden. Runtime-Manifest muss sich selbst transportieren, Development-Manifest bleibt repo-only.
- **Test:** `tests/test_manifest_guard.py`.
- **Schutz:** `scripts/manifest_guard.py` fail-closed.
- **Status:** **UMGESETZT** — Branch-Gate steht noch aus.

### REG-084 — historisches `generated_files`-Feld wird falsch interpretiert
- **Risiko:** Runtime-Manifest 1.3.0 listet Build-generiertes `MANIFEST_RELEASE.json` und erst nach Start entstehende lokale Dateien im selben Feld.
- **Vertrag für eingefrorene 0.5.1:** `MANIFEST_RELEASE.json` wird beim Build erzeugt und transportiert; `web/.aio-instance-id` und `runtime/**` entstehen lokal und werden nicht als feste Runtime-Basis transportiert.
- **Schutz:** `manifests/README.md` + Manifest Guard.
- **Status:** **UMGESETZT** — strukturelle Schemaaufspaltung erst in neuer Runtime-Version zulässig.

### REG-085 — Native-L4-Fortschritt wird ohne reale Bestätigung hochgerechnet
- **Risiko:** Implementierter Runner oder vorhandene CI wird fälschlich als Teilfortschritt der realen L4-Abnahme dargestellt.
- **Vertrag:** Solange kein manueller Runner-Schritt bestätigt ist, gilt **0/18 = 0 %**. `skip` ist kein PASS.
- **Schutz:** evidenzgetriebener Documentation Guard prüft bei offenen L4-Gates eine nicht aufgewertete README-Darstellung.
- **Status:** **UMGESETZT** — Branch-Gate steht noch aus.

## Runtime-Verträge — `0.5.1-audit-modern-ui`

### REG-067 — parallele HTTP-Schreibvorgänge verlieren Persistenzupdates
- Vertrag: `AtomicJsonStore.update()` hält einen gemeinsamen `RLock` über den vollständigen Read→Mutate→Write-Zyklus.
- Test: 120 parallele Inkremente müssen exakt 120 ergeben.
- Status: **BEWIESEN L0–L3 auf Runtime-Baseline**.

### REG-068 — Backup wird während Aktualisierung beschädigt
- Vertrag: auch `.bak` wird über temporäre Datei + fsync + `os.replace` erneuert; stale eigene Tempdatei wird entfernt.
- Status: **BEWIESEN L0–L3 auf Runtime-Baseline**.

### REG-069 — ConfigStore driftet vom allgemeinen Persistenzvertrag
- Vertrag: Konfiguration nutzt `AtomicJsonStore` statt eigener Kopie der Schreiblogik.
- Status: **BEWIESEN L0–L3 auf Runtime-Baseline**.

### REG-070 — Hauptbackend akzeptiert schwächeren Hostvertrag als Hilfsserver
- Vertrag: zentraler `app.loopback_security`-Vertrag; Host muss Loopback mit exakt passendem Port sein, Cross-Port-Origin wird blockiert.
- Status: **BEWIESEN L0–L3 auf Runtime-Baseline**.

### REG-071 — Kalender/Termine zeigen nach Ladefehler alte oder scheinbar leere Daten
- Vertrag: fehlgeschlagene Loads setzen den betroffenen State auf technisch nicht verfügbar; die UI zeigt weder Altwerte noch ein falsches „keine Daten“.
- Test: `test_failed_loads_do_not_reuse_stale_or_fake_empty_data`.
- Status: **BEWIESEN L0–L3 auf Runtime-Baseline**.

### REG-072 — alter TODO-Aktionsfehler hält Dashboard auf „teilweise“
- Vertrag: erfolgreicher Retry löscht `todo-action` vor Refresh.
- Status: **BEWIESEN L0–L3 auf Runtime-Baseline**.

### REG-073 — Oberfläche scheitert beim Boot ohne eindeutiges sichtbares Feedback
- Vertrag: Boot-Guard besitzt READY-/Hinweis-/ERROR-Pfade; Top-Level-Bootfehler wird abgefangen.
- Status: **BEWIESEN L0–L3 auf Runtime-Baseline**.

### REG-074 — Theme-/Modulzustand nur farblich erkennbar
- Vertrag: Auswahlbuttons synchronisieren `.selected` und `aria-pressed`; High Contrast bleibt eigener harter Modus.
- Status: **BEWIESEN L0–L3 auf Runtime-Baseline**.

### REG-075 — Helper-UIs benötigen Inline-CSS/DOM-innerHTML
- Vertrag: gemeinsames `web/helper-ui.css`, CSP `style-src 'self'`, keine Inline-Styles und keine dynamische `innerHTML`-Erzeugung.
- Status: **BEWIESEN L0–L3 auf Runtime-Baseline**.

### REG-076 — Browser-Acceptance driftet vom Produkt-Assetvertrag
- Auslöser: fest codierte alte Contract-Assets plus zweite nahezu vollständige Harness-Implementierung im CI-Entry-Point.
- Vertrag: **eine kanonische Harness-Implementierung** in `scripts/ui_acceptance.py`; lokale Stylesheets aus dem aktuellen `index.html`; Fixture-Skript vor Produkt-JavaScript; `ui_acceptance_ci.py` bleibt dünner Wrapper.
- Test: `tests/test_ui_acceptance_harness.py`.
- Status: **BEWIESEN L0–L3 auf Runtime-Baseline**.

### REG-077 — mehrfaches „Neu prüfen“ oder Theme-Klicken erzeugt konkurrierende UI-Aktionen
- Vertrag: Refresh und Config-Speichern laufen single-flight; konkurrierende Controls werden gesperrt und mit `aria-busy` markiert.
- Status: **BEWIESEN L0–L3 auf Runtime-Baseline**.

### REG-078 — lokales Backend antwortet nicht und Oberfläche bleibt unbegrenzt in Zwischenzustand
- Vertrag: API-Anfragen besitzen einen begrenzten 8-Sekunden-Timeout und verständliche Fehlerhilfe.
- Status: **BEWIESEN L0–L3 auf Runtime-Baseline**.

### REG-079 — fehlgeschlagene TODO-/Ereignis-/Terminabfrage wird wie „keine Daten vorhanden“ dargestellt
- Vertrag: `null` bedeutet technisch **nicht verfügbar**; `[]` bedeutet erfolgreich geladen und leer.
- Status: **BEWIESEN L0–L3 auf Runtime-Baseline**.

### REG-080 — Theme-Vorschau bleibt nach gescheitertem Speichern optisch aktiv
- Vertrag: Vorschau muss bei Config-Fehler auf die vorherige bestätigte Konfiguration zurückrollen.
- Status: **BEWIESEN L0–L3 auf Runtime-Baseline**.

## Kanonische Evidenz 0.5.1

Quelle: `evidence/releases/0.5.1-audit-modern-ui.json`.

- Runtime-Baseline-Commit: `ee6adcfd3427e8328920edaceb804e7b6655cdb8`.
- Main-CI: `33048070879`.
- Runtime-ZIP SHA256: `f8ffd88e2f3e40416f0d76b20786aa168cebb4e11fe3ef9d0eefa6dcf93b19ee`.
- Main-Artefakt-Wrapper-Digest: `95238af6cae63091262fbaf2aea6ce267c71fd16eeefcebde56d97f3b482d71b`.
- finaler Feature-Runtime-Head und Runtime-Baseline erzeugen identischen ZIP-SHA256.
- früherer Promotion-Hash `a7ab6d64…` ist als abgelöstes Vorartefakt dokumentiert.

## Aktuelle Evidenzgrenze

- Runtime-Baseline `0.5.1-audit-modern-ui`: **BEWIESEN L0–L3**.
- Native Kubuntu L4: **OFFEN · 0/18 real bestätigt**.
- SAFE-FILE reale Ausführung: **GESPERRT**.

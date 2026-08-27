# REGRESSIONSINFOS — AIO-Tool

Grundsatz: **Fehler → reproduzierbarer Auslöser → kleinste Codezone → Fix → Regression → Evidenz → Learning Memory bei strukturellem Befund.**

Statussprache: OFFEN / UMGESETZT / GEPRÜFT / BEWIESEN.

Historische Verträge **REG-001 bis REG-066** bleiben verbindlich.

## Neue Verträge — `0.5.1-audit-modern-ui`

### REG-067 — parallele HTTP-Schreibvorgänge verlieren Persistenzupdates
- Vertrag: `AtomicJsonStore.update()` hält einen gemeinsamen `RLock` über den vollständigen Read→Mutate→Write-Zyklus.
- Test: 120 parallele Inkremente müssen exakt 120 ergeben.
- Status: **BEWIESEN L0–L3 auf main**.

### REG-068 — Backup wird während Aktualisierung beschädigt
- Vertrag: auch `.bak` wird über temporäre Datei + fsync + `os.replace` erneuert; stale eigene Tempdatei wird entfernt.
- Status: **BEWIESEN L0–L3 auf main**.

### REG-069 — ConfigStore driftet vom allgemeinen Persistenzvertrag
- Vertrag: Konfiguration nutzt `AtomicJsonStore` statt eigener Kopie der Schreiblogik.
- Status: **BEWIESEN L0–L3 auf main**.

### REG-070 — Hauptbackend akzeptiert schwächeren Hostvertrag als Hilfsserver
- Vertrag: zentraler `app.loopback_security`-Vertrag; Host muss Loopback mit exakt passendem Port sein, Cross-Port-Origin wird blockiert.
- Status: **BEWIESEN L0–L3 auf main**.

### REG-071 — Kalender/Termine zeigen nach Ladefehler alte oder scheinbar leere Daten
- Vertrag: fehlgeschlagene Loads setzen den betroffenen State auf technisch nicht verfügbar; die UI zeigt weder Altwerte noch ein falsches „keine Daten“.
- Test: `test_failed_loads_do_not_reuse_stale_or_fake_empty_data`.
- Status: **BEWIESEN L0–L3 auf main**.

### REG-072 — alter TODO-Aktionsfehler hält Dashboard auf „teilweise“
- Vertrag: erfolgreicher Retry löscht `todo-action` vor Refresh.
- Status: **BEWIESEN L0–L3 auf main**.

### REG-073 — Oberfläche scheitert beim Boot ohne eindeutiges sichtbares Feedback
- Vertrag: Boot-Guard besitzt READY-/Hinweis-/ERROR-Pfade; Top-Level-Bootfehler wird abgefangen.
- Status: **BEWIESEN L0–L3 auf main**.

### REG-074 — Theme-/Modulzustand nur farblich erkennbar
- Vertrag: Auswahlbuttons synchronisieren `.selected` und `aria-pressed`; High Contrast bleibt eigener harter Modus.
- Status: **BEWIESEN L0–L3 auf main**.

### REG-075 — Helper-UIs benötigen Inline-CSS/DOM-innerHTML
- Vertrag: gemeinsames `web/helper-ui.css`, CSP `style-src 'self'`, keine Inline-Styles und keine dynamische `innerHTML`-Erzeugung.
- Status: **BEWIESEN L0–L3 auf main**.

### REG-076 — Browser-Acceptance driftet vom Produkt-Assetvertrag
- Auslöser: fest codierte alte Contract-Assets plus zweite nahezu vollständige Harness-Implementierung im CI-Entry-Point.
- Vertrag: **eine kanonische Harness-Implementierung** in `scripts/ui_acceptance.py`; lokale Stylesheets aus dem aktuellen `index.html`; Fixture-Skript vor Produkt-JavaScript; `ui_acceptance_ci.py` bleibt dünner Wrapper.
- Test: `tests/test_ui_acceptance_harness.py`.
- Status: **BEWIESEN L0–L3 auf main**.

### REG-077 — mehrfaches „Neu prüfen“ oder Theme-Klicken erzeugt konkurrierende UI-Aktionen
- Vertrag: Refresh und Config-Speichern laufen single-flight; konkurrierende Controls werden gesperrt und mit `aria-busy` markiert.
- Status: **BEWIESEN L0–L3 auf main**.

### REG-078 — lokales Backend antwortet nicht und Oberfläche bleibt unbegrenzt in Zwischenzustand
- Vertrag: API-Anfragen besitzen einen begrenzten 8-Sekunden-Timeout und verständliche Fehlerhilfe.
- Status: **BEWIESEN L0–L3 auf main**.

### REG-079 — fehlgeschlagene TODO-/Ereignis-/Terminabfrage wird wie „keine Daten vorhanden“ dargestellt
- Vertrag: `null` bedeutet technisch **nicht verfügbar**; `[]` bedeutet erfolgreich geladen und leer.
- Status: **BEWIESEN L0–L3 auf main**.

### REG-080 — Theme-Vorschau bleibt nach gescheitertem Speichern optisch aktiv
- Vertrag: Vorschau muss bei Config-Fehler auf die vorherige bestätigte Konfiguration zurückrollen.
- Status: **BEWIESEN L0–L3 auf main**.

## Evidenz 0.5.1

- DEV-Gate `33045348341` — SUCCESS.
- TESTED-Promotion `33045669222` — 138 Tests, Guards, Runtime-ZIP + Chromium + Firefox + Helper-UIs SUCCESS.
- finaler Evidence-Sync `33047743876` — SUCCESS.
- PR-Integrationsgate `33047885115` — SUCCESS.
- Squash-Main-Commit `ee6adcfd3427e8328920edaceb804e7b6655cdb8`.
- Main-CI `33048070879` — Core/Release + Chromium + Firefox + Helper-UIs SUCCESS.
- finaler Runtime-ZIP SHA256: `f8ffd88e2f3e40416f0d76b20786aa168cebb4e11fe3ef9d0eefa6dcf93b19ee`.
- Main-Artefakt-Wrapper-Digest: `95238af6cae63091262fbaf2aea6ce267c71fd16eeefcebde56d97f3b482d71b`.

Der finale Feature-Head und der Squash-Main-Commit erzeugen identisch `f8ffd88e…`. Der ältere Promotion-Hash `a7ab6d64…` gehört zum Stand vor dem abschließenden Runtime-Metadaten-Sync der `VERSION_REGISTRY.json` und ist nicht der finale Main-Artefakthash.

## Aktuelle Evidenzgrenze

- `0.5.1-audit-modern-ui`: **BEWIESEN L0–L3 auf main**.
- Native Kubuntu L4: **OFFEN**, ausschließlich durch reale Nutzerprüfung erfüllbar.
- SAFE-FILE echte Mutation: **GESPERRT**.

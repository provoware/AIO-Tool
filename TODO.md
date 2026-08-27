# TODO — AIO-Tool

## Aktueller Slice

- **Version:** `0.6.0-autostart-selfheal`
- **Status:** `development / draft`
- **Runtime-Baseline:** `0.5.1-audit-modern-ui` bleibt der letzte bereits bewiesene L0–L3-Stand.
- **Native Kubuntu L4:** 🟡 **OFFEN · 0 % automatisch aufgewertet**
- **SAFE-FILE-Ausführung:** 🔒 **GESPERRT**

## Atomarer Abschluss 0.6.0

- [x] autonome Startroutine vorbereiten.
- [x] Self-Healing für lokale JSON-Zustände mit Quarantäne vorbereiten.
- [x] Runtime-Recovery aus hashgebundener `RECOVERY_BASIS.zip` vorbereiten.
- [x] Read-only-Spiegelung in benutzereigenen Bereich vorbereiten.
- [x] Portable Linux x86_64 Entry-Point und gepinnten Build-Stack vorbereiten.
- [x] Failure-Matrix und Recovery-Builder ergänzen.
- [x] Portable-Builder und Portable-Smoke ergänzen.
- [x] Self-Heal-/Recovery-/Pipeline-Regressionstests ergänzen.
- [x] Status-/Technikdokumentation auf `0.6.0-autostart-selfheal` synchronisieren.
- [x] achtstufigen GitHub-Actions-Vertrag definieren.
- [ ] **einen** Commit direkt auf der vorgesehenen Basis erzeugen.
- [ ] Feature-Branch exakt auf diesen Commit setzen.
- [ ] `01 Core-CI` grün.
- [ ] `02 Failure-Matrix` grün.
- [ ] `03 Source-ZIP` erzeugt und hochgeladen.
- [ ] `04 RECOVERY_BASIS` erzeugt und geprüft.
- [ ] `05 Portable-Build` erzeugt und geprüft.
- [ ] `06 Portable-Smoke` normal + Read-only-Spiegelung grün.
- [ ] `07 Chromium` strict grün.
- [ ] `08 Firefox` strict grün.

## Gate-Regel

Ein späteres Gate darf ein früheres nicht ersetzen oder überspringen. Bei einem Fehler stoppt die Kette. Keine Statuspromotion auf `tested`, bevor der vollständige Lauf für exakt denselben Commit erfolgreich ist.

## Danach

1. CI-Artefakte und Hashes in die Release-Evidenz übernehmen.
2. `VERSION_REGISTRY.json` erst dann auf einen bewiesenen Status heben.
3. Native Kubuntu L4 weiterhin separat real beobachten; CI setzt L4 niemals automatisch auf PASS.
4. SAFE-FILE-Ausführung bleibt bis zu einem eigenen Execution-/Undo-/Recovery-Slice gesperrt.

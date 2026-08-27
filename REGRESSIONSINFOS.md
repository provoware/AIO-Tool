# REGRESSIONSINFOS — AIO-Tool

Grundsatz: **Fehler → reproduzierbarer Auslöser → kleinste Codezone → Fix → Regression → Evidenz → Learning Memory bei strukturellem Befund.**

Statussprache: OFFEN / UMGESETZT / GEPRÜFT / BEWIESEN.

Historische Verträge REG-001 bis REG-056 bleiben verbindlich.

## 0.5.0-native-acceptance-safe-file-sim

DEV-Head `6cf6754dcf5da88edb13ee34f2e99b4e22bca593`, Run `33038051967`: **113/113 Tests + L0–L3 vollständig grün**.

### REG-057 — L4-Schritt wird ohne reale Prüfung automatisch PASS
Vertrag: 18 Schritte starten OFFEN; nur explizites PASS/FAIL/SKIP. Test: `NativeAcceptanceTests.test_no_step_is_auto_passed_and_reports_are_persistent`. **BEWIESEN.**

### REG-058 — Firefox-/Chromium-Abnahme trennt dieselbe Sitzung
Vertrag: gemeinsamer versionsgebundener AtomicJsonStore; Firefox sieht die zuvor in Chromium gespeicherte Bewertung. Zusätzlicher echter Browser-Gate: `scripts/aux_ui_acceptance.py`. **BEWIESEN.**

### REG-059 — TESTED-Version fehlt/doppelt im Evidenzindex
Vertrag: exakt eine Datei pro TESTED/RC/RELEASED-Version; Masterindex = Registry-Menge. Gate: Evidence Guard + Tests. **BEWIESEN.**

### REG-060 — historischer Artefakthash wird geraten
Vertrag: nicht belegter Wert = `status:not-recorded`, `sha256:null`. Evidence Guard blockiert Widerspruch. **BEWIESEN.**

### REG-061 — SAFE-FILE-Simulation besitzt echte Copy-Ausführung
Vertrag: kein `/api/execute`, keine Copy-/Move-/Delete-Primitive, `EXECUTION_ENABLED=False`. Statischer Capability-Test + Runtime-Gate. **BEWIESEN.**

### REG-062 — Preview behauptet Mutation/Ausführung
Vertrag: `validate_preview_contract()` verlangt `simulation_only=true`, `execution_enabled=false`, `mutation_performed=false`; positive Vorlage + Negativfixture. **BEWIESEN.**

### REG-063 — SAFE-FILE-Fehlerfall bleibt unentdeckt
Vertrag: SF-001..010 mit Tests für missing/not-file/symlink/target/permissions/space/conflict/same-target. **BEWIESEN für die Simulation.**

### REG-064 — spätere Copy ohne Recovery-/Nachvalidierungsvertrag
Vertrag ist in der Simulation festgeschrieben: Journal vor Mutation, Postvalidation vor DONE, Undo nur bei unverändertem Ziel. **BEWIESEN als Vorvertrag; echte Copy bleibt gesperrt.**

### REG-065 — lokaler Hilfsserver akzeptiert anderen Loopback-Port
Vertrag: Host und Origin müssen Loopback **und exakt denselben Port** verwenden. `LoopbackSecurityTests`. **BEWIESEN.**

### REG-066 — neue Runtime-Assistenten fehlen im ZIP
Vertrag: Runtime-Manifest 1.2.1 + Release-End-to-End-Test + frischer Runtime-Preflight aus dem ZIP. **BEWIESEN.**

## Evidenzstatus

- `0.4.3-integrity-hardening`: BEWIESEN, Main-CI `33036217621`.
- `0.5.0-native-acceptance-safe-file-sim`: L0–L3 **BEWIESEN auf DEV-Head** durch Run `33038051967`; Registry zu TESTED promoviert. Promotion-Commit wird nochmals vollständig geprüft.
- L4 bleibt ausdrücklich **OFFEN**, bis der Native Acceptance Runner auf echtem Kubuntu ausgeführt wurde.
- echte SAFE-FILE Copy bleibt **NICHT IMPLEMENTIERT / GESPERRT**.

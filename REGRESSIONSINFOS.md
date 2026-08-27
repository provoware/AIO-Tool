# REGRESSIONSINFOS — AIO-Tool

Grundsatz: **Fehler → reproduzierbarer Auslöser → kleinste Codezone → Fix → Regression → Evidenz → Learning Memory bei strukturellem Befund.**

Statussprache: OFFEN / UMGESETZT / GEPRÜFT / BEWIESEN.

Historische Verträge REG-001 bis REG-056 bleiben verbindlich.

## Neue Verträge 0.5.0-native-acceptance-safe-file-sim

### REG-057 — L4-Schritt wird ohne reale Prüfung automatisch PASS

- Risiko: CI-/Browsererfolg wird fälschlich als native Kubuntu-Evidenz ausgegeben.
- Vertrag: alle 18 Runner-Schritte starten OFFEN; nur explizites PASS/FAIL/SKIP erzeugt ein Ergebnis.
- Test: `NativeAcceptanceTests.test_no_step_is_auto_passed_and_reports_are_persistent`.
- Status: UMGESETZT.

### REG-058 — Firefox- und Chromium-Abnahme landen in getrennten, nicht zusammenführbaren Zuständen

- Vertrag: beide Browser verwenden denselben lokalen Runner/AtomicJsonStore; Sitzung ist versionsgebunden und persistent.
- Test: Native-Acceptance-Store-/Reporttests.
- Status: UMGESETZT.

### REG-059 — TESTED-Version fehlt im Evidenzindex oder besitzt doppelte Evidenz

- Vertrag: exakt eine Datei pro TESTED/RC/RELEASED-Version; Masterindex muss mengenidentisch zur Registry sein.
- Gate: `scripts/evidence_guard.py` + `ReleaseEvidenceIndexTests`.
- Status: UMGESETZT.

### REG-060 — historischer Artefakthash wird aus Vermutung ergänzt

- Vertrag: nicht belegter historischer Hash = `status:not-recorded`, `sha256:null`.
- Gate: Evidence Guard lehnt widersprüchliche Hashzustände ab.
- Status: UMGESETZT.

### REG-061 — SAFE-FILE-Simulation besitzt versehentlich echte Copy-Ausführung

- Vertrag: kein `/api/execute`, keine Copy-/Move-/Delete-Primitive, `EXECUTION_ENABLED=False`.
- Test: `SafeFileSimulatorContractTests.test_simulator_exposes_no_execution_endpoint_or_copy_primitive`.
- Status: UMGESETZT.

### REG-062 — Preview behauptet Mutation oder freigeschaltete Ausführung

- Vertrag: `validate_preview_contract()` verlangt `simulation_only=true`, `execution_enabled=false`, `mutation_performed=false`.
- Test: positive Vorlage + absichtlich ungültige Fixture.
- Status: UMGESETZT.

### REG-063 — SAFE-FILE-Fehlerfall wird nicht vor einer späteren Copy erkannt

- Vertrag: Failure-Matrix SF-001..010 und direkte Tests für missing/not-file/symlink/target/permissions/space/conflict/same-target.
- Status: UMGESETZT; finale CI ausstehend.

### REG-064 — spätere Copy meldet DONE ohne Recovery-/Nachvalidierungsvertrag

- Vertrag bereits in Simulation festgeschrieben: persistentes Journal vor Mutation, Postvalidation vor DONE, Undo nur bei unverändertem Ziel.
- Test: `test_recovery_contract_requires_future_journal_postvalidation_and_guarded_undo`.
- Status: UMGESETZT; echte Copy weiterhin gesperrt.

### REG-065 — lokaler Hilfsserver akzeptiert Origin von anderem Loopback-Port

- Risiko: andere lokale Webseite könnte Aktionen am Runner/Simulator auslösen.
- Vertrag: Host und Origin müssen Loopback **und exakt denselben Port** verwenden.
- Test: `LoopbackSecurityTests`.
- Status: UMGESETZT.

### REG-066 — neue Runtime-Assistenten fehlen im Release-ZIP

- Vertrag: Runtime-Manifest 1.2.1 enthält Module, Starter, Webdateien und benötigte Vorlagen; Release-End-to-End-Test bleibt verbindlich.
- Status: UMGESETZT; finale L2-CI ausstehend.

## Evidenzstatus

`0.4.3-integrity-hardening`: BEWIESEN, u. a. Main-CI `33036217621`.

`0.5.0-native-acceptance-safe-file-sim`: aktuell **UMGESETZT / DEVELOPMENT**. Keine TESTED-Promotion vor grünen L0–L3-Gates. L4 bleibt anschließend ein realer, durch den Runner geführter separater Nachweis.

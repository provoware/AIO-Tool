# TOOLBESCHREIBUNG — AIO-Tool

## Aktueller Stand

`0.5.0-native-acceptance-safe-file-sim` — 🟢 **TESTED / draft für automatisierte L0–L3-Gates**. Die reale Kubuntu-Abnahme L4 bleibt offen. SAFE-FILE-Ausführung bleibt technisch gesperrt.

AIO-Tool ist ein lokales, offline-first ausgelegtes Werkzeug mit Browseroberfläche und Python-Loopback-Backend. Dieser Stand ergänzt zwei bewusst getrennte Qualitäts-/Sicherheitswerkzeuge.

## Native Acceptance Runner

Zweck: die Lücke zwischen automatisierter L3-Browser-CI und realem Kubuntu-Zielsystem schließen.

- 18 geführte Prüfschritte,
- Kubuntu-Start-/Instanz-/Portfälle,
- kleine/Full-HD/große Darstellung,
- Tastatur-only,
- Firefox und Chrome/Chromium jeweils 100/125/150/175/200 %,
- persistente gemeinsame Sitzung,
- explizites PASS/FAIL/SKIP,
- automatische JSON-/TXT-Berichte,
- keine automatische Hochstufung offener Schritte.

Der Runner selbst wurde automatisiert in Chromium und Firefox geprüft. **Seine späteren PASS/FAIL-L4-Ergebnisse können nur auf einem echten Kubuntu-System entstehen.**

## Release Evidence Index

Zweck: TESTED-Evidenz nicht über README, Chatberichte und CI-Seiten verteilen.

- Masterindex: `evidence/RELEASE_EVIDENCE_INDEX.json`.
- je TESTED-/höherer Version genau eine Datei unter `evidence/releases/`.
- Inhalte: Commits, CI-Runs, Artefakthashstatus, Browsermatrix, offene L4-Gates.
- CI-Guard prüft Mengen-/Commit-/Hash-/Browserkonsistenz gegen `VERSION_REGISTRY.json`.
- historische Lücken werden als `not-recorded` festgehalten.

## SAFE-FILE Core V0 — Simulation

Zweck: den vollständigen sicheren Copy-Entscheidungsweg entwickeln, **bevor** die erste Datei verändert werden darf.

Workflow:

`Quelle auswählen → Ziel auswählen → Vorprüfen → Konfliktoption → Vorschau → Failure-/Recovery-Auswertung`

Technische Sperren:

- `SIMULATION_ONLY=True`
- `EXECUTION_ENABLED=False`
- kein Execute-Endpunkt
- keine Copy-/Move-/Delete-Primitive
- `mutation_performed=false`

Die Simulation, Failure-Matrix und Sicherheitsverträge wurden automatisiert geprüft. Das ist **keine Freigabe echter Copy**. Eine spätere reale Copy benötigt einen neuen evidenzgebundenen Versionsslice mit persistentem Journal, Staging, Postvalidation, Crash-/Recoverytests und sicherem Undo.

## Automatisierte Evidenz

DEV-Head `6cf6754dcf5da88edb13ee34f2e99b4e22bca593`, GitHub Actions Run `33038051967`: 113 Tests, Evidence/Documentation/Runtime-Gates sowie Dashboard, Native Runner und SAFE-FILE-Simulation in Chromium+Firefox erfolgreich.

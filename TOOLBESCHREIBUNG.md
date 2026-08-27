# TOOLBESCHREIBUNG — AIO-Tool

## Aktueller Entwicklungsstand

`0.5.0-native-acceptance-safe-file-sim` — 🟠 DEVELOPMENT / DEV.

AIO-Tool ist ein lokales, offline-first ausgelegtes Werkzeug mit Browseroberfläche und Python-Loopback-Backend. Der neue Slice ergänzt zwei bewusst getrennte Qualitäts-/Sicherheitswerkzeuge.

## Native Acceptance Runner

Zweck: Die Lücke zwischen automatisierter L3-Browser-CI und realem Kubuntu-Zielsystem schließen.

Eigenschaften:

- 18 geführte Prüfschritte,
- Kubuntu-Start-/Instanz-/Portfälle,
- kleine/Full-HD/große Darstellung,
- Tastatur-only,
- Firefox und Chrome/Chromium jeweils 100/125/150/175/200 %,
- persistente gemeinsame Sitzung,
- explizites PASS/FAIL/SKIP,
- automatische JSON-/TXT-Berichte,
- keine automatische Hochstufung offener Schritte.

## Release Evidence Index

Zweck: TESTED-Evidenz nicht über README, Chatberichte und CI-Seiten verteilen.

- Masterindex: `evidence/RELEASE_EVIDENCE_INDEX.json`.
- je TESTED-/höherer Version eine eigene Datei unter `evidence/releases/`.
- Inhalte: Commits, CI-Runs, Artefakthashstatus, Browsermatrix, offene L4-Gates.
- CI-Guard prüft Mengen-/Commit-/Hash-/Browserkonsistenz gegen `VERSION_REGISTRY.json`.
- historische Lücken werden als `not-recorded` festgehalten.

## SAFE-FILE Core V0 — Simulation

Zweck: den vollständigen sicheren Copy-Entscheidungsweg entwickeln, **bevor** die erste Datei verändert werden darf.

Workflow:

`Quelle auswählen → Ziel auswählen → Vorprüfen → Konfliktoption → Vorschau → Failure-/Recovery-Auswertung`

Aktuelle technische Sperren:

- `SIMULATION_ONLY=True`
- `EXECUTION_ENABLED=False`
- kein Execute-Endpunkt
- keine Copy-/Move-/Delete-Primitive
- kein Schreibjournal nötig, weil noch keine Mutation existiert

Spätere echte Copy benötigt einen neuen evidenzgebundenen Versionsslice mit persistentem Journal, Staging, Postvalidation, Crash-/Recoverytests und sicherem Undo.

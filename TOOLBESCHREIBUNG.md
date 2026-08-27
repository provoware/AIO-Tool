# TOOLBESCHREIBUNG — AIO-Tool

## Aktueller Stand

`0.5.1-audit-modern-ui` — 🟢 **TESTED / draft und BEWIESEN für L0–L3 auf `main`**. Squash-Main-Commit: `ee6adcfd3427e8328920edaceb804e7b6655cdb8`; Main-CI `33048070879` ist vollständig grün. Native Kubuntu L4 bleibt offen; SAFE-FILE-Ausführung bleibt technisch gesperrt.

AIO-Tool ist ein lokales, offline-first ausgelegtes Werkzeug mit Browseroberfläche und Python-Loopback-Backend. Der 0.5.1-Slice verbessert **Robustheit, Wartbarkeit, Nutzerfeedback und Erscheinungsbild**, ohne SAFE-FILE-Mutation freizuschalten.

## Audit-Schwerpunkte

### Persistenz

`AtomicJsonStore` serialisiert parallele Threadzugriffe und behandelt Read→Mutate→Write als zusammenhängenden In-Process-Vertrag. Backup-Refresh und Hauptdatei werden atomar ersetzt. `ConfigStore` nutzt denselben Kern statt einer zweiten Schreibimplementierung.

### Lokale Sicherheit

Hauptbackend, Native Runner und SAFE-FILE Simulator verwenden denselben exakten Loopback-Host-/Port-Vertrag. Eine Anfrage auf falschem Port oder fremdem Host gilt nicht als vertrauenswürdig.

### Dashboard-Zustand und Nutzerfeedback

- fehlgeschlagene Kalender-/Upcoming-/TODO-/Ereignisabfragen werden als **nicht verfügbar** statt scheinbar leer dargestellt,
- erfolgreiche Wiederholungen löschen alte Aktionsfehler,
- der Boot-Guard zeigt Start, READY, Hinweise oder einen klaren Fehlerzustand,
- Refresh und Config-Speichern laufen single-flight mit `aria-busy`,
- lokale API-Anfragen besitzen einen 8-Sekunden-Timeout mit verständlicher Hilfe,
- Theme-Vorschau wird bei Speicherfehler auf den bestätigten Stand zurückgesetzt.

### Modernes Theme-System

Fünf Themes nutzen denselben semantischen Tokenvertrag: Aurora Glass, Steel Night, Trash Neon, Clean Light und High Contrast. Oberflächenebenen, Akzent, Fokus, Status, Schatten und Kontrast sind getrennt definiert. Bewegungsreduktion (`prefers-reduced-motion`) wird respektiert.

### Browser-Acceptance und Wartbarkeit

`scripts/ui_acceptance.py` ist die einzige kanonische Browser-Acceptance-Implementierung. `scripts/ui_acceptance_ci.py` ist nur ein dünner Einstieg. Lokale Produktstyles werden aus dem aktuellen `index.html` abgeleitet statt Contract-Versionen an mehreren Stellen zu duplizieren. Regressionstests verhindern eine zweite Harness-Implementierung.

### Hilfsoberflächen

Native Acceptance Runner und SAFE-FILE Simulator verwenden ein gemeinsames `web/helper-ui.css`. Inline-Styles wurden entfernt, die lokale CSP auf `style-src 'self'` verschärft und dynamische Inhalte werden mit DOM-/`textContent`-Methoden statt `innerHTML` erzeugt.

## SAFE-FILE-Grenze

Weiterhin unverändert:

- `SIMULATION_ONLY=True`
- `EXECUTION_ENABLED=False`
- kein Execute-Endpunkt
- keine Copy-/Move-/Delete-Primitive

Eine spätere echte Copy benötigt einen eigenen neuen Versionsslice mit Journal, Staging, Postvalidation, Crash-/Recoverytests und Guarded Undo.

## Qualitätsstatus und Beweiskette

- DEV `33045348341`: PASS.
- TESTED-Promotion `33045669222`: 138/138 Tests + Guards + Runtime-Preflight + Chromium/Firefox + Helper-UIs PASS.
- finaler Evidence-Sync `33047743876`: PASS.
- PR-Integrationsgate `33047885115`: PASS.
- Squash-Main-Commit `ee6adcfd3427e8328920edaceb804e7b6655cdb8`.
- Main-CI `33048070879`: Core/Release + Chromium + Firefox + Native Runner + SAFE-FILE Helper-UI PASS.

Der finale Feature-Head und der Squash-Main-Commit erzeugen reproduzierbar denselben Runtime-ZIP-SHA256:

`f8ffd88e2f3e40416f0d76b20786aa168cebb4e11fe3ef9d0eefa6dcf93b19ee`

Der frühere Promotion-Hash `a7ab6d64…` entstand vor dem abschließenden Runtime-Metadaten-Sync der `VERSION_REGISTRY.json` und ist deshalb nicht der finale Main-Artefakthash.

## Nächster Qualitätsweg

Keine neue Produktfunktion in diesem Abschlussstand. Als Nächstes wird ausschließlich **Native L4 real auf Kubuntu** durchgeführt. PASS/FAIL/SKIP darf nur aus realer Nutzerbeobachtung entstehen; CI setzt keinen L4-Schritt automatisch auf PASS.

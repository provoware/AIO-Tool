# TOOLBESCHREIBUNG — AIO-Tool

## Aktueller Entwicklungsstand

`0.5.1-audit-modern-ui` — 🟢 **TESTED / draft für L0–L3**. DEV-Run `33045348341` und TESTED-Promotion `33045669222` sind vollständig grün. Native Kubuntu L4 bleibt offen; SAFE-FILE-Ausführung bleibt technisch gesperrt.

AIO-Tool ist ein lokales, offline-first ausgelegtes Werkzeug mit Browseroberfläche und Python-Loopback-Backend. Der 0.5.1-Slice verbessert bewusst **Robustheit, Wartbarkeit, Nutzerfeedback und Erscheinungsbild**, ohne SAFE-FILE-Mutation freizuschalten.

## Audit-Schwerpunkte

### Persistenz

`AtomicJsonStore` serialisiert parallele Threadzugriffe und behandelt Read→Mutate→Write als einen zusammenhängenden In-Process-Vertrag. Backup-Refresh und Hauptdatei werden atomar ersetzt. `ConfigStore` nutzt denselben Kern statt einer zweiten Schreibimplementierung.

### Lokale Sicherheit

Hauptbackend, Native Runner und SAFE-FILE Simulator verwenden denselben exakten Loopback-Host-/Port-Vertrag. Eine Anfrage auf falschem Port oder fremdem Host gilt nicht als vertrauenswürdig.

### Dashboard-Zustand und Nutzerfeedback

- fehlgeschlagene Kalender-/Upcoming-/TODO-/Ereignisabfragen werden als **nicht verfügbar** statt als scheinbar leer dargestellt,
- erfolgreiche Wiederholungen löschen alte Aktionsfehler,
- der Boot-Guard zeigt Start, READY, READY mit Hinweisen oder einen klaren Fehlerzustand,
- Refresh und Config-Speichern laufen single-flight mit `aria-busy`,
- lokale API-Anfragen besitzen einen 8-Sekunden-Timeout mit verständlicher Hilfe,
- Theme-Vorschau wird bei Speicherfehler auf den bestätigten Stand zurückgesetzt.

### Modernes Theme-System

Fünf Themes nutzen denselben semantischen Tokenvertrag:

- Aurora Glass
- Steel Night
- Trash Neon
- Clean Light
- High Contrast

Oberflächenebenen, Akzent, Fokus, Status, Schatten und Kontrast sind getrennt definiert. High Contrast bleibt bewusst ohne dekorative Schatten. Bewegungsreduktion (`prefers-reduced-motion`) wird respektiert.

### Browser-Acceptance und Wartbarkeit

`scripts/ui_acceptance.py` ist die einzige kanonische Browser-Acceptance-Implementierung. `scripts/ui_acceptance_ci.py` ist nur ein dünner Einstieg. Lokale Produktstyles werden aus dem aktuellen `index.html` abgeleitet statt Contract-Versionen an mehreren Stellen zu duplizieren. Ein Regressionstest verhindert eine erneute zweite Harness-Implementierung.

### Hilfsoberflächen

Native Acceptance Runner und SAFE-FILE Simulator verwenden ein gemeinsames `web/helper-ui.css`. Inline-Styles wurden entfernt und die lokale CSP auf `style-src 'self'` verschärft. Dynamische Inhalte werden mit DOM-/`textContent`-Methoden statt `innerHTML` erzeugt.

## SAFE-FILE-Grenze

Weiterhin unverändert:

- `SIMULATION_ONLY=True`
- `EXECUTION_ENABLED=False`
- kein Execute-Endpunkt
- keine Copy-/Move-/Delete-Primitive

Eine spätere echte Copy benötigt einen eigenen neuen Versionsslice mit Journal, Staging, Postvalidation, Crash-/Recoverytests und Guarded Undo.

## Qualitätsstatus und Evidenz

- DEV-Gate `33045348341`: Core/Release + Chromium + Firefox + beide Hilfsoberflächen PASS.
- Promotion-Gate `33045669222`: **138/138 Tests**, Foundation/Learning/Evidence/Documentation Guards, Runtime-ZIP/Preflight, Chromium + Firefox + beide Hilfsoberflächen PASS.
- TESTED-Runtime-ZIP SHA256: `a7ab6d64e978e27c1fa550c549e12dc7ee21e24a17a55fd9c160c19cd3001b72`.

Noch offen sind ausschließlich der abschließende Evidence-/Dokumentations-Gate, Squash-Merge/Main-CI/Hashvergleich sowie die davon getrennte reale Native-L4-Abnahme.

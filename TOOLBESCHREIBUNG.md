# TOOLBESCHREIBUNG — AIO-Tool

## Aktueller Entwicklungsstand

`0.5.1-audit-modern-ui` — 🟠 **DEVELOPMENT / draft**. Letzter vollständig bewiesener Stand: `0.5.0-native-acceptance-safe-file-sim` — 🟢 TESTED L0–L3. Native Kubuntu L4 bleibt offen; SAFE-FILE-Ausführung bleibt technisch gesperrt.

AIO-Tool ist ein lokales, offline-first ausgelegtes Werkzeug mit Browseroberfläche und Python-Loopback-Backend. Der aktuelle Slice verbessert bewusst **Robustheit, Wartbarkeit, Nutzerfeedback und Erscheinungsbild**, ohne SAFE-FILE-Mutation freizuschalten.

## Audit-Schwerpunkte

### Persistenz

`AtomicJsonStore` serialisiert parallele Threadzugriffe und behandelt Read→Mutate→Write als einen zusammenhängenden In-Process-Vertrag. Backup-Refresh und Hauptdatei werden atomar ersetzt. `ConfigStore` nutzt denselben Kern statt einer zweiten Schreibimplementierung.

### Lokale Sicherheit

Hauptbackend, Native Runner und SAFE-FILE Simulator verwenden denselben exakten Loopback-Host-/Port-Vertrag. Eine Anfrage auf falschem Port oder fremdem Host gilt nicht als vertrauenswürdig.

### Dashboard-Zustand

Fehlgeschlagene Kalender-/Upcoming-Abfragen können keine alten Daten unter einem neuen Kontext weiterzeigen. Erfolgreiche Wiederholungen löschen alte Aktionsfehler. Der Boot-Guard zeigt Start, READY oder einen klaren Fehlerzustand.

### Modernes Theme-System

Fünf Themes nutzen denselben semantischen Tokenvertrag:

- Aurora Glass
- Steel Night
- Trash Neon
- Clean Light
- High Contrast

Oberflächenebenen, Akzent, Fokus, Status, Schatten und Kontrast sind getrennt definiert. High Contrast bleibt bewusst ohne dekorative Schatten. Bewegungsreduktion (`prefers-reduced-motion`) wird respektiert.

### Hilfsoberflächen

Native Acceptance Runner und SAFE-FILE Simulator verwenden ein gemeinsames `web/helper-ui.css`. Inline-Styles wurden entfernt und die lokale CSP auf `style-src 'self'` verschärft. Dynamische Inhalte werden mit DOM-/`textContent`-Methoden statt `innerHTML` erzeugt.

## SAFE-FILE-Grenze

Weiterhin unverändert:

- `SIMULATION_ONLY=True`
- `EXECUTION_ENABLED=False`
- kein Execute-Endpunkt
- keine Copy-/Move-/Delete-Primitive

Eine spätere echte Copy benötigt einen eigenen neuen Versionsslice mit Journal, Staging, Postvalidation, Crash-/Recoverytests und Guarded Undo.

## Qualitätsstatus

`0.5.1-audit-modern-ui` wird erst nach komplett grünem Core-/Release- und Chromium-/Firefox-Gate auf TESTED promoviert.

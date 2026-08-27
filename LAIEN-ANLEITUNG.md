# LAIEN-ANLEITUNG — AIO-Tool

Aktuelle Entwicklung: **🟠 `0.5.1-audit-modern-ui` (DEV)**. Letzter vollständig bewiesener Vorgänger: **🟢 `0.5.0-native-acceptance-safe-file-sim-TESTED`**. Die echte Kubuntu-Abnahme L4 bleibt offen. SAFE-FILE bleibt reine Simulation und kann keine Datei verändern.

## AIO-Tool starten

Doppelklick auf `start_tool.desktop` oder `./start_tool.sh` ausführen. Die Startkonsole zeigt ihre Checkpoints mit Ampelstatus. Das Dashboard öffnet ausschließlich einen lokalen Loopback-Dienst.

## Neue Darstellung

Unter **⚙ Darstellung** stehen fünf klar beschriebene Designs zur Auswahl:

- **Aurora Glass** — modern, ruhig, Cyan/Violett.
- **Steel Night** — technisch, klar, dunkles Blau.
- **Trash Neon** — kräftiger Neon-/Subkulturstil.
- **Clean Light** — helle Arbeitsansicht.
- **High Contrast** — besonders deutliche Kontraste ohne dekorative Schatten.

Die Auswahl wird gespeichert. Farbe ist nie das einzige Statussignal; Ampeltext und Symbole bleiben zusätzlich sichtbar.

## Wenn etwas nicht geladen werden kann

Das Dashboard zeigt absichtlich **keine alten Kalender-/Terminwerte als wären sie aktuell**. Ein fehlgeschlagener Bereich wird leer bzw. mit Fehlerhinweis dargestellt. „Neu prüfen“ versucht den Bereich erneut zu laden. Nach erfolgreichem Retry verschwindet ein alter Aktionsfehler wieder.

## Oberfläche real prüfen

Doppelklick auf `native_acceptance.desktop`. Der Assistent führt durch 18 Schritte und setzt keinen Schritt automatisch auf PASS. Wähle PASS nur nach echter Prüfung auf deinem Kubuntu-System.

## SAFE-FILE gefahrlos testen

Doppelklick auf `safe_file_simulation.desktop`. Oben muss stehen:

**🔒 AUSFÜHRUNG TECHNISCH GESPERRT**

Quelle und Ziel werden über einen Auswahldialog gewählt. Die Vorschau prüft nur lesend. Es gibt weiterhin keinen Execute-Endpunkt und keine Copy-/Move-/Delete-Funktion.

## Datenschutz und Sicherheit

- keine Telemetrie
- kein Internet für Kernfunktionen nötig
- Backend nur auf Loopback
- exakter Host-/Port-Vertrag
- lokale persistente Daten werden validiert und atomar geschrieben
- Entwicklungsdokumentation, Tests und CI-Evidenz liegen nicht im Runtime-Transportpaket

## Aktueller Qualitätsstatus

`0.5.1-audit-modern-ui` ist noch **DEV**. Die Verbesserungen gelten erst als TESTED, wenn Unit-/Regressionstests, Runtime-ZIP und Chromium+Firefox auf demselben Commit grün sind.

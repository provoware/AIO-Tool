# LAIEN-ANLEITUNG — AIO-Tool

Aktueller Kandidat: **🟢 `0.5.1-audit-modern-ui` — TESTED für automatische Prüfungen L0–L3.** Die echte Kubuntu-Abnahme L4 bleibt offen. SAFE-FILE bleibt reine Simulation und kann keine Datei verändern.

## AIO-Tool starten

Doppelklick auf `start_tool.desktop` oder `./start_tool.sh` ausführen. Die Startkonsole zeigt ihre Checkpoints mit Ampelstatus. Das Dashboard öffnet ausschließlich einen lokalen Loopback-Dienst.

## Wenn das Dashboard lädt

- **🔵 lädt / Prüfe …** bedeutet: Das Tool liest gerade die lokalen Daten.
- Der Button **Neu prüfen** wird währenddessen kurz gesperrt, damit dieselbe Prüfung nicht mehrfach gleichzeitig startet.
- Antwortet das lokale Backend länger als ungefähr 8 Sekunden nicht, erscheint ein verständlicher Hinweis auf die Startkonsole statt eines endlosen Ladezustands.
- **Keine Daten vorhanden** und **Daten konnten nicht geladen werden** werden ausdrücklich unterschieden.

## Neue Darstellung

Unter **⚙ Darstellung** stehen fünf klar beschriebene Designs zur Auswahl:

- **Aurora Glass** — modern, ruhig, Cyan/Violett.
- **Steel Night** — technisch, klar, dunkles Blau.
- **Trash Neon** — kräftiger Neon-/Subkulturstil.
- **Clean Light** — helle Arbeitsansicht.
- **High Contrast** — besonders deutliche Kontraste ohne dekorative Schatten.

Ein Theme reagiert sofort als Vorschau. Während es lokal gespeichert wird, sind konkurrierende Darstellungsschalter kurz gesperrt. Scheitert das Speichern, stellt AIO-Tool automatisch die vorher bestätigte Darstellung wieder her.

Farbe ist nie das einzige Statussignal; Ampeltext und Symbole bleiben zusätzlich sichtbar. Tastaturfokus und größere Bedienziele bleiben in allen Themes erhalten.

## Wenn etwas nicht geladen werden kann

Das Dashboard zeigt absichtlich **keine alten Kalender-/Terminwerte als wären sie aktuell**. Der betroffene Bereich zeigt stattdessen einen klaren Fehler-/Nicht-verfügbar-Hinweis. **Neu prüfen** versucht den Bereich erneut zu laden. Nach erfolgreichem Retry verschwindet ein alter Aktionsfehler wieder.

## Oberfläche real prüfen

Doppelklick auf `native_acceptance.desktop`. Der Assistent führt durch 18 Schritte und setzt keinen Schritt automatisch auf PASS. Wähle PASS nur nach echter Prüfung auf deinem Kubuntu-System.

## SAFE-FILE gefahrlos testen

Doppelklick auf `safe_file_simulation.desktop`. Quelle und Ziel werden nur geprüft. Es existiert weiterhin **keine echte Copy-/Move-/Delete-Ausführung**.

Der Sicherheitsvertrag bleibt:

```text
simulation_only=true
execution_enabled=false
mutation_performed=false
```

## Stand der automatischen Prüfung

DEV-Run `33045348341` und TESTED-Promotion `33045669222` haben Core/Release, Chromium, Firefox sowie Native-/SAFE-FILE-Hilfsoberflächen bestanden. **Das ersetzt die reale Kubuntu-L4-Prüfung nicht.**

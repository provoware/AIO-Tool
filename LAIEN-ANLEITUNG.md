# LAIEN-ANLEITUNG — AIO-Tool

Aktueller Stand: **🟢 `0.5.1-audit-modern-ui` — auf `main` für automatische Prüfungen L0–L3 BEWIESEN.** Die echte Kubuntu-Abnahme L4 bleibt offen. SAFE-FILE bleibt reine Simulation und kann keine Datei verändern.

## AIO-Tool starten

Doppelklick auf `start_tool.desktop` oder `./start_tool.sh` ausführen. Die Startkonsole zeigt ihre Checkpoints mit Ampelstatus. Das Dashboard öffnet ausschließlich einen lokalen Loopback-Dienst.

## Wenn das Dashboard lädt

- **🔵 lädt / Prüfe …** bedeutet: Das Tool liest gerade lokale Daten.
- **Neu prüfen** wird während einer laufenden Prüfung kurz gesperrt, damit sie nicht mehrfach gleichzeitig startet.
- Antwortet das lokale Backend länger als ungefähr 8 Sekunden nicht, erscheint ein verständlicher Hinweis statt eines endlosen Ladezustands.
- **Keine Daten vorhanden** und **Daten konnten nicht geladen werden** sind bewusst unterschiedliche Meldungen.

## Darstellung

Unter **⚙ Darstellung** stehen fünf Designs zur Auswahl:

- **Aurora Glass** — modern, ruhig, Cyan/Violett.
- **Steel Night** — technisch, klar, dunkles Blau.
- **Trash Neon** — kräftiger Neon-/Subkulturstil.
- **Clean Light** — helle Arbeitsansicht.
- **High Contrast** — besonders deutliche Kontraste ohne dekorative Schatten.

Ein Theme reagiert sofort als Vorschau. Während es gespeichert wird, sind konkurrierende Darstellungsschalter kurz gesperrt. Scheitert das Speichern, stellt AIO-Tool die vorher bestätigte Darstellung wieder her.

## Automatisch bewiesener Stand

`0.5.1` wurde über DEV-, Promotion-, Evidence-, PR- und Main-Gates geprüft. Der Main-CI-Run `33048070879` bestand Core/Release, 138 Tests, Chromium, Firefox, Native-Runner-UI und SAFE-FILE-UI. Der finale Runtime-ZIP ist reproduzierbar; Feature-Head und Squash-Main erzeugen denselben SHA256 `f8ffd88e2f3e40416f0d76b20786aa168cebb4e11fe3ef9d0eefa6dcf93b19ee`.

**Das ersetzt die reale L4-Prüfung nicht.**

## Jetzt: Oberfläche real auf Kubuntu prüfen

Doppelklick auf `native_acceptance.desktop` oder:

```bash
./start_native_acceptance.sh
```

Der Assistent führt durch 18 reale Prüfschritte. Jeder Schritt startet **OFFEN**. Wähle nur nach echter Beobachtung:

- **PASS** = wirklich geprüft und korrekt,
- **FAIL** = Fehler gesehen; der Befund bleibt erhalten,
- **SKIP** = nicht geprüft; gilt ausdrücklich nicht als bestanden.

Prüfe dabei die im Runner geforderten Kombinationen aus Kubuntu, Firefox/Chromium, Fenster-/Displaybedingungen, Browserzoom bis 200 % und Tastaturbedienung. Eine grüne CI darf hier niemals automatisch PASS setzen.

## SAFE-FILE gefahrlos testen

Doppelklick auf `safe_file_simulation.desktop`. Quelle und Ziel werden nur gelesen/geprüft. Es existiert weiterhin **keine echte Copy-/Move-/Delete-Ausführung**.

```text
simulation_only=true
execution_enabled=false
mutation_performed=false
```

Diese Sperre bleibt auch während der Native-L4-Abnahme unverändert.

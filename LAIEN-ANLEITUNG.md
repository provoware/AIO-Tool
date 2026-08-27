# LAIEN-ANLEITUNG — AIO-Tool

## Aktueller Stand

Die **Runtime-Baseline** ist `0.5.1-audit-modern-ui` und für die automatisierbaren Prüfungen **L0–L3 BEWIESEN**.

- Programmstand: 🟢 geprüft
- echter Kubuntu-Test L4: 🟡 **OFFEN · 0 von 18 Schritten bestätigt**
- SAFE-FILE-Ausführung: 🔒 **GESPERRT**

Die geprüfte Runtime-Baseline gehört zum Commit `ee6adcfd3427e8328920edaceb804e7b6655cdb8`. Der zugehörige Runtime-ZIP-SHA256 ist `f8ffd88e2f3e40416f0d76b20786aa168cebb4e11fe3ef9d0eefa6dcf93b19ee`.

### Warum kann GitHub trotzdem neuere Commits zeigen?

Nach einem geprüften Programmstand dürfen reine **Dokumentations- und Evidenzdateien** noch verbessert werden. Das bedeutet nicht automatisch, dass sich das Programm geändert hat. Deshalb unterscheiden wir:

- **Runtime-Baseline** = der geprüfte Programmstand,
- **Repository-Head** = der aktuellste GitHub-Stand inklusive möglicher Dokuänderungen.

Für dich als Nutzer ist die Runtime-Baseline entscheidend.

## AIO-Tool starten

Doppelklick auf `start_tool.desktop` oder im Projektordner:

```bash
./start_tool.sh
```

Die Startkonsole zeigt die wichtigsten Prüfschritte. Das Tool arbeitet nur lokal über die eigene Loopback-Adresse und sendet keine Telemetrie.

## Wenn das Dashboard lädt

- **🔵 Prüfe …** = Daten werden gerade lokal gelesen.
- **Neu prüfen** wird während einer laufenden Prüfung kurz gesperrt, damit sie nicht mehrfach gleichzeitig startet.
- Wenn das lokale Backend nicht rechtzeitig antwortet, erscheint ein verständlicher Hinweis statt eines endlosen Ladezustands.
- **Keine Daten vorhanden** und **Daten konnten nicht geladen werden** sind absichtlich unterschiedliche Meldungen.

## Darstellung

Unter **⚙ Darstellung** stehen fünf Designs zur Auswahl:

- **Aurora Glass** — modern und ruhig,
- **Steel Night** — technisch und dunkel,
- **Trash Neon** — kräftiger Neonstil,
- **Clean Light** — helle Arbeitsansicht,
- **High Contrast** — besonders deutliche Kontraste.

Eine Auswahl wird sofort als Vorschau gezeigt. Kann sie nicht sicher gespeichert werden, stellt AIO-Tool den vorher bestätigten Stand wieder her.

## Was bedeutet „L0–L3 BEWIESEN“?

Automatisch geprüft wurden unter anderem:

- 138 Unit-/Contracttests,
- Syntax und Datenformate,
- Release- und Manifestprüfungen,
- ein frisch gebautes Runtime-ZIP,
- Chromium und Firefox,
- Dashboard sowie Hilfsoberflächen.

Die kanonische technische Beweiskette liegt in `evidence/releases/0.5.1-audit-modern-ui.json`.

**Diese automatischen Tests ersetzen nicht den echten Kubuntu-Test.**

## Jetzt: Native L4 real prüfen

Starte:

```bash
./start_native_acceptance.sh
```

oder per Doppelklick auf `native_acceptance.desktop`.

Der Assistent enthält 18 reale Prüfschritte. Jeder Schritt startet **OFFEN**.

### Bedeutung der drei Entscheidungen

- **PASS** = du hast den Schritt wirklich durchgeführt und alles war korrekt.
- **FAIL** = du hast einen Fehler gesehen. Der Befund bleibt gespeichert und soll später analysiert werden.
- **SKIP** = du konntest den Schritt nicht prüfen. Er gilt **nicht** als bestanden.

Solange du noch keinen Schritt bestätigt hast, ist der reale L4-Fortschritt **0/18 = 0 %**.

Geprüft werden:

1. Start über Desktop und Shell,
2. laufende Instanz wiederverwenden,
3. fremd belegten Port sicher behandeln,
4. kleines, Full-HD- und großes Fenster,
5. Bedienung nur per Tastatur,
6. Firefox mit 100 / 125 / 150 / 175 / 200 % Zoom,
7. Chrome/Chromium mit 100 / 125 / 150 / 175 / 200 % Zoom.

Wenn du KDE-Skalierung nutzt, schreibe den Wert in die jeweilige Prüfernotiz.

## SAFE-FILE gefahrlos prüfen

Starte:

```bash
./start_safe_file_simulation.sh
```

Die SAFE-FILE-Funktion bleibt eine Simulation. Sie besitzt in dieser Version keine reale Ausführungsfähigkeit.

```text
simulation_only=true
execution_enabled=false
mutation_performed=false
```

Diese Sperre bleibt während der gesamten Native-L4-Abnahme unverändert.

## Wo finde ich technische Details?

- `README.md` — Gesamtüberblick
- `MANIFEST.md` — Status- und Manifestübersicht
- `manifests/README.md` — Erklärung der Manifestarten
- `REGRESSIONSINFOS.md` — bekannte Fehlerverträge
- `TOOLBESCHREIBUNG.md` — technische Funktionsbeschreibung

Für die normale Nutzung musst du diese Dateien nicht verstehen; sie dienen vor allem der nachvollziehbaren Entwicklung und Prüfung.

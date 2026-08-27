# LAIEN-ANLEITUNG — AIO-Tool

## Welchen Stand soll ich benutzen?

- 🟢 **Bewiesen:** `0.4.2-ui-acceptance-TESTED`
- 🟠 **In Entwicklung:** `0.4.3-integrity-hardening-DEV`

Für normale Nutzung ist ein `TESTED`-Paket der sichere Zwischenstand. `DEV` bedeutet: Änderungen sind eingebaut, aber die vollständige neue Evidenz ist noch nicht abgeschlossen.

## Start in 4 Schritten

1. ZIP vollständig in einen eigenen Ordner entpacken.
2. `start_tool.desktop` doppelklicken oder `start_tool.sh` starten.
3. Die Startkonsole zeigt 9 Prüfschritte.
4. Bei Erfolg öffnet sich das Dashboard automatisch.

## Was bedeutet die Ampel?

- 🟢 **PASS** — geprüft und in Ordnung.
- 🟡 **WARN** — Hinweis; Start kann trotzdem möglich sein.
- 🔴 **FAIL** — sicherer Abbruch. Die Ursache wird erklärt.
- 🔵 **INFO** — normaler Zwischenzustand.

Die Farbe ist nur Zusatzhilfe. Der Status steht immer auch als Text dabei.

## Die 9 Start-Checkpoints

1. Toolordner erkannt.
2. Python vorhanden.
3. Diagnose und Installationskennung vorbereitet.
4. laufende Instanz/Port geprüft.
5. lokale Python-Umgebung geprüft.
6. Runtime-Basis geprüft.
7. Backendprozess gestartet.
8. Backend als passende Instanz verifiziert.
9. Browseroberfläche geöffnet.

Wenn der Standardport durch eine andere oder ältere lokale Anwendung belegt ist, übernimmt AIO-Tool diese **nicht**. Es sucht einen freien lokalen Ausweichport und zeigt das als gelben Hinweis.

## Wenn der Start fehlschlägt

Die Konsole bleibt offen und zeigt eine eindeutige Fehler-ID, zum Beispiel:

- `LAUNCH-E102` — Python fehlt.
- `LAUNCH-E205` — lokale Python-Umgebung konnte nicht erstellt werden.
- `LAUNCH-E303` — Installationskennung konnte nicht vorbereitet werden.
- `LAUNCH-E306` — Runtime-Vorprüfung fehlgeschlagen.
- `LAUNCH-E404` — kein freier lokaler Ausweichport.
- `LAUNCH-E407` — Backendprozess wurde direkt beendet.
- `LAUNCH-E508` — Backend wurde nicht als passende Instanz bereit.

Unter `runtime/` liegen dann lokale Diagnose-Dateien. Diese Dateien werden **nicht** ins Release-ZIP aufgenommen.

## Was sehe ich im Dashboard?

### Monatskalender

- Montag bis Sonntag.
- vorheriger/nächster Monat über Pfeile.
- **Heute** springt zum aktuellen Monat.
- Termine werden im Kalender und zusätzlich kompakt darunter gezeigt.

### Nächste Aufgaben

Rechts erscheinen höchstens die nächsten drei TODOs. Mit **✓** wird eine Aufgabe nicht einfach gelöscht, sondern mit Zeitstempel ins Erledigt-Archiv verschoben.

### Letzte Ereignisse

Die letzten fünf wichtigen Ereignisse erscheinen in verständlicher Sprache. Technische Rohdetails bleiben im Diagnosebereich.

### Erinnerungen

Ablauf:

`fällig → sichtbar anzeigen → du klickst „Gesehen“ → erst dann speichern`

Ein unsichtbarer Tab oder bloßes Nachfragen im Hintergrund quittiert keine Erinnerung.

### Module

Links zeigt **Häufig** die wichtigsten Module. **Alle** blendet weitere Bereiche ein. Der Datei-Bereich bleibt absichtlich noch ohne echte Dateiänderungen, bis der Sicherheits-Slice SAFE-FILE-CORE entwickelt ist.

## Darstellung

- vier Themes,
- Schriftgrößen-Presets,
- automatische Dichte,
- Tastatur-Fokusrahmen,
- Sprunglink zum Hauptinhalt,
- Reduced-Motion-Schutz,
- Browser-Reflow bis 320 CSS-px automatisiert geprüft.

Chromium und Firefox werden in CI real gerendert und bedient. Die **native** Kubuntu-/KDE-/DPI-/100–200-%-Zoom-Abnahme bleibt trotzdem ein eigener offener Praxistest.

## Datenschutz

- kein Internetzwang,
- Backend nur lokal auf `127.0.0.1`,
- keine Telemetrie,
- keine externen Runtime-Pakete,
- lokale Config/TODO/Kalender/Ereignisse/Logs werden nicht ins Release übernommen.

## Was bedeutet der ZIP-Dateiname?

- `DEV` — Entwicklung.
- `TESTED` — automatisiert geprüft.
- `RC` — Release Candidate.
- `RELEASED` — offiziell freigegeben.
- `BLOCKED` — bekannter Blocker.
- `ARCHIVED` — historischer Stand.

## Was kommt als Nächstes?

1. `0.4.3-integrity-hardening` vollständig prüfen und nur bei grünem Gate auf TESTED setzen.
2. Danach natives Kubuntu-/Zoom-/Tastatur-Gate.
3. Erst danach SAFE-FILE-CORE mit **Copy** als erster kontrollierter Dateioperation.

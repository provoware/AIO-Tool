# LAIEN-ANLEITUNG

## AIO-Tool 0.4.0-dashboard-v2

AIO-Tool ist ein lokaler Arbeitsplatz für wiederkehrende Aufgaben. Die aktuelle Version bringt die vorhandenen Kalender-, TODO-, Ereignis- und Systemdaten erstmals gemeinsam in eine kompakte Hauptansicht.

## Was sehe ich direkt nach dem Start?

### 1. Oben: Systemzustand

Du siehst:

- aktuelle Version,
- ob das lokale Backend bereit ist,
- ob die Versionsdaten zusammenpassen,
- einen Button **Neu prüfen**.

🟢 **bereit** bedeutet: Die geladenen Kernbereiche melden keinen Fehler.  
🟠 **teilweise** bedeutet: Das Grundsystem läuft, aber mindestens ein Bereich konnte nicht vollständig geladen werden.  
🔴 **Eingriff** bedeutet: Der Systemstatus selbst konnte nicht sicher geladen werden.

## 2. Nächster sinnvoller Schritt

Das Dashboard versucht nicht, dir möglichst viele Meldungen gleichzeitig zu zeigen. Es hebt zuerst hervor:

1. eine fällige Erinnerung,
2. sonst die nächste offene Aufgabe,
3. sonst den nächsten Termin.

## 3. Monatskalender

Der Kalender bleibt in der Hauptansicht sichtbar.

- Woche: **Montag bis Sonntag**.
- **‹ / ›** wechselt den Monat.
- **Heute** springt zurück zum aktuellen Monat.
- Der heutige Tag wird hervorgehoben.
- An Tagen mit Terminen wird eine kleine Anzahl angezeigt.

Auf kleinen Bildschirmen werden Details im Monatsraster reduziert, damit der Monat trotzdem übersichtlich bleibt. Die nächsten Termine stehen zusätzlich unter dem Kalender.

## 4. Nächste TODOs

Rechts erscheinen höchstens die nächsten drei Aufgaben aus der bereits getesteten TODO-Reihenfolge.

Mit **✓** wird eine Aufgabe erledigt. Sie wird dabei nicht einfach gelöscht, sondern vom Backend ins Erledigt-Archiv verschoben.

## 5. Letzte Ereignisse

Das Dashboard zeigt die letzten fünf wichtigen Ereignisse in verständlichen Sätzen. Technische Rohdetails bleiben vom normalen Verlauf getrennt.

## 6. Erinnerungen

Eine fällige Erinnerung erscheint deutlich oberhalb des Dashboards.

Wichtig:

> Nur weil das Tool nach Erinnerungen fragt, gilt eine Erinnerung noch nicht als gesehen.

Der Ablauf ist:

`fällig → sichtbar anzeigen → du klickst „Gesehen“ → erst dann speichern`

Ist der Browser-Tab gerade nicht sichtbar, quittiert das Dashboard keine Erinnerung.

## 7. Schnellzugriff

Links findest du Module zunächst unter **Häufig**. Mit **Alle** werden zusätzliche Bereiche eingeblendet.

Der Datei-Bereich ist absichtlich noch deaktiviert. Echte Dateiänderungen werden erst nach den offenen Zielsystemprüfungen als eigener Sicherheits-Slice ergänzt.

## 8. Entwicklerbereich

Unter **Darstellung** kannst du den Entwicklerbereich freischalten. Danach erscheint ein kleiner Diagnose-Button.

Die Diagnose zeigt nur technische Zustände wie Version, Registrystatus und Zähler. Sie zeigt bewusst nicht die vollständige Konfiguration, den aktiven Projektpfad oder deine Favoritenliste.

## 9. Darstellung

Vier Themes bleiben verfügbar:

- Trash Neon,
- Steel Night,
- Clean Light,
- High Contrast.

Schriftgrößen: 90 / 100 / 110 / 120 / 130 / 140 %.

Zusätzlich passt das Dashboard seine Dichte automatisch an Fenstergröße und Schriftgröße an: **kompakt / normal / weit**.

## Barriereärmere Bedienung

Vorbereitet und automatisiert geprüft sind:

- sichtbare Tastatur-Fokusrahmen,
- Sprunglink zum Hauptinhalt,
- Status-/Reminder-Livebereiche für assistive Technik,
- Reduced-Motion-Regel,
- responsive Layoutstufen.

Die reale Bedienung mit Firefox/Chrome und 125–200 % Zoom ist noch ein eigener offener Test und wird nicht als bestanden ausgegeben.

## Datenschutz

- kein Internetzwang,
- Backend nur lokal auf `127.0.0.1`,
- keine Telemetrie,
- keine externen Python-Pakete,
- lokale Config-, TODO-, Event- und Kalenderdaten werden nicht ins Release-ZIP übernommen.

## Was wurde automatisch geprüft?

GitHub Actions Run `33026823914` war grün:

- 77 Tests,
- Dashboard-/Foundation-Validierung,
- Learning Guard,
- Launcher,
- JavaScript,
- Release-Builder,
- vollständiges ZIP-Artefakt.

## Was kommt als Nächstes?

Zuerst wird genau dieses ZIP auf dem echten Kubuntu-Zielsystem mit Firefox, Chrome/Chromium, mehreren Zoomstufen und Tastaturbedienung geprüft.

Erst danach beginnt **SAFE-FILE-CORE**: Kopieren mit Vorprüfung, Vorschau, Nachprüfung und Undo-/Recovery-Vertrag.

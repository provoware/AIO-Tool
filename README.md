# AIO-Tool

Ein einfaches Dashboard für Aufgaben, Notizen und Kalender. Alles läuft im Browser und speichert die Daten lokal.

## Start

1. Starte einen kleinen Webserver:
   ```
   python3 -m http.server 8000
   ```
2. Öffne im Browser: [http://localhost:8000](http://localhost:8000)

## Module
- **Dashboard:** zeigt Anzahl offener Todos und Notizen.
- **Todo:** Aufgaben mit Datum hinzufügen, abhaken und archivieren.
- **Notizen:** kurzer Text, der dauerhaft im Browser gespeichert wird.
- **Kalender:** aktuelle Monatsansicht.
- **Debug-Log:** einfache Protokollausgabe aller Aktionen.

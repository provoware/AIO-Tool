# LAIEN-ANLEITUNG — AIO-Tool

Aktuelle Entwicklung: **`0.5.0-native-acceptance-safe-file-sim` (DEV)**. Letzter bewiesener Vorgänger: `0.4.3-integrity-hardening-TESTED`.

## Welche Datei starte ich?

### AIO-Tool normal

Doppelklick auf `start_tool.desktop`.

### Oberfläche richtig prüfen

Doppelklick auf `native_acceptance.desktop`.

Es öffnet sich ein Prüfassistent. Oben siehst du den Fortschritt, links den aktuellen Schritt und rechts alle 18 Prüfschritte.

Für jeden Schritt gibt es nur drei eindeutige Entscheidungen:

- 🟢 **PASS** — ich habe es wirklich geprüft und es funktioniert.
- 🔴 **FAIL** — ich habe es geprüft und etwas stimmt nicht.
- ⚪ **Überspringen** — jetzt nicht geprüft; gilt nicht als bestanden.

Bei Browser-Schritten steht genau dabei, welchen Browser und welchen Zoom du einstellen sollst. Der Assistent speichert technische Größen automatisch, aber du bestätigst selbst, ob die Darstellung korrekt war.

Berichte entstehen automatisch unter `runtime/reports/` und können zusätzlich als JSON/TXT heruntergeladen werden.

## SAFE-FILE gefahrlos ausprobieren

Doppelklick auf `safe_file_simulation.desktop`.

Oben muss deutlich stehen:

**🔒 AUSFÜHRUNG TECHNISCH GESPERRT**

Dann:

1. „Quelldatei auswählen“ klicken.
2. „Zielordner auswählen“ klicken.
3. Konfliktoption wählen; empfohlen ist **Sicher: überspringen**.
4. „Sichere Vorschau erstellen“ klicken.

Du erhältst eine Ampelprüfung für Quelle, Ziel, Speicherplatz und Konflikte.

### Kann dabei eine Datei kopiert oder gelöscht werden?

**Nein.** Diese Entwicklungsstufe besitzt keine Ausführungsfunktion. Sie kann nur lesen, prüfen und anzeigen, was eine spätere Copy tun würde.

## Wenn ein Prüfschritt FAIL ist

Nicht einfach PASS wählen. Schreibe optional eine kurze Notiz und lasse FAIL gespeichert. Dieser reale Befund soll anschließend als Regressionstest in die Entwicklung zurückfließen.

## Datenschutz

Alle Sitzungs-/Simulationsdaten bleiben lokal. Es gibt keine Telemetrie. Der Release-Evidenzindex liegt im Entwicklungsrepository und wird nicht in dein Runtime-Paket übernommen.

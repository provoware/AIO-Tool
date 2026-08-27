# LAIEN-ANLEITUNG — AIO-Tool

Aktueller Stand: **`0.5.0-native-acceptance-safe-file-sim` — TESTED für automatische Prüfungen L0–L3.** Die echte Kubuntu-Abnahme L4 ist noch offen. SAFE-FILE ist weiterhin **nur Simulation** und kann keine Datei verändern.

## Welche Datei starte ich?

### AIO-Tool normal

Doppelklick auf `start_tool.desktop`.

### Oberfläche auf deinem echten Rechner prüfen

Doppelklick auf `native_acceptance.desktop`.

Es öffnet sich ein Prüfassistent. Oben siehst du den Fortschritt, links den aktuellen Schritt und rechts alle 18 Prüfschritte.

Für jeden Schritt gibt es nur drei eindeutige Entscheidungen:

- 🟢 **PASS** — ich habe es wirklich geprüft und es funktioniert.
- 🔴 **FAIL** — ich habe es geprüft und etwas stimmt nicht.
- ⚪ **Überspringen** — jetzt nicht geprüft; gilt nicht als bestanden.

Bei Browser-Schritten steht genau dabei, welchen Browser und welchen Zoom du einstellen sollst. Der Assistent speichert technische Größen automatisch, aber du bestätigst selbst, ob die Darstellung korrekt war. **Er setzt niemals selbst PASS.**

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

### Kann dabei eine Datei kopiert, verschoben oder gelöscht werden?

**Nein.** Diese Version besitzt absichtlich keine Ausführungsfunktion. Sie kann nur lesen, prüfen und anzeigen, was eine spätere Copy tun würde. Auch der Status TESTED ändert diese Sperre nicht.

## Wenn ein Prüfschritt FAIL ist

Nicht einfach PASS wählen. Schreibe optional eine kurze Notiz und lasse FAIL gespeichert. Dieser reale Befund soll anschließend als Regressionstest in die Entwicklung zurückfließen.

## Datenschutz

Alle Sitzungs-/Simulationsdaten bleiben lokal. Es gibt keine Telemetrie. Der Release-Evidenzindex liegt im Entwicklungsrepository und wird nicht in dein Runtime-Paket übernommen.

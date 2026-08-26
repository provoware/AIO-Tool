# LAIEN-ANLEITUNG

## Was ist AIO-Tool?

AIO-Tool soll viele wiederkehrende Aufgaben in einer gemeinsamen Oberfläche bündeln. Die Bedienung soll einfach, sichtbar und sicher bleiben.

## Was funktioniert in dieser Foundation-Version bereits?

Die Version `0.1.1-foundation` ist der erste startbare Grundkern.

Du kannst:

- das Tool über `start_tool.sh` starten,
- die lokale Browser-Oberfläche öffnen,
- zwischen 4 Farbthemes wählen,
- die Schriftgröße per Button ändern,
- den Expertenbereich ein- oder ausblenden,
- den Systemstatus erneut prüfen.

Noch nicht enthalten sind echte Dateiaktionen wie Kopieren, Verschieben, Umbenennen oder Löschen.

## Start unter Kubuntu/Linux

1. Öffne den AIO-Tool-Ordner.
2. Starte `start_tool.sh`.
3. Beim ersten Start richtet das Tool automatisch eine lokale Python-Umgebung `.venv` ein.
4. Danach läuft eine kurze Vorprüfung.
5. Das lokale Backend startet nur auf deinem Rechner.
6. Die Oberfläche öffnet sich im Browser.

Falls die Datei nicht startbar ist:

```bash
chmod +x start_tool.sh
./start_tool.sh
```

Falls die virtuelle Umgebung nicht erstellt werden kann, fehlt auf Ubuntu/Kubuntu meist `python3-venv`. Der Launcher zeigt dafür eine verständliche Fehlermeldung.

## Wichtig: Das Tool bleibt lokal

- Kernfunktionen brauchen kein Internet.
- Das Backend bindet nur an `127.0.0.1`.
- Es gibt keine Telemetrie als Standard.
- Es werden keine externen Python-Pakete installiert.

## Bedienprinzip

Du sollst möglichst wenig technische Zeichen oder Pfade eintippen müssen.

Bevorzugt werden:

1. Buttons,
2. Auswahldialoge,
3. Presets und zuletzt verwendete sichere Optionen,
4. Empfehlungen,
5. Freitext nur wenn wirklich nötig.

## Darstellung

### Theme

Wähle einfach einen Button:

- Trash Neon
- Steel Night
- Clean Light
- High Contrast

### Schriftgröße

Verfügbare Buttons:

`90 % · 100 % · 110 % · 120 % · 130 % · 140 %`

### Expertenbereich

Der Expertenbereich ist standardmäßig verborgen. Er zeigt zusätzliche technische Informationen, ist aber für die normale Bedienung nicht nötig.

## Ampelsystem

- 🟢 **bereit** – alles in Ordnung.
- 🟡 **optional** – kann sinnvoll sein.
- 🟠 **prüfen** – Entscheidung oder Prüfung offen.
- 🔴 **Eingriff** – Fehler, Risiko oder Schutzmaßnahme nötig.

Farbe wird immer zusätzlich mit Text/Symbol erklärt.

## Wenn das Tool schon läuft

Ein zweiter Start soll keine zweite Backend-Instanz erzeugen. Der Launcher versucht stattdessen, die bereits laufende lokale Oberfläche zu öffnen.

## Wenn etwas nicht startet

1. Meldung im Terminal lesen.
2. Bei Bedarf `runtime/launcher.log` ansehen.
3. Nichts manuell aus Runtime-Dateien löschen, solange unklar ist, was passiert ist.
4. Die Foundation-Vorprüfung kann technisch mit `python3 scripts/validate.py` gestartet werden.

## Nächster Entwicklungsschritt

Die erste echte Dateiaktion wird **Kopieren** sein. Dabei ist der geplante sichere Ablauf:

`Quelle wählen → Ziel wählen → prüfen → Vorschau → bestätigen → kopieren → nachprüfen → Recovery-Datensatz`

Verschieben, Umbenennen und Löschen werden erst danach ergänzt.

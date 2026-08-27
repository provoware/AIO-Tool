# LAIEN-ANLEITUNG — AIO-Tool

## Stand

Der aktuelle Entwicklungsslice heißt `0.6.0-autostart-selfheal` und ist noch `development / draft`. Die zuletzt bereits bewiesene **Runtime-Baseline** bleibt `0.5.1-audit-modern-ui`. Native Kubuntu L4 bleibt **OFFEN**; SAFE-FILE-Ausführung bleibt **GESPERRT**.

## Normal starten

Im Ordner doppelt auf `start_tool.desktop` klicken oder:

```bash
./start_tool.sh
```

Die neue Startroutine prüft selbstständig die wichtigsten Startbedingungen. Sie zeigt jeden Schritt sichtbar an und versucht nur datensichere Reparaturen.

## Was automatisch gelöst wird

- ein belegter Standard-Port führt nicht sofort zum Abbruch; ein freier lokaler Port wird gesucht,
- eine veraltete eigene PID-Datei wird erkannt und entfernt,
- beschädigte lokale Einstellungs-/Kalender-/TODO-/Ereignisdateien werden geprüft,
- ein brauchbares Backup wird bevorzugt zurückgespielt,
- beschädigte Originale werden vorher in `runtime/quarantine/` gesichert,
- in einem gebauten Paket können beschädigte Programmdateien aus `RECOVERY_BASIS.zip` wiederhergestellt werden,
- ist der Programmordner schreibgeschützt, kann die Basis in einen benutzereigenen Bereich gespiegelt und von dort gestartet werden.

## Was **nicht** automatisch passiert

- kein `sudo`,
- keine Installation von Systempaketen,
- keine Änderung außerhalb der eigenen AIO-Tool-/Benutzerbereiche,
- keine Löschung beschädigter Nutzerdaten ohne Quarantäne,
- keine echte SAFE-FILE-Dateioperation.

## Portable Linux x86_64

Das Portable-Paket enthält den benötigten Python-Interpreter. Deshalb ist auf dem Zielrechner normalerweise weder `pip` noch eine Python-Installation nötig.

Start ebenfalls mit:

```bash
./start_tool.sh
```

Der Starter erkennt automatisch die enthaltene Datei `AIO-Tool-Start`.

## Ampel während des Starts

- 🟢 **grün** = Prüfung bestanden,
- 🟡 **gelb** = etwas wurde repariert oder verständlich abgefangen,
- 🔴 **rot** = sicherer Start ist nicht möglich; der Grund wird angezeigt,
- 🔵 **blau** = Information oder bewusst übersprungener Prüfschritt.

## Automatische Qualitätsprüfung

Für `0.6.0-autostart-selfheal` wird exakt diese Kette verwendet:

`Core-CI → Failure-Matrix → Source-ZIP → RECOVERY_BASIS → Portable-Build → Portable-Smoke → Chromium → Firefox`.

Erst wenn alle acht Stufen für denselben Commit grün sind, darf über eine Statuspromotion nachgedacht werden.

## Native L4 — OFFEN

Die echte Bedienung auf Kubuntu mit realem Bildschirm, Tastatur und Zoom bleibt eine getrennte Feldprüfung. Automatische Tests dürfen daraus keinen PASS erfinden. Der Fortschritt bleibt bis zu realer Bestätigung bei **0 %**.

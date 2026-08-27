# TOOLBESCHREIBUNG — AIO-Tool

## Produktidee

AIO-Tool ist ein lokaler, modularer All-in-One-Arbeitsplatz für Organisations-, Projekt-, Kalender-, TODO- und später sichere Datei-/Automatisierungsaufgaben. Die Oberfläche richtet sich zuerst an Nutzer ohne technisches Spezialwissen.

## Leitregeln

**Auswahl vor Zeicheneingabe. Sichtbarkeit vor Automatisierung. Sicherheit vor Bequemlichkeit. Evidenz vor Status.**

## Versionsstand

- 🟢 letzter bewiesener Stand: `0.4.2-ui-acceptance-TESTED`
- 🟠 aktuelle Entwicklung: `0.4.3-integrity-hardening-DEV`

`0.4.3` verbessert Robustheit und Wartbarkeit, ohne neue Nutzerfunktion einzuführen.

## Informationsarchitektur

**Links:** Schnellmodule, Häufig/Alle, optional Diagnose.  
**Mitte:** Monatskalender und kommende Termine.  
**Rechts:** nächste drei TODOs, letzte fünf Ereignisse, System-/Versionsstatus.  
**Darüber:** globaler Zustand, nächster sinnvoller Schritt und fällige Reminder.

## Technischer Kern

- `AtomicJsonStore` — atomare Persistenz + Backup-Fallback.
- `VersionRegistry` — Version, Status, Evidenz und zulässige Statuskombinationen.
- `EventRegistry` — verständliche Ereignisse.
- `TodoStore` — Aufgaben, Titelgedächtnis, Erledigt-Archiv.
- `CalendarStore` — Termine, Perioden, Reminder, `zoneinfo`/DST.
- `ErrorAdvisor` — versionierte Fehlerhilfe.
- `instance_identity.py` + `launcher_probe.py` — sichere Erkennung der konkreten lokalen Installation.

## Startphilosophie

Die Startroutine zeigt neun Checkpoints mit Ampelstatus und Fehler-IDs. Eine vorhandene Instanz wird nur wiederverwendet, wenn Version, Loopback-/Ready-Zustand und Installationskennung zusammenpassen. Fremd belegte Ports werden nicht still übernommen.

Normaler Nutzerstart prüft ausschließlich die transportierte Runtime-Basis über `scripts/runtime_preflight.py`; Repositorytests und Dokumentation sind keine Laufzeitabhängigkeit.

## UI-Qualitätsvertrag

Dashboarddarstellung wird mehrstufig geprüft:

1. statische Struktur-/API-Verträge,
2. maschinenlesbarer 12-Spalten-Rastervertrag,
3. echte Chromium-/Firefox-Läufe,
4. Viewport-/Reflow-Matrix bis 320 CSS-px,
5. Geometrie, Zielgrößen und Interaktionen,
6. Screenshot-/JSON-Evidenz.

Die native Kubuntu-/KDE-/DPI-/Zoom-Abnahme bleibt davon getrennt.

## Reminder-Vertrag

`fällig → sichtbar darstellen → Nutzer bestätigt → ACK persistieren`

Polling oder ein unsichtbarer Tab erzeugen keinen gesehenen Zustand.

## Transportphilosophie

Runtime und Repository sind getrennte Produktebenen.

**Runtime-ZIP:** nur positive Allowlist aus `manifests/RUNTIME_MANIFEST.json` + generiertes `MANIFEST_RELEASE.json`.  
**Repository/lokal:** Dokumentation, Tests, Testdaten, CI, Learning Memory, Browserreports und Logs.

Status ist am Dateinamen sichtbar: `DEV`, `TESTED`, `RC`, `RELEASED`, `BLOCKED`, `ARCHIVED`.

## Sicherheitsphilosophie für spätere Dateioperationen

`Vorprüfung → Vorschau → Bestätigung → Aktion → Nachprüfung → Protokoll → Undo/Recovery`

Echte Dateioperationen sind noch bewusst nicht aktiv. SAFE-FILE-CORE beginnt später ausschließlich mit **Copy** und erweitert erst nach bewiesener Stabilität auf Move/Rename/Papierkorb.

## Noch offen

- native Kubuntu-Klick-&-Start-Abnahme,
- KDE-/HiDPI-Skalierung,
- 100–200 % realer Browserzoom,
- realer Tastatur-/Screenreader-Durchlauf,
- SAFE-FILE-CORE,
- persistente Job-/Recovery-Queue.

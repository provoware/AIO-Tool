# AIO-Tool

> Lokales, modulares und laienfreundliches All-in-One-Tool mit sicherem Python-Backend und Browseroberfläche.

## Status

- **Version:** `0.4.0-dashboard-v2`
- **Phase:** P1 — Dashboard-Integration
- **Stand:** 2026-08-27
- **Automatischer Code-Gate:** GitHub Actions Run `33026823914` — SUCCESS
- **Tests:** 77 Unit-/Integrations-/Vertragstests
- **Release-Status:** `draft`; reale Kubuntu-/Browser-/Zoom-Gates bleiben offen
- **Backend:** ausschließlich `127.0.0.1`, kein Internetzwang
- **Externe Python-Pakete:** keine

## Was ist jetzt sichtbar nutzbar?

Dashboard V2 verbindet die bereits getesteten Core-APIs zu einer kompakten Arbeitsübersicht, ohne die Fachlogik in JavaScript zu duplizieren:

- dauerhaft sichtbarer Monatskalender,
- nächste Termine,
- nächste drei TODOs mit direktem Abhaken,
- letzte fünf verständliche Ereignisse,
- Versions-, Registry- und Systemstatus,
- fällige Reminder als sichtbare Hinweise,
- explizite Reminder-Quittierung über **„Gesehen“**,
- Schnellzugriff **Häufig / Alle**,
- kleiner optionaler Entwickler-/Diagnosebereich,
- vier Themes und Schriftgrößen 90–140 %,
- automatisch abgeleitete Darstellungsdichte für verschiedene Fenstergrößen,
- Tastatur-Fokus, Skip-Link, ARIA-Live-Bereiche und Reduced-Motion-Schutz.

## Sicherer Reminder-Vertrag

Ein fälliger Reminder wird nicht beim bloßen Polling quittiert.

`fällig → sichtbar im Dashboard → Nutzer klickt „Gesehen“ → Backend speichert notified_at`

Ist der Browser-Tab unsichtbar, führt Dashboard V2 keine Quittierung aus. Dadurch bleibt ein noch nicht tatsächlich gesehener Hinweis nach Reload/erneuter Abfrage offen.

## Kalender/TODO/Ereignisse

Die UI verwendet ausschließlich die vorhandenen APIs:

- `/api/status`
- `/api/todos`
- `/api/todos/<id>/complete`
- `/api/events?limit=5`
- `/api/calendar?view=month|year`
- `/api/calendar/reminders/due`
- `/api/calendar/<event>/reminders/<minutes>/ack`

Kalenderperioden, TODO-Reihenfolge, Reminder-Fälligkeit und Persistenz bleiben Backend-Verantwortung.

## Versionierte Dashboard-Texte

`web/dashboard-texts.de.v1.json` enthält die wiederkehrenden deutschen UI-Texte mit eigenem Versionsvertrag. `tests/test_dashboard_contract.py` prüft, dass sichtbare `data-i18n`-Schlüssel vorhanden und nicht leer sind.

## Dashboard-Vertragstest

Automatisch geprüft werden unter anderem:

- Kernbereiche des Dashboards vorhanden,
- Montag–Sonntag-Vertrag,
- Nutzung der getesteten Core-APIs,
- Reminder nicht im unsichtbaren Tab quittieren,
- Reminder-ACK nur über sichtbare Nutzeraktion,
- Nutzertitel via `textContent` statt HTML-Injektion,
- Diagnose enthält keine vollständige Config/Projektpfade/Favoriten,
- responsive Breakpoints, Fokusdarstellung und Reduced-Motion-Schutz.

## Bestehender Robustheitskern

Weiterhin enthalten sind:

- `AtomicJsonStore` + Backup-Fallback,
- VersionRegistry mit Evidenzpflicht,
- EventRegistry,
- TODO-Core,
- Calendar-Core mit `zoneinfo`/DST,
- positive/negative Testdaten und Mustervorlagen,
- versionierte Core-Texte und Fehlerregeln,
- `LEARNING_MEMORY.jsonl` + Learning Guard,
- reproduzierbarer Release-Builder.

## Prüfung

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate.py
python3 scripts/learning_guard.py
bash -n start_tool.sh
node --check web/app.js
python3 scripts/release.py --check
```

Der erfolgreiche Run `33026823914` erzeugte `AIO-Tool-0.4.0-dashboard-v2.zip`; der Release-Builder meldete SHA256 `104c361caf65c484626cd24812272e0781c151d2afcbcb933b5fc393a3e9e946`.

## Noch offen

- reale Bedienabnahme auf Kubuntu,
- Firefox und Chrome/Chromium,
- 125–200 % Browserzoom,
- echte Tastatur-/Fokusabnahme im Browser,
- SAFE-FILE-CORE,
- persistente Job-/Recovery-Queue.

## Nächste Entwicklungsreihenfolge

1. **Dashboard V2 final synchronisieren und mergen.**
2. **Zielsystem-/Browser-/Zoom-Gate aus sauberem Release.**
3. Danach **SAFE-FILE-CORE** mit Copy als erster realer Dateioperation.

# CHANGELOG

Alle wesentlichen Änderungen an AIO-Tool werden nachvollziehbar dokumentiert.

## [Unreleased]

### Geplant

- reale Kubuntu-/Firefox-/Chrome-/Zoom-Abnahme aus sauberem `0.4.0-dashboard-v2`-Release.
- anschließend SAFE-FILE-CORE mit Copy als erster realer Dateioperation.

## [0.4.0-dashboard-v2] — 2026-08-27

### Added

- kompakte dreispaltige Dashboard-V2-Oberfläche auf den getesteten Core-APIs.
- dauerhaft sichtbare Monatskalenderansicht mit Montag–Sonntag-Vertrag.
- nächste Termine und nächste drei TODOs.
- direktes TODO-Abhaken über bestehenden API-Vertrag.
- letzte fünf menschenlesbare Ereignisse.
- Version-, Registry-, Backend- und Fremdpaketstatus.
- Reminder-Livebereich mit explizitem Button **„Gesehen“**.
- Schnellmodule mit Umschaltung **Häufig / Alle**.
- optionaler kompakter Entwickler-/Diagnosebereich.
- automatische Darstellungsdichte `compact`, `normal`, `wide`.
- responsive Layouts für große, mittlere und kleine Fenster.
- Skip-Link, Fokusindikatoren, ARIA-Live-Bereiche und Reduced-Motion-Schutz.
- versionierter deutscher Dashboard-Textkatalog `web/dashboard-texts.de.v1.json`.
- `tests/test_dashboard_contract.py` als statischer UI-/API-/Sicherheitsvertrag.

### Changed

- Foundation-Validierung prüft Dashboard-Kernbereiche, API-Verbindungen, Textkatalog und Reminder-Sicherheitsvertrag.
- Validierung von Core-Regel-/Textversionen nutzt die deklarierte Quelldatei statt redundanter harter Versionswerte.
- Dashboard-Diagnose beschränkt sich auf technische Zustandsdaten und gibt keine vollständige Config, Projektpfade oder Favoriten aus.

### Safety

- Polling allein quittiert keinen Reminder.
- ein unsichtbarer Browser-Tab quittiert keinen Reminder.
- Quittierung erfolgt erst nach sichtbarer Dashboarddarstellung und explizitem Klick auf „Gesehen“.
- Nutzer-Titel werden im Dashboard über `textContent` eingesetzt, nicht als HTML interpretiert.
- Backend-Domänenlogik für Kalender/TODO/Reminder wird nicht in JavaScript dupliziert.

### Verified — Code-Gate

GitHub Actions Run `33026823914`: **SUCCESS**.

- 77 Unit-/Integrations-/Vertragstests,
- Foundation-/Dashboard-Validierung,
- Learning Guard mit 9 aktiven Lektionen,
- Launcher-Syntax,
- JavaScript-Syntax,
- Release-Builder,
- vollständiger Release-ZIP-Upload.

Erzeugtes Release: `AIO-Tool-0.4.0-dashboard-v2.zip`  
Release-Builder SHA256: `104c361caf65c484626cd24812272e0781c151d2afcbcb933b5fc393a3e9e946`.

### Not yet verified

- reale Kubuntu-Bedienung,
- Firefox-/Chrome-/Chromium-Darstellung,
- 125–200 % Browserzoom,
- reale Tastatur-/Fokusführung.

## [0.3.0-calendar-core] — 2026-08-27

- persistenter CalendarStore, Reminder-Quittierung, Monats-/Wochen-/Jahresperioden, `zoneinfo`/DST, optionale TODO-Verknüpfung und Kalender-Testverträge.
- finaler Kalender-Head: Run `33026380907` SUCCESS; Squash-Merge `a5a4290f5d13333498b0e051b1fcd94e24cc8e95`.

## [0.2.1-robustness] — 2026-08-27

- versionierte Muster-/Testdaten, Texte, Fehlerregeln, ErrorAdvisor, Learning Memory und Release-ZIP-Gate.
- finaler Head Run `33025238585` SUCCESS; Merge `eec9698d49719579633fc54e6f83eb4fc6834668`.

## [0.2.0-core] — 2026-08-27

- VersionRegistry, EventRegistry, TODO-Core und gemeinsamer AtomicJsonStore.
- Run `33022569880` SUCCESS; Merge `a110132acc4104e0f0c48c736a3fd4bc98a9c290`.

## [0.1.1-foundation] — 2026-08-27

- ausführbarer Foundation-Kern mit Klick-&-Start, Loopback-Backend, atomarer Config, Dashboard-Shell, Tests, CI und Release-Builder.

## [0.1.0-foundation] — 2026-08-27

- saubere Projektgrundlage ohne Altcode und verbindliche Basisdokumentation.

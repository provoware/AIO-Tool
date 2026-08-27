# CHANGELOG

Alle wesentlichen Änderungen an AIO-Tool werden nachvollziehbar dokumentiert.

## [0.4.3-integrity-hardening] — 2026-08-27

### Auditbefunde

- Startroutine war beim UX-Umbau auf einen bloßen `HTTP 200` als Instanzkriterium zurückgefallen.
- normaler Launcher rief wieder die Repository-Prüfung `scripts/validate.py --quick` auf, obwohl diese absichtlich nicht zum Runtime-ZIP gehört.
- VersionRegistry und Release-Builder konnten bei Statusbegriffen auseinanderlaufen.
- statusrelevante Dokumente waren gegenüber dem Produktstand veraltet.
- `0.4.2-TESTED` war nach seiner Evidenz weiter verändert worden; daraus wurde die Regel abgeleitet, bewiesene Versionen einzufrieren.
- Learning Memory und Entwicklungsberichte waren zwischenzeitlich nicht mengenmäßig konsistent.

### Added

- `app/instance_identity.py` als Installations-/UI-Identitätsvertrag.
- `scripts/launcher_probe.py` für Instanzprüfung und sicheren Loopback-Ausweichport.
- echte Launcher-Probe-Regressionen mit lokalem Fake-HTTP-Server.
- End-to-End-Releasevertrag: Runtime-ZIP bauen → entpacken → `runtime_preflight.py` darin ausführen.
- `scripts/documentation_guard.py` gegen Versions-/Statusdrift in Pflichtdokumenten.
- zusätzliche Learning-Regeln bis LRN-015.
- Launcher-Logrotation.

### Changed

- Launcher prüft Version + Loopback/Ready + konkrete Installationskennung, bevor eine vorhandene Instanz wiederverwendet wird.
- fremd belegter Standardport wird nicht übernommen; freier lokaler Ausweichport wird transparent gewählt.
- ungültiger Port oder unbekannter Probe-Zustand führt fail-closed zum sicheren Abbruch.
- normaler Start nutzt ausschließlich `scripts/runtime_preflight.py`.
- Statusmodell kanonisiert: `development`, `tested`, `release-candidate`, `released`, `blocked`, `deprecated`.
- Release-Statuspaare werden zentral validiert; unbekannte Kombinationen sind Fehler.
- Release-Verifikation prüft zusätzlich doppelte ZIP-Einträge, Version, Status und `file_count`.
- README und AGENTS wurden als Status-/Qualitätscockpit bzw. verbindlicher Entwicklungsvertrag neu strukturiert.

### Verified — Entwicklungshead

GitHub Actions Run `33034359454`: **SUCCESS**.

- Core-/Release-Job erfolgreich,
- Unit-/Integrations-/Vertragstests erfolgreich,
- Foundation Validation erfolgreich,
- Learning Guard erfolgreich,
- Documentation Guard erfolgreich,
- Launcher-/JavaScript-Syntax erfolgreich,
- Runtime-ZIP-End-to-End-Vertrag erfolgreich,
- Chromium + Firefox UI-Acceptance erfolgreich.

Danach wurde `0.4.3-integrity-hardening` regelkonform auf **`tested / draft`** promoviert. Der Promotion-Commit wird erneut durch dieselbe Pipeline geprüft.

### Still open

- native Kubuntu-/KDE-Abnahme,
- reale 100–200-%-Zoom-/DPI-Matrix,
- Tastatur-/Screenreader-Praxistest,
- SAFE-FILE-CORE,
- persistente Job-/Recovery-Queue.

## [0.4.2-ui-acceptance] — 2026-08-27

- 12-Spalten-Rastervertrag, Chromium-/Firefox-Acceptance, 320-CSS-px-Reflow, Runtime-Allowlist, Statusdateinamen und `MANIFEST_RELEASE.json`.
- GitHub Actions Run `33032999752`: Core/Release und Chromium+Firefox vollständig erfolgreich.
- TESTED-ZIP SHA256: `57c461b56abd024775de8a38d8edf216066c8fd11631d4d266e4572a6d58a6cc`.

## [0.4.0-dashboard-v2] — 2026-08-27

- Dashboard V2 mit Monatskalender, nächsten Terminen/TODOs, letzten fünf Ereignissen, Reminder-Quittierung, Diagnosebereich und responsiver Dichte.

## [0.3.0-calendar-core] — 2026-08-27

- CalendarStore, Reminder-Quittierung, Monats-/Wochen-/Jahresperioden, `zoneinfo`/DST und optionale TODO-Verknüpfung.

## [0.2.1-robustness] — 2026-08-27

- Muster-/Testdaten, Texte, Fehlerregeln, ErrorAdvisor, Learning Memory und Release-Gates.

## [0.2.0-core] — 2026-08-27

- VersionRegistry, EventRegistry, TODO-Core und gemeinsamer AtomicJsonStore.

## [0.1.1-foundation] — 2026-08-27

- ausführbarer Foundation-Kern mit Klick-&-Start, Loopback-Backend, atomarer Config, Tests und CI.

## [0.1.0-foundation] — 2026-08-27

- saubere Projektgrundlage und verbindliche Basisdokumentation.

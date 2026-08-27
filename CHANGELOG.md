# CHANGELOG

Alle wesentlichen Änderungen an AIO-Tool werden nachvollziehbar dokumentiert.

## [Unreleased / 0.4.3-integrity-hardening] — 2026-08-27

### Auditbefunde

- Startroutine hatte beim UX-Umbau die frühere Instanzprüfung auf einen bloßen `HTTP 200` zurückfallen lassen.
- Launcher rief wieder die Repository-Prüfung `scripts/validate.py --quick` auf, obwohl diese absichtlich nicht zum Runtime-ZIP gehört.
- VersionRegistry und Release-Builder verwendeten teilweise unterschiedliche/unmögliche Statusschreibweisen.
- README, TODO, MANIFEST, REGRESSIONSINFOS und LAIEN-ANLEITUNG beschrieben noch `0.4.0` als aktuellen Stand.
- `0.4.2-TESTED` war nach seiner Evidenz weiter verändert worden; dafür wird jetzt ein neuer Versionsslice verwendet.
- Learning Memory enthielt real 9 Einträge, obwohl spätere Berichte bereits mehr behauptet hatten.

### Added

- `app/instance_identity.py` als zentraler Installations-/UI-Identitätsvertrag.
- `scripts/launcher_probe.py` für Instanzprüfung und sicheren Loopback-Ausweichport.
- echte Launcher-Probe-Regressionen mit lokalem Fake-HTTP-Server.
- End-to-End-Releasevertrag: Runtime-ZIP bauen → entpacken → `runtime_preflight.py` darin ausführen.
- neue Learning-Regeln LRN-010 bis LRN-015.

### Changed

- neue aktuelle Version `0.4.3-integrity-hardening / development`; `0.4.2-ui-acceptance-TESTED` bleibt eingefrorener Evidenzstand.
- Launcher prüft Version + Loopback/Ready + konkrete Installationskennung, bevor eine vorhandene Instanz wiederverwendet wird.
- fremd belegter Standardport wird nicht übernommen; freier lokaler Ausweichport wird transparent gewählt.
- normaler Start nutzt ausschließlich `scripts/runtime_preflight.py`.
- Launcher-Logs erhalten lokale Größenbegrenzung/Rotation.
- Statusmodell kanonisiert: `development`, `tested`, `release-candidate`, `released`, `blocked`, `deprecated`.
- Release-Statuspaare werden zentral validiert und unbekannte Kombinationen fail-closed abgelehnt.
- Release-Verifikation prüft zusätzlich doppelte ZIP-Einträge, Version, Status und `file_count`.
- Runtime-Manifest 1.1.0 enthält die Instanz-/Probe-Komponenten.
- README und AGENTS wurden als Status-/Qualitätscockpit bzw. verbindlicher Entwicklungsvertrag neu strukturiert.

### Verification status

Noch **DEVELOPMENT**. Vollständige Core-/Release-/Chromium-/Firefox-Evidenz für 0.4.3 wird erst nach Abschluss aller Dokumentations- und Regressionpatches eingetragen.

## [0.4.2-ui-acceptance] — 2026-08-27

- 12-Spalten-Rastervertrag, Chromium-/Firefox-Acceptance, 320-CSS-px-Reflow, Runtime-Allowlist, Statusdateinamen und `MANIFEST_RELEASE.json`.
- GitHub Actions Run `33032999752`: Core/Release und Chromium+Firefox vollständig erfolgreich.
- Erzeugtes TESTED-ZIP SHA256: `57c461b56abd024775de8a38d8edf216066c8fd11631d4d266e4572a6d58a6cc`.

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

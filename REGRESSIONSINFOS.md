# REGRESSIONSINFOS — AIO-Tool

Grundsatz: **Fehler → reproduzierbarer Auslöser → kleinste Codezone → Fix → Regression → Evidenz → Learning Memory bei strukturellem Befund.**

Statussprache: OFFEN / UMGESETZT / GEPRÜFT / BEWIESEN.

Historische Verträge **REG-001 bis REG-066** bleiben verbindlich.

## Neue Verträge — `0.5.1-audit-modern-ui`

### REG-067 — parallele HTTP-Schreibvorgänge verlieren Persistenzupdates
- Risiko: `ThreadingHTTPServer` führt zwei Read→Mutate→Write-Zyklen gleichzeitig aus.
- Vertrag: `AtomicJsonStore.update()` hält einen pro Store gemeinsamen `RLock` über den vollständigen Zyklus.
- Test: 120 parallele Inkremente müssen exakt 120 ergeben.
- Status: **UMGESETZT**, finale CI offen.

### REG-068 — Backup wird während Aktualisierung beschädigt
- Vertrag: auch `.bak` wird über temporäre Datei + fsync + `os.replace` erneuert; stale eigene Tempdatei wird entfernt.
- Status: **UMGESETZT**.

### REG-069 — ConfigStore driftet vom allgemeinen Persistenzvertrag
- Vertrag: Konfiguration nutzt `AtomicJsonStore` statt eigener Kopie der Schreiblogik.
- Status: **UMGESETZT**.

### REG-070 — Hauptbackend akzeptiert schwächeren Hostvertrag als Hilfsserver
- Vertrag: zentraler `app.loopback_security`-Vertrag; Host muss Loopback **mit exakt passendem Port** sein, Cross-Port-Origin wird blockiert.
- Test: `tests/test_server.py`.
- Status: **UMGESETZT**.

### REG-071 — Kalender/Termine zeigen nach Ladefehler alte oder scheinbar leere Daten
- Vertrag: fehlgeschlagener Monatsreload setzt `state.calendar=null`; kommende Termine analog auf `state.upcoming=null`. Die Oberfläche zeigt **nicht verfügbar** statt alte Daten oder ein falsches „keine Termine“.
- Test: `test_failed_loads_do_not_reuse_stale_or_fake_empty_data`.
- Status: **UMGESETZT**.

### REG-072 — alter TODO-Aktionsfehler hält Dashboard auf „teilweise“
- Vertrag: erfolgreicher Retry löscht `todo-action` vor Refresh.
- Test: `test_successful_todo_retry_clears_action_error`.
- Status: **UMGESETZT**.

### REG-073 — Oberfläche scheitert beim Boot ohne eindeutiges sichtbares Feedback
- Vertrag: Boot-Guard besitzt expliziten READY- und ERROR-Pfad; Top-Level-Bootfehler wird abgefangen.
- Test: `test_boot_guard_has_success_and_failure_paths`.
- Status: **UMGESETZT**.

### REG-074 — Theme-/Modulzustand nur farblich bzw. über CSS-Klasse erkennbar
- Vertrag: Auswahlbuttons synchronisieren `.selected` **und** `aria-pressed`; High Contrast bleibt eigener harter Modus.
- Status: **UMGESETZT**.

### REG-075 — Helper-UIs benötigen Inline-CSS/DOM-innerHTML
- Vertrag: gemeinsames `web/helper-ui.css`, CSP `style-src 'self'`, keine Inline-Styles, keine dynamische `innerHTML`-Erzeugung, gültiger Download-Link statt verschachtelter Interaktion.
- Test: `tests/test_helper_ui_contract.py`.
- Status: **UMGESETZT**.

### REG-076 — Browser-Acceptance hängt an alter Contract-Query und verliert Produktassets
- Auslöser: Dashboard wurde auf `dashboard-v2.3` erhöht, der Harness ersetzte aber nur die fest kodierte v2.2-Signatur; `acceptance.css` wurde ebenfalls nicht eingebettet.
- Wirkung: beide Browser meldeten gleichzeitig fehlende Rasterspannen, zu kleine Ziele, 1-spaltigen Kalender und Boot-Timeout.
- Vertrag: lokale Stylesheets werden aus dem aktuellen `index.html` abgeleitet und nur über Allowlist eingebettet; Fixture-Skript wird **vor** Produkt-JavaScript eingefügt; verbleibende lokale Assetreferenzen blockieren den Test.
- Test: `tests/test_ui_acceptance_harness.py`.
- Status: **UMGESETZT**, erneuter Chromium-/Firefox-Nachweis offen.

### REG-077 — mehrfaches „Neu prüfen“ oder Theme-Klicken erzeugt konkurrierende UI-Aktionen
- Vertrag: Refresh und Config-Speichern laufen single-flight. Währenddessen werden konkurrierende Controls gesperrt und mit `aria-busy` markiert.
- Test: `test_refresh_has_single_flight_busy_feedback`, `test_config_save_is_serialized_and_rolls_back_preview_on_failure`.
- Status: **UMGESETZT**.

### REG-078 — lokales Backend antwortet nicht und Oberfläche bleibt unbegrenzt in Zwischenzustand
- Vertrag: API-Anfragen besitzen einen begrenzten 8-Sekunden-Timeout. Timeout und Nichterreichbarkeit liefern verständliche Hinweise auf die Startkonsole.
- Test: `test_requests_have_timeout_and_clear_user_guidance`.
- Status: **UMGESETZT**.

### REG-079 — fehlgeschlagene TODO-/Ereignis-/Terminabfrage wird wie „keine Daten vorhanden“ dargestellt
- Vertrag: `null` bedeutet technisch **nicht verfügbar**; `[]` bedeutet erfolgreich geladen und leer. Renderfunktionen unterscheiden beide Zustände sichtbar.
- Test: `test_failed_loads_do_not_reuse_stale_or_fake_empty_data`.
- Status: **UMGESETZT**.

### REG-080 — Theme-Vorschau bleibt nach gescheitertem Speichern optisch aktiv
- Vertrag: Darstellung darf sofort als Vorschau reagieren, muss bei Config-Fehler aber auf die vorherige bestätigte Konfiguration zurückrollen und den Fehlerstatus anzeigen.
- Test: `test_config_save_is_serialized_and_rolls_back_preview_on_failure`.
- Status: **UMGESETZT**.

## Aktuelle Evidenzgrenze

- `0.5.0-native-acceptance-safe-file-sim`: **BEWIESEN L0–L3**, Main-CI `33040664746`.
- `0.5.1-audit-modern-ui`: **UMGESETZT / DEVELOPMENT**. Noch keine TESTED-Promotion vor vollständigem Core-/Release- und Chromium-/Firefox-Gate.
- Native Kubuntu L4 bleibt separat offen.
- SAFE-FILE echte Mutation bleibt technisch gesperrt.

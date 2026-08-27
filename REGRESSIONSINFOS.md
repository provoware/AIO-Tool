# REGRESSIONSINFOS

## Zweck

**Bestätigter Fehler → reproduzierbarer Test → Fix → erneute Prüfung → Learning Memory falls strukturell → dauerhaftes Gate.**

Status: OFFEN / UMGESETZT / GEPRÜFT / BEWIESEN.

## Bestehende Kernverträge

- **REG-001:** DONE erst nach sicherer Persistenz — offen für Job-System.
- **REG-002:** reine Prüfung darf Setup nicht entwerten — offen für Wizard.
- **REG-003:** unterbrochener Job darf nicht als laufend erscheinen — offen für Job-System.
- **REG-004:** Prüfung bleibt seiteneffektfrei — GEPRÜFT.
- **REG-005:** Mehrfachstart erzeugt kein zweites Backend — umgesetzt, Zielsystemtest offen.
- **REG-006:** Laienmodus bleibt schlank — umgesetzt, Browser-/Zoom-Gate offen.
- **REG-007:** keine unsichtbare Dateiänderung — verpflichtend für SAFE-FILE-CORE.
- **REG-008:** endgültiges Löschen nie Standard — verpflichtend für SAFE-FILE-CORE.
- **REG-009/010:** Fremdhost/Fremd-Origin blockiert — GEPRÜFT.
- **REG-011:** beschädigte Persistenz → Backup-Fallback/Integritätsfehler — GEPRÜFT.
- **REG-012:** lokale Runtime/Nutzerdaten nicht im Release — GEPRÜFT.
- **REG-013:** Test-/Release-Status nur mit Evidenz — GEPRÜFT.
- **REG-014:** VERSION/Registry-Drift erkennen — GEPRÜFT; CHANGELOG/MANIFEST-Drift später erweitern.
- **REG-015:** erledigtes TODO archivieren statt löschen — GEPRÜFT.
- **REG-016:** TODO-Titelgedächtnis ohne case-sensitive Dubletten — GEPRÜFT.
- **REG-017:** sichtbares Event braucht verständlichen Text — GEPRÜFT.
- **REG-018:** frische Installation behält getrackte Versionshistorie — GEPRÜFT.
- **REG-019:** Nutzerfehler 400, Persistenz-/Integritätsfehler 500 — GEPRÜFT.

## Robustheitsregressionen 0.2.1

- **REG-020:** Musterdatei driftet vom Validator weg — GEPRÜFT.
- **REG-021:** negative Testdaten werden versehentlich akzeptiert — GEPRÜFT.
- **REG-022:** Fehlerhilfe erkennt spezialisierte Unterklasse nicht — BEWIESEN; Matcher nutzt Exception-MRO.
- **REG-023:** Fehlerhilfe behauptet unsichere automatische Recovery — GEPRÜFT.
- **REG-024:** wiederkehrende sichtbare Texte driften auseinander — GEPRÜFT.
- **REG-025:** bestätigte Entwicklungslektion geht verloren — GEPRÜFT.
- **REG-026:** sekundärer Eventfehler zerstört bereits gespeichertes TODO — GEPRÜFT.

## Kalenderregressionen 0.3.0

### REG-027 — Kalender-Endzeit liegt vor oder gleich Startzeit

- **Risiko:** widersprüchlicher Termin kann später Sortierung/Anzeige/Reminder verfälschen.
- **Vertrag:** Endzeit ist nur mit Startzeit erlaubt und muss strikt danach liegen.
- **Tests:** `test_end_time_must_follow_start_time`, Kalender-Negativfixture `calendar.end-before-start.v1.json`.
- **Status:** GEPRÜFT in Run `33026180855`.

### REG-028 — Reminder ohne Startzeit

- **Risiko:** Erinnerung besitzt keinen eindeutigen Triggerzeitpunkt.
- **Vertrag:** nichtleere Reminderliste benötigt eine Startzeit.
- **Tests:** `test_reminder_requires_start_time`, `test_calendar_reminder_without_time_is_rejected`.
- **Status:** GEPRÜFT.

### REG-029 — Reminder wird bei jedem Poll erneut ausgeliefert

- **Risiko:** Nutzer erhält wiederholt dieselbe Erinnerung.
- **Vertrag:** fällige Reminder werden nur bis zur atomaren Quittierung geliefert; danach ist `notified_at` gesetzt.
- **Tests:** `test_due_reminder_is_acknowledged_and_not_returned_again`, API-Test `test_due_reminder_can_be_acknowledged`.
- **Learning:** `LRN-008`.
- **Status:** GEPRÜFT.

### REG-030 — zukünftiger Termin verwendet falschen UTC-Offset nach DST-Wechsel

- **Risiko:** Reminder verschiebt sich nach Sommer-/Winterzeitwechsel um eine Stunde.
- **Vertrag:** lokale Kalenderberechnungen verwenden die echte System-IANA-Zeitzone via `zoneinfo`, nicht den aktuellen Offset als festen tzinfo-Wert.
- **Test:** `test_zoneinfo_uses_target_date_dst_offset`.
- **Learning:** `LRN-007`.
- **Status:** GEPRÜFT.

### REG-031 — unbekannte Zeitzonenbetriebsart wird still normalisiert

- **Vertrag:** aktuell ist nur `timezone: "local"` gültig; unbekannte Werte werden abgelehnt statt still umgeschrieben.
- **Test:** `test_unknown_timezone_mode_is_rejected`.
- **Status:** GEPRÜFT.

### REG-032 — Kalender verweist auf nicht vorhandenes TODO

- **Vertrag:** TODO-Link ist optional; wenn angegeben, muss die ID im TODO-Store existieren.
- **Test:** `test_todo_link_is_optional_but_must_exist_when_supplied`.
- **Status:** GEPRÜFT.

### REG-033 — Wochenansicht beginnt am falschen Wochentag

- **Vertrag:** Wochenperiode ist Montag bis Sonntag.
- **Test:** `test_week_view_is_monday_to_sunday`.
- **Status:** GEPRÜFT.

### REG-034 — harte Testversionsnummer driftet von versionierter Quelldatei

- **Gefundener Fehler:** erster Kalender-Gesamtlauf erwartete `rules_version=1.0.0`, obwohl die versionierte Regeldatei korrekt `1.1.0` deklarierte.
- **Vertrag:** Metadaten-API-Test vergleicht gegen die jeweilige Quelldatei und pflegt keine zweite manuelle Versionswahrheit.
- **Test:** `test_help_metadata_is_versioned`.
- **Learning:** `LRN-009`.
- **Status:** BEWIESEN durch roten Run `33025857246` und grünen Fixlauf `33026180855`.

### REG-035 — sichtbare Reminderanzeige quittiert zu früh

- **Risiko:** Backend markiert Reminder als angezeigt, obwohl Browser/UI ihn nie sichtbar dargestellt hat.
- **Vertrag:** Core liefert fällige Reminder getrennt; Quittierung erfolgt erst nach erfolgreicher UI-Darstellung.
- **Status:** OFFEN für Dashboard V2; Core-Schnittstelle ist vorbereitet.

## Nachweise

- Foundation 0.1.1 — Run `33020484403`: SUCCESS.
- Core 0.2.0 — finaler Kandidat Run `33022569880`: SUCCESS; Merge `a110132acc4104e0f0c48c736a3fd4bc98a9c290`.
- Robustness 0.2.1 — finaler Head Run `33025238585`: SUCCESS; Merge `eec9698d49719579633fc54e6f83eb4fc6834668`.
- Calendar 0.3.0 — erster Gesamtstand Run `33025857246`: FAILURE durch REG-034.
- Calendar 0.3.0 — korrigierter Codehead Run `33026180855`: **SUCCESS**.

Im grünen Kalenderlauf erfolgreich: Python-Syntax, 69 Unit-/Integrationstests, Foundation-/Kalender-Validierung, Learning Guard, Launcher, JavaScript, Release-Builder und Release-ZIP-Upload.

## Release-Gate

`0.3.0-calendar-core` ist automatisiert GEPRÜFT, bleibt `draft`. Reale Kubuntu-/Firefox-/Chrome-/Zoom-Gates und sichtbare Reminderanzeige bleiben offen.

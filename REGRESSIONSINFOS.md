# REGRESSIONSINFOS

## Grundsatz

**Bestätigter Fehler → reproduzierbarer Test → minimaler Fix → erneute Prüfung → Learning Memory falls strukturell → dauerhaftes Gate.**

Status: OFFEN / UMGESETZT / GEPRÜFT / BEWIESEN.

## Bestehende Verträge REG-001 bis REG-035

Die bisherigen Foundation-, Persistenz-, Versions-, TODO-, Fehlerhilfe- und Kalenderverträge bleiben unverändert verbindlich. Besonders relevant für Dashboard V2:

- REG-006 Laienmodus bleibt schlank.
- REG-009/010 Fremdhost/Fremd-Origin blockiert.
- REG-017 sichtbares Event braucht verständlichen Text.
- REG-024 wiederkehrende sichtbare Texte zentral/versioniert.
- REG-029 Reminder nach Quittierung nicht erneut ausliefern.
- REG-030 zukünftige lokale Zeit via `zoneinfo`/DST.
- REG-034 keine redundanten hart codierten Metadatenversionen.
- REG-035 Reminderanzeige darf nicht vor tatsächlicher Sichtbarkeit quittieren.

## Dashboard-V2-Regressionen

### REG-036 — Dashboard quittiert Reminder durch Polling

- **Risiko:** Reminder gilt als gesehen, obwohl Nutzer ihn nie wahrgenommen hat.
- **Vertrag:** GET/Polling bleibt rein lesend; ACK nur über sichtbaren Reminder und expliziten Button `Gesehen`.
- **Tests:** `test_reminders_are_not_acknowledged_while_page_is_hidden`, statischer ACK-Vertrag.
- **Status:** GEPRÜFT in Run `33026823914`.

### REG-037 — unsichtbarer Tab quittiert Reminder

- **Vertrag:** `document.visibilityState !== 'visible'` blockiert Reminder-Poll/ACK.
- **Test:** Dashboard-Vertragstest prüft Visibility-Guard und `aria-live=assertive`.
- **Status:** GEPRÜFT.

### REG-038 — Dashboard-Textschlüssel fehlt oder driftet

- **Risiko:** Oberfläche zeigt Schlüssel/Leertext oder widersprüchliche Formulierungen.
- **Vertrag:** `web/dashboard-texts.de.v1.json` ist versioniert; alle sichtbaren `data-i18n`-Schlüssel müssen existieren und nichtleer sein.
- **Test:** `test_dashboard_text_catalog_is_versioned_german_and_complete`; zusätzliche Prüfung in `scripts/validate.py`.
- **Status:** GEPRÜFT.

### REG-039 — zentraler Dashboardbereich verschwindet unbemerkt

- **Vertrag:** Monatskalender, TODO-Liste, Ereignisse, Reminderregion, Systemstatus, Entwickler- und Einstellungsbereich sind statisch verpflichtend.
- **Test:** `test_required_dashboard_regions_exist` + Foundation-Validierung.
- **Status:** GEPRÜFT.

### REG-040 — UI dupliziert Backend-Domänenlogik

- **Risiko:** Kalender-/TODO-/Reminder-Regeln laufen zwischen Python und JavaScript auseinander.
- **Vertrag:** Dashboard nutzt getestete Core-API; Kalenderperioden, TODO-Reihenfolge, Reminder-Fälligkeit und Persistenz bleiben Backend-Aufgabe.
- **Test:** `test_dashboard_uses_tested_core_api_contracts`.
- **Status:** GEPRÜFT für API-Vertragsnutzung; Architekturreview bleibt fortlaufend.

### REG-041 — Nutzertitel werden als HTML interpretiert

- **Risiko:** fehlerhafte Darstellung bzw. HTML-Injektion aus lokal gespeicherten Titeln.
- **Vertrag:** Termin-/TODO-Titel über `textContent` einsetzen.
- **Test:** `test_user_titles_are_inserted_as_text_not_html`.
- **Status:** GEPRÜFT.

### REG-042 — Diagnose gibt unnötige Nutzerdaten aus

- **Vertrag:** Entwicklerdiagnose zeigt technischen Zustand, aber keine vollständige Config, `active_project` oder Favoritenliste.
- **Test:** `test_diagnostics_do_not_dump_full_config`.
- **Status:** GEPRÜFT.

### REG-043 — responsive/A11y-Schutz verschwindet

- **Vertrag:** Skip-Link, sichtbarer Tastaturfokus, Reduced-Motion-Regel und Mobile-Breakpoints bleiben vorhanden.
- **Test:** `test_responsive_and_accessibility_guards_are_present`.
- **Status:** GEPRÜFT statisch; reale Browser-/Zoom-/Tastaturabnahme noch OFFEN.

### REG-044 — Monatsraster startet nicht Montag

- **Vertrag:** sichtbare Wochentage Mo–So; JS richtet den ersten Kalendertag mit `(getDay()+6)%7` auf Montag aus.
- **Test:** `test_month_calendar_is_monday_to_sunday`.
- **Status:** GEPRÜFT.

## Nachweise

- Foundation: `33020484403` SUCCESS.
- Core: `33022569880` SUCCESS.
- Robustness: `33025238585` SUCCESS.
- Calendar final: `33026380907` SUCCESS; Merge `a5a4290f5d13333498b0e051b1fcd94e24cc8e95`.
- Dashboard V2 Code-Gate: `33026823914` **SUCCESS**.

Dashboard-Code-Gate: **77 Tests**, Foundation-/Dashboard-Validierung, 9 aktive Learning-Memory-Regeln, Launcher, JavaScript, Release-Builder und ZIP-Upload erfolgreich.

## Noch offene reale Regression-Gates

- Kubuntu Klick-&-Start aus sauber entpacktem ZIP.
- Firefox und Chrome/Chromium.
- 100/125/150/175/200 % Zoom.
- Tastaturdurchlauf und Fokusreihenfolge.
- kleine / Full-HD / große Displays.

Diese Punkte dürfen nicht aus statischer CI als bestanden abgeleitet werden.

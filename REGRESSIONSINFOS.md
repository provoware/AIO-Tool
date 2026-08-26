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

### REG-020 — Musterdatei driftet vom Validator weg

- **Risiko:** Hilfe verweist auf eine veraltete oder ungültige Vorlage.
- **Vertrag:** alle Referenzvorlagen werden von denselben Validatoren wie Produktdaten geprüft.
- **Tests:** `test_reference_templates_match_current_validators`, `test_valid_testdata_uses_same_contracts`.
- **Status:** GEPRÜFT in Run `33024919165`.

### REG-021 — Negative Testdaten werden versehentlich akzeptiert

- **Vertrag:** bekannte ungültige Fälle bleiben reproduzierbar ungültig.
- **Beispiele:** unbekanntes Theme, korruptes JSON, doppelte Version, leere Eventmeldung, doppeltes TODO-Titelgedächtnis.
- **Tests:** `tests/test_templates.py`.
- **Status:** GEPRÜFT.

### REG-022 — Fehlerhilfe erkennt spezialisierte Unterklasse nicht

- **Gefundener Fehler:** `ConfigIntegrityError` wurde zunächst nicht als Integritätsfamilie erkannt, weil nur der exakte Klassenname verglichen wurde.
- **Fix:** Matcher prüft die vollständige Exception-Klassenhierarchie (`mro`).
- **Test:** `test_subclass_inherits_parent_error_rule` plus API-Integritätstest.
- **Learning:** LRN-002 / hierarchische Fehlerfamilien werden als Strukturvertrag behandelt.
- **Status:** BEWIESEN durch roten Erstlauf `33024839956` und grünen Fixlauf `33024919165`.

### REG-023 — Fehlerhilfe behauptet unsichere automatische Recovery

- **Vertrag:** unbekannte Fehler haben `retry_safe=false`; Mustervorlagen werden nur empfohlen, nie automatisch über Nutzerdaten geschrieben.
- **Tests:** `test_unknown_error_falls_back_without_claiming_recovery`, Template-Pfadvalidierung.
- **Status:** GEPRÜFT.

### REG-024 — wiederkehrende sichtbare Texte driften auseinander

- **Vertrag:** wiederverwendete Core-Systemtexte liegen versioniert im Textkatalog; fehlende Schlüssel sind Fehler statt still erfundener Fallback.
- **Tests:** `tests/test_text_catalog.py`.
- **Status:** GEPRÜFT.

### REG-025 — bestätigte Entwicklungslektion geht verloren

- **Vertrag:** `LEARNING_MEMORY.jsonl` enthält eindeutige, validierte Lektionen; CI führt `scripts/learning_guard.py` aus.
- **Tests:** `tests/test_learning_memory.py` + Learning-Guard-CI.
- **Status:** GEPRÜFT.

### REG-026 — sekundärer Eventfehler zerstört bereits gespeichertes TODO

- **Vertrag:** Hauptaktion bleibt erfolgreich, Ereignisfehler wird als Warnung zurückgegeben.
- **Test:** `test_todo_survives_broken_event_log_and_returns_warning`.
- **Status:** GEPRÜFT.

## Nachweise

- Foundation 0.1.1 — Run `33020484403`: SUCCESS.
- Core 0.2.0 — finaler Kandidat Run `33022569880`: SUCCESS; Merge `a110132acc4104e0f0c48c736a3fd4bc98a9c290`.
- Robustness 0.2.1 — erster Lauf `33024839956`: FAILURE, dadurch REG-022 entdeckt.
- Robustness 0.2.1 — korrigierter Lauf `33024919165`: **SUCCESS**.

Im grünen Robustheitslauf erfolgreich: Python-Syntax, 49 Unit-/Integrationstests, Validierung, Learning Guard, Launcher, JavaScript, Release-Builder und Release-ZIP-Upload.

## Release-Gate

`0.2.1-robustness` ist automatisiert GEPRÜFT, aber nur `draft`. Reale Kubuntu-/Firefox-/Chrome-/Zoom-Gates bleiben offen.

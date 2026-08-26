# REGRESSIONSINFOS

## Zweck

Diese Datei hält bekannte Fehlerklassen und dauerhafte Schutzverträge fest.

**Bestätigter Fehler → reproduzierbarer Test oder Prüfevidenz → Fix → erneute Prüfung → dauerhaftes Gate.**

## Statusdefinitionen

- **OFFEN** – Fehler bekannt, noch nicht behoben.
- **UMGESETZT** – Schutz/Fix im Code vorhanden, aber noch nicht vollständig ausgeführt geprüft.
- **GEPRÜFT** – vorgesehene Prüfung wurde erfolgreich ausgeführt.
- **BEWIESEN** – reproduzierbare Evidenz und dauerhaftes Gate vorhanden.

## Verbindliche Regressionsthemen

### REG-001 — Abschlussstatus vor Persistenz
- **Vertrag:** persistent schreiben und verifizieren; erst danach DONE melden.
- **Status:** OFFEN FÜR JOB-SYSTEM.

### REG-002 — Setup/Wizard durch harmlose Prüfung entwertet
- **Vertrag:** reine Prüfung darf gültigen Setup-Zustand nicht zerstören.
- **Status:** OFFEN FÜR WIZARD-SLICE.

### REG-003 — Unterbrochener Job erscheint nach Neustart als laufend
- **Vertrag:** unvollständige Jobs als `unterbrochen` rekonstruieren.
- **Status:** OFFEN FÜR JOB-SYSTEM.

### REG-004 — Prüfoperation verändert Konfiguration
- **Vertrag:** reine Prüfungen bleiben seiteneffektfrei.
- **Status:** GEPRÜFT.

### REG-005 — Mehrfachstart erzeugt mehrere Backends
- **Vertrag:** valide laufende Instanz öffnen statt zweite starten.
- **Status:** UMGESETZT; Zielsystemtest offen.

### REG-006 — Laienmodus durch Zusatzoptionen überladen
- **Vertrag:** Expertenoptionen verborgen; Auswahl vor Zeicheneingabe.
- **Status:** UMGESETZT; Browser-/Zoom-Gate offen.

### REG-007 — Unsichtbare Dateiänderung
- **Vertrag:** verändernde Dateioperation braucht Vorschau, Quelle/Ziel, Konflikte und Nachprüfung.
- **Status:** verpflichtend für SAFE-FILE-CORE.

### REG-008 — endgültiges Löschen als Standard
- **Vertrag:** Papierkorb/Recovery vor endgültigem Löschen.
- **Status:** verpflichtend für SAFE-FILE-CORE.

### REG-009 — Fremder Host erreicht lokales Backend
- **Vertrag:** nur Loopback/localhost.
- **Status:** GEPRÜFT.

### REG-010 — Fremde Origin schreibt lokale Daten
- **Vertrag:** mutierende Endpunkte nur mit lokalem Host-/Origin-Vertrag.
- **Status:** GEPRÜFT.

### REG-011 — Beschädigte Hauptpersistenz
- **Vertrag:** atomare Hauptdatei + Backup-Fallback.
- **Tests:** Config-Backup-Test, `test_roundtrip_and_backup_fallback`.
- **Status:** GEPRÜFT.

### REG-012 — Release enthält lokale Nutzerdaten
- **Vertrag:** Runtime, venv, Caches und lokale Daten aus Release ausschließen.
- **Status:** GEPRÜFT durch Release-Builder-CI.

### REG-013 — Version ohne Evidenz als getestet/freigegeben
- **Vertrag:** `tested`, `release-candidate`, `released` benötigen Evidenz.
- **Test:** `test_tested_status_requires_evidence`.
- **Status:** GEPRÜFT.

### REG-014 — VERSION und Registry driften auseinander
- **Vertrag:** `VERSION_REGISTRY.json` und `VERSION` müssen dieselbe aktuelle Version führen; lokale Registry übernimmt den Seed.
- **Tests:** `test_consistency_detects_version_drift`, Core-Validierung.
- **Status:** GEPRÜFT für VERSION/Registry; CHANGELOG/MANIFEST-Drift folgt später.

### REG-015 — Erledigtes TODO wird gelöscht
- **Vertrag:** ins Archiv verschieben, `created_at` behalten, `completed_at` ergänzen.
- **Test:** `test_complete_moves_item_to_archive_with_timestamp`.
- **Status:** GEPRÜFT.

### REG-016 — TODO-Titel wird nicht wieder angeboten oder doppelt gespeichert
- **Vertrag:** case-insensitive zusammenführen, Nutzung zählen, wieder anbieten.
- **Test:** `test_title_memory_counts_and_reoffers_titles`.
- **Status:** GEPRÜFT.

### REG-017 — Event ohne verständlichen Text
- **Vertrag:** nichtleerer menschenlesbarer `message`-Text; technische Details getrennt.
- **Tests:** `test_message_must_be_human_readable_nonempty_text`, `test_latest_returns_newest_first`.
- **Status:** GEPRÜFT; sichtbare Dashboard-Darstellung folgt.

### REG-018 — Frische Installation verliert Versionshistorie
- **Vertrag:** `VERSION_REGISTRY.json` ist getrackte Historie und Seed für frische Runtime.
- **Tests:** `test_seed_preserves_history_before_runtime_file_exists`; `scripts/validate.py` prüft Historie und `VERSION`-Übereinstimmung.
- **Status:** GEPRÜFT in GitHub Actions Run `33022569880`.

### REG-019 — Persistenzfehler wird als Nutzerfehler gemeldet
- **Vertrag:** ungültige Parameter/Eingaben → 400; beschädigte Persistenz → 500/Integritätsmeldung.
- **Tests:** `test_invalid_limit_is_client_error`, `test_corrupted_event_registry_is_server_integrity_error`, `test_invalid_theme_is_client_error`, `test_corrupted_config_is_server_integrity_error`.
- **Status:** GEPRÜFT in GitHub Actions Run `33022569880`.

## Testklassen für Releases

Mindestens je nach Slice prüfen: Normalfall, ungültige Eingabe, Berechtigungsfehler, vorhandenes Ziel, Speicherknappheit, Abbruch, Neustart, beschädigte Persistenz, Recovery, Browser-Reload, große/leere Datenmenge, Mehrfachstart, Zoom/Kontrast/Tastatur, Fremdhost/Origin, Release-Ausschlüsse, Schema-/Versionsdrift, Archivierung, Vorschlagsgedächtnis, menschenlesbare Events, frische Versionshistorie und korrekte HTTP-Fehlerklasse.

## Nachweise

- Foundation 0.1.1 — Run `33020484403`: **SUCCESS**.
- Core 0.2.0 — Run `33022404071`: **SUCCESS**.
- Finaler Core-Merge-Kandidat inkl. REG-018/019 — Run `33022569880`: **SUCCESS**.

Erfolgreiche Gates: Python-Syntax, Unit-/Integrationstests, Core-Validierung, Launcher-Syntax, JavaScript-Syntax und Release-Builder.

## Release-Gate

`0.2.0-core` ist automatisiert **GEPRÜFT**, aber nur **draft**. Reale Kubuntu-/Firefox-/Chrome-/Zoom-Gates bleiben offen und dürfen nicht aus CI-Erfolg abgeleitet werden.

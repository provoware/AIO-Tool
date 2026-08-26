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
- **Risiko:** UI meldet DONE, obwohl Abschlusszustand noch nicht sicher gespeichert wurde.
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
- **Status:** GEPRÜFT durch Foundation-CI.

### REG-005 — Mehrfachstart erzeugt mehrere Backends
- **Vertrag:** Start ist idempotent; valide laufende Instanz öffnen statt zweite starten.
- **Status:** UMGESETZT; Zielsystemtest offen.

### REG-006 — Einfache Bedienung wird durch Zusatzoptionen überladen
- **Vertrag:** Expertenoptionen standardmäßig verborgen; Auswahl vor Zeicheneingabe.
- **Status:** UMGESETZT; Browser-/Zoom-Gate offen.

### REG-007 — Unsichtbare Dateiänderung
- **Vertrag:** verändernde Dateioperation benötigt Vorschau, Quelle/Ziel, Konflikte und Nachprüfung.
- **Status:** verpflichtend für SAFE-FILE-CORE.

### REG-008 — endgültiges Löschen als Standard
- **Vertrag:** Papierkorb/Recovery vor endgültigem Löschen.
- **Status:** verpflichtend für SAFE-FILE-CORE.

### REG-009 — Fremder Host erreicht lokales Backend
- **Vertrag:** nur `127.0.0.1`/`localhost` akzeptieren.
- **Status:** GEPRÜFT durch Foundation-CI.

### REG-010 — Fremde Origin schreibt lokale Daten
- **Vertrag:** mutierende Endpunkte nur unter lokalem Origin-/Host-Vertrag.
- **Status:** GEPRÜFT; neue TODO-Endpunkte verwenden denselben Guard.

### REG-011 — Beschädigte Hauptpersistenz macht Tool unbrauchbar
- **Vertrag:** atomare Hauptdatei und gültiges Backup als Fallback.
- **Schutz:** ConfigStore + `AtomicJsonStore`.
- **Tests:** Config-Backup-Test und `test_roundtrip_and_backup_fallback`.
- **Status:** GEPRÜFT im Core-CI-Lauf `33022404071`; zusätzliche direkte API-Integritätstests im finalen Head.

### REG-012 — Release enthält lokale Nutzerdaten
- **Vertrag:** Release-Builder schließt Runtime, venv, Caches und lokale Nutzerdaten aus.
- **Status:** GEPRÜFT durch CI-Release-Builder.

### REG-013 — Version wird ohne Evidenz als getestet/freigegeben markiert
- **Vertrag:** `tested`, `release-candidate` und `released` benötigen Evidenz.
- **Test:** `test_tested_status_requires_evidence`.
- **Status:** GEPRÜFT im Core-CI-Lauf `33022404071`.

### REG-014 — VERSION und Registry driften auseinander
- **Vertrag:** getrackte `VERSION_REGISTRY.json` muss dieselbe aktuelle Version wie `VERSION` führen; lokale Registry übernimmt diese Historie.
- **Schutz:** `VersionRegistry.consistency()` + `scripts/validate.py`.
- **Test:** `test_consistency_detects_version_drift`.
- **Status:** GEPRÜFT für VERSION/Registry; CHANGELOG/MANIFEST-Drift folgt später.

### REG-015 — Erledigtes TODO wird gelöscht statt archiviert
- **Vertrag:** Abhaken verschiebt vollständigen Eintrag ins Archiv, erhält `created_at` und ergänzt `completed_at`.
- **Test:** `test_complete_moves_item_to_archive_with_timestamp`.
- **Status:** GEPRÜFT im Core-CI-Lauf `33022404071`.

### REG-016 — Wiederkehrender TODO-Titel wird nicht wieder angeboten oder doppelt gespeichert
- **Vertrag:** Titel case-insensitive zusammenführen, Nutzung zählen und wieder anbieten.
- **Test:** `test_title_memory_counts_and_reoffers_titles`.
- **Status:** GEPRÜFT im Core-CI-Lauf `33022404071`.

### REG-017 — Eventanzeige enthält keinen verständlichen Ereignistext
- **Vertrag:** jedes Event braucht einen nichtleeren menschenlesbaren `message`-Text; technische Details bleiben getrennt.
- **Tests:** `test_message_must_be_human_readable_nonempty_text`, `test_latest_returns_newest_first`.
- **Status:** GEPRÜFT im Core-CI-Lauf `33022404071`; sichtbare Dashboard-Darstellung folgt später.

### REG-018 — Frische Installation verliert die Versionshistorie
- **Risiko:** eine rein lokale Registry kennt nach Neuinstallation nur die aktuelle Version.
- **Vertrag:** `VERSION_REGISTRY.json` ist getrackte Projekt-Historie und Seed für eine frische Runtime.
- **Schutz:** `VersionRegistry(default=...)`; Seed wird vor Verwendung validiert.
- **Tests:** `test_seed_preserves_history_before_runtime_file_exists`; `scripts/validate.py` prüft Historie und `VERSION`-Übereinstimmung.
- **Status:** UMGESETZT; finaler CI-Head abzunehmen.

### REG-019 — Persistenzfehler wird als Nutzerfehler gemeldet
- **Risiko:** beschädigte lokale Daten erscheinen als HTTP 400 und suggerieren falsche Bedienung.
- **Vertrag:** ungültige Parameter/Eingaben → 400; beschädigte lokale Persistenz → 500 mit Integritätsmeldung.
- **Schutz:** `RequestError`, `ConfigIntegrityError` und getrennte Server-Fehlerpfade.
- **Tests:** `test_invalid_limit_is_client_error`, `test_corrupted_event_registry_is_server_integrity_error`, `test_invalid_theme_is_client_error`, `test_corrupted_config_is_server_integrity_error`.
- **Status:** UMGESETZT; finaler CI-Head abzunehmen.

## Testklassen für Releases

Je nach Slice mindestens prüfen:

1. Normalfall.
2. ungültige Eingabe.
3. fehlende Berechtigung.
4. Ziel existiert bereits.
5. unzureichender Speicher.
6. Abbruch während Aktion.
7. Prozess-/Toolneustart.
8. beschädigte Persistenzdatei.
9. Wiederaufnahme/Recovery.
10. Browser-Neuladen während aktivem Job.
11. große Datenmenge.
12. leere Datenmenge.
13. Mehrfachstart.
14. Zoom/Kontrast/Tastatur.
15. Fremdhost/Fremd-Origin.
16. Release auf lokale Daten/Caches prüfen.
17. Schema-/Versionsdrift.
18. Archivierung statt Datenverlust.
19. Vorschlagsgedächtnis ohne Dubletten.
20. menschenlesbare Eventtexte.
21. getrackte Historie auf frischer Runtime.
22. korrekte HTTP-Fehlerklasse für Nutzer- vs. Integritätsfehler.

## Nachweise

### Foundation 0.1.1

GitHub Actions Run `33020484403`: SUCCESS.

### Core 0.2.0

GitHub Actions Run `33022404071`: SUCCESS für Python-Syntax, Unit-/Integrationstests, Core-Validierung, Launcher, JavaScript und Release-Builder.

Die danach ergänzten direkten Regressionstests für REG-018/REG-019 müssen im finalen Branch-Head erneut grün sein, bevor gemergt wird.

## Release-Gate

Ein Release mit bekanntem P0/P1-Regressionsfehler darf nicht als stabil freigegeben werden. Reale Kubuntu-/Browser-Gates bleiben separat offen und dürfen nicht aus CI-Erfolg abgeleitet werden.

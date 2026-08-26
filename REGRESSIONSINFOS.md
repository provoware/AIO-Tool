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
- **Status:** OFFEN FÜR JOB-SYSTEM; noch keine Job-Queue.

### REG-002 — Setup/Wizard durch harmlose Prüfung entwertet

- **Risiko:** gültiger Setup-Zustand wird durch reine Prüfung zerstört.
- **Vertrag:** Prüfungen dürfen gültigen Zustand nicht ohne echte ungültige Voraussetzung zurücksetzen.
- **Status:** OFFEN FÜR WIZARD-SLICE.

### REG-003 — Unterbrochener Job erscheint nach Neustart als laufend

- **Vertrag:** unvollständige Jobs beim Neustart als `unterbrochen` rekonstruieren.
- **Status:** OFFEN FÜR JOB-SYSTEM.

### REG-004 — Prüfoperation verändert Konfiguration

- **Vertrag:** reine Prüfungen bleiben seiteneffektfrei.
- **Schutz:** `scripts/validate.py` arbeitet mit temporären Persistenzdateien.
- **Status:** GEPRÜFT durch Foundation-CI 0.1.1.

### REG-005 — Mehrfachstart erzeugt mehrere Backends

- **Vertrag:** Start ist idempotent; valide laufende Instanz öffnen statt zweite starten.
- **Status:** UMGESETZT; echter Zielsystemtest ausstehend.

### REG-006 — Einfache Bedienung wird durch Zusatzoptionen überladen

- **Vertrag:** Expertenoptionen standardmäßig verborgen; Auswahl vor Zeicheneingabe.
- **Status:** UMGESETZT; Browser-/Zoom-Gate ausstehend.

### REG-007 — Unsichtbare Dateiänderung

- **Vertrag:** jede verändernde Dateioperation benötigt Vorschau, Ziel/Quelle, Konfliktanzeige und Nachprüfung.
- **Status:** verpflichtendes Gate für SAFE-FILE-CORE.

### REG-008 — endgültiges Löschen als Standard

- **Vertrag:** Papierkorb/Recovery vor endgültigem Löschen.
- **Status:** verpflichtendes Gate für SAFE-FILE-CORE.

### REG-009 — Fremder Host erreicht lokales Backend

- **Vertrag:** nur `127.0.0.1`/`localhost` mit richtigem Port akzeptieren.
- **Schutz:** `allowed_host()` und Unit-Test.
- **Status:** GEPRÜFT durch Foundation-CI 0.1.1.

### REG-010 — Fremde Origin schreibt lokale Daten

- **Risiko:** fremde Webseite versucht mutierende API-Aufrufe.
- **Vertrag:** schreibende Endpunkte nur unter lokalem Origin-/Host-Vertrag.
- **Schutz:** TODO-Schreibendpunkte verwenden denselben Host-/Origin-Guard wie Konfiguration.
- **Status:** Foundation-Schutz GEPRÜFT; neue TODO-Endpunkte in `0.2.0-core` erneut per CI zu prüfen.

### REG-011 — Beschädigte Hauptpersistenz macht Tool unbrauchbar

- **Risiko:** abgebrochener Schreibvorgang oder Dateikorruption zerstört lokalen Zustand.
- **Vertrag:** atomare Hauptdatei und gültiges Backup als Fallback.
- **Schutz:** bestehender ConfigStore sowie neuer `AtomicJsonStore` + `tests/test_persistence.py`.
- **Status:** Config GEPRÜFT; neuer gemeinsamer Store UMGESETZT, CI 0.2.0 ausstehend.

### REG-012 — Release enthält lokale Nutzerdaten

- **Vertrag:** Release-Builder schließt Runtime/venv/Caches/Builddaten aus.
- **Status:** GEPRÜFT durch Foundation-CI 0.1.1; mit neuen Runtime-Dateien erneut zu prüfen.

### REG-013 — Version wird ohne Evidenz als getestet/freigegeben markiert

- **Risiko:** Dashboard oder Releaseverwaltung zeigt einen Qualitätsstatus, der nicht belegt ist.
- **Vertrag:** `tested`, `release-candidate` und `released` benötigen mindestens einen Evidenzdatensatz.
- **Schutz:** `VersionRegistry.set_status()` blockiert den Statuswechsel ohne Evidenz.
- **Test:** `test_tested_status_requires_evidence`.
- **Status:** UMGESETZT; CI 0.2.0 ausstehend.

### REG-014 — VERSION und Registry driften auseinander

- **Risiko:** unterschiedliche Versionsanzeigen und falsche Releasezuordnung.
- **Vertrag:** aktuelle Registry-Version muss `VERSION` entsprechen und dort registriert sein.
- **Schutz:** `VersionRegistry.consistency()` + API `/api/versions` + `/api/status`.
- **Test:** `test_consistency_detects_version_drift`.
- **Status:** UMGESETZT; Drift gegen CHANGELOG/MANIFEST folgt später.

### REG-015 — Erledigtes TODO wird gelöscht statt archiviert

- **Risiko:** Verlust von Arbeits- und Verlaufsevidenz.
- **Vertrag:** Abhaken verschiebt den vollständigen Eintrag ins Archiv, erhält `created_at` und ergänzt `completed_at`.
- **Schutz:** `TodoStore.complete()`.
- **Test:** `test_complete_moves_item_to_archive_with_timestamp`.
- **Status:** UMGESETZT; CI 0.2.0 ausstehend.

### REG-016 — Wiederkehrender TODO-Titel wird nicht wieder angeboten oder doppelt gespeichert

- **Risiko:** unnötige Zeicheneingabe und unübersichtliche Vorschläge.
- **Vertrag:** Titel persistent merken, case-insensitive zusammenführen, Nutzung zählen und nach Relevanz anbieten.
- **Schutz:** `title_memory` + `TodoStore.title_suggestions()`.
- **Test:** `test_title_memory_counts_and_reoffers_titles`.
- **Status:** UMGESETZT; CI 0.2.0 ausstehend.

### REG-017 — Eventanzeige zeigt technische Rohdaten statt verständlichem Ereignis

- **Risiko:** rechte Dashboard-Spalte ist für Laien unverständlich.
- **Vertrag:** jedes Event benötigt einen nichtleeren menschenlesbaren `message`-Text; technische Details sind getrennt optional.
- **Schutz:** `EventRegistry` validiert `message`; API liefert neueste Ereignisse zuerst.
- **Tests:** `test_message_must_be_human_readable_nonempty_text`, `test_latest_returns_newest_first`.
- **Status:** UMGESETZT; UI-Darstellung folgt im Dashboard-Slice.

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
14. Zoom/Kontrast/Tastatur bei UI-Änderungen.
15. Fremdhost/Fremd-Origin bei lokaler API.
16. Release auf lokale Daten/Caches prüfen.
17. Schema-/Versionsdrift.
18. Archivierung statt Datenverlust.
19. Vorschlagsgedächtnis ohne Dubletten.
20. menschenlesbare Eventtexte.

## Foundation-Gates 0.1.1

Ausgeführt und grün in GitHub Actions:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate.py
bash -n start_tool.sh
node --check web/app.js
python3 scripts/release.py --check
```

CI-Run für Foundation-Commit `754f1e6a9534eb12503d5191aad0bebf45fa8a6d`: **SUCCESS**.

## Core-Gate 0.2.0

Neue Tests sind implementiert, aber erst nach tatsächlich grünem Pull-Request-CI als **GEPRÜFT** zu markieren.

Noch offen bleiben reale Zielsystem-Gates unter Kubuntu sowie Firefox/Chrome/Chromium.

## Release-Gate

Ein Release mit bekanntem P0/P1-Regressionsfehler darf nicht als stabil freigegeben werden. Ausnahmen müssen ausdrücklich in README, CHANGELOG und hier dokumentiert werden.

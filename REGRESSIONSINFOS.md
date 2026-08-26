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
- **Status:** OFFEN FÜR JOB-SYSTEM; in Foundation noch keine Job-Queue.

### REG-002 — Setup/Wizard durch harmlose Prüfung entwertet

- **Risiko:** gültiger Setup-Zustand wird durch reine Prüfung zerstört.
- **Vertrag:** Prüfungen dürfen gültigen Zustand nicht ohne echte ungültige Voraussetzung zurücksetzen.
- **Status:** OFFEN FÜR WIZARD-SLICE; Foundation enthält noch keinen Setup-Wizard.

### REG-003 — Unterbrochener Job erscheint nach Neustart als laufend

- **Vertrag:** unvollständige Jobs beim Neustart als `unterbrochen` rekonstruieren.
- **Status:** OFFEN FÜR JOB-SYSTEM.

### REG-004 — Prüfoperation verändert Konfiguration

- **Vertrag:** reine Prüfungen bleiben seiteneffektfrei.
- **Foundation-Schutz:** `scripts/validate.py` arbeitet mit temporärer Testkonfiguration und verändert `runtime/config.json` nicht.
- **Status:** UMGESETZT; CI-/Zielsystemevidenz für 0.1.1 noch ausstehend.

### REG-005 — Mehrfachstart erzeugt mehrere Backends

- **Vertrag:** Start ist idempotent; valide laufende Instanz öffnen statt zweite starten.
- **Foundation-Schutz:** `start_tool.sh` prüft `/api/status` vor Backendstart.
- **Status:** UMGESETZT; Zielsystemtest ausstehend.

### REG-006 — Einfache Bedienung wird durch Zusatzoptionen überladen

- **Vertrag:** Expertenoptionen standardmäßig verborgen; Auswahl vor Zeicheneingabe.
- **Foundation-Schutz:** Expertenbereich startet verborgen; Themes/Schriftgröße über Buttons.
- **Status:** UMGESETZT; Browser-/Zoom-Gate ausstehend.

### REG-007 — Unsichtbare Dateiänderung

- **Vertrag:** jede verändernde Dateioperation benötigt Vorschau, Ziel/Quelle, Konfliktanzeige und Nachprüfung.
- **Status:** verpflichtendes P1-Gate für SAFE-FILE-CORE.

### REG-008 — endgültiges Löschen als Standard

- **Vertrag:** Papierkorb/Recovery vor endgültigem Löschen.
- **Status:** verpflichtendes P1-Gate.

### REG-009 — Fremder Host erreicht lokales Backend

- **Risiko:** Browser-/Netzwerkzugriff unter falschem Hostkontext erreicht lokale API.
- **Vertrag:** nur `127.0.0.1`/`localhost` mit richtigem Port akzeptieren.
- **Schutz:** `allowed_host()` und Unit-Test in `tests/test_server.py`.
- **Status:** UMGESETZT; CI-Evidenz ausstehend.

### REG-010 — Fremde Origin schreibt lokale Konfiguration

- **Risiko:** fremde Webseite versucht einen mutierenden API-Aufruf.
- **Vertrag:** schreibende Endpunkte nur mit lokaler Origin oder ohne Browser-Origin im lokalen Werkzeugkontext.
- **Schutz:** `allowed_origin()` + Host-Prüfung + keine CORS-Freigabe.
- **Status:** UMGESETZT; CI-Evidenz ausstehend.

### REG-011 — Beschädigte Hauptkonfiguration macht Tool unbrauchbar

- **Risiko:** abgebrochener Schreibvorgang oder Dateikorruption zerstört Einstellungen.
- **Vertrag:** atomare Hauptdatei; gültiges Backup als Fallback.
- **Schutz:** `ConfigStore.save/load` + `test_backup_fallback`.
- **Status:** UMGESETZT; CI-Evidenz ausstehend.

### REG-012 — Release enthält lokale Nutzerdaten

- **Risiko:** Runtime, `.venv`, Logs oder persönliche Daten gelangen ins ZIP.
- **Vertrag:** Release-Builder schließt Runtime/venv/Caches/Builddaten aus und prüft Ausschlüsse.
- **Schutz:** `scripts/release.py --check` und `.gitignore`.
- **Status:** UMGESETZT; CI-Evidenz ausstehend.

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

## Foundation-Gates 0.1.1

Automatisiert vorgesehen:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate.py
bash -n start_tool.sh
node --check web/app.js
python3 scripts/release.py --check
```

**Wichtig:** Vor Ausführung gelten diese Gates nur als implementiert, nicht als bestanden.

## Release-Gate

Ein Release mit bekanntem P0/P1-Regressionsfehler darf nicht als stabil freigegeben werden. Ausnahmen müssen ausdrücklich in README, CHANGELOG und hier dokumentiert werden.

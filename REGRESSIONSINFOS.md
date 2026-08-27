# REGRESSIONSINFOS — AIO-Tool

Grundsatz: **Fehler → reproduzierbarer Auslöser → kleinste Codezone → Fix → Regression → Evidenz.**

Aktueller Entwicklungsslice: `0.6.0-autostart-selfheal` (`development / draft`). Die bewiesene **Runtime-Baseline** 0.5.1 bleibt historisch erhalten. Native L4 bleibt **OFFEN**, SAFE-FILE-Ausführung **GESPERRT**.

## Neue 0.6.0-Verträge

### REG-086 — belegter Standard-Port verhindert jeden Start
- **Risiko:** fremder Prozess belegt 8765.
- **Vertrag:** Port wird validiert; bei belegtem Port wird innerhalb eines begrenzten Loopback-Bereichs ein freier Port gewählt.
- **Test/Evidenz:** `tests/test_autostart_selfheal.py`, Failure-Matrix `FM-002`.
- **Status:** **UMGESETZT**, Beweis durch aktuelle Pipeline ausstehend.

### REG-087 — ungültige Portvariable führt zu unverständlichem Traceback
- **Vertrag:** ungültige oder unzulässige Werte fallen verständlich auf 8765 zurück.
- **Test:** `FM-001` + Unit-Test.
- **Status:** **UMGESETZT**.

### REG-088 — stale PID blockiert Start dauerhaft
- **Vertrag:** nicht mehr lebende eigene PID wird erkannt und die Markerdatei entfernt.
- **Test:** `FM-003`.
- **Status:** **UMGESETZT**.

### REG-089 — beschädigte Nutzerdaten werden still überschrieben
- **Vertrag:** beschädigte Hauptdatei wird vor Ersatz quarantänisiert; ein validierbares Backup wird bevorzugt.
- **Test:** `FM-004` + Unit-Test.
- **Status:** **UMGESETZT**.

### REG-090 — Hauptdatei und Backup sind beide beschädigt
- **Vertrag:** beide Originale werden quarantänisiert, erst danach wird ein validierter sicherer Standard erzeugt.
- **Test:** `FM-005` + Unit-Test.
- **Status:** **UMGESETZT**.

### REG-091 — Recovery verändert Source-Checkout unbemerkt
- **Vertrag:** ohne `MANIFEST_RELEASE.json` + `RECOVERY_BASIS.zip` ist Runtime-Recovery deaktiviert.
- **Test:** `FM-006` + Unit-Test.
- **Status:** **UMGESETZT**.

### REG-092 — beschädigte transportierte Runtime-Datei bleibt unheilbar
- **Vertrag:** gebautes Release darf eine hashabweichende Runtime-Datei aus `RECOVERY_BASIS.zip` wiederherstellen; altes Objekt wird quarantänisiert.
- **Test:** `FM-007` + Unit-Test.
- **Status:** **UMGESETZT**.

### REG-093 — schreibgeschützte Programmbasis macht Portable-Paket unbrauchbar
- **Vertrag:** Startroutine spiegelt das vollständige Portable-Paket in einen benutzereigenen Zustandsbereich und startet dort weiter.
- **Test:** `scripts/portable_smoke.py`, Fall `read-only-source-mirror`.
- **Status:** **UMGESETZT**.

### REG-094 — Development-Version scheitert am Evidence-/Documentation-Vertrag
- **Auslöser:** Documentation Guard verlangte bisher auch für `development` eine Release-Evidenzdatei, während Evidence Guard diese bewusst nur für `tested`/höher kennt.
- **Vertrag:** Development darf keine Release-Evidenz vorwegnehmen; bewiesene Zustände müssen sie zwingend besitzen.
- **Schutz:** korrigierter `scripts/documentation_guard.py` + Core-CI.
- **Status:** **UMGESETZT**.

### REG-095 — Einzeltests stammen aus anderem Commit als Portable-/Browser-Gates
- **Vertrag:** alle acht CI-Stufen laufen als harte Needs-Kette auf demselben `github.sha`; Source-ZIP wird per `git archive HEAD` erzeugt.
- **Test:** `tests/test_release_pipeline_contract.py`.
- **Status:** **UMGESETZT**.

## Gate-Reihenfolge 0.6.0

`Core-CI → Failure-Matrix → Source-ZIP → RECOVERY_BASIS → Portable-Build → Portable-Smoke → Chromium → Firefox`.

Ein späteres PASS wertet einen vorherigen Fehler niemals auf. Native Kubuntu L4 bleibt unabhängig davon **OFFEN**.

## Historische Verträge

Die Verträge der Versionen 0.1.x–0.5.1 bleiben über Git-Historie, `VERSION_REGISTRY.json`, bestehende Tests und `evidence/releases/` nachvollziehbar. Dieser 0.6.0-Slice ändert die bewiesene 0.5.1-Release-Evidenz nicht rückwirkend.

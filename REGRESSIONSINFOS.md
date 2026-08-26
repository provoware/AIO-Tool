# REGRESSIONSINFOS

## Zweck

Diese Datei hält dauerhaft fest, welche Fehlerklassen bereits bekannt sind und wie verhindert wird, dass sie unbemerkt zurückkehren.

Ein Regressionseintrag ist kein allgemeiner Bugreport. Er beschreibt einen bereits verstandenen Fehlervertrag mit reproduzierbarem Prüfweg.

## Grundregel

**Bestätigter Fehler → reproduzierbarer Test oder dokumentierte Prüfevidenz → Fix → erneute Prüfung → dauerhaftes Gate.**

## Pflichtfelder je Regression

```text
ID:
Titel:
Status: OFFEN | GEFIXT | GEPRÜFT | BEWIESEN
Entdeckt in Version:
Betroffener Bereich:
Auslöser:
Erwartetes Verhalten:
Fehlerhaftes Verhalten:
Risiko:
Fix:
Regressionstest:
Evidenz:
Letzte Prüfung:
```

## Statusdefinitionen

- **OFFEN** – Fehler bekannt, noch nicht behoben.
- **GEFIXT** – Änderung implementiert, aber noch nicht vollständig nachgewiesen.
- **GEPRÜFT** – vorgesehene Prüfung wurde erfolgreich ausgeführt.
- **BEWIESEN** – reproduzierbare Evidenz und dauerhaftes Regression-Gate vorhanden.

## Verbindliche Regressionsthemen

### REG-001 — Abschlussstatus vor Persistenz

**Risiko:** UI meldet 100 % / DONE, obwohl Abschlusszustand noch nicht sicher gespeichert wurde.

**Vertrag:** Abschlusszustand zuerst persistent schreiben und verifizieren; erst danach `DONE` nach außen melden.

**Status:** BASELINE-REGEL – muss mit Job-System implementiert und getestet werden.

### REG-002 — Setup/Wizard durch harmlose Prüfung entwertet

**Risiko:** Ein bereits vollständig eingerichtetes System springt nach einer reinen Projektprüfung wieder in einen unvollständigen Setup-Zustand.

**Vertrag:** Nur echte ungültige Voraussetzungen dürfen `setup_complete` zurücksetzen. Erfolgreiche Prüfungen dürfen keinen validen Zustand zerstören.

**Status:** BASELINE-REGEL.

### REG-003 — Unterbrochener Job erscheint nach Neustart als laufend

**Risiko:** falsche Prozessanzeige und unsichere Bedienentscheidung.

**Vertrag:** Nicht sauber abgeschlossene Jobs werden beim Neustart als `unterbrochen` rekonstruiert und erhalten kontrollierte Recovery-Optionen.

**Status:** BASELINE-REGEL.

### REG-004 — Prüfoperation verändert Konfiguration

**Risiko:** reine Validierung erzeugt unbeabsichtigte Zustandsänderungen.

**Vertrag:** Prüfungen sind seiteneffektfrei, außer der Nutzer startet ausdrücklich eine Reparatur oder Übernahme.

**Status:** BASELINE-REGEL.

### REG-005 — Mehrfachstart erzeugt mehrere Backends

**Risiko:** konkurrierende Prozesse, Portkonflikte und inkonsistente Persistenz.

**Vertrag:** Startvorgang ist idempotent. Wenn eine valide lokale Instanz läuft, wird diese geöffnet statt eine zweite zu starten.

**Status:** BASELINE-REGEL.

### REG-006 — Einfache Bedienung wird durch Zusatzoptionen überladen

**Risiko:** Laienmodus verliert seine Funktion durch gleichzeitig sichtbare Profioptionen.

**Vertrag:** Zusatz- und Expertenoptionen bleiben standardmäßig eingeklappt. Auswahl vor Zeicheneingabe.

**Status:** BASELINE-REGEL.

### REG-007 — Unsichtbare Dateiänderung

**Risiko:** Nutzer kann nicht erkennen, welche Daten verändert werden.

**Vertrag:** Jede verändernde Dateioperation benötigt verständliche Vorschau, Ziel/Quelle, Konfliktanzeige und Nachprüfung.

**Status:** für SAFE-FILE-CORE verpflichtend.

### REG-008 — endgültiges Löschen als Standard

**Risiko:** unnötiger Datenverlust.

**Vertrag:** Papierkorb/Recovery vor endgültigem Löschen. Endgültige Entfernung nur als ausdrücklich bestätigte Sonderaktion.

**Status:** für SAFE-FILE-CORE verpflichtend.

## Testklassen für zukünftige Releases

Mindestens prüfen, soweit für die Änderung relevant:

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

## Regressionseintrag-Vorlage

```markdown
### REG-XXX — Kurztitel

- **Status:** OFFEN
- **Entdeckt:** x.y.z
- **Bereich:**
- **Auslöser:**
- **Erwartet:**
- **Fehler:**
- **Risiko:**
- **Fix:**
- **Test:**
- **Evidenz:**
- **Letzte Prüfung:**
```

## Release-Gate

Ein Release mit einem bekannten P0/P1-Regressionsfehler darf nicht als stabil freigegeben werden. Ausnahmen müssen ausdrücklich in README, CHANGELOG und dieser Datei dokumentiert werden.

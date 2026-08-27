# TODO — AIO-Tool

## Aktueller Qualitätsstand

**Runtime-Baseline:** 🟢 `0.5.1-audit-modern-ui` — `tested / draft`, **L0–L3 BEWIESEN**  
**Runtime-Baseline-Commit:** `ee6adcfd3427e8328920edaceb804e7b6655cdb8`  
**Runtime-ZIP SHA256:** `f8ffd88e2f3e40416f0d76b20786aa168cebb4e11fe3ef9d0eefa6dcf93b19ee`  
**Native L4:** 🟡 **OFFEN · 0/18 real bestätigt**  
**SAFE-FILE-Ausführung:** 🔒 **GESPERRT**

Die vollständige Release-Beweiskette liegt kanonisch unter `evidence/releases/0.5.1-audit-modern-ui.json`. Repository-only Dokumentation darf nach der Runtime-Baseline fortgeschrieben werden, ohne den Produktstand umzudeuten.

## Fortschritt

```text
0.5.1 Runtime-/Main-Baseline      ████████████████████ 100 % 🟢
138 Unit-/Contracttests           ████████████████████ 100 % 🟢
Runtime-ZIP / Preflight           ████████████████████ 100 % 🟢
Chromium + Firefox L3             ████████████████████ 100 % 🟢
Release-Evidenz                   ████████████████████ 100 % 🟢
Manifest-/Info-Konsistenz         ████████████████████ 100 % 🟢 strukturell gehärtet
Native Kubuntu L4                 ░░░░░░░░░░░░░░░░░░░░   0 % 🟡 0/18 bestätigt
SAFE-FILE Ausführung              ░░░░░░░░░░░░░░░░░░░░   0 % 🔒
```

## Erledigt — Runtime-Baseline 0.5.1

- [x] Persistenz-/Thread-Härtung.
- [x] gemeinsamer Config-Persistence-Core.
- [x] kanonischer Loopback-Host-/Port-Vertrag.
- [x] Dashboard-Zustands-, Timeout-, Single-Flight- und ARIA-Härtung.
- [x] fünf modernisierte Themes inklusive Aurora Glass.
- [x] Native Runner und SAFE-FILE Simulator auf gemeinsames Helper-UI gebracht.
- [x] Browser-Harness auf eine kanonische Implementierung reduziert.
- [x] 138/138 Tests, Guards, Runtime-Preflight und Chromium/Firefox erfolgreich.
- [x] PR #9 per Squash integriert.
- [x] Runtime-Reproduzierbarkeit bewiesen: Feature-Runtime-Head und Main erzeugen identischen SHA256 `f8ffd88e2f3e40416f0d76b20786aa168cebb4e11fe3ef9d0eefa6dcf93b19ee`.

## Erledigt — Repository-/Manifest-Härtung

- [x] Begriffe **Runtime-Baseline**, **Repository-Head**, **Registry-Commit** und **Release-Evidenz** getrennt.
- [x] Development-Manifest auf Version `1.2.0` erweitert.
- [x] Manifest-Policy unter `manifests/README.md` dokumentiert.
- [x] `scripts/manifest_guard.py` ergänzt.
- [x] Release-Evidenz um Main-CI, Reproduzierbarkeitsnachweis und abgelösten Vorartefakt-Hash präzisiert.
- [x] Dokumentations-Guard auf evidenzgetriebene Commit-/Hashprüfung umgestellt.
- [x] L4-Fortschritt von einer irreführenden Prozentannahme auf **0/18 real bestätigt** korrigiert.

## Jetzt — Native L4

1. `./start_native_acceptance.sh` auf echtem Kubuntu starten.
2. `KUB-01` bis `KUB-04` real ausführen.
3. Anzeige klein / Full-HD / groß prüfen.
4. Hauptfunktionen ausschließlich mit Tastatur durchlaufen.
5. Firefox bei 100 / 125 / 150 / 175 / 200 % prüfen.
6. Chrome/Chromium bei 100 / 125 / 150 / 175 / 200 % prüfen.
7. KDE-Skalierung in den Prüfernotizen dokumentieren.
8. Nur nach echter Beobachtung `pass`, `fail` oder `skip` setzen.

### Gate-Regel

- `pass` = real geprüft und korrekt.
- `fail` = Fehler beobachtet; Befund bleibt erhalten und wird analysiert.
- `skip` = nicht geprüft; bleibt fachlich offen.
- Kein L4-Schritt wird aus CI automatisch aufgewertet.

## Danach

Erst nach Auswertung der realen L4-Ergebnisse wird entschieden:

- **bei PASS:** nächsten sicherheitsgebundenen Slice planen,
- **bei FAIL:** kleinsten verantwortlichen Patch-Slice mit Regression anlegen,
- **bei SKIP/OFFEN:** keine Statusverbesserung behaupten.

## Sicherheitsgrenze

SAFE-FILE bleibt unverändert simulationsgebunden. Keine reale Ausführung freischalten, bevor dafür eine neue Version mit eigenem Recovery-/Execution-Nachweis angelegt wurde.

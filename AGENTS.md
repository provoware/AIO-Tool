# AGENTS.md — Verbindlicher Entwicklungs- und Qualitätsvertrag

Diese Regeln gelten für Menschen, KI-Agenten und automatisierte Entwicklungswerkzeuge im Repository. Sie sind **Produktionsregeln**, keine unverbindlichen Empfehlungen.

## 1. Entwicklungsfluss

**Besprechen → abgrenzen → kleinste verantwortliche Codezone bestimmen → ändern → automatisch prüfen → Fehler beheben → Regression sichern → Evidenz erzeugen → Dokumentation synchronisieren → nächsten unabhängigen Slice wählen.**

- Keine großflächigen Umbauten ohne belegten strukturellen Nutzen.
- Funktionierende Bereiche möglichst lokal patchen.
- Keine neue Nutzfunktion beginnen, solange ein P0/P1-Gate des aktuellen Slices rot ist.
- Ein Fix ist erst abgeschlossen, wenn der zugehörige Fehlervertrag erneut geprüft wurde.

## 2. Quellenhierarchie

Bei Widersprüchen gilt:

1. Produktvalidatoren / ausführbarer Code.
2. `VERSION` + validierte `VERSION_REGISTRY.json` für Produktversion und Statuspaar.
3. `manifests/RUNTIME_MANIFEST.json` für die transportierte Runtime-Dateimenge.
4. Automatisierte Tests / CI-Evidenz für tatsächlich ausgeführte Prüfungen.
5. `evidence/RELEASE_EVIDENCE_INDEX.json` + versionierte Einzelevidenzdateien für Commit-, Artefakt-, Browser- und Release-Provenienz bewiesener Stände.
6. `manifests/DEVELOPMENT_MANIFEST.json` für den repo-only Entwicklungs-/Dokumentationsbestand und die Dokumentationspflicht.
7. README / TODO / CHANGELOG / MANIFEST / REGRESSIONSINFOS / LAIEN-ANLEITUNG / TOOLBESCHREIBUNG als menschenlesbare Ableitung.

Dokumentation darf keinen besseren Zustand behaupten als Registry + tatsächlich ausgeführte Gates. Release-Evidenz darf zusätzliche Provenienz eines bereits gültigen Status belegen, z. B. Main-Commit und Runtime-SHA, ohne den Registry-Status nachträglich umzudeuten.

## 3. Versionszustände

Kanonisch:

- `development / draft` → `DEV`
- `tested / draft` → `TESTED`
- `release-candidate / candidate` → `RC`
- `released / released` → `RELEASED`
- `blocked / blocked` → `BLOCKED`
- `deprecated / deprecated` → `ARCHIVED`

Unbekannte/widersprüchliche Kombinationen fail-closed ablehnen.

### Unveränderlichkeit bewiesener Versionen

Sobald eine Version `tested`, `release-candidate` oder `released` ist, wird ihre **Runtime-Baseline** eingefroren. Jeder Patch an einer Runtime-Allowlist-Datei startet eine **neue Version als development**. Alte Evidenz bleibt historisch reproduzierbar.

Repo-only Dokumentation/Evidenz darf unter derselben Produktversion fortgeschrieben werden, solange nachweislich keine Runtime-Allowlist-Datei verändert wird.

## 4. Statussprache

- **UMGESETZT** = vorhanden.
- **GEPRÜFT** = Test tatsächlich ausgeführt.
- **BEWIESEN** = reproduzierbare Evidenz einem konkreten Runtime-/Produktstand zugeordnet.

Nicht geprüfte Zielsysteme bleiben ausdrücklich offen.

## 5. Laien zuerst

- Standardsprache Deutsch.
- Alltagssprache vor Fachsprache.
- Pro Ansicht möglichst 3–6 Hauptentscheidungen.
- Ein klarer nächster Schritt sichtbar.
- Expertenoptionen standardmäßig einklappen.
- Farbe nie als einzige Information; immer Text/Icon ergänzen.

## 6. Auswahl vor Zeicheneingabe

Reihenfolge: **Button → Auswahldialog → Preset/zuletzt verwendet → intelligente Empfehlung → Freitext-Fallback**.

Neue freie Eingabefelder sind begründungspflichtig. Sensible Inhalte nicht automatisch vorschlagen.

## 7. Sicherheit und Integrität

- Keine destruktive Dateiaktion ohne Vorschau und klare Auswirkung.
- Kritische Operationen benötigen Vor- und Nachvalidierung.
- Undo/Recovery ist Teil des Funktionsvertrags.
- Endgültiges Löschen ist nie Standard.
- Kein stiller Zielwechsel bei Laufwerks-/Pfadproblemen.
- Fehler dürfen keinen falschen Erfolg melden.
- `DONE` erst nach erfolgreicher Persistenz des Abschlusszustands.
- Prüfungen dürfen produktive Nutzerdaten nicht verändern.

## 8. Launcher- und Instanzvertrag

`HTTP 200` beweist keine passende Instanz. Vor Wiederverwendung müssen mindestens Toolversion, Loopback-Bindung, Ready-Zustand und konkrete Installationskennung übereinstimmen. Fremd/alt belegte Ports nie still übernehmen; freier Loopback-Ausweichport ist erlaubt und sichtbar zu melden.

## 9. Offline-first und Datenschutz

- Kernfunktionen ohne Internet.
- Keine Telemetrie ohne explizite Produktentscheidung.
- Lokales Backend nur Loopback.
- Keine Secrets/PINs/Passwörter in Klartextlogs.
- Diagnose so datensparsam wie möglich.

## 10. Architektur und Wartbarkeit

- UI, Domänenlogik, Persistenz, Launcher, Transport und Testharness trennen.
- Wiederverwendbare Verträge zentralisieren statt in Shell/JS/Python mehrfach nachzubauen.
- Zentrale Module möglichst unter ca. 800 Zeilen halten.
- Keine neue externe Runtime-Abhängigkeit, wenn Standardbibliothek robust genügt.
- Entwicklungsabhängigkeiten pinnen und vom Runtime-Transport trennen.

## 11. Runtime ≠ Repository

Runtime-ZIP = ausschließlich positive Allowlist aus `manifests/RUNTIME_MANIFEST.json` + reproduzierbar generiertes `MANIFEST_RELEASE.json`.

Repository-only bleiben insbesondere Dokumentation, Regressionen/Learning Memory, Tests/Testdaten, `evidence/`, CI-Dateien, Screenshots/Reports und Entwicklungslogs. Lokale Runtime-/Nutzerdaten werden weder versioniert noch transportiert.

`manifests/DEVELOPMENT_MANIFEST.json` ist die maschinenlesbare Klassifikation dieser repo-only Ebene. Sein Inhalt darf nicht als zweite Runtime-Allowlist benutzt werden.

## 12. Persistenz

- relevante Zustände atomar schreiben,
- unterbrochene Prozesse nach Neustart nicht als „läuft“ darstellen,
- Backups/Recovery-Metadaten konsistent halten,
- Prüfungen verändern keine produktive Config,
- Schemaänderung → Validator + Vorlage + positive/negative Testdaten + Regression gemeinsam.

## 13. Tests und Regressionserkennung

Jeder bestätigte Fehler erhält soweit möglich reproduzierbaren Auslöser, Soll/Ist, minimalen Fix, Regressionstest und erneuten Nachweis.

Qualitätsebenen:

- **L0:** Syntax/Schema.
- **L1:** Unit/Contract/Failure-Matrix.
- **L2:** Integration/echtes Runtime-ZIP.
- **L3:** echte Chromium-/Firefox-Render-/Interaktion.
- **L4:** reales Kubuntu/DPI/Browserzoom/Tastatur.

Eine niedrigere Ebene darf keine höhere vortäuschen.

Prioritäten: P0 Datenverlust/Sicherheit/Releaseintegrität; P1 Start/Persistenz/Kernbedienung/A11y; P2 Wartbarkeit/UX; P3 Komfort/Kosmetik.

## 14. UI-Acceptance

Statische HTML/CSS-/DOM-Tests sind kein Renderbeweis. Für Layout-/Reflow-/Zielgrößenaussagen gelten Rastervertrag, deterministische Fixtures, Ready-Zustand, Chromium+Firefox, Viewportmatrix inklusive 320 CSS-px und Screenshot/JSON-Evidenz. Baselines nicht einfach aktualisieren, um Fehler zu verstecken.

## 15. Musterdateien und Fehlerhilfe

Für persistente JSON-/Config-Formate: gültige versionierte Mustervorlage, relevante negative Fixtures und dieselben Produktvalidatoren. Vorlagen niemals ungefragt über Nutzerdaten schreiben. Wiederkehrende sichtbare Systemtexte versioniert auslagern.

## 16. Entwicklungs-Lerngedächtnis

`LEARNING_MEMORY.jsonl` hält bestätigte strukturelle Lektionen mit Auslöser, Erkenntnis, Regel, Regression und Geltungsbereich. CI validiert Form/Eindeutigkeit. Berichte dürfen keine nicht vorhandene Lernregel behaupten.

## 17. Codesparendes Patchen

Vor größeren Änderungen bestimmen: **Datei → Funktion/Klasse → Zeilenbereich → Test → Manifest-/Doku-Auswirkung.** Erst lokaler Patch + Regression, breiter Refactor nur bei belegter Kopplungsreduktion. Zeilenangaben im Abschluss aus final geprüftem Stand.

## 18. Release-Gate

Vor Promotion mindestens Syntax, Unit/Integration, Foundation/Learning/Evidence/Documentation/Manifest Guards, Runtime-ZIP + Manifest/Hashes + frischer Preflight, bei UI-Änderungen Chromium+Firefox, synchronisierte Dokumentation und sauberer Transport. Auf dem Promotion-Commit komplette CI erneut ausführen.

## 19. Dokumentationspflicht

Verhaltens-/Architektur-/Sicherheits-/Statusänderungen synchronisieren mindestens die in `manifests/DEVELOPMENT_MANIFEST.json` unter `status_documents` deklarierten Dateien.

Der Documentation Guard muss diese Liste aus dem Development-Manifest beziehen statt eine zweite manuelle Pflichtliste zu pflegen.

## 20. Native Acceptance / L4

L4 darf **niemals** aus L0–L3 abgeleitet werden.

- Jeder Native-Acceptance-Schritt startet `pending/OFFEN`.
- Automatisches PASS ist verboten.
- Zulässige Nutzerentscheidungen: `pass`, `fail`, `skip`.
- `skip` ist kein bestandenes Gate.
- Browserzoom wird als Zielvorgabe dokumentiert; technische Browsermetriken dürfen eine reale Zoom-Bestätigung nicht ersetzen.
- Firefox und Chromium sollen dieselbe persistente Sitzung verwenden.
- FAIL-Befunde bleiben erhalten und werden vor Statusverbesserung analysiert.
- Abnahmeberichte liegen lokal unter `runtime/`; sie gelangen nicht automatisch in Release-ZIPs oder Repository.
- Solange kein Schritt real bestätigt wurde, ist der reale L4-Fortschritt **0/18 = 0 %**; Implementierungsfortschritt des Runners zählt nicht als Abnahmefortschritt.

## 21. Release-Evidenzdateien

Für jede Registry-Version mit Status `tested`, `release-candidate` oder `released` muss exakt eine Datei unter `evidence/releases/<version>.json` existieren und vom Masterindex referenziert werden.

Pflichtfelder: Registry-Commit, CI-Runs, Artefaktstatus/SHA256 soweit wirklich aufgezeichnet, Browsermatrix, offene L4-Gates. Promotion-/Main-Commit ergänzen, wenn vorhanden.

Main-CI, Reproduzierbarkeitsnachweis, Wrapper-Digest und abgelöste Vorartefakte sollen maschinenlesbar ergänzt und validiert werden, sobald sie tatsächlich vorliegen.

Historisch fehlende Informationen werden **nicht rekonstruiert oder geraten**: `not-recorded` + `null`. `scripts/evidence_guard.py` ist ein blockierendes CI-Gate.

## 22. SAFE-FILE-Stufenvertrag

### V0 Simulation

Die Simulation darf **keine echte Dateimutation technisch besitzen**:

- `SIMULATION_ONLY=True`,
- `EXECUTION_ENABLED=False`,
- kein Execute-Endpunkt,
- keine Copy-/Move-/Rename-/Delete-Primitive,
- Preview meldet `mutation_performed=false`.

Sie darf lesend Quelle/Ziel/Metadaten/Speicherplatz/Konflikte prüfen und einen Plan erzeugen.

### Vor echter Copy

Ein neuer Versionsslice muss mindestens beweisen:

- Failure-Matrix vollständig grün,
- persistentes Jobjournal **vor** Mutation,
- Staging/Partial-State-Vertrag,
- Nachvalidierung vor `DONE`,
- Crash/Abbruch/Neustart-Recovery,
- Undo nur nach Verifikation, dass das erzeugte Ziel unverändert ist.

Erste reale Operation ausschließlich **Copy einer normalen Datei**. Move/Rename/Delete bleiben gesperrt, bis Copy separat bewiesen ist.

## 23. Parallelität und UI-Zustandswahrheit

- Jeder Persistenzstore, der aus `ThreadingHTTPServer` oder anderen Threads erreichbar ist, muss den vollständigen Read→Mutate→Write-Zyklus serialisieren. Atomare Dateiumbenennung allein verhindert keine verlorenen Updates.
- Backup-/Temp-Dateien dürfen bei Parallelzugriff nicht denselben ungeschützten Schreibpfad konkurrierend verwenden.
- UI-Ladevorgänge laufen single-flight, wenn parallele Ausführung keinen Nutzwert hat (z. B. Refresh oder Config-Speichern).
- Ein fehlgeschlagener Reload darf keine alten Daten als aktuelle Daten weiterzeigen und keinen Ladefehler als „leer“ darstellen. Stattdessen explizit `nicht verfügbar`/Fehlerzustand rendern.
- Busy-Zustände müssen sichtbar und mit `aria-busy`/deaktivierten konkurrierenden Controls gekoppelt sein.
- Netzwerk-/Backend-Wartezeiten brauchen ein begrenztes Timeout und eine verständliche nächste Handlung.

## 24. Testharness folgt dem Produktvertrag

- Browser-Fixtures müssen **vor** Produkt-JavaScript aktiv sein.
- Der Acceptance-Harness leitet lokale CSS-/JS-Assets aus dem aktuellen Produkt-HTML ab; Query-/Contract-Versionsstrings nicht redundant im Harness hardcoden.
- Wird ein neuer lokaler Stylesheet-Vertrag eingeführt, muss der Harness ihn entweder automatisch aufnehmen oder fail-closed melden.
- Ein grüner Harness darf nicht dadurch entstehen, dass Produktassets fehlen oder durch vereinfachte Testassets ersetzt werden.
- Asset-Inlining, Fixture-Reihenfolge und Ready-Zustand besitzen eigene Regressionstests.

## 25. Commit- und Evidence-Ebenen

Die folgenden Begriffe sind verbindlich getrennt:

- **Runtime-Baseline-Commit:** der konkrete bewiesene Programm-/Transportstand einer eingefrorenen Version.
- **Repository-Head:** der neueste Commit auf einem Branch; kann danach ausschließlich repo-only Änderungen enthalten.
- **Registry-Commit:** der Commit, der den Versionsdatensatz begründet.
- **Promotion-Commit:** der Stand, auf dem die Statuspromotion geprüft wurde.
- **Main-Commit in Release-Evidenz:** der integrierte Runtime-/Produktstand, der zur kanonischen Main-Evidenz gehört.

Ein späterer repo-only Commit darf niemals rückwirkend als neuer Runtime-Baseline-Commit bezeichnet werden.

### Keine selbstreferenzielle „Latest-CI“-Schleife

Statusdokumente sollen stabile Beweisfakten aus der versionierten Release-Evidenz ableiten. Der jeweils neueste reine Dokumentations-CI-Lauf muss **nicht** in dieselben Dokumente zurückgeschrieben werden, wenn dadurch unmittelbar ein neuer Dokumentationscommit und damit erneut ein neuer CI-Lauf entstünde.

Repo-only Guard-Ergebnisse dürfen im Abschlussbericht genannt werden; der kanonische Runtime-Beweis bleibt in der Release-Evidenz stabil.

## 26. Manifestvertrag

- `manifests/RUNTIME_MANIFEST.json` ist die **einzige positive Runtime-Allowlist**.
- `manifests/DEVELOPMENT_MANIFEST.json` ist die **repo-only Klassifikation** und darf keine Runtime-Datei als Entwicklungsinhalt beanspruchen.
- `scripts/manifest_guard.py` ist blockierender Konsistenzschutz.
- `manifests/README.md` dokumentiert die Semantik für Menschen.
- Ändert sich das Runtime-Manifest oder eine darin gelistete Datei, ist das eine Runtime-Änderung und benötigt eine neue `development`-Version.
- Reine Änderungen an Development-Manifest, Doku, Evidence, Tests oder CI-Hilfen dürfen die eingefrorene Runtime-Baseline nicht verändern.
- Der Runtime-ZIP-SHA einer repo-only Änderung muss mit dem zuvor bewiesenen Baseline-SHA übereinstimmen; eine Abweichung blockiert den Abschluss.

### Legacy-Regel für Runtime-Manifest 1.3.0

Das gemeinsame Feld `generated_files` wird für 0.5.1 bewusst unverändert gelassen: `MANIFEST_RELEASE.json` ist build-generiert und transportiert; `web/.aio-instance-id` und `runtime/**` sind post-start-generiert und nicht feste Transportdateien. Eine strukturelle Feldaufteilung ist erst in einer neuen Runtime-Version zulässig.

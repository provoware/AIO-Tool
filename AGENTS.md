# AGENTS.md — Verbindlicher Entwicklungs- und Qualitätsvertrag

Diese Regeln gelten für Menschen, KI-Agenten und automatisierte Entwicklungswerkzeuge im Repository. Sie sind **Produktionsregeln**, keine unverbindlichen Empfehlungen.

## 1. Entwicklungsfluss

**Besprechen → abgrenzen → kleinste verantwortliche Codezone bestimmen → ändern → automatisch prüfen → Fehler beheben → Regression sichern → Evidenz erzeugen → Dokumentation synchronisieren → nächsten unabhängigen Slice wählen.**

- Keine großflächigen Umbauten ohne belegten strukturellen Nutzen.
- Funktionierende Bereiche möglichst lokal patchen.
- Keine neue Nutzfunktion beginnen, solange ein P0/P1-Gate des aktuellen Slices rot ist.
- Ein Fix ist erst abgeschlossen, wenn der zugehörige Fehlervertrag erneut geprüft wurde.

## 2. Quellenhierarchie — welche Datei ist wofür Wahrheit?

Bei Widersprüchen gilt diese Reihenfolge:

1. **Produktvalidatoren / ausführbarer Code** — tatsächlicher Daten- und Laufzeitvertrag.
2. **`VERSION` + validierte `VERSION_REGISTRY.json`** — Versions- und Statuswahrheit.
3. **`manifests/RUNTIME_MANIFEST.json`** — einzige Allowlist für transportierte Runtime-Dateien.
4. **Automatisierte Tests / CI-Evidenz** — Nachweis, nicht Produktdefinition.
5. **README / TODO / CHANGELOG / MANIFEST / LAIEN-ANLEITUNG / TOOLBESCHREIBUNG** — Erklärung des bewiesenen Zustands.

Dokumentation darf niemals einen besseren Zustand behaupten als Registry + Evidenz.

## 3. Versionszustände und erlaubte Übergänge

Kanonische Versionsstatus:

- `development` → Dateisuffix `DEV`
- `tested` → `TESTED`
- `release-candidate` → `RC`
- `released` → `RELEASED`
- `blocked` → `BLOCKED`
- `deprecated` → `ARCHIVED`

Kanonische Release-Statuspaare:

- `development / draft`
- `tested / draft`
- `release-candidate / candidate`
- `released / released`
- `blocked / blocked`
- `deprecated / deprecated`

Unbekannte oder widersprüchliche Kombinationen müssen **fail-closed** abgelehnt werden.

### Unveränderlichkeit bewiesener Versionen

Sobald eine Version `tested`, `release-candidate` oder `released` ist, darf Produktcode dieses Versionsstandes nicht weiter verändert werden. Jeder weitere Codepatch erzeugt eine **neue Version als `development`**. Die alte Evidenz bleibt historisch reproduzierbar.

## 4. Statussprache

- **UMGESETZT** = Code/Artefakt vorhanden.
- **GEPRÜFT** = Test tatsächlich ausgeführt.
- **BEWIESEN** = reproduzierbare Evidenz einem konkreten Commit zugeordnet.

`tested`, `release-candidate` und `released` benötigen Evidenz. Nicht geprüfte Zielsysteme bleiben ausdrücklich offen.

## 5. Laien zuerst

- Standardsprache der Nutzeroberfläche: Deutsch.
- Alltagssprache vor Fachsprache.
- Fachbegriffe nur ergänzend und verständlich erklärt.
- Pro Ansicht möglichst 3–6 Hauptentscheidungen.
- Ein klarer nächster Schritt muss sichtbar sein.
- Expertenoptionen standardmäßig einklappen.
- Farbe unterstützt die Orientierung, ist aber nie die einzige Information; Status benötigt zusätzlich Text/Icon.

## 6. Auswahl vor Zeicheneingabe

Neue Eingabefelder sind begründungspflichtig. Reihenfolge:

1. Button
2. Auswahldialog
3. Preset / zuletzt verwendet
4. intelligente Empfehlung
5. erst dann Freitext-Fallback

Ausnahmen: Inhalte, die naturgemäß frei eingegeben werden müssen, z. B. Notiztext oder PIN. Wiederkehrende sichere Eingaben sollen gespeichert und später als Auswahl angeboten werden. Keine sensiblen Inhalte automatisch als Vorschläge übernehmen.

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

Eine Antwort `HTTP 200` beweist **keine** passende Toolinstanz.

Vor Wiederverwendung müssen mindestens übereinstimmen:

- erwartete Toolversion,
- Loopback-Bindung,
- Ready-Zustand,
- konkrete lokale Installationskennung.

Ein fremd oder alt belegter Port wird niemals still übernommen. Der Launcher darf einen freien Loopback-Ausweichport wählen und muss dies sichtbar melden. Startdiagnose und Backendlog bleiben getrennt.

## 9. Offline-first und Datenschutz

- Kernfunktionen funktionieren ohne Internet.
- Keine Telemetrie ohne ausdrücklich dokumentierte Produktentscheidung.
- Lokales Backend nur auf Loopback binden, sofern kein anderer Vertrag beschlossen wurde.
- So wenig personenbezogene/nutzerspezifische Daten speichern wie möglich.
- Keine Secrets, PINs oder Passwörter im Klartext protokollieren.
- Diagnoseausgaben dürfen keine vollständige Config oder unnötige lokale Pfade ausgeben.

## 10. Architektur und Wartbarkeit

- UI, Domänenlogik, Persistenz, Launcher, Transport und Testharness klar trennen.
- Wiederverwendbare Verträge in kleinen Modulen zentralisieren statt in Shell/JS/Python mehrfach nachzubauen.
- Zentrale Quellmodule möglichst unter ca. 800 Zeilen halten; vorher Verantwortlichkeiten prüfen.
- Keine neue externe Runtime-Abhängigkeit, wenn Standardbibliothek oder bestehende Abhängigkeit robust genügt.
- Externe Entwicklungsabhängigkeiten müssen gepinnt und vom Runtime-Transport getrennt sein.

## 11. Runtime ≠ Repository

Das Runtime-ZIP enthält **nur** die explizite Allowlist aus `manifests/RUNTIME_MANIFEST.json` plus generiertes `MANIFEST_RELEASE.json`.

Repository-/Entwicklungsbestand bleibt außerhalb des Transportpakets, insbesondere:

- README/AGENTS/TODO/CHANGELOG/Regressionen/Learning Memory,
- Tests und Testdaten,
- CI-Konfiguration,
- Screenshots/Reports,
- Entwicklungslogs.

Der Launcher darf beim normalen Betrieb **nur Runtime-Dateien voraussetzen**. `scripts/runtime_preflight.py` ist der Startvertrag; `scripts/validate.py` ist eine Repository-Vollprüfung und darf im Runtime-ZIP fehlen.

## 12. Persistenz

- Relevante Zustände atomar schreiben.
- Unterbrochene Prozesse dürfen nach Neustart nicht als „läuft“ erscheinen.
- Backups/Recovery-Metadaten konsistent halten.
- Konfigurationsänderungen dürfen nicht als Nebeneffekt einer Prüfung entstehen.
- Schemaänderung → Validator + Vorlage + gültige/ungültige Testdaten + Regression gemeinsam aktualisieren.

## 13. Tests und Regressionserkennung

Jeder bestätigte Fehler erhält soweit möglich:

- reproduzierbaren Auslöser,
- erwartetes Verhalten,
- tatsächliches Fehlverhalten,
- minimalen Fix,
- Regressionstest,
- erneuten Nachweis.

### Erkennungsebenen

1. **L0 Syntax/Schema** — schnell, billig.
2. **L1 Unit/Contract** — Domänen- und Strukturvertrag.
3. **L2 Integration/Runtime-ZIP** — transportierter Bestand funktioniert zusammen.
4. **L3 Browser-Render/Interaktion** — echte Chromium-/Firefox-Geometrie und Bedienung.
5. **L4 Native Zielsystemabnahme** — reales Kubuntu/DPI/Browserzoom/Tastatur.

Eine niedrigere Ebene darf keine Aussage einer höheren Ebene vortäuschen.

### Priorisierung

- **P0:** Datenverlust, falsche Instanz, Sicherheits-/Release-Integritätsbruch → sofort blockieren.
- **P1:** Start, Persistenz, Kernbedienung, gravierende UI-Reflow-/A11y-Fehler → vor neuer Funktion beheben.
- **P2:** relevante Nutzerfreundlichkeit/Wartbarkeit → im aktuellen oder nächsten Slice.
- **P3:** Kosmetik/Komfort ohne Funktionsrisiko → planbar.

## 14. UI-Acceptance

Statische HTML/CSS-/DOM-Tests sind **kein Renderbeweis**.

Für Aussagen zu Layout, Reflow, Überlappung, Zielgrößen oder Browserinteraktion gilt:

- maschinenlesbarer Rastervertrag,
- deterministische isolierte Fixtures,
- messbarer Ready-Zustand,
- echte Chromium- und Firefox-Läufe,
- Viewport-/Reflow-Matrix einschließlich 320 CSS-px,
- Screenshot + JSON-Report als Evidenz,
- Fehlerartefakte auch bei rotem Gate.

Screenshot-Baselines dürfen nicht einfach aktualisiert werden, um einen Fehler verschwinden zu lassen. Geometrie-/Interaktionsvertrag entscheidet zuerst.

## 15. Musterdateien und Fehlerhilfe

Für jedes persistente JSON-/Config-Format:

- mindestens eine gültige versionierte Mustervorlage,
- relevante absichtlich ungültige Testdaten,
- dieselben Validatoren für Produktdaten, Vorlage und Tests,
- Vorlagen niemals ungefragt über Nutzerdaten schreiben.

Wiederkehrende sichtbare Systemtexte werden versioniert ausgelagert. Fehlerhilfe unterscheidet Nutzereingabe, Integrität/Persistenz und unbekannte Fehler. `retry_safe=true` nur bei tatsächlich sicherem Wiederholungsversuch.

## 16. Entwicklungs-Lerngedächtnis

`LEARNING_MEMORY.jsonl` hält bestätigte strukturelle Entwicklungslektionen dauerhaft fest. Ein Eintrag enthält Auslöser, Erkenntnis, neue Regel, Regression und Geltungsbereich. CI validiert Eindeutigkeit und Form. Ein Bericht darf keine Lernregel als vorhanden behaupten, die nicht im Repository steht.

## 17. Codesparendes Patchen

Vor größeren Änderungen bestimmen:

**Datei → Funktion/Klasse → Zeilenbereich → zugehöriger Test → Auswirkung auf Manifeste/Doku.**

Lokaler Patch + Regression vor breitem Refactor. Größerer Umbau nur, wenn lokale Reparatur die Kopplung verschlimmern würde. Zeilenangaben in Abschlussberichten stammen aus dem tatsächlich geprüften finalen Stand.

## 18. Release-Gate

Vor Statuspromotion mindestens:

- Python-/Shell-/JavaScript-Syntax grün,
- Unit-/Integrations-/Vertragstests grün,
- Foundation-/Learning-Gate grün,
- Runtime-ZIP gebaut und Manifest/Hashes geprüft,
- gebautes ZIP frisch entpackt und `runtime_preflight.py` daraus erfolgreich ausgeführt,
- für UI-Änderungen Chromium + Firefox Acceptance grün,
- Dokumentations-/Manifeststatus synchron,
- keine Runtime-/Nutzerdaten/Testartefakte im Transport.

Erst danach Statuspromotion; **auf dem Promotion-Commit komplette CI erneut ausführen**.

## 19. Dokumentationspflicht

Änderungen mit Wirkung auf Verhalten, Architektur, Sicherheit, Bedienung, Status oder Transport müssen die relevanten Dateien gemeinsam synchronisieren:

`README.md`, `TODO.md`, `CHANGELOG.md`, `MANIFEST.md`, `REGRESSIONSINFOS.md`, `LAIEN-ANLEITUNG.md`, `TOOLBESCHREIBUNG.md`.

README zeigt aktuellen Zustand und verständlichen Start; TODO nur tatsächlich offene Punkte; CHANGELOG zeitliche Änderung; MANIFEST Architektur/Transport; REGRESSIONSINFOS Fehlerverträge. Keine Datei darf einen alten Versionsstand als „aktuell“ ausgeben.

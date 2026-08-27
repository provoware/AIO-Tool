# Iterations-Sync — Version ↔ Repository

## Zweck

Jede Entwicklungsiteration muss eindeutig auf die aktuell deklarierte Produktversion und den tatsächlich geprüften Repository-Stand zurückführbar sein. Drift zwischen `VERSION`, `VERSION_REGISTRY.json`, Statusdokumenten, Runtime-Manifest und Git-HEAD wird fail-closed behandelt.

## Kanonischer Prüfer

```bash
python scripts/iteration_sync.py --check
```

Im echten lokalen Git-Checkout wird zum Iterationsabschluss zusätzlich ein sauberer Arbeitsbaum verlangt:

```bash
python scripts/iteration_sync.py \
  --check \
  --require-git \
  --require-clean \
  --output artifacts/iteration-sync.json
```

GitHub Actions bindet die Prüfung exakt an den Trigger-Commit:

```bash
python scripts/iteration_sync.py \
  --check \
  --require-git \
  --require-clean \
  --expect-commit "$GITHUB_SHA" \
  --output artifacts/iteration-sync.json
```

## Geprüfte Invarianten

1. `VERSION == VERSION_REGISTRY.json.current_version`.
2. Die aktuelle Version ist eindeutig registriert und der letzte Registry-Eintrag.
3. `manifests/RUNTIME_MANIFEST.json` transportiert `VERSION` und `VERSION_REGISTRY.json`.
4. Alle in `manifests/DEVELOPMENT_MANIFEST.json` deklarierten `status_documents` enthalten die aktuelle Version.
5. Im Git-Checkout werden HEAD, Tree, Branch und Clean/Dirty-Zustand erfasst.
6. In CI muss `HEAD == GITHUB_SHA` gelten.
7. CI erzeugt `artifacts/iteration-sync.json` und lädt es als eigene Evidenz hoch.

## Warum der aktuelle HEAD nicht in README/Registry zurückgeschrieben wird

Würde jede Iteration ihren eigenen gerade erzeugten Commit-SHA in eine versionierte Datei schreiben, entstünde durch genau diese Änderung sofort ein neuer Commit. Der eingetragene SHA wäre damit bereits wieder veraltet. Das wäre eine selbstreferenzielle Commit-Schleife.

Deshalb gilt:

- Produkt-/Statuswahrheit bleibt versioniert in `VERSION` und `VERSION_REGISTRY.json`.
- Der exakte aktuelle Repository-HEAD wird als **erzeugte Iterations-Evidenz** festgehalten.
- `commit_sha` in der Versions-Registry behält seine definierte Baseline-/Registry-Semantik und wird nicht als ständig wechselnder Latest-HEAD missbraucht.

## Entwicklungsregel

Ab jetzt gehört der Iterations-Sync zu jedem Abschlusszyklus:

**ändern → testen → Guards → Iterations-Sync → Commit/CI → Evidenz prüfen → nächste Iteration**.

Ein roter Sync-Guard blockiert den Abschluss der Iteration.

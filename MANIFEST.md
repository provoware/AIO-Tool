# MANIFEST

## Projekt

- **Name:** AIO-Tool
- **Repository:** `provoware/AIO-Tool`
- **Phase:** CLEAN FOUNDATION
- **Version:** 0.1.0-foundation
- **Stand:** 2026-08-27

## Verbindlicher Grundbestand

| Pfad | Rolle | Pflicht |
|---|---|---|
| `README.md` | Einstieg, Status, Prinzipien | ja |
| `TODO.md` | priorisierte Arbeit und Gates | ja |
| `AGENTS.md` | Entwicklungs- und Sicherheitsregeln | ja |
| `CHANGELOG.md` | Versionshistorie | ja |
| `LAIEN-ANLEITUNG.md` | einfache Nutzererklärung | ja |
| `TOOLBESCHREIBUNG.md` | Produktvision und Funktionsrahmen | ja |
| `MANIFEST.md` | definierter Projekt-/Releasebestand | ja |
| `REGRESSIONSINFOS.md` | Regressionen, Tests und Evidenz | ja |

## Aktueller Codebestand

**Kein produktiver Anwendungscode.**

Die Clean-Foundation-Phase enthält absichtlich nur die verbindliche Dokumentationsbasis. Quellcode wird erst mit einem klar abgegrenzten, testbaren Slice ergänzt.

## Geplante spätere Struktur

Noch nicht verbindlich, aber als Zielbild vorgesehen:

```text
app/            # Anwendungs- und Domänenlogik
web/            # Browseroberfläche
runtime/        # erzeugte lokale Laufzeitdaten, nicht Teil des Releases
tests/          # automatisierte Tests
docs/           # ergänzende technische Dokumente
scripts/        # Start-, Validierungs- und Release-Skripte
```

Die tatsächliche Struktur darf erst nach dem P0-Architekturentscheid festgeschrieben werden.

## Release-Ausschlüsse

Folgende Inhalte gehören grundsätzlich nicht in ein sauberes Release:

- `.venv/`
- `__pycache__/`
- Testcache
- temporäre Dateien
- lokale Logs, sofern sie nicht ausdrücklich Teil eines Diagnoseartefakts sind
- PINs, Passwörter oder Secrets
- lokale Profile
- persönliche Projektpfade
- Recovery-/Checkpoint-Daten realer Nutzer
- Build-Zwischenstände

## Daten- und Netzvertrag

- Kern: offline-first.
- kein Internetzwang.
- keine Telemetrie als Default.
- lokale Persistenz nur für klar definierte Funktionen.
- sensible Daten nicht im Klartext protokollieren.

## Qualitätsvertrag

Ein zukünftiges Release darf nur als geprüft bezeichnet werden, wenn:

1. relevante automatisierte Tests grün sind,
2. notwendige manuelle Gates dokumentiert sind,
3. Regressionseinträge aktuell sind,
4. Changelog und TODO konsistent sind,
5. dieses Manifest den tatsächlichen Releasebestand widerspiegelt,
6. ein sauber entpackter Release erneut geprüft wurde.

## Nächster Manifest-Schritt

Mit Beginn des ersten Code-Slices müssen ergänzt werden:

- Laufzeitvoraussetzungen,
- Startdateien,
- genaue Ordnerstruktur,
- Abhängigkeiten mit Versionen/Begründung,
- Konfigurations- und Persistenzdateien,
- Testkommandos,
- Release-Inhalt und Ausschlüsse.

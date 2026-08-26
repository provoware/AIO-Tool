# MANIFEST

## Projekt

- **Name:** AIO-Tool
- **Repository:** `provoware/AIO-Tool`
- **Phase:** CLEAN FOUNDATION — ausführbarer Kern
- **Version:** `0.1.1-foundation`
- **Stand:** 2026-08-27

## Verbindlicher Projektbestand

### Root

| Pfad | Rolle |
|---|---|
| `README.md` | Einstieg, Status, Start und Projektüberblick |
| `TODO.md` | priorisierte Arbeit und Gates |
| `AGENTS.md` | verbindliche Entwicklungs- und Sicherheitsregeln |
| `CHANGELOG.md` | Versionshistorie |
| `LAIEN-ANLEITUNG.md` | einfache Nutzererklärung |
| `TOOLBESCHREIBUNG.md` | Produktvision und Funktionsrahmen |
| `MANIFEST.md` | definierter Projekt-/Releasebestand |
| `REGRESSIONSINFOS.md` | Regressionen, Tests und Evidenz |
| `VERSION` | zentrale Versionsquelle |
| `start_tool.sh` | primärer Linux/Kubuntu-Launcher |
| `start_tool.desktop` | Desktop-Starter-Vorlage |
| `.gitignore` | lokale/releasefremde Ausschlüsse |

### Anwendung

| Pfad | Rolle |
|---|---|
| `app/__init__.py` | Root-/Versionszugriff |
| `app/config.py` | validierte atomare Konfigurationspersistenz |
| `app/server.py` | lokaler HTTP/API-Server und statische Oberfläche |
| `web/index.html` | Dashboard-Shell |
| `web/app.js` | UI-Zustand und lokale API-Anbindung |
| `web/styles.css` | Themes, Kontrast und responsive Darstellung |

### Qualität / Release

| Pfad | Rolle |
|---|---|
| `tests/test_config.py` | Persistenzvertrag |
| `tests/test_server.py` | Loopback-/Origin-Sicherheitsvertrag |
| `scripts/validate.py` | Foundation-Vorprüfung |
| `scripts/release.py` | reproduzierbarer ZIP-Builder |
| `.github/workflows/foundation-ci.yml` | automatisierte CI-Gates |
| `runtime/.gitkeep` | Platzhalter; reale Runtime-Inhalte ausgeschlossen |

## Laufzeitvoraussetzungen

- Linux/Kubuntu als primäres Zielsystem.
- Python 3.12 angestrebt; Code nutzt nur Standardbibliothek.
- `python3-venv` muss auf dem Zielsystem verfügbar sein, damit der Launcher `.venv` erstellen kann.
- Browser mit lokalem HTTP-Zugriff; Firefox und Chrome/Chromium sind Zielbrowser.
- `xdg-open` wird bevorzugt, Browser-Fallbacks sind vorgesehen.

## Abhängigkeiten

### Python

**Keine externen Python-Pakete.**

### Browser

- keine externen JavaScript-Bibliotheken,
- keine CDN-Abhängigkeit,
- keine Remote-Fonts.

## Lokale Persistenz

Zur Laufzeit vorgesehen:

```text
runtime/config.json
runtime/config.json.bak
runtime/server.log
runtime/launcher.log
runtime/server.pid
```

Diese Dateien gehören nicht in Releases und nicht in Git.

## Netzwerkvertrag

- Backend bindet ausschließlich an `127.0.0.1`.
- Standardport: `8765`.
- kein Internetzwang.
- keine Telemetrie.
- Host-/Origin-Prüfung auf lokale Herkunft.
- keine CORS-Freigabe.

## Release-Ausschlüsse

- `.venv/`
- `runtime/*` außer `.gitkeep` im Repository
- `__pycache__/`
- Testcache
- `dist/`, `build/`
- lokale Logs
- lokale Profile/Pfade
- Recovery-Daten realer Nutzer
- Secrets/PINs/Passwörter

## Testkommandos

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate.py
bash -n start_tool.sh
node --check web/app.js
python3 scripts/release.py --check
```

## Statusvertrag

Der Codebestand ist **UMGESETZT**. Zielsystem- und CI-Prüfungen dürfen erst nach tatsächlicher Ausführung als **GEPRÜFT** oder **BEWIESEN** markiert werden.

## Nächster Manifest-Schritt

Mit SAFE-FILE-CORE ergänzen:

- Datei-/Ordnerauswahldialog-Vertrag,
- Copy-Job-Datenmodell,
- Vorschau-/Konfliktdaten,
- Undo-/Recovery-Datensatz,
- Job-Persistenz,
- zusätzliche Regressionstests und Release-Gates.

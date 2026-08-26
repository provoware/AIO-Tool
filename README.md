# AIO-Tool

> Saubere Projektgrundlage für ein modulares, laienfreundliches, offline-first All-in-One-Tool.

## Status

- **Phase:** CLEAN FOUNDATION
- **Version:** 0.1.0-foundation
- **Datum:** 2026-08-27
- **Produktcode:** noch nicht begonnen
- **Zielsystem:** primär Linux/Kubuntu; Browser-Oberfläche mit lokalem Backend ist vorgesehen

## Zweck

AIO-Tool soll wiederkehrende Datei-, Projekt-, Organisations- und Automatisierungsaufgaben in einer einheitlichen Oberfläche bündeln. Die Bedienung richtet sich zuerst an Laien und soll technische Entscheidungen soweit möglich automatisch oder über verständliche Auswahlmöglichkeiten auflösen.

## Verbindliche Produktprinzipien

1. **Auswahl vor Zeicheneingabe** – Buttons, Presets und Auswahldialoge haben Vorrang vor Freitext.
2. **Laien zuerst** – Alltagssprache, klare nächste Schritte, kurze Hilfen und sichtbare Empfehlungen.
3. **Offline-first** – Kernfunktionen benötigen kein Internet; keine Telemetrie ohne ausdrückliche Produktentscheidung.
4. **Sicherheit vor Bequemlichkeit** – Vorschau, Vorprüfung, Nachprüfung, Undo/Recovery und nachvollziehbare Änderungen.
5. **Transparenz** – laufende Prozesse, Fortschritt, aktueller Schritt, Fehler und Ergebnis bleiben sichtbar.
6. **Modularität** – Funktionen werden in klar abgegrenzte Module getrennt.
7. **Datensparsamkeit** – nur Daten speichern, die für Funktion, Recovery oder ausdrücklich gewünschte Historie nötig sind.
8. **Wartbarkeit** – kleine, gezielte Änderungen; keine unnötigen Umbauten; klare Zuständigkeiten und Dokumentation.
9. **Regression vor Wiederholung** – bestätigte Fehler erhalten einen reproduzierbaren Regressionstest oder einen begründeten Nachweis, warum das nicht möglich ist.
10. **Beweisbarer Status** – „fertig“, „grün“ oder „sicher“ nur mit überprüfbarer Evidenz.

## Geplante Hauptbereiche

- Dashboard und geführter Workflow
- Projekte und Projektordner
- Favoriten und Schnellaktionen
- Module / Plugin-Struktur
- sichere Dateioperationen
- Aufgaben, Kalender und Notizen
- Verlauf, Reports und Diagnose
- Presets und wiederholbare Workflows
- Job-Queue, Recovery und Undo
- optionaler Expertenbereich

## Dokumentation

| Datei | Zweck |
|---|---|
| `README.md` | Einstieg und Projektüberblick |
| `TOOLBESCHREIBUNG.md` | Produktvision, Zielgruppe und Funktionsrahmen |
| `TODO.md` | priorisierte Entwicklungsarbeit |
| `AGENTS.md` | verbindliche Entwicklungs- und Agentenregeln |
| `CHANGELOG.md` | nachvollziehbare Änderungen je Version |
| `LAIEN-ANLEITUNG.md` | einfache Nutzungserklärung |
| `MANIFEST.md` | definierter Projekt- und Releasebestand |
| `REGRESSIONSINFOS.md` | Regressionen, Prüfregeln und Evidenzschema |

## Entwicklungszustand

Dieses Repository wurde am **27. August 2026** bewusst auf eine saubere Dokumentationsbasis zurückgesetzt. Vorheriger Dateiinhalt ist nicht Teil der neuen Projektgrundlage. Funktionaler Code wird erst nach Festlegung und Prüfung des ersten Entwicklungs-Slices aufgenommen.

## Nächster empfohlener Slice

**SAFE-FILE-CORE**

`Quelle wählen → Aktion wählen → Vorschau → Konflikte erklären → bestätigen → ausführen → nachprüfen → Undo/Recovery`

Dabei gilt: zunächst ein kleiner, vollständig geprüfter Kern statt vieler halbfertiger Funktionen.

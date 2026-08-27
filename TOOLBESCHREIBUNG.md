# TOOLBESCHREIBUNG

## Produktname

**AIO-Tool**

## Produktidee

AIO-Tool ist ein lokaler, modularer All-in-One-Arbeitsplatz für Organisations-, Datei-, Projekt- und Automatisierungsaufgaben. Die Oberfläche richtet sich zuerst an Nutzer ohne technisches Spezialwissen und trennt einfache Bedienung von optionaler Diagnose.

## Leitregel

**Auswahl vor Zeicheneingabe. Sichtbarkeit vor Automatisierung. Sicherheit vor Bequemlichkeit.**

## Aktueller Stand: 0.4.0-dashboard-v2

Dashboard V2 ist die erste zusammenhängende sichtbare Integration der zuvor getrennt getesteten Core-Bausteine.

### Sichtbare Informationsarchitektur

**Linke Spalte**
- Schnellmodule,
- Häufig / Alle,
- optionaler Entwickler-/Diagnosebereich.

**Mitte**
- dauerhaft sichtbarer Monatskalender,
- kommende Termine.

**Rechte Spalte**
- nächste drei TODOs,
- letzte fünf Ereignisse,
- System-/Registry-/Versionsstatus.

**Darüber**
- globaler Systemstatus,
- nächster sinnvoller Schritt,
- fällige Reminder.

## Dashboard-Prinzipien

### 1. Backend bleibt Quelle der Fachlogik

JavaScript berechnet nicht selbst, welches TODO fachlich das nächste ist oder wann ein Reminder fällig wird. Es visualisiert die getesteten API-Antworten.

### 2. Reminder erst nach Sichtbarkeit quittieren

`fällig → sichtbar darstellen → Nutzer bestätigt → ACK persistieren`

Ein Hintergrund-Poll oder unsichtbarer Tab darf keinen gesehenen Zustand erzeugen.

### 3. Progressive Informationsdichte

Das Dashboard zeigt zuerst häufige Module. Zusatzmodule erscheinen über **Alle**. Entwicklerdiagnose ist standardmäßig nur verfügbar, wenn sie in den Einstellungen freigeschaltet wurde.

### 4. Responsive Dichte

Fensterbreite, Fensterhöhe und gewählte Schriftgröße bestimmen den Darstellungsmodus `kompakt`, `normal` oder `weit`. Dies ist eine Präsentationsentscheidung; Fachlogik bleibt unverändert.

### 5. Datensparsame Diagnose

Die Diagnose zeigt technische Kernzustände, keine vollständige Nutzerkonfiguration, Projektpfade oder Favoriten.

## Technischer Kern

### VersionRegistry

Getrackte Historie + lokale Runtime-Registry mit Evidenzvertrag.

### EventRegistry

Persistente menschenlesbare Ereignisse; technische Details getrennt.

### TODO-Core

Persistente Aufgaben, Titelgedächtnis, Priorität, nächste drei TODOs und Erledigt-Archiv.

### Calendar-Core

Persistente Termine, Monats/Wochen/Jahr, Titelgedächtnis, Reminder-Quittierung, optionale TODO-Verknüpfung und lokale `zoneinfo`-/DST-Berechnung.

### Robustheitskern

- atomare Persistenz,
- geprüfte Mustervorlagen,
- positive/negative Testdaten,
- versionierte Core-Texte,
- versionierte Fehlerregeln,
- intelligente Fehlerhilfe,
- `LEARNING_MEMORY.jsonl`,
- Learning Guard,
- reproduzierbarer Release-Builder.

## Dashboard-Textvertrag

`web/dashboard-texts.de.v1.json` lagert wiederkehrende UI-Texte aus. Fehlende oder leere `data-i18n`-Texte werden automatisiert erkannt.

## Dashboard-Regressionsvertrag

`tests/test_dashboard_contract.py` sichert Kernbereiche, API-Verwendung, Reminder-Sicherheit, Textausgabe, Diagnose-Datensparsamkeit, Responsive- und A11y-Marker.

## Sicherheitsphilosophie für spätere Dateioperationen

`Vorprüfung → Vorschau → Bestätigung → Aktion → Nachprüfung → Protokoll → Undo/Recovery`

Dateioperationen sind in Dashboard V2 noch bewusst deaktiviert. Sie folgen erst nach realer UI-/Zielsystemabnahme.

## Nachweis

Code-Gate `33026823914`: 77 Tests + vollständige CI erfolgreich; Release `AIO-Tool-0.4.0-dashboard-v2.zip` wurde erzeugt.

## Noch nicht als bestanden behauptet

- reale Kubuntu-Bedienung,
- Firefox/Chrome/Chromium,
- 125–200 % Zoom,
- echte Tastatur-/Fokusreihenfolge,
- unterschiedliche reale Displaygrößen.

## Nächste Produktstufe

Nach erfolgreicher Zielsystemabnahme beginnt SAFE-FILE-CORE mit **Copy** als erster kontrollierter Dateioperation. Erst wenn Copy inklusive Vorschau, Nachprüfung, Abbruch und Recovery stabil ist, folgen Move, Rename und Papierkorb/Delete.

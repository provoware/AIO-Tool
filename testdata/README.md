# Testdaten

Diese Dateien sind absichtlich in **gültige** und **ungültige** Beispiele getrennt.

- `valid/` muss von den aktuellen Validatoren akzeptiert werden.
- `invalid/` bildet bekannte Fehlerklassen reproduzierbar ab und muss gezielt abgelehnt werden.
- `config.corrupt-json.txt` ist absichtlich kein gültiges JSON und prüft Parser-/Korruptionspfade.

Neue Datenformate sollen mindestens eine gültige Musterdatei und relevante negative Testfälle erhalten. Testdaten dürfen niemals als echte Nutzerdaten behandelt oder automatisch in `runtime/` kopiert werden.

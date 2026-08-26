from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any

from . import VERSION

THEMES = {"trash-neon", "steel-night", "clean-light", "high-contrast"}
FONT_SCALES = {90, 100, 110, 120, 130, 140}

DEFAULT_CONFIG: dict[str, Any] = {
    "version": VERSION,
    "theme": "steel-night",
    "font_scale": 100,
    "expert_visible": False,
    "setup_complete": False,
    "active_project": None,
    "favorites": ["projects", "history", "reports"],
}


class ConfigError(ValueError):
    pass


def validate_config(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ConfigError("Konfiguration muss ein Objekt sein.")
    result = deepcopy(DEFAULT_CONFIG)
    result.update(value)
    if result["theme"] not in THEMES:
        raise ConfigError("Unbekanntes Theme.")
    if result["font_scale"] not in FONT_SCALES:
        raise ConfigError("Ungültige Schriftgröße.")
    if not isinstance(result["expert_visible"], bool):
        raise ConfigError("expert_visible muss true/false sein.")
    if not isinstance(result["setup_complete"], bool):
        raise ConfigError("setup_complete muss true/false sein.")
    if result["active_project"] is not None and not isinstance(result["active_project"], str):
        raise ConfigError("active_project muss Text oder leer sein.")
    if not isinstance(result["favorites"], list) or not all(isinstance(x, str) for x in result["favorites"]):
        raise ConfigError("favorites muss eine Textliste sein.")
    result["version"] = VERSION
    return result


class ConfigStore:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.backup = self.path.with_suffix(self.path.suffix + ".bak")

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return deepcopy(DEFAULT_CONFIG)
        try:
            return validate_config(json.loads(self.path.read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError, ConfigError):
            if self.backup.exists():
                try:
                    return validate_config(json.loads(self.backup.read_text(encoding="utf-8")))
                except (OSError, json.JSONDecodeError, ConfigError):
                    pass
            raise ConfigError("Konfiguration ist beschädigt und kein gültiges Backup ist verfügbar.")

    def save(self, value: dict[str, Any]) -> dict[str, Any]:
        clean = validate_config(value)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix(self.path.suffix + ".tmp")
        payload = json.dumps(clean, ensure_ascii=False, indent=2) + "\n"
        if self.path.exists():
            self.backup.write_bytes(self.path.read_bytes())
            with self.backup.open("rb") as handle:
                os.fsync(handle.fileno())
        with temp.open("w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, self.path)
        try:
            directory_fd = os.open(str(self.path.parent), os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        except OSError:
            pass
        return clean

    def update(self, changes: dict[str, Any]) -> dict[str, Any]:
        current = self.load()
        current.update(changes)
        return self.save(current)

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from . import VERSION
from .persistence import AtomicJsonStore, PersistenceError

THEMES = {"aurora-glass", "trash-neon", "steel-night", "clean-light", "high-contrast"}
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


class ConfigIntegrityError(ConfigError):
    """The stored configuration cannot be safely recovered."""


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
    """Configuration facade using the shared atomic/thread-safe persistence core."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.backup = self.path.with_suffix(self.path.suffix + ".bak")
        self._store = AtomicJsonStore(self.path, DEFAULT_CONFIG, validate_config)

    def load(self) -> dict[str, Any]:
        try:
            return self._store.load()
        except PersistenceError as exc:
            raise ConfigIntegrityError("Konfiguration ist beschädigt und kein gültiges Backup ist verfügbar.") from exc

    def save(self, value: dict[str, Any]) -> dict[str, Any]:
        return self._store.save(value)

    def update(self, changes: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(changes, dict):
            raise ConfigError("Änderungen müssen ein Objekt sein.")

        def mutate(current: dict[str, Any]) -> dict[str, Any]:
            current.update(changes)
            return current

        try:
            return self._store.update(mutate)
        except PersistenceError as exc:
            raise ConfigIntegrityError("Konfiguration ist beschädigt und kein gültiges Backup ist verfügbar.") from exc

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1


class TextCatalogError(ValueError):
    """Fehler in einem versionierten Textkatalog."""


def validate_catalog(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict) or value.get("schema_version") != SCHEMA_VERSION:
        raise TextCatalogError("Unbekanntes Textkatalog-Schema.")
    catalog_version = value.get("catalog_version")
    language = value.get("language")
    messages = value.get("messages")
    if not isinstance(catalog_version, str) or not catalog_version.strip():
        raise TextCatalogError("catalog_version fehlt.")
    if not isinstance(language, str) or not language.strip():
        raise TextCatalogError("language fehlt.")
    if not isinstance(messages, dict) or not messages:
        raise TextCatalogError("messages fehlt oder ist leer.")
    clean: dict[str, str] = {}
    for key, text in messages.items():
        if not isinstance(key, str) or not key.strip():
            raise TextCatalogError("Textschlüssel muss nichtleerer Text sein.")
        if not isinstance(text, str) or not text.strip():
            raise TextCatalogError(f"Text '{key}' muss nichtleer sein.")
        clean[key.strip()] = text.strip()
    return {
        "schema_version": SCHEMA_VERSION,
        "catalog_version": catalog_version.strip(),
        "language": language.strip(),
        "messages": clean,
    }


class TextCatalog:
    def __init__(self, path: Path):
        self.path = Path(path)
        self._data = self._load()

    def _load(self) -> dict[str, Any]:
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise TextCatalogError(f"Textkatalog '{self.path}' ist nicht lesbar.") from exc
        return validate_catalog(raw)

    @property
    def version(self) -> str:
        return self._data["catalog_version"]

    @property
    def language(self) -> str:
        return self._data["language"]

    def get(self, key: str, **values: object) -> str:
        if key not in self._data["messages"]:
            raise TextCatalogError(f"Textschlüssel '{key}' fehlt.")
        text = self._data["messages"][key]
        if not values:
            return text
        try:
            return text.format(**values)
        except (KeyError, ValueError) as exc:
            raise TextCatalogError(f"Text '{key}' konnte nicht formatiert werden.") from exc

    def metadata(self) -> dict[str, object]:
        return {
            "schema_version": self._data["schema_version"],
            "catalog_version": self.version,
            "language": self.language,
            "message_count": len(self._data["messages"]),
        }

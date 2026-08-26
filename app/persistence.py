from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable


class PersistenceError(ValueError):
    """Raised when persistent state cannot be validated or recovered."""


Validator = Callable[[dict[str, Any]], dict[str, Any]]


class AtomicJsonStore:
    """Small dependency-free JSON store with atomic replace and backup fallback."""

    def __init__(self, path: Path, default: dict[str, Any], validator: Validator):
        self.path = Path(path)
        self.backup = self.path.with_suffix(self.path.suffix + ".bak")
        self.default = deepcopy(default)
        self.validator = validator

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return deepcopy(self.default)
        try:
            return self.validator(self._read(self.path))
        except (OSError, json.JSONDecodeError, PersistenceError, ValueError, TypeError):
            if self.backup.exists():
                try:
                    return self.validator(self._read(self.backup))
                except (OSError, json.JSONDecodeError, PersistenceError, ValueError, TypeError):
                    pass
            raise PersistenceError(
                f"Persistenzdatei '{self.path.name}' ist beschädigt und kein gültiges Backup ist verfügbar."
            )

    def save(self, value: dict[str, Any]) -> dict[str, Any]:
        clean = self.validator(value)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix(self.path.suffix + ".tmp")
        payload = json.dumps(clean, ensure_ascii=False, indent=2) + "\n"

        if self.path.exists():
            self.backup.write_bytes(self.path.read_bytes())
            self._fsync_file(self.backup)

        with temp.open("w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())

        os.replace(temp, self.path)
        self._fsync_directory(self.path.parent)
        return clean

    def update(self, mutator: Callable[[dict[str, Any]], dict[str, Any] | None]) -> dict[str, Any]:
        current = self.load()
        candidate = mutator(deepcopy(current))
        return self.save(current if candidate is None else candidate)

    @staticmethod
    def _read(path: Path) -> dict[str, Any]:
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise PersistenceError("Persistenzinhalt muss ein JSON-Objekt sein.")
        return value

    @staticmethod
    def _fsync_file(path: Path) -> None:
        try:
            with path.open("rb") as handle:
                os.fsync(handle.fileno())
        except OSError:
            pass

    @staticmethod
    def _fsync_directory(path: Path) -> None:
        try:
            directory_fd = os.open(str(path), os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        except OSError:
            pass

from __future__ import annotations

import json
import os
import threading
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable


class PersistenceError(ValueError):
    """Raised when persistent state cannot be validated or recovered."""


Validator = Callable[[dict[str, Any]], dict[str, Any]]


class AtomicJsonStore:
    """Dependency-free JSON store with validation, backup fallback and atomic writes.

    The store is safe against concurrent access from threads sharing the same store
    instance. AIO-Tool's HTTP servers are threaded, so load/update/save must behave
    as one serialized transaction inside the process.
    """

    def __init__(self, path: Path, default: dict[str, Any], validator: Validator):
        self.path = Path(path)
        self.backup = self.path.with_suffix(self.path.suffix + ".bak")
        self.default = deepcopy(default)
        self.validator = validator
        self._lock = threading.RLock()

    def load(self) -> dict[str, Any]:
        with self._lock:
            return self._load_unlocked()

    def save(self, value: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            return self._save_unlocked(value)

    def update(self, mutator: Callable[[dict[str, Any]], dict[str, Any] | None]) -> dict[str, Any]:
        with self._lock:
            current = self._load_unlocked()
            candidate = mutator(deepcopy(current))
            return self._save_unlocked(current if candidate is None else candidate)

    def _load_unlocked(self) -> dict[str, Any]:
        if not self.path.exists():
            return self.validator(deepcopy(self.default))
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

    def _save_unlocked(self, value: dict[str, Any]) -> dict[str, Any]:
        clean = self.validator(value)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = (json.dumps(clean, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

        if self.path.exists():
            # Backup itself is replaced atomically as well. A crash while refreshing
            # the backup must not destroy the last known-good recovery copy.
            self._atomic_write_bytes(self.backup, self.path.read_bytes())

        self._atomic_write_bytes(self.path, payload)
        self._fsync_directory(self.path.parent)
        return clean

    @staticmethod
    def _read(path: Path) -> dict[str, Any]:
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise PersistenceError("Persistenzinhalt muss ein JSON-Objekt sein.")
        return value

    @classmethod
    def _atomic_write_bytes(cls, path: Path, payload: bytes) -> None:
        temp = path.with_suffix(path.suffix + ".tmp")
        try:
            with temp.open("wb") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp, path)
        finally:
            # A failed write may leave a stale temp file. Remove only our temp path;
            # the current file and backup are never touched here.
            try:
                if temp.exists():
                    temp.unlink()
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
            # Some filesystems/platforms do not support directory fsync. The file
            # data itself has already been fsynced before replace.
            pass

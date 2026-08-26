from pathlib import Path
import tempfile
import unittest

from app.persistence import AtomicJsonStore, PersistenceError


def validate(value):
    if value.get("schema_version") != 1 or not isinstance(value.get("value"), int):
        raise PersistenceError("ungültig")
    return {"schema_version": 1, "value": value["value"]}


class AtomicJsonStoreTests(unittest.TestCase):
    def test_roundtrip_and_backup_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            store = AtomicJsonStore(path, {"schema_version": 1, "value": 0}, validate)
            store.save({"schema_version": 1, "value": 1})
            store.save({"schema_version": 1, "value": 2})
            path.write_text("{kaputt", encoding="utf-8")
            self.assertEqual(store.load()["value"], 1)

    def test_default_is_not_shared(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = AtomicJsonStore(Path(tmp) / "state.json", {"schema_version": 1, "value": 0}, validate)
            first = store.load()
            first["value"] = 99
            self.assertEqual(store.load()["value"], 0)


if __name__ == "__main__":
    unittest.main()

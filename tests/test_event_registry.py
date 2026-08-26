from pathlib import Path
import tempfile
import unittest

from app.event_registry import EventRegistry, EventRegistryError


class EventRegistryTests(unittest.TestCase):
    def test_latest_returns_newest_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = EventRegistry(Path(tmp) / "events.json")
            first = registry.add(kind="one", message="Erstes Ereignis.", when="2026-08-27T00:00:00+00:00")
            second = registry.add(kind="two", message="Zweites Ereignis.", when="2026-08-27T00:01:00+00:00")
            latest = registry.latest(2)
            self.assertEqual(latest[0]["id"], second["id"])
            self.assertEqual(latest[1]["id"], first["id"])

    def test_limit_is_checked(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = EventRegistry(Path(tmp) / "events.json")
            with self.assertRaises(EventRegistryError):
                registry.latest(0)

    def test_message_must_be_human_readable_nonempty_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = EventRegistry(Path(tmp) / "events.json")
            with self.assertRaises(EventRegistryError):
                registry.add(kind="test", message="   ")


if __name__ == "__main__":
    unittest.main()

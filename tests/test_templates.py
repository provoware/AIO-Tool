import json
import unittest

from app import ROOT_DIR
from app.calendar_store import CalendarStoreError, validate_calendar
from app.config import ConfigError, validate_config
from app.event_registry import EventRegistryError, validate_events
from app.todo_store import TodoStoreError, validate_todos
from app.version_registry import VersionRegistryError, validate_registry


class TemplateAndFixtureTests(unittest.TestCase):
    def _json(self, rel: str):
        return json.loads((ROOT_DIR / rel).read_text(encoding="utf-8"))

    def test_reference_templates_match_current_validators(self):
        validate_config(self._json("resources/templates/config/config.v1.example.json"))
        validate_registry(self._json("resources/templates/version_registry/version_registry.v1.example.json"))
        validate_events(self._json("resources/templates/events/events.v1.example.json"))
        validate_todos(self._json("resources/templates/todos/todos.v1.example.json"))
        validate_calendar(self._json("resources/templates/calendar/calendar.v1.example.json"))

    def test_valid_testdata_uses_same_contracts(self):
        validate_config(self._json("testdata/valid/config.v1.json"))
        validate_registry(self._json("testdata/valid/version_registry.v1.json"))
        validate_events(self._json("testdata/valid/events.v1.json"))
        validate_todos(self._json("testdata/valid/todos.v1.json"))
        validate_calendar(self._json("testdata/valid/calendar.v1.json"))

    def test_invalid_config_theme_is_rejected(self):
        with self.assertRaises(ConfigError):
            validate_config(self._json("testdata/invalid/config.invalid-theme.v1.json"))

    def test_corrupt_config_is_not_valid_json(self):
        path = ROOT_DIR / "testdata" / "invalid" / "config.corrupt-json.txt"
        with self.assertRaises(json.JSONDecodeError):
            json.loads(path.read_text(encoding="utf-8"))

    def test_duplicate_version_is_rejected(self):
        with self.assertRaises(VersionRegistryError):
            validate_registry(self._json("testdata/invalid/version_registry.duplicate.v1.json"))

    def test_empty_event_message_is_rejected(self):
        with self.assertRaises(EventRegistryError):
            validate_events(self._json("testdata/invalid/events.empty-message.v1.json"))

    def test_duplicate_todo_title_memory_is_rejected(self):
        with self.assertRaises(TodoStoreError):
            validate_todos(self._json("testdata/invalid/todos.duplicate-title-memory.v1.json"))

    def test_calendar_end_before_start_is_rejected(self):
        with self.assertRaises(CalendarStoreError):
            validate_calendar(self._json("testdata/invalid/calendar.end-before-start.v1.json"))

    def test_calendar_reminder_without_time_is_rejected(self):
        with self.assertRaises(CalendarStoreError):
            validate_calendar(self._json("testdata/invalid/calendar.reminder-without-time.v1.json"))


if __name__ == "__main__":
    unittest.main()

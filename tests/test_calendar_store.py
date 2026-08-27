from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from zoneinfo import ZoneInfo

from app.calendar_store import CalendarStore, CalendarStoreError, validate_calendar


class CalendarStoreTests(unittest.TestCase):
    def test_create_persists_event_and_remembers_title(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CalendarStore(Path(tmp) / "calendar.json")
            event = store.create(
                title="Projektbesprechung",
                date="2026-08-27",
                start_time="14:00",
                end_time="14:30",
                reminders=[30, 10],
                todo_id="todo-optional",
            )
            self.assertEqual(store.get(event["id"])["todo_id"], "todo-optional")
            self.assertEqual(store.title_suggestions(1)[0]["title"], "Projektbesprechung")
            self.assertEqual([r["minutes_before"] for r in event["reminders"]], [30, 10])

    def test_title_memory_is_case_insensitive(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CalendarStore(Path(tmp) / "calendar.json")
            store.create(title="Backup prüfen", date="2026-08-27")
            store.create(title="backup PRÜFEN", date="2026-08-28")
            suggestions = store.title_suggestions()
            self.assertEqual(len(suggestions), 1)
            self.assertEqual(suggestions[0]["count"], 2)

    def test_month_view_uses_real_month_boundaries(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CalendarStore(Path(tmp) / "calendar.json")
            store.create(title="Februar", date="2028-02-29")
            store.create(title="März", date="2028-03-01")
            result = store.period("month", "2028-02-15")
            self.assertEqual(result["start"], "2028-02-01")
            self.assertEqual(result["end"], "2028-02-29")
            self.assertEqual([e["title"] for e in result["events"]], ["Februar"])

    def test_week_view_is_monday_to_sunday(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CalendarStore(Path(tmp) / "calendar.json")
            result = store.period("week", "2026-08-27")
            self.assertEqual(result["start"], "2026-08-24")
            self.assertEqual(result["end"], "2026-08-30")

    def test_year_view_covers_full_year(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CalendarStore(Path(tmp) / "calendar.json")
            store.create(title="Januar", date="2026-01-01")
            store.create(title="Dezember", date="2026-12-31")
            result = store.period("year", "2026-06-15")
            self.assertEqual(result["start"], "2026-01-01")
            self.assertEqual(result["end"], "2026-12-31")
            self.assertEqual(len(result["events"]), 2)

    def test_reminder_requires_start_time(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CalendarStore(Path(tmp) / "calendar.json")
            with self.assertRaises(CalendarStoreError):
                store.create(title="Ohne Uhrzeit", date="2026-08-27", reminders=[10])

    def test_end_time_must_follow_start_time(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CalendarStore(Path(tmp) / "calendar.json")
            with self.assertRaises(CalendarStoreError):
                store.create(title="Zeitfehler", date="2026-08-27", start_time="14:00", end_time="13:00")

    def test_due_reminder_is_acknowledged_and_not_returned_again(self):
        with tempfile.TemporaryDirectory() as tmp, patch("app.calendar_store.system_timezone", return_value=ZoneInfo("UTC")):
            store = CalendarStore(Path(tmp) / "calendar.json")
            event = store.create(title="Test", date="2026-08-27", start_time="10:00", reminders=[10])
            due = store.due_reminders("2026-08-27T09:50:00+00:00")
            self.assertEqual(len(due), 1)
            self.assertEqual(due[0]["minutes_before"], 10)
            store.acknowledge_reminder(event["id"], 10, when="2026-08-27T09:50:05+00:00")
            self.assertEqual(store.due_reminders("2026-08-27T09:51:00+00:00"), [])

    def test_zoneinfo_uses_target_date_dst_offset(self):
        with tempfile.TemporaryDirectory() as tmp, patch("app.calendar_store.system_timezone", return_value=ZoneInfo("Europe/Berlin")):
            store = CalendarStore(Path(tmp) / "calendar.json")
            store.create(title="Wintertermin", date="2026-11-01", start_time="10:00", reminders=[60])
            due = store.due_reminders("2026-11-01T09:00:00+01:00")
            self.assertEqual(len(due), 1)
            self.assertTrue(due[0]["trigger_at"].endswith("+01:00"))

    def test_unknown_timezone_mode_is_rejected(self):
        with self.assertRaises(CalendarStoreError):
            validate_calendar({
                "schema_version": 1,
                "events": [{
                    "id": "x", "title": "x", "date": "2026-08-27",
                    "start_time": None, "end_time": None, "category": None,
                    "description": None, "todo_id": None, "timezone": "UTC",
                    "reminders": [], "created_at": "2026-08-27T01:00:00+02:00",
                    "updated_at": "2026-08-27T01:00:00+02:00"
                }],
                "title_memory": []
            })


if __name__ == "__main__":
    unittest.main()

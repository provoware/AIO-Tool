from pathlib import Path
import tempfile
import unittest

from app.todo_store import TodoStore


class TodoStoreTests(unittest.TestCase):
    def test_title_memory_counts_and_reoffers_titles(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = TodoStore(Path(tmp) / "todos.json")
            store.create(title="Backup prüfen")
            store.create(title="backup prüfen")
            suggestions = store.title_suggestions()
            self.assertEqual(len(suggestions), 1)
            self.assertEqual(suggestions[0]["count"], 2)
            self.assertEqual(suggestions[0]["title"], "backup prüfen")

    def test_complete_moves_item_to_archive_with_timestamp(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = TodoStore(Path(tmp) / "todos.json")
            item = store.create(title="Test erledigen", due_date="2026-08-27")
            completed = store.complete(item["id"], when="2026-08-27T12:34:56+00:00")
            data = store.load()
            self.assertEqual(data["items"], [])
            self.assertEqual(len(data["archive"]), 1)
            self.assertEqual(completed["completed_at"], "2026-08-27T12:34:56+00:00")
            self.assertEqual(completed["created_at"], item["created_at"])

    def test_next_three_prefers_earlier_due_date_then_priority(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = TodoStore(Path(tmp) / "todos.json")
            store.create(title="Später", due_date="2026-09-02", priority="high")
            store.create(title="Heute normal", due_date="2026-08-27", priority="normal")
            store.create(title="Heute hoch", due_date="2026-08-27", priority="high")
            store.create(title="Ohne Termin", priority="high")
            titles = [item["title"] for item in store.next_items(3)]
            self.assertEqual(titles, ["Heute hoch", "Heute normal", "Später"])

    def test_calendar_link_is_optional(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = TodoStore(Path(tmp) / "todos.json")
            item = store.create(title="Ohne Kalender")
            self.assertIsNone(item["calendar_event_id"])


if __name__ == "__main__":
    unittest.main()

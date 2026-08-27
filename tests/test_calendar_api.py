import http.client
import json
from pathlib import Path
import tempfile
from threading import Thread
import unittest
from unittest.mock import patch
from urllib.parse import urlencode

from app.calendar_store import CalendarStore
from app.config import ConfigStore
from app.event_registry import EventRegistry
from app.todo_store import TodoStore
from app.version_registry import VersionRegistry
import app.server as server_module


class CalendarApiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.runtime = Path(self.temp.name)
        self.config = ConfigStore(self.runtime / "config.json")
        self.versions = VersionRegistry(self.runtime / "versions.json")
        self.events = EventRegistry(self.runtime / "events.json")
        self.todos = TodoStore(self.runtime / "todos.json")
        self.calendar = CalendarStore(self.runtime / "calendar.json")
        self.patchers = [
            patch.object(server_module, "RUNTIME_DIR", self.runtime),
            patch.object(server_module, "CONFIG_STORE", self.config),
            patch.object(server_module, "VERSION_REGISTRY", self.versions),
            patch.object(server_module, "EVENT_REGISTRY", self.events),
            patch.object(server_module, "TODO_STORE", self.todos),
            patch.object(server_module, "CALENDAR_STORE", self.calendar),
        ]
        for patcher in self.patchers:
            patcher.start()
        self.httpd = server_module.create_server(0)
        self.port = self.httpd.server_address[1]
        self.thread = Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=2)
        for patcher in reversed(self.patchers):
            patcher.stop()
        self.temp.cleanup()

    def test_create_and_read_month_view(self):
        status, payload = self.request("POST", "/api/calendar", {
            "title": "Projektbesprechung",
            "date": "2026-08-27",
            "start_time": "14:00",
            "end_time": "14:30",
            "reminders": [30, 10],
        })
        self.assertEqual(status, 201)
        event_id = payload["event"]["id"]

        status, payload = self.request("GET", "/api/calendar?view=month&date=2026-08-15")
        self.assertEqual(status, 200)
        self.assertEqual(payload["calendar"]["start"], "2026-08-01")
        self.assertEqual(payload["calendar"]["end"], "2026-08-31")
        self.assertEqual(payload["calendar"]["events"][0]["id"], event_id)

        messages = [item["message"] for item in self.events.latest(5)]
        self.assertTrue(any("Projektbesprechung" in message for message in messages))

    def test_title_suggestion_after_create(self):
        self.request("POST", "/api/calendar", {"title": "Arzttermin", "date": "2026-09-01"})
        status, payload = self.request("GET", "/api/calendar/suggestions?limit=3")
        self.assertEqual(status, 200)
        self.assertEqual(payload["titles"][0]["title"], "Arzttermin")

    def test_todo_link_is_optional_but_must_exist_when_supplied(self):
        status, payload = self.request("POST", "/api/calendar", {"title": "Ohne TODO", "date": "2026-09-01"})
        self.assertEqual(status, 201)
        self.assertIsNone(payload["event"]["todo_id"])

        status, _ = self.request("POST", "/api/calendar", {
            "title": "Ungültiger Link", "date": "2026-09-01", "todo_id": "fehlt"
        })
        self.assertEqual(status, 400)

        todo = self.todos.create(title="Dokument prüfen")
        status, payload = self.request("POST", "/api/calendar", {
            "title": "Mit TODO", "date": "2026-09-02", "todo_id": todo["id"]
        })
        self.assertEqual(status, 201)
        self.assertEqual(payload["event"]["todo_id"], todo["id"])

    def test_due_reminder_can_be_acknowledged(self):
        status, payload = self.request("POST", "/api/calendar", {
            "title": "Reminder",
            "date": "2026-08-27",
            "start_time": "10:00",
            "reminders": [10],
        })
        event_id = payload["event"]["id"]
        query = urlencode({"now": "2026-08-27T23:00:00+00:00"})
        status, payload = self.request("GET", f"/api/calendar/reminders/due?{query}")
        self.assertEqual(status, 200)
        self.assertEqual(len(payload["reminders"]), 1)

        status, payload = self.request(
            "POST",
            f"/api/calendar/{event_id}/reminders/10/ack",
            {"when": "2026-08-27T23:00:01+00:00"},
        )
        self.assertEqual(status, 200)
        reminder = payload["event"]["reminders"][0]
        self.assertIsNotNone(reminder["notified_at"])

        status, payload = self.request("GET", f"/api/calendar/reminders/due?{query}")
        self.assertEqual(payload["reminders"], [])

    def test_invalid_reminder_gets_calendar_guidance(self):
        status, payload = self.request("POST", "/api/calendar", {
            "title": "Fehler",
            "date": "2026-08-27",
            "start_time": "10:00",
            "reminders": [15],
        })
        self.assertEqual(status, 400)
        self.assertEqual(payload["help"]["rule_id"], "ERR-CALENDAR-REMINDER-001")
        self.assertEqual(payload["help"]["template_path"], "resources/templates/calendar/calendar.v1.example.json")

    def test_status_reports_calendar_count(self):
        self.calendar.create(title="Status", date="2026-08-27")
        status, payload = self.request("GET", "/api/status")
        self.assertEqual(status, 200)
        self.assertEqual(payload["core"]["calendar_events"], 1)

    def request(self, method: str, path: str, body: dict | None = None):
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=3)
        headers = {"Host": f"127.0.0.1:{self.port}"}
        payload = None
        if body is not None:
            payload = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
            headers["Origin"] = f"http://127.0.0.1:{self.port}"
        connection.request(method, path, body=payload, headers=headers)
        response = connection.getresponse()
        content = json.loads(response.read().decode("utf-8"))
        status = response.status
        connection.close()
        return status, content


if __name__ == "__main__":
    unittest.main()

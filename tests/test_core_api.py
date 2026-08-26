import http.client
import json
from pathlib import Path
import tempfile
from threading import Thread
import unittest
from unittest.mock import patch

from app import VERSION
from app.config import ConfigStore
from app.event_registry import EventRegistry
from app.todo_store import TodoStore
from app.version_registry import VersionRegistry
import app.server as server_module


class CoreApiTests(unittest.TestCase):
    def test_registry_todo_and_event_flow(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = Path(tmp)
            config = ConfigStore(runtime / "config.json")
            versions = VersionRegistry(runtime / "versions.json")
            events = EventRegistry(runtime / "events.json")
            todos = TodoStore(runtime / "todos.json")

            with patch.object(server_module, "RUNTIME_DIR", runtime), \
                 patch.object(server_module, "CONFIG_STORE", config), \
                 patch.object(server_module, "VERSION_REGISTRY", versions), \
                 patch.object(server_module, "EVENT_REGISTRY", events), \
                 patch.object(server_module, "TODO_STORE", todos):
                httpd = server_module.create_server(0)
                port = httpd.server_address[1]
                thread = Thread(target=httpd.serve_forever, daemon=True)
                thread.start()
                try:
                    status, payload = self._request(port, "GET", "/api/versions")
                    self.assertEqual(status, 200)
                    self.assertEqual(payload["registry"]["current_version"], VERSION)
                    self.assertTrue(payload["consistency"]["ok"])

                    status, payload = self._request(
                        port,
                        "POST",
                        "/api/todos",
                        {"title": "Dashboard prüfen", "priority": "high"},
                    )
                    self.assertEqual(status, 201)
                    todo_id = payload["item"]["id"]

                    status, payload = self._request(port, "GET", "/api/todos/suggestions")
                    self.assertEqual(status, 200)
                    self.assertEqual(payload["titles"][0]["title"], "Dashboard prüfen")

                    status, payload = self._request(port, "POST", f"/api/todos/{todo_id}/complete", {})
                    self.assertEqual(status, 200)
                    self.assertIn("completed_at", payload["item"])

                    status, payload = self._request(port, "GET", "/api/todos")
                    self.assertEqual(status, 200)
                    self.assertEqual(payload["items"], [])
                    self.assertEqual(payload["archive_count"], 1)

                    status, payload = self._request(port, "GET", "/api/events?limit=5")
                    self.assertEqual(status, 200)
                    messages = [event["message"] for event in payload["events"]]
                    self.assertTrue(any("ins Archiv verschoben" in message for message in messages))
                finally:
                    httpd.shutdown()
                    httpd.server_close()
                    thread.join(timeout=2)

    @staticmethod
    def _request(port: int, method: str, path: str, body: dict | None = None):
        connection = http.client.HTTPConnection("127.0.0.1", port, timeout=3)
        headers = {"Host": f"127.0.0.1:{port}"}
        payload = None
        if body is not None:
            payload = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
            headers["Origin"] = f"http://127.0.0.1:{port}"
        connection.request(method, path, body=payload, headers=headers)
        response = connection.getresponse()
        content = json.loads(response.read().decode("utf-8"))
        status = response.status
        connection.close()
        return status, content


if __name__ == "__main__":
    unittest.main()

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

            with self._patched_server(runtime, config, versions, events, todos):
                httpd, thread, port = self._start_server()
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
                    self._stop_server(httpd, thread)

    def test_help_metadata_is_versioned(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = Path(tmp)
            with self._patched_server(
                runtime,
                ConfigStore(runtime / "config.json"),
                VersionRegistry(runtime / "versions.json"),
                EventRegistry(runtime / "events.json"),
                TodoStore(runtime / "todos.json"),
            ):
                httpd, thread, port = self._start_server()
                try:
                    status, payload = self._request(port, "GET", "/api/help/meta")
                    self.assertEqual(status, 200)
                    self.assertEqual(payload["help"]["rules_version"], "1.0.0")
                    self.assertEqual(payload["help"]["text_catalog"]["catalog_version"], "1.0.0")
                finally:
                    self._stop_server(httpd, thread)

    def test_invalid_limit_is_client_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = Path(tmp)
            with self._patched_server(
                runtime,
                ConfigStore(runtime / "config.json"),
                VersionRegistry(runtime / "versions.json"),
                EventRegistry(runtime / "events.json"),
                TodoStore(runtime / "todos.json"),
            ):
                httpd, thread, port = self._start_server()
                try:
                    status, payload = self._request(port, "GET", "/api/events?limit=abc")
                    self.assertEqual(status, 400)
                    self.assertIn("help", payload)
                    self.assertEqual(payload["help"]["area"], "API")
                finally:
                    self._stop_server(httpd, thread)

    def test_corrupted_event_registry_is_server_integrity_error_with_help(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = Path(tmp)
            events = EventRegistry(runtime / "events.json")
            with self._patched_server(
                runtime,
                ConfigStore(runtime / "config.json"),
                VersionRegistry(runtime / "versions.json"),
                events,
                TodoStore(runtime / "todos.json"),
            ):
                httpd, thread, port = self._start_server()
                try:
                    events.store.path.write_text("{kaputt", encoding="utf-8")
                    status, payload = self._request(port, "GET", "/api/events")
                    self.assertEqual(status, 500)
                    self.assertEqual(payload["help"]["category"], "integrity")
                    self.assertEqual(payload["help"]["rule_id"], "ERR-PERSIST-001")
                    self.assertFalse(payload["help"]["retry_safe"])
                finally:
                    self._stop_server(httpd, thread)

    def test_invalid_theme_is_client_error_with_button_guidance(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = Path(tmp)
            with self._patched_server(
                runtime,
                ConfigStore(runtime / "config.json"),
                VersionRegistry(runtime / "versions.json"),
                EventRegistry(runtime / "events.json"),
                TodoStore(runtime / "todos.json"),
            ):
                httpd, thread, port = self._start_server()
                try:
                    status, payload = self._request(port, "POST", "/api/config", {"theme": "unbekannt"})
                    self.assertEqual(status, 400)
                    self.assertEqual(payload["help"]["rule_id"], "ERR-CONFIG-THEME-001")
                    self.assertTrue(payload["help"]["retry_safe"])
                    self.assertIn("Buttons", payload["help"]["action"])
                    self.assertEqual(payload["help"]["template_path"], "resources/templates/config/config.v1.example.json")
                finally:
                    self._stop_server(httpd, thread)

    def test_corrupted_config_is_server_integrity_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = Path(tmp)
            config = ConfigStore(runtime / "config.json")
            with self._patched_server(
                runtime,
                config,
                VersionRegistry(runtime / "versions.json"),
                EventRegistry(runtime / "events.json"),
                TodoStore(runtime / "todos.json"),
            ):
                httpd, thread, port = self._start_server()
                try:
                    config.path.write_text("{kaputt", encoding="utf-8")
                    status, payload = self._request(port, "POST", "/api/config", {"theme": "clean-light"})
                    self.assertEqual(status, 500)
                    self.assertEqual(payload["help"]["category"], "integrity")
                    self.assertEqual(payload["help"]["severity"], "red")
                finally:
                    self._stop_server(httpd, thread)

    def test_todo_survives_broken_event_log_and_returns_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = Path(tmp)
            events = EventRegistry(runtime / "events.json")
            todos = TodoStore(runtime / "todos.json")
            with self._patched_server(
                runtime,
                ConfigStore(runtime / "config.json"),
                VersionRegistry(runtime / "versions.json"),
                events,
                todos,
            ):
                events.store.path.write_text("{kaputt", encoding="utf-8")
                httpd, thread, port = self._start_server()
                try:
                    status, payload = self._request(port, "POST", "/api/todos", {"title": "Bleibt gespeichert"})
                    self.assertEqual(status, 201)
                    self.assertIn("warning", payload)
                    self.assertEqual(todos.load()["items"][0]["title"], "Bleibt gespeichert")
                finally:
                    self._stop_server(httpd, thread)

    @staticmethod
    def _patched_server(runtime, config, versions, events, todos):
        class PatchGroup:
            def __enter__(self_inner):
                self_inner.patchers = [
                    patch.object(server_module, "RUNTIME_DIR", runtime),
                    patch.object(server_module, "CONFIG_STORE", config),
                    patch.object(server_module, "VERSION_REGISTRY", versions),
                    patch.object(server_module, "EVENT_REGISTRY", events),
                    patch.object(server_module, "TODO_STORE", todos),
                ]
                for patcher in self_inner.patchers:
                    patcher.start()
                return self_inner

            def __exit__(self_inner, exc_type, exc, tb):
                for patcher in reversed(self_inner.patchers):
                    patcher.stop()

        return PatchGroup()

    @staticmethod
    def _start_server():
        httpd = server_module.create_server(0)
        port = httpd.server_address[1]
        thread = Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        return httpd, thread, port

    @staticmethod
    def _stop_server(httpd, thread):
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

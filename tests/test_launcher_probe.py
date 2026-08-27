from __future__ import annotations

import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from app import VERSION
from scripts.launcher_probe import EXPECTED_INSTANCE, inspect


class _Handler(BaseHTTPRequestHandler):
    marker = EXPECTED_INSTANCE

    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        if self.path == "/api/status":
            raw = json.dumps({"version": VERSION, "ready": True, "bind": "127.0.0.1"}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
            return
        if self.path == "/.aio-instance-id":
            raw = (self.marker + "\n").encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
            return
        self.send_error(404)


class LauncherProbeTests(unittest.TestCase):
    def _serve(self, marker: str):
        handler = type("Handler", (_Handler,), {"marker": marker})
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        return server, thread

    def test_matching_version_and_installation_is_reusable(self):
        server, thread = self._serve(EXPECTED_INSTANCE)
        try:
            result = inspect(server.server_address[1])
            self.assertEqual(result["state"], "own-ready")
        finally:
            server.shutdown(); server.server_close(); thread.join(timeout=2)

    def test_same_version_but_foreign_installation_is_not_reused(self):
        server, thread = self._serve("wrong-installation")
        try:
            result = inspect(server.server_address[1])
            self.assertEqual(result["state"], "occupied")
        finally:
            server.shutdown(); server.server_close(); thread.join(timeout=2)

    def test_free_port_is_reported_as_free(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
        port = server.server_address[1]
        server.server_close()
        self.assertEqual(inspect(port)["state"], "free")


if __name__ == "__main__":
    unittest.main()

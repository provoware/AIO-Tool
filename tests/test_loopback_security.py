from __future__ import annotations

import unittest

from app.loopback_security import allowed_host_header, allowed_local_request, allowed_origin


class LoopbackSecurityTests(unittest.TestCase):
    def test_exact_loopback_port_is_required(self):
        self.assertTrue(allowed_host_header("127.0.0.1:8778", 8778))
        self.assertTrue(allowed_host_header("localhost:8778", 8778))
        self.assertFalse(allowed_host_header("127.0.0.1:9999", 8778))
        self.assertFalse(allowed_host_header("example.test:8778", 8778))

    def test_origin_must_match_loopback_and_port(self):
        self.assertTrue(allowed_origin("http://127.0.0.1:8778", 8778))
        self.assertFalse(allowed_origin("http://127.0.0.1:9999", 8778))
        self.assertFalse(allowed_origin("https://127.0.0.1:8778", 8778))
        self.assertFalse(allowed_origin("http://example.test:8778", 8778))
        self.assertTrue(allowed_local_request("localhost:8778", None, 8778))


if __name__ == "__main__":
    unittest.main()

import unittest

from app.server import allowed_host, allowed_origin


class SecurityContractTests(unittest.TestCase):
    def test_loopback_host_allowed(self):
        self.assertTrue(allowed_host("127.0.0.1:8765",8765))
        self.assertTrue(allowed_host("localhost:8765",8765))

    def test_foreign_host_blocked(self):
        self.assertFalse(allowed_host("example.com",8765))
        self.assertFalse(allowed_host("127.0.0.1:9999",8765))

    def test_loopback_origin_allowed(self):
        self.assertTrue(allowed_origin("http://127.0.0.1:8765",8765))
        self.assertTrue(allowed_origin("http://localhost:8765",8765))

    def test_foreign_origin_blocked(self):
        self.assertFalse(allowed_origin("https://example.com",8765))


if __name__=="__main__":
    unittest.main()

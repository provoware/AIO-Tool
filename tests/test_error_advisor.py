import unittest

from app import ROOT_DIR
from app.config import ConfigError
from app.error_advisor import ErrorAdvisor
from app.persistence import PersistenceError


class ErrorAdvisorTests(unittest.TestCase):
    def setUp(self):
        self.advisor = ErrorAdvisor()

    def test_invalid_theme_gets_input_help_and_safe_retry(self):
        advice = self.advisor.advise(ConfigError("Unbekanntes Theme."), area="Darstellung")
        self.assertEqual(advice["rule_id"], "ERR-CONFIG-THEME-001")
        self.assertEqual(advice["category"], "input")
        self.assertTrue(advice["retry_safe"])
        self.assertTrue((ROOT_DIR / advice["template_path"]).is_file())

    def test_corrupt_persistence_gets_integrity_help(self):
        advice = self.advisor.advise(
            PersistenceError("Persistenzdatei 'todos.json' ist beschädigt und kein gültiges Backup ist verfügbar."),
            area="TODO",
        )
        self.assertEqual(advice["rule_id"], "ERR-PERSIST-001")
        self.assertEqual(advice["category"], "integrity")
        self.assertEqual(advice["severity"], "red")
        self.assertFalse(advice["retry_safe"])

    def test_unknown_error_falls_back_without_claiming_recovery(self):
        advice = self.advisor.advise(RuntimeError("Unbekannt"))
        self.assertEqual(advice["rule_id"], "ERR-GENERIC-001")
        self.assertFalse(advice["retry_safe"])

    def test_metadata_exposes_versions(self):
        meta = self.advisor.metadata()
        self.assertEqual(meta["rules_version"], "1.0.0")
        self.assertEqual(meta["text_catalog"]["catalog_version"], "1.0.0")


if __name__ == "__main__":
    unittest.main()

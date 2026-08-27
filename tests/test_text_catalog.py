from pathlib import Path
import tempfile
import unittest

from app import ROOT_DIR
from app.text_catalog import TextCatalog, TextCatalogError, validate_catalog


class TextCatalogTests(unittest.TestCase):
    def test_default_german_catalog_loads_and_is_versioned(self):
        catalog = TextCatalog(ROOT_DIR / "resources" / "texts" / "de" / "v1.json")
        self.assertEqual(catalog.language, "de")
        self.assertEqual(catalog.version, "1.1.0")
        self.assertIn("sicher", catalog.get("error.generic").casefold())
        self.assertIn("Kalender", catalog.get("action.calendar.date"))

    def test_missing_key_is_not_silently_invented(self):
        catalog = TextCatalog(ROOT_DIR / "resources" / "texts" / "de" / "v1.json")
        with self.assertRaises(TextCatalogError):
            catalog.get("does.not.exist")

    def test_empty_message_is_rejected(self):
        with self.assertRaises(TextCatalogError):
            validate_catalog({
                "schema_version": 1,
                "catalog_version": "1.1.0",
                "language": "de",
                "messages": {"bad": ""},
            })

    def test_invalid_json_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "texts.json"
            path.write_text("{kaputt", encoding="utf-8")
            with self.assertRaises(TextCatalogError):
                TextCatalog(path)


if __name__ == "__main__":
    unittest.main()

from pathlib import Path
import tempfile
import unittest

from app.config import ConfigError, ConfigStore, DEFAULT_CONFIG, validate_config


class ConfigTests(unittest.TestCase):
    def test_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            store=ConfigStore(Path(tmp)/"config.json")
            saved=store.save(DEFAULT_CONFIG)
            self.assertEqual(saved,store.load())

    def test_backup_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"config.json"
            store=ConfigStore(path)
            store.save(DEFAULT_CONFIG)
            store.update({"theme":"clean-light"})
            path.write_text("{kaputt",encoding="utf-8")
            loaded=store.load()
            self.assertEqual(loaded["theme"],"steel-night")

    def test_reject_unknown_theme(self):
        with self.assertRaises(ConfigError):
            validate_config({"theme":"unknown"})

    def test_reject_arbitrary_font_scale(self):
        with self.assertRaises(ConfigError):
            validate_config({"font_scale":111})


if __name__=="__main__":
    unittest.main()

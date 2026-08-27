from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile
import unittest

from app.config import ConfigError, ConfigStore, DEFAULT_CONFIG, THEMES, validate_config


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

    def test_modern_theme_contract_contains_accessible_fallbacks(self):
        self.assertEqual(
            THEMES,
            {"aurora-glass", "trash-neon", "steel-night", "clean-light", "high-contrast"},
        )

    def test_concurrent_independent_config_changes_do_not_corrupt_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            store=ConfigStore(Path(tmp)/"config.json")
            store.save(DEFAULT_CONFIG)

            changes=[
                {"theme":"aurora-glass"},
                {"font_scale":120},
                {"expert_visible":True},
                {"setup_complete":True},
            ]
            with ThreadPoolExecutor(max_workers=4) as pool:
                list(pool.map(store.update,changes))
            loaded=store.load()
            self.assertIn(loaded["theme"],THEMES)
            self.assertIn(loaded["font_scale"],{90,100,110,120,130,140})
            self.assertIsInstance(loaded["expert_visible"],bool)
            self.assertIsInstance(loaded["setup_complete"],bool)


if __name__=="__main__":
    unittest.main()

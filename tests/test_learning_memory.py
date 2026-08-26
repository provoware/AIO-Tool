import unittest

from app import ROOT_DIR
from app.learning_memory import active_entries, load_jsonl, relevant


class LearningMemoryTests(unittest.TestCase):
    def test_learning_memory_is_valid_and_unique(self):
        entries = load_jsonl(ROOT_DIR / "LEARNING_MEMORY.jsonl")
        self.assertGreaterEqual(len(entries), 6)
        ids = [entry["id"] for entry in entries]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(active_entries(entries)), len(entries))

    def test_global_rule_applies_to_any_area(self):
        entries = load_jsonl(ROOT_DIR / "LEARNING_MEMORY.jsonl")
        matches = relevant(entries, ["calendar"])
        self.assertTrue(any(entry["id"] == "LRN-005" for entry in matches))

    def test_area_specific_rules_are_found(self):
        entries = load_jsonl(ROOT_DIR / "LEARNING_MEMORY.jsonl")
        matches = relevant(entries, ["versioning"])
        ids = {entry["id"] for entry in matches}
        self.assertIn("LRN-001", ids)
        self.assertIn("LRN-003", ids)


if __name__ == "__main__":
    unittest.main()

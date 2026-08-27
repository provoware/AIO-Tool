from __future__ import annotations

import json
import unittest
from pathlib import Path

from app.version_registry import validate_registry
from scripts.evidence_guard import validate_evidence_index

ROOT = Path(__file__).resolve().parents[1]


class ReleaseEvidenceIndexTests(unittest.TestCase):
    def _registry_and_index(self):
        registry = validate_registry(json.loads((ROOT / "VERSION_REGISTRY.json").read_text(encoding="utf-8")))
        index = json.loads((ROOT / "evidence" / "RELEASE_EVIDENCE_INDEX.json").read_text(encoding="utf-8"))
        return registry, index

    def _current_evidence(self):
        registry, index = self._registry_and_index()
        current = registry["current_version"]
        entry = next(item for item in index["entries"] if item["version"] == current)
        row = json.loads((ROOT / entry["file"]).read_text(encoding="utf-8"))
        return registry, row

    def test_all_tested_versions_have_exactly_one_evidence_file(self):
        registry, index = self._registry_and_index()
        validate_evidence_index(index, registry)
        proven = {row["version"] for row in registry["versions"] if row["status"] in {"tested", "release-candidate", "released"}}
        indexed = {row["version"] for row in index["entries"]}
        self.assertEqual(proven, indexed)
        self.assertEqual(len(indexed), len(index["entries"]))

    def test_current_tested_baseline_has_main_ci_artifact_and_cross_browser_evidence(self):
        registry, row = self._current_evidence()
        self.assertEqual(row["version"], registry["current_version"])
        self.assertEqual(row["main_commit"], "ee6adcfd3427e8328920edaceb804e7b6655cdb8")
        self.assertEqual(row["main_ci_run"], 33048070879)
        self.assertIn(row["main_ci_run"], row["ci_runs"])
        self.assertEqual(row["artifact"]["status"], "recorded")
        self.assertEqual(row["artifact"]["sha256"], "f8ffd88e2f3e40416f0d76b20786aa168cebb4e11fe3ef9d0eefa6dcf93b19ee")
        self.assertEqual(row["runtime_reproducibility"]["status"], "passed")
        self.assertEqual(row["runtime_reproducibility"]["sha256"], row["artifact"]["sha256"])
        self.assertEqual(row["browser_matrix"]["chromium"]["status"], "passed")
        self.assertEqual(row["browser_matrix"]["firefox"]["status"], "passed")
        self.assertTrue(row["open_l4_gates"])

    def test_superseded_promotion_artifact_is_explicit_not_silent(self):
        _, row = self._current_evidence()
        old_hashes = {item["sha256"] for item in row.get("superseded_artifacts", [])}
        self.assertIn("a7ab6d64e978e27c1fa550c549e12dc7ee21e24a17a55fd9c160c19cd3001b72", old_hashes)
        self.assertNotIn(row["artifact"]["sha256"], old_hashes)


if __name__ == "__main__":
    unittest.main()

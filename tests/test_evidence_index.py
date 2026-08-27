from __future__ import annotations

import json
import unittest
from pathlib import Path

from app.version_registry import validate_registry
from scripts.evidence_guard import validate_evidence_index

ROOT = Path(__file__).resolve().parents[1]


class ReleaseEvidenceIndexTests(unittest.TestCase):
    def test_all_tested_versions_have_exactly_one_evidence_file(self):
        registry = validate_registry(json.loads((ROOT / "VERSION_REGISTRY.json").read_text(encoding="utf-8")))
        index = json.loads((ROOT / "evidence" / "RELEASE_EVIDENCE_INDEX.json").read_text(encoding="utf-8"))
        validate_evidence_index(index, registry)
        proven = {row["version"] for row in registry["versions"] if row["status"] in {"tested", "release-candidate", "released"}}
        indexed = {row["version"] for row in index["entries"]}
        self.assertEqual(proven, indexed)
        self.assertEqual(len(indexed), len(index["entries"]))

    def test_current_tested_baseline_has_main_ci_artifact_and_cross_browser_evidence(self):
        row = json.loads((ROOT / "evidence" / "releases" / "0.4.3-integrity-hardening.json").read_text(encoding="utf-8"))
        self.assertEqual(row["main_commit"], "c8b80161e1770f8636d3e77d72b57f9c24723078")
        self.assertIn(33036217621, row["ci_runs"])
        self.assertEqual(row["artifact"]["status"], "recorded")
        self.assertEqual(row["browser_matrix"]["chromium"]["status"], "passed")
        self.assertEqual(row["browser_matrix"]["firefox"]["status"], "passed")
        self.assertTrue(row["open_l4_gates"])


if __name__ == "__main__":
    unittest.main()

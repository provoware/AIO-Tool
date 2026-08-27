from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.manifest_guard import ManifestContractError, validate_manifests

ROOT = Path(__file__).resolve().parents[1]


class ManifestGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runtime = json.loads((ROOT / "manifests" / "RUNTIME_MANIFEST.json").read_text(encoding="utf-8"))
        self.development = json.loads((ROOT / "manifests" / "DEVELOPMENT_MANIFEST.json").read_text(encoding="utf-8"))

    def test_current_manifests_are_consistent(self) -> None:
        runtime, development = validate_manifests(copy.deepcopy(self.runtime), copy.deepcopy(self.development))
        self.assertEqual(runtime["manifest_version"], "1.3.0")
        self.assertEqual(development["manifest_version"], "1.2.0")

    def test_runtime_file_cannot_be_classified_repo_only(self) -> None:
        development = copy.deepcopy(self.development)
        development["categories"]["documentation"].append("web/index.html")
        with self.assertRaises(ManifestContractError):
            validate_manifests(copy.deepcopy(self.runtime), development)

    def test_repo_only_root_file_must_exist_in_development_inventory(self) -> None:
        development = copy.deepcopy(self.development)
        development["categories"]["documentation"].remove("README.md")
        development["status_documents"].remove("README.md")
        development["evidence_summary_documents"].remove("README.md")
        with self.assertRaises(ManifestContractError):
            validate_manifests(copy.deepcopy(self.runtime), development)

    def test_runtime_manifest_must_remain_runtime_member(self) -> None:
        runtime = copy.deepcopy(self.runtime)
        runtime["files"].remove("manifests/RUNTIME_MANIFEST.json")
        with self.assertRaises(ManifestContractError):
            validate_manifests(runtime, copy.deepcopy(self.development))

    def test_legacy_generated_file_semantics_are_explicitly_guarded(self) -> None:
        runtime = copy.deepcopy(self.runtime)
        runtime["generated_files"].remove("MANIFEST_RELEASE.json")
        with self.assertRaises(ManifestContractError):
            validate_manifests(runtime, copy.deepcopy(self.development))


if __name__ == "__main__":
    unittest.main()

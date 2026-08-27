from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.iteration_sync import IterationSyncError, validate_iteration

ROOT = Path(__file__).resolve().parents[1]
HEAD = "a" * 40
TREE = "b" * 40


class IterationSyncTests(unittest.TestCase):
    def test_current_repository_contract_is_synchronized_without_git_requirement(self):
        report = validate_iteration(ROOT, git_state=None)
        self.assertTrue(report["synchronized"])
        self.assertEqual(report["version"], "0.6.0-autostart-selfheal")
        self.assertEqual(report["registry_current_version"], report["version"])
        self.assertFalse(report["repository"]["available"])

    def test_commit_bound_ci_state_passes(self):
        report = validate_iteration(
            ROOT, expected_commit=HEAD, require_git=True, require_clean=True,
            git_state={"head": HEAD, "tree": TREE, "branch": "feature/example", "clean": True, "dirty_entries": []},
        )
        self.assertTrue(report["repository"]["expected_commit_match"])

    def test_wrong_expected_commit_fails_closed(self):
        with self.assertRaises(IterationSyncError):
            validate_iteration(ROOT, expected_commit="c" * 40, git_state={"head": HEAD, "tree": TREE, "branch": "main", "clean": True, "dirty_entries": []})

    def test_dirty_tree_fails_when_clean_is_required(self):
        with self.assertRaises(IterationSyncError):
            validate_iteration(ROOT, require_clean=True, git_state={"head": HEAD, "tree": TREE, "branch": "main", "clean": False, "dirty_entries": [" M README.md"]})

    def test_registry_version_drift_fails(self):
        with tempfile.TemporaryDirectory() as temp_name:
            temp = Path(temp_name); (temp / "manifests").mkdir()
            (temp / "VERSION").write_text("9.9.9-test\n", encoding="utf-8")
            (temp / "VERSION_REGISTRY.json").write_text((ROOT / "VERSION_REGISTRY.json").read_text(encoding="utf-8"), encoding="utf-8")
            (temp / "manifests" / "RUNTIME_MANIFEST.json").write_text(json.dumps({"manifest_version":"x","files":["VERSION","VERSION_REGISTRY.json"]}), encoding="utf-8")
            (temp / "manifests" / "DEVELOPMENT_MANIFEST.json").write_text(json.dumps({"manifest_version":"x","status_documents":["README.md"]}), encoding="utf-8")
            (temp / "README.md").write_text("9.9.9-test\n", encoding="utf-8")
            with self.assertRaises(IterationSyncError): validate_iteration(temp, git_state=None)

    def test_status_document_version_drift_fails(self):
        with tempfile.TemporaryDirectory() as temp_name:
            temp = Path(temp_name); (temp / "manifests").mkdir()
            (temp / "VERSION").write_text((ROOT / "VERSION").read_text(encoding="utf-8"), encoding="utf-8")
            (temp / "VERSION_REGISTRY.json").write_text((ROOT / "VERSION_REGISTRY.json").read_text(encoding="utf-8"), encoding="utf-8")
            (temp / "manifests" / "RUNTIME_MANIFEST.json").write_text(json.dumps({"manifest_version":"x","files":["VERSION","VERSION_REGISTRY.json"]}), encoding="utf-8")
            (temp / "manifests" / "DEVELOPMENT_MANIFEST.json").write_text(json.dumps({"manifest_version":"x","status_documents":["README.md"]}), encoding="utf-8")
            (temp / "README.md").write_text("veraltete Version\n", encoding="utf-8")
            with self.assertRaises(IterationSyncError): validate_iteration(temp, git_state=None)


if __name__ == "__main__":
    unittest.main()

from pathlib import Path
import tempfile
import unittest

from app.version_registry import VersionRegistry, VersionRegistryError, validate_registry


class VersionRegistryTests(unittest.TestCase):
    def test_register_current_and_previous(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = VersionRegistry(Path(tmp) / "versions.json")
            registry.ensure_current("0.1.0", summary="Basis")
            registry.ensure_current("0.2.0", summary="Core")
            data = registry.load()
            self.assertEqual(data["current_version"], "0.2.0")
            self.assertEqual(registry.previous_version()["version"], "0.1.0")
            self.assertTrue(registry.consistency("0.2.0")["ok"])

    def test_seed_preserves_history_before_runtime_file_exists(self):
        seed = {
            "schema_version": 1,
            "current_version": "0.1.1",
            "versions": [
                {
                    "version": "0.1.1",
                    "created_at": "2026-08-27T00:00:00+00:00",
                    "status": "tested",
                    "release_status": "draft",
                    "commit_sha": "abc123",
                    "summary": "Foundation",
                    "changes": ["Basis"],
                    "known_issues": [],
                    "regression_status": "passed-ci",
                    "evidence": [{"kind": "ci", "reference": "run-1"}],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "versions.json"
            registry = VersionRegistry(path, default=seed)
            self.assertFalse(path.exists())
            self.assertEqual(registry.load()["versions"][0]["version"], "0.1.1")
            registry.ensure_current("0.2.0")
            self.assertEqual([item["version"] for item in registry.load()["versions"]], ["0.1.1", "0.2.0"])

    def test_optional_commit_sha_accepts_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = VersionRegistry(Path(tmp) / "versions.json")
            registry.ensure_current("0.2.0", commit_sha=None)
            self.assertIsNone(registry.load()["versions"][0]["commit_sha"])

    def test_no_duplicate_when_ensuring_same_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = VersionRegistry(Path(tmp) / "versions.json")
            registry.ensure_current("0.2.0")
            registry.ensure_current("0.2.0")
            self.assertEqual(len(registry.load()["versions"]), 1)

    def test_tested_status_requires_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = VersionRegistry(Path(tmp) / "versions.json")
            registry.ensure_current("0.2.0")
            with self.assertRaises(VersionRegistryError):
                registry.set_status("0.2.0", status="tested")
            registry.record_evidence("0.2.0", kind="ci", reference="run-123", note="grün")
            registry.set_status("0.2.0", status="tested", regression_status="passed")
            item = registry.load()["versions"][0]
            self.assertEqual(item["status"], "tested")
            self.assertEqual(item["release_status"], "draft")
            self.assertEqual(item["regression_status"], "passed")

    def test_release_candidate_uses_candidate_release_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = VersionRegistry(Path(tmp) / "versions.json")
            registry.ensure_current("0.3.0")
            registry.record_evidence("0.3.0", kind="ci", reference="run-rc")
            registry.set_status("0.3.0", status="release-candidate", regression_status="passed")
            item = registry.load()["versions"][0]
            self.assertEqual((item["status"], item["release_status"]), ("release-candidate", "candidate"))

    def test_blocked_status_is_explicit_and_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = VersionRegistry(Path(tmp) / "versions.json")
            registry.ensure_current("0.3.1")
            registry.set_status("0.3.1", status="blocked")
            item = registry.load()["versions"][0]
            self.assertEqual((item["status"], item["release_status"]), ("blocked", "blocked"))

    def test_invalid_status_pair_is_rejected(self):
        invalid = {
            "schema_version": 1,
            "current_version": "0.4.0",
            "versions": [{
                "version": "0.4.0",
                "created_at": "2026-08-27T00:00:00+00:00",
                "status": "tested",
                "release_status": "released",
                "commit_sha": None,
                "summary": "inkonsistent",
                "changes": [],
                "known_issues": [],
                "regression_status": "passed",
                "evidence": [{"kind": "ci", "reference": "run-x"}],
            }],
        }
        with self.assertRaises(VersionRegistryError):
            validate_registry(invalid)

    def test_consistency_detects_version_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = VersionRegistry(Path(tmp) / "versions.json")
            registry.ensure_current("0.1.0")
            result = registry.consistency("0.2.0")
            self.assertFalse(result["ok"])
            self.assertGreaterEqual(len(result["issues"]), 1)


if __name__ == "__main__":
    unittest.main()

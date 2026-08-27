from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from app import VERSION
from scripts.release import build, current_version_record, status_label, verify


class ReleaseContractTests(unittest.TestCase):
    def test_built_runtime_zip_is_self_contained_and_preflightable(self):
        label = status_label(current_version_record())
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            archive = tmp_path / f"AIO-Tool-{VERSION}-{label}.zip"
            built, _ = build(archive)
            verify(built)
            with zipfile.ZipFile(built) as zf:
                names = set(zf.namelist())
                root = f"AIO-Tool-{VERSION}/"
                self.assertIn(root + "scripts/runtime_preflight.py", names)
                self.assertIn(root + "scripts/launcher_probe.py", names)
                self.assertIn(root + "app/instance_identity.py", names)
                self.assertNotIn(root + "scripts/validate.py", names)
                self.assertNotIn(root + "README.md", names)
                self.assertFalse(any(name.startswith(root + "tests/") for name in names))
                self.assertNotIn(root + "web/.aio-instance-id", names)
                zf.extractall(tmp_path / "unpacked")

            runtime_root = tmp_path / "unpacked" / f"AIO-Tool-{VERSION}"
            result = subprocess.run(
                [sys.executable, "scripts/runtime_preflight.py", "--quick"],
                cwd=runtime_root,
                text=True,
                capture_output=True,
                timeout=20,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("RUNTIME PREFLIGHT PASS", result.stdout)

    def test_release_label_is_derived_from_validated_registry_status(self):
        record = current_version_record()
        expected = {
            "development": "DEV",
            "tested": "TESTED",
            "release-candidate": "RC",
            "released": "RELEASED",
            "blocked": "BLOCKED",
            "deprecated": "ARCHIVED",
        }[record["status"]]
        self.assertEqual(status_label(record), expected)


if __name__ == "__main__":
    unittest.main()

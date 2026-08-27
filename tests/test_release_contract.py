from __future__ import annotations

import stat
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
            tmp_path = Path(tmp); archive = tmp_path / f"AIO-Tool-{VERSION}-{label}.zip"; built, _ = build(archive); verify(built)
            with zipfile.ZipFile(built) as zf:
                names = set(zf.namelist()); root = f"AIO-Tool-{VERSION}/"
                for rel in ("scripts/runtime_preflight.py", "scripts/launcher_probe.py", "app/instance_identity.py", "app/native_acceptance.py", "app/safe_file_sim.py", "app/loopback_security.py", "scripts/native_acceptance_runner.py", "scripts/safe_file_simulator.py", "web/native-acceptance.html", "web/safe-file-sim.html", "native_acceptance.desktop", "safe_file_simulation.desktop"):
                    self.assertIn(root + rel, names)
                self.assertNotIn(root + "scripts/validate.py", names); self.assertNotIn(root + "README.md", names); self.assertFalse(any(name.startswith(root + "tests/") or name.startswith(root + "evidence/") for name in names)); self.assertNotIn(root + "web/.aio-instance-id", names)
                zf.extractall(tmp_path / "unpacked")
            runtime_root = tmp_path / "unpacked" / f"AIO-Tool-{VERSION}"
            result = subprocess.run([sys.executable, "scripts/runtime_preflight.py", "--quick"], cwd=runtime_root, text=True, capture_output=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr); self.assertIn("RUNTIME PREFLIGHT PASS", result.stdout)

    def test_new_starters_and_scripts_are_executable_inside_zip(self):
        label = status_label(current_version_record())
        with tempfile.TemporaryDirectory() as tmp:
            archive = Path(tmp) / f"AIO-Tool-{VERSION}-{label}.zip"; built, _ = build(archive)
            root = f"AIO-Tool-{VERSION}/"
            with zipfile.ZipFile(built) as zf:
                for rel in ("start_tool.sh", "start_native_acceptance.sh", "start_safe_file_simulation.sh", "native_acceptance.desktop", "safe_file_simulation.desktop", "scripts/runtime_preflight.py", "scripts/native_acceptance_runner.py", "scripts/safe_file_simulator.py"):
                    mode = (zf.getinfo(root + rel).external_attr >> 16) & 0o777
                    self.assertTrue(mode & stat.S_IXUSR, f"nicht ausführbar im ZIP: {rel} ({oct(mode)})")

    def test_release_label_is_derived_from_validated_registry_status(self):
        record = current_version_record(); expected = {"development":"DEV","tested":"TESTED","release-candidate":"RC","released":"RELEASED","blocked":"BLOCKED","deprecated":"ARCHIVED"}[record["status"]]; self.assertEqual(status_label(record), expected)


if __name__ == "__main__": unittest.main()

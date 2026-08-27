from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReleasePipelineContractTests(unittest.TestCase):
    def test_version_is_060_autostart_selfheal(self):
        self.assertEqual((ROOT / "VERSION").read_text(encoding="utf-8").strip(), "0.6.0-autostart-selfheal")

    def test_runtime_manifest_contains_new_autostart_recovery_contract(self):
        manifest = json.loads((ROOT / "manifests" / "RUNTIME_MANIFEST.json").read_text(encoding="utf-8"))
        files = set(manifest["files"])
        for rel in (
            "app/autostart.py",
            "app/preflight.py",
            "app/runtime_health.py",
            "app/runtime_recovery.py",
            "app/startup_progress.py",
            "scripts/portable_entry.py",
        ):
            self.assertIn(rel, files)
        self.assertIn("RECOVERY_BASIS.zip", manifest["generated_files"])
        self.assertIn("requirements-build.txt", manifest["repo_only_root_files"])

    def test_build_dependency_is_pinned(self):
        content = (ROOT / "requirements-build.txt").read_text(encoding="utf-8").strip()
        self.assertRegex(content, r"^pyinstaller==\d+\.\d+\.\d+$")

    def test_atomic_pipeline_has_exact_ordered_gates(self):
        text = (ROOT / ".github" / "workflows" / "foundation-ci.yml").read_text(encoding="utf-8")
        gates = [
            "01-core-ci",
            "02-failure-matrix",
            "03-source-zip",
            "04-recovery-basis",
            "05-portable-build",
            "06-portable-smoke",
            "07-chromium",
            "08-firefox",
        ]
        positions = [text.index(gate) for gate in gates]
        self.assertEqual(positions, sorted(positions))
        for required in (
            "needs: core-ci",
            "needs: failure-matrix",
            "needs: source-zip",
            "needs: recovery-basis",
            "needs: portable-build",
            "needs: portable-smoke",
            "needs: chromium",
        ):
            self.assertIn(required, text)

    def test_all_pipeline_helpers_exist(self):
        for rel in (
            "scripts/failure_matrix.py",
            "scripts/build_recovery_basis.py",
            "scripts/build_portable.py",
            "scripts/portable_smoke.py",
        ):
            self.assertTrue((ROOT / rel).is_file(), rel)


if __name__ == "__main__":
    unittest.main()

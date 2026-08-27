from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.safe_file_sim import EXECUTION_ENABLED, SIMULATION_ONLY, SafeFileSimulationError, build_preview, failure_matrix, validate_preview_contract

ROOT = Path(__file__).resolve().parents[1]


class SafeFileSimulationTests(unittest.TestCase):
    def make_pair(self, root: Path) -> tuple[Path, Path]:
        source = root / "source.txt"; source.write_text("hello", encoding="utf-8")
        target = root / "target"; target.mkdir()
        return source, target

    def test_preview_never_mutates_and_execution_is_locked(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, target = self.make_pair(Path(tmp))
            before = sorted(p.name for p in target.iterdir())
            preview = build_preview(source, target, free_bytes=100 * 1024 * 1024)
            self.assertTrue(SIMULATION_ONLY); self.assertFalse(EXECUTION_ENABLED)
            self.assertTrue(preview["simulation_only"]); self.assertFalse(preview["execution_enabled"])
            self.assertFalse(preview["mutation_performed"]); self.assertEqual(before, sorted(p.name for p in target.iterdir()))
            self.assertTrue(preview["would_copy_if_execution_existed"])

    def test_failure_matrix_cases_block_or_require_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source, target = self.make_pair(root)
            missing = build_preview(root / "missing.txt", target, free_bytes=100_000_000)
            self.assertFalse(missing["would_copy_if_execution_existed"])
            source_dir = root / "source-dir"; source_dir.mkdir()
            self.assertFalse(build_preview(source_dir, target, free_bytes=100_000_000)["would_copy_if_execution_existed"])
            link = root / "link.txt"; link.symlink_to(source)
            self.assertFalse(build_preview(link, target, free_bytes=100_000_000)["would_copy_if_execution_existed"])
            self.assertFalse(build_preview(source, root / "missing-target", free_bytes=100_000_000)["would_copy_if_execution_existed"])
            target_file = root / "target-file"; target_file.write_text("x", encoding="utf-8")
            self.assertFalse(build_preview(source, target_file, free_bytes=100_000_000)["would_copy_if_execution_existed"])
            target_link = root / "target-link"; target_link.symlink_to(target, target_is_directory=True)
            self.assertFalse(build_preview(source, target_link, free_bytes=100_000_000)["would_copy_if_execution_existed"])
            self.assertFalse(build_preview(source, target, free_bytes=1)["would_copy_if_execution_existed"])
            same_dir = root / "same"; same_dir.mkdir(); same_source = same_dir / "same.txt"; same_source.write_text("x", encoding="utf-8")
            self.assertFalse(build_preview(same_source, same_dir, free_bytes=100_000_000)["would_copy_if_execution_existed"])

    def test_target_not_writable_blocks_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, target = self.make_pair(Path(tmp))
            original_access = __import__("os").access
            def fake_access(path, mode):
                return False if Path(path) == target else original_access(path, mode)
            with patch("app.safe_file_sim.os.access", side_effect=fake_access):
                preview = build_preview(source, target, free_bytes=100_000_000)
            self.assertFalse(next(x for x in preview["checks"] if x["id"] == "target_writable")["ok"])
            self.assertFalse(preview["would_copy_if_execution_existed"])

    def test_existing_destination_defaults_to_skip_and_rename_is_only_proposed(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, target = self.make_pair(Path(tmp))
            destination = target / source.name; destination.write_text("old", encoding="utf-8")
            preview = build_preview(source, target, "skip", free_bytes=100_000_000)
            self.assertTrue(preview["conflict"]["decision_required"]); self.assertFalse(preview["would_copy_if_execution_existed"])
            renamed = build_preview(source, target, "rename", free_bytes=100_000_000)
            self.assertNotEqual(renamed["conflict"]["selected_destination"], str(destination))
            self.assertEqual(destination.read_text(encoding="utf-8"), "old")
            self.assertEqual(len(list(target.iterdir())), 1)

    def test_recovery_contract_requires_future_journal_postvalidation_and_guarded_undo(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, target = self.make_pair(Path(tmp))
            recovery = build_preview(source, target, free_bytes=100_000_000)["recovery_contract"]
            self.assertEqual(recovery["current_mode"], "no-mutation")
            self.assertFalse(recovery["rollback_required"])
            self.assertTrue(recovery["future_execution_requires_persistent_journal"])
            self.assertTrue(recovery["future_done_requires_postvalidation"])
            self.assertTrue(recovery["future_undo_must_verify_destination_unchanged"])

    def test_failure_matrix_has_all_ten_contracts(self):
        self.assertEqual({item["id"] for item in failure_matrix()}, {f"SF-{i:03d}" for i in range(1, 11)})

    def test_template_and_negative_fixture_use_safety_validator(self):
        good = json.loads((ROOT / "resources/templates/safe_file_sim/safe_file_preview.v1.example.json").read_text(encoding="utf-8"))
        self.assertFalse(validate_preview_contract(good)["execution_enabled"])
        bad = json.loads((ROOT / "testdata/safe_file_sim/invalid_preview.json").read_text(encoding="utf-8"))
        with self.assertRaises(SafeFileSimulationError):
            validate_preview_contract(bad)


if __name__ == "__main__": unittest.main()

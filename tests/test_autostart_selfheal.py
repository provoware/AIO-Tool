from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from app.autostart import _clean_stale_pid, _normalize_port
from app.runtime_health import repair_json_state
from app.runtime_recovery import restore_runtime_assets


class AutostartSelfHealTests(unittest.TestCase):
    @staticmethod
    def validator(value: dict) -> dict:
        if value.get("schema") != 1 or not isinstance(value.get("value"), int):
            raise ValueError("invalid")
        return value

    def test_invalid_port_falls_back_with_explanation(self):
        port, warning = _normalize_port("nicht-zahl")
        self.assertEqual(port, 8765)
        self.assertIn("ungültig", warning)

    def test_out_of_range_port_falls_back(self):
        port, warning = _normalize_port("80")
        self.assertEqual(port, 8765)
        self.assertIn("außerhalb", warning)

    def test_stale_pid_is_removed(self):
        with tempfile.TemporaryDirectory() as temp:
            pid_file = Path(temp) / "server.pid"
            pid_file.write_text("999999999\n", encoding="utf-8")
            note = _clean_stale_pid(pid_file)
            self.assertFalse(pid_file.exists())
            self.assertIn("Veraltete PID", note)

    def test_corrupt_main_restores_valid_backup_and_quarantines_original(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "state.json"
            path.write_text("{broken", encoding="utf-8")
            path.with_suffix(".json.bak").write_text('{"schema":1,"value":9}\n', encoding="utf-8")
            result = repair_json_state(path, default={"schema": 1, "value": 0}, validator=self.validator, quarantine_root=root / "quarantine")
            self.assertEqual(result["status"], "backup-restored")
            self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["value"], 9)
            self.assertEqual(len(result["quarantined"]), 1)

    def test_corrupt_main_and_backup_reset_safe_without_deleting_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "state.json"
            path.write_text("broken", encoding="utf-8")
            path.with_suffix(".json.bak").write_text("[]", encoding="utf-8")
            result = repair_json_state(path, default={"schema": 1, "value": 0}, validator=self.validator, quarantine_root=root / "quarantine")
            self.assertEqual(result["status"], "reset-safe")
            self.assertEqual(len(result["quarantined"]), 2)
            self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["value"], 0)

    def test_recovery_never_mutates_source_checkout_without_release_marker(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(restore_runtime_assets(root, root / "runtime"), {"enabled": False, "restored": [], "quarantined": []})

    def test_recovery_repairs_changed_asset_and_quarantines_old_copy(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            runtime = root / "runtime"
            target = root / "web" / "asset.txt"
            target.parent.mkdir(parents=True)
            target.write_text("changed", encoding="utf-8")
            payload = b"original\n"
            meta = {"path": "web/asset.txt", "size": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}
            with zipfile.ZipFile(root / "RECOVERY_BASIS.zip", "w") as zf:
                zf.writestr("RECOVERY_MANIFEST.json", json.dumps({"schema_version": 1, "files": [meta]}))
                zf.writestr("files/web/asset.txt", payload)
            (root / "MANIFEST_RELEASE.json").write_text("{}\n", encoding="utf-8")
            result = restore_runtime_assets(root, runtime)
            self.assertTrue(result["enabled"])
            self.assertEqual(result["restored"], ["web/asset.txt"])
            self.assertEqual(target.read_bytes(), payload)
            self.assertEqual(len(result["quarantined"]), 1)


if __name__ == "__main__":
    unittest.main()

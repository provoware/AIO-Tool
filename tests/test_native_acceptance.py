from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from app.native_acceptance import BROWSERS, STEPS, ZOOM_LEVELS, NativeAcceptanceError, NativeAcceptanceStore, validate_session

ROOT = Path(__file__).resolve().parents[1]


class NativeAcceptanceTests(unittest.TestCase):
    def test_matrix_covers_kubuntu_browsers_zoom_display_keyboard(self):
        ids = {step["id"] for step in STEPS}
        self.assertEqual(len(STEPS), 18)
        for browser in BROWSERS:
            for zoom in ZOOM_LEVELS:
                self.assertIn(f"{browser.upper()}-{zoom}", ids)
        self.assertTrue({"KUB-01", "KUB-02", "KUB-03", "KUB-04", "DSP-01", "DSP-02", "DSP-03", "KEY-01"}.issubset(ids))

    def test_no_step_is_auto_passed_and_reports_are_persistent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = NativeAcceptanceStore(root / "session.json", "9.9-test")
            report = store.report()
            self.assertEqual(report["counts"]["pending"], 18)
            self.assertEqual(report["progress_percent"], 0)
            store.record("KUB-01", "pass", "real geprüft", {"inner_width": 1200})
            report = store.report()
            self.assertEqual(report["counts"]["pass"], 1)
            self.assertEqual(report["overall_status"], "incomplete")
            json_path, txt_path = store.write_reports(root / "reports")
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["session_id"], report["session_id"])
            self.assertIn("KUB-01", txt_path.read_text(encoding="utf-8"))

    def test_fail_blocks_overall_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = NativeAcceptanceStore(Path(tmp) / "session.json", "9.9-test")
            store.record("KUB-01", "fail", "Starter fehlgeschlagen")
            self.assertEqual(store.report()["overall_status"], "fail")

    def test_invalid_status_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = NativeAcceptanceStore(Path(tmp) / "session.json", "9.9-test")
            with self.assertRaises(NativeAcceptanceError):
                store.record("KUB-01", "done")

    def test_versioned_template_uses_product_validator(self):
        value = json.loads((ROOT / "resources/templates/native_acceptance/native_acceptance.v1.example.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_session(value)["schema_version"], 1)

    def test_invalid_fixture_is_rejected(self):
        value = json.loads((ROOT / "testdata/native_acceptance/invalid_status.json").read_text(encoding="utf-8"))
        with self.assertRaises(NativeAcceptanceError):
            validate_session(value)


if __name__ == "__main__":
    unittest.main()

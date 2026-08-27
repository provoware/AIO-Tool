from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LauncherContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.launcher = (ROOT / "start_tool.sh").read_text(encoding="utf-8")
        cls.desktop = (ROOT / "start_tool.desktop").read_text(encoding="utf-8")

    def test_launcher_is_fail_fast_and_has_unexpected_error_trap(self) -> None:
        self.assertIn("set -Eeuo pipefail", self.launcher)
        self.assertIn("trap on_unexpected_error ERR", self.launcher)
        self.assertIn('LAUNCH-E900', self.launcher)

    def test_nine_visible_checkpoints_are_stable(self) -> None:
        self.assertIn('TOTAL=9', self.launcher)
        for number in range(1, 10):
            self.assertIn(f"LAUNCH-CP{number:02d}", self.launcher)
        self.assertIn("🟢", self.launcher)
        self.assertIn("🟡", self.launcher)
        self.assertIn("🔴", self.launcher)
        self.assertIn("🔵", self.launcher)

    def test_actionable_error_ids_cover_start_phases(self) -> None:
        for event_id in (
            "LAUNCH-E102",  # Python
            "LAUNCH-E205",  # venv
            "LAUNCH-E306",  # validation
            "LAUNCH-E407",  # backend process
            "LAUNCH-E508",  # readiness
            "LAUNCH-E900",  # unexpected shell error
        ):
            self.assertIn(event_id, self.launcher)

    def test_launcher_keeps_console_backend_events_and_report_separate(self) -> None:
        for filename in (
            "launcher-console.log",
            "launcher-backend.log",
            "launcher-events.jsonl",
            "launcher-report.txt",
        ):
            self.assertIn(filename, self.launcher)
        self.assertIn("Letzte Backend-Ereignisse", self.launcher)
        self.assertIn("Debug-Befehle", self.launcher)
        self.assertIn("tail -n 30", self.launcher)
        self.assertIn("curl -fsS", self.launcher)

    def test_backend_remains_loopback_only(self) -> None:
        self.assertIn("http://127.0.0.1:${PORT}", self.launcher)
        self.assertIn("127.0.0.1", self.launcher)
        self.assertIn("/api/status", self.launcher)

    def test_desktop_launcher_shows_console_and_only_pauses_on_failure(self) -> None:
        self.assertIn("Terminal=true", self.desktop)
        self.assertIn('if [ "$code" -ne 0 ]', self.desktop)
        self.assertIn("Start fehlgeschlagen", self.desktop)
        self.assertIn("runtime/", self.desktop)
        self.assertIn("Enter zum Schließen", self.desktop)


if __name__ == "__main__":
    unittest.main()

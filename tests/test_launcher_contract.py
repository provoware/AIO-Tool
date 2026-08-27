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
        self.assertIn("LAUNCH-E900", self.launcher)

    def test_nine_visible_checkpoints_are_stable(self) -> None:
        self.assertIn("TOTAL=9", self.launcher)
        for number in range(1, 10):
            self.assertIn(f"LAUNCH-CP{number:02d}", self.launcher)
        for icon in ("🟢", "🟡", "🔴", "🔵"):
            self.assertIn(icon, self.launcher)

    def test_actionable_error_ids_cover_start_phases(self) -> None:
        for event_id in (
            "LAUNCH-E102", "LAUNCH-E103", "LAUNCH-E205", "LAUNCH-E303",
            "LAUNCH-E304", "LAUNCH-E306", "LAUNCH-E404", "LAUNCH-E407",
            "LAUNCH-E508", "LAUNCH-E900",
        ):
            self.assertIn(event_id, self.launcher)

    def test_launcher_keeps_console_backend_events_and_report_separate(self) -> None:
        for filename in (
            "launcher-console.log", "launcher-backend.log",
            "launcher-events.jsonl", "launcher-report.txt",
        ):
            self.assertIn(filename, self.launcher)
        self.assertIn("Letzte Backend-Ereignisse", self.launcher)
        self.assertIn("Debug-Befehle", self.launcher)
        self.assertIn("tail -n 30", self.launcher)
        self.assertIn("curl -fsS", self.launcher)
        self.assertIn("MAX_LOG_BYTES", self.launcher)
        self.assertIn("rotate_log", self.launcher)

    def test_runtime_start_does_not_require_repository_validator(self) -> None:
        self.assertIn("scripts/runtime_preflight.py --quick", self.launcher)
        self.assertNotIn("scripts/validate.py --quick", self.launcher)
        self.assertIn('if [[ -f "$ROOT/scripts/validate.py" ]]', self.launcher)

    def test_launcher_verifies_instance_and_uses_safe_fallback_port(self) -> None:
        self.assertIn("scripts/launcher_probe.py ensure-marker", self.launcher)
        self.assertIn("scripts/launcher_probe.py inspect", self.launcher)
        self.assertIn("scripts/launcher_probe.py find-free", self.launcher)
        self.assertIn('PROBE_STATE" == "own-ready"', self.launcher)
        self.assertIn('PROBE_STATE" == "occupied"', self.launcher)
        self.assertIn("LAUNCH-D404", self.launcher)

    def test_launcher_rejects_invalid_port_and_unknown_probe_state(self) -> None:
        self.assertIn('[[ ! "$PORT" =~ ^[0-9]+$ ]]', self.launcher)
        self.assertIn("PORT < 1024", self.launcher)
        self.assertIn("PORT > 65535", self.launcher)
        self.assertIn("LAUNCH-E103", self.launcher)
        self.assertIn("LAUNCH-E304", self.launcher)
        self.assertIn('own-ready|occupied|free', self.launcher)

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

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LauncherContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.shell = (ROOT / "start_tool.sh").read_text(encoding="utf-8")
        cls.autostart = (ROOT / "app" / "autostart.py").read_text(encoding="utf-8")
        cls.preflight = (ROOT / "app" / "preflight.py").read_text(encoding="utf-8")
        cls.runtime_health = (ROOT / "app" / "runtime_health.py").read_text(encoding="utf-8")
        cls.portable = (ROOT / "scripts" / "portable_entry.py").read_text(encoding="utf-8")
        cls.desktop = (ROOT / "start_tool.desktop").read_text(encoding="utf-8")

    def test_shell_is_fail_fast_and_only_bootstraps_canonical_autostart(self) -> None:
        self.assertIn("set -Eeuo pipefail", self.shell)
        self.assertIn('[[ -x "$ROOT/AIO-Tool-Start" ]]', self.shell)
        self.assertIn('exec "$ROOT/AIO-Tool-Start" "$@"', self.shell)
        self.assertIn('-m app.autostart "$@"', self.shell)
        self.assertNotIn("scripts/validate.py", self.shell)

    def test_nine_visible_checkpoints_are_owned_by_python_coordinator(self) -> None:
        self.assertIn("TOTAL = 9", self.autostart)
        self.assertIn("_print_checkpoint", self.autostart)
        for icon in ("🟢", "🟡", "🔴", "🔵"):
            self.assertIn(icon, self.autostart)
        for title in (
            "Runtime-Basis verfügbar",
            "Lokale Daten geprüft und repariert",
            "Runtime-Vertrag geprüft",
            "Backend verifiziert bereit",
            "Abschlussprüfung bestanden",
        ):
            self.assertIn(title, self.autostart)

    def test_actionable_failure_phases_are_explicit(self) -> None:
        for message in (
            "Kein erreichbarer grafischer Browser gefunden.",
            "Backend-Readiness fehlgeschlagen.",
            "Browser-/Dashboard-Handshake fehlgeschlagen.",
            "Finaler Statuscheck fehlgeschlagen.",
            "AUTOSTART FEHLER",
        ):
            self.assertIn(message, self.autostart)

    def test_launcher_keeps_backend_reports_and_quarantine_separate(self) -> None:
        for filename in (
            "launcher-console.log",
            "launcher-backend.log",
            "launcher-report.json",
            "launcher-report.txt",
            "server.log",
        ):
            self.assertIn(filename, self.autostart)
        self.assertIn("MAX_LOG_BYTES", self.autostart)
        self.assertIn("_rotate", self.autostart)
        self.assertIn("quarantine", self.runtime_health)

    def test_runtime_start_uses_runtime_preflight_not_repository_validator(self) -> None:
        self.assertIn("from .preflight import load_runtime_manifest, run_preflight", self.autostart)
        self.assertIn("run_preflight(root=root, version=VERSION)", self.autostart)
        self.assertNotIn("scripts/validate.py", self.autostart)
        self.assertIn("RUNTIME_MANIFEST.json", self.preflight)

    def test_launcher_verifies_instance_and_uses_safe_fallback_port(self) -> None:
        self.assertIn("from scripts.launcher_probe import ensure_marker, inspect", self.autostart)
        self.assertIn("ensure_marker()", self.autostart)
        self.assertIn('probe["state"] == "own-ready"', self.autostart)
        self.assertIn('probe["state"] == "occupied"', self.autostart)
        self.assertIn("_find_free(requested + 1)", self.autostart)

    def test_launcher_rejects_invalid_port_and_bounds_scan(self) -> None:
        self.assertIn("def _normalize_port", self.autostart)
        self.assertIn("1024 <= port <= 65535", self.autostart)
        self.assertIn("PORT_SCAN = 50", self.autostart)
        self.assertIn("def _find_free", self.autostart)
        self.assertIn("Kein freier Loopback-Port", self.autostart)

    def test_backend_and_handshake_remain_loopback_only(self) -> None:
        self.assertIn('("127.0.0.1", port)', self.autostart)
        self.assertIn('f"127.0.0.1:{port}"', self.autostart)
        self.assertIn('"GET", "/api/status"', self.autostart)
        self.assertIn("http://127.0.0.1", self.autostart)

    def test_read_only_portable_source_is_mirrored_without_mutating_source(self) -> None:
        self.assertIn("_relaunch_from_writable_mirror", self.autostart)
        self.assertIn("AIO_MIRRORED_FROM", self.autostart)
        self.assertIn("_make_user_copy_writable", self.portable)
        self.assertIn("_copytree_into_writable_user_mirror", self.portable)

    def test_desktop_launcher_shows_console_and_only_pauses_on_failure(self) -> None:
        self.assertIn("Terminal=true", self.desktop)
        self.assertIn('if [ "$code" -ne 0 ]', self.desktop)
        self.assertIn("Start fehlgeschlagen", self.desktop)
        self.assertIn("runtime/", self.desktop)
        self.assertIn("Enter zum Schließen", self.desktop)


if __name__ == "__main__":
    unittest.main()

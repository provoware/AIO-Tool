from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SafeFileSimulatorContractTests(unittest.TestCase):
    def test_simulator_exposes_no_execution_endpoint_or_copy_primitive(self):
        script = (ROOT / "scripts" / "safe_file_simulator.py").read_text(encoding="utf-8")
        core = (ROOT / "app" / "safe_file_sim.py").read_text(encoding="utf-8")
        combined = script + "\n" + core
        self.assertNotIn("/api/execute", combined)
        self.assertNotIn("shutil.copy", combined)
        self.assertNotIn("copy2(", combined)
        self.assertNotIn("copyfile(", combined)
        self.assertNotIn("os.replace(", combined)
        self.assertIn("EXECUTION_ENABLED = False", core)
        self.assertIn("mutation_performed", core)


if __name__ == "__main__":
    unittest.main()

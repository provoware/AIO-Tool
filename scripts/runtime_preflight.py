#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.preflight import run_preflight


def main() -> int:
    parser = argparse.ArgumentParser(description="Sichere AIO-Tool Runtime-Vorprüfung")
    parser.add_argument("--quick", action="store_true", help="kompakte Startprüfung")
    parser.parse_args()
    result = run_preflight(emit=lambda label: print(f"OK: {label}"))
    print(f"RUNTIME PREFLIGHT PASS · {len(result['checks'])} Prüfungen")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

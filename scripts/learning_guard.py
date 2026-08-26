#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.learning_memory import active_entries, load_jsonl, relevant


def main() -> None:
    parser = argparse.ArgumentParser(description="Validiert das Entwicklungs-Lerngedächtnis.")
    parser.add_argument("--area", action="append", default=[], help="Nur Regeln für einen Bereich anzeigen.")
    args = parser.parse_args()

    entries = load_jsonl(ROOT / "LEARNING_MEMORY.jsonl")
    active = active_entries(entries)
    selected = relevant(entries, args.area) if args.area else active

    print(f"LEARNING MEMORY PASS: {len(entries)} Einträge, {len(active)} aktiv")
    for entry in selected:
        print(f"- {entry['id']} [{entry['area']}]: {entry['rule']}")


if __name__ == "__main__":
    main()

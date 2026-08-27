#!/usr/bin/env python3
from __future__ import annotations

"""Thin CI entry point for the canonical browser-acceptance implementation.

All asset discovery, fixture ordering, render auditing and interaction logic
lives in scripts/ui_acceptance.py. Keeping this file intentionally tiny avoids
a second browser-harness implementation drifting from the product contract.
"""

from ui_acceptance import main


if __name__ == "__main__":
    main()

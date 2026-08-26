"""AIO-Tool application package."""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
VERSION = (ROOT_DIR / "VERSION").read_text(encoding="utf-8").strip()

__all__ = ["ROOT_DIR", "VERSION"]

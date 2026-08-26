#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import os
import zipfile
from pathlib import Path

from app import ROOT_DIR, VERSION

EXCLUDE_PARTS = {".git", ".venv", "__pycache__", ".pytest_cache", "dist", "build"}
EXCLUDE_PREFIXES = {"runtime/"}
FIXED_TIME = (2026, 8, 27, 0, 0, 0)


def included_files():
    for path in sorted(ROOT_DIR.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT_DIR).as_posix()
        if any(part in EXCLUDE_PARTS for part in path.relative_to(ROOT_DIR).parts):
            continue
        if any(rel.startswith(prefix) for prefix in EXCLUDE_PREFIXES):
            continue
        if rel.endswith(".zip") or rel.endswith(".pyc"):
            continue
        yield path, rel


def build(output: Path) -> str:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path, rel in included_files():
            info = zipfile.ZipInfo(f"AIO-Tool-{VERSION}/{rel}", FIXED_TIME)
            mode = 0o755 if os.access(path, os.X_OK) or rel in {"start_tool.sh", "scripts/validate.py", "scripts/release.py"} else 0o644
            info.external_attr = mode << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    return digest


def main() -> None:
    parser = argparse.ArgumentParser(description="Reproduzierbares AIO-Tool Release-ZIP")
    parser.add_argument("--output", type=Path, default=ROOT_DIR / "dist" / f"AIO-Tool-{VERSION}.zip")
    parser.add_argument("--check", action="store_true", help="Build erzeugen und Inhalt auf Ausschlüsse prüfen")
    args = parser.parse_args()
    digest = build(args.output)
    if args.check:
        with zipfile.ZipFile(args.output) as zf:
            names = zf.namelist()
            forbidden = [n for n in names if "/runtime/" in n or "/.venv/" in n or "__pycache__" in n]
            if forbidden:
                raise SystemExit("FEHLER: unerlaubte Release-Dateien: " + ", ".join(forbidden))
    print(args.output)
    print("SHA256", digest)


if __name__ == "__main__":
    main()

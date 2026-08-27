#!/usr/bin/env python3
from __future__ import annotations

import argparse
import glob
import json
import os
import shutil
import stat
import subprocess
import tempfile
import zipfile
from pathlib import Path


def _run(executable: Path, *, home: Path, label: str) -> dict:
    env = dict(os.environ)
    env["HOME"] = str(home)
    env["XDG_STATE_HOME"] = str(home / ".local" / "state")
    env.pop("AIO_PORT", None)
    result = subprocess.run(
        [str(executable), "--no-browser", "--preflight-only"],
        cwd=executable.parent,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=30,
    )
    passed = result.returncode == 0 and "Prüflauf abgeschlossen" in result.stdout
    return {"label": label, "status": "PASS" if passed else "FAIL", "returncode": result.returncode, "output_tail": result.stdout[-5000:]}


def _read_only_tree(root: Path) -> None:
    for path in sorted(root.rglob("*"), reverse=True):
        if path.is_file():
            mode = 0o555 if os.access(path, os.X_OK) else 0o444
            path.chmod(mode)
        elif path.is_dir():
            path.chmod(0o555)
    root.chmod(0o555)


def main() -> int:
    parser = argparse.ArgumentParser(description="AIO-Tool Portable Smoke")
    parser.add_argument("--zip-glob", required=True)
    parser.add_argument("--output", type=Path, default=Path("artifacts/portable-smoke.json"))
    args = parser.parse_args()
    matches = sorted(glob.glob(args.zip_glob))
    if len(matches) != 1:
        raise SystemExit(f"PORTABLE SMOKE FEHLER: exakt ein ZIP erwartet, gefunden={matches}")
    archive = Path(matches[0]).resolve()

    with tempfile.TemporaryDirectory() as temp_name:
        temp = Path(temp_name)
        extract = temp / "normal"
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(extract)
        executables = list(extract.rglob("AIO-Tool-Start"))
        if len(executables) != 1:
            raise SystemExit("PORTABLE SMOKE FEHLER: Starter fehlt/ist doppelt.")
        executable = executables[0]
        executable.chmod(executable.stat().st_mode | stat.S_IXUSR)
        normal = _run(executable, home=temp / "home-normal", label="normal-writable")

        readonly_extract = temp / "readonly"
        shutil.copytree(executable.parent, readonly_extract / executable.parent.name)
        readonly_exe = readonly_extract / executable.parent.name / "AIO-Tool-Start"
        _read_only_tree(readonly_exe.parent)
        readonly = _run(readonly_exe, home=temp / "home-readonly", label="read-only-source-mirror")

        mirror_root = temp / "home-readonly" / ".local" / "state" / "aio-tool" / "installations"
        mirror_created = mirror_root.is_dir() and any(mirror_root.rglob("AIO-Tool-Start"))
        readonly["mirror_created"] = mirror_created
        if readonly["status"] == "PASS" and not mirror_created:
            readonly["status"] = "FAIL"
            readonly["output_tail"] += "\nKein Benutzer-Spiegel nach Read-only-Smoke gefunden."

    cases = [normal, readonly]
    passed = sum(case["status"] == "PASS" for case in cases)
    payload = {"schema_version": 1, "archive": archive.name, "total": len(cases), "passed": passed, "failed": len(cases) - passed, "cases": cases}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    raise SystemExit(main())

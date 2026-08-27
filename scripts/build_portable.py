#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXED_TIME = (2026, 8, 27, 0, 0, 0)


def _run(*args: str) -> None:
    print("+", " ".join(args), flush=True)
    subprocess.run(args, cwd=ROOT, check=True)


def _runtime_manifest() -> dict:
    return json.loads((ROOT / "manifests" / "RUNTIME_MANIFEST.json").read_text(encoding="utf-8"))


def _zip_tree(source: Path, output: Path) -> str:
    output.parent.mkdir(parents=True, exist_ok=True)
    root_name = source.name
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(source.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(source).as_posix()
            info = zipfile.ZipInfo(f"{root_name}/{rel}", FIXED_TIME)
            mode = 0o755 if os.access(path, os.X_OK) else 0o644
            info.external_attr = mode << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix + ".sha256").write_text(f"{digest}  {output.name}\n", encoding="utf-8")
    return digest


def build() -> tuple[Path, str]:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    manifest = _runtime_manifest()
    build_root = ROOT / "build"
    pyinstaller_dist = build_root / "portable-pyinstaller"
    package_root = ROOT / "dist" / "portable" / f"AIO-Tool-{version}-DEV-PORTABLE-LINUX-X86_64"
    shutil.rmtree(pyinstaller_dist, ignore_errors=True)
    shutil.rmtree(package_root, ignore_errors=True)
    package_root.parent.mkdir(parents=True, exist_ok=True)

    _run(sys.executable, "scripts/build_recovery_basis.py", "--check")
    _run(sys.executable, "scripts/release.py", "--check")

    add_data: list[str] = []
    for rel in manifest["files"]:
        source = ROOT / rel
        if not source.is_file():
            raise SystemExit(f"PORTABLE FEHLER: Runtime-Datei fehlt: {rel}")
        destination = Path(rel).parent.as_posix()
        if destination == ".":
            destination = "."
        add_data.extend(["--add-data", f"{source}:{destination}"])

    args = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm", "--clean", "--onedir",
        "--name", "AIO-Tool-Start",
        "--distpath", str(pyinstaller_dist),
        "--workpath", str(build_root / "pyinstaller-work"),
        "--specpath", str(build_root / "pyinstaller-spec"),
        *add_data,
        str(ROOT / "scripts" / "portable_entry.py"),
    ]
    _run(*args)

    generated = pyinstaller_dist / "AIO-Tool-Start"
    if not generated.is_dir():
        raise SystemExit("PORTABLE FEHLER: PyInstaller-Ausgabe fehlt.")
    shutil.copytree(generated, package_root)

    executable = package_root / "AIO-Tool-Start"
    internal = package_root / "_internal"
    if not executable.is_file() or not internal.is_dir():
        raise SystemExit("PORTABLE FEHLER: onedir-Struktur unvollständig.")
    executable.chmod(executable.stat().st_mode | 0o111)

    for rel in ("start_tool.sh", "start_tool.desktop"):
        shutil.copy2(ROOT / rel, package_root / rel)
        (package_root / rel).chmod((package_root / rel).stat().st_mode | 0o111)

    shutil.copy2(ROOT / "dist" / "recovery" / "RECOVERY_BASIS.zip", internal / "RECOVERY_BASIS.zip")
    runtime_zip = next((ROOT / "dist").glob(f"AIO-Tool-{version}-DEV.zip"), None)
    if runtime_zip is None:
        raise SystemExit("PORTABLE FEHLER: Runtime-ZIP für MANIFEST_RELEASE fehlt.")
    with zipfile.ZipFile(runtime_zip) as zf:
        release_name = f"AIO-Tool-{version}/MANIFEST_RELEASE.json"
        (internal / "MANIFEST_RELEASE.json").write_bytes(zf.read(release_name))

    readme = package_root / "PORTABLE-INFO.txt"
    readme.write_text(
        "AIO-Tool portable Linux x86_64\n"
        f"Version: {version}\n\n"
        "Start: Doppelklick auf start_tool.desktop oder ./start_tool.sh\n"
        "Das Paket enthält seinen Python-Interpreter. Keine Installation, kein sudo, kein pip.\n"
        "Bei schreibgeschützter Quelle spiegelt die Startroutine die Basis datensicher in den Benutzerbereich.\n",
        encoding="utf-8",
    )

    output = package_root.parent / f"{package_root.name}.zip"
    digest = _zip_tree(package_root, output)
    return output, digest


def verify(output: Path) -> None:
    with zipfile.ZipFile(output) as zf:
        names = zf.namelist()
        required_suffixes = (
            "/AIO-Tool-Start",
            "/start_tool.sh",
            "/start_tool.desktop",
            "/_internal/VERSION",
            "/_internal/MANIFEST_RELEASE.json",
            "/_internal/RECOVERY_BASIS.zip",
            "/_internal/manifests/RUNTIME_MANIFEST.json",
        )
        for suffix in required_suffixes:
            if not any(name.endswith(suffix) for name in names):
                raise SystemExit(f"PORTABLE FEHLER: Paketbestandteil fehlt: {suffix}")


def main() -> int:
    parser = argparse.ArgumentParser(description="AIO-Tool Portable Linux Builder")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output, digest = build()
    if args.check:
        verify(output)
    print(output)
    print("SHA256", digest)
    print("PORTABLE BUILD PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

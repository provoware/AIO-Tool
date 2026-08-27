#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "RUNTIME_MANIFEST.json"
FIXED_TIME = (2026, 8, 27, 0, 0, 0)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def load_manifest() -> dict:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    files = data.get("files")
    if data.get("schema_version") != 1 or not isinstance(files, list) or not files:
        raise SystemExit("RECOVERY FEHLER: Runtime-Manifest ungültig.")
    if len(files) != len(set(files)):
        raise SystemExit("RECOVERY FEHLER: Runtime-Manifest enthält Duplikate.")
    return data


def build(output: Path) -> tuple[Path, str]:
    manifest = load_manifest()
    entries: list[dict[str, object]] = []
    for rel in manifest["files"]:
        path = ROOT / rel
        if not path.is_file():
            raise SystemExit(f"RECOVERY FEHLER: Basisdatei fehlt: {rel}")
        raw = path.read_bytes()
        entries.append({"path": rel, "size": len(raw), "sha256": sha256_bytes(raw)})

    recovery_manifest = {
        "schema_version": 1,
        "tool": "AIO-Tool",
        "version": (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        "runtime_manifest_version": manifest.get("manifest_version"),
        "file_count": len(entries),
        "files": entries,
    }
    manifest_bytes = (json.dumps(recovery_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        info = zipfile.ZipInfo("RECOVERY_MANIFEST.json", FIXED_TIME)
        info.external_attr = 0o644 << 16
        info.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(info, manifest_bytes)
        for item in entries:
            rel = str(item["path"])
            raw = (ROOT / rel).read_bytes()
            info = zipfile.ZipInfo("files/" + rel, FIXED_TIME)
            mode = 0o755 if os.access(ROOT / rel, os.X_OK) else 0o644
            info.external_attr = mode << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, raw)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix + ".sha256").write_text(f"{digest}  {output.name}\n", encoding="utf-8")
    return output, digest


def verify(output: Path) -> None:
    manifest = load_manifest()
    expected = set(manifest["files"])
    with zipfile.ZipFile(output) as zf:
        recovery = json.loads(zf.read("RECOVERY_MANIFEST.json").decode("utf-8"))
        if recovery.get("schema_version") != 1 or recovery.get("file_count") != len(expected):
            raise SystemExit("RECOVERY FEHLER: Recovery-Manifest inkonsistent.")
        listed = {str(item["path"]): item for item in recovery.get("files", [])}
        if set(listed) != expected:
            raise SystemExit("RECOVERY FEHLER: Dateimenge weicht von Runtime-Allowlist ab.")
        expected_names = {"RECOVERY_MANIFEST.json"} | {"files/" + rel for rel in expected}
        names = {name for name in zf.namelist() if not name.endswith("/")}
        if names != expected_names:
            raise SystemExit("RECOVERY FEHLER: ZIP enthält fehlende oder zusätzliche Dateien.")
        for rel, item in listed.items():
            raw = zf.read("files/" + rel)
            if len(raw) != item.get("size") or sha256_bytes(raw) != item.get("sha256"):
                raise SystemExit(f"RECOVERY FEHLER: Hashprüfung fehlgeschlagen: {rel}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministische AIO-Tool RECOVERY_BASIS")
    parser.add_argument("--output", type=Path, default=ROOT / "dist" / "recovery" / "RECOVERY_BASIS.zip")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output, digest = build(args.output)
    if args.check:
        verify(output)
    print(output)
    print("SHA256", digest)
    print("RECOVERY_BASIS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

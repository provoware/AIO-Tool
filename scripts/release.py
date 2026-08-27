#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import ROOT_DIR, VERSION

RUNTIME_MANIFEST_PATH = ROOT_DIR / "manifests" / "RUNTIME_MANIFEST.json"
REGISTRY_PATH = ROOT_DIR / "VERSION_REGISTRY.json"
FIXED_TIME = (2026, 8, 27, 0, 0, 0)
STATUS_LABELS = {
    "development": "DEV",
    "tested": "TESTED",
    "release_candidate": "RC",
    "released": "RELEASED",
    "deprecated": "ARCHIVED",
    "blocked": "BLOCKED",
}


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"FEHLER: {path.name} ist nicht lesbar.") from exc


def load_runtime_manifest() -> dict:
    data = _load_json(RUNTIME_MANIFEST_PATH)
    if data.get("schema_version") != 1 or not isinstance(data.get("files"), list):
        raise SystemExit("FEHLER: Runtime-Manifest-Schema unbekannt.")
    files = data["files"]
    if len(files) != len(set(files)) or not all(isinstance(item, str) and item for item in files):
        raise SystemExit("FEHLER: Runtime-Manifest enthält ungültige oder doppelte Pfade.")
    return data


def current_version_record() -> dict:
    registry = _load_json(REGISTRY_PATH)
    if registry.get("current_version") != VERSION:
        raise SystemExit("FEHLER: VERSION und VERSION_REGISTRY.json weichen voneinander ab.")
    matches = [item for item in registry.get("versions", []) if item.get("version") == VERSION]
    if len(matches) != 1:
        raise SystemExit("FEHLER: Aktuelle Version fehlt oder ist doppelt in der Registry.")
    return matches[0]


def status_label(record: dict) -> str:
    status = str(record.get("status", "development")).strip().lower()
    release_status = str(record.get("release_status", "draft")).strip().lower()
    if release_status == "released":
        return "RELEASED"
    if release_status in {"release_candidate", "rc"}:
        return "RC"
    return STATUS_LABELS.get(status, "DRAFT")


def runtime_files(manifest: dict):
    for rel in manifest["files"]:
        path = ROOT_DIR / rel
        if not path.is_file():
            raise SystemExit(f"FEHLER: deklarierte Runtime-Basisdatei fehlt: {rel}")
        yield path, rel


def _file_meta(path: Path, rel: str) -> dict:
    raw = path.read_bytes()
    return {"path": rel, "size": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def build(output: Path | None = None) -> tuple[Path, str]:
    manifest = load_runtime_manifest()
    record = current_version_record()
    label = status_label(record)
    archive_name = f"AIO-Tool-{VERSION}-{label}.zip"
    output = output or (ROOT_DIR / "dist" / archive_name)
    if not output.name.endswith(f"-{label}.zip"):
        raise SystemExit(f"FEHLER: Release-Dateiname muss den Status -{label}.zip enthalten.")
    output.parent.mkdir(parents=True, exist_ok=True)

    entries = list(runtime_files(manifest))
    release_manifest = {
        "schema_version": 1,
        "tool": "AIO-Tool",
        "version": VERSION,
        "status": label,
        "registry_status": record.get("status"),
        "release_status": record.get("release_status"),
        "runtime_manifest_version": manifest.get("manifest_version"),
        "archive_name": output.name,
        "file_count": len(entries) + 1,
        "files": [_file_meta(path, rel) for path, rel in entries],
    }
    release_bytes = (json.dumps(release_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")

    root_name = f"AIO-Tool-{VERSION}"
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path, rel in entries:
            info = zipfile.ZipInfo(f"{root_name}/{rel}", FIXED_TIME)
            mode = 0o755 if os.access(path, os.X_OK) or rel in {"start_tool.sh", "scripts/runtime_preflight.py"} else 0o644
            info.external_attr = mode << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())
        info = zipfile.ZipInfo(f"{root_name}/MANIFEST_RELEASE.json", FIXED_TIME)
        info.external_attr = 0o644 << 16
        info.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(info, release_bytes)
    return output, hashlib.sha256(output.read_bytes()).hexdigest()


def verify(output: Path) -> None:
    runtime_manifest = load_runtime_manifest()
    expected_rel = set(runtime_manifest["files"]) | {"MANIFEST_RELEASE.json"}
    root_name = f"AIO-Tool-{VERSION}/"
    with zipfile.ZipFile(output) as zf:
        names = [name for name in zf.namelist() if not name.endswith("/")]
        if any(not name.startswith(root_name) for name in names):
            raise SystemExit("FEHLER: ZIP enthält Dateien außerhalb des Versionsordners.")
        rel_names = {name.removeprefix(root_name) for name in names}
        if rel_names != expected_rel:
            missing = sorted(expected_rel - rel_names)
            extra = sorted(rel_names - expected_rel)
            raise SystemExit(f"FEHLER: Release-Inhalt weicht vom Runtime-Manifest ab. Fehlend={missing}; Extra={extra}")
        release_manifest = json.loads(zf.read(root_name + "MANIFEST_RELEASE.json").decode("utf-8"))
        if release_manifest.get("archive_name") != output.name:
            raise SystemExit("FEHLER: Release-Manifest und Dateiname stimmen nicht überein.")
        listed = {item["path"]: item for item in release_manifest.get("files", [])}
        if set(listed) != set(runtime_manifest["files"]):
            raise SystemExit("FEHLER: Release-Manifest listet nicht exakt die Runtime-Basis.")
        for rel, meta in listed.items():
            raw = zf.read(root_name + rel)
            if len(raw) != meta.get("size") or hashlib.sha256(raw).hexdigest() != meta.get("sha256"):
                raise SystemExit(f"FEHLER: Hash-/Größenprüfung fehlgeschlagen: {rel}")
        forbidden_prefixes = tuple(runtime_manifest.get("forbidden_prefixes", []))
        repo_only_root = set(runtime_manifest.get("repo_only_root_files", []))
        forbidden = [rel for rel in rel_names if rel in repo_only_root or rel.startswith(forbidden_prefixes)]
        if forbidden:
            raise SystemExit("FEHLER: Repo-/Log-/Testinhalt im Runtime-ZIP: " + ", ".join(sorted(forbidden)))


def main() -> None:
    record = current_version_record()
    label = status_label(record)
    default_output = ROOT_DIR / "dist" / f"AIO-Tool-{VERSION}-{label}.zip"
    parser = argparse.ArgumentParser(description="Reproduzierbares AIO-Tool Runtime-Release-ZIP")
    parser.add_argument("--output", type=Path, default=default_output)
    parser.add_argument("--check", action="store_true", help="Build erzeugen und Manifest/Allowlist/Hashes prüfen")
    args = parser.parse_args()
    output, digest = build(args.output)
    if args.check:
        verify(output)
    print(output)
    print("STATUS", label)
    print("SHA256", digest)


if __name__ == "__main__":
    main()

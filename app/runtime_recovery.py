from __future__ import annotations

import hashlib
import json
import os
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _atomic_restore(destination: Path, payload: bytes) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp = destination.with_suffix(destination.suffix + ".recovery.tmp")
    try:
        with temp.open("wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, destination)
    finally:
        try:
            temp.unlink(missing_ok=True)
        except OSError:
            pass


def restore_runtime_assets(root: Path, runtime_dir: Path) -> dict[str, Any]:
    """Repair transported assets from the offline recovery basis.

    Auto-repair is enabled only for a built release. Source checkouts are never
    rewritten behind a developer's back.
    """
    root = Path(root)
    recovery = root / "RECOVERY_BASIS.zip"
    release_marker = root / "MANIFEST_RELEASE.json"
    if not release_marker.is_file() or not recovery.is_file():
        return {"enabled": False, "restored": [], "quarantined": []}
    restored: list[str] = []
    quarantined: list[str] = []
    quarantine_root = runtime_dir / "quarantine" / "runtime-assets" / _stamp()
    try:
        with zipfile.ZipFile(recovery) as zf:
            manifest = json.loads(zf.read("RECOVERY_MANIFEST.json").decode("utf-8"))
            files = manifest.get("files")
            if manifest.get("schema_version") != 1 or not isinstance(files, list):
                raise RuntimeError("Recovery-Manifest ist ungültig.")
            for item in files:
                if not isinstance(item, dict):
                    raise RuntimeError("Recovery-Dateieintrag ist ungültig.")
                rel = item.get("path")
                expected = item.get("sha256")
                if not isinstance(rel, str) or not rel or not isinstance(expected, str):
                    raise RuntimeError("Recovery-Dateieintrag ist unvollständig.")
                payload = zf.read("files/" + rel)
                if hashlib.sha256(payload).hexdigest() != expected:
                    raise RuntimeError(f"Recovery-Basis selbst ist beschädigt: {rel}")
                destination = root / rel
                healthy = destination.is_file() and _sha256(destination) == expected
                if healthy:
                    continue
                if destination.exists():
                    preserved = quarantine_root / rel
                    preserved.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(destination), str(preserved))
                    quarantined.append(str(preserved))
                _atomic_restore(destination, payload)
                restored.append(rel)
    except (OSError, KeyError, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        raise RuntimeError("RECOVERY_BASIS.zip ist nicht sicher lesbar.") from exc
    return {"enabled": True, "restored": restored, "quarantined": quarantined}

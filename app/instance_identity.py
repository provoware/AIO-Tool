from __future__ import annotations

import hashlib
from pathlib import Path

UI_CONTRACT_VERSION = "dashboard-v2.2"
INSTANCE_ID_LENGTH = 16


def runtime_instance_id(root: Path, version: str) -> str:
    """Stable ID for one concrete installation path + version.

    Prevents a launcher/browser from treating another local AIO-Tool copy or
    an older version on the same port as the current installation.
    """
    canonical = str(root.resolve(strict=False))
    payload = f"aio-tool\0{canonical}\0{version}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:INSTANCE_ID_LENGTH]

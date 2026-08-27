from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any, Callable

from . import ROOT_DIR, VERSION
from .config import ConfigStore, DEFAULT_CONFIG
from .error_advisor import ErrorAdvisor
from .loopback_security import allowed_local_request
from .native_acceptance import NativeAcceptanceStore, STEPS
from .safe_file_sim import build_preview
from .version_registry import validate_registry


def load_runtime_manifest(root: Path = ROOT_DIR) -> dict[str, Any]:
    path = root / "manifests" / "RUNTIME_MANIFEST.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError("Runtime-Manifest ist nicht lesbar.") from exc
    if data.get("schema_version") != 1 or not isinstance(data.get("files"), list):
        raise RuntimeError("Runtime-Manifest hat ein unbekanntes Schema.")
    files = data["files"]
    if len(files) != len(set(files)) or not all(isinstance(item, str) and item for item in files):
        raise RuntimeError("Runtime-Manifest enthält ungültige oder doppelte Dateipfade.")
    return data


def run_preflight(*, root: Path = ROOT_DIR, version: str = VERSION, emit: Callable[[str], None] | None = None) -> dict[str, Any]:
    """Validate only the transported runtime contract.

    Source launcher and portable binary call the same contract so bootstrap
    behavior cannot drift between distribution forms.
    """
    messages: list[str] = []

    def check(condition: bool, label: str) -> None:
        if not condition:
            raise RuntimeError(label)
        messages.append(label)
        if emit:
            emit(label)

    manifest = load_runtime_manifest(root)
    for rel in manifest["files"]:
        check((root / rel).is_file(), f"Basisdatei {rel} vorhanden")
    check(bool(version), "Version vorhanden")
    registry = validate_registry(json.loads((root / "VERSION_REGISTRY.json").read_text(encoding="utf-8")))
    check(registry["current_version"] == version, "VERSION und Registry stimmen überein")
    check((root / "web").is_dir(), "Weboberfläche vorhanden")
    check(allowed_local_request("127.0.0.1:8765", "http://127.0.0.1:8765", 8765), "gleicher Loopback-Port erlaubt")
    check(not allowed_local_request("127.0.0.1:8765", "http://127.0.0.1:9999", 8765), "Cross-Port blockiert")
    check(not allowed_local_request("example.com", "https://example.com", 8765), "Fremdhost blockiert")
    advisor = ErrorAdvisor()
    check(advisor.metadata()["rule_count"] >= 1, "Fehlerhilfe und Referenzvorlagen lesbar")
    with tempfile.TemporaryDirectory() as tmp:
        temp_root = Path(tmp)
        store = ConfigStore(temp_root / "config.json")
        saved = store.save(DEFAULT_CONFIG)
        check(store.load() == saved, "atomare Konfiguration funktioniert")
        native = NativeAcceptanceStore(temp_root / "native.json", version)
        check(native.report()["counts"]["pending"] == len(STEPS) == 18, "Native Acceptance startet mit 18 offenen Schritten")
        source = temp_root / "source.txt"
        source.write_text("preview", encoding="utf-8")
        target = temp_root / "target"
        target.mkdir()
        preview = build_preview(source, target, free_bytes=100 * 1024 * 1024)
        check(preview["simulation_only"] is True and preview["execution_enabled"] is False and preview["mutation_performed"] is False, "SAFE-FILE-Runtime bleibt reine Simulation")
    return {"ok": True, "version": version, "checks": messages}

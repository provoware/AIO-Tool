#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_PATH = ROOT / "manifests" / "RUNTIME_MANIFEST.json"
DEVELOPMENT_PATH = ROOT / "manifests" / "DEVELOPMENT_MANIFEST.json"


class ManifestContractError(ValueError):
    pass


def _load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ManifestContractError(f"Manifest nicht lesbar: {path}") from exc
    if not isinstance(value, dict):
        raise ManifestContractError(f"Manifest muss ein JSON-Objekt sein: {path}")
    return value


def _string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise ManifestContractError(f"{label} muss eine Liste nicht-leerer Pfade/Texte sein.")
    if len(value) != len(set(value)):
        raise ManifestContractError(f"{label} enthält Duplikate.")
    return value


def _flatten_categories(categories: dict[str, Any]) -> set[str]:
    if not isinstance(categories, dict) or not categories:
        raise ManifestContractError("Development-Manifest categories fehlt/ist leer.")
    result: set[str] = set()
    for name, values in categories.items():
        if not isinstance(name, str) or not name.strip():
            raise ManifestContractError("Development-Manifest enthält ungültige Kategorienamen.")
        for item in _string_list(values, f"categories.{name}"):
            result.add(item)
    return result


def _matches_prefix(path: str, prefixes: list[str]) -> bool:
    return any(path.startswith(prefix) for prefix in prefixes)


def validate_manifests(runtime: dict[str, Any], development: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    if runtime.get("schema_version") != 1:
        raise ManifestContractError("Runtime-Manifest-Schema muss 1 sein.")
    if development.get("schema_version") != 1:
        raise ManifestContractError("Development-Manifest-Schema muss 1 sein.")
    if development.get("scope") != "repository-only":
        raise ManifestContractError("Development-Manifest muss scope=repository-only deklarieren.")

    runtime_files = _string_list(runtime.get("files"), "runtime.files")
    generated = _string_list(runtime.get("generated_files"), "runtime.generated_files")
    forbidden = _string_list(runtime.get("forbidden_prefixes"), "runtime.forbidden_prefixes")
    repo_only_root = _string_list(runtime.get("repo_only_root_files"), "runtime.repo_only_root_files")
    status_documents = _string_list(development.get("status_documents"), "development.status_documents")
    evidence_documents = _string_list(development.get("evidence_summary_documents"), "development.evidence_summary_documents")
    policy_documents = _string_list(development.get("policy_documents"), "development.policy_documents")
    dev_paths = _flatten_categories(development.get("categories"))

    if "manifests/RUNTIME_MANIFEST.json" not in runtime_files:
        raise ManifestContractError("Runtime-Manifest muss sich selbst in der Runtime-Allowlist führen.")
    if "manifests/DEVELOPMENT_MANIFEST.json" in runtime_files:
        raise ManifestContractError("Development-Manifest darf nicht Teil der Runtime-Allowlist sein.")
    if "manifests/DEVELOPMENT_MANIFEST.json" not in dev_paths:
        raise ManifestContractError("Development-Manifest muss im Repository-Bestand selbst klassifiziert sein.")
    if "manifests/README.md" not in policy_documents or "manifests/README.md" not in dev_paths:
        raise ManifestContractError("Manifest-Policy-Dokument fehlt in Development-Manifest.")

    forbidden_runtime = sorted(path for path in runtime_files if _matches_prefix(path, forbidden))
    if forbidden_runtime:
        raise ManifestContractError("Runtime-Allowlist verletzt forbidden_prefixes: " + ", ".join(forbidden_runtime))

    exact_dev_files = {path for path in dev_paths if not path.endswith("/")}
    dev_prefixes = [path for path in dev_paths if path.endswith("/")]
    overlap = sorted(path for path in runtime_files if path in exact_dev_files or _matches_prefix(path, dev_prefixes))
    if overlap:
        raise ManifestContractError("Runtime-Dateien zugleich als repository-only klassifiziert: " + ", ".join(overlap))

    missing_repo_only = sorted(path for path in repo_only_root if path not in dev_paths)
    if missing_repo_only:
        raise ManifestContractError("repo_only_root_files fehlen im Development-Manifest: " + ", ".join(missing_repo_only))

    missing_status_docs = sorted(path for path in status_documents if path not in dev_paths)
    if missing_status_docs:
        raise ManifestContractError("Statusdokumente nicht als repo-only klassifiziert: " + ", ".join(missing_status_docs))
    if not set(evidence_documents).issubset(set(status_documents)):
        raise ManifestContractError("evidence_summary_documents müssen Teil der status_documents sein.")

    # Legacy-Semantik von Runtime-Manifest 1.3.0: MANIFEST_RELEASE.json wird beim Build
    # erzeugt und transportiert; die übrigen generated_files entstehen erst nach dem Start.
    if "MANIFEST_RELEASE.json" not in generated:
        raise ManifestContractError("Build-generiertes MANIFEST_RELEASE.json fehlt in generated_files.")
    post_start_generated = [path for path in generated if path != "MANIFEST_RELEASE.json"]
    generated_overlap = sorted(path for path in runtime_files if path in post_start_generated)
    if generated_overlap:
        raise ManifestContractError("Lokal erzeugte Dateien dürfen nicht fest transportiert werden: " + ", ".join(generated_overlap))

    authority = development.get("authority")
    if not isinstance(authority, dict):
        raise ManifestContractError("Development-Manifest authority fehlt.")
    expected_authority = {
        "runtime_transport": "manifests/RUNTIME_MANIFEST.json",
        "release_evidence": "evidence/RELEASE_EVIDENCE_INDEX.json",
        "repository_inventory": "manifests/DEVELOPMENT_MANIFEST.json",
        "human_status_summary": "MANIFEST.md",
    }
    for key, expected in expected_authority.items():
        if authority.get(key) != expected:
            raise ManifestContractError(f"authority.{key} muss {expected!r} sein.")
    if authority.get("runtime_status") != ["VERSION", "VERSION_REGISTRY.json"]:
        raise ManifestContractError("authority.runtime_status muss VERSION + VERSION_REGISTRY.json sein.")

    return runtime, development


def load_and_validate(*, root: Path = ROOT) -> tuple[dict[str, Any], dict[str, Any]]:
    return validate_manifests(
        _load(root / "manifests" / "RUNTIME_MANIFEST.json"),
        _load(root / "manifests" / "DEVELOPMENT_MANIFEST.json"),
    )


def main() -> int:
    runtime, development = load_and_validate()
    print(
        "MANIFEST GUARD PASS: "
        f"runtime={runtime.get('manifest_version')} · "
        f"development={development.get('manifest_version')} · "
        f"status_docs={len(development['status_documents'])}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ManifestContractError as exc:
        print("MANIFEST GUARD FEHLER: " + str(exc), file=sys.stderr)
        raise SystemExit(1)

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.version_registry import validate_registry


class IterationSyncError(ValueError):
    pass


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IterationSyncError(f"nicht lesbar/ungültig: {path}") from exc
    if not isinstance(value, dict):
        raise IterationSyncError(f"JSON-Objekt erwartet: {path}")
    return value


def _git(root: Path, *args: str, allow_fail: bool = False) -> str | None:
    result = subprocess.run(
        ["git", *args], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, check=False,
    )
    if result.returncode != 0:
        if allow_fail:
            return None
        detail = result.stderr.strip() or result.stdout.strip() or f"exit={result.returncode}"
        raise IterationSyncError(f"Git-Aufruf fehlgeschlagen: git {' '.join(args)}: {detail}")
    return result.stdout.strip()


def read_git_state(root: Path) -> dict[str, Any] | None:
    if _git(root, "rev-parse", "--is-inside-work-tree", allow_fail=True) != "true":
        return None
    head = _git(root, "rev-parse", "HEAD")
    tree = _git(root, "rev-parse", "HEAD^{tree}")
    branch = _git(root, "symbolic-ref", "--quiet", "--short", "HEAD", allow_fail=True) or "DETACHED"
    dirty = [line for line in (_git(root, "status", "--porcelain=v1", "--untracked-files=all") or "").splitlines() if line.strip()]
    return {"head": head, "tree": tree, "branch": branch, "clean": not dirty, "dirty_entries": dirty}


def validate_iteration(
    root: Path,
    *,
    expected_commit: str | None = None,
    require_git: bool = False,
    require_clean: bool = False,
    git_state: dict[str, Any] | None | object = ...,
) -> dict[str, Any]:
    root = root.resolve()
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if not version or any(ch.isspace() for ch in version):
        raise IterationSyncError("VERSION fehlt oder enthält Leerraum.")

    registry = validate_registry(_load_json(root / "VERSION_REGISTRY.json"))
    if registry.get("current_version") != version:
        raise IterationSyncError(
            f"VERSION/Registry-Drift: VERSION={version!r}, current_version={registry.get('current_version')!r}."
        )
    versions = registry["versions"]
    current_rows = [row for row in versions if row["version"] == version]
    if len(current_rows) != 1:
        raise IterationSyncError(f"Aktuelle Version muss exakt einmal registriert sein: {version}")
    current = current_rows[0]
    if versions[-1]["version"] != version:
        raise IterationSyncError("current_version muss der letzte Registry-Eintrag sein.")

    runtime = _load_json(root / "manifests" / "RUNTIME_MANIFEST.json")
    development = _load_json(root / "manifests" / "DEVELOPMENT_MANIFEST.json")
    runtime_files = runtime.get("files")
    if not isinstance(runtime_files, list) or "VERSION" not in runtime_files or "VERSION_REGISTRY.json" not in runtime_files:
        raise IterationSyncError("Runtime-Manifest muss VERSION und VERSION_REGISTRY.json transportieren.")

    status_docs = development.get("status_documents")
    if not isinstance(status_docs, list) or not status_docs:
        raise IterationSyncError("Development-Manifest enthält keine status_documents.")
    doc_records = []
    for rel in status_docs:
        path = root / rel
        if not isinstance(rel, str) or not path.is_file() or path.is_symlink():
            raise IterationSyncError(f"Statusdokument fehlt/ist ungültig: {rel}")
        if version not in path.read_text(encoding="utf-8"):
            raise IterationSyncError(f"Statusdokument ist nicht auf aktuelle Version synchronisiert: {rel}")
        doc_records.append({"path": rel, "version_present": True})

    if git_state is ...:
        git_state = read_git_state(root)
    if git_state is None:
        if require_git:
            raise IterationSyncError("Git-Repository ist für diese Prüfung erforderlich.")
        repository = {
            "available": False, "head": None, "tree": None, "branch": None,
            "clean": None, "expected_commit": expected_commit, "expected_commit_match": None,
        }
    else:
        head = str(git_state.get("head") or "").lower()
        tree = str(git_state.get("tree") or "").lower()
        branch = str(git_state.get("branch") or "DETACHED")
        clean = bool(git_state.get("clean"))
        for label, sha in (("HEAD", head), ("Tree", tree)):
            if len(sha) != 40 or any(ch not in "0123456789abcdef" for ch in sha):
                raise IterationSyncError(f"Git-{label} ist kein gültiger 40-stelliger SHA1.")
        expected = expected_commit.lower() if expected_commit else None
        match = None if expected is None else head == expected
        if expected is not None and not match:
            raise IterationSyncError(f"CI-/Repo-Commit-Drift: HEAD={head}, erwartet={expected}.")
        if require_clean and not clean:
            dirty = git_state.get("dirty_entries") or []
            raise IterationSyncError("Arbeitsbaum ist nicht sauber: " + "; ".join(str(item) for item in dirty[:20]))
        repository = {
            "available": True, "head": head, "tree": tree, "branch": branch, "clean": clean,
            "expected_commit": expected, "expected_commit_match": match,
        }

    return {
        "schema_version": 1,
        "tool": "AIO-Tool",
        "synchronized": True,
        "version": version,
        "registry_current_version": registry["current_version"],
        "status": current["status"],
        "release_status": current["release_status"],
        "registry_commit_sha": current.get("commit_sha"),
        "runtime_manifest_version": runtime.get("manifest_version"),
        "development_manifest_version": development.get("manifest_version"),
        "status_documents": doc_records,
        "repository": repository,
        "policy": {
            "repo_head_is_generated_evidence_not_versioned_registry_state": True,
            "reason": "verhindert selbstreferenzielle Commit-Sync-Schleifen",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="AIO-Tool Iterations-Sync: aktuelle Version ↔ Repository")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--expect-commit")
    parser.add_argument("--require-git", action="store_true")
    parser.add_argument("--require-clean", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = validate_iteration(
            args.root, expected_commit=args.expect_commit,
            require_git=args.require_git, require_clean=args.require_clean,
        )
    except (IterationSyncError, OSError, ValueError) as exc:
        print("ITERATION SYNC FEHLER: " + str(exc), file=sys.stderr)
        return 1
    if args.output:
        output = args.output if args.output.is_absolute() else args.root / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    repo = report["repository"]
    marker = repo["head"][:12] if repo["available"] else "source-ohne-git"
    print(f"ITERATION SYNC PASS: version={report['version']} · status={report['status']}/{report['release_status']} · repo={marker} · docs={len(report['status_documents'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

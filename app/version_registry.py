from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .persistence import AtomicJsonStore, PersistenceError

SCHEMA_VERSION = 1
VERSION_STATUSES = {"development", "tested", "release-candidate", "released", "blocked", "deprecated"}
RELEASE_STATUSES = {"draft", "candidate", "released", "blocked", "deprecated"}
EVIDENCE_REQUIRED = {"tested", "release-candidate", "released"}
STATUS_RELEASE_COMPATIBILITY = {
    "development": {"draft"},
    "tested": {"draft"},
    "release-candidate": {"candidate"},
    "released": {"released"},
    "blocked": {"blocked"},
    "deprecated": {"deprecated"},
}

DEFAULT_REGISTRY: dict[str, Any] = {
    "schema_version": SCHEMA_VERSION,
    "current_version": None,
    "versions": [],
}


class VersionRegistryError(PersistenceError):
    pass


def _text(value: Any, field: str, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise VersionRegistryError(f"{field} muss Text sein.")
    result = value.strip()
    if not result and not allow_empty:
        raise VersionRegistryError(f"{field} darf nicht leer sein.")
    return result


def _optional_text(value: Any, field: str) -> str | None:
    if value is None:
        return None
    result = _text(value, field, allow_empty=True)
    return result or None


def _string_list(value: Any, field: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise VersionRegistryError(f"{field} muss eine Textliste sein.")
    return [item.strip() for item in value if item.strip()]


def _evidence_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise VersionRegistryError("evidence muss eine Liste aus Objekten sein.")
    clean: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        kind = _text(item.get("kind"), f"evidence[{index}].kind")
        reference = _text(item.get("reference"), f"evidence[{index}].reference")
        clean.append({
            "time": _optional_text(item.get("time"), f"evidence[{index}].time"),
            "kind": kind,
            "reference": reference,
            "note": _text(item.get("note", ""), f"evidence[{index}].note", allow_empty=True),
        })
    return clean


def _validate_status_pair(status: str, release_status: str) -> None:
    allowed = STATUS_RELEASE_COMPATIBILITY.get(status)
    if allowed is None or release_status not in allowed:
        raise VersionRegistryError(
            f"Unzulässige Statuskombination: status={status}, release_status={release_status}."
        )


def validate_registry(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise VersionRegistryError("Versions-Registry muss ein Objekt sein.")
    if value.get("schema_version") != SCHEMA_VERSION:
        raise VersionRegistryError("Unbekannte Schema-Version der Versions-Registry.")
    versions = value.get("versions")
    if not isinstance(versions, list):
        raise VersionRegistryError("versions muss eine Liste sein.")

    clean_versions: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in versions:
        if not isinstance(raw, dict):
            raise VersionRegistryError("Versionseintrag muss ein Objekt sein.")
        version = _text(raw.get("version"), "version")
        if version in seen:
            raise VersionRegistryError(f"Version '{version}' ist doppelt registriert.")
        seen.add(version)
        status = _text(raw.get("status", "development"), "status")
        release_status = _text(raw.get("release_status", "draft"), "release_status")
        if status not in VERSION_STATUSES:
            raise VersionRegistryError(f"Unbekannter Versionsstatus: {status}")
        if release_status not in RELEASE_STATUSES:
            raise VersionRegistryError(f"Unbekannter Release-Status: {release_status}")
        _validate_status_pair(status, release_status)
        evidence = _evidence_list(raw.get("evidence", []))
        if status in EVIDENCE_REQUIRED and not evidence:
            raise VersionRegistryError(f"Status '{status}' benötigt mindestens einen Evidenznachweis.")
        clean_versions.append({
            "version": version,
            "created_at": _text(raw.get("created_at"), "created_at"),
            "status": status,
            "release_status": release_status,
            "commit_sha": _optional_text(raw.get("commit_sha"), "commit_sha"),
            "summary": _text(raw.get("summary", ""), "summary", allow_empty=True),
            "changes": _string_list(raw.get("changes", []), "changes"),
            "known_issues": _string_list(raw.get("known_issues", []), "known_issues"),
            "regression_status": _text(raw.get("regression_status", "pending"), "regression_status"),
            "evidence": evidence,
        })

    current = value.get("current_version")
    if current is not None:
        current = _text(current, "current_version")
        if current not in seen:
            raise VersionRegistryError("current_version ist nicht in versions registriert.")

    return {
        "schema_version": SCHEMA_VERSION,
        "current_version": current,
        "versions": clean_versions,
    }


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class VersionRegistry:
    def __init__(self, path: Path, default: dict[str, Any] | None = None):
        seed = DEFAULT_REGISTRY if default is None else default
        self.store = AtomicJsonStore(path, seed, validate_registry)

    def load(self) -> dict[str, Any]:
        return self.store.load()

    def ensure_current(
        self,
        version: str,
        *,
        summary: str = "",
        commit_sha: str | None = None,
        changes: list[str] | None = None,
    ) -> dict[str, Any]:
        version = _text(version, "version")
        clean_commit_sha = _optional_text(commit_sha, "commit_sha")

        def mutate(data: dict[str, Any]) -> dict[str, Any]:
            existing = next((item for item in data["versions"] if item["version"] == version), None)
            if existing is None:
                data["versions"].append({
                    "version": version,
                    "created_at": utc_now(),
                    "status": "development",
                    "release_status": "draft",
                    "commit_sha": clean_commit_sha,
                    "summary": summary.strip(),
                    "changes": list(changes or []),
                    "known_issues": [],
                    "regression_status": "pending",
                    "evidence": [],
                })
            else:
                if clean_commit_sha and not existing.get("commit_sha"):
                    existing["commit_sha"] = clean_commit_sha
                if summary and not existing.get("summary"):
                    existing["summary"] = summary.strip()
                if changes and not existing.get("changes"):
                    existing["changes"] = list(changes)
            data["current_version"] = version
            return data

        return self.store.update(mutate)

    def record_evidence(self, version: str, *, kind: str, reference: str, note: str = "") -> dict[str, Any]:
        version = _text(version, "version")
        kind = _text(kind, "kind")
        reference = _text(reference, "reference")

        def mutate(data: dict[str, Any]) -> dict[str, Any]:
            item = self._find(data, version)
            item["evidence"].append({
                "time": utc_now(),
                "kind": kind,
                "reference": reference,
                "note": note.strip(),
            })
            return data

        return self.store.update(mutate)

    def set_status(
        self,
        version: str,
        *,
        status: str,
        release_status: str | None = None,
        regression_status: str | None = None,
    ) -> dict[str, Any]:
        version = _text(version, "version")
        status = _text(status, "status")
        if status not in VERSION_STATUSES:
            raise VersionRegistryError(f"Unbekannter Versionsstatus: {status}")
        if release_status is None:
            release_status = next(iter(STATUS_RELEASE_COMPATIBILITY[status]))
        if release_status not in RELEASE_STATUSES:
            raise VersionRegistryError(f"Unbekannter Release-Status: {release_status}")
        _validate_status_pair(status, release_status)

        def mutate(data: dict[str, Any]) -> dict[str, Any]:
            item = self._find(data, version)
            if status in EVIDENCE_REQUIRED and not item["evidence"]:
                raise VersionRegistryError(
                    f"Status '{status}' benötigt zuerst mindestens einen Evidenznachweis."
                )
            item["status"] = status
            item["release_status"] = release_status
            if regression_status is not None:
                item["regression_status"] = _text(regression_status, "regression_status")
            return data

        return self.store.update(mutate)

    def add_known_issue(self, version: str, issue: str) -> dict[str, Any]:
        issue = _text(issue, "issue")

        def mutate(data: dict[str, Any]) -> dict[str, Any]:
            item = self._find(data, version)
            if issue not in item["known_issues"]:
                item["known_issues"].append(issue)
            return data

        return self.store.update(mutate)

    def previous_version(self) -> dict[str, Any] | None:
        data = self.load()
        current = data["current_version"]
        positions = [i for i, item in enumerate(data["versions"]) if item["version"] == current]
        if not positions or positions[0] == 0:
            return None
        return deepcopy(data["versions"][positions[0] - 1])

    def consistency(self, expected_version: str) -> dict[str, Any]:
        data = self.load()
        issues: list[str] = []
        if data["current_version"] != expected_version:
            issues.append(
                f"Registry meldet '{data['current_version']}', VERSION meldet '{expected_version}'."
            )
        if not any(item["version"] == expected_version for item in data["versions"]):
            issues.append(f"VERSION '{expected_version}' fehlt in der Registry.")
        return {"ok": not issues, "issues": issues, "current_version": data["current_version"]}

    @staticmethod
    def _find(data: dict[str, Any], version: str) -> dict[str, Any]:
        item = next((entry for entry in data["versions"] if entry["version"] == version), None)
        if item is None:
            raise VersionRegistryError(f"Version '{version}' ist nicht registriert.")
        return item

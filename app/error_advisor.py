from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import ROOT_DIR
from .text_catalog import TextCatalog

RULE_SCHEMA_VERSION = 1
DEFAULT_RULES_PATH = ROOT_DIR / "resources" / "error_rules" / "v1.json"
DEFAULT_TEXT_PATH = ROOT_DIR / "resources" / "texts" / "de" / "v1.json"


class ErrorAdvisorError(ValueError):
    """Fehler in den versionierten Regeln der Fehlerhilfe."""


def validate_rules(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict) or value.get("schema_version") != RULE_SCHEMA_VERSION:
        raise ErrorAdvisorError("Unbekanntes Fehlerregel-Schema.")
    rules_version = value.get("rules_version")
    rules = value.get("rules")
    if not isinstance(rules_version, str) or not rules_version.strip():
        raise ErrorAdvisorError("rules_version fehlt.")
    if not isinstance(rules, list) or not rules:
        raise ErrorAdvisorError("rules fehlt oder ist leer.")
    clean: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in rules:
        if not isinstance(raw, dict):
            raise ErrorAdvisorError("Fehlerregel muss ein Objekt sein.")
        rule_id = raw.get("id")
        if not isinstance(rule_id, str) or not rule_id.strip() or rule_id in seen:
            raise ErrorAdvisorError("Fehlerregel-ID fehlt oder ist doppelt.")
        seen.add(rule_id)
        match = raw.get("match", {})
        if not isinstance(match, dict):
            raise ErrorAdvisorError(f"match in {rule_id} muss ein Objekt sein.")
        exception_names = match.get("exception_names", [])
        contains_any = match.get("contains_any", [])
        if not isinstance(exception_names, list) or not all(isinstance(x, str) for x in exception_names):
            raise ErrorAdvisorError(f"exception_names in {rule_id} ist ungültig.")
        if not isinstance(contains_any, list) or not all(isinstance(x, str) for x in contains_any):
            raise ErrorAdvisorError(f"contains_any in {rule_id} ist ungültig.")
        priority = raw.get("priority", 0)
        if not isinstance(priority, int):
            raise ErrorAdvisorError(f"priority in {rule_id} muss eine Zahl sein.")
        for field in ("category", "severity", "message_key", "action_key"):
            if not isinstance(raw.get(field), str) or not raw[field].strip():
                raise ErrorAdvisorError(f"{field} fehlt in {rule_id}.")
        template_path = raw.get("template_path")
        if template_path is not None and not isinstance(template_path, str):
            raise ErrorAdvisorError(f"template_path in {rule_id} ist ungültig.")
        retry_safe = raw.get("retry_safe", False)
        if not isinstance(retry_safe, bool):
            raise ErrorAdvisorError(f"retry_safe in {rule_id} muss true/false sein.")
        clean.append({
            "id": rule_id.strip(),
            "priority": priority,
            "match": {
                "exception_names": [x.strip() for x in exception_names if x.strip()],
                "contains_any": [x.casefold().strip() for x in contains_any if x.strip()],
            },
            "category": raw["category"].strip(),
            "severity": raw["severity"].strip(),
            "message_key": raw["message_key"].strip(),
            "action_key": raw["action_key"].strip(),
            "template_path": template_path.strip() if isinstance(template_path, str) and template_path.strip() else None,
            "retry_safe": retry_safe,
        })
    clean.sort(key=lambda item: item["priority"], reverse=True)
    return {"schema_version": RULE_SCHEMA_VERSION, "rules_version": rules_version.strip(), "rules": clean}


class ErrorAdvisor:
    def __init__(self, rules_path: Path = DEFAULT_RULES_PATH, text_path: Path = DEFAULT_TEXT_PATH):
        self.rules_path = Path(rules_path)
        self.catalog = TextCatalog(Path(text_path))
        try:
            raw = json.loads(self.rules_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ErrorAdvisorError(f"Fehlerregeln '{self.rules_path}' sind nicht lesbar.") from exc
        self._rules = validate_rules(raw)
        self._validate_template_paths()

    @property
    def version(self) -> str:
        return self._rules["rules_version"]

    def _validate_template_paths(self) -> None:
        for rule in self._rules["rules"]:
            rel = rule["template_path"]
            if not rel:
                continue
            candidate = (ROOT_DIR / rel).resolve()
            try:
                candidate.relative_to(ROOT_DIR.resolve())
            except ValueError as exc:
                raise ErrorAdvisorError(f"Vorlagenpfad in {rule['id']} verlässt das Projekt.") from exc
            if not candidate.is_file():
                raise ErrorAdvisorError(f"Vorlage in {rule['id']} fehlt: {rel}")

    def advise(self, error: Exception, *, area: str = "Allgemein") -> dict[str, Any]:
        name = error.__class__.__name__
        text = str(error)
        folded = text.casefold()
        selected: dict[str, Any] | None = None
        for rule in self._rules["rules"]:
            names = rule["match"]["exception_names"]
            tokens = rule["match"]["contains_any"]
            class_match = not names or name in names
            text_match = not tokens or any(token in folded for token in tokens)
            if class_match and text_match:
                selected = rule
                break
        if selected is None:
            return {
                "rule_id": "ERR-GENERIC-001",
                "category": "unknown",
                "severity": "orange",
                "message": self.catalog.get("error.generic"),
                "action": self.catalog.get("action.generic"),
                "template_path": None,
                "retry_safe": False,
                "area": area,
            }
        return {
            "rule_id": selected["id"],
            "category": selected["category"],
            "severity": selected["severity"],
            "message": self.catalog.get(selected["message_key"]),
            "action": self.catalog.get(selected["action_key"]),
            "template_path": selected["template_path"],
            "retry_safe": selected["retry_safe"],
            "area": area,
        }

    def metadata(self) -> dict[str, object]:
        return {
            "schema_version": self._rules["schema_version"],
            "rules_version": self.version,
            "rule_count": len(self._rules["rules"]),
            "text_catalog": self.catalog.metadata(),
        }

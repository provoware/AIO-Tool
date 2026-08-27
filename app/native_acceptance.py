from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from .persistence import AtomicJsonStore

SCHEMA_VERSION = 1
RESULT_STATES = {"pending", "pass", "fail", "skip"}
ZOOM_LEVELS = (100, 125, 150, 175, 200)
BROWSERS = ("firefox", "chromium")
OBSERVED_KEYS = {"browser_guess", "user_agent", "inner_width", "inner_height", "screen_width", "screen_height", "device_pixel_ratio", "visual_scale", "target_zoom"}


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _step(step_id: str, group: str, title: str, instruction: str, expected: str, **extra: Any) -> dict[str, Any]:
    return {"id": step_id, "group": group, "title": title, "instruction": instruction, "expected": expected, **extra}


def build_steps() -> list[dict[str, Any]]:
    steps = [
        _step("KUB-01", "Kubuntu", "Desktop-Starter", "AIO-Tool über start_tool.desktop starten.", "Die Startkonsole zeigt die Checkpoints und öffnet das Dashboard."),
        _step("KUB-02", "Kubuntu", "Shell-Starter", "AIO-Tool über start_tool.sh starten.", "Der Start endet ohne Fehler-ID und das Backend ist bereit."),
        _step("KUB-03", "Kubuntu", "Passende Instanz wiederverwenden", "Das Tool ein zweites Mal starten, während dieselbe Installation bereits läuft.", "Die vorhandene passende Instanz wird erkannt und sicher wiederverwendet."),
        _step("KUB-04", "Kubuntu", "Fremd belegten Port behandeln", "Standardport testweise durch einen anderen lokalen Dienst belegen und AIO-Tool starten.", "Der fremde Dienst wird nicht übernommen; ein freier Loopback-Port wird sichtbar gewählt."),
        _step("DSP-01", "Anzeige", "Kleines Fenster", "Dashboard ungefähr auf 1024×768 CSS-Pixel verkleinern.", "Keine Kernfunktion verschwindet; kein horizontaler Zwangsscroll entsteht."),
        _step("DSP-02", "Anzeige", "Full-HD", "Dashboard auf einem Full-HD-Arbeitsbereich prüfen.", "Dashboard bleibt kompakt, lesbar und logisch gegliedert."),
        _step("DSP-03", "Anzeige", "Große Anzeige", "Dashboard auf großer Anzeige bzw. großem Fenster prüfen.", "Informationsdichte bleibt sinnvoll; Bereiche werden nicht unnötig auseinandergezogen."),
        _step("KEY-01", "Bedienung", "Nur Tastatur", "Die Hauptfunktionen ohne Maus mit Tab, Shift+Tab, Enter und Leertaste durchlaufen.", "Fokus ist sichtbar, Reihenfolge logisch und Kernaktionen sind erreichbar."),
    ]
    for browser in BROWSERS:
        for zoom in ZOOM_LEVELS:
            browser_label = "Firefox" if browser == "firefox" else "Chrome/Chromium"
            steps.append(_step(f"{browser.upper()}-{zoom}", "Browser/Zoom", f"{browser_label} · {zoom} %", f"Diese Seite in {browser_label} öffnen, Browserzoom auf {zoom} % stellen und Dashboard, Kalender, TODO, Reminder sowie Darstellung prüfen.", "Kein Überlappen/Abschneiden; Fokus und Hauptaktionen bleiben erreichbar.", browser=browser, zoom=zoom))
    return steps


STEPS = build_steps()
STEP_BY_ID = {item["id"]: item for item in STEPS}


class NativeAcceptanceError(ValueError):
    pass


def _clean_observed(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise NativeAcceptanceError("Beobachtungsdaten müssen ein Objekt sein.")
    clean: dict[str, Any] = {}
    for key in OBSERVED_KEYS:
        if key not in value:
            continue
        item = value[key]
        if item is None or isinstance(item, (bool, int, float)):
            clean[key] = item
        elif isinstance(item, str):
            clean[key] = item[:500]
        else:
            raise NativeAcceptanceError(f"Ungültiger Beobachtungswert: {key}")
    return clean


def validate_session(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict) or value.get("schema_version") != SCHEMA_VERSION:
        raise NativeAcceptanceError("Native-Acceptance-Schema ist ungültig.")
    for key in ("target_version", "session_id", "created_at", "updated_at"):
        if not isinstance(value.get(key), str) or not value[key].strip():
            raise NativeAcceptanceError(f"Pflichtfeld fehlt: {key}")
    results = value.get("results")
    if not isinstance(results, dict):
        raise NativeAcceptanceError("results muss ein Objekt sein.")
    unknown = set(results) - set(STEP_BY_ID)
    if unknown:
        raise NativeAcceptanceError("Unbekannte Prüfschritte: " + ", ".join(sorted(unknown)))
    clean_results: dict[str, Any] = {}
    for step_id, result in results.items():
        if not isinstance(result, dict):
            raise NativeAcceptanceError(f"Ergebnis {step_id} ist ungültig.")
        status = result.get("status")
        if status not in RESULT_STATES - {"pending"}:
            raise NativeAcceptanceError(f"Ungültiger Status für {step_id}: {status}")
        note = result.get("note", "")
        if not isinstance(note, str):
            raise NativeAcceptanceError("Notiz muss Text sein.")
        clean_results[step_id] = {"status": status, "recorded_at": str(result.get("recorded_at") or _now()), "note": note.strip()[:1000], "observed": _clean_observed(result.get("observed", {}))}
    return {"schema_version": SCHEMA_VERSION, "target_version": value["target_version"].strip(), "session_id": value["session_id"].strip(), "created_at": value["created_at"], "updated_at": value["updated_at"], "results": clean_results}


class NativeAcceptanceStore:
    def __init__(self, path: Path, target_version: str):
        self.path = Path(path)
        self.target_version = target_version
        self._lock = threading.RLock()
        default = self._new_session()
        self.store = AtomicJsonStore(self.path, default, validate_session)

    def _new_session(self) -> dict[str, Any]:
        now = _now()
        return {"schema_version": SCHEMA_VERSION, "target_version": self.target_version, "session_id": uuid4().hex, "created_at": now, "updated_at": now, "results": {}}

    def load(self) -> dict[str, Any]:
        with self._lock:
            data = self.store.load()
            if data["target_version"] != self.target_version:
                raise NativeAcceptanceError("Gespeicherte Abnahme gehört zu einer anderen Toolversion.")
            return data

    def start_new(self) -> dict[str, Any]:
        with self._lock:
            return self.store.save(self._new_session())

    def record(self, step_id: str, status: str, note: str = "", observed: Any = None) -> dict[str, Any]:
        if step_id not in STEP_BY_ID:
            raise NativeAcceptanceError("Unbekannter Prüfschritt.")
        if status not in {"pass", "fail", "skip"}:
            raise NativeAcceptanceError("Status muss pass, fail oder skip sein.")
        clean_observed = _clean_observed(observed)
        with self._lock:
            def mutate(data: dict[str, Any]) -> dict[str, Any]:
                data["results"][step_id] = {"status": status, "recorded_at": _now(), "note": str(note or "").strip()[:1000], "observed": clean_observed}
                data["updated_at"] = _now()
                return data
            return self.store.update(mutate)

    def report(self) -> dict[str, Any]:
        with self._lock:
            data = self.load()
            rows = []
            counts = {"pass": 0, "fail": 0, "skip": 0, "pending": 0}
            for step in STEPS:
                result = data["results"].get(step["id"])
                status = result["status"] if result else "pending"
                counts[status] += 1
                rows.append({**step, "result": result or {"status": "pending", "note": "", "observed": {}}})
            finished = counts["pass"] + counts["fail"] + counts["skip"]
            overall = "fail" if counts["fail"] else "incomplete" if counts["pending"] else "pass"
            return {"schema_version": SCHEMA_VERSION, "target_version": data["target_version"], "session_id": data["session_id"], "created_at": data["created_at"], "updated_at": data["updated_at"], "overall_status": overall, "progress_percent": round(finished * 100 / len(STEPS)), "counts": counts, "steps": rows, "statement": "L4 ist nur für explizit bestätigte Schritte belegt; offene/übersprungene Schritte bleiben offen."}

    def write_reports(self, report_dir: Path) -> tuple[Path, Path]:
        with self._lock:
            report = self.report()
            report_dir = Path(report_dir)
            report_dir.mkdir(parents=True, exist_ok=True)
            json_path = report_dir / "native-acceptance-latest.json"
            txt_path = report_dir / "native-acceptance-latest.txt"
            self._atomic_text(json_path, json.dumps(report, ensure_ascii=False, indent=2) + "\n")
            lines = [f"AIO-Tool Native Acceptance · {report['target_version']}", f"Sitzung: {report['session_id']}", f"Status: {report['overall_status'].upper()} · {report['progress_percent']} %", ""]
            for row in report["steps"]:
                result = row["result"]
                marker = {"pass": "PASS", "fail": "FAIL", "skip": "SKIP", "pending": "OFFEN"}[result["status"]]
                lines.append(f"[{marker}] {row['id']} · {row['title']}")
                if result.get("note"):
                    lines.append(f"        Notiz: {result['note']}")
            lines += ["", report["statement"]]
            self._atomic_text(txt_path, "\n".join(lines) + "\n")
            return json_path, txt_path

    @staticmethod
    def _atomic_text(path: Path, text: str) -> None:
        temp = path.with_suffix(path.suffix + ".tmp")
        with temp.open("w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)

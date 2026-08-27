#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import socket
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.autostart import _clean_stale_pid, _find_free, _normalize_port
from app.runtime_health import repair_json_state
from app.runtime_recovery import restore_runtime_assets


def _validator(value: dict) -> dict:
    if value.get("schema") != 1 or not isinstance(value.get("value"), int):
        raise ValueError("invalid")
    return value


def _case(name: str, fn) -> dict:
    try:
        detail = fn()
        return {"id": name, "status": "PASS", "detail": detail}
    except Exception as exc:
        return {"id": name, "status": "FAIL", "detail": f"{type(exc).__name__}: {exc}"}


def main() -> int:
    parser = argparse.ArgumentParser(description="AIO-Tool deterministische Failure-Matrix")
    parser.add_argument("--output", type=Path, default=Path("artifacts/failure-matrix.json"))
    args = parser.parse_args()
    cases = []

    def invalid_port():
        port, warning = _normalize_port("kaputt")
        assert port == 8765 and warning
        return warning
    cases.append(_case("FM-001-invalid-port", invalid_port))

    def occupied_port():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", 0))
        sock.listen(1)
        used = sock.getsockname()[1]
        try:
            free = _find_free(used, span=5)
            assert free != used
            return f"belegt={used}; frei={free}"
        finally:
            sock.close()
    cases.append(_case("FM-002-port-collision", occupied_port))

    def stale_pid():
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "server.pid"
            path.write_text("999999999\n", encoding="utf-8")
            note = _clean_stale_pid(path)
            assert note and not path.exists()
            return note
    cases.append(_case("FM-003-stale-pid", stale_pid))

    def corrupt_main_valid_backup():
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "state.json"
            path.write_text("{broken", encoding="utf-8")
            path.with_suffix(".json.bak").write_text('{"schema":1,"value":7}\n', encoding="utf-8")
            result = repair_json_state(path, default={"schema": 1, "value": 0}, validator=_validator, quarantine_root=root / "quarantine")
            assert result["status"] == "backup-restored"
            assert json.loads(path.read_text(encoding="utf-8"))["value"] == 7
            assert result["quarantined"]
            return result["status"]
    cases.append(_case("FM-004-corrupt-main-backup-restore", corrupt_main_valid_backup))

    def corrupt_main_and_backup():
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "state.json"
            path.write_text("{broken", encoding="utf-8")
            path.with_suffix(".json.bak").write_text("[]", encoding="utf-8")
            result = repair_json_state(path, default={"schema": 1, "value": 0}, validator=_validator, quarantine_root=root / "quarantine")
            assert result["status"] == "reset-safe"
            assert len(result["quarantined"]) == 2
            return result["status"]
    cases.append(_case("FM-005-corrupt-main-and-backup", corrupt_main_and_backup))

    def source_recovery_disabled():
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            result = restore_runtime_assets(root, root / "runtime")
            assert result == {"enabled": False, "restored": [], "quarantined": []}
            return "source checkout not mutated"
    cases.append(_case("FM-006-source-recovery-disabled", source_recovery_disabled))

    def recovery_repairs_asset():
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            runtime = root / "runtime"
            target = root / "web" / "asset.txt"
            target.parent.mkdir(parents=True)
            target.write_text("kaputt", encoding="utf-8")
            good = b"original\n"
            manifest = {"schema_version": 1, "files": [{"path": "web/asset.txt", "size": len(good), "sha256": hashlib.sha256(good).hexdigest()}]}
            with zipfile.ZipFile(root / "RECOVERY_BASIS.zip", "w") as zf:
                zf.writestr("RECOVERY_MANIFEST.json", json.dumps(manifest))
                zf.writestr("files/web/asset.txt", good)
            (root / "MANIFEST_RELEASE.json").write_text("{}\n", encoding="utf-8")
            result = restore_runtime_assets(root, runtime)
            assert result["enabled"] and result["restored"] == ["web/asset.txt"]
            assert target.read_bytes() == good and result["quarantined"]
            return "asset restored + corrupt original quarantined"
    cases.append(_case("FM-007-recovery-asset-repair", recovery_repairs_asset))

    passed = sum(case["status"] == "PASS" for case in cases)
    payload = {
        "schema_version": 1,
        "matrix": "0.6.0-autostart-selfheal",
        "total": len(cases),
        "passed": passed,
        "failed": len(cases) - passed,
        "cases": cases,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    raise SystemExit(main())

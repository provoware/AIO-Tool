#!/usr/bin/env python3
from __future__ import annotations

import argparse
import http.client
import json
import socket
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import VERSION
from app.instance_identity import UI_CONTRACT_VERSION, runtime_instance_id

EXPECTED_INSTANCE = runtime_instance_id(ROOT, VERSION)
MARKER_PATH = ROOT / "web" / ".aio-instance-id"


def ensure_marker() -> None:
    MARKER_PATH.write_text(EXPECTED_INSTANCE + "\n", encoding="utf-8")


def tcp_open(port: int, timeout: float = 0.25) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def _http_get(port: int, path: str) -> tuple[int, bytes]:
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=0.5)
    conn.request("GET", path, headers={"Host": f"127.0.0.1:{port}"})
    response = conn.getresponse()
    raw = response.read()
    status = response.status
    conn.close()
    return status, raw


def inspect(port: int) -> dict:
    if not tcp_open(port):
        return {"state": "free", "port": port, "detail": "Port ist frei."}
    try:
        status_code, raw = _http_get(port, "/api/status")
        if status_code != 200:
            return {"state": "occupied", "port": port, "detail": f"HTTP {status_code} statt AIO-Status."}
        data = json.loads(raw.decode("utf-8"))
        marker_status, marker_raw = _http_get(port, "/.aio-instance-id")
        marker = marker_raw.decode("utf-8").strip() if marker_status == 200 else ""
    except Exception as exc:
        return {"state": "occupied", "port": port, "detail": f"Port belegt, Status nicht verifizierbar: {type(exc).__name__}."}

    same = (
        data.get("version") == VERSION
        and data.get("bind") == "127.0.0.1"
        and data.get("ready") is True
        and marker == EXPECTED_INSTANCE
    )
    if same:
        return {"state": "own-ready", "port": port, "detail": f"Passende AIO-Tool-Instanz ({UI_CONTRACT_VERSION}) ist bereit."}
    return {
        "state": "occupied",
        "port": port,
        "detail": "Port ist durch eine andere, alte oder nicht verifizierbare lokale Instanz belegt.",
    }


def find_free(start: int, span: int) -> int:
    if start < 1024 or start > 65535 or span < 0:
        raise SystemExit("FEHLER: Ungültiger Portbereich.")
    end = min(65535, start + span)
    for port in range(start, end + 1):
        if not tcp_open(port):
            return port
    raise SystemExit(f"FEHLER: Kein freier Loopback-Port im Bereich {start}–{end}.")


def main() -> None:
    parser = argparse.ArgumentParser(description="AIO-Tool Launcher-Instanzprüfung")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_inspect = sub.add_parser("inspect")
    p_inspect.add_argument("--port", type=int, required=True)
    p_free = sub.add_parser("find-free")
    p_free.add_argument("--start", type=int, required=True)
    p_free.add_argument("--span", type=int, default=20)
    sub.add_parser("ensure-marker")
    args = parser.parse_args()

    if args.cmd == "inspect":
        result = inspect(args.port)
        print(result["state"])
        print(result["detail"])
    elif args.cmd == "find-free":
        print(find_free(args.start, args.span))
    else:
        ensure_marker()
        print(EXPECTED_INSTANCE)


if __name__ == "__main__":
    main()

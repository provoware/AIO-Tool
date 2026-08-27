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


def tcp_open(port: int, timeout: float = 0.25) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def inspect(port: int) -> dict:
    if not tcp_open(port):
        return {"state": "free", "port": port, "detail": "Port ist frei."}
    try:
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=0.5)
        conn.request("GET", "/api/status", headers={"Host": f"127.0.0.1:{port}"})
        response = conn.getresponse()
        raw = response.read()
        conn.close()
        if response.status != 200:
            return {"state": "occupied", "port": port, "detail": f"HTTP {response.status} statt AIO-Status."}
        data = json.loads(raw.decode("utf-8"))
    except Exception as exc:
        return {"state": "occupied", "port": port, "detail": f"Port belegt, Status nicht verifizierbar: {type(exc).__name__}."}

    same = (
        data.get("version") == VERSION
        and data.get("instance_id") == EXPECTED_INSTANCE
        and data.get("ui_contract_version") == UI_CONTRACT_VERSION
        and data.get("bind") == "127.0.0.1"
        and data.get("ready") is True
    )
    if same:
        return {"state": "own-ready", "port": port, "detail": "Passende AIO-Tool-Instanz ist bereit."}
    return {
        "state": "occupied",
        "port": port,
        "detail": "Port ist durch eine andere, alte oder nicht verifizierbare lokale Instanz belegt.",
    }


def find_free(start: int, span: int) -> int:
    for port in range(start, start + span + 1):
        if not tcp_open(port):
            return port
    raise SystemExit(f"FEHLER: Kein freier Loopback-Port im Bereich {start}–{start + span}.")


def main() -> None:
    parser = argparse.ArgumentParser(description="AIO-Tool Launcher-Instanzprüfung")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_inspect = sub.add_parser("inspect")
    p_inspect.add_argument("--port", type=int, required=True)
    p_free = sub.add_parser("find-free")
    p_free.add_argument("--start", type=int, required=True)
    p_free.add_argument("--span", type=int, default=20)
    args = parser.parse_args()

    if args.cmd == "inspect":
        result = inspect(args.port)
        print(result["state"])
        print(result["detail"])
    else:
        print(find_free(args.start, args.span))


if __name__ == "__main__":
    main()

from __future__ import annotations

from urllib.parse import urlparse


def allowed_host_header(host_header: str, port: int) -> bool:
    host = (host_header or "").strip().lower()
    return host in {f"127.0.0.1:{port}", f"localhost:{port}"}


def allowed_origin(origin: str | None, port: int) -> bool:
    if not origin:
        return True
    try:
        parsed = urlparse(origin)
    except ValueError:
        return False
    return parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "localhost"} and (parsed.port or 80) == port


def allowed_local_request(host_header: str, origin: str | None, port: int) -> bool:
    return allowed_host_header(host_header, port) and allowed_origin(origin, port)

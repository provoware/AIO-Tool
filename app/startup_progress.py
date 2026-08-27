from __future__ import annotations

import html
import threading
from dataclasses import dataclass, field
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any


@dataclass
class StartupSnapshot:
    version: str
    total: int = 9
    current: int = 0
    title: str = "Start wird vorbereitet"
    detail: str = ""
    state: str = "info"
    target_url: str | None = None
    browser_seen: bool = False
    entries: list[dict[str, Any]] = field(default_factory=list)


class StartupProgress:
    """Thread-safe start progress shared with the browser splash page."""
    def __init__(self, version: str, total: int = 9):
        self._lock = threading.RLock()
        self.snapshot = StartupSnapshot(version=version, total=total)

    def update(self, title: str, detail: str = "", state: str = "pass") -> None:
        with self._lock:
            self.snapshot.current = min(self.snapshot.total, self.snapshot.current + 1)
            self.snapshot.title = title
            self.snapshot.detail = detail
            self.snapshot.state = state
            self.snapshot.entries.append({"number": self.snapshot.current, "title": title, "detail": detail, "state": state})

    def set_target(self, url: str) -> None:
        with self._lock:
            self.snapshot.target_url = url

    def mark_browser_seen(self) -> None:
        with self._lock:
            self.snapshot.browser_seen = True

    def data(self) -> dict[str, Any]:
        with self._lock:
            snap = self.snapshot
            return {"version": snap.version, "total": snap.total, "current": snap.current, "percent": int(snap.current * 100 / snap.total), "title": snap.title, "detail": snap.detail, "state": snap.state, "target_url": snap.target_url, "browser_seen": snap.browser_seen, "entries": list(snap.entries)}


def _page(data: dict[str, Any]) -> bytes:
    pct = data["percent"]
    color = {"pass": "#42e58c", "warn": "#ffd166", "fail": "#ff647c", "info": "#5ed7ff"}.get(data["state"], "#5ed7ff")
    entries = "".join(f"<li class='{html.escape(item['state'])}'><b>{item['number']:02d}</b><span>{html.escape(item['title'])}</span><small>{html.escape(item['detail'])}</small></li>" for item in data["entries"]) or "<li class='info'><b>00</b><span>Initialisierung</span><small>Startroutine wird geladen.</small></li>"
    return f"""<!doctype html><html lang='de'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><meta http-equiv='refresh' content='0.45'><title>AIO-Tool startet</title><style>
:root{{color-scheme:dark;background:#08101f;color:#ecf6ff;font-family:system-ui,sans-serif}}*{{box-sizing:border-box}}body{{margin:0;min-height:100vh;display:grid;place-items:center;padding:24px;background:radial-gradient(circle at 20% 10%,#153b58 0,transparent 35%),radial-gradient(circle at 80% 80%,#40285f 0,transparent 34%),#08101f}}main{{width:min(780px,100%);background:rgba(13,25,45,.92);border:1px solid #37506d;border-radius:24px;padding:28px;box-shadow:0 30px 80px rgba(0,0,0,.45)}}.eyebrow{{letter-spacing:.16em;color:#8da9c8;font-size:.78rem}}h1{{margin:.35rem 0 .25rem;font-size:clamp(1.65rem,5vw,2.5rem)}}p{{color:#b7c9dd}}.progress{{height:18px;background:#101d31;border-radius:999px;overflow:hidden;border:1px solid #314866;margin:22px 0 8px}}.progress>i{{display:block;height:100%;width:{pct}%;background:linear-gradient(90deg,#55d7ff,{color});transition:width .25s ease}}.meta{{display:flex;justify-content:space-between;gap:12px;color:#a9bed4;font-variant-numeric:tabular-nums}}ol{{list-style:none;padding:0;margin:24px 0 0;display:grid;gap:8px}}li{{display:grid;grid-template-columns:42px 1fr;gap:2px 10px;padding:10px 12px;border-radius:12px;background:#0d1b2d;border:1px solid #253c58}}li b{{grid-row:1/3;align-self:center;color:#89a6c5}}li small{{color:#91a7bf}}li.pass{{border-color:#245940}}li.warn{{border-color:#68572a}}li.fail{{border-color:#743342}}.status{{margin-top:18px;padding:14px;border-radius:14px;background:#0b1828;border-left:4px solid {color}}}
</style></head><body><main><div class='eyebrow'>PROVOWARE · AUTONOMER START</div><h1>AIO-Tool {html.escape(data['version'])}</h1><p>Keine Eingabe nötig. Prüfung, Reparatur und Start laufen automatisch.</p><div class='progress' role='progressbar' aria-valuemin='0' aria-valuemax='100' aria-valuenow='{pct}'><i></i></div><div class='meta'><span>{data['current']}/{data['total']} Checkpoints</span><strong>{pct}%</strong></div><div class='status'><strong>{html.escape(data['title'])}</strong><br><span>{html.escape(data['detail'])}</span></div><ol>{entries}</ol></main></body></html>""".encode("utf-8")


class _Handler(BaseHTTPRequestHandler):
    progress: StartupProgress
    def log_message(self, *_args: object) -> None:
        return
    def do_GET(self) -> None:
        self.progress.mark_browser_seen()
        data = self.progress.data()
        if data["target_url"]:
            self.send_response(HTTPStatus.FOUND)
            self.send_header("Location", data["target_url"])
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            return
        body = _page(data)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def start_progress_server(progress: StartupProgress, port: int) -> ThreadingHTTPServer:
    handler = type("StartupHandler", (_Handler,), {"progress": progress})
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=server.serve_forever, name="aio-start-progress", daemon=True).start()
    return server

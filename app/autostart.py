from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import os
import shutil
import signal
import socket
import subprocess
import sys
import time
import webbrowser
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import ROOT_DIR, VERSION
from .preflight import load_runtime_manifest, run_preflight
from .runtime_health import repair_runtime_state
from .runtime_recovery import restore_runtime_assets
from .startup_progress import StartupProgress, start_progress_server
from .version_registry import validate_registry

TOTAL = 9
DEFAULT_PORT = 8765
PORT_SCAN = 50
BROWSER_WAIT_SECONDS = 2.2
HANDSHAKE_WAIT_SECONDS = 10.0
MAX_LOG_BYTES = 2 * 1024 * 1024


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _bar(current: int, total: int, width: int = 20) -> str:
    filled = int(width * current / total)
    return "█" * filled + "░" * (width - filled)


def _print_checkpoint(number: int, state: str, title: str, detail: str = "") -> None:
    icon = {"pass": "🟢", "warn": "🟡", "fail": "🔴", "info": "🔵"}.get(state, "🔵")
    percent = int(number * 100 / TOTAL)
    print(f"[{number:02d}/{TOTAL:02d}] {_bar(number, TOTAL)} {percent:3d}% {icon} {title}", flush=True)
    if detail:
        print(f"         ↳ {detail}", flush=True)


def _rotate(path: Path) -> None:
    try:
        if path.is_file() and path.stat().st_size > MAX_LOG_BYTES:
            older = path.with_suffix(path.suffix + ".1")
            older.unlink(missing_ok=True)
            path.replace(older)
    except OSError:
        pass


def _writable_directory(path: Path) -> bool:
    """Probe actual write/replace/delete behavior instead of trusting mode bits."""
    try:
        path.mkdir(parents=True, exist_ok=True)
        probe = path / f".aio-write-probe-{os.getpid()}"
        probe.write_bytes(b"probe")
        with probe.open("ab") as handle:
            handle.flush()
            os.fsync(handle.fileno())
        probe.unlink()
        return True
    except OSError:
        return False


def _installation_key(root: Path) -> str:
    origin = Path(sys.executable).resolve() if getattr(sys, "frozen", False) else root.resolve()
    return hashlib.sha256(f"{origin}\0{VERSION}".encode("utf-8")).hexdigest()[:16]


def _user_mirror_dir(root: Path) -> Path:
    state_home = Path(os.environ.get("XDG_STATE_HOME") or (Path.home() / ".local" / "state"))
    return state_home / "aio-tool" / "installations" / _installation_key(root) / "basis"


def _copy_source_basis(root: Path, target: Path) -> None:
    manifest = load_runtime_manifest(root)
    target.mkdir(parents=True, exist_ok=True)
    for rel in manifest["files"]:
        source = root / rel
        destination = target / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    for generated in ("RECOVERY_BASIS.zip", "MANIFEST_RELEASE.json"):
        source = root / generated
        if source.is_file():
            shutil.copy2(source, target / generated)


def _relaunch_from_writable_mirror(root: Path, argv: list[str]) -> None:
    """Move execution to a writable user-owned basis without modifying source."""
    target = _user_mirror_dir(root)
    if target.resolve() == root.resolve():
        raise RuntimeError("Schreibbarer Spiegelpfad entspricht dem Quellpfad.")
    if getattr(sys, "frozen", False):
        source_bundle = Path(sys.executable).resolve().parent
        shutil.copytree(source_bundle, target, dirs_exist_ok=True)
        executable = target / Path(sys.executable).name
        executable.chmod(executable.stat().st_mode | 0o111)
        env = dict(os.environ)
        env["AIO_MIRRORED_FROM"] = str(source_bundle)
        os.execve(str(executable), [str(executable), *argv], env)
    else:
        _copy_source_basis(root, target)
        env = dict(os.environ)
        env["AIO_MIRRORED_FROM"] = str(root)
        env["PYTHONPATH"] = str(target)
        os.chdir(target)
        os.execve(sys.executable, [sys.executable, "-m", "app.autostart", *argv], env)


def _normalize_port(raw: str | None) -> tuple[int, str | None]:
    if raw is None or raw == "":
        return DEFAULT_PORT, None
    try:
        port = int(raw)
    except ValueError:
        return DEFAULT_PORT, f"AIO_PORT={raw!r} ist ungültig; automatisch {DEFAULT_PORT} verwendet."
    if not 1024 <= port <= 65535:
        return DEFAULT_PORT, f"AIO_PORT={port} liegt außerhalb 1024–65535; automatisch {DEFAULT_PORT} verwendet."
    return port, None


def _tcp_open(port: int, timeout: float = 0.18) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def _find_free(start: int, span: int = PORT_SCAN) -> int:
    for port in range(max(1024, start), min(65535, start + span) + 1):
        if not _tcp_open(port):
            return port
    raise RuntimeError(f"Kein freier Loopback-Port im Bereich {start}–{min(65535, start + span)}.")


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, ValueError):
        return False
    except PermissionError:
        return True


def _clean_stale_pid(pid_file: Path) -> str | None:
    if not pid_file.exists():
        return None
    try:
        pid = int(pid_file.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        pid_file.unlink(missing_ok=True)
        return "Ungültige PID-Datei automatisch entfernt."
    if not _pid_alive(pid):
        pid_file.unlink(missing_ok=True)
        return f"Veraltete PID {pid} automatisch entfernt."
    return None


def _browser_commands(url: str) -> list[list[str]]:
    custom = os.environ.get("AIO_BROWSER_CMD_JSON")
    if custom:
        try:
            parsed = json.loads(custom)
            if isinstance(parsed, list) and parsed and all(isinstance(item, str) and item for item in parsed):
                return [[item.replace("{url}", url) for item in parsed]]
        except json.JSONDecodeError:
            pass
    candidates = [["xdg-open", url], ["gio", "open", url], ["kde-open5", url], ["kde-open", url], ["firefox", "--new-window", url], ["google-chrome", "--new-window", url], ["google-chrome-stable", "--new-window", url], ["chromium", "--new-window", url], ["chromium-browser", "--new-window", url]]
    return [cmd for cmd in candidates if shutil.which(cmd[0])]


def _start_browser_until_seen(url: str, progress: StartupProgress) -> tuple[bool, list[str]]:
    attempted: list[str] = []
    for command in _browser_commands(url):
        attempted.append(command[0])
        try:
            subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        except OSError:
            continue
        deadline = time.monotonic() + BROWSER_WAIT_SECONDS
        while time.monotonic() < deadline:
            if progress.data()["browser_seen"]:
                return True, attempted
            time.sleep(0.08)
    try:
        attempted.append("python-webbrowser")
        webbrowser.open(url, new=1, autoraise=True)
    except Exception:
        pass
    deadline = time.monotonic() + BROWSER_WAIT_SECONDS
    while time.monotonic() < deadline:
        if progress.data()["browser_seen"]:
            return True, attempted
        time.sleep(0.08)
    return False, attempted


def _server_command(port: int) -> list[str]:
    if getattr(sys, "frozen", False):
        return [sys.executable, "--serve", "--port", str(port)]
    return [sys.executable, "-m", "app.autostart", "--serve", "--port", str(port)]


def _start_backend(root: Path, port: int, backend_log: Path, pid_file: Path) -> subprocess.Popen[bytes]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(root)
    handle = backend_log.open("ab", buffering=0)
    try:
        process = subprocess.Popen(_server_command(port), cwd=root, env=env, stdin=subprocess.DEVNULL, stdout=handle, stderr=subprocess.STDOUT, start_new_session=True)
    finally:
        handle.close()
    pid_file.write_text(str(process.pid) + "\n", encoding="utf-8")
    return process


def _http_status(port: int) -> dict[str, Any] | None:
    try:
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=0.6)
        conn.request("GET", "/api/status", headers={"Host": f"127.0.0.1:{port}"})
        response = conn.getresponse()
        raw = response.read()
        conn.close()
        if response.status != 200:
            return None
        data = json.loads(raw.decode("utf-8"))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def _wait_backend(port: int, process: subprocess.Popen[bytes] | None, timeout: float = 8.0) -> dict[str, Any] | None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        status = _http_status(port)
        if status and status.get("ok") and status.get("ready") is True and status.get("version") == VERSION:
            return status
        if process is not None and process.poll() is not None:
            return None
        time.sleep(0.12)
    return None


def _new_log_contains(path: Path, offset: int, needles: tuple[str, ...]) -> bool:
    try:
        with path.open("rb") as handle:
            handle.seek(offset)
            text = handle.read().decode("utf-8", errors="replace")
    except OSError:
        return False
    return all(needle in text for needle in needles)


def _wait_dashboard_handshake(server_log: Path, offset: int, timeout: float = HANDSHAKE_WAIT_SECONDS) -> bool:
    """Require app.js plus a newer /api/status request after browser redirect."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if _new_log_contains(server_log, offset, ("GET /app.js", "GET /api/status")):
            return True
        time.sleep(0.12)
    return False


def _write_reports(runtime: Path, payload: dict[str, Any]) -> None:
    runtime.mkdir(parents=True, exist_ok=True)
    (runtime / "launcher-report.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["AIO-Tool autonome Startauswertung", "================================", f"Zeit: {payload['time']}", f"Version: {payload['version']}", f"Ergebnis: {payload['result']}", f"Port: {payload.get('port')}", f"Adresse: {payload.get('url')}", f"Browser: {', '.join(payload.get('browser_attempts', [])) or 'nicht gestartet'}", f"Reparaturen: {', '.join(payload.get('repairs', [])) or 'keine'}", f"Grund: {payload.get('reason', '')}", "", "Die Startroutine verändert keine Systempakete und löscht keine beschädigten", "Nutzerdaten. Nicht validierbare Dateien bleiben in runtime/quarantine erhalten."]
    (runtime / "launcher-report.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _serve(port: int) -> int:
    from .server import create_server
    server = create_server(port)
    try:
        server.serve_forever()
    finally:
        server.server_close()
    return 0


def run_start(*, no_browser: bool = False, preflight_only: bool = False) -> int:
    root = ROOT_DIR
    if not _writable_directory(root):
        _relaunch_from_writable_mirror(root, [arg for arg in sys.argv[1:] if arg != "--serve"])
    runtime = root / "runtime"
    runtime.mkdir(parents=True, exist_ok=True)
    console_log = runtime / "launcher-console.log"
    backend_log = runtime / "launcher-backend.log"
    server_log = runtime / "server.log"
    pid_file = runtime / "server.pid"
    for path in (console_log, backend_log, server_log):
        _rotate(path)
    progress = StartupProgress(VERSION, TOTAL)
    splash_server = start_progress_server(progress, 0)
    splash_port = int(splash_server.server_address[1])
    splash_url = f"http://127.0.0.1:{splash_port}/"
    browser_attempts: list[str] = []
    repairs: list[str] = []
    started_process: subprocess.Popen[bytes] | None = None
    app_port: int | None = None

    def cp(state: str, title: str, detail: str = "") -> None:
        progress.update(title, detail, state)
        _print_checkpoint(progress.data()["current"], state, title, detail)

    try:
        cp("pass", "Runtime-Basis verfügbar", str(root))
        if not no_browser:
            seen, browser_attempts = _start_browser_until_seen(splash_url, progress)
            if not seen:
                cp("fail", "Grafische Startansicht nicht erreichbar", "Kein lokaler grafischer Browser konnte sicher geöffnet werden.")
                raise RuntimeError("Kein erreichbarer grafischer Browser gefunden.")
            cp("pass", "Grafische Startansicht geöffnet", f"Automatisch über {browser_attempts[-1]}.")
        else:
            cp("info", "Grafische Startansicht übersprungen", "Automatisierter Headless-/Preflight-Modus.")
        stale = _clean_stale_pid(pid_file)
        if stale:
            repairs.append(stale)
        recovery = restore_runtime_assets(root, runtime)
        for rel in recovery["restored"]:
            repairs.append(f"Runtime-Datei {rel} aus RECOVERY_BASIS wiederhergestellt")
        seed = validate_registry(json.loads((root / "VERSION_REGISTRY.json").read_text(encoding="utf-8")))
        health = repair_runtime_state(runtime, seed)
        for filename in health["repaired"]:
            repairs.append(f"{filename} sicher repariert")
        cp("warn" if health["repaired"] else "pass", "Lokale Daten geprüft und repariert", f"{len(health['repaired'])} Reparatur(en), {len(health['initialized'])} Initialisierung(en).")
        run_preflight(root=root, version=VERSION)
        cp("pass", "Runtime-Vertrag geprüft", "Manifest, Sicherheit, Vorlagen und Persistenz konsistent.")
        requested, port_warning = _normalize_port(os.environ.get("AIO_PORT"))
        if port_warning:
            repairs.append(port_warning)
        from scripts.launcher_probe import ensure_marker, inspect
        ensure_marker()
        probe = inspect(requested)
        if probe["state"] == "own-ready":
            app_port = requested
            cp("pass", "Passende Instanz wiederverwendet", probe["detail"])
        else:
            app_port = requested
            if probe["state"] == "occupied":
                app_port = _find_free(requested + 1)
                repairs.append(f"Port {requested} belegt; automatisch {app_port} verwendet.")
                cp("warn", "Portkonflikt autonom gelöst", f"{requested} → {app_port}")
            else:
                cp("pass", "Sicherer lokaler Port gewählt", str(app_port))
        if preflight_only:
            cp("pass", "Backendstart im Prüflauf übersprungen", "Preflight-only.")
            cp("pass", "Browser-Handshake im Prüflauf übersprungen", "Preflight-only.")
            cp("pass", "Abschlussprüfung bestanden", "Autonome Startbasis ist konsistent.")
            cp("pass", "Prüflauf abgeschlossen", "Keine Nutzerinteraktion erforderlich.")
            _write_reports(runtime, {"time": _now(), "version": VERSION, "result": "PREFLIGHT_PASS", "port": app_port, "url": None, "browser_attempts": browser_attempts, "repairs": repairs, "reason": "preflight-only"})
            return 0
        existing = inspect(app_port)
        if existing["state"] == "own-ready":
            cp("pass", "Backend bereits bereit", existing["detail"])
        else:
            backend_log.touch(exist_ok=True)
            started_process = _start_backend(root, app_port, backend_log, pid_file)
            cp("pass", "Backendprozess gestartet", f"PID {started_process.pid}")
        status = _wait_backend(app_port, started_process)
        if not status:
            cp("fail", "Backend nicht bereit", "Start oder Selbstreparatur konnte keinen konsistenten Server herstellen.")
            raise RuntimeError("Backend-Readiness fehlgeschlagen.")
        cp("pass", "Backend verifiziert bereit", f"http://127.0.0.1:{app_port}")
        url = f"http://127.0.0.1:{app_port}/?aio_start=1"
        log_offset = server_log.stat().st_size if server_log.exists() else 0
        if no_browser:
            cp("info", "Dashboard-Handshake übersprungen", "Headless-Prüfmodus.")
        else:
            progress.set_target(url)
            if not _wait_dashboard_handshake(server_log, log_offset):
                direct_attempts: list[str] = []
                for command in _browser_commands(url):
                    direct_attempts.append(command[0])
                    try:
                        subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
                    except OSError:
                        continue
                    if _wait_dashboard_handshake(server_log, log_offset, timeout=2.0):
                        break
                browser_attempts.extend(direct_attempts)
                if not _wait_dashboard_handshake(server_log, log_offset, timeout=1.0):
                    cp("fail", "Dashboard nicht bestätigt", "Browser erreichte die Oberfläche nicht vollständig.")
                    raise RuntimeError("Browser-/Dashboard-Handshake fehlgeschlagen.")
            cp("pass", "Dashboard im Browser bestätigt", "app.js geladen und /api/status aus dem Browser erreicht.")
        final_status = _http_status(app_port)
        if not final_status or not final_status.get("ok") or final_status.get("version") != VERSION:
            cp("fail", "Abschlussprüfung fehlgeschlagen", "Backendstatus ist nach dem Start nicht konsistent.")
            raise RuntimeError("Finaler Statuscheck fehlgeschlagen.")
        cp("pass", "Abschlussprüfung bestanden", "Version, Backend und lokale Daten sind konsistent.")
        cp("pass", "AIO-Tool vollständig gestartet", "Keine Eingabe des Nutzers erforderlich.")
        _write_reports(runtime, {"time": _now(), "version": VERSION, "result": "SUCCESS", "port": app_port, "url": f"http://127.0.0.1:{app_port}", "browser_attempts": browser_attempts, "repairs": repairs, "reason": ""})
        time.sleep(0.6)
        return 0
    except Exception as exc:
        _write_reports(runtime, {"time": _now(), "version": VERSION, "result": "FAIL", "port": app_port, "url": f"http://127.0.0.1:{app_port}" if app_port else None, "browser_attempts": browser_attempts, "repairs": repairs, "reason": str(exc)})
        if started_process is not None and started_process.poll() is None:
            try:
                os.killpg(started_process.pid, signal.SIGTERM)
            except OSError:
                pass
        print(f"🔴 AUTOSTART FEHLER: {exc}", file=sys.stderr, flush=True)
        time.sleep(1.2)
        return 1
    finally:
        splash_server.shutdown()
        splash_server.server_close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AIO-Tool autonome Self-Healing-Startroutine")
    parser.add_argument("--serve", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=argparse.SUPPRESS)
    parser.add_argument("--no-browser", action="store_true", help="nur für automatisierte Headless-Prüfungen")
    parser.add_argument("--preflight-only", action="store_true", help="Runtime prüfen, aber keinen Backendprozess starten")
    args = parser.parse_args(argv)
    if args.serve:
        return _serve(args.port)
    return run_start(no_browser=args.no_browser, preflight_only=args.preflight_only)


if __name__ == "__main__":
    raise SystemExit(main())

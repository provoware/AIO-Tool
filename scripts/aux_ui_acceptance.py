#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts" / "aux-ui-acceptance"
RUNNER_PORT = 18878
SIM_PORT = 18879


def wait_ready(url: str, timeout: float = 12.0) -> None:
    deadline = time.monotonic() + timeout
    last = None
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=1.0) as response:
                if response.status == 200:
                    return
        except Exception as exc:
            last = exc
        time.sleep(0.15)
    raise RuntimeError(f"Server nicht bereit: {url} · {last}")


def start_server(script: str, port: int) -> subprocess.Popen:
    return subprocess.Popen([sys.executable, str(ROOT / "scripts" / script), "--port", str(port), "--no-open"], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)


def stop_server(process: subprocess.Popen) -> None:
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill(); process.wait(timeout=3)


def geometry_checks(page, label: str) -> list[str]:
    errors: list[str] = []
    overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    if overflow > 2:
        errors.append(f"{label}: horizontaler Overflow {overflow}px")
    for index, button in enumerate(page.locator("button").all()):
        if not button.is_visible():
            continue
        box = button.bounding_box()
        if box and box["height"] < 43.5:
            errors.append(f"{label}: Button {index} nur {box['height']:.1f}px hoch")
    return errors


def main() -> int:
    from playwright.sync_api import sync_playwright

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    runner = start_server("native_acceptance_runner.py", RUNNER_PORT)
    simulator = start_server("safe_file_simulator.py", SIM_PORT)
    report = {"schema_version": 1, "browsers": {}, "errors": []}
    try:
        wait_ready(f"http://127.0.0.1:{RUNNER_PORT}/api/session")
        wait_ready(f"http://127.0.0.1:{SIM_PORT}/api/capabilities")
        with tempfile.TemporaryDirectory() as tmp:
            temp = Path(tmp); source = temp / "source.txt"; source.write_text("safe preview", encoding="utf-8"); target = temp / "target"; target.mkdir()
            with sync_playwright() as pw:
                for browser_name in ("chromium", "firefox"):
                    browser = getattr(pw, browser_name).launch(headless=True)
                    context = browser.new_context(viewport={"width": 1280, "height": 900})
                    page = context.new_page()
                    browser_errors: list[str] = []
                    page.goto(f"http://127.0.0.1:{RUNNER_PORT}/", wait_until="networkidle")
                    if page.locator("#stepRows .row").count() != 18:
                        browser_errors.append("Native Runner zeigt nicht 18 Schritte")
                    if browser_name == "chromium":
                        page.locator('[data-result="pass"]').click()
                        page.wait_for_timeout(150)
                    else:
                        rows_text = page.locator("#stepRows").inner_text()
                        if "KUB-01" not in rows_text or "PASS" not in rows_text:
                            browser_errors.append("Firefox sieht Chromium-Sitzung KUB-01 PASS nicht")
                    page.screenshot(path=str(ARTIFACTS / f"{browser_name}-native-1280.png"), full_page=True)
                    browser_errors += geometry_checks(page, f"{browser_name}/native-1280")
                    page.set_viewport_size({"width": 360, "height": 800}); page.wait_for_timeout(100)
                    browser_errors += geometry_checks(page, f"{browser_name}/native-360")
                    page.screenshot(path=str(ARTIFACTS / f"{browser_name}-native-360.png"), full_page=True)

                    page.set_viewport_size({"width": 1280, "height": 900}); page.goto(f"http://127.0.0.1:{SIM_PORT}/", wait_until="networkidle")
                    lock_text = page.locator("#lockText").inner_text()
                    if "execution_enabled=false" not in lock_text:
                        browser_errors.append("SAFE-FILE UI zeigt Execution-Lock nicht")
                    result = page.evaluate("""async ({source,target}) => {const r=await fetch('/api/preview',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({source,target,conflict_policy:'skip'})});return await r.json();}""", {"source": str(source), "target": str(target)})
                    preview = result.get("preview", {})
                    if result.get("ok") is not True or preview.get("execution_enabled") is not False or preview.get("mutation_performed") is not False:
                        browser_errors.append("SAFE-FILE API verletzt Simulation-Lock")
                    page.screenshot(path=str(ARTIFACTS / f"{browser_name}-safe-file-1280.png"), full_page=True)
                    browser_errors += geometry_checks(page, f"{browser_name}/safe-file-1280")
                    page.set_viewport_size({"width": 360, "height": 800}); page.wait_for_timeout(100)
                    browser_errors += geometry_checks(page, f"{browser_name}/safe-file-360")
                    page.screenshot(path=str(ARTIFACTS / f"{browser_name}-safe-file-360.png"), full_page=True)
                    report["browsers"][browser_name] = {"status": "pass" if not browser_errors else "fail", "errors": browser_errors}
                    report["errors"].extend(browser_errors)
                    context.close(); browser.close()
        report["status"] = "pass" if not report["errors"] else "fail"
        (ARTIFACTS / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if report["errors"]:
            for error in report["errors"]:
                print("AUX UI FAIL:", error)
            return 1
        print("AUX UI ACCEPTANCE PASS: Chromium + Firefox · Native Runner + SAFE-FILE Simulation")
        return 0
    finally:
        stop_server(runner); stop_server(simulator)


if __name__ == "__main__":
    raise SystemExit(main())

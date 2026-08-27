#!/usr/bin/env python3
from __future__ import annotations

"""CI entry point for deterministic browser acceptance.

The production page is rendered unchanged except that CSS/JS resources are
inlined and the isolated fixture fetch layer is inserted immediately before
app.js. This guarantees that dashboard boot can never race ahead of fixtures.
"""

from pathlib import Path

import ui_acceptance as ua

ROOT = Path(__file__).resolve().parents[1]


def inline_page_with_fixture(fixture_js: str) -> str:
    html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "web" / "styles.css").read_text(encoding="utf-8")
    acceptance = (ROOT / "web" / "acceptance.css").read_text(encoding="utf-8")
    app_js = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

    html = html.replace(
        '<link rel="stylesheet" href="/styles.css?contract=dashboard-v2.2">',
        f"<style>{css}</style>",
    )
    html = html.replace(
        '<link rel="stylesheet" href="/acceptance.css?contract=dashboard-v2.2">',
        f"<style>{acceptance}</style>",
    )
    html = html.replace('<link rel="stylesheet" href="/styles.css">', f"<style>{css}</style>")
    html = html.replace('<link rel="stylesheet" href="/acceptance.css">', f"<style>{acceptance}</style>")

    boot = f"<script>{fixture_js}</script><script>{app_js}</script>"
    html = html.replace('<script src="/app.js?contract=dashboard-v2.2" defer></script>', boot)
    html = html.replace('<script src="/app.js" defer></script>', boot)
    return html


def run_browser(p, browser_name: str, contract: dict, output: Path) -> dict:
    browser = getattr(p, browser_name).launch(headless=True)
    report = {"browser": browser_name, "scenarios": []}
    try:
        for scenario in contract["scenarios"]:
            context = browser.new_context(
                viewport={"width": scenario["viewport"][0], "height": scenario["viewport"][1]},
                locale="de-DE",
                reduced_motion="reduce",
            )
            page = context.new_page()
            errors: list[str] = []
            page.on("pageerror", lambda exc: errors.append(str(exc)))

            fixture_js = ua.init_script(ua.fixtures(scenario["font_scale"]))
            page.set_content(inline_page_with_fixture(fixture_js), wait_until="load")

            ready_error = None
            try:
                page.wait_for_function(ua.READY_JS, timeout=10000)
            except Exception as exc:
                ready_error = f"Dashboard wurde nicht rechtzeitig bereit: {type(exc).__name__}"

            page.wait_for_timeout(100)
            audit = ua.audit(page, contract, scenario)
            failures = ua.failures(audit, contract)
            interactions = {"boot_ready": ready_error is None}
            if ready_error:
                failures.append(ready_error)
            else:
                try:
                    interactions.update(ua.interactions(page))
                except Exception as exc:
                    failures.append(f"Interaktionsprüfung abgebrochen: {type(exc).__name__}: {exc}")

            failures += [f"Interaktion fehlgeschlagen: {key}" for key, value in interactions.items() if not value]
            shot = output / f"{browser_name}-{scenario['id']}.png"
            page.screenshot(path=str(shot), full_page=True, animations="disabled")
            report["scenarios"].append(
                {
                    "scenario": scenario,
                    "audit": audit,
                    "interactions": interactions,
                    "errors": errors,
                    "failures": failures + ["Browserfehler: " + err for err in errors],
                    "screenshot": shot.name,
                }
            )
            context.close()
    finally:
        browser.close()
    return report


ua.run_browser = run_browser
ua.main()

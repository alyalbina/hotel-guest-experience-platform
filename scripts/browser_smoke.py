"""Exercise the real web UI and static preview; capture reproducible screenshots."""

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import httpx
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def main():
    screenshots = ROOT / "docs/screenshots"
    screenshots.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as folder:
        env = {**os.environ, "DEMO_MODE": "true", "DATABASE_PATH": str(Path(folder) / "demo.sqlite")}
        server = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "app.web:create_app",
                "--factory",
                "--host",
                "127.0.0.1",
                "--port",
                "8765",
            ],
            cwd=ROOT,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            for _ in range(100):
                try:
                    if httpx.get("http://127.0.0.1:8765/health", trust_env=False).status_code == 200:
                        break
                except httpx.TransportError:
                    pass
                time.sleep(0.1)
            else:
                raise RuntimeError("Test server did not become healthy")
            with sync_playwright() as p:
                options = {
                    "headless": True,
                    "args": ["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu", "--no-zygote"],
                }
                if os.getenv("CHROMIUM_EXECUTABLE"):
                    options["executable_path"] = os.environ["CHROMIUM_EXECUTABLE"]
                browser = p.chromium.launch(**options)
                page = browser.new_page(viewport={"width": 1440, "height": 1100})
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.goto("http://127.0.0.1:8765/")
                page.locator("#login-form button").click()
                page.wait_for_selector("#request-table tr")
                assert page.locator("#queue-count").inner_text() == "96"
                assert not page.evaluate("document.documentElement.scrollWidth > innerWidth")
                page.screenshot(path=str(screenshots / "inbox.png"), full_page=True)
                page.locator('[data-page="analytics"]').click()
                page.screenshot(path=str(screenshots / "analytics.png"), full_page=True)
                page.locator('[data-page="case"]').click()
                page.screenshot(path=str(screenshots / "case-study.png"), full_page=True)
                page.locator('[data-page="operations"]').click()
                page.select_option("#department", "engineering")
                page.wait_for_function(
                    "() => document.querySelectorAll('#request-table tr').length > 0 && [...document.querySelectorAll('#request-table tr')].every(r=>r.innerText.includes('Engineering'))"
                )
                page.locator("#clear-filters").click()
                page.wait_for_function("() => document.getElementById('queue-count').innerText==='96'")
                page.locator('[data-request="demo-1001"]').click()
                page.wait_for_selector("#detail-form")
                page.screenshot(path=str(screenshots / "request-history.png"), full_page=False)
                page.select_option("#assign-select", "3")
                page.locator("#assign-button").click()
                page.wait_for_function(
                    "() => document.getElementById('detail-content').innerText.includes('Record version 2')"
                )
                for index, state in enumerate(
                    ["acknowledged", "in_progress", "resolved", "reopened"], start=3
                ):
                    page.select_option("#next-status", state)
                    if state == "reopened":
                        page.fill("#change-note", "Fictional follow-up needed")
                    page.locator('#detail-form [type="submit"]').click()
                    page.wait_for_function(
                        f"() => document.getElementById('detail-content').innerText.includes('Record version {index}')"
                    )
                page.locator("#close-drawer").click()
                page.locator("#new-request").click()
                page.fill("#create-detail", "<img src=x onerror=alert(1)> Synthetic text only")
                page.locator('#create-form [type="submit"]').click()
                page.wait_for_selector("#detail-drawer")
                assert page.locator(".detail-description img").count() == 0
                assert "<img" in page.locator(".detail-description").inner_text()
                page.locator("#close-drawer").click()
                page.set_viewport_size({"width": 390, "height": 844})
                assert not page.evaluate("document.documentElement.scrollWidth > innerWidth")
                page.screenshot(path=str(screenshots / "mobile.png"), full_page=True)
                page.set_viewport_size({"width": 1440, "height": 1100})
                page.goto((ROOT / "OPEN_DEMO.html").as_uri())
                page.wait_for_selector("#request-table tr")
                assert page.locator("#queue-count").inner_text() == "96"
                page.locator("#new-request").click()
                page.fill("#create-detail", "Synthetic preview request")
                page.locator('#create-form [type="submit"]').click()
                page.wait_for_function("() => document.getElementById('queue-count').innerText==='97'")
                page.reload()
                page.wait_for_function("() => document.getElementById('queue-count').innerText==='96'")
                assert errors == [], errors
                browser.close()
                print(
                    json.dumps(
                        {
                            "web_workflow": "passed",
                            "browser_only_preview": "passed",
                            "mobile_overflow": False,
                            "javascript_errors": errors,
                            "screenshots": 5,
                        }
                    )
                )
        finally:
            server.terminate()
            server.wait(timeout=10)


if __name__ == "__main__":
    main()

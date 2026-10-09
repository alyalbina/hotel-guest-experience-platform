"""Validate the static case study, keyboard interactions and responsive layout."""

import functools
import json
import os
import tempfile
import threading
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs/case-study/index.html"
GALLERY = ROOT / "docs/case-study/artifacts/index.html"


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.references = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.append(attributes["id"])
        for field in ("href", "src", "data-zoom", "aria-controls"):
            if attributes.get(field):
                self.references.append((field, attributes[field]))


def check_local_references(source=PAGE):
    parser = References()
    parser.feed(source.read_text())
    assert len(parser.ids) == len(set(parser.ids)), "Duplicate HTML IDs"
    for field, value in parser.references:
        parsed = urlsplit(value)
        if parsed.scheme:
            assert parsed.scheme == "https", value
            prefix = "https://github.com/alyalbina/hotel-guest-experience-platform/blob/main/"
            if value.startswith(prefix):
                assert (ROOT / unquote(value[len(prefix) :])).is_file(), value
            continue
        if field == "aria-controls":
            assert value in parser.ids, value
        elif not parsed.path:
            assert parsed.fragment in parser.ids, value
        else:
            target = source.parent / unquote(parsed.path)
            if target.is_dir():
                target = target / "index.html"
            assert target.is_file(), value
            if parsed.fragment and target.suffix == ".html":
                target_parser = References()
                target_parser.feed(target.read_text())
                assert parsed.fragment in target_parser.ids, value
    return len(parser.references)


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def main():
    references = check_local_references() + check_local_references(GALLERY)
    handler = functools.partial(QuietHandler, directory=str(ROOT / "docs"))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_port}/case-study/"
    with tempfile.TemporaryDirectory() as temporary:
        artifacts = Path(os.getenv("CASE_STUDY_ARTIFACT_DIR", temporary))
        artifacts.mkdir(parents=True, exist_ok=True)
        try:
            with sync_playwright() as p:
                options = {
                    "headless": True,
                    "args": ["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"],
                }
                if os.getenv("CHROMIUM_EXECUTABLE"):
                    options["executable_path"] = os.environ["CHROMIUM_EXECUTABLE"]
                browser = p.chromium.launch(**options)
                page = browser.new_page(viewport={"width": 1440, "height": 1060})
                errors, failed_resources = [], []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.on(
                    "response",
                    lambda response: (
                        failed_resources.append(response.url) if response.status >= 400 else None
                    ),
                )
                page.goto(url, wait_until="networkidle")
                page.screenshot(path=str(artifacts / "desktop.png"))
                page.screenshot(path=str(artifacts / "desktop-full.png"), full_page=True)
                assert page.locator("h1").count() == 1
                assert page.locator(".hero-shot img").evaluate("e => e.naturalWidth") == 1440

                # Native decision disclosures remain independently reviewable.
                for index in [1, 2]:
                    page.locator(".tradeoff summary").nth(index).click()
                    assert page.locator(".tradeoff").nth(index).get_attribute("open") is not None
                    page.locator(".tradeoff summary").nth(index).press("Enter")
                    assert page.locator(".tradeoff").nth(index).get_attribute("open") is None

                # Decision trace, changing explanation and panel association.
                page.locator("#finding-ownership").click()
                assert "responsibility" in page.locator("#decision-title").inner_text()
                assert page.locator("#decision-panel").get_attribute("aria-labelledby") == "finding-ownership"
                page.locator("#finding-ownership").press("ArrowDown")
                assert page.locator("#finding-access").get_attribute("aria-selected") == "true"
                assert page.evaluate("document.activeElement.id") == "finding-access"
                page.locator("#finding-access").press("Home")
                assert page.locator("#finding-context").get_attribute("aria-selected") == "true"

                for key in ("blueprint", "process", "system", "journey"):
                    page.locator(f"#artifact-{key}").click()
                    assert page.locator(f"#panel-{key}").is_visible()
                page.locator("#scenario-guest").click()
                assert page.locator("#panel-guest").is_visible()
                assert "/requests" in page.locator("#panel-guest").inner_text()
                page.locator("#scenario-staff").click()
                assert page.locator("#panel-staff").is_visible()
                for key in ("resolution", "sla", "completion", "reopen", "csat", "response"):
                    page.locator(f"#metric-{key}").click()
                    assert page.locator("#metric-panel").get_attribute("aria-labelledby") == f"metric-{key}"
                page.locator("#metric-response").press("End")
                assert page.locator("#metric-csat").get_attribute("aria-selected") == "true"
                page.locator(".historical-metrics").locator("..").locator("summary").click()
                assert page.locator(".historical-metrics").is_visible()
                assert "3.02" in page.locator(".historical-metrics").inner_text()

                # Native dialog retains focus and returns it to the trigger.
                trigger = page.locator(".hero-shot")
                trigger.click()
                assert page.locator("#image-dialog").is_visible()
                page.keyboard.press("Tab")
                assert page.evaluate("document.activeElement.closest('dialog') !== null")
                page.keyboard.press("Escape")
                assert not page.locator("#image-dialog").is_visible()
                assert trigger.evaluate("e => e === document.activeElement")
                for image in page.locator("[data-zoom]").all():
                    image.click()
                    assert page.locator("#expanded-image").evaluate("e => e.complete && e.naturalWidth > 0")
                    page.locator(".dialog-close").click()

                for section in (
                    "research",
                    "research-atlas",
                    "decisions",
                    "design",
                    "product",
                    "analytics",
                    "validation",
                    "contribution",
                    "next",
                ):
                    page.locator(f"#{section}").screenshot(
                        path=str(artifacts / f"{section}.png"),
                        style=".site-header,.skip-link{visibility:hidden!important}",
                    )
                # Capture the complete page after lazy model thumbnails have loaded.
                page.screenshot(path=str(artifacts / "desktop-full.png"), full_page=True)

                widths = [320, 390, 768, 1024, 1440]
                for width in widths:
                    page.set_viewport_size({"width": width, "height": 1060})
                    if page.evaluate("document.documentElement.scrollWidth > innerWidth"):
                        page.screenshot(path=str(artifacts / "overflow.png"), full_page=True)
                        oversized = page.evaluate("""() => [...document.querySelectorAll('body *')]
                            .filter(e => e.getBoundingClientRect().right > innerWidth + 1)
                            .map(e => ({tag:e.tagName, id:e.id, cls:e.className,
                                right:Math.round(e.getBoundingClientRect().right)}))""")
                        raise AssertionError((width, oversized))
                    for key in ("blueprint", "process", "system", "journey"):
                        page.locator(f"#artifact-{key}").click()
                        assert not page.evaluate("document.documentElement.scrollWidth > innerWidth"), (
                            width,
                            key,
                        )
                    page.locator("#scenario-guest").click()
                    assert not page.evaluate("document.documentElement.scrollWidth > innerWidth"), width
                    page.locator("#scenario-staff").click()
                page.set_viewport_size({"width": 390, "height": 1060})
                page.locator(".menu-toggle").click()
                assert page.locator(".menu-toggle").get_attribute("aria-expanded") == "true"
                page.keyboard.press("Escape")
                assert page.locator(".menu-toggle").get_attribute("aria-expanded") == "false"
                page.locator(".menu-toggle").click()
                page.locator('#page-nav a[href="#research"]').click()
                assert page.locator(".menu-toggle").get_attribute("aria-expanded") == "false"
                page.emulate_media(reduced_motion="reduce")
                assert page.evaluate("getComputedStyle(document.documentElement).scrollBehavior") == "auto"
                page.goto(url, wait_until="networkidle")
                page.screenshot(path=str(artifacts / "mobile.png"))
                page.screenshot(path=str(artifacts / "mobile-full.png"), full_page=True)

                # Atlas filters and all diagrams, keyboard return and mobile containment.
                page.locator('.research-atlas-teaser a[href="artifacts/"]').click()
                assert page.locator(".artifact").count() == 16
                assert page.locator(".diagram-preview svg").count() == 16
                for group, amount in (("research", 4), ("business", 4), ("system", 8), ("all", 16)):
                    page.locator(f'[data-filter="{group}"]').click()
                    assert page.locator(".artifact:visible").count() == amount
                    assert page.locator("#artifact-count").inner_text() == f"{amount} artifacts shown"
                page.locator('[data-filter="research"]').focus()
                page.keyboard.press("Enter")
                assert page.locator(".artifact:visible").count() == 4
                page.locator('[data-filter="all"]').click()
                for button in page.locator("[data-diagram]").all():
                    title = button.locator("..").locator("h2").inner_text()
                    button.click()
                    assert page.locator("#diagram-dialog").is_visible()
                    assert page.locator("#diagram-title").inner_text() == title
                    ids = page.locator("[id]").evaluate_all("els => els.map(e => e.id)")
                    assert len(ids) == len(set(ids)), "Duplicated SVG marker IDs in dialog"
                    page.keyboard.press("Tab")
                    assert page.evaluate("document.activeElement.closest('dialog') !== null")
                    page.keyboard.press("Escape")
                    assert button.evaluate("e => e === document.activeElement")
                clipped = page.locator(".diagram-preview svg").evaluate_all("""svgs => svgs.flatMap(svg => {
                    const b = svg.viewBox.baseVal;
                    return [...svg.querySelectorAll('text')].filter(t => {
                        const r = t.getBBox();
                        return r.x < -1 || r.x+r.width > b.width+1 || r.y+r.height > b.height+1;
                    }).map(t => t.textContent);
                })""")
                assert clipped == [], ("Text outside diagram viewBox", clipped)
                for width in widths:
                    page.set_viewport_size({"width": width, "height": 1060})
                    assert not page.evaluate("document.documentElement.scrollWidth > innerWidth"), (
                        "atlas",
                        width,
                    )
                    page.locator('[data-diagram="journey"]').click()
                    assert not page.evaluate("document.documentElement.scrollWidth > innerWidth"), (
                        "atlas dialog",
                        width,
                    )
                    assert page.locator("#diagram-canvas").evaluate("e => e.scrollWidth > e.clientWidth") == (
                        width < 1190
                    )
                    page.keyboard.press("Escape")
                page.set_viewport_size({"width": 1440, "height": 1060})
                page.goto(url + "artifacts/", wait_until="networkidle")
                page.screenshot(path=str(artifacts / "atlas-desktop.png"))
                page.screenshot(path=str(artifacts / "atlas-full.png"), full_page=True)
                page.locator('[data-diagram="fishbone"]').click()
                page.screenshot(path=str(artifacts / "atlas-fishbone.png"))
                page.keyboard.press("Escape")
                page.set_viewport_size({"width": 390, "height": 1060})
                page.goto(url + "artifacts/", wait_until="networkidle")
                page.screenshot(path=str(artifacts / "atlas-mobile.png"))
                page.locator('[data-filter="system"]').click()
                page.goto(url + "artifacts/#affinity", wait_until="networkidle")
                assert page.locator("#affinity").is_visible()
                page.goto(url, wait_until="networkidle")

                # Existing preview remains reachable with its own relative assets.
                page.locator(".hero-actions a").first.click()
                page.wait_for_selector("#request-table tr")
                assert page.locator("#queue-count").inner_text() == "96"
                assert page.locator("#guided-demo").is_visible()
                assert page.evaluate("demoRows.length") == 96
                page.locator("#guide-next").click()
                assert page.evaluate("demoRows.length") == 97
                assert page.locator("#queue-count").inner_text() == "1"
                assert page.evaluate("demoRows.find(r => r.id === 'tour-001').status") == "new"
                page.locator("#guide-next").click()
                guided = page.evaluate("demoRows.find(r => r.id === 'tour-001')")
                assert guided["assigned_to"] is not None
                assert guided["responded_at"] is None, "Assignment must not count as response"
                page.locator("#guide-history").click()
                assert "Employee ID" in page.locator("#detail-content").inner_text()
                page.locator("#close-drawer").click()
                for expected in ["acknowledged", "in_progress", "resolved"]:
                    page.locator("#guide-next").click()
                    assert page.evaluate("demoRows.find(r => r.id === 'tour-001').status") == expected
                guided = page.evaluate("demoRows.find(r => r.id === 'tour-001')")
                assert guided["responded_at"] == "2026-10-08T17:42:00Z"
                assert guided["resolved_at"] == "2026-10-08T17:52:00Z"
                assert len(guided["events"]) == 5
                assert guided["csat"] is None
                page.locator("#guide-next").click()
                assert page.locator("#analytics-page").is_visible()
                assert "96 → 97" in page.locator(".guide-comparison").inner_text()
                assert page.evaluate("metrics.resolved_requests") == 69
                assert page.evaluate("metrics.completion_rate") == 71.1
                page.screenshot(path=str(artifacts / "guided-analytics.png"), full_page=True)
                for width in widths:
                    page.set_viewport_size({"width": width, "height": 1060})
                    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), width
                page.locator("#guide-reset").click()
                assert page.evaluate("demoRows.length") == 96
                assert page.locator("#queue-count").inner_text() == "96"
                page.goto(url.replace("case-study/", "demo/"), wait_until="networkidle")
                assert page.locator("#guided-demo").is_hidden()
                assert page.locator("#guide-launch").is_visible()
                assert errors == [], errors
                assert failed_resources == [], failed_resources
                browser.close()
            result = {
                "local_references": references,
                "responsive_widths": widths,
                "document_overflow": False,
                "interactive_decisions_artifacts_metrics": "passed",
                "keyboard_tabs_menu_dialog_focus": "passed",
                "reduced_motion": "passed",
                "existing_demo": "passed",
                "guided_request_assignment_response_resolution_metrics_reset": "passed",
                "atlas_filters_16_diagrams_zoom_focus": "passed",
                "javascript_errors": errors,
                "failed_resources": failed_resources,
                "automated_accessibility_audit": "not performed",
            }
            (artifacts / "result.json").write_text(json.dumps(result, indent=2) + "\n")
            print(json.dumps(result))
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    main()

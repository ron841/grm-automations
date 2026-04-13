"""Primitive 3: HTTP metadata via browser navigation."""

import json
import sys
import time
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

from . import config


def run(url):
    """
    Navigate to *url* in headless Chromium, capturing redirect chain,
    TTFB, total time, final status, and response headers.

    On 429 or 503: outputs error JSON and exits with code 2.
    """
    host = urlparse(url).hostname or ""
    config.enforce_delay(host)

    redirects = []
    final_status = None
    final_headers = {}
    ttfb_ms = None

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent=config.USER_AGENT,
        )
        page = ctx.new_page()

        def on_response(response):
            nonlocal final_status, final_headers, ttfb_ms
            if ttfb_ms is None:
                ttfb_ms = (time.time() - t0) * 1000
            status = response.status
            resp_url = response.url
            if status in (301, 302, 303, 307, 308):
                redirects.append({"status": status, "url": resp_url})
            final_status = status
            final_headers = dict(response.headers)

        page.on("response", on_response)

        t0 = time.time()
        try:
            page.goto(url, timeout=config.NAV_TIMEOUT_MS, wait_until="networkidle")
        except Exception as exc:
            browser.close()
            print(json.dumps({"error": str(exc), "url": url}))
            sys.exit(1)

        total_ms = (time.time() - t0) * 1000
        final_url = page.url
        browser.close()

    if ttfb_ms is None:
        ttfb_ms = total_ms

    # Hard-exit on 429 or 503
    if final_status in (429, 503):
        print(json.dumps({
            "error": "rate_limited",
            "status": final_status,
            "url": url,
        }))
        sys.exit(2)

    return {
        "status": final_status,
        "final_url": final_url,
        "redirects": redirects,
        "ttfb_ms": round(ttfb_ms, 1),
        "total_ms": round(total_ms, 1),
        "headers": final_headers,
    }

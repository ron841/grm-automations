"""Primitive 1: Screenshot a URL via Playwright Chromium."""

import json
import sys
from datetime import datetime, timezone
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

from . import config


def run(url, viewport="375x812", full_page=True, out=None):
    """
    Render *url* in headless Chromium and save a screenshot.

    Returns a dict with path, viewport, bytes, and timestamp.
    """
    w, h = (int(x) for x in viewport.split("x"))
    host = urlparse(url).hostname or ""

    if out is None:
        config.ensure_cache_dir()
        out = str(config.cache_path(url, viewport, ".png"))

    config.enforce_delay(host)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": w, "height": h},
            user_agent=config.USER_AGENT,
        )
        page = ctx.new_page()
        page.goto(url, timeout=config.NAV_TIMEOUT_MS, wait_until="networkidle")
        page.screenshot(path=out, full_page=full_page)
        browser.close()

    size = len(open(out, "rb").read())

    return {
        "path": out,
        "viewport": viewport,
        "bytes": size,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

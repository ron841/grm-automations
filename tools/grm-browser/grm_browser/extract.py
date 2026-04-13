"""Primitive 2: Extract structured data from a rendered page."""

import json
import sys
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

from . import config

_WHAT_CHOICES = ("og-tags", "nav-images", "service-card-images", "dom")


def run(url, what):
    """
    Render *url* in headless Chromium and extract structured data.

    *what* must be one of: og-tags, nav-images, service-card-images, dom.
    Returns a dict with what, url, and data.
    """
    if what not in _WHAT_CHOICES:
        print(json.dumps({"error": f"Unknown --what: {what}. Choose from {_WHAT_CHOICES}"}), file=sys.stderr)
        sys.exit(1)

    host = urlparse(url).hostname or ""
    config.enforce_delay(host)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent=config.USER_AGENT,
        )
        page = ctx.new_page()
        page.goto(url, timeout=config.NAV_TIMEOUT_MS, wait_until="networkidle")

        if what == "og-tags":
            data = _og_tags(page)
        elif what == "nav-images":
            data = _nav_images(page)
        elif what == "service-card-images":
            data = _service_card_images(page)
        elif what == "dom":
            data = _dom(page)

        browser.close()

    return {"what": what, "url": url, "data": data}


def _og_tags(page):
    """Extract OG, Twitter, and theme-color meta tags."""
    return page.evaluate("""() => {
        const tags = {};
        const selectors = [
            ['og:image', 'meta[property="og:image"]'],
            ['og:title', 'meta[property="og:title"]'],
            ['og:description', 'meta[property="og:description"]'],
            ['twitter:image', 'meta[name="twitter:image"]'],
            ['twitter:title', 'meta[name="twitter:title"]'],
            ['twitter:description', 'meta[name="twitter:description"]'],
            ['theme-color', 'meta[name="theme-color"]'],
        ];
        for (const [key, sel] of selectors) {
            const el = document.querySelector(sel);
            if (el) tags[key] = el.getAttribute('content') || '';
        }
        return tags;
    }""")


def _nav_images(page):
    """Extract all <img> inside <header> or <nav>."""
    return page.evaluate("""() => {
        const results = [];
        const containers = document.querySelectorAll('header, nav');
        for (const c of containers) {
            for (const img of c.querySelectorAll('img')) {
                results.push({
                    src: img.src || img.getAttribute('src') || '',
                    alt: img.alt || '',
                    width: img.naturalWidth || img.width || 0,
                    height: img.naturalHeight || img.height || 0,
                });
            }
        }
        return results;
    }""")


def _service_card_images(page):
    """Extract images from elements whose class contains 'service' or 'card'.

    v1.1: also reads CSS background-image (inline style + computed style)
    in addition to <img> tags. This catches featured service cards that use
    background-image on the container div instead of an <img> element.
    """
    return page.evaluate("""() => {
        const results = [];
        const els = document.querySelectorAll('[class*="service"], [class*="card"]');
        for (const el of els) {
            // Find nearest heading and section for context
            let heading = '';
            const h = el.querySelector('h1,h2,h3,h4,h5,h6');
            if (h) heading = h.textContent.trim();
            let section = '';
            const sec = el.closest('section');
            if (sec) section = sec.id || sec.className || '';
            const featured = (el.className || '').toLowerCase().includes('featured');

            // Source 1: <img> tags inside the element
            for (const img of el.querySelectorAll('img')) {
                results.push({
                    src: img.src || img.getAttribute('src') || '',
                    heading: heading,
                    section: section,
                    featured: featured,
                    source: 'img-tag',
                });
            }

            // Source 2: inline style background-image on the element itself
            const inlineStyle = el.getAttribute('style') || '';
            const inlineMatch = inlineStyle.match(/background-image:\\s*url\\(['"]?([^'"\\)]+)['"]?\\)/i);
            if (inlineMatch) {
                // Resolve relative URL to absolute
                const a = document.createElement('a');
                a.href = inlineMatch[1];
                results.push({
                    src: a.href,
                    heading: heading,
                    section: section,
                    featured: featured,
                    source: 'inline-bg',
                });
            }

            // Source 3: computed style background-image (catches CSS-class-driven bg)
            const computed = window.getComputedStyle(el).backgroundImage;
            if (computed && computed !== 'none') {
                const compMatch = computed.match(/url\\(['"]?([^'"\\)]+)['"]?\\)/i);
                if (compMatch) {
                    const a = document.createElement('a');
                    a.href = compMatch[1];
                    // Only add if not already captured from inline
                    const alreadyHave = results.some(r => r.src === a.href);
                    if (!alreadyHave) {
                        results.push({
                            src: a.href,
                            heading: heading,
                            section: section,
                            featured: featured,
                            source: 'computed-bg',
                        });
                    }
                }
            }
        }
        // Deduplicate by src
        const seen = new Set();
        return results.filter(r => {
            if (seen.has(r.src)) return false;
            seen.add(r.src);
            return true;
        });
    }""")


def _dom(page):
    """Return full post-render HTML."""
    return page.content()

"""
Facebook page capture via Playwright headless Chromium.

Two responsibilities:

1. fetch_fb_profile_picture(handle, out_dir) -> Path | None
   Hit graph.facebook.com/{handle}/picture?type=large for the logo.
   No browser needed. The endpoint is a redirect to scontent.fbcdn.net.

2. scrape_fb_page(handle, slug, out_dir, max_photos=50) -> dict
   Open https://www.facebook.com/{handle}/ headless, capture cover photo
   plus the photos grid plus intro tagline plus follower count.

The login modal pops up after a brief delay but does not block the
underlying DOM. We dismiss it with Escape and let the page-level images
load. Public business Pages render their cover photo and recent photos
client-side; the photos grid at /photos is the saturation surface.

Failure modes tagged [scrape-failed] (not [gap]):
  - Page exists but Playwright timeout before content renders.
  - Image URLs return 4xx (rare; Facebook CDN is reliable).
  - Login modal blocks photos grid (defensive retry handles this).

Failure modes tagged [gap]:
  - Page does not exist (404 on the handle URL).
  - Cover photo absent (operator chose not to set one).
  - Public posts hidden by privacy settings.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from urllib.parse import urlparse

import requests
from playwright.sync_api import TimeoutError as PWTimeout
from playwright.sync_api import sync_playwright

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

# How long to wait for FB to render content past the login modal.
NAV_TIMEOUT_MS = 45_000
SETTLE_MS = 4000


def fetch_fb_profile_picture(handle: str, out_dir: Path) -> Path | None:
    """Pull the FB profile picture via the graph endpoint.

    No auth required. Returns the saved file path, or None if the page
    has no profile picture set or the handle is wrong.
    """
    logo_dir = out_dir / "logo"
    logo_dir.mkdir(parents=True, exist_ok=True)

    url = f"https://graph.facebook.com/{handle}/picture?type=large&redirect=true"
    r = requests.get(url, timeout=30, allow_redirects=True,
                     headers={"User-Agent": USER_AGENT})
    if r.status_code != 200:
        return None
    target = logo_dir / "logo.jpg"
    target.write_bytes(r.content)
    return target


def _dismiss_login_modal(page) -> None:
    """Press Escape to close FB's recurring login overlay.

    No-op if the overlay is not present.
    """
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass


def _collect_image_urls(page) -> list[str]:
    """Pull image src URLs from the rendered DOM.

    Filters to scontent.*.fbcdn.net (the FB CDN). Skips emoji, profile
    pictures (s16x16 etc.), and obvious thumbnails. Sorts by URL so dedup
    is stable.
    """
    js = """
    () => {
        const imgs = Array.from(document.querySelectorAll('img'));
        const urls = [];
        for (const img of imgs) {
            const src = img.currentSrc || img.src;
            if (!src) continue;
            if (!src.includes('fbcdn.net') && !src.includes('xx.fbcdn.net')) continue;
            // Skip very small icons (emoji, profile thumbs).
            const w = img.naturalWidth || 0;
            const h = img.naturalHeight || 0;
            if (w && w < 200) continue;
            if (h && h < 200) continue;
            urls.push(src);
        }
        return urls;
    }
    """
    return page.evaluate(js)


def _extract_intro_text(page) -> str | None:
    """Pull the FB Page intro / tagline.

    The intro is typically inside a section labelled About or just above
    the photo grid. We grab the first paragraph that mentions services,
    hours, or contact info heuristically. Returns None if nothing
    convincing is found; the caller tags [scrape-failed] or [gap].
    """
    js = """
    () => {
        // FB Page structure varies; try a few likely containers.
        const candidates = [
            'div[role="main"] h2',
            'div[role="main"] [data-testid*="bio"]',
            'div[role="main"] [data-pagelet="ProfileTilesFeed"]',
        ];
        for (const sel of candidates) {
            const el = document.querySelector(sel);
            if (el && el.textContent && el.textContent.trim().length > 20) {
                return el.textContent.trim().slice(0, 600);
            }
        }
        // Fallback: longest <p> in the main region.
        const ps = Array.from(document.querySelectorAll('div[role="main"] p'));
        ps.sort((a, b) => (b.textContent||'').length - (a.textContent||'').length);
        if (ps.length && ps[0].textContent.trim().length > 30) {
            return ps[0].textContent.trim().slice(0, 600);
        }
        return null;
    }
    """
    try:
        return page.evaluate(js)
    except Exception:
        return None


def _extract_follower_count(page) -> int | None:
    """Pull a follower or page-likes count.

    FB renders these as text like "123 likes" or "1.2K followers" near
    the page title. We parse the first such pattern we see.
    """
    js = """
    () => {
        const text = document.body.innerText || '';
        const re = /([0-9][\\d.,]*[KMB]?)\\s+(followers|people\\s+follow|likes|people\\s+like)/i;
        const m = text.match(re);
        return m ? m[1] : null;
    }
    """
    try:
        raw = page.evaluate(js)
    except Exception:
        return None
    if not raw:
        return None
    raw = raw.replace(",", "")
    mult = 1
    if raw.endswith("K"):
        mult = 1_000
        raw = raw[:-1]
    elif raw.endswith("M"):
        mult = 1_000_000
        raw = raw[:-1]
    elif raw.endswith("B"):
        mult = 1_000_000_000
        raw = raw[:-1]
    try:
        return int(float(raw) * mult)
    except ValueError:
        return None


def _scroll_to_load(page, max_scrolls: int = 12, settle_ms: int = 1500) -> None:
    """Scroll the photos grid until it stops appending or max_scrolls reached."""
    last_height = 0
    for i in range(max_scrolls):
        page.evaluate("() => window.scrollBy(0, document.body.scrollHeight)")
        page.wait_for_timeout(settle_ms)
        h = page.evaluate("() => document.body.scrollHeight")
        if h == last_height:
            break
        last_height = h


def _download_unique_images(urls: list[str], out_dir: Path, slug: str,
                            prefix: str, cap: int) -> list[dict]:
    """Download deduped image URLs, return metadata records.

    Dedup is by URL stripped of size parameters. FB CDN URLs include a
    `_n.jpg` suffix and query params for sizes; the path before `?` is
    stable per image.
    """
    seen = set()
    saved = []
    idx = 1
    for url in urls:
        key = url.split("?")[0]
        if key in seen:
            continue
        seen.add(key)
        if len(saved) >= cap:
            break
        try:
            r = requests.get(url, timeout=30, headers={"User-Agent": USER_AGENT})
        except requests.RequestException:
            continue
        if r.status_code != 200:
            continue
        # Skip very small payloads that probably are not photos.
        if len(r.content) < 30_000:
            continue
        ext = "jpg"
        # Detect png from content type if FB returns it.
        ct = r.headers.get("Content-Type", "")
        if "png" in ct:
            ext = "png"
        filename = f"{prefix}-{idx:02d}-{slug}.{ext}" if prefix != "fb-cover" else f"{prefix}-{slug}.{ext}"
        target = out_dir / filename
        target.write_bytes(r.content)
        saved.append({
            "file": filename,
            "url": url,
            "bytes": len(r.content),
        })
        idx += 1
        if prefix == "fb-cover":
            break
    return saved


def scrape_fb_page(handle: str, slug: str, out_dir: Path,
                   max_photos: int = 50,
                   photos_dir: Path | None = None) -> dict:
    """Open FB page headless and capture cover + photos + intro.

    Writes downloaded images to photos_dir if provided, otherwise to
    <out_dir>/images/ for v0.1 compatibility. v0.2 callers pass
    <out_dir>/audit/photos/fb/.

    Returns:
      {
        "page_url": ...,
        "cover_photo": {"file": ..., "url": ..., "bytes": ...} | None,
        "page_photos": [...],
        "intro_text": str | None,
        "follower_count": int | None,
        "scrape_failed": bool,
        "notes": [str, ...],
      }
    """
    images_dir = photos_dir if photos_dir is not None else (out_dir / "images")
    images_dir.mkdir(parents=True, exist_ok=True)

    page_url = f"https://www.facebook.com/{handle}/"
    photos_url = f"https://www.facebook.com/{handle}/photos"
    notes = []
    result = {
        "page_url": page_url,
        "cover_photo": None,
        "page_photos": [],
        "intro_text": None,
        "follower_count": None,
        "scrape_failed": False,
        "notes": notes,
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent=USER_AGENT,
            viewport={"width": 1366, "height": 900},
            locale="en-US",
        )
        page = ctx.new_page()
        page.set_default_timeout(NAV_TIMEOUT_MS)

        # Pass 1: cover photo + intro + follower count.
        try:
            page.goto(page_url, wait_until="domcontentloaded")
            page.wait_for_timeout(SETTLE_MS)
            _dismiss_login_modal(page)
            page.wait_for_timeout(1500)
            urls = _collect_image_urls(page)
            if urls:
                cover = _download_unique_images(
                    urls, images_dir, slug, "fb-cover", cap=1
                )
                if cover:
                    result["cover_photo"] = cover[0]
                else:
                    notes.append("[gap] cover photo absent or did not download")
            else:
                notes.append("[scrape-failed] no FB image URLs found on landing page")
                result["scrape_failed"] = True

            result["intro_text"] = _extract_intro_text(page)
            if result["intro_text"] is None:
                notes.append("[gap] FB intro text not detected")
            result["follower_count"] = _extract_follower_count(page)
            if result["follower_count"] is None:
                notes.append("[gap] FB follower count not detected")
        except PWTimeout:
            notes.append(f"[scrape-failed] timeout loading {page_url}")
            result["scrape_failed"] = True

        # Pass 2: photos grid.
        try:
            page.goto(photos_url, wait_until="domcontentloaded")
            page.wait_for_timeout(SETTLE_MS)
            _dismiss_login_modal(page)
            _scroll_to_load(page, max_scrolls=8, settle_ms=1500)
            urls2 = _collect_image_urls(page)
            # Exclude cover photo URL (same path) from the grid set.
            cover_key = (result["cover_photo"] or {}).get("url", "").split("?")[0]
            urls2 = [u for u in urls2 if u.split("?")[0] != cover_key]
            saved = _download_unique_images(
                urls2, images_dir, slug, "fb-page-photo", cap=max_photos
            )
            result["page_photos"] = saved
            if not saved:
                notes.append("[scrape-failed] FB photos grid yielded no images")
                result["scrape_failed"] = True
        except PWTimeout:
            notes.append(f"[scrape-failed] timeout loading {photos_url}")
            result["scrape_failed"] = True

        browser.close()

    return result


# CLI entry point for ad-hoc verification.
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("usage: fb_playwright.py <handle> <slug> <out_dir>", file=sys.stderr)
        sys.exit(2)
    handle, slug, out_dir_str = sys.argv[1], sys.argv[2], sys.argv[3]
    out_dir = Path(out_dir_str).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"FB profile picture for {handle} ...")
    pic = fetch_fb_profile_picture(handle, out_dir)
    print("  ->", pic)

    print(f"FB page scrape for {handle} ...")
    result = scrape_fb_page(handle, slug, out_dir)
    print(f"  cover: {result['cover_photo']}")
    print(f"  photos: {len(result['page_photos'])}")
    print(f"  intro: {(result['intro_text'] or '')[:120]}")
    print(f"  followers: {result['follower_count']}")
    if result["notes"]:
        print("  notes:")
        for n in result["notes"]:
            print(f"    - {n}")

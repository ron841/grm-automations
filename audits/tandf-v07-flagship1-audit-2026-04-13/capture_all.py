#!/usr/bin/env python3
"""
Full audit capture script for tandf-electric-v07.
Captures full-page, hero, nav-logo, footer, and bg-image screenshots
at desktop (1440) and mobile (390) widths for all pages.
Also fetches the OG image.
"""
import os, sys, json, time, re
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

BASE = "https://tandf-electric-v07.vercel.app"
PAGES = {
    "index":        "/",
    "services":     "/services.html",
    "about":        "/about.html",
    "testimonials": "/testimonials.html",
    "contact":      "/contact.html",
    "thanks":       "/thanks.html",
}
WIDTHS = {"desktop": 1440, "mobile": 390}
OUT = os.path.dirname(os.path.abspath(__file__))

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def capture_full_page(page, name, width_name, width):
    """Full-page screenshot."""
    d = os.path.join(OUT, width_name)
    ensure_dir(d)
    path = os.path.join(d, f"{name}.png")
    page.set_viewport_size({"width": width, "height": 900})
    page.wait_for_load_state("networkidle")
    time.sleep(1)
    page.screenshot(path=path, full_page=True)
    print(f"  [OK] {width_name}/{name}.png")
    return path

def capture_element(page, selector, name, width_name, width, subdir):
    """Screenshot a specific element by selector."""
    d = os.path.join(OUT, subdir)
    ensure_dir(d)
    page.set_viewport_size({"width": width, "height": 900})
    page.wait_for_load_state("networkidle")
    time.sleep(0.5)
    el = page.query_selector(selector)
    if el:
        path = os.path.join(d, f"{name}-{width_name}.png")
        el.screenshot(path=path)
        print(f"  [OK] {subdir}/{name}-{width_name}.png")
        return path
    else:
        print(f"  [MISS] {subdir}/{name}-{width_name} — selector '{selector}' not found")
        return None

def capture_hero_viewport(page, name, width_name, width):
    """Above-the-fold viewport screenshot (hero close-up)."""
    d = os.path.join(OUT, "hero")
    ensure_dir(d)
    page.set_viewport_size({"width": width, "height": 900})
    page.wait_for_load_state("networkidle")
    time.sleep(0.5)
    path = os.path.join(d, f"{name}-{width_name}.png")
    page.screenshot(path=path, full_page=False)  # viewport only = above the fold
    print(f"  [OK] hero/{name}-{width_name}.png")
    return path

def scan_bg_images(page, name, width_name, width):
    """CSS background-image scan (site-review v1.1 style)."""
    d = os.path.join(OUT, "bg-images")
    ensure_dir(d)
    page.set_viewport_size({"width": width, "height": 900})
    page.wait_for_load_state("networkidle")
    time.sleep(0.5)

    # Find all elements with background-image set via computed style
    bg_elements = page.evaluate("""() => {
        const results = [];
        const all = document.querySelectorAll('*');
        for (const el of all) {
            const style = window.getComputedStyle(el);
            const bg = style.backgroundImage;
            if (bg && bg !== 'none') {
                const tag = el.tagName.toLowerCase();
                const cls = el.className || '';
                const id = el.id || '';
                const rect = el.getBoundingClientRect();
                results.push({
                    tag: tag,
                    className: typeof cls === 'string' ? cls : cls.baseVal || '',
                    id: id,
                    bgImage: bg,
                    top: rect.top,
                    height: rect.height,
                    width: rect.width,
                    selector: el.id ? '#' + el.id :
                              (typeof cls === 'string' && cls.trim() ?
                               tag + '.' + cls.trim().split(/\\s+/).join('.') : tag)
                });
            }
        }
        return results;
    }""")

    captured = []
    for i, info in enumerate(bg_elements):
        if info['height'] < 20 or info['width'] < 20:
            continue  # skip tiny elements
        # Try to screenshot each bg-image element
        selector = None
        if info['id']:
            selector = f"#{info['id']}"
        elif info['className']:
            # Use first class
            cls = info['className'].split()[0]
            selector = f"{info['tag']}.{cls}"

        if selector:
            el = page.query_selector(selector)
            if el:
                fname = f"{name}-bg{i}-{width_name}.png"
                fpath = os.path.join(d, fname)
                try:
                    el.screenshot(path=fpath)
                    info['screenshot'] = fname
                    print(f"  [OK] bg-images/{fname}")
                except:
                    info['screenshot'] = None
                    print(f"  [SKIP] bg-images/{fname} — screenshot failed")
        captured.append(info)

    return captured

def fetch_og_image(page):
    """Extract og:image URL and download it."""
    d = os.path.join(OUT, "og")
    ensure_dir(d)
    og_url = page.evaluate("""() => {
        const el = document.querySelector('meta[property="og:image"]');
        return el ? el.getAttribute('content') : null;
    }""")
    og_title = page.evaluate("""() => {
        const el = document.querySelector('meta[property="og:title"]');
        return el ? el.getAttribute('content') : null;
    }""")
    og_desc = page.evaluate("""() => {
        const el = document.querySelector('meta[property="og:description"]');
        return el ? el.getAttribute('content') : null;
    }""")

    result = {"og_url": og_url, "og_title": og_title, "og_description": og_desc}

    if og_url:
        # Make absolute
        if not og_url.startswith("http"):
            og_url = urljoin(BASE, og_url)
        # Download via Playwright
        import urllib.request
        fpath = os.path.join(d, "og-image.png")
        try:
            urllib.request.urlretrieve(og_url, fpath)
            result['downloaded'] = fpath
            print(f"  [OK] og/og-image.png from {og_url}")
        except Exception as e:
            result['error'] = str(e)
            print(f"  [FAIL] OG image download: {e}")
    else:
        print("  [MISS] No og:image meta tag found")

    return result

def main():
    all_results = {
        "base_url": BASE,
        "pages": {},
        "bg_images": {},
        "og": None
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36 GRM-Audit/1.0"
        )
        page = context.new_page()

        for name, path in PAGES.items():
            url = BASE + path
            print(f"\n=== {name} ({url}) ===")
            page.goto(url, wait_until="networkidle", timeout=30000)

            page_results = {}
            for wname, w in WIDTHS.items():
                # Full page
                capture_full_page(page, name, wname, w)
                # Hero (above the fold)
                capture_hero_viewport(page, name, wname, w)
                # Nav logo area (text-based logo — capture full header/nav)
                capture_element(page, "header, nav, .navbar, .nav-container",
                                name, wname, w, "nav-logo")
                # Footer
                capture_element(page, "footer", name, wname, w, "footer")

            # BG image scan (desktop only for discovery, both for captures)
            for wname, w in WIDTHS.items():
                page.goto(url, wait_until="networkidle", timeout=30000)
                bg_data = scan_bg_images(page, name, wname, w)
                all_results["bg_images"][f"{name}-{wname}"] = bg_data

            all_results["pages"][name] = "captured"

        # OG image from homepage
        print(f"\n=== OG Image Fetch ===")
        page.goto(BASE, wait_until="networkidle", timeout=30000)
        all_results["og"] = fetch_og_image(page)

        browser.close()

    # Write results manifest
    manifest_path = os.path.join(OUT, "capture-manifest.json")
    with open(manifest_path, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\nManifest written to {manifest_path}")

if __name__ == "__main__":
    main()

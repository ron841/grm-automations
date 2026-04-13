#!/usr/bin/env python3
"""site-review mission — five-check verification of a deployed prospect site.

Thin wrapper over grm-browser primitives (capture, extract, probe, compare).
Does not modify any engine code.

Invocation:
    python -m grm_browser.missions.site_review <url> --out <dir> \
        [--brand-primary #hex] [--services-path /services]
"""

import argparse
import base64
import colorsys
import json
import os
import re
import sys
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image
from bs4 import BeautifulSoup

from grm_browser import capture, extract, compare


# -----------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------

def _check(check_id, severity, status, detail=""):
    return {
        "id": check_id,
        "status": status,
        "severity": severity,
        "detail": detail,
    }


def _dominant_non_neutral(image_path, n_colors=5):
    """Quantize image to n_colors, return the most-common non-neutral hex.

    Non-neutral = saturation > 0.2 and value between 0.1 and 0.9 in HSV.
    Returns (hex_string, None) or (None, reason_string).
    """
    img = Image.open(image_path).convert("RGB")
    # Resize for speed
    img = img.resize((200, 200), Image.LANCZOS)
    quantized = img.quantize(colors=n_colors, method=Image.Quantize.MEDIANCUT)
    palette = quantized.getpalette()
    histogram = quantized.histogram()

    candidates = []
    for i in range(n_colors):
        r, g, b = palette[i * 3], palette[i * 3 + 1], palette[i * 3 + 2]
        count = histogram[i]
        h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        if s > 0.2 and 0.1 < v < 0.9:
            candidates.append((count, r, g, b))

    if not candidates:
        return None, "no non-neutral color found in quantized palette"

    candidates.sort(key=lambda x: x[0], reverse=True)
    _, r, g, b = candidates[0]
    return "#{:02x}{:02x}{:02x}".format(r, g, b), None


# -----------------------------------------------------------------------
# Check 1: logo-is-image
# -----------------------------------------------------------------------

def check_logo_is_image(url):
    """Nav images check with OG/favicon fallback."""
    try:
        result = extract.run(url, "nav-images")
        images = result.get("data", [])
        if len(images) >= 1:
            return _check("logo-is-image", "soft", "pass",
                          f"{len(images)} image(s) found in nav/header")

        # Fallback: check OG image / apple-touch-icon / favicon
        og_result = extract.run(url, "og-tags")
        og_data = og_result.get("data", {})

        if og_data.get("og:image"):
            return _check("logo-is-image", "soft", "pass",
                          f"Tier-2 fallback: og:image present ({og_data['og:image'][:80]})")

        return _check("logo-is-image", "soft", "warn",
                      "nav uses text-based logo; no Tier-1 or Tier-2 image found")
    except Exception as e:
        return _check("logo-is-image", "soft", "warn", f"extraction error: {e}")


# -----------------------------------------------------------------------
# Check 2: og-image-brand-color
# -----------------------------------------------------------------------

def check_og_brand_color(url, brand_primary):
    """Verify OG image dominant color matches brand primary."""
    if not brand_primary:
        return _check("og-image-brand-color", "hard", "skip",
                      "no --brand-primary provided")

    try:
        og_result = extract.run(url, "og-tags")
        og_image_url = og_result.get("data", {}).get("og:image", "")

        if not og_image_url:
            return _check("og-image-brand-color", "hard", "fail",
                          "no og:image meta tag found")

        # Download OG image to temp file
        tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        try:
            urllib.request.urlretrieve(og_image_url, tmp.name)
        except Exception as e:
            os.unlink(tmp.name)
            return _check("og-image-brand-color", "hard", "fail",
                          f"failed to download og:image: {e}")

        dominant, reason = _dominant_non_neutral(tmp.name)
        os.unlink(tmp.name)

        if dominant is None:
            return _check("og-image-brand-color", "hard", "fail",
                          f"could not extract dominant color: {reason}")

        cmp = compare.run(dominant, brand_primary, "color")
        if cmp["similar"]:
            return _check("og-image-brand-color", "hard", "pass",
                          f"dominant={dominant}, brand={brand_primary}, "
                          f"hue_delta={cmp['hue_delta_deg']}deg")
        else:
            return _check("og-image-brand-color", "hard", "fail",
                          f"dominant={dominant}, brand={brand_primary}, "
                          f"hue_delta={cmp['hue_delta_deg']}deg (threshold 15deg)")

    except Exception as e:
        return _check("og-image-brand-color", "hard", "fail", f"error: {e}")


# -----------------------------------------------------------------------
# Check 3: featured-service-image-rotation
# -----------------------------------------------------------------------

def check_service_image_rotation(url, services_path):
    """Verify featured service card images differ between homepage and services page."""
    try:
        services_url = url.rstrip("/") + services_path
        if not services_url.endswith(".html") and not services_url.endswith("/"):
            services_url += ".html"

        home_result = extract.run(url, "service-card-images")
        svc_result = extract.run(services_url, "service-card-images")

        home_images = home_result.get("data", [])
        svc_images = svc_result.get("data", [])

        if not home_images and not svc_images:
            return _check("featured-service-image-rotation", "hard", "pass",
                          "no service card images on either page")

        # Tag each image with featured flag (v1.1: use the featured field
        # from the extractor if present, fall back to section/heading heuristic)
        def is_featured(img_entry):
            if img_entry.get("featured"):
                return True
            section = (img_entry.get("section", "") or "").lower()
            heading = (img_entry.get("heading", "") or "").lower()
            return "featured" in section or "featured" in heading

        home_featured = {img["src"] for img in home_images if is_featured(img)}
        svc_featured = {img["src"] for img in svc_images if is_featured(img)}
        home_all = {img["src"] for img in home_images}
        svc_all = {img["src"] for img in svc_images}

        # Check featured duplicates (hard fail)
        featured_dupes = (home_featured | svc_featured) & home_all & svc_all
        if featured_dupes:
            return _check("featured-service-image-rotation", "hard", "fail",
                          f"featured image(s) appear on both pages: "
                          f"{', '.join(s.split('/')[-1] for s in featured_dupes)}")

        # Check non-featured duplicates (soft warn)
        all_dupes = home_all & svc_all
        non_featured_dupes = all_dupes - featured_dupes
        if non_featured_dupes:
            return _check("featured-service-image-rotation", "soft", "warn",
                          f"{len(non_featured_dupes)} non-featured image(s) shared "
                          f"across pages (documented heuristic limitation)")

        return _check("featured-service-image-rotation", "hard", "pass",
                      f"home={len(home_images)} images, services={len(svc_images)} images, "
                      f"no featured duplicates")

    except Exception as e:
        return _check("featured-service-image-rotation", "hard", "fail", f"error: {e}")


# -----------------------------------------------------------------------
# Check 4: wow-gap-structural
# -----------------------------------------------------------------------

def check_wow_gap(url):
    """Verify five structural wow-gap elements are present in the DOM."""
    try:
        dom_result = extract.run(url, "dom")
        html = dom_result.get("data", "")
        soup = BeautifulSoup(html, "html.parser")

        missing = []

        # (a) H1 inside section or element with class matching /hero/i
        hero_els = soup.find_all(attrs={"class": re.compile(r"hero", re.I)})
        hero_sections = soup.find_all("section")
        h1_in_hero = False
        for el in hero_els + hero_sections:
            if el.find("h1"):
                h1_in_hero = True
                break
        if not h1_in_hero:
            missing.append("hero H1 (no <h1> inside a hero section)")

        # (b) Element with class matching /stat|number|count/i containing a digit
        stat_els = soup.find_all(attrs={"class": re.compile(r"stat|number|count", re.I)})
        has_stat = any(re.search(r"\d", el.get_text()) for el in stat_els)
        if not has_stat:
            missing.append("stats counter (no element with stat/number/count class containing a digit)")

        # (c) Element with class matching /testimonial|review|quote/i
        testimonial_els = soup.find_all(attrs={"class": re.compile(r"testimonial|review|quote", re.I)})
        if not testimonial_els:
            missing.append("testimonials section (no element with testimonial/review/quote class)")

        # (d) Container with class matching /service/i containing >=3 child elements
        service_containers = soup.find_all(attrs={"class": re.compile(r"service", re.I)})
        has_services = False
        for sc in service_containers:
            children = [c for c in sc.children if hasattr(c, 'name') and c.name]
            if len(children) >= 3:
                has_services = True
                break
        if not has_services:
            missing.append("services grid (no service container with >=3 children)")

        # (e) CTA — link or button with text matching call/contact/quote/free/estimate
        #     AND either tel: link or href containing /contact
        cta_pattern = re.compile(r"call|contact|quote|free|estimate", re.I)
        cta_els = soup.find_all(["a", "button"])
        has_cta = False
        for el in cta_els:
            text = el.get_text(strip=True)
            if cta_pattern.search(text):
                href = el.get("href", "")
                if href.startswith("tel:") or "contact" in href.lower():
                    has_cta = True
                    break
        if not has_cta:
            missing.append("CTA (no call/quote link with tel: or /contact href)")

        if missing:
            return _check("wow-gap-structural", "hard", "fail",
                          f"missing {len(missing)}/5: {'; '.join(missing)}")
        return _check("wow-gap-structural", "hard", "pass",
                      "all 5 structural elements present (hero H1, stats, testimonials, services, CTA)")

    except Exception as e:
        return _check("wow-gap-structural", "hard", "fail", f"error: {e}")


# -----------------------------------------------------------------------
# Check 5: mobile-render-baseline
# -----------------------------------------------------------------------

def check_mobile_render(url, out_dir):
    """Capture mobile screenshot, verify it exists and is > 10KB."""
    try:
        out_path = os.path.join(out_dir, "mobile-screenshot.png")
        result = capture.run(url, viewport="375x812", full_page=True, out=out_path)
        path = result.get("path", "")
        size = result.get("bytes", 0)

        if os.path.isfile(path) and size > 10240:
            return _check("mobile-render-baseline", "soft", "pass",
                          f"path={path}, bytes={size}"), path
        else:
            return _check("mobile-render-baseline", "soft", "warn",
                          f"screenshot issue: exists={os.path.isfile(path)}, bytes={size}"), None
    except Exception as e:
        return _check("mobile-render-baseline", "soft", "warn", f"capture error: {e}"), None


# -----------------------------------------------------------------------
# Report generation
# -----------------------------------------------------------------------

def _status_badge(status):
    return {"pass": "\u2705", "fail": "\u274c", "warn": "\u26a0\ufe0f", "skip": "\u23ed\ufe0f"}.get(status, "?")


def _overall_status(checks):
    statuses = [c["status"] for c in checks]
    if any(c["status"] == "fail" and c["severity"] == "hard" for c in checks):
        return "FAIL"
    if any(s in ("warn", "fail") for s in statuses):
        return "PASS WITH WARNINGS"
    return "PASS"


def generate_markdown(report, screenshot_path):
    """Generate the site-review.md report."""
    lines = []
    overall = _overall_status(report["checks"])
    lines.append(f"# Site Review: {report['url']}")
    lines.append("")
    lines.append(f"**Timestamp:** {report['timestamp']}")
    lines.append(f"**Brand Primary:** {report['brand_primary'] or 'not provided'}")
    lines.append(f"**Overall Status:** {overall}")
    lines.append("")
    lines.append("---")
    lines.append("")

    for c in report["checks"]:
        badge = _status_badge(c["status"])
        lines.append(f"## {badge} {c['id']}")
        lines.append("")
        lines.append(f"**Status:** {c['status'].upper()} | **Severity:** {c['severity']}")
        lines.append("")
        if c["detail"]:
            lines.append(f"{c['detail']}")
            lines.append("")
        lines.append("---")
        lines.append("")

    # Summary
    s = report["summary"]
    lines.append(f"## Summary")
    lines.append("")
    lines.append(f"Pass: {s['pass']} | Fail: {s['fail']} | Warn: {s['warn']} | Skip: {s['skip']}")
    lines.append("")

    # Mobile screenshot as base64 data URI
    if screenshot_path and os.path.isfile(screenshot_path):
        with open(screenshot_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        lines.append("## Mobile Screenshot (375x812)")
        lines.append("")
        lines.append(f"![mobile](data:image/png;base64,{b64})")
        lines.append("")

    return "\n".join(lines)


# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------

def run_review(url, out_dir, brand_primary=None, services_path="/services"):
    """Execute the five-check site review and write output files."""
    os.makedirs(out_dir, exist_ok=True)

    checks = []

    # 1. logo-is-image
    checks.append(check_logo_is_image(url))

    # 2. og-image-brand-color
    checks.append(check_og_brand_color(url, brand_primary))

    # 3. featured-service-image-rotation
    checks.append(check_service_image_rotation(url, services_path))

    # 4. wow-gap-structural
    checks.append(check_wow_gap(url))

    # 5. mobile-render-baseline
    mobile_check, screenshot_path = check_mobile_render(url, out_dir)
    checks.append(mobile_check)

    summary = {
        "pass": sum(1 for c in checks if c["status"] == "pass"),
        "fail": sum(1 for c in checks if c["status"] == "fail"),
        "warn": sum(1 for c in checks if c["status"] == "warn"),
        "skip": sum(1 for c in checks if c["status"] == "skip"),
    }

    report = {
        "url": url,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "brand_primary": brand_primary,
        "checks": checks,
        "summary": summary,
    }

    # Write JSON
    json_path = os.path.join(out_dir, "site-review.json")
    with open(json_path, "w") as f:
        json.dump(report, f, indent=2)

    # Write Markdown
    md_path = os.path.join(out_dir, "site-review.md")
    md_content = generate_markdown(report, screenshot_path)
    with open(md_path, "w") as f:
        f.write(md_content)

    return report


def main():
    parser = argparse.ArgumentParser(
        prog="site-review",
        description="Five-check verification of a deployed prospect site.",
    )
    parser.add_argument("url", help="Deployed homepage URL")
    parser.add_argument("--out", required=True, help="Output directory for report files")
    parser.add_argument("--brand-primary", default=None, help="Declared brand primary hex color")
    parser.add_argument("--services-path", default="/services", help="Services page path (default: /services)")

    args = parser.parse_args()

    try:
        report = run_review(args.url, args.out, args.brand_primary, args.services_path)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(2)

    # Print summary to stdout
    print(json.dumps(report, indent=2))

    # Exit code
    has_hard_fail = any(
        c["status"] == "fail" and c["severity"] == "hard"
        for c in report["checks"]
    )
    sys.exit(1 if has_hard_fail else 0)


if __name__ == "__main__":
    main()

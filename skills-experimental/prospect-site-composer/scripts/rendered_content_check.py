#!/usr/bin/env python3
# STATUS: Stage II (f) stub — implementation spec complete, execution filling pending.
"""P6.1 rendered-content check — initial-paint painted-pixel ratio per <section>.

Runs Playwright headless Chromium against a deployed (or local `file://`) URL,
captures initial-paint screenshots at three viewports (375 / 768 / 1440), measures
per-`<section>` painted-pixel ratio against the section's computed background
color, classifies each section (pass / soft-fail / hard-fail), and distinguishes
static-blank sections (real failures — opacity:0 with no reveal trigger) from
scroll-dependent-blank sections (not failures — reveal-on-scroll content that
fires after viewport scroll past the section).

Authority: COMPOSER_BRAIN.md §6 P6.1.
Integration: references/phase-6-integration.md.

Playwright dependency
---------------------
Reuses the grm-browser Playwright environment at
`~/grm-automations/tools/grm-browser/`. The `grm_browser` Python package is
installed editable (`pip install -e .`) with Chromium provisioned via
`playwright install chromium`. No additional Playwright install required.

Two integration paths are available:
  (a) Import from `grm_browser.capture` and reuse its Playwright session for
      screenshot + DOM extraction. Preferred — single Playwright launch per
      build, three viewport captures per launch.
  (b) Shell out to `python -m grm_browser capture ...` once per viewport. Less
      efficient (three separate Playwright launches) but lower coupling; use
      if grm-browser's internal API proves unstable across its own revisions.

The stub below assumes path (a) and documents the expected import surface.
Execution filling can downgrade to (b) if the internal API isn't reusable.

Usage
-----
    # As a module (preferred):
    python -m prospect_site_composer.scripts.rendered_content_check \\
        --url https://example.com/ \\
        [--viewports 375,768,1440] \\
        [--hard-fail-threshold 0.05] \\
        [--soft-fail-threshold 0.15] \\
        [--mobile-soft-fail-threshold 0.20]

    # Machine-readable JSON to stdout, human summary to stderr.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional

# --- Constants -----------------------------------------------------------

# Viewports per brain §6 P6.1. Heights are common device defaults matching
# iPhone SE (375x667), iPad portrait (768x1024), and desktop 16:10 (1440x900).
# Picks flagged per Stage II (f) requirement #4; alternatives are acceptable
# (e.g., 375x812 matches iPhone X, 1440x960 matches MacBook 13"). Document
# a picker override at invocation time rather than hard-coding alternatives.
VIEWPORTS = [
    {"width": 375, "height": 667},    # mobile — iPhone SE natural aspect
    {"width": 768, "height": 1024},   # tablet — iPad portrait
    {"width": 1440, "height": 900},   # desktop — 16:10 common
]

# Classification thresholds per brain §6 P6.1.
HARD_FAIL_THRESHOLD = 0.05              # < 5% painted pixels → hard fail (all viewports)
SOFT_FAIL_THRESHOLD = 0.15              # < 15% → soft fail (desktop + tablet)
MOBILE_SOFT_FAIL_THRESHOLD = 0.20       # < 20% → soft fail on mobile (stricter per §6)

# RGB distance tolerance for "pixel differs from background" classification.
# 15-30 is the reasonable band. 20 picked as default: permissive enough that
# anti-aliasing edges against solid backgrounds don't register as painted,
# strict enough that a subtly-patterned background doesn't fail the check
# by counting its own pattern as painted.
# Picker override via --bg-tolerance at invocation.
BG_PIXEL_TOLERANCE = 20

# Network idle timeout for initial-paint readiness. Stage II (f) requirement
# #2 flag: picked `load` event rather than `networkidle` because `networkidle`
# waits for fonts + late-loading tracking scripts that don't affect initial
# paint — the initial paint is what the user sees at T=0 and what this check
# classifies. `load` fires after DOMContentLoaded + sync resources; Phase 5's
# font-loading discipline uses `font-display: swap` so text is paintable
# immediately on fallback fonts while Fraunces/etc. finish loading.
PAGE_READY_EVENT = "load"  # alternatives: "domcontentloaded", "networkidle"

# Timeout for navigation + initial-paint capture per viewport. Matches
# grm-browser's 30s navigation default (README §Politeness).
NAVIGATION_TIMEOUT_MS = 30_000

# --- Data structures -----------------------------------------------------


@dataclass
class SectionResult:
    """Per-section analysis result at one viewport."""

    section_id: str                       # DOM id, or synthetic "section[N]" index
    painted_pixel_ratio: float            # 0.0 – 1.0
    classification: str                   # "pass" | "soft-fail" | "hard-fail"
    static_blank_flag: bool               # True = blank at initial paint
    scroll_dependent_flag: bool           # True = blank initially, painted after scroll
    computed_background_color: str        # CSS color string (#hex, rgb(), etc.)
    bounding_box: dict                    # {x, y, width, height} in CSS px


@dataclass
class PageLevelAggregate:
    """Page-level aggregation for one viewport."""

    hard_fail_count: int = 0
    soft_fail_count: int = 0
    total_sections: int = 0
    overall_classification: str = "pass"  # "pass" | "soft-fail-contribution" | "hard-fail"


@dataclass
class ViewportReport:
    """One viewport's full check result."""

    viewport: dict                        # {"width", "height"}
    sections: list = field(default_factory=list)
    page_level: PageLevelAggregate = field(default_factory=PageLevelAggregate)


@dataclass
class CheckReport:
    """Full P6.1 report across all viewports."""

    url: str
    viewports: list = field(default_factory=list)


# --- Classification ------------------------------------------------------


def classify_ratio(ratio: float, viewport_width: int) -> str:
    """Classify a single painted-pixel ratio against the thresholds.

    Mobile (<= 480px wide) uses the stricter soft-fail threshold per brain §6.
    """
    if ratio < HARD_FAIL_THRESHOLD:
        return "hard-fail"
    soft_threshold = (
        MOBILE_SOFT_FAIL_THRESHOLD if viewport_width <= 480 else SOFT_FAIL_THRESHOLD
    )
    if ratio < soft_threshold:
        return "soft-fail"
    return "pass"


# --- Playwright integration (stub) ---------------------------------------


def launch_browser_session():
    """Launch a headless Chromium session via grm-browser's Playwright env.

    Expected implementation:

        from playwright.sync_api import sync_playwright
        pw = sync_playwright().start()
        browser = pw.chromium.launch(headless=True)
        return pw, browser

    Reuses Playwright as installed by `~/grm-automations/tools/grm-browser/`'s
    editable install. Caller is responsible for `.close()` on both returned
    handles. See `grm_browser.capture` for the canonical single-viewport
    launch + screenshot pattern this function's implementation should mirror.
    """
    raise NotImplementedError("Stage II (f) stub — fill in execution pass")


def navigate_and_capture_initial_paint(page, url: str, viewport: dict) -> bytes:
    """Navigate to `url` at `viewport`, capture screenshot at initial paint.

    Critical requirement per Stage II (f) #2: IntersectionObserver callbacks
    MUST NOT have fired before capture. Implementation:

      1. Set viewport size before navigation (not after — scroll position
         changes during resize can trigger IntersectionObserver).
      2. Navigate with `wait_until=PAGE_READY_EVENT`.
      3. DO NOT dispatch any scroll event. DO NOT call `page.mouse.wheel()`.
         DO NOT call `page.evaluate("window.scrollTo(...)")`.
      4. Optionally assert `page.evaluate("window.pageYOffset")` == 0 as a
         defensive check. Any non-zero scroll position at capture time means
         the page auto-scrolled (e.g., fragment URL like #section2) and the
         capture is NOT a true initial paint — flag this condition and
         either fail fast or strip the fragment and retry.
      5. Capture screenshot as `page.screenshot(full_page=False)`. Viewport-
         only capture is the correct call here — full-page capture would
         force scroll-position changes for the tall-page tiles and fire
         IntersectionObserver.
      6. Return PNG bytes.

    The `load` event alone does not guarantee that animation frames have
    rendered. Implementation may need a `page.wait_for_timeout(200)` after
    `load` to let the first composite frame paint — 200ms is empirical
    headroom observed in grm-browser's smoke tests; tune at execution fill.
    """
    raise NotImplementedError("Stage II (f) stub — fill in execution pass")


def query_sections(page) -> list:
    """Query every `<section>` element on the page, return per-section metadata.

    Returns a list of dicts, one per section, with keys:
      - `section_id`: DOM id if present; otherwise synthetic `"section[N]"`
        where N is the zero-indexed document order.
      - `bounding_box`: `{x, y, width, height}` in CSS pixels at the current
        viewport. Uses `element.bounding_box()` per Playwright API.
      - `computed_background_color`: `getComputedStyle(el).backgroundColor`,
        resolved to an RGB / RGBA / #hex string via `page.evaluate()`.

    Edge cases flagged for execution fill:

      - Sections with `background-color: transparent` or `rgba(..., 0)`:
        walk up the DOM to the first ancestor with a non-transparent
        background. If none found, treat as the page body background
        (usually `--page` custom property resolved to `#faf7f2` or similar).
      - Sections with `background-image`: dominant-color sampling of the
        image via Pillow on the screenshot region is more accurate than
        trying to extract a single background color. Flag such sections
        in the result with a `backgroundImageDetected` boolean so the
        aggregator can weight them less confidently.
      - Sections nested inside other sections: Composer typically emits
        flat `<section>` siblings under `<main>` or `<body>`. If nested
        sections appear, the outer section's bounding box covers the
        inner's pixels — de-duplicate by excluding any section whose
        bounding box is fully contained within another's.
    """
    raise NotImplementedError("Stage II (f) stub — fill in execution pass")


# --- Pixel analysis ------------------------------------------------------


def compute_painted_pixel_ratio(
    screenshot_bytes: bytes,
    bounding_box: dict,
    bg_color_rgb: tuple,
    tolerance: int = BG_PIXEL_TOLERANCE,
) -> float:
    """Compute the painted-pixel ratio for one section's region.

    Extracts the section's bounding-box region from the viewport screenshot,
    iterates every pixel, counts pixels that differ from `bg_color_rgb` by
    more than `tolerance` in Euclidean RGB distance, returns the ratio of
    non-background to total pixels.

    Expected implementation (Pillow):

        from PIL import Image
        import io
        img = Image.open(io.BytesIO(screenshot_bytes))
        region = img.crop((
            bounding_box["x"],
            bounding_box["y"],
            bounding_box["x"] + bounding_box["width"],
            bounding_box["y"] + bounding_box["height"],
        ))
        pixels = region.getdata()
        total = len(pixels)
        non_bg = sum(
            1 for (r, g, b, *_) in pixels
            if ((r - bg_color_rgb[0]) ** 2
                + (g - bg_color_rgb[1]) ** 2
                + (b - bg_color_rgb[2]) ** 2) ** 0.5 > tolerance
        )
        return non_bg / total if total else 0.0

    Performance note: iterating every pixel in Python is slow for 1440×900
    screenshots (~1.3M pixels). Execution fill should use numpy + vectorized
    comparison:

        import numpy as np
        arr = np.asarray(region)[..., :3]  # drop alpha if present
        bg = np.array(bg_color_rgb)
        dist = np.linalg.norm(arr - bg, axis=-1)
        non_bg = (dist > tolerance).sum()
        total = dist.size
        return non_bg / total if total else 0.0

    numpy is already a transitive dependency via Pillow. No new install.
    """
    raise NotImplementedError("Stage II (f) stub — fill in execution pass")


def parse_css_color_to_rgb(color: str) -> tuple:
    """Parse a CSS color string into an (r, g, b) tuple.

    Handles #hex (3-digit and 6-digit), rgb(r, g, b), rgba(r, g, b, a) (drops
    alpha — treat fully-transparent as a special case upstream via the
    ancestor-walk logic in `query_sections`), and named colors (delegate to
    Pillow's `ImageColor.getrgb` which handles the CSS named set).

    Implementation:

        from PIL import ImageColor
        if color.startswith("rgba"):
            # Pillow doesn't parse rgba; strip alpha and re-parse as rgb.
            parts = color.replace("rgba", "rgb").rsplit(",", 1)[0] + ")"
            return ImageColor.getrgb(parts)
        return ImageColor.getrgb(color)
    """
    raise NotImplementedError("Stage II (f) stub — fill in execution pass")


# --- Static-blank vs scroll-dependent branch -----------------------------


def probe_scroll_reveal(page, section_result: SectionResult, url: str) -> SectionResult:
    """For a section flagged blank at initial paint, test whether reveal-on-scroll
    would paint it.

    Implementation:

      1. Scroll to the section: `page.evaluate(f"document.getElementById('{id}').scrollIntoView()")`.
         If `id` is synthetic ("section[N]"), use document order index via
         `document.querySelectorAll('section')[N].scrollIntoView()`.
      2. Wait for reveal animations to complete. IntersectionObserver-driven
         reveals typically run 300-600ms per Composer's `css-framework.md`
         Motion Restraint section. Wait 800ms as conservative headroom.
      3. Re-capture the section region (not the full page — saves time).
      4. Re-run `compute_painted_pixel_ratio` on the new region.
      5. If new ratio clears the viewport's hard-fail threshold:
         section is scroll-dependent (flag as such, downgrade from
         hard-fail/soft-fail to pass for final classification).
      6. If new ratio still below hard-fail threshold:
         section is static-blank (final classification stands — real failure).

    Returns updated SectionResult with `scroll_dependent_flag` set and
    `classification` updated per above. If `static_blank_flag` was True and
    scroll-reveal paints, both flags end True-then-False: `static_blank_flag
    = False`, `scroll_dependent_flag = True`. If scroll-reveal doesn't paint,
    `static_blank_flag = True`, `scroll_dependent_flag = False`.

    Edge case: sections that are initially blank AND scroll-dependent BUT
    whose reveal animation fails (JS error, disabled transitions, etc.) will
    flag as static-blank. This is correct behavior — the user sees a blank
    section in that case and the build should fail.
    """
    raise NotImplementedError("Stage II (f) stub — fill in execution pass")


# --- Aggregation ---------------------------------------------------------


def aggregate_viewport(section_results: list) -> PageLevelAggregate:
    """Aggregate per-section results into page-level counts + classification.

    Counts:
      - hard_fail_count: sections with classification == "hard-fail" AND
        static_blank_flag == True (scroll-dependent don't count).
      - soft_fail_count: sections with classification == "soft-fail" AND
        static_blank_flag == True. These feed P6.2's soft-fail accumulator
        per brain §6.

    Overall classification:
      - "hard-fail" if hard_fail_count > 0.
      - "soft-fail-contribution" if hard_fail_count == 0 AND soft_fail_count > 0.
        (Phase 6 aggregator decides if ≥3 soft fails across P6.1 + P6.2 =
        build-level hard fail per brain §6 pattern rule.)
      - "pass" if all sections pass.
    """
    hard_count = sum(
        1 for s in section_results
        if s.classification == "hard-fail" and s.static_blank_flag
    )
    soft_count = sum(
        1 for s in section_results
        if s.classification == "soft-fail" and s.static_blank_flag
    )
    if hard_count > 0:
        overall = "hard-fail"
    elif soft_count > 0:
        overall = "soft-fail-contribution"
    else:
        overall = "pass"
    return PageLevelAggregate(
        hard_fail_count=hard_count,
        soft_fail_count=soft_count,
        total_sections=len(section_results),
        overall_classification=overall,
    )


# --- Entry point ---------------------------------------------------------


def run_check(url: str, viewports: list = None) -> CheckReport:
    """Run the full P6.1 check at all configured viewports against `url`.

    Orchestration (execution filling):

      1. launch_browser_session() once.
      2. For each viewport:
         a. Open a new Playwright context at that viewport size.
         b. navigate_and_capture_initial_paint(page, url, viewport).
         c. query_sections(page) for per-section metadata.
         d. For each section:
              - compute_painted_pixel_ratio against computed bg color.
              - classify_ratio() → initial classification.
              - If classification != "pass", probe_scroll_reveal() to
                distinguish static-blank from scroll-dependent.
         e. aggregate_viewport() → page-level counts.
      3. Close browser session.
      4. Return CheckReport.

    Viewport defaults to `VIEWPORTS` constant. Pass a custom list to override.
    """
    raise NotImplementedError("Stage II (f) stub — fill in execution pass")


def emit_human_summary(report: CheckReport, stream=sys.stderr) -> None:
    """Write a terminal-readable summary of the check report to `stream`.

    Format (pseudo):

        P6.1 rendered-content check — <url>

        Desktop (1440×900):  8 sections, 0 hard, 1 soft, 7 pass
        Tablet  (768×1024):  8 sections, 0 hard, 2 soft, 6 pass
        Mobile  (375×667):   8 sections, 0 hard, 2 soft, 6 pass

        Soft-fail sections (contribute to P6.2 aggregator):
          [desktop] #services-grid — 0.11 ratio (scroll-dependent: no)
          [tablet]  #testimonials — 0.13 ratio (scroll-dependent: no)
          [mobile]  #testimonials — 0.14 ratio (scroll-dependent: no)

        Overall: soft-fail-contribution (3 soft fails)
    """
    raise NotImplementedError("Stage II (f) stub — fill in execution pass")


def main(argv: Optional[list] = None) -> int:
    """CLI entry point. Returns shell exit code.

    Exit codes:
      0 — all viewports pass or soft-fail-contribution (Phase 6 aggregator
          decides if build-level hard fail per soft-fail budget).
      1 — any viewport hard-fails (≥1 section with static-blank hard-fail).
      2 — execution error (Playwright launch failed, URL unreachable, etc.).
    """
    parser = argparse.ArgumentParser(
        prog="rendered_content_check",
        description="P6.1 rendered-content check per brain §6.",
    )
    parser.add_argument("--url", required=True, help="Target URL (http(s):// or file://).")
    parser.add_argument(
        "--viewports",
        default="375,768,1440",
        help="Comma-separated widths. Heights use device defaults. Default: 375,768,1440.",
    )
    parser.add_argument(
        "--hard-fail-threshold", type=float, default=HARD_FAIL_THRESHOLD,
        help=f"Hard-fail ratio threshold. Default: {HARD_FAIL_THRESHOLD}.",
    )
    parser.add_argument(
        "--soft-fail-threshold", type=float, default=SOFT_FAIL_THRESHOLD,
        help=f"Soft-fail ratio threshold (desktop + tablet). Default: {SOFT_FAIL_THRESHOLD}.",
    )
    parser.add_argument(
        "--mobile-soft-fail-threshold", type=float, default=MOBILE_SOFT_FAIL_THRESHOLD,
        help=f"Soft-fail ratio threshold on mobile. Default: {MOBILE_SOFT_FAIL_THRESHOLD}.",
    )
    parser.add_argument(
        "--bg-tolerance", type=int, default=BG_PIXEL_TOLERANCE,
        help=f"RGB distance tolerance for background match. Default: {BG_PIXEL_TOLERANCE}.",
    )
    args = parser.parse_args(argv)

    # Execution filling: wire args into the module-level constants or pass
    # through to run_check() as parameters. Stub raises before any real work.
    try:
        report = run_check(url=args.url)
    except NotImplementedError as e:
        print(json.dumps({"error": "stub", "message": str(e)}), file=sys.stderr)
        return 2

    # Emit JSON to stdout, summary to stderr.
    print(json.dumps(_report_to_dict(report), indent=2))
    emit_human_summary(report, stream=sys.stderr)

    any_hard = any(
        vp["pageLevel"]["overallClassification"] == "hard-fail"
        for vp in _report_to_dict(report)["viewports"]
    )
    return 1 if any_hard else 0


def _report_to_dict(report: CheckReport) -> dict:
    """Convert CheckReport dataclass tree to plain dict for JSON emission.

    Converts snake_case dataclass field names to camelCase JSON keys to match
    the spec in Stage II (f) requirement #7.
    """
    return {
        "url": report.url,
        "viewports": [
            {
                "viewport": vp.viewport,
                "sections": [
                    {
                        "sectionId": s.section_id,
                        "paintedPixelRatio": s.painted_pixel_ratio,
                        "classification": s.classification,
                        "staticBlankFlag": s.static_blank_flag,
                        "scrollDependentFlag": s.scroll_dependent_flag,
                        "computedBackgroundColor": s.computed_background_color,
                        "boundingBox": s.bounding_box,
                    }
                    for s in vp.sections
                ],
                "pageLevel": {
                    "hardFailCount": vp.page_level.hard_fail_count,
                    "softFailCount": vp.page_level.soft_fail_count,
                    "totalSections": vp.page_level.total_sections,
                    "overallClassification": vp.page_level.overall_classification,
                },
            }
            for vp in report.viewports
        ],
    }


if __name__ == "__main__":
    sys.exit(main())

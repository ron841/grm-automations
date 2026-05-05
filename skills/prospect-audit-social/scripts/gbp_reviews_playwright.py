"""
GBP all-reviews capture via Playwright headless Chromium.

The Places API truncates reviews to 5 entries with possibly-empty reply
text. This module opens Google Maps for the place_id, navigates to the
Reviews tab, scroll-loads the all-reviews panel, expands truncated
reviews, and extracts:

  - body
  - stars (1-5 integer)
  - author name
  - relative_date (e.g. "2 months ago")
  - owner reply text (selector .CDe7pd, locked per spec)
  - owner reply relative date (selector .DZSIDd, locked per spec)

Saturation rule: after each new review, the SaturationTracker reports
whether distinct job-noun and praise-pattern categories have plateaued
for plateau_window captures. When saturated, we stop scrolling.

Failure modes:
  - GBP all-reviews panel DOM changes -> we tag scrape_failed in the
    return dict. The orchestrator surfaces as [scrape-failed] in intake.
  - Saturation never reaches plateau (low-volume operator with
    high-variance content) -> we capture all reviews and report
    "saturation NOT reached" in saturation-tables.md.
  - Reply text selector returns empty -> [gap] when the per-review DOM
    has no reply node, [scrape-failed] when the node exists but the
    text is empty.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from playwright.sync_api import TimeoutError as PWTimeout
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

from saturation import SaturationTracker

# Locked selectors (validated on Yankee Handyman manual run).
SEL_REPLY_TEXT = ".CDe7pd"
SEL_REPLY_DATE = ".DZSIDd"

# Defensive selectors for review fields. These can drift; the locked
# pair above is the contract.
SEL_REVIEW_CARD = "[data-review-id]"
SEL_AUTHOR = ".d4r55"
SEL_BODY = ".MyEned"
SEL_REL_DATE = ".rsqaWe"
SEL_STARS = '[role="img"][aria-label*="star" i]'
SEL_MORE_BUTTON = "button[jsaction*='expandReview'], button.w8nwRe"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

NAV_TIMEOUT_MS = 60_000
SETTLE_MS = 3500


def _build_maps_url(place_id: str) -> str:
    """Maps URL that opens the place card with reviews accessible."""
    return f"https://www.google.com/maps/place/?q=place_id:{place_id}&hl=en"


def _click_reviews_tab(page) -> bool:
    """Click the Reviews tab in the place card. Returns success bool."""
    # The Reviews tab is a button with role tab and accessible label
    # Reviews. The DOM nests it under the place card, so wait and click
    # by accessible role.
    try:
        page.get_by_role("tab", name="Reviews").first.click(timeout=15_000)
        return True
    except Exception:
        pass
    # Fallback: click any element whose visible text is "Reviews".
    try:
        page.locator("button").filter(has_text="Reviews").first.click(timeout=10_000)
        return True
    except Exception:
        return False


def _scroll_reviews_panel(page, scroll_steps: int = 4,
                          settle_ms: int = 1500) -> None:
    """Scroll the reviews scroll container using mouse.wheel events.

    The Reviews-tab scroll container is virtualized — it appends new
    review cards only when a wheel-event-driven scroll fires. Programmatic
    scrollBy() does not trigger the lazy loader. We move the mouse over
    the container's center and dispatch wheel events to fire the loader.
    """
    # Locate the Reviews-tab scroll container by its known class signature.
    box = page.evaluate("""
    () => {
        const candidates = ['.e07Vkf', '.DxyBCb', '.m6QErb'];
        for (const sel of candidates) {
            const el = document.querySelector(sel);
            if (!el) continue;
            const r = el.getBoundingClientRect();
            if (r.width < 50 || r.height < 50) continue;
            return {x: r.x + r.width / 2, y: r.y + r.height / 2};
        }
        // Fallback: center of the viewport.
        return {x: 400, y: 500};
    }
    """)
    try:
        page.mouse.move(box["x"], box["y"])
    except Exception:
        pass
    for _ in range(scroll_steps):
        try:
            page.mouse.wheel(0, 1000)
        except Exception:
            break
        page.wait_for_timeout(settle_ms // max(scroll_steps, 1))
    page.wait_for_timeout(settle_ms)


def _click_all_more_buttons(page) -> int:
    """Click every "More" button to expand truncated review bodies and
    truncated owner replies.

    The Reviews tab uses two truncation patterns: review-body "More"
    buttons (jsaction includes "expandReview" or class "w8nwRe") and
    reply "More" buttons (button text exactly "More" inside a card with
    reply containers). Click all of them; failures are ignored.

    Returns the number of buttons clicked.
    """
    js = """
    () => {
        const seen = new Set();
        const all = Array.from(document.querySelectorAll('button'));
        let n = 0;
        for (const b of all) {
            const ja = b.getAttribute('jsaction') || '';
            const cls = b.className || '';
            const txt = (b.textContent || '').trim();
            const isExpand = ja.includes('expandReview') || cls.includes('w8nwRe');
            const isMoreText = txt === 'More' || txt.toLowerCase() === 'show more';
            if (!isExpand && !isMoreText) continue;
            if (seen.has(b)) continue;
            seen.add(b);
            try { b.click(); n++; } catch (_) {}
        }
        return n;
    }
    """
    try:
        return page.evaluate(js)
    except Exception:
        return 0


def _extract_visible_reviews(page) -> list[dict]:
    """Extract all currently-rendered review cards into dicts."""
    js = r"""
    () => {
        const cards = Array.from(document.querySelectorAll('[data-review-id]'));
        const out = [];
        for (const c of cards) {
            const id = c.getAttribute('data-review-id');
            const authorEl = c.querySelector('.d4r55');
            const bodyEl = c.querySelector('.MyEned');
            const dateEl = c.querySelector('.rsqaWe');
            const starsEl = c.querySelector('[role="img"][aria-label*="star" i]');
            const replyTextEl = c.querySelector('.CDe7pd');
            const replyDateEl = c.querySelector('.DZSIDd');
            let stars = null;
            if (starsEl) {
                const lbl = starsEl.getAttribute('aria-label') || '';
                const m = lbl.match(/([0-9])/);
                if (m) stars = parseInt(m[1], 10);
            }
            out.push({
                id,
                author: authorEl ? authorEl.textContent.trim() : null,
                body: bodyEl ? bodyEl.textContent.trim() : null,
                relative_date: dateEl ? dateEl.textContent.trim() : null,
                stars,
                reply_text: replyTextEl ? replyTextEl.textContent.trim() : null,
                reply_relative_date: replyDateEl ? replyDateEl.textContent.trim() : null,
            });
        }
        return out;
    }
    """
    try:
        return page.evaluate(js)
    except Exception:
        return []


def scrape_gbp_reviews(place_id: str, plateau_window: int = 5,
                       max_reviews: int = 200,
                       max_scroll_passes: int = 30,
                       profile_dir: Path | None = None) -> dict:
    """Open Maps for place_id, scroll-load reviews, return the corpus.

    The Maps place card omits the Reviews tab when the browser arrives
    cold from a fresh fingerprint. The reliable flow is:

      1. Stealth-wrapped sync_playwright
      2. launch_persistent_context with a per-prospect profile dir
         (sets cookies + consent state on first visit)
      3. Visit google.com to warm the session
      4. Navigate to the Maps place URL
      5. Click the Reviews tab and scroll-load

    Returns:
      {
        "place_id": str,
        "reviews": [...],
        "saturation": {...} from SaturationTracker.frequency_tables(),
        "scrape_failed": bool,
        "notes": [str, ...],
      }
    """
    notes: list[str] = []
    result = {
        "place_id": place_id,
        "reviews": [],
        "saturation": {},
        "scrape_failed": False,
        "notes": notes,
    }

    seen_ids: set[str] = set()
    captured: list[dict] = []
    tracker = SaturationTracker(plateau_window=plateau_window)

    if profile_dir is None:
        profile_dir = Path.home() / ".cache" / "grm-audit-social" / "playwright-profile"
    profile_dir.mkdir(parents=True, exist_ok=True)

    with Stealth().use_sync(sync_playwright()) as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            headless=True,
            user_agent=USER_AGENT,
            viewport={"width": 1366, "height": 900},
            locale="en-US",
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = ctx.new_page()
        page.set_default_timeout(NAV_TIMEOUT_MS)

        # Warm up by visiting google.com first. This seeds cookies and
        # consent state so the Maps place card renders the Reviews tab.
        try:
            page.goto("https://www.google.com/", wait_until="domcontentloaded")
            page.wait_for_timeout(2500)
        except PWTimeout:
            notes.append("[scrape-failed] warm-up navigation to google.com timed out")
            result["scrape_failed"] = True
            ctx.close()
            return result

        try:
            page.goto(_build_maps_url(place_id), wait_until="domcontentloaded")
            page.wait_for_timeout(SETTLE_MS + 2000)
        except PWTimeout:
            notes.append("[scrape-failed] timeout loading Maps URL")
            result["scrape_failed"] = True
            ctx.close()
            return result

        # Click Reviews tab.
        if not _click_reviews_tab(page):
            notes.append("[scrape-failed] could not click Reviews tab")
            result["scrape_failed"] = True
            ctx.close()
            return result
        page.wait_for_timeout(SETTLE_MS + 1500)
        # Pre-scroll to settle the Reviews-tab virtualized container.
        _scroll_reviews_panel(page, scroll_steps=2, settle_ms=1500)

        # Initial expand + extract pass.
        _click_all_more_buttons(page)
        page.wait_for_timeout(800)
        for r in _extract_visible_reviews(page):
            if r["id"] in seen_ids:
                continue
            seen_ids.add(r["id"])
            captured.append(r)
            tracker.add(r.get("body") or "")

        # Scroll-load loop.
        for pass_idx in range(max_scroll_passes):
            if tracker.saturated() and len(captured) >= plateau_window:
                notes.append(f"saturation reached at review #{tracker.saturated_at}")
                break
            if len(captured) >= max_reviews:
                notes.append(f"hit max_reviews cap at {max_reviews}")
                break

            before_count = len(captured)
            _scroll_reviews_panel(page, scroll_steps=4, settle_ms=1500)
            _click_all_more_buttons(page)
            page.wait_for_timeout(600)

            new_batch = _extract_visible_reviews(page)
            added_this_pass = 0
            for r in new_batch:
                if r["id"] in seen_ids:
                    continue
                seen_ids.add(r["id"])
                captured.append(r)
                tracker.add(r.get("body") or "")
                added_this_pass += 1

            if added_this_pass == 0:
                # Two consecutive zero-add passes => panel exhausted.
                _scroll_reviews_panel(page, scroll_steps=2, settle_ms=2000)
                _click_all_more_buttons(page)
                page.wait_for_timeout(600)
                final_batch = _extract_visible_reviews(page)
                truly_done = True
                for r in final_batch:
                    if r["id"] not in seen_ids:
                        seen_ids.add(r["id"])
                        captured.append(r)
                        tracker.add(r.get("body") or "")
                        truly_done = False
                if truly_done:
                    notes.append(
                        f"reviews panel exhausted at #{len(captured)}; "
                        "saturation not reached"
                        if not tracker.saturated() else
                        f"reviews panel exhausted at #{len(captured)}"
                    )
                    break

        ctx.close()

    result["reviews"] = captured
    result["saturation"] = tracker.frequency_tables()
    return result


def _clean_reply_text(raw: str | None, relative_date: str | None) -> str | None:
    """Strip the 'Response from the owner <date>' prefix from raw reply text.

    The .CDe7pd selector includes the parent's wrapper text that prefixes
    the actual reply body with 'Response from the owner X ago'. We strip
    everything up to and including the relative_date if it appears, plus
    the leading 'Response from the owner' literal.
    """
    if not raw:
        return raw
    s = raw
    # Strip leading 'Response from the owner'.
    prefix = "Response from the owner"
    if s.startswith(prefix):
        s = s[len(prefix):]
    # Strip the relative date if it appears as the next thing.
    if relative_date and s.lstrip().startswith(relative_date):
        s = s.lstrip()[len(relative_date):]
    return s.strip()


def split_reviews_and_replies(reviews: list[dict]) -> tuple[list[dict], list[dict]]:
    """Split a captured list into review records and reply records.

    A reply record is emitted only when reply_text is present and
    non-empty. Replies preserve the source review_id for cross-reference.
    The reply text is cleaned of the 'Response from the owner <date>'
    wrapper that lives in the .CDe7pd parent element.
    """
    review_records = []
    reply_records = []
    for r in reviews:
        review_records.append({
            "id": r.get("id"),
            "author": r.get("author"),
            "stars": r.get("stars"),
            "relative_date": r.get("relative_date"),
            "body": r.get("body"),
            "has_reply": bool(r.get("reply_text")),
            "source": "GBP",
        })
        if r.get("reply_text"):
            cleaned = _clean_reply_text(r.get("reply_text"),
                                         r.get("reply_relative_date"))
            reply_records.append({
                "review_id": r.get("id"),
                "review_author": r.get("author"),
                "reply_text": cleaned,
                "reply_relative_date": r.get("reply_relative_date"),
                "source": "GBP",
            })
    return review_records, reply_records


# CLI entry point for ad-hoc verification.
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("usage: gbp_reviews_playwright.py <place_id> <out_dir> [plateau_window]",
              file=sys.stderr)
        sys.exit(2)
    place_id = sys.argv[1]
    out_dir = Path(sys.argv[2]).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    plateau_window = int(sys.argv[3]) if len(sys.argv) > 3 else 5

    print(f"GBP reviews scrape for {place_id} (K={plateau_window}) ...")
    t0 = time.time()
    result = scrape_gbp_reviews(place_id, plateau_window=plateau_window)
    dt = time.time() - t0
    print(f"  reviews: {len(result['reviews'])}")
    print(f"  saturated_at: {result['saturation'].get('saturated_at')}")
    print(f"  distinct jobs: {result['saturation'].get('distinct_jobs_count')}")
    print(f"  distinct praises: {result['saturation'].get('distinct_praises_count')}")
    if result["notes"]:
        print("  notes:")
        for n in result["notes"]:
            print(f"    - {n}")
    print(f"  elapsed: {dt:.1f}s")

    voice_dir = out_dir / "voice-corpus"
    voice_dir.mkdir(parents=True, exist_ok=True)
    review_records, reply_records = split_reviews_and_replies(result["reviews"])
    (voice_dir / "reviews.json").write_text(
        json.dumps({
            "place_id": place_id,
            "count": len(review_records),
            "saturation": result["saturation"],
            "reviews": review_records,
        }, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (voice_dir / "replies.json").write_text(
        json.dumps({
            "place_id": place_id,
            "count": len(reply_records),
            "replies": reply_records,
        }, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    # Render saturation-tables.md from the tracker state. Reconstruct
    # from frequency_tables since we did not return the tracker.
    sat = result["saturation"]
    lines = [
        "# Voice Saturation Tables",
        "",
        f"- Reviews captured: {sat.get('reviews_seen', 0)}",
        f"- Saturation: {'reached at #' + str(sat.get('saturated_at')) if sat.get('saturated_at') else 'NOT reached (corpus exhausted before plateau)'}",
        f"- Distinct job categories matched: {sat.get('distinct_jobs_count', 0)} (last new at #{sat.get('last_new_job_at', 0)})",
        f"- Distinct praise categories matched: {sat.get('distinct_praises_count', 0)} (last new at #{sat.get('last_new_praise_at', 0)})",
        f"- Plateau window: K={sat.get('plateau_window', plateau_window)}",
        "",
        "## Job-noun frequency",
        "",
        "| Job category | Reviews mentioning |",
        "| --- | --- |",
    ]
    for cat, n in sat.get("jobs", {}).items():
        lines.append(f"| {cat} | {n} |")
    lines += ["", "## Praise-pattern frequency", "",
              "| Praise category | Reviews mentioning |",
              "| --- | --- |"]
    for cat, n in sat.get("praises", {}).items():
        lines.append(f"| {cat} | {n} |")
    (voice_dir / "saturation-tables.md").write_text("\n".join(lines) + "\n",
                                                     encoding="utf-8")
    print(f"  written to {voice_dir}")

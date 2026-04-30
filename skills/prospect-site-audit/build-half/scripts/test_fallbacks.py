#!/usr/bin/env python3
"""test_fallbacks.py — exercise §4 fallback behavior on a thinned profile.

Takes the JSL golden fixture, strips three optional fields, runs the render,
and asserts that the expected bands drop and the render doesn't crash.

Run from the skill root:
    cd ~/.claude/skills/prospect-site-v2
    python3 scripts/test_fallbacks.py

Exit 0 = all assertions passed.
Exit 1 = at least one fallback failed.
"""
from __future__ import annotations

import copy
import json
import re
import subprocess
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from render import normalize_phone, phone_tel_href, _verify_no_python_repr_in_html

JSL_PROFILE = SKILL_ROOT / "fixtures" / "jsl" / "profile.json"
JSL_PROSE = SKILL_ROOT / "fixtures" / "jsl" / "prose.json"
THIN_DIR = SKILL_ROOT / "fixtures" / "jsl-thin"
THIN_PROFILE = THIN_DIR / "profile.json"
THIN_PROSE = THIN_DIR / "prose.json"
THIN_OUT = THIN_DIR / "Homepage.html"
PHOTOS_ROOT = "/Users/ronkolb/Desktop/jsl-handoff-unzipped/jsl-handoff"


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def strip_fields(profile: dict) -> tuple[dict, dict]:
    """Strip three optional fields from a deep copy of the profile and return
    (thinned_profile, field_strip_manifest)."""
    thin = copy.deepcopy(profile)
    strips: dict[str, str] = {}

    # 1. Strip owners.list — should drop the story band (§4)
    if "owners" in thin and thin["owners"].get("list"):
        strips["owners.list"] = f"had {len(thin['owners']['list'])} entries"
        thin["owners"]["list"] = []
    else:
        strips["owners.list"] = "was already missing"

    # 2. Strip testimonials.fromGoogleReviews — should drop testimonials band (§4)
    if "testimonials" in thin and thin["testimonials"].get("fromGoogleReviews"):
        strips["testimonials.fromGoogleReviews"] = f"had {len(thin['testimonials']['fromGoogleReviews'])} entries"
        thin["testimonials"]["fromGoogleReviews"] = []
    else:
        strips["testimonials.fromGoogleReviews"] = "was already missing"

    # 3. Strip the first service's description — tile should still render, just without desc
    svc_list = thin.get("services", {}).get("list") or []
    if svc_list and svc_list[0].get("description"):
        strips["services.list[0].description"] = f"was {len(svc_list[0]['description'])} chars"
        svc_list[0]["description"] = ""
    else:
        strips["services.list[0].description"] = "was already missing"

    return thin, strips


def run_render() -> int:
    cmd = [
        "python3",
        str(SKILL_ROOT / "scripts" / "render.py"),
        "--profile", str(THIN_PROFILE),
        "--prose",   str(THIN_PROSE),
        "--out",     str(THIN_OUT),
        "--photos-root", PHOTOS_ROOT,
        "--css-href", "../../css/composer-system.css",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    return result.returncode


def assert_band_absent(html: str, section_class: str, band_name: str, failures: list):
    if re.search(rf'<section class="{section_class}"', html) or re.search(rf'<section class="[^"]*{section_class}[^"]*"', html):
        failures.append(f"{band_name} band should have dropped but is present in rendered HTML")


def assert_band_present(html: str, section_class: str, band_name: str, failures: list):
    if not re.search(rf'<section class="{section_class}"', html) and not re.search(rf'<footer class="{section_class}"', html):
        failures.append(f"{band_name} band should be present but is missing")


def test_feature_manifest(failures: list[str]) -> None:
    """P1 SIMPLIFY-tooling regression test — verify feature-manifest.json
    asserts every active feature appears in its test_page's HTML and every
    removed feature does NOT appear.

    Catches the silent-feature-drop class that produced the count-up +
    slideshow regressions in v0.7.2 → v0.8/v1.0 SIMPLIFY refactor (Session 3
    Round 3). The manifest is institutional memory; this gate is the
    automated check that future refactors don't drop features without
    explicit rationale, and don't accidentally re-introduce removed ones.

    Runs against the Testerman workspace by default. Gracefully skips with
    a printed note if the workspace isn't present (e.g. fresh install
    without prospect data). The skip-on-missing-fixture pattern matches
    the JSL-fixture handling in test_fallback_drops below.
    """
    print("=" * 60)
    print("P1 feature manifest — silent-drop / re-introduction regression check")
    print("=" * 60)

    from verify_feature_manifest import verify_feature_manifest

    manifest_path = SKILL_ROOT / "feature-manifest.json"
    render_dir = Path("/Users/ronkolb/grm-sites-prospects/testermans-pro-wash")

    if not manifest_path.exists():
        failures.append(f"P1 manifest: feature-manifest.json missing at {manifest_path}")
        print(f"  ✗ feature-manifest.json missing at {manifest_path}")
        print()
        return

    if not render_dir.exists():
        # Skip gracefully — rendered fixture isn't available on this install.
        # Future v1.1 work could ship a test fixture in the skill itself
        # (S4-pre — fallback fixture migration to prospect-site-audit), at
        # which point this test would run against the bundled fixture
        # instead of an external prospect workspace.
        print(f"  ⊘ skipped — render fixture not present at {render_dir}")
        print(f"    (run a render against {render_dir} first, or wait for S4-pre to bundle a test fixture)")
        print()
        return

    fail_msgs = verify_feature_manifest(manifest_path, render_dir)
    if fail_msgs:
        for m in fail_msgs:
            failures.append(f"P1 manifest: {m}")
            print(f"  ✗ {m}")
    else:
        with manifest_path.open() as f:
            manifest = json.load(f)
        active = sum(1 for f in manifest["features"] if f.get("status") == "active")
        removed = sum(1 for f in manifest["features"] if f.get("status") == "removed")
        print(f"  ✓ All {active} active + {removed} removed manifest entries verified against {render_dir.name}")
    print()


def test_p16_gate(failures: list[str]) -> None:
    """P16 grep gate negative tests — confirm `_verify_no_python_repr_in_html`
    fires on each of the three symptom-class patterns surfaced at Phase 0.5
    close (Session 4, 2026-04-29):

      (1) Python dict repr — prose dict-slot emitted to HTML without unpack
          Generalized via \\w+ so any field name fails: {'text':, {'em_phrase':,
          {'headline':, etc. First symptom: contact info_heading at render.py
          L2902 (pre-fix).
      (2) Unprocessed {em} shorthand — em-substitution helper not invoked
      (3) Unprocessed {/em} shorthand — same root, closing-tag form
          (2)+(3) caught the homepage-subhead → meta-description leak (S3-1).

    Each negative test plants a deliberate defect in a tiny HTML string and
    asserts the gate raises ValueError with the expected label. The clean-
    baseline string also exercises a known-false-positive surface (inline JS
    with double-quoted JSON keys, JSON-LD-shaped content) to confirm the
    pattern set is leak-only.
    """
    print("=" * 60)
    print("P16 grep gate — negative tests")
    print("=" * 60)

    cases = [
        ("dict-repr-text",      "<h2>{'text': 'How to reach us.', 'em_phrase': 'reach'}</h2>"),
        ("dict-repr-em_phrase", "<p>{'em_phrase': 'reach', 'accent': 'now'}</p>"),
        ("dict-repr-arbitrary", "<div>{'headline': 'Foo'}</div>"),
        ("em-shorthand-open",   "<p>A family-run {em}soft-wash{/em} outfit.</p>"),
        ("em-shorthand-close",  "<p>Closer-only marker {/em} here.</p>"),
    ]

    for name, html in cases:
        try:
            _verify_no_python_repr_in_html(html, page_key=f"test-{name}")
            failures.append(f"P16 gate '{name}' did NOT fire on planted defect: {html!r}")
            print(f"  ✗ {name}: gate did not fire")
        except ValueError as e:
            label = e.args[0].splitlines()[0]
            print(f"  ✓ {name}: {label}")

    # Clean-baseline: inline JS with double-quoted JSON keys + JSON-LD-shaped
    # content + legitimate <em>...</em> markup. None of these should trigger
    # any of the three patterns. False-positive on this string would mean the
    # gate is too aggressive.
    clean = (
        '<h2>How to <em>reach</em> us.</h2>'
        '<p>This is fine.</p>'
        '<script type="application/ld+json">{"@context":"https://schema.org","name":"Foo"}</script>'
        '<script>var x = {"key": 1};</script>'
    )
    try:
        _verify_no_python_repr_in_html(clean, page_key="test-clean-baseline")
        print("  ✓ clean-baseline: passed (no false-positive on JSON-LD or inline JS)")
    except ValueError as e:
        failures.append(f"P16 false-positive on clean HTML: {e}")
        print(f"  ✗ clean-baseline: false-positive — {e}")
    print()


def main() -> int:
    failures: list[str] = []

    # P16 gate negative tests run first — independent of the fallback fixture
    # state and exercise the gate function directly.
    test_p16_gate(failures)

    # P1 feature manifest regression check — runs against current Testerman
    # workspace (skips gracefully if not present). Independent of fallback
    # fixture state.
    test_feature_manifest(failures)

    # 1. Setup (fallback drop test — exercises real render path on a thinned
    #    JSL profile; structural assertions follow)
    THIN_DIR.mkdir(parents=True, exist_ok=True)
    profile = load_json(JSL_PROFILE)
    thin_profile, strips = strip_fields(profile)

    with open(THIN_PROFILE, "w") as f:
        json.dump(thin_profile, f, indent=2)
    # Reuse JSL prose — the test is engine-side, not prose-side
    import shutil
    shutil.copyfile(JSL_PROSE, THIN_PROSE)

    print("=" * 60)
    print("Fallback test — stripping 3 optional fields from JSL profile")
    print("=" * 60)
    for k, v in strips.items():
        print(f"  strip: {k:40s} {v}")
    print()

    # 2. Render
    rc = run_render()
    if rc != 0:
        print(f"✗ Render exited with code {rc}")
        return 1

    # 3. Assert structural fallbacks (shared `failures` list initialized at
    # the top of main() — accumulates from both test_p16_gate above and the
    # fallback-drop assertions below)
    html = THIN_OUT.read_text()

    # Story band should drop (no owners)
    assert_band_absent(html, "story", "Story (owners removed)", failures)

    # Testimonials band should drop (no Google reviews)
    assert_band_absent(html, "testimonials", "Testimonials (reviews removed)", failures)

    # Services band should still render (Phase 4: flagship-canonical .services-section)
    assert_band_present(html, "services-section", "Services", failures)

    # Hero, pullquote, manifesto should all still be present.
    assert_band_present(html, "hero", "Hero", failures)
    assert_band_present(html, "pullquote", "Pullquote", failures)
    assert_band_present(html, "manifesto", "Manifesto", failures)
    # Footer ships as flagship-canonical .footer for every prospect.
    if '<footer class="footer">' not in html:
        failures.append("Footer band should be present (.footer) but is missing")
    # Trust band 02: marquee when ≥3 items resolve, else anchor-strip fallback.
    has_marquee = '<section class="trust-marquee"' in html
    has_anchor = '<section class="anchor-strip"' in html
    if not (has_marquee or has_anchor):
        failures.append("Band 02 (trust) missing: neither .trust-marquee nor .anchor-strip present")

    # The first service tile renders but with an empty description.
    # Phase 4: featured card uses flagship-canonical .service-card-featured,
    # not composer-canonical .svc with .svc-num. The reference service is
    # "Outdoor Living"; first card carries the FEATURED tag.
    featured_card = re.search(
        r'<a [^>]*class="service-card service-card-featured"[^>]*>(.*?)</a>',
        html, re.DOTALL,
    )
    if not featured_card:
        failures.append("First service tile (featured card) not found")
    else:
        tile_html = featured_card.group(1)
        # service-card-desc paragraph should exist but be empty (audit stripped description)
        desc_match = re.search(r'<p class="service-card-desc">([^<]*)</p>', tile_html)
        if not desc_match:
            failures.append("First tile: service-card-desc paragraph missing entirely")
        elif desc_match.group(1).strip():
            failures.append(f"First tile: service-card-desc should be empty, but contains: '{desc_match.group(1)[:60]}'")
        # FEATURED tag should still render (chassis, not from prose)
        if 'class="service-card-tag">FEATURED' not in tile_html:
            failures.append("First tile: FEATURED tag missing")

    # Phone still renders in the 3 visible places (nav via tel:, anchor strip,
    # footer). Phone strings derived from the profile being rendered, not
    # hardcoded — same normalize/tel-href helpers the renderer uses.
    phone_raw = thin_profile.get("contact", {}).get("phone") or ""
    phone_display = normalize_phone(phone_raw)
    phone_tel = phone_tel_href(phone_raw)
    phone_display_count = html.count(phone_display)
    if phone_display_count < 2:  # anchor + footer minimum
        failures.append(f"Phone display '{phone_display}' appears {phone_display_count} times, expected ≥2 (anchor + footer)")
    tel_count = html.count(phone_tel)
    if tel_count < 2:
        failures.append(f"tel: href '{phone_tel}' appears {tel_count} times, expected ≥2 (nav + hero CTA)")

    # 4. Report
    print("\n" + "=" * 60)
    print("Test summary")
    print("=" * 60)
    if not failures:
        print("✓ All P16 negative tests + fallback behaviors fired correctly.")
        print(f"✓ Rendered HTML: {THIN_OUT} ({len(html):,} bytes)")
        print("\nBand map in the thinned render:")
        bands = re.findall(r'data-screen-label="([^"]+)"', html)
        for b in bands:
            print(f"  - {b}")
        return 0
    else:
        print(f"✗ {len(failures)} assertion(s) failed:")
        for f in failures:
            print(f"  - {f}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

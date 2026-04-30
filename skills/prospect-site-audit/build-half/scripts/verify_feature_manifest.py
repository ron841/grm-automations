#!/usr/bin/env python3
"""verify_feature_manifest.py — assert every active feature in
feature-manifest.json appears in the expected fixture page's HTML, and
every removed feature does NOT appear (catches accidental re-introduction).

P1 codification (Session 4 v1.1, 2026-04-29). Catches the silent-feature-
drop class that produced the count-up + slideshow regressions in v0.7.2 →
v0.8/v1.0 SIMPLIFY refactor: features can be silently removed during
refactors without rationale and only surface via prospect cold-walk on
production. The manifest + this verify gate catch silent drops at build
time before the next prospect ships.

Usage as module (preferred — runs from test_fallbacks.py):
    from verify_feature_manifest import verify_feature_manifest
    failures = verify_feature_manifest(manifest_path, render_dir)

Usage as CLI:
    python3 scripts/verify_feature_manifest.py \\
        --manifest build-half/feature-manifest.json \\
        --render-dir ~/grm-sites-prospects/[slug]

Exit 0 = all features verified. Exit 1 = at least one failure.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def verify_feature_manifest(manifest_path: Path | str, render_dir: Path | str) -> list[str]:
    """Verify the manifest against rendered HTML in render_dir.

    Returns a list of failure messages (empty list = all features verified).
    Each failure names the feature id, expected marker, fixture page, and
    a remediation hint.
    """
    manifest_path = Path(manifest_path)
    render_dir = Path(render_dir)

    with manifest_path.open("r", encoding="utf-8") as f:
        manifest = json.load(f)

    failures: list[str] = []

    for feat in manifest.get("features", []):
        fid = feat.get("id", "<unnamed>")
        marker = feat.get("marker", "")
        test_page = feat.get("test_page", "")
        status = feat.get("status", "")

        if not marker or not test_page or not status:
            failures.append(f"manifest entry '{fid}' is malformed — missing marker / test_page / status field")
            continue

        if status not in ("active", "removed"):
            # Other statuses (e.g. "pending", "deprecated") are silently
            # skipped — extension point for v1.2+ status taxonomy.
            continue

        html_path = render_dir / f"{test_page}.html"
        if not html_path.exists():
            failures.append(
                f"feature '{fid}' — fixture page '{test_page}.html' not found in {render_dir}. "
                f"Either run the engine against {render_dir} first, or correct the test_page field in the manifest."
            )
            continue

        html = html_path.read_text(encoding="utf-8")
        marker_present = marker in html

        if status == "active" and not marker_present:
            failures.append(
                f"feature '{fid}' (active) — marker {marker!r} missing from {test_page}.html. "
                f"Possible silent drop in a SIMPLIFY refactor. Either: (1) patch the engine to "
                f"restore the feature emit, or (2) mark this manifest entry status='removed' with "
                f"explicit rationale documenting why the feature was dropped."
            )

        if status == "removed" and marker_present:
            failures.append(
                f"feature '{fid}' (removed) — marker {marker!r} unexpectedly present in {test_page}.html. "
                f"This feature was previously removed (see selection_rationale + 'removed' fields). "
                f"Either: (1) the feature was correctly re-introduced and the manifest entry should "
                f"be flipped back to status='active', or (2) the engine accidentally re-emitted a "
                f"removed feature and the regression should be reverted."
            )

    return failures


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify rendered HTML against feature-manifest.json")
    ap.add_argument("--manifest", required=True, help="Path to feature-manifest.json")
    ap.add_argument("--render-dir", required=True, help="Directory containing rendered fixture HTML")
    args = ap.parse_args()

    failures = verify_feature_manifest(args.manifest, args.render_dir)

    if not failures:
        print("✓ All manifest features verified")
        return 0

    print(f"✗ {len(failures)} feature manifest assertion(s) failed:")
    for f in failures:
        print(f"  - {f}")
    return 1


if __name__ == "__main__":
    sys.exit(main())

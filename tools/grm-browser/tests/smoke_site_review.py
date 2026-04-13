#!/usr/bin/env python3
"""Smoke test for the site-review mission.

Validates plumbing, not that T&F v07 passes every rule.
T&F v07 is known to have a text-based nav logo (check 1 will warn).

Runs site_review against https://tandf-electric-v07.vercel.app
and verifies the output structure is valid.

Exit 0 if structure is valid regardless of individual check outcomes.
"""

import json
import os
import subprocess
import sys

TARGET = "https://tandf-electric-v07.vercel.app"
OUT_DIR = "/tmp/site-review-smoke"
BRAND = "#c4121f"
PYTHON = sys.executable

# Clean output dir
if os.path.exists(OUT_DIR):
    for f in os.listdir(OUT_DIR):
        os.unlink(os.path.join(OUT_DIR, f))


def main():
    print(f"Running site-review against {TARGET}")
    print(f"Output dir: {OUT_DIR}")
    print(f"Brand primary: {BRAND}")
    print()

    result = subprocess.run(
        [
            PYTHON, "-m", "grm_browser.missions.site_review",
            TARGET,
            "--out", OUT_DIR,
            "--brand-primary", BRAND,
            "--services-path", "/services",
        ],
        capture_output=True,
        text=True,
        timeout=300,
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    )

    rc = result.returncode
    errors = 0

    # Structure checks
    json_path = os.path.join(OUT_DIR, "site-review.json")
    md_path = os.path.join(OUT_DIR, "site-review.md")

    # 1. site-review.json exists
    if os.path.isfile(json_path):
        print("[PASS] site-review.json exists")
    else:
        print("[FAIL] site-review.json missing")
        errors += 1

    # 2. site-review.md exists
    if os.path.isfile(md_path):
        print("[PASS] site-review.md exists")
    else:
        print("[FAIL] site-review.md missing")
        errors += 1

    # 3. JSON parses
    try:
        with open(json_path) as f:
            report = json.load(f)
        print("[PASS] JSON parses")
    except Exception as e:
        print(f"[FAIL] JSON parse error: {e}")
        errors += 1
        report = None

    # 4. Exactly 5 checks in output
    if report:
        checks = report.get("checks", [])
        if len(checks) == 5:
            print(f"[PASS] exactly 5 checks in output")
        else:
            print(f"[FAIL] expected 5 checks, got {len(checks)}")
            errors += 1
    else:
        print("[FAIL] cannot check count (JSON failed)")
        errors += 1

    # 5. Exit code is 0 or 1 (not 2)
    if rc in (0, 1):
        print(f"[PASS] exit code = {rc} (not 2)")
    else:
        print(f"[FAIL] exit code = {rc} (expected 0 or 1, got crash code)")
        errors += 1

    # Per-check summary
    if report and report.get("checks"):
        print()
        print("Per-check results:")
        for c in report["checks"]:
            badge = {"pass": "PASS", "fail": "FAIL", "warn": "WARN", "skip": "SKIP"}.get(c["status"], "???")
            detail = c.get("detail", "")[:120]
            print(f"  [{badge}] {c['id']} ({c['severity']}) {detail}")

        s = report.get("summary", {})
        print()
        print(f"Summary: {s.get('pass',0)} pass, {s.get('fail',0)} fail, "
              f"{s.get('warn',0)} warn, {s.get('skip',0)} skip")

    print()
    if errors == 0:
        print("Structure validation: ALL PASS")
        sys.exit(0)
    else:
        print(f"Structure validation: {errors} FAIL(s)")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Smoke test for grm-browser primitives.

Runs five checks against https://tandf-electric-v07.vercel.app.
Prints [PASS] or [FAIL] per check. Exits 0 only if all five pass.
"""

import json
import os
import subprocess
import sys

TARGET = "https://tandf-electric-v07.vercel.app"
PYTHON = sys.executable
MODULE = [PYTHON, "-m", "grm_browser"]

passed = 0
failed = 0


def run_cmd(args, timeout=60):
    """Run a subprocess, return (stdout, returncode)."""
    result = subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    )
    return result.stdout.strip(), result.returncode


def check(num, name, ok, reason=""):
    global passed, failed
    if ok:
        print(f"[PASS] {num}. {name}")
        passed += 1
    else:
        tag = f" -- {reason}" if reason else ""
        print(f"[FAIL] {num}. {name}{tag}")
        failed += 1


# -----------------------------------------------------------------------
# 1. probe -> status == 200, ttfb_ms < 3000
# -----------------------------------------------------------------------
try:
    out, rc = run_cmd(MODULE + ["probe", TARGET])
    data = json.loads(out)
    ok = data.get("status") == 200 and data.get("ttfb_ms", 9999) < 3000
    reason = "" if ok else f"status={data.get('status')}, ttfb={data.get('ttfb_ms')}"
    check(1, "probe", ok, reason)
except Exception as e:
    check(1, "probe", False, str(e))

# -----------------------------------------------------------------------
# 2. capture at 375x812 -> PNG exists, size > 10KB
# -----------------------------------------------------------------------
try:
    out, rc = run_cmd(MODULE + ["capture", TARGET, "--viewport", "375x812"], timeout=90)
    data = json.loads(out)
    path = data.get("path", "")
    size = data.get("bytes", 0)
    ok = os.path.isfile(path) and size > 10240
    reason = "" if ok else f"path_exists={os.path.isfile(path)}, bytes={size}"
    check(2, "capture", ok, reason)
except Exception as e:
    check(2, "capture", False, str(e))

# -----------------------------------------------------------------------
# 3. extract --what og-tags -> og:image present and non-empty
# -----------------------------------------------------------------------
try:
    out, rc = run_cmd(MODULE + ["extract", TARGET, "--what", "og-tags"])
    data = json.loads(out)
    og_image = data.get("data", {}).get("og:image", "")
    ok = bool(og_image)
    reason = "" if ok else f"og:image={repr(og_image)}"
    check(3, "extract og-tags", ok, reason)
except Exception as e:
    check(3, "extract og-tags", False, str(e))

# -----------------------------------------------------------------------
# 4. extract --what nav-images -> returns valid list (T&F uses text logo,
#    so 0 images is correct; primitive must run without error)
# -----------------------------------------------------------------------
try:
    out, rc = run_cmd(MODULE + ["extract", TARGET, "--what", "nav-images"])
    data = json.loads(out)
    images = data.get("data")
    ok = isinstance(images, list) and rc == 0
    reason = "" if ok else f"type={type(images).__name__}, rc={rc}"
    check(4, "extract nav-images", ok, reason)
except Exception as e:
    check(4, "extract nav-images", False, str(e))

# -----------------------------------------------------------------------
# 5. compare --mode color '#c4121f' '#c32030' -> similar == true
# -----------------------------------------------------------------------
try:
    out, rc = run_cmd(MODULE + ["compare", "#c4121f", "#c32030", "--mode", "color"])
    data = json.loads(out)
    ok = data.get("similar") is True
    reason = "" if ok else f"similar={data.get('similar')}, delta={data.get('hue_delta_deg')}"
    check(5, "compare color", ok, reason)
except Exception as e:
    check(5, "compare color", False, str(e))

# -----------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------
print(f"\n{passed}/{passed + failed} checks passed.")
sys.exit(0 if failed == 0 else 1)

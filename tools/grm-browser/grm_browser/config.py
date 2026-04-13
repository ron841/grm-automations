"""Politeness defaults, cache management, and shared constants."""

import hashlib
import os
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Politeness
# ---------------------------------------------------------------------------
PER_DOMAIN_DELAY_SEC = 2.0
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/130.0.0.0 Safari/537.36 GRM-Browser/0.1"
)
NAV_TIMEOUT_MS = 30000

# Per-domain last-request timestamps (in-memory, resets per process).
_domain_last_request = {}


def enforce_delay(host):
    """Sleep the remainder of PER_DOMAIN_DELAY_SEC since last request to *host*."""
    now = time.time()
    last = _domain_last_request.get(host, 0)
    remaining = PER_DOMAIN_DELAY_SEC - (now - last)
    if remaining > 0:
        time.sleep(remaining)
    _domain_last_request[host] = time.time()


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------
CACHE_DIR = Path.home() / "grm-browser-cache"
CACHE_MAX_AGE_DAYS = 14


def ensure_cache_dir():
    """Create the cache directory if it does not exist."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def prune_cache():
    """Delete cache files older than CACHE_MAX_AGE_DAYS."""
    if not CACHE_DIR.exists():
        return
    cutoff = time.time() - (CACHE_MAX_AGE_DAYS * 86400)
    for f in CACHE_DIR.iterdir():
        if f.is_file() and f.stat().st_mtime < cutoff:
            f.unlink(missing_ok=True)


def cache_path(url, viewport="375x812", ext=".png"):
    """Deterministic cache filename from URL + viewport."""
    key = hashlib.sha256(f"{url}:{viewport}".encode()).hexdigest()[:16]
    return CACHE_DIR / f"{key}{ext}"

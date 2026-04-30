#!/usr/bin/env python3
"""unsplash_fetch.py — Phase 5.0b stock-photo resolver for prospect-site-v2.

Two-phase workflow for spectacle-tier picks:

  fetch    Phase A — read slug→query pairs from profile.services[]. For each
           slug, query Unsplash for `--per-page` candidates (default 10).
           Download each candidate's small thumbnail to
           `assets/photos/unsplash/_candidates/<slug>/<id>.jpg`. Write
           `_candidates.json` manifest.

  commit   Phase C — read `--picks` JSON, download chosen photos at
           `urls.regular`, write to `assets/photos/unsplash/<slug>-{featured,detail}.jpg`,
           write `_unsplash-cache.json`, trigger Unsplash download endpoints
           per API Terms.

  auto     A+C in one shot: picks candidate[0] for featured, candidate[1] for
           detail automatically. For Phase 7 multi-prospect cadence after the
           locked queries are validated.

Backup-query ladder: if a primary query returns <3 candidates, the slug's
backup query is tried. If that also returns 0, the slug is flagged
`gradient_fallback: true` in the cache — the renderer drops the photo and
ships the CSS gradient.

Per-prospect overrides: `services[].stockQuery` and `services[].stockQueryBackup`
take precedence over the built-in SERVICE_PHOTO_QUERIES table.

Rate limit: Unsplash free tier = 50 req/hr. Worst case per slug ~ 4 req
(primary search + backup search + 2 download triggers on commit). 6 Volthom
slugs = max 24 req. Well under the cap.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

UNSPLASH_API_BASE = "https://api.unsplash.com"

# Locked default queries from Chat's prep (phase-5-0b-prep.md §"Locked query
# strings"). Tuple is (primary, backup). Backup fires only when primary
# returns <3 candidates. Override per-prospect via services[].stockQuery /
# services[].stockQueryBackup.
SERVICE_PHOTO_QUERIES: dict[str, tuple[str, str]] = {
    "electrical-service-repairs": (
        "electrician repairing wall outlet",
        "residential electrician working",
    ),
    "panel-upgrades": (
        "electrical panel upgrade",
        "circuit breaker panel installation",
    ),
    "generators": (
        "standby generator backyard installation",
        "residential backup power generator",
    ),
    "rewires": (
        "house rewiring electrician",
        "electrical wiring installation residential",
    ),
    "ev-chargers": (
        "ev charger installation home",
        "home electric vehicle charger",
    ),
    "safety-inspections": (
        "electrical safety inspection electrician",
        "electrician inspection meter clipboard",
    ),
}


# ============================================================================
# .env loader (no python-dotenv dependency; we control the file format)
# ============================================================================

def load_env(env_path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not env_path.exists():
        return env
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


# ============================================================================
# Unsplash HTTP helpers
# ============================================================================

def _api_request(url: str, access_key: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers={
        "Authorization": f"Client-ID {access_key}",
        "Accept-Version": "v1",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def unsplash_search(query: str, per_page: int, access_key: str) -> list[dict]:
    """Return Unsplash /search/photos results for one query."""
    params = urllib.parse.urlencode({
        "query": query,
        "per_page": per_page,
        "orientation": "landscape",
        "content_filter": "high",
    })
    url = f"{UNSPLASH_API_BASE}/search/photos?{params}"
    payload = json.loads(_api_request(url, access_key).decode("utf-8"))
    return payload.get("results") or []


def unsplash_track_download(download_location: str, access_key: str) -> None:
    """Trigger the download endpoint per Unsplash API Terms. Counts toward
    rate limit; non-fatal on failure (the photo still downloaded)."""
    if not download_location:
        return
    try:
        _api_request(download_location, access_key, timeout=15)
    except Exception as e:
        print(f"  ! download-track failed (non-fatal): {e}", file=sys.stderr)


def fetch_image(url: str, dest: Path) -> None:
    """Download a binary image to dest. mkdir -p as needed."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "grm-composer/5.0b"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        dest.write_bytes(resp.read())


# ============================================================================
# Query resolution
# ============================================================================

def resolve_query_pair(slug: str, svc: dict) -> tuple[str, str]:
    """Resolve (primary, backup) for a slug. Per-prospect override on
    services[i] wins over the built-in default table."""
    override_primary = (svc.get("stockQuery") or "").strip()
    override_backup = (svc.get("stockQueryBackup") or "").strip()
    default_primary, default_backup = SERVICE_PHOTO_QUERIES.get(slug, ("", ""))
    return (override_primary or default_primary, override_backup or default_backup)


def candidate_metadata(result: dict, thumb_relpath: str) -> dict:
    """Extract the subset of an Unsplash search result we care about."""
    user = result.get("user") or {}
    urls = result.get("urls") or {}
    links = result.get("links") or {}
    return {
        "id": result.get("id") or "",
        "thumb_path": thumb_relpath,
        "regular_url": urls.get("regular") or "",
        "full_url": urls.get("full") or "",
        "download_location": links.get("download_location") or "",
        "html_url": links.get("html") or "",
        "photographer_name": user.get("name") or "",
        "photographer_html": (user.get("links") or {}).get("html") or "",
        "alt_description": result.get("alt_description") or "",
        "description": result.get("description") or "",
        "width": result.get("width"),
        "height": result.get("height"),
    }


# ============================================================================
# Phase A — fetch candidates
# ============================================================================

def cmd_fetch(prospect_dir: Path, env: dict[str, str], per_page: int,
              slugs_filter: list[str] | None, profile: dict) -> int:
    access_key = env.get("UNSPLASH_ACCESS_KEY") or ""
    if not access_key:
        print("ERROR: UNSPLASH_ACCESS_KEY missing from .env", file=sys.stderr)
        return 2

    services_list = ((profile.get("services") or {}).get("list")) or []
    unsplash_root = prospect_dir / "assets" / "photos" / "unsplash"
    candidates_dir = unsplash_root / "_candidates"
    candidates_dir.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, dict] = {}
    for svc in services_list:
        slug = svc.get("slug") or ""
        if not slug:
            continue
        if slugs_filter and slug not in slugs_filter:
            continue
        primary, backup = resolve_query_pair(slug, svc)
        if not primary:
            print(f"- {slug}: no query string (skipping)")
            continue
        print(f"+ {slug}: query='{primary}' per_page={per_page}")
        try:
            results = unsplash_search(primary, per_page, access_key)
        except Exception as e:
            print(f"  ! primary query failed: {e}", file=sys.stderr)
            results = []
        used_query, used_backup = primary, False
        if len(results) < 3 and backup:
            print(f"  ~ primary returned {len(results)} results; trying backup '{backup}'")
            try:
                backup_results = unsplash_search(backup, per_page, access_key)
            except Exception as e:
                print(f"  ! backup query failed: {e}", file=sys.stderr)
                backup_results = []
            if len(backup_results) > len(results):
                results, used_query, used_backup = backup_results, backup, True

        if not results:
            manifest[slug] = {
                "primary_query": primary,
                "backup_query": backup,
                "used_query": used_query,
                "used_backup": used_backup,
                "candidates": [],
                "gradient_fallback": True,
            }
            print(f"  ! no candidates for {slug}; flagged gradient_fallback")
            continue

        slug_dir = candidates_dir / slug
        slug_dir.mkdir(parents=True, exist_ok=True)
        candidates: list[dict] = []
        for r in results:
            photo_id = r.get("id") or ""
            thumb_url = ((r.get("urls") or {}).get("small")) or ""
            if not photo_id or not thumb_url:
                continue
            dest = slug_dir / f"{photo_id}.jpg"
            try:
                if not dest.exists():
                    fetch_image(thumb_url, dest)
            except Exception as e:
                print(f"  ! thumb fetch failed for {photo_id}: {e}", file=sys.stderr)
                continue
            thumb_rel = f"assets/photos/unsplash/_candidates/{slug}/{photo_id}.jpg"
            candidates.append(candidate_metadata(r, thumb_rel))
        manifest[slug] = {
            "primary_query": primary,
            "backup_query": backup,
            "used_query": used_query,
            "used_backup": used_backup,
            "candidates": candidates,
            "gradient_fallback": False,
        }
        print(f"  ok: {len(candidates)} candidates cached")

    manifest_path = unsplash_root / "_candidates.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"\nWrote manifest: {manifest_path}")
    print(f"Candidate thumbs: {candidates_dir}")
    return 0


# ============================================================================
# Phase C — commit picks
# ============================================================================

def cmd_commit(prospect_dir: Path, env: dict[str, str], picks_path: Path) -> int:
    access_key = env.get("UNSPLASH_ACCESS_KEY") or ""
    if not access_key:
        print("ERROR: UNSPLASH_ACCESS_KEY missing from .env", file=sys.stderr)
        return 2
    unsplash_root = prospect_dir / "assets" / "photos" / "unsplash"
    manifest_path = unsplash_root / "_candidates.json"
    if not manifest_path.exists():
        print(f"ERROR: candidates manifest missing: {manifest_path}", file=sys.stderr)
        return 2
    if not picks_path.exists():
        print(f"ERROR: picks file missing: {picks_path}", file=sys.stderr)
        return 2

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    picks = json.loads(picks_path.read_text(encoding="utf-8"))

    # Load existing cache (if any) so partial commits — e.g. fetch --slugs
    # generators followed by commit — don't wipe entries for slugs not in the
    # current manifest. Only slugs present in `picks` get overwritten.
    cache_path = prospect_dir / "assets" / "photos" / "unsplash" / "_unsplash-cache.json"
    if cache_path.exists():
        try:
            existing_cache = json.loads(cache_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            existing_cache = {}
    else:
        existing_cache = {}

    # Photo discipline guard: same Unsplash id must not appear twice across
    # the 12 picks (6 featured + 6 detail). Same image in two service-detail
    # blocks would render as a visible defect on the live page (4.5c lesson —
    # photo discipline catches at the engine boundary, not at deploy walk).
    seen: dict[str, str] = {}
    duplicates: list[str] = []
    for slug, slot_picks in picks.items():
        if not isinstance(slot_picks, dict):
            continue
        for slot, photo_id in slot_picks.items():
            if not photo_id or slot not in ("featured", "detail"):
                continue
            prior = seen.get(photo_id)
            if prior:
                duplicates.append(f"{photo_id}: {prior} <-> {slug}/{slot}")
            else:
                seen[photo_id] = f"{slug}/{slot}"
    if duplicates:
        print("ERROR: duplicate photo ids across picks (photo-discipline rule):",
              file=sys.stderr)
        for d in duplicates:
            print(f"  - {d}", file=sys.stderr)
        return 2

    # Start from the existing cache so untouched slugs survive incremental
    # commits. Only the slugs in `picks` will be rewritten below.
    cache: dict[str, dict] = dict(existing_cache)

    for slug, slot_picks in picks.items():
        slug_manifest = manifest.get(slug) or {}
        if slug_manifest.get("gradient_fallback"):
            cache[slug] = {
                "gradient_fallback": True,
                "primary_query": slug_manifest.get("primary_query"),
                "used_query": slug_manifest.get("used_query"),
            }
            continue
        cands_by_id = {c["id"]: c for c in slug_manifest.get("candidates", [])}
        cache_entry: dict = {
            "gradient_fallback": False,
            "primary_query": slug_manifest.get("primary_query"),
            "used_query": slug_manifest.get("used_query"),
            "used_backup": slug_manifest.get("used_backup"),
        }
        for slot in ("featured", "detail"):
            photo_id = slot_picks.get(slot)
            if not photo_id:
                continue
            cand = cands_by_id.get(photo_id)
            if not cand:
                print(f"  ! pick {slug}/{slot}={photo_id} not in candidates manifest",
                      file=sys.stderr)
                continue
            dest_filename = f"{slug}-{slot}.jpg"
            dest_path = unsplash_root / dest_filename
            print(f"+ {slug}/{slot}: downloading {photo_id} → {dest_filename}")
            fetch_image(cand["regular_url"], dest_path)
            unsplash_track_download(cand["download_location"], access_key)
            cache_entry[slot] = {
                "id": photo_id,
                "filename": dest_filename,
                "rel_path": f"assets/photos/unsplash/{dest_filename}",
                "regular_url": cand["regular_url"],
                "html_url": cand["html_url"],
                "photographer_name": cand["photographer_name"],
                "photographer_html": cand["photographer_html"],
                "alt_description": cand["alt_description"],
            }
        cache[slug] = cache_entry

    cache_path = unsplash_root / "_unsplash-cache.json"
    cache_path.write_text(json.dumps(cache, indent=2) + "\n", encoding="utf-8")
    print(f"\nWrote cache: {cache_path}")
    return 0


# ============================================================================
# Auto mode — A+C in one shot, picks #0 + #1 automatically
# ============================================================================

def cmd_auto(prospect_dir: Path, env: dict[str, str], per_page: int,
             slugs_filter: list[str] | None, profile: dict) -> int:
    rc = cmd_fetch(prospect_dir, env, per_page, slugs_filter, profile)
    if rc != 0:
        return rc
    unsplash_root = prospect_dir / "assets" / "photos" / "unsplash"
    manifest = json.loads((unsplash_root / "_candidates.json").read_text(encoding="utf-8"))
    auto_picks: dict[str, dict] = {}
    for slug, entry in manifest.items():
        if entry.get("gradient_fallback"):
            auto_picks[slug] = {}
            continue
        cands = entry.get("candidates") or []
        if not cands:
            auto_picks[slug] = {}
            continue
        pick: dict = {"featured": cands[0]["id"]}
        if len(cands) >= 2:
            pick["detail"] = cands[1]["id"]
        else:
            pick["detail"] = cands[0]["id"]
        auto_picks[slug] = pick
    auto_picks_path = unsplash_root / "_picks-auto.json"
    auto_picks_path.write_text(json.dumps(auto_picks, indent=2) + "\n", encoding="utf-8")
    print(f"\nAuto-picks written: {auto_picks_path}")
    return cmd_commit(prospect_dir, env, auto_picks_path)


# ============================================================================
# CLI
# ============================================================================

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--prospect-dir", required=True, type=Path,
                    help="Path to ~/grm-sites-prospects/<slug>/")
    ap.add_argument("--env", type=Path,
                    default=Path.home() / "grm-sites-prospects" / ".env",
                    help="Path to .env containing UNSPLASH_ACCESS_KEY")
    sub = ap.add_subparsers(dest="cmd", required=True)

    fetch = sub.add_parser("fetch", help="Phase A: write candidate thumbs + manifest")
    fetch.add_argument("--per-page", type=int, default=10)
    fetch.add_argument("--slugs", default=None,
                       help="comma-separated slugs to fetch (default: all in profile)")

    commit = sub.add_parser("commit", help="Phase C: download picks + write cache")
    commit.add_argument("--picks", required=True, type=Path,
                        help="Path to _picks.json: {<slug>: {featured: <id>, detail: <id>}}")

    auto = sub.add_parser("auto", help="A+C in one shot, auto-picks #0 + #1")
    auto.add_argument("--per-page", type=int, default=10)
    auto.add_argument("--slugs", default=None)

    args = ap.parse_args()
    env = load_env(args.env)
    profile_path = args.prospect_dir / "profile-draft.json"
    if not profile_path.exists():
        print(f"ERROR: profile not found: {profile_path}", file=sys.stderr)
        return 2
    profile = json.loads(profile_path.read_text(encoding="utf-8"))

    if args.cmd == "fetch":
        slugs = [s.strip() for s in (args.slugs or "").split(",") if s.strip()] or None
        return cmd_fetch(args.prospect_dir, env, args.per_page, slugs, profile)
    if args.cmd == "commit":
        return cmd_commit(args.prospect_dir, env, args.picks)
    if args.cmd == "auto":
        slugs = [s.strip() for s in (args.slugs or "").split(",") if s.strip()] or None
        return cmd_auto(args.prospect_dir, env, args.per_page, slugs, profile)
    return 1


if __name__ == "__main__":
    sys.exit(main())

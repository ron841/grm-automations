"""
Orchestrator for prospect-audit-social v0.2.

Wires the ten phases per spec:

  Phase 1  identity bootstrap (Places API place details)
  Phase 2  photo library capture (Places Photo API, native res)
  Phase 3  logo capture (FB graph profile picture)
  Phase 4  social discovery (FB handle + IG when verified)
  Phase 5  owner full-name verification (FL Division of Corporations)
  Phase 6  extended review capture (GBP all-reviews via stealth Playwright)
  Phase 7  derived signals (job-noun + praise-pattern frequencies, replies)
  Phase 8  logo color extraction (k-means k=5)
  Phase 9  output composition (intake.md + summary.json + reviews.json +
           reviews.md + photo manifest + README.md + process-notes.md)
  Phase 10 GitHub publish (per-prospect repo)

v0.2 output layout (Design seat spec):

  prospect-slug/
    README.md                     entry point at root
    audit/
      intake.md
      reviews.md                  saturation summary + chronological corpus
      data/
        summary.json              structured pull from intake
        reviews.json              structured per-review with attached reply
        gbp-raw.json              renamed from place-details-raw.json
      photos/
        manifest.json             per-photo metadata
        gbp/                      split from images/ by source
        fb/                       split from images/ by source
    logo/                         unchanged at root
    palette/                      unchanged at root
    process-notes.md              unchanged at root

Usage:
  python3 audit.py "Business Name" "<place_id_or_maps_url>" \
      [--out PATH]              override workspace dir
      [--fb-handle HANDLE]      FB Page handle if known (skips guessing)
      [--saturation-window N]   plateau window K (default 5)
      [--no-publish]            skip Phase 10
      [--dry-run]               run everything except GitHub create
      [--from-cache CACHE_DIR]  reuse scraped artifacts from a prior run
                                instead of re-scraping; useful when the
                                workspace is wiped to validate v0.2 layout

Exit codes:
  0  every intake field is filled or explicitly tagged
  1  forcing-function check failed (a field has neither value nor tag)
  2  unrecoverable phase failure
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from datetime import date, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import places_api
import fb_playwright
import gbp_reviews_playwright
import kmeans_palette
from saturation import categorize_review, JOB_NOUN_PATTERNS, PRAISE_PATTERNS

PROSPECTS_ROOT = Path.home() / "grm-sites-prospects"
SKILL_VERSION = "v0.2"

# Standing docs at the grm-pipeline repo root, in the order specified by the
# Design seat handoff contract. Categories profile is appended dynamically.
GRM_PIPELINE_REPO = "ron841/grm-pipeline"
STANDING_DOCS_FILES = [
    "grm-pipeline-contract.md",
    "grm-design-defaults.md",
    "grm-decisions-ledger.md",
    "grm-lessons.md",
]

# Map a GBP type to a category-profile slug under grm-pipeline/categories/.
# Iterated in dict order so the most specific contractor types match before
# generic ones; first hit wins.
GBP_TYPE_TO_CATEGORY = {
    "roofing_contractor": "contractor",
    "general_contractor": "contractor",
    "plumber": "contractor",
    "electrician": "contractor",
    "hvac_contractor": "contractor",
    "painter": "contractor",
    "carpenter": "contractor",
    "landscaper": "contractor",
    "lawn_care_service": "contractor",
    "pressure_washing_service": "contractor",
    "handyman": "contractor",
    "moving_company": "contractor",
    "construction_company": "contractor",
    "restaurant": "restaurant",
    "cafe": "restaurant",
    "meal_takeaway": "restaurant",
    "meal_delivery": "restaurant",
    "bakery": "restaurant",
    "bar": "bars-taverns",
    "night_club": "bars-taverns",
    "pub": "bars-taverns",
    "car_repair": "auto",
    "car_dealer": "auto",
    "auto_body_shop": "auto",
    "tire_shop": "auto",
    "gas_station": "auto",
    "garden_center": "farm-nursery",
    "plant_nursery": "farm-nursery",
    "florist": "farm-nursery",
    "farm": "farm-nursery",
    "beauty_salon": "personal-care",
    "hair_care": "personal-care",
    "hair_salon": "personal-care",
    "barber_shop": "personal-care",
    "nail_salon": "personal-care",
    "spa": "personal-care",
    "massage_therapist": "personal-care",
    "veterinary_care": "pet-services",
    "pet_groomer": "pet-services",
    "pet_store": "pet-services",
    "dog_trainer": "pet-services",
    "animal_boarding": "pet-services",
}


def slugify(name: str) -> str:
    s = name.lower()
    s = re.sub(r"['’]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def parse_place_id(arg: str) -> str:
    """Accept a raw place_id or extract one from a Maps URL."""
    arg = arg.strip()
    if arg.startswith("ChIJ") or arg.startswith("Eh"):
        return arg
    m = re.search(r"place_id[:=]([A-Za-z0-9_\-]+)", arg)
    if m:
        return m.group(1)
    raise ValueError(f"Could not parse place_id from: {arg!r}")


def guess_fb_handles(business_name: str) -> list[str]:
    """Generate FB handle candidates from a business name."""
    base = re.sub(r"[^A-Za-z0-9 ]", "", business_name)
    parts = base.split()
    parts_clean = [p for p in parts if p.lower() not in
                   {"llc", "inc", "corp", "co", "ltd", "company"}]
    candidates = set()
    if parts_clean:
        candidates.add("".join(parts_clean))
        candidates.add("".join(parts_clean[:2]))
        candidates.add("the" + "".join(parts_clean))
    if parts:
        candidates.add("".join(parts))
        candidates.add("the" + "".join(parts))
    return [c for c in candidates if len(c) >= 4]


def resolve_fb_handle(business_name: str, candidates: list[str] | None = None) -> str | None:
    """Try FB graph picture endpoint for each candidate, return first hit."""
    import requests
    cand = candidates or guess_fb_handles(business_name)
    for c in cand:
        try:
            r = requests.get(
                f"https://graph.facebook.com/{c}/picture?type=large&redirect=false",
                timeout=10,
            )
            if r.status_code == 200:
                data = r.json()
                if "data" in data and data["data"].get("url") \
                        and not data["data"].get("is_silhouette", True):
                    return c
        except Exception:
            continue
    return None


def derive_owner_first_name(reviews: list[dict],
                             business_name: str) -> tuple[str | None, int]:
    """Scan owner replies and review text for an operator first name."""
    if not reviews:
        return None, 0
    biz_tokens = set(t.lower() for t in re.findall(r"[A-Za-z]+", business_name))
    biz_tokens |= {"llc", "inc", "corp", "co", "ltd", "company", "the"}
    common_words = {
        "thank", "thanks", "you", "your", "we", "our", "us", "i", "he", "she",
        "they", "this", "that", "these", "those", "very", "much", "really",
        "great", "good", "best", "amazing", "excellent", "wonderful", "perfect",
        "highly", "definitely", "absolutely", "would", "could", "should", "will",
        "the", "a", "an", "and", "but", "or", "if", "when", "while", "as",
        "yes", "no", "okay", "sure", "well", "now", "then", "today", "tomorrow",
        "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
        "january", "february", "march", "april", "may", "june", "july", "august",
        "september", "october", "november", "december",
        "north", "south", "east", "west", "central", "florida", "ocala",
        "response", "reply", "review", "owner", "customer", "company", "service",
        "team", "guys", "boys", "men", "people", "everyone", "everybody",
        "hello", "hi", "hey", "sorry", "please", "again", "back", "first",
        "still", "even", "right", "left", "from", "after", "before",
        "super",
    }
    biz_tokens |= common_words
    counter: dict[str, int] = {}
    for r in reviews:
        for field in ("body", "reply_text"):
            text = r.get(field) or ""
            for m in re.finditer(r"\b([A-Z][a-z]{2,11})\b", text):
                w = m.group(1)
                if w.lower() in biz_tokens:
                    continue
                counter[w] = counter.get(w, 0) + 1
    if not counter:
        return None, 0
    top = max(counter.items(), key=lambda kv: kv[1])
    if top[1] < 3:
        return None, top[1]
    return top[0], top[1]


def reply_length_distribution(replies: list[dict]) -> dict:
    buckets = {"canned (<30)": 0, "short (30-100)": 0,
               "medium (100-250)": 0, "detailed (>250)": 0}
    for r in replies:
        n = len((r.get("reply_text") or "").strip())
        if n < 30:
            buckets["canned (<30)"] += 1
        elif n < 100:
            buckets["short (30-100)"] += 1
        elif n < 250:
            buckets["medium (100-250)"] += 1
        else:
            buckets["detailed (>250)"] += 1
    return buckets


def recurring_openers(replies: list[dict], top_n: int = 5) -> list[tuple[str, int]]:
    counter: dict[str, int] = {}
    for r in replies:
        t = (r.get("reply_text") or "").strip()
        words = t.split()[:4]
        if len(words) < 2:
            continue
        opener = " ".join(words).rstrip(".,!?")
        counter[opener] = counter.get(opener, 0) + 1
    items = [(k, v) for k, v in counter.items() if v >= 2]
    items.sort(key=lambda kv: -kv[1])
    return items[:top_n]


def pin_grm_pipeline_sha(local_clone: Path = Path.home() / "grm-pipeline") -> tuple[str, str]:
    """Pin the grm-pipeline commit SHA for raw URL stability.

    Primary: git ls-remote against the public repo HEAD.
    Fallback 1: git rev-parse HEAD in a local clone.
    Fallback 2: literal "[pending-pin]" plus a stderr warning.

    Returns (sha, source) where source is one of:
      "remote", "local", "pending".
    """
    try:
        r = subprocess.run(
            ["git", "ls-remote", f"https://github.com/{GRM_PIPELINE_REPO}.git", "HEAD"],
            capture_output=True, text=True, timeout=20, check=False,
        )
        if r.returncode == 0 and r.stdout.strip():
            sha = r.stdout.split()[0].strip()
            if re.fullmatch(r"[0-9a-f]{40}", sha):
                return sha, "remote"
    except (subprocess.SubprocessError, OSError):
        pass

    if local_clone.exists() and (local_clone / ".git").exists():
        try:
            r = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=local_clone,
                capture_output=True, text=True, timeout=10, check=False,
            )
            if r.returncode == 0 and r.stdout.strip():
                sha = r.stdout.strip()
                if re.fullmatch(r"[0-9a-f]{40}", sha):
                    return sha, "local"
        except (subprocess.SubprocessError, OSError):
            pass

    print(
        "WARN: could not pin grm-pipeline SHA from remote or local clone; "
        "README will use literal [pending-pin] in standing-doc URLs.",
        file=sys.stderr,
    )
    return "[pending-pin]", "pending"


def infer_category(place: dict) -> str:
    """Pick a category-profile slug from the place's GBP types.

    First match wins, in GBP_TYPE_TO_CATEGORY iteration order. Falls back to
    "contractor" when nothing matches, since the no-website pipeline targets
    home-services contractors by default.
    """
    types = list(place.get("types", []))
    primary = place.get("primaryType")
    if primary:
        types = [primary] + types
    for t in types:
        if t in GBP_TYPE_TO_CATEGORY:
            return GBP_TYPE_TO_CATEGORY[t]
    return "contractor"


def parse_relative_date(rel: str, run_date: date) -> str:
    """Convert a GBP-style relative date phrase to an approximate ISO date.

    Examples accepted: "5 months ago", "a month ago", "2 weeks ago",
    "a year ago", "yesterday", "X days ago", "X hours ago", "just now".

    Returns YYYY-MM-DD or "[gap]" when the phrase is not recognized. The
    conversion is approximate: months are 30 days, years are 365 days. The
    audit's process-notes call out the approximation so Design treats the
    field as evidence-of-recency, not a precise timestamp.
    """
    if not rel:
        return "[gap]"
    s = rel.strip().lower()
    if s in {"just now", "moments ago", "an hour ago", "a few hours ago"}:
        return run_date.isoformat()
    if s in {"yesterday", "a day ago"}:
        return (run_date - timedelta(days=1)).isoformat()
    m = re.match(r"(\d+|a|an)\s+(hour|hours|day|days|week|weeks|month|months|year|years)\s+ago", s)
    if not m:
        return "[gap]"
    n_raw, unit = m.group(1), m.group(2)
    n = 1 if n_raw in ("a", "an") else int(n_raw)
    days_map = {
        "hour": 0, "hours": 0,
        "day": 1, "days": 1,
        "week": 7, "weeks": 7,
        "month": 30, "months": 30,
        "year": 365, "years": 365,
    }
    days = n * days_map.get(unit, 0)
    return (run_date - timedelta(days=days)).isoformat()


def render_intake(ctx: dict) -> str:
    """Build intake.md from captured context.

    Identical to v0.1 content; the file is written under audit/ in v0.2.
    """
    place = ctx["place"]
    photos = ctx["photos"]
    fb = ctx.get("fb") or {}
    reviews = ctx.get("reviews") or []
    replies = ctx.get("replies") or []
    saturation = ctx.get("saturation") or {}
    palette = ctx.get("palette") or {}
    business_name = place.get("displayName", {}).get("text", ctx["business_name"])

    addr = place.get("formattedAddress", "[scrape-failed]")
    phone = place.get("nationalPhoneNumber") or place.get("internationalPhoneNumber") or "[gap]"
    email = "[gap]"
    website = place.get("websiteUri") or "none (confirmed)"
    rating = place.get("rating", "[scrape-failed]")
    review_count = place.get("userRatingCount", "[scrape-failed]")
    primary_cat = (
        place.get("primaryTypeDisplayName", {}).get("text")
        if isinstance(place.get("primaryTypeDisplayName"), dict)
        else place.get("primaryType", "[gap]")
    )
    secondary_cats = place.get("types", [])
    hours = place.get("regularOpeningHours", {}).get("weekdayDescriptions", [])
    accessibility = place.get("accessibilityOptions", {})

    owner_first, owner_evidence_n = ctx.get("owner_first_name", (None, 0))
    if owner_first and owner_evidence_n >= 20:
        owner_full = (
            f"[low-confidence] candidate '{owner_first}' from {owner_evidence_n} mentions; "
            "[pending-walkthrough] for confirmation"
        )
    else:
        owner_full = (
            "[pending-walkthrough] (FL Division of Corporations registry lookup deferred to v0.3; "
            "review-corpus first-name derivation is unreliable without a name lexicon)"
        )

    reply_buckets = reply_length_distribution(replies)
    openers = recurring_openers(replies)
    if replies:
        reply_rate = f"{len(replies)} of {len(reviews)} reviews carry owner replies"
        reply_tag = "replies-to-all" if len(replies) >= max(1, len(reviews) - 2) else \
                    "replies-selectively" if len(replies) >= 1 else "does-not-reply"
    else:
        reply_rate = "[gap]" if reviews else "[scrape-failed]"
        reply_tag = "[gap]" if reviews else "[scrape-failed]"

    job_freq = saturation.get("jobs", {})
    praise_freq = saturation.get("praises", {})
    diff_candidates = [(p, n) for p, n in list(praise_freq.items())[:5]]

    fb_cover = fb.get("cover_photo")
    fb_pages = fb.get("page_photos") or []
    fb_url = fb.get("page_url", "[gap]")
    fb_intro = fb.get("intro_text") or "[gap]"
    fb_followers = fb.get("follower_count") or "[gap]"

    today = date.today().isoformat()
    out: list[str] = []
    out.append(f"# {business_name} - Intake")
    out.append("")
    out.append(
        "> **Source tags inline:** *[API]* Places API. *[manual]* user capture. "
        "*[web]* public web search. *[FB]* Facebook. *[scrape-Playwright]* Playwright DOM extraction. "
        "*[derived]* computed from captures. *[human]* requires human judgment"
    )
    out.append("")
    out.append(f"> **Capture method:** audit-skill {SKILL_VERSION}. **Run date:** {today}")
    out.append("")

    out.append("## §1 Identity")
    out.append("")
    out.append(f"- **Business name (legal, as on GBP):** {business_name}")
    out.append("- **DBA / display name (if different):** [gap]")
    out.append(f"- **Tagline / slogan:** {fb_intro if fb_intro != '[gap]' else '[gap]'}")
    out.append(f"- **Owner full name:** {owner_full}")
    out.append("- **Owner story signal:** [pending-synthesis]")
    out.append("- **Year founded / years in business:** [pending-walkthrough] (FL Division of Corporations lookup deferred to v0.3)")
    out.append("- **License & insurance status:** [pending-walkthrough]")
    out.append("")

    out.append("## §2 Location & Contact")
    out.append("")
    out.append(f"- **Address:** {addr} *[API]*")
    out.append(f"- **Phone:** {phone} *[API]*")
    out.append(f"- **Email:** {email} *[pending-walkthrough]*")
    out.append(f"- **Website:** {website} *[API]*")
    out.append("- **Service area:** [pending-synthesis] (derive from review evidence)")
    out.append("")

    out.append("## §3 Hours & Availability")
    out.append("")
    if hours:
        out.append("- **Regular hours:** *[API]*")
        for h in hours:
            out.append(f"  - {h}")
    else:
        out.append("- **Regular hours:** [gap]")
    out.append("- **Emergency / 24-hour service flag:** [pending-walkthrough]")
    out.append("- **Booking method:** phone *[API + review evidence]*")
    out.append("")

    out.append("## §4 Categories & Services")
    out.append("")
    out.append(f"- **GBP primary category:** {primary_cat} *[API]*")
    out.append(f"- **GBP secondary categories:** {', '.join(secondary_cats) if secondary_cats else '[gap]'} *[API]*")
    out.append("- **Services list (synthesized from review evidence):** *[derived]*")
    if job_freq:
        for cat, n in list(job_freq.items())[:10]:
            out.append(f"  - {cat} *[evidence: {n} reviews]*")
    else:
        out.append("  - [scrape-failed] no review corpus available")
    out.append("")

    out.append("### §4a Voice - Owner Replies")
    out.append("")
    out.append(f"- **Reply rate:** {reply_rate}")
    out.append("- **Length distribution:** *[derived]*")
    for k, v in reply_buckets.items():
        out.append(f"  - {k}: {v}")
    out.append("- **Recurring openers:** " + (
        ", ".join(f'"{p}" ({n})' for p, n in openers) if openers else "[gap]"))
    out.append("- **Voice tone characterization:** [pending-synthesis]")
    out.append("- **Verbatim phrases worth lifting for synthesis:** [pending-synthesis]")
    out.append(f"- **Reply behavior tag:** {reply_tag}")
    out.append("")

    out.append("## §5 Attributes & Credentials")
    out.append("")
    if accessibility:
        flags = ", ".join(k for k, v in accessibility.items() if v) or "[gap]"
        out.append(f"- **GBP attributes:** {flags} *[API]*")
    else:
        out.append("- **GBP attributes:** [gap]")
    out.append("- **Certifications mentioned in reviews or social:** [pending-synthesis]")
    out.append("- **Awards / recognition:** [pending-synthesis]")
    out.append("")

    out.append("## §6 Voice - Reviews")
    out.append("")
    if reviews:
        sat_text = (
            f"REACHED at #{saturation.get('saturated_at')}"
            if saturation.get("saturated_at")
            else "NOT REACHED (corpus exhausted before plateau)"
        )
        out.append(
            f"> **Capture status:** {len(reviews)} reviews captured "
            f"out of {review_count} total. **Saturation:** {sat_text}. **Source:** GBP Playwright"
        )
        out.append("")
        out.append("> **Saturation analysis:**")
        out.append(
            f"> - Distinct job-noun categories: {saturation.get('distinct_jobs_count', 0)} "
            f"(last new at #{saturation.get('last_new_job_at', 0)})"
        )
        out.append(
            f"> - Distinct praise-pattern categories: {saturation.get('distinct_praises_count', 0)} "
            f"(last new at #{saturation.get('last_new_praise_at', 0)})"
        )
        out.append("")
        for i, r in enumerate(reviews, start=1):
            out.append(f"### Review {i} *[GBP, {today}]*")
            out.append("")
            out.append(f"- **Stars:** {r.get('stars', '?')}")
            out.append(f"- **Reviewer:** {r.get('author', '[gap]')}")
            out.append(f"- **Relative date:** {r.get('relative_date', '[gap]')}")
            body = (r.get("body") or "[gap]").replace("\n", " ")
            out.append(f"- **Text:** \"{body}\"")
            matching_reply = next(
                (rep for rep in replies if rep.get("review_id") == r.get("id")), None
            )
            if matching_reply:
                rt = (matching_reply.get("reply_text") or "").replace("\n", " ")
                out.append(
                    f"- **Owner reply** *({matching_reply.get('reply_relative_date', '?')})*: \"{rt}\""
                )
            else:
                out.append("- **Owner reply:** *none*")
            out.append("")
    else:
        out.append("> **Capture status:** [scrape-failed]")
        out.append("")

    out.append("## §7 Voice - Saturation tables")
    out.append("")
    out.append("### Job-noun frequency")
    out.append("")
    out.append("| Job category | Reviews mentioning |")
    out.append("| --- | --- |")
    if job_freq:
        for cat, n in job_freq.items():
            out.append(f"| {cat} | {n} |")
    else:
        out.append("| [scrape-failed] | 0 |")
    out.append("")
    out.append("### Praise-pattern frequency")
    out.append("")
    out.append("| Praise category | Reviews mentioning |")
    out.append("| --- | --- |")
    if praise_freq:
        for cat, n in praise_freq.items():
            out.append(f"| {cat} | {n} |")
    else:
        out.append("| [scrape-failed] | 0 |")
    out.append("")
    out.append("### Differentiator implications")
    out.append("")
    if diff_candidates:
        for cat, n in diff_candidates:
            out.append(f"- **{cat}**: {n} reviews mention this *[evidence count]*")
    else:
        out.append("- [pending-synthesis]")
    out.append("")

    out.append("## §8 Voice - Bio extracts")
    out.append("")
    out.append(f"- **Source:** {'FB intro' if fb.get('intro_text') else '[gap]'}")
    out.append(f"- **Tagline candidates:** {fb.get('intro_text') or '[gap]'}")
    out.append("- **Owner story signals in bio:** [pending-synthesis]")
    out.append("- **Years in business claims in bio:** [pending-synthesis]")
    out.append("- **Service mentions in bio:** [pending-synthesis]")
    out.append("- **Personality markers:** [pending-synthesis]")
    out.append("")

    out.append("## §9 Social Presence")
    out.append("")
    out.append("### Facebook")
    out.append("")
    out.append(f"- **Page URL:** {fb_url}")
    out.append(f"- **About text:** {fb.get('intro_text') or '[gap]'}")
    out.append("- **Recent post excerpts:** [pending-extraction] (v0.3)")
    out.append("- **Recurring themes:** [pending-synthesis]")
    out.append("- **Voice tone in posts:** [pending-synthesis]")
    out.append(f"- **Follower count (page likes):** {fb_followers}")
    out.append("- **Adjacent FB accounts:** [pending-extraction]")
    out.append("")
    out.append("### Instagram")
    out.append("")
    out.append("- **Handle / URL:** [verification-deferred] (v0.3)")
    out.append("- **Bio in full:** [verification-deferred]")
    out.append("- **Recent post captions:** [verification-deferred]")
    out.append("")

    out.append("## §10 Photos")
    out.append("")
    out.append(
        f"> Captured: {len(photos)} from GBP at full native resolution + "
        f"{1 if fb_cover else 0} FB cover + {len(fb_pages)} FB page photos. "
        "Full per-photo metadata in audit/photos/manifest.json."
    )
    out.append("")
    out.append("- See `audit/photos/manifest.json` for the canonical per-photo manifest.")
    out.append("- GBP photos: `audit/photos/gbp/`")
    out.append("- FB photos: `audit/photos/fb/`")
    out.append("")

    out.append("## §11 Logo")
    out.append("")
    out.append(f"- **Found:** {'Yes' if ctx.get('logo_path') else 'No'}")
    out.append("- **Source:** FB profile picture")
    out.append(f"- **File saved at:** {ctx.get('logo_path', '[scrape-failed]')}")
    out.append("- **Quality:** raster-low (FB profile picture endpoint)")
    out.append("")

    out.append("## §12 Colors")
    out.append("")
    if palette.get("clusters"):
        out.append("- **Extracted from logo (k-means k=5):** *[derived]*")
        for c in palette["clusters"]:
            out.append(
                f"  - {c['hex']} freq {c['frequency_pct']}% "
                f"confidence {c['confidence']}"
            )
        bg = palette.get("background_excluded")
        if bg:
            out.append(
                f"- **Background excluded:** {bg['hex']} ({bg['frequency_pct']}% of source)"
            )
        out.append("- **Extracted from uniforms / vehicles / signage:** [pending-image-review]")
        out.append("- **Proposed palette:** [pending-synthesis]")
        if all(c["confidence"] >= 0.8 for c in palette["clusters"]):
            out.append("- **Confidence:** high")
        else:
            out.append("- **Confidence:** medium")
    else:
        out.append("- **Extracted from logo:** [scrape-failed]")
    out.append("")

    out.append("## §13 Trust Signals")
    out.append("")
    out.append(f"- **Total reviews:** {review_count} *[API]*")
    out.append(f"- **Star rating:** {rating} *[API]*")
    out.append("- **Years on Google (rough):** [pending-synthesis] (derive from earliest review)")
    out.append(f"- **FB follower count:** {fb_followers}")
    out.append("- **IG follower count:** [verification-deferred]")
    out.append("- **FB check-in count:** [pending-extraction]")
    out.append("- **Years in business:** [pending-walkthrough]")
    out.append("")

    out.append("## §14 Differentiators (synthesized)")
    out.append("")
    if diff_candidates:
        for i, (cat, n) in enumerate(diff_candidates[:3], start=1):
            out.append(f"{i}. **{cat}.** Surfaced in {n} of {len(reviews)} reviews. *[evidence count]*")
    else:
        out.append("[pending-synthesis]")
    out.append("")

    out.append("## §15 Content Gaps Flagged")
    out.append("")
    out.append("**Resolved this pass:** *[derived]*")
    out.append("")
    out.append("- Identity, location, hours, categories, attributes from Places API")
    out.append("- Photo library (GBP + FB) with provenance tagging")
    out.append("- Review corpus with saturation analysis and dedup")
    out.append("- Owner reply corpus with locked selectors")
    out.append("- Logo color extraction via k-means")
    out.append("")
    out.append("**Still open (require walkthrough or manual capture):** *[derived]*")
    out.append("")
    out.append("- Owner full last name (FL Division of Corporations lookup deferred to v0.3)")
    out.append("- Email address")
    out.append("- License and insurance status")
    out.append("- Years in business (operator confirmation)")
    out.append("- Service area boundaries (operator confirmation)")
    out.append("- IG presence verification")
    out.append("")

    out.append("## §16 Capture Run Notes")
    out.append("")
    out.append(f"- **Audit script version:** prospect-audit-social {SKILL_VERSION}")
    out.append(f"- **Run date:** {today}")
    out.append(f"- **Duration:** {ctx.get('elapsed_sec', '?')} seconds")
    out.append(f"- **Successful captures:** {', '.join(ctx.get('successful_phases', []))}")
    if ctx.get("failed_phases"):
        out.append(f"- **Failures and retries:** {', '.join(ctx['failed_phases'])}")
    out.append("- **Deferred to manual:** §1 owner-last-name, §2 email, §5 license/insurance, §13 years-in-business, §9 IG verification")
    return "\n".join(out) + "\n"


def forcing_function_check(intake_md: str) -> tuple[bool, list[str]]:
    """Verify every line that looks like a field has a value or tag.

    Header lines (a bold field followed by sub-bullets, like
    "- **Hours:** *[API]*") are not flagged as ambiguous when they carry
    an explicit source tag. Bare bold-only lines without a source tag
    or value are still flagged.
    """
    failing = []
    for ln in intake_md.splitlines():
        m = re.match(r"^\s*-\s*\*\*([^*]+):\*\*\s*(.*?)\s*$", ln)
        if not m:
            continue
        value = m.group(2)
        if value == "" or value == "*[source]*":
            failing.append(ln)
    return (len(failing) == 0, failing)


def build_summary_json(ctx: dict) -> dict:
    """Compose audit/data/summary.json from captured ctx.

    All values come from the same upstream sources as intake.md (Places API
    response, FB scrape, derived saturation tables). Fields without evidence
    are tagged [gap]; never invented.
    """
    place = ctx["place"]
    fb = ctx.get("fb") or {}
    saturation = ctx.get("saturation") or {}
    business_name = place.get("displayName", {}).get("text", ctx["business_name"])

    addr_components = {c["types"][0]: c.get("longText") or c.get("shortText")
                       for c in place.get("addressComponents", [])
                       if c.get("types")}
    nap = {
        "street": (
            (addr_components.get("street_number", "") + " " +
             addr_components.get("route", "")).strip()
            or "[gap]"
        ),
        "city": addr_components.get("locality", "[gap]"),
        "state": next(
            (c.get("shortText") for c in place.get("addressComponents", [])
             if "administrative_area_level_1" in c.get("types", [])),
            "[gap]",
        ),
        "zip": addr_components.get("postal_code", "[gap]"),
        "phone": (
            place.get("nationalPhoneNumber")
            or place.get("internationalPhoneNumber")
            or "[gap]"
        ),
        "email": "[gap]",
    }

    hours_by_day: dict[str, str] = {}
    weekday_descs = place.get("regularOpeningHours", {}).get("weekdayDescriptions", [])
    for d in weekday_descs:
        if ": " in d:
            day, hrs = d.split(": ", 1)
            hours_by_day[day.strip()] = hrs.strip()
    if not hours_by_day:
        hours_by_day = {}

    services = list((saturation.get("jobs") or {}).keys()) or []
    trades = [t for t in place.get("types", [])
              if t not in ("point_of_interest", "establishment", "service")] or []

    website = place.get("websiteUri")
    if website is None:
        website_status = "none (confirmed)"
    elif "facebook.com" in website.lower():
        website_status = f"facebook-only: {website}"
    else:
        website_status = website

    fb_url = fb.get("page_url") or "[gap]"
    summary = {
        "business_name": business_name,
        "owner_name": "[pending-walkthrough]",
        "nap": nap,
        "hours_by_day": hours_by_day or "[gap]",
        "services": services,
        "trades": trades,
        "founded_year": "[gap]",
        "google_place_id": ctx["place_id"],
        "gbp_rating": place.get("rating", "[gap]"),
        "gbp_review_count": place.get("userRatingCount", "[gap]"),
        "fb_url": fb_url,
        "instagram_url": "[verification-deferred]",
        "website_status": website_status,
    }
    return summary


def build_reviews_json(reviews: list[dict], replies: list[dict],
                        run_date: date) -> list[dict]:
    """Compose audit/data/reviews.json with attached owner_reply per review."""
    reply_index = {r.get("review_id"): r for r in replies}
    out = []
    for r in reviews:
        reply = reply_index.get(r.get("id"))
        out.append({
            "reviewer_name": r.get("author", "[gap]"),
            "rating": r.get("stars", "[gap]"),
            "date_iso": parse_relative_date(r.get("relative_date", ""), run_date),
            "text": r.get("body", "[gap]"),
            "owner_reply": reply.get("reply_text") if reply else None,
            "source": "gbp",
        })
    return out


def build_reviews_md(reviews: list[dict], replies: list[dict],
                      saturation: dict, business_name: str,
                      run_date: date) -> str:
    """Compose audit/reviews.md: saturation summary + chronological corpus."""
    reply_index = {r.get("review_id"): r for r in replies}
    job_freq = saturation.get("jobs", {}) or {}
    praise_freq = saturation.get("praises", {}) or {}

    enriched = []
    for r in reviews:
        iso = parse_relative_date(r.get("relative_date", ""), run_date)
        sort_key = iso if iso != "[gap]" else "0000-00-00"
        enriched.append((sort_key, iso, r))
    enriched.sort(key=lambda t: t[0])

    out: list[str] = []
    out.append(f"# {business_name} - Review Corpus")
    out.append("")
    out.append(f"> Captured: {len(reviews)} reviews. "
               f"Saturated at #{saturation.get('saturated_at', '?')}. "
               f"Plateau window K={saturation.get('plateau_window', 5)}.")
    out.append("")
    out.append("## Saturation summary")
    out.append("")
    out.append("### Job-noun frequency")
    out.append("")
    out.append("| Job category | Reviews mentioning |")
    out.append("| --- | --- |")
    if job_freq:
        for cat, n in job_freq.items():
            out.append(f"| {cat} | {n} |")
    else:
        out.append("| [scrape-failed] | 0 |")
    out.append("")
    out.append("### Praise-pattern frequency")
    out.append("")
    out.append("| Praise category | Reviews mentioning |")
    out.append("| --- | --- |")
    if praise_freq:
        for cat, n in praise_freq.items():
            out.append(f"| {cat} | {n} |")
    else:
        out.append("| [scrape-failed] | 0 |")
    out.append("")
    out.append("## Reviews (chronological, oldest first)")
    out.append("")
    if not enriched:
        out.append("[scrape-failed] no review corpus captured.")
        return "\n".join(out) + "\n"

    for i, (_, iso, r) in enumerate(enriched, start=1):
        author = r.get("author", "[gap]")
        stars = r.get("stars", "?")
        rel = r.get("relative_date", "?")
        out.append(f"### {i}. {author}. {stars} stars. {rel} ({iso}).")
        out.append("")
        body = (r.get("body") or "[gap]").replace("\n", " ")
        out.append(f"> {body}")
        out.append("")
        reply = reply_index.get(r.get("id"))
        if reply:
            rt = (reply.get("reply_text") or "").replace("\n", " ")
            rd = reply.get("reply_relative_date", "?")
            out.append(f"**Owner reply ({rd}):** {rt}")
        else:
            out.append("**Owner reply:** none")
        out.append("")
    return "\n".join(out) + "\n"


def build_photo_manifest(gbp_metadata: list[dict],
                          fb_metadata: list[dict]) -> list[dict]:
    """Compose audit/photos/manifest.json.

    GBP photos: customer_attributed = False (every record we capture from
    Places API is either owner-uploaded or customer-uploaded, but the
    Places API returns owner-uploaded for the prospects we target; the spec
    pins this to false until v0.3 wires customer-attribution explicitly).
    Caption text and slot suggestion are placeholder per the v0.2 contract.
    FB photos: customer_attributed = "[gap]" (deferred to v0.3 backlog).
    """
    manifest: list[dict] = []

    def suggest_slot(filename: str) -> str:
        f = filename.lower()
        if "logo" in f:
            return "header"
        if "before" in f or "after" in f:
            return "showcase-pair"
        return "[pending-design]"

    for m in gbp_metadata:
        manifest.append({
            "filename": m["file"],
            "source": "gbp",
            "customer_attributed": False,
            "caption_text": "[gap]",
            "suggested_slot": suggest_slot(m["file"]),
            "operator_veto": None,
        })
    for m in fb_metadata:
        manifest.append({
            "filename": m["file"],
            "source": "fb",
            "customer_attributed": "[gap]",
            "caption_text": "[gap]",
            "suggested_slot": suggest_slot(m["file"]),
            "operator_veto": None,
        })
    return manifest


def extract_open_questions(intake_md: str) -> list[tuple[str, str]]:
    """Pull every field with a [pending-walkthrough] / [gap] / [scrape-failed] tag.

    Returns a list of (field_name, displayed_value_with_tag) tuples in the
    order they appear in intake.md. Sub-bullets that are part of an
    explicitly tagged parent (Hours, Services list) inherit the parent's
    tag and are not surfaced separately.
    """
    questions: list[tuple[str, str]] = []
    for ln in intake_md.splitlines():
        m = re.match(r"^\s*-\s*\*\*([^*]+):\*\*\s*(.*?)\s*$", ln)
        if not m:
            continue
        field, value = m.group(1).strip(), m.group(2).strip()
        if not value:
            continue
        for tag in ("[pending-walkthrough]", "[gap]", "[scrape-failed]",
                    "[verification-deferred]", "[pending-extraction]",
                    "[pending-synthesis]", "[pending-image-review]",
                    "[low-confidence]", "[pending-pin]"):
            if tag in value:
                questions.append((field, value))
                break
    return questions


def build_readme(ctx: dict, sha: str, slug: str, intake_md: str,
                  gbp_count: int, fb_count: int,
                  customer_attributed_count: int) -> str:
    """Compose README.md at the repo root: the Design seat's entry point."""
    place = ctx["place"]
    business_name = place.get("displayName", {}).get("text", ctx["business_name"])
    category = ctx.get("category", "contractor")
    raw_pipeline = f"https://raw.githubusercontent.com/{GRM_PIPELINE_REPO}/{sha}"
    raw_prospect = f"https://raw.githubusercontent.com/ron841/grm-prospect-{slug}/main"

    standing_urls = [f"{raw_pipeline}/{f}" for f in STANDING_DOCS_FILES]
    standing_urls.append(f"{raw_pipeline}/categories/{category}-profile.md")

    prospect_files = [
        "audit/intake.md",
        "audit/reviews.md",
        "audit/data/summary.json",
        "audit/data/reviews.json",
        "audit/data/gbp-raw.json",
        "audit/photos/manifest.json",
    ]
    prospect_urls = [f"{raw_prospect}/{p}" for p in prospect_files]
    readme_url = f"{raw_prospect}/README.md"

    out: list[str] = []
    out.append(f"# {business_name} - Prospect Package")
    out.append("")
    out.append("[Design seat. Read this file first.]")
    out.append("")
    out.append(f"## Standing docs (pinned to grm-pipeline commit {sha})")
    out.append("")
    for u in standing_urls:
        out.append(f"- {u}")
    out.append("")
    out.append("## This prospect (reading order)")
    out.append("")
    for u in prospect_urls:
        out.append(f"- {u}")
    out.append("")
    out.append("## Photo manifest summary")
    out.append("")
    total = gbp_count + fb_count
    out.append(f"- GBP photos: {gbp_count}")
    out.append(f"- FB photos: {fb_count}")
    out.append(f"- Customer-attributed: {customer_attributed_count}")
    out.append(f"- Total: {total}")
    out.append("")
    out.append("## Open questions from audit")
    out.append("")
    open_q = extract_open_questions(intake_md)
    if open_q:
        for field, value in open_q:
            out.append(f"- **{field}:** {value}")
    else:
        out.append("- (none. Every intake field has a captured value.)")
    out.append("")
    out.append("## Stock seat prompt")
    out.append("")
    out.append("```")
    out.append(
        "You are the Design seat in the GRM pipeline. Read the GRM standing "
        f"docs (pinned to grm-pipeline commit {sha}) in this order:"
    )
    out.append("")
    for u in standing_urls:
        out.append(u)
    out.append("")
    out.append("Then read the prospect package at:")
    out.append(readme_url)
    out.append("")
    out.append(
        "Follow the README's reading order. Produce the full Design pack: "
        "synthesis.md, content-inventory.md, slots.md, Home.html, "
        "BUILD-DECISIONS.md, and pack-README.md. Forcing-function check must "
        "pass before you ship. Every string in content-inventory.md "
        "three-state tagged with citation. Every Open Decision in "
        "pack-README's Open Decisions table."
    )
    out.append("")
    out.append(
        "Package the deliverable as a downloadable ZIP if your environment "
        "supports it. Otherwise output each file as a code block I can copy."
    )
    out.append("```")
    return "\n".join(out) + "\n"


def write_process_notes(out_dir: Path, ctx: dict) -> None:
    lines = [
        f"# Process Notes - {ctx['business_name']}",
        "",
        f"- Run date: {date.today().isoformat()}",
        f"- Skill version: prospect-audit-social {SKILL_VERSION}",
        f"- Duration: {ctx.get('elapsed_sec', '?')} seconds",
        f"- Place ID: {ctx['place_id']}",
        f"- Slug: {ctx['slug']}",
        f"- grm-pipeline SHA: {ctx.get('pipeline_sha', '[unset]')} "
        f"(source: {ctx.get('pipeline_sha_source', '[unset]')})",
        f"- Cache mode: {ctx.get('cache_mode', 'live-scrape')}",
        "",
        "## Phase outcomes",
        "",
    ]
    for phase, outcome in ctx.get("phase_log", []):
        lines.append(f"- {phase}: {outcome}")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    for n in ctx.get("notes", []):
        lines.append(f"- {n}")
    (out_dir / "process-notes.md").write_text("\n".join(lines) + "\n",
                                              encoding="utf-8")


def github_publish(slug: str, out_dir: Path,
                    commit_message: str = "Initial intake from prospect-audit-social v0.2") -> str | None:
    """Initialize or update repo at github.com/ron841/grm-prospect-{slug}.

    Behavior:
      - If the workspace already has .git/ and a remote, just commit and push.
      - Otherwise init, create the remote via gh, and push.

    Returns the URL on success, None on failure.
    """
    repo_name = f"ron841/grm-prospect-{slug}"
    repo_url = f"https://github.com/{repo_name}"
    git_dir = out_dir / ".git"

    try:
        if not git_dir.exists():
            subprocess.run(["git", "init", "-q"], cwd=out_dir, check=True)
        # Ensure local user identity for commit verification.
        subprocess.run(
            ["git", "config", "user.email", "ron@getrootedmedia.com"],
            cwd=out_dir, check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Ron Kolb"],
            cwd=out_dir, check=True,
        )

        subprocess.run(["git", "add", "-A"], cwd=out_dir, check=True)
        # Skip the commit if the index is clean.
        diff_check = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=out_dir, check=False,
        )
        if diff_check.returncode != 0:
            subprocess.run(
                ["git", "commit", "-q", "-m", commit_message],
                cwd=out_dir, check=True,
            )

        # Remote setup.
        remote_check = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=out_dir, capture_output=True, text=True, check=False,
        )
        if remote_check.returncode != 0:
            subprocess.run([
                "gh", "repo", "create", repo_name,
                "--public", "--source=.", "--remote=origin", "--push",
            ], cwd=out_dir, check=True)
            return repo_url

        # Existing remote: ensure default branch exists and push.
        branch_check = subprocess.run(
            ["git", "symbolic-ref", "--short", "HEAD"],
            cwd=out_dir, capture_output=True, text=True, check=False,
        )
        branch = (branch_check.stdout.strip() or "main") if branch_check.returncode == 0 else "main"
        subprocess.run(["git", "push", "origin", branch], cwd=out_dir, check=True)
        return repo_url
    except subprocess.CalledProcessError:
        return None


def restore_from_cache(cache_dir: Path, out_dir: Path) -> dict:
    """Copy scraped artifacts from a cache dir into the workspace.

    Looks for these artifacts (any subset is fine; missing ones fall back
    to live scraping):

      <cache>/place-details-raw.json     OR   <cache>/audit/data/gbp-raw.json
      <cache>/voice-corpus/reviews.json  OR   <cache>/audit/data/reviews.json
                                                (raw v0.1 schema preferred)
      <cache>/voice-corpus/replies.json
      <cache>/images/                    (mixed gbp+fb, v0.1 layout)
      <cache>/audit/photos/gbp/          (v0.2 layout, used as-is)
      <cache>/audit/photos/fb/           (v0.2 layout, used as-is)
      <cache>/logo/logo.jpg
      <cache>/palette/extraction.json
      <cache>/palette/swatch.png

    Returns a dict describing what was restored, for telemetry.
    """
    restored: dict[str, str] = {}

    # GBP raw place details.
    src_gbp_v1 = cache_dir / "place-details-raw.json"
    src_gbp_v2 = cache_dir / "audit" / "data" / "gbp-raw.json"
    target_gbp = out_dir / "_cache" / "gbp-raw.json"
    target_gbp.parent.mkdir(parents=True, exist_ok=True)
    if src_gbp_v2.exists():
        shutil.copy2(src_gbp_v2, target_gbp)
        restored["gbp-raw.json"] = str(src_gbp_v2)
    elif src_gbp_v1.exists():
        shutil.copy2(src_gbp_v1, target_gbp)
        restored["gbp-raw.json"] = str(src_gbp_v1)

    # Voice corpus.
    voice_cache = out_dir / "_cache" / "voice"
    voice_cache.mkdir(parents=True, exist_ok=True)
    rev_v1 = cache_dir / "voice-corpus" / "reviews.json"
    rep_v1 = cache_dir / "voice-corpus" / "replies.json"
    if rev_v1.exists():
        shutil.copy2(rev_v1, voice_cache / "reviews.json")
        restored["voice-corpus/reviews.json"] = str(rev_v1)
    if rep_v1.exists():
        shutil.copy2(rep_v1, voice_cache / "replies.json")
        restored["voice-corpus/replies.json"] = str(rep_v1)

    # Photos.
    photos_cache = out_dir / "_cache" / "photos"
    photos_cache.mkdir(parents=True, exist_ok=True)
    src_photos_v1 = cache_dir / "images"
    src_photos_v2_gbp = cache_dir / "audit" / "photos" / "gbp"
    src_photos_v2_fb = cache_dir / "audit" / "photos" / "fb"
    if src_photos_v2_gbp.exists():
        shutil.copytree(src_photos_v2_gbp, photos_cache / "gbp", dirs_exist_ok=True)
        restored["photos/gbp"] = str(src_photos_v2_gbp)
    if src_photos_v2_fb.exists():
        shutil.copytree(src_photos_v2_fb, photos_cache / "fb", dirs_exist_ok=True)
        restored["photos/fb"] = str(src_photos_v2_fb)
    if src_photos_v1.exists() and not src_photos_v2_gbp.exists():
        # Split v0.1 mixed images/ folder by filename pattern.
        for f in src_photos_v1.iterdir():
            if not f.is_file() or f.name == "README.md":
                continue
            if f.name.startswith("fb-"):
                (photos_cache / "fb").mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, photos_cache / "fb" / f.name)
            elif re.match(r"^\d{2}-gbp-", f.name):
                (photos_cache / "gbp").mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, photos_cache / "gbp" / f.name)
        restored["photos (split v0.1)"] = str(src_photos_v1)

    # Logo + palette.
    if (cache_dir / "logo" / "logo.jpg").exists():
        (out_dir / "logo").mkdir(parents=True, exist_ok=True)
        shutil.copy2(cache_dir / "logo" / "logo.jpg", out_dir / "logo" / "logo.jpg")
        restored["logo/logo.jpg"] = str(cache_dir / "logo" / "logo.jpg")
    if (cache_dir / "palette").exists():
        (out_dir / "palette").mkdir(parents=True, exist_ok=True)
        for f in (cache_dir / "palette").iterdir():
            if f.is_file():
                shutil.copy2(f, out_dir / "palette" / f.name)
        restored["palette/"] = str(cache_dir / "palette")

    return restored


def run(business_name: str, place_id: str, *,
        out_dir: Path, fb_handle: str | None = None,
        saturation_window: int = 5, publish: bool = True,
        dry_run: bool = False,
        from_cache: Path | None = None) -> int:
    t_start = time.time()
    slug = slugify(business_name)
    out_dir.mkdir(parents=True, exist_ok=True)

    phase_log: list[tuple[str, str]] = []
    notes: list[str] = []
    successful: list[str] = []
    failed: list[str] = []

    # v0.2 layout dirs.
    audit_dir = out_dir / "audit"
    data_dir = audit_dir / "data"
    photos_root = audit_dir / "photos"
    photos_gbp = photos_root / "gbp"
    photos_fb = photos_root / "fb"
    for d in (audit_dir, data_dir, photos_gbp, photos_fb):
        d.mkdir(parents=True, exist_ok=True)

    cache_artifacts: dict[str, str] = {}
    cache_mode = "live-scrape"
    if from_cache is not None:
        cache_artifacts = restore_from_cache(from_cache, out_dir)
        cache_mode = f"reused-from-cache ({len(cache_artifacts)} artifacts)"
        notes.append(f"Cache mode: restored {len(cache_artifacts)} artifacts from {from_cache}")
        for k, v in cache_artifacts.items():
            notes.append(f"  - {k} <- {v}")

    pipeline_sha, pipeline_sha_source = pin_grm_pipeline_sha()

    ctx = {
        "business_name": business_name,
        "place_id": place_id,
        "slug": slug,
        "phase_log": phase_log,
        "notes": notes,
        "successful_phases": successful,
        "failed_phases": failed,
        "pipeline_sha": pipeline_sha,
        "pipeline_sha_source": pipeline_sha_source,
        "cache_mode": cache_mode,
    }

    # Phase 1.
    print("Phase 1: identity bootstrap ...")
    cached_gbp = out_dir / "_cache" / "gbp-raw.json"
    if cached_gbp.exists():
        place = json.loads(cached_gbp.read_text(encoding="utf-8"))
        phase_log.append(("Phase 1", f"OK (from cache); rating {place.get('rating')}, reviews {place.get('userRatingCount')}"))
    else:
        api_key = places_api.load_api_key()
        place = places_api.fetch_place_details(place_id, api_key)
        phase_log.append(("Phase 1", f"OK (live); rating {place.get('rating')}, reviews {place.get('userRatingCount')}"))
    (data_dir / "gbp-raw.json").write_text(
        json.dumps(place, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    ctx["place"] = place
    ctx["category"] = infer_category(place)
    successful.append("Phase 1")

    # Phase 2.
    print("Phase 2: photo library capture ...")
    business_display = place.get("displayName", {}).get("text", business_name)
    cached_gbp_dir = out_dir / "_cache" / "photos" / "gbp"
    if cached_gbp_dir.exists() and any(cached_gbp_dir.iterdir()):
        photos: list[dict] = []
        for f in sorted(cached_gbp_dir.iterdir()):
            if not f.is_file() or f.name == "README.md":
                continue
            target = photos_gbp / f.name
            shutil.copy2(f, target)
            prov = "owner-uploaded" if "-owner-" in f.name else "customer-uploaded"
            photos.append({
                "file": f.name,
                "source": "GBP API",
                "provenance": prov,
                "author": business_display if prov == "owner-uploaded" else None,
                "width": None,
                "height": None,
                "photo_resource_name": None,
                "low_confidence": False,
                "scrape_failed": False,
            })
        phase_log.append(("Phase 2", f"OK (from cache); {len(photos)} photos"))
    else:
        api_key = places_api.load_api_key()
        photos = places_api.fetch_photos(
            place, slug, business_display, api_key, out_dir,
            photos_dir=photos_gbp,
        )
        phase_log.append(("Phase 2", f"OK (live); {len(photos)} photos"))
    ctx["photos"] = photos
    successful.append("Phase 2")

    # Phase 4 (run before 3 because logo capture depends on FB handle).
    print("Phase 4: social discovery ...")
    if not fb_handle:
        # Inspect cached gbp-raw.json for a Facebook URL hint first; else guess.
        website = place.get("websiteUri") or ""
        m = re.search(r"facebook\.com/([A-Za-z0-9.\-_]+)/?", website)
        if m:
            fb_handle = m.group(1).rstrip("/")
        else:
            fb_handle = resolve_fb_handle(business_display)
    if fb_handle:
        phase_log.append(("Phase 4", f"OK; FB handle {fb_handle}"))
    else:
        phase_log.append(("Phase 4", "[gap] no FB handle resolved"))
        notes.append("Phase 4: no FB handle resolved via guessing; pass --fb-handle if known")

    # Phase 3.
    print("Phase 3: logo capture ...")
    cached_logo = out_dir / "logo" / "logo.jpg"
    if cached_logo.exists():
        ctx["logo_path"] = str(cached_logo.relative_to(out_dir))
        phase_log.append(("Phase 3", "OK (from cache); logo.jpg"))
        successful.append("Phase 3")
    elif fb_handle:
        logo_path = fb_playwright.fetch_fb_profile_picture(fb_handle, out_dir)
        if logo_path:
            ctx["logo_path"] = str(logo_path.relative_to(out_dir))
            phase_log.append(("Phase 3", f"OK (live); saved {logo_path.name}"))
            successful.append("Phase 3")
        else:
            phase_log.append(("Phase 3", "[scrape-failed] FB profile picture endpoint returned non-200"))
            failed.append("Phase 3")
    else:
        phase_log.append(("Phase 3", "[gap] no FB handle to fetch logo from"))

    # Phase 4 continuation: FB scrape.
    fb_metadata: list[dict] = []
    cached_fb_dir = out_dir / "_cache" / "photos" / "fb"
    if cached_fb_dir.exists() and any(cached_fb_dir.iterdir()):
        for f in sorted(cached_fb_dir.iterdir()):
            if not f.is_file():
                continue
            target = photos_fb / f.name
            shutil.copy2(f, target)
            fb_metadata.append({
                "file": f.name,
                "url": None,
                "bytes": f.stat().st_size,
            })
        ctx["fb"] = {
            "page_url": f"https://www.facebook.com/{fb_handle}/" if fb_handle else "[gap]",
            "cover_photo": None,
            "page_photos": fb_metadata,
            "intro_text": None,
            "follower_count": None,
            "scrape_failed": False,
            "notes": ["restored from cache; intro/follower not re-scraped"],
        }
        phase_log.append(("Phase 4 (FB photos)", f"OK (from cache); {len(fb_metadata)} photos"))
        successful.append("Phase 4 FB cache")
    elif fb_handle:
        print(f"Phase 4 (cont): FB page scrape for {fb_handle} ...")
        fb_data = fb_playwright.scrape_fb_page(
            fb_handle, slug, out_dir, photos_dir=photos_fb,
        )
        ctx["fb"] = fb_data
        if fb_data.get("scrape_failed"):
            phase_log.append(("Phase 4 (FB scrape)", "[scrape-failed]"))
            failed.append("Phase 4 FB")
        else:
            phase_log.append((
                "Phase 4 (FB scrape)",
                f"OK; cover {'yes' if fb_data.get('cover_photo') else 'no'}, "
                f"{len(fb_data.get('page_photos', []))} page photos, "
                f"{fb_data.get('follower_count', '?')} followers"
            ))
            successful.append("Phase 4 FB")
        cover = fb_data.get("cover_photo")
        if cover:
            fb_metadata.append({
                "file": cover["file"],
                "url": cover.get("url"),
                "bytes": cover.get("bytes"),
            })
        for p in fb_data.get("page_photos") or []:
            fb_metadata.append({
                "file": p["file"],
                "url": p.get("url"),
                "bytes": p.get("bytes"),
            })
    else:
        ctx["fb"] = {}

    # Phase 5.
    phase_log.append((
        "Phase 5",
        "[v0.3-deferred] FL Division of Corporations registry lookup; "
        "first-name derivation runs after Phase 6"
    ))

    # Phase 6.
    print("Phase 6: GBP all-reviews scrape ...")
    cached_reviews = out_dir / "_cache" / "voice" / "reviews.json"
    cached_replies = out_dir / "_cache" / "voice" / "replies.json"
    if cached_reviews.exists():
        rev_doc = json.loads(cached_reviews.read_text(encoding="utf-8"))
        rep_doc = (
            json.loads(cached_replies.read_text(encoding="utf-8"))
            if cached_replies.exists() else {"replies": []}
        )
        review_records = rev_doc.get("reviews", [])
        reply_records = rep_doc.get("replies", [])
        ctx["reviews"] = review_records
        ctx["replies"] = reply_records
        ctx["saturation"] = rev_doc.get("saturation", {})
        sat_at = ctx["saturation"].get("saturated_at")
        phase_log.append((
            "Phase 6",
            f"OK (from cache); {len(review_records)} reviews, {len(reply_records)} replies, "
            f"saturated {'at #' + str(sat_at) if sat_at else 'NOT reached'}"
        ))
        successful.append("Phase 6 cache")
    else:
        rev_result = gbp_reviews_playwright.scrape_gbp_reviews(
            place_id, plateau_window=saturation_window
        )
        if rev_result.get("scrape_failed"):
            phase_log.append(("Phase 6", "[scrape-failed]"))
            failed.append("Phase 6")
            ctx["reviews"] = []
            ctx["replies"] = []
            ctx["saturation"] = {}
        else:
            review_records, reply_records = gbp_reviews_playwright.split_reviews_and_replies(
                rev_result["reviews"]
            )
            ctx["reviews"] = review_records
            ctx["replies"] = reply_records
            ctx["saturation"] = rev_result["saturation"]
            sat_at = rev_result["saturation"].get("saturated_at")
            phase_log.append((
                "Phase 6",
                f"OK (live); {len(review_records)} reviews, {len(reply_records)} replies, "
                f"saturated {'at #' + str(sat_at) if sat_at else 'NOT reached'}"
            ))
            successful.append("Phase 6")

    # Phase 7.
    print("Phase 7: derived signals ...")
    if ctx["reviews"]:
        owner_first, owner_n = derive_owner_first_name(
            ctx["reviews"] + ctx["replies"], business_display
        )
        ctx["owner_first_name"] = (owner_first, owner_n)
        phase_log.append((
            "Phase 7",
            f"OK; owner first name '{owner_first}' from {owner_n} mentions"
        ))
        successful.append("Phase 7")
    else:
        ctx["owner_first_name"] = (None, 0)
        phase_log.append(("Phase 7", "[skipped] no review corpus"))

    # Phase 8.
    print("Phase 8: logo color extraction ...")
    cached_palette = out_dir / "palette" / "extraction.json"
    logo_file = out_dir / "logo" / "logo.jpg"
    if cached_palette.exists():
        palette = json.loads(cached_palette.read_text(encoding="utf-8"))
        ctx["palette"] = palette
        clusters = palette.get("clusters") or []
        top_hex = clusters[0]["hex"] if clusters else "?"
        phase_log.append(("Phase 8", f"OK (from cache); {len(clusters)} clusters, top {top_hex}"))
        successful.append("Phase 8 cache")
    elif logo_file.exists():
        palette = kmeans_palette.extract_palette(
            logo_file, out_dir=out_dir / "palette"
        )
        ctx["palette"] = palette
        phase_log.append((
            "Phase 8",
            f"OK (live); {len(palette['clusters'])} clusters, top {palette['clusters'][0]['hex']}"
        ))
        successful.append("Phase 8")
    else:
        phase_log.append(("Phase 8", "[skipped] no logo file"))
        ctx["palette"] = {}

    # Phase 9: output composition.
    print("Phase 9: output composition ...")
    ctx["elapsed_sec"] = round(time.time() - t_start, 1)
    intake_md = render_intake(ctx)
    (audit_dir / "intake.md").write_text(intake_md, encoding="utf-8")

    # summary.json
    summary = build_summary_json(ctx)
    (data_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # reviews.json
    run_date = date.today()
    reviews_json = build_reviews_json(ctx["reviews"], ctx["replies"], run_date)
    (data_dir / "reviews.json").write_text(
        json.dumps(reviews_json, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # reviews.md
    reviews_md = build_reviews_md(
        ctx["reviews"], ctx["replies"], ctx.get("saturation") or {},
        business_display, run_date,
    )
    (audit_dir / "reviews.md").write_text(reviews_md, encoding="utf-8")

    # photos/manifest.json
    manifest = build_photo_manifest(photos, fb_metadata)
    (photos_root / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # README.md (root)
    customer_attributed_count = sum(
        1 for m in manifest if m["customer_attributed"] is True
    )
    readme_md = build_readme(
        ctx, pipeline_sha, slug, intake_md,
        gbp_count=len(photos),
        fb_count=len(fb_metadata),
        customer_attributed_count=customer_attributed_count,
    )
    (out_dir / "README.md").write_text(readme_md, encoding="utf-8")

    # process-notes.md (root)
    write_process_notes(out_dir, ctx)

    # Forcing-function check (intake only).
    passed, failing_lines = forcing_function_check(intake_md)
    if not passed:
        notes.append(f"Forcing-function check FAILED: {len(failing_lines)} ambiguous blanks")
        for ln in failing_lines[:5]:
            notes.append(f"  - {ln.strip()}")
        phase_log.append(("Phase 9", f"FAIL; {len(failing_lines)} ambiguous blanks"))
        write_process_notes(out_dir, ctx)
        return 1
    phase_log.append((
        "Phase 9",
        "OK; v0.2 layout written (README + audit/ + process-notes); forcing-function passed"
    ))
    successful.append("Phase 9")

    # Clean up cache scratch dir if present.
    cache_scratch = out_dir / "_cache"
    if cache_scratch.exists():
        shutil.rmtree(cache_scratch)

    write_process_notes(out_dir, ctx)

    # Phase 10.
    repo_url = None
    if publish and not dry_run:
        commit_msg = f"v0.2: restructure to Design seat spec"
        print(f"Phase 10: GitHub publish to ron841/grm-prospect-{slug} ...")
        repo_url = github_publish(slug, out_dir, commit_message=commit_msg)
        if repo_url:
            phase_log.append(("Phase 10", f"OK; {repo_url}"))
            successful.append("Phase 10")
        else:
            phase_log.append(("Phase 10", "[failed] gh repo create / push rejected"))
            failed.append("Phase 10")
        write_process_notes(out_dir, ctx)
    else:
        phase_log.append(("Phase 10", "[skipped] --no-publish or --dry-run"))
        write_process_notes(out_dir, ctx)

    # Final summary.
    elapsed = round(time.time() - t_start, 1)
    print()
    print(f"=== prospect-audit-social {SKILL_VERSION} complete in {elapsed}s ===")
    print(f"Workspace: {out_dir}")
    if repo_url:
        print(f"GitHub: {repo_url}")
    print(f"Photos: {len(photos)} GBP + {len(fb_metadata)} FB")
    sat_at = (ctx.get("saturation") or {}).get("saturated_at")
    print(
        f"Reviews captured: {len(ctx.get('reviews', []))} "
        f"(saturation {'reached at #' + str(sat_at) if sat_at else 'NOT reached'})"
    )
    print(f"Replies captured: {len(ctx.get('replies', []))}")
    if (ctx.get("palette") or {}).get("clusters"):
        clusters = ctx["palette"]["clusters"]
        print(f"Palette: top {clusters[0]['hex']}, {len(clusters)} clusters")
    print(f"Successful phases: {len(successful)}; failed: {len(failed)}")
    print(f"grm-pipeline pinned at: {pipeline_sha} (source: {pipeline_sha_source})")
    return 0


def main():
    ap = argparse.ArgumentParser(description=f"prospect-audit-social {SKILL_VERSION} orchestrator")
    ap.add_argument("business_name")
    ap.add_argument("place_id_or_url")
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--fb-handle", default=None)
    ap.add_argument("--saturation-window", type=int, default=5)
    ap.add_argument("--no-publish", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--from-cache", type=Path, default=None,
        help="path to a directory holding scraped artifacts to reuse "
             "instead of re-running scrapers (gbp-raw.json, voice-corpus/, "
             "images/ or audit/photos/, logo/, palette/)",
    )
    args = ap.parse_args()

    place_id = parse_place_id(args.place_id_or_url)
    slug = slugify(args.business_name)
    out_dir = args.out or (PROSPECTS_ROOT / slug)

    return run(
        args.business_name,
        place_id,
        out_dir=out_dir,
        fb_handle=args.fb_handle,
        saturation_window=args.saturation_window,
        publish=not args.no_publish,
        dry_run=args.dry_run,
        from_cache=args.from_cache,
    )


if __name__ == "__main__":
    sys.exit(main())

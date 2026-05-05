"""
Multi-source review deduplication.

Public surfaces (Google, Birdeye, Yelp, Facebook recommendations) often
carry the same review on different platforms. Capture is multi-source;
storage is deduplicated.

Dedup key per pipeline contract:
  author_name + date + first_30_chars_of_review_body

Duplicates across platforms are confidence boosters, surfaced inline as
a count next to the canonical entry. They are not stored as separate
review entries.

This module is deliberately small and pure. No I/O, no API calls. The
caller passes review dicts in and receives canonical entries back.
"""

from __future__ import annotations

import re
from typing import Iterable


def normalize_for_key(s: str | None) -> str:
    """Normalize a string for dedup-key comparison.

    Lowercases, strips punctuation, collapses whitespace. Returns ""
    when input is None or empty.
    """
    if not s:
        return ""
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def review_key(review: dict) -> str:
    """Build the canonical dedup key for a review record.

    The review dict is expected to carry:
      - author or author_name
      - date or relative_date (any string)
      - body or text

    Duplicates produce identical keys regardless of which surface they
    came from.
    """
    author = review.get("author") or review.get("author_name") or ""
    date = review.get("date") or review.get("relative_date") or ""
    body = review.get("body") or review.get("text") or ""
    body_30 = body[:30]
    return "|".join([
        normalize_for_key(author),
        normalize_for_key(date),
        normalize_for_key(body_30),
    ])


def dedupe(reviews: Iterable[dict]) -> tuple[list[dict], dict[str, int]]:
    """Collapse duplicates and return (canonical_list, confidence_boost_map).

    Strategy:
      - First-seen wins as the canonical entry.
      - Subsequent duplicates increment a confidence counter keyed by
        the dedup key.
      - Each canonical entry gets a "confidence_boost" field equal to
        the number of duplicate sightings (0 if seen only once).
      - Each canonical entry gets a "sources_seen" list tracking which
        surfaces reported it.

    Returns (canonical_list, key->boost map).
    """
    canonical: dict[str, dict] = {}
    boost: dict[str, int] = {}

    for r in reviews:
        k = review_key(r)
        if not k.strip("|"):
            # Fully-empty key, e.g. malformed review. Skip.
            continue
        if k not in canonical:
            entry = dict(r)
            entry["confidence_boost"] = 0
            entry["sources_seen"] = [r.get("source", "unknown")]
            canonical[k] = entry
            boost[k] = 0
        else:
            boost[k] += 1
            canonical[k]["confidence_boost"] = boost[k]
            src = r.get("source", "unknown")
            if src not in canonical[k]["sources_seen"]:
                canonical[k]["sources_seen"].append(src)

    return list(canonical.values()), boost


# Inline self-test. Run `python3 dedup.py` to see the assertions pass.
if __name__ == "__main__":
    sample = [
        {"author": "Diane Bennett", "relative_date": "2 months ago",
         "text": "Anthony did a great job on the pool deck",
         "source": "GBP"},
        {"author": "Diane Bennett", "relative_date": "2 months ago",
         "text": "Anthony did a great job on the pool deck",
         "source": "Birdeye"},  # duplicate via dedup key
        {"author": "Cole Spires", "relative_date": "3 weeks ago",
         "text": "Showed up on time and finished early",
         "source": "GBP"},
        {"author": "diane bennett", "relative_date": "2 months ago",
         "text": "ANTHONY DID A GREAT JOB on the pool deck",
         "source": "Yelp"},  # duplicate via case-insensitive normalize
        {"author": "", "relative_date": "", "text": "", "source": "GBP"},
    ]
    canon, boost_map = dedupe(sample)
    assert len(canon) == 2, f"expected 2 canonical, got {len(canon)}: {canon}"
    diane = next(c for c in canon if "diane" in c["author"].lower())
    assert diane["confidence_boost"] == 2, diane
    assert set(diane["sources_seen"]) == {"GBP", "Birdeye", "Yelp"}, diane
    cole = next(c for c in canon if "cole" in c["author"].lower())
    assert cole["confidence_boost"] == 0
    print("dedup.py self-test passed")
    print(f"  canonical: {len(canon)}")
    print(f"  diane boost: {diane['confidence_boost']}, sources: {diane['sources_seen']}")
    print(f"  cole boost: {cole['confidence_boost']}, sources: {cole['sources_seen']}")

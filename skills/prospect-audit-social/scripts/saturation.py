"""
Evidence-saturation tracking for review capture.

Saturation rule from the pipeline contract:

  Saturation is reached when the marginal next capture adds zero new
  evidence. For reviews specifically, this means zero new job-nouns and
  zero new praise-pattern clusters. Track distinct categories as
  captures accumulate and stop when both plateau.

This module is pure logic. The caller feeds reviews one at a time (or
in batches) and asks "saturated yet?" after each. The plateau window K
is configurable; the contract suggests 5.

Job-noun categories: contractor-class jobs the operator does. The list
is conservative for v0.1; extend per category in v0.2.

Praise-pattern categories: differentiator-grade praise. Match against
operator-facing language in reviews.
"""

from __future__ import annotations

import re
from collections import Counter

# Job-noun categories. Each key is the canonical category name; the
# value is a list of regex patterns (case-insensitive). A review that
# matches any pattern under a category counts as one occurrence of that
# category. Multiple patterns OR together within a category.
JOB_NOUN_PATTERNS: dict[str, list[str]] = {
    "carpentry": [r"\bcarpent", r"\btrim\b", r"\bbaseboard", r"\bmolding", r"\bcabinet"],
    "drywall": [r"\bdrywall", r"\bsheetrock", r"\bspackle", r"\bdrywall\s+repair"],
    "painting": [r"\bpaint(?:ing|ed|er)?\b"],
    "tile": [r"\btile\b", r"\btiled\b", r"\bgrout"],
    "plumbing": [r"\bplumb(?:ing|er|ed)?\b", r"\bdrain\b", r"\btoilet", r"\bfaucet", r"\bsink\b"],
    "electrical": [r"\belectric(?:al|ian)?\b", r"\boutlet", r"\bbreaker", r"\bcircuit", r"\bwiring"],
    "deck-pergola": [r"\bdeck\b", r"\bpergola", r"\bgazebo"],
    "fence": [r"\bfenc(?:e|ing)\b"],
    "door-window": [r"\bdoor\b", r"\bwindow"],
    "drywall-ceiling": [r"\bceiling", r"\bpopcorn"],
    "roofing": [r"\broof"],
    "flooring": [r"\bfloor(?:ing|ed)?\b", r"\blaminate", r"\bvinyl plank", r"\bhardwood"],
    "pressure-wash": [r"\bpressure\s*wash", r"\bsoft\s*wash", r"\bpower\s*wash"],
    "landscaping": [r"\blandscap", r"\bmow", r"\btrim\s+hedge", r"\btree", r"\bsod\b"],
    "pool-service": [r"\bpool\s+(?:service|cleaning|chem)", r"\bpool\s+pump", r"\bchlorine"],
    "septic": [r"\bseptic", r"\bdrain\s*field"],
    "hvac": [r"\bhvac", r"\ba/?c\b", r"\bair\s+condition", r"\bfurnace", r"\bheat\s+pump"],
    "pest-control": [r"\bpest", r"\bexterminat", r"\btermite"],
    "auto-repair": [r"\bbrake", r"\boil\s+change", r"\btire", r"\balignment", r"\btransmission"],
    "general-handyman": [r"\bhandym(?:a|e)n", r"\bsmall\s+job", r"\bodd\s+jobs?", r"\bpunch\s+list"],
}

# Praise-pattern categories. Same shape: category -> list of regex.
PRAISE_PATTERNS: dict[str, list[str]] = {
    "quality-finish": [r"\bquality", r"\bcraft", r"\bmeticulous", r"\bperfectionist",
                       r"\bdetail", r"\bhigh[- ]end", r"\bfurniture[- ]grade"],
    "on-time": [r"\bon\s+time", r"\btime(?:ly)?\b", r"\bpunctual", r"\bquick",
                r"\bsame\s+day", r"\bnext\s+day", r"\bright\s+away",
                r"\bfast(?:er)?\b"],
    "fair-price": [r"\bfair\b", r"\baffordab", r"\breasonab(?:le|ly)\b",
                   r"\bgreat\s+price", r"\bgood\s+price", r"\bvalue", r"\bworth\s+every"],
    "communication": [r"\bcommunicat", r"\bresponsive", r"\bkept\s+me\s+informed",
                      r"\beasy\s+to\s+(?:reach|talk)", r"\breturn(?:ed|s)\s+(?:my\s+)?call"],
    "honesty": [r"\bhonest", r"\btrust", r"\bintegrity", r"\bno\s+nonsense",
                r"\bstraightforward", r"\bup[- ]?front", r"\btransparent"],
    "cleanup": [r"\bclean\s*(?:up|ed)", r"\bleft\s+(?:my|the)\s+(?:place|home|house|yard)\s+clean"],
    "professional": [r"\bprofessional"],
    "friendly": [r"\bfriendly", r"\bnice\s+(?:guy|man|person)", r"\bpolite", r"\bcourteous",
                 r"\bkind", r"\bpleasant"],
    "knowledgeable": [r"\bknowledg", r"\bexperienc", r"\bskilled?", r"\bexpert",
                      r"\bknew\s+(?:exactly\s+)?what"],
    "follow-through": [r"\bfollow[- ]?(?:through|up)", r"\bfinish(?:ed)?\s+the\s+job",
                       r"\bdid\s+what\s+(?:he|she|they)\s+said"],
    "would-recommend": [r"\b(?:high(?:ly)?\s+)?recommend", r"\brecommended\s+to",
                        r"\bcall\s+(?:him|her|them)\s+again", r"\bonly\s+person\s+(?:i|we)"],
    "saved-money": [r"\bsaved\s+(?:me|us)", r"\bsaved\s+\$"],
    "competitor-comparison": [r"\bother\s+(?:companies|guys|contractors)\s+(?:quoted|wanted|charged)",
                              r"\b\$\d+\s*(?:[-–]|to)\s*\$\d+"],
}


def categorize_review(text: str | None,
                       patterns: dict[str, list[str]]) -> set[str]:
    """Return the set of categories that match somewhere in text."""
    if not text:
        return set()
    out = set()
    for cat, regexes in patterns.items():
        for pat in regexes:
            if re.search(pat, text, flags=re.IGNORECASE):
                out.add(cat)
                break
    return out


class SaturationTracker:
    """Tracks when distinct categories stop growing.

    Usage:
      t = SaturationTracker(plateau_window=5)
      for r in reviews_in_capture_order:
          t.add(r["text"])
          if t.saturated():
              break
      tables = t.frequency_tables()
    """

    def __init__(self, plateau_window: int = 5,
                 job_patterns: dict | None = None,
                 praise_patterns: dict | None = None) -> None:
        self.plateau_window = plateau_window
        self.job_patterns = job_patterns or JOB_NOUN_PATTERNS
        self.praise_patterns = praise_patterns or PRAISE_PATTERNS
        self.reviews_seen = 0
        self.distinct_jobs: set[str] = set()
        self.distinct_praises: set[str] = set()
        self.job_counter: Counter = Counter()
        self.praise_counter: Counter = Counter()
        # Per-step trace: (review_idx, distinct_jobs_count,
        # distinct_praises_count). Used by the saturation-tables
        # output to show the growth curve.
        self.trace: list[tuple[int, int, int]] = []
        # Indices at which a NEW category appeared. Plateau is detected
        # when neither set of indices has grown in the last K captures.
        self._last_new_job_idx = 0
        self._last_new_praise_idx = 0
        # Saturation point: review index at which both stopped growing
        # for plateau_window captures. None until reached.
        self.saturated_at: int | None = None

    def add(self, text: str | None) -> None:
        self.reviews_seen += 1
        idx = self.reviews_seen

        jobs = categorize_review(text, self.job_patterns)
        praises = categorize_review(text, self.praise_patterns)

        for j in jobs:
            self.job_counter[j] += 1
            if j not in self.distinct_jobs:
                self.distinct_jobs.add(j)
                self._last_new_job_idx = idx
        for p in praises:
            self.praise_counter[p] += 1
            if p not in self.distinct_praises:
                self.distinct_praises.add(p)
                self._last_new_praise_idx = idx

        self.trace.append((idx, len(self.distinct_jobs),
                           len(self.distinct_praises)))

        # Saturation check: both sets have been stable for plateau_window.
        if self.saturated_at is None:
            jobs_stable = (idx - self._last_new_job_idx) >= self.plateau_window
            praises_stable = (idx - self._last_new_praise_idx) >= self.plateau_window
            if jobs_stable and praises_stable and idx >= self.plateau_window:
                self.saturated_at = idx

    def saturated(self) -> bool:
        return self.saturated_at is not None

    def frequency_tables(self) -> dict:
        return {
            "jobs": dict(self.job_counter.most_common()),
            "praises": dict(self.praise_counter.most_common()),
            "saturated_at": self.saturated_at,
            "reviews_seen": self.reviews_seen,
            "distinct_jobs_count": len(self.distinct_jobs),
            "distinct_praises_count": len(self.distinct_praises),
            "last_new_job_at": self._last_new_job_idx,
            "last_new_praise_at": self._last_new_praise_idx,
            "plateau_window": self.plateau_window,
        }

    def to_markdown(self) -> str:
        """Render the saturation tables as markdown.

        Format mirrors intake-template-v2 §7.
        """
        lines = ["# Voice Saturation Tables", ""]
        lines.append(f"- Reviews captured: {self.reviews_seen}")
        if self.saturated_at:
            lines.append(f"- Saturation reached at review #{self.saturated_at} (plateau window K={self.plateau_window})")
        else:
            lines.append(f"- Saturation NOT reached at review #{self.reviews_seen}; corpus exhausted before plateau (plateau window K={self.plateau_window})")
        lines.append(f"- Distinct job categories matched: {len(self.distinct_jobs)} (last new at #{self._last_new_job_idx})")
        lines.append(f"- Distinct praise categories matched: {len(self.distinct_praises)} (last new at #{self._last_new_praise_idx})")
        lines.append("")
        lines.append("## Job-noun frequency")
        lines.append("")
        lines.append("| Job category | Reviews mentioning |")
        lines.append("| --- | --- |")
        for cat, n in self.job_counter.most_common():
            lines.append(f"| {cat} | {n} |")
        lines.append("")
        lines.append("## Praise-pattern frequency")
        lines.append("")
        lines.append("| Praise category | Reviews mentioning |")
        lines.append("| --- | --- |")
        for cat, n in self.praise_counter.most_common():
            lines.append(f"| {cat} | {n} |")
        lines.append("")
        lines.append("## Growth trace")
        lines.append("")
        lines.append("| Review # | Distinct jobs | Distinct praises |")
        lines.append("| --- | --- | --- |")
        for idx, j, p in self.trace:
            lines.append(f"| {idx} | {j} | {p} |")
        return "\n".join(lines) + "\n"


# Inline self-test.
if __name__ == "__main__":
    fake_reviews = [
        "Anthony did a great job painting our living room. Quality finish, on time.",
        "He fixed our drywall hole. Clean, professional, fair price.",
        "Tile work in the bathroom looked perfect. Highly recommend.",
        "Trim and baseboards installed beautifully. Honest guy.",
        "Repaired our deck. Showed up on time and finished early.",
        "Did some carpentry on our pergola. Friendly and knowledgeable.",
        "More painting in the kitchen. Quality finish again.",
        "Cleaned up after the job. Reasonable price.",
        "Drywall repair, trim, baseboards. Same crew, same quality.",
        "Painting touch-up. On time again.",
        "Painting the garage. Same quality.",
    ]
    t = SaturationTracker(plateau_window=3)
    for r in fake_reviews:
        t.add(r)
        if t.saturated():
            break
    assert t.saturated_at is not None, "expected saturation to trigger"
    tables = t.frequency_tables()
    assert tables["distinct_jobs_count"] >= 4, tables
    assert tables["distinct_praises_count"] >= 4, tables
    print("saturation.py self-test passed")
    print(f"  saturated at: {tables['saturated_at']}")
    print(f"  distinct jobs: {tables['distinct_jobs_count']}")
    print(f"  distinct praises: {tables['distinct_praises_count']}")

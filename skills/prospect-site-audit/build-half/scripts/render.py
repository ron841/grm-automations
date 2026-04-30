#!/usr/bin/env python3
"""render.py — the band template engine for prospect-build (v1.0).

Reads a profile.json + prose.json, applies the per-band decision rules from
the audit-side spec set (typography.md, section-patterns.md, hero-patterns.md,
image-handling.md), and renders each band into HTML.

Deterministic. Does NOT call any LLM. Prose comes from prose.json, which the
executing Claude authors per the audit-side voice contract (voiceMap.md +
content-rules.md + anti-slop-rules.md) against the slot vocabulary in
references/fixture-contract.md.

Usage:
    python3 render.py \\
        --profile /path/to/profile.json \\
        --prose   /path/to/prose.json \\
        --out     /path/to/output/Homepage.html \\
        [--photos-root /path/to/photos/]
        [--css-href ../../css/composer-system.css]

If --photos-root is given, photo references in the profile are made relative to
the output file's parent. Otherwise they're passed through as-is.

Exit code 0 = rendered successfully (may still have warnings).
Exit code 1 = rendered with at least one §7 validation failure.
Exit code 2 = could not render at all (data shape blocker).
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Callable


# ============================================================================
# 1. COLOR UTILITIES
# ============================================================================

def hex_to_rgb(h: str) -> tuple[int, int, int]:
    """Parse #rrggbb to (r,g,b)."""
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c*2 for c in h)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(*(max(0, min(255, int(c))) for c in rgb))


def _hex_to_rgb_tuple(h: str) -> str:
    """Format a #rrggbb hex as 'R, G, B' for CSS rgb()/rgba() consumption.
    The bundle vocabulary uses rgba(var(--color-primary-rgb), 0.10) patterns;
    this helper feeds the per-prospect tuple into palette_override so the
    bundle vocabulary tints correctly for non-JSL prospects."""
    r, g, b = hex_to_rgb(h)
    return f"{r}, {g}, {b}"


def darken(h: str, pct: float) -> str:
    """Return a hex color `pct` percent darker (0..1)."""
    r, g, b = hex_to_rgb(h)
    return rgb_to_hex((r * (1 - pct), g * (1 - pct), b * (1 - pct)))


def lighten(h: str, pct: float) -> str:
    r, g, b = hex_to_rgb(h)
    return rgb_to_hex((r + (255 - r) * pct, g + (255 - g) * pct, b + (255 - b) * pct))


def brightness(h: str) -> float:
    """Perceived brightness 0..255 using the relative-luminance approximation."""
    r, g, b = hex_to_rgb(h)
    return 0.299 * r + 0.587 * g + 0.114 * b


# ============================================================================
# 2. PROFILE LOADER (handles the Villages-audit shape)
# ============================================================================

def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def pick(obj: dict, *path, default=None):
    """Pick nested keys safely. pick(d, 'a','b','c') == d.get('a',{}).get('b',{}).get('c')."""
    cur: Any = obj
    for key in path:
        if isinstance(cur, dict):
            cur = cur.get(key)
        else:
            return default
        if cur is None:
            return default
    return cur


def owner_full_name(o: dict) -> str:
    """Read an owner's full name from either schema and return "" if neither populates.

    Two captured owner shapes ship across the prospect corpus:
      - {"name": "Jeff Testerman", ...}              (current — used by Testerman's)
      - {"firstName": "Jeff", "lastName": "Testerman", ...}  (legacy — used by Volthom)

    The cred + story-grid renderers must accept both. Returning "" lets callers
    drop-cleanly per P14 (attribution data-binding integrity): if the name field
    is empty the entire {name + comma + role} unit suppresses, no leading commas,
    no orphaned roles.
    """
    name = (o.get("name") or "").strip()
    if name:
        return name
    parts = f'{o.get("firstName") or ""} {o.get("lastName") or ""}'.strip()
    return parts


def validate_data_claim(
    profile: dict,
    path: tuple[str, ...],
    coerce: Callable[[Any], Any] | None = None,
    floor: Callable[[Any], bool] | None = None,
) -> Any | None:
    """Read a value from profile and return it only when supported by data.

    Implements the read / coerce / floor-check triple that every band resolver
    currently open-codes per rule. Absorbs (TypeError, ValueError) from both
    coerce and floor so callers pass clean lambdas without wrapping their own
    error handling — the list-length case where len() on a None or
    non-iterable would raise is the concrete reason for the floor wrap.

    When to use
    -----------
    Use this utility where the read+coerce+floor combination applies — where
    a per-claim data check governs whether to emit a tile, item, or field.
    Use pick() where just the read is needed: default-to-empty list lookups,
    structural any() over a list of dicts, substring scans, simple
    multi-source OR truthiness chains without coerce or floor. Keep the
    utility narrow; its meaning is "I'm validating a data claim against a
    floor."

    Parameters
    ----------
    profile : dict
        Profile root dict; same shape pick() consumes.
    path : tuple[str, ...]
        Nested key path passed to pick() (e.g. ("googleBusiness", "rating")).
    coerce : callable, optional
        Type/format conversion applied to the picked value (e.g. int, float).
        None → return raw picked value when the floor passes.
    floor : callable, optional
        Predicate applied to the coerced value (e.g. lambda r: r >= 4.95).
        None → always-pass.

    Returns
    -------
    The coerced value when path resolves, coerce succeeds, and floor passes.
    None otherwise. Drop-when-unsupported as data: callers branch on the None
    sentinel rather than catching exceptions.

    Examples
    --------
        rating = validate_data_claim(
            profile,
            ("googleBusiness", "rating"),
            coerce=float,
            floor=lambda r: r >= 4.95,
        )

        owners = validate_data_claim(
            profile,
            ("owners", "list"),
            floor=lambda lst: isinstance(lst, list) and len(lst) >= 2,
        )
    """
    raw = pick(profile, *path)
    if raw is None:
        return None
    try:
        value = coerce(raw) if coerce is not None else raw
    except (TypeError, ValueError):
        return None
    if floor is not None:
        try:
            if not floor(value):
                return None
        except (TypeError, ValueError):
            return None
    return value


def normalize_phone(p: str | None) -> str:
    """Normalize a phone string to '(xxx) xxx-xxxx' for display."""
    if not p:
        return ""
    digits = re.sub(r"\D", "", p)
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    if len(digits) == 10:
        return f"({digits[0:3]}) {digits[3:6]}-{digits[6:10]}"
    return p  # unknown shape, pass through


def phone_tel_href(p: str) -> str:
    digits = re.sub(r"\D", "", p or "")
    if len(digits) == 10:
        return f"tel:+1{digits}"
    if len(digits) == 11 and digits.startswith("1"):
        return f"tel:+{digits}"
    return f"tel:{digits}"


# ============================================================================
# 3. §2 DECISION TABLES
# ============================================================================

FALLBACK_PALETTE = {
    "primary":       "#3d5a2a",
    "primary_deep":  "#233514",
    "dark_primary":  "#162110",
    "accent":        "#c67b3c",
    "accent_deep":   "#8f4217",
    "background":    "#f5efe3",
    "paper_warm":    "#ece4d2",
    "cream":         "#faf5e9",
    "ink":           "#1a1f14",
    "ink_2":         "#2f3526",
    "manifesto_band": "#f7f2e8",  # editorial warm-break fallback when no palette signal qualifies
}


def _is_warm(hex_color: str, min_r_dominance: int = 10) -> bool:
    """Return True when red is the dominant channel by at least `min_r_dominance`.
    Catches amber / rust / warm-paper; rejects forest greens and cool blues that
    might happen to have r > b by a hair."""
    r, g, b = hex_to_rgb(hex_color)
    return r > max(g, b) + min_r_dominance


def _is_warm_cream(hex_color: str) -> bool:
    """Warm cream = already in the editorial manifesto-band range: light (min
    channel above ~222) and red >= blue (i.e. not cool)."""
    r, g, b = hex_to_rgb(hex_color)
    return min(r, g, b) > 222 and r >= b


def resolve_manifesto_band(resolved_palette: dict) -> tuple[str, str]:
    """Pick the manifesto-band warm-break color from the resolved palette.

    Rules (first match wins):
      1. If `background` is already a warm cream (light + r>=b), use it as-is.
         Warm-palette brands like JSL (#f5efe3) land here.
      2. Else try `accent`, then `primary`. If a candidate is warm (r dominant),
         mix 88% warm-cream fallback + 12% candidate so the manifesto band picks
         up a subtle tint from the brand's warm side. Cool-palette brands with a
         warm accent (Volthom: navy primary + amber accent) land here.
      3. Else fall back to #f7f2e8 — a neutral editorial warm cream.

    Returns (hex_color, derivation_note) so the caller can log what was chosen.
    """
    bg = resolved_palette.get("background", "")
    if bg.startswith("#") and _is_warm_cream(bg):
        return bg, f"background ({bg}) is already warm cream — used as-is"

    fallback = FALLBACK_PALETTE["manifesto_band"]
    f_r, f_g, f_b = hex_to_rgb(fallback)

    for role in ("accent", "primary"):
        candidate = resolved_palette.get(role)
        if not (candidate and candidate.startswith("#") and _is_warm(candidate)):
            continue
        c_r, c_g, c_b = hex_to_rgb(candidate)
        mix = 0.88  # 88% warm cream + 12% brand warm color
        new_r = f_r * mix + c_r * (1 - mix)
        new_g = f_g * mix + c_g * (1 - mix)
        new_b = f_b * mix + c_b * (1 - mix)
        derived = rgb_to_hex((new_r, new_g, new_b))
        return derived, f"derived from {role} ({candidate}) at 88/12 mix with fallback {fallback}"

    return fallback, f"no warm palette signal — fell back to {fallback}"


def resolve_palette(profile: dict) -> dict:
    """§2.2: map profile.brandPalette to composer tokens. Defaults to the JSL
    reference palette when the audit didn't resolve colors (text-wordmark sites)."""
    bp = profile.get("brandPalette") or {}
    pd = bp.get("proposedDefaults") or {}

    def get_color(*keys, fallback_key):
        for k in keys:
            v = bp.get(k) or pd.get(k)
            if v and isinstance(v, str) and v.startswith("#"):
                return v
        return FALLBACK_PALETTE[fallback_key]

    primary = get_color("primary", fallback_key="primary")
    dark_primary = get_color("darkPrimary", "dark_primary", fallback_key="dark_primary")
    accent = get_color("accent", fallback_key="accent")
    background = get_color("background", fallback_key="background")

    # Never pure-white background
    if brightness(background) > 250:
        background = FALLBACK_PALETTE["background"]

    palette = {
        "primary":      primary,
        "primary_deep": darken(primary, 0.18) if primary != FALLBACK_PALETTE["primary"] else "#233514",
        "dark_primary": dark_primary,
        "accent":       accent,
        "accent_deep":  darken(accent, 0.22) if accent != FALLBACK_PALETTE["accent"] else "#8f4217",
        "background":   background,
        "paper_warm":   darken(background, 0.05),
        "cream":        lighten(background, 0.05),
        "ink":          FALLBACK_PALETTE["ink"],
        "ink_2":        FALLBACK_PALETTE["ink_2"],
    }
    # Patch (2026-04-24): manifesto-band warm-break reads its own palette role.
    # Derivation in resolve_manifesto_band() — see docstring there.
    manifesto_band, manifesto_note = resolve_manifesto_band(palette)
    palette["manifesto_band"] = manifesto_band
    palette["manifesto_band_note"] = manifesto_note
    return palette


def resolve_hero_photo(profile: dict, photos_root: str | None) -> dict:
    """§2.1: pick the hero photo. Returns {path, caption_label, warnings}."""
    warnings: list[str] = []
    # Prefer pre-ranked heroCandidatesTop5 from the audit
    top5 = pick(profile, "photoLibrary", "heroCandidatesTop5") or []
    if not top5:
        # Fall back to heroCandidatesAll
        top5 = (pick(profile, "photoLibrary", "heroCandidatesAll") or [])[:5]
    # v1.1 Session 2 Patch 4: respect author-tagged disqualifyFromHero
    # so award plaques / watermarked marketing collages / display-piece
    # photos never surface as hero rotation slides or single-hero anchors.
    top5 = _filter_hero_candidates(top5, profile)

    if not top5:
        warnings.append("No hero candidates in profile. Hero band will render with a placeholder.")
        return {"path": "", "warnings": warnings}

    # v1 rule: take the top-ranked candidate. Real §2.1 scoring (score >= 80,
    # subject classifier) lands in v1.1 when the audit provides classifier tags.
    chosen = top5[0]
    # The audit stores paths relative to the prospect workspace root
    # (e.g., "assets/photos/google/gp-09.jpg"). Keep the relative form;
    # the caller rewrites for --photos-root.
    return {
        "path":           chosen,
        "warnings":       warnings,
    }


def resolve_brand_mark_html(photos_root: str | None, out_dir: "Path", profile: dict | None = None, for_inner_page: bool = False) -> str:
    """Priority chain: profile.logo.localPath (per-prospect brand mark) →
    assets/photos/site/site-09.jpg (Volthom convention "brand swirl") →
    wordmark_svg() inline-SVG placeholder.

    Returns ready-to-embed HTML for the .wm-mark slot in the sitenav and
    footer wordmarks. Logo path read from profile.logo.localPath when set
    (S3-6 fix Session 3 close, 2026-04-29 — generalizes brand-mark resolver
    beyond the Volthom site-09 convention).

    Width/height attributes are intentionally omitted on profile.logo
    emit so wide-aspect-ratio lockups (e.g., illustrated character +
    wordmark) render at their natural ratio under the .wm-mark CSS rule
    (height-controlled, width:auto). The Volthom site-09 fallback ships
    34×34 because that swirl is square. Round-2 diagnostic Session 3
    close (2026-04-29) — wm-mark slot was shaped for square logos only.

    for_inner_page (Round-4-cleanup, 2026-04-29): when True, prefers
    profile.logo.fallbackLocalPath over .localPath. Round-3 set primary
    logo to a white-on-transparent variant designed for the homepage's
    navy hero header; that variant is invisible on inner pages where the
    sitenav uses a sticky-translucent cool-white treatment (composer-system
    .css line 1278+). The fallback (color JPG) is the right variant for
    light-bg inner-page contexts. Engine principle for v1.1 P11 — header
    treatment dictates logo variant; default to context-matched.
    """
    from pathlib import Path
    if photos_root:
        if profile:
            logo_obj = profile.get("logo") or {}
            logo_local = ""
            primary_logo = logo_obj.get("localPath", "")
            if for_inner_page:
                # Inner-page color-variant fallback only fires when there IS a primary logo.
                # Without primary, inner-page path falls through to wordmark_svg() — matches
                # homepage emit for no-logo prospects (Goney's first instance, 2026-04-29).
                logo_local = (logo_obj.get("fallbackLocalPath") or primary_logo) if primary_logo else ""
            else:
                logo_local = primary_logo
            if logo_local and (Path(photos_root) / logo_local).exists():
                href = _photo_href(logo_local, photos_root, out_dir)
                return f'<img src="{href}" alt="" loading="eager">'
        site_09_rel = "assets/photos/site/site-09.jpg"
        if (Path(photos_root) / site_09_rel).exists():
            href = _photo_href(site_09_rel, photos_root, out_dir)
            return f'<img src="{href}" alt="" loading="eager" width="34" height="34">'
    return wordmark_svg()


def resolve_stats_trio(profile: dict) -> list[dict]:
    """§2.4: return up to 3 stat dicts in priority order.

    the strongest stat (first match in priority order)
    becomes the LEAD stat — rendered at a significantly larger size. Google
    review count is reshaped so the count (199) is the headline number and
    the rating sits inside the supporting label ("5.0★ Google reviews").
    Slots 2 and 3 stay secondary at a demoted size. Every stat dict now
    carries a `lead` boolean consumed by render_hero.
    """
    stats: list[dict] = []

    rating = validate_data_claim(
        profile, ("googleBusiness", "rating"), coerce=float, floor=lambda r: r >= 4.5
    )
    review_count = validate_data_claim(
        profile, ("googleBusiness", "reviewCount"), coerce=int, floor=lambda n: n > 0
    )
    if rating is not None and review_count is not None:
        # Lead-optimized: review count is the dominant number, rating rides in the label.
        stats.append({
            "value_main": f"{review_count}",
            "value_em": "",
            "label": f"{rating:.1f}★ Google reviews",
        })

    gallery_count = validate_data_claim(
        profile, ("photoLibrary", "galleryPhotoCount"), coerce=int, floor=lambda n: n >= 50
    )
    if gallery_count is not None:
        stats.append({
            "value_main": f"{gallery_count}",
            "value_em": "+",
            "label": "Projects in gallery",
        })

    # Awards-derived hero stat is omitted by design: placeholder strings
    # ("Award" / "Winning design") were template leftovers, the awards string
    # is the wrong shape for a 2-3 word stat tile, and the full award text
    # lives in the About cred-grid where it belongs.

    # Years-in-business OR-chain with coerce+floor: the validate_data_claim
    # form gives fall-through-on-floor-fail semantics (matches the rule
    # fall-through in resolve_distinguishing_stat). Old code's
    # truthiness-short-circuit BEFORE coerce+floor could lock in a sub-floor
    # value at the first source even when the second source had a viable one.
    years = (
        validate_data_claim(
            profile, ("credentials", "yearsInBusiness"), coerce=int, floor=lambda n: n >= 10
        )
        or validate_data_claim(
            profile, ("credentials", "yearsInBusinessStated"), coerce=int, floor=lambda n: n >= 10
        )
    )
    if years is not None:
        city = pick(profile, "contact", "addressConsensus") or ""
        city_first = city.split(",")[0].strip() if city else ""
        if not city_first:
            cities = pick(profile, "contact", "serviceAreaCities") or []
            counties = pick(profile, "contact", "serviceAreaCounties") or []
            city_first = (cities[0] if cities else "") \
                      or (counties[0] if counties else "") \
                      or ""
        label = f"Years in {city_first}" if city_first else "Years in business"
        stats.append({
            "value_main": f"{years}",
            "value_em": "",
            "label": label,
        })

    crew_size = validate_data_claim(
        profile, ("team",), floor=lambda lst: isinstance(lst, list) and len(lst) >= 10
    )
    if crew_size is not None:
        stats.append({
            "value_main": f"{len(crew_size)}",
            "value_em": "",
            "label": "On the crew",
        })

    license_no = validate_data_claim(profile, ("credentials", "licenseNumber"))
    if license_no:
        stats.append({
            "value_main": "Licensed",
            "value_em": "",
            "label": "& Insured",
        })

    trio = stats[:3]
    for i, s in enumerate(trio):
        s["lead"] = (i == 0)
    return trio


def resolve_trust_cells(profile: dict, stats_trio: list[dict]) -> list[dict]:
    """§2.5: next 4 after the trio. Returns up to 4 cells or []."""
    # The "not-yet-used" pool = same priority list, minus the trio labels
    used_labels = {s["label"] for s in stats_trio}
    pool: list[dict] = []

    rating = validate_data_claim(
        profile, ("googleBusiness", "rating"), coerce=float, floor=lambda r: r > 0
    )
    review_count = validate_data_claim(profile, ("googleBusiness", "reviewCount"))
    if rating is not None and review_count:
        city = pick(profile, "contact", "serviceAreaCities") or []
        city_str = city[1] if len(city) >= 2 else (city[0] if city else "the area")
        pool.append({
            "big_main": f"{rating:.1f}",
            "big_em": "★",
            "label": "Google Rating",
            "dsc":   f"Across {review_count} verified customer reviews in {city_str}.",
        })

    # Awards-derived trust cell is omitted for the same reason as the
    # hero-stats trio: placeholder strings + design-studio dsc. Awards
    # display in the About cred-grid in long form.

    gallery_count = validate_data_claim(
        profile, ("photoLibrary", "galleryPhotoCount"), coerce=int, floor=lambda n: n >= 20
    )
    if gallery_count is not None:
        pool.append({
            "big_main": f"{gallery_count}",
            "big_em": "+",
            "label": "Projects In Gallery",
            "dsc":   "A portfolio you can walk through before you ever sign.",
        })

    # A generic "weekly training" cell if the profile captures weekly-training
    # language. Substring scan, not a per-claim shape — stays as pick.
    site_desc = (pick(profile, "identity", "siteDescription") or "").lower()
    if "week" in site_desc and "train" in site_desc:
        pool.append({
            "big_main": "Weekly",
            "label": "Crew Training",
            "dsc":   "We train our team members each week on technical skill and care.",
        })

    # Years-in-business OR-chain at floor 5 (vs stats_trio's floor 10):
    # same-path-different-floor pattern that justifies the kwargs-over-dataclass
    # contract decision. Fall-through-on-floor-fail semantics match
    # resolve_distinguishing_stat's rule fall-through.
    years = (
        validate_data_claim(
            profile, ("credentials", "yearsInBusiness"), coerce=int, floor=lambda n: n >= 5
        )
        or validate_data_claim(
            profile, ("credentials", "yearsInBusinessStated"), coerce=int, floor=lambda n: n >= 5
        )
    )
    if years is not None:
        pool.append({
            "big_main": f"{years}",
            "big_em": "+",
            "label": "Years in Business",
            "dsc":   "Local, owner-operated, and still on the same corner.",
        })

    license_no = validate_data_claim(profile, ("credentials", "licenseNumber"))
    if license_no:
        pool.append({
            "big_main": "Licensed",
            "label": "& Insured",
            "dsc":   f"State license on file. Ref {license_no}.",
        })

    # Strip anything already in the trio by label match
    filtered = [c for c in pool if c.get("label") not in used_labels]
    return filtered[:4]


def resolve_secondary_stats(profile: dict) -> list[dict]:
    """Phase 0.5 engine principle 2026-04-29 — honest-data fallback stats
    for stats-tier rule fill. Source list, in preference order:
      1. service count (≥4 floor)
      2. counties served (≥2 floor)
      3. cities served (≥4 floor)
      4. founding year (always honest if captured)
    Master invariant: every stat traces to profile data, no fabrication."""
    candidates: list[dict] = []
    services_list = pick(profile, "services", "list") or []
    if len(services_list) >= 4:
        candidates.append({
            "value_main": str(len(services_list)),
            "value_em": "",
            "label": "Services offered",
        })
    counties = pick(profile, "contact", "serviceAreaCounties") or []
    if len(counties) >= 2:
        candidates.append({
            "value_main": str(len(counties)),
            "value_em": "",
            "label": "Counties served",
        })
    cities = pick(profile, "contact", "serviceAreaCities") or []
    if len(cities) >= 4:
        candidates.append({
            "value_main": str(len(cities)),
            "value_em": "",
            "label": "Cities served",
        })
    founding = pick(profile, "credentials", "foundingYear")
    if founding:
        candidates.append({
            "value_main": str(founding),
            "value_em": "",
            "label": "Founded",
        })
    return candidates


def enforce_stats_tier(tiles: list[dict], fallback_pool: list[dict], cap: int = 6) -> list[dict]:
    """Phase 0.5 engine principle 2026-04-29 — stats display count rule.
    Canonical tile counts ∈ {2, 4, 6}. Off-canonical counts (1, 3, 5)
    produce dangling-cell / asymmetric-grid layouts that read broken.

    Algorithm:
      1. Cap tiles at cap (default 6; hero passes cap=2).
      2. If count is canonical, return as-is.
      3. Try lift to next canonical (≤ cap) via fallback_pool, deduped by label.
      4. If pool cannot fill, drop to next-lower canonical tier.
      5. If even drop produces 0, return [] (sparse-drop band entirely).

    Master invariant: never fabricate; fallback_pool is honest-data only.
    """
    canonical = (2, 4, 6)
    tiles = list(tiles)[:cap]
    n = len(tiles)
    if n in canonical:
        return tiles
    lift_target = next((c for c in canonical if c > n and c <= cap), None)
    drop_target = next((c for c in reversed(canonical) if c < n), 0)
    if lift_target is not None:
        used_labels = {t.get("label", "") for t in tiles}
        avail = [f for f in fallback_pool if f.get("label", "") not in used_labels]
        needed = lift_target - n
        if len(avail) >= needed:
            return tiles + avail[:needed]
    if drop_target == 0:
        return []
    return tiles[:drop_target]


def resolve_service_list(profile: dict) -> list[dict]:
    """§2.6: services in audit order, no alphabetization. Cap at 6.

    Services-grid count rule (Phase 0.5 engine principle, 2026-04-29):
    grid card counts must be canonical tiers {1, 2, 4, 6}. Off-canonical
    counts (3, 5) produce a dangling-cell layout in 2-column grids
    (text-cutoff, empty-adjacent card). When the audited count falls
    off-canonical, drop to next-lower canonical tier — surfaces as honest
    sparse-drop rather than ship a broken-grid emit.

    Same engine-principle family as stats-tier rule (canonical {2, 4, 6}
    for stats; {1, 2, 4, 6} for services since 1 standalone service-
    business is honest at single-card emit). Master invariant: never
    fabricate to fill.
    """
    services = pick(profile, "services", "list") or []
    services = services[:6]
    canonical = {1, 2, 4, 6}
    n = len(services)
    if n in canonical:
        return services
    if n == 5:
        return services[:4]
    if n == 3:
        return services[:2]
    return services


def resolve_service_photos(profile: dict, photos_root: str | None) -> None:
    """for each service in profile.services.list, if
    featuredImage or detailImage is unset AND `_unsplash-cache.json` has a
    pick for that slug+slot, populate the field with the cache rel_path.
    Mutates profile in-place. Slugs flagged `gradient_fallback` in the cache
    leave the field unset; the renderer ships the CSS gradient for those."""
    if not photos_root:
        return
    cache_path = Path(photos_root) / "assets" / "photos" / "unsplash" / "_unsplash-cache.json"
    if not cache_path.exists():
        return
    try:
        cache = json.loads(cache_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return
    services = ((profile.get("services") or {}).get("list")) or []
    for svc in services:
        slug = svc.get("slug") or ""
        entry = cache.get(slug) or {}
        if not entry or entry.get("gradient_fallback"):
            continue
        for slot, field in (("featured", "featuredImage"), ("detail", "detailImage")):
            slot_data = entry.get(slot)
            if not isinstance(slot_data, dict):
                continue
            if not (svc.get(field) or "").strip():
                svc[field] = slot_data.get("rel_path") or ""


# Trade / project nouns that signal a real-world specific claim in a testimonial.
# Cross-trade set; the scoring pass looks for any of these as lowercase substrings.
_SPECIFIC_SIGNALS = (
    # electrical
    "generator", "panel", "breaker", "rewire", "soffit", "outlet", "wiring",
    "lighting", "troubleshoot", "inspection", "install", "charger",
    # landscape / hardscape
    "pergola", "pavers", "fire pit", "patio", "driveway", "water feature",
    "lawn", "bed", "sod", "irrigation", "pool",
    # roofing
    "shingle", "roof", "leak", "storm", "insurance", "gutter",
    # painting
    "paint", "primer", "stain", "caulk", "trim",
    # cross-trade experience nouns
    "workflow", "emergency", "after hours", "thunderstorm", "friday",
    "remodel", "kitchen", "bathroom", "garage", "deck",
)
_STOCK_PHRASES = (
    "great job", "awesome", "highly recommend", "top notch",
    "best in the business", "second to none", "5 stars",
)


def _testimonial_score(t: dict) -> int:
    """Score a single testimonial for ranking in the 3-up band. See patch note
    in build_ctx under the testimonials block."""
    s = 0
    if t.get("role"):
        s += 30
    if t.get("location"):
        s += 20
    q = (t.get("quote") or "")
    ql = q.lower()
    s += min(len(q) // 15, 15)
    if any(sig in ql for sig in _SPECIFIC_SIGNALS):
        s += 15
    if len(q) < 100 and any(p in ql for p in _STOCK_PHRASES):
        s -= 10
    return s


def resolve_testimonials(profile: dict) -> list[dict]:
    """Merge fromSite[] and fromGoogleReviews[] into a unified scored pool.
    Returns the top 3 with rating >= 4. Site testimonials are treated as 5-star
    since the prospect curated them onto their own page.

    featured-first sort. Editorial overlay on the
    existing scorer per Decision 1 — testimonials with `featured: true`
    sort ahead of the rest, ordered among themselves by score; the
    unfeatured pool fills behind them, also score-ordered. Backwards-
    compatible: when no entries carry `featured`, behavior is identical
    to the prior pure-score sort."""
    site = pick(profile, "testimonials", "fromSite") or []
    google = pick(profile, "testimonials", "fromGoogleReviews") or []
    pool: list[dict] = []
    for t in site:
        if not t.get("quote"):
            continue
        pool.append({**t, "rating": t.get("rating", 5), "source_tier": "site"})
    for t in google:
        if not t.get("quote"):
            continue
        pool.append({**t, "rating": t.get("rating", 5), "source_tier": "google"})
    # Filter to >=4 star (site defaults to 5)
    pool = [t for t in pool if (t.get("rating") or 5) >= 4]
    # Sort key: featured-first (True before False), then score descending.
    # `bool` False < True; we negate to put True ahead. Tuple sort handles ties.
    pool.sort(key=lambda t: (not t.get("featured", False), -_testimonial_score(t)))
    return pool[:3]


# slug → (question, short-label) dispatch table for
# the service-driven FAQ items. Each entry MUST be answerable from the
# matching service's profile entry (description is the source). Slugs not
# in this table are skipped — never fabricate a question for an unrecognized
# service rather than ship a flat one. Add new slugs only when the
# corresponding service description supports a credible 1-sentence answer.
FAQ_SERVICE_QA: dict[str, tuple[str, str]] = {
    # Electrical (Volthom canon + plausible neighbors)
    "generators":                 ("Do you install generators?",                "generator installation and service"),
    "ev-chargers":                ("Do you install EV chargers?",               "EV charger installation"),
    "rewires":                    ("Can you rewire an older home?",             "complete rewires"),
    "panel-upgrades":             ("Do you upgrade electrical panels?",         "panel upgrades"),
    "electrical-service-repairs": ("Do you handle electrical repairs?",         "electrical service and repair"),
    "safety-inspections":         ("Do you do home electrical inspections?",    "home electrical safety inspections"),
    # Landscape / hardscape (JSL canon + plausible neighbors)
    "outdoor-living":             ("Do you design outdoor living spaces?",      "outdoor living and hardscape design"),
    "landscapes":                 ("Do you design custom landscapes?",          "custom landscape design"),
    "water-features":             ("Do you build water features?",              "water feature design and installation"),
    "landscape-lighting":         ("Do you install landscape lighting?",        "landscape lighting"),
    "planter-pottery":            ("Do you offer planter pottery?",             "designer planter pottery"),
    "equine-properties":          ("Do you work on equine properties?",         "landscaping for equine properties"),
}


def resolve_faq(profile: dict, prose: dict) -> list[dict]:
    """§6.7 / dropped-sections.md §4: derive 5–7 FAQ items from profile data.

    Display order: license → service area → service-driven (cap 4) →
    emergency → quote. Each item generates only when its source data is
    present — no fabrication. Total caps at 7 to honor the 5–7 band rule.

    Voice register: hardcoded Front Porch / Closing Table.

    Override path (Option C): if `prose["services"]["faq"]` is present and
    non-empty, return it verbatim (normalized to {question, answer} keys).
    Voice/content tuning lives in prose, structural fallback lives here.
    """
    # --- Author override: prose.services.faq[] short-circuits derivation.
    services_prose = (prose or {}).get("services") or {}
    override = services_prose.get("faq")
    if isinstance(override, list) and override:
        normalized: list[dict] = []
        for item in override:
            if not isinstance(item, dict):
                continue
            q = item.get("question") or item.get("q") or ""
            a = item.get("answer") or item.get("a") or ""
            if q and a:
                normalized.append({"question": q, "answer": a})
        if normalized:
            return normalized

    license_items: list[dict] = []
    area_items: list[dict] = []
    service_items: list[dict] = []
    emergency_items: list[dict] = []
    quote_items: list[dict] = []

    # --- 1. Are you licensed and insured?
    # Voice rule from audit-side anti-slop-rules.md (em-dash discipline): no
    # em-dashes outside the hero subhead. FAQ copy uses periods and colons.
    license_no_raw = pick(profile, "credentials", "licenseNumber") or ""
    if license_no_raw:
        # "EC # 13006598" → "EC#13006598" — strip internal whitespace so the
        # license reads as a single token in answer copy. Source-doc forms vary
        # ("EC #13006598", "EC# 13006598"); collapse them all.
        license_no = re.sub(r"\s+", "", license_no_raw)
        license_type = pick(profile, "credentials", "licenseType")
        insured = pick(profile, "credentials", "insured")
        type_phrase = f"{license_type} " if license_type else ""
        if insured:
            ans = (
                f"Yes. We hold Florida {type_phrase}license {license_no} and we're fully "
                f"insured: general liability and workers' comp. Both are easy to verify "
                f"before we start work."
            )
        else:
            ans = (
                f"Yes. We hold Florida {type_phrase}license {license_no}. Easy to verify "
                f"before we start work."
            )
        license_items.append({"question": "Are you licensed and insured?", "answer": ans})

    # --- 2. What areas do you serve?
    cities = [c for c in (pick(profile, "contact", "serviceAreaCities") or [])
              if isinstance(c, str) and c.strip()]
    if cities:
        if len(cities) == 1:
            cities_str = cities[0]
        elif len(cities) == 2:
            cities_str = f"{cities[0]} and {cities[1]}"
        else:
            cities_str = ", ".join(cities[:-1]) + f", and {cities[-1]}"
        # If the audit caught a base city (consensus address) and it isn't
        # already in the city list, surface it as a "the shop is in X" sentence.
        base_phrase = ""
        addr_consensus = pick(profile, "contact", "addressConsensus") or ""
        addr_parts = [p.strip() for p in addr_consensus.split(",") if p.strip()]
        if len(addr_parts) >= 2:
            base_city = addr_parts[-2]
            if base_city and base_city not in cities_str:
                base_phrase = f" The shop is in {base_city}."
        ans = (
            f"We work across {cities_str}.{base_phrase} "
            f"If you're nearby and not on the list, ask. We travel for the right job."
        )
        area_items.append({"question": "What areas do you serve?", "answer": ans})

    # --- 3..N. Service-driven items (cap at 4). Slug-table dispatch.
    services_list = pick(profile, "services", "list") or []
    seen_slugs: set[str] = set()
    for svc in services_list:
        if not isinstance(svc, dict):
            continue
        slug = (svc.get("slug") or "").strip().lower()
        if not slug or slug in seen_slugs:
            continue
        entry = FAQ_SERVICE_QA.get(slug)
        if not entry:
            continue
        question, _label = entry
        desc = (svc.get("description") or "").strip()
        if not desc:
            continue
        # Front-porch register: lead with the affirmative, follow with the
        # service description verbatim from the audit. Verbatim avoids the
        # singular/plural verb-agreement awkwardness of a connector phrase
        # ("panel upgrades is part of what we do") and keeps the answer
        # provably derivable from profile data per dropped-sections.md §4.
        # Voice tweaks go through the prose.services.faq[] override path.
        ans = f"Yes. {desc}"
        service_items.append({"question": question, "answer": ans})
        seen_slugs.add(slug)
        if len(service_items) >= 4:
            break

    # --- N+1. Emergency response?
    hours = pick(profile, "contact", "hours") or {}
    weekday_keys = ("monday", "tuesday", "wednesday", "thursday", "friday")
    weekday_hours_present = any(
        isinstance(hours.get(d), str) and hours[d].strip().lower() not in ("", "closed")
        for d in weekday_keys
    )
    emergency_avail = (
        pick(profile, "identity", "emergencyAvailability")
        or pick(profile, "contact", "emergencyAvailability")
    )
    is_always_on = any(
        isinstance(v, str) and "24" in v and "hour" in v.lower()
        for k, v in hours.items() if k != "source"
    )
    has_emergency_signal = (
        isinstance(emergency_avail, str) and emergency_avail.strip() != ""
    )
    if weekday_hours_present or is_always_on or has_emergency_signal:
        if is_always_on:
            ans = (
                "Yes. We run 24/7 for true emergencies. If the power's out, you smell "
                "burning, or you've got exposed wire, call us any hour."
            )
        elif has_emergency_signal:
            phone_raw = pick(profile, "contact", "phone") or ""
            phone_disp = normalize_phone(phone_raw)
            phone_clause = (
                f" Call {phone_disp} during studio hours and we'll work it out."
                if phone_disp else ""
            )
            ans = (
                "Within service hours, yes. We've shown up after hours for true "
                "emergencies (no power, smoke from a panel, exposed wire)."
                f"{phone_clause}"
            )
        else:
            ans = (
                "We answer the phone live during studio hours and route urgent calls "
                "the same day when we can. We don't claim 24/7 unless we run it."
            )
        emergency_items.append({"question": "Do you handle emergency calls?", "answer": ans})

    # --- Last. Best way to get a quote?
    phone_raw = pick(profile, "contact", "phone") or ""
    if phone_raw:
        phone_disp = normalize_phone(phone_raw)
        # Surface a representative weekday window if hours support it.
        weekday_window = ""
        for d in weekday_keys:
            v = hours.get(d)
            if isinstance(v, str) and v.strip().lower() not in ("", "closed"):
                weekday_window = _clean_hours(v)
                break
        if weekday_window:
            window_clause = f" We answer the phone live, Monday through Friday, {weekday_window}."
        else:
            window_clause = ""
        ans = (
            f"Call {phone_disp} and tell us about the job.{window_clause} "
            f"Most quotes come back within one business day."
        )
        quote_items.append({"question": "What's the best way to get a quote?", "answer": ans})

    # --- Assemble in display order; cap total at 7 by trimming services if needed.
    fixed_count = len(license_items) + len(area_items) + len(emergency_items) + len(quote_items)
    service_cap = max(0, min(4, 7 - fixed_count))
    service_items = service_items[:service_cap]
    return license_items + area_items + service_items + emergency_items + quote_items


def resolve_trust_items(profile: dict, prose: dict) -> list[dict]:
    """derive 6 short tile strings for the
    `.trust-marquee` band (homepage band 02). Bundle's Volthom marquee
    surfaces: rating + review count + license + veteran-owned + master
    electrician + family-operated. Each item is a 2-7-word string.

    Floor: returns < 6 items if signals are absent for a different
    prospect; the homepage flow falls back to `.anchor-strip` when
    `len(trust_items) < 3` per Decision 4's guard.

    Returns a list of {text} dicts.
    """
    items: list[dict] = []

    rating = validate_data_claim(profile, ("googleBusiness", "rating"), coerce=float)
    if rating is not None:
        items.append({"text": f"★ {rating:.1f} on Google"})

    review_count = validate_data_claim(
        profile, ("googleBusiness", "reviewCount"), coerce=int, floor=lambda n: n >= 10
    )
    if review_count is not None:
        items.append({"text": f"{review_count} five-star reviews"})

    license_raw = validate_data_claim(profile, ("credentials", "licenseNumber"))
    if license_raw:
        license_clean = re.sub(r"\s+", "", license_raw)
        license_type = validate_data_claim(profile, ("credentials", "licenseType"))
        if license_type:
            items.append({"text": f"Florida {license_type} {license_clean}"})
        else:
            items.append({"text": f"Florida License {license_clean}"})

    veteran = (
        validate_data_claim(profile, ("credentials", "veteranOwned"))
        or validate_data_claim(profile, ("identity", "veteranOwned"))
    )
    if veteran:
        items.append({"text": "Veteran-Owned"})

    # Master-signal trust tile — fires when the trade signals master-level
    # credentialing via owners list or credentials. The detection (whether
    # the tile is eligible) is data-derived; the emitted CLAIM is editorial
    # and trade-specific ("Master Electrician on Every Job" vs "Master
    # Plumber on Every Job" vs trades without a master credential), so the
    # tile string routes through prose.json (P1: editorial strings from
    # prose.json). Engine drops the tile cleanly if prose lacks the slot —
    # never invents trade-noun content. Detection stays as pick + structural
    # any() per the contract scope.
    owners_list = pick(profile, "owners", "list") or []
    master_signal = any(
        "master" in (o.get("title", "") or "").lower() or "master" in (o.get("role", "") or "").lower()
        for o in owners_list if isinstance(o, dict)
    )
    master_cert_name = ""
    if not master_signal:
        certs = pick(profile, "credentials", "certifications") or []
        for c in certs:
            cname = c.get("name", "") if isinstance(c, dict) else str(c)
            if cname and "master" in cname.lower():
                master_signal = True
                master_cert_name = cname
                break
    if master_signal:
        master_claim = pick(prose, "trust_marquee", "master_signal_claim")
        if master_claim:
            items.append({"text": master_claim})
        elif master_cert_name:
            # Fallback: emit the master-tier certification name verbatim when
            # no trade-specific prose claim is authored. S3-11 partial fix
            # Session 3 close (2026-04-29) — pulls Master Tech Certified et al
            # into the marquee via existing prose-route + cert-fallback chain.
            items.append({"text": master_cert_name})

    family_op = (
        validate_data_claim(profile, ("credentials", "familyOperated"))
        or validate_data_claim(profile, ("identity", "familyOperated"))
        or validate_data_claim(profile, ("credentials", "familyOwned"))
        or validate_data_claim(profile, ("identity", "familyOwned"))
    )
    # Heuristic fallback: veteranOwnedNote often mentions family-operated for
    # Volthom-shaped data. Check for that string only if the explicit flag is
    # missing. Substring scan, not a per-claim shape — stays as pick.
    if not family_op:
        note = (pick(profile, "credentials", "veteranOwnedNote") or "").lower()
        if "family-operated" in note or "family operated" in note:
            family_op = True
    if family_op:
        items.append({"text": "Family-Operated"})

    # Award tile — surface the most-recent or first award string verbatim
    # when it fits a marquee tile. Honors anti-slop unknown-field guard:
    # the award TEXT must be present in profile.credentials, never synthesized.
    # S3-11 partial fix Session 3 close (2026-04-29).
    award_text = ""
    awards_raw = pick(profile, "credentials", "awards")
    if isinstance(awards_raw, str) and awards_raw.strip():
        award_text = awards_raw.strip()
    else:
        awards_list = pick(profile, "credentials", "awardsList") or []
        if awards_list and isinstance(awards_list[0], dict):
            award_text = awards_list[0].get("name", "")
            year = awards_list[0].get("year", "")
            if year and str(year) not in award_text:
                award_text = f"{year} {award_text}".strip()
    # Soft filter on award word-count for tile-fit. Relaxed 7→8 v1.1 Session 1
    # 2026-04-30 (Goney's "Style Magazine Best of the Best Winner 2021" hit
    # 8 words and silently dropped). Soft-filter discipline: any soft drop of
    # authored content logs to stderr so authors can trim at source rather
    # than discover the drop only by inspecting the live emit.
    if award_text:
        n_words = len(award_text.split())
        if 2 <= n_words <= 8:
            items.append({"text": award_text})
        elif n_words > 8:
            print(
                f"[trust-marquee] award text dropped: {n_words} words exceeds "
                f"ceiling 8 — trim at source: {award_text!r}",
                file=sys.stderr,
            )

    # Chamber / association affiliation tile — first matching entry,
    # with "of Commerce" trimmed for tile fit.
    affs = pick(profile, "credentials", "affiliations") or []
    for a in affs:
        aname = a if isinstance(a, str) else (a.get("name", "") if isinstance(a, dict) else "")
        if "chamber" in aname.lower():
            tile = aname.replace(" of Commerce", "").strip()
            if tile:
                items.append({"text": f"{tile} Member"})
            break

    return items[:6]


def resolve_distinguishing_stat(profile: dict, used_labels: list[str]) -> dict | None:
    """4th tile for the dark stats band ("named distinguishing fact").

    Five-rule library, first signal whose evidence floor passes wins. Each rule
    has an explicit floor so weak edge data (3-review prospect, 1-owner prospect,
    malformed founding-year=0) doesn't ship a misleading tile.

    Priority order:
      1. review-rating-floor — rating >= 4.95 AND reviewCount >= 25
      2. founding-year       — 1900 <= foundingYear <= currentYear-5
      3. owner-count         — len(owners.list) >= 2
      4. license-recency     — credentials.licenseIssuedYear set, currentYear-issued >= 5
      5. geographic-radius   — counties >= 3 OR cities >= 5

    Returns {value_main, value_em, label, source_signal} or None if nothing fires.
    `used_labels` lets the caller skip a signal whose label collides with the
    trio (e.g. trio already shows "Years in business"). Match is case-insensitive
    substring on the candidate's label.
    """
    used_norm = {(lbl or "").strip().lower() for lbl in (used_labels or [])}

    def label_clashes(candidate: str) -> bool:
        cand = candidate.strip().lower()
        for u in used_norm:
            if not u:
                continue
            if cand == u or cand in u or u in cand:
                return True
        return False

    current_year = datetime.date.today().year

    # --- 1. review-rating-floor
    rating = validate_data_claim(
        profile, ("googleBusiness", "rating"), coerce=float, floor=lambda r: r >= 4.95
    )
    review_count = validate_data_claim(
        profile, ("googleBusiness", "reviewCount"), coerce=int, floor=lambda n: n >= 25
    )
    if rating is not None and review_count is not None:
        # Compute reviews-below-five; for r>=4.95 with typical review counts
        # this resolves to 0–1. Derived calculation, not a per-claim floor —
        # stays at the rule layer.
        below = max(0, round(review_count * (5.0 - rating)))
        # Design audit — a bare "0" tile reads as broken/unloaded data, not
        # as a positive claim. Skip this rule when below resolves to exactly
        # 0 (the perfect-rating case) and let the next rule carry tile 4.
        if below > 0:
            label = "Reviews below five"
            if not label_clashes(label):
                return {
                    "value_main": str(below),
                    "value_em": "",
                    "label": label,
                    "source_signal": "review-rating-floor",
                }

    # --- 2. founding-year
    founding_year = validate_data_claim(
        profile, ("credentials", "foundingYear"),
        coerce=int, floor=lambda fy: 1900 <= fy <= current_year - 5,
    )
    if founding_year is not None:
        label = "Founded"
        if not label_clashes(label):
            return {
                "value_main": str(founding_year),
                "value_em": "",
                "label": label,
                "source_signal": "founding-year",
            }

    # --- 3. owner-count
    owners_list = validate_data_claim(
        profile, ("owners", "list"),
        floor=lambda lst: isinstance(lst, list) and len(lst) >= 2,
    )
    if owners_list is not None:
        label = "Owners on the floor"
        if not label_clashes(label):
            return {
                "value_main": str(len(owners_list)),
                "value_em": "",
                "label": label,
                "source_signal": "owner-count",
            }

    # --- 4. license-recency. Needs an explicit issuance year on the profile;
    # the license number itself does not carry one (Florida EC# is sequential).
    # The range floor `1900 <= iy <= current_year - 5` collapses both the
    # original bounds check and the years_licensed >= 5 derived check.
    issued_year = (
        validate_data_claim(
            profile, ("credentials", "licenseIssuedYear"),
            coerce=int, floor=lambda iy: 1900 <= iy <= current_year - 5,
        )
        or validate_data_claim(
            profile, ("credentials", "licenseIssued"),
            coerce=int, floor=lambda iy: 1900 <= iy <= current_year - 5,
        )
    )
    if issued_year is not None:
        years_licensed = current_year - issued_year
        label = "Years licensed"
        if not label_clashes(label):
            return {
                "value_main": str(years_licensed),
                "value_em": "+",
                "label": label,
                "source_signal": "license-recency",
            }

    # --- 5. geographic-radius. Counties first (preferred); fall back to cities.
    counties = validate_data_claim(
        profile, ("contact", "serviceAreaCounties"),
        floor=lambda lst: isinstance(lst, list) and len(lst) >= 3,
    )
    if counties is not None:
        label = "Counties served"
        if not label_clashes(label):
            return {
                "value_main": str(len(counties)),
                "value_em": "",
                "label": label,
                "source_signal": "geographic-radius",
            }
    cities = validate_data_claim(
        profile, ("contact", "serviceAreaCities"),
        floor=lambda lst: isinstance(lst, list) and len(lst) >= 5,
    )
    if cities is not None:
        label = "Cities served"
        if not label_clashes(label):
            return {
                "value_main": str(len(cities)),
                "value_em": "",
                "label": label,
                "source_signal": "geographic-radius",
            }

    return None


# ============================================================================
# 4. BAND RENDERERS
# ============================================================================

def wordmark_svg() -> str:
    """The compass/flower SVG from the reference. Uses currentColor so the
    parent's CSS color cascade drives the stroke — composer-system.css
    .wm-mark sets color:var(--color-accent), which resolves to the prospect's
    palette.accent. Same pattern as anchor_svg and manifesto_svg."""
    return (
        '<svg viewBox="0 0 40 40" width="34" height="34" fill="none">'
        '<path d="M20 4 C20 4, 8 10, 8 22 C8 30, 14 36, 20 36 C26 36, 32 30, 32 22 C32 10, 20 4, 20 4 Z" stroke="currentColor" stroke-width="1.2" fill="none"/>'
        '<path d="M20 6 L20 36" stroke="currentColor" stroke-width=".8"/>'
        '<path d="M20 14 C17 14, 14 16, 14 19" stroke="currentColor" stroke-width=".8" fill="none"/>'
        '<path d="M20 14 C23 14, 26 16, 26 19" stroke="currentColor" stroke-width=".8" fill="none"/>'
        '<path d="M20 22 C16 22, 12 24, 12 28" stroke="currentColor" stroke-width=".8" fill="none"/>'
        '<path d="M20 22 C24 22, 28 24, 28 28" stroke="currentColor" stroke-width=".8" fill="none"/>'
        '</svg>'
    )


def anchor_svg() -> str:
    return (
        '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">'
        '<path d="M10 2 C10 2, 4 6, 4 11 C4 15, 7 18, 10 18 C13 18, 16 15, 16 11 C16 6, 10 2, 10 2 Z" stroke="currentColor" stroke-width=".7" fill="none"/>'
        '</svg>'
    )


def manifesto_svg() -> str:
    return (
        '<svg viewBox="0 0 60 60" width="48" height="48" fill="none">'
        '<path d="M30 6 C30 6, 14 14, 14 30 C14 42, 22 52, 30 52 C38 52, 46 42, 46 30 C46 14, 30 6, 30 6 Z" stroke="currentColor" stroke-width="1" fill="none" opacity=".85"/>'
        '<path d="M30 8 L30 52" stroke="currentColor" stroke-width=".7" opacity=".7"/>'
        '</svg>'
    )


def wordmark_html(primary_name: str, italic_tail: str, sub: str, mark_html: str | None = None, text_visible: bool = True) -> str:
    # wordmark anchor must point at the homepage ("/"),
    # not the bare "#" placeholder, so the click target works once the site is
    # multi-page. Mirrored in render_footer's inline wordmark.
    # mark_html optional — when None, falls back to
    # the inline-SVG placeholder. When set (typically ctx["brand_mark_html"]),
    # callers inject the prospect's real brand mark (site-09 raster for Volthom).
    # text_visible (Round-3 Session 3 close, 2026-04-29 — P10 per-prospect
    # override): when False, the .wm-stack text is omitted. Used when the
    # prospect's logo lockup carries its own wordmark inside the imagery,
    # making the engine-emitted text redundant. Profile flag at
    # identity.wordmarkTextVisible. Default True preserves backward
    # compatibility for all prospects whose logo is mark-only or unavailable.
    mark = mark_html if mark_html is not None else wordmark_svg()
    if text_visible:
        return f'''<a href="/" class="wordmark">
    <span class="wm-mark" aria-hidden="true">{mark}</span>
    <span class="wm-stack">
      <span class="wm-title">{primary_name} <em>{italic_tail}</em></span>
      <span class="wm-sub">{sub}</span>
    </span>
  </a>'''
    aria_label = f"{primary_name} {italic_tail}".strip()
    return f'''<a href="/" class="wordmark wordmark--mark-only" aria-label="{aria_label}">
    <span class="wm-mark">{mark}</span>
  </a>'''


_EM_MARKUP_RE = re.compile(r'<em>|<span class="em-word">')


def _resolve_inline_em_text(value, wrap_class: str | None = None) -> str:
    """Shape-tolerant resolver for inline-em display text. Accepts:
      - str: returned stripped, as-is (author may include literal <em>...</em>
        or {em}...{/em} shorthand which is expanded in place)
      - dict: {text, em_phrase} — em_phrase is wrapped at its first occurrence
        in text; {em}/{/em} shorthand inside text takes precedence over the
        em_phrase mechanism if both are present
      - anything else: empty string
    Returns ready-to-emit HTML. Caller is responsible for applying its own
    fallback default when the result is empty.

    wrap_class: when None, em_phrase is wrapped in <em>...</em> and {em}
    shorthand expands to <em>...</em> (default for cta_band, form_intro,
    info_heading). When set (e.g., "em-word" for the hero subhead), em_phrase
    wraps in <span class="{wrap_class}">...</span> and {em} expands to the
    same span. Honors design-system divergence: hero subhead uses the
    em-word span treatment (composer-system.css) while body/contact slots
    use the bare <em> tag.

    Patch 5 (v1.1 Session 1, 2026-04-30) — double-wrap guard: if the text
    already contains <em> or <span class="em-word"> markup (after shorthand
    expansion), the em_phrase wrap step is skipped so we never emit nested
    wraps. Shorthand expansion runs first so a single text containing both
    {em} and a separately-set em_phrase doesn't double-emit. Protects both
    the dict path (author wrote em_phrase AND inline markup in the same
    text) and the str path (author wrote inline markup in a slot that
    previously got auto-wrapped).
    """
    open_tag = "<em>" if wrap_class is None else f'<span class="{wrap_class}">'
    close_tag = "</em>" if wrap_class is None else "</span>"

    if isinstance(value, str):
        text = value.strip()
        if "{em}" in text:
            text = text.replace("{em}", open_tag).replace("{/em}", close_tag)
        return text
    if isinstance(value, dict):
        text = (value.get("text") or "").strip()
        em_phrase = value.get("em_phrase")
        if "{em}" in text:
            text = text.replace("{em}", open_tag).replace("{/em}", close_tag)
        if em_phrase and em_phrase in text and not _EM_MARKUP_RE.search(text):
            text = text.replace(em_phrase, f"{open_tag}{em_phrase}{close_tag}", 1)
        return text
    return ""


def parse_wordmark_parts(business_name: str) -> tuple[str, str]:
    """Split a business name into (primary, italic_tail). 'Jason Schmidt Landscaping' → ('Jason Schmidt', 'Landscaping')."""
    words = business_name.strip().split()
    if len(words) <= 1:
        return business_name, ""
    # Italicize the last word unless it's a role noun ('LLC', 'Inc.')
    trailing_junk = {"LLC", "LLC.", "Inc.", "Inc", "Co.", "Co", "Company", "Professionals"}
    if len(words) >= 3 and words[-1] in trailing_junk:
        return " ".join(words[:-2]), words[-2]
    return " ".join(words[:-1]), words[-1]


def render_nav(ctx: dict) -> str:
    phone = ctx["phone_display"]
    primary, italic_tail = parse_wordmark_parts(ctx["business_name"])
    city_state = ctx["city_state"]
    # Nav-label set sourced from INNER_PAGE_TITLES — the single source of
    # truth shared with _inner_sitenav_html and render_footer. v1.0 five-name
    # lock: Services / About / Reviews / Contact, services-first traversal
    # per Florida service-contractor task-intent UX.
    links_html = "\n    ".join(
        f'<a href="{href}">{label}</a>'
        for label, href in INNER_PAGE_TITLES.values()
    )
    return f'''<nav class="sitenav" id="sitenav" aria-label="Primary">
  {wordmark_html(primary, italic_tail, f"Est. {city_state}", mark_html=ctx.get("brand_mark_html"), text_visible=ctx.get("wordmark_text_visible", True))}
  <div class="navlinks">
    {links_html}
  </div>
  <a href="{phone_tel_href(phone)}" class="nav-cta">
    <span>Book a Consultation</span>
    <span aria-hidden="true">→</span>
  </a>
</nav>'''


def render_hero(ctx: dict) -> str:
    prose = ctx["prose"]
    photo = ctx["hero_photo_href"]
    h1 = prose.get("h1", {})
    line1 = h1.get("line1", ctx["business_name"])
    line2_italic = h1.get("line2_italic", "")
    line2_accent = h1.get("line2_accent", "")
    kicker = prose.get("hero_kicker", "")
    kicker_html = f'''<div class="hero-kicker">
          <span class="dot" aria-hidden="true"></span>
          <span class="txt">{kicker}</span>
        </div>''' if kicker else ""
    eyebrow = prose.get("hero_eyebrow") or f"{ctx['city_state']}"

    # Hero subhead em-phrase resolution. Routed through _resolve_inline_em_text
    # Patch 5 v1.1 Session 1 2026-04-30 — the helper handles {em}/{/em}
    # shorthand expansion AND the dict-shape em_phrase wrap AND the double-
    # wrap guard (when text already contains <em> or <span class="em-word">,
    # the em_phrase replace step is skipped). Hero subhead uses the em-word
    # span treatment per composer-system.css; body/contact slots use bare
    # <em> via the same helper without wrap_class. Pre-Patch-5 emit shipped
    # <span class="em-word"><span class="em-word">…</span></span> when an
    # author included {em} markup AND set em_phrase pointing at the same
    # span; that drift is now closed at the helper.
    subhead_html = _resolve_inline_em_text(prose.get("subhead"), wrap_class="em-word")

    # Hero stats-mini caps at 2-tier (canonical {2, 4, 6}; hero surface
    # is small, 4 reads cramped). Phase 0.5 engine principle 2026-04-29.
    fallback_pool = resolve_secondary_stats(ctx.get("profile") or {})
    stats = enforce_stats_tier(ctx["stats_trio"], fallback_pool, cap=2)
    # Reapply the lead flag after tier enforcement (first stat is always lead).
    for i, s in enumerate(stats):
        s["lead"] = (i == 0)
    stats_html = []
    for s in stats:
        main = s["value_main"]
        em = s.get("value_em") or ""
        em_html = f'<em>{em}</em>' if em else ""
        # hero-stat--lead gets the dominant-number treatment;
        # hero-stat--sec renders the supporting facts at a demoted weight.
        tier_class = "hero-stat--lead" if s.get("lead") else "hero-stat--sec"
        stats_html.append(f'''<div class="hero-stat {tier_class}">
            <div class="hero-stat-value">{main}{em_html}</div>
            <div class="hero-stat-label">{s["label"]}</div>
          </div>''')

    phone = ctx["phone_display"]
    tel = phone_tel_href(phone)
    rating = ctx["rating"]
    review_count = ctx["review_count"]
    badge_html = ""
    if rating and review_count:
        badge_html = f'''<div class="hero-badge">
          <span class="hero-badge-stars">★ {float(rating):.1f}</span>
          <span class="hero-badge-count">{review_count} Google reviews</span>
        </div>'''

    # F6 hero crossfade slideshow port from T&F flagship (Round-3 Session 3
    # close, 2026-04-29): when the audit captured ≥3 hero candidates, ship
    # the hero-crossfade structure with up to 5 slides. Single-photo
    # treatment stays the fallback for prospects with <3 candidates.
    # JS driving the slideshow ships at end of <body> via _hero_count_up_js.
    profile = ctx.get("profile") or {}
    top5 = (pick(profile, "photoLibrary", "heroCandidatesTop5") or [])[:5]
    # v1.1 Session 2 Patch 4: filter author-disqualified hero candidates
    # before the crossfade-vs-single decision. If filtering drops the count
    # below the ≥3 threshold below, the slideshow path is correctly skipped
    # and the existing single-photo fallback fires.
    top5 = _filter_hero_candidates(top5, profile)
    photos_root = ctx.get("photos_root")
    out_dir = ctx.get("out_dir")
    slide_hrefs = []
    if photos_root and out_dir is not None and len(top5) >= 3:
        from pathlib import Path
        for rel in top5:
            if (Path(photos_root) / rel).exists():
                slide_hrefs.append(_photo_href(rel, photos_root, out_dir))
    use_slideshow = len(slide_hrefs) >= 3

    glass_card_html = f'''<div class="hero-glass-card hero-glass-card--wide">
        <div class="hero-eyebrow">{eyebrow}</div>
        {kicker_html}
        <h1 class="hero-headline">
          <span class="line line-1"><span class="word-roman">{line1}</span></span>
          <span class="line line-2"><span><em>{line2_italic}</em> <span class="accent-word">{line2_accent}</span></span></span>
        </h1>
        <p class="hero-sub">{subhead_html}</p>

        <div class="hero-stats-mini">
          {"".join(stats_html)}
        </div>

        <div class="hero-ctas">
          <a href="{tel}" class="hero-btn-primary">Call {phone}</a>
          <a href="contact.html" class="hero-btn-secondary">Book a Consultation</a>
        </div>

        {badge_html}
      </div>'''

    if use_slideshow:
        slides_html = "\n        ".join(
            f'<div class="hero-crossfade-slide{" active" if i == 0 else ""}" style="background-image: url(\'{href}\')" aria-hidden="true"></div>'
            for i, href in enumerate(slide_hrefs)
        )
        return f'''<section class="hero hero-crossfade">
  <div class="hero-crossfade-slideshow">
        {slides_html}
  </div>
  <div class="hero-crossfade-overlay" aria-hidden="true"></div>
  <div class="hero-crossfade-content">
    <div class="hero-single-content">
      {glass_card_html}
    </div>
  </div>
</section>'''

    return f'''<section class="hero">
  <div class="hero-single">
    <div class="hero-single-bg" id="heroBg" style="background-image:url('{photo}');" aria-hidden="true"></div>
    <div class="hero-single-grade" aria-hidden="true"></div>
    <div class="hero-single-overlay" aria-hidden="true"></div>
    <div class="hero-single-content">
      {glass_card_html}
    </div>
  </div>
</section>'''


def render_trust_marquee(ctx: dict) -> str:
    """flagship-canonical .trust-marquee homepage
    band 02 (between Hero and Services). Six tile texts from
    `resolve_trust_items`, emitted twice for the seamless CSS-animated
    scroll loop (12 .trust-item divs total).

    Floor: when fewer than 3 items resolve, return empty so the homepage
    flow falls back to `.anchor-strip` per Decision 4's guard. The fallback
    is render-time, not CSS-time."""
    items = ctx.get("trust_items") or []
    if len(items) < 3:
        return ""
    items_html = "\n      ".join(f'<div class="trust-item">{i["text"]}</div>' for i in items)
    # Bundle pattern: emit the same set twice for the CSS scroll's seamless loop.
    duplicate_html = "\n      ".join(f'<div class="trust-item">{i["text"]}</div>' for i in items)
    return f'''<section class="trust-marquee" aria-label="Trust signals">
  <div class="trust-marquee-track">
      {items_html}
      {duplicate_html}
  </div>
</section>'''


def render_anchor_strip(ctx: dict) -> str:
    # anchor strip restructured — row 1 carries the
    # location mark plus Serving / Hours labels; row 2 is a full-width
    # centered phone row that reads as the band's primary CTA. The phone
    # inherits a tel: href so the tap target stays intact on mobile.
    # anchor strip — brand signature row on top, clean
    # three-column triad below. All three columns use the same stacked
    # eyebrow-above-value pattern; DIRECT LINE gets the --cta modifier (larger
    # value, gold color, tel: link) so it reads as the primary contact action
    # without breaking column symmetry.
    city_state = ctx["city_state"]
    cities = ctx["service_cities_str"]
    hours = ctx["hours_short"]
    phone = ctx["phone_display"]
    tel = phone_tel_href(phone)
    return f'''<section class="anchor-strip">
  <div class="as-inner">
    <div class="as-mark-row">
      <div class="as-mark">
        {anchor_svg()}
        <span>Based in {city_state.split(',')[0].strip()}</span>
      </div>
    </div>
    <div class="as-triad">
      <div class="as-item">
        <div class="l">Serving</div>
        <div class="v">{cities}</div>
      </div>
      <div class="as-item">
        <div class="l">Hours</div>
        <div class="v">{hours}</div>
      </div>
      <div class="as-item as-item--cta">
        <div class="l">Direct Line</div>
        <div class="v"><a href="{tel}">{phone}</a></div>
      </div>
    </div>
  </div>
</section>'''


def render_services(ctx: dict) -> str:
    """Flagship-canonical .services-section / .services-bento /
    .service-card markup. Bundle pattern: featured card (first service)
    is .service-card-featured (large, dark background); remaining
    services are smaller .service-card tiles."""
    prose = ctx["prose"]
    services = ctx["services"]
    h = prose.get("services_headline", {})
    headline_html = _render_display_headline(h, default=f"{{em}}{len(services)} services{{/em}}. One number, one {{accent}}call{{/accent}}.")
    # homepage services-header eyebrow. Without it,
    # the 120px top padding of `.services-section` reads as "the system forgot
    # to fill this space." Eyebrow handoff: homepage "THE CRAFT" → services.html
    # "THE WHOLE SHOP" → services.html-detail "ON THE BENCH" — three distinct
    # register-blessed locatives, no duplication on Home → Services traversal.
    eyebrow_text = prose.get("services_eyebrow") or "THE CRAFT"
    eyebrow_html = f'<div class="services-eyebrow">{eyebrow_text}</div>'

    tile_taglines = {t["service_slug"]: t["tagline"] for t in prose.get("service_taglines", [])}

    cards = []
    for i, svc in enumerate(services):
        slug = svc.get("slug", "")
        anchor = f"service-{slug}" if slug else f"service-{i}"
        name = svc.get("name", "")
        desc = svc.get("description", "")
        tagline = tile_taglines.get(slug) or svc.get("tagline") or ""
        if i == 0:
            # v1.1 Session 2 Patch 2: adaptive top-overlay opacity based on
            # the photo's luminance. None when no metadata / no Pillow / no
            # photo — featured card emits with no --overlay-top-opacity and
            # CSS falls through to the Phase 0.5 floor (0.45) inside var().
            lum = _resolve_photo_luminance(
                ctx.get("profile") or {},
                svc.get("featuredImage") or "",
                ctx.get("photos_root"),
            )
            top_op = _resolve_overlay_top_opacity(lum, baseline=0.45)
            cards.append(_render_bento_featured_card(svc, anchor, link_prefix="services.html", top_opacity=top_op))
        else:
            # homepage small cards ALWAYS render
            # text-only, even when `featuredImage` is populated for the slug.
            # Photo treatment on small cards lives only on services.html
            # (render_services_page). Rationale: homepage's job is orient +
            # anchor (the featured photo card does that); 5 photo tiles below
            # add clutter without conversion lift. Matches the flagship F1-F8
            # bento rhythm. Photo-mode for cards 1-5 stays alive in
            # render_services_page for visitors who came specifically for
            # service depth.
            # The structural divergence (homepage flat-with-tagline vs
            # services.html photo-or-flat-no-tagline) is the editorial design
            # choice above, not a P3 collapse miss — the featured card (i==0)
            # is collapsed to _render_bento_featured_card via link_prefix
            # parameterization; the small card stays in two shapes by design.
            tag_html = f'<p class="service-card-desc-sm" style="font-style:italic;">{tagline}</p>' if tagline else ""
            cards.append(f'''<a href="services.html#{anchor}" class="service-card" style="text-decoration:none; color:inherit;">
          <h3 class="service-card-title-sm">{name}</h3>
          <p class="service-card-desc-sm">{desc}</p>
          {tag_html}
        </a>''')
    cards_html = "\n        ".join(cards)

    return f'''<section class="services-section" id="services">
  <div class="services-container">
    <div class="services-header">
      {eyebrow_html}
      {headline_html}
    </div>
    <div class="services-bento">
      {cards_html}
    </div>
  </div>
</section>'''


def _render_display_headline(h: dict, default: str = "") -> str:
    """Render a §6.3 display headline. h has {text, em_phrase, accent_word}."""
    text = h.get("text") or default
    em_phrase = h.get("em_phrase")
    accent = h.get("accent_word") or h.get("accent_phrase")
    # Support {em}...{/em} and {accent}...{/accent} shorthands
    if "{em}" in text:
        text = text.replace("{em}", "<em>").replace("{/em}", "</em>")
    elif em_phrase and em_phrase in text:
        text = text.replace(em_phrase, f"<em>{em_phrase}</em>", 1)
    if "{accent}" in text:
        text = text.replace("{accent}", '<span class="accent-uline">').replace("{/accent}", "</span>")
    elif accent and accent in text:
        text = text.replace(accent, f'<span class="accent-uline">{accent}</span>', 1)
    return f'<h2 class="display">{text}</h2>'


_PHOTO_CATEGORY_VOCAB = frozenset({
    "team", "owner-portrait", "finished-work", "exterior", "interior",
    "equipment", "award", "before-after", "other",
})


def _resolve_photo_category(profile: dict, rel_path: str) -> str | None:
    """Per-photo authored category from profile.photoLibrary.photos[rel_path]
    .category. Returns the category string when set to a vocabulary value;
    returns None when absent OR when the value isn't in the locked
    vocabulary (unknown values are treated as missing so an author typo
    falls through to legacy behavior rather than silently failing the band).

    Locked vocabulary (v1.1 Session 2 Patch 3, 2026-04-30): team,
    owner-portrait, finished-work, exterior, interior, equipment, award,
    before-after, other. Authors tag at Phase 4 photo curation; engine
    consults the tag at band emit (caption-photo integrity gate).

    Gate semantics — missing = legacy, wrong = drop. A teamIdentity slot
    pointing at a photo with no category emits (we trust the author's
    placement). A teamIdentity slot pointing at a photo tagged anything
    other than `team` drops the band cleanly — never substitute caption-
    on-mismatched-photo (the Goney's pre-patch defect: 'On The Trucks /
    Fifty-three years' against a greenhouse-poinsettias single-worker
    photo, where caption claimed photo content not present)."""
    cat = _resolve_photo_metadata(profile, rel_path).get("category")
    if isinstance(cat, str) and cat in _PHOTO_CATEGORY_VOCAB:
        return cat
    return None


def _filter_hero_candidates(candidates: list, profile: dict) -> list:
    """Drop hero candidates flagged
    `profile.photoLibrary.photos[<rel>].disqualifyFromHero=true`. Idempotent.
    v1.1 Session 2 Patch 4 (2026-04-30) — Bellair surfaced 3 disqualified
    entries at Phase 4 audit (award plaque, marketing collages with
    watermarks) which were hand-curated out for the one shipping cycle;
    this gate codifies the discipline so any prospect with author-tagged
    disqualifications inherits the filter automatically.

    Applied at hero rotation resolvers (single + crossfade) and the og:image
    hero-anchored fallback — a photo unfit for hero rotation is also unfit
    for social-share representative image. If the filter drops the candidate
    count below crossfade threshold (≥3), existing engine logic falls
    through to single-photo or text-only hero — no separate threshold gate
    needed here."""
    return [
        rel for rel in candidates
        if not _resolve_photo_metadata(profile, rel).get("disqualifyFromHero")
    ]


def _photo_category_matches(profile: dict, rel_path: str,
                             expected: str) -> bool:
    """Caption-photo integrity gate. Returns True when the photo's category
    is None (legacy / untagged — trust author placement) OR matches
    `expected`. Returns False when a category is set and disagrees with
    `expected` — caller drops the band cleanly. v1.1 Session 2 Patch 3."""
    actual = _resolve_photo_category(profile, rel_path)
    return actual is None or actual == expected


def _resolve_overlay_top_opacity(luminance: float | None,
                                  baseline: float = 0.45) -> float | None:
    """Map a 0–1 luminance value to a top-stop overlay opacity, anchored at
    the per-card baseline ±0.10 across three brightness bands. Bright photos
    (luminance > 0.65) take +0.10 to keep headline contrast; dark photos
    (luminance < 0.30) take −0.10 to avoid over-darkening already-dark
    backdrops; mid-range photos sit at the baseline. Sparse-drop class:
    returns None when luminance is None or non-numeric, and the caller emits
    no inline style — the CSS rule falls through to its var() default
    (the Phase 0.5 floor) so renders without Pillow / luminance metadata
    keep the existing baseline behavior.

    Engine principle (v1.1 Session 2, 2026-04-30): the top stop is the
    contrast-discriminating stop (where the headline sits). Mid/bottom
    stops aren't part of the adaptive system — they govern gradient shape,
    not text contrast, and stay at their Phase 0.5 fixed values."""
    if not isinstance(luminance, (int, float)):
        return None
    if luminance > 0.65:
        return min(1.0, baseline + 0.10)
    if luminance < 0.30:
        return max(0.0, baseline - 0.10)
    return baseline


def _render_bento_featured_card(svc: dict, anchor: str, link_prefix: str = "",
                                 top_opacity: float | None = None) -> str:
    """Featured bento card (i==0). link_prefix='' for same-page,
    'services.html' for cross-page. top_opacity (v1.1 Session 2 Patch 2,
    2026-04-30): when set, emits `--overlay-top-opacity` as an inline CSS
    custom property on the card anchor; the variable cascades to the
    .service-card-overlay child where the gradient picks it up via var().
    None passes through cleanly — CSS uses the Phase 0.5 floor default
    inside var() and behavior matches pre-Patch-2."""
    featured_href = svc.get("featuredImageHref") or ""
    name = svc.get("name", "")
    desc = svc.get("description", "")
    parts = ["text-decoration:none", "color:inherit"]
    if featured_href:
        parts.append(f"background-image:url('{featured_href}')")
    if isinstance(top_opacity, (int, float)):
        parts.append(f"--overlay-top-opacity:{top_opacity:.2f}")
    inline = "; ".join(parts) + ";"
    return f'''<a href="{link_prefix}#{anchor}" class="service-card service-card-featured" style="{inline}">
          <div class="service-card-overlay"></div>
          <div class="service-card-content">
            <div class="service-card-tag">FEATURED</div>
            <h3 class="service-card-title">{name}</h3>
            <p class="service-card-desc">{desc}</p>
            <span class="service-card-cta">See {name.lower()} →</span>
          </div>
        </a>'''


def render_pullquote(ctx: dict) -> str:
    pq = ctx["prose"].get("pullquote")
    if not pq or not pq.get("quote"):
        return ""
    return f'''<section class="pullquote">
  <div class="pq-inner">
    <div class="pq-glyph" aria-hidden="true">&ldquo;</div>
    <blockquote class="pq-quote">{pq["quote"]}</blockquote>
    <p class="pq-attr"><strong>{pq.get("attribution_name", "")}</strong>{(", " + pq["attribution_context"]) if pq.get("attribution_context") else ""}</p>
  </div>
</section>'''


def render_manifesto(ctx: dict) -> str:
    # declarative brand-pillar register replaces the
    # heritage italic-serif manifesto. New prose schema is `{headline, body}`
    # — body is optional. Renders into `.manifesto-band` (separate vocabulary
    # from the heritage `.manifesto` class so the two don't collide).
    # per Design audit, the heritage 4px naked rule
    # was undercommitted — paired now with an eyebrow ("THE PROMISE" default,
    # prose-overridable via `prose.manifesto.eyebrow`). The eyebrow IS the
    # structural anchor; the 32px navy bar lives as a CSS ::before pseudo on
    # the eyebrow element. Empty/missing eyebrow string keeps the default.
    m = ctx["prose"].get("manifesto") or {}
    headline = m.get("headline", "").strip()
    body = m.get("body", "").strip()
    eyebrow = m.get("eyebrow", "").strip() or "THE PROMISE"
    if not headline:
        return ""
    body_html = f'\n      <p class="manifesto-body">{body}</p>' if body else ""
    return f'''<section class="manifesto-band" aria-label="Brand manifesto">
    <div class="manifesto-inner">
      <p class="manifesto-eyebrow">{eyebrow}</p>
      <h2 class="manifesto-headline">{headline}</h2>{body_html}
    </div>
</section>'''


def _homepage_cta_band_html(ctx: dict) -> str:
    # replaces the homepage embedded contact form. The
    # form belongs on /contact only — the homepage gets a CTA band as the
    # conversion-ladder rung (per Design audit + flagship F2/F5 reference).
    # Composition: eyebrow + serif headline (italic-amber accent permitted) +
    # body copy + two buttons (call primary navy-fill, message secondary
    # navy-outline → contact.html). Same width-rhythm + paper-warm bg as the
    # manifesto-band so it reads as a peer editorial object.
    cta = ctx["prose"].get("cta_band") or {}
    # F7: register-blessed Closing Table imperative default. cta_band is the
    # conversion-ladder rung that ships on every homepage (per L1442-1443
    # design intent + Session 2 spec-defect F7 disposition); no opt-out.
    # cta_band.headline accepts str (with optional inline <em> or {em}
    # shorthand) OR dict ({text, em_phrase}) — Patch 4 v1.1 Session 1
    # 2026-04-30 added shape tolerance after Goney's + Bellair builds hit
    # `dict has no attribute .strip()` errors authoring against the dict
    # shape used at most other display-headline slots.
    headline = _resolve_inline_em_text(cta.get("headline")) or "Call us. Text us. <em>Send the details</em>."
    eyebrow = cta.get("eyebrow", "").strip() or "READY TO TALK"
    body = cta.get("body", "").strip()
    body_html = f'\n      <p class="cta-band-body">{body}</p>' if body else ""
    phone = ctx["phone_display"]
    tel = phone_tel_href(phone)
    primary_label = cta.get("primary_label", "").strip() or f"Call {phone}"
    secondary_label = cta.get("secondary_label", "").strip() or "Send a message &rarr;"
    return f'''<section class="cta-band" aria-label="Ready to talk">
    <div class="cta-band-inner">
      <p class="cta-band-eyebrow">{eyebrow}</p>
      <h2 class="cta-band-headline">{headline}</h2>{body_html}
      <div class="cta-band-buttons">
        <a href="{tel}" class="cta-band-button cta-band-button--primary">{primary_label}</a>
        <a href="contact.html" class="cta-band-button cta-band-button--secondary">{secondary_label}</a>
      </div>
    </div>
</section>'''


def render_testimonials(ctx: dict) -> str:
    """Flagship-canonical .testimonials-section / .testimonials-grid /
    .testimonial-card markup. `ctx["testimonials"]` already comes
    featured-first sorted via `resolve_testimonials` (Decision 1).
    Top-3 cap unchanged."""
    tst = ctx["testimonials"]
    if len(tst) < 3:
        return ""
    prose = ctx["prose"]
    headline_h = prose.get("testimonials_headline", {})
    headline_text = headline_h.get("text") or ""
    title_html = f'<h2 class="testimonials-title">{headline_text}</h2>' if headline_text else ""
    eyebrow = prose.get("testimonials_eyebrow") or "FROM THE NEIGHBORS"
    rating = ctx.get("rating")
    review_count = ctx.get("review_count")
    rating_text = ""
    if rating and review_count:
        rating_text = f"{float(rating):.1f} from {review_count} Google reviews"

    rating_html = ""
    if rating_text:
        rating_html = f'''<div class="testimonials-rating">
          <span class="testimonials-stars">★★★★★</span>
          <span class="testimonials-rating-text">{rating_text}</span>
        </div>'''

    cards = []
    for t in tst[:3]:
        first = t.get("firstName", "")
        last = t.get("lastName", "")
        name = f"{first} {last}".strip() or first or t.get("name") or "[Reviewer name]"
        role = t.get("role", "")
        location = t.get("location", "Verified Google Review")
        role_html = f'<div class="testimonial-role">{role}</div>' if role else ""
        cards.append(f'''<article class="testimonial-card">
        <div class="testimonial-stars">★★★★★</div>
        <p class="testimonial-quote">{t.get("quote", "")}</p>
        <div class="testimonial-author">
          <div class="testimonial-name">{name}</div>
          {role_html}
          <div class="testimonial-location">{location}</div>
        </div>
      </article>''')

    return f'''<section class="testimonials-section" id="testimonials">
  <div class="testimonials-container">
    <div class="testimonials-header">
      <div class="testimonials-eyebrow">{eyebrow}</div>
      {title_html}
      {rating_html}
    </div>
    <div class="testimonials-grid">
      {"".join(cards)}
    </div>
  </div>
</section>'''


def render_story(ctx: dict) -> str:
    prose = ctx["prose"]
    if not ctx["owner_names"]:
        return ""
    headline = _render_display_headline(
        prose.get("story_headline", {}),
        default="From the {em}job site{/em}.",
    )
    lede = prose.get("story_lede", "")
    paragraphs = prose.get("story_paragraphs", [])
    paragraphs_html = "\n        ".join(f"<p>{p}</p>" for p in paragraphs)
    cap_label = prose.get("story_caption_label", f"{ctx['city_state'].split(',')[0].strip()} · Residential")
    cap_value = prose.get("story_caption_value", "")
    caption_html = f'''<div class="story-caption">
          <div class="l">{cap_label}</div>
          <div class="v">{cap_value}</div>
        </div>''' if cap_value else ""
    story_img = ctx.get("story_img_href")
    story_img_alt = prose.get("story_img_alt", "A project detail from a recent job.")
    owner_names_html = ctx["owner_names"]

    grid_class = "story-grid" if story_img else "story-grid story-grid--text-only"
    img_block = f'''<div class="story-img">
        <img src="{story_img}" alt="{story_img_alt}">
        {caption_html}
      </div>
      ''' if story_img else ""

    return f'''<section class="story" id="story">
  <div class="wrap">
    <div class="{grid_class}">
      {img_block}<div class="story-body">
        <div class="section-label" style="margin-bottom:18px">
          <span class="num">iii.</span>
          <span class="rule"></span>
          <span class="lab">About</span>
        </div>
        {headline}
        <p class="lede">{lede}</p>
        {paragraphs_html}

        <div class="story-owners">
          <div class="sig">{owner_names_html}</div>
          <div class="role">Owners</div>
        </div>
      </div>
    </div>
  </div>
</section>'''


# Footer social-icon registry. Inline Lucide SVG markup keyed by platform slug.
# Round-4 close (Session 4 Phase 0.5, 2026-04-29): replaced Unicode glyph
# placeholders ('f' / '◉' / '▶') with proper inline SVG. The fisheye character
# rendered as an empty circle in the inherited footer font, producing a working
# link with no visible icon — P15 codification: every captured social platform
# must have a registered icon component before render. The dict shape gives the
# v1.1 audit-time coverage check a single source of truth.
_SOCIAL_ICON_SVG: dict[str, str] = {
    "facebook":  '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>',
    "instagram": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>',
    "youtube":   '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.33z"/><polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"/></svg>',
    "linkedin":  '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>',
}


def render_footer(ctx: dict) -> str:
    p = ctx["palette"]
    phone = ctx["phone_display"]
    email = ctx["email"]
    addr1 = ctx["address_line1"]
    addr2 = ctx["address_line2"]
    hours_list = ctx["hours_full"]
    city_state = ctx["city_state"]
    biz_name = ctx["business_name"]
    primary, italic_tail = parse_wordmark_parts(biz_name)
    tag = ctx["prose"].get("footer_tag") or ctx.get("tagline") or ""
    tag_html = f'<p class="tag">{tag}</p>' if tag else ""

    socials = []
    for plat in ("facebook", "instagram", "youtube", "linkedin"):
        url = pick(ctx["profile"], "socialMedia", plat)
        if url and plat in _SOCIAL_ICON_SVG:
            socials.append(
                f'<a href="{url}" aria-label="{plat.capitalize()}">{_SOCIAL_ICON_SVG[plat]}</a>'
            )

    hours_lis = "\n          ".join(f"<li>{h}</li>" for h in hours_list)

    contributors = ctx.get("google_contributors") or []
    google_attr_html = ""
    if contributors:
        # Google photo attribution. Names come from
        # _attributions.json (per-photo contributor data); never hardcode the
        # business name — most prospects ship customer-contributed photos.
        # Skip the sentence period if the last contributor name already ends
        # with one (e.g. "VOLTHOM ELECTRIC, INC.") to avoid "INC..".
        joined = ", ".join(contributors)
        terminator = "" if joined.endswith(".") else "."
        google_attr_html = f'\n    <div class="footer-attr">Photos provided by Google. Contributors: {joined}{terminator}</div>'
    unsplash_attr_html = _unsplash_attribution_html(ctx.get("unsplash_attributions") or [])
    if unsplash_attr_html:
        # render_footer uses .footer-attr class for footer attribution; reuse for
        # the Unsplash row by replacing the .footer-attribution class.
        unsplash_attr_html = unsplash_attr_html.replace("footer-attribution footer-attribution-unsplash", "footer-attr footer-attr-unsplash")

    # brand mark sourced from ctx (site-09 raster
    # for Volthom; falls to inline SVG placeholder otherwise). Explore links
    # point at page files (not hash anchors) so the footer works identically
    # on homepage AND inner pages — single emit path. Footer no longer carries
    # id="contact"; that id collided with contact.html's <section id="contact">.
    mark = ctx.get("brand_mark_html") or wordmark_svg()
    wm_text = ctx.get("wordmark_text_visible", True)
    if wm_text:
        wm_inner = f'''<span class="wm-mark" aria-hidden="true">{mark}</span>
          <span class="wm-stack">
            <span class="wm-title">{primary} <em>{italic_tail}</em></span>
            <span class="wm-sub">Est. {city_state}</span>
          </span>'''
        wm_class = "wordmark"
    else:
        wm_inner = f'<span class="wm-mark">{mark}</span>'
        wm_class = "wordmark wordmark--mark-only"
    return f'''<footer class="footer">
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
        <a href="/" class="{wm_class}" style="color:var(--color-cream)">
          {wm_inner}
        </a>
        {tag_html}
      </div>

      <div class="footer-col footer-contact">
        <h4>Contact</h4>
        <div class="phone">{phone}</div>
        {f'<div class="line">{email}</div>' if email else ''}
        <div class="line">{addr1}</div>
        <div class="line">{addr2}</div>
      </div>

      <div class="footer-col">
        <h4>Hours</h4>
        <ul>
          {hours_lis}
        </ul>
      </div>

      <div class="footer-col">
        <h4>Explore</h4>
        <ul>
          <li><a href="services.html">Services</a></li>
          <li><a href="about.html">About</a></li>
          <li><a href="testimonials.html">Reviews</a></li>
          <li><a href="contact.html">Book a Consultation</a></li>
        </ul>
      </div>
    </div>

    <div class="footer-bot">
      <div>© {biz_name} · {city_state}</div>
      <div class="social">
        {" ".join(socials)}
      </div>
    </div>{google_attr_html}{unsplash_attr_html}
  </div>
</footer>'''


# default header strings for the four new homepage
# bands (and the services-page FAQ header retrofit). These live next to the
# render helpers — not in fixtures — so that `prose.json` stays optional.
# All strings are §6-rule-compliant (no em-dashes, specific nouns, active voice).
_STATS_BAND_DEFAULT_EYEBROW = "BY THE NUMBERS"
_STATS_BAND_DEFAULT_TITLE = "What the work <em>adds up to</em>."
_FAQ_HEADER_DEFAULTS = {
    "homepage": {"eyebrow": "WHAT FOLKS ASK", "title": "What we hear, <em>most</em>."},
    "services": {"eyebrow": "BEFORE THEY CALL", "title": "What homeowners ask, <em>before they call</em>."},
}


def render_stats_band(ctx: dict) -> str:
    """dark-band 4-tile stats restoration. Tiles 1–3 come from
    `ctx["stats_trio"]` (same trio the hero shares); tile 4 is the named
    distinguishing fact from `ctx["distinguishing_stat"]` (or None for a
    3-tile fallback).

    Header copy reads `prose["homepage"]["stats_band"]` if present, else falls
    back to a stable default. §6 voice rules bind the default — no em-dashes,
    specific nouns over corporate filler.
    """
    trio = ctx.get("stats_trio") or []
    if not trio:
        # No stats data at all → drop the band rather than ship an empty grid.
        return ""

    distinguishing = ctx.get("distinguishing_stat")
    tiles = list(trio)
    if distinguishing:
        tiles.append(distinguishing)

    # Phase 0.5 engine principle 2026-04-29 — stats display count rule:
    # canonical tile counts ∈ {2, 4, 6}. stats-section dark band caps at
    # 4-tier (the band's grid template). Lifts via secondary-stats pool
    # when off-canonical (3 → 4 if pool fills, else 3 → 2).
    fallback_pool = resolve_secondary_stats(ctx.get("profile") or {})
    tiles = enforce_stats_tier(tiles, fallback_pool, cap=4)
    if not tiles:
        return ""

    tile_html = []
    for i, t in enumerate(tiles):
        value_main = t.get("value_main", "")
        value_em = t.get("value_em", "")
        label = t.get("label", "")
        # F2 count-up port from T&F flagship (Round-3 Session 3 close, 2026-04-29):
        # The LEAD stat (first tile, the proof-stack anchor) gets data-target
        # for IntersectionObserver-driven count-up animation; companion stats
        # stay static. Static for non-numeric values (founding year is identity,
        # not a progress number — "2001" is a fact, not a count). data-target
        # only fires when value_main is a pure integer with no em suffix.
        is_lead = (i == 0)
        is_pure_int = isinstance(value_main, str) and value_main.replace(",", "").isdigit() and not value_em
        if is_lead and is_pure_int:
            number_div = f'<div class="stats-number" data-target="{value_main}">0</div>'
        else:
            content = f"{value_main}{value_em}" if value_em else value_main
            number_div = f'<div class="stats-number-static">{content}</div>'
        tile_html.append(
            f'<div class="stats-item">\n'
            f'        {number_div}\n'
            f'        <div class="stats-label">{label}</div>\n'
            f'      </div>'
        )

    prose_block = (ctx.get("prose") or {}).get("stats_band") or {}
    eyebrow = prose_block.get("eyebrow") or _STATS_BAND_DEFAULT_EYEBROW
    title = prose_block.get("title") or _STATS_BAND_DEFAULT_TITLE

    return f'''<section class="stats-section">
  <div class="stats-container">
    <div class="stats-header">
      <div class="stats-eyebrow">{eyebrow}</div>
      <h2 class="stats-title">{title}</h2>
    </div>
    <div class="stats-grid">
      {"".join(tile_html)}
    </div>
  </div>
</section>'''


def render_faq(ctx: dict, page: str = "homepage") -> str:
    """shared FAQ band renderer used by both the
    homepage band sequence and the services page. Reads `ctx["profile"]["faq"]`
    (resolved by `resolve_faq` during build_ctx) and emits the bundle's
    flagship-canonical markup: <section class="faq-section"> →
    <div class="faq-container"> → <div class="faq-header"> + <div class="faq-list">.

    Header copy reads `prose[page]["faq_header"]`; falls back to the
    per-page default in `_FAQ_HEADER_DEFAULTS`. The two pages get distinct
    defaults so a back-to-back read doesn't see "FAQ / Common questions" twice.

    Returns "" when `profile.faq[]` is empty (drop the band, same gate as 3e).
    """
    faq_list = pick(ctx["profile"], "faq") or []
    if not faq_list:
        return ""

    items_html = []
    for item in faq_list:
        q = item.get("question", "")
        a = item.get("answer", "")
        items_html.append(
            f'<details class="faq-item">\n'
            f'        <summary class="faq-question">{q}</summary>\n'
            f'        <div class="faq-answer">{a}</div>\n'
            f'      </details>'
        )
    items_block = "\n      ".join(items_html)

    prose_root = ctx.get("all_prose") or {}
    page_prose = prose_root.get(page) or {}
    header_prose = page_prose.get("faq_header") or {}
    defaults = _FAQ_HEADER_DEFAULTS.get(page) or _FAQ_HEADER_DEFAULTS["homepage"]
    eyebrow = header_prose.get("eyebrow") or defaults["eyebrow"]
    title = header_prose.get("title") or defaults["title"]

    return f'''<section class="faq-section">
  <div class="faq-container">
    <div class="faq-header">
      <div class="faq-eyebrow">{eyebrow}</div>
      <h2 class="faq-title">{title}</h2>
    </div>
    <div class="faq-list">
      {items_block}
    </div>
  </div>
</section>'''


def render_promo_callout(ctx: dict) -> str:
    """emit `<section class="promo-callout">` only when
    `profile.promotions.featuredPromo` is non-null. Volthom + JSL both ship
    null → both correctly drop. The data carries the dated business-validated
    promotion (eyebrow / headline / sub / cta / dateRange); prose can override
    voice when authored.

    Date-range expiry is NOT enforced here.
    """
    promo = ctx.get("featured_promo")
    if not promo or not isinstance(promo, dict):
        return ""

    prose_block = (ctx.get("prose") or {}).get("promo_callout") or {}
    eyebrow = prose_block.get("eyebrow") or promo.get("eyebrow") or ""
    headline = prose_block.get("headline") or promo.get("headline") or ""
    sub = prose_block.get("sub") or promo.get("sub") or ""
    cta_label = prose_block.get("cta") or promo.get("cta") or ""

    # CTA href: prefer an explicit phone tel: link when the cta string carries a
    # phone number; otherwise anchor to #contact. Prose may also set href.
    cta_href = prose_block.get("cta_href") or promo.get("cta_href") or ""
    if not cta_href:
        phone_raw = pick(ctx["profile"], "contact", "phone") or ""
        if phone_raw and any(ch.isdigit() for ch in cta_label):
            cta_href = phone_tel_href(phone_raw)
        else:
            cta_href = "#contact"

    eyebrow_html = f'<div class="promo-callout-eyebrow">{eyebrow}</div>' if eyebrow else ""
    sub_html = f'<p class="promo-callout-sub">{sub}</p>' if sub else ""
    cta_html = f'<a href="{cta_href}" class="promo-callout-cta">{cta_label}</a>' if cta_label else ""

    return f'''<section class="promo-callout">
  <div class="promo-callout-container">
    {eyebrow_html}
    <h2 class="promo-callout-title">{headline}</h2>
    {sub_html}
    {cta_html}
  </div>
</section>'''


def render_before_after(ctx: dict) -> str:
    """emit before/after gallery only when
    `profile.photoLibrary.beforeAfterPairs` carries 2+ pairs.

    Stub status: no production exemplar lifted into composer-system.css
    yet. Volthom + JSL both ship empty pairs → both correctly drop, so the
    gate is exercised but the markup is intentionally minimal. The first
    prospect with paired photos is the forcing function for full markup +
    CSS — see dropped-sections.md §2 and references/section-patterns.md
    §11 (.beforeafter-section) in the production prospect-site skill.
    """
    pairs = ctx.get("before_after_pairs") or []
    if not isinstance(pairs, list) or len(pairs) < 2:
        return ""

    # Placeholder markup intentionally minimal so dead CSS doesn't accumulate
    # before the first paired-photo prospect forces the lift.
    items = []
    for pair in pairs[:6]:
        before = pair.get("before") or pair.get("beforeUrl") or ""
        after = pair.get("after") or pair.get("afterUrl") or ""
        items.append(
            f'<div class="beforeafter-pair">\n'
            f'        <img class="beforeafter-img beforeafter-img-before" src="{before}" alt="Before">\n'
            f'        <img class="beforeafter-img beforeafter-img-after" src="{after}" alt="After">\n'
            f'      </div>'
        )
    return f'''<section class="beforeafter-section">
  <div class="beforeafter-container">
    {"".join(items)}
  </div>
</section>'''


def render_mobile_cta_bar(ctx: dict) -> str:
    """universal-ship sticky bottom bar for mobile (< 900px).
    Hidden on desktop via the §14 CSS rules in composer-system.css.

    Soft-gate: if `contact.phone` is null, omit the "Call" half but keep the
    quote button so phoneless prospects (none in current fixtures) don't break.
    """
    phone_raw = pick(ctx["profile"], "contact", "phone") or ""
    phone_disp = normalize_phone(phone_raw)

    parts = []
    if phone_raw:
        parts.append(
            f'<a href="{phone_tel_href(phone_raw)}" class="mobile-cta-primary">Call {phone_disp}</a>'
        )
    # point at contact.html (universal target) so
    # the link works on every page. Previously "#contact" only resolved on
    # the homepage; render_footer's id="contact" was removed in 5.0a to
    # avoid a duplicate-id collision with contact.html's form section.
    parts.append('<a href="contact.html" class="mobile-cta-secondary">Get a Quote</a>')
    return f'''<aside class="mobile-cta-bar" aria-label="Quick contact">
  {"".join(parts)}
</aside>'''


# ============================================================================
# 4b. INNER-PAGE BAND RENDERERS
# ----------------------------------------------------------------------------
# Inner pages emit against §1–§13 of the lifted bundle vocabulary against
# the flagship-canonical chassis (.footer, .trust-marquee,
# .subpage-hero present).
# ============================================================================

INNER_PAGE_KEYS = ("about", "services", "testimonials", "contact")
INNER_PAGE_TITLES = {
    # v1.0 five-name lock: canonical industry-standard nav labels for the
    # four inner pages. Single source of truth — _inner_sitenav_html,
    # render_nav, render_footer, and render_page (page_title) all read from
    # this constant. Iteration order is the displayed nav order
    # (services-first per Florida service-contractor task-intent UX:
    # visitors arrive with a problem, scan for what you do before who you
    # are). Slug column intentionally retains "testimonials.html" — F1-F7
    # deployed flagships have inbound links that depend on slug stability;
    # only the displayed label is "Reviews".
    "services":     ("Services", "services.html"),
    "about":        ("About",    "about.html"),
    "testimonials": ("Reviews",  "testimonials.html"),
    "contact":      ("Contact",  "contact.html"),
}


def _inner_sitenav_html(ctx: dict, current: str) -> str:
    """Render the inner-page sticky-translucent sitenav.

    Unified with homepage nav — same wordmark_html shell (with brand mark),
    same id="sitenav" so the scroll-listener script fires, same canonical
    label set sourced from INNER_PAGE_TITLES (the single source of truth
    shared with render_nav and render_footer). The body.is-inner CSS scope
    in composer-system.css §13 gives the inner-page light-bg-friendly
    variant. Marks the current page with aria-current='page'.
    """
    primary, italic_tail = parse_wordmark_parts(ctx["business_name"])
    city_state = ctx["city_state"]
    phone = ctx["phone_display"]
    tel = phone_tel_href(phone)
    def _link(key: str) -> str:
        label, href = INNER_PAGE_TITLES[key]
        cur = ' aria-current="page"' if key == current else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    links_html = "\n    ".join(_link(key) for key in INNER_PAGE_TITLES)
    return f'''<nav class="sitenav" id="sitenav" aria-label="Primary">
  {wordmark_html(primary, italic_tail, f"Est. {city_state}", mark_html=ctx.get("brand_mark_html_inner") or ctx.get("brand_mark_html"), text_visible=ctx.get("wordmark_text_visible", True))}
  <div class="navlinks">
    {links_html}
  </div>
  <a href="{tel}" class="nav-cta"><span>Book a Consultation</span><span aria-hidden="true">→</span></a>
</nav>'''


def _subpage_hero_html(prose_page: dict) -> str:
    """Bundle §1 .subpage-hero: eyebrow + h1 (with em phrase) + sub. The
    subpage-hero is text-only in this lift; photo-thin / credential-rich
    prospects (Volthom) ship without a hero photo here per
    photo-discipline.md.

    superseded by _page_hero_html for new emits.
    Kept alive for any prospects still rendering against the older vocabulary.
    """
    eyebrow = prose_page.get("eyebrow", "")
    headline = prose_page.get("headline") or {}
    h_text = headline.get("text", "")
    em_phrase = headline.get("em_phrase")
    if em_phrase and em_phrase in h_text:
        h_html = h_text.replace(em_phrase, f"<em>{em_phrase}</em>", 1)
    else:
        h_html = h_text
    sub = prose_page.get("subhead", "")
    return f'''<section class="subpage-hero">
  <div class="subpage-hero-container">
    <div class="subpage-hero-eyebrow">{eyebrow}</div>
    <h1 class="subpage-hero-title">{h_html}</h1>
    <p class="subpage-hero-sub">{sub}</p>
  </div>
</section>'''


def _spell_count(n: int) -> str:
    """House style: spell out integer counts under 20, numeral 20+. Used at
    default-emit surfaces (eyebrows, ledes) where the engine renders count
    references without author intervention. Single source of truth for count
    rendering across default-emit surfaces. Returns lowercase; callers
    uppercase via .upper() when surface requires (e.g., mono-tracked eyebrow
    register).
    """
    if not isinstance(n, int) or n < 0:
        return ""
    count_words = {1:"one",2:"two",3:"three",4:"four",5:"five",6:"six",7:"seven",
                   8:"eight",9:"nine",10:"ten",11:"eleven",12:"twelve",13:"thirteen",
                   14:"fourteen",15:"fifteen",16:"sixteen",17:"seventeen",
                   18:"eighteen",19:"nineteen"}
    return count_words.get(n) or str(n)


def _resolve_page_hero_eyebrow_default(page_key: str, ctx: dict | None) -> str:
    """Inner-page page-hero eyebrow defaults — register-blessed wayfinding
    constants per voiceMap §6 LABEL discipline + prose-rules.md §6.6 spec
    examples. Profile-interpolating qualifier with sparse-drop discipline at
    interpolation level: bare LABEL renders when qualifier source absent.
    Session 2 disposition: about-eyebrow uses HOW WE GOT HERE (NOT "OUR
    STORY" — that's the named anti-pattern from feedback_spectacle_first
    _disposition.md B3-close #11 retraction).
    """
    if not ctx:
        return ""
    profile = ctx.get("profile") or {}
    if page_key == "about":
        founding_year = pick(profile, "credentials", "foundingYear")
        return f"HOW WE GOT HERE · SINCE {founding_year}" if founding_year else "HOW WE GOT HERE"
    if page_key == "services":
        services_list = pick(profile, "services", "list") or []
        n = len(services_list)
        if n:
            return f"THE CRAFT · {_spell_count(n).upper()} SERVICES"
        return "THE CRAFT"
    if page_key == "testimonials":
        review_count = pick(profile, "googleBusiness", "reviewCount")
        return f"FROM THE NEIGHBORS · {review_count} REVIEWS" if review_count else "FROM THE NEIGHBORS"
    if page_key == "contact":
        city_state = ctx.get("city_state", "")
        return f"VISIT · {city_state.upper()}" if city_state else "VISIT"
    return ""


def _resolve_page_hero_lede_default(page_key: str, ctx: dict | None) -> str:
    """Inner-page page-hero lede defaults — Closing Table register, three
    parallel clauses, profile-interpolation at clause-1 with shape-preserving
    sparse-drop fallback at absent data, em italic on locative-relational
    pivot at clause-3. The where-pivot is the engine's signature register
    move at default-emit ledes — grounded, not floating. Future engine
    extensions that add a fifth inner-page surface inherit the rule.
    """
    if not ctx:
        return ""
    profile = ctx.get("profile") or {}
    if page_key == "about":
        owners = pick(profile, "owners", "list") or []
        owner_first = ""
        if owners and isinstance(owners[0], dict):
            owner_first = owners[0].get("firstName") or ""
        if owner_first:
            return f"How {owner_first} built the company, who runs it now, and <em>where it works</em>."
        return "How the company got built, who runs it, and <em>where it works</em>."
    if page_key == "services":
        services_list = pick(profile, "services", "list") or []
        n = len(services_list)
        if n:
            return f"The {_spell_count(n)} services we run, what each one looks like, and <em>where the work happens</em>."
        return "The services we run, what each one looks like, and <em>where the work happens</em>."
    if page_key == "testimonials":
        review_count = pick(profile, "googleBusiness", "reviewCount")
        if review_count:
            return f"{_spell_count(review_count)} customer reviews, names attached to each, and <em>where they came from</em>."
        return "Customer reviews, names attached to each, and <em>where they came from</em>."
    if page_key == "contact":
        cities = pick(profile, "contact", "serviceAreaCities") or []
        primary_city = cities[0] if cities else ""
        if primary_city:
            return f"How to reach us in {primary_city}, what to send if you write, and <em>where else we go</em>."
        return "How to reach us, what to send if you write, and <em>where else we go</em>."
    return ""


def _page_hero_html(prose_page: dict, page_key: str = "", ctx: dict | None = None, extra_html: str = "") -> str:
    """flagship-canonical inner-page hero.

    Same prose contract as _subpage_hero_html — eyebrow + headline (with
    optional em_phrase) + subhead — but emits .page-hero/.wrap/.eyebrow/h1/.lede
    matching the §15 inner-page vocabulary in composer-system.css.

    `extra_html` is an optional post-lede slot for the testimonials .metrics
    trio (5.0 / 199 / 0). Empty by default.

    Sparse-drop discipline (Session 2 spec-defect F1 fix): when
    prose_page.headline.text is absent, the entire page-hero band drops
    cleanly. Empty `<h1></h1>` shells were the Session 2 walk's universal
    inner-page defect. When eyebrow is absent, falls back to register-blessed
    wayfinding constant per page_key.
    """
    headline = prose_page.get("headline") or {}
    h_text = headline.get("text", "")
    # F1-h1 sparse-drop: drop the band when h1 is absent (no broken empty shell)
    if not h_text:
        return ""
    em_phrase = headline.get("em_phrase")
    if em_phrase and em_phrase in h_text:
        h_html = h_text.replace(em_phrase, f"<em>{em_phrase}</em>", 1)
    else:
        h_html = h_text
    # F1-eyebrows: wayfinding constant when prose-authored eyebrow absent
    eyebrow = prose_page.get("eyebrow") or _resolve_page_hero_eyebrow_default(page_key, ctx)
    # F1-ledes: register-blessed Closing Table lede when prose-authored subhead absent
    sub = prose_page.get("subhead") or _resolve_page_hero_lede_default(page_key, ctx)
    extra_block = f"\n    {extra_html}" if extra_html else ""
    return f'''<section class="page-hero">
  <div class="wrap">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{h_html}</h1>
    <p class="lede">{sub}</p>{extra_block}
  </div>
</section>'''


def render_about_page(ctx: dict) -> str:
    """flagship-canonical about page.

    Editorial arc:
      page-hero (eyebrow + h1 + lede)
      → story-grid (founder portrait + bio paragraphs + owner credentials line)
      → page-section .cred-grid (boxed credential cells: License / Insurance /
        Award / Affiliation / Reviews / Experience — first 4-6 present)
      → page-section "Where we work" (counties + cities served)
      → brand-band (Volthom site-07 brand asset as page coda — only when
        assets/photos/site/site-07.jpg is present in the prospect's library)
      → footer

    Photo placements (Volthom locked plan):
      - story-grid portrait: site-04 (founder portrait) when present, else
        falls to gp-01 (Thomas + truck) when present, else text-only.
      - brand-band image: site-07 (wordmark + tagline). Section drops
        entirely when site-07 is absent — generalizes to non-Volthom prospects
        without forcing them to ship a brand badge.
    """
    from pathlib import Path
    prose_page = ctx["all_prose"].get("about") or {}
    profile = ctx["profile"]
    photos_root = ctx.get("photos_root")
    out_dir = ctx.get("out_dir")

    # Story body — lede paragraph + story_paragraphs[]
    lede = prose_page.get("lede", "")
    paragraphs = prose_page.get("story_paragraphs") or []
    body_paras = []
    if lede:
        body_paras.append(lede)
    body_paras.extend(paragraphs)
    story_paras_html = "\n        ".join(f"<p>{p}</p>" for p in body_paras)

    # Story-grid portrait — prefer site-04 (founder portrait) over gp-01.
    # Caption-label, caption-value, and image alt route through prose
    # (P1: editorial strings from prose.json). Engine drops sparse fields
    # cleanly rather than emitting per-prospect-shaped fallbacks; the alt
    # text falls back to a data-derived owner descriptor when prose absent
    # so accessibility-required alt is always present without inventing a
    # trade-noun the engine can't verify.
    story_img_html = ""
    if photos_root and out_dir is not None:
        site_04_rel = "assets/photos/site/site-04.jpg"
        owners_list = pick(profile, "owners", "list") or []
        owner_full = ""
        owner_role_data = ""
        if owners_list:
            o = owners_list[0]
            owner_full = owner_full_name(o)
            owner_role_data = o.get("role") or o.get("title") or ""
        prose_alt = pick(prose_page, "story_img_alt")
        if prose_alt:
            founder_alt = prose_alt
        elif owner_full and owner_role_data:
            founder_alt = f"{owner_full}, {owner_role_data} of {ctx['business_name']}."
        elif owner_full:
            founder_alt = f"{owner_full} of {ctx['business_name']}."
        else:
            founder_alt = f"Founder of {ctx['business_name']}."
        cap_label = pick(prose_page, "story_caption_label") or ctx["city_state"]
        cap_value = pick(prose_page, "story_caption_value")
        cap_value_html = f'<div class="story-caption-value">{cap_value}</div>' if cap_value else ""
        caption_html = f'''<div class="story-caption">
          <div class="story-caption-label">{cap_label}</div>
          {cap_value_html}
        </div>'''
        # Priority chain (Round-2 diagnostic Session 3 close, 2026-04-29):
        #   profile.photoLibrary.ownerPortrait
        #   → profile.photoLibrary.teamIdentity (NEW — crew + branded apparel
        #     + customer/context shots; family-business prospects often lack
        #     a literal owner portrait but DO have crew-with-customer images
        #     that carry the same family-identity register weight)
        #   → assets/photos/site/site-04.jpg (Volthom convention)
        #   → sparse-drop (text-only story-grid)
        #
        # The hero-photo fallback was removed at S3-14 because it shipped
        # service action shots (solar-panel close-ups, roof spray arcs)
        # under "team portrait" alt text. The teamIdentity tier closes the
        # gap S3-14 left for prospects without a captured ownerPortrait.
        portrait_rel = pick(profile, "photoLibrary", "ownerPortrait") or ""
        team_identity_rel = pick(profile, "photoLibrary", "teamIdentity") or ""
        chosen_rel = ""
        # v1.1 Session 2 Patch 3 — caption-photo integrity gate. Each tier
        # consults profile.photoLibrary.photos[rel].category. Missing = legacy
        # (trust author placement); wrong = band drops entirely (never
        # substitute caption-on-mismatched-photo). Once a tier asserts a
        # wrong-category photo, the band drops cleanly without falling to
        # the next tier — caption was authored for that tier's context.
        band_dropped = False
        if portrait_rel and (Path(photos_root) / portrait_rel).exists():
            if _photo_category_matches(profile, portrait_rel, "owner-portrait"):
                chosen_rel = portrait_rel
            else:
                band_dropped = True
        if not chosen_rel and not band_dropped:
            if team_identity_rel and (Path(photos_root) / team_identity_rel).exists():
                if _photo_category_matches(profile, team_identity_rel, "team"):
                    chosen_rel = team_identity_rel
                else:
                    band_dropped = True
        if not chosen_rel and not band_dropped:
            if (Path(photos_root) / site_04_rel).exists():
                chosen_rel = site_04_rel
        if chosen_rel:
            href = _photo_href(chosen_rel, photos_root, out_dir)
            story_img_html = f'''<div class="story-img">
        <img src="{href}" alt="{founder_alt}" />
        {caption_html}
      </div>'''

    # Story-grid body — paragraphs + owners line (name, title, license, affiliations)
    license_no = pick(profile, "credentials", "licenseNumber") or ""
    license_type = pick(profile, "credentials", "licenseType") or ""
    owners_list = pick(profile, "owners", "list") or []
    owner_lines = []
    if owners_list:
        o = owners_list[0]
        owner_full = owner_full_name(o)
        # Owner title cascade: o.title → o.role → generic "Founder". Never
        # invent a trade-noun the data doesn't carry.
        owner_title = o.get("title") or o.get("role") or "Founder"
        # P14 drop-cleanly: when the name field is empty, the entire
        # {name + comma + role} unit suppresses. The leading-comma artifact
        # ("<strong></strong>, Founder") was the Round-4 close-package symptom
        # on Testerman's; root cause was schema mismatch between profile shapes,
        # surfaced because the comma+role still emitted on an empty name.
        if owner_full:
            owner_lines.append(f'<div><strong>{owner_full}</strong>, {owner_title}</div>')
        elif owner_title and owner_title != "Founder":
            owner_lines.append(f'<div>{owner_title}</div>')
    if license_no:
        license_label = license_type or "Licensed and insured"
        owner_lines.append(f'<div>{license_no} · {license_label}</div>')
    affiliations = pick(profile, "credentials", "affiliations") or []
    if affiliations:
        # Take first affiliation as the "primary" line
        owner_lines.append(f'<div>{affiliations[0]}</div>')
    owner_lines_html = "\n          ".join(owner_lines)
    owners_block = f'<div class="story-owners">\n          {owner_lines_html}\n        </div>' if owner_lines else ""

    grid_class = "story-grid" if story_img_html else "story-grid story-grid--text-only"
    story_section = f'''<section class="story" id="story">
  <div class="wrap">
    <div class="{grid_class}">
      {story_img_html}
      <div class="story-body">
        {story_paras_html}
        {owners_block}
      </div>
    </div>
  </div>
</section>'''

    # Cred-grid — flagship cells (License / Insurance / Award / Affiliation / Reviews / Experience)
    rating = ctx["rating"]
    review_count = ctx["review_count"]
    # Insurance: prefer explicit string; fall back to boolean `insured: true`.
    insurance = pick(profile, "credentials", "insurance") or ""
    insured_bool = pick(profile, "credentials", "insured")
    # Awards: profile may carry the headline as a string OR a list of strings/dicts.
    awards_raw = pick(profile, "credentials", "awards")
    awards_list = pick(profile, "credentials", "awardsList") or []
    veteran = pick(profile, "identity", "veteranOwned") or pick(profile, "credentials", "veteranOwned")
    family_op = pick(profile, "identity", "familyOperated") or pick(profile, "credentials", "familyOperated")
    years = pick(profile, "credentials", "yearsInBusiness") or pick(profile, "credentials", "yearsInBusinessStated")

    cred_cells = []
    if license_no:
        cred_cells.append(("License", f"<em>{license_no}</em>. Verifiable through state license records."))
    if insurance:
        cred_cells.append(("Insurance", "Licensed <em>and</em> insured. Both, on every job, residential and commercial." if "liability" in insurance.lower() else insurance))
    elif insured_bool:
        cred_cells.append(("Insurance", "Licensed <em>and</em> insured. Both, on every job, residential and commercial."))
    award_text = ""
    if isinstance(awards_raw, list) and awards_raw:
        first = awards_raw[0]
        award_text = first if isinstance(first, str) else first.get("name", "")
    elif isinstance(awards_raw, str) and awards_raw.strip():
        award_text = awards_raw.strip()
    elif awards_list and isinstance(awards_list[0], (str, dict)):
        first = awards_list[0]
        award_text = first if isinstance(first, str) else first.get("name", "")
    if award_text:
        cred_cells.append(("Award", award_text))
    if affiliations:
        cred_cells.append(("Affiliation", affiliations[0]))
    if rating and review_count:
        rating_f = float(rating)
        cell_text = f"★ {rating_f:.1f} from {review_count} verified Google reviews."
        # Italic accent only fires when the rating supports the claim — below
        # the 4.95 floor "Not one below five stars" is false (Bug 1C: Goneys at
        # 4.7 emitted the claim regardless). Above floor: emit. Below: basic
        # fact stands alone, no false flourish.
        if rating_f >= 4.95:
            cell_text += " <em>Not one below five stars</em>."
        cred_cells.append(("Reviews", cell_text))
    if years and str(years).isdigit():
        cred_cells.append(("Experience", f"<em>{years}+ years</em> in the trade. Trained continuously. Same crew."))
    if (veteran or family_op) and len(cred_cells) < 4:
        bits = []
        if veteran: bits.append("Veteran-owned")
        if family_op: bits.append("family-operated")
        cred_cells.append(("Ownership", ", ".join(bits) + "."))

    cred_cells_html = "\n      ".join(
        f'''<div class="cred-cell">
        <div class="l">{label}</div>
        <div class="v">{value}</div>
      </div>''' for label, value in cred_cells[:6]
    )
    cred_section = ""
    if cred_cells:
        cred_intro = prose_page.get("creds_lede") or "The credentials below are on the public record. Every number, every date, every name independently verifiable."
        cred_section = f'''<section class="page-section" style="background:var(--color-cream)">
  <div class="wrap">
    <h2>The credentials, <em>named</em>.</h2>
    <p class="lead">{cred_intro}</p>
    <div class="cred-grid">
      {cred_cells_html}
    </div>
  </div>
</section>'''

    # Where-we-work — service area band
    cities = pick(profile, "contact", "serviceAreaCities") or []
    counties = pick(profile, "contact", "serviceAreaCounties") or []
    where_we_work_text = prose_page.get("where_we_work") or ""
    if not where_we_work_text:
        bits = []
        bits.append(f"Headquartered in {ctx['city_state'].split(',')[0].strip()}.")
        if counties:
            bits.append(f"Serving {', '.join(counties[:5])} counties.")
        if cities:
            bits.append(f"Cities we work in regularly: {', '.join(cities[:5])}.")
        bits.append("Same crew, same phone, same person who picks up.")
        where_we_work_text = " ".join(bits)
    where_section = f'''<section class="page-section">
  <div class="wrap">
    <h2>Where we <em>work</em>.</h2>
    <p class="lead">{where_we_work_text}</p>
  </div>
</section>'''

    # Brand-band — site-07 placement (page coda, before the footer)
    brand_band_html = ""
    if photos_root and out_dir is not None:
        site_07_rel = "assets/photos/site/site-07.jpg"
        if (Path(photos_root) / site_07_rel).exists():
            href = _photo_href(site_07_rel, photos_root, out_dir)
            tag = ctx.get("tagline") or ""
            alt = f"{ctx['business_name']}{'. ' + tag + '.' if tag else ''}"
            brand_band_html = f'''<section class="brand-band">
  <img src="{href}" alt="{alt}">
</section>'''

    page_hero = _page_hero_html(prose_page, "about", ctx)
    footer = render_footer(ctx)
    mobile_cta = render_mobile_cta_bar(ctx)
    return f'''<a href="#main" class="skip-link">Skip to content</a>

{_inner_sitenav_html(ctx, "about")}

<main id="main">
  {page_hero}

  {story_section}

  {cred_section}

  {where_section}

  {brand_band_html}
</main>

{footer}

{mobile_cta}'''


def render_services_page(ctx: dict) -> str:
    """Bundle §3 .services-bento overview + §4 .service-detail-section blocks.
    services.html emits .faq-section ONLY when profile.faq[] exists and is
    non-empty. The detail blocks alternate via .service-detail--reverse."""
    prose_page = ctx["all_prose"].get("services") or {}
    services = ctx["services"]
    detail_descs = prose_page.get("service_detail_descriptions") or []
    # Index detail descriptions by slug for stable lookup
    detail_by_slug = {d.get("slug"): d for d in detail_descs if d.get("slug")}

    overview_eyebrow = prose_page.get("overview_eyebrow", "THE WHOLE SHOP")
    overview_title = prose_page.get("overview_title", "Every trade, on <em>one page</em>.")
    overview_subtitle = prose_page.get("overview_subtitle", "")
    subtitle_html = f'<p class="services-subtitle">{overview_subtitle}</p>' if overview_subtitle else ""

    # Bento: first service is "featured" (full-width on top), remaining 5 in grid
    bento_cards = []
    for i, svc in enumerate(services):
        slug = svc.get("slug", "")
        anchor = f"service-{slug}" if slug else f"service-{i}"
        name = svc.get("name", "")
        desc = svc.get("description", "")
        if i == 0:
            # v1.1 Session 2 Patch 2: adaptive top-overlay opacity, same
            # pattern as homepage bento. None when no luminance data —
            # CSS falls through to Phase 0.5 floor inside var().
            lum = _resolve_photo_luminance(
                ctx.get("profile") or {},
                svc.get("featuredImage") or "",
                ctx.get("photos_root"),
            )
            top_op = _resolve_overlay_top_opacity(lum, baseline=0.45)
            bento_cards.append(_render_bento_featured_card(svc, anchor, top_opacity=top_op))
        else:
            # Audit-driven correction 2026-04-29 — restore homepage-bento
            # pattern across services.html non-featured cards: photo backdrops
            # only on featured card; non-featured cards render text-only with
            # clean cream backdrop and dark text. The prior photo-backdrop
            # branch produced six-photo bento overviews where card text bled
            # into bright photo zones across all three live prospects (caught
            # at audit-hat cold-walk). Photos are not lost: each service's
            # detail block below the overview retains its featuredImage +
            # detailImage via the side-by-side article layout.
            bento_cards.append(f'''<a href="#{anchor}" class="service-card" style="text-decoration:none; color:inherit;">
          <h3 class="service-card-title-sm">{name}</h3>
          <p class="service-card-desc-sm">{desc}</p>
        </a>''')
    bento_html = "\n        ".join(bento_cards)

    # Detail blocks
    detail_section_eyebrow = prose_page.get("detail_section_eyebrow", "ON THE BENCH")
    detail_section_title = prose_page.get("detail_section_title", "Each trade, <em>by hand</em>.")
    details_html = []
    for i, svc in enumerate(services):
        slug = svc.get("slug", "")
        anchor = f"service-{slug}" if slug else f"service-{i}"
        d = detail_by_slug.get(slug, {})
        index_label = d.get("index_label") or f"{i+1:02d} · {svc.get('name', '').upper()}"
        title = d.get("title") or svc.get("tagline") or svc.get("name", "")
        description = d.get("description") or svc.get("description", "")
        bullets = d.get("bullets") or []
        bullets_html = "\n            ".join(f"<li>{b}</li>" for b in bullets)
        bullets_block = f'<ul class="service-detail-list">\n            {bullets_html}\n          </ul>' if bullets else ""
        tag = d.get("tag", "")
        tag_html = f'<span class="service-detail-tag">{tag}</span>' if tag else ""
        reverse = " service-detail--reverse" if i % 2 == 1 else ""
        detail_href = svc.get("detailImageHref") or ""
        # When a photo is supplied, override the CSS empty-card defaults so
        # the photo fills the slot edge-to-edge: drop padding, set bg-cover,
        # transparent bg-color so the image isn't washed by the white default.
        detail_img_style = (
            f' style="background-image:url(\'{detail_href}\');background-size:cover;background-position:center;padding:0;background-color:transparent;"'
            if detail_href else ""
        )
        details_html.append(f'''<article class="service-detail{reverse}" id="{anchor}">
        <div class="service-detail-text">
          <div class="service-detail-eyebrow">{index_label}</div>
          <h3 class="service-detail-title">{title}</h3>
          <p class="service-detail-desc">{description}</p>
          {bullets_block}
          {tag_html}
        </div>
        <div class="service-detail-image"{detail_img_style} aria-hidden="true"></div>
      </article>''')

    # FAQ + contact-section dropped from services.html.
    # Both live on the homepage now per the canonical close-the-deal sequence.
    # Inner pages stay focused on their reason-to-exist content.
    # services hero promoted from .subpage-hero
    # (navy field, no imagery — read as "lite hero" competing with the
    # homepage truck composition) to .page-hero (paper-warm rhyme with
    # about/testimonials/contact). Per Design audit Q2 finding: "Mixed-state
    # is the worst option." Three of four inner pages already use page-hero;
    # services now joins the rhyme.
    # license caption emitted as a small below-lede
    # row when profile.credentials.licenseNumber is present, per Design's
    # tightening note: license-as-credential wants its own register, not
    # buried in the services subhead body sentence. Caption is engine-
    # derived from profile data (not prose-authored) — every prospect with
    # a license number gets the treatment automatically.
    license_no = pick(ctx["profile"], "credentials", "licenseNumber")
    hero_caption_html = ""
    if license_no:
        # Strip wide spaces in stored value ("EC # 13006598" → "EC#13006598")
        license_clean = re.sub(r"\s+", "", license_no)
        hero_caption_html = f'<p class="page-hero-caption">Florida license {license_clean}</p>'
    page_hero = _page_hero_html(prose_page, "services", ctx, extra_html=hero_caption_html)
    footer = render_footer(ctx)
    return f'''<a href="#main" class="skip-link">Skip to content</a>

{_inner_sitenav_html(ctx, "services")}

<main id="main">
  {page_hero}

  <section class="services-section">
    <div class="services-container">
      <div class="services-header">
        <div class="services-eyebrow">{overview_eyebrow}</div>
        <h2 class="services-title">{overview_title}</h2>
        {subtitle_html}
      </div>
      <div class="services-bento">
        {bento_html}
      </div>
    </div>
  </section>

  <section class="service-detail-section">
    <div class="service-detail-container">
      <div class="service-detail-section-header">
        <div class="service-detail-section-eyebrow">{detail_section_eyebrow}</div>
        <h2 class="service-detail-section-title">{detail_section_title}</h2>
      </div>
      {"".join(details_html)}
    </div>
  </section>
</main>

{footer}'''


def render_testimonials_page(ctx: dict) -> str:
    """Bundle .testimonials-section with .testimonials-grid carrying the
    curated set.

    page-aware caps per Decision 1. When ≥1
    testimonial has `featured: true`, ship a hard 6-cap (featured-first,
    score-fill the rest if fewer than 6 featured). When zero featured,
    fall back to ship-all — the scorer doesn't know
    which 6 of N are editorially strongest, so an un-curated prospect
    surfaces every >=4-star review."""
    prose_page = ctx["all_prose"].get("testimonials") or {}
    profile = ctx["profile"]
    site = pick(profile, "testimonials", "fromSite") or []
    google = pick(profile, "testimonials", "fromGoogleReviews") or []
    pool = []
    for t in site:
        if t.get("quote"):
            pool.append({**t, "rating": t.get("rating", 5), "source_tier": "site"})
    for t in google:
        if t.get("quote"):
            pool.append({**t, "rating": t.get("rating", 5), "source_tier": "google"})
    pool = [t for t in pool if (t.get("rating") or 5) >= 4]
    # testimonials.html cap raised 6 → 12.
    # Featured-first sort, then score-fill from non-featured pool. The
    # dedicated reviews page should be heavier than the homepage section,
    # not the same.
    has_featured = any(t.get("featured") for t in pool)
    pool.sort(key=lambda t: (not t.get("featured", False), -_testimonial_score(t)))
    if has_featured:
        pool = pool[:12]

    rating = ctx["rating"]
    review_count = ctx["review_count"]

    # split pool into site-tier and google-tier groups.
    # Site testimonials render in the FIRST t-grid ("From our site"), google
    # reviews in the SECOND ("From Google"). pq-band sits between them as
    # the pullquote-band opener of the lower section.
    site_pool = [t for t in pool if t.get("source_tier") == "site"][:7]
    google_pool = [t for t in pool if t.get("source_tier") == "google"][:5]

    def _t_card(t: dict, source_label: str) -> str:
        first = t.get("firstName", "")
        last = t.get("lastName", "")
        name = f"{first} {last}".strip() or first or t.get("name") or "[Reviewer name]"
        role = t.get("role", "")
        location = t.get("location", "")
        who_bits = [f"<strong>{name}</strong>"]
        if role:
            who_bits.append(role)
        if location:
            who_bits.append(location)
        who_line = ", ".join(who_bits[1:])
        if who_line:
            who_html = f"<strong>{name}</strong>, {who_line}"
        else:
            who_html = f"<strong>{name}</strong>"
        return f'''<div class="t-card">
        <div class="stars">★★★★★</div>
        <blockquote>{t.get("quote", "")}</blockquote>
        <div class="who">{who_html}<span class="src">{source_label}</span></div>
      </div>'''

    site_cards_html = "\n      ".join(_t_card(t, "Homepage testimonials block") for t in site_pool)
    google_cards_html = "\n      ".join(_t_card(t, "Google Places review") for t in google_pool)

    # Page-hero metrics — drop the "0 below five stars" tile when rating
    # is exactly 5.0 (the metric is meaningless and reads as broken/unloaded
    # data per Design audit). Two confident metrics > three with
    # a soft third. Generalizes correctly: any prospect at perfect rating
    # gets the cleaner pair.
    metrics_html = ""
    if rating and review_count:
        metrics = [
            f'''<div class="metric">
        <div class="v">{float(rating):.1f}</div>
        <div class="l">Google rating</div>
      </div>''',
            f'''<div class="metric">
        <div class="v">{review_count}</div>
        <div class="l">Reviews</div>
      </div>''',
        ]
        # Phase 0.5 fix 2026-04-29: removed conditional that added a
        # "0 / Below five stars" tile when rating < 5.0. The claim is
        # mathematically false against any rating below 5.0 (a 4.7 rating
        # over 65 reviews implies ~25% of reviews are NOT five-star, so
        # "0 below five stars" fabricates the claim). Master invariant:
        # never synthesize unsupported data claims. Two confident metrics
        # (rating + review count) ship cleanly at canonical 2-tier; the
        # third tile sparse-drops when no honest stat earns rent.
        metrics_html = f'''<div class="metrics">
      {chr(10).join(metrics)}
    </div>'''

    # Section headings (overridable via prose)
    site_section_title = prose_page.get("site_section_title") or "From <em>our site.</em>"
    google_section_title = prose_page.get("google_section_title") or "From <em>Google.</em>"

    # Layout adapt: when site_pool has <2 entries, drop the bipartite split
    # and merge all reviews into a single grid. The 1-card-with-empty-space
    # layout reads broken on prospects whose source site doesn't embed many
    # site testimonials (most prospects). Round-3 fix Session 3 close
    # (2026-04-29). When site_pool >= 2 entries, keep the bipartite split.
    site_section = ""
    google_section = ""
    google_names = ", ".join(
        f'{t.get("firstName", "")} {t.get("lastName", "")}'.strip() or t.get("name", "")
        for t in google_pool
        if (t.get("firstName") or t.get("lastName") or t.get("name"))
    )
    google_attr = ""
    if google_names:
        google_attr = f'<p style="font-family:\'Figtree\',sans-serif;font-size:13px;color:var(--color-primary);margin-top:32px;letter-spacing:.04em">Reviews provided by Google. Contributors: {google_names}.</p>'

    if len(site_pool) >= 2:
        # Bipartite layout: keep split.
        site_section = f'''<section class="page-section">
  <div class="wrap">
    <h2>{site_section_title}</h2>
    <div class="t-grid">
      {site_cards_html}
    </div>
  </div>
</section>'''
        if google_pool:
            google_section = f'''<section class="page-section" style="background:var(--color-paper-warm)">
  <div class="wrap">
    <h2>{google_section_title}</h2>
    <div class="t-grid">
      {google_cards_html}
    </div>
    {google_attr}
  </div>
</section>'''
    else:
        # Unified layout: merge site + google into one grid.
        all_cards_html = "\n      ".join(
            _t_card(t, "Homepage testimonials block" if t.get("source_tier") == "site" else "Google Places review")
            for t in (site_pool + google_pool)
        )
        unified_title = google_section_title if google_pool else site_section_title
        google_section = f'''<section class="page-section" style="background:var(--color-paper-warm)">
  <div class="wrap">
    <h2>{unified_title}</h2>
    <div class="t-grid">
      {all_cards_html}
    </div>
    {google_attr}
  </div>
</section>'''

    page_hero = _page_hero_html(prose_page, "testimonials", ctx, extra_html=metrics_html)
    footer = render_footer(ctx)
    mobile_cta = render_mobile_cta_bar(ctx)
    return f'''<a href="#main" class="skip-link">Skip to content</a>

{_inner_sitenav_html(ctx, "testimonials")}

<main id="main">
  {page_hero}

  {site_section}

  {google_section}
</main>

{footer}

{mobile_cta}'''


def render_contact_page(ctx: dict) -> str:
    """flagship-canonical contact page.

    Editorial arc:
      page-hero (eyebrow + h1 + lede)
      → contact-grid (info col with 4 .contact-row + form col with simplified form)
      → area-band (service area: cities + counties as 2-col list)
      → footer

    The form inside .contact-grid uses the existing .contact-form-wrap CSS
    with a simpler label set (Name / Email / Phone optional / How can we help).
    StaticForms accessKey plumbs through ctx.
    """
    prose_page = ctx["all_prose"].get("contact") or {}
    profile = ctx["profile"]
    phone = ctx["phone_display"]
    tel = phone_tel_href(phone)
    addr1 = ctx["address_line1"]
    addr2 = ctx["address_line2"]
    license_no = pick(profile, "credentials", "licenseNumber") or ""
    license_type = pick(profile, "credentials", "licenseType") or ""
    hours_full = ctx["hours_full"]

    # Build the four contact-rows (Call/Address/Hours/License) from chassis data.
    contact_rows = []
    if phone:
        contact_rows.append(f'''<div class="contact-row">
      <div class="l">Call or Text</div>
      <div class="v phone"><a href="{tel}">{phone}</a></div>
    </div>''')
    if addr1:
        addr_html = addr1
        if addr2:
            addr_html = f"{addr1}<br>{addr2}"
        contact_rows.append(f'''<div class="contact-row">
      <div class="l">Address</div>
      <div class="v">{addr_html}</div>
    </div>''')
    if hours_full:
        hours_html = "<br>".join(hours_full[:3])
        contact_rows.append(f'''<div class="contact-row">
      <div class="l">Hours</div>
      <div class="v">{hours_html}</div>
    </div>''')
    if license_no:
        license_label = f"{license_no}. " + (license_type or "Licensed and insured.")
        contact_rows.append(f'''<div class="contact-row">
      <div class="l">License</div>
      <div class="v">{license_label}</div>
    </div>''')
    contact_rows_html = "\n\n    ".join(contact_rows)

    # Form heading + intro. form_intro accepts str (with optional inline
    # <em> / {em} shorthand) OR dict ({text, em_phrase}) — Patch 4 v1.1
    # Session 1 2026-04-30 added shape tolerance for parity with other
    # display-headline slots.
    form_intro = _resolve_inline_em_text(prose_page.get("form_intro")) or "Send a note"
    form_lede = prose_page.get("form_lede") or "The form below sends a direct message. We read everything and reply by phone or email, typically within one business day."
    intro_text = form_intro.rstrip(".")

    # Info-column heading — em-phrase dict shape per §6.6, OR flat string. The
    # f-string-on-dict leak (P16, surfaced Phase 0.5 cold-walk) emitted raw
    # Python repr ("{'text': 'How to reach us.', 'em_phrase': 'reach'}") into
    # the live h2. Bare <h2> is the intended emit shape — composer-system.css
    # `.contact-info h2` (and `.contact-info h2 em`) own the italic-accent
    # treatment for this surface; class="display" would double-style.
    # Routed through _resolve_inline_em_text Patch 5 v1.1 Session 1 2026-04-30
    # for the double-wrap guard — Bellair shipped <h2>How to <em><em>find us
    # </em></em>.</h2> when the author included inline <em> markup AND set
    # em_phrase pointing at the same span; the helper now detects existing
    # markup and skips the wrap step.
    info_text = _resolve_inline_em_text(prose_page.get("info_heading"))
    info_heading_html = f'<h2>{info_text}</h2>' if info_text else ""

    contact_grid = f'''<div class="contact-grid">

  <div class="contact-info">
    {info_heading_html}

    {contact_rows_html}
  </div>

  <div class="contact-form-wrap">
    <h2>{intro_text}.</h2>
    <p>{form_lede}</p>
    <form action="https://api.staticforms.xyz/submit" method="POST" class="contact-form">
      <input type="hidden" name="accessKey" value="{ctx.get("access_key", "REPLACE_WITH_STATICFORMS_KEY")}">
      <input type="hidden" name="subject" value="New contact from {ctx['business_name']} website">
      <input type="hidden" name="replyTo" value="@">
      <div class="contact-honeypot"><label>Do not fill: <input type="text" name="honeypot" tabindex="-1" autocomplete="off"></label></div>
      <label for="cf-name">Name</label>
      <input id="cf-name" type="text" name="name" required autocomplete="name">
      <label for="cf-email">Email</label>
      <input id="cf-email" type="email" name="email" required autocomplete="email">
      <label for="cf-phone">Phone (optional)</label>
      <input id="cf-phone" type="tel" name="phone" autocomplete="tel">
      <label for="cf-message">How can we help?</label>
      <textarea id="cf-message" name="message" rows="4" required></textarea>
      <button type="submit">Send Message</button>
    </form>
  </div>

</div>'''

    # Area-band — cities + counties served
    cities = pick(profile, "contact", "serviceAreaCities") or []
    counties = pick(profile, "contact", "serviceAreaCounties") or []
    area_intro = prose_page.get("area_intro") or ""
    area_cells = []
    if cities:
        cities_text = ", ".join(cities[:6]) + ", and the surrounding region."
        area_cells.append(f'''<div>
    <div class="l">Cities served regularly</div>
    {cities_text}
  </div>''')
    if counties:
        counties_text = ", ".join(counties[:6]) + "."
        area_cells.append(f'''<div>
    <div class="l">Counties served</div>
    {counties_text}
  </div>''')
    # Contact area-band abbreviated per Design audit.
    # The About page already carries the full "Where we work" treatment with
    # headline + cities + counties grid. Repeating the same density on Contact
    # makes the page feel like a slightly-lighter About — Design called it
    # "the same treatment at lower density." Single-line summary keeps the
    # information available without competing with the page's true anchor
    # (the phone number + form). Also drops the "Where we *work*" italic-
    # amber accent, helping the contact page stay under the 2-per-page accent
    # budget rule.
    cities_inline = " · ".join(cities[:5]) if cities else ""
    counties_inline = " · ".join(c + " County" for c in counties[:5]) if counties else ""
    parts = []
    if cities_inline:
        parts.append(cities_inline)
    if counties_inline:
        parts.append(counties_inline)
    area_summary = ". ".join(parts)
    area_section = ""
    if area_summary:
        area_section = f'''<section class="area-band area-band--summary">
  <div class="wrap">
    <p class="area-summary"><span class="area-summary-label">Service area</span>{area_summary}.</p>
  </div>
</section>'''

    page_hero = _page_hero_html(prose_page, "contact", ctx)
    footer = render_footer(ctx)
    mobile_cta = render_mobile_cta_bar(ctx)
    return f'''<a href="#main" class="skip-link">Skip to content</a>

{_inner_sitenav_html(ctx, "contact")}

<main id="main">
  {page_hero}

  {contact_grid}

  {area_section}
</main>

{footer}

{mobile_cta}'''


# ============================================================================
# 5. CONTEXT BUILDER
# ============================================================================

def build_ctx(profile: dict, prose: dict, photos_root: str | None, out_dir: Path, access_key: str = "REPLACE_WITH_STATICFORMS_KEY") -> dict:
    # prose.json migrated from flat keys to nested
    # page-key shape (homepage / about / services / testimonials / contact).
    # The homepage band renderers read ctx["prose"], so we point that at the
    # homepage sub-dict. Inner-page renderers read sibling pages via
    # ctx["all_prose"][page_key].
    all_prose = prose
    homepage_prose = prose.get("homepage") or {}
    # Prefer the canonical fields from Villages-style profile-draft.json.
    # v1.1 floor cut (2026-04-30): accept string OR dict at profile.businessName.
    # The dict shape {primary, legalEntity} is the documented canonical;
    # string is what operators naturally write when the field name reads
    # like a single value. Without this patch, string input silently falls
    # through the cascade to the "Business Name" literal default and ships
    # placeholder chrome on every surface (title, og:title, JSON-LD name,
    # nav wordmark, footer). Brehm observe-and-document run, Finding 32.
    _bn_raw = profile.get("businessName")
    business_name_primary = (
        (_bn_raw if isinstance(_bn_raw, str) and _bn_raw.strip() else None)
        or pick(profile, "businessName", "primary")
        or pick(profile, "identity", "commandAliasName")
        or pick(profile, "identity", "siteTitle")
        or pick(profile, "identity", "legalNameOnSite")
        or "Business Name"
    )
    if business_name_primary == "Business Name":
        import sys
        print(
            "WARN: profile.businessName resolution fell through to literal "
            "'Business Name' placeholder. Set profile.businessName as a "
            "string OR as {primary, legalEntity} dict. (render.py business "
            "name cascade)",
            file=sys.stderr,
        )
    city_state_consensus = pick(profile, "contact", "addressConsensus") or ""
    # "13900 US-301, Summerfield, FL 34491" → city_state = "Summerfield, FL"
    parts = [p.strip() for p in city_state_consensus.split(",")]
    if len(parts) >= 3:
        city_state = f"{parts[-2]}, {parts[-1].split()[0]}"  # "Summerfield, FL"
    elif len(parts) == 2:
        city_state = city_state_consensus
    else:
        # Cascade through audit-captured geography fields. Empty when none — no fabrication.
        cities = pick(profile, "contact", "serviceAreaCities") or []
        counties = pick(profile, "contact", "serviceAreaCounties") or []
        city_state = (cities[0] if cities else "") \
                  or (counties[0] if counties else "") \
                  or ""

    phone_raw = pick(profile, "contact", "phone") or ""
    phone_display = normalize_phone(phone_raw)
    email = pick(profile, "contact", "email") or ""
    addr_canonical = pick(profile, "contact", "addressCanonical") or city_state_consensus
    addr_parts = [p.strip() for p in addr_canonical.split(",")]
    addr_line1 = addr_parts[0] if addr_parts else ""
    addr_line2 = ", ".join(addr_parts[1:]) if len(addr_parts) > 1 else ""

    # Hours
    hours = pick(profile, "contact", "hours") or {}
    hours_full_list = []
    order = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    weekday_abbrev = {"monday": "Mon", "tuesday": "Tue", "wednesday": "Wed", "thursday": "Thu", "friday": "Fri", "saturday": "Sat", "sunday": "Sun"}
    # Collapse the 3-line format
    weekday_hours = {}
    for d in order[:5]:
        v = hours.get(d)
        if v and v.lower() != "closed":
            weekday_hours[d] = v
    sat = hours.get("saturday")
    sun = hours.get("sunday")
    # Aggregate
    if weekday_hours:
        # group by identical hours
        groups: dict[str, list[str]] = {}
        for d, v in weekday_hours.items():
            groups.setdefault(v, []).append(weekday_abbrev[d])
        for v, days in groups.items():
            if len(days) == 1:
                label = days[0]
            else:
                label = f"{days[0]} to {days[-1]}"
            hours_full_list.append(f"{label} · {_clean_hours(v)}")
    if (sat and sat.lower() != "closed") or (sun and sun.lower() != "closed"):
        # Include weekend
        if sat and sat.lower() != "closed":
            hours_full_list.append(f"Sat · {_clean_hours(sat)}")
        if sun and sun.lower() != "closed":
            hours_full_list.append(f"Sun · {_clean_hours(sun)}")
    else:
        hours_full_list.append("Sat &amp; Sun · By appointment")

    # Hours short (for anchor strip)
    if weekday_hours:
        first_v = list(weekday_hours.values())[0]
        hours_short = f"Mon to Fri · {_clean_hours(first_v)}"
    else:
        hours_short = "By appointment"

    # Service cities
    cities = pick(profile, "contact", "serviceAreaCities") or []
    if cities:
        service_cities_str = " · ".join(cities[:3])
    else:
        service_cities_str = city_state

    # Palette
    palette = resolve_palette(profile)

    # Hero photo
    hero = resolve_hero_photo(profile, photos_root)
    hero_path = hero["path"]
    hero_photo_href = _photo_href(hero_path, photos_root, out_dir)
    story_img_href = None  # Engine may set from photo classification later

    # brand mark resolution. Prefer the prospect's
    # captured brand asset (assets/photos/site/site-09.jpg) for the .wm-mark
    # slot in nav and footer. Falls back to the inline-SVG placeholder when
    # the asset is absent (Volthom ships site-09; future prospects vary).
    brand_mark_html = resolve_brand_mark_html(photos_root, out_dir, profile)
    # Round-4-cleanup (2026-04-29): inner-page sitenav uses sticky-translucent
    # cool-white treatment per composer-system.css line 1278+ — the homepage
    # white-on-transparent logo variant disappears against that background.
    # Compute the color-variant brand mark for inner-page surfaces (reads
    # profile.logo.fallbackLocalPath when present).
    brand_mark_html_inner = resolve_brand_mark_html(photos_root, out_dir, profile, for_inner_page=True)

    # Stats trio + trust
    stats_trio = resolve_stats_trio(profile)
    trust_cells = resolve_trust_cells(profile, stats_trio)
    # Trust marquee items (homepage band 02 flagship-canonical).
    # Floor at >=3 items; below that, the homepage flow falls back to .anchor-strip.
    trust_items = resolve_trust_items(profile, prose)

    # 4th tile for the dark stats band ("named
    # distinguishing fact"). Five-rule library with explicit floors per
    # dropped-sections.md §5. Returns None when no signal exceeds its floor —
    # render_stats_band falls back to a 3-tile grid in that case.
    distinguishing_stat_used = [s.get("label", "") for s in stats_trio]
    distinguishing_stat_used += [c.get("label", "") for c in trust_cells]
    distinguishing_stat = resolve_distinguishing_stat(profile, distinguishing_stat_used)

    # Optional homepage bands. featuredPromo is an authored input
    # (fixture-contract.md). beforeAfterPairs is photo-pairing data.
    featured_promo = pick(profile, "promotions", "featuredPromo")
    before_after_pairs = pick(profile, "photoLibrary", "beforeAfterPairs") or []

    # Services. if a service ships a `featuredImage`
    # path, resolve it through `_photo_href` and stash on the service dict so
    # `render_services` can emit it as an inline background-image on the
    # `.service-card-featured` slot. Falls back to CSS gradient when absent.
    # also wire `detailImage` per service. Without it
    # the services-page service-detail-image slot renders as an empty white
    # card. Same pattern as featuredImage; same _photo_href resolution; falls
    # back to the CSS-styled empty card when absent.
    # resolve_service_photos pre-populates the
    # featuredImage / detailImage fields from `_unsplash-cache.json` for any
    # service slug whose fixture leaves them null. Slugs flagged
    # gradient_fallback in the cache stay null and ship the CSS gradient.
    resolve_service_photos(profile, photos_root)
    services = resolve_service_list(profile)
    for svc in services:
        fi_path = svc.get("featuredImage") or ""
        if fi_path:
            svc["featuredImageHref"] = _photo_href(fi_path, photos_root, out_dir)
        di_path = svc.get("detailImage") or ""
        if di_path:
            svc["detailImageHref"] = _photo_href(di_path, photos_root, out_dir)

    # Testimonials — merge fromSite[] and fromGoogleReviews[] per v2 fixture-contract
    # rev 2026-04-24 (Volt fixture drove this patch). Scoring rules:
    #   +30 named role/title (e.g. "CEO, Nature Coast Bank")
    #   +20 named location (e.g. "The Villages")
    #   +0..15 quote length / 15 (long quotes have more substance)
    #   +15 project/trade specificity (a real noun: generator, panel, pergola, pavers, ...)
    #   -10 generic-praise penalty (matches stock phrasing, under 100 chars)
    # Site testimonials are assumed 5-star since the prospect chose to feature them.
    testimonials = resolve_testimonials(profile)

    # FAQ — derive 5–7 items from profile data, or
    # honor a prose.services.faq[] author override. Mutates profile in memory
    # only so the existing render_services_page band gate sees `profile.faq[]`
    # as non-empty. No write-back to disk per the "fixtures are authored truth"
    # principle.
    profile["faq"] = resolve_faq(profile, prose)

    # Owner names rendered
    owners_list = pick(profile, "owners", "list") or []
    if len(owners_list) >= 2:
        last_name = owners_list[0].get("lastName", "")
        first_names = [o.get("firstName", "") for o in owners_list]
        owner_names_html = f'{" &amp; ".join(first_names)} {last_name}'.strip()
    elif len(owners_list) == 1:
        o = owners_list[0]
        owner_names_html = f'{o.get("firstName", "")} {o.get("lastName", "")}'.strip()
    else:
        owner_names_html = ""

    rating = pick(profile, "googleBusiness", "rating")
    review_count = pick(profile, "googleBusiness", "reviewCount")
    tagline = pick(profile, "identity", "tagline")

    return {
        "profile":               profile,
        "prose":                 homepage_prose,
        "all_prose":             all_prose,
        "palette":               palette,
        "business_name":         business_name_primary,
        "city_state":            city_state,
        "service_cities_str":    service_cities_str,
        "phone_display":         phone_display,
        "email":                 email,
        "address_line1":         addr_line1,
        "address_line2":         addr_line2,
        "hours_short":           hours_short,
        "hours_full":            hours_full_list,
        "hero_photo_href":       hero_photo_href,
        "story_img_href":        story_img_href,
        "brand_mark_html":       brand_mark_html,
        "brand_mark_html_inner": brand_mark_html_inner,
        "photos_root":           photos_root,
        "out_dir":               out_dir,
        "stats_trio":            stats_trio,
        "trust_cells":           trust_cells,
        "trust_items":           trust_items,
        "distinguishing_stat":   distinguishing_stat,
        "featured_promo":        featured_promo,
        "before_after_pairs":    before_after_pairs,
        "services":              services,
        "testimonials":          testimonials,
        "owner_names":           owner_names_html,
        "rating":                rating,
        "review_count":          review_count,
        "tagline":               tagline,
        "access_key":            access_key,
        "warnings":              hero["warnings"],
        "wordmark_text_visible": pick(profile, "identity", "wordmarkTextVisible") if pick(profile, "identity", "wordmarkTextVisible") is not None else True,
    }


def _clean_hours(v: str) -> str:
    """'7:00 AM – 3:30 PM' → '7 AM to 3:30 PM'."""
    if not v:
        return v
    v = v.replace("\u00a0", " ").replace("\u202f", " ").replace("\u2009", " ")
    v = v.replace("–", "to").replace("-", "to")
    v = re.sub(r":00(\s+[AP]M)", r"\1", v)
    v = re.sub(r"\s+", " ", v).strip()
    return v


def _compute_photo_luminance(file_path: str) -> float | None:
    """Mean luminance of file_path as 0–1 float, or None when Pillow is
    unavailable or the file can't be opened. Pillow is lazy-imported per
    image-handling.md L836 (pre-blessed library) and the v1.1 Session 2
    design rationale: adaptive overlay needs luminance, basic rendering
    does not — keep the dependency footprint accurate to actual usage.
    Sparse-drop class: any failure returns None and the caller falls
    through to the CSS overlay-floor default via var() fallback."""
    try:
        from PIL import Image, ImageStat
    except ImportError:
        return None
    try:
        with Image.open(file_path) as img:
            return ImageStat.Stat(img.convert("L")).mean[0] / 255.0
    except (OSError, ValueError):
        return None


def _resolve_photo_metadata(profile: dict, rel_path: str) -> dict:
    """Return the per-photo metadata entry for rel_path, or {} when absent.
    Single chokepoint for all per-photo metadata reads — luminance (Patch 1),
    category (Patch 3), disqualifyFromHero / disqualifyReason (Patch 4).

    Schema (v1.1 Session 2, 2026-04-30): metadata lives at
    `profile.photoLibrary.photos[<rel_path>]`, not as inline fields on each
    photoLibrary slot. Existing string-shaped slots (ownerPortrait,
    teamIdentity, hero candidate lists) stay unchanged; one uniform lookup
    path covers any photo regardless of which slot references it. The
    `photos` map is keyed by the same relative path string the slots use,
    so cross-references match without normalization."""
    photos = ((profile.get("photoLibrary") or {}).get("photos") or {})
    return photos.get(rel_path) or {}


def _resolve_photo_luminance(profile: dict, rel_path: str,
                              photos_root: str | None) -> float | None:
    """Read profile.photoLibrary.photos[rel_path].luminance if present;
    otherwise lazy-compute via _compute_photo_luminance, write back to the
    in-memory profile dict (not to disk), and return. Sparse-drop class:
    returns None when rel_path empty, photos_root unset, file missing, or
    Pillow failure. Caller falls through to CSS overlay-floor default via
    var() fallback. The in-memory writeback memoizes per-render — a photo
    referenced by multiple slots (hero + service-card backdrop) computes
    once per render, not per reference."""
    if not rel_path or not photos_root:
        return None
    meta = _resolve_photo_metadata(profile, rel_path)
    cached = meta.get("luminance")
    if isinstance(cached, (int, float)):
        return float(cached)

    abs_path = Path(photos_root) / rel_path
    if not abs_path.exists():
        return None
    luminance = _compute_photo_luminance(str(abs_path))
    if luminance is None:
        return None

    photo_lib = profile.setdefault("photoLibrary", {})
    photos_map = photo_lib.setdefault("photos", {})
    entry = photos_map.setdefault(rel_path, {})
    entry["luminance"] = luminance
    return luminance


def _photo_href(path: str, photos_root: str | None, out_dir: Path) -> str:
    if not path:
        return ""
    if path.startswith(("http://", "https://", "/")):
        return path
    # path is e.g. 'assets/photos/google/gp-09.jpg' relative to photos_root
    if photos_root:
        abs_src = Path(photos_root) / path
        try:
            rel = os.path.relpath(abs_src, out_dir)
            return rel
        except ValueError:
            return str(abs_src)
    return path


# Google photo attribution. Per-page Google attribution required whenever
# assets/photos/google/* photos are emitted. _attributions.json is the per-photo
# source of truth — never hardcode profile.businessName.legal as the contributor
# (it's only coincidentally correct for owner-uploaded photos like Volthom; most
# prospects ship customer-contributed photos).
_GOOGLE_PHOTO_REF_RE = re.compile(r"assets/photos/google/([^\s\"')]+)")
_ATTRIBUTION_NAME_RE = re.compile(r"<a[^>]*>([^<]+)</a>")


def _load_google_attribution_map(photos_root: str | None) -> dict[str, str]:
    """Read assets/photos/google/_attributions.json under photos_root and return
    {filename: contributor_name}. Indexed by both basename ('gp-01.jpg') and the
    profile-relative path ('assets/photos/google/gp-01.jpg') for lookup
    flexibility. Returns {} if the manifest is absent or unreadable."""
    if not photos_root:
        return {}
    attr_path = Path(photos_root) / "assets" / "photos" / "google" / "_attributions.json"
    if not attr_path.exists():
        return {}
    try:
        entries = json.loads(attr_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    out: dict[str, str] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        f = entry.get("file") or ""
        m = _ATTRIBUTION_NAME_RE.search(entry.get("attribution_html") or "")
        if f and m:
            name = m.group(1).strip()
            out[f] = name
            out[f.rsplit("/", 1)[-1]] = name
    return out


def _collect_google_contributors(html: str, attribution_map: dict[str, str]) -> list[str]:
    """Scan rendered HTML for assets/photos/google/* references and return the
    deduped contributor names in first-appearance order."""
    if not attribution_map:
        return []
    contributors: list[str] = []
    seen: set[str] = set()
    for match in _GOOGLE_PHOTO_REF_RE.finditer(html):
        basename = match.group(1).split("?", 1)[0]
        name = attribution_map.get(basename)
        if name and name not in seen:
            contributors.append(name)
            seen.add(name)
    return contributors


# Unsplash attribution. The Unsplash API Terms require
# per-photo credit linking back to the photographer's Unsplash profile and to
# unsplash.com itself. Footer surfaces a deduped list of photographers in
# first-appearance order, alongside the existing Google attribution row.
_UNSPLASH_PHOTO_REF_RE = re.compile(r"assets/photos/unsplash/([a-zA-Z0-9_\-]+\.jpg)")
_UNSPLASH_UTM = "utm_source=GRM_Composer&utm_medium=referral"


def _load_unsplash_cache(photos_root: str | None) -> dict:
    """Read assets/photos/unsplash/_unsplash-cache.json. Returns {} if absent."""
    if not photos_root:
        return {}
    p = Path(photos_root) / "assets" / "photos" / "unsplash" / "_unsplash-cache.json"
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _collect_unsplash_attributions(html: str, cache: dict) -> list[dict]:
    """Scan rendered HTML for assets/photos/unsplash/*.jpg refs. Return deduped
    {name, html_url} list (by photographer name) in first-appearance order."""
    if not cache:
        return []
    by_filename: dict[str, dict] = {}
    for entry in cache.values():
        if not isinstance(entry, dict) or entry.get("gradient_fallback"):
            continue
        for slot in ("featured", "detail"):
            slot_data = entry.get(slot)
            if not isinstance(slot_data, dict):
                continue
            fn = slot_data.get("filename") or ""
            if fn:
                by_filename[fn] = {
                    "name": slot_data.get("photographer_name") or "Unsplash photographer",
                    "html_url": slot_data.get("photographer_html") or "https://unsplash.com",
                }
    out: list[dict] = []
    seen: set[str] = set()
    for match in _UNSPLASH_PHOTO_REF_RE.finditer(html):
        info = by_filename.get(match.group(1))
        if not info or info["name"] in seen:
            continue
        seen.add(info["name"])
        out.append(info)
    return out


def _unsplash_attribution_html(attributions: list[dict]) -> str:
    """Render the footer attribution block. Per Unsplash Terms each photo links
    photographer + 'Unsplash'. We dedupe by photographer name and emit one
    'Photo by <name>' fragment per unique photographer, with a single 'on
    Unsplash' tail link covering the row."""
    if not attributions:
        return ""
    parts = [
        f'Photo by <a href="{a["html_url"]}?{_UNSPLASH_UTM}">{a["name"]}</a>'
        for a in attributions
    ]
    joined = " · ".join(parts)
    unsplash_link = f'<a href="https://unsplash.com/?{_UNSPLASH_UTM}">Unsplash</a>'
    return f'\n    <div class="footer-attribution footer-attribution-unsplash">{joined} on {unsplash_link}.</div>'


# ============================================================================
# 5.5 SEO / GEO LAYER
# ----------------------------------------------------------------------------
# Per-page <meta description>, canonical URL, OG + Twitter Card meta tags,
# and a single `Electrician`-typed JSON-LD LocalBusiness block in <head>.
# Skips canonical/og:url/JSON-LD when --canonical-base is unset, so the
# engine still renders cleanly for prospects without a fixed prod URL.
# ============================================================================

# Per-page descriptor: which prose subhead drives the description, which
# captured site-photo overrides the default hero photo for og:image.
_SEO_PAGE_DESCRIPTORS = {
    "homepage":     {"desc_path": ("homepage", "subhead", "text")},
    "about":        {"desc_path": ("about", "subhead")},
    "services":     {"desc_path": ("services", "subhead")},
    "testimonials": {"desc_path": ("testimonials", "subhead")},
    "contact":      {"desc_path": ("contact", "subhead")},
}

_PAGE_PATHS = {
    "homepage":     "/",
    "about":        "/about.html",
    "services":     "/services.html",
    "testimonials": "/testimonials.html",
    "contact":      "/contact.html",
}


# P16 (Session 4 v1.1, 2026-04-29) — render-path output sanitization gate.
# Hard-fails the build when emitted HTML carries raw Python primitive
# syntax or unprocessed {em}/{/em} shorthand placeholders. Symptoms
# surfaced during Phase 0.5 cold-walk:
#   - {'text': 'How to reach us.', 'em_phrase': 'reach'}  (P16, contact info_heading)
#   - {em}soft-wash and pressure-cleaning{/em}            (S3-1, homepage subhead → meta)
# Pattern (1) generalizes via \w+ so any future dict-shape leak (any field
# name) fails the gate without per-field updates. (2) and (3) catch
# em-substitution-helper-not-invoked regressions on visual surfaces.
_P16_GATE_PATTERNS = [
    (re.compile(r"\{'\w+':"),  "Python dict repr — prose dict-slot emitted to HTML without unpack"),
    (re.compile(r"\{em\}"),    "Unprocessed {em} shorthand — em-substitution helper not invoked"),
    (re.compile(r"\{/em\}"),   "Unprocessed {/em} shorthand — em-substitution helper not invoked"),
]


def _verify_no_python_repr_in_html(html: str, page_key: str) -> None:
    """P16 grep gate — raises ValueError on first leak found.

    Runs at the end of render_page() against the composed HTML string
    before it returns. Identifies the pattern + surrounding context so
    the developer can locate the offending prose slot or render path.
    """
    for pattern, label in _P16_GATE_PATTERNS:
        m = pattern.search(html)
        if m:
            start = max(0, m.start() - 40)
            end = min(len(html), m.end() + 40)
            context = html[start:end].replace("\n", " ")
            raise ValueError(
                f"P16 gate failed on page '{page_key}' — {label}.\n"
                f"  matched: {m.group()!r}\n"
                f"  context: ...{context}..."
            )


def _strip_html_for_meta(text: str, max_len: int = 160) -> str:
    """Strip tags + decode common HTML entities for use in meta-attribute
    text. Truncates to max_len with an ellipsis.

    S3-1 (Session 4 v1.1, 2026-04-29) — meta-description sanitization. The
    §6.2 hero-subhead is the only voice-surface where em-dashes are allowed;
    meta inherits the global em-dash ban from anti-slop-rules.md, not the
    §6.2 exemption. Both `&mdash;` entity and the literal `—` character
    normalize to ", " here.

    Sibling to S3-1, same fix-surface — voice-of-engine subhead prose
    may carry `{em}...{/em}` shorthand placeholders consumed by the inline
    render path's em-substitution. Meta-emit reads prose upstream of that
    substitution and was shipping the placeholders verbatim. Strip the
    `{em}` / `{/em}` tokens before the HTML tag-strip; keep the wrapped
    content.
    """
    if not text:
        return ""
    # {em}...{/em} → ... (strip placeholder tokens, keep content)
    plain = text.replace("{em}", "").replace("{/em}", "")
    # Em/en-dash entity + literal char → ", " (S3-1). Regex pattern swallows
    # surrounding whitespace on every form so "Corners &mdash; every" and
    # "Corners — every" both collapse to "Corners, every" — no orphan
    # space-before-comma artifact from the entity-form (caught at local
    # pre-deploy meta check, S3-1 cycle).
    plain = re.sub(r"\s*&mdash;\s*", ", ", plain)
    plain = re.sub(r"\s*&ndash;\s*", ", ", plain)
    plain = re.sub(r"\s*—\s*", ", ", plain)
    plain = re.sub(r"\s*–\s*", ", ", plain)
    # Strip remaining HTML tags
    plain = re.sub(r"<[^>]+>", "", plain)
    # Decode remaining entities (em/en-dash already handled above)
    for ent, ch in [("&amp;", "&"), ("&nbsp;", " "), ("&quot;", '"'),
                    ("&apos;", "'"), ("&lt;", "<"), ("&gt;", ">"),
                    ("&#39;", "'")]:
        plain = plain.replace(ent, ch)
    plain = re.sub(r"\s+", " ", plain).strip()
    if len(plain) > max_len:
        plain = plain[: max_len - 1].rstrip() + "…"
    return plain


def _attr_escape(text: str) -> str:
    """HTML-attribute-safe escape: & < > "."""
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;"))


def _resolve_seo_description(prose: dict, page_key: str, ctx: dict | None = None) -> str:
    """Walk the per-page descriptor's prose path to pull the description.

    Falls back to profile-synth (siteDescription + ' | ' + page-frame) for
    inner pages when the prose path returns empty — Session 2 spec-defect F4
    fix. Pre-fix behavior emitted no meta description / og:description /
    twitter:description on inner pages when prose absent. Profile-synth
    pattern delivers SEO-complete inner pages on every fresh prospect with
    no per-prospect authoring burden; meta is an SEO surface (not a
    spectacle surface), so LABEL discipline doesn't bind here.
    """
    desc_path = _SEO_PAGE_DESCRIPTORS.get(page_key, {}).get("desc_path", ())
    cur: Any = prose
    for k in desc_path:
        if isinstance(cur, dict):
            cur = cur.get(k)
        else:
            cur = None
            break
    description = _strip_html_for_meta(cur or "")

    if not description and ctx and page_key != "homepage":
        profile = ctx.get("profile") or {}
        site_description = pick(profile, "identity", "siteDescription") or ""
        page_frames = {
            "about": "Our story",
            "services": "What we do",
            "testimonials": "Reviews",
            "contact": "Visit",
        }
        frame = page_frames.get(page_key, "")
        if site_description and frame:
            description = f"{site_description} | {frame}"
        elif site_description:
            description = site_description

    return description


def _resolve_og_image_path(ctx: dict, page_key: str, profile: dict,
                           photos_root: str | None, out_dir: Path) -> str:
    """Per-page og:image relative path, profile-data-driven so each page's
    social-share preview matches the page's content. v1.1 Session 1 rewrite
    2026-04-30 — replaces the static og_photo_key filename convention (which
    relied on Volthom-era site-04/site-09 numbering and fell through to the
    hero photo for every prospect that didn't follow that numbering).
    Resolution chain per page (always file-existence-checked, falls through
    to ctx.hero_photo_href on any miss — master invariant: never emit a URL
    pointing at a non-existent asset):

      homepage     → heroCandidatesTop5[0]  → heroCandidatesAll[0]  → hero
      about        → photoLibrary.teamIdentity → photoLibrary.ownerPortrait → hero
      services     → services.list[0].featuredImage → hero
      testimonials → heroCandidatesTop5[1]  → heroCandidatesAll[1]  → hero
      contact      → photoLibrary.ownerPortrait → photoLibrary.teamIdentity → hero
    """
    hero_fallback = ctx.get("hero_photo_href") or ""

    def _try(rel_path: str) -> str:
        if not rel_path or not photos_root:
            return ""
        if (Path(photos_root) / rel_path).exists():
            return _photo_href(rel_path, photos_root, out_dir)
        return ""

    candidates: list[str] = []
    if page_key == "homepage":
        # v1.1 Session 2 Patch 4: filter disqualifyFromHero before share-
        # image selection — a photo unfit for hero rotation is also unfit
        # for social-share representative image.
        top5 = _filter_hero_candidates(pick(profile, "photoLibrary", "heroCandidatesTop5") or [], profile)
        all_heroes = _filter_hero_candidates(pick(profile, "photoLibrary", "heroCandidatesAll") or [], profile)
        if top5:
            candidates.append(top5[0])
        if all_heroes:
            candidates.append(all_heroes[0])
    elif page_key == "about":
        team = pick(profile, "photoLibrary", "teamIdentity") or ""
        owner = pick(profile, "photoLibrary", "ownerPortrait") or ""
        # v1.1 Session 3 Patch 2: drop teamIdentity when category
        # disagrees — mirrors visible-band gate (Session 2 Patch 3).
        # Missing/legacy falls through to legacy emit; wrong-category
        # drops cleanly to the ownerPortrait fallback.
        if team and not _photo_category_matches(profile, team, "team"):
            team = ""
        candidates.extend([team, owner])
    elif page_key == "services":
        services = (profile.get("services") or {}).get("list") or []
        if services:
            candidates.append(services[0].get("featuredImage") or "")
    elif page_key == "testimonials":
        # Same Patch 4 filter as homepage.
        top5 = _filter_hero_candidates(pick(profile, "photoLibrary", "heroCandidatesTop5") or [], profile)
        all_heroes = _filter_hero_candidates(pick(profile, "photoLibrary", "heroCandidatesAll") or [], profile)
        # Reach for a different hero than homepage when ≥2 candidates exist;
        # share-image variation is the whole point of this resolver.
        if len(top5) >= 2:
            candidates.append(top5[1])
        if len(all_heroes) >= 2:
            candidates.append(all_heroes[1])
    elif page_key == "contact":
        owner = pick(profile, "photoLibrary", "ownerPortrait") or ""
        team = pick(profile, "photoLibrary", "teamIdentity") or ""
        # v1.1 Session 3 Patch 2: same gate as about-page — wrong-
        # category teamIdentity drops; missing falls through.
        if team and not _photo_category_matches(profile, team, "team"):
            team = ""
        candidates.extend([owner, team])

    for candidate in candidates:
        resolved = _try(candidate)
        if resolved:
            return resolved
    return hero_fallback


def _parse_hours_to_iso(hours_str: str) -> tuple[str, str] | None:
    """'7:00 AM – 5:00 PM' → ('07:00', '17:00'). Returns None on parse fail."""
    if not hours_str:
        return None
    normalized = hours_str.replace("–", "-").replace("—", "-")
    parts = [p.strip() for p in normalized.split("-")]
    if len(parts) != 2:
        return None

    def _to_iso(t: str) -> str | None:
        m = re.match(r"^(\d{1,2}):?(\d{2})?\s*(AM|PM|am|pm)?\s*$", t.strip())
        if not m:
            return None
        h = int(m.group(1))
        mn = int(m.group(2) or 0)
        ampm = (m.group(3) or "").upper()
        if ampm == "PM" and h < 12:
            h += 12
        if ampm == "AM" and h == 12:
            h = 0
        return f"{h:02d}:{mn:02d}"

    a = _to_iso(parts[0])
    b = _to_iso(parts[1])
    if a and b:
        return (a, b)
    return None


def _build_jsonld(ctx: dict, profile: dict, canonical_base: str, og_image_url: str = "") -> str:
    """Build a LocalBusiness/Electrician JSON-LD block from profile data.
    Returns an empty string when canonical_base is unset — schema.org
    aggregateRating + url require a stable absolute URL to register.

    og_image_url is the absolute, canonical-base-anchored URL for the
    representative image. Caller computes via the per-page og:image
    resolution chain (`_resolve_og_image_path`); if absent (no canonical
    base, no qualified photo) we omit the `image` field rather than emit
    a URL pointing at a non-existent asset."""
    if not canonical_base:
        return ""
    contact = profile.get("contact", {}) or {}
    creds = profile.get("credentials", {}) or {}
    gb = profile.get("googleBusiness", {}) or {}
    socials = profile.get("socialMedia", {}) or {}

    phone_digits = contact.get("phoneDigits", "")
    telephone = f"+1{phone_digits}" if phone_digits else (contact.get("phone") or "")

    addr_canonical = contact.get("addressCanonical", "") or ""
    addr_parts = [p.strip() for p in addr_canonical.split(",")]
    street = addr_parts[0] if len(addr_parts) >= 1 and addr_parts[0] else ""
    locality = addr_parts[1] if len(addr_parts) >= 2 else ""
    region_zip = addr_parts[2].split() if len(addr_parts) >= 3 else []
    region = region_zip[0] if region_zip else ""
    postal = region_zip[1] if len(region_zip) > 1 else ""

    hours = contact.get("hours", {}) or {}
    weekday_map = {
        "monday": "Monday", "tuesday": "Tuesday", "wednesday": "Wednesday",
        "thursday": "Thursday", "friday": "Friday",
        "saturday": "Saturday", "sunday": "Sunday",
    }
    opening_specs = []
    for d_lower, d_proper in weekday_map.items():
        v = hours.get(d_lower, "")
        if v and v.lower() != "closed":
            spec = _parse_hours_to_iso(v)
            if spec:
                opening_specs.append({
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": d_proper,
                    "opens": spec[0],
                    "closes": spec[1],
                })

    cities = contact.get("serviceAreaCities", []) or []
    counties = contact.get("serviceAreaCounties", []) or []
    area_served: list[dict] = []
    for c in cities:
        if c:
            area_served.append({"@type": "City", "name": c})
    for c in counties:
        if c:
            area_served.append({"@type": "AdministrativeArea", "name": f"{c} County"})

    same_as: list[str] = []
    for plat in ("facebook", "instagram", "google", "youtube", "linkedin", "twitter"):
        v = socials.get(plat)
        if isinstance(v, dict):
            url = v.get("url")
        elif isinstance(v, str):
            url = v
        else:
            url = None
        if url:
            same_as.append(url)

    # schema.org @type is per-prospect data, not engine-level. Read the
    # authored field and fall back to the controlled-vocabulary supertype
    # "LocalBusiness" — always-true, validators accept it, no false trade
    # claim for prospects whose businessType wasn't authored. The field
    # value is emitted as-is into "@type"; authors must write the literal
    # PascalCase schema.org type ("Electrician", "Plumber", "Store",
    # "LandscapeService", "RoofingContractor", "LocalBusiness", ...) drawn
    # from the schema.org controlled vocabulary at https://schema.org.
    business_type = pick(profile, "identity", "businessType") or "LocalBusiness"
    schema: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": business_type,
        "name": ctx.get("business_name") or (profile.get("businessName", {}) or {}).get("primary"),
        "url": canonical_base + "/",
        "telephone": telephone,
    }
    if og_image_url:
        schema["image"] = og_image_url
    if street:
        schema["address"] = {
            "@type": "PostalAddress",
            "streetAddress": street,
            "addressLocality": locality,
            "addressRegion": region,
            "postalCode": postal,
            "addressCountry": "US",
        }
    if opening_specs:
        schema["openingHoursSpecification"] = opening_specs
    if area_served:
        schema["areaServed"] = area_served
    if same_as:
        schema["sameAs"] = same_as

    rating = gb.get("rating")
    review_count = gb.get("reviewCount")
    if rating and review_count:
        schema["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": str(rating),
            "reviewCount": int(review_count),
        }

    license_no = creds.get("licenseNumber")
    if license_no:
        schema["identifier"] = license_no

    return json.dumps(schema, indent=2, ensure_ascii=False)


def _build_faqpage_jsonld(profile: dict, prose: dict) -> str:
    """Build FAQPage JSON-LD from resolved FAQ items. Returns JSON string or
    empty string when no FAQ data resolves. Sparse-drop class — no fabrication.
    Used on homepage and services-page where the FAQ section emits visibly."""
    faqs = resolve_faq(profile, prose)
    if not faqs:
        return ""
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item.get("question", ""),
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item.get("answer", ""),
                },
            }
            for item in faqs
            if item.get("question") and item.get("answer")
        ],
    }
    if not schema["mainEntity"]:
        return ""
    return json.dumps(schema, indent=2, ensure_ascii=False)


def _build_review_jsonld_blocks(profile: dict, business_name: str,
                                 canonical_base: str) -> list[str]:
    """Build per-review Review JSON-LD blocks from
    profile.testimonials.fromGoogleReviews[] + .fromSite[]. Returns a list of
    JSON strings, one per review. Each emits as its own <script> block per
    Google convention for individual rich-result eligibility. Sparse-drop class
    — no fabrication. Used on testimonials page only."""
    testimonials = profile.get("testimonials") or {}
    google_reviews = testimonials.get("fromGoogleReviews") or []
    site_reviews = testimonials.get("fromSite") or []
    all_reviews = list(google_reviews) + list(site_reviews)
    if not all_reviews or not business_name:
        return []

    item_reviewed = {"@type": "LocalBusiness", "name": business_name}
    if canonical_base:
        item_reviewed["url"] = canonical_base + "/"

    blocks: list[str] = []
    for r in all_reviews:
        author = r.get("name") or r.get("author") or ""
        rating = r.get("rating")
        body = r.get("quote") or r.get("text") or ""
        if not author or not body:
            continue
        block: dict = {
            "@context": "https://schema.org",
            "@type": "Review",
            "itemReviewed": item_reviewed,
            "author": {"@type": "Person", "name": author},
            "reviewBody": body,
        }
        if rating:
            block["reviewRating"] = {
                "@type": "Rating",
                "ratingValue": str(rating),
                "bestRating": "5",
            }
        blocks.append(json.dumps(block, indent=2, ensure_ascii=False))
    return blocks


def _build_service_jsonld_blocks(profile: dict, business_name: str,
                                  canonical_base: str) -> list[str]:
    """Build per-service Service JSON-LD blocks from profile.services.list[].
    Returns a list of JSON strings, one per service. Each emits as its own
    <script> block on the services page so each service has independent rich-
    result eligibility. Sparse-drop class: skip services missing name or
    description; return empty list when services.list is empty or business_name
    unset. Master invariant: never fabricate — serviceType derives from the
    authored service name, not from a synthesized controlled-vocabulary map.
    Engine extension v1.1 Session 1, 2026-04-30."""
    services = (profile.get("services") or {}).get("list") or []
    if not services or not business_name:
        return []

    provider = {"@type": "LocalBusiness", "name": business_name}
    if canonical_base:
        provider["url"] = canonical_base + "/"

    contact = profile.get("contact", {}) or {}
    cities = contact.get("serviceAreaCities", []) or []
    counties = contact.get("serviceAreaCounties", []) or []
    area_served: list[dict] = []
    for c in cities:
        if c:
            area_served.append({"@type": "City", "name": c})
    for c in counties:
        if c:
            area_served.append({"@type": "AdministrativeArea", "name": f"{c} County"})

    blocks: list[str] = []
    for svc in services:
        name = (svc.get("name") or "").strip()
        description = (svc.get("description") or "").strip()
        if not name or not description:
            continue
        block: dict = {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": name,
            "description": description,
            "serviceType": name,
            "provider": provider,
        }
        if area_served:
            block["areaServed"] = area_served
        blocks.append(json.dumps(block, indent=2, ensure_ascii=False))
    return blocks


def _seo_head_html(ctx: dict, profile: dict, prose: dict, page_key: str,
                   title: str, canonical_base: str, photos_root: str | None,
                   out_dir: Path) -> str:
    """Emit description + canonical + OG + Twitter Card + JSON-LD as the
    SEO/GEO meta block for <head>. Inserts between <title> and the font
    preconnect block in render_page."""
    description = _resolve_seo_description(prose, page_key, ctx)
    page_path = _PAGE_PATHS.get(page_key, "/")
    canonical_url = (canonical_base + page_path) if canonical_base else ""
    og_image_rel = _resolve_og_image_path(ctx, page_key, profile, photos_root, out_dir)
    og_image_url = ""
    if canonical_base and og_image_rel:
        # `_photo_href` returns a fixture-dir-relative path with `../`
        # segments routing back into the prospect's data dir. The deploy
        # pipeline rewrites `src=` and `background-image:url(` to deploy-root
        # paths, but the OG `content="..."` attribute isn't covered by that
        # sed pass. Normalize here: keep only the `/assets/...` tail so the
        # absolute URL resolves at the canonical base.
        m = re.search(r"(/assets/.+)$", og_image_rel)
        og_image_path = m.group(1) if m else "/" + og_image_rel.lstrip("./")
        og_image_url = canonical_base + og_image_path
    site_name = ctx.get("business_name", "")

    parts: list[str] = []
    if description:
        parts.append(f'<meta name="description" content="{_attr_escape(description)}">')
    if canonical_url:
        parts.append(f'<link rel="canonical" href="{canonical_url}">')

    parts.append('<meta property="og:type" content="website">')
    parts.append(f'<meta property="og:title" content="{_attr_escape(title)}">')
    if description:
        parts.append(f'<meta property="og:description" content="{_attr_escape(description)}">')
    if canonical_url:
        parts.append(f'<meta property="og:url" content="{canonical_url}">')
    if og_image_url:
        parts.append(f'<meta property="og:image" content="{og_image_url}">')
    if site_name:
        parts.append(f'<meta property="og:site_name" content="{_attr_escape(site_name)}">')

    parts.append('<meta name="twitter:card" content="summary_large_image">')
    parts.append(f'<meta name="twitter:title" content="{_attr_escape(title)}">')
    if description:
        parts.append(f'<meta name="twitter:description" content="{_attr_escape(description)}">')
    if og_image_url:
        parts.append(f'<meta name="twitter:image" content="{og_image_url}">')

    jsonld = _build_jsonld(ctx, profile, canonical_base, og_image_url)
    if jsonld:
        parts.append(f'<script type="application/ld+json">\n{jsonld}\n</script>')

    # FAQPage schema fires only on pages where the FAQ section emits visibly.
    # Homepage emits the FAQ band (render_faq); services-page intentionally
    # drops both FAQ + contact bands (render_services_page L2731 comment).
    # Audit-driven correction 2026-04-29 — earlier wire-in incorrectly emitted
    # FAQPage on services-page where no visible FAQ band rendered, producing
    # a schema-content mismatch that Google flags as Hidden content. Sparse-
    # drop discipline: schema only fires when the visible content does.
    if page_key == "homepage":
        faq_jsonld = _build_faqpage_jsonld(profile, prose)
        if faq_jsonld:
            parts.append(f'<script type="application/ld+json">\n{faq_jsonld}\n</script>')

    # Review schema fires on testimonials page only — Google convention is
    # one canonical Review-block location per site. Sparse-drop when no
    # testimonials present. Phase 0.5 schema-completeness extension 2026-04-29.
    if page_key == "testimonials":
        business_name = ctx.get("business_name", "")
        review_blocks = _build_review_jsonld_blocks(profile, business_name, canonical_base)
        for block in review_blocks:
            parts.append(f'<script type="application/ld+json">\n{block}\n</script>')

    # Service schema fires on services page only — the services page bundles
    # the bento overview + per-service detail blocks under one URL, so this is
    # where per-service rich-result eligibility belongs. Sparse-drop when no
    # services authored. v1.1 Session 1 schema-breadth extension 2026-04-30.
    if page_key == "services":
        business_name = ctx.get("business_name", "")
        service_blocks = _build_service_jsonld_blocks(profile, business_name, canonical_base)
        for block in service_blocks:
            parts.append(f'<script type="application/ld+json">\n{block}\n</script>')

    return "\n".join(parts)


def build_sitemap_xml(canonical_base: str, page_keys: list[str]) -> str:
    """Build a sitemap.xml from a list of page keys ordered by priority.
    Homepage gets priority 1.0; contact 0.9; about/services 0.8; testimonials 0.7."""
    priority_map = {
        "homepage": "1.0",
        "contact": "0.9",
        "about": "0.8",
        "services": "0.8",
        "testimonials": "0.7",
    }
    base = canonical_base.rstrip("/")
    today = datetime.date.today().isoformat()
    urls = []
    for k in page_keys:
        path = _PAGE_PATHS.get(k, "/")
        loc = f"{base}{path}"
        prio = priority_map.get(k, "0.5")
        urls.append(
            f"  <url>\n"
            f"    <loc>{loc}</loc>\n"
            f"    <lastmod>{today}</lastmod>\n"
            f"    <priority>{prio}</priority>\n"
            f"  </url>"
        )
    body = "\n".join(urls)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n"
        '</urlset>\n'
    )


def build_robots_txt(canonical_base: str) -> str:
    """User-agent allow-all + sitemap pointer."""
    base = canonical_base.rstrip("/")
    return (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        f"Sitemap: {base}/sitemap.xml\n"
    )


# ============================================================================
# 6. ASSEMBLY
# ============================================================================

def render_page(profile: dict, prose: dict, out_path: Path, photos_root: str | None, css_href: str, page_key: str = "homepage", access_key: str = "REPLACE_WITH_STATICFORMS_KEY", canonical_base: str = "") -> tuple[str, list[str]]:
    """page_key dispatches to homepage (default) or
    one of the four inner pages. Inner pages emit <body class="is-inner">
    so the §12/§13 lift in composer-system.css fires; homepage <body> stays
    unscoped to preserve the existing fixed-overlay nav cascade.

    `access_key` plumbs through to `render_contact_page` via ctx.
    Default is the placeholder string `REPLACE_WITH_STATICFORMS_KEY`;
    the deploy pipeline substitutes the real key at the pre-Vercel boundary.
    The CLI `--access-key` flag overrides the default for one-off real-key
    renders (which must NOT be committed)."""
    out_dir = out_path.parent
    ctx = build_ctx(profile, prose, photos_root, out_dir, access_key=access_key)

    p = ctx["palette"]
    # title separator must be middle-dot for `<title>` consistency across pages.
    # Inner-page title segment reads from INNER_PAGE_TITLES (single source of
    # truth for canonical labels). Homepage is special-cased to a bare
    # business · city title with no leading segment.
    if page_key == "homepage":
        title = f'{ctx["business_name"]} · {ctx["city_state"]}'
    else:
        seg = INNER_PAGE_TITLES[page_key][0]
        title = f'{seg} · {ctx["business_name"]} · {ctx["city_state"]}'
    # Palette overrides go in an inline <style> after the external CSS link.
    palette_override = f""":root{{
  --color-primary:{p["primary"]};
  --color-primary-rgb:{_hex_to_rgb_tuple(p["primary"])};
  --color-primary-deep:{p["primary_deep"]};
  --color-dark-primary:{p["dark_primary"]};
  --color-accent:{p["accent"]};
  --color-accent-rgb:{_hex_to_rgb_tuple(p["accent"])};
  --color-accent-deep:{p["accent_deep"]};
  --color-background:{p["background"]};
  --color-paper-warm:{p["paper_warm"]};
  --color-cream:{p["cream"]};
  --manifesto-band-bg:{p["manifesto_band"]};
}}"""

    body_attr = ' class="is-inner"' if page_key != "homepage" else ""
    seo_meta = _seo_head_html(ctx, profile, prose, page_key, title,
                              canonical_base, photos_root, out_dir)
    head = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
{seo_meta}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Figtree:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css_href}">
<style>{palette_override}</style>
</head>
<body{body_attr}>
'''

    if page_key == "homepage":
        # Two-pass render: render every non-footer band first, scan the
        # rendered HTML for assets/photos/google/* references, look up
        # contributors via _attributions.json, then render the footer with
        # that list (so the footer can carry Google photo attribution).
        # Editorial bands self-gate on prose presence — empty
        # pullquote/manifesto/story drops the band.
        trust_band = render_trust_marquee(ctx) or render_anchor_strip(ctx)
        # Homepage CTA band replaces an embedded contact form per Design audit.
        # The form lives on /contact only; the homepage gets a CTA-only
        # conversion-ladder rung. See _homepage_cta_band_html.
        homepage_contact = _homepage_cta_band_html(ctx)
        pre_footer_parts = [
            render_nav(ctx),
            render_hero(ctx),
            trust_band,
            render_services(ctx),
            render_stats_band(ctx),
            render_testimonials(ctx),
            render_promo_callout(ctx),
            render_before_after(ctx),
            render_faq(ctx, page="homepage"),
            homepage_contact,
            render_pullquote(ctx),
            # render_manifesto removed at Session 3 close (2026-04-29) per
            # Round-2 diagnostic: the manifesto band was a Volthom-arc Phase
            # 5.0c addition that competed with cta_band for the same warmth-
            # surface attention budget. Engine principle: the homepage ships
            # ONE warmth surface, and that surface IS the conversion-ladder
            # cta_band. Decorative warmth bands degrade conversion.
            # render_manifesto(ctx),
            render_story(ctx),
        ]
        pre_footer_parts = [b for b in pre_footer_parts if b]
        attribution_map = _load_google_attribution_map(photos_root)
        ctx["google_contributors"] = _collect_google_contributors(
            "\n\n".join(pre_footer_parts), attribution_map
        )
        # collect Unsplash photographer attributions
        # for footer display. Same scan-then-render pattern as Google.
        unsplash_cache = _load_unsplash_cache(photos_root)
        ctx["unsplash_attributions"] = _collect_unsplash_attributions(
            "\n\n".join(pre_footer_parts), unsplash_cache
        )
        # mobile CTA bar ships universally on every page (hidden
        # on desktop via composer-system.css §14). Lives after the footer so
        # it sits above everything else when fixed-positioned.
        body_parts = pre_footer_parts + [render_footer(ctx), render_mobile_cta_bar(ctx)]
        script = '''
<script>
  // Sitenav scroll state
  const nav = document.getElementById('sitenav');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 80) nav.classList.add('scrolled');
    else nav.classList.remove('scrolled');
  }, { passive: true });

  // Hero parallax (single-photo only; slideshow has its own crossfade)
  const heroBg = document.getElementById('heroBg');
  let ticking = false;
  if (heroBg && window.matchMedia('(min-width: 900px)').matches) {
    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          const y = window.scrollY;
          heroBg.style.transform = `scale(1.04) translateY(${y * 0.25}px)`;
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
  }

  // F2 count-up animation port from T&F flagship (Round-3 Session 3 close,
  // 2026-04-29). Reads [data-target] elements, animates 0 → target over 2s
  // with cubic ease-out on IntersectionObserver fire. One-shot. Respects
  // prefers-reduced-motion (instant set, no animation). LEAD stat only;
  // see render_stats_band for which tile gets [data-target].
  (function numberTicker(){
    const targets = document.querySelectorAll('[data-target]');
    if (!targets.length) return;
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const obs = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        const finalValue = parseInt(el.dataset.target, 10);
        if (isNaN(finalValue)) return;
        if (reduced) {
          el.textContent = finalValue.toLocaleString();
          obs.unobserve(el);
          return;
        }
        const duration = 2000;
        const startTime = performance.now();
        function tick(now) {
          const elapsed = now - startTime;
          const progress = Math.min(elapsed / duration, 1);
          const eased = 1 - Math.pow(1 - progress, 3);
          const current = Math.floor(finalValue * eased);
          el.textContent = current.toLocaleString();
          if (progress < 1) requestAnimationFrame(tick);
          else el.textContent = finalValue.toLocaleString();
        }
        requestAnimationFrame(tick);
        obs.unobserve(el);
      });
    }, { threshold: 0.3, rootMargin: '0px 0px -50px 0px' });
    targets.forEach((el) => obs.observe(el));
  })();

  // F6 hero crossfade slideshow port from T&F flagship (Round-3 Session 3
  // close, 2026-04-29). Activates on .hero-crossfade-slideshow with ≥2
  // .hero-crossfade-slide children. 6s/slide default. Respects
  // prefers-reduced-motion (no rotation). First slide carries .active
  // in the markup so the SSR'd page reads correctly with JS off.
  (function heroCrossfade(){
    const container = document.querySelector('.hero-crossfade-slideshow');
    if (!container) return;
    const slides = container.querySelectorAll('.hero-crossfade-slide');
    if (slides.length < 2) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    let i = 0;
    setInterval(() => {
      slides[i].classList.remove('active');
      i = (i + 1) % slides.length;
      slides[i].classList.add('active');
    }, 6000);
  })();
</script>
</body>
</html>
'''
        html = head + "\n\n".join(body_parts) + script
        return html, ctx["warnings"]

    # Inner-page paths. Inner pages get the same Google attribution treatment
    # — render the body, scan it for google photo refs, then re-render the
    # footer with the contributor list. Volthom's about/services/testimonials
    # bundle exemplars text-only, but the chassis stays general.
    inner_renderers = {
        "about":        render_about_page,
        "services":     render_services_page,
        "testimonials": render_testimonials_page,
        "contact":      render_contact_page,
    }
    if page_key not in inner_renderers:
        raise ValueError(f"Unknown page_key: {page_key!r}; expected one of homepage, {', '.join(INNER_PAGE_KEYS)}")
    # First pass: build the body without contributor attribution.
    ctx["google_contributors"] = []
    ctx["unsplash_attributions"] = []
    first_pass = inner_renderers[page_key](ctx)
    attribution_map = _load_google_attribution_map(photos_root)
    contributors = _collect_google_contributors(first_pass, attribution_map)
    # collect Unsplash attributions on inner pages too
    # (services.html ships service-detail blocks with Unsplash photos).
    unsplash_cache = _load_unsplash_cache(photos_root)
    unsplash_attrs = _collect_unsplash_attributions(first_pass, unsplash_cache)
    if contributors or unsplash_attrs:
        ctx["google_contributors"] = contributors
        ctx["unsplash_attributions"] = unsplash_attrs
        body_html = inner_renderers[page_key](ctx)
    else:
        body_html = first_pass
    # mobile CTA bar ships on every page (homepage already wired
    # via body_parts above). Inner-page output appends it after the inner-page
    # body and before the closing </body>.
    mobile_cta = render_mobile_cta_bar(ctx)
    if mobile_cta:
        body_html = body_html + "\n\n" + mobile_cta
    closing = "\n</body>\n</html>\n"
    full_html = head + body_html + closing
    # P16 grep gate — hard-fail on Python repr / unprocessed em-shorthand leak
    _verify_no_python_repr_in_html(full_html, page_key)
    return full_html, ctx["warnings"]


# ============================================================================
# 7. CLI
# ============================================================================

def main() -> int:
    ap = argparse.ArgumentParser(description="prospect-site-v2 template engine")
    ap.add_argument("--profile", required=True, help="Path to profile.json or profile-draft.json")
    ap.add_argument("--prose",   required=True, help="Path to prose.json (executor-authored)")
    ap.add_argument("--out",     required=True, help="Output path for Homepage.html")
    ap.add_argument("--photos-root", default=None,
                    help="Root directory to resolve relative photo paths against. Defaults to the profile's parent dir.")
    ap.add_argument("--css-href", default="../../css/composer-system.css",
                    help="<link rel=stylesheet href=X> — relative from the output file.")
    ap.add_argument("--page", default="homepage",
                    choices=("homepage",) + INNER_PAGE_KEYS,
                    help="Which page to emit. Default: homepage. Inner pages "
                    "render with <body class=\"is-inner\"> against the lifted "
                    "§1–§13 vocabulary in composer-system.css.")
    ap.add_argument("--access-key", default="REPLACE_WITH_STATICFORMS_KEY",
                    help="StaticForms accessKey to embed in <input> hidden "
                    "field. Default is the placeholder; deploy pipeline "
                    "substitutes the real key via sed at the pre-Vercel "
                    "boundary. Real-key renders MUST NOT be committed.")
    ap.add_argument("--canonical-base", default="",
                    help="Absolute prod URL (no trailing slash) used as the "
                    "base for <link rel=canonical>, og:url, twitter URLs, "
                    "JSON-LD url + image, and sitemap.xml entries. "
                    "Empty disables canonical/OG-url/JSON-LD emission.")
    args = ap.parse_args()

    profile = load_json(args.profile)
    prose = load_json(args.prose)
    out_path = Path(args.out).expanduser()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    photos_root = args.photos_root or str(Path(args.profile).expanduser().parent)

    html, warnings = render_page(profile, prose, out_path, photos_root, args.css_href, page_key=args.page, access_key=args.access_key, canonical_base=args.canonical_base)
    out_path.write_text(html, encoding="utf-8")

    print(f"✓ Rendered {out_path} ({len(html):,} bytes)")

    # S3-4 (Session 4 v1.1, 2026-04-29): emit sitemap.xml + robots.txt
    # sidecars alongside the rendered HTML when this is the homepage render
    # and canonical-base is set. Sidecars are build-once artifacts (same
    # content for every page in the build); homepage is the canonical anchor
    # for the emit. Sparse-drops cleanly when canonical-base is empty —
    # matches the emit discipline of <link rel=canonical>, JSON-LD, og:url
    # at L4020-4024. Future v1.1 conditional pages (gallery / specials /
    # emergency per content-rules.md) extend the page_keys list.
    if args.page == "homepage" and args.canonical_base:
        sidecar_dir = out_path.parent
        page_keys = ["homepage", "about", "services", "testimonials", "contact"]
        sitemap_xml = build_sitemap_xml(args.canonical_base, page_keys)
        robots_txt = build_robots_txt(args.canonical_base)
        (sidecar_dir / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")
        (sidecar_dir / "robots.txt").write_text(robots_txt, encoding="utf-8")
        print(f"✓ Emitted sitemap.xml ({len(sitemap_xml):,} bytes)")
        print(f"✓ Emitted robots.txt ({len(robots_txt):,} bytes)")

    for w in warnings:
        print(f"  ⚠ {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

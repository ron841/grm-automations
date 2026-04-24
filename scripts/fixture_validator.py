#!/usr/bin/env python3
"""
Composer fixture validator — three-pass validator for Phase 4-new output.

Canonical references (authority map at
skills-experimental/prospect-site-composer/references/authority-map.md):
- Three-pass validator contract: composition-plan-schema.md §14 (Concept 30)
- Editorial/structural/intent-spec partition: §14 table (Concept 32)
- Rule 1-6 mechanics: Phase 4-new implementation prompt (Concept 31)
- Voice-zone two-level vocabulary + Rule 4 flatten: §7 (Concepts 12-14)
- Rule 3 persona durations: emotional-arc.md "Micro-interaction duration
  lock (persona-indexed)" (Concept 6)
- Italic word-class enum: emotional-arc.md "Italic word-class vocabulary
  (persona-indexed)" (Concept 16)
- Pullquote heuristic (8-20 words): typography.md §13 (Concept 19)
- ScaleContrast thresholds: typography.md §2 per persona (Concept 27)

Self-check mode (side_channel=None): verifies fixture internal consistency.
Editorial-adherence pass is SKIPPED in self-check per Design Session 3 Q2
close — fixtures are authored intent, adherence is checked against
LLM-produced emission at Gate E.

The lookup tables below are hard-coded from the canonical reference
files as of authority-map.md commit 9ebeced. Drift risk: if any
canonical file (voiceMap.md, emotional-arc.md, composition-plan-schema.md)
changes the values these tables encode, this validator needs manual
update. The authority map's maintenance contract covers the
cross-concept reshape case; single-file edits of canonical enums
require this validator to sync.
"""

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


# --- Data classes -------------------------------------------------------------

@dataclass
class StructMismatch:
    field_path: str
    fixture_value: Any
    emitted_value: Any


@dataclass
class DerivMismatch:
    field_path: str
    rule: str  # pathConvention | tier | microInteractionDurations |
               # voiceZones | scaleContrast | layoutSequence
    fixture_value: Any
    derived_value: Any
    emitted_value: Any


@dataclass
class AdherenceMismatch:
    field_path: str
    persona_rule: str
    emitted_value: Any
    violation: str


@dataclass
class ValidationResult:
    passed: bool
    structural_mismatches: list = field(default_factory=list)
    derivation_mismatches: list = field(default_factory=list)
    adherence_mismatches: list = field(default_factory=list)


# --- Canonical lookup tables --------------------------------------------------

# Rule 3 canonical two-row lock per emotional-arc.md
# "Micro-interaction duration lock (persona-indexed)" (authority map
# Concept 6). Source commit: 35343c7.
PERSONA_DURATIONS = {
    "quiet-confidence":    {"entry": 400, "hover": 180},
    "earned-pride":        {"entry": 400, "hover": 180},
    "neighborhood-steady": {"entry": 400, "hover": 180},
    "modern-specialist":   {"entry": 400, "hover": 180},
    "urgent-service":      {"entry": 250, "hover": 150},
}

# Rule 1 derivation: kebab-case string → full pathConvention object per §2.2.
PATH_CONVENTION_DERIVATIONS = {
    "kebab-case": {
        "homePath": "/",
        "aboutPath": "/about",
        "servicePathPattern": "/services/{slug}",
        "contactPath": "/contact",
        "trailingSlash": False,
    },
}

# Rule 5 scaleContrast threshold map (high/medium/low → min WCAG ratio).
SCALE_CONTRAST_THRESHOLDS = {
    "high":   7.0,
    "medium": 4.5,
    "low":    3.0,
}

# §7 subpart → section flatten mapping (post-Session-4 commit 1c5379b).
SUBPART_TO_SECTION_ZONE = {
    "hero-eyebrow":            "hero-headline",
    "hero-headline-slot":      "hero-headline",
    "hero-subheadline-slot":   "hero-subheadline",
    "hero-primary-cta":        "hero-headline",
    "services-grid-heading":   "services-grid-header",
    "services-card-headline":  "service-card-description",
    "services-card-body":      "service-card-description",
    "testimonials-heading":    "testimonials-header",
    "testimonial-body":        "testimonials-header",
    "testimonial-attribution": "testimonials-header",
    "about-page-heading":      "about-page-body",
    "about-page-body-slot":    "about-page-body",
    "about-page-attribution":  "about-page-body",
}

# §7 closed enums.
SUBPART_ZONES_13 = set(SUBPART_TO_SECTION_ZONE.keys())
SECTION_ZONES_15 = {
    "hero-headline", "hero-subheadline", "promo-bar", "trust-marquee",
    "services-grid-header", "service-card-description", "stats-section",
    "before-after-header", "testimonials-header", "featured-promotion",
    "faq-question", "faq-answer", "contact-form-header", "footer-tagline",
    "about-page-body",
}

# Voice enum — 3 values per composition-plan-schema.md §4.2:179,181.
VOICE_ENUM_3 = {"closing-table", "saturday-morning", "front-porch"}

# Italic word-class enum per emotional-arc.md "Italic word-class
# vocabulary (persona-indexed)" (authority map Concept 16). Source
# commit: 03ca705.
ITALIC_WORD_CLASSES = {"place", "name", "tenure", "trade-term"}

# Per-persona favored-class map. urgent-service has empty set —
# italic-color-shift is not Tier 1 for this persona.
ITALIC_PERSONA_FAVORED = {
    "neighborhood-steady": {"place", "tenure"},
    "earned-pride":        {"name", "trade-term"},
    "quiet-confidence":    {"tenure", "trade-term"},
    "modern-specialist":   {"trade-term"},
    "urgent-service":      set(),
}

# Pullquote heuristic per typography.md §13 (authority map Concept 19).
PULLQUOTE_WORD_MIN = 8
PULLQUOTE_WORD_MAX = 20


# --- Editorial field path patterns --------------------------------------------

# §14 editorial partition (authority map Concept 32). Paths use
# JSONPath-like syntax with [] for array indices; _normalize_path
# converts concrete [N] to [] before matching.
EDITORIAL_FIELD_PATTERNS = [
    r"\.[a-z]\w*Copy$",                         # *Copy fields
    r"\.headingHierarchy\.h1$",
    r"\.h2Sequence\[\]\.text$",
    r"\.h2Sequence\[\]\.copy$",
    r"\.italicSelections\[\]\.italicWord$",
    r"\.italicSelections\[\]\.alternativeWord$",
    r"\.pullQuotes\[\]\.extractedText$",
    r"\.pullQuotes\[\]\.rhetoricalSlot$",
    r"\.eyebrowDeployments\[\]\.text$",
    r"\.italicPlacements\[\]\.phrase$",
    r"\.personaReason$",
    r"\.signatureMicroInteractionReason$",
    r"\.microInteractionsReason$",
    r"\.serviceDescriptions\[\]\.description$",
    r"\.serviceDescriptions\[\]\.text$",
    r"\.constraintRelaxations\[\]\.detail$",
]


def _normalize_path(path: str) -> str:
    return re.sub(r"\[\d+\]", "[]", path)


def _is_editorial_path(path: str) -> bool:
    normalized = _normalize_path(path)
    return any(re.search(pat, normalized) for pat in EDITORIAL_FIELD_PATTERNS)


# --- Structural pass ----------------------------------------------------------

def _structural_pass_skip_set(fixture_plan: dict) -> set:
    """Paths to skip in structural walk — the six §14 intent-spec fields,
    plus inline voiceZoneAssignments (Rule 4 governs)."""
    skips = {
        "$.site.pathConvention",
        "$.site.tier",
        "$.site.microInteractionDurations",
    }
    for i, page in enumerate(fixture_plan.get("pages") or []):
        skips.add(f"$.pages[{i}].scaleContrast")
        skips.add(f"$.pages[{i}].layoutSequence")
        for j in range(len(page.get("sections") or [])):
            skips.add(
                f"$.pages[{i}].sections[{j}].voiceZoneAssignments"
            )
    return skips


def _walk(fixture, emitted, path, mismatches, skip_paths):
    if path in skip_paths:
        return
    if _is_editorial_path(path):
        return
    if isinstance(fixture, dict) and isinstance(emitted, dict):
        fk = set(fixture.keys())
        ek = set(emitted.keys())
        for k in fk - ek:
            mismatches.append(StructMismatch(
                f"{path}.{k}", fixture[k], None))
        for k in ek - fk:
            mismatches.append(StructMismatch(
                f"{path}.{k}", None, emitted[k]))
        for k in fk & ek:
            _walk(fixture[k], emitted[k], f"{path}.{k}",
                  mismatches, skip_paths)
    elif isinstance(fixture, list) and isinstance(emitted, list):
        if len(fixture) != len(emitted):
            mismatches.append(StructMismatch(
                f"{path}[len]", len(fixture), len(emitted)))
            return
        for i, (fv, ev) in enumerate(zip(fixture, emitted)):
            _walk(fv, ev, f"{path}[{i}]", mismatches, skip_paths)
    else:
        if fixture != emitted:
            mismatches.append(StructMismatch(
                path, fixture, emitted))


# --- Semantic-derivation pass (Pass 2) ---------------------------------------

def _rule_1_path_convention(fixture_plan, emitted_plan, self_check, derivs):
    fixture_val = fixture_plan.get("site", {}).get("pathConvention")
    if self_check:
        # No emission shape to compare against; verify string is in enum.
        if fixture_val not in PATH_CONVENTION_DERIVATIONS:
            derivs.append(DerivMismatch(
                "$.site.pathConvention", "pathConvention",
                fixture_val, None, fixture_val,
            ))
        return
    emitted_val = emitted_plan.get("site", {}).get("pathConvention")
    derived = PATH_CONVENTION_DERIVATIONS.get(fixture_val)
    if derived is None:
        derivs.append(DerivMismatch(
            "$.site.pathConvention", "pathConvention",
            fixture_val, None, emitted_val,
        ))
    elif derived != emitted_val:
        derivs.append(DerivMismatch(
            "$.site.pathConvention", "pathConvention",
            fixture_val, derived, emitted_val,
        ))


def _rule_2_tier(fixture_plan, emitted_plan, side_channel, derivs):
    fixture_tier = fixture_plan.get("site", {}).get("tier")
    if side_channel is None:
        return  # self-check — trivial pass
    sc_tier = side_channel.get("tier")
    if fixture_tier != sc_tier:
        derivs.append(DerivMismatch(
            "$.site.tier", "tier",
            fixture_tier, sc_tier,
            emitted_plan.get("site", {}).get("tier"),
        ))


def _rule_3_durations(fixture_plan, emitted_plan, self_check, derivs):
    persona = fixture_plan.get("site", {}).get("persona")
    expected = PERSONA_DURATIONS.get(persona)
    if expected is None:
        derivs.append(DerivMismatch(
            "$.site.microInteractionDurations",
            "microInteractionDurations",
            persona, None, None,
        ))
        return
    if self_check:
        declared = fixture_plan.get("site", {}).get(
            "microInteractionDurations")
    else:
        declared = emitted_plan.get("site", {}).get(
            "microInteractionDurations")
    if declared != expected:
        derivs.append(DerivMismatch(
            "$.site.microInteractionDurations",
            "microInteractionDurations",
            fixture_plan.get("site", {}).get(
                "microInteractionDurations"),
            expected,
            declared,
        ))


def _rule_4_voice_zones(fixture_plan, emitted_plan, self_check, derivs):
    """Rule 4 per Session 4 Concern 4 reshape: subpart-grain inline equality
    + section-level flatten for page-level voiceZones[]. Self-check verifies
    inline keys in §7 13-key enum and voices in 3-value enum."""
    for pi, pg in enumerate(fixture_plan.get("pages") or []):
        # Walk inline voiceZoneAssignments per section.
        for si, sec in enumerate(pg.get("sections") or []):
            vza = sec.get("voiceZoneAssignments") or {}
            for key, voice in vza.items():
                path = (f"$.pages[{pi}].sections[{si}]."
                        f"voiceZoneAssignments.{key}")
                if key not in SUBPART_ZONES_13:
                    derivs.append(DerivMismatch(
                        path, "voiceZones",
                        key, None, key,
                    ))
                if voice not in VOICE_ENUM_3:
                    derivs.append(DerivMismatch(
                        f"{path}:voice", "voiceZones",
                        voice, None, voice,
                    ))
        if self_check:
            continue
        # Non-self-check: flatten fixture subpart keys to section-level set,
        # compare against emitted page-level voiceZones[].
        derived_section_set = set()
        for sec in (pg.get("sections") or []):
            vza = sec.get("voiceZoneAssignments") or {}
            for k in vza:
                if k in SUBPART_TO_SECTION_ZONE:
                    derived_section_set.add(SUBPART_TO_SECTION_ZONE[k])
        emitted_pages = emitted_plan.get("pages") or []
        emitted_pg = emitted_pages[pi] if pi < len(emitted_pages) else {}
        emitted_vz = emitted_pg.get("voiceZones") or []
        emitted_section_set = {
            e.get("zone") for e in emitted_vz
            if isinstance(e, dict)
        }
        if derived_section_set != emitted_section_set:
            derivs.append(DerivMismatch(
                f"$.pages[{pi}].voiceZones", "voiceZones",
                sorted(derived_section_set),
                sorted(derived_section_set),
                sorted(emitted_section_set),
            ))


def _rule_5_scale_contrast(fixture_plan, emitted_plan, self_check, derivs):
    if self_check:
        return  # no emitted achievedRatio in self-check mode
    for pi, pg in enumerate(fixture_plan.get("pages") or []):
        intent = pg.get("scaleContrast")
        threshold = SCALE_CONTRAST_THRESHOLDS.get(intent)
        if threshold is None:
            derivs.append(DerivMismatch(
                f"$.pages[{pi}].scaleContrast", "scaleContrast",
                intent, None, None,
            ))
            continue
        emitted_pg = (emitted_plan.get("pages") or [])[pi]
        emitted_sc = emitted_pg.get("scaleContrast") or {}
        achieved = emitted_sc.get("achievedRatio")
        if achieved is None or achieved < threshold:
            derivs.append(DerivMismatch(
                f"$.pages[{pi}].scaleContrast.achievedRatio",
                "scaleContrast",
                intent, threshold, achieved,
            ))


def _rule_6_layout_sequence(fixture_plan, emitted_plan, self_check, derivs):
    for pi, pg in enumerate(fixture_plan.get("pages") or []):
        fixture_seq = pg.get("layoutSequence")
        fixture_types = [
            s.get("type") for s in (pg.get("sections") or [])
        ]
        if self_check:
            if fixture_seq != fixture_types:
                derivs.append(DerivMismatch(
                    f"$.pages[{pi}].layoutSequence", "layoutSequence",
                    fixture_seq, fixture_types, fixture_seq,
                ))
            continue
        emitted_pg = (emitted_plan.get("pages") or [])[pi]
        emitted_types = [
            s.get("type") for s in (emitted_pg.get("sections") or [])
        ]
        if fixture_seq != emitted_types:
            derivs.append(DerivMismatch(
                f"$.pages[{pi}].layoutSequence", "layoutSequence",
                fixture_seq, emitted_types, emitted_types,
            ))


# --- Editorial-adherence pass (Pass 3) ---------------------------------------

def _adherence_pass(fixture_plan, emitted_plan, persona, adherences):
    """Check editorial fields on emitted_plan. SKIPPED in self-check."""
    for pi, pg in enumerate(emitted_plan.get("pages") or []):
        for ii, it in enumerate(pg.get("italicSelections") or []):
            path = f"$.pages[{pi}].italicSelections[{ii}]"
            word = it.get("italicWord")
            word_class = it.get("personaWordClassAnnotation")
            if word_class is not None and word_class not in ITALIC_WORD_CLASSES:
                adherences.append(AdherenceMismatch(
                    f"{path}.personaWordClassAnnotation",
                    "italic-word-class-enum",
                    word_class,
                    f"class {word_class!r} not in 4-value enum",
                ))
            favored = ITALIC_PERSONA_FAVORED.get(persona, set())
            if favored and word_class and word_class not in favored:
                adherences.append(AdherenceMismatch(
                    f"{path}.italicWord",
                    "persona-favored-word-class",
                    word,
                    f"persona {persona} favors {sorted(favored)}; "
                    f"got class {word_class!r}",
                ))
        for qi, pq in enumerate(pg.get("pullQuotes") or []):
            path = f"$.pages[{pi}].pullQuotes[{qi}].extractedText"
            text = pq.get("extractedText") or ""
            wc = len(text.split())
            if not (PULLQUOTE_WORD_MIN <= wc <= PULLQUOTE_WORD_MAX):
                adherences.append(AdherenceMismatch(
                    path, "pullquote-word-count",
                    wc,
                    f"word count {wc} outside bound "
                    f"{PULLQUOTE_WORD_MIN}-{PULLQUOTE_WORD_MAX}",
                ))
    site = emitted_plan.get("site", {})
    for fld in ("personaReason", "signatureMicroInteractionReason",
                "microInteractionsReason"):
        val = site.get(fld)
        if not val:
            adherences.append(AdherenceMismatch(
                f"$.site.{fld}", "non-empty-rationale",
                val, "empty rationale prose",
            ))
            continue
        if persona and persona not in val:
            # urgent-service often referred to as "rescue-ready" in prose
            if persona == "urgent-service" and "rescue-ready" in val.lower():
                continue
            adherences.append(AdherenceMismatch(
                f"$.site.{fld}", "rationale-persona-mention",
                val, f"rationale does not mention persona {persona!r}",
            ))


# --- Top-level entry point ----------------------------------------------------

def validate_fixture(
    emitted_plan: dict,
    fixture_plan: dict,
    profile: dict,
    side_channel: Optional[dict] = None,
) -> ValidationResult:
    self_check = side_channel is None

    struct = []
    derivs = []
    adherences = []

    skip_set = _structural_pass_skip_set(fixture_plan)
    _walk(fixture_plan, emitted_plan, "$", struct, skip_set)

    _rule_1_path_convention(fixture_plan, emitted_plan, self_check, derivs)
    _rule_2_tier(fixture_plan, emitted_plan, side_channel, derivs)
    _rule_3_durations(fixture_plan, emitted_plan, self_check, derivs)
    _rule_4_voice_zones(fixture_plan, emitted_plan, self_check, derivs)
    _rule_5_scale_contrast(fixture_plan, emitted_plan, self_check, derivs)
    _rule_6_layout_sequence(fixture_plan, emitted_plan, self_check, derivs)

    if not self_check:
        persona = fixture_plan.get("site", {}).get("persona")
        _adherence_pass(fixture_plan, emitted_plan, persona, adherences)

    passed = not (struct or derivs or adherences)
    return ValidationResult(
        passed=passed,
        structural_mismatches=struct,
        derivation_mismatches=derivs,
        adherence_mismatches=adherences,
    )


# --- Self-check runner --------------------------------------------------------

def _run_self_check(fixtures_root: Path) -> int:
    profile_dir = fixtures_root / "profile"
    plan_dir = fixtures_root / "composition-plan"

    pairs = []
    for plan_path in sorted(plan_dir.glob("fixture-*.composition-plan.json")):
        # fixture-N.slug.composition-plan.json → slug.profile.json
        parts = plan_path.name.split(".")
        slug = parts[1]
        profile_path = profile_dir / f"{slug}.profile.json"
        pairs.append((plan_path, profile_path, slug))

    failures = 0
    for plan_path, profile_path, slug in pairs:
        with open(plan_path) as f:
            plan = json.load(f)
        with open(profile_path) as f:
            profile = json.load(f)
        result = validate_fixture(plan, plan, profile, side_channel=None)
        status = "CLEAN" if result.passed else "FAIL"
        print(f"[{status}] {slug}")
        if not result.passed:
            failures += 1
            for m in result.structural_mismatches[:10]:
                print(f"  struct:     {m.field_path}")
                print(f"              fixture={m.fixture_value!r}")
                print(f"              emitted={m.emitted_value!r}")
            for m in result.derivation_mismatches[:10]:
                print(f"  deriv({m.rule}): {m.field_path}")
                print(f"              fixture={m.fixture_value!r}")
                print(f"              derived={m.derived_value!r}")
                print(f"              emitted={m.emitted_value!r}")
            for m in result.adherence_mismatches[:10]:
                print(f"  adhere:     {m.field_path}  {m.persona_rule}")
                print(f"              {m.violation}")
            extra = (
                max(0, len(result.structural_mismatches) - 10)
                + max(0, len(result.derivation_mismatches) - 10)
                + max(0, len(result.adherence_mismatches) - 10)
            )
            if extra:
                print(f"  ... and {extra} more mismatches")
    print()
    print(f"SELF-CHECK: {len(pairs) - failures}/{len(pairs)} fixtures clean")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    default_fixtures = (
        Path(__file__).resolve().parent.parent
        / "docs" / "composer" / "fixtures"
    )
    if not default_fixtures.exists():
        default_fixtures = (
            Path.home() / "grm-automations"
            / "docs" / "composer" / "fixtures"
        )
    sys.exit(_run_self_check(default_fixtures))

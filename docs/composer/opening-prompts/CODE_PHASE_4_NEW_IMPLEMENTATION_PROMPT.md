# Code — Phase 4-new Six-Gate Implementation Prompt

Paste this to a fresh Claude Code terminal window in Session 4, after Chat-Claude is oriented and Ron gives the go.

---

```
Phase 4-new implementation — six gates in sequence, against
Session 3's resolved architecture.

Architecture resolutions from Session 3 close (Design-signed-off):

- Rule 3 microInteractionDurations: two-row table. All
  personas except urgent-service at entry 400 / hover 180.
  Urgent-service (rescue-ready) at entry 250 / hover 150.
  No per-persona hover differentiation.
- Editorial authoring happens INSIDE Phase 4-new modules
  via LLM calls at named editorial steps. Python
  orchestrates; Claude authors at copy / italic /
  pullquote / eyebrow / rationale prose steps. Output is
  non-deterministic.
- Validator contract for editorial fields: persona-rule
  adherence, not exact-string equality. Structural fields
  remain exact-equality.
- Editorial fields (LLM-authored, adherence-checked):
  * All *Copy fields (headlineCopy, subheadlineCopy,
    eyebrowCopy)
  * headingHierarchy.h1 + h2Sequence[].copy
  * italicSelections[].italicWord + alternativeWord
  * pullQuotes[].extractedText + rhetoricalSlot
  * eyebrowDeployments[].text
  * aboutStory narrativeBlocks[].italicPlacements[].phrase
  * serviceDescriptions[] text content (wordCountTarget
    stays structural)
  * personaReason, signatureMicroInteractionReason,
    microInteractionsReason (rationale prose)
  * constraintRelaxations[].detail prose (rule name stays
    structural)
- Structural fields (deterministic, exact-equality): persona
  enum, tier enum, signature enum values, layout enum
  values, voiceZoneAssignments map keys (values derived
  from voiceMap.md + persona bias — deterministic lookup),
  photoAssignments shape (photo ID selection deterministic
  given inventory + eligibility rules), displayMoment
  pixel values, scaleContrast enum, constraintsOK boolean,
  constraintRelaxations[] rule names + severity,
  microInteractionDurations (per locked Rule 3),
  pathConvention, colorScheme values
- Approval gate UI reshapes locked from Design:
  * constraintsOK block renders ABOVE site-level header
    when false; omits entirely when true
  * Italic status nomenclature: "matches" /
    "class-expected-match" / "class-banned-for-persona"
  * show-derivation <surface> command added to feedback
    loop

Module target: ~/.claude/skills/prospect-site-composer/
(symlinked from ~/grm-automations/skills-experimental/
prospect-site-composer/). Phase 4-new source files live
under phase_4_new/ (Python underscore convention).
Validator lives at scripts/fixture_validator.py.

Six gates. Each ends with an atomic commit. Each has
explicit stop conditions. Report back on any stop
condition triggering — halt before committing, do not
press through.

Session 3 lesson carried: Rule 3 drift surfaced because
the prompt table didn't match committed fixtures. If
ANY rule in this prompt doesn't match fixture state on
disk, halt and report before implementing.

═══════════════════════════════════════════════════════════
GATE A — fixture_validator.py
═══════════════════════════════════════════════════════════

Build the two-pass validator at scripts/fixture_validator.py.
Pure Python, no Phase 4-new dependency. Consumes three
inputs (four with side-channel): emitted plan, fixture
plan, profile, side_channel dict. Returns ValidationResult.

Interface:

    @dataclass
    class StructMismatch:
        field_path: str
        fixture_value: Any
        emitted_value: Any

    @dataclass
    class DerivMismatch:
        field_path: str
        rule: str  # pathConvention | tier |
                   # microInteractionDurations | voiceZones |
                   # scaleContrast | layoutSequence
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
        structural_mismatches: list[StructMismatch]
        derivation_mismatches: list[DerivMismatch]
        adherence_mismatches: list[AdherenceMismatch]

    def validate_fixture(
        emitted_plan: dict,
        fixture_plan: dict,
        profile: dict,
        side_channel: dict = None,
    ) -> ValidationResult:
        ...

Structural pass: deep-object equality on every field in §2
+ §4 + §5.3 outside the six §14 intent-spec fields AND
outside the editorial fields list above. Arrays compared
element-wise ordered. Nulls match null↔null. Missing-field
vs null distinguished.

Editorial-adherence pass (on editorial fields only, not
structural):
- italicSelections[].italicWord: must be drawn from
  persona's expected word-class per Gate 1 persona table.
  Lookup from emotional-arc.md persona-word-class column.
  Non-matching class → AdherenceMismatch.
- pullQuotes[].extractedText: word count must be 8-20
  per composition-plan-schema heuristic. Out-of-bound →
  AdherenceMismatch. (Note: Fixture 2 carries a 32-word
  pullquote as grandfathered authoring; see Checkpoint
  2 retrofit decision. For Gate A self-check mode,
  adherence pass SKIPPED on editorial fields since
  fixtures are authored intent not emission output.)
- Rationale prose (personaReason etc.): validated on
  non-empty + persona name mention, not content.
- All other editorial fields: validated on non-empty
  string presence per schema requirement.

Semantic-derivation pass per Design's signed-off rules:

RULE 1 — pathConvention
Derive fixture.site.pathConvention "kebab-case" → {
  homePath: "/", aboutPath: "/about",
  servicePathPattern: "/services/{slug}",
  contactPath: "/contact", trailingSlash: false
}. Deep equality: derived vs emitted.

RULE 2 — tier
Side-channel: validator accepts optional side_channel
dict parameter. Assert fixture.site.tier == side_channel
.get("tier"). When side_channel is None (self-check mode),
compare fixture.site.tier to itself — always passes.

RULE 3 — microInteractionDurations (LOCKED TWO-ROW)
Derive from persona:

    persona_durations = {
      "quiet-confidence":    {"entry": 400, "hover": 180},
      "earned-pride":        {"entry": 400, "hover": 180},
      "neighborhood-steady": {"entry": 400, "hover": 180},
      "modern-specialist":   {"entry": 400, "hover": 180},
      "urgent-service":      {"entry": 250, "hover": 150},
    }

Lookup from fixture.site.persona; compare to emitted
site.microInteractionDurations (or in self-check mode,
to fixture.site.microInteractionDurations).

RULE 4 — voice-zone flatten
Each page's sections carry inline voiceZoneAssignments
(key→voice maps). Flatten across all sections to build
page-level voiceZones[] per §4.2:

    {
      zone: string,
      defaultVoice: string,     # lookup from voiceMap.md
                                 # 13-row zone table + hero/
                                 # faq splits to 15 zones
                                 # per schema §7
      personaBiasApplied: bool,
      resolvedVoice: string,
      biasReason: string|null,  # from voiceMap.md persona-bias
                                 # column if personaBiasApplied
    }

Validator reads voiceMap.md at load time. Builds two
lookups: {zone_key: default_voice} and {(zone_key, persona):
bias_reason_text}. When resolvedVoice != defaultVoice,
look up bias_reason_text. If no entry found but
resolvedVoice differs, DerivMismatch.

Compare flattened array to emitted page.voiceZones[].
Order-independent on zone keys; per-zone structural
equality on fields. In self-check mode, verify
inline-to-flatten internal consistency: no duplicate zones,
all zones drawn from voiceMap.md 15-zone enum, every
resolvedVoice differing from defaultVoice has a
persona-bias rule backing it.

RULE 5 — scaleContrast threshold
Map fixture.page.scaleContrast string to minimum ratio:
high → 7.0, medium → 4.5, low → 3.0. Assert emitted
page.scaleContrast.achievedRatio >= minimum. Threshold-GE,
not equality. Achieved ratio computed by Phase 4-new at
emission time from colorScheme primary/darkPrimary/accent
vs dominant background via WCAG contrast math. In
self-check mode, rule is SKIPPED (no emitted achievedRatio
yet; rule activates at Gate E).

RULE 6 — layoutSequence
Derive from emitted page.sections: [s.type for s in
sections]. Assert fixture.page.layoutSequence == derived
element-wise ordered. In self-check mode, verify
fixture.page.layoutSequence == fixture.page.sections.map(type).

GATE A EXECUTION

1. Implement validator per above.
2. Run self-check mode against all 6 fixtures:
   validate_fixture(fixture_plan, fixture_plan, profile,
   side_channel=None) for each.
3. Self-check expected to pass cleanly on all 6. Any
   failure surfaces fixture authoring drift OR §14 spec
   ambiguity.

STOP CONDITION: if any of the 6 fixtures fail validator
self-check, HALT before committing. Report which fixture,
which rule, which field, what the derivation produced vs
what the fixture declared. Do NOT fix the fixture; flag
for Chat-Claude / Design resolution.

Note: editorial-adherence pass is SKIPPED in self-check
mode per Design's Session 3 close note — fixtures are
authored intent, adherence is checked against LLM-produced
emission. Fixture 2 pullquote retrofit decision defers to
Checkpoint 2.

Commit message: "composer: stage III gate A —
fixture_validator.py two-pass validator with self-check
clean on 6 fixtures"

═══════════════════════════════════════════════════════════
GATE B — Site-level modules
═══════════════════════════════════════════════════════════

Build under phase_4_new/site/. Five modules:

1. score_profile.py — scoreProfile() function.
   Authority: SKILL.md lines 286-294 (rubric). Pure
   function over profile signals. Returns int 0-100 +
   category breakdown.

2. assign_tier.py — assignTier() function.
   Authority: SKILL.md lines 296-300 thresholds. Premium
   70-100 / Professional 40-69 / Standard 0-39.

3. select_persona.py — selectPersona() function.
   Authority: emotional-arc.md Persona selection section
   + tenure+trade convergence clause + Gate 1 6-column
   bias table. Input: profile.json + tier. Output:
   {persona, personaReason}. Implements three-input
   priority: captured tone → tenure+trade → trade-default →
   QC fallback.

   personaReason is EDITORIAL. Invoke Claude with prompt
   encoding the three-input priority trace + convergence
   logic. Validator checks non-empty + persona name
   mention.

4. resolve_signatures.py — resolveSignatures() function.
   Authority: SKILL.md Gate 2 signature tree + Gate 1
   Tier 1 / Tier 2 default columns. Input: persona, tier,
   profile. Output: {signatureMicroInteraction,
   signatureMicroInteractionReason, microInteractions,
   microInteractionsReason, microInteractionDurations}.
   Durations from persona per locked two-row Rule 3
   (same table as validator).

   signatureMicroInteractionReason + microInteractionsReason
   are EDITORIAL. Invoke Claude with tree-rule firing
   trace as prompt context.

5. set_color_scheme.py — setColorScheme() function.
   Authority: composition-plan-schema §2.3 reference
   table, emotional-arc.md Gate 1 persona default-bias.
   Input: profile.brandPalette, persona. Output:
   {primary, accent, darkPrimary, primaryUsage}.
   primaryUsage values: primary-heavy | balanced |
   accent-heavy | accent-only.

Orchestrator stub at phase_4_new/phase_4_new.py imports
all five, composes in dependency order, emits partial
site block. pathConvention emits "kebab-case"
(intent-spec). voicesInUse emits []. constraintsOK true,
constraintRelaxations []. (Both fill at Gate E.)

GATE B EXECUTION

Run phase_4_new.py against all 6 fixture profile.json
inputs. For each, build partial emitted plan (site block
only, pages: []). Validate against fixture expected
composition-plan.json in site-block-only mode.

STOP CONDITION: if site-block validation fails for any
fixture, HALT. Report fixture, field or rule, what
Phase 4-new produced vs fixture expects.

Commit message: "composer: stage III gate B — Phase 4-new
site-level modules (score, tier, persona, signatures,
colorScheme)"

═══════════════════════════════════════════════════════════
GATE C — Page structure + section emitters
═══════════════════════════════════════════════════════════

Build under phase_4_new/pages/ and phase_4_new/sections/.

phase_4_new/pages/:

1. emit_heading_hierarchy.py — emitHeadingHierarchy()
   function. Authority: composition-plan-schema §4.1 +
   SEO preservation §7 item 2. Input: profile + page
   context. Output: {h1, h2Sequence[]}. H1 + all h2 copy
   are EDITORIAL — invoke Claude with persona-voice
   guidance.

2. select_layouts_per_page.py — selectLayoutsPerPage()
   function. Authority: composition-plan-schema §5.3
   allowed-layout enum + emotional-arc.md Gate 1
   "Editorial layouts (weighted)" column. Input:
   sections, persona, tier. Output: each section's
   layout field.

3. enforce_layout_distinctness.py — post-assignment
   invariant. Per schema §6, 3-5 distinct layouts per
   page. Returns validation error if not met.

phase_4_new/sections/:

4. emit_hero.py — emitHero() per §5.3.1. Authority:
   §5.3.1, hero-patterns.md, SKILL.md legacy heroMode
   + glassVariant trees re-authored against new output
   path.

5. emit_services_grid.py — emitServicesGrid() per
   §5.3.2. Includes multi-vertical category-grouped
   branch when profile has ≥2 service categories and
   ≥6 total services.

6. emit_testimonials_section.py —
   emitTestimonialsSection() per §5.3.3. reviewCountCallout
   emits when reviewCount ≥ 100 per persona rule.

7. emit_about_story.py — emitAboutStory() per §5.3.4.
   Narrative block copy + italicPlacements are EDITORIAL.

8. emit_minimal_section.py — for 6 stub types (faqSection,
   beforeAfter, anchorStrip, trustSection, contactForm,
   footerSection). Emits {type, id} + fixture-observed
   optional fields. Log new emission shape decisions
   inline in code comments referencing fixture source.

Orchestrator update: phase_4_new.py emits sections[] +
headingHierarchy + layoutSequence (derived). Cross-page
editorial stays empty for Gate C.

GATE C EXECUTION

Run phase_4_new.py against all 6 fixtures. Validator
checks site + page-structure + §5.3 section contracts
(hero/servicesGrid/testimonialsSection/aboutStory);
structural equality for 6 stub types via
emitMinimalSection. Rule 6 layoutSequence derivation
active. Editorial fields get adherence check (H1 + h2
copy non-empty + persona word-class eligibility).

STOP CONDITION: structural mismatch on §5.3 field,
layoutSequence derivation mismatch, distinctness
invariant failure, or editorial adherence failure on
any fixture → HALT.

Commit message: "composer: stage III gate C — Phase 4-new
page structure + 4 §5.3 section emitters + 6 minimal-stub
emitters"

═══════════════════════════════════════════════════════════
GATE D — Cross-page editorial
═══════════════════════════════════════════════════════════

Build under phase_4_new/editorial/.

1. resolve_voice_zones.py — resolveVoiceZones().
   Authority: voiceMap.md 15-zone table + persona bias,
   composition-plan-schema §4.2 + §7. Input: sections,
   persona. Output: inline voiceZoneAssignments per
   section + page-level voiceZones[] (§4.2 shape).
   Phase 4-new emits both per Design's clarification.

2. select_italics.py — selectItalics(). Authority:
   emotional-arc.md Gate 1 italic word-class per
   persona, composition-plan-schema §4.4. Input:
   headingHierarchy + persona + profile. Output:
   italicSelections[] per §4.4: {headingId, italicWord,
   personaWordClassAnnotation, approvalState,
   alternativeWord}. italicWord + alternativeWord are
   EDITORIAL. approvalState defaults "pending" at
   Phase 4-new emission.

3. deploy_pull_quotes.py — deployPullQuotes(). Authority:
   typography-patterns.md §6 8-20-word heuristic,
   composition-plan-schema §4.5 count limits. Input:
   profile.testimonials + page sections. Output:
   pullQuotes[] per §4.5. extractedText + rhetoricalSlot
   are EDITORIAL.

4. deploy_eyebrows.py — deployEyebrows(). Authority:
   composition-plan-schema §4.6, Check 4 banned-section
   rule. Input: sections. Output: eyebrowDeployments[].
   text field is EDITORIAL.

5. set_display_moment.py — setDisplayMoment(). Authority:
   composition-plan-schema §4.9 + Check 8 threshold.
   Input: sections, persona, Tier 1 signature. Output:
   displayMoment or null. Contact pages emit null.

6. compute_scale_contrast.py — computeScaleContrast().
   Authority: typography.md §7 per-persona minimum,
   composition-plan-schema §4.10. Input: sections +
   persona. Output: scaleContrast string (intent-spec) +
   achievedRatio (side-channel for validator Rule 5)
   via WCAG math on colorScheme vs dominant background.

Orchestrator: voicesInUse per page from voiceZones[]
resolvedVoice set; site-level voicesInUse is union across
pages.

GATE D EXECUTION

Run phase_4_new.py against all 6 fixtures. Validator
Rules 4 + 5 fire. Italic / pullquote / eyebrow /
displayMoment structural equality + editorial adherence
checked.

STOP CONDITION: voice-zone flatten derivation failure,
scaleContrast threshold failure, structural mismatch on
editorial-field shape, or adherence failure on any
fixture → HALT.

Commit message: "composer: stage III gate D — Phase 4-new
cross-page editorial (voice zones, italics, pullquotes,
eyebrows, display moment, scale contrast)"

═══════════════════════════════════════════════════════════
GATE E — Photo + integrity + full orchestrator
═══════════════════════════════════════════════════════════

Build under phase_4_new/photo/ and phase_4_new/integrity/.

phase_4_new/photo/:

1. assign_photos.py — assignPhotos(). Authority:
   profile-schema §10.1 eligibility predicates,
   image-handling.md content-match, composition-plan-schema
   §4.3 + §5.3 per-section photo-role. Input:
   profile.photoInventory + sections + persona. Output:
   page.photoAssignments[] per §4.3 shape.
   placeholderFlag + placeholderReason populated from
   content-match failure type.

phase_4_new/integrity/:

2. detect_over_constraint.py — detectOverConstraint().
   Authority: SKILL.md 513-557 legacy reasons + Fixture 3
   extended vocabulary (photoLibrary.accepted <= 4,
   servicesGrid photo-content-match, brandPalette
   .vibrantPopulation low-confidence, reviewCount below
   threshold, yearsInBusiness null),
   composition-plan-schema §2. Input: full draft plan +
   profile. Output: {constraintsOK, constraintRelaxations[]}.
   detail prose on each relaxation is EDITORIAL.

Orchestrator full assembly:

    def phase_4_new(profile: dict) -> dict:
        score = score_profile(profile)
        tier = assign_tier(score)
        persona_result = select_persona(profile, tier)
        signatures = resolve_signatures(
            persona_result["persona"], tier, profile
        )
        color_scheme = set_color_scheme(
            profile["brandPalette"], persona_result["persona"]
        )

        pages = []
        for page_context in enumerate_pages(profile):
            hh = emit_heading_hierarchy(profile, page_context)
            sections = emit_sections_for_page(
                profile, page_context,
                persona_result["persona"], tier
            )
            layouts = select_layouts_per_page(
                sections, persona_result["persona"], tier
            )
            enforce_layout_distinctness(sections, layouts)
            voice_zones = resolve_voice_zones(
                sections, persona_result["persona"]
            )
            italics = select_italics(
                hh, persona_result["persona"], profile
            )
            pull_quotes = deploy_pull_quotes(
                profile["testimonials"], sections
            )
            eyebrows = deploy_eyebrows(sections)
            display_moment = set_display_moment(
                sections, persona_result["persona"],
                signatures["signatureMicroInteraction"]
            )
            scale_contrast, achieved_ratio = \
                compute_scale_contrast(
                    sections, persona_result["persona"],
                    color_scheme
                )
            photo_assignments = assign_photos(
                profile["photoInventory"], sections,
                persona_result["persona"]
            )
            pages.append(assemble_page(
                page_context, hh, sections, layouts,
                voice_zones, italics, pull_quotes, eyebrows,
                display_moment, scale_contrast, achieved_ratio,
                photo_assignments
            ))

        site_voices_in_use = union_of_page_voices(pages)
        draft_plan = assemble_plan(
            profile, score, tier, persona_result, signatures,
            color_scheme, site_voices_in_use, pages
        )
        integrity = detect_over_constraint(draft_plan, profile)
        draft_plan["site"]["constraintsOK"] = \
            integrity["constraintsOK"]
        draft_plan["site"]["constraintRelaxations"] = \
            integrity["constraintRelaxations"]

        return draft_plan

GATE E EXECUTION

Run full phase_4_new.py against all 6 fixture profiles.
Validator runs full two-pass + editorial-adherence:
- Structural equality on every field outside §14
  intent-spec AND outside editorial fields list
- Editorial adherence on editorial fields (persona-rule
  adherence, not exact-string)
- Semantic derivation on all 6 intent-spec rules (Rules
  1-6), including Rule 5 threshold now active

All 6 fixtures expected to pass. Moment of truth.

STOP CONDITION: any fixture fails validation → HALT.
Report complete ValidationResult.

Known signal: Fixture 6 (Summit) quiet-confidence ×
Professional. Phase 4-new structural emission should be
clean. Drift A/B is a Phase 5 concern, not Phase 4-new.
If Fixture 6 validates clean here, Phase 4-new is not the
drift source.

Commit message: "composer: stage III gate E — Phase 4-new
photo assignment + over-constraint detection + full
orchestrator; all 6 fixtures pass two-pass validation"

═══════════════════════════════════════════════════════════
GATE F — Approval gate renderer
═══════════════════════════════════════════════════════════

Build phase_4_new/approval/render_approval_gate.py.

Authority: brain §9 + Design's three signed-off reshapes.

RESHAPE 1 — ordering. When constraintsOK=false,
⚠ constraint-conflicts block renders ABOVE site-level
header. When constraintsOK=true, block omits entirely.

RESHAPE 2 — italic status nomenclature:
- "matches" (unchanged)
- "class-expected-match" (renamed from "expected-class")
- "class-banned-for-persona" (renamed from
  "banned-class-warning")

Rendering: "italic: <phrase> class=<word-class> [status]"

RESHAPE 3 — feedback-loop commands add "show-derivation":
Full command list:
- proceed
- revise <surface>
- override persona:<name>
- override signature:<name>
- override layout:<pageKey>.<sectionId>:<layout>
- show-derivation <surface>  ← new
- Per-italic / per-pull-quote inline commands

show-derivation dumps the resolution chain: tree rule
fired, persona default consulted, tie-break applied. For
persona → three-input priority trace. For signature →
Gate 2 tree rules walked. For voice zone → voiceMap.md
lookup + persona-bias rule applied. For layout →
allowed-enum intersection with persona weighted-column.

Format: Code's Session 3 scoping Part 3 holistic per-page
proposal + reshapes. Site-level header, per-page blocks
home → about → contact → service alphabetical. Italic
pick-or-confirm mechanic per renamed statuses. Feedback
commands at bottom.

Additional signed-off surfaces:
- placeholderFlag=true inline with ⚠ fallback-path-b +
  placeholderReason
- vibrantPopulation low-confidence as site-level palette
  annotation
- yearsInBusiness.exact null as site-level key-facts
  annotation
- reviewCount below threshold as data-quality signal
- multi-trade licenseNumber parsed site-level
- Pull-quote approvalState with italic-identical mechanic
- microInteractionDurations override footnote
  (rescue-ready 250ms entry: "entry: 250ms ← persona
  accelerates from 400ms default")

Interface:

    def render_approval_gate(
        composition_plan: dict,
        profile: dict,
    ) -> str:
        """Returns formatted text for chat-mediated review,
        per brain §9 + Design's signed-off UI spec with
        reshapes 1/2/3."""

GATE F EXECUTION

For each of 6 fixtures, run phase_4_new.py → produce
composition_plan → render_approval_gate(composition_plan,
profile). Verify output matches Design's spec:
- Constraint-conflicts block position (above header for
  Fixture 3 constraintsOK=false; omitted for other 5)
- Italic status nomenclature uses new names
- show-derivation in feedback block
- Additional surfaces render based on fixture data

STOP CONDITION: rendered output diverges from Design's
spec → HALT, report divergence.

Commit message: "composer: stage III gate F — Phase 4-new
approval gate renderer per brain §9 + Design's signed-off
UI spec with 3 reshapes"

═══════════════════════════════════════════════════════════
AFTER GATE F
═══════════════════════════════════════════════════════════

Report back with:
- 6 gate commit hashes (A-F)
- Module file count per gate
- Any stop conditions triggered + how resolved
- Validation summary: 6/6 fixtures clean at Gate E
- Any emission shape decisions in emit_minimal_section.py
  logged inline per Part 5 convention

After Gate F, Stage III closes pending Checkpoint 2
(Design reviews 2-3 fixture outputs — Fixtures 2/3/4
anchor set). Chat-Claude coordinates Checkpoint 2 review
with Design. Post-sign-off, Stage IV Phase 5-new scoping
opens.

No writes outside the 6 gate commit targets.
```

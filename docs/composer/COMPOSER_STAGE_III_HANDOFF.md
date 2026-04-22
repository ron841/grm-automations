# Composer Stage III — Handoff Brief

**For:** Fresh Chat-Claude window opening Stage III work. Authored: 2026-04-22 evening, end of Session 2 (Stage II close — sub-stages c/d/e/f committed). Your role: Chat-Claude in CTO seat, translating between Design (creative director) and Code (implementation), reporting to Ron (founder, ultimate authority on both product and process).

**Read order for Session 3 open:**
1. This file — first. Working culture before mechanics.
2. `~/grm-automations/docs/composer/COMPOSER_BRAIN.md` — source-of-truth spec. Read PART I fully; scan PART II Living section newest-to-oldest until you've absorbed the 2026-04-22 Stage II close block.
3. `~/grm-automations/skills-experimental/prospect-site-composer/references/profile-schema.md` and `composition-plan-schema.md` — the locked schema surface Phase 4-new builds against.
4. `~/grm-automations/docs/composer/composer-backlog.md` — Active items; several gate Stage III work.
5. Code's read-only diagnostic of Composer's current Phase 4 and Phase 5 state (first prompt you'll send in Session 3).

---

## Part I — The working culture (read this first)

### The three parties and their authority

**Ron** (founder, CTO-over-Chat). Originates the project, holds veto authority on everything. ~30 years of media and phone sales experience; communicates primarily via voice-to-text, so interpret intent charitably over literal transcription. When Ron says "you're the CTO, lead this" or "trust your instinct," it's real delegation — not performative. Make the calls. Don't loop back for confirmation on judgment calls you're equipped to make. Ron will also correct your instincts in real time when they drift — today he redirected away from over-engineering a verification gate on CONFIG.spacing calibration ("tier has become less important to me"). Corrections are the signal, not the criticism.

**Design** (creative director, editorial authority). Built the editorial framework Composer exists to implement. Authority on editorial matters is higher than the brain file's stated intent — when evidence warrants, Design overrules the spec. This session Design delivered two architectural innovations that weren't in his original Checkpoint 1 response: the two-tier signature resolution (Tier 1 compositional singular + Tier 2 motion plural) on signatureMicroInteraction, and the base-plus-multiplier architecture on CONFIG.spacing (splitting editorial authorship from engineering calibration). Design operates at the architecture level, not just the editorial-values level. Expect him to reframe, not just respond.

**Code** (implementation, tech authority). Executes in Claude Code. Permanent memory across sessions via claude-mem — reads commits, file paths, and prior context without re-briefing. Leans toward mechanical fidelity to the brain file and diagnostic-first discipline before destructive operations. Code has demonstrated authority-read discipline that pays off — reading `image-handling.md` before profile-schema Flag 1 surfaced the richer role vocabulary; reading SKILL.md Phase 4 before the composition-plan-schema commit surfaced the framework-level signatureMicroInteraction mismatch. Both were framework-level issues Chat-Claude's drafts wouldn't have caught. Trust Code under full authorship on mechanical work. Keep Code on draft-and-report when editorial translation is load-bearing.

**Chat-Claude** (you, CTO seat). Translate between Design and Code. Draft paste-ready prompts for Code; draft review briefs for Design (with all artifacts included — no `[PASTE X HERE]` placeholders); hold the thread between sessions. Your role is not to lead creative direction (Design) or execute implementation (Code) — it's to hold both voices honestly, surface friction instead of suppressing it, and deliver highest-fidelity translation in both directions.

### The friction between Code and Design is real and productive

Code wants spec fidelity. Design wants editorial authority. Those disciplines will conflict at multiple points in Stage III. When they do, don't flatten the conflict. Don't quietly split the difference. Don't pick one side by default. Surface the conflict to Ron with both perspectives clearly named.

This session's clearest example: Code's verification step before committing composition-plan-schema.md surfaced a framework-level mismatch on signatureMicroInteraction that Chat-Claude hadn't caught and Design's Checkpoint 1 response hadn't anticipated. Chat-Claude routed to Design with three paths named; Design resolved with a fourth (two-tier architecture). That's the pattern — Code surfaces, Chat routes, Design reframes, Ron approves.

### Ron's governing philosophy — "right over fast"

Atomic commits over bundled commits. Diagnostic-first over assumption-based. Full authorship earned through demonstrated trust rather than granted by default. Pause at natural stopping points rather than pushing through to exhaustion. Quality of the commit matters more than volume of commits.

This cuts both ways. "No rushing to close stages because a session is ending" also means "no rushing to end a session because a stage is closing" — today Ron chose to push through Stage II close-out rather than wrap between sub-stages, and that worked because capacity and context held. Read your own state and Ron's lead, not the clock.

### The small-check-ins-on-editorial-reach rule (Session 2 codification)

When Code surfaces a conflict, pushback, or substantive finding on anything that touches Design's editorial authority, route to Design for a check-in before making the call — even when the surface reads like pure mechanics. Ron named this rule explicitly this session: "anytime conflict pops up from Code on items that involved Design, small check-ins always get us the best result."

The corrected pattern: Chat-Claude makes the call only when it's obviously *not* editorial; everything ambiguous routes to Design for a small check-in. Cheaper to send a three-question Design brief than to commit a decision that Design corrects later.

### What Design actually needs from you

- Paste-ready briefs with all artifacts included. No placeholders.
- Specific questions with options where there are options; open-ended where there aren't.
- Don't bluff signoff. If you're uncertain whether Design has enough to answer, ask what else he needs before drafting the answer yourself.
- Honor Design's reframes. If Design's response reshapes the question you asked rather than answering it, the reshape is the answer — don't try to pull him back to your original framing.

### What Code actually needs from you

- Clear stop conditions ("if X, stop and report").
- Full-authorship scope named explicitly when granted.
- Diagnostic-first discipline on risky operations.
- Exact OLD → NEW strings when Chat-Claude is pre-specifying edits; full latitude when Chat-Claude isn't.
- Bundle prompts when the sequence is well-understood; unbundle when diagnostics could change the next step's scope.

Code will push back when a prompt is wrong. The pushback is almost always correct — treat it as the signal.

### Composer's load-bearing principles

Three principles govern Composer's architecture. They'll shape Stage III Phase 4-new implementation:

1. **Variety across prospects comes from persona variety, not font-selection randomness.** Two prospects with the same persona get the same font pairing by default. Phase 4-new's persona decision is the primary variety axis.

2. **Phase 4 decides. Phase 5 implements. Phase 5.5 references.** No editorial decision-making in Phase 5 — it emits HTML from composition-plan.json. No facts invented in Phase 4 — it consumes from profile.json. Schema is the contract that enables this separation.

3. **No v0.7 default HTML inheritance.** If composition-plan.json doesn't specify a layout, Phase 5 hard-errors. Complete-by-design.

If a Stage III implementation draft violates any of these three, it's wrong regardless of how it looks otherwise.

---

## Part II — Where the build is (what Sessions 1-2 accomplished)

Stage I (scoping locks), Stage II (a)+(b) (file copies + Wave 1/2 backports), and Stage II (c)+(d)+(e)+(f) are all closed. **Stage II closed 2026-04-22.**

### Substantively done in Composer's files (Session 2)

**Schemas on disk (Stage II (c)):**
- `references/profile-schema.md` — 389 lines. Phase 3 output contract. `schemaVersion: 1.0`. Eight-role closed `eligibleRoles` enum (heroBackground, heroPlate, ownerPortrait, environmentalPortrait, detailShot, evidenceShot, gallery, credential). Phase 4 `design.*` fields migrated out. photoInventory carries parsed widthPx/heightPx integers. brandPalette raw-swatches-only. (Commit 83b2c43.)
- `references/composition-plan-schema.md` — 530 lines. Phase 4 → Phase 5 contract. `schemaVersion: 1.0`. Two-tier signature architecture (Tier 1 `signatureMicroInteraction` compositional + Tier 2 `microInteractions` motion). 15 closed voice zones. 17 locked scope decisions in §13. Per-section-type allowed-layout enum. Check 11 unfalsifiable by construction via single-value stats. (Commit 06262f9.)

**Typography merge on disk (Stage II (d)):**
- `references/typography.md` — 952 lines. Three-voice system (Display/Body/Data). Appendix B rewritten to persona-conditional-universal. Orientation-gating prose preserved under role-class SectionOpener framing. `--ff-*` tokens swept to `--font-*`. Serif-display/sans-display persona grouping declared at §11 to support downstream anti-slop Block A refactor (added in Stage II (e), fc0ebfa predates it). (Commit 4e70a0b.)
- `references/voiceMap.md` — 532 lines. Design's 13-row zone table + Composer's anchor-strip section + three-tier service composition + Featured Pullquote voice-layering breakdown. Cross-references typography.md Rule 5 for pullquote placement. (Commit fc0ebfa.)

**Tier-logic strip on disk (Stage II (e)):**
- `references/css-framework.md` CONFIG.spacing refactored to persona-base (5 personas × 4 values) + tier-multiplier (2 multipliers). `:root.tier-*` blocks retired. Tier-keyed font tables removed with cross-reference to typography.md §11.
- `references/anti-slop-rules.md` Block A refactored around persona + serif-display/sans-display grouping.
- `SKILL.md` glass-variant wide-trigger rationale cites Appendix B section-density dimension; `class="persona-{kebab-key}"` replaces `class="tier-premium"` emission.
- `references/example-build.md` pre-Composer-era status-note header added (full rewrite backlogged). (Commit 4e70a0b.)

**P6.1 on disk (Stage II (f)):**
- `scripts/rendered_content_check.py` — 530-line Python stub. Playwright + Pillow via grm-browser reuse. Two-threshold model (hard-fail <5%, soft-fail <15% desktop/tablet, <20% mobile). Static-blank vs. scroll-dependent branch. CLI arg wiring. `NotImplementedError` marks execution-fill points.
- `references/phase-6-integration.md` — 153-line integration spec covering P6.1 fully + P6.2/P6.3/P6.4 placeholders. (Commit 2650ac1.)

### Docs-side done (Session 2)

- `COMPOSER_BRAIN.md` PART II Living section — 2026-04-22 Stage II close block appended. Stage II close state captured in full.
- `COMPOSER_STAGE_II_C_HANDOFF.md` committed to disk (the handoff that opened Session 2; was in chat context but never on disk).
- `composer-backlog.md` — 2 items transitioned Active → Resolved; ~10 new Active items added across four commits.
- `execution-log.md` — rolling per-action trace updated per brain §13 convention.

### Deferred and tracked (composer-backlog.md Active items that affect Stage III)

Read these at Session 3 open — they gate or shape Phase 4-new implementation:

**Direct Stage III gates (must land before Phase 4-new signs off):**
1. `emotional-arc.md` persona-signature column rewrite — currently keyed to legacy five motion-based strings; rewrite to reference Tier 1 compositional signatures + add Tier 2 parallel column. Phase 4-new consults this file for persona-indexed defaults.
2. `SKILL.md` Phase 4 signature decision tree (lines 417–427) rewrite against Tier 1/Tier 2 vocabulary.
3. `css-framework.md` Motion Restraint review — confirm section governs Tier 2 cleanly and doesn't reference Tier 1.

**Adjacent to Stage III (may or may not gate; review at session open):**
4. Hero background hue-warmth derivation rule citation — Phase 5 computes but rule isn't cited authoritatively anywhere. If Phase 4-new touches hero decisions, this surfaces.
5. `image-handling.md` role-hierarchy eligibility/assignment split — prose needs updating for the eligibility (plural) vs. assignment (singular) distinction. Not blocking Phase 4-new if Code reads schemas as authority; could surface as confusion during implementation.
6. `composition-plan-schema.md §5.3` per-section-type contracts — stubs for 11 section types (hero, servicesGrid, testimonialsSection, featuredPullQuote, faqSection, beforeAfter, anchorStrip, trustSection, contactForm, footerSection, aboutStory) deferred from Checkpoint 1 q6. Priority order per Design: hero, servicesGrid, testimonialsSection, aboutStory, remainder. Phase 4-new implementation probably wants these filled in before producing composition plans — they define what each section type's composition-plan entry must carry.

**Deferred (don't gate Stage III):**
7. Post-Stage-II-(e) F1-F8 spot-check — Luna covered; 4 other personas × tiers pending.
8. First-real-build editorial reviews — shimmer-hero-cta retention decision.
9. Composer-era reference build authoring pass (replace example-build.md header-noted state).
10. Editorial nickname asymmetry for urgent-service persona.
11. `scale-architecture.md` structural rewrite.
12. `LESSONS.md` entry format normalization + v0.7/v0.8 identity language.
13. P6.1 execution filling pending (Stage II (f) stub → full implementation).

### Informational
- Design artifact filenames ≠ Composer filenames (cross-check before commit drafts).

---

## Part III — What Stage III is

Per brain §8 Stage III: **Phase 4-new implementation.** Code builds Phase 4-new reading `profile-schema.md` and `composition-plan-schema.md`. Reads `profile.json`. Produces `composition-plan.json`. Validated against Stage II.5 fixtures first, then Luna F8's actual profile.json.

**But Stage II.5 precedes Stage III.** Per brain §8 Stage II.5: hand-written `profile.json` fixtures covering sparse photo library (0-3 hero candidates), populated library (8+), over-constraint (insufficient photos for layout minimum), high-review-count, low-content-depth, multi-vertical. Each fixture pairs with an expected `composition-plan.json` outcome. Feeds Stage III.

### Stage II.5 — profile.json fixtures (session 3 first work)

**Scope character:** editorial translation + fixture engineering. Chat-Claude likely drafts the fixture inventory (what persona/tier/vertical each fixture represents, what photo-library shape each exercises) with Design pre-review on the persona/vertical selection. Code implements hand-authored `profile.json` files at `~/grm-automations/docs/composer/fixtures/profile/`.

**Six fixtures minimum per brain §8 Stage II.5:**
- Sparse photo library (0–3 hero candidates)
- Populated library (8+)
- Over-constraint (insufficient photos for layout minimum — exercises brain §4 addendum fallback-path-b)
- High-review-count
- Low-content-depth
- Multi-vertical

**Each fixture pairs with an expected composition-plan.json outcome.** Chat-Claude or Design authors the expected outcome based on how Phase 4-new SHOULD behave given the input. This is what Code's Phase 4-new implementation validates against.

**Estimated effort:** 3–5 hours of focused work. Fixture content is ~400–800 lines of JSON per fixture × 6 = substantial but tractable. Could split across sessions.

### Stage III — Phase 4-new implementation

**Scope character:** substantive Code implementation. Full authorship on execution; draft-and-report on architecture decisions that surface. Reads `profile-schema.md` + `composition-plan-schema.md`. Produces Phase 4-new that consumes profile.json, makes all editorial decisions, and produces composition-plan.json.

Key implementation areas:
- **Persona decision** — three-input priority per current SKILL.md Phase 4 + `emotional-arc.md` persona tables (once rewritten per backlog item 1).
- **Layout selection** — 3–5 distinct layouts from {A, B, C, D, E} per page, constrained by per-section-type allowed-value map from composition-plan-schema §6.
- **Voice zone resolution** — 15 zones × persona bias rules from voiceMap.md → resolvedVoice per zone per page.
- **Photo assignments** — consume profile.photoInventory eligibleRoles, produce composition-plan photoAssignments with placeholderFlag on fallback-path-b.
- **Italic selections** — per-H1/H2 with approvalState mirroring approval gate pattern.
- **Pull-quote deployments** — 2-of-5 heuristic from typography-patterns.md §6; count limits from §4.5 (max 1 at sections.length ≤6, max 2 at ≥7).
- **Display moment** — per page, declare which element carries ≥80px desktop / ≥56px mobile.
- **Two-tier signatures** — Tier 1 compositional (6 values) + Tier 2 motion (4 values) with persona defaults per `emotional-arc.md` (once rewritten).
- **colorScheme.primaryUsage** — persona default-bias from composition-plan-schema.md §2.3 reference table.
- **Constraint over-constraint detection** — brain §4 addendum fallback path (a) or (b) emission.

**Estimated effort:** 8–15 hours of focused work. Natural session-splitting expected.

### Checkpoint 2 — Design reviews Phase 4-new output on 2-3 fixtures

Per brain §8 Stage III gate: "Design reviews Phase 4-new output on 2-3 fixtures before Stage IV begins." This is post-implementation, pre-Stage-IV — Design validates Phase 4-new produces sensible composition plans on a representative fixture subset.

**What Design needs to sign off on:**
- Phase 4-new's persona decision tracks `emotional-arc.md` priority logic correctly.
- Layout selection produces 3–5 distinct layouts respecting the per-section allowed-value constraints.
- Voice zone resolution applies persona bias per voiceMap.md rules without conversion-critical-zone leakage.
- Photo assignments handle the eligibility → assignment split correctly, including fallback-path-b placeholder emission.
- Italic selections, pull-quote deployments, display moment placements read as editorial decisions, not template outputs.

**Not Design's job at Checkpoint 2:** schema critique (locked at Checkpoint 1), implementation code review (Code's authorship), fixture review (Stage II.5 pre-work).

---

## Part IV — Session 3 structure (recommended)

**Three plausible shapes, pick based on capacity at session open:**

### Shape A — Stage II.5 only (bounded session)
- Phase 1: Chat-Claude drafts fixture inventory (persona/tier/vertical per fixture + expected composition-plan outcome shape).
- Phase 2: Design pre-review on fixture inventory. Persona/vertical selections signed off.
- Phase 3: Code implements fixtures at `~/grm-automations/docs/composer/fixtures/profile/`. Six files.
- Phase 4: Chat-Claude + Ron validate fixtures against schema. Commit.

Session closes cleanly. Stage III Phase 4-new starts in Session 4.

### Shape B — Stage II.5 + Phase 4-new kickoff (stretched session)
- Shape A through commit.
- Phase 5: Code diagnostic on current SKILL.md Phase 4 (what the legacy tree does). Feeds Phase 4-new authoring.
- Phase 6: Chat-Claude + Design + Code scope Phase 4-new architecture (does it rewrite SKILL.md Phase 4 in place? Live alongside? Staging convention?).
- Session closes with Phase 4-new scoped but not yet implemented.

### Shape C — Stage II.5 + Phase 4-new implementation (long session)
- Shape B through scoping.
- Phase 7: Code authors Phase 4-new against schemas. Likely multi-commit.
- Phase 8: Validate against fixtures.
- Phase 9: Checkpoint 2 prep if time.

Shape C is realistic only if Session 3 opens with high energy and stays focused. Read the session as it unfolds.

**Recommended:** Shape A for a clean session; Shape B if Session 3 opens strong and Stage II.5 wraps faster than expected. Shape C is aspirational — don't plan for it; let it emerge.

---

## Part V — Opening prompt for Session 3 (paste-ready)

Paste into fresh Chat-Claude window to open Session 3:

```
Read ~/grm-automations/docs/composer/COMPOSER_BRAIN.md in full before
responding. That's the source of truth for the Composer rebuild.

Also read the Stage III handoff brief at
~/grm-automations/docs/composer/COMPOSER_STAGE_III_HANDOFF.md. It
captures Session 2's Stage II close, Session 3's options, and the
three-party working culture between you (Chat-Claude), Code, and
Design.

Read the handoff FIRST, then the brain file. Character before
mechanics.

Stage II closed Session 2 (2026-04-22): all six sub-stages a-f
committed. Schemas, typography merge, tier-strip, P6.1 spec all
on disk. Architecture specification complete.

Session 3 scope is Stage II.5 fixture authoring, leading into
Stage III Phase 4-new implementation. Tell me what you read as
Session 3's opening move. My framing: Stage II.5 precedes Stage III
per brain §8 — six profile.json fixtures pair with expected
composition-plan.json outcomes, feeding Phase 4-new validation.
Shape A (Stage II.5 only), Shape B (Stage II.5 + Phase 4-new
kickoff), Shape C (full Phase 4-new implementation) are the three
recommended session shapes in the handoff Part IV.

No execution yet. First prompt to Code should be a read-only
diagnostic of current Phase 4 state (SKILL.md lines 282-536, or the
current line range; handoff Part II has the state at Stage II close)
and composer-backlog.md Active items gating Stage III. That
diagnostic feeds fixture scoping.
```

---

## Part VI — Session 2 process learnings (carry these forward)

**Small check-ins on editorial-reach are the rule.** Ron's explicit codification this session. When Code surfaces a conflict, pushback, or substantive finding on anything with editorial implications, route to Design before making the call. Don't pattern-match "this looks mechanical" and resolve unilaterally.

**Framework-level mismatches surface at Code's authority reads, not in your drafts.** Today's signatureMicroInteraction two-tier resolution wouldn't have happened without Code's verification step reading SKILL.md Phase 4. Yesterday's role-vocabulary expansion wouldn't have happened without Code reading image-handling.md. Authority reads before drafting is Code discipline worth preserving.

**Design operates at the architecture level.** Design's Checkpoint 1 response did more than answer 8 questions — it surfaced structural improvements (per-section-type allowed-layout map vs. single enum; serif-display/sans-display grouping vs. per-persona enumeration). Design's Stage II (e) CONFIG.spacing authorship didn't just author 20 values — it split editorial authorship from engineering calibration as a base-plus-multiplier architecture. Expect architectural innovation, not just value authoring.

**"Trust your instinct" means making calls.** Ron said it twice this session. Once on Item 3 scoping (example-build.md reframe: defer vs. now vs. strip-only) — I made the call (defer with header note). Once on the Luna drift verification gate — Ron redirected my over-engineered verification to "ship Design's values, log spot-check as post-commit." In both cases the right call was to decide, not to route back for confirmation.

**Prompt granularity: bundle when sequence is well-understood; unbundle when diagnostics could change scope.** Session 2 hit the right cadence most passes — inventory-then-execute for Stage II (e) worked well (surfaced four editorial-reach items that would've been silent under bundled execution); single-prompt for Stage II (d) merge execution worked well (12 conflicts resolved upfront, no mid-execution surprises).

**Placeholder-free briefs or don't send.** Every brief to Design this session was paste-ready with all artifacts included. Yesterday's handoff flagged this as a Session 1 failure mode; Session 2 didn't repeat it. Keep this discipline.

**Own your errors, don't hedge.** My four scoping errors from Session 1's handoff didn't repeat today. Where I made a scoping error today (Item 3 — Code flagged that "header note is a speed-bump, not a fix" is a real limitation, not a clean solution), I logged it honestly in the backlog rather than dressing it up.

**Framing corrections from Code are the signal.** Code's "tier isn't retiring from Composer" opener at Stage II (e) inventory reshaped how Chat-Claude and Design processed the entire sub-stage. When Code leads a diagnostic with a framing correction, slow down and absorb it before proceeding.

---

## Part VII — What would make Session 3 fail

**Rushing Stage II.5 fixtures.** Fixtures are the ground truth Phase 4-new validates against. A sloppy fixture (unrealistic photo library, wrong persona signal, expected-composition-plan that doesn't track Design's framework) produces silent Phase 4-new bugs discovered only at Stage V. Spend the time.

**Skipping the backlog triage at Session 3 open.** Three Stage III backlog items (emotional-arc persona-signature column rewrite; SKILL.md Phase 4 signature tree rewrite; css-framework.md Motion Restraint review) gate Phase 4-new implementation. Read these before starting Stage II.5 so they land in the right sequence. Missing one means Phase 4-new consumes stale authority.

**Authoring Phase 4-new against schemas alone without reading emotional-arc.md after its Stage III rewrite.** Schemas declare what; emotional-arc.md declares how personas behave at decision points. Phase 4-new needs both.

**Defaulting to controlling Code rather than trusting full authorship.** Fresh Chat-Claude windows may not inherit Session 2's earned trust. Read Part I carefully to reset the trust model from the start. Code earned additional trust in Session 2 via Stage II (e) framing correction and Stage II (f) mechanical spec; Session 3 opens with that trust intact.

**Flattening Design/Code conflict when it surfaces.** It will surface. Don't split the difference. Surface to Ron with both perspectives named. The two-tier signature resolution was possible because Chat-Claude didn't flatten the framework mismatch Code surfaced.

**Ignoring the Luna F8 drift signal on any near-term quiet-confidence × Professional build.** The drift is real. A visual A/B against Luna F8 precedes locking Design's persona-base values. If Stage III Phase 4-new validates on a fixture that exercises quiet-confidence × Professional, that build's output is a test of the persona-base values as much as of Phase 4-new itself.

**Pushing Shape C when Shape A is the honest session.** The three session shapes are ranked by ambition for a reason. If Session 3 opens with middling energy or context pressure, Shape A is the right landing. Shape C is aspirational — don't plan for it.

---

## Part VIII — Composer health at session close (Stage II close, 2026-04-22)

- `git status` clean for Composer scope.
- Stage II closed: six sub-stages a-f committed on main.
- Six Session 2 commits: c0235af (handoff) + 83b2c43 (profile-schema) + 06262f9 (composition-plan-schema) + fc0ebfa (typography merge) + 4e70a0b (tier-strip) + 2650ac1 (P6.1 stub). Plus six log commits.
- Architecture specification complete. Phase 4-new has a locked spec surface to build against.
- 17 scope decisions locked in `composition-plan-schema.md §13`. 15 locked decisions in `profile-schema.md` (implicit in field structure + migration notes).
- `composer-backlog.md`: ~12 Active items; 2 transitioned to Resolved this session. Clear separation of Stage-III-gating, Stage-III-adjacent, and deferred items.
- Rule E6 + Check 18 intact across all Stage II sub-stages. Sentinel checks passed.
- Playwright + Pillow via grm-browser confirmed reusable; no new dependencies required for P6.1.
- Luna F8 drift signal logged for next quiet-confidence × Professional build A/B.
- All three parties holding clean: Ron, Code, Design.

Composer is stable, well-documented, and ready for Stage II.5 fixture authoring → Stage III Phase 4-new implementation.

---

## End of handoff

Session 3 Chat-Claude: you're not starting fresh on Composer. You're inheriting a collaboration that took two full sessions of careful work to build. Code, Design, and Ron all trust this pattern. Honor it. Read Part I twice before drafting anything. The mechanics only make sense when the culture is the frame.

Character before mechanics. Right over fast. Three voices, one decision. Small check-ins on editorial-reach.

Stage III starts with Stage II.5. Start there.

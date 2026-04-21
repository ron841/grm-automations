# COMPOSER_BRAIN.md

**Source of truth for the v0.8 Composer rebuild of the prospect-site skill.**

Living document. Read from the top at every session open. Updated at every session close.

Canonical path: `~/grm-automations/docs/composer/COMPOSER_BRAIN.md`

Authorship: Code writes all updates via bash. Chat-Claude and Design provide content through chat; Ron reviews and instructs Code to commit. Ron never edits directly.

---

## HOW TO USE THIS FILE

**Opening a fresh window (Claude Code or chat):** First instruction is always *"Read `~/grm-automations/docs/composer/COMPOSER_BRAIN.md` in full before responding. That's the source of truth for the Composer rebuild. Tell me what stage we're on and what's next."* Window orients from the Living section, then goes to work.

**Closing a window:** Last instruction is always *"Update `~/grm-automations/docs/composer/COMPOSER_BRAIN.md` — append a new session block to the Living section with today's date, what we did this session, what changed, what's next. Commit and push."* File captures state before the window closes.

**Two big sections:**
- **PART I — FIXED** is the locked Composer spec. Does not change session-to-session. Only changes via formal revision (see §12 in PART I).
- **PART II — LIVING** accumulates session-close blocks at the top (newest first). Each block captures what happened, what changed, what's next.

---
---

# PART I — FIXED (the locked spec)

## 0. QUICK REFERENCE

- **Name:** v0.8 Composer
- **Retired prior v0.8 scope:** renamed to "v0.8 Scale (deferred)" — items preserved in `project_v08_backlog.md`
- **Foundation skill:** `prospect-site-design` at `~/.claude/skills/prospect-site-design/`
- **Target skill path:** `~/.claude/skills/prospect-site-composer/` (new, symlinked from `~/grm-automations/skills-experimental/prospect-site-composer/`, slash command `/prospect-site-composer`)
- **Production skill (untouched through development):** `prospect-site` at `~/.claude/skills/prospect-site/`
- **Three skills coexist during Composer development:** design-skill as foundation, production as backport source and fallback, prospect-site-composer as Composer's target
- **Status:** Stage I scope locked 2026-04-21. Stages II-VI execute in fresh windows.
- **Two-pillar foundational commitment (both hard gates):** Pillar 1 editorial (Design's framework delivering Luna F8 quality and beyond). Pillar 2 SEO/GEO (schema validity, AI-citation infrastructure, Lighthouse SEO ≥95). A Composer build failing either pillar does not ship. Neither is primary. Neither is secondary.

## 1. LOAD-BEARING PRINCIPLE

**Variety across prospects comes from persona variety, not font-selection randomness.** Two prospects with the same persona should get the same font pairing by default. That is what makes the persona system legible. If future maintainers are ever tempted to add a "mix it up" knob to font selection, that sentence is the answer for why not.

This principle extends beyond fonts to the whole Composer architecture. Phase 4 is deterministic given a profile.json. Composition decisions are explicit and traceable, not emergent. Two contractors with the same persona, tier, and service shape get the same composition plan by default. Variety comes from the five personas producing five different compositions, not from shuffling within a persona.

## 2. BACKGROUND

The prospect-site skill iterated through v0.7.x / v0.8 over the week preceding 2026-04-21. Wave 2 closed 2026-04-20 with rhythm tokens, SectionOpener primitive, StatRow primitive, font system primitives, and Hard Rules #11/#12 landing in production.

On 2026-04-21, Ron paused a planned rebuild-from-scratch and ran a different experiment: Claude Design authored an editorial upgrade package against a v0.7 baseline. The package installed as a parallel experimental skill at `~/.claude/skills/prospect-site-design/`. Luna Master Painting ran through it as Flagship 8. Luna F8 validated Design's editorial framework — Design's own visual diagnosis called it "the first build where the editorial layer is clearly active." The build surfaced seven skill-level bugs, each fixed as Luna build-level patches rather than skill patches.

Composer is the work that restructures design-skill's Phase 4 and Phase 5 against Design's editorial framework, backports production's Wave 1/Wave 2 infrastructure, formalizes the Phase 4 → Phase 5 handoff contract, and ships a skill that makes Luna F8 the baseline rather than the ceiling. Phases 0-3, 5.5, 6, 7, 8 stay structurally intact with small logged patches.

## 3. ARCHITECTURAL FRAME

Two components inside one pipeline with a formalized seam.

**Component A — Site Generator** (Phases 0, 1, 2, 3, 5.5, 6, 7, 8)
Pre-flight integrity, homepage capture + crawl, profile extraction, photo pipeline, SEO/GEO injection, verification, Vercel deploy, HubSpot + backup. Structurally unchanged. Small targeted patches only (§6).

**Component B — Site Designer** (Phase 4 + Phase 5)
Design engine and HTML/CSS/JS emission. Restructured in Composer — not rewritten from scratch. The editorial framework (personas, layouts A-E, photo role hierarchy, E1-E6 discipline rules, scale contrast, motion restraint, signature micro-interactions) stays intact. What changes is how Phase 4 decides composition and how Phase 5 emits HTML, with a formal contract between them and no inheritance of v0.7 default HTML templates.

Component seam lives at Phase 3 → Phase 4 and Phase 5 → Phase 5.5/Phase 6.

## 4. HANDOFF CONTRACT

Three-stage contract:

```
Phase 3 → profile.json (schema: profile-schema.md)
       ↓
Phase 4-new → composition-plan.json (schema: composition-plan-schema.md)
       ↓
Phase 5-new → emitted HTML/CSS/JS + page-level metadata
       ↓
Phase 5.5 → schemas / meta tags / llms.txt (reads profile.json + composition-plan.json, not DOM)
       ↓
Phase 6 → audits emitted files
```

**profile.json** is the canonical output of Phase 3. Business facts, services, photos with photo manifest including dimensions, testimonials, credentials, brand colors, operational claims, service area. Schema formalized in `profile-schema.md` (newly authored in Stage II).

**composition-plan.json** is the new artifact the whole architecture turns on. Structured description of the site in Design's vocabulary: site-level fields (persona, signature micro-interaction selection, path convention, voicesInUse), per-page fields (layout sequence, photo role assignments with fallback behavior, voice-map zone assignments, italic-word selections per headline flagged for Phase 4 human review, scale contrast targets, FAQ question/answer pairs, service descriptions, canonical URL, heading hierarchy contract, lede placements, pull-quote extractions, eyebrow deployments). Phase 5-new reads this plan and emits HTML against it with zero editorial decision-making of its own. Phase 4 decides. Phase 5 implements. Phase 5.5 references.

**Schema versioning from day one.** Every JSON artifact carries a top-level `"$schemaVersion": "1.0"` key plus `"$schema": "profile"` or `"$schema": "composition-plan"`. The corresponding `-schema.md` reference files declare `schemaVersion: 1.0` in their own frontmatter. Stage III Phase 4-new hard-errors if profile.json's `$schemaVersion` doesn't match what profile-schema.md declares. Same for Stage IV and composition-plan.json. Schema version format: `major.minor` — major increments = breaking, minor = additive.

**No v0.7 default HTML inheritance.** Phase 5-new has no fallback templates. If composition-plan.json doesn't specify a layout for a section, the build halts with a schema error; it does not fall back to a v0.7 default. This makes the contract complete by design.

**Photo role scarcity handling.** When profile.json's photo manifest doesn't have enough photos of a role to satisfy a persona's layout preferences, Phase 4 does NOT silently fall back. Phase 4 either (a) selects a layout that doesn't require the missing role, or (b) emits a placeholder-flagged composition plan that Phase 5 renders with a visible placeholder Ron sees at the approval gate. The behavior is named explicitly in composition-plan-schema.md.

## 5. FOUNDATION DECISION (LOCKED)

**Composer is built from `prospect-site-design`** (`~/.claude/skills/prospect-site-design/`).

Rationale (Code's evidence-backed, Ron-confirmed recommendation):

1. Luna F8 empirically validates Design's editorial framework running on design-skill's pipeline. Production has not been validated with that framework running against its Wave 2 primitives.
2. Design's editorial framework is diffused across 5+ reference files in design-skill, co-authored as one coherent package. Transferring into production's Wave 2-evolved files would be a 3-way merge with unknown integration quality. Backporting Wave 2 infrastructure into design-skill is atomic, additive, mostly mechanical.
3. Design-skill carries the color-derivation hardening (Rule E6, Phase 6 Check 18, sentinel defaults, derivePrimaryHover()) that production lacks. Starting from production would mean re-authoring.
4. Pillar 1 is design-skill's strength. Pillar 2 is production's strength. Building up Pillar 2 on design-skill via file copies + bounded cherry-picks is more tractable than building up Pillar 1 on production via multi-file editorial merges.

Production stays untouched through Composer development. Retirement decision deferred to Stage VI.

## 6. COMPONENT A PATCH INVENTORY

All patches are additions to existing phases. No phase restructuring.

**Phase 1:**
- **P1.1** Logo orientation detection. Emit icon-only markup vs. icon+span markup based on source logo aspect ratio. Thresholds: aspect ≤0.9 = square combined-mark (emit combined-logo + span pattern per Chad's flagship), aspect ≥1.1 = landscape wordmark (emit landscape-logo + span pattern), 0.9 < aspect < 1.1 = ambiguous (emit combined-logo + span, flag for human confirmation at Phase 4 gate). Addresses Luna F8 logo-sizing bug class.

**Phase 6:**
- **P6.1** Rendered-content check. Playwright headless Chromium loads the deployed page, captures screenshot at initial paint without scrolling (IntersectionObserver callbacks must not fire before capture). Per-`<section>` painted-pixel ratio measured via canvas pixel analysis against section's computed background color. Two thresholds:
  - **Hard fail below 5%** (severe blank — catches full opacity:0 sections)
  - **Soft fail below 15%** (partial render — contributes to P6.2 soft-fail pattern)
  - Three viewports tested: 375 (mobile), 768 (tablet), 1440 (desktop). Mobile threshold +5% stricter on soft fail (20%) because narrow viewports make blanks starker.
  - Per-section output: pass / hard-fail / soft-fail, plus static-blank/scroll-dependent flag.
  - Implementation lives in `scripts/rendered_content_check.py`, authored in Stage II (f).

- **P6.2** Editorial-rule check suite. **Thirteen checks** per Design's specification in typography-patterns.md:
  1. Max one italic span per H1/H2 (hard fail on 2+)
  2. Eyebrow proximity to H2 within 24px (hard fail)
  3. Eyebrow count per page ≤3 (soft fail on 4+)
  4. No eyebrow on service grids, FAQ, contact forms (soft fail)
  5. Service card numerals use `font-variant-numeric: tabular-nums` (hard fail)
  6. No `.role-body-*` element computes to `var(--font-display)` family (hard fail — body copy in display font)
  7. No `.role-data-*` element computes to `font-size >40px` (hard fail — data voice at display scale)
  8. Minimum display-scale moment per page (`font-size ≥80px` desktop, `≥56px` mobile on at least one element) (hard fail on missing)
  9. Italic word selection vs. persona word-class list (soft fail with warning; human review at Phase 4 approval gate is authoritative)
  10. Pull-quote deployment count (≤1 per standard page, ≤2 on scroll-depth >6) (hard fail on more)
  11. Stats watermark consistency (`.role-display-watermark` text equals `.role-data-numeral` text within same cell) (hard fail — addresses Luna F8 "04" bug)
  12. Three-voice presence per page (at least one `.role-display-*`, one `.role-body-*`, one `.role-data-*`) (hard fail — page using only two voices is incomplete)
  13. Mobile watermark treatment (at 375 viewport, `.role-display-watermark` computes to `font-size ≤100px` OR `display:none` OR corner-positioned via absolute positioning) (hard fail)

  Pattern rule: a build passing all hard-fail checks but accumulating 3 or more soft fails across P6.1 partial-render + P6.2 soft checks = hard fail at the build level. Individual soft fails are shippable; patterns of them are not.

- **P6.3** Composition-plan completeness check. Every section in emitted HTML traces back to a composition-plan.json entry. Unmapped sections = hard fail.
- **P6.4** Schema-to-HTML consistency check. FAQPage schema question/answer pairs match Phase 5's rendered output (which reads from composition-plan.json). Same for Service schema descriptions and ImageObject dimensions vs. photo manifest. Any mismatch = hard fail.

**Phase 5.5 (reclassified as preservation contract, not just patches):**
- **P5.5.1** Phase 5.5 reads schema-relevant content from composition-plan.json and profile.json, not from Phase 5's emitted DOM. Closes the fragile DOM-parsing dependency.
- **P5.5.2** llms.txt generation stays reading from profile.json (formalized current behavior).
- **P5.5.3** All six existing SEO/GEO Phase 6 checks carry forward unchanged as hard gates: BLUF content, semantic HTML + internal linking, AI crawler access, llms.txt, structured data validation, meta tag verification.

**Cross-phase patches from Luna F8 lessons:**
- **PA.1** Skip-link base CSS: `transform: translateY(-100%)` vs. `top: -40px` to hide fully above viewport.
- **PA.2** Mobile promo-bar overlap: nav top-offset responsive to promo-bar wrapped height via media query.
- **PA.3** Stats data binding correctness: Phase 5 binds profile.json stats values to rendered numerals (not display indices). This is a Phase 5-new item primarily but is flagged as cross-phase because of the lesson.
- **PA.4** DarkVibrant swatch override rule. If populated, overrides primary color default derivation. Already in design-skill via Rule E6; preserved across Wave 2 backport.
- **PA.5** Font-loading fallback behavior. If persona-conditional heading font fails to load, page falls back to `--font-body` (safe web font) rather than system default. Fallback chain documented in typography.md after Stage II (d) merge. Tested at Stage V Pillar 2 gates with throttled network profile.

## 7. SEO/GEO PRESERVATION CONTRACT (PILLAR 2)

Phase 5-new must preserve or deliberately replace with documented equivalents:

1. **Semantic HTML discipline.** `<article>` wraps homepage/about/sub-page content. `<section>` wraps every distinct content section with `aria-labelledby` pointing to unique heading ID. `<footer>` exactly one per page. `<nav>` with `aria-label`. Exactly one `<h1>` per page. `<h2>` for major sections, `<h3>` for subsections, no skipped levels. `<address>` for contact blocks. `<time>` with `datetime` attributes.

2. **Per-page heading hierarchy.** Homepage: h1 hero → h2 services (h3 per service) → h2 stats → h2 before/after → h2 testimonials → h2 FAQ (h3 per question) → h2 contact. Service sub-page: h1 → h2 sections → h2 service-specific FAQ → h2 contact CTA. About: h1 → h2 founding → h2 credentials → h2 service area.

   **BLUF DOM-order reconciliation:** Editorial layouts A-E (Layout D full-bleed image with text overlay, Layout E watermark numeral with caption) can push fact-dense content past word 300 in DOM order. Phase 4 enforces BLUF at composition-plan time — either accept a BLUF penalty for a hero layout OR swap to a layout that preserves DOM-order facts. Phase 6 Check 7 (existing SEO/GEO check) does not catch this post-hoc because it reads DOM order only. The enforcement is in Phase 4, not Phase 6.

3. **FAQ content available to Phase 5.5 via composition-plan.json.** Move from DOM-read to plan-read. Eliminates schema-HTML drift class of bug.

4. **BLUF DOM-order discipline.** First 300 DOM words of every page include business name, service category, primary city, license number if captured, phone. Closing Table voice.

5. **Photo manifest with dimensions in profile-schema.md.** OG tag dimensions depend on this. Currently implicit; formalized in Stage II schema authoring.

6. **Canonical URL convention documented in composition-plan-schema.md.** Stable across builds.

7. **Schema-dependent content available to Phase 5.5 via composition-plan.json:** FAQ pairs, service descriptions, aggregate rating, photo references.

**Auto-preserved (no action):** llms.txt generation (reads profile.json), Review schema, LocalBusiness schema, BreadcrumbList.

## 8. MIGRATION SEQUENCE

Each stage ends when it ends. No timelines.

**Stage I — Scoping locks.** Complete as of 2026-04-21. Foundation decision locked. Naming locked as Composer. Pillar framing locked. Handoff contract locked. Component A patch inventory enumerated. Component B restructuring scope locked. SEO/GEO preservation contract enumerated. Stage V/VI rubrics authored (§10, §11). Ron, Code, Design signoff.

**Stage II — Reference files authored, cleaned, backported.** Stage work, in order:

- **(a) File copies** from production `prospect-site` into design-skill (the Composer foundation):
  - `references/typography.md` (545 lines, Design F5-era + Q1/Q2/Q3 revisions + Wave 2 retrofits)
  - `references/voiceMap.md` (261 lines, Design F5-era)
  - `references/LESSONS.md` (473 lines, accumulated build lessons)
  - `references/handoff-discipline.md` (283 lines, Hard Rules #11/#12 process doc)

- **(b) Cherry-pick 11 Wave 1/Wave 2 commits** from production into design-skill:
  - `593173e` (Wave 1 core — rhythm tokens, vercel.json cache-header, content-rules reconciliation)
  - `b0c04e9` (SectionOpener primitive spec)
  - `8654668` + `816f58a` (SectionOpener retrofits — combine)
  - `14820f2` + `d0affba` (StatRow primitive + retrofit — combine)
  - `6ec0f6d` (Fraunces universal across tiers — reconcile tier-removal conflict at Stage III)
  - `076ffec` (`--font-mono` CONFIG token)
  - `11415e6` (JetBrains Mono preload)
  - `83d088a` (mobile breakpoint reconciliation)
  - `6739aa5` (SKILL.md voice-map integration point)
  - `1ca3bd5` (stale font-loading template rewrite — required because design-skill's css-framework.md is pre-Wave-2)

- **(c) Schemas authored:**
  - `profile-schema.md` (formalize current Phase 3 implicit output; include photo manifest with dimensions; declare `schemaVersion: 1.0`)
  - `composition-plan-schema.md` (Phase 4 → 5 contract; complete-by-design — no implicit fallbacks; include FAQ pairs, service descriptions, photo role assignments with fallback behavior, per-page canonical URL, heading hierarchy contract, italic-word selections, lede placements, pull-quote extractions, eyebrow deployments, voicesInUse field, site-level signature selection; declare `schemaVersion: 1.0`)
  - **Design review checkpoint 1** — Design reviews `composition-plan-schema.md` before Stage II.5 fixtures are authored. Critical gate. If schema doesn't express what Design's framework needs (italic-word selection per headline, photo role with fallback, signature micro-interaction site-level placement), Phase 4-new cannot implement it.

- **(d) Typography three-way diff merge:**
  - Three files enter: production baseline (Stage II (a) file copies), Design in-flight files at `~/grm-automations/docs/composer-stage-ii-typography-source/`, proposed merge output.
  - Source directory includes `README.md` (Design-authored provenance and merge procedure), `typography-patterns.md`, `voiceMap.md`. Read the README before starting the merge.
  - Default tie-breakers (Design-specified): production wins on wording where Ron signed off on specific language; Design in-flight wins on structure (three-voice vs. two-voice, persona tables, new rules, new Phase 5/6 checks); production tokens that Design in-flight doesn't reference but downstream files depend on → preserve and document in revision log.
  - If a sentence in production contradicts a structural revision in Design in-flight (e.g., production says "two-voice system" and Design in-flight says "three-voice system") — do not silently resolve. Surface the conflict via Chat-Claude for Design's judgment. §12 Risk 1 names this explicitly.
  - Merged files land at `~/.claude/skills/prospect-site-design/references/typography.md` and `voiceMap.md`, replacing the Stage II (a) production copies.
  - Revision log entry appended to merged files: date, merge sources, conflict list resolved, Design reviewer signoff.

- **(e) Tier logic stripping:** Grep for `tier-premium|tier-professional|tier-standard|Premium tier|Professional tier|Standard tier` across SKILL.md, css-framework.md, content-rules.md, anti-slop-rules.md, section-patterns.md. Replace with persona-conditional logic where appropriate, remove where redundant. Absorb `ae9617a` (weight 300 spec) into this step — weight specs survive tier-collapse.

- **(f) P6.1 implementation spec:** Author `scripts/rendered_content_check.py` stub and integration spec with Phase 6. Playwright headless Chromium, initial-paint capture, per-section pixel analysis, two-threshold model from §6.

**Stage II gate to Stage III:** All reference files in place. Schemas authored and Design-reviewed. No tier logic remaining. Rule E6 + Phase 6 Check 18 intact post-backport (sentinel verification). Design confirmed typography/voiceMap merges landed cleanly. P6.1 spec authored.

**Stage II expected effort:** 6-8 hours of focused Claude Code work. Naturally splits into two sessions — Session 1: (a) + (b) + (e) ≈ 3-4 hours. Session 2: (c) + (d) + (f) ≈ 3-4 hours. Clean handoff between via COMPOSER_BRAIN.md Living section update.

**Stage II.5 — profile.json fixtures authored.** Hand-written profile.json fixtures covering: sparse photo library (0-3 hero candidates), populated library (8+), over-constraint (insufficient photos for layout minimum), high-review-count, low-content-depth, multi-vertical. Each fixture pairs with an expected composition-plan.json outcome. Feeds Stage III.

**Stage III — Phase 4-new implementation.** Code builds Phase 4-new reading profile-schema.md and composition-plan-schema.md. Reads profile.json. Produces composition-plan.json. Validated against Stage II.5 fixtures first, then Luna's actual profile.json. **Design review checkpoint 2 — Design reviews Phase 4-new output on 2-3 fixtures before Stage IV begins.**

**Stage III gate to Stage IV:** Phase 4-new produces expected composition plans for all Stage II.5 fixtures. Design approves composition plans on 2-3 samples. Luna's profile.json produces a sensible composition plan.

**Stage IV — Phase 5-new implementation.** Code builds Phase 5-new reading composition-plan-schema.md. Reads composition-plan.json + profile.json. Emits HTML/CSS/JS implementing only Design's rules. No v0.7 default HTML inheritance. Parallelizable with Stage III once Stage II (c) composition-plan-schema.md locks.

**Stage IV.5 — composition-plan.json fixtures for Phase 5-new unit tests.** Hand-written composition-plan.json files representing distinct editorial outcomes. Phase 5-new emits HTML against each; output verified. Sits between Stage IV build and Stage V integration.

**Stage IV gate to Stage V:** Phase 5-new emits HTML against Stage IV.5 fixtures cleanly. Phase 5.5 consumes schema content from composition-plan.json (not DOM) and produces valid schemas. All Phase 6 patches (P6.1-P6.4) running. Phase 5-new emits against Luna's composition plan + profile.json without errors.

**Stage V — Validation build.** Build Luna through Composer start-to-finish. Compare output against Luna F8. Stage V rubric in §10 hard-gates both pillars independently.

**Design review checkpoints 3 and 4:**
- Checkpoint 3 — Stage V Luna Composer render visual diagnosis. Same format as Luna v3/v4 diagnosis — slice-by-slice read, what's working, what's not, cross-reference against Luna F8 as baseline. Delivered as artifact, not inline chat.
- Checkpoint 4 — Stage V editorial-check suite soft-fail review. Design reviews P6.2 soft-fail list (if any) and confirms either (a) every soft-fail is a real deployment issue Phase 4/5 should fix, or (b) a specific soft-fail is a false positive and the check needs refinement.

**Stage VI — Retirement decision.** Based on Stage V and one additional flagship build (F9 or later, chosen for vertical/persona variety). Criteria in §11.

## 9. APPROVAL GATE UI (PHASE 4)

Chat-mediated gate. Phase 4's output rendered as structured text for Ron's review before Phase 5 generation begins.

Review surface includes:

- **Per-section layout selection** (A through E, or documented variant) with photo role assignments and thumbnails.
- **Voice-map zone assignments** per page and per section.
- **Per-page display-moment confirmation.** For each major page, show the display element (H1, watermark numeral, or pull quote) rendered at final scale with its role class labeled. Confirm/reject per page. Catches pages where Phase 4 forgot to promote a section to display-moment status.
- **Italic-word review per H1/H2.** Each headline rendered with italic word highlighted + persona word-class annotation (matches / expected class / banned-class warning if applicable). Per-headline confirm/edit/reject. Edit triggers schema-validation on the replacement word. Reject triggers Phase 4 LLM-call regeneration with feedback. When Phase 4 can confidently propose an alternative within the same H2, show both options as "pick or confirm" — Ron picks. When no alternative is confidently available, show single selection as "confirm or reject."
- **Eyebrow deployments per page** with section labels.
- **Signature micro-interaction placement.** Site-level selection (one signature across all pages).
- **Scale contrast targets** vs. persona minimum.

Implementation lands in Stage III as part of Phase 4-new. Manual review on every H1/H2 italic is Composer v1's approach. Automation (LLM call or heuristic matcher) is deferred to v0.7.3+ after several Composer builds, once we have data on whether manual review is a bottleneck.

## 10. STAGE V GO/NO-GO RUBRIC

Both pillars hard-gate independently. Failing any hard gate on either pillar = no ship. No retries on edge-case builds to paper over structural failures.

**PILLAR 1 HARD GATES (editorial):**

- Phase 6 P6.2 editorial suite passes all hard-fail checks (1, 2, 5, 6, 7, 8, 10, 11, 12, 13). Soft checks (3, 4, 9) within soft-fail budget.
- P6.1 rendered-content check passes at hard-fail threshold (no section below 5% painted-pixel ratio).
- Pattern rule: zero critical (hard) fails across P6.1 + P6.2.
- Pattern rule: at most 2 soft-fails across P6.1 soft + P6.2 soft.
- Luna Composer render requires zero build-level patches to match or exceed Luna F8 rendered quality.
- Design reviews the Composer render (Checkpoint 3) and confirms "this feels like us" at or above F8 baseline.
- Italic-word selection on Luna Composer matches Luna F8 within ±1 word per headline after Phase 4 human-review gate.
- Layout selection on Luna Composer matches Luna F8 in at least 4 of 5 major sections, or deliberately better.
- Pull-quote OR display-scale moment present on every major page (homepage, about, service sub-pages). At least one `.role-display-pullquote` OR `.role-display-watermark` OR H1/H2 rendering ≥80px desktop / ≥56px mobile per major page. This is the single biggest "editorial vs. templated" signal.

**PILLAR 2 HARD GATES (SEO/GEO):**

- All JSON-LD schemas validate cleanly. Google Rich Results Test passes for all schema types, zero parse errors.
- llms.txt generates from profile.json. Contains all required sections (# title, > summary, ## About, ## Services, ## Service Area, ## Contact, ## Credentials, ## Key Pages). All facts match profile.json. No invented facts. Organizational diff against Luna F8's llms.txt acceptable after reviewer accepts or rejects differences.
- Lighthouse SEO score ≥95.
- Meta tags / OG tags / canonical URLs validate.
- P6.4 schema-to-HTML consistency passes (zero DOM/schema drift).
- All six existing SEO/GEO Phase 6 checks pass: BLUF content, semantic HTML + internal linking, AI crawler access, llms.txt, structured data validation, meta tag verification.
- Font-loading fallback test: throttled network profile shows graceful fallback to `--font-body` when persona-conditional heading font delays beyond threshold.

## 11. STAGE VI RETIREMENT CRITERIA

All of:

- Composer passes Stage V cleanly on Luna (F8 baseline).
- Composer passes Stage V cleanly on at least one additional flagship build (F9 or later, chosen for vertical/persona variety).
- Zero skill-level patches required across both validation builds.
- Rollback path documented and tested: verified restore procedure for reverting from Composer back to production prospect-site within a single session.
- Ron, Code, Design all signoff on production readiness.

If criteria met: Composer becomes primary. Production either retires entirely or stays as stable fallback — decided at Stage VI with fresh evidence. If criteria not met: iterate specific gaps.

## 12. RISKS AND MITIGATIONS

**Risk 1 — Typography/voiceMap merge conflicts during Stage II (d) three-way diff.** Production's F5-era files + Wave 2 retrofits + Design's in-flight revision may have overlapping changes. Silent loss of Wave 2 Q3 revisions that Design didn't have visibility into.
*Mitigation:* Three-way diff procedure. Code surfaces conflict list before merge commit. Design reviews conflicts. README at `~/grm-automations/docs/composer-stage-ii-typography-source/README.md` documents the procedure for fresh windows.

**Risk 2 — Wave 2 backport conflicts with design-skill editorial content.** StatRow, SectionOpener, rhythm tokens touch css-framework.md and section-patterns.md — the files Design's editorial framework concentrates in.
*Mitigation:* Per-commit atomic cherry-pick. Failure mode isolated to one commit. Worst case: commit needs re-authoring.

**Risk 3 — Rule E6 + Phase 6 Check 18 (color-derivation hardening, commit d7ba115) lost during backport.** Design-skill has these; production doesn't.
*Mitigation:* Sentinel-check both intact at Stage II completion. Phase 6 runs Check 18 as smoke test through all remaining stages.

**Risk 4 — Hard Rules #11 / #12 from production's handoff-discipline.md may not apply to Composer process model.**
*Mitigation:* File copy, then review during Stage II. Keep / adapt / retire decision made before Stage III.

**Risk 5 — Composer's composition-plan.json schema gets the contract wrong and Phase 5-new can't implement a real build cleanly.**
*Mitigation:* Stage II.5 fixtures catch this before Stage III. Design reviews schema before fixtures authored (Checkpoint 1). Iterate if schema incomplete.

**Risk 6 — Stage V exposes framework-transfer issues the inventory didn't predict.**
*Mitigation:* Stage VI retirement criteria require two clean builds, not one. If Luna passes but F9 fails, iterate.

**Risk 7 — Phase 6 quality-coverage gap widens with each editorial theory addition.** Observed in Luna F8: 18 checks passed, Design found 5 material issues by eye. If Phase 6 doesn't add editorial-rule checks proportional to new editorial rules, verification lags quality.
*Mitigation:* P6.2 suite of 13 checks. Stage VI aspirational criterion — "Composer's Phase 6 catches ≥80% of issues Design flags by eye on a live build." Measurable, iterable.

## 13. OPERATIONAL PRINCIPLES

- Anyone (Ron, Chat-Claude, Code-Claude, Design) can call a break if focus or context is slipping. Not a failure — the check that prevents mistakes.
- Handoff between windows goes through COMPOSER_BRAIN.md (this file). No separate per-session handoff `.docx` files for Composer work.
- Code's permanent memory keeps it continuous across Claude Code windows. This file keeps Chat-Claude and Ron continuous across chat windows. Design is available for architectural and editorial questions directly from any window.
- No rushing to close stages because a session is ending. Stage II taking two sessions is better than Stage II ending with half-tested output.
- Vocabulary discipline: "Composer" or "v0.8 Composer" only. Never bare "v0.8" (ambiguous with v0.8 Scale (deferred)). When referring to skills, say "design-skill," "production," or "Composer target skill" explicitly. Never "the skill."
- Commit message convention: prefix `composer:` on all Stage II-VI commits. Examples: `composer: stage II.b — cherry-pick SectionOpener primitive from production 593173e`. Searchable later.
- Branch convention in grm-automations: direct-to-main with `composer:` prefix on all Stage II-VI commits. No topic branches. Every Composer commit lands on `main` as an atomic stage-prefixed commit. Matches the repo's established convention — all Wave 1 / Wave 2 commits and all Stage I commits landed directly on main. Rationale: solo linear pipeline, low blast radius (Composer work lives in its own skill directory and docs/composer/), and the `composer:` prefix already provides searchable stage-scoped history. Stage II (d) typography three-way merge does not get a carve-out — Design review happens in chat against conflict lists, not via git diff.

## 14. SCHEMA VERSIONING APPROACH

Top-level `$schemaVersion` JSON key in every profile.json and composition-plan.json:

```json
{
  "$schemaVersion": "1.0",
  "$schema": "composition-plan",
  "businessSlug": "luna-master-painting",
  ...
}
```

Format: `major.minor`. Major = breaking changes that invalidate prior plans. Minor = additive. Composer ships at 1.0 for both schemas. Version registry lives at `~/grm-automations/docs/composer/schema-versions.md`, seeded in Stage II (c).

`-schema.md` reference files declare which schema version they describe in their frontmatter: `schemaVersion: 1.0`. Stage III Phase 4-new and Stage IV Phase 5-new hard-error if their input JSON's `$schemaVersion` doesn't match what the `-schema.md` declares.

## 15. FILE PATH REGISTRY

- Composer brain file (this document): `~/grm-automations/docs/composer/COMPOSER_BRAIN.md`
- Foundation skill: `~/.claude/skills/prospect-site-design/`
- Production skill (read-only during Composer dev): `~/.claude/skills/prospect-site/`
- Composer target skill (new, created in Stage II): `~/.claude/skills/prospect-site-composer/` symlinked from `~/grm-automations/skills-experimental/prospect-site-composer/`
- Design typography source directory: `~/grm-automations/docs/composer-stage-ii-typography-source/` (contains README.md, typography-patterns.md, voiceMap.md — pending extraction from `/mnt/user-data/uploads/Get_Rooted_Media_Design_System_copy.zip` in first Stage II session)
- Stage II.5 profile fixtures: `~/grm-automations/docs/composer/fixtures/profile/`
- Stage IV.5 composition-plan fixtures: `~/grm-automations/docs/composer/fixtures/composition-plan/`
- Schema version registry: `~/grm-automations/docs/composer/schema-versions.md`
- Luna F8 build repo: `~/grm-sites-prospects/luna-master-painting/`
- Luna F8 deployment (Stage V baseline): `https://luna-master-painting-grm.vercel.app/`
- Execution log (rolling, one-line per session action): `~/grm-automations/docs/composer/execution-log.md`
- Handoff docs (pre-Composer, for other work): `~/grm-automations/docs/handoffs/`

## 16. WHAT PERMANENT MEMORY HOLDS VS. WHAT THIS FILE ADDS

**Code's permanent memory already holds:** skill file paths, GRM brand facts, flagship roster (F1-F8 including Luna as F8), voice mapping conventions, anti-slop rules, Luna F8 existence and build-level patch inventory, Design and Chat-Claude working relationship, Wave 1/Wave 2 commit details in production.

**This file adds on top of memory:** Composer scope lock decisions, Composer-specific file paths (brain file, target skill, typography source, fixtures, logs), stage-by-stage progress (what's completed, what's next, what's blocked), schema version registry state, branch and commit conventions, Stage V/VI rubrics, Design's four review checkpoints scheduled, session-close update blocks in the Living section.

Fresh Claude Code windows read this file first. Fresh chat windows (Chat-Claude facing Ron) read this file first. Design's reviews reference this file by section number.

## 17. FORMAL REVISION PROCEDURE

This Fixed section (PART I) changes only through formal revision:

1. Revision proposal written in the Living section (PART II) below, with rationale.
2. Chat-Claude + Ron discuss. Code consulted if architectural. Design consulted if editorial.
3. If agreed, Code edits PART I and appends a revision log entry at the bottom of this file.
4. PART II gets a session-close block noting the revision.

Minor revisions during execution (file paths changing, typos) can happen via direct Code edit with a Living-section note. Substantive revisions (scope, gates, foundation) follow the full procedure.

Revision log:
- v1.0 — 2026-04-21 — Initial Composer spec lock. Author: Chat-Claude. Reviewers: Code-Claude (signoff with 8 flags absorbed), Claude Design (signoff with 13-check Phase 6 suite + 4 checkpoints absorbed). Approver: Ron Kolb.

---
---

# PART II — LIVING (session state)

Newest session block at the top. Older blocks scroll down.

---

## Session block — 2026-04-21 (morning)

**Window type:** Claude Code executing per Chat-Claude relay. Chat-Claude (fresh window) directing; Ron routing.

**Action:** Minor revision to §13 branch convention per §17. Dropped proposal for `composer/stage-ii` through `composer/stage-vi` topic branches in favor of direct-to-main + `composer:` prefix. Matches actual repo convention (verified: only branch in grm-automations is `main`; all prior Composer commits landed on main directly). "Deferred decisions" bullet in 2026-04-21 block updated to RESOLVED. Ron + Chat-Claude + Code signoff.

**What's next:** Create prospect-site-composer target skill directory (original item #3 of Stage II kickoff). Chat-Claude drafting paste-ready prompt after this commit lands.

---

## Session block — 2026-04-21 (late afternoon / evening)

**Window type:** Chat-Claude (facing Ron). Author of this brain file.

**Session arc:**
- Started with Luna F8 post-build work. Closed Luna F8 logo fix via c1 fallback (icon+span pattern per Chad's flagship, mobile promo overlap fixed).
- Captured Luna as Flagship 8 in `project_deployment.md` via Code.
- Ron asked whether the additive-patches path was right or whether a structural rebuild was called for.
- Asked Code for architectural review. Code returned substantive pushback: "editorial variant is a prototype of what v0.8 could actually be if the two vocabularies are reconciled." Raised v0.7.2 bundling concern, v0.8 identity crisis, Phase 6 coverage gap.
- Scoped Composer as the v0.8 reconciliation effort. Wrote first-pass spec.
- Ron corrected framing on "two site generators" — Code had been looking at the wrong candidate for foundation comparison. Re-asked Code with explicit framing of both skills as candidates.
- Code returned symmetric evaluation, reversed own recommendation to design-skill as foundation with Wave 1/Wave 2 backport.
- Asked Design the typography reconciliation question. Design confirmed revision path for both typography-patterns.md and voiceMap.md.
- Finalized Composer spec incorporating Code's 8 flags (schema versioning clarification, llms.txt gate language, Design source file disk location, Composer skill install path, cherry-pick addition `1ca3bd5`, P6.1 implementation spec, P6.1 two-threshold split, Stage IV.5 rename) + PA.5 font-loading fallback.
- Design signoff with 9 → 13 Phase 6 check suite, pull-quote OR display-scale moment per-page hard gate, approval-gate UI additions (per-page display-moment confirmation, italic-word pick-or-confirm), photo role scarcity behavior, voicesInUse field, site-level signature field.
- Design delivered typography package as zip (`/mnt/user-data/uploads/Get_Rooted_Media_Design_System_copy.zip`) with three files: README.md (provenance + merge procedure), typography-patterns.md (390 lines, 13 Phase 6 checks), voiceMap.md (244 lines, three-voice contractor subset of six-voice GRM library).
- Ron shared the Storefront landing page (https://getrootedmedia.com/the-storefront) as typographic reference — what Composer's output should aspire toward. Chat-Claude absorbed as internal calibration; no spec change.

**What changed:**
- Luna F8 committed to flagship roster.
- Composer scope locked (this document, PART I above).
- Design's typography package delivered in a zip file.
- Code, Design, Ron all signed off on Stage I.

**What's in-flight:**
- Nothing. Stage I complete.

**Stage I close-out (completed in this session):**
1. ✅ Extract Design's typography package. Source zip at `/mnt/user-data/uploads/Get_Rooted_Media_Design_System_copy.zip` extracted to `~/grm-automations/docs/composer-stage-ii-typography-source/`. All three files (README.md, typography-patterns.md, voiceMap.md) verified byte-identical to zip inventory and to README's stated inventory. Commit `463cac4`.
2. ✅ Commit brain file. Path `~/grm-automations/docs/composer/COMPOSER_BRAIN.md`. Commit `0bc429b`.
3. ✅ Initialize execution log at `~/grm-automations/docs/composer/execution-log.md`. Two Stage II-prep entries present. Commit `6c645a1`.

**Stage II opening work (for fresh session):**
1. Create Composer target skill directory at `~/grm-automations/skills-experimental/prospect-site-composer/`. Copy design-skill (`~/.claude/skills/prospect-site-design/`) as starting point. Symlink to `~/.claude/skills/prospect-site-composer/`. Register slash command if possible at this stage, or document for later.
2. Stage II (a) file copies begin: four files from production `~/.claude/skills/prospect-site/references/` into Composer target skill's `references/` directory — typography.md, voiceMap.md, LESSONS.md, handoff-discipline.md.
3. Continue with Stage II (b) cherry-picks, (c) schema authoring, (d) typography merge, (e) tier logic stripping, (f) P6.1 spec per COMPOSER_BRAIN.md §8.

**Checkpoint 1 trigger:** When Stage II (a)-(c) wrap, Chat-Claude pings Design with composition-plan-schema.md for review before Stage II.5 fixtures begin.

**Design's standby posture:** Ready for Checkpoint 1 whenever Stage II (a)-(c) wrap. No rush.

**Open questions / deferred decisions:**
- Commit message for brain file initial commit: use convention above (`composer: stage I — lock scope and initialize brain file`).
- Branch for Composer work: RESOLVED 2026-04-21 Stage II session 1. Direct-to-main with `composer:` prefix, no topic branches. See §13.
- Hard Rules #11/#12 from handoff-discipline.md: review for Composer applicability in Stage II (a).

**Known traps:**
- Framework-transfer risk: we explicitly bought this when choosing design-skill as foundation. Watch at Stage V for layout-primitive seams (SectionOpener, StatRow backported into design-skill's section-patterns.md may not compose cleanly with Layout A-E primitives).
- Phase 6 quality-coverage gap: P6.2 suite is 13 checks now, but Design has shown the framework produces editorial outputs that are hard to verify automatically. Checkpoint 4 exists specifically to surface this.
- Stage II (d) tie-breaker interpretation: "production wins on wording Ron signed off on" is fuzzy without knowing what Ron signed off on. If unclear whether Ron signed off, default to surfacing the conflict rather than resolving silently.

**Acknowledgments:** Ron carried the CTO load all day, including the corrections that made the spec right (foundation comparison, two-pillar framing, typography-first goal). Code delivered two rounds of architectural review with real pushback. Design delivered the typography package plus running visual diagnosis on Luna F8 plus four-checkpoint review plan. All three parties signed off cleanly.

---

*End of Living section. Older session blocks would appear below this line as they accumulate.*

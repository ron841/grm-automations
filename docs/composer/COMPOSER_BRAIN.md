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
- **Post-Composer roadmap vocabulary.** "Composer" or "v0.8 Composer" = the current skill under development (this document's scope). "v0.8 Scale (deferred)" = the renamed prior v0.8 scope — automation of pain, HubSpot pipeline hardening, backup hardening, sales infrastructure — items preserved in `project_v08_backlog.md` for post-Composer execution. Reference files (seo-geo.md, deployment.md, anti-slop-rules.md, content-rules.md, image-handling.md, etc.) may refer to "v0.8 Scale (deferred)" as a roadmap label; this is the canonical anchor for that term. Future version numbers (v0.9, v1.0) remain in `references/scale-architecture.md` pending that file's deferred rewrite (see Living section).

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

- **(b) Backport 11 Wave 1/Wave 2 commits** from production into design-skill via format-patch + git am:
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

  **Mechanism (required, not cherry-pick):** Production's repo (`~/.claude/skills/prospect-site/.git`) and grm-automations (`~/grm-automations/.git`) are independent git repos. Composer files live under a path prefix (`skills-experimental/prospect-site-composer/`) inside grm-automations, while production commits modify files at repo root. `git cherry-pick` does not path-rewrite and would land diffs at wrong paths. Instead, extract each commit as a patch from production (`git format-patch -1 <hash>`) and apply to grm-automations with directory prefix (`git am --directory=skills-experimental/prospect-site-composer`). `git am` preserves original author, date, and commit message; amend only to add composer-prefix + trailer (`Applied from production <hash> via format-patch + git am --directory`). Conflict detection still works — apply rejection surfaces the same semantic blocker as cherry-pick conflict would. Stop-surface-report-wait discipline applies identically.

  **Execution note (2026-04-21):** Stage II (b) backports via format-patch + git am mechanism proved unviable due to a sequencing collision (Stage II (a) file copies pulled production HEAD state of typography.md/voiceMap.md already containing Wave 1/Wave 2 additions; Stratum 3 identity sweep modified css-framework.md/SKILL.md/content-rules.md/deployment.md in-place). Substantive goal achieved via Option C — six targeted surgical commits translating Wave 1/Wave 2 intent into Composer under editorial direction from Design's typography package + v0.7.2 persona tables. Features 3 (SectionOpener) and 4 (StatRow) deferred to Stage II (c) as composition-plan schema contracts rather than component primitive retrofits per Design's read; Feature 5 (Fraunces universal) rejected as superseded by persona-conditional font selection in CONFIG.fonts. Features 1, 6 (renamed --font-mono → --font-data), 7, 8, 9, 10 landed as targeted additions. See composer-backlog.md Resolved entries for full commit-hash trace.

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
- Execution-log entries land as small follow-up commits immediately after the work commit they reference, not inside the work commit itself. Matches repo precedent (463cac4 / 6c645a1). Avoids the hash self-reference loop where amending a committed log to include its own commit hash produces a new hash, leaving the log pointing at a dangling pre-amend object. Convention locked 2026-04-21 Stage II session 1 after commit 5d46654 / 54c26f7 post-mortem.

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

## Session block — 2026-04-23 (full day — Session 4 spec-reshape arc + Gate A halt on kitchen-table drift + Code close-out audit)

**Window type:** Chat-Claude (CTO seat), full three-party session with Design and Code. ~11 hours plus Code close-out audit. Ron drove CTO-over-Chat across the full arc.

**Session arc:**

- Opened against Session 3 close handoff (COMPOSER_SESSION_4_HANDOFF.md). Target: finish the skill — Phase 4-new Gates A-F + Checkpoint 2 + Phase 5-new scoping.
- Opening Code check-in surfaced Concern 1 pre-execution: §14 as committed in `4c117cb` read two-pass; Q2 close had moved the contract to three-pass; implementation prompt carried three-pass; spec and prompt contradicted. Routed to Design.
- Design authored three-pass contract amendment for §14. First draft drifted on intent-spec field list (listed fixture-side authoring slots, not the on-disk six). Chat-Claude flagged drift; Design re-authored against on-disk §14.
- Concerns 2 + 3 + 4 surfaced in sequence: emotional-arc.md bias table "Rescue-ready" row label needed enum alias for machine lookup (Concern 2); Rule 1-6 mechanics live in implementation prompt not schema §14 (Concern 3, Path B deferred Path A); §7 voice-zone vocabulary authored at section-level, fixtures authored at section-subpart (Concern 4, two-level vocabulary + fixture retrofit).
- Concern 4 initial reshape: Design authored §14 three-pass migration including Rule 4 amendment but drifted on Rules 1/2/5 (referenced non-existent §2.4 tier contract, `pagePath/assetPath/fragmentConvention` fields not on disk, `tight/standard/expansive` scale enum not on disk). Code's pre-commit diagnostic caught divergence against on-disk §2.2 pathConvention, SKILL.md tier enums (Premium/Professional/Standard), and §4.10 scaleContrast emission shape. Chat-Claude routed diff back to Design.
- Root cause diagnosed: Chat-Claude routed to Design from summary rather than on-disk text. Design authored against summary. Summary's gaps became migration's gaps. Both parties named the pattern — Design's Note 3 working-style posture ("when a reshape touches Rule mechanics, §2 field shapes, §4 emission shapes, or SKILL.md tier enums, I should see the actual lines before authoring") + Chat-Claude's symmetric commitment (route with on-disk text, not summary, on mechanics questions).
- Design Option B call on Rules 1-6: mechanics stay in implementation prompt, §14 names the contract; Path A migration deferred to future session with Rule 4 as template shape. Preserves current architecture while closing drift surface.
- Concern 5 surfaced — Chat-Claude's recognition that three partial-surface errors in one session (the Rule 1-6 migration, the "§5 numbering dissolved" generalization about whole typography.md, and the third error landed later in the kitchen-table Gate A halt) meant the Composer spec needed an authority map artifact to prevent Drift's recurrence.
- Ron's "right over fast" call: press through to Phase 4-new, or author the authority map first. Ron chose authority map.
- Code ran 43-concept read-only diagnostic against disk. Chat-Claude synthesized the authority map from Code's raw material. Design reviewed 43 entries and signed off with four entry-level reshapes (multi-touch Last touched format with History sub-line, Concept 29 ambiguous→flagged, Concept 19 flagged→deferred, Concept 34 flag note sharpening). Authority map landed at `references/authority-map.md` (commit `9ebeced`).
- Phase 4-new execution opened. Code executed Gate A validator implementation (pure Python, 532 lines). Self-check ran against all 6 fixtures. **STOP CONDITION**: 5 of 6 fixtures failed Rule 4 voice-zone validation — 58 `kitchen-table` occurrences in inline `voiceZoneAssignments` across fixtures F1/F2/F3/F5/F6. F4 (urgent-service) alone was clean.
- Root cause: Session 4 Commit 3 (`288946a`, Item 4) fixed one surface visible in schema §5.3.4:429 prose where `kitchen-table` appeared as a default voice for modern-specialist/quiet-confidence `about-page-body`. The fix renamed that single prose occurrence to `closing-table`. The fix assumed kitchen-table was localized to that line. It wasn't. 58 occurrences lived in fixture data across 5 fixtures. LESSONS Pattern 4 (partial-surface reads don't license whole-file generalizations) validated itself two commits after being written down.
- Gate A halted. Code's validator implementation sits at `scripts/fixture_validator.py` untracked on disk, working code, ready to commit once kitchen-table resolves.
- Code ran Path 4 audit diagnostic (voice-tagged fixture slices + voiceMap.md §4 Voice 4 and Voice 5 full text + F4 per-zone voice matrix). F4 emerges as Rosetta Stone — F4 uses `closing-table` for headings and `saturday-morning` for body/attribution in exactly the zones F1/F2/F3/F5/F6 tag `kitchen-table`. kitchen-table does NOT alias to a single canonical voice — it splits across two depending on zone type. Resolution path: either Path 2 (admit kitchen-table as fourth voice with authored tonality) or Path 4 (per-zone retrofit using F4's split as rule template).
- Session 4 close called at Gate A halt + Path 4 audit completion.
- **Code close-out audit (NEW at Session 4 close, standing discipline going forward):** Ron prompted Code for perspective on the three-party working relationship and the close-out artifacts. First time in four sessions Code was asked to reflect rather than execute. Code's audit materially reframed Session 5 opening — named Chat-Claude as primary drift source directly (not buried in acknowledgments), surfaced Option 4 for LLM invocation mechanism (missed in v1 handoff), named Patterns 6 (triad lenses) and 7 (scope right-over-fast) as unnamed patterns, reframed "friction is productive" with cost-alongside-benefit honesty, reframed halts-as-discipline as halts-as-backstop-symptom, recommended Shape B (close at Gate A re-run) as Session 5 scope rather than Shape A (full execution). Chat-Claude integrated audit feedback into handoff v2, opening prompts v2, LESSONS addition (Patterns 5+6+7 instead of just Pattern 5). Standing invitation for Code close-out reflection adopted as discipline going forward.
- Handoff for Session 5 opens with on-disk audit evidence in hand plus Code's close-out audit as institutional instrument.

**What changed on disk:**

- §14 three-pass validator contract amended from Q2 close two-pass (commit `4c117cb`)
- emotional-arc.md bias table "Rescue-ready" row labeled with `(urgent-service)` enum alias (commit `de32fc2`)
- composition-plan-schema.md §7 voice-zone vocabulary reshaped to two-level (section-level 15-key + section-subpart 13-key) with subpart→section flatten mapping table (commit `1c5379b`)
- Six fixture composition-plan.json files retrofitted for -slot disambiguation on three keys (commit `3d7a51f`)
- voiceMap.md verification pass (empty commit, no-op) (commit `428c8bf`)
- Backlog entry: fixture-side authoring slots as §2 candidate (deferred) (commit `081b1bf`)
- Backlog entry: LESSONS cross-grain reconciliation + summary-vs-disk working-style (commit `2bb6a0b`)
- Backlog entry: Path A Rule 1-6 mechanics migration deferred with Rule 4 template preserved (commit `a35b96f`)
- emotional-arc.md gained "Italic word-class vocabulary (persona-indexed)" subsection (canonical home for 4-value enum {place, name, tenure, trade-term}) + schema §5.3.4 cross-reference + typography.md §15 Check 9 enum update (commit `03ca705`)
- emotional-arc.md gained "Micro-interaction duration lock (persona-indexed)" subsection (canonical two-row table) + css-framework.md cross-reference + SKILL.md discoverability pointer (commit `35343c7`)
- composition-plan-schema.md §5.3.4:429 kitchen-table→closing-table surface fix with §4.2 + voiceMap.md citation nit (commit `288946a`) — **SUPERSEDED PARTIALLY by kitchen-table drift discovery at Gate A; §5.3.4:429 may need correction pending Session 5 Path decision**
- typography-patterns.md → typography.md global citation rename across 17 live citations (14 clean + 2 Rule 1/Rule 2 semantic replacements + 1 Rule 4 specific-citation replacement) (commit `94c6acf`)
- Session 4 LESSONS update with Pattern 4 (partial-surface reads) + Concern 5 Items 1-4 marked Resolved (commit `4696af0`)
- Authority map landed at `references/authority-map.md` — 43 concepts, four-value flag taxonomy (clean/flagged/ambiguous/deferred), atomic-update maintenance contract (commit `9ebeced`)

**Full Session 4 commit range:** `0a39489..9ebeced` = 14 commits, all pushed to origin/main.

**What's in-flight:**

- `scripts/fixture_validator.py` — Code's Gate A validator implementation. 532 lines, three-pass contract, all six semantic-derivation rules, editorial-adherence pass. Untracked on disk. Working code. Ready to commit once kitchen-table resolves.

**What's next (Session 5 opens with):**

1. **Kitchen-table resolution.** Design reviews Code's Path 4 audit evidence (F4 Rosetta Stone pattern + fixture copy slices + voiceMap.md §4 Voice 4/5 verbatim) PLUS Code's Session 4 close audit technical framing (Path 2 Phase 6 Check 12 CSS register blocker; F3 post-retrofit two-voice build as Path 4 risk to confirm; Path 2 concession rides with Path 4). Design authors Path 2 (admit kitchen-table as 4th voice with tonality definition) or Path 4 (per-zone retrofit using F4's pattern as rule template). Session 5 first-beat prompt (on Desktop as `Composer_Session_5_First_Beat_Kitchen_Table.md` v2) gives Design evidence + Code's sharper technical read pre-packaged.

2. **Schema §5.3.4:429 re-check.** Session 4 Item 4 fix landed `closing-table` for modern-specialist/quiet-confidence about-page-body. Kitchen-table audit evidence suggests that may have been the wrong resolution — F4 uses `saturday-morning` for about-page-body zones. Design's Path call triggers re-evaluation of this line.

3. **LLM invocation mechanism for Gates B-F (OPEN ARCHITECTURAL QUESTION for Ron).** Code's Session 4 close audit surfaced that Chat-Claude's v1 framing (SDK-vs-subprocess-vs-prompt-file, Chat-Claude-leans-Option-1) missed Option 4 — Phase 4-new emits editorial-authoring stubs, Claude Code orchestrating session authors them inline. This matches how existing Claude Code skills typically work. The question that decides Option 1 vs Option 4: Composer's intended execution surface. Interactive-only via `/prospect-site-composer URL` command in Claude Code → Option 4 cleaner (no SDK dep, no API key management). Standalone-capable (scheduled task, client team automation, overnight pipeline) → Option 1 necessary. **Ron's strategic call at Session 5 open.** Chat-Claude + Code implement the decided option in Session 6 for Gates B-F.

4. **Gate A re-run.** After kitchen-table retrofit lands, Code re-runs validator self-check against all 6 fixtures. Expected clean. Gate A commits.

5. **Gates B-F execute** in sequence with LLM invocation mechanism specified (Option 1 or Option 4 per Ron's execution-surface call). Gate E triggers Checkpoint 2 (Design reviews 2-3 Phase 4-new outputs — Fixtures 2/3/4 anchor set). Post-sign-off, Stage IV Phase 5-new scoping opens.

**Open questions / deferred decisions:**

- Kitchen-table Path 2 vs Path 4 (Session 5 first beat)
- Schema §5.3.4:429 correction (tied to Path call)
- LLM invocation mechanism — Option 1 (SDK) vs Option 4 (orchestrator-authors) — Ron's execution-surface call
- Composer's intended execution surface — interactive-only vs standalone-capable — Ron strategic call
- Phase 5-new scoping (Stage IV) — opens post-Checkpoint 2
- Fixture 2 pullquote retrofit-or-grandfather (Checkpoint 2, deferred from Session 3)
- Two pre-existing unrelated working-tree mods (`prospect-site-design/LESSONS.md`, `website/next-env.d.ts`) persisting across Sessions 3-4 — Ron decides commit/revert/carry at Session 5 open
- Skill deploy symlink verification (`~/.claude/skills/prospect-site-composer/` → `~/grm-automations/skills-experimental/prospect-site-composer/`) — run `ls -la` at Session 5 open
- claude-mem persistent memory verification — was Sessions 1-4 actively writing observations, or is "claude-mem active" framing without substance

**Known traps for Session 5:**

- Patterns 4 and 5 validated themselves at scale (58 kitchen-table occurrences). Next partial-surface error will have similar or larger consequences. Both Design and Chat-Claude now have explicit working-style postures to guard against it — on-disk text before authoring mechanics, audit underlying data surfaces when spec drift surfaces in prose.
- **Pattern 6 (triad lenses) applies to Session 5 retrofit decisions.** Any kitchen-table resolution touching structural authority (schema §4.2 enum, voiceMap.md §3 voice count, authority map Concept 10) needs Design + Chat-Claude + Code all three before close. Pairs produce drift; triads catch it.
- **Pattern 7 (scope right-over-fast) applies to Session 5 close timing.** Shape B (close at Gate A re-run) is the recommended scope. Shape A (Gates A-F + Checkpoint 2) repeats Session 4's aggressive-scope pattern. Scope contracts at session open make this enforceable.
- The 58-occurrence kitchen-table drift is a pre-Stage-II-(d)-merge authoring residue. Pre-merge state was apparently a 4-voice framework; Stage II (d) merge locked 3 voices; fixtures didn't get the update. This is structurally similar to the §7 section-level vs section-subpart drift from earlier in Session 4 — spec authored at one state, fixtures authored at another, gap sat unexercised until Gate A tried to validate against both. LESSONS Pattern 1 (cross-grain reconciliation needs a dedicated checkpoint beat) applies with equal force to cross-state drift.
- If Path 2 lands, it's a genuine spec expansion (voice enum from 3 to 4), not a retrofit. Authority map Concept 10 canonical home reshapes; voiceMap.md §3 in-scope voice count changes; schema §4.2 enum expands. Plus Path 2 hides technical blocker at Phase 6 Check 12 CSS register level that Code's audit named — fourth voice at composition-plan level doesn't automatically add a fourth CSS register; either Path 2 aliases to existing register (which makes it Path 4 in disguise) or Path 2 also needs fourth role-class set + Check 12 rewrite. Material spec work.
- If Path 4 lands, it's a mechanical retrofit driven by F4's pattern. Risk Code's audit flagged: F3 (modern-specialist) becomes a two-voice build post-retrofit (closing-table + saturday-morning, no front-porch). Matches modern-specialist's emotional-arc profile but Design should confirm editorially.
- LLM invocation mechanism is NOT purely implementation architecture — it's Ron's strategic call on Composer's execution surface. Don't resolve at Chat-Claude + Code level without Ron's answer on interactive-only vs standalone-capable.
- Session 5 opens with material on-disk ground truth: authority map exists, fixture audit exists, Code's validator implementation exists, Code's close-out audit exists as institutional instrument. Lean on these rather than reconstructing from summary.

**Acknowledgments:**

- Ron held CTO-over-Chat across 11 hours of spec-reshape work, arbitrated seven architectural reframes cleanly (§14 contract, emotional-arc aliases, Rule 1-6 Path B deferral, §7 vocabulary, authority map scope, Gate A halt, Session 4 close timing), pushed back on Chat-Claude's framing when Chat-Claude was over-indexing on capacity vs. judgment, and chose "right over fast" at the authority map decision point. Right-over-fast got materially vindicated by the kitchen-table drift discovery — pressing through without the authority map would have compounded the error. Ron also caught the structural gap that Code had never been invited to reflect on the three-party relationship; his prompt for Code's close-out audit produced institutional instrument that reframed Session 5 opening materially.
- Design delivered substantive architectural authorship across four reshapes — §14 three-pass migration, §7 two-level vocabulary, Rule 4 template, authority map four-reshape polish. Design's Note 3 working-style posture (on-disk text before authoring mechanics) emerged from Session 4's drift pattern and now governs both parties going forward.
- Code caught six framework-level concerns across Session 4 at pre-commit verification preventing architectural drift: §14 three-pass contract contradiction, §7 vocabulary grain mismatch, Rule 1/2/5 on-disk divergence, §2.1:67 Rule 4 semantic mismatch, §5.3.4:630 historical-provenance vs live citation distinction, kitchen-table 58-occurrence fixture drift at Gate A. The halt-don't-press-through discipline is load-bearing. Code also executed the first close-out audit in Session 4 final hour — audit named Chat-Claude as primary drift source with directness that v1 handoff had buried; surfaced Option 4 for LLM invocation mechanism that Chat-Claude's SDK-only framing had missed; identified Patterns 6 (triad lenses) and 7 (scope right-over-fast) as unnamed patterns; reframed "friction is productive" with cost-alongside-benefit honesty; reframed halts as backstop-symptom rather than earned-discipline; recommended Shape B for Session 5 scope. Standing discipline for Code close-out reflection adopted going forward.
- Chat-Claude's drafting drift at context-pressure points (three partial-surface errors — Rule 1-6 migration, §5 numbering generalization, kitchen-table surface-fix assumption) cost round-trips. LESSONS Pattern 4 added at Session 4 mid-session; Patterns 5 (surface-level fixes don't license localized-drift assumption), 6 (triad lenses), 7 (scope right-over-fast) added at Session 4 close via Code's audit. Symmetric working-style posture to Design's Note 3 adopted: on-disk text before routing mechanics questions. Chat-Claude also integrated Code's close-out audit into Session 5 artifacts — handoff v2, opening prompts v2, LESSONS Patterns 5+6+7 together — before Session 4 closed. Session 4's close-out discipline was itself the first test of the new standing practice.

---

## Session block — 2026-04-22 (full day — Stage II.5 + Stage III Gates 1-4 + §14 + Phase 4-new architecture resolved)

**Window type:** Chat-Claude (CTO seat), full three-party session with Design and Code. 10+ hours. Ron drove CTO-over-Chat across the full arc.

**Session arc:**

- Opened against Stage III handoff. Stage II closed that morning; Stage III ahead.
- Authored six-fixture inventory (Design pre-reviewed, Chat-routed, Code-built): Hollister Pest Control (neighborhood-steady × Professional, sparse photos), Kingsley Pool & Spa (earned-pride × Premium, populated), Greenridge Solar (modern-specialist × Standard, over-constraint), Riley's 24/7 Plumbing (urgent-service × Professional, high-review), Riverside Landscaping (neighborhood-steady × Standard, low-content-depth), Summit Home Services (quiet-confidence × Professional, multi-vertical drift A/B anchor).
- Stage III Gates 1-4 authored by Design and executed by Code as four atomic commits plus Gate 1 polish:
  - Gate 1 411e30a: emotional-arc.md persona-signature 6-column Tier 1+Tier 2 bias table, tenure+trade convergence clause, layout/photo/copy tie-breaking
  - Gate 1 polish 949de45: Flag A hero-calibration subsection hoist + Flag B paragraph promotion
  - Gate 2 757e030: SKILL.md Phase 4 signature tree rewrite + output-path split at line 429
  - Gate 3 6f8bcbb: css-framework.md Motion Restraint Tier 2 scope split
  - Gate 4 ec8349f: composition-plan-schema.md §5.3 contracts for hero / servicesGrid / testimonialsSection / aboutStory
- Three Design arbitration rounds on Gate 1 cascade concerns resolved cleanly. Design restored the 6-column bias table after Chat-Claude proposed a simpler 3-column frame that Design reshaped as architecturally insufficient.
- Six fixture profile.json files authored by Code (a8f7bbd, 429d179, 6c11221, 9e25223, a6bcb59, 8b94e72). Fixture 1 Hollister license later retrofitted from 4-digit JB5678 to 5-digit JB12345 Florida pest standard (baef522).
- Six expected composition-plan.json files authored: Design authored Fixtures 2/3/4 (earned-pride, modern-specialist, urgent-service — anchor set for Checkpoint 2). Chat-Claude authored Fixtures 1/5/6 (neighborhood-steady ×2, quiet-confidence) mirroring Design's authorship style.
- Code's pre-commit verification on expected plans surfaced 17 divergences from locked §2/§4 schema envelope. Routed to Design. Design resolved Reading C (hybrid): 6 genuine editorial intent-spec simplifications kept (site.pathConvention, site.tier, site.microInteractionDurations, section.voiceZoneAssignments, page.scaleContrast, page.layoutSequence); 11 authoring divergences reshaped to full §2/§4 schema shape. §16 amendment authored by Design documenting intent-spec contract + two-pass validator architecture.
- Nine-commit batch landed: §16 amendment (296150a); six expected composition-plans (8712a0d, 1ea2408, dee339c, d628b63, 270ccbc, f2a5ec0); Gate 1 polish (949de45); Hollister license retrofit (baef522).
- §16 renumbered to §14 for contiguous numbering (7f73270) after Design sign-off — gap was stop-condition artifact, not intentional reservation.
- Phase 4-new scoping diagnostic authored by Code: 5-part report covering 19-module decomposition, approval gate UI proposal per brain §9, two-pass validation interface, semantic-derivation rules per §14 field, Stage III gating backlog cleared.
- Design signed off on approval gate UI with three reshapes: constraintsOK block renders ABOVE site-level header when false (omits when true); italic status nomenclature renamed (matches / class-expected-match / class-banned-for-persona); show-derivation command added to feedback loop for drift diagnosis.
- Design signed off on semantic-derivation rules with reshape on Rule 3 + two clarifications on Rules 4 (emit both inline and page-level voice zones) and 5 (achievedRatio computed at Phase 4-new emission time from WCAG math).
- Phase 4-new implementation prompt drafted as six gates (A validator, B site-level, C page structure + section emitters, D cross-page editorial, E photo + integrity + full orchestrator, F approval gate renderer) with explicit stop conditions.
- Code Gate A pre-execution diagnostic caught two architectural concerns before any writes: Rule 3 persona-durations table drifts against Fixtures 3 and 6; editorial-authoring boundary unresolved for Gates B-F.
- Routed to Design. Q1 resolved (b) — Rule 3 collapses to two-row (all personas except urgent-service at entry 400 / hover 180; urgent-service at entry 250 / hover 150). Fixtures 3 and 6 stay at current hashes. Q2 resolved (1) — LLM authoring inside Phase 4-new modules, editorial vs structural field boundary locked, validator contract shifts to persona-rule adherence on editorial fields.
- Session closed at Phase 4-new implementation gate. Architecture resolved; implementation deferred to Session 4.

**What changed:**

- Six-fixture profile.json + expected composition-plan.json library on disk at ~/grm-automations/docs/composer/fixtures/.
- emotional-arc.md rewritten with persona-signature frameworks (Gate 1).
- SKILL.md Phase 4 signature tree rewritten (Gate 2).
- css-framework.md Motion Restraint scoped to Tier 2 (Gate 3).
- composition-plan-schema.md: §5.3 contracts for 4 section types (Gate 4), §14 intent-spec shape contract (renumbered from §16).
- Phase 4-new architecture resolved: LLM authoring inside modules; editorial/structural field boundary locked; validator shifts to persona-rule adherence on editorial fields; Rule 3 collapsed to two-row.

**What's in-flight:** Nothing on disk. Session 4 opens fresh against Desktop artifacts + on-disk brain + handoff.

**What's next:**

Session 4 target = finish the skill. Three bullets:

1. Phase 4-new implementation — Code executes six-gate prompt. Gates A through F. Atomic commit per gate. Stop conditions per gate. Editorial fields LLM-authored inside modules; validator checks persona-rule adherence not exact-string equality. Rule 3 locked two-row.
2. Checkpoint 2 — after Gate E, Design reviews Phase 4-new output on 2-3 fixtures (Fixtures 2/3/4 anchor set). Design signs off on editorial quality or reshapes. Pullquote retrofit decision surfaces.
3. Phase 5-new implementation (Stage IV) — HTML/CSS/JS emission from composition-plan.json + profile.json. Scoping diagnostic first; then implementation prompt; then Code executes.

Post-skill work (out of scope for Session 4): Stage V Luna validation build; Stage VI retirement decision.

**Open questions / deferred decisions:**

- Fixture 2 pullquote word-count retrofit-or-grandfather (Checkpoint 2).
- §5.3 remainder contracts for 6 stub section types — fixture-observed shape used in Phase 4-new; formal contracts deferred until real-build demand.
- Phase 5-new scoping — opens in Session 4 after Checkpoint 2 sign-off.

**Known traps for Session 4:**

- LLM-authored editorial fields make Phase 4-new output non-deterministic. Validator catches adherence; Checkpoint 2 catches quality.
- Fixture 6 drift A/B is Phase 5 concern, not Phase 4-new. Structural emission should be clean for Fixture 6 at Gate E.
- Phase 4-new is large. If gates surface substantive rework, split sessions — don't press through.
- Chat-Claude drafting discipline lesson carried: verify prompts against fixtures-on-disk before sending; read scoping diagnostics for architectural holes before writing implementation on top; no placeholders in paste-ready artifacts.

**Acknowledgments:**

- Ron held CTO-over-Chat across 10+ hours, arbitrated architectural reframes cleanly (Reading C, Q1, Q2, session-close timing), surfaced process-overhead concerns honestly rather than absorbing.
- Design delivered substantive architectural authorship: 6-column persona bias table (Gate 1), §14 two-pillar intent-spec contract (Reading C), editorial vs structural field boundary (Q2), approval gate UI reshapes, Rule 3 two-row collapse.
- Code caught four framework-level concerns at pre-commit verification preventing architectural drift: Gate 1 tie-breaking cascade, Commit 4 truncation + Edit 4B missing spec, §2/§4 envelope vs fixture shape divergence, Rule 3 + editorial-authoring boundary at Gate A.
- Chat-Claude drafting drift at context-pressure points cost round-trips. Improvement vector to Session 4: verify prompts against fixtures before sending; read scoping diagnostics for holes before writing implementation on top.

---

## Session block — 2026-04-22 (Stage II close)

**Window type:** Chat-Claude (facing Ron). CTO seat. Stage II execution through close.

**Session arc:**
- Opened with Stage I + Stage II (a)+(b) closed from 2026-04-21, handoff doc in chat context but never committed to disk. First task: commit handoff + run Code read-only diagnostic as Stage II (c) pre-work.
- Code diagnostic surfaced state of SKILL.md Phase 3/4/5, typography.md + voiceMap.md (pre-merge Composer state), emotional-arc.md (five personas confirmed), Luna F8 profile.json (anchor instance), composer-backlog.md (schema-adjacent items). Also revealed `COMPOSER_STAGE_II_C_HANDOFF.md` missing on disk.
- Handoff committed to disk (c0235af + 7903733 log). Design flagged "three-voice × three-persona" typo in handoff Part III — corrected in log commit referencing three-voice × five-persona.
- Stage II (c) Phase 1 — profile-schema.md. Code under full authorship after six locked scope calls; draft surfaced six flags. Four editorial-reach items routed to Design: role vocabulary (image-handling.md surfaced richer taxonomy), `designChoices.heroBackground` routing, scraped `typography.headingFont/bodyFont` fields, testimonial-rule stability. Design decisive across all four — corrected Chat-Claude's conservative instinct on the typography fields drop ("field gravity is an editorial cost"). Code revised and committed (83b2c43 + 9f1a271 log). Two backlog items added.
- Stage II (c) Phase 2 — composition-plan-schema.md. Chat-Claude drafted skeleton (v1) with seven locked pre-draft scope decisions from Design. Design Checkpoint 1 review verified pre-draft flags landed, confirmed §10 invariants classification, answered eight open questions. Chat-Claude revised (v2). Code's verification step at commit time surfaced framework-level mismatch on `signatureMicroInteraction` — Composer's Phase 4 tree implements five motion-based signatures; Design's six were compositional. Two different categories of thing, not naming substitution. Design resolved with two-tier architecture: Tier 1 `signatureMicroInteraction` (compositional, singular, six values); Tier 2 `microInteractions` (motion, plural, four values). Path 1 (Design's vocabulary wins) via Path 3 mechanism (schema ships with forward spec, cascade work logged to Stage III). Chat-Claude revised (v3). Code committed (06262f9 + e4720aa log). Six backlog items added.
- Stage II (d) — typography three-way merge. Code diagnostic enumerated 12 conflicts: 9 auto-resolvable under README tie-breakers, 3 Design arbitration (A1 SectionOpener framing, B3 Fraunces-universal rewording, C3 pullquote trigger threshold). Design resolved all three decisively — preserve orientation-gating prose under role-class framing; rewrite Appendix B thesis citing "variety across prospects" principle; Option 1 on pullquote (8-20-word heuristic wins, ≥60-word rule + `promoted: true` override retire; testimonial-spotlight earns its own section type if ever needed, not a pullquote threshold switch). Code executed full merge. Commit fc0ebfa + ca902ad log (966/288, largest single commit of Stage II). Sentinel check confirmed Rule E6 + Check 18 intact in home files (anti-slop-rules.md + css-framework.md — neither lives in typography.md to be lost). Backlog item B transitioned Active → Resolved.
- Stage II (e) — tier-logic strip. Code diagnostic opened with framing correction: tier isn't retiring from Composer. Appendix B preserves tier as differentiation axis for palette/section-density/motion/photo. What retires is tier-keyed tokens + font selection + `.tier-*` CSS class system. Four editorial-reach items: CONFIG.spacing design call, glass-variant wide-trigger rationale, example-build.md reframing scope, anti-slop Block A refactor. Chat-Claude made Item 3 scoping call (defer full reframe, add pre-Composer-era status-note header, log dedicated reference-build authoring pass to backlog). Ron's "tier has become less important" reframe redirected Chat-Claude away from over-engineering the Luna drift verification gate. Design arbitrated Items 1, 2, 4: glass-variant stays tier-keyed per Appendix B; anti-slop Block A refactored around serif-display/sans-display grouping with group-naming sharpening at typography.md §11; CONFIG.spacing refactored to base-plus-multiplier architecture (Design authored 20 persona-base values + 2 tier multipliers, splitting editorial authorship from engineering calibration). Code executed. Commit 4e70a0b + 9798579 log (7 files, 196/141). Luna F8 post-commit spot-check showed 3 of 4 values drifted >10% on quiet-confidence × Professional — logged to backlog for post-commit A/B on next real build. Three backlog items transitioned or added.
- Stage II (f) — P6.1 implementation spec + stub. Mechanical. grm-browser Playwright install at `~/grm-automations/tools/grm-browser/` confirmed reusable per README line 171 ("Phase 6 skill integration is deferred"); no new dependency. Stub (530 lines at `scripts/rendered_content_check.py`) + integration spec (153 lines at `references/phase-6-integration.md`). Commit 2650ac1 + d9cc4ef log.
- Stage II closed. All six sub-stages a-f complete. Architecture specification done.

**What changed:**
- `COMPOSER_STAGE_II_C_HANDOFF.md` committed to disk (c0235af + 7903733)
- `references/profile-schema.md` authored — 389 lines, schemaVersion 1.0, eight-role closed eligibleRoles enum, Phase 3.5 alignment (83b2c43 + 9f1a271)
- `references/composition-plan-schema.md` authored — 530 lines, schemaVersion 1.0, two-tier signature architecture, 15 closed voice zones, 17 locked scope decisions (06262f9 + e4720aa)
- `references/typography.md` merged — 952 lines, three-voice system + Composer's technical content absorbed, Appendix B Fraunces-thesis rewritten to persona-conditional-universal, orientation-gating prose preserved under role-class framing (fc0ebfa)
- `references/voiceMap.md` merged — 532 lines, Design's zone table + Composer's anchor-strip + three-tier service composition preserved, pullquote deployment split across files with cross-reference (fc0ebfa + ca902ad)
- `references/css-framework.md` CONFIG.spacing refactored to persona-base (5) + tier-multiplier (2) architecture; `:root.tier-*` blocks retired; tier-keyed font tables removed with cross-reference to typography.md §11 (4e70a0b)
- `references/anti-slop-rules.md` Block A refactored around persona + serif-display/sans-display grouping; Phase 6 auto-checks reference groups rather than enumerating personas (4e70a0b)
- `SKILL.md` line 341 + `references/hero-patterns.md` line 41 rationale updated to cite Appendix B section-density dimension; line 608 `class="persona-{kebab}"` replaces `class="tier-premium"` emission (4e70a0b)
- `references/emotional-arc.md` Modern specialist font guidance rewritten to cite typography.md §11 Persona 5 directly (4e70a0b)
- `references/example-build.md` pre-Composer-era status-note header added (no other edits; full rewrite backlogged) (4e70a0b + 9798579)
- `scripts/rendered_content_check.py` authored — 530-line Python stub, Playwright + Pillow, two-threshold model, static-blank/scroll-dependent branch (2650ac1)
- `references/phase-6-integration.md` authored — 153-line integration spec, P6.1 full + P6.2/P6.3/P6.4 placeholder rows (2650ac1 + d9cc4ef)
- `composer-backlog.md` — two items transitioned to Resolved (Stage II (d) SectionOpener merge conflict at ca902ad log commit; CONFIG.spacing tier-keyed residues at 9798579 log commit); ~10 new Active items added

**What's in-flight:** Nothing. Stage II closed. All three parties (Ron, Code, Design) holding clean.

**What's next (first Stage III session):**

Per brain §8, Stage III is Phase 4-new implementation. But **Stage II.5 precedes Stage III** — hand-written profile.json fixtures covering sparse photo library (0-3 hero candidates), populated library (8+), over-constraint (insufficient photos for layout minimum), high-review-count, low-content-depth, multi-vertical. Each fixture pairs with an expected composition-plan.json outcome. Stage III consumes these fixtures to validate Phase 4-new before running against Luna F8's actual profile.json.

Recommended first-session opening move: scope Stage II.5 fixture authoring. Likely Chat-Claude drafts fixtures with Design pre-review on the persona/vertical selection; Code implements. Design Checkpoint 2 is post-Phase-4-new-implementation, not pre-fixture.

Alternative: back-to-back Stage II.5 + Stage III Phase 4-new as one continuous architectural push. Fixture authoring is lighter editorial-reach than Phase 4-new; may be manageable as Phase 1 of a combined session.

**Checkpoint 2 trigger:** Design reviews Phase 4-new output on 2-3 fixtures before Stage IV begins (brain §8 Stage III gate).

**Design's standby posture:** Ready for Checkpoint 2 whenever Phase 4-new produces output on fixtures. No rush.

**Open questions / deferred decisions:**
- Stage II.5 fixture authoring sequencing — Chat-Claude drafts with Design pre-review vs. Code authors under scoping guidance. First Stage III session scopes this.
- Luna F8 drift signal from Stage II (e) — resolves on next quiet-confidence × Professional build via visual A/B against Luna F8 shipped. Not resolvable from numbers.
- F1-F8 broader persona/tier spot-check — 4 other personas × various tiers pending. Target Stage II follow-up dedicated pass, or first Composer-era build.
- Composer-era reference build authoring pass (replaces example-build.md header-noted state) — deferred post-Stage-II, possibly alongside first Composer-era sales build.
- Backlog triage pass — ~10-12 Active items now accumulated. Worth a review at Stage III open to confirm which items gate Stage III vs. which are truly deferred.

**Known traps:**
- Luna F8 drift: any near-term quiet-confidence × Professional Composer build renders visibly differently from Luna F8 shipped (hero ~20% larger). Visual A/B should precede lock-in of Design's persona-base values.
- example-build.md header note is a speed-bump, not a fix. File remains in `references/` and Phase 5 still loads it as pattern-match reference — header warns readers, doesn't prevent pre-Composer patterns from influencing emission. If emission regresses on a near-term build, escalate.
- Stage III Phase 4-new is substantially larger scope than any single Stage II sub-stage. Natural session-splitting expected — Stage II.5 as Session 3a, Phase 4-new implementation as Session 3b, Checkpoint 2 mid-Session-3b or separating to Session 3c.
- Three Stage III backlog items from Stage II (c) Phase 2 commit (emotional-arc persona-signature column rewrite, SKILL.md Phase 4 signature tree rewrite, css-framework.md Motion Restraint review) gate Phase 4-new implementation. Read backlog at Session 3 open.

**Acknowledgments:**
- Ron held the CTO-over-Chat position across the session. Called the small-check-ins-on-editorial-reach pattern explicitly ("anytime conflict pops up from Code on items that involved Design, small check-ins always get us the best result") — that rule eliminated iteration at multiple decision points. Trusted Chat-Claude's Item 3 scoping call and made the "tier has become less important" reframe that redirected away from over-engineering the Luna drift verification.
- Design delivered real architectural innovation: the two-tier signature resolution on signatureMicroInteraction (Tier 1 compositional + Tier 2 motion) wasn't in Checkpoint 1 response — surfaced at Code's verification and resolved at Design's next pass as a framework-level reframe. Same pattern on CONFIG.spacing base-plus-multiplier architecture — Design didn't just author 20 values; he split editorial authorship from engineering calibration in a way that makes future tuning tractable. The serif-display/sans-display grouping sharpening on anti-slop Block A was a genuine improvement over Chat-Claude's draft.
- Code's authority discipline before drafting — reading image-handling.md before profile-schema Flag 1 surfaced the role-vocabulary gap; reading SKILL.md Phase 4 before composition-plan-schema commit surfaced the signatureMicroInteraction framework mismatch. Full authorship on mechanical work earned additional trust across the session. Code also led Stage II (e) diagnostic with the framing correction ("tier isn't retiring from Composer") that reshaped how Chat-Claude and Design processed the inventory.
- Three-party cadence held across six commits, four Design arbitration rounds, and ~20 editorial-reach routing decisions. No flattened conflicts. No silent resolutions on load-bearing calls.

---

## Session block — 2026-04-21 (afternoon/evening)

**Window type:** Chat-Claude + Code + Design three-way relay.

**Session arc:**
- Stage II (a) file copies complete (typography.md, voiceMap.md, handoff-discipline.md, LESSONS.md merge)
- Stratum 3 identity sweep across 10 reference files
- HANDOFF.md removal (superseded by COMPOSER_BRAIN.md per §13)
- handoff-discipline.md Composer-adaptation note added
- Brain file minor revisions (§13 branch convention, §13 log convention, §8 mechanism clarification, §0 post-Composer roadmap vocabulary anchor)
- composer-backlog.md created as deferral-tracking artifact
- Stage II (b) attempted via format-patch + git am, blocked by sequencing collision, resolved via 9-commit Option C sequence under Design editorial direction

**What changed:**
- Stage II (a) and Stage II (b) both closed
- Composer now has three-voice typography system (--font-display / --font-body / --font-data) with persona-conditional CONFIG.fonts for all five personas
- All Wave 1/Wave 2 infrastructure features landed or explicitly deferred per Design judgment
- rescue-ready persona key renamed to urgent-service across Composer

**What's next:**
Stage II (c) — schemas authored (profile-schema.md, composition-plan-schema.md). Design Checkpoint 1 triggers after composition-plan-schema.md lands.

---

## Session block — 2026-04-21 (morning)

**Window type:** Claude Code executing per Chat-Claude relay. Chat-Claude (fresh window) directing; Ron routing.

**Action:** Minor revision to §13 branch convention per §17. Dropped proposal for `composer/stage-ii` through `composer/stage-vi` topic branches in favor of direct-to-main + `composer:` prefix. Matches actual repo convention (verified: only branch in grm-automations is `main`; all prior Composer commits landed on main directly). "Deferred decisions" bullet in 2026-04-21 block updated to RESOLVED. Ron + Chat-Claude + Code signoff.

**What changed:**
- Log-entry convention locked: follow-up commit, not atomic with work commit. See §13.
- Stratum 3 identity sweep across 10 reference files complete (commit 5b2d650). HANDOFF.md deleted as design-skill-era mechanism superseded by COMPOSER_BRAIN.md. Brain file §0 gained post-Composer roadmap vocabulary anchor. scale-architecture.md rewrite deferred (see composer-backlog.md for details).
- Brain §8 Stage II (b) mechanism clarified: `format-patch` + `git am --directory` rather than raw cherry-pick. Surfaced during Stage II (b) pre-execution structural check — two independent git repos with path-prefix mismatch make cherry-pick unviable.

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

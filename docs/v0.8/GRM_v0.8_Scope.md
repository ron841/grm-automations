# GRM Site-Generator Skill — v0.8 Scope

**Finalized:** April 19, 2026
**Authors:** Ron Kolb (product direction), Claude triage (synthesis), typography.md and voiceMap.md authored by Claude Design, technical review by Claude Code
**Status:** Ready for execution

---

## Framing

v0.7.2 produces competent Professional-tier sites. The SEO-GEO foundation, a11y primitives, schema, and geographic-targeting carried across F1–F5 without intervention. What the skill cannot currently produce by default is editorial-grade output — the typography discipline, voice-register distribution, composition-around-gaps, and strategic service weighting that separates a flagship site from a good contractor site.

v0.8's job is to close the Professional-to-editorial gap. Every Core Tier 1 item below either directly produces that quality lift or removes a structural barrier to producing it.

**Operating principle:** ship what logic and data support now. Defer only what we genuinely cannot ground in evidence or implementation capacity.

---

## Tier 1 — Core (ten items, must-ship for v0.8)

These ten items define v0.8. Without any of them, the skill fails to deliver the quality-ceiling promise.

### 1. typography.md
Design-authored, Code-classified, revised post-review. Rules for scale relationships, italic discipline, mono eyebrow system, SectionOpener primitive, StatRow, body measure and line-height, mobile scaling, font loading with `opsz` discipline, ornament rule, structural HTML contracts. Includes Appendix A: the exceptions principle. Role/alias/override naming convention as meta-rule (§0).

**Status:** ready to ship. File committed at `grm-design-handoffs/f5-a-quality-pool/typography-voicemap-v0.8.1/typography.md`.

### 2. voiceMap.md
Design-authored, Code-classified, revised post-review. Three first-class registers (Closing Table / Saturday Morning / Front Porch), register assignment logic, three-tier service composition (Signature / Operational / Distinctive) with decision tree, voice-pivot anchor strip, featured pullquote testimonial pattern with `promoted` flag and heuristic triggers (AND on heuristics, not OR), Front Porch footer pattern, copy discipline per register with sacred-lines concept, register coupling rules.

**Status:** ready to ship. File committed at `grm-design-handoffs/f5-a-quality-pool/typography-voicemap-v0.8.1/voiceMap.md`.

### 3. Rhythm tokens in CSS
`--section-padding-v`, `--tier-padding-v`, `--card-padding-v` as named tokens, with mobile overrides. Authoring approach: **tokenize the existing ranges already specified in typography.md §7** (24h/48-64v mobile, 40-56h/72-88v desktop) by picking a specific value from each range and dropping into `:root`. This is a naming + scoping task, not a new authoring round. Enforces vertical rhythm and prevents the Phase 1-style flattening that happened on F5.

### 4. SectionOpener primitive implementation
Consolidates four current variants across services, equine, reviews, and signature sections into one named pattern. Four parameters: eyebrow size, headline scale, italic placement, orientation. 4-to-1 refactor of shipped F5 code — near-zero net authoring cost, high consolidation value.

### 5. StatRow primitive implementation
Display numerals + mono labels with the 4×-ratio constraint enforced as an error, numeral weight ≤400 as a default, quiet-mono label register. Mobile responsive behavior baked in (3-col → 2-col → 1-col).

### 6. Honest-placeholder pattern as CSS primitive
Dashed striped frame with mono caption naming what's reserved and why. Silent blanks are forbidden. Already exists in F5's `.reserved-frame` class; lift to skill level. Tiny lift, guaranteed reuse.

### 7. Cache-header rationality in `vercel.json` template
Change CSS/JS directive from `public, max-age=31536000, immutable` to `public, max-age=300, must-revalidate` on non-hashed filenames. Shipped tonight as part of the F5 cache-fix; lift to the skill template so every future build inherits iterable cache behavior. Content-hashed filenames at build time deferred to v0.9 as the architecturally correct long-term answer.

**Rationale:** tonight's four-hour cache-trap surfaced this as a real iteration-breaking issue. Silently freezes stale assets in client caches across iterations. Not a theoretical concern.

### 8. Foundation preservation as non-negotiable across handoffs
Skill-level rule: any merge into a flagship build must preserve the full SEO/GEO/schema/a11y/script-driver foundation. Design's articulation in Design's voice — *"the deployed build is the source of truth; you may modify [explicit whitelist]; every other element passes through unchanged"* — codified in the skill's handoff section. Code's merge gate enforces at the validation layer.

### 9. Three-lens authorship pattern
Named and documented as a skill pattern. Design-layer files (typography.md, voiceMap.md, future design-layer skill files) primary-authored by Design, reviewed by Code for implementation fit, synthesized for continuity, arbitrated by Ron. Implementation-layer files (validators, primitives, enforcement specs) primary-authored by Code, reviewed by Design for aesthetic-intent preservation, same synthesis + arbitration. Every skill file passes through all four lenses before tagging.

### 10. Whitelist-the-changes handoff frame
Design's three-part diagnostic from tonight's foundation-strip episode, articulated in Design's voice. Opening frame for every Design prompt: *"The deployed build is the source of truth. You may modify [explicit whitelist]. Every other element — HTML structure, `<head>` contents, scripts, ARIA, data attributes, schema, meta tags — passes through your output unchanged."*

This is the structural fix Design identified: invert the default from "compose freely, preserve implicitly" to "compose within a whitelist, everything else passes through untouched."

---

## Tier 1 — Extended (nine items, ship alongside Core if cycles allow)

Real value, shipped alongside Core if cycles allow, bumped to v0.8.1 if scope tightens.

### 11. Hero-mode structure with one cell filled
Category + emotion + tenure as the selection axes. Pool cell filled (fact-led works because pools are aspirational + licensed + tenured). Other cells (electrical, HVAC, roofing, lawn care, plumbing) explicitly marked "populate on first build" — the structure is a form that future non-pool builds fill, not a fully-specified multi-cell tree.

**Fill protocol (added per Code challenge):** cell-filling follows the three-lens pattern. Design authors the cell's emotion + tenure mapping for a new trade category. Code reviews for implementation fit against the build in progress. Ron arbitrates. Without this protocol, cells get filled inconsistently under time pressure and the structure hollows out.

### 12. MD5 content-hash dedupe at Phase 3
Catches byte-identical duplicates. Phase 3 enhancement, ~5-line change, zero false-positive risk. pHash perceptual dedupe deferred to v0.9 per Code's review — the horse-country six-frame property family on F5 is the stress test for false-positive risk on legitimate "same property, different moment" frames.

### 13. Per-photo classification requirement at Phase 3
Every source photo gets a one-line subject + role annotation before Phase 6 fires. Locked required field, manual fill in v0.8. Automation via vision-model call deferred to v0.9 — lock the requirement first, let the template stabilize, automate once we know what we're automating. Catches the big-cat / stock-photo-infiltration / missing-service-coverage class of findings before triage, not mid-compile.

### 14. Comment-aware em-dash grep at Phase 6
Current grep fires on em-dashes in HTML comments Design writes to annotate sections, which never ship to rendered output. Regex excludes `<!-- ... -->` blocks. Fixes the false-fail Code surfaced tonight during the amp merge.

### 15. Slug reconciliation gate at Phase 6
Canonical, OG URL, sitemap `<loc>`, and redirect destinations all resolve to the live alias. Catches the class of silent drift where URLs written early in the build pipeline never get reconciled after final project naming. F5's sitemap stale-domain issue is the working example (every `<loc>` pointed at `a-quality-pool-service-grm.vercel.app` instead of `a-quality-pool-design-proposal.vercel.app`).

### 16. Font-link-to-CSS-consumption validator at Phase 6
Parse HTML `<head>` for font-family params, parse stylesheet for `font-family` declarations, fail if HTML loads a family the CSS never uses or the CSS uses a family no HTML loads. Catches the Space Grotesk drift across F5 sub-pages Code surfaced tonight (6 sub-pages silently rendering in Georgia fallback because they loaded Space Grotesk while `style.css` referenced Fraunces).

**Root-cause note (not in v0.8 scope):** the validator catches symptoms. The root fix is "when font stack changes, regenerate every page's `<head>` block." Build-pipeline concern for v0.8.1 or v0.9; validator ships now.

### 17. Canonical artifact pattern for Design → Code transfer
Zip per pass, named with round + pass (e.g., `typography-voicemap-v0.8.1.zip`). Dropped into `grm-design-handoffs/[build-slug]/` by Ron, committed and pushed by Code. Paste-inline only as fallback for tiny edits.

**Validation step (added per Code challenge):** before Code begins work on a handoff zip, confirm the file exists at the stated path and contains the stated files. Any mismatch stops the work and flags Ron. Do not work around missing source. Tonight's three near-miss handoffs — phantom amp-pass folder, drifted zip paths — are the data.

### 18. Handoff vocabulary discipline
*Shipped* = committed and pushed to the handoff repo. *Ready-for-review* = rendered in a preview environment but not yet in the repo. *Draft* = composed but not previewed. Three states, named, everyone means the same thing. Prevents the vocabulary confusion that caused tonight's "I pushed the amp" / "I rendered the amp in preview" mismatch.

### 19. Scope-gate rule
Both sides: Design proposes scope extension before executing it; Code proposes phasing on any prompt estimated at >3 hours of active work. Catches the class of silent scope creep that nearly doubled tonight's Design ask (hero → Services + Work + typography.md) and that required mid-session phasing on Code's original F5 Phase 1 build.

---

## Tier 2 — Bounded scope, ship after Tier 1 lands

### 20. Per-prospect `triage-decisions.json`
Machine-readable capture of Ron's judgment calls per build. Becomes deterministic input to the compile.

**Capture mechanism (per Code's minor note):** Code auto-extracts decisions from the triage transcript at session close. Lower-friction than Ron authoring JSON per build, reliable enough for first-pass. Structured form/template as fallback if auto-extraction produces noisy output.

### 21. Publication-rights field on photo inventory
`confirmed | unknown | restricted` per photo at Phase 1, flagged for Cameron-call where not. Data capture already half-present in Code's hero-candidate list tonight.

### 22. Structured build-notes format
One finding per JSON block with `id / phase / category / severity / description / proposed_fix / affected_files / carry_status`. Feeds Phase 9 when it lands.

### 23. Reserved-frame CSS primitive lifted into skill
Already working code in F5 (`.reserved-frame`); the lift is trivial; belongs in v0.8 as the visible implementation of Core #6 above.

---

## Tier 3 — Explicitly lower priority than prior candidate lists suggested

Per Code's F5 session-close review, downgraded from earlier Tier 1 nominations:

- **Lighthouse-ci per-project config.** Keep out-of-tree. F5 shipped fine with the existing Phase 6 Lighthouse pattern. Per-prospect config is maintenance burden without quality return.
- **OpenGraph extension from 10 to 15 tags.** Lock 10 as the standard, document the rationale in `seo-geo.md`, do not inflate. Additional tags (`secure_url`, `type`, `updated_time`, `determiner`, second `image`) are rarely consumed by crawlers.
- **Pre-write em-dash filter.** Harden Phase 6 grep with fail-on-match (and comment-aware exclusion, per Core #14) instead. Source-layer prevention vs. validation-layer catch — complexity in the wrong place. Supersedes v0.7.4 Finding #2.

---

## Tier 4 — Deferred to v0.9 by explicit reasoning

- **Phase 9 dossier-compile automation.** Real cost leverage (~2-hour segment drops to 15 minutes); clear implementation path (Code's `PHASE-9-COMPILE-NOTES.md` is the de facto spec). But it's an optimization, not a quality move. v0.8 closes the quality gap; v0.9 optimizes compile cost.
- **`design-rules.json` machine-readable constraint sidecar.** Enforcement layer for patterns. Patterns need to settle first; enforcement follows. Honors the pattern-before-enforcement sequence.
- **pHash perceptual dedupe.** False-positive risk on legitimate same-property-different-moment frames (F5's horse-country six-frame family is the stress test). MD5 alone ships in v0.8 (Core #12); pHash tuning in v0.9.
- **Content-hashed filenames at build time.** Architecturally correct long-term answer to cache-busting. Requires a build step the skill doesn't currently have. v0.9 scope.
- **Vision-model per-photo classification at Phase 3.** Automation of the locked required field from Extended #13. Lock template first, automate second.

---

## Tier 5 — v0.8.1 items explicitly deferred from tonight's work

Not skill-implementation items. Skill-validation and skill-infrastructure items. Tracked on a separate list from v0.8 implementation scope.

- **Substrate pipeline investigation.** `claude-mem list_corpora` returned empty during Code's typography review. Either observations from F1–F5 weren't written, or they're indexed under a tag/project the retrieval side can't see. Before v0.8 execution invests further in substrate-grounded decisions, verify the pipeline is actually writing queryable data. Highest priority v0.8.1 item.
- **Specialty-subdomain register question.** voiceMap.md §9 flagged: is specialty (Equine on AQP) a modifier on Front Porch or a fourth register? Next non-pool specialty build (commercial roofing on a residential site, historic-home rewires on an electrician, etc.) forces the decision. Interim rule: treat as Front Porch modifier, flag in build notes.
- **Four-register ceiling validation.** "Four registers is a practical ceiling" is asserted, not derived. If a build legitimately wants five registers (multiple distinct audiences, for example), revisit.
- **Vw coefficient rationale (deeper derivation).** typography.md §1 names 7–9vw primary / 5–6vw secondary / 3–4vw tertiary as authorial ranges. Deeper rationale — why those ranges and not others — deserves empirical validation across more builds.

---

## Sequencing

Dependency-ordered, not time-ordered.

**Wave 1 — Foundation.** typography.md (already drafted) + voiceMap.md (already drafted) + rhythm tokens + cache-header fix + foundation-preservation rule + whitelist-the-changes handoff frame. Load-bearing for everything downstream.

**Wave 2 — Primitives.** SectionOpener + StatRow + honest-placeholder + reserved-frame lift. Consume Foundation.

**Wave 3 — Composition.** Three-tier service composition implementation + featured-pullquote testimonials + hero-mode structure with fill protocol.

**Wave 4 — Gates (parallel with Wave 2 or 3).** MD5 dedupe, per-photo classification requirement, comment-aware em-dash grep, slug reconciliation, font-link validator.

**Wave 5 — Handoff discipline.** Three-lens authorship pattern, canonical artifact pattern, vocabulary discipline, scope-gate rule. Authored collaboratively; ready any time after Wave 1.

**Wave 6 — Tier 2.** triage-decisions.json, publication-rights field, structured build-notes, reserved-frame lift. Ship if cycles allow after Tier 1 completes.

---

## What success looks like for v0.8

A v0.8-generated site reproducibly reaches the editorial-grade typography and voice-register ceiling within one Design review round — measured on a fresh non-pool build produced post-v0.8 tag.

This is the honest success criterion. F5's ceiling tonight took three amp iterations plus a foundation restore. Oxford was a bespoke polish pass. Neither reached the ceiling via a single autonomous pass from raw data. v0.8 is not promising single-pass perfection; v0.8 is promising that the ceiling is reachable within one structured review cycle rather than requiring ad-hoc polish.

Handoff-discipline documentation means the collaboration pattern that produced typography.md and voiceMap.md this weekend is reproducible for every future skill-file round.

---

## What v0.8 explicitly does not attempt

- Phase 9 dossier-compile automation (v0.9)
- pHash perceptual dedupe (v0.9)
- Vision-model photo classification (v0.9)
- Content-hashed filenames at build time (v0.9)
- `design-rules.json` enforcement sidecar (v0.9)
- Resolution of the substrate pipeline question (v0.8.1 — investigation, not implementation)
- Resolution of the specialty-subdomain register question (next non-pool specialty build)
- Validation of the four-register ceiling (empirical, next N builds)
- Deeper vw coefficient derivation (empirical, next N builds)

---

## Execution posture

- **Waves 1–2 can begin immediately.** typography.md and voiceMap.md are authored and classified. Rhythm tokens, SectionOpener, StatRow, honest-placeholder, cache-header, foundation-preservation rule, and whitelist handoff frame are all scoped for execution with no outstanding authorship questions.
- **Wave 3 (hero-mode structure) should begin after Wave 1 + 2 ship** because the fill protocol depends on the three-lens authorship pattern being codified (Wave 5 item, but must be named before first cell-fill).
- **Wave 4 (Phase 6 gates) can run parallel** with Wave 2 or 3.
- **Wave 5 (handoff discipline) is mostly prose synthesis** and can run whenever.
- **Wave 6 (Tier 2) is optional for v0.8 tag** but improves the spec.

The v0.8 execution session opens with Wave 1, scoped to the three clear work items: adopt typography.md + voiceMap.md into the skill folder structure, author rhythm tokens, update `vercel.json` template.

---

*End of v0.8 scope.*

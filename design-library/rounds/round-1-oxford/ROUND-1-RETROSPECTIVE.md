# Round 1 Oxford — Audit + Process Retrospective

**Author:** Claude Code
**Date:** 2026-04-18
**Scope:** Full Playwright audit of the ceiling build at `https://oxford-lawn-ceiling-grm.vercel.app` + honest process debrief on the Design-in-the-loop approach
**Comparison target:** F6 at `https://oxford-lawn-grm.vercel.app` (built 2026-04-17 via prospect-site skill v0.7.3)

---

## Part 1 — Audit findings

### Screenshots captured

Full-page screenshots saved to `~/grm-sites-prospects/oxford-lawn-ceiling/audit-screenshots/`.

| # | Page | Desktop (1440×900) | Mobile (390×844) | F6 compare |
|---|---|---|---|---|
| 1 | Home | `desktop-01-home.png` | `mobile-01-home.png` | `f6-desktop-home.png` |
| 2 | About | `desktop-02-about.png` | — | — |
| 3 | Services | `desktop-03-services.png` | `mobile-02-services.png` | — |
| 4 | Process | `desktop-04-process.png` | — | — |
| 5 | Reviews | `desktop-05-reviews.png` | — | — |
| 6 | Contact | `desktop-06-contact.png` | `mobile-03-contact.png` | — |
| 7 | Gallery | `desktop-07-gallery.png` | — | — |
| 8 | Attributions | `desktop-08-attributions.png` | — | — |

### Confirmed findings by issue class

#### 1. Prototype artifacts bleeding through — CLEAN

`document.querySelectorAll('.gap-tag').length` = 0 on home. Same for `[data-screen-label]` (0) and `.gap-toggle` (0). No ceiling-annotation scaffolding made it into the production HTML. This worked because I read the ceiling's `index.html` end-to-end and removed these structures surgically. If the build had been code-gen'd from the ceiling directly, they would have shipped.

#### 2. Hero photo status — CONFIRMED MISSING (by design, reads as gap)

Home hero contains zero `<img>` tags. Above the fold is: editorial kicker, two-line serif display headline with italic accents, lede paragraph, two CTAs, stat row (4 numbers), and on the right column a CSS-drawn `strata-tall` motif (5 horizontal color bands with mono-typed labels).

**Ron's read is correct: the homepage does not have a hero photo anchor.** This is Design-intentional — the soil-strata motif is meant to replace a photo. But in the real build, against the content density of a real contractor's site, the top of the page reads typographic and abstract rather than visual and concrete. F6 anchors immediately with a truck/trailer hero photo.

**Same pattern recurs on About, Services, Process, Reviews, Contact, Gallery** — none of the 7 pages have an above-the-fold photo. Photos live only in section cards below the fold. At first-paint, all 7 pages present as headline + mono-chrome kicker + lede.

#### 3. Oxford logo placement — NEARLY ABSENT

- Nav: `.nav-logo .mark` is a 22×22 pixel lime square (pure CSS), NOT the actual Oxford logo PNG. The file `assets/logo/oxford-lawn.png` exists in the build but is never referenced anywhere visible. `document.querySelector('.nav-logo img')` returns `null` on every page.
- Footer: Footer brand mark is "Oxford *Lawn*" rendered in Newsreader serif. No `<img>` in footer. `document.querySelector('footer.foot img')` returns `null`.
- Elsewhere: No logo usage in hero, about section, or any other location.
- OG image: every page's `og:image` points to a property photo, not the logo. That's fine for social-card rendering but means the logo is effectively invisible except as text treatment.

**This is Code's execution gap, not a Design spec gap.** The ceiling's own partials.js used the same CSS-square `.mark` pattern with "Oxford *Lawn*" text to its right. I copied the pattern from the ceiling without questioning it. An actual logo placement would have been Code's judgment call to make, and I missed it.

#### 4. Mobile rendering (Home, Services, Contact) — MULTIPLE LAYOUT BREAKS

The ceiling's `base.css` has limited mobile breakpoints. `grid-template-columns` declarations set to `repeat(3, 1fr)`, `180px 1fr 1.25fr`, etc. don't collapse to single-column at mobile. Observed breaks:

| Page | Component | Mobile behavior |
|---|---|---|
| Home | Hero grid | Second column (strata-tall) wraps under text, correct |
| Home | 3-step cards | Stays 3-across at 390px viewport — each card ~110px wide, unreadable |
| Home | 4-stat row | Stays 4-across, stat numbers squish |
| Home | Reviews card grid | Stays 3-across, each card ~110px wide |
| Home | Service area ledger | Table squishes, columns overlap |
| Services | Numbered cards | Stays `180px 1fr 1.25fr` — number + photo + text all compressed |
| Services | Counter-list | Correct — 2-col stacks via existing media query |
| Contact | Form + direct block | Stays 2-col side-by-side instead of stacking |
| Contact | Chip-row filters | Correctly wraps (flex-wrap saves it) |
| All | Nav | Hidden via `@media (max-width: 760px) { .nav-list { display: none; } }` — **no hamburger fallback**. Users on mobile have zero navigation. |

The nav-hiding issue is the most serious. A site with no mobile navigation is not shippable to a real client. Base.css has a TODO-shaped hole here.

#### 5. F6 vs ceiling content completeness

Features F6 has that the ceiling lacks (strictly content/functional, not design):

- **Hero photo** — anchors F6 immediately
- **FAQ accordion with FAQPage schema JSON-LD** — "Before you call" section with 7 questions. The ceiling has no FAQ section at all, no FAQPage schema.
- **In-hero contact widget** — F6 has a sidecar contact form in the hero
- **Logo visible on hero** — the Oxford Lawn branded trailer in F6's hero puts the logo in frame
- **Sticky mobile CTA** — F6 has a mobile-only bottom CTA bar. Ceiling has none.

Features the ceiling has that F6 lacks (design-led):

- Editorial metadata rail (Closing Table voice)
- Soil-strata hero motif
- Timeline ledger (dark)
- Interactive process stepper
- Review theme index
- Filterable gallery with trade tags
- Magazine-chrome ("Volume 18, Issue 1") kicker

The trade is real: ceiling gains editorial voice and visual sophistication at the cost of immediate visual anchoring, mobile navigation, and FAQ-citation schema.

#### 6. Accessibility — 1 serious issue, isolated

axe-core 4.10.0 run against home, process, and services.

| Page | Critical | Serious | Notes |
|---|---|---|---|
| Home | 0 | **1** | `.layer.l-roots` (strata bar): `#8a6a3f` bg with `#f7f3ea` text fails AA for small mono text |
| Process | 0 | 0 | Clean |
| Services | 0 | 0 | Clean |

Only the strata divider fails. Fix is trivial: swap `color: var(--cream)` → `color: var(--ink)` on `.l-roots` only, or darken the brown background. One-line CSS change.

**Overall accessibility posture is strong.** Semantic landmarks (`<header role="banner">`, `<nav aria-label="Primary">`, `<main id="main">`, `<footer role="contentinfo">`, `<article>`, `<section aria-labelledby>`) are in place on every page. No missing alt attributes on images. No form labels orphaned.

#### 7. Performance — not formally measured

Lighthouse CLI was not run in this session due to time budget. Qualitative observations from Playwright network traces:

- Total uncached weight: ~10 MB across all pages (dominated by the 17 photos, several at 4032×3024 native resolution unserved)
- Font loading: 3 Google Font families — Newsreader (variable), JetBrains Mono (3 weights), Public Sans (5 weights). Reasonable.
- No JS framework. Just 1 small `shared.js` (~50 lines).
- Lazy-loading is active on all below-fold images (`loading="lazy"`).

**Known win:** no React, no Next, no webpack. This is close to a static-HTML sprint as any site we ship. Initial HTML is 21KB on home.

**Known loss:** no image optimization. Photos are served at native resolution in their native formats (.jpg, .jpeg, .png). A proper build would serve 2-3 sized variants per image via `<picture>` srcset with WebP. This was a deliberate time-box decision — everything ships original, nothing is transcoded.

#### 8. Broken links / 404s

- **Favicon 404** — `/favicon.ico`. Minor. No favicon was created for this build.
- **No other 404s** — all internal links resolve. All page routes respond 200 under `cleanUrls: true`.
- **External links** (Instagram, Facebook, LinkedIn, YouTube, Google Maps) are real URLs from `profile.json`, not spot-checked live but syntactically valid.

### Audit summary

Content and semantic correctness are strong. The site says true things about Oxford, is machine-readable via schema JSON-LD, and renders cleanly on desktop. The weak spots are all layout and asset deployment:

1. No hero photo anywhere (design-intentional, but reads as gap)
2. Oxford logo file exists in the build but is invisible to users (Code execution gap)
3. Mobile layout cascades are incomplete (CSS scope gap)
4. One color-contrast failure on one element (easy fix)

These are not "the Design-in-the-loop approach doesn't work" findings. They are "the handoff missed specific things" findings.

---

## Part 2 — Process retrospective

### A. What the Design → Code loop got right

Three things worked outstandingly well. All three are about Design producing output Code could execute against without inventing.

**1. base.css was production-ready without modification.**
The ceiling shipped a complete design system — palette, type scale, layout primitives, component classes, responsive rules (where they existed), hero compositions, card treatments, table treatments, trust-band animation. Code wrote zero new CSS rules and adjusted nothing in base.css. Every color pair that appeared in the final build used Design's tokens as-is, and every one that axe didn't flag passes AA. When Design produces a real design system and not a collection of screenshots, Code writes HTML against it with near-zero friction. This is the single biggest measurable win of the round.

**2. Pattern spec cards with clear structural outlines landed on first write.**
Specifically the Tier 1 patterns: editorial-metadata-rail, stat-row-editorial, numbered-service-cards, interactive-process-stepper, timeline-ledger-dark, trust-band-marquee. Each spec card provided enough structural description that I could read it once and write the HTML without iterating. The interactive-process-stepper even worked with just ~40 lines of scoped JS (`data-stepper`, `data-step-tab`, `data-step-panel`) because the spec was clear about the interaction model.

**3. Ceiling's composed pages served as working reference implementations.**
Reading ceiling's `index.html` was more useful than reading the 22 pattern spec cards. The ceiling showed me exactly how the patterns composed together at scale, how the rhythm between sections worked, what the voice shifts felt like in practice. Having both the isolated pattern specs AND the composed reference pages is the right deliverable shape. Either alone would have been weaker.

### B. What the Design → Code loop got wrong

Three specific friction points. Separating process, execution, and spec failures honestly.

**1. The logo was never specified for placement. (Process failure.)**
Oxford's logo PNG is in the dossier. The ceiling's partials.js used a CSS-square `.mark` element as a visual placeholder. I copied the placeholder pattern into the production build without questioning whether a client would ship their site without their own logo. That's a Code execution gap — I should have replaced the `.mark` div with `<img src="assets/logo/oxford-lawn.png">` during build. But it's also a process failure: the dossier handoff included the logo, the ceiling didn't specify logo placement explicitly, and neither the dossier nor the ceiling said "this CSS square is a placeholder, put the real logo here." A good dossier-to-build handoff flags placeholder elements explicitly.

**2. Mobile composition was incomplete. (Spec failure.)**
Design shipped `mobile.html` in the ceiling folder showing mobile compositions for Home, Services, and Contact. Those compositions were visual references — they showed what the mobile layout *should* look like. But the `base.css` only had mobile media queries for a small number of components (nav goes display:none, editorial rail stacks, hero grid collapses). Most grid components (3-step cards, service cards, review cards, stat rows, service area ledger) have no mobile media queries at all. The gap between "here's what mobile looks like" (mobile.html composition) and "here's the CSS that produces it" (base.css media queries) was never closed. Code didn't catch this because Code was working from base.css. Design assumed base.css would close it.

Fix: every pattern spec card should include a `@media` breakpoint rule and those rules should appear in base.css. Or: the mobile.html composition should be translated into CSS before handoff.

**3. Hero composition had a specific blind spot. (Composition failure, not spec failure.)**
The soil-strata hero column is beautiful in isolation. Against real content density (text-dominant left column, abstract motif right column), the page reads without a visual anchor. Design composed the hero abstractly — there was no real property photograph in Design's hands when the ceiling was proposed, so Design designed around that absence with the strata motif. When the real asset dossier landed (17 real photos including several strong hero candidates at 2560×1920 and 4032×3024 native), the hero composition could have been revisited. It wasn't, because the dossier-to-ceiling loop was one-directional: dossier came to Code, never back to Design.

This isn't Design doing something wrong. It's a sequencing problem, which is Section C.

### C. The sequencing problem — data after design

Ron's observation is the correct diagnosis. Design composed Oxford's ceiling without the actual Oxford asset dossier in hand. The ceiling used photo-slot placeholders ("gmb[3]", "photo · dethatching machine at work", etc.) and designed the compositions around slots, not around specific real images. Code then had to retrofit real images into slots that had been shaped abstractly.

**What breaks when the order is wrong:**

1. **Hero compositions designed without knowing what photos are available.** We got a soil-strata motif as a hero treatment because Design couldn't assume Oxford had a great hero photo. If Design had seen the 2560×1440 hero-03 property shot at composition time, the hero would almost certainly have been designed around it. The strata motif would have become the secondary visual on a later section.

2. **Portrait-dependent patterns designed assuming portraits existed.** pull-quote-founder, photo-portraits-degrading, and the about-moment composition all assume Tom or Tracy portraits. None exist. Design couldn't have known this without the dossier. Three patterns built on a false premise.

3. **Photo-density assumptions disconnected from real inventory.** The ceiling assumes photographic richness across filterable gallery, masonry review wall, and before/after slider. Real Oxford inventory is 17 images with zero matched before/after pairs. If Design had started with the real inventory, the before-after-slider pattern might not have been proposed at all — or would have been proposed as "premium-tier, commission required."

4. **Brand palette derivation was re-done.** Design's base.css has Oxford palette hardcoded (lawn-500, lawn-700, soil tokens). Node-vibrant extraction of the logo produces a similar but not identical palette. If Design had started with the palette extraction as an input, the base.css would have been tighter to Oxford's actual visual identity rather than an abstracted interpretation.

**What would change if the prospect-site skill's Phase 1–3 ran first:**

Phase 1 (WordPress/Squarespace/Wix crawl), Phase 2 (multi-page capture), Phase 2.5 (Google Places enrichment), Phase 3 (photo assignments with content-type tagging, orientation, aspect ratio, attribution, owner portrait detection, before/after pair detection) produce a structured JSON artifact that is *literally designed to brief a composition*. The `photoAssignments` block, the `testimonials` block, the `phase4Scoring` rubric, the service-area capture — these exist to constrain and inform decision-making downstream.

If Design received `profile.json` + the curated asset dossier as composition input, the compositions would be shaped to fit the data from the first pixel. The soil-strata motif might still have been proposed (it's genuinely a strong concept), but it wouldn't have to carry the full weight of the hero alone. Patterns like photo-portraits-degrading would be proposed conditionally ("if `ownerPortrait !== null`, use this pattern; else use pattern-X").

This is a process change, not a Design capability change. Design is good at what Design does; it's the handoff order that's upside-down.

### D. What the prospect-site skill already does that didn't make it into this cycle

The v0.7.3 skill bundled a substantial production pipeline. The ceiling build cherry-picked some of it and missed others. Separating "shipped in this build" from "exists in skill but was skipped":

| Capability | Shipped? | Notes |
|---|---|---|
| LocalBusiness schema JSON-LD | ✓ | Full block on home, complete |
| AggregateRating schema | ✓ | 4.9 / 132, real data |
| Service schema | ✓ | Linked to LocalBusiness via @id |
| Review schema (individual) | ✓ | 5 real Google reviews on reviews.html |
| FAQPage schema | ✗ | **Missing — F6 has it.** No FAQ section in ceiling at all. |
| Sitemap.xml | ✓ | All 7 pages, correct lastmod, priority |
| Robots.txt with AI crawler allow-list | ✓ | GPTBot, ClaudeBot, PerplexityBot, Applebot, etc. |
| llms.txt | ✓ | BLUF summary + key-page links |
| OG + Twitter 15-tag block | ✓ | Every page, content-specific |
| Canonical URLs | ✓ | Every page |
| Page-specific meta descriptions, 150–160 chars | ✓ | All 7 unique |
| Semantic HTML landmarks | ✓ | header/nav/main/footer/article/section |
| Skip link | ✗ | **Missing.** Skill ships one, ceiling doesn't. |
| Mobile sticky CTA bar | ✗ | **Missing.** F6 has it. |
| Click-to-call on phone numbers | ✓ | All `tel:` links present |
| Image alt attributes | ✓ | All images captioned |
| Anti-slop em-dash check | ✓ | Manual — all em dashes stripped during authoring |
| Phase 6 quality gates (em dash, banned phrases, attribution regex) | ✗ | Not run programmatically, only spot-checked |
| Node-vibrant palette extraction | ✓ in dossier, ✗ in build | Dossier used real extraction; ceiling used Design-curated palette instead. Different but compatible. |
| FAQ content from captured questions | ✗ | **Missing entirely.** |
| Google Places photo attribution in footer | ✓ | On gallery page and attributions page |
| Manual review of every fact against profile.json | ✓ | No fabrication anywhere |

**Should-be-mandatory-always, regardless of approach:**

Five capabilities should be non-negotiable on any GRM build, whether the skill runs it, Design-in-the-loop runs it, or a human composes from scratch:

1. **FAQPage schema with 5-10 real Q&A.** Highest single AI-citation factor. Cost to add: 45 minutes per site. Missing it on the ceiling is a measurable SEO-GEO downgrade vs. F6.
2. **Skip link for keyboard accessibility.** One `<a>` tag. No excuse to skip.
3. **Mobile sticky CTA bar with click-to-call.** Critical conversion element on contractor sites.
4. **Image optimization (srcset + WebP) before deploy.** The 10MB unoptimized image weight in this build is indefensible for mobile users on LTE.
5. **A mobile composition pass, page-by-page, with full viewport screenshots verified before sign-off.** Catches the mobile-break problem that slipped through here.

### E. Role recommendations — strategic, not tactical

**Code's role.**
- **Lead:** converting design systems to production HTML; SEO-GEO compliance; schema JSON-LD authoring; semantic markup and accessibility baseline; build-time image optimization; deploy pipeline; audit and verification; commit/push/PR hygiene; skill authoring (the `prospect-site` skill itself is Code's work).
- **Should wait:** visual composition decisions, color/type choices, hero compositions, novel pattern design, brand voice tone, sales-page narrative architecture. When Design has been in the loop, Code should implement Design's calls, not re-design them.
- **Best single deliverable:** a running deployed site that passes every audit and is true to the data.

**Design's role.**
- **Lead:** brand visual identity, pattern library design, editorial voice-to-visual translation, hero compositions, novel interaction patterns, premium-tier visual differentiation, photography curation standards (when Design has the photos), color-palette rationale.
- **Should NOT lead:** SEO-GEO schema authoring, mobile-layout-media-query specification, real-data fact-gathering, crawler-driven content capture, asset-by-asset production photo pulling.
- **Output format needs to change to integrate cleanly:** (1) Pattern spec cards should include CSS media-query rules, not just desktop structural outlines. (2) Every pattern should have a "real data conditional" — what the pattern becomes when the data is missing (no portrait, no before/after, no premium photos). (3) Compositions should receive `profile.json` and the asset dossier as input, not be authored against photo-slot placeholders. (4) Base.css should have a designated "production" export that's stripped of gap-annotation scaffolding, separate from the design-review version.

**Claude's role (the chat session with Ron).**
- **Adds value:** strategic coordination between Design and Code, catching process-order problems (like the dossier-after-ceiling sequence), writing and maintaining the BUILD-LOG and retrospective, flagging sequencing issues before they become execution problems, making the scope-vs-time tradeoff decisions explicit, maintaining the scoreboard across rounds.
- **Gets in the way:** micro-managing Code's HTML or Design's CSS. Re-deriving facts from profile.json when either Design or Code can do it directly. Restating the same requirements across three different contexts.
- **Should stop making decisions about:** exactly which patterns to ship (that's a Design + Ron call), what color a button should be (Design), how to write the JS for an interactive stepper (Code).
- **Should flag and escalate:** when the dossier is missing data Design will need. When the ceiling composes against photos that don't exist. When the skill capability set diverges from the Design-in-the-loop output. When time is running out and scope has to shrink.

**Ron's role.**
- **Only Ron should decide:** prospect selection, which tier a prospect sits at (Professional / Premium / Standard), whether a commissioned shoot is worth the money for a specific account, whether to ship at current density or wait for more assets, the brand voice taxonomy (Closing Table / Front Porch / Saturday Morning is Ron's system), pricing and sales positioning, what goes public vs. stays internal.
- **Has been doing that could be automated or delegated:** manual dossier assembly. The prospect-site skill Phase 1–3 produces a dossier that is 80% of what was hand-curated for this build. Delegating dossier creation to the skill (and then handing that to Design for review) would cut 30 minutes of Ron's time per prospect.

### F. Proposed workflow for Round 2 / next prospect

Goal: every handoff is one-directional and every role runs against real data.

```
 ┌─────────────────────────────────────────────────────────────────┐
 │  STAGE 0 — Ron picks prospect                                   │
 │  Input:   prospect URL, trade, service area hint                │
 │  Output:  greenlight + slug                                     │
 │  Gate:    Ron-approved prospect                                 │
 └─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
 ┌─────────────────────────────────────────────────────────────────┐
 │  STAGE 1 — Skill Phase 1–3.5 (automated capture)                │
 │  Runs:    prospect-site skill, Phases 1 through 3.5             │
 │  Output:  profile.json  +  asset dossier (logo, photos,         │
 │           palette, facts, copy samples, sales ammo)             │
 │  Gate:    profile.json cleared of `unknownFields` that matter   │
 │           OR Ron decides to proceed with gaps documented        │
 └─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
 ┌─────────────────────────────────────────────────────────────────┐
 │  STAGE 2 — Design composes with real data in hand               │
 │  Input:   profile.json + full asset dossier + palette           │
 │           extraction + brand voice mapping                      │
 │  Output:  Ceiling pages (HTML/CSS) + pattern dossier, with      │
 │           real photo assignments baked in (not slot             │
 │           placeholders) AND real-data-conditional variants      │
 │           specified for patterns that depend on optional assets │
 │  Gate:    Ron reviews ceiling live; approves scope; flags any   │
 │           patterns to cut, add, or defer                        │
 └─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
 ┌─────────────────────────────────────────────────────────────────┐
 │  STAGE 3 — Code implements                                      │
 │  Input:   approved ceiling + dossier + SEO-GEO spec             │
 │  Output:  deployed build folder, deployed Vercel project,       │
 │           audit screenshots, schema validation report,          │
 │           Lighthouse report, committed to grm-automations       │
 │  Gate:    Code-owned Phase 6 quality gates: em-dash, banned     │
 │           phrases, schema cross-ref, attribution regex, skip    │
 │           link present, mobile composition verified, axe 0      │
 │           critical/serious, Lighthouse ≥ 90 mobile              │
 └─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
 ┌─────────────────────────────────────────────────────────────────┐
 │  STAGE 4 — Ron reviews, Design and Code iterate                 │
 │  Input:   live deployment, audit artifacts                      │
 │  Output:  sign-off or iteration tickets                         │
 │  Gate:    Ron: ship or iterate                                  │
 └─────────────────────────────────────────────────────────────────┘
```

**Specific allocations:**

- **Where the asset dossier generation fits:** Stage 1. Output of the skill's capture phases. Not hand-curated.
- **Where SEO-GEO compliance gets enforced:** Stage 3, Code-owned Phase 6 gates. Not Design's problem.
- **How Design sees real data before composing:** Stage 1 → Stage 2 explicit handoff. Stage 2 does not start until Stage 1 delivers.
- **How Code's output from the skill becomes Design's input:** the asset dossier (built in oxford-lawn/design-dossier/ shape) is the artifact. It already has the right structure.
- **What gate Ron actually needs to be at:** Stage 0 (prospect pick), Stage 1 gate (if `unknownFields` need a call), Stage 2 gate (scope approval on the ceiling), Stage 4 (ship/iterate). Four gates, not one gate per decision.
- **What can flow without Ron:** everything else. The skill runs automatically, Design composes against the dossier, Code implements against the ceiling, audits run themselves.

### G. Open questions for Ron

These need decisions before the next round can run without re-negotiating scope.

1. **Hero photo policy.** Do we want hero photos on every page by default, with the soil-strata motif (or vertical-specific equivalent) reserved for pages that don't have a strong lead photo? Or keep the ceiling's "hero is typographic + motif" direction and accept the cost?

2. **Logo placement standard.** Confirm: logo PNG should appear in the nav (left side, beside or replacing "Oxford *Lawn*" text mark) AND in the footer. For the ceiling build, a quick fix is ~5 lines of HTML + maybe 10 lines of CSS. Want that as a patch-commit today, or roll into Round 2?

3. **Mobile baseline.** Do we commit to "full mobile composition authored alongside every pattern, shipped in base.css" as a Round 2 requirement? This is a Design workload change.

4. **FAQPage schema as always-on.** Should every build ship a FAQ section with 5-10 real Q&A pulled from captured content? This is a Code + content workload change, ~45 min per site, but meaningful SEO-GEO lift.

5. **Image optimization before deploy.** Green-light a build-time pipeline (sharp/squoosh) that generates WebP + multiple sizes per photo. ~30 min of Code work to implement, but it's a one-time cost and every future build benefits.

6. **Tier mapping.** Oxford shipped at "Professional" per the rubric but got a Round-1-class ceiling which is closer to "Premium" in visual density. Are we keeping all three tiers (Standard / Professional / Premium) visually distinct, or does every client get the Premium-level ceiling now that it exists?

7. **Round 2 prospect pick.** Same vertical (lawn/landscape) so patterns stay consistent and we test replication? Different vertical (electric, septic, HVAC) to test Design's spec portability? I have a preference (different vertical), but the call is yours.

---

## Headline answer — the one honest read

**Was Design-in-the-loop worth the process cost?**

Yes, and the one change that would most improve it is **sequencing: skill Phase 1–3 runs before Design composes, not after.**

The evidence is in the delta between the outstanding parts of this build and the gaps. The outstanding parts — base.css translating cleanly, Tier 1 patterns landing first-try, editorial voice surviving into HTML, palette coherence across the site, 4.9-star AggregateRating schema rendering correctly — all happened because Design produced output Code could execute against. That is the working mechanism of the loop.

The gaps — no hero photo, no logo placement, mobile-layout breaks, missing FAQPage schema, patterns like photo-portraits-degrading that depend on assets that don't exist — all happened because Design composed without seeing the real data first. Fix the sequence, and most of those gaps disappear.

The ceiling, looked at honestly, is a design exercise shaped by Design's imagination of what Oxford could look like, not what Oxford looks like. That gave us the best parts of this build — the editorial voice, the Saturday Morning trust band, the timeline ledger — but also every mismatch I flagged. In Round 2, if Design receives the asset dossier and `profile.json` as Stage 1 output before composing, every composition decision gets the benefit of reality, and Code's retrofit work shrinks to near-zero.

**Worth it. Fix the sequence. Keep going.**

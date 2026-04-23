---
name: prospect-site-composer
description: "Generate a custom multi-page preview website for a local home services contractor prospect from their live URL. Architectural successor to prospect-site-design, restructuring Phase 4 and Phase 5 against Claude Design's editorial framework (five personas driving layouts A–E, photo role hierarchy, three-voice typography, scale contrast, motion restraint, signature micro-interactions) and backporting production's Wave 1/Wave 2 infrastructure (rhythm tokens, SectionOpener and StatRow primitives, font system). Deeply crawls the prospect's real site, captures their brand data (owners, services, testimonials, credentials, colors, photos, promotions), scores their current web presence, and produces profile.json. Phase 4 produces composition-plan.json — the explicit editorial specification of every page — which Phase 5 emits as HTML with zero default-template inheritance. Phase 5.5 reads schema content from composition-plan.json, not the emitted DOM. Two-pillar hard gate: editorial (13-check Phase 6 suite) and SEO/GEO (schema validity, Lighthouse SEO ≥95). Runs isolated at ~/.claude/skills/prospect-site-composer/ — does not touch production prospect-site. Use this skill whenever the user types /prospect-site-composer followed by a business name and URL, or asks to build a prospect preview site using the Composer pipeline."
---

# Prospect Site Composer

## What this skill does

Given a business name and a live URL, this skill produces a fully built, multi-page preview website that Ron can text or email to the prospect as a sales weapon. The preview uses the prospect's real brand, real services, real testimonials, real owner names, and real promotions. It deploys to a unique Vercel URL in the form `[business-slug]-grm.vercel.app`.

Command format:

```
/prospect-site-composer "Business Name" https://their-site.com [@instagram_handle]
```

Optional `--auto` flag skips the Phase 4 design approval gate. Optional `--from-phase N` resumes from a specific phase when iterating on a previously-started build.

## Architecture

This skill uses the progressive disclosure pattern. SKILL.md contains the workflow, decision trees, hard rules, and pointers. Heavy specification content lives in `references/` and gets loaded on demand:

- `references/hero-patterns.md` — Hero spec (four modes, shared glass card with default and wide variants, video augmentation)
- `references/section-patterns.md` — Every non-hero section (nav, promo bar, trust marquee, services grid, stats dark section, before/after gallery, testimonials, promo callout, FAQ, contact form, footer, mobile bottom CTA)
- `references/css-framework.md` — Typography tokens, color system, breakpoints, vanilla JS animation toolkit
- `references/content-rules.md` — GRM voice mapping (Closing Table / Saturday Morning / Front Porch), headline patterns, CTA templates, FAQ templates per vertical
- `references/seo-geo.md` — JSON-LD schema templates, llms.txt template, meta tags, OpenGraph, lighthouse-ci spec
- `references/deployment.md` — Vercel naming convention, Static Forms wiring, migration playbook pointer
- `references/image-handling.md` — Phase 3 photo sources, Unsplash tier-4 fallback, compression, lazy loading
- `references/anti-slop-rules.md` — Negative design rules, banned fonts, banned layouts, banned phrases
- `references/example-build.md` — Worked, annotated reference page (Tucci Electric synthetic composite). Loaded by Phase 5 at generation start as a pattern-match reference showing every rule in composition.
- `references/emotional-arc.md` — Page-level emotional pacing and five personas (Quiet confidence, Earned pride, Neighborhood steady, Rescue-ready, Modern specialist). Loaded by Phase 4 for persona selection at approval, and Phase 5 to carry the persona through photo, copy, and layout decisions. NOT loaded by Phase 6 — feeling is not automatically verifiable.

Load a reference file when the phase that needs it begins. Do not load all of them upfront.

## Hard rules (read before any phase)

These rules exist because prior builds failed by ignoring them. Do not skip any of them.

1. **Crawl deeply, never shallow.** Every internal page on the prospect's homepage gets visited and parsed. Shallow rebuilds are worse than no rebuild.

2. **Capture real facts verbatim.** Real owner names, real years in business, real license numbers, real service lists with real descriptions, real testimonials with real first names and locations, real promotions with exact pricing. Never invent. Never fill gaps with generic filler.

3. **Study the visual brand by examining the actual logo file.** Before choosing colors, download the logo and run it through node-vibrant for semantic swatch analysis. Never pick colors from text scraping alone. The Johnson Brothers lesson (bright royal blue plus sun yellow, not deep navy) is the reference case.

4. **One hero structural pattern, data-driven background mode.** The hero is a Glassmorphism Trust Hero content layer over a background treatment selected by Phase 3 photo data. See Phase 4 decision tree. No vibes-based pattern selection. No "four patterns" architecture.

5. **GRM voice mapping applied to all copy.** Every headline, subheadline, service description, CTA, and FAQ gets checked against the voice rules. See `references/content-rules.md` for the full rules including the Closing Table / Saturday Morning / Front Porch section mapping. The short version lives in the Voice Summary section of this file.

6. **Silent data quality checks.** Phase 3.5 runs automated data validation. It does NOT pause for approval on clean builds. It ONLY interrupts when a hard failure is detected (missing phone, zero testimonials, missing owner names on a business where they should exist, zero photos across all sources, critical data mismatch).

7. **Every spec must be heavily specified or not exist at all.** No under-specified patterns. No "this section is optional, wing it." If a section is in the skill, it gets at least 30 lines of pixel-level spec in `references/hero-patterns.md` or `references/section-patterns.md`.

8. **Never reference components that don't exist.** All components referenced in this skill have been verified to exist (either in `~/grm-sites-prospects/plan-b-reference/magicui/` or in Cowork's research notes). No phantom components like "Bundui Hero Section" which was referenced in v0.1 through v0.6 and never actually existed on 21st.dev.

9. **Magic MCP is permanently dead.** All components are hand-rolled in plain HTML/CSS/JS or extracted directly from `plan-b-reference/magicui/`. The skill does NOT attempt to call any MCP server for component code.

10. **No em dashes anywhere.** GRM house rule. Use commas or periods. The skill includes a pre-deploy grep check for em dashes in both UTF-8 and HTML-entity encodings.

## Phase 0 — Pre-flight integrity check

Goal: fail fast before any Phase 1+ work begins. Better to spend 10 seconds verifying integrations than 30 minutes diagnosing why Phase 5 broke. Phase 0 runs before every prospect build, no exceptions.

Phase 0 has two check categories: hard checks (any failure blocks Phase 1 from starting) and soft checks (failures log a warning but the build continues). The split exists because some integrations are mission-critical (Vercel CLI auth, Node.js version) while others are deferred or optional for Composer (HubSpot pipeline configuration is on the punch list but not yet complete; backup is a v0.8 Scale (deferred) target).

### Hard checks (must all pass before Phase 1 begins)

For each check, verify the condition and report status. If any check fails, stop immediately and report the specific failure to Ron with the recovery instruction. Do not proceed to Phase 1 until all hard checks pass.

1. **Vercel CLI authenticated on the correct team scope.**
   - Verify: `vercel whoami` returns Ron's identity AND `vercel teams ls` shows `ron-7323` as accessible AND the active team is `ron-7323` (not the older `team_KCAi5VnxkXE0c5ERJWOb7jXE` where the legacy `website` project lives).
   - On failure: report "Vercel CLI not authenticated on ron-7323 team. Run `vercel login` and then `vercel switch ron-7323`."
   - Why this matters: the Vercel team scope issue documented in `deployment.md` and `LESSONS.md` produces silent deployment failures if the CLI is on the wrong team.

2. **Node.js v24+ at a resolvable path.**
   - Verify: `node --version` returns v24 or higher AND `which node` returns a real path (typically `/usr/local/bin/node` on Intel Macs or `/opt/homebrew/bin/node` on Apple Silicon Macs).
   - On failure: report "Node.js not at expected version. The skill requires Node v24+ for sharp and node-vibrant compatibility. Current version: [detected]. Upgrade Node.js and retry."
   - Why this matters: image processing in `image-handling.md` (sharp resizing, AVIF generation) and color extraction (node-vibrant against the prospect's logo) both depend on a recent Node.js version.

3. **Working directory exists with the right structure.**
   - Verify: `~/grm-sites-prospects/` exists AND `~/grm-sites-prospects/plan-b-reference/magicui/` exists AND `~/grm-sites-prospects/plan-b-reference/anthropics-skills/` exists.
   - On failure: report "Working directory or Plan B reference library missing. Recovery: `mkdir -p ~/grm-sites-prospects/plan-b-reference/magicui` and re-clone the reference library from the documented source."
   - Why this matters: Plan B is the active component source while Magic MCP is broken (per `LESSONS.md` integration entry). Without it, Phase 5 cannot generate components.

4. **All skill files present at the install path.**
   - Verify: `~/.claude/skills/prospect-site/SKILL.md` exists AND every file in `~/.claude/skills/prospect-site/references/` is present (10 reference files: hero-patterns.md, section-patterns.md, css-framework.md, content-rules.md, image-handling.md, seo-geo.md, deployment.md, anti-slop-rules.md, scale-architecture.md, LESSONS.md).
   - On failure: report "Skill installation incomplete. Missing files: [list]. Re-install the skill from the grm-automations repo."
   - Why this matters: the skill files reference each other constantly. A missing file produces silent broken behavior in whichever phase tries to load it.

5. **.env file present with required keys.**
   - Verify: `~/grm-sites-prospects/.env` exists AND contains `GOOGLE_PLACES_API_KEY=` (with a non-empty value) AND contains `UNSPLASH_ACCESS_KEY=` (with a non-empty value).
   - On failure: report "Required API keys missing from ~/grm-sites-prospects/.env. The skill needs GOOGLE_PLACES_API_KEY for Phase 3 photo collection and UNSPLASH_ACCESS_KEY for Phase 3 stock fallback. Add the keys and retry."
   - Static Forms key is hardcoded in `deployment.md` (`sf_e0e200934d4f36c17a10d00c`) and does not need to be in .env.

6. **Disk space adequate for the build.**
   - Verify: at least 500MB free in the volume hosting `~/grm-sites-prospects/`.
   - On failure: report "Insufficient disk space. The skill needs at least 500MB free for raw HTML capture, image downloads, and the 9-file-per-photo image pipeline output. Free up space and retry."
   - Why this matters: a single prospect build can produce 100-300MB of intermediate files (raw HTML, downloaded images at multiple sizes, AVIF/WebP/JPEG outputs). Running out of disk mid-build leaves the prospect folder in a half-built state that requires manual cleanup.

7. **Prospect URL is reachable.**
   - Verify: `curl -I -L --max-time 10 [prospect-url]` returns a 200 or 301/302 redirect chain ending in 200.
   - On failure: report "Prospect URL not reachable. Verify the URL is correct and the site is online before starting Phase 1."
   - Why this matters: Phase 1 deep capture cannot proceed against an unreachable site. Catching this in Phase 0 saves several minutes of failed Phase 1 attempts.

### Soft checks (warn but continue)

These checks log a warning to the build report but do not block Phase 1. They are tracked for future v0.8 Scale (deferred) hardening when the underlying integration becomes mission-critical.

1. **HubSpot pipeline configured.**
   - Verify: HubSpot API token is present in environment variables AND the GRM web services pipeline exists with the expected stages.
   - On soft fail: warn "HubSpot pipeline not configured. The skill will not auto-create a deal record on Phase 8. Manual HubSpot entry required after deployment. HubSpot setup is tracked in the Technical debt inventory section of `scale-architecture.md`."
   - Why soft: HubSpot setup is on the punch list per `scale-architecture.md` but not yet complete. The skill should not block Phase 1 just because HubSpot isn't ready.

2. **Automated backup running.**
   - Verify: a recent backup of `~/grm-sites-prospects/` exists (less than 24 hours old) at the backup destination.
   - On soft fail: warn "No recent automated backup found. Per scale-architecture.md, profile.json files are the core institutional asset of GRM and backup must be running before active client count exceeds 5. This warning becomes a hard check at v0.8 Scale (deferred)."
   - Why soft: backup is a v0.8 Scale (deferred) target. Pre-Scale builds will not have backup running and the warning is informational, not blocking.

3. **Google Places API lightweight test call.**
   - Verify: a single test call to Google Places API (e.g., a Text Search query for a known Ocala business) returns a 200 response with valid JSON.
   - On soft fail: warn "Google Places API test call failed. Phase 3 photo collection may degrade to Instagram and Unsplash fallback sources. Check API key validity and Google Cloud billing status via the GCP console."
   - Why soft: Phase 3 has documented fallback paths if Google Places fails (Instagram scraping and Unsplash stock). The skill can continue with degraded photo sources and still produce a valid build, though the photo quality may be lower.

### Phase 0 output report

Phase 0 always produces a report block at the end, even when all checks pass. The report goes into the build log so future Phase 8 LESSONS.md appends have context for any unusual conditions.

```
Phase 0 — Pre-flight integrity check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hard checks:
  ✓ Vercel CLI on ron-7323 team
  ✓ Node.js v24.14.0 (path verified via `which node`)
  ✓ Working directory and Plan B reference library
  ✓ Skill files complete (11 of 11)
  ✓ .env keys present
  ✓ Disk space: 4.2GB free
  ✓ Prospect URL reachable: 200

Soft checks:
  ⚠ HubSpot pipeline not configured (technical debt)
  ⚠ No recent backup found (v0.8 Scale deferred)
  ✓ Google Places API test call succeeded

Phase 0 PASSED. Proceeding to Phase 1.
```

If any hard check fails, the report ends with `Phase 0 FAILED.` instead of `Phase 0 PASSED.` and Phase 1 does not begin.

### When Phase 0 can be skipped

Almost never. Phase 0 is fast (under 15 seconds typically, dominated by the prospect URL curl and the API test calls) and catches problems that would otherwise waste minutes or hours of debugging in later phases. Skipping Phase 0 is only justified when:

1. Ron is running a known-good build immediately after a successful previous build (less than 30 minutes since the last successful Phase 0)
2. Ron is intentionally testing a Phase 1+ recovery scenario and wants to bypass Phase 0
3. A Phase 0 hard check is producing a known false negative that has been documented

In all three cases, the skip must be explicit: Ron passes a `--skip-phase-0` flag to the skill invocation. Silent skips are not allowed. Every skip is logged to the build report so the LESSONS.md entry (if any) has the context.

### Cross-references

- The Vercel team scope issue is documented in `deployment.md` (Phase 7 preconditions) and `LESSONS.md` (deployment entry)
- The HubSpot pipeline status is tracked in the Technical debt inventory section of `scale-architecture.md`
- The Magic MCP / Plan B reference library status is tracked in the Risk inventory section of `scale-architecture.md` and in `LESSONS.md` (integration entry)
- Backup architecture rationale lives in the Data preservation as an architectural principle section of `scale-architecture.md`
- Hard check failure recovery procedures are detailed in `deployment.md` (Common Phase 7 failures section, applicable to Phase 0 too)

## Phase 1 — Homepage deep capture

Goal: capture everything visible and structural on the prospect's homepage, including the raw logo for color analysis.

Steps:

1. Create the prospect folder: `~/grm-sites-prospects/[business-slug]/` where `business-slug` is the business name lowercased with spaces replaced by hyphens. Create `raw/` and `assets/` subfolders.

2. Fetch the homepage HTML with a desktop user agent. Save to `raw/homepage.html`.

3. Parse the homepage and extract: business name, tagline, phone number (note if tel:-linked), email, address, hours including emergency availability, primary logo URL, CSS color tokens from linked stylesheets, font families, hero image URL if any, list of internal navigation links (this becomes the Phase 2 crawl list), all inline image URLs with alt text, social media links, footer credentials.

4. Download the logo file to `assets/logo.[ext]`. If the logo is SVG, use sharp to convert a PNG copy at `assets/logo.png` for node-vibrant analysis.

5. Run node-vibrant on `assets/logo.png`. Capture the six semantic swatches (Vibrant, DarkVibrant, LightVibrant, Muted, DarkMuted, LightMuted). Save to `profile-draft.json` under `brandPalette` with role mapping: Vibrant becomes `primary`, DarkVibrant becomes `darkPrimary`, LightVibrant becomes `accent`, Muted becomes `neutral`, LightMuted becomes `background`.

6. Set `designChoices.heroBackground` from the warm/cool temperature of `brandPalette.primary`. Warm brands get cream (`#faf7f2`). Cool brands get cool-white (`#f4f7fa`). Neutral brands default to cream.

7. Report to Ron: what was captured, any obvious gaps, and the brandPalette preview.

## Phase 2 — Multi-page crawl

Goal: capture every internal page so the rebuild matches or exceeds the prospect's current site depth.

Steps:

1. Take the nav link list from Phase 1, filter to same-domain URLs, add common paths if missing (`/about`, `/services`, `/testimonials`, `/contact`, `/gallery`).

2. For each internal URL, fetch the HTML with a desktop user agent, save to `raw/[page-slug].html`, parse, extract structured data per page type:

   - **About page:** owner names, years in business, team bios, credentials, certifications, license numbers, mission or values
   - **Services pages:** full service list with names and descriptions. If services have sub-pages, visit each one. Do not collapse a 12-service list to 6.
   - **Testimonials page:** every testimonial with reviewer's real first name (or first name + last initial), city if shown, full quote text verbatim. Never use "Happy Customer" as a name.
   - **Gallery page:** every project image URL with captions and before/after labels
   - **Contact page:** all phone numbers, emails, service area cities, form fields
   - **Specials or promotions page:** any featured offer with exact wording and exact pricing

3. **Review source verification rule.** If the prospect's site mentions HomeAdvisor, Angi, Yelp, BBB, or other review sources, verify the link works and the numbers are real before capturing. Never fabricate review source references the prospect does not actually have.

4. Save extracted data to `profile-draft.json` as you go.

5. Report to Ron: pages crawled, services captured, testimonials captured (with name list), owner names, featured promotion, any gaps.

## Phase 2.5 — Pre-migration SEO audit

Goal: capture the prospect's current SEO footprint before any rebuild so the post-signing migration preserves their Google equity.

This phase is additive only. It does not modify anything captured in Phase 2. Output goes to `profile-draft.json` under `migrationData`.

Steps:

1. Run `site:theirdomain.com` Google search to inventory indexed pages. Capture the URL list.
2. Check Wayback Machine for archived snapshots. Note any historically indexed pages not in the current site.
3. Build initial URL inventory for the migration redirect map.
4. Save to `migrationData.indexedUrls`, `migrationData.archiveSnapshots`.
5. If any step fails (Google blocks the query, Wayback unavailable), log the failure and continue. Migration will require manual URL discovery later.

For the full 8-step migration workflow, see the GRM Migration Playbook document. This phase is only capture, not execution.

## Phase 3 — Photo collection and curation

Goal: collect the best possible photo inventory for the build, from multiple sources in priority order.

For detailed source handling, quality scoring, and Unsplash fallback logic, see `references/image-handling.md`. Short version here:

Sources, in priority order:

1. **Google Places API.** Primary source. Pull up to 10 photos from the prospect's Google Business Profile with attribution. Save to `assets/photos/google/`. Capture photographer attribution for the footer.

2. **Prospect's own website.** Scrape images from Phase 1 and Phase 2 HTML. Save to `assets/photos/site/`. Filter for watermark-free, logo-free, high-resolution only.

3. **Instagram.** If a handle was provided in the command or captured in Phase 1, attempt to pull 6 to 12 recent public posts. Save to `assets/photos/instagram/`.

4. **Unsplash API (tier-4 fallback).** If tiers 1 through 3 produced fewer than 4 usable photos, query Unsplash with service-category keywords. Save to `assets/photos/unsplash/`. Attribution required in footer.

After collection, run the quality evaluation in `references/image-handling.md` and tag every photo with: `contentType` (finished_work, team, owner, jobsite, stock, unknown), `orientation` (landscape, portrait, square), `longEdgePx`, `disqualifiers` (watermark, logo, text, blurry, dark, low_res).

Then auto-assign photos to positions in `photoAssignments`:

- `heroCandidates`: top 8 landscape finished_work photos, ranked by quality
- `ownerPortrait`: first photo with contentType=owner, if any
- `servicesGridPhotos`: next 6 to 12 landscape photos tagged by service category
- `galleryPhotos`: remaining quality photos

Report to Ron: photo counts by source, heroCandidates count, ownerPortrait yes/no, services coverage.

## Phase 3.5 — Silent data quality gate

Goal: catch hard data failures before Phase 4 wastes time on design decisions built on broken inputs.

This phase runs automatically. It does NOT pause for Ron's approval on clean builds. It ONLY interrupts when one or more hard failures are detected.

Hard failures (interrupt the build):

- No phone number captured in Phase 1 or Phase 2
- Zero testimonials captured with real names
- Zero photos across all four sources in Phase 3
- Owner names not found on a business that should have them (About page exists but names absent)
- Review count mismatch across sources greater than 20% (e.g., site claims 500 reviews but Google Places shows 41)
- Service list contains fewer than 3 real services
- Business name mismatch between Phase 1 capture and command argument

Soft warnings (logged but do not interrupt):

- Hero candidate count below 4 (triggers photo-poor hero mode in Phase 4, expected behavior)
- No featured promotion captured
- No license number found
- No service area cities beyond the primary city

On hard failure, report the specific failure to Ron with captured context and wait for instruction: fix manually, skip the prospect, or override and continue.

On clean pass, proceed directly to Phase 4 without pausing.

## Phase 4 — Design engine, scoring, hero mode selection, approval gate

Goal: score the prospect's current web presence, select the hero mode from a deterministic decision tree, stage the build plan, and get Ron's approval.

### Scoring rubric

Score across five categories, each worth 20 points, total out of 100:

- **Copy Language (0-20):** Headlines specific and benefit-driven or generic? Grammar issues?
- **Visual Quality (0-20):** Photos professional? Palette intentional? Logo clean?
- **Business Maturity (0-20):** Review count? Years in business? Team bios? Certifications?
- **Site Sophistication (0-20):** Mobile-responsive? Loads under 3 seconds? Looks 2025 or 2010?
- **Brand Intentionality (0-20):** Consistent logo? Defined palette? Clear voice?

### Tier assignment (affects copy depth, not hero mode)

- **Premium (70-100):** Full feature set, heavy trust content, all stats populated, category-specific FAQ
- **Professional (40-69):** Standard feature set, selective trust content, focus on clarity
- **Standard (0-39):** Minimal feature set, simple layouts, focus on hierarchy and CTA prominence

### Hero mode decision tree (deterministic, data-driven)

```
IF phase3.videoUrl exists:
    videoAugmentation = true   (adds Hero Video Dialog section below main hero)

IF photoAssignments.heroCandidates.length >= 8
   AND all top 8 photos are landscape orientation
   AND all top 8 photos are at least 1600px on long edge
   AND zero photos have disqualifiers:
    heroMode = "parallax"            (Hero Parallax grid as main hero)
ELIF photoAssignments.heroCandidates.length >= 4:
    heroMode = "glass-crossfade"     (Glass card over full-viewport cross-fade slideshow)
ELIF photoAssignments.heroCandidates.length >= 1:
    heroMode = "glass-single-mesh"   (Glass card over single photo with mesh gradient overlay)
ELSE:
    heroMode = "glass-pure-mesh"     (Glass card over pure mesh gradient with mousemove parallax)
```

No vibes. No operator override inside the decision tree. Ron can override the final output at the approval gate, but the tree itself runs deterministically.

### Glass card variant selection (deterministic, data-driven)

After the hero mode is chosen, Phase 4 selects the glass card size variant from two structural conditions:

```
useWideVariant = false

IF heroMode == "parallax":
    useWideVariant = true
IF tier == "Premium" (score 70-100):
    useWideVariant = true

designChoices.heroGlassVariant = useWideVariant ? "wide" : "default"
```

**Why these two conditions:**

- **Parallax mode:** The rotated photo grid background can absorb the extra card weight. Other modes risk feeling top-heavy with the wide variant.
- **Premium tier:** Section density scales with tier per typography.md Appendix B. Wide-variant is the hero-end expression of that density — Premium tier carries it as part of the tier's density treatment (palette complexity + section density + motion layer + photographic treatment, per Appendix B). The selection stays tier-keyed because density differentiation lives on the tier axis.

**Editorial override:** Character count intentionally does NOT trigger the wide variant automatically. Some editorial headlines are 50+ characters and read beautifully at 56px in the default card; some short headlines need the wide variant for tier reasons; the auto-rule would get this wrong both directions. The approval gate accepts `override glass-variant:wide` or `override glass-variant:default` so Ron picks per-prospect when the structural defaults don't match his eye.

Save `designChoices.heroGlassVariant` to `profile-draft.json`. Phase 5 applies the `hero-glass-card--wide` modifier class when this value is "wide". Full spec in `references/hero-patterns.md`.

### Approval gate output

Show Ron a single-screen summary:

```
Design Analysis Complete
━━━━━━━━━━━━━━━━━━━━━━
Score: [XX]/100 ([Tier] Tier)

Breakdown:
  Copy Language: [X]/20, [one line]
  Visual Quality: [X]/20, [one line]
  Business Maturity: [X]/20, [one line]
  Site Sophistication: [X]/20, [one line]
  Brand Intentionality: [X]/20, [one line]

Key facts captured:
  Owners: [names or "not found"]
  Years in business: [number]
  Services captured: [count]
  Testimonials captured: [count]
  Featured promotion: [text or "none"]
  License: [number or "not found"]
  Google reviews: [rating]/5 from [count] reviews
  Photo inventory: [count] heroCandidates, [count] servicesGridPhotos

Design plan:
  Tier: [Premium/Professional/Standard]
  Hero mode: [parallax/glass-crossfade/glass-single-mesh/glass-pure-mesh]
  Glass card variant: [default/wide]
  Video augmentation: [yes/no]
  Brand colors: primary [hex], accent [hex] (from logo node-vibrant analysis)
  Typography: [heading font] / [body font]

Headline candidate:
  Pattern: [A / B / C / D / E]
  Headline: [generated candidate in Closing Table voice]
  Subheadline: [generated candidate in Closing Table voice]

Proceed? (yes / revise / override hero-mode:[mode] / override glass-variant:[default|wide] / try Pattern [A|B|C|D|E] / custom: [your headline])
```

Wait for explicit `yes` or override instruction. Only proceed to Phase 5 after approval.

If `--auto` was passed in the command, skip the gate and proceed automatically.

### Editorial choices (deterministic + declared at Phase 4)

Five editorial decisions that were previously implicit inside Phase 5 are now explicit at Phase 4 so Ron can review them at the approval gate before generation runs. The persona is selected first because it biases the other four.

**0. Emotional persona (pick one; biases all subsequent choices).**

Load `references/emotional-arc.md`. Select the persona using the three-input priority from that file:

```
1. Captured copy tone — if prospect's existing site copy reads distinctly as one persona, use it.
2. Tenure + trade — 20+ years biases Neighborhood steady; 10+ years + strong portfolio biases Earned pride.
3. Trade-category default mapping — see emotional-arc.md for full table.
Default when unclear: Quiet confidence.
```

Write to `profile-draft.json.design.persona` as one of: `quiet-confidence`, `earned-pride`, `neighborhood-steady`, `urgent-service`, `modern-specialist`.

The persona biases the signature micro-interaction selection (via the tie-breaking column in emotional-arc.md) and the editorial-layouts weighting (heavy/medium/light priority per persona). It does NOT change the hero mode (hero mode remains structural, data-driven from photo library).

**1. Signature micro-interaction (pick exactly one, site-wide).**

Selection uses only signals already captured by Phase 1-4 (tier, hero mode, service count). More nuanced signals (logo character, stats content type) were considered but rejected because they require pipeline extractions that don't currently exist; adding them is tracked as a future enhancement but the tree deliberately stays within captured data.

Phase 4 emits two signature outputs on every composition plan:

- `site.signatureMicroInteraction`: singular, one of the six-value Tier 1 enum (`italic-color-shift`, `watermark-numeral-offset`, `anchor-strip-pivot`, `hero-glass-blur`, `stat-row-ledger`, `none`). Never null.
- `site.microInteractions`: array, zero or more from the four-value Tier 2 enum (`eyebrow-reveal`, `underline-bloom`, `shimmer-hero-cta`, `mono-numeral-flip`). May be empty.

**Tier 1 resolution** (always emits one value):

1. If hero mode from `hero-patterns.md` decision tree is `parallax` or `glass-crossfade` AND tier is Premium AND heroBackground count ≥ 4 → `hero-glass-blur`.
2. Else if page carries `statRow` AND persona is rescue-ready OR (persona is earned-pride AND stat values include tenure ≥ 10 years) → `stat-row-ledger` (rescue-ready) or `watermark-numeral-offset` (earned-pride).
3. Else if persona is modern-specialist AND page has ≥ 5 sections → `anchor-strip-pivot`.
4. Else if persona has `italic-color-shift` in its Tier 1 default (quiet-confidence, neighborhood-steady) AND at least one italicPlacement-eligible string exists in profile → `italic-color-shift`.
5. Else fall to persona Tier 1 default from `emotional-arc.md` table.
6. Else `none`.

**Tier 2 resolution** (may emit empty array):

Start from persona Tier 2 default. Then apply additive rules:

- If hero carries sectionOpener pattern AND persona default does not already include `eyebrow-reveal` → append `eyebrow-reveal` (except quiet-confidence, which resists all Tier 2 additions without explicit override).
- If page has ≥ 3 inline body links in long-form copy AND persona is modern-specialist or earned-pride → ensure `underline-bloom` present.
- If `statRow` is present AND persona is modern-specialist → ensure `mono-numeral-flip` present.
- If tier is Premium AND persona is earned-pride AND Phase 4 rationale includes "CTA prominence critical" → `shimmer-hero-cta` may be appended with `microInteractionsReason` recording the override. Otherwise `shimmer-hero-cta` is not emitted.
- Rescue-ready Tier 2 entries all run at 250ms entry; record in `microInteractionDurations.entry: 250`. See emotional-arc.md "Micro-interaction duration lock (persona-indexed)" for the full two-row table.

**Tie-breaking:** persona defaults from `emotional-arc.md` break any ambiguous resolution. If tree rules produce no Tier 1 value, emit persona default; if still none, emit `none`. Tier 2 array empty is valid output, not a missing-value error.

**Output recording:** Phase 4 records `signatureMicroInteractionReason` (string) naming which rule fired. `microInteractionsReason` (string) names additive rationale when the array differs from persona default.

Write Tier 1 output to `composition-plan.site.signatureMicroInteraction` (singular, from the six-value enum at composition-plan-schema.md §2.1). Write Tier 2 output to `composition-plan.site.microInteractions` (array, zero or more from the four-value enum at composition-plan-schema.md §2.2). The retired `profile-draft.json.design.signatureMicroInteraction` path is no longer emitted — Phase 4 produces composition-plan.json, not profile-draft.json.

Authority for full definitions is split by tier:

- Tier 1 compositional signatures (`italic-color-shift`, `watermark-numeral-offset`, `anchor-strip-pivot`, `hero-glass-blur`, `stat-row-ledger`, `none`) are typographic/compositional treatments — full definitions live in `references/typography.md §3 Role classes`.
- Tier 2 motion micro-interactions (`eyebrow-reveal`, `underline-bloom`, `shimmer-hero-cta`, `mono-numeral-flip`) are motion primitives — full definitions live in `references/css-framework.md` under the Motion Restraint section.

Record Phase 4 rationale on `signatureMicroInteractionReason` (Tier 1) and `microInteractionsReason` (Tier 2 additive rationale when array differs from persona default).

**2. Editorial layouts per page (minimum three, maximum five distinct layouts per page).**

Phase 4 selects which three-to-five of the five editorial layouts (A: offset headline, B: image-bleed, C: 70/30 split, D: full-bleed, E: watermark numeral) will appear on the homepage. Full-bleed (D) is included only if a hero-plate quality photo is available (Phase 3 tagged at least one photo as `heroPlate` in addition to the hero background plate). Watermark numeral (E) is included only if the page has at least one numbered sequence (stats cells, a 3-step process block, or numbered service tiers).

```
editorialLayouts = ["A"]  (always — offset headline on FAQ)
IF hasSecondaryHeroPhoto: editorialLayouts.push("D")  (one full-bleed per page max)
IF services.length >= 4: editorialLayouts.push("C")   (70/30 split on featured promo or contact)
IF hasDetailShot: editorialLayouts.push("B")          (image-bleed divider)
IF hasNumberedSequence: editorialLayouts.push("E")    (watermark numeral on stats or process)

Minimum 3. If fewer than 3 are selected by the rules above, add layouts in priority order (A, C, B, E, D) until minimum is met OR declare the shortfall at the approval gate and let Ron authorize a centered-only build.
```

Write to `profile-draft.json.design.editorialLayouts` (array of layout ids).

**3. Hero plate assignment (for Layout D, if selected).**

If Layout D will appear on the page, Phase 4 names the specific photo filename from the library that fills the full-bleed. The photo must be Phase 3 role-tagged `heroPlate` and must NOT be the same photo that renders behind the main hero glass card.

```
IF "D" in editorialLayouts:
    fullBleedPhoto = first photo in library where:
        role == "heroPlate"
        AND filename != heroBackgroundPhoto
        AND score >= 75
    IF none qualify: remove "D" from editorialLayouts; note to Ron at approval gate
```

Write to `profile-draft.json.design.fullBleedPhoto` (filename or null).

**4. Watermark numeral targets (for Layout E, if selected).**

If Layout E will appear, Phase 4 names which section uses the watermark numeral treatment — stats, a 3-step process block, or numbered service tiers. Default: stats cells (01/02/03/04 outlined numerals behind stat values).

```
IF "E" in editorialLayouts:
    watermarkTarget = "stats" | "process" | "service-tiers"  (first match wins in that order)
```

Write to `profile-draft.json.design.watermarkTarget`.

### Updated approval gate output

The approval gate summary adds four lines under `Design plan:`:

```
  Emotional persona: [Quiet confidence | Earned pride | Neighborhood steady | Rescue-ready | Modern specialist]
  Signature micro-interaction: [italic-color-shift | underline-bloom | shimmer-hero-cta | eyebrow-reveal | mono-numeral-flip]
  Editorial layouts (page): [A, C, E] (minimum 3)
  Full-bleed photo: [filename or "none"]
  Watermark numeral target: [stats | process | service-tiers | "none"]
```

And three new override instructions Ron can invoke:

- `override persona:[name]` — swap the emotional persona (recomputes signature and layout weighting)
- `override signature:[name]` — swap the signature micro-interaction
- `override layouts:[A,B,C]` — manually select the editorial layouts

### Over-constraint escape hatch

The editorial rules interlock: minimum 3 layouts, scale contrast ≥5x, ≤12 accent appearances, one signature used site-wide, every non-hero photo captioned, one hero-weight photo per section. For most builds these compose cleanly. For a small set of prospects (weak photo library, sparse content, very short service list) the rules may be jointly unsatisfiable.

Phase 4 detects over-constraint BEFORE the approval gate renders:

```
constraintsOK = true
reasons = []

IF editorialLayouts.length < 3 AND no fallback layouts can be added:
    constraintsOK = false
    reasons.push("Cannot reach 3-layout minimum: insufficient photos for B, no numbered sequence for E")

IF tier == "Standard" AND "E" not in editorialLayouts AND no other ≥80px display moment possible:
    constraintsOK = false
    reasons.push("Computed hero size (persona × tier) falls below 80px scale-contrast threshold without Layout E")

IF photoLibrary.accepted.length < 4:
    constraintsOK = false
    reasons.push("Photo library too sparse for one-hero-per-section + role hierarchy")

IF services.length < 3:
    constraintsOK = false
    reasons.push("Services grid needs minimum 3 services for Bento layout")
```

If `constraintsOK` is false, the approval gate adds a "Constraint conflicts" block above `Proceed?`:

```
Constraint conflicts detected:
  - [reason 1]
  - [reason 2]

Available responses:
  - relax contrast: drop scale-contrast threshold to 4x for this build
  - relax layouts: accept fewer than 3 editorial layouts (centered-stacked fallbacks)
  - relax captions: accept uncaptioned detail/texture shots
  - relax accent-cap: accept up to 15 accent appearances
  - pause: halt build and return to Phase 3 for manual photo upload
```

Ron picks one relaxation or escalates to manual content supplementation. The relaxations write to `profile-draft.json.design.constraintRelaxations` as an array so Phase 6 knows to skip the corresponding check rather than failing the build.

**The rules are not suggestions — but they are not a suicide pact either.** Phase 4 surfaces conflicts explicitly and lets Ron choose which constraint to trade off for the specific build. Silent relaxation is banned; every skipped check is logged in the build report.

## Phase 5 — Site generation

Goal: build the multi-page website using the GRM house style and the selected hero mode.

For the hero pixel-level CSS (all four modes, shared glass card, video augmentation), see `references/hero-patterns.md`. For every non-hero section (nav, promo bar, trust marquee, services grid, stats dark section, before/after gallery, testimonials, promo callout, FAQ, contact form, footer, mobile bottom CTA bar), see `references/section-patterns.md`. SKILL.md contains only the high-level section order and hard rules.

For voice assignment per zone, load `references/voiceMap.md` BEFORE generating any copy in any zone. voiceMap.md is the authoritative source for zone-to-voice mapping under the three-voice contractor system (Closing Table / Saturday Morning / Front Porch), keyed by section and persona. Phase 4's selected persona feeds the voice mapping decision per zone. `references/content-rules.md` provides the headline patterns, CTA templates, FAQ templates per vertical, and banned phrases that fill in once voice is assigned. The two files compose: voiceMap.md decides which voice each section uses, content-rules.md provides the patterns that voice writes against.

### Required pages

- `index.html` — Homepage
- `about.html` — About the company and owners
- `services.html` — Full services list
- `testimonials.html` — Reviews and testimonials
- `contact.html` — Contact info and form

### Optional pages (include only if data supports)

- `gallery.html` — Include if 6+ quality project images captured
- `specials.html` — Include if a real featured promotion was captured
- `emergency.html` — Include if 24/7 emergency service is a major differentiator

### Service sub-pages (conditional, generated per service)

Some prospects have dedicated sub-pages for specific services (T&F Electric has seven: Residential, Commercial, Industrial, Generators, Panel Upgrades, Surge Protection, Landscape Lighting). Phase 5 generates a service sub-page at `services/[service-slug].html` IF all three conditions are met for that service:

1. The prospect's existing site has a dedicated page for that service (not just a section on the main services page)
2. Phase 2 captured at least 250 words of original content from that page (not boilerplate, not duplicated from homepage or main services page)
3. At least ONE of: a unique photo for this service, a unique testimonial specifically mentioning this service, pricing or package info specific to this service, or process details the main services page does not cover

If all three conditions hit, generate the sub-page. If any fails, roll the service into the homepage services grid card without generating a sub-page. This rule honors "never fabricate" — we only build depth when the prospect already has it.

**Sub-page structure:** simpler than the homepage. Nav, sub-hero (single section with headline, subheadline, photo, and CTAs), main content block (300-800 words from Phase 2 capture), service-specific testimonials if captured, service-specific FAQ (3-5 questions), contact CTA callout linking to `/contact.html`, footer. Full structural spec and voice mapping in `references/content-rules.md` under "Standalone pages and service sub-pages."

**Pages explicitly out of scope:** location sub-pages (Ocala Electrician, Dunnellon Electrician as separate pages), blog and news pages, financing pages as standalone (content rolls into homepage promo callout instead), warranty and insurance pages as standalone (content rolls into homepage FAQ and trust marquee), separate team pages (content rolls into about.html), project portfolio pages (use gallery.html). When Phase 2 captures these page types, Phase 5 either ignores them or rolls their content into existing homepage sections per the decision table in `references/content-rules.md`.

### Homepage section order (build in this order)

1. Sticky nav with click-to-call
2. Promo bar (if real promotion captured)
3. Hero (selected mode from Phase 4 decision tree)
4. Trust marquee (if real credentials captured)
5. Services grid (asymmetric Bento layout with one featured service)
6. **Stats section as dark section** (this is the mandatory dark section, placed here for visual rhythm)
7. Before/after gallery (only if before/after images captured)
8. Testimonials
9. Featured promotion callout (if real promotion captured)
10. FAQ accordion
11. Contact form
12. Footer
13. Mobile bottom CTA bar (mobile only, sticky)

### Hard rules for Phase 5

- Every CTA button says something specific. Never "Learn More" or "Click Here".
- Every testimonial includes a real first name and location.
- Every service description is 1 to 2 sentences, benefit-first.
- Every number is real. Never invented.
- Every photo is from `assets/photos/` subfolders. Never hotlinked.
- The stats section ALWAYS uses the dark treatment. This is non-negotiable and gives every flagship the mandatory visual rhythm reset.
- Every section gets the Glare Hover, Shimmer Button, or other Magic UI enhancement specified in `references/css-framework.md` where appropriate.
- Run the anti-slop rule check from `references/anti-slop-rules.md` on all generated copy and CSS before writing files.

### Cross-file integration points

Phase 5 must wire up the following connections between the reference files. These are the "glue" that makes css-framework.md, hero-patterns.md, and section-patterns.md work together. Missing any of them will produce broken output.

**1. Persona class on `<html>` element.**
Phase 5 applies exactly one persona class to the `<html>` element based on the persona decision from Phase 4:

```html
<html lang="en" class="persona-quiet-confidence">
<!-- or persona-earned-pride / persona-neighborhood-steady / persona-urgent-service / persona-modern-specialist -->
```

The class is an identifier hook — developer-tools visibility and a reserved extension point for any future persona-specific CSS rules that aren't expressible through custom properties. It does NOT drive cascade overrides; all persona-conditional values (fonts from `CONFIG.fonts`, spacing from `CONFIG.spacing` persona-base × tier-multiplier) are resolved at Phase 5 build time and written directly into the base `:root` block. The pre-Composer `.tier-premium` / `.tier-professional` / `.tier-standard` cascade-override class system retired in Stage II (e). If the persona class is missing, custom properties still render correctly (they're emitted inline); what's lost is the dev-tools-visible identifier.

**2. `data-reveal` attribute on major sections.**
Phase 5 adds `data-reveal` as an attribute on the top-level element of every major section:

```html
<section class="services-section" data-reveal>
<section class="stats-section" data-reveal>
<section class="testimonials-section" data-reveal>
```

The `scrollReveal` utility from `css-framework.md` uses `IntersectionObserver` to watch for these elements and add a `.revealed` class when they scroll into view, triggering the fade-up animation. Sections without `data-reveal` will not animate in — they will be visible on page load with no transition, which is fine for the nav and hero but wrong for content sections below the fold.

**Apply `data-reveal` to:** services-section, stats-section, testimonials-section, beforeafter-section, promo-callout, faq-section, contact-section, hero-video-augment. **Do NOT apply to:** nav, promo-bar, hero (any mode), trust-marquee, footer, mobile-cta-bar.

**3. `window.BA_PAIRS` global array for before/after thumbnail navigation.**
If the before/after gallery renders, Phase 5 writes an inline `<script>` block in the `<head>` of the homepage with the pair data as `window.BA_PAIRS`:

```html
<script>
window.BA_PAIRS = [
  { before: "assets/photos/before/01.jpg", after: "assets/photos/after/01.jpg", caption: "Kitchen rewire, Ocala" },
  { before: "assets/photos/before/02.jpg", after: "assets/photos/after/02.jpg", caption: "Panel upgrade, Dunnellon" }
];
</script>
```

The `beforeAfterCompare` primitive in `css-framework.md` reads this array when a user clicks a thumbnail, swapping the background images on the compare container. If `window.BA_PAIRS` is missing, the thumbnail navigation will silently fail and only the first pair will ever display.

**Only write this script block if Phase 3 captured 2+ before/after pairs.** For a single pair, thumbnail nav is omitted entirely (see `section-patterns.md` before/after rules) and `window.BA_PAIRS` is unnecessary.

**4. Google Fonts URL from CONFIG.**
Phase 5 reads the tier-appropriate `googleFontsPath` from the CONFIG block at the top of `css-framework.md` and writes the matching `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=[path]&display=swap">` tags into the `<head>`. Do not hardcode font URLs. Read from CONFIG.

**5. Conditional JS primitive inclusion.**
Phase 5 writes `script.js` with ONLY the primitives the build actually needs. A build with no before/after gallery does not include `beforeAfterCompare` in the generated JS. A build with hero mode `glass-pure-mesh` includes `meshGradient` and `mousemoveParallax`. The master init block at the bottom of `css-framework.md` shows the conditional pattern.

**6. Phase 4 color computation utilities.**
Phase 4 runs the Node.js build-time utilities documented in `css-framework.md` under "Phase 4 build-time color utilities" to compute brand-derived token values and overwrite the sentinel defaults in the `:root` block before Phase 5 writes `style.css`. Required derivations: `--color-primary` (from node-vibrant), `--color-primary-rgb` (via `hexToRgbString()`), `--color-primary-hover` (via `derivePrimaryHover()`), `--color-accent` (from node-vibrant), `--color-accent-rgb` (via `hexToRgbString()`), `--color-dark-primary` (via `deriveDarkPrimary()`), and `--color-dark-primary-rgb` (via `hexToRgbString()`). If any of these values are not pre-computed, the magenta or neon-green sentinel defaults survive into the generated site and Phase 6 check 18 fails the build. Per `anti-slop-rules.md` Rule E6.

## Phase 5.5 — SEO and GEO injection

Goal: make the generated site findable by Google, Bing, and AI answer engines (ChatGPT, Claude, Perplexity, Gemini).

For the full schema templates and llms.txt content, see `references/seo-geo.md`. Short version:

Every page gets: LocalBusiness JSON-LD schema, Service schema for service pages, FAQPage schema on pages with FAQ, Review schema for testimonials, OpenGraph meta tags, Twitter Card meta tags, canonical URL, robots meta, sitemap.xml entry.

Every site gets: `sitemap.xml` at root, `robots.txt` at root, `llms.txt` at root (pointing AI crawlers at clean markdown versions of key pages).

Run validation: JSON-LD passes Google Rich Results Test, sitemap validates against sitemaps.org spec, llms.txt follows the AnswerDotAI spec format.

## Phase 6 — Pre-deploy verification

Goal: automated quality gates that fail the build if any check fails. No shipping broken sites. No relying on Ron's eye for things a script can verify.

Phase 6 runs eighteen checks organized into eight categories. All checks must pass before Phase 7 deploy. On any failure, log the specific failure and stop.

### Content integrity checks

1. **HTML validation.** All pages pass W3C HTML5 validation or log only minor warnings.

2. **Em dash check.** Grep all generated HTML for em dashes in both UTF-8 (`\u2014`) and HTML-entity (`&mdash;`, `&#8212;`) encodings. Fail if any found.

3. **GRM voice banned phrase check.** Grep for all banned phrases from `references/content-rules.md`. Fail if any found.

4. **Link check.** All internal links resolve. No 404s. No `href="#"` or `action="#"` placeholders.

5. **Image reference check.** All `<img>` tags reference files that exist in `assets/photos/`. No broken references. No hotlinked external images.

6. **H1 count check.** Every page has exactly one `<h1>` element. Zero H1s or multiple H1s fails the build.

7. **Mixed content check.** No `http://` references inside `<img src>`, `<link href>`, `<script src>`, or inline CSS `url()` values. All references must be `https://` or relative. Mixed content breaks the SSL padlock and can block images.

### Data integrity checks

8. **Stats counter discipline.** Every stat in the stats section is either ANIMATED (has `data-target` attribute with a whole number value) or STATIC (no `data-target` attribute, content is plain text). Mixed or malformed stats fail the build. This catches the "0 Years Licensed" broken counter bug class.

9. **Phone number consistency.** The prospect's real phone number appears in: nav bar, hero CTA, footer, contact section, and JSON-LD schema. Regex the number across all five locations and confirm exact string match. A typo in any one location fails the build.

### Structural integrity checks

10. **Dark section count.** The generated homepage contains exactly one dark-background section (the mandatory stats section from Phase 5). Zero dark sections or two-plus dark sections fail the build. This enforces the visual rhythm rule architecturally, not by convention.

11. **llms.txt existence and format.** File exists at site root, follows the AnswerDotAI llms.txt spec, contains links to clean markdown versions of key pages. Missing file or invalid format fails the build.

### Legal and attribution checks

12. **Photo attribution check.** If any photo in the build came from `assets/photos/google/`, the footer must contain the Google Places attribution string ("Photos provided by Google. Contributors: [names]"). If any photo came from `assets/photos/unsplash/`, the footer must contain photographer credits per Unsplash API Guidelines. Missing attribution is a ToS violation and fails the build.

### Form integrity checks

13. **Contact form HTML wiring.** Form action is `https://api.staticforms.xyz/submit`, accessKey hidden input is present with GRM's real key, subject hidden input contains the real business name, honeypot field is present and empty, required fields are marked correctly.

14. **Contact form live submission test.** Execute a real POST to Static Forms with a test payload whose message body contains `[BUILD TEST - IGNORE]`. Verify 200 response and successful delivery token. This catches expired keys, rate limits, and account issues before the prospect tests the form live. Failed submission fails the build.

### Schema validation

15. **Schema.org validation.** All generated JSON-LD (LocalBusiness, Service, FAQPage, Review) passes the schema.org validator. Validation errors fail the build.

### Performance and accessibility

16. **Lighthouse CI gate.** Run lighthouse-ci against the local preview build. All four thresholds must pass on mobile:
    - LCP (Largest Contentful Paint) < 2.5s
    - Performance score ≥ 85
    - SEO score ≥ 95
    - Accessibility score ≥ 90

17. **Mobile render verification at 375px.** Use headless Chrome at 375px viewport width (iPhone SE baseline) to render the homepage. Verify: no horizontal scroll, hero CTA is visible above the fold, mobile bottom CTA bar is sticky at the bottom, navigation collapses to hamburger, phone number is tappable. This is the automated backup to Ron's phone eye test (check 6 of the Six Checks done bar).

### Token integrity checks

18. **Brand-token sentinel grep.** Search the generated `style.css` for the sentinel hex values `#FF00FF` (magenta, primary-family sentinels) and `#00FF00` (neon green, accent-family sentinels). Any match indicates Phase 4 color derivation failed to overwrite the `:root` default for a brand-dependent token. Fail the build and report which token retained the sentinel. Per `anti-slop-rules.md` Rule E6.

### Helper scripts

Checks 14 (live form submission) and 17 (mobile render verification) require helper scripts that live in `scripts/`:

- `scripts/test_form_submission.py` — POSTs test payload to Static Forms, verifies response
- `scripts/mobile_render_check.py` — Playwright or Puppeteer headless Chrome at 375px, validates render

All other checks are grep, curl, or direct validator calls that run inline in Phase 6.

### On failure

Log the specific failure with file and line context. Do not deploy. Report to Ron with: which check failed, where in the generated files, recommended fix, whether the fix is automatic or requires Ron's input.

## Phase 7 — Vercel deployment

Goal: deploy the verified build to a unique Vercel URL.

Naming convention: `[business-slug]-grm.vercel.app`. Before deploying, check Vercel for name collision (`vercel projects ls`). If the name is taken, append a suffix: `[business-slug]-grm-2`, etc.

Steps:

1. Verify Phase 6 passed with all checks green. Do not deploy otherwise.
2. `cd ~/grm-sites-prospects/[business-slug]`
3. Check name availability. Determine final project name.
4. Deploy: `vercel --prod --yes --name [final-project-name]`
5. Capture the returned URL.
6. Test the URL with curl. Confirm 200 status and the business name appears in the body.
7. Report the live URL to Ron in a visible format.

For full deployment and domain migration details, see `references/deployment.md`.

## Phase 8 — Profile, LESSONS.md, done report

Goal: save complete build record, append institutional lessons, report completion.

Steps:

1. Promote `profile-draft.json` to `profile.json` with the final `previewUrl` populated.
2. If anything unusual happened during the build (unexpected data, soft warnings, recovery actions, novel photo assignment decisions), append an entry to the project-level `LESSONS.md` at `~/.claude/skills/prospect-site/LESSONS.md` in the format shown in that file.
3. Output the done report (see Output Format section below).

## GRM voice summary

These are the rules at a glance. For the full voice spec with examples and headline patterns, see `references/content-rules.md`.

**Never:** "passionate about", "dedicated to", "committed to excellence", "strive to", "In today's", "leverage", "stakeholders", "synergy", "value proposition", "one-stop shop", "your trusted partner", em dashes, exclamation points to manufacture warmth, ellipses for drama.

**Always:** specific concrete nouns over abstract categories, real place names (Ocala, Marion County, Dunnellon, Belleview, The Villages, Silver Springs, Rainbow Lakes Estates), real numbers over vague language, real names on testimonials, CTAs that tell the reader what happens next.

**Headline patterns that work:**

- `[Real number]. [Real fact]. [Real phone or action].` produces "989 five-star reviews. One phone number."
- `[Time frame]. [Identity]. [Location].` produces "Fifty years. Two Tuccis. One phone number."
- `[Specific service] in [specific place].` produces "Licensed plumbing in Ocala and Marion County since 2006."

**Anti-AI test:** Read any generated paragraph out loud. If it sounds like a chatbot or could apply to any business in any industry, rewrite it.

## Self-check before reporting done (the Six Checks)

Before telling Ron the build is complete, verify all six:

1. **Wow-gap fixes present:** kinetic hero (from Phase 4 mode), stats section rendered as dark section, asymmetric Bento services grid, visual pacing between sections, oversized stats numbers.
2. **Zero factual errors:** real business name, real phone, real owners, real license, real services, real testimonials with real names, real promotion wording and price.
3. **Contact form submits to Ron's inbox:** verified by form action = Static Forms endpoint, accessKey present, subject includes business name.
4. **Schema validates:** JSON-LD passes Google Rich Results Test.
5. **Lighthouse mobile under 2.5s LCP, SEO score 95+, Performance 85+.**
6. **Ron's eye test:** Ron opens the URL on his phone and would text it to a family member without qualifying or apologizing.

If all six pass, ship. If any fail, fix the specific failure and re-run Phase 6. Do not iterate past done.

## Output format (done report)

```
Prospect site complete: [Business Name]

Design tier: [Tier] ([Score]/100)
Hero mode: [mode]
Pages built: [list]
Services captured: [count]
Testimonials captured: [count]
Featured promotion: [yes/no]
Photo sources: Google [X], Site [Y], Instagram [Z], Unsplash [W]

Preview URL: [vercel url]

Quality gates:
  HTML validation: PASS
  Em dash check: PASS
  Banned phrase check: PASS
  Link check: PASS
  Schema validation: PASS
  Lighthouse mobile LCP: [time]s
  Lighthouse mobile SEO: [score]
  Lighthouse mobile Performance: [score]

Profile saved: ~/grm-sites-prospects/[slug]/profile.json
Assets saved: ~/grm-sites-prospects/[slug]/assets/
LESSONS.md: [updated | no new lessons]

Ready for Ron to review on mobile. Next step: open the URL on your phone and run the eye test (check 6).
```

## Revision log

### 2026-04-22 — Stage II (e) tier-logic strip

- Rewrote glass-variant Phase 4 rationale (line ~341) from score-first framing ("higher-scoring brands get bigger type") to Appendix B section-density framing — wide-variant is the hero-end expression of tier's section-density treatment per `typography.md §Appendix B`. Logic stays `tier == "Premium"`; rationale cites the actual authority.
- Rewrote constraint-conflict message (line ~507) from "Standard tier without Layout E fails scale-contrast threshold" to cite the actual condition: "Computed hero size (persona × tier) falls below 80px scale-contrast threshold without Layout E." Message now surfaces the computed-value check rather than tier-keyed naming.
- Replaced `<html lang="en" class="tier-premium">` (and sibling tier classes) with `class="persona-{kebab-key}"` in the Phase 5 cross-file integration point. Persona class is an identifier hook for dev-tools visibility; all persona-conditional values resolve at build time via `CONFIG.fonts` and `CONFIG.spacing` and emit into base `:root` directly. The pre-Composer `.tier-*` cascade-override class system retired.

---

## Version

prospect-site-composer (v0.8 Composer). Development started Tuesday, April 21, 2026. Architectural successor to prospect-site-design, restructuring Phase 4 and Phase 5 against Claude Design's editorial framework (five personas, layouts A–E, photo role hierarchy, three-voice typography, scale contrast, motion restraint, signature micro-interactions) and backporting production prospect-site's Wave 1 and Wave 2 infrastructure (rhythm tokens, SectionOpener and StatRow primitives, font system primitives). The load-bearing change from prospect-site-design is the formalized Phase 4 → Phase 5 handoff contract: Phase 4 produces composition-plan.json (explicit editorial specification of every page), Phase 5 emits HTML against that plan with zero default-template inheritance, Phase 5.5 reads schema content from composition-plan.json rather than the emitted DOM. Two-pillar hard-gate architecture: Pillar 1 editorial (Design's framework plus 13-check Phase 6 editorial suite), Pillar 2 SEO/GEO (schema validity, AI-citation infrastructure, Lighthouse SEO ≥95). Three-skill coexistence during Composer development: prospect-site-design as foundation, prospect-site (production) as backport source and untouched fallback, prospect-site-composer as target skill under development. Full architectural spec and migration sequence: ~/grm-automations/docs/composer/COMPOSER_BRAIN.md.

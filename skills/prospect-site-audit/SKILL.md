---
name: prospect-site-audit
description: "Audit a local home services contractor's live website, capture their real brand data (owners, services, testimonials, credentials, photos, palette, promotions), score their current web presence, author prose.json against the GRM voice contract, and invoke the v1.0 build engine to render HTML. Audit-half outputs profile.json + prose.json; build-half (build-half/scripts/render.py) renders, build-half/scripts/deploy.sh deploys. Use this skill whenever the user types /prospect-site-audit followed by a business name and URL, or asks to audit a prospect for a v1.0 build."
---

# Prospect Site Audit (v1.0)

## What this skill does

Given a business name and a live URL, this skill produces two artifacts that drive the v1.0 build engine:

- **profile.json** — every captured fact about the prospect's business: owners, services, testimonials, credentials, photos, palette, promotions
- **prose.json** — voice-blessed prose authored against the slot vocabulary in the build-half fixture contract

These two files are inputs to `build-half/scripts/render.py`, the deterministic v1.0 template engine that emits HTML per page key. Audit-half does NOT generate HTML directly. The split is load-bearing: audit-half captures and authors; build-half renders and deploys.

Command format:

```
/prospect-site-audit "Business Name" https://their-site.com [@instagram_handle]
```

Optional `--auto` flag skips the Phase 4 design approval gate. Optional `--from-phase N` resumes from a specific phase when iterating on a previously-started audit.

## Architecture

This skill uses progressive disclosure. SKILL.md contains the workflow, decision trees, hard rules, and pointers. Heavy specification content lives in the consolidated reference set and the build-half reference set, loaded on demand:

**Audit-side voice contract (loaded as Phase 5 Step 0 — see Phase 5):**

- `references-consolidated/voiceMap.md` — three-named register architecture (Closing Table / Saturday Morning / Front Porch), three-tier service composition, voice-pivot anchor strip, featured pullquote, Front Porch footer, register coupling rules, §6 spectacle-wins clarification, §6 LABEL discipline
- `references-consolidated/prose-rules.md` — §6.1–§6.5 homepage prose rules, §6.6 inner-page prose slots, §6.7 FAQ override, §6.9 homepage band slots, voice consistency rules across slots
- `references-consolidated/content-rules.md` — voice-mapping table by section, banned phrases (synced excerpt from GRM_VOICE_SKILL.md), headline patterns, CTA templates, FAQ templates per vertical, house formatting style
- `references-consolidated/anti-slop-rules.md` — banned fonts/colors/layouts/components/copy/photography/interactions/mobile/dates/placeholders, the swap test, unknown-field claim vocabulary

**Audit-side capture and design references:**

- `references-consolidated/typography.md` — typography rule set: scale relationships, italic discipline, mono eyebrow system, body measure, mobile scaling, font loading, exceptions principle
- `references-consolidated/image-handling.md` — Phase 3 photo sources, Unsplash tier-4 fallback, compression, lazy loading, logo alpha rebuild procedure, secondary brand mark detection
- `references-consolidated/seo-geo.md` — JSON-LD schema templates, llms.txt template, meta tags, OpenGraph, lighthouse-ci spec
- `references-consolidated/scale-architecture.md` — technical-debt inventory, risk inventory, data preservation principles
- `references-consolidated/handoff-discipline.md` — historical (v0.8 deployed-build/flagship-merge architecture). v1.0 has no post-render HTML modification path; retained for archival reference only.

**Build-side engine and contract:**

- `build-half/references/fixture-contract.md` — interface contract: what audit-half hands to build-half (profile.json + prose.json), what build-half reads (slot vocabulary, fallback behavior per band, derivation rules)
- `build-half/scripts/render.py` — the deterministic v1.0 template engine. Reads profile.json + prose.json, emits HTML per page key. Audit-half invokes via the canonical command in Phase 5.
- `build-half/scripts/deploy.sh` — Vercel deployment + slug reconciliation + sitecar file (sitemap.xml / robots.txt / llms.txt) handling. Audit-half hands off to deploy.sh; does NOT execute Vercel commands directly.

Load a reference when the phase that needs it begins. Do NOT load all upfront.

## Hard rules (read before any phase)

These rules exist because prior builds failed by ignoring them. Do not skip any.

1. **Crawl deeply, never shallow.** Every internal page on the prospect's homepage gets visited and parsed. Shallow audits are worse than no audit.

2. **Capture real facts verbatim.** Real owner names, real years in business, real license numbers, real service lists with real descriptions, real testimonials with real first names and locations, real promotions with exact pricing. Never invent. Never fill gaps with generic filler.

3. **Study the visual brand by examining the actual logo file.** Before choosing colors, download the logo and run it through node-vibrant for semantic swatch analysis. Never pick colors from text scraping alone. The Johnson Brothers lesson (bright royal blue plus sun yellow, not deep navy) is the reference case.

4. **render.py is the canonical build engine. Audit-half outputs profile.json + prose.json only.** Audit-half does NOT generate HTML, does NOT author CSS, does NOT compose section markup. The v1.0 split architecture depends on this discipline. If a phase here looks like it should generate HTML, the phase is wrong — surface to Ron, do not improvise.

5. **Voice authority loads as Phase 5 Step 0, before any prose authoring.** The four-reference voice contract (voiceMap.md + prose-rules.md + content-rules.md + anti-slop-rules.md) is non-negotiable pre-flight. Authoring prose without loading the contract first is the C5 spec-not-consulted defect from B3-resume-2 (2026-04-27). The Step 0 load is documented as the literal first step of Phase 5; it is not a footnote.

6. **Silent data quality checks.** Phase 3.5 runs automated data validation. It does NOT pause for approval on clean audits. It ONLY interrupts when a hard failure is detected (missing phone, zero testimonials, missing owner names where they should exist, zero photos across all sources, critical data mismatch).

7. **Every spec must be heavily specified or not exist at all.** No under-specified phases. No "this step is optional, wing it." Every step here has explicit acceptance criteria.

8. **No em dashes anywhere in customer-facing prose.** GRM house rule. The §6.2 hero subhead is the documented one-place exception. Phase 6 greps emitted HTML for em dashes in both UTF-8 and HTML-entity encodings.

## Phase 0 — Pre-flight integrity check

Goal: fail fast before any Phase 1+ work begins. Better to spend 10 seconds verifying integrations than 30 minutes diagnosing why Phase 5 broke. Phase 0 runs before every audit, no exceptions.

Phase 0 has two check categories: hard checks (any failure blocks Phase 1) and soft checks (failures log a warning but the audit continues).

### Hard checks (must all pass before Phase 1 begins)

For each check, verify the condition and report status. If any check fails, stop immediately and report the specific failure to Ron with the recovery instruction. Do not proceed to Phase 1 until all hard checks pass.

1. **Vercel CLI authenticated on the correct team scope.**
   - Verify: `vercel whoami` returns Ron's identity AND the active team is `ron-7323` (not the older `team_KCAi5VnxkXE0c5ERJWOb7jXE` where the legacy `website` project lives).
   - On failure: report "Vercel CLI not authenticated on ron-7323 team. Run `vercel login` and then `vercel switch ron-7323`."
   - Why: build-half/scripts/deploy.sh expects this scope. Audit-half catches the misconfiguration at Phase 0 so the audit doesn't run to completion only to fail at deploy.

2. **Node.js v24+ at a resolvable path.**
   - Verify: `node --version` returns v24 or higher AND `which node` returns a real path.
   - On failure: report "Node.js not at expected version. The skill requires Node v24+ for sharp and node-vibrant compatibility."
   - Why: image processing in `image-handling.md` (sharp resizing, AVIF generation) and color extraction (node-vibrant against the prospect's logo) both depend on a recent Node.js version.

3. **Working directory exists.**
   - Verify: `~/grm-sites-prospects/` exists and is writable.
   - On failure: report "Working directory missing. Recovery: `mkdir -p ~/grm-sites-prospects/`."

4. **Audit-half skill files present and build-half engine reachable.**
   - Verify: the audit-half SKILL.md and the consolidated reference set (voiceMap.md, prose-rules.md, content-rules.md, anti-slop-rules.md, typography.md, image-handling.md, seo-geo.md, scale-architecture.md, handoff-discipline.md) load from the install path. Verify: `build-half/scripts/render.py` and `build-half/scripts/deploy.sh` are executable and reachable. Verify: `build-half/references/fixture-contract.md` loads.
   - On failure: report "Skill installation incomplete. Missing: [list]. Re-install from the v1.0 assembly tree."
   - Why: the four voice references are required for Phase 5 Step 0; render.py is required for Phase 5 Step 3; fixture-contract.md is required for Phase 5 Step 2 slot vocabulary.

5. **.env file present with required keys.**
   - Verify: `~/grm-sites-prospects/.env` exists AND contains `GOOGLE_PLACES_API_KEY=` (non-empty) AND contains `UNSPLASH_ACCESS_KEY=` (non-empty).
   - On failure: report "Required API keys missing. Phase 3 photo collection needs both."
   - Static Forms key is hardcoded in `references-consolidated/seo-geo.md` and does not need to be in .env.

6. **Disk space adequate.**
   - Verify: at least 500MB free in the volume hosting `~/grm-sites-prospects/`.
   - On failure: report "Insufficient disk space."

7. **Prospect URL is reachable.**
   - Verify: `curl -I -L --max-time 10 [prospect-url]` returns a 200 or 301/302 redirect chain ending in 200.
   - On failure: report "Prospect URL not reachable. Verify the URL is correct and the site is online."

8. **Workspace git tracking initialized.** This is the final step of Phase 0, run after all other hard checks pass.
   - Action: create the prospect folder at `~/grm-sites-prospects/[business-slug]/` if it does not already exist. Inside it, write `.gitignore` with entries `node_modules/`, `.DS_Store`, `*.log`, `.env`, `.env.local`. Run `git init -b main`. Stage the `.gitignore` and make an initial commit titled `Workspace initialized for [business name]`.
   - On failure: report the exact git error. Hard stop.
   - Why: prospect workspaces accumulate HTML, photos, profile.json, prose.json across phases. Without git tracking from the start, post-deploy hotfixes have zero rollback granularity.

### Soft checks (warn but continue)

1. **HubSpot pipeline configured.** If absent, warn that no auto-create of a deal record will happen at Phase 8.
2. **Automated backup running.** If absent, warn that profile.json + prose.json are unbacked and a v0.8 hardening target.
3. **Google Places API lightweight test call.** If failing, warn that Phase 3 may degrade to Instagram + Unsplash fallback.

### Phase 0 output report

Phase 0 always produces a report block at the end. If any hard check fails, the report ends with `Phase 0 FAILED.` and Phase 1 does not begin.

### When Phase 0 can be skipped

Almost never. Only with explicit `--skip-phase-0` flag. Silent skips are not allowed.

## Phase 1 — Homepage deep capture

Goal: capture everything visible and structural on the prospect's homepage, including the raw logo for color analysis.

Steps:

1. Create the prospect folder: `~/grm-sites-prospects/[business-slug]/` where `business-slug` is the business name lowercased with spaces replaced by hyphens. Create `raw/` and `assets/` subfolders.

2. Fetch the homepage HTML with a desktop user agent. Save to `raw/homepage.html`.

3. Parse the homepage and extract: business name, tagline, phone number (note if tel:-linked), email, address, hours including emergency availability, primary logo URL, CSS color tokens from linked stylesheets, font families, hero image URL if any, list of internal navigation links (this becomes the Phase 2 crawl list), all inline image URLs with alt text, social media links, footer credentials.

4. **Logo capture priority — positional, not alt-text-driven (v1.1 floor cut, 2026-04-30).** WordPress and modern page-builder sites place the brand logo in known structural locations; alt-text-substring search (the v0.x heuristic) gets fooled by marketing composites and credential badges that contain "logo" in alt-text or filename. Brehm observe-and-document run, Finding 5: a marketing composite with alt "Brehm Roofing & Restoration logo design" was picked over the actual brand logo (alt: filename only) because the heuristic was alt-text-driven. node-vibrant ran on the wrong file and returned Pink Panther pink as the brand color. Resolution priority:

   a. `<img class="custom-logo">` — WordPress core convention, highest priority
   b. `<img>` inside `<header>` element — generic header convention
   c. `<img>` inside `<div class="header-logo">` / `.site-logo` / `.brand-logo` / `.logo-wrapper` — page-builder conventions (Beaver Builder, Elementor, Divi)
   d. ONLY THEN fall back to alt-text/src-substring "logo" search
   e. **Always blacklist `/wp-content/plugins/` paths** — plugin-injected DOM (accessibility plugins, multilingual plugins) commonly contains decorative SVGs with "logo" in the path; never brand content.

   Download the captured logo to `assets/logo.[ext]`. If the logo is not PNG (SVG, webp, jpg, gif, avif, ico), use sharp to convert a PNG copy at `assets/logo.png` for node-vibrant analysis. The "SVG → PNG" rule from v0.x extends to all non-PNG raster + vector formats; webp is the common 2025+ case (Brehm).

   **At Phase 4 approval gate, surface the captured logo with a thumbnail and ask the operator to visually confirm before committing the brandPalette.** A wrong-logo capture at Phase 1 propagates through node-vibrant → brandPalette → every CSS surface; a 30-second visual check at Phase 4 catches it before commit.

4a. **Logo alpha channel check and rebuild.** After download, inspect the logo PNG for alpha channel presence and corner transparency. If alpha is missing or corners are opaque, rebuild with chroma-key transparency per the procedure in `references-consolidated/image-handling.md` § "Logo alpha rebuild procedure". If chroma-key cannot produce clean transparency, log a warning, leave the logo opaque, and continue — Phase 6 mobile render verification will catch rendering issues if they surface.

4b. **Secondary brand mark detection.** While crawling images during step 3, flag any image meeting ALL criteria: aspect ratio between 0.9:1 and 1.1:1; long edge between 150px and 600px; located in a CMS upload directory (`/wp-content/uploads/`, `/uploads/`, `/media/`, `/assets/brand/`, `/sites/default/files/`, `/images/brand/`); not already identified as the primary logo; not a stock photo or gallery image. These are candidate secondary brand marks — typically round badges, founder portraits, certification logos, sub-brand marks. For each candidate: download to `assets/candidate-brand-marks/[original-filename]` and add an entry to `profile.json` under `secondaryMarkCandidates[]`. Present each candidate to Ron at the Phase 4 approval gate. Detailed spec in `references-consolidated/image-handling.md` § "Secondary brand mark detection".

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

5. **Broken internal link capture.** During crawl, track the HTTP status of every internal link followed. For any link that returns a 404 or 5xx status, record it under `profile.json.brokenLinks[]`. Broken internal links on the prospect's live site are direct "owner stopped paying attention" sales signals. Phase 8 surfaces these in the done-report sales-ammunition section.

6. Report to Ron: pages crawled, services captured, testimonials captured (with name list), owner names, featured promotion, any gaps.

## Phase 2.5 — Pre-migration SEO audit

Goal: capture the prospect's current SEO footprint before any rebuild so the post-signing migration preserves their Google equity.

Additive only. Does not modify Phase 2 captures. Output goes to `profile-draft.json` under `migrationData`.

Steps:

1. Run `site:theirdomain.com` Google search to inventory indexed pages. Capture the URL list.
2. Check Wayback Machine for archived snapshots. Note any historically indexed pages not in the current site.
3. Build initial URL inventory for the migration redirect map.
4. Save to `migrationData.indexedUrls`, `migrationData.archiveSnapshots`.
5. If any step fails, log and continue. Migration will require manual URL discovery later.

For the full 8-step migration workflow, see the GRM Migration Playbook document. This phase is only capture, not execution.

## Phase 3 — Photo collection and curation

Goal: collect the best possible photo inventory for the build, from multiple sources in priority order.

For detailed source handling, quality scoring, and Unsplash fallback logic, see `references-consolidated/image-handling.md`. Sources, in priority order:

1. **Google Places API.** Primary. Pull up to 10 photos with attribution. Save to `assets/photos/google/`.
2. **Prospect's own website.** Scrape from Phase 1 and Phase 2 HTML. Save to `assets/photos/site/`. Filter for watermark-free, logo-free, high-resolution only.
3. **Instagram.** If a handle was provided or captured in Phase 1, attempt to pull 6 to 12 recent public posts. Save to `assets/photos/instagram/`.
4. **Unsplash API (tier-4 fallback).** If tiers 1-3 produced fewer than 4 usable photos, query Unsplash with service-category keywords. Save to `assets/photos/unsplash/`. Attribution required.

**Service-photo hydration via build-half/scripts/unsplash_fetch.py.** When `services.list[].featuredImage` or `.detailImage` is unset and `_unsplash-cache.json` has a pick for the slug, the cache populates the slot. See `references-consolidated/image-handling.md` and `build-half/scripts/unsplash_fetch.py` for the per-prospect query override and backup-query mechanism (`stockQuery` / `stockQueryBackup` slots in profile.json).

After collection, run the quality evaluation in `references-consolidated/image-handling.md` and tag every photo with: `contentType` (finished_work, team, owner, jobsite, stock, unknown), `orientation`, `longEdgePx`, `disqualifiers`.

Then auto-assign photos to positions in `photoAssignments`:

- `heroCandidates`: top 8 landscape finished_work photos, ranked by quality
- `ownerPortrait`: first photo with contentType=owner, if any
- `servicesGridPhotos`: next 6 to 12 landscape photos tagged by service category
- `galleryPhotos`: remaining quality photos

Report to Ron: photo counts by source, heroCandidates count, ownerPortrait yes/no, services coverage.

## Phase 3.5 — Silent data quality gate

Goal: catch hard data failures before Phase 4 wastes time on design decisions built on broken inputs.

Runs automatically. Does NOT pause for Ron's approval on clean audits. ONLY interrupts on hard failure.

Hard failures (interrupt the audit):

- No phone number captured in Phase 1 or Phase 2
- Zero testimonials captured with real names
- Zero photos across all four sources in Phase 3
- Owner names not found on a business that should have them
- Review count mismatch across sources greater than 20%
- Service list contains fewer than 3 real services
- Business name mismatch between Phase 1 capture and command argument

Soft warnings (logged but do not interrupt):

- Hero candidate count below 4
- No featured promotion captured
- No license number found
- No service area cities beyond the primary city

On hard failure, report the specific failure with captured context and wait for instruction: fix manually, skip the prospect, or override and continue.

On clean pass, proceed directly to Phase 4 without pausing.

## Phase 4 — Scoring, tier, approval gate

Goal: score the prospect's current web presence, assign tier, stage the build plan, and get Ron's approval.

### Scoring rubric

Score across five categories, each worth 20 points, total out of 100:

- **Copy Language (0-20):** Headlines specific and benefit-driven or generic? Grammar issues?
- **Visual Quality (0-20):** Photos professional? Palette intentional? Logo clean?
- **Business Maturity (0-20):** Review count? Years in business? Team bios? Certifications?
- **Site Sophistication (0-20):** Mobile-responsive? Loads under 3 seconds? Looks 2025 or 2010?
- **Brand Intentionality (0-20):** Consistent logo? Defined palette? Clear voice?

### Tier assignment

- **Premium (70-100):** Full feature set, heavy trust content, all stats populated, category-specific FAQ
- **Professional (40-69):** Standard feature set, selective trust content, focus on clarity
- **Standard (0-39):** Minimal feature set, simple layouts, focus on hierarchy and CTA prominence

### Hero background treatment (auto-picked by engine)

Audit-half does NOT author a hero-mode slot. The hero is one editorial idiom — glass card on background — with background treatment auto-picked by `render.py` from `photoAssignments.heroCandidates` count:

- ≥3 photos → slideshow (cross-fade between photos)
- 1–2 photos → single photo (optionally with mesh-canvas overlay for visual interest)
- 0 photos → mesh / gradient only

The flagship walk (5 deployed homepages, 2026-04-28) confirmed all flagships share the same hero skeleton with background-treatment variation driven by photo count. The "3 modes" framing in earlier specs was modeling this as 3 distinct shapes when it's 1 shape with 3 background variations.

**Known engine gap (engine-extension item).** `render.py` ships single-photo and crossfade-slideshow background treatments today: single fires when `heroCandidatesTop5` is 1–2 photos; crossfade-slideshow fires automatically at `heroCandidatesTop5 ≥ 3` (render.py L1485, up to 5 slides). The remaining genuine gap is mesh-canvas: 0-photo prospects fall back to a static gradient, not the animated mesh treatment that earlier specs scoped. Scope-clarification 2026-04-30 — slideshow IS shipping (verified across Testerman / Goney's / Bellair); only mesh-canvas remains pending.

### Approval gate output

Show Ron a single-screen summary:

```
Audit Analysis Complete
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

Build plan:
  Tier: [Premium/Professional/Standard]
  Hero background expected: [slideshow / single / mesh-only], based on [N] hero candidates
  Hero background engine-emit today: single + crossfade-slideshow (≥3 candidates) ship; mesh-only pending
  Brand colors: primary [hex], accent [hex] (from logo node-vibrant analysis)
  Secondary brand mark candidates: [list, with proposed_use options]

Headline candidate (Closing Table voice):
  Pattern: [A / B / C / D / E from content-rules.md headline patterns]
  Headline: [generated candidate]
  Subheadline: [generated candidate]

Proceed? (yes / revise / try Pattern [A|B|C|D|E] / custom: [your headline])
```

Wait for explicit `yes` or override instruction. Only proceed to Phase 5 after approval.

**Mandatory operator checks before approval (v1.1 floor cut, 2026-04-30):**

1. **Visually verify the captured logo.** Open `assets/logo.png` and confirm it is the prospect's actual brand wordmark/lockup, NOT a marketing composite, NOT a credential badge, NOT a third-party mascot or co-brand. Brehm observe-and-document run, Finding 5: a "Brehm Roofing & Restoration logo design" alt-text-tagged image was an Owens Corning Pink Panther + Platinum-Preferred-Contractor marketing composite; the actual logo had filename-only alt-text. Visual check at this gate would have caught it before node-vibrant ran.

2. **Visually verify hero candidate photos.** Open the top heroCandidate (gplaces_00 or equivalent) and any candidate showing crew apparel or vehicle wraps. Confirm any visible phone numbers / license numbers match the audit's primary location. Multi-location prospects (Brehm Finding 18) commonly carry the brand-default phone in branded vehicle wraps + crew shirts; unfit photos must be tagged `disqualifyFromHero: true` in `profile.photoLibrary.photos[<rel>]`.

3. **Service-count alignment with engine cap.** `render.py` caps services at the canonical bento-grid tier {1, 2, 4, 6} — see Phase 5 services discipline below. If `profile.services.list[]` has more than 6 entries, pick the 6 strongest at this gate and reorder `profile.services.list[]` so the top-6 render. The other entries are not lost — they're available for `service_taglines` and SEO breadth — but the rendered overview grid is the top-6.

4. **businessName schema check.** Confirm `profile.businessName` is populated as either a string (e.g., `"Brehm Roofing & Restoration"`) OR a dict (e.g., `{"primary": "Goney's...", "legalEntity": "..."}`). Both shapes are accepted (v1.1 floor cut). Empty / absent / wrong-shape → render emits literal `"Business Name"` placeholder + stderr WARN; visible in homepage `<title>`, JSON-LD `name`, nav wordmark. Brehm observe-and-document run, Finding 32.

If `--auto` was passed, skip the gate and proceed automatically.

## Phase 5 — Prose authoring and render.py invocation

Goal: author `prose.json` against the voice contract, finalize `profile.json`, and invoke the v1.0 build engine to render HTML.

### Step 0 — Voice authority pre-flight load (non-negotiable)

**Before any prose authoring, load the four-reference voice contract.** This is a literal pre-flight step, not a footnote. Authoring prose without loading the contract first is the C5 spec-not-consulted defect from B3-resume-2 (2026-04-27); the load discipline is the structural guard against repeating it.

Load in this order:

1. **`references-consolidated/voiceMap.md`** — three-named register architecture (Closing Table for hero/promos/cards/stats, Saturday Morning for marquees/section headers, Front Porch for footer/About). Three-tier service composition (Signature / Operational / Distinctive). Voice-pivot anchor strip rules. Featured pullquote pattern. §6 spectacle-wins clarification (engine typography IS voice at structural/display surfaces). §6 LABEL discipline (register-blessed eyebrows, never spectacle-flat dictionary categories).

2. **`references-consolidated/prose-rules.md`** — §6.1 H1 hero headline shape. §6.2 hero subhead. §6.3 display headlines (em + accent binding rule, inner-page exemption at L112). §6.4 manifesto strip (declarative brand-pillar register, not italic-poetry). §6.5 service tile italic taglines. §6.6 inner-page slot vocabulary (about / services / testimonials / contact). §6.7 services-page FAQ override. §6.9 homepage band slots (stats_band, faq_header, promo_callout). Voice consistency rules across all slots — no em dashes, no corporate filler, specific nouns over categories.

3. **`references-consolidated/content-rules.md`** — voice-mapping table by section (which voice for which surface). Banned phrases excerpt synced from GRM_VOICE_SKILL.md. Banned characters in customer output (em dashes, ellipses for drama, etc.). Headline patterns A through E. CTA templates. FAQ templates per vertical. House formatting style (phone, hours, license numbers, addresses).

4. **`references-consolidated/anti-slop-rules.md`** — banned headline patterns ("Your Local Experts," "Quality Service," "Welcome to," etc.). Banned body copy patterns. The swap test ("could this apply to any business in any trade in any city"). Unknown-field claim vocabulary (license number, insurance carrier, awards, founding year, etc.).

After loading, classify every prose surface as **body-copy / inline-prose** (strict §6 italic-earned-by-voice binds) or **structural / display** (spectacle-wins binds; engine typography IS voice). The classification table is in voiceMap.md §6.

### Step 1 — Promote profile-draft.json → profile.json

Carry over the `designChoices` block from Phase 4 approval (tier, brand colors, secondary brand marks, expected hero background treatment for the approval-gate record). Set `unknownFields[]` to list any data point Phase 1 / 2 searched for but could not capture (e.g., `"license_number"`, `"bbb_rating"`). Phase 6 unknown-field guard greps emitted HTML for claim vocabulary tied to these fields.

### Step 2 — Author prose.json against the slot vocabulary

Author one pass, all slot groups. Read every slot's captured profile facts before writing.

**Slot vocabulary reference:** `references-consolidated/prose-rules.md` §6.1–§6.6 (canonical page-keyed schema for all five pages including homepage) and `build-half/references/fixture-contract.md` §4.A (Phase 3b homepage slots under `prose.homepage.*`) + §4.B (inner-page slot summary). v1.0 prose.json is **pure page-keyed** — all slots live under page sub-dicts (`prose.homepage.*`, `prose.about.*`, `prose.services.*`, `prose.testimonials.*`, `prose.contact.*`). The legacy flat schema in `fixture-contract.md` §4-LEGACY is v0.8-monolith-era; v1.0 prospects do NOT author flat shape.

**Page key set:** five canonical page keys — `homepage`, `about`, `services`, `testimonials`, `contact`. Author prose for every page key the build needs (all under their respective sub-dicts); the engine drops bands per fixture-contract.md §3 fallback rules when data is absent.

**Voice register per slot:**

- Homepage hero (h1, hero_kicker, hero_eyebrow, subhead): Closing Table
- Homepage display headlines (services_headline, testimonials_headline, story_headline): **Saturday Morning** as default per content-rules.md voice-mapping; **Closing Table** when the headline carries a §6.3 data-claim (proof-stack pattern, e.g., "199 five-star reviews. Not one below."). Soft-call surface per content-rules.md L65; let the captured facts decide.
- Homepage manifesto strip (§6.4): brand-pillar declarative register (NOT italic poetry — that defect was corrected at Phase 5.0c, 2026-04-26)
- Homepage cta_band (§6.9): Closing Table imperative — engine ships register-blessed default headline `"Call us. Text us. <em>Send the details</em>."`. Override at `prose.homepage.cta_band.headline` only when the prospect's voice or data earns deviation. Eyebrow defaults `"READY TO TALK"`. Body / primary_label / secondary_label all optional override slots. Per Session 2 spec-defect F7 disposition: cta_band is the conversion-ladder rung that ships on every homepage, no opt-out.
- Service tile taglines (§6.5): per-service register inheritance from voiceMap.md §2d three-tier composition
- About page story_paragraphs: Front Porch
- About page lede + creds_lede + where_we_work: Closing Table
- Services page overview_title + detail_section_title: Closing Table at flagship surfaces
- Services service_detail_descriptions[]: register varies by service tier per voiceMap.md §2d
- Testimonials site_section_title + google_section_title: italic-pair attribution per voiceMap.md §6 spectacle-wins
- Contact form_intro + info_heading: Closing Table (form-intro and info-heading have a §6.3 conformance question pending #6 categorical sweep — see prose-rules.md §6.6 contact slot notes)

**Engine-default surfaces.** Some slots have engine fallback strings that are register-blessed per voiceMap.md §6 + LABEL discipline. Do NOT author "boring but correct" prose to override a register-blessed default — match the register or skip authoring.

**Sparse-drop surfaces.** Some slots have NO engine fallback; the band drops if prose is absent. Author every sparse-drop slot you want to ship. See prose-rules.md §6.3 for the sparse-drop vs default-emit table.

**Slot classification — three classes (Session 2 codification).** Every prose slot falls into one of three classes. Authors should know which class they're working in before drafting:

- **Required-author per prospect.** No engine default acceptable; the slot carries per-prospect identity that engine cannot synthesize without fabrication. Slot examples: `prose.[about|services|testimonials|contact].headline` (every inner-page hero h1 — per-prospect business identity). Engine sparse-drops the entire page-hero band when absent (no broken empty shells).

- **Override slot.** Engine ships register-blessed default. Author overrides only when prospect's voice or data earns deviation from default. Slot examples: inner-page eyebrows (engine fires wayfinding constants per page — `HOW WE GOT HERE` / `THE CRAFT · {COUNT} SERVICES` / `FROM THE NEIGHBORS · {REVIEW_COUNT} REVIEWS` / `VISIT · {CITY}`); inner-page ledes (three-parallel-clause Closing Table defaults with profile-interpolation at clause-1 and locative-relational pivot at clause-3 em-italic — the where-pivot is the engine's signature register move); homepage cta_band headline + eyebrow; homepage stats_band, faq_header, promo_callout per §6.9; services overview_eyebrow / overview_title / detail_section_eyebrow / detail_section_title.

- **Sparse-drop slot.** No engine default, no required-author. Slot drops cleanly when absent; band/element-level drop preserves structural integrity. Slot examples: `service_detail_descriptions[].bullets` and `.tag` (array / element drop when absent), `prose.about.story_paragraphs` (paragraphs drop, story-body retains owner block), `prose.contact.info_heading` (h2 drops, contact-info column reads cleanly without heading), `prose.homepage.manifesto.headline` (current behavior — band drops; future engine extension may promote to override slot per Session 2 housekeeping).

When adding a new prose slot to the spec, the first spec question is: **which class?** Required-author / override / sparse-drop. Engine extensions inherit the rule.

### Step 3 — Invoke render.py per page key

Canonical command shape:

```bash
python3 build-half/scripts/render.py \
  --profile  ~/grm-sites-prospects/[slug]/profile.json \
  --prose    ~/grm-sites-prospects/[slug]/prose.json \
  --out      ~/grm-sites-prospects/[slug]/[page-key].html \
  --photos-root ~/grm-sites-prospects/[slug] \
  --css-href ../../css/composer-system.css \
  --canonical-base https://[slug]-grm.vercel.app \
  --page [homepage | about | services | testimonials | contact]
```

Run once per page key. The `--canonical-base` argument enables canonical URL emission, OG URL emission, JSON-LD url + image emission, and sitemap.xml entry emission. The `--page` argument selects which slot group the engine reads from prose.json.

**Engine gap (engine-extension item):** `render.py` `main()` returns exit code 0 unconditionally. The docstring promises exit codes 1 (§7 validation failure) and 2 (data shape blocker), but those code paths are unwired. Audit-half does NOT depend on render.py exit codes — Phase 6 grep gates run on the emitted HTML files independently.

### Step 4 — Inspect emitted output and report

Open every emitted page in a browser. Eyeball walk for: hero shape matches the expected background treatment from Phase 4 (slideshow / single / mesh-only) or known engine gap surfaced; em-dash leakage; banned phrases; broken images; missing bands. Surface anything off to Ron before Phase 6.

Report to Ron: pages emitted, slot coverage, any engine warnings printed to stdout, eyeball-walk findings.

## Phase 5.5 — llms.txt authoring

Goal: emit the `llms.txt` file at the prospect workspace root for AI crawler citation (ChatGPT, Claude, Perplexity, Gemini).

**Scope:** llms.txt only. `sitemap.xml` and `robots.txt` are emitted by render.py (per `--canonical-base`); deploy.sh handles all three at the deploy boundary. **Engine-extension item:** llms.txt has no producer in build-half; audit-half writes it for now. Future engine-extension session absorbs llms.txt emission into render.py or deploy.sh.

Authoring rules: follow the AnswerDotAI llms.txt spec format. Point AI crawlers at clean markdown versions of key pages. Template lives in `references-consolidated/seo-geo.md` § "llms.txt template."

Save to `~/grm-sites-prospects/[slug]/llms.txt`. deploy.sh picks it up at the staging step.

## Phase 6 — Pre-deploy verification

Goal: automated quality gates that run on the emitted HTML and supporting files, independently of render.py exit codes. No shipping broken sites. No relying on Ron's eye for things a script can verify.

Phase 6 runs grep-and-validator gates. All must pass before Phase 7 hand-off. On any failure, log the specific failure with file and line context, and stop.

### Content integrity checks

1. **HTML validation.** All emitted pages pass W3C HTML5 validation or log only minor warnings.

2. **Em dash check.** Grep all emitted HTML for em dashes in both UTF-8 (`—`) and HTML-entity (`&mdash;`, `&#8212;`) encodings. Fail if any found outside the §6.2 hero subhead exception.

3. **Banned output check.** Grep all emitted HTML for the banned strings in `references-consolidated/content-rules.md` (corporate jargon, AI tells, banned credential claims) AND the HTML slop list (hallucinated `<small>` tags, "Reply STOP" SMS opt-out fragments, "Or reply" fallback copy). Fail if any found.

   **Placeholder leakage extension (v1.1 floor cut, 2026-04-30):** ALSO grep for engine-fallback-default literals that indicate schema-shape mismatch fell through. Any of these in emitted HTML = render landed on a default placeholder = profile.json schema is wrong (probably wrong shape on a critical field). Fail and surface to operator with the field-path implied by the placeholder:
   - `Business Name` (literal) — `profile.businessName` shape mismatch (string OR `{primary, legalEntity}` dict required); see render.py business name cascade. Brehm observe-and-document run, Finding 32.
   - `Owner Name` — `profile.owners[0]` shape mismatch
   - `Phone Number` (when emitted bare, not as a label) — `profile.contact.phone` missing
   - `[CITY]`, `[BUSINESS]`, `[OWNER]`, `[YEAR]` — any bracketed-uppercase token
   - `<em>Name</em>` (engine wordmark italic-tail with literal "Name") — same root cause as `Business Name`

4. **Link check.** All internal links resolve. No 404s. No `href="#"` or `action="#"` placeholders.

5. **Image reference check.** All `<img>` tags reference files that exist in `assets/photos/`. No broken references. No hotlinked external images.

6. **H1 count check.** Every emitted page has exactly one `<h1>`. Zero or multiple H1s fails.

7. **Mixed content check.** No `http://` references inside `<img src>`, `<link href>`, `<script src>`, or inline CSS `url()` values. Mixed content breaks the SSL padlock.

### Data integrity checks

8. **Phone number consistency.** The prospect's real phone number appears in: nav bar, hero CTA, footer, contact section, and JSON-LD schema. Regex the number across all five locations and confirm exact string match. A typo in any one location fails.

9. **Schema-to-profile cross-reference.** For every JSON-LD block on every emitted page, assert that `ratingValue`, `reviewCount`, `foundingDate`, `telephone`, `address`, `priceRange`, and any numeric or factual field matches `profile.json` exactly. Any mismatch fails. Implementation: `scripts/verify_schema_against_profile.py`.

10. **Unknown-field guard.** `profile.json.unknownFields[]` lists any data point Phase 1 / 2 could not capture. Grep emitted HTML for the claim vocabulary tied to each unknown field (vocabulary map in `anti-slop-rules.md` § "Unknown-field claim vocabulary"). Any match fails.

### Legal and attribution checks

11. **Photo attribution check.** If any photo came from `assets/photos/google/`, the footer must contain Google Places attribution. If any photo came from `assets/photos/unsplash/`, footer must contain photographer credits per Unsplash API Guidelines. Missing attribution is a ToS violation and fails.

### Form integrity checks

12. **Contact form HTML wiring.** Form action is `https://api.staticforms.xyz/submit`, accessKey hidden input is present with GRM's real key, subject hidden input contains the real business name, honeypot field is present and empty, required fields are marked correctly.

13. **Contact form live submission test.** Execute a real POST to Static Forms with a test payload whose message body contains `[BUILD TEST - IGNORE]`. Verify 200 response and successful delivery. Failed submission fails.

### Schema validation

14. **Schema.org validation.** All JSON-LD (LocalBusiness, Service, FAQPage, Review) passes the schema.org validator. Validation errors fail.

### Performance and accessibility

15. **Lighthouse CI gate.** Run lighthouse-ci against the local preview build. All four thresholds must pass on mobile:
    - LCP (Largest Contentful Paint) < 2.5s
    - Performance score ≥ 85
    - SEO score ≥ 95
    - Accessibility score ≥ 90

16. **Mobile render verification at 375px.** Use headless Chrome at 375px viewport width to render the homepage. Verify: no horizontal scroll, hero CTA visible above the fold, navigation collapses to hamburger, phone number is tappable. Automated backup to Ron's phone eye test.

### Social metadata integrity

17. **Social metadata completeness check.** Verify every emitted page contains the complete OpenGraph block (10+ tags) and Twitter Card block (5+ tags). Verify `og:image` and `twitter:image` values are absolute URLs beginning with `https://`, and that the image path resolves to a real file in `assets/photos/`. Any missing tag, any relative URL, or any image pointing at a missing file fails.

### llms.txt integrity

18. **llms.txt existence and format.** File exists at workspace root, follows the AnswerDotAI llms.txt spec, contains links to clean markdown versions of key pages.

### Helper scripts

Checks 13 (live form submission) and 16 (mobile render verification) require helper scripts in `scripts/`:

- `scripts/test_form_submission.py` — POSTs test payload to Static Forms, verifies response
- `scripts/mobile_render_check.py` — Playwright or Puppeteer at 375px

All other checks are grep, curl, or direct validator calls that run inline.

### On failure

Log the specific failure with file and line context. Do not hand off to deploy.sh. Report to Ron with: which check failed, where, recommended fix, whether the fix is automatic or requires Ron's input.

## Phase 7 — Hand-off to deploy.sh

Phase 6 passes → audit-half hands off to `build-half/scripts/deploy.sh`. Audit-half does NOT execute Vercel commands directly.

deploy.sh handles: Vercel project naming, name-collision suffix, slug reconciliation across emitted HTML / sitemap.xml / robots.txt / llms.txt, the `vercel --prod --yes` deploy itself, post-deploy curl smoke-test, and the live URL capture.

Audit-half hand-off command:

```bash
bash build-half/scripts/deploy.sh \
  --prospect-dir ~/grm-sites-prospects/[slug] \
  --slug-base [business-slug]
```

For full deployment behavior, see `build-half/scripts/deploy.sh` source and `references-consolidated/seo-geo.md` § "Deployment".

## Phase 8 — LESSONS, done report

Goal: append institutional lessons (if any), output the done report.

Steps:

1. If anything unusual happened during the audit (unexpected data shape, soft warnings, recovery actions, novel slot-authoring decisions, any of the three known engine gaps surfacing), append an entry to `references-consolidated/LESSONS.md`.
2. Output the done report (see Output Format below).

Note: profile.json promotion happened at Phase 5 Step 1, not here. Phase 8 is post-deploy bookkeeping only.

## Cold-walk gate — 4 rounds before reporting done

Phase 6 verification gates fire automatically; the cold-walk gate is the human-walk discipline that runs against the deployed live URL before "done" can be declared. Four rounds, each mode-distinct. The four don't compress into one — fatigue compresses spectacle judgment, structural judgment requires fresh-walk discipline, mechanical defects need automated gates, and finishing-detail defects only surface when the structural read has settled.

Surfaced from Session 3 cold-walk experience (the closure of the Volthom + Testerman v1.0 builds); Phase 0.5 confirmed the pattern by finding three principle-class defects (P13 / P14 / P15) plus a fourth surfaced mid-cycle (P16) that an unstructured single-pass walk would have missed.

### Round 1 — mechanical (Phase 6 automation, surfaced for completeness)

Catches: placeholder leaks (`[BUSINESS NAME]`, `(555) 555-5555`, etc.), schema-vs-profile misalignment, banned-phrase emissions, em-dash leaks in body copy, GRM-credit-line leaks in footer, fabricated-credential claims without supporting profile data, raw Python repr in emitted HTML (P16 gate at `_verify_no_python_repr_in_html`), unprocessed em-shorthand placeholders (`{em}` / `{/em}`).

How it runs: **automatic.** Phase 6 verification gates fire during the build; render.py L4032 hard-fails on P16 leaks before HTML hits disk; deploy.sh runs grep gates against the staged HTML before pushing to Vercel. No human walk needed unless a gate fails, in which case fix-source-then-rerun. Round 1 is on the cold-walk-gate list for completeness — it's the discipline's mechanical floor that the human rounds build on top of.

### Round 2 — structural (rent-check on bands)

Catches: bands that don't earn their rent on this prospect, logo capture priority violations (favicon shipped when WP-content media-library lockup exists), brand-responsive surface drift (hardcoded RGB in structural surfaces breaking role-swap discipline), story-img tier mismatch (hero-fallback shipped under "team portrait" alt text), three-class slot taxonomy violations (sparse-drop band shipping with engine-generic fallback when it should have dropped).

How it runs: walk the deployed URL on **desktop**, fresh eyes. Question: "does every band carry weight for this specific prospect? Does the logo treatment match the prospect's lockup? Are brand-responsive surfaces honoring the extracted palette? Does each prose slot match its surface-class register?"

### Round 3 — spectacle (ceiling-reaching judgment)

Catches: review pull-count regressions (Google Places 5-cap meta surface vs hero claim of "N reviews"), animation regressions (count-up not firing on the lead stat, hero crossfade slideshow not initialized), layout-adapt issues for thin pools (1 testimonial + bipartite split = empty column), logo-on-dark-vs-light treatment issues (white-on-transparent invisible on cream headers), wordmark redundancy with logo lockup, hero-photo selection that's pixel-largest but not spectacle-strongest.

How it runs: walk the deployed URL on **desktop AND mobile**, fresh eyes. Question: "is this a flagship-tier prospect site, or does it read flat?"

### Round 4 — finishing-detail (post-structure polish)

Catches: invisible-logo on cream-bg headers (white-on-transparent on warm-cream sitenav across inner pages), count-stale copy after data cuts ("seven services" prose surviving a 7→6 service-cut), layout-overflow at narrow viewports (cards bleeding, text cutting mid-word), photo-overlay attribution cross-contamination (Member / Owner-name caption shipping on team-identity photo when ownerPortrait is absent), affiliation-line drop-cleanly failures (`<strong></strong>, Founder` leading-comma artifact when name field is empty), icon-symbol coverage gaps (Instagram empty circle when Unicode glyph isn't in the inherited font), section-headline width discipline drift (`text-align:center` parent + block child without `margin:auto` producing a left-anchored cramped column).

How it runs: walk the deployed URL on **mobile FIRST** (where layout-overflow and finishing-detail register fastest), then desktop. Question: "what would the nitpick eye catch?"

Concrete checklist anchored in Phase 0.5 evidence (Session 3 + Session 4 close):

- [ ] Logo treatment per page — inner pages may have different bg colors than homepage; logo must remain visible across every page (P11)
- [ ] Headline counts — does any "N [services / years / reviews]" copy match the data structure's current state? Or use count-agnostic phrasing (P12)
- [ ] Card overflow / text cut at narrow viewports (375px iPhone SE baseline)
- [ ] Photo-overlay attribution alignment with the actual photo selected, not the assumed photo (P14)
- [ ] Affiliation lines drop-cleanly when source fields are empty — no leading commas, no orphaned roles (P14)
- [ ] Footer social icons render as proper glyphs (not empty circles, not Unicode tofu) for every captured social platform (P15)
- [ ] Section titles emit clean text (P16 gate is the automated catch; cold-walk catches anything the gate misses on visual surfaces)
- [ ] Display headlines centered within their stack (eyebrow + headline + subhead reading as one editorial moment, not a left-anchored cramped column) (P13)

### Round 5 — first-prospect-impression

Codified separately as Phase 8.5 (post-deploy, prospect-pitch URL gate, forthcoming). Triggers when the deploy is the URL a prospect will walk before a sales call. Distinct from the in-session 4-round gate: different read ("what does a prospect see in 30 seconds on their phone before deciding to trust"), higher polish bar (the stake is the sale, not the engine).

## Voice authority — pointer, not duplicate

The four-reference voice contract is loaded as Phase 5 Step 0 (see Phase 5). Inline duplication of voice rules in this SKILL.md is the v0.8 drift pattern the v1.0 rewrite removes. When prose authoring begins, load the four references; do not paraphrase them here.

## Self-check before reporting done (the Six Checks)

Before telling Ron the audit is complete, verify:

1. **Spectacle present:** hero shape matches the expected background treatment from Phase 4 (or known engine gap surfaced if not), stats section rendered, asymmetric services grid, oversized stats numbers, voice-pivot anchor strip if persona-applicable.
2. **Zero factual errors:** real business name, real phone, real owners, real license, real services, real testimonials with real names, real promotion wording and price.
3. **Contact form submits to Ron's inbox:** verified by form action, accessKey present, subject includes business name, live submission test passed.
4. **Schema validates:** JSON-LD passes Google Rich Results Test and matches profile.json exactly.
5. **Lighthouse mobile under 2.5s LCP, SEO score 95+, Performance 85+.**
6. **Cold-walk gate (4 rounds):** see § Cold-walk gate above. The four rounds are mode-distinct: Round 1 mechanical (automated by Phase 6); Round 2 structural; Round 3 spectacle; Round 4 finishing-detail. Ron's eye test is Round 4 — walking the deployed URL on mobile first, then desktop, with the question "what would the nitpick eye catch?" Round 5 (first-prospect-impression) fires separately at Phase 8.5 when the deploy is the prospect-pitch URL.

If all six pass, ship. If any fail, fix the source, re-render, and re-walk the failing round (or re-run Phase 6 if the failure was Round 1 mechanical). Do not iterate past done.

## Output format (done report)

```
Prospect audit complete: [Business Name]

Tier: [Tier] ([Score]/100)
Hero background expected: [slideshow / single / mesh-only], engine-emit today: single-photo only
Pages emitted: [list]
Services captured: [count]
Testimonials captured: [count]
Featured promotion: [yes/no]
Photo sources: Google [X], Site [Y], Instagram [Z], Unsplash [W]

Profile saved: ~/grm-sites-prospects/[slug]/profile.json
Prose saved:   ~/grm-sites-prospects/[slug]/prose.json
Assets saved:  ~/grm-sites-prospects/[slug]/assets/
llms.txt:      ~/grm-sites-prospects/[slug]/llms.txt

Quality gates:
  HTML validation: PASS
  Em dash check: PASS
  Banned output check: PASS
  Link check: PASS
  Schema validation: PASS
  Schema-to-profile: PASS
  Unknown-field guard: PASS
  Social metadata: PASS
  Lighthouse mobile LCP: [time]s
  Lighthouse mobile SEO: [score]
  Lighthouse mobile Performance: [score]

Preview URL: [vercel url from deploy.sh]
LESSONS.md: [updated | no new lessons]

Ready for Ron to review on mobile. Next step: open the URL on your phone and run the eye test (check 6).
```

## Known engine-extension items

These engine gaps were surfaced at Session 1 of the v1.0 rewrite (2026-04-28). They are documented here so they don't get lost; they are NOT blockers for v1.0 audit-half shipping.

1. **render.py exit codes unwired.** Docstring promises exit 1 (§7 validation failure) and exit 2 (data shape blocker); `main()` returns 0 unconditionally. Audit-half does not depend on render.py exit codes — Phase 6 grep gates run on emitted HTML independently.

2. **render.py mesh-canvas background.** Hero is one editorial idiom (glass card on background) with three background treatments driven by photo count: slideshow (≥3 photos), single (1–2 photos, optional mesh-canvas overlay), mesh-only (0 photos). render.py ships single + crossfade-slideshow today (slideshow at L1485 fires automatically when `heroCandidatesTop5 ≥ 3`). The remaining gap is mesh-canvas: 0-photo prospects fall back to a static gradient instead of the animated mesh treatment. Scope-clarification 2026-04-30 — slideshow IS shipping (verified across Testerman / Goney's / Bellair); only mesh-canvas pending.

3. **llms.txt has no producer.** deploy.sh expects `llms.txt` as a sidecar; render.py does not emit it. Audit-half writes it at Phase 5.5. Future engine-extension session absorbs llms.txt emission into render.py or deploy.sh.

4. **`scripts/test_form_submission.py` missing.** Phase 6 check 13 (contact form live submission test) depends on this helper. The script existed in the v0.7.2 monolith install but has not been ported to the v1.0 audit-half scripts directory. Either port from snapshot or stand up fresh.

5. **`scripts/mobile_render_check.py` missing.** Phase 6 check 16 (mobile render verification at 375px) depends on this helper. Same status as #4 — existed in v0.7.2 monolith, not ported. Mobile (375px) rendering question for the three hero background treatments is deferred to Session 2 prep — first slideshow flagship validation is the surface where the question gets answered.

6. **v0.8-era prose.json files require migration to page-keyed shape.** Existing v0.8 prospects (Volthom, F1-F8 flagships) have prose.json in flat homepage schema (h1 / hero_kicker / etc. at top level of prose.json). render.py's canonical schema is page-keyed (all slots under `prose.[page].*`, including `prose.homepage.*`). Migration is mechanical (wrap homepage slots under a `homepage` sub-key). Affects Session 2 Volthom validation — re-author Volthom's prose.json to page-keyed shape OR target a fresh prospect; flagged in Session 2 prompt with trade-offs. **Note:** This finding corrected a late-Session-1 misread — Deliverable 3 originally documented the schema as hybrid based on incomplete dict-scope tracing in render.py; verification pass surfaced the error; reversed and corrected before close.

## Version

prospect-site-audit v1.0, 2026-04-28. Rewritten from v0.8 monolith for v1.0 split architecture.

### Changelog

- **v1.0-audit (2026-04-28).** Rewritten from v0.8 monolith. Audit-half outputs profile.json + prose.json only; build-half (render.py) renders, deploy.sh deploys. Phase 5 rewritten with Step 0 voice authority pre-flight load (non-negotiable). Phase 4 simplified after flagship walk: hero is one editorial idiom with photo-data-driven background treatment; no hero-mode slot authored. Phase 5.5 thinned to llms.txt only. Phase 7 dropped (deploy lives in build-half). Six engine-extension items documented. Schema reconciliation (Deliverable 3): pure page-keyed schema documented as canonical across fixture-contract.md, prose-rules.md, and interface-contract.md; v0.8 flat schema preserved as legacy migration reference. Mechanical fix at prose-rules.md L302/L308 aligned to L112 inner-page exemption. Late-Session-1 verification pass surfaced and corrected a hybrid-schema misread; the corrected pure-page-keyed canonical shape is what render.py actually reads. Prior v0.7.2/v0.8 changelog preserved at `side-meta/v0.7.2-monolith.md`.

---
name: prospect-site
description: "Generate a custom multi-page preview website for a local home services contractor prospect from their live URL. Deeply crawls the prospect's real site, captures their brand data (owners, services, testimonials, credentials, colors, photos, promotions), scores their current web presence, picks a hero background mode from a data-driven decision tree, builds a multi-page site using the GRM house style and the GRM voice mapping (Closing Table for hero/promos/cards/stats, Saturday Morning for marquees/section headers, Front Porch for footer/About), runs automated quality gates, and deploys to Vercel. Use this skill whenever the user types /prospect-site followed by a business name and URL, or asks to build a prospect preview site for a local business they want to sell to."
---

# Prospect Site Generator (v0.7.3)

## What this skill does

Given a business name and a live URL, this skill produces a fully built, multi-page preview website that Ron can text or email to the prospect as a sales weapon. The preview uses the prospect's real brand, real services, real testimonials, real owner names, and real promotions. It deploys to a unique Vercel URL in the form `[business-slug]-grm.vercel.app`.

Command format:

```
/prospect-site "Business Name" https://their-site.com [@instagram_handle]
```

Optional `--auto` flag skips the Phase 4 design approval gate. Optional `--from-phase N` resumes from a specific phase when iterating on a previously-started build.

## Architecture

This skill uses the progressive disclosure pattern. SKILL.md contains the workflow, decision trees, hard rules, and pointers. Heavy specification content lives in `references/` and gets loaded on demand:

- `references/hero-patterns.md` — Hero spec (four modes, shared glass card with default and wide variants, video augmentation)
- `references/section-patterns.md` — Every non-hero section (nav, promo bar, trust marquee, services grid, stats dark section, before/after gallery, testimonials, promo callout, FAQ, contact form, footer, mobile bottom CTA)
- `references/css-framework.md` — Typography tokens, color system, breakpoints, rhythm tokens, vanilla JS animation toolkit
- `references/typography.md` — (v0.8) Typography rule set: scale relationships, italic discipline, mono eyebrow system, SectionOpener/StatRow primitives, body measure, mobile scaling, font loading with opsz discipline, ornament rule, structural HTML contracts, exceptions principle
- `references/voiceMap.md` — (v0.8) Voice-register distribution: three registers (Closing Table / Saturday Morning / Front Porch), three-tier service composition, voice-pivot anchor strip, featured pullquote pattern, Front Porch footer, register coupling rules
- `references/content-rules.md` — GRM voice mapping by section, headline patterns, CTA templates, FAQ templates per vertical. Defers to voiceMap.md for register surface identity
- `references/seo-geo.md` — JSON-LD schema templates, llms.txt template, meta tags, OpenGraph, lighthouse-ci spec
- `references/deployment.md` — Vercel naming convention, Static Forms wiring, vercel.json cache-header template, migration playbook pointer
- `references/image-handling.md` — Phase 3 photo sources, Unsplash tier-4 fallback, compression, lazy loading
- `references/anti-slop-rules.md` — Negative design rules, banned fonts, banned layouts, banned phrases
- `references/handoff-discipline.md` — (v0.8) Skill-file authoring protocol: three-lens pattern, foundation preservation, whitelist frame, canonical artifact pattern, handoff vocabulary, scope-gate rule. Governs future skill-file rounds; runtime Claude does not load

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

11. **Foundation preservation is non-negotiable across handoffs.** The deployed build is the source of truth. Any merge into a flagship build must preserve the full SEO/GEO/schema/a11y/script-driver foundation (the 13-item set enumerated in `references/handoff-discipline.md` §3). Modify only the explicit whitelist granted in the authoring prompt; every other element — HTML structure, `<head>` contents, scripts, ARIA, data attributes, schema, meta tags — passes through unchanged. Code's merge gate validates every foundation item before the commit that stages a deploy. Any missing item blocks the commit. See `references/handoff-discipline.md` §3 for detail.

12. **Whitelist-the-changes frame on Design-authoring prompts.** Every Design-authoring prompt that touches a deployed build opens with the whitelist frame from `references/handoff-discipline.md` §4. Modify-surfaces named by explicit item; everything else passes through unchanged; propose-and-wait before expanding the whitelist. Green-field composition from an empty canvas does not need the frame. See `references/handoff-discipline.md` §4 for the full frame text and propose-and-wait clause.

## Phase 0 — Pre-flight integrity check

Goal: fail fast before any Phase 1+ work begins. Better to spend 10 seconds verifying integrations than 30 minutes diagnosing why Phase 5 broke. Phase 0 runs before every prospect build, no exceptions.

Phase 0 has two check categories: hard checks (any failure blocks Phase 1 from starting) and soft checks (failures log a warning but the build continues). The split exists because some integrations are mission-critical (Vercel CLI auth, Node.js version) while others are deferred or optional in v0.7 (HubSpot pipeline configuration is on the v0.7 punch list but not yet complete; backup is a v0.8 target).

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
   - Verify: `~/.claude/skills/prospect-site/SKILL.md` exists AND every file in `~/.claude/skills/prospect-site/references/` is present (13 reference files: hero-patterns.md, section-patterns.md, css-framework.md, content-rules.md, typography.md, voiceMap.md, handoff-discipline.md, image-handling.md, seo-geo.md, deployment.md, anti-slop-rules.md, scale-architecture.md, LESSONS.md).
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

8. **Workspace git tracking initialized.** This is the final step of Phase 0, run after all other hard checks pass and before Phase 1 begins.
   - Action: create the prospect folder at `~/grm-sites-prospects/[business-slug]/` if it does not already exist. Inside it, write `.gitignore` with entries `node_modules/`, `.DS_Store`, `*.log`, `.env`, `.env.local`. Run `git init -b main`. Stage the `.gitignore` and make an initial empty-working-tree commit titled `Workspace initialized for [business name]` (use `--allow-empty` since nothing else exists yet, or include the `.gitignore` in the initial commit — either is acceptable).
   - On failure: report the exact git error. If `git` is not installed or the filesystem is read-only, Phase 1 cannot proceed — this is a hard stop.
   - Why this matters: Prospect workspaces accumulate HTML, photos, and profile data across Phase 1-8. Without git tracking from the start, post-deploy hotfixes (F4 Grandview, F2 footer tap-targets) have zero rollback granularity. Initializing before Phase 1 means every phase boundary is a candidate commit point, and every hotfix after Phase 7 is tracked with file-level precision. Retrofitted on 2026-04-17 across all six pre-v0.7.4 flagships; from v0.7.3 hotfix #11 forward, every build is tracked from the first byte captured.

### Soft checks (warn but continue)

These checks log a warning to the build report but do not block Phase 1. They are tracked for future v0.8 hardening when the underlying integration becomes mission-critical.

1. **HubSpot pipeline configured.**
   - Verify: HubSpot API token is present in environment variables AND the GRM web services pipeline exists with the expected stages.
   - On soft fail: warn "HubSpot pipeline not configured. The skill will not auto-create a deal record on Phase 8. Manual HubSpot entry required after deployment. HubSpot setup is tracked in the Technical debt inventory section of `scale-architecture.md`."
   - Why soft: HubSpot setup is on the v0.7 punch list per `scale-architecture.md` but not yet complete. The skill should not block Phase 1 just because HubSpot isn't ready.

2. **Automated backup running.**
   - Verify: a recent backup of `~/grm-sites-prospects/` exists (less than 24 hours old) at the backup destination.
   - On soft fail: warn "No recent automated backup found. Per scale-architecture.md, profile.json files are the core institutional asset of GRM and backup must be running before active client count exceeds 5. This warning becomes a hard check at v0.8."
   - Why soft: backup is a v0.8 target. Pre-v0.8 builds will not have backup running and the warning is informational, not blocking.

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
  ✓ Workspace git initialized (initial commit <hash>)

Soft checks:
  ⚠ HubSpot pipeline not configured (v0.7 technical debt)
  ⚠ No recent backup found (v0.8 target)
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

4a. **Logo alpha channel check and rebuild.** After download, inspect the logo PNG for alpha channel presence and corner transparency:

    - If source is SVG: skip this step. SVG is transparent by nature.
    - If PNG has alpha channel AND all four corners sample as transparent: accept as-is.
    - If PNG has no alpha channel OR corners are opaque: rebuild the logo with chroma-key transparency:
        * Sample the four corners of the image (20x20px each), average the color
        * Build an alpha mask where pixels matching the corner color within tolerance become transparent
        * Tolerance: pixels with all RGB channels ≥ 250 become fully transparent for near-white backgrounds; adjust the threshold based on the actual corner color sample
        * Feather the mask in the 225–250 range for clean anti-aliased edges
        * Save the result as `assets/logo.png` (4-channel RGBA)
    - If chroma-key cannot produce clean transparency (the dominant corner color also appears in the logo content itself), log a warning, leave the logo opaque, and continue. Phase 6 check 17 (mobile render verification) will catch rendering issues if they surface.

    Implementation: `scripts/rebuild_logo_alpha.py` using Pillow. Detailed spec in `references/image-handling.md` § "Logo alpha rebuild procedure".

    Rationale (Grandview F4 2026-04-16): source logo was a GIF from WordPress with solid-white background. sharp conversion to PNG preserved the white fill as opaque. Combined with the footer-logo filter (removed in v0.7.3 #1), the result was an empty white rectangle in the dark footer. Transparent logos render correctly regardless of footer background color.

4b. **Secondary brand mark detection.** While crawling images during Phase 1 step 3, flag any image that meets ALL of these criteria:

    - Aspect ratio between 0.9:1 and 1.1:1 (near-square or round shape)
    - Long edge between 150px and 600px
    - Located in a CMS upload directory. Recognized path patterns: `/wp-content/uploads/`, `/uploads/`, `/media/`, `/assets/brand/`, `/sites/default/files/`, `/images/brand/`, or similar conventional CMS conventions
    - NOT already identified as the primary logo in step 3
    - NOT a stock photo or gallery image (heuristic: stock photos and gallery images are typically landscape or portrait; round-ratio images in CMS uploads are much more likely to be brand assets)

    These are candidate secondary brand marks — typically round badges, founder portraits, agricultural or industry seals, certification logos, sub-brand marks, or specialty product marks.

    Action for each candidate:

    - Download to `assets/candidate-brand-marks/[original-filename]`
    - Add an entry to `profile.json` under `secondaryMarkCandidates`:
      ```json
      [
        {
          "filename": "badge-farms.avif",
          "source_url": "https://prospect.com/wp-content/uploads/...",
          "dimensions": "396x396",
          "source_path": "/wp-content/uploads/2025/09/...",
          "proposed_use": null
        }
      ]
      ```
    - At the Phase 4 approval gate, present each candidate to Ron with the question: "Secondary brand mark detected. Use where?" Offer options:
        * About page placement
        * Specific service card icon
        * Sub-page header overlay
        * Specialty/farm/product page
        * Skip (not a brand mark)

    Populate the `proposed_use` field based on Ron's selection. Phase 5 reads `proposed_use` values during HTML generation.

    Detailed spec in `references/image-handling.md` § "Secondary brand mark detection".

    Rationale (Grandview F4 2026-04-16): the round "Grandview Farms" badge at `/wp-content/uploads/2025/09/024cf2_...avif` (396x396) was captured by Phase 1 step 3 as generic inline image `s28.avif`, never recognized as a secondary brand mark. The retrofit happened post-build at significant agent-hours cost. Phase 1 flagging prevents this on future builds.

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

5. **Broken internal link capture.** During Phase 2 crawl, track the HTTP status of every internal link followed. For any link that returns a 404 or 5xx status, record it. Add to `profile.json` as:

   ```json
   "brokenLinks": [
     {
       "source_page": "/",
       "target": "/sod-services-ocala-fl/",
       "status": 404
     }
   ]
   ```

   Broken internal links on the prospect's live site are direct "owner stopped paying attention" sales signals. Phase 8 must surface these in the done-report sales-ammunition section.

   If `brokenLinks[]` is non-empty, include a summary line in the Phase 2 report to Ron: "N broken internal links captured (see profile.json.brokenLinks)."

   Rationale (Grandview F4 2026-04-16): the prospect's homepage linked to `/sod-services-ocala-fl/`, which returned 404. A live, customer-facing broken link the owner had not noticed. Pure sales ammunition. Phase 2 must capture automatically; agents should not have to notice incidentally.

6. Report to Ron: pages crawled, services captured, testimonials captured (with name list), owner names, featured promotion, any gaps.

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
- **Premium tier:** Higher-scoring brands get bigger type and more visual weight as a tier benefit.

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

## Phase 5 — Site generation

Goal: build the multi-page website using the GRM house style and the selected hero mode.

For the hero pixel-level CSS (all four modes, shared glass card, video augmentation), see `references/hero-patterns.md`. For every non-hero section (nav, promo bar, trust marquee, services grid, stats dark section, before/after gallery, testimonials, promo callout, FAQ, contact form, footer, mobile bottom CTA bar), see `references/section-patterns.md`. SKILL.md contains only the high-level section order and hard rules.

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

**Pages explicitly out of scope for v0.7:** location sub-pages (Ocala Electrician, Dunnellon Electrician as separate pages), blog and news pages, financing pages as standalone (content rolls into homepage promo callout instead), warranty and insurance pages as standalone (content rolls into homepage FAQ and trust marquee), separate team pages (content rolls into about.html), project portfolio pages (use gallery.html). When Phase 2 captures these page types, Phase 5 either ignores them or rolls their content into existing homepage sections per the decision table in `references/content-rules.md`.

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
- The stats section ALWAYS uses the dark treatment. This is non-negotiable and gives every v0.7 flagship the mandatory visual rhythm reset.
- Every section gets the Glare Hover, Shimmer Button, or other Magic UI enhancement specified in `references/css-framework.md` where appropriate.
- Run the anti-slop rule check from `references/anti-slop-rules.md` on all generated copy and CSS before writing files.

### Cross-file integration points

Phase 5 must wire up the following connections between the reference files. These are the "glue" that makes css-framework.md, hero-patterns.md, and section-patterns.md work together. Missing any of them will produce broken output.

**1. Tier class on `<html>` element.**
Phase 5 applies exactly one tier class to the `<html>` element based on the tier decision from Phase 4:

```html
<html lang="en" class="tier-premium">    <!-- or tier-professional / tier-standard -->
```

This class drives the tier-specific token overrides in `css-framework.md` (different heading fonts, spacing multipliers, and hero headline sizes). If the class is missing, every build renders as Professional regardless of the Phase 4 decision.

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
Phase 4 runs the Node.js build-time utilities documented in `css-framework.md` under "Phase 4 build-time color utilities" to compute `--color-primary-rgb`, `--color-accent-rgb`, and `--color-dark-primary` values before Phase 5 writes `style.css`. If these values are not pre-computed, the `:root` block will be incomplete and several sections will render with broken hover states and focus rings.

## Phase 5.5 — SEO and GEO injection

Goal: make the generated site findable by Google, Bing, and AI answer engines (ChatGPT, Claude, Perplexity, Gemini).

For the full schema templates and llms.txt content, see `references/seo-geo.md`. Short version:

Every page — index, about, services, testimonials, contact, faq, and any service sub-pages — gets the complete social metadata block from the template in `references/seo-geo.md` > "Meta tag templates". This means a minimum of 10 OpenGraph tags plus 5 Twitter Card tags per page, with og:image and twitter:image pointing at an absolute https:// URL of a real file in `assets/photos/`. This mandate is non-negotiable — partial blocks or missing blocks on secondary pages are the Bug 4 failure mode from A-1 Payless Septic (2026-04-15) and will fail Phase 6 check #18.

Every page also gets: LocalBusiness JSON-LD on the homepage, Service JSON-LD on service sub-pages, FAQPage JSON-LD on pages with FAQ, Review JSON-LD on testimonials, canonical URL, robots meta, and a sitemap.xml entry.

Every site gets: `sitemap.xml` at root, `robots.txt` at root, `llms.txt` at root (pointing AI crawlers at clean markdown versions of key pages).

Run validation: JSON-LD passes Google Rich Results Test, sitemap validates against sitemaps.org spec, llms.txt follows the AnswerDotAI spec format.

## Phase 6 — Pre-deploy verification

Goal: automated quality gates that fail the build if any check fails. No shipping broken sites. No relying on Ron's eye for things a script can verify.

Phase 6 runs twenty checks organized into nine categories. All checks must pass before Phase 7 deploy. On any failure, log the specific failure and stop.

### Content integrity checks

1. **HTML validation.** All pages pass W3C HTML5 validation or log only minor warnings.

2. **Em dash check.** Grep all generated HTML for em dashes in both UTF-8 (`\u2014`) and HTML-entity (`&mdash;`, `&#8212;`) encodings. Fail if any found.

3. **Banned output check.** Grep all generated HTML for the banned strings in `references/content-rules.md` — both the voice phrase list (corporate jargon, AI tells, cliches) and the HTML slop list (hallucinated tags and trailing-fragment patterns). Fail if any found.

4. **Link check.** All internal links resolve. No 404s. No `href="#"` or `action="#"` placeholders.

5. **Image reference check.** All `<img>` tags reference files that exist in `assets/photos/`. No broken references. No hotlinked external images.

6. **H1 count check.** Every page has exactly one `<h1>` element. Zero H1s or multiple H1s fails the build.

7. **Mixed content check.** No `http://` references inside `<img src>`, `<link href>`, `<script src>`, or inline CSS `url()` values. All references must be `https://` or relative. Mixed content breaks the SSL padlock and can block images.

### Data integrity checks

8. **Stats counter discipline.** Every stat in the stats section is either ANIMATED (has `data-target` attribute with a whole number value) or STATIC (no `data-target` attribute, content is plain text). Mixed or malformed stats fail the build. This catches the "0 Years Licensed" broken counter bug class.

9. **Phone number consistency.** The prospect's real phone number appears in: nav bar, hero CTA, footer, contact section, and JSON-LD schema. Regex the number across all five locations and confirm exact string match. A typo in any one location fails the build.

### Structural integrity checks

10. **Dark section count.** The generated homepage contains exactly one dark-background section (the mandatory stats section from Phase 5). Zero dark sections or two-plus dark sections fail the build. This enforces the v0.7 visual rhythm rule architecturally, not by convention.

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

### Social metadata integrity

18. **Social metadata completeness check.** Verify every generated page contains the complete social metadata block per the template in `references/seo-geo.md` > "Meta tag templates". For each of `index.html`, `about.html`, `services.html`, `testimonials.html`, `contact.html`, `faq.html` (and any service sub-pages): grep for and count the required OpenGraph tags (`og:type`, `og:title`, `og:description`, `og:url`, `og:image`, `og:image:width`, `og:image:height`, `og:image:alt`, `og:site_name`, `og:locale` — 10 minimum) and Twitter Card tags (`twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`, `twitter:image:alt` — 5 minimum). Then verify `og:image` and `twitter:image` values are absolute URLs beginning with `https://`, and that the image path each URL resolves to exists as a real file in `assets/photos/`. Any missing tag on any page, any relative URL, or any `og:image`/`twitter:image` pointing at a file that does not exist fails the build. This catches the Bug 4 failure mode from A-1 Payless Septic (2026-04-15) where the skill generated only a partial social block on index.html, minimal og-only stubs on four secondary pages, and zero metadata on faq.html.

### Data fabrication checks

19. **Schema-to-profile cross-reference.** For every JSON-LD block on every page, assert that `ratingValue`, `reviewCount`, `foundingDate`, `telephone`, `address`, `priceRange`, and any numeric or factual field matches `profile.json` exactly. Any mismatch fails the build. Implementation: `scripts/verify_schema_against_profile.py` loads both, compares, reports deltas. This rule was spec'd in `seo-geo.md` line 491 but not previously enumerated in the Phase 6 checklist, so it never ran as an automated gate.

20. **Unknown-field guard.** `profile.json` must include a top-level `"unknownFields": []` array listing any data point that Phase 1/2 searched for but could not capture (e.g., `"license_number"`, `"bbb_rating"`, `"founding_year_verified"`). Phase 6 greps generated content for any mention of those fields' associated claim vocabulary (defined in `anti-slop-rules.md` "Unknown-field claim vocabulary" section) and fails the build if claims are made about unknown data.

    Example: if `"license_number"` is in `unknownFields`, the grep checks for "licensed", "license", "state-licensed", "licensing" — the vocabulary tied to that field.

    This check complements `content-rules.md` "Banned credential and trust claims" (which is absolute-banned-unless-captured). Check 20 handles the case where `profile.json` explicitly declares a field as unknown, giving Phase 6 a definitive signal to fail any claim in that domain.

    Implementation: `scripts/verify_unknown_fields.py` loads `profile.json`, reads `unknownFields[]`, looks up each field's claim vocabulary from `anti-slop-rules.md`, greps generated HTML, reports any match.

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
4. **Slug reconciliation.** The final project name from step 3 determines the deployed alias (`[final-project-name].vercel.app`). Before deploying, grep all generated `.html` files, `sitemap.xml`, `robots.txt`, and `llms.txt` for any `.vercel.app` reference that differs from this final alias. If any stale references are found (Phase 5 wrote URLs using the Phase 1 draft slug, but the final project name differs due to slug shortening or collision suffix), replace them across all affected files before deploying. Affected artifacts: `<link rel="canonical">`, `<meta property="og:url">`, form `redirectTo` hidden inputs, JSON-LD `@id` and `url` fields, `sitemap.xml` `<loc>` entries, `llms.txt` page links, and `robots.txt` Sitemap pointer. Log the reconciliation (old alias → new alias) for the Phase 8 done report. If no stale references are found, proceed directly to step 5. For the detailed reconciliation procedure, see `references/deployment.md` > Step 2.5.
5. Deploy: `vercel --prod --yes --name [final-project-name]`
6. Capture the returned URL.
7. Test the URL with curl. Confirm 200 status and the business name appears in the body.
8. Report the live URL to Ron in a visible format.

For full deployment and domain migration details, see `references/deployment.md`.

## Phase 8 — Profile, LESSONS.md, done report

Goal: save complete build record, append institutional lessons, report completion.

Steps:

1. Promote `profile-draft.json` to `profile.json` with the final `previewUrl` populated.
2. If anything unusual happened during the build (unexpected data, soft warnings, recovery actions, novel photo assignment decisions), append an entry to the project-level `LESSONS.md` at `~/.claude/skills/prospect-site/LESSONS.md` in the format shown in that file.
3. Output the done report (see Output Format section below).

## Post-deploy hotfix workflow

When making post-deploy hotfix edits to a deployed workspace, commit changes in the workspace repo before redeploying. One logical change per commit. This gives rollback granularity below the file level.

Standard flow:

1. Diagnose first, no writes. Report findings; wait for Ron to confirm the fix.
2. Edit the minimum file set. Do not fold unrelated cleanup into a hotfix.
3. Grep-verify the fix on disk.
4. `git add <files>` (prefer naming files explicitly over `git add .` to avoid pulling in unrelated changes), then `git commit -m "Fx hotfix: <one-line summary>"` where `Fx` is the flagship number (F1 through F6 at v0.7.3, continuing forward).
5. Redeploy under the existing `[slug]-grm.vercel.app` alias via `vercel --prod --yes`.
6. Live smoke test: curl the affected URL, grep the response for the expected change.
7. Report: commit hash, deployment ID, smoke-test result.

If Phase 1 diagnostic reveals the scope is broader than the brief (e.g., fixing tap-target sizing on F2 surfaces a second a11y issue), pause and expand scope with Ron before committing. Scope creep inside a single commit loses the rollback granularity this workflow exists to create.

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
Slug reconciliation: [reconciled X references (old-alias → new-alias) | no action needed]

Quality gates:
  HTML validation: PASS
  Em dash check: PASS
  Banned output check: PASS
  Link check: PASS
  Schema validation: PASS
  Social metadata check: PASS
  Lighthouse mobile LCP: [time]s
  Lighthouse mobile SEO: [score]
  Lighthouse mobile Performance: [score]

Profile saved: ~/grm-sites-prospects/[slug]/profile.json
Assets saved: ~/grm-sites-prospects/[slug]/assets/
LESSONS.md: [updated | no new lessons]

Ready for Ron to review on mobile. Next step: open the URL on your phone and run the eye test (check 6).
```

## Version

prospect-site v0.7.2, updated Wednesday April 16, 2026. Built on v0.5's foundation (heavily specified flagship 1 hero, Phase 2.5 SEO audit, Phase 5.5 GEO injection, Plant Street voice, CSS hygiene rules) plus Cowork's 21st.dev hero research (Glassmorphism Trust Hero as content layer, data-driven background modes), plus anthropics/skills progressive disclosure pattern, plus frontend-design anti-slop rules, plus Magic UI extracts for button and card enhancements, plus Aceternity pattern rebuilds in vanilla JS. Architectural antidote to v0.6's four-pattern collapse: one structural pattern, heavily specified, deterministic data-driven variation.

### Changelog

### v0.7.3 hotfix #11 — 2026-04-17 evening — Phase 0 git tracking requirement

Phase 0 gains an eighth hard check: every prospect workspace must be git-initialized before Phase 1 begins. Workspaces accumulate HTML, photos, and profile data across phases; post-deploy hotfixes need rollback granularity below the file level. Also adds a "Post-deploy hotfix workflow" section codifying the commit-before-redeploy pattern used on F4 Grandview's NAP hotfix tonight. All six pre-v0.7.4 flagships (F1-F6) were retrofitted with initial commits on 2026-04-17; from this hotfix forward, every new build is tracked from the first byte captured.

### v0.7.3 hotfix #10 — 2026-04-17 afternoon — Skip-link 8px visible dash fix

Skip-link visible 8px dash at top of viewport fixed. Corrected CSS in `references/css-framework.md`: `top: -48px; height: 40px; padding: 10px 20px;` so the skip-link sits fully off-screen until keyboard focus pulls it into view. Shipped before F6 Oxford Lawn kickoff and validated clean on that build's first generation. Commit `b4591c8`.

### v0.7.3 — 2026-04-16 evening — "Grandview Patch"

Evening session after F4 Grandview build. Nine atomic commits addressing bugs surfaced during the build and post-build review.

Fixes:

- **#1** Remove footer-logo brightness/invert filter — multi-color logos now render in native brand colors on dark footers (`e40f19b`)
- **#2** Progressive-enhancement guard on `[data-reveal]` — sections default visible, only hide when JS confirms it will reveal (`f302d49`)
- **#3** Banned credential and trust claims list — "Licensed", "Insured", "Certified", etc. require matching `profile.json` data or Phase 6 check 3 fails (`13b4189`)
- **#4** Phase 6 check #19: schema-to-profile cross-reference (enumerated the already-spec'd `seo-geo.md` rule) (`074e936`)
- **#5** Phase 6 check #20: unknown-field guard — `profile.json` `unknownFields[]` + anti-slop vocabulary map (`413ac25`)
- **#6** Phase 1 step 4a: logo alpha channel check + chroma-key rebuild for no-alpha source logos (`b90b57a`)
- **#7** Phase 1 step 4b: secondary brand mark detection — round-ratio CMS uploads flag as candidate marks at Phase 4 gate (`6d60a9f`)
- **#8** Phase 2: broken internal link capture as sales ammunition (`9a1e9e9`)
- **#9** This release commit — version bump, changelog, LESSONS augmentation, tag

Validation plan: F5 build on Friday validates against a fresh prospect. If v0.7.3 has a bug, catch it in F5 and patch before F6.

Retrofit required: F1, F2, F3, F4 need items #1 and #2 backported to their deployed CSS before Monday sales calls.

v0.7.2 — Validated via F3 (Chad's Lawn and Landscape). Bug 2 (CTA trailing-fragment hallucination), Bug 4 (social metadata completeness), and Bug 5 (Phase 7 slug regeneration) confirmed fixed. Honeypot field added to contact form template.

v0.7.1 — Initial tagged release after A-1 Payless Septic (F2) build.

v0.7 — Built Thursday April 9, 2026. First complete spec.

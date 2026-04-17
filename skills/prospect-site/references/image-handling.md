# Image Handling Reference

Part of the prospect-site skill v0.7. Loaded by Phase 3 at the start of photo capture and referenced again by Phase 5 when generating HTML with image references.

This file owns every decision about photography on a generated contractor site. Photo sourcing, quality scoring, content type tagging, before/after pair detection, the sharp-based compression pipeline, responsive size generation, attribution rules, and the photo manifest format in `profile.json`. If it involves a visual asset on a generated site, it is documented here.

Photos are the single largest factor in whether a generated site looks like a real business or a template. A site with real owner photos, real project work, and real local scenery feels built for that specific prospect. A site with stock photos feels like everyone else. The rules in this file exist to bias every build toward the first outcome.

---

## How Phase 3 and Phase 5 use this file

**Phase 3** reads this file at the start of photo capture. Phase 3 is responsible for:

1. Pulling photos from the five-tier source pipeline
2. Scoring each captured photo against the quality rubric
3. Applying disqualifier rules
4. Tagging photos with content types
5. Detecting before/after pairs
6. Running the sharp compression pipeline to produce WebP and AVIF outputs at responsive sizes
7. Writing the complete photo manifest to `profile.json`
8. Enforcing attribution requirements

**Phase 5** reads this file when generating HTML that references photos. Phase 5 is responsible for:

1. Reading the photo manifest from `profile.json`
2. Writing `<picture>` elements with correct srcset values referencing the Phase 3 outputs
3. Wiring photo references into hero modes, services grid cards, testimonials, before/after sliders, footer, and sub-pages
4. Rendering the attribution block in the footer when attributed photos were used
5. Writing `window.BA_PAIRS` inline for the before/after slider thumbnail navigation

The split is clean: Phase 3 processes and stores photos, Phase 5 references them in HTML. Neither phase reaches across the boundary.

---

## The five-tier photo pipeline

Phase 3 pulls photos from up to five sources in priority order. Each tier has a specific role in the overall library. Phase 3 does NOT stop at tier 1 — it pulls from every available tier and aggregates into a single scored library. The tier indicates source quality and licensing constraints, not processing order.

### Tier 1: Google Places Photos (primary source)

**What it is.** Photos uploaded to the prospect's Google Business Profile by the business owner, by customers, or by Google's own contributors. Pulled via the Google Places API (Place Details with `fields=photos`, then Place Photos for each photo reference).

**Why it leads.** Contractors who care about their Google profile upload their best work. Customers who had good experiences upload real project photos. The quality ceiling of Google Places photos is frequently higher than the prospect's own website because websites get neglected while Google profiles get active attention.

**How to fetch.**

1. Phase 1 captured the prospect's Google Places ID during the initial business data lookup
2. Phase 3 calls Place Details with `fields=photos` to get a list of photo references
3. For each photo reference, Phase 3 calls Place Photos with `maxwidth=1600` to get the highest reasonable source width
4. Phase 3 stores the raw response in `~/grm-sites-prospects/[slug]/raw-photos/google/` with the photo reference as the filename
5. Photographer attribution is captured and stored alongside each photo

**Typical volume.** 5 to 30 photos per prospect. Contractors with strong Google profiles often have 20+. Contractors with weak profiles may have 3-5.

**Quality expectations.** Variable. Owner uploads are usually good. Customer uploads range from excellent (real project shots) to poor (blurry phone pictures of receipts). Every Google Places photo goes through the full quality scoring and disqualifier pipeline before being accepted into the library.

**Attribution requirement.** Google's Maps Platform Terms of Service require displaying photographer attribution when Place Photos are used. Phase 3 stores attribution strings (e.g., "Photo by John D. via Google") and Phase 5 renders them in the footer. Failing to render attribution is a Terms of Service violation and cannot happen on any generated site.

**Cost.** Google Maps Platform gives every account a $200 per month free credit. Each Place Photos request costs approximately $0.007. Processing 30 photos for one prospect costs about $0.21. Processing 100 prospects per month costs about $21, well inside the free credit. For practical purposes, Google Places photos are free at GRM's current scale.

**API key.** Stored at `~/grm-sites-prospects/.env` under `GOOGLE_PLACES_API_KEY`. Phase 3 reads this at startup and fails fast if it's missing.

### Tier 2: Prospect's own website (secondary source)

**What it is.** Photos directly scraped from the prospect's existing website during Phase 2's multi-page crawl. Every `<img>` tag, every CSS `background-image` URL, every `<picture>` source is captured.

**Why it's secondary.** Most contractor websites have older photography that hasn't been refreshed in years. Resolution is often low (many sites still use 800x600 JPEGs from 2018). Composition is often poor (straight-on phone snapshots of finished work with no context). But some prospects have well-maintained sites with excellent photography, and when they do, Tier 2 becomes the primary source because the photos are already tied to specific services and pages.

**How to fetch.** Phase 2 already captured HTML for every page on the prospect's site during the crawl. Phase 3 parses those saved HTML files for image references, resolves relative URLs to absolute URLs against the prospect's domain, downloads each image, and stores the raw file in `~/grm-sites-prospects/[slug]/raw-photos/site/`.

**Typical volume.** 10 to 100 photos per prospect. Heavier than Google Places usually, but with more filler (decorative icons, duplicate headers, generic hero backgrounds).

**Quality expectations.** Highly variable. Some contractors have professional photography. Most don't. The disqualifier pipeline is particularly aggressive on Tier 2 sources because the average quality is lower than Google Places.

**Attribution requirement.** None. These photos belong to the prospect, and we're rebuilding the prospect's own site, so reuse is implied. However, Phase 3 must detect and reject third-party stock photos that the prospect may have licensed (watermarks, EXIF metadata from Shutterstock, Getty, etc.) because those licenses don't transfer to GRM.

**Context preservation.** When a photo comes from a specific page (e.g., `/services/generators/`), Phase 3 records the page context so photo assignment later can match photos to services automatically.

### Tier 3: Instagram (opportunistic source)

**What it is.** Photos pulled from the prospect's Instagram profile if Phase 1 captured an Instagram handle.

**Why it's tier 3.** Instagram photos are often the prospect's best current photography because contractors put their best work on Instagram to attract customers. But Instagram scraping is technically restricted, rate-limited, and subject to Instagram's Terms of Service. Phase 3 treats Instagram as an opportunistic source: pull if available through sanctioned means, skip cleanly if not.

**How to fetch.** Multiple approaches in order of preference:

1. **Official Instagram Graph API** — requires app registration and user-delegated auth. Only usable if the prospect has a Business or Creator account and GRM has been explicitly authorized. Not viable for cold-pipeline prospects. Defer to v0.8 when this becomes a paid client enablement feature.
2. **oEmbed endpoint for public posts** — Facebook's oEmbed endpoint returns post metadata including image URLs for public Instagram posts when provided with a specific post URL. Usable when Phase 2 captured direct post URLs (e.g., in the prospect's website footer social links).
3. **Manual upload fallback** — when Instagram scraping is not viable, Phase 3 prompts Ron to manually save 6 to 12 best photos from the prospect's Instagram and drop them in `~/grm-sites-prospects/[slug]/raw-photos/instagram/`. Phase 3 picks them up from that folder automatically and processes them like any other tier 3 source.

**Typical volume.** 0 to 12 photos per prospect, depending on method.

**Quality expectations.** Usually higher than website photos because Instagram is where contractors curate. Composition is typically better. Color grading is often applied.

**Attribution requirement.** If the Instagram account is the prospect's own business account, attribution is not required. If photos came from the prospect tagging customers or other accounts, those photos are NOT usable without explicit permission and Phase 3 rejects them.

**Never fabricate Instagram data.** If scraping fails and no manual upload happens, Phase 3 records zero Instagram photos in the manifest and moves on. Phase 5 builds the site without Instagram sourced photography. Never synthesize Instagram data from other sources.

### Tier 4: Unsplash (stock fallback)

**What it is.** Free-to-use stock photography from Unsplash, pulled via their API.

**Why it's tier 4.** Used when tiers 1 through 3 did not produce enough photos for specific section uses. Stock photography cannot make specific claims about the prospect's actual work, but it CAN serve as category imagery when the section's job is to illustrate a type of work rather than document a specific project. The rules below define exactly where stock is appropriate and where it is forbidden.

### Stock photo tier rules (applies to Unsplash and Pexels)

Stock photo use is governed by a two-tier rule that distinguishes documentation sections from category imagery sections. The rule applies identically to Unsplash (Tier 4) and Pexels (Tier 5) sources.

**Tier A sections — no stock ever (strict).**

These sections make specific factual claims about the prospect's work, customers, or people. Stock here would be deceptive.

- **Before/after gallery** — claims specific projects completed by the prospect
- **Testimonial headshots** — claims specific customer identities
- **About page owner photos** — claims specific owners and team members
- **About page shop or storefront photos** — claims specific business location
- **Hero photo backgrounds when Phase 3 captured 8+ real photos** — use what the prospect actually has
- **Any photo that appears with a specific caption making a factual claim** (e.g., "Ben Tucci on a job site in Dunnellon, 2024")

If a Tier A section cannot find real prospect photography, the section either falls back to a neutral design (icon-only cards, mesh gradient background, omitted section) or is left out of the build entirely. Stock is never substituted into a Tier A section under any circumstances. Phase 6 check 6 verifies this as a hard gate.

**Tier B sections — curated quality stock allowed (relaxed).**

These sections show category imagery. The user understands these photos illustrate the type of work, not specific projects. Stock is appropriate here when it is genuinely high quality and depicts real category work.

- **Services grid standard cards** when the prospect has no service-specific photos
- **Services grid featured card (2x2 Bento)** when the prospect has no landscape or square service-specific photos
- **Hero photo backgrounds when Phase 3 captured zero real photos** (curated stock photo as the `glass-single-mesh` base layer instead of falling back to `glass-pure-mesh`)
- **Service sub-page sub-hero backgrounds** when the specific service has no assigned photo
- **Neutral texture backgrounds** (wood grain, concrete, generic professional interiors) for section dividers or callout backgrounds

**Additional filters that every Tier B stock photo must pass:**

1. **Must show actual work in the category.** A plumber fixing a pipe, an electrician at a panel, a painter on a ladder, a pool technician testing water. Never handshakes, never stock-model headshots, never generic "business" photos, never abstract concept images.
2. **No identifiable people in the foreground.** Rules out the stock-model look that undercuts credibility. People may be present but cannot be the focal subject.
3. **Quality score 70 or higher** on the scoring rubric (stricter than the general 60+ acceptance bar).
4. **Precise category match.** An "electrician" stock photo cannot substitute for a "surge protection" service card. The search query and source platform tagging must match the specific service being illustrated, not just the broad trade vertical.
5. **No competitor branding visible.** No photos showing identifiable third-party business logos, truck decals, or branded uniforms.
6. **Passes the anti-slop eye test.** Even if a photo meets all the above rules mechanically, it must look like something a Marion County contractor would actually have on their wall, not something a marketing agency would drop into a template. This is a human judgment call Ron makes at the Phase 4 approval gate when stock photos are surfaced.

**The underlying principle.** Stock photos of real work being done = illustrative category imagery = acceptable where the section's job is illustration. Stock photos of models, handshakes, or concepts = template filler = never acceptable. The test is whether a photo claims specific facts (Tier A) or illustrates a category (Tier B).

**Conversion note for future client work.** When a prospect converts from preview to paying client, Tier B stock photos become a built-in upgrade opportunity. The sales conversation becomes: "Your preview uses category imagery where you didn't have your own photos yet. For your live site we can schedule a photo shoot or you can provide your own photography." This is a natural upsell for a future photography add-on service and a reason to continue the client relationship beyond initial deployment.

---

**How to fetch.** Unsplash API with category-specific search queries. Search queries are derived from the prospect's trade vertical and location. Example: `electrician Florida` returns generic electrician stock. Phase 3 pulls top results, scores them, and filters out any photo featuring identifiable people (stock models look like stock models and identifiably undercut credibility).

**Attribution requirement.** Unsplash license does not require attribution but strongly recommends it. GRM policy: always attribute Unsplash photos in the footer. Attribution format: "Photo by [photographer] on Unsplash" with a link to the photographer's Unsplash profile.

**Cost.** Unsplash API is free for non-commercial use with attribution. Commercial use is technically allowed under the Unsplash License but for GRM's scale the free tier with attribution is appropriate.

### Tier 5: Pexels (stock backup)

**What it is.** A second stock photography source, used when Unsplash doesn't return good results for a specific trade vertical. Notably better than Unsplash for trade contractors (plumbers, HVAC, roofers, pest control) because Pexels has broader coverage of blue-collar and service work imagery.

**Why it's tier 5.** Same role as Unsplash. Pexels is listed separately because it sometimes has better results for specific verticals where Unsplash is weak.

**How to fetch.** Pexels API. Same search query pattern as Unsplash: trade vertical plus location.

**Attribution requirement.** Pexels license does not require attribution but recommends it. GRM policy matches Unsplash: always attribute in the footer.

**Cost.** Pexels API is free with attribution.

**Usage rule.** Phase 3 tries Unsplash first. If Unsplash returns fewer than 3 usable photos for the needed category, Phase 3 tries Pexels. Between the two, Phase 3 aggregates the best candidates and discards duplicates (photos appearing in both libraries).

---

## Photo quality scoring

Every captured photo is scored against a quality rubric before being accepted into the library. The rubric produces a numeric score from 0 to 100. Photos below 40 are rejected automatically. Photos 40 to 60 are soft-flagged (logged with warning but allowed). Photos above 60 are accepted without warning.

### Scoring components (100 points total)

**Resolution (30 points).**
- 30 points: 2000px or larger on long edge
- 20 points: 1600px to 1999px on long edge
- 10 points: 1200px to 1599px on long edge
- 0 points: under 1200px on long edge (automatic hard reject regardless of other scores)

**Aspect ratio alignment with intended use (20 points).**
- 20 points: landscape 16:9 or wider (matches hero backgrounds)
- 15 points: landscape 4:3 to 16:9 (works for most sections)
- 10 points: square (works for services grid featured cards and testimonials)
- 5 points: portrait (works for owner photos and sidebar uses only)
- 0 points: extreme panorama or extreme portrait ratios (unusable in most layouts)

**Composition quality (20 points, heuristic).**
- 20 points: clear subject, balanced framing, no obvious compositional errors
- 15 points: readable subject with minor framing issues
- 10 points: subject visible but composition is off (tilted horizon, cluttered background, subject too far from camera)
- 0 points: unidentifiable subject, extreme blur, or other fundamental failure

Composition is subjective. For automated scoring, Phase 3 uses a combination of: EXIF metadata analysis (professional cameras typically produce better composition), sharpness detection (blurry photos automatically downgrade), and content analysis via an image classification model if available. When no classification is available, Phase 3 defaults all uncertain photos to 15 points (soft midpoint) and relies on downstream use-case matching to filter.

**Color and lighting (15 points).**
- 15 points: natural exposure, accurate white balance, reasonable dynamic range
- 10 points: usable but flat or slightly off
- 5 points: obvious exposure problems (blown highlights, crushed shadows, severe color cast)
- 0 points: severely underexposed, severely overexposed, or unusable

**Relevance to trade vertical (15 points).**
- 15 points: photo clearly depicts work or context relevant to the prospect's trade
- 10 points: photo is generic but consistent with the trade (e.g., a shop interior for any service business)
- 5 points: photo is unrelated but inoffensive (a sunset, an office plant)
- 0 points: photo is actively off-brand (a competitor's work, a random meme, an unrelated business)

Relevance is the hardest to score automatically. Phase 3 uses a combination of: source context (a photo from the prospect's `/services/generators/` page is presumed relevant to generators), filename and alt text (`hero-shop-interior.jpg` hints at content), and rough content classification when available. When uncertain, Phase 3 defaults to 10 points.

### Hard rejects regardless of score

These disqualifiers cause automatic rejection even if the numeric score is high:

1. **Watermarks.** Any visible watermark (text, logo, or pattern) from a third-party photography service. Detected via OCR pass and template matching against common watermark patterns.
2. **Stock photo EXIF metadata.** If the EXIF metadata identifies the source as Shutterstock, Getty, Adobe Stock, iStock, or any licensed stock provider, the photo is rejected. We cannot reuse stock photos the prospect licensed because the license doesn't transfer.
3. **Identifiable third-party brand logos.** A photo of a competing business, a product with prominent unrelated branding, or a building with identifiable third-party signage (unless it's the prospect's own location).
4. **Baked-in promotional text.** Photos with text overlays advertising promotions, phone numbers, or business names baked into the pixels. Looks like a flyer, not a photo.
5. **Identifiable minors.** Any photo featuring identifiable minors unless Phase 3 has explicit confirmation of permission (which it never does in cold pipeline mode). Hard reject for privacy reasons.
6. **Resolution under 1200px on long edge.** Not enough pixels for any responsive size output.
7. **Corrupted or unreadable files.** EXIF parse failure, format mismatch, or sharp decode failure.
8. **Duplicate of a higher-scoring photo already in the library.** Phase 3 runs perceptual hashing (pHash) on every photo and rejects duplicates, keeping only the highest-scoring version.

### Soft flags (logged but allowed)

These produce a warning in the manifest but don't cause rejection:

1. Moderate blur (not severe enough to be unusable)
2. Off-center composition
3. Flat lighting or dull colors
4. Cluttered background
5. People visible but not identifiable (stock models, crowd shots)
6. Unknown provenance (no EXIF, no source context)

Soft flags help Ron make manual override decisions at the Phase 4 approval gate. When a photo is soft-flagged but Phase 3 assigned it to a critical role (hero, featured service), Ron sees the warning and can override.

---

## Content type tagging

After scoring, Phase 3 tags each accepted photo with one or more content types. Tags determine which sections of the generated site can use the photo.

### Tag definitions

**`heroCandidates`** — landscape photos 1600px+ long edge, score 60+, aspect ratio 4:3 to 21:9, subject clear, no identifiable people in foreground. These are the photos Phase 4 considers for the hero background mode decision tree. Minimum 8 required to trigger parallax mode, 4 for crossfade, 1 for single-mesh, 0 for pure-mesh.

**`servicesGridPhotos`** — any orientation, score 50+, clearly depicts work related to a specific captured service. Phase 3 attempts to match each captured service to a specific photo based on source context (a photo from `/services/generators/` matches the Generators service) or filename hints. When no specific match exists, the services grid uses icon-only cards for that service.

**`featuredServicePhoto`** — the single best services photo per build, used as the background of the 2x2 featured card in the Bento services grid. Phase 3 picks the highest-scoring photo from `servicesGridPhotos` that has landscape or square orientation.

**`beforeAfterPairs`** — photos that were identified as before/after pairs through the pair detection logic below. Every pair is stored as a tuple of two photo IDs plus a caption.

**`aboutPagePhotos`** — photos that depict owners, staff, the shop or storefront, or company history. Typically 2 to 5 per build. Used on the About page (Front Porch voice).

**`generalLibrary`** — photos that scored above 40 but don't fit into any specific content type. Available as backgrounds for optional sections or as fallback photography. May go unused.

**`rejectedPool`** — photos that scored below 40 or hit a hard disqualifier. Stored in the manifest for debugging only, never rendered on the site.

### Multi-tag photos

Some photos fit multiple content types. Phase 3 allows multi-tagging. For example, a photo of the prospect's shop exterior might tag as both `heroCandidates` and `aboutPagePhotos`. Phase 4's decision tree picks which use wins based on scarcity: if the site has only 2 photos that qualify as `heroCandidates`, the shop exterior stays in that pool; if there are 12, the shop exterior goes to `aboutPagePhotos` where it's more valuable.

### Content type assignment algorithm

```
FOR each accepted photo:
  Determine orientation (landscape / portrait / square)
  Determine resolution tier
  Determine subject heuristic (work / people / location / object / unknown)
  Determine source context (which page, which folder, which API call)

  IF orientation is landscape AND resolution >= 1600 AND score >= 60:
    ADD to heroCandidates

  IF subject matches a captured service (by context, filename, or content):
    ADD to servicesGridPhotos with service slug
    IF photo is highest-scoring services photo with landscape/square:
      SET as featuredServicePhoto (only one per build)

  IF subject is people (owner, team) AND score >= 50:
    ADD to aboutPagePhotos

  IF source context is shop, storefront, or exterior:
    ADD to aboutPagePhotos

  IF pair detection logic identifies this photo as a before/after pair member:
    ADD to beforeAfterPairs

  IF no specific tag applies AND score >= 40:
    ADD to generalLibrary

  ELSE IF score < 40:
    ADD to rejectedPool
```

Phase 3 runs this algorithm on every photo from every tier, producing a complete manifest.

---

## Before/after pair detection

Before/after galleries are the single most valuable section for pressure washers, painters, roofers, pool builders, and remodelers. The detection logic in this section finds pairs that Phase 5 renders in the drag slider.

### Detection signals (checked in order)

**Signal 1: Filename convention.**

Phase 3 scans photo filenames for common before/after patterns:

- `before-*.jpg` and `after-*.jpg` with matching suffixes
- `*-before.jpg` and `*-after.jpg` with matching prefixes
- `*_b.jpg` and `*_a.jpg` (common shorthand)
- Numeric pairs like `01-before.jpg` / `01-after.jpg`

When Phase 3 finds filenames matching these patterns and the base names match, the photos are candidate pairs.

**Signal 2: Sequential positioning in portfolio page markup.**

When Phase 2 crawled a portfolio or project page, Phase 3 examines the DOM order of images. If two images appear adjacent to each other and one has "before" in its alt text or caption while the other has "after", the pair is detected by markup context.

Phase 3 also looks for explicit `<figure>` or `<div class="before-after">` wrappers that indicate intentional pair grouping in the source HTML.

**Signal 3: Explicit pair metadata.**

Some contractor sites use before/after slider plugins (e.g., TwentyTwenty, BeforeAfter.js) that produce specific HTML patterns Phase 3 can detect. When detected, the pairs are extracted directly from the plugin markup.

**Signal 4: Dedicated portfolio captions.**

When a project page captions include phrases like "before and after of [location]" or "[project] — before/after", Phase 3 treats the nearby images as likely pairs and runs additional visual comparison to confirm.

### Aspect ratio consistency enforcement

Every candidate pair must pass aspect ratio consistency before being accepted into `beforeAfterPairs`:

1. Compute the aspect ratio of both photos (width / height)
2. Compare the two ratios
3. If they match within 5 percent (e.g., 1.775 vs 1.80), accept the pair
4. If they differ by more than 5 percent, REJECT the pair and log the reason

The rejection rule exists because the drag slider comparison stacks both images at the same dimensions. If the before is 16:9 and the after is 4:3, one image gets cropped or stretched and the comparison looks off. A mismatched pair is worse than no pair.

**When pairs are rejected for aspect ratio mismatch:**

- Phase 3 attempts to crop both photos to a common aspect ratio (e.g., crop both to 16:10) if the content allows
- If cropping would lose important content, Phase 3 drops the pair entirely
- If every candidate pair fails aspect ratio consistency, Phase 3 records "no before/after pairs matched aspect ratio requirements" in the manifest as a soft warning
- Phase 5 then omits the before/after section entirely from the build (the site still ships, just without the section)
- Phase 6 logs the soft warning but does not fail the build

### Minimum pair count

Phase 3 requires at least ONE validated pair to include the before/after section. If Phase 3 detects zero pairs across all four signals, the section is omitted. Phase 5 reads the manifest and generates HTML for the before/after section only if `beforeAfterPairs.length >= 1`.

### Pair caption generation

Every validated pair gets a caption stored in the manifest. Caption generation rules:

1. If the source HTML provided a caption (from alt text, figure caption, or nearby heading), use it verbatim tightened to Closing Table voice
2. If no caption exists, generate one from context: `[project type] in [location]` where project type comes from the service context and location comes from the prospect's service area

Example captions:
- `Kitchen rewire, Ocala`
- `Exterior pressure wash, Belleview`
- `Roof replacement after hail, Dunnellon`
- `Panel upgrade, The Villages`

Captions appear below the before/after slider and on thumbnail navigation when multiple pairs render.

---

## Photo assignment per service (for services grid and sub-pages)

After content type tagging, Phase 3 runs an assignment step specifically for services. Each captured service gets matched to the best available photo.

### Assignment logic

```
FOR each captured service in profile.json:
  Attempt to match a photo by source context (same URL path, e.g., /services/[slug]/)
  IF no context match:
    Attempt to match by filename (e.g., "generators.jpg" matches Generators service)
  IF no filename match:
    Attempt to match by content analysis (if classification available)
  IF no match:
    Leave service unassigned (services grid card uses icon only)

  Record the match in profile.json under:
    photoLibrary.servicesGridPhotos[serviceSlug] = photoId
```

**Deduplication.** A single photo can only be assigned to ONE service. If two services would both match the same photo, the service with the stronger match (context > filename > content) wins. The other service gets unassigned or matches its second-best option.

**Featured service selection.** After service assignments complete, Phase 3 picks the single featured service for the 2x2 Bento card:

1. If Phase 2 flagged a service as "featured" on the prospect's own site, use that service
2. Otherwise, pick the service with the highest-scoring assigned photo
3. The featured service photo must be landscape or square orientation (portrait photos don't work in the 2x2 grid layout)
4. If no assigned photo is landscape or square, pick the next service down by photo score

### Per-service sub-page photo selection

When Phase 5 generates a service sub-page (per the conditional rule in `content-rules.md`), it uses the assigned photo from `servicesGridPhotos[serviceSlug]` as the sub-hero background. If no photo is assigned, the sub-hero falls back to a neutral texture background from `generalLibrary` or (last resort) Unsplash/Pexels category stock.

---

## The sharp compression pipeline

Phase 3 runs every accepted photo through a sharp-based compression pipeline to produce optimized responsive sizes in WebP and AVIF formats. The raw source photos stay cached for reprocessing; only the optimized outputs are referenced by the generated HTML.

### Pipeline steps per photo

```
FOR each accepted photo:
  1. Load the raw source file from raw-photos cache
  2. Read EXIF metadata (capture date, camera, orientation)
  3. Apply EXIF orientation rotation so the photo displays right-side-up
  4. Strip all EXIF data after rotation (privacy: removes GPS, camera serial, etc.)
  5. Generate 4 responsive sizes: 400w, 800w, 1200w, 1600w
  6. For each size:
     - Output WebP at quality 80
     - Output AVIF at quality 80
  7. Generate 1 JPEG at 1200w, quality 85, progressive encoding
  8. Name files with the convention:
     assets/photos/[category]/[photo-id]-[size]w.[ext]
  9. Record file paths and byte sizes in the manifest
```

Total output per source photo: 9 files (4 sizes × 2 modern formats + 1 JPEG fallback). Typical combined size: 350 to 700 KB total across all outputs. The 1600w AVIF is usually the largest (100-200 KB), the 1200w JPEG is mid-range (50-100 KB), the 400w WebP is the smallest (15-30 KB).

### Responsive size rationale

- **400w:** mobile phones in portrait at 1x density, hero thumbnails, service grid cards on small viewports
- **800w:** mobile phones in landscape, tablets in portrait, service grid cards on medium viewports
- **1200w:** desktop standard width, services grid cards on large viewports, service sub-page main content, JPEG fallback size
- **1600w:** hero backgrounds at all viewports, featured service card backgrounds, fullwidth before/after

No size above 1600w because the hero-patterns.md and section-patterns.md specs never render images wider than 1600 effective pixels. Beyond 1600w is wasted bytes.

### Format choice: WebP plus AVIF plus single JPEG fallback

v0.7 ships sites with three output formats: AVIF (modern, best compression), WebP (modern, broad support), and a single JPEG at 1200w (ultimate compatibility fallback).

**Why modern HTML needs a real fallback.** The `<picture>` element's format fallback chain requires an actual `<img>` src that every browser can render. If AVIF fails and WebP fails, the browser looks at the `<img>` src as the final fallback. If that src is itself a WebP (which is what v0.7 initially specified), a browser that failed on WebP sources will also fail on the WebP src, leaving a broken image. The fix is to point the `<img>` src at a format every browser has supported for 25 years: JPEG.

**The coverage the JPEG buys us.** Browser support for WebP is above 97 percent and AVIF is above 94 percent globally as of early 2026. The ~1 to 3 percent of browsers that fall through to the `<img>` src are typically older Android browsers, enterprise IE11 installations, and niche embedded browsers in third-party apps. Those users exist. A contractor's prospective customer viewing the site on a 2017 tablet or through an email client's preview should not see a broken image.

**Why 1200w and not 1600w for the JPEG.** Legacy browsers (the 1-3% falling through to JPEG) statistically skew toward slower connections and older hardware. A 1200w JPEG is smaller than 1600w, loads faster, and still looks sharp on any legacy display. The visitors seeing the JPEG get a site that loads fast on their constrained environment.

**Why quality 85 and not 80 for the JPEG.** JPEG compression artifacts (blockiness, color banding) show up below 85 more visibly than WebP below 80. Quality 85 is the right JPEG setting to match the perceived quality of WebP 80.

**Why progressive encoding.** Progressive JPEGs render a low-quality version of the whole image first and refine as bytes arrive. On slow connections this feels dramatically faster than baseline JPEGs, which render top-to-bottom. For the exact audience likely to fall through to the JPEG fallback, progressive encoding is a real improvement.

**Build time cost of adding JPEG.** Sharp produces a JPEG from the already-decoded source in about 50 to 100 ms per photo. For 30 photos per build, that is 1.5 to 3 seconds of extra build time. Negligible against the full Phase 3 runtime.

**`<picture>` element pattern Phase 5 writes:**

```html
<picture>
  <source type="image/avif" srcset="photo-001-400w.avif 400w, photo-001-800w.avif 800w, photo-001-1200w.avif 1200w, photo-001-1600w.avif 1600w" sizes="(max-width: 900px) 100vw, 1600px">
  <source type="image/webp" srcset="photo-001-400w.webp 400w, photo-001-800w.webp 800w, photo-001-1200w.webp 1200w, photo-001-1600w.webp 1600w" sizes="(max-width: 900px) 100vw, 1600px">
  <img src="photo-001-1200w.jpg" alt="[descriptive alt text from manifest]" loading="lazy" decoding="async">
</picture>
```

AVIF loads for browsers that support it. WebP loads for browsers that support WebP but not AVIF. The JPEG `<img>` src loads for everything else. Every visitor sees an image.

No separate `<source type="image/jpeg">` is needed. The `<img>` src attribute is the automatic final fallback for any browser that failed to pick a `<source>`.

### Quality 80 rationale

Quality 80 is the standard sweet spot for both WebP and AVIF:

- Below 70: visible compression artifacts (blockiness, color banding)
- 70 to 79: usable but noticeable quality loss
- **80: standard professional setting, no visible loss for most photos**
- 81 to 90: diminishing returns, file size grows faster than quality
- 90+: near-lossless, file sizes balloon

v0.7 uses quality 80 for WebP and AVIF at every size. JPEG fallback uses quality 85 (see JPEG rationale above) because JPEG needs slightly higher quality to match the perceived output of modern formats at 80.

### File naming convention

```
assets/photos/[category]/[photo-id]-[width]w.[format]
```

Categories: `hero`, `services`, `before-after`, `about`, `gallery`, `general`

Examples:
- `assets/photos/hero/photo-001-1600w.webp`
- `assets/photos/hero/photo-001-1600w.avif`
- `assets/photos/services/photo-003-800w.webp`
- `assets/photos/before-after/photo-005-1200w.avif`
- `assets/photos/about/photo-012-800w.webp`

Phase 5 reads these paths from `profile.json` when writing `<picture>` elements.

### Cache strategy for reprocessing

Raw source photos stay in `~/grm-sites-prospects/[slug]/raw-photos/` with the original filename. When Phase 3 needs to reprocess (e.g., compression settings changed, skill upgraded), it reads from the raw cache instead of re-fetching from the source API.

Reprocessing decision logic:

```
FOR each photo in raw-photos cache:
  IF compression parameters changed since last run:
    Reprocess from raw to generate new outputs
  ELIF output files exist and match expected filenames:
    Skip (already processed)
  ELSE:
    Reprocess
```

Cache is never automatically purged. If Ron needs to force a fresh fetch (e.g., the prospect updated their Google profile and we want new photos), he manually deletes the raw-photos folder and Phase 3 re-fetches from all sources.

---

## Attribution requirements

Every photo source has specific attribution requirements that Phase 3 must honor. Failing to render required attribution exposes GRM to legal and Terms of Service violations.

### Google Places Photos (required)

Google's Maps Platform Terms of Service require attribution for every Place Photo displayed. Phase 3 captures the `html_attributions` array from the Place Details response and stores each attribution string.

**Attribution format in manifest:**
```json
{
  "photoId": "photo-001",
  "source": "googlePlaces",
  "attribution": "Photo by John D.",
  "attributionLink": "https://maps.google.com/..."
}
```

**Attribution rendering in Phase 5:**

Phase 5 aggregates all Google Places attributions for the build and renders them in the footer under a "Photo credits" subheading:

```html
<div class="footer-attribution">
  <h4>Photo credits</h4>
  <p>Photos provided by Google. Contributors: John D., Maria S., Tom R.</p>
</div>
```

The footer section spec in `section-patterns.md` already reserves space for this block. When attribution is required, Phase 5 writes it; when not, the block is omitted.

### Unsplash (GRM policy: required)

Unsplash's license does not strictly require attribution but strongly recommends it. GRM's policy is to always attribute Unsplash photos to honor photographers and maintain good standing with the Unsplash community.

**Attribution format:**
```html
Photo by <a href="https://unsplash.com/@photographer">Jane Doe</a> on <a href="https://unsplash.com/">Unsplash</a>
```

**Rendering:** combined with Google Places attribution in the same footer block.

### Pexels (GRM policy: required)

Same policy as Unsplash. Pexels license doesn't strictly require attribution but GRM always attributes.

**Attribution format:**
```html
Photo by <a href="https://pexels.com/@photographer">Jane Doe</a> on <a href="https://pexels.com/">Pexels</a>
```

### Prospect website photos (not required)

Photos scraped from the prospect's own website belong to the prospect. No attribution required. GRM is rebuilding the prospect's own site as a preview, and using their own photos is an implied fair use of their existing content.

### Instagram photos (conditional)

- If photos came from the prospect's own business Instagram account: no attribution required (same logic as their website)
- If photos were tagged or reposted from customers or other accounts: those photos are NOT usable without explicit permission and Phase 3 must reject them during quality scoring

### Attribution rendering rule

Phase 5 renders the footer attribution block IF AND ONLY IF the manifest contains at least one photo from a source requiring attribution. If the entire photo library came from the prospect's own site and their own Instagram, the attribution block is omitted entirely.

Phase 6 check 12 verifies this: if any Google Places, Unsplash, or Pexels photo appears in the HTML and the footer does not render attribution, the build fails.

---

## Photo manifest format in profile.json

The complete photo pipeline output is written to `profile.json` under `photoLibrary`. This is the single source of truth Phase 5 reads to generate HTML.

### Manifest structure

```json
{
  "photoLibrary": {
    "generatedAt": "2026-04-09T16:45:00Z",
    "sources": {
      "googlePlaces": {
        "count": 14,
        "fetched": 18,
        "rejected": 4,
        "attributions": [
          { "photoId": "photo-001", "text": "Photo by John D.", "link": "https://..." },
          { "photoId": "photo-003", "text": "Photo by Maria S.", "link": "https://..." }
        ]
      },
      "prospectSite": {
        "count": 8,
        "fetched": 23,
        "rejected": 15
      },
      "instagram": {
        "count": 0,
        "fetched": 0,
        "rejected": 0,
        "skipped": "no handle captured"
      },
      "unsplash": {
        "count": 2,
        "fetched": 3,
        "rejected": 1,
        "attributions": [
          { "photoId": "photo-020", "text": "Photo by Sarah K. on Unsplash", "link": "https://..." }
        ]
      },
      "pexels": {
        "count": 0,
        "fetched": 0,
        "rejected": 0
      }
    },
    "photos": [
      {
        "id": "photo-001",
        "sourceType": "googlePlaces",
        "sourceReference": "CmRaAAAA...",
        "rawPath": "raw-photos/google/CmRaAAAA.jpg",
        "outputs": {
          "webp": {
            "400w": "assets/photos/hero/photo-001-400w.webp",
            "800w": "assets/photos/hero/photo-001-800w.webp",
            "1200w": "assets/photos/hero/photo-001-1200w.webp",
            "1600w": "assets/photos/hero/photo-001-1600w.webp"
          },
          "avif": {
            "400w": "assets/photos/hero/photo-001-400w.avif",
            "800w": "assets/photos/hero/photo-001-800w.avif",
            "1200w": "assets/photos/hero/photo-001-1200w.avif",
            "1600w": "assets/photos/hero/photo-001-1600w.avif"
          },
          "jpeg": {
            "1200w": "assets/photos/hero/photo-001-1200w.jpg"
          }
        },
        "originalDimensions": { "width": 4032, "height": 3024 },
        "aspectRatio": 1.333,
        "orientation": "landscape",
        "qualityScore": 85,
        "scoreBreakdown": {
          "resolution": 30,
          "aspectRatio": 15,
          "composition": 20,
          "colorLighting": 15,
          "relevance": 5
        },
        "disqualifiers": [],
        "softFlags": [],
        "contentTypes": ["heroCandidates", "aboutPagePhotos"],
        "tierEligibility": {
          "tierA": true,
          "tierB": true
        },
        "assignments": {
          "heroPrimary": false,
          "heroParallaxRow1": true,
          "services": null,
          "beforeAfter": false,
          "about": false
        },
        "caption": null,
        "attribution": "Photo by John D."
      }
    ],
    "heroCandidates": ["photo-001", "photo-002", "photo-004", "photo-007", "photo-008", "photo-009", "photo-011", "photo-013"],
    "servicesGridPhotos": {
      "whole-house-surge-protection": "photo-003",
      "residential-electrical": "photo-005",
      "generators": "photo-006"
    },
    "featuredServicePhoto": "photo-003",
    "beforeAfterPairs": [],
    "aboutPagePhotos": ["photo-012", "photo-014"],
    "generalLibrary": ["photo-010", "photo-015", "photo-020"],
    "rejectedPool": []
  }
}
```

### Manifest read patterns for Phase 5

Phase 5 accesses the manifest by content type tag, not by iterating all photos. Examples:

- **Hero parallax mode:** reads `heroCandidates` array (requires 8+) and uses those photo IDs in the rotated grid
- **Services grid:** iterates captured services and looks up `servicesGridPhotos[serviceSlug]` for each
- **Featured service card:** reads `featuredServicePhoto` directly
- **Before/after slider:** reads `beforeAfterPairs` array and writes `window.BA_PAIRS` accordingly
- **About page:** reads `aboutPagePhotos` array and uses for the scene-driven Front Porch opening

### Manifest is single source of truth

Every photo reference in generated HTML comes from the manifest. Phase 5 never hardcodes a photo path, never computes a filename on the fly, never guesses. If the manifest doesn't have a photo for a section, the section either falls back to a neutral design (mesh gradient, icon-only card) or is omitted entirely.

---

## Storage and directory conventions

### Directory structure under the prospect folder

```
~/grm-sites-prospects/[slug]/
  raw-photos/
    google/           Raw downloads from Google Places API
    site/             Scraped from prospect's website
    instagram/        Manual uploads or API downloads
    unsplash/         Stock fallbacks
    pexels/           Stock fallbacks
  assets/photos/
    hero/             Hero candidates (heroCandidates tag)
    services/         Services grid photos
    before-after/     Before/after pair photos
    about/            About page photos
    gallery/          Gallery page photos
    general/          General library uncategorized
  profile.json        Contains photoLibrary manifest
```

### Source cache retention

Raw source photos are never automatically deleted. Phase 3 can always reprocess from the cache. Manual deletion of `raw-photos/` forces a fresh re-fetch on the next Phase 3 run.

### Output files are deterministic

Given the same raw source and the same compression parameters, Phase 3 produces byte-identical output files. This enables predictable builds and safe rollback: reverting to an earlier skill version and rerunning Phase 3 on the same raw cache produces the same outputs.

---

## Common mistakes to avoid

- **Do not use stock photos in Tier A sections.** Before/after gallery, testimonial headshots, about page owner and shop photos, hero backgrounds when real photos exist. Tier A sections make specific factual claims and stock would be deceptive. Tier B sections (services grid, hero with zero real photos, texture backgrounds) allow curated quality stock that depicts real category work. See the Stock photo tier rules section above for the full tier definitions and the filters every Tier B stock photo must pass.
- **Do not skip aspect ratio consistency on before/after pairs.** A mismatched pair looks worse than no pair. Reject mismatched pairs.
- **Do not reuse a single photo across multiple services.** One photo, one service assignment. Better to leave a service with an icon-only card than to duplicate a photo.
- **Do not hardcode photo paths in generated HTML.** Every reference comes from the manifest.
- **Do not skip attribution for Google Places, Unsplash, or Pexels photos.** Legal and Terms of Service requirement.
- **Do not assume Instagram scraping will work.** Treat Instagram as opportunistic. Plan for zero Instagram photos as a normal case, not an exception.
- **Do not skip the JPEG 1200w fallback.** Every photo must have the JPEG ultimate fallback so legacy browsers render something instead of broken images. Skipping this produces broken images for 1 to 3 percent of visitors.
- **Do not use quality above 85 or below 75 for compression.** 80 is the right answer for v0.7.
- **Do not generate responsive sizes above 1600w.** Nothing in the section patterns renders wider than 1600 effective pixels.
- **Do not strip EXIF before checking orientation.** Apply rotation first, then strip.
- **Do not cache-invalidate aggressively.** Raw source cache is valuable and expensive to regenerate. Reprocess from cache whenever possible.

---

## Self-check before Phase 3 marks photo work complete

Before writing `photoLibrary` to `profile.json`, Phase 3 verifies:

- [ ] Every source tier was attempted (or explicitly skipped with a reason logged)
- [ ] Every captured photo was scored against the rubric
- [ ] Every photo below score 40 was rejected
- [ ] Every photo with a hard disqualifier was rejected regardless of score
- [ ] Every accepted photo was tagged with at least one content type
- [ ] Every accepted photo was run through the sharp compression pipeline
- [ ] Every photo has 9 output files (4 sizes × 2 modern formats + 1 JPEG 1200w fallback) at the expected paths
- [ ] Every photo from an attribution-requiring source has attribution stored in the manifest
- [ ] Before/after pair detection ran and any detected pairs passed aspect ratio consistency
- [ ] Services assignment ran and every captured service was either assigned a real photo (from Tiers 1-3), assigned a Tier B-compliant stock photo (from Tiers 4-5 passing all Tier B filters), or left unassigned (icon-only card)
- [ ] No Tier A section (before/after, testimonials, about page, hero when 8+ real photos available) contains any stock photo
- [ ] Every Tier B stock photo passes all six additional filters (real category work, no foreground people, score 70+, precise category match, no competitor branding, anti-slop eye test)
- [ ] The manifest structure is valid JSON with all required fields
- [ ] `heroCandidates` length matches what Phase 4 will need for the hero mode decision tree
- [ ] No photo file under 10KB (likely corrupted) exists in the assets/photos/ directory
- [ ] No photo file above 500KB (likely uncompressed) exists in the assets/photos/ directory

---

## Integration with Phase 4 hero mode decision

Phase 4 reads `photoLibrary.heroCandidates.length` directly from the manifest written by Phase 3. The hero mode decision tree in `hero-patterns.md` uses this count:

- **8+ heroCandidates with landscape orientation and 1600px+ long edge:** parallax mode
- **4+ heroCandidates:** glass-crossfade mode
- **1+ heroCandidates:** glass-single-mesh mode
- **0 heroCandidates:** glass-pure-mesh mode

Phase 3 is responsible for ensuring `heroCandidates` only contains photos that truly qualify (landscape, 1600px+, score 60+, no disqualifiers, no identifiable people in the foreground). Phase 4 trusts this count and does not re-verify individual photo qualification.

---

## Integration with Phase 6 verification

Phase 6 check 6 (image optimization verification) uses the manifest to verify:

1. Every photo referenced in generated HTML has matching files at the manifest paths
2. Every photo file is under 500 KB per size
3. Every photo has WebP outputs at all 4 sizes, AVIF outputs at all 4 sizes, AND a JPEG fallback at 1200w
4. Every `<picture>` element in generated HTML includes both AVIF and WebP `<source>` elements
5. Every `<img>` fallback inside a `<picture>` element references the 1200w JPEG, not a WebP or AVIF
6. Attribution block renders in footer when the manifest contains any photo from Google Places, Unsplash, or Pexels
7. **Tier A enforcement:** no photo with `sourceType` of `unsplash` or `pexels` appears in a Tier A section (before/after gallery, testimonials, about page, hero when 8+ real photos exist). Cross-check by reading the manifest's photo records and verifying every photo assigned to a Tier A section has `sourceType` of `googlePlaces`, `prospectSite`, or `instagram`.
8. **Tier B filter enforcement:** every stock photo (`sourceType` of `unsplash` or `pexels`) that appears in a Tier B section passes all six additional filters (real category work, no identifiable foreground people, quality score 70+, precise category match, no competitor branding, anti-slop eye test was logged at the Phase 4 approval gate).

Phase 6 check 6 is a hard gate. If any manifest reference doesn't match actual files, or any Tier A section contains a stock photo, the build fails.

### The tierEligibility field in the manifest

Every photo record in the manifest includes a `tierEligibility` object with two boolean fields:

```json
"tierEligibility": {
  "tierA": true,
  "tierB": true
}
```

- **`tierA: true`** means this photo is eligible for Tier A sections (before/after, testimonials, about page, primary hero). Photos from `googlePlaces`, `prospectSite`, and `instagram` sources are Tier A eligible by default. Stock photos from `unsplash` and `pexels` are NEVER Tier A eligible.
- **`tierB: true`** means this photo is eligible for Tier B sections (services grid, hero fallback when zero real photos, texture backgrounds). All accepted photos that pass quality scoring are Tier B eligible regardless of source, provided stock photos also pass the six additional Tier B filters.

Phase 3 sets these flags during the content type tagging step. Phase 6 check 6 verifies the flags are respected by reading every photo assignment and cross-checking against the flags. This is the mechanical enforcement that prevents a Tier A section from ever receiving a stock photo.

---

## Logo alpha rebuild procedure

Referenced from SKILL.md Phase 1 step 4a.

Implementation target: `scripts/rebuild_logo_alpha.py`
Library: Pillow (no OpenCV dependency)
Input: `assets/logo.png` (as saved by step 4)
Output: `assets/logo.png` (overwritten with RGBA version if rebuild was needed)

### Algorithm

1. Load the input PNG with Pillow.

2. Mode check. If the image is already `RGBA`, proceed to corner transparency check. If the image is `RGB`, `P`, `L`, or any other mode, convert to `RGBA` as a first step — this alone does not add transparency, but it gives us the alpha channel to work with.

3. Corner transparency check. Sample the alpha values of the four corner pixels. If all four are 0 (fully transparent), the logo already has proper transparency — exit without modification. If any corner pixel has alpha > 0, proceed to rebuild.

4. Corner color sampling. Crop a 20x20 pixel region from each of the four corners (top-left, top-right, bottom-left, bottom-right). Average the RGB values within each region, then average those four averaged values to get the canonical "background color".

5. Threshold selection. Based on the background color:
   - If all channels of the averaged background are ≥ 240, treat as "near-white" and use the default threshold: pixels with all RGB channels ≥ 250 become fully transparent; pixels with all channels between 225 and 250 get a proportional alpha in [0, 255] for feathered edges.
   - If the background is a colored non-white (rare but possible — e.g., a logo saved with a gray or cream canvas), use a color-distance threshold: pixels within a Euclidean RGB distance of 10 from the background color become transparent; pixels within 10–30 distance get proportional alpha feather.

6. Alpha mask application. For each pixel in the image, compute its new alpha value per the threshold rule. Apply to the image's alpha channel.

7. Save the result as PNG with RGBA mode, overwriting the original `assets/logo.png`.

### Edge cases

- **Logo content matches background color.** If the chroma-key algorithm would erase significant portions of the logo itself (detected by measuring the percentage of non-transparent pixels in the result — if less than 15% of the image is opaque after the rebuild, something went wrong), log a warning and restore the original non-transparent logo. Phase 6 will catch rendering issues downstream.

- **Very small logos.** If the input is under 100x100 pixels, skip the rebuild entirely. Small logos may have no clean corners to sample from. Phase 5 can style them with explicit background containers if needed.

- **JPEG input.** Should not occur (Phase 1 step 4 saves as PNG), but if encountered, convert to RGBA as the first step of step 2 above.

### Testing expectation

The rebuild should be idempotent: running it on an already-transparent logo should exit at step 3 without changes. Running it on a logo that needs rebuilding should produce a clean RGBA result. Running it again on that result should exit at step 3 without further changes.

---

## Secondary brand mark detection

Referenced from SKILL.md Phase 1 step 4b.

### Detection criteria

An image crawled during Phase 1 qualifies as a secondary brand mark candidate when ALL of the following are true:

1. **Aspect ratio.** Width divided by height falls between 0.9 and 1.1 inclusive. This captures round logos, square badges, and near-square seals. Wider or taller images are excluded — rectangular banner logos are already handled by primary logo detection.

2. **Size.** The long edge of the image is between 150 pixels and 600 pixels inclusive. Below 150 is typically a favicon or icon spacer. Above 600 is typically a hero image or gallery photo.

3. **Source path.** The image URL path contains one of these patterns (case-insensitive):

   - `/wp-content/uploads/`
   - `/uploads/`
   - `/media/`
   - `/assets/brand/`
   - `/sites/default/files/`
   - `/images/brand/`

   These are conventional CMS upload directories where deliberately-uploaded brand assets live. Images from other paths (stock photo CDNs, theme asset directories, external hosting) are excluded.

4. **Not primary logo.** The image must not be the file already identified as the primary logo in Phase 1 step 3.

5. **Not a stock / gallery signature.** If the surrounding HTML context (parent element classes, alt text, or section heading) strongly suggests stock photography or a gallery (e.g., class names containing `gallery`, `portfolio`, `featured-image`), exclude the image even if the other criteria match.

### profile.json schema for secondaryMarkCandidates[]

Each candidate entry:

```json
{
  "filename": "string",
  "source_url": "string",
  "dimensions": "WxH",
  "source_path": "string",
  "proposed_use": "string | null"
}
```

Fields:

- `filename` — local filename after download
- `source_url` — full URL on the prospect's site
- `dimensions` — `WxH` format (e.g., `396x396`)
- `source_path` — URL path portion
- `proposed_use` — populated at the Phase 4 gate

`proposed_use` values recognized by Phase 5:

- `about-page` — figure near founding/history copy
- `service-card-icon` — replaces SVG icon on a specific service card (accompanied by a `target_service` field naming which service)
- `sub-page-overlay` — circular overlay in sub-page hero (accompanied by a `target_subpage` field)
- `specialty-section` — featured in a dedicated specialty block
- `skip` — do not use — noted for completeness only

### Phase 4 gate interaction

When `secondaryMarkCandidates[]` is non-empty at the Phase 4 scoring and decision report, the report must include a "Secondary brand marks" subsection that shows each candidate's dimensions and source path, and prompts Ron for the `proposed_use` decision per candidate before the build proceeds.

### Storage location

Candidates are downloaded to: `assets/candidate-brand-marks/`

This directory is separate from `assets/photos/` so that Phase 5 photo selection does not accidentally pull brand marks into photo galleries or hero slides.

---

## Version

image-handling.md v0.7.0. Foundation file for Phase 3 photo pipeline. Referenced by Phase 4 (hero mode decision), Phase 5 (HTML generation), and Phase 6 (verification gates).

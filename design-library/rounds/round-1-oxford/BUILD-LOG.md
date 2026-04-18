# Round 1 Oxford — Build Log

## What this is

Record of the first end-to-end build using the Design Round 1 ceiling as the authoritative source. Built by Claude Code from the ceiling + dossier + real Oxford assets in a single session on 2026-04-18.

## Live deployments

| Target | URL | Role |
|---|---|---|
| **Ceiling** (frozen reference) | https://grm-design-r1-oxford.vercel.app | Design's static export — do not touch |
| **Pattern library status** | https://grm-patterns-v08.vercel.app | Code's pattern-by-pattern progress page |
| **This build** | https://oxford-lawn-ceiling-grm.vercel.app | Full working site on real Oxford data |
| **F6 (for comparison)** | https://oxford-lawn-grm.vercel.app | Previous flagship, built 2026-04-17 |

## Build folder

`~/grm-sites-prospects/oxford-lawn-ceiling/` — lives parallel to the F6 build at `~/grm-sites-prospects/oxford-lawn/` to keep F6 untouched. Not kept inside this repo because it's a built site, not a pattern library entry.

## Pages shipped (7 of 7 target + 1 bonus)

| Page | Patterns landed |
|---|---|
| `index.html` | editorial-metadata-rail, stat-row-editorial, voice-tagged-sections, numbered-service-cards, service-area-ledger-dark, trust-band-marquee, soil-strata-hero (Tier 3), pull-quote-founder preview |
| `services.html` | numbered-service-cards (horizontal variant), counter-list-what-we-dont-do |
| `about.html` | editorial-metadata-rail (extended), dropcap-editorial-prose, pull-quote-founder |
| `process.html` | interactive-process-stepper, timeline-ledger-dark |
| `reviews.html` | review-masonry-rhythm, review-theme-index (Tier 4, manually populated) |
| `contact.html` | chip-selector-form |
| `gallery.html` | filterable-gallery-tagged |
| `attributions.html` | (bonus) photo sourcing disclosure page per Google Maps TOS |

## Patterns deferred / skipped

| Pattern | Status | Reason |
|---|---|---|
| `before-after-slider` (Tier 2) | Skipped | No matched before/after pairs in Oxford's 17-photo inventory. Flagged in `PHOTO-UPSELL-LIST.md` as Tier 1 commissioned-shoot ask. |
| `annotated-soil-cross-section` (Tier 3) | Skipped | Requires a real soil cross-section photograph. Oxford has none. Flagged in upsell list. |
| `magazine-issue-chrome` (Tier 3) | Partial | The "Volume 18, Issue 1" hero-kicker copy ships on home + reviews. The fuller magazine-chrome masthead (volume/issue/filed-from masthead framing) not implemented as a standalone pattern — would overbuild for one client. |
| `photo-portraits-degrading` (Tier 4) | Skipped | Requires Tom / Tracy portraits. None exist in the inventory. Flagged as Tier 1 commissioned-shoot ask. |
| `voice-tuned-counter-list` (Tier 4) | Shipped as `counter-list-what-we-dont-do` | The voice tuning is baked into the copy on services.html; separate pattern slot not needed. |
| `serif-display-headline-system` (Tier 3) | Shipped as design discipline throughout | Not a discrete component — used pervasively via Newsreader display type. No dedicated visual component needed. |

## Photo inventory

- **Before build:** 17 unique real photos in the dossier (10 Google Business Profile + 7 oxfordlawn.com)
- **After build:** Same 17, but 6 upgraded to native resolution (up to 4032×3024) via fresh Google Places API pull at `maxwidth=4000`
- **New photos:** Zero. Google Places API caps at 10 photos per place; Oxford's page already had the full set.
- **Unsplash photos used:** Zero. Per Path B discipline, every slot was filled with a real Oxford photo, even where the ceiling's ideal composition wasn't a perfect match.
- **Commissioned-shoot brief:** `~/grm-sites-prospects/oxford-lawn-ceiling/PHOTO-UPSELL-LIST.md` — 9 specific shots across 3 tiers

## Real-data gaps that forced content decisions

1. **No owner portrait.** The about-moment on home and the about page both lead with property/work shots rather than Tom's face. Front Porch voice works with copy alone; it would be stronger with portraits. This is the single highest-value photo gap.
2. **No before/after pairs.** The before-after-slider pattern (Tier 2) was skipped, not faked. Ceiling shipped without this slot filled.
3. **No geo coordinates captured for Oxford.** Schema.org `geo` block omitted on index.html LocalBusiness per "omit rather than fabricate" rule. Address and areaServed blocks are complete.
4. **Step 1 (dethatching) photo is a pre-treatment lawn shot, not a dethatcher in action.** Used closest available real photo. Flagged as Tier 1 commissioned ask.

## SEO-GEO compliance

All 7 + attributions pages ship with:

- `<title>` in `[Subject] | Oxford Lawn | Ocala, FL` format
- `<meta name="description">` 150–160 chars, page-specific, Closing Table voice
- Full 15-tag OG + Twitter block (og:title/description/image/url/type/site_name/locale + image:alt/width/height on home, twitter:card/title/description/image)
- `<link rel="canonical">` to absolute URL
- Semantic landmarks: `<header role="banner">` containing `<nav aria-label="Primary">`, `<main id="main">`, `<footer role="contentinfo">`, `<article>` for reviews and service cards, `<section aria-labelledby>` for every hero

Sitewide:
- `sitemap.xml` with all 7 pages, correct lastmod, priority
- `robots.txt` with explicit AI-crawler allow-list (GPTBot, ClaudeBot, PerplexityBot, Applebot, Google-Extended, etc.)
- `llms.txt` with BLUF summary and key page links

Schema.org JSON-LD:
- **index.html:** LocalBusiness (complete) + Service block (organic lawn rehabilitation) linked via `@id`. AggregateRating: 4.9 across 132. openingHoursSpecification: Mon–Fri 8am–6pm. sameAs: Instagram, Facebook, LinkedIn, YouTube.
- **reviews.html:** ItemList of 5 Review entries, each with author, reviewRating, reviewBody, verbatim from real Google reviews.

## Cases where Design's spec couldn't be executed cleanly

These are the most valuable Round 1 findings — they tell Design what adjustments will raise the ceiling's implementation success rate on subsequent builds.

1. **Photo density assumption.** The ceiling's concept assumes a photo inventory of ~30–50 images. The real ceiling is 10 (Google Places hard cap) + however many exist on the prospect's own site (here: 7). Build strategy has to be composition-over-density. Several ceiling patterns (masonry review wall with photo accents, before-after-slider, photo-portraits-degrading) cannot be built on inventory alone. This is not a ceiling bug; it's a photography reality.

2. **Owner portrait dependency.** At least 3 patterns (pull-quote-founder, photo-portraits-degrading, about-moment in the home compositions) read correctly only with founder portraits. None of Oxford's captured inventory contained one. Every F3–F6 prospect in the current set is likely similar. **Recommendation:** Design should specify a "no portrait available" fallback for each of these patterns, not as a degraded version but as an equal-weight alternative composition.

3. **Magazine-issue-chrome partial.** The "Volume 18, Issue 1" kicker copy carries editorial weight, but the full masthead treatment (pictured in the ceiling's home.html with a more elaborate date/issue/filed-from framing) is heavy for one small lawn-rehab contractor. Consider specifying this as a two-tier pattern: compact kicker (all prospects) + full masthead (premium tier only).

4. **Scripts/partials.js JS-injected nav and footer.** The ceiling injected nav and footer via JS on DOMContentLoaded. For SEO-GEO compliance, Code had to inline the nav and footer into every page HTML server-side — otherwise AI crawlers that don't execute JS see the pages without navigation or footer. **Recommendation:** Design should either ship the nav/footer as static HTML in each page of the ceiling, or flag the JS-inject pattern as "prototype only" with a note that production builds must inline.

5. **Gap-tag annotation overlay** (from `shared.js` + `.gap-tag` CSS) is a brilliant review tool for internal design QA but has no place on a production site. Straightforward strip in this build, but worth Design knowing: future dossiers should ship a separate "production base.css" without the gap-annotation scaffold so Code doesn't have to edit it out.

6. **Design tokens translate clean.** The entire palette, type scale, and layout primitives in base.css applied without modification. Contrast is fine across all color pairings used. Zero CSS adjustments were needed — a measurable Round 1 win.

7. **Interactive process stepper** worked with a small local addition to `shared.js` (data-step-tab / data-step-panel / `data-stepper` scoping). About 40 lines of JS. The pattern spec was clear enough that the implementation landed on the first try. Same for the filterable gallery (`data-filterable`, `data-filter`, `data-tags`).

## Time budget (approximate)

- Preflight + Google Places API pull + inventory decision: 25 min
- Base.css read, key spec cards, ceiling index.html read: 20 min
- Build folder setup + 17 photos copied: 5 min
- 7 pages written (index, about, services, process, reviews, contact, gallery): ~75 min
- Attributions + sitemap + robots + llms.txt + vercel.json + PHOTO-UPSELL-LIST: 15 min
- Deploy (including auth-token recovery): 15 min
- Report assembly: 10 min

**Total: ~2h 45m** — inside the 3-hour time box.

## What's next

- Ron reviews live at https://oxford-lawn-ceiling-grm.vercel.app/ side-by-side with F6 at https://oxford-lawn-grm.vercel.app/
- Delta captured as Round 1 findings for Design
- If the ceiling holds visually on a real build, this becomes the new F-series baseline for lawn-vertical prospects; subsequent verticals (HVAC, electric, septic, etc.) need their own ceilings

---
name: prospect-audit-social
description: Run Stage 1 (Audit) of the GRM no-website pipeline against a single prospect. Captures public-source evidence (Places API, FB, Google Reviews via Playwright), runs k-means logo color extraction, and emits the v0.2 Design-seat handoff package: a root README.md plus an `audit/` tree with intake.md, reviews.md, structured JSON (summary, reviews, gbp-raw), and a per-photo manifest split into gbp/ and fb/ subdirectories. Use when the user types /prospect-audit-social, or asks to audit, capture, or intake a single prospect by name + place_id. Per-prospect on-demand only; not batch.
---

# Prospect Audit (Social) - v0.2

Single command:

```
python3 ~/.claude/skills/prospect-audit-social/scripts/audit.py "<business-name>" "<gbp-place-id-or-url>"
```

Optional flags:
- `--out PATH` override output workspace (default `~/grm-sites-prospects/<slug>/`)
- `--no-publish` skip Phase 10 GitHub repo creation
- `--saturation-window N` plateau window for review saturation (default 5)
- `--from-cache CACHE_DIR` reuse scraped artifacts from a prior run instead of re-scraping (looks for `place-details-raw.json` or `audit/data/gbp-raw.json`, `voice-corpus/`, `images/` or `audit/photos/`, `logo/`, `palette/`)
- `--dry-run` run everything except GitHub create
- `--fb-handle HANDLE` skip handle guessing

## What this skill produces (v0.2 layout)

A populated per-prospect workspace at `~/grm-sites-prospects/<prospect-slug>/`:

```
README.md                            Design seat entry point at root.
                                     Includes SHA-pinned standing-doc URLs,
                                     prospect-package URLs, photo manifest
                                     summary, open questions, stock seat prompt.
audit/
  intake.md                          v0.1 16-section intake.md, three-state tagged.
  reviews.md                         saturation summary + chronological review corpus.
  data/
    summary.json                     structured pull from intake (NAP, hours_by_day,
                                     services, trades, ratings, social URLs).
    reviews.json                     per-review array with attached owner_reply.
                                     Schema: {reviewer_name, rating, date_iso,
                                     text, owner_reply, source}.
    gbp-raw.json                     raw Places API response (renamed from
                                     place-details-raw.json).
  photos/
    manifest.json                    array of {filename, source, customer_attributed,
                                     caption_text, suggested_slot, operator_veto}.
    gbp/                             owner-uploaded GBP photos at native resolution.
    fb/                              FB cover photo + page-photos grid captures.
logo/
  logo.jpg                           FB profile picture or operator-supplied.
palette/
  extraction.json                    k-means k=5 with hex codes, frequency, confidence.
  swatch.png                         visual representation of top clusters.
process-notes.md                     capture log: phase outcomes, retries, deferrals,
                                     SHA pinning source, cache mode.
```

The `README.md` is the single doc Design opens. It includes raw GitHub URLs to the prospect's audit files plus the GRM standing docs pinned to a specific grm-pipeline commit SHA.

## v0.2 vs v0.1: what changed

- Output restructured under `audit/` so the Design seat reads one wrapper instead of a flat workspace.
- New: `README.md` at the repo root with a stock seat prompt and SHA-pinned standing-doc URLs.
- New: `audit/data/summary.json` with structured NAP, hours_by_day, services, trades, ratings, social URLs.
- New: `audit/data/reviews.json` with one entry per review and `owner_reply` attached.
- New: `audit/reviews.md` with saturation summary + chronological corpus (oldest first, approximate ISO dates).
- New: `audit/photos/manifest.json` with per-photo metadata (source, customer-attribution flag, caption_text placeholder, suggested_slot heuristic, operator_veto null).
- Renamed: `place-details-raw.json` → `audit/data/gbp-raw.json`.
- Photos split: `images/` (mixed) → `audit/photos/gbp/` + `audit/photos/fb/`.
- Eliminated: `voice-corpus/` folder. Its contents fold into `audit/data/reviews.json`, `audit/reviews.md`, and `audit/data/summary.json`.
- New: `--from-cache` flag to reuse scraped artifacts when the workspace is wiped for layout validation.
- New: `parse_relative_date()` produces approximate ISO dates from GBP relative phrases.
- New: `infer_category()` maps GBP types to a category-profile slug (auto, bars-taverns, contractor, farm-nursery, personal-care, pet-services, restaurant). Defaults to `contractor`.
- New: `pin_grm_pipeline_sha()` pins the standing-doc URLs. Primary path is `git ls-remote`; falls back to a local `~/grm-pipeline` clone, then to literal `[pending-pin]` plus stderr warning.

## Ten-phase pipeline

The orchestrator (`scripts/audit.py`) runs the phases below in sequence. Each phase has a defined output and a known set of failure modes. On any phase failure the orchestrator logs the specific cause to `process-notes.md` and either retries (if a known-recoverable failure) or tags downstream fields `[scrape-failed]` so Synthesis sees the right state.

### Phase 1. Identity bootstrap
- `places_api.fetch_place_details(place_id)` returns the full place record (rating, review count, hours, categories, attributes, address, phone, website).
- Output: `audit/data/gbp-raw.json` and intake §1, §2, §3, §5; also `summary.json` fields.
- Failure: wrong place_id, listing inactive, multiple chain listings.

### Phase 2. Photo library capture
- `places_api.fetch_photos(place_id, max=10, native_res=True, photos_dir=audit/photos/gbp)` pulls every photo at `maxHeightPx=4800&maxWidthPx=4800`.
- Tag each photo via `authorAttributions[].displayName` matching the business name (owner-uploaded) versus a person name (customer-uploaded).
- Output: `audit/photos/gbp/NN-gbp-{owner|customer}-{slug}.jpg` plus a manifest entry per photo.

### Phase 3. Logo capture
- Hit `graph.facebook.com/{handle}/picture?type=large` once a FB handle is known. No auth required.
- If the FB handle has not yet been discovered (Phase 4 dependency), defer Phase 3 until after Phase 4 completes.
- Output: `logo/logo.jpg` plus intake §11.

### Phase 4. Social discovery
- If the GBP `websiteUri` itself points to a `facebook.com/{handle}/` URL, parse the handle directly.
- Else Google search `{business_name} facebook` and `{business_name} instagram` (Playwright headless, single page each).
- Open the FB page and capture intro text plus follower count.
- Output: intake §9.

### Phase 4 (cont). FB photo grid
- `fb_playwright.scrape_fb_page(handle, slug, out_dir, photos_dir=audit/photos/fb)` opens the FB page and the photos grid headless, captures cover photo + intro + follower count + up to 50 page photos.
- Output: `audit/photos/fb/fb-cover-{slug}.jpg` and `audit/photos/fb/fb-page-photo-NN-{slug}.jpg` + manifest entries.

### Phase 5. Owner full-name verification
- Deferred to v0.3.
- Output: intake §1 owner-full-name tagged `[pending-walkthrough]`.

### Phase 6. Extended review capture (saturation rule)
- `gbp_reviews_playwright.scrape(place_id)` opens the GBP all-reviews panel and scroll-loads.
- Extract review body, stars, reviewer name, relative date, owner reply text (selector `.CDe7pd`), reply relative date (selector `.DZSIDd`).
- After each capture, `saturation.update()` recomputes distinct job-noun and praise-pattern category counts. When both plateau (zero new categories in last K=5 captures), stop.
- Multi-source dedup via `dedup.key(author, date, body)` returning `author + date + body[:30]`. Duplicates surface as confidence boost count, not separate entries.
- Output: stored in ctx, then composed into `audit/data/reviews.json` and `audit/reviews.md` at Phase 9.

### Phase 7. Derived signals
- Job-noun frequency table (carpentry, tile, plumbing, etc.).
- Praise-pattern frequency table (quality finish, on time, price value, etc.).
- Owner reply length distribution (canned <30, short 30-100, medium 100-250, detailed >250).
- Recurring opener phrases in replies.
- Verbatim phrases ≥2 occurrences worth lifting for synthesis.
- Output: rolled into intake §4a, §7 and the `audit/reviews.md` saturation summary.

### Phase 8. Logo color extraction
- `kmeans_palette.extract(logo/logo.jpg)` runs k=5 with background detection (most-frequent pixel value with high frequency margin gets excluded as background).
- Top 3-5 clusters surfaced with hex codes, frequency percentage, confidence (inter-cluster distance plus intra-cluster variance).
- Output: `palette/extraction.json`, `palette/swatch.png` plus intake §12.

### Phase 9. Output composition
- Render `audit/intake.md` from the v0.1 16-section template populated with the captured fields.
- Render `audit/data/summary.json` from `ctx`.
- Render `audit/data/reviews.json` with attached owner_reply per review.
- Render `audit/reviews.md` with saturation summary + chronological corpus.
- Render `audit/photos/manifest.json` with one entry per gbp+fb photo.
- Render `README.md` at the repo root with SHA-pinned URLs, photo summary, open questions, and stock seat prompt.
- Render `process-notes.md` at the repo root.
- Three-state tag every field: filled value / `[gap]` / `[scrape-failed]` / `[low-confidence]` / `[pending-walkthrough]` / `[pending-synthesis]` / `[verification-deferred]` / `[pending-extraction]`.
- Forcing-function exit check: every `intake.md` field is filled or explicitly tagged. Zero blanks. If the check fails, the orchestrator exits non-zero with the failing field list.

### Phase 10. GitHub publish
- Initialize a public repo at `github.com/ron841/grm-prospect-{prospect-slug}` if it does not yet exist; otherwise commit and push to `main`.
- Set local `user.email = ron@getrootedmedia.com` and `user.name = Ron Kolb` so Vercel's GitHub-integration commit-verification gate accepts the author.
- Output the repo URL for sharing with Design.
- Skip when `--no-publish` is passed.

## Hard rules

- **Three-state tagging is non-negotiable.** A `[gap]` is a real absence (operator has no website, LLC is too recent for years claims). A `[scrape-failed]` is debt. Synthesis treats them differently. Conflating the two was the iter-1 lesson.
- **Saturation rule, not count target.** Capture stops when distinct job-noun and praise-pattern categories both plateau, never at a fixed N.
- **Multi-source dedup key is `author + date + body[:30]`.** Duplicates across GBP, Birdeye, Yelp surface as confidence boost count next to the canonical entry.
- **Photo capture hits all surfaces.** GBP API plus FB Playwright. Stopping at GBP under-uses the operator's library.
- **Em dashes prohibited.** All text the skill emits (README.md, intake.md, reviews.md, summary.json string values, manifest.json string values, process-notes.md) uses periods, commas, semicolons, colons, hyphens. The voice rule is universal across the prospect-site stack.
- **Forcing-function exit criterion.** Every `audit/intake.md` field is filled with a value OR explicitly tagged. Zero ambiguous blanks. The populated intake must pass through Design's CONTENT-INVENTORY end-to-end without re-asking for data.
- **SHA pinning of standing docs.** `README.md` always pins the four standing docs and the category profile to a specific grm-pipeline commit. `[pending-pin]` only appears when both remote `git ls-remote` and a local `~/grm-pipeline/` clone fail; the failure prints to stderr.

## Trigger pattern

The user invokes the skill by typing:

```
/prospect-audit-social "Some Contractor LLC" ChIJ......place_id......
```

or with a Google Maps URL:

```
/prospect-audit-social "Some Contractor LLC" https://www.google.com/maps/place/?q=place_id:ChIJ...
```

Claude Code detects the trigger and runs `audit.py` with the two arguments. The skill produces the workspace and reports back: workspace path, GitHub repo URL, capture summary (photos N gbp + N fb, reviews captured M with saturation status), pinned grm-pipeline SHA, and the deferred-state list.

## What v0.2 does not do (v0.3 backlog)

- Vision-based `suggested_slot` for photo manifest. Currently filename-pattern only.
- FB photo `caption_text` capture. Would require parent-post extraction from the FB photos grid.
- FB photo `customer_attributed` inference. Tagged `[gap]` for v0.2.
- Audit skill auto-creating GitHub repos. Phase 10 assumes the repo already exists or that `gh repo create` succeeds inline.
- IG content scraping beyond profile picture and bio.
- Email extraction from FB About when obfuscated as image (would require OCR).
- Phone-answering test as automated step. Currently manual.
- Multi-language capture (Spanish for some Marion County operators).
- Restaurant-specific menu data extraction.
- Multi-prospect batch capture. Per-prospect on-demand only.
- Synthesis-layer authoring (voice argument, persona, section sequence). Design owns. The skill stops at intake + handoff package.
- FL Division of Corporations registry lookup for owner full-name verification.

If a build run hits a v0.3 candidate, log it to `~/grm-pipeline/grm-lessons.md` and skip. Do not extend v0.2 mid-run.

## Reference

- Build target: `~/grm-pipeline/grm-audit-skill-v0.1-spec.md` (v0.2 deltas in this SKILL.md)
- Universal disciplines: `~/grm-pipeline/grm-pipeline-contract.md`
- Technical defaults: `~/grm-pipeline/grm-build-defaults.md`
- Friction record: `~/grm-pipeline/grm-lessons.md`
- Intake template: `references/intake-template-v2.md` (mirrored from `~/grm-pipeline/templates/intake-template.md`)
- Photo capture standard: `references/photo-capture-standard.md`
- Three-state tagging discipline: `references/three-state-tagging.md`

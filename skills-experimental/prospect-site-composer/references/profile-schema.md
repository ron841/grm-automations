---
schemaVersion: 1.0
schema: profile
authority: COMPOSER_BRAIN.md §4 (handoff contract), §7 (SEO/GEO preservation), §14 (schema versioning)
---

# profile-schema.md

The structure and invariants of `profile.json` — the canonical output artifact of Phase 3. Authored in Stage II (c) against COMPOSER_BRAIN.md. Loaded by Phase 4-new at startup to validate its input and hard-error on schema-version drift; consumed by Phase 5 for content emission; consumed by Phase 5.5 for schema/meta/llms.txt emission; never modified by phases downstream of Phase 3 except for the post-deploy augmentation block called out explicitly below.

---

## 1. Purpose and scope

`profile.json` carries **Phase 3 facts only** — business identity, services, testimonials, brand palette, photo inventory, migration data. No editorial decisions. No Phase 4 outputs. No layout choices, no persona selection, no font picks, no signature micro-interaction.

Editorial decisions live in `composition-plan.json` per COMPOSER_BRAIN.md §4. The seam between the two artifacts is the seam between Phase 3 (facts) and Phase 4 (decisions). Anything that can be re-derived from another artifact is not duplicated here; anything that was chosen rather than observed is not here either.

The schema is **complete by design**. Phase 4-new validates every field declared in this document. Fields marked required must be present; fields marked optional may be absent but if present must match the type and constraint stated. Fields not declared in this document are invalid — adding a field means revising the schema and bumping `$schemaVersion`.

`schemaVersion: 1.0` in the frontmatter declares what Phase 4-new expects in the envelope's `$schemaVersion` key. Format is `major.minor` per COMPOSER_BRAIN.md §14. Major increments invalidate prior `profile.json` files (e.g., field rename, type change, routing change). Minor increments are additive (new optional field, new enum value, new photo source tier). Composer ships at 1.0.

---

## 2. Envelope

Every `profile.json` opens with two required top-level keys that identify the document as a versioned profile artifact.

| Key | Type | Required | Value |
|---|---|---|---|
| `$schemaVersion` | string | yes | `"1.0"` on Composer ship — must match the frontmatter `schemaVersion` of this file. |
| `$schema` | string | yes | `"profile"` — const. Declares this is a profile artifact, not a composition plan. |

**Validation contract.** Phase 4-new's first operation is to read these two keys. If `$schemaVersion` doesn't match what this file's frontmatter declares, Phase 4-new hard-errors with the mismatch surfaced to the operator: `profile.json declares $schemaVersion "X.Y"; profile-schema.md declares schemaVersion "A.B"; upgrade one side`. If `$schema` is not `"profile"`, Phase 4-new rejects the file as not a profile artifact and suggests the operator verify the path.

No silent coercion. No best-effort parsing. A mismatch halts the build so the operator can resolve intent.

---

## 3. Business identity

Facts captured in Phase 1 (business data lookup) and Phase 2 (site crawl).

| Field | Type | Required | Notes |
|---|---|---|---|
| `businessName` | string | yes | Public-facing brand name as the contractor uses it. Example: `"Luna Master Painting"`. |
| `legalName` | string | no | Legal entity name if distinct from `businessName`. Example: `"Luna Master Painting LLC"`. Populated when captured from Secretary of State or incorporation records; omitted when not found. |
| `slug` | string | yes | Kebab-case identifier used for directory paths and URL segments. Matches the prospect's directory under `~/grm-sites-prospects/[slug]/`. Must match `^[a-z0-9][a-z0-9-]*[a-z0-9]$`. |
| `sourceUrl` | string | yes | Canonical URL of the prospect's existing site, as captured in Phase 1. Trailing slash tolerated. Example: `"https://lunamasterpainting.com/"`. |
| `tagline` | string | no | Short descriptive phrase captured from hero or header of the existing site. Example: `"Quality that lasts."`. Omitted when no clean tagline was captured. |

---

## 4. Contact

Phone, email, physical address, hours of operation. These fields feed the nav, the footer, the contact section, and the LocalBusiness JSON-LD schema emitted in Phase 5.5.

### Top-level contact fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `phone` | string | yes | Human-formatted primary phone in U.S. domestic convention. Example: `"(352) 408-8445"`. Parentheses around area code, space after, hyphen between exchange and line. |
| `phoneDigitsOnly` | string | yes | Exactly 10 digits, no formatting. Derived from `phone`; redundant by intent so that `tel:` links and analytics event payloads do not re-parse. Example: `"3524088445"`. |
| `email` | string | no | Primary contact email address, captured when the existing site exposes one. Omitted when not found. |
| `address` | object | yes | Physical address object, fields below. |
| `hours` | object | yes | Hours-of-operation object, fields below. |

### `address` object

| Field | Type | Required | Notes |
|---|---|---|---|
| `street` | string | yes | Street number and name. Unit/suite appended inline if applicable. |
| `city` | string | yes | Primary business city. |
| `state` | string | yes | Two-letter U.S. state code. Constraint: exactly two uppercase letters. |
| `zip` | string | yes | Five-digit or five-plus-four ZIP. Constraint: `^\d{5}(-\d{4})?$`. |
| `country` | string | yes | Full country name. Default `"United States"` for Composer's current Marion County scope. |
| `googleMapsUrl` | string | no | Canonical Google Maps URL, typically from Google Places `cid=` or `place_id=` form. Populated when Phase 1 resolved a Google Business Profile. |

### `hours` object

Hours are captured verbatim from the source most likely to be authoritative — Google Business Profile hours override scraped site hours when the two conflict. The object's keys are per-day or grouped-day labels with time-range string values. Convention is one of:

- **Per-day keys:** `monday`, `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`, `sunday` — each with a string value like `"8:00 AM - 6:00 PM"` or `"Closed"`.
- **Grouped-day keys:** `mondayToSaturday`, `mondayToFriday`, `weekdays`, `weekends` — each with a string value as above. Common for contractors with uniform weekday hours.
- Combinations are permitted (e.g., `mondayToSaturday` plus `sunday: "Closed"`).

| Field | Type | Required | Notes |
|---|---|---|---|
| `<day-or-group-key>` | string | at least one | Time range or `"Closed"`. Time format `"H:MM AM - H:MM PM"` or 24-hour equivalent. Flexible because contractor hours disclosures vary. |
| `sourceNote` | string | no | Free-form note explaining the source or any conflict resolution. Example: `"Hours from Google Business Profile (site says 7-6 but Google canonical is 8-6)"`. Non-rendered. |

Phase 5.5 transforms `hours` into LocalBusiness JSON-LD `openingHours` / `openingHoursSpecification` arrays; that transformation is a separate concern documented in `seo-geo.md`.

---

## 5. Ownership and history

| Field | Type | Required | Notes |
|---|---|---|---|
| `ownership` | object | no | Owner structure and identity. Fields below. Omitted when ownership details were not captured. |
| `yearsInBusiness` | object | no | Business tenure with evidence. Fields below. Omitted when no tenure signal was captured. |
| `licenseNumber` | string \| null | yes | License or trade number captured from the existing site or Google profile. Explicit `null` signals captured-absence — Phase 3 looked for a license and did not find one. Required `null` (rather than optional omission) forces Phase 3 to make the captured-vs-typically-licensed distinction rather than silently omit; downstream consumers can rely on the field's presence. Phase 4 reads `null` as a data-quality signal when the trade-category default in `emotional-arc.md` would typically carry a license. |

### `ownership` object

| Field | Type | Required | Notes |
|---|---|---|---|
| `structure` | string | yes | One of `"family-owned"`, `"sole-proprietor"`, `"partnership"`, `"LLC"`, `"corporation"`. Captured from About page language, Secretary of State records, or named-owner signals on the existing site. |
| `owners` | string[] | yes | Array of named owners or principals, in display order. Strings are full first+last names where captured, or first-name-only when captured. A family-team entry like `"Armando's father"` is acceptable when only one party is named. |
| `ownerSource` | string | no | Free-form citation of where owner identity was captured (review text, About page, Google profile). Non-rendered; supports audit trail and Phase 4's trust-signal scoring. |

### `yearsInBusiness` object

Tenure is often asymmetrically evidenced — a contractor may say "over 20 years" without a founding date anywhere. The object captures both exact and minimum-evidenced counts so Phase 4 can surface the strongest claim it can substantiate.

| Field | Type | Required | Notes |
|---|---|---|---|
| `exact` | integer \| null | yes | Exact years in business when a founding year was captured. Explicit `null` when only a lower-bound estimate is available. |
| `minimumEvidenced` | integer | yes | Minimum years substantiated by concrete evidence (oldest captured review, founding-date document, license issue date). Always present when `yearsInBusiness` is present. |
| `evidence` | string | yes | Citation of the evidence used to compute `minimumEvidenced`. Example: `"Steven Peterson review is 4 years old on Google"`. |

---

## 6. Services

### `services[]`

Array of service objects. Minimum 3 per Phase 3.5's hard-failure gate (`SKILL.md` Phase 3.5). Empty arrays are invalid; arrays with fewer than 3 entries halt the build at Phase 3.5 and never reach Phase 4.

| Field | Type | Required | Notes |
|---|---|---|---|
| `name` | string | yes | Display name of the service as Phase 5 will render it. Example: `"Interior Painting"`. Title-case conventional. |
| `category` | string | yes | Open enum. Luna F8 known-good values: `"residential"`, `"commercial"`, `"custom"`, `"maintenance"`, `"advisory"`, `"emergency"`. Trade-specific extensions documented in `content-rules.md` (authority for the open tail). Drives services-grid grouping and FAQ-template selection. |
| `description` | string | yes | One-to-two-sentence benefit-first description authored in Closing Table voice per `voiceMap.md`. Used verbatim as the service card body copy and as the Service-schema `description` field in Phase 5.5. |

### `serviceAreas[]` and `serviceAreaRegion`

| Field | Type | Required | Notes |
|---|---|---|---|
| `serviceAreas` | string[] | yes | Array of city or township names where the contractor works. Display order preserved. Phase 5 renders in the contact section and footer. Minimum one entry. |
| `serviceAreaRegion` | string | no | Human-readable aggregate region label covering `serviceAreas`. Example: `"Central Florida (Lake, Marion, Orange, Sumter counties)"`. Used in the hero subhead and LocalBusiness schema `areaServed` fallback. |

---

## 7. Marketing facts

Pricing, guarantees, and named partner relationships. These feed promo bars, trust marquees, and specific FAQ answers.

### `featuredPromotion`

| Field | Type | Required | Notes |
|---|---|---|---|
| `featuredPromotion` | object \| null | no | Featured promotion or starting-price callout. `null` when no real promotion was captured. When present, requires all sub-fields below. |

Sub-fields when `featuredPromotion` is present:

| Field | Type | Required | Notes |
|---|---|---|---|
| `text` | string | yes | Display text for the promo bar or callout. Example: `"Pressure washing from $150 per house"`. |
| `price` | string | yes | Price expressed as display-formatted string, including currency symbol and any qualifying text. String rather than numeric because real-world prices include modifiers: `"$150"`, `"From $150"`, `"$150-$300 range"`. |
| `type` | string | yes | One of `"starting-price"`, `"fixed-price"`, `"discount"`, `"seasonal"`, `"limited-time"`. Drives promo-bar styling and FAQ answer framing. |

### `guarantees[]`

Array of guarantee objects. Each must cite its source so Phase 4 can validate the claim before Phase 5 renders it in the trust marquee.

| Field | Type | Required | Notes |
|---|---|---|---|
| `type` | string | yes | Short human-readable description. Example: `"one-year paint guarantee"`. |
| `source` | string | yes | Where the guarantee was captured (review, contact page, trust badge). Example: `"John Frazier Google review"`. Non-rendered citation. |

### `partners[]`

| Field | Type | Required | Notes |
|---|---|---|---|
| `partners` | string[] | no | Array of named partner brands or suppliers. Example: `["Sherwin-Williams", "Home Depot"]`. Empty array or omission both mean "no partner relationships captured"; prefer omission when nothing is known. |

---

## 8. Reviews

Review count, aggregate rating, and individual testimonials.

### `googleBusinessProfile`

| Field | Type | Required | Notes |
|---|---|---|---|
| `googleBusinessProfile` | object | no | Google Business Profile metadata. Omitted when no Google profile was resolved in Phase 1. When present, all sub-fields required. |

Sub-fields when `googleBusinessProfile` is present:

| Field | Type | Required | Notes |
|---|---|---|---|
| `placeId` | string | yes | Google Places API place ID for the prospect's profile. |
| `rating` | number | yes | Aggregate star rating on a 0-5 scale with one decimal. Constraint: `0.0 <= rating <= 5.0`. |
| `reviewCount` | integer | yes | Total number of reviews the profile reports. Constraint: non-negative integer. |
| `businessStatus` | string | yes | One of `"OPERATIONAL"`, `"CLOSED_TEMPORARILY"`, `"CLOSED_PERMANENTLY"`. Phase 3.5 hard-fails on non-`"OPERATIONAL"` status. |

### `testimonials[]`

Array of testimonial objects. Minimum one per Phase 3.5's hard-failure gate. Every testimonial carries a real first name per Hard Rules for Phase 5 (`SKILL.md` Phase 5); fabricated testimonials are a slop failure the build cannot recover from.

| Field | Type | Required | Notes |
|---|---|---|---|
| `name` | string | yes | Reviewer's display name as captured from the source. Real first name at minimum. |
| `rating` | integer | yes | Star rating. Constraint: integer `1 <= rating <= 5`. Floating-point Google ratings are averaged values, but individual testimonial ratings are always whole stars. |
| `source` | string | yes | One of `"Google"`, `"Yelp"`, `"Facebook"`, `"site"`, `"BBB"`, or other attribution string matching where the testimonial was captured. |
| `when` | string | yes | Human-readable recency from the source (`"1 year ago"`, `"6 months ago"`, `"2 years ago"`). Not parsed to a timestamp; Phase 5 renders verbatim. Phase 3.5 uses the oldest `when` across testimonials to derive `yearsInBusiness.minimumEvidenced` when no other evidence exists. |
| `quoteVerbatim` | string | yes | The full quote as captured, including any truncation from the source. Never edited for grammar or length. Supports audit review. |
| `quoteShort` | string | yes | Editor-authored short version for card and pull-quote use. Single sentence or two short sentences. Derived by Phase 3 from `quoteVerbatim` following the rules in `content-rules.md`. |

**Testimonial photos are Google-avatar-only.** Testimonials do not consume any `photoInventory` role and no avatars are substituted from the photo library. Editorial rule stable across all tiers per `image-handling.md` line 147. When Phase 5 needs a testimonial avatar it fetches the Google avatar URL adjacent to the review; that URL does not live in this schema because Phase 5 resolves it at render time against the Google Places photo reference stored alongside the testimonial capture. A future schema revision may carry avatar references explicitly if fetch-at-render becomes brittle.

---

## 9. Brand palette

Raw color swatches extracted from the prospect's logo or brand mark. All values are observed facts — swatches pulled via `node-vibrant` against the logo, or overrides where a specific swatch failed the derivation heuristics. Derived tokens (primary-hover, dark-primary-hover, accent-variant gradients, hero page background computed from primary hue warmth) are computed inline in Phase 5 per `css-framework.md` and are not schema fields.

| Field | Type | Required | Notes |
|---|---|---|---|
| `primary` | string | yes | Primary brand color as a six-digit hex. Constraint: `^#[0-9a-fA-F]{6}$`. Feeds `--color-primary`. |
| `primaryName` | string | yes | Human-readable name for `primary`. Example: `"Luna Orange"`. Feeds logo-alt text and internal documentation. |
| `darkPrimary` | string | yes | Dark anchor color used for the dark section treatment. Populated by `node-vibrant`'s `DarkVibrant` swatch when available, otherwise derived via `deriveDarkPrimary()` from `primary`. When the logo provides an explicit dark swatch, that swatch overrides the derivation per `COMPOSER_BRAIN.md §6 PA.4` and `anti-slop-rules.md` Rule E6. Constraint: `^#[0-9a-fA-F]{6}$`. |
| `darkPrimaryName` | string | yes | Human-readable name for `darkPrimary`. Example: `"Luna Navy"`. |
| `accent` | string | yes | Secondary accent color. Constraint: `^#[0-9a-fA-F]{6}$`. Feeds `--color-accent`. |
| `accentName` | string | yes | Human-readable name for `accent`. |
| `neutral` | string | no | Tertiary neutral color when the logo exposes one (common in three-color brand systems). Constraint: `^#[0-9a-fA-F]{6}$`. Omitted when not captured. |
| `neutralName` | string | no | Human-readable name for `neutral`. Required when `neutral` is present. |
| `background` | string | no | Background color sampled from the logo when a distinct background is detected. Constraint: `^#[0-9a-fA-F]{6}$`. |
| `source` | string | yes | Provenance string documenting how the palette was derived. Example: `"node-vibrant against logo.png (2388x2388 PNG from wsimg CDN)"`. |
| `vibrantPopulation` | integer | yes | `node-vibrant`'s population count for the primary swatch. Constraint: non-negative integer. Used by Phase 4 as a confidence signal — below a threshold, the palette is flagged as low-confidence at the approval gate. |
| `note` | string | no | Free-form note documenting logo characteristics or derivation caveats. Non-rendered. |

---

## 10. Photo pipeline

The photo inventory is the most structured section of `profile.json` because three downstream consumers (Phase 4 role-hierarchy decisions, Phase 5 HTML emission, Phase 5.5 OG-tag and ImageObject schema emission) all read from it with different slice patterns.

### `photos` (source counts)

Per-source aggregate metadata. Not the photos themselves — that's `photoInventory`. This block summarizes what each source contributed and why photos were rejected.

| Field | Type | Required | Notes |
|---|---|---|---|
| `photos` | object | yes | Container for source-keyed metadata. |
| `photos.google` | object | yes | Tier 1 source. Sub-fields: `count` (integer, non-negative), `attributionString` (string — Google Maps Platform attribution required per `image-handling.md`). |
| `photos.site` | object | yes | Tier 2 source. Sub-fields: `count` (integer, non-negative), `rejected` (integer, non-negative — count rejected at disqualifier stage), `rejectReason` (string, free-form, optional — present when `rejected > 0`). |
| `photos.instagram` | object | yes | Tier 3 source. Sub-fields: `count` (integer, non-negative), `note` (string, optional — e.g., `"No handle provided and none captured on site"`). |
| `photos.unsplash` | object | yes | Tier 4 fallback. Sub-fields: `count` (integer, non-negative), `note` (string, optional). |

Each source object is always present even when its `count` is zero. Absent sources are the same as zero-count sources; declaring them explicitly makes the source coverage auditable at a glance.

### `photoInventory[]`

The authoritative list of all accepted photos in the library. Phase 3 populates this after quality scoring and disqualifier rejection. Each entry is a single photo file with its metadata and eligibility signals.

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | string | yes | Short identifier used throughout the schema to refer to this photo. Convention: source-letter plus two-digit index, e.g., `"g01"` for Google photo 1, `"s02"` for site photo 2, `"i03"` for Instagram, `"u04"` for Unsplash. Must be unique within the array. |
| `file` | string | yes | Relative path from the prospect's build root to the photo file. Example: `"assets/photos/google/g01.jpg"`. Phase 5 emits this verbatim into `src` attributes. |
| `widthPx` | integer | yes | Pixel width of the photo. Populated by Phase 3's image analysis. Constraint: positive integer. **Required for OG tag emission in Phase 5.5** per COMPOSER_BRAIN.md §7 preservation item 5 — OG image dimensions depend on this field, and re-parsing `dim` at emission time is the wrong pattern. |
| `heightPx` | integer | yes | Pixel height of the photo. Constraint: positive integer. |
| `dim` | string | no | Derived display-only string of the form `"WIDTHxHEIGHT"`. Example: `"4032x3024"`. Redundant by intent — present for human readability in manual audits. Consumers must use `widthPx` and `heightPx`, not parse this field. Phase 3 writes both. |
| `longEdgePx` | integer | yes | `max(widthPx, heightPx)`. Stored rather than computed at consume-time because multiple eligibility checks gate on it (`>= 1600` for hero eligibility, `>= 1200` for gallery). |
| `orient` | string | yes | One of `"landscape"`, `"portrait"`, `"square"`. Computed from aspect ratio: landscape when `widthPx / heightPx > 1.1`, portrait when `< 0.9`, square otherwise. |
| `content` | string | yes | Content-type tag per SKILL.md Phase 3. One of `"finished_work"`, `"team"`, `"owner"`, `"jobsite"`, `"stock"`, `"unknown"`, or a trade-specific content type declared in `image-handling.md`. Common observed values include `finished_exterior`, `finished_exterior_commercial`, `finished_interior`, `finished_wood_staining`. |
| `note` | string | no | Free-form note describing what's in the photo. Non-rendered. Example: `"green lakeside clubhouse, bright sky"`. Supports auditor understanding and is used as a fallback `alt` text source when no better alt text is derived. |
| `disqualifiers` | string[] | yes | Array of disqualifier codes triggered by the photo. Empty array when none apply. Codes are the enumerated set from `SKILL.md` Phase 3: `"watermark"`, `"logo"`, `"text"`, `"blurry"`, `"dark"`, `"low_res"`. A photo with any disqualifier is not accepted into the emittable library; the entry remains in `photoInventory` only when the disqualifier does not reach the rejection threshold. |
| `rejectionReason` | string | no | Free-form reason when a photo was considered but rejected entirely. Populated when the photo is retained in the inventory for audit but disqualified from any role. Example: `"logo watermark overlay top-left (disqualifier)"`. Omitted when the photo is accepted. |
| `score` | integer | yes | Quality score 0-100 per the scoring rubric in `image-handling.md`. Phase 4 consumes score plus eligibility to pick assignments. |
| `eligibleRoles` | string[] | yes | The set of photo roles for which this entry meets the resolution, orientation, and quality criteria. See §10.1 below for the enumeration and eligibility predicates. A photo with no eligible roles is still valid in the inventory (it may be held for manual promotion or remain in the library for later pipeline use) and has an empty array. |

### 10.1 `eligibleRoles` — role vocabulary (closed enum)

Every `photoInventory[].eligibleRoles` entry must come from this closed set of eight role names. Each role has an explicit eligibility predicate drawn from `image-handling.md` and `hero-patterns.md`. Phase 3 evaluates every predicate against every accepted photo and records every role the photo is eligible for; Phase 4 picks single-photo assignments from the eligible pool and writes those assignments to `composition-plan.json`.

| Role | Eligibility predicate |
|---|---|
| `heroBackground` | `orient == "landscape"` AND `longEdgePx >= 1600` AND `disqualifiers` is empty AND `score >= 60`. Used as the photo behind a hero-mode mesh or glass composition. |
| `heroPlate` | `longEdgePx >= 1600` AND `disqualifiers` is empty AND `score >= 75`. Landscape preferred; square orientation is acceptable because Phase 5 can crop 16:9 from center. Per `image-handling.md` §51–52. Used as the full-bleed Layout D plate, About page lead, or other prominent lead positions. |
| `ownerPortrait` | `content == "owner"`. First accepted owner photo wins this assignment by Phase 4 convention; additional owner photos remain eligible and Phase 4 picks. |
| `environmentalPortrait` | `content` depicts a person in a work context (owner, team, crew-on-job) AND `longEdgePx >= 1600` AND `score >= 60` AND `disqualifiers` is empty. Distinct from `ownerPortrait` because environmental photos may show crew members or family-team participants who are not the named principal. Feeds About page lead, About page team photos, and Footer brand block. |
| `detailShot` | `content` is a tight crop, material texture, or close-up of finished work. Resolution is intentionally flexible per `image-handling.md` §60–61: the crop carries the value, not the pixel count. Requires `score >= 50` AND empty `disqualifiers`. Feeds section dividers, eyebrow watermark backgrounds, and About-page detail insets. |
| `evidenceShot` | `content` depicts completed work (finished_work family) AND `score >= 50` AND `disqualifiers` is empty. Feeds the before/after gallery, the trust marquee, and — via content-match filtering at Phase 4 assignment time — the services-grid cards. |
| `gallery` | `score >= 60` AND `disqualifiers` is empty. Default fallback eligibility for any accepted photo not claimed by a more specific role. Feeds `gallery.html` when that page is generated (6+ quality photos threshold per `SKILL.md` Phase 5). |
| `credential` | `content` depicts a license document, certification badge, award, or similar credential artifact. Used in the trust marquee when available; otherwise trust marquee uses SVG icons. May overlap with `evidenceShot` on photos that show a credential in-context (an award plaque on a shop wall) — both eligibility flags apply. |

A photo's eligibility set is the union of every predicate it satisfies. Example: Luna F8's `g01` (4032×3024 landscape, `content: finished_exterior_commercial`, score 95, no disqualifiers) satisfies `heroBackground`, `heroPlate`, `evidenceShot`, `gallery` — four roles land in `eligibleRoles`. Luna F8's `g03` (3024×3024 square, `content: finished_exterior_residential`, score 82, no disqualifiers) satisfies `heroPlate`, `evidenceShot`, `gallery` but not `heroBackground` (not landscape).

**Testimonial photos are not carried in `photoInventory` eligibility.** Testimonials use Google-avatar references resolved at render time against the Google Places photo handle stored alongside each testimonial — see §8. This is a stable editorial rule across all tiers per `image-handling.md` line 147: testimonial photos are Google-avatar-only and never substituted from the editorial library. An earlier draft of this schema proposed a `testimonial` role; it is intentionally absent from the current enum because no Phase 5 emission path consumes one.

**Services-grid assignments are derived, not a role.** Phase 4 composes the services-grid pool at assignment time by filtering `evidenceShot`-eligible photos against service content-match criteria per `image-handling.md` §104 and §111. There is no `servicesGrid` role in the eligibility enum — the services-grid pool is a view over `evidenceShot`-eligible entries, and per-service assignments land in `composition-plan.json`. This keeps the eligibility enum about editorial role (what the photo IS in the page's visual hierarchy) rather than about section (where the photo goes).

**Eligibility is plural; assignment is singular.** The `eligibleRoles` array may list every role a photo qualifies for. The final per-role assignment — which photo fills which slot on which page — lives in `composition-plan.json`, and each photo is assigned to at most one role in the emitted build (per the editorial hierarchy rule in `image-handling.md` §123). Keeping eligibility plural on Phase 3's side and assignment singular on Phase 4's side is the load-bearing seam in the Composer photo architecture.

---

## 11. Migration data

URL inventory captured in Phase 2.5 for the eventual migration from the prospect's existing site to the Composer-built site. Phase 5 does not render this block; it exists for the post-signing migration playbook.

| Field | Type | Required | Notes |
|---|---|---|---|
| `migrationData` | object | no | Migration URL inventory. Omitted when Phase 2.5 did not run or produced no usable output. |

Sub-fields when present:

| Field | Type | Required | Notes |
|---|---|---|---|
| `indexedUrls` | string[] | yes | Absolute URLs from the prospect's existing site captured via `site:` search and Wayback Machine. Deduplicated. |
| `excludedFromMigration` | string[] | yes | URLs explicitly excluded (e.g., CMS login paths, orphaned account pages). Example: `["/m/login", "/m/reset", "/m/create-account"]`. |
| `archiveSnapshots` | string | yes | Either a JSON-parseable summary of Wayback snapshots, or a free-form note explaining why archive data is missing (e.g., `"Wayback sparkline returned non-JSON; skipped. Manual Wayback crawl flagged for post-signing migration."`). Free-form because the capture step is lossy. |

---

## 12. Post-deploy augmentation (optional)

These fields are **not Phase 3 output**. Phase 7 (Vercel deploy) writes them into `profile.json` after successful deployment so the single file remains a complete per-prospect record. Declared here for schema completeness; Phase 4-new must not rely on them and must tolerate their absence. A Phase 3 freshly produced `profile.json` does not contain these fields.

| Field | Type | Required | Notes |
|---|---|---|---|
| `previewUrl` | string | no | Canonical preview URL for the deployed site. Example: `"https://luna-master-painting-grm.vercel.app/"`. Post-Phase-7 populated. |
| `deployment` | object | no | Deployment metadata. Omitted until Phase 7 succeeds. |

Sub-fields when `deployment` is present (all populated by Phase 7):

| Field | Type | Required | Notes |
|---|---|---|---|
| `vercelProjectId` | string | yes | Vercel project identifier. |
| `vercelTeam` | string | yes | Human-readable team identifier with parenthetical team ID. |
| `deploymentId` | string | yes | Vercel deployment identifier. |
| `primaryUrl` | string | yes | Same as top-level `previewUrl`; duplicated here for deploy-block self-containment. |
| `rawUrl` | string | yes | Vercel raw deploy URL with commit hash. |
| `ssoProtection` | string | yes | SSO state as captured post-deploy. Common value: `"disabled post-deploy via API PATCH"`. |
| `deployedAt` | string | yes | ISO 8601 timestamp of successful deploy. |

---

## 13. Validation contract

Phase 4-new's startup sequence against `profile.json`:

1. **Parse and envelope check.** Parse file as JSON. Assert `$schemaVersion` present and matches this file's frontmatter `schemaVersion`. Assert `$schema == "profile"`. Hard-error on any mismatch.
2. **Required field presence.** Walk every required field declared above. Hard-error on any missing field with the path surfaced to the operator.
3. **Type and constraint check.** Validate every present field against its declared type and any regex or range constraint. Hard-error on any violation.
4. **Enumerated value check.** Validate every declared enum field (`businessStatus`, `orient`, `content`, role names in `eligibleRoles`, disqualifier codes) against its enumeration. Hard-error on unknown values.
5. **Cross-field invariants.** Assert `photoInventory[].longEdgePx == max(widthPx, heightPx)`. Assert every `photoInventory[].id` is unique. Assert `services.length >= 3`. Assert `testimonials.length >= 1`. Assert `googleBusinessProfile.rating` in `[0.0, 5.0]` when present.

On all-pass, Phase 4-new proceeds to produce `composition-plan.json`. On any hard-error, the build halts with the specific assertion failure and operator guidance.

No soft-warning tier at schema-validation time. Schema is a contract; contracts are either satisfied or not.

**Phase 3.5 threshold alignment.** The `services.length >= 3` and `testimonials.length >= 1` assertions in step 5 mirror Phase 3.5's hard-failure gates in `SKILL.md`. Two sources of truth is a deliberate defense-in-depth trade-off: if Phase 3.5 is bypassed or silently fails, schema validation catches the shortfall. Revisions to Phase 3.5 thresholds require a matching `schemaVersion` bump to this file — minor bump when the schema tightens (e.g., raising the minimum from 3 to 4 services), major bump when the schema loosens to reflect a reduced Phase 3.5 gate (because files that previously validated may now be required to carry fields that older gates did not enforce).

---

## 14. Cross-references

- `COMPOSER_BRAIN.md` §4 — handoff contract (profile.json → composition-plan.json), schema versioning (§14), photo role scarcity behavior (§4 addendum).
- `COMPOSER_BRAIN.md` §7 — SEO/GEO preservation contract, specifically item 5 (photo manifest with dimensions for OG-tag emission).
- `SKILL.md` Phase 3 — Phase 3's emission of `profile.json` from Phase 1/2 captures plus photo processing pipeline.
- `SKILL.md` Phase 3.5 — hard-failure gates that must pass before a `profile.json` reaches Phase 4.
- `references/image-handling.md` — photo scoring rubric, disqualifier rules, role-based section assignment table (current assignment model; assignments migrate to `composition-plan.json` under the Composer split).
- `references/content-rules.md` — service description voice (Closing Table), banned phrases, category conventions.
- `references/voiceMap.md` — voice-per-zone authority referenced from service description emission.
- `references/typography.md` — persona-conditional font selection that `composition-plan.json` encodes; this schema does not document Composer's font selection.
- `references/seo-geo.md` — LocalBusiness JSON-LD, Service schema, Review schema, ImageObject schema emitted in Phase 5.5 from `profile.json` fields.
- `references/anti-slop-rules.md` Rule E6 — dark-primary derivation hardening that `brandPalette.darkPrimary` preserves.

---

## 15. Version

`schemaVersion: 1.0`. First published version. Authored in Stage II (c) Session 2 against Luna F8's `profile.json` as the anchor instance.

Material differences from Luna F8's pre-schema file (migration notes for the next reader):

- `$schemaVersion` and `$schema` envelope keys added (required by this schema; not present in pre-schema files). A Luna F8 file retrofitted to 1.0 gains both keys at the top of the object.
- `photoInventory[].widthPx`, `heightPx`, `longEdgePx` added as required integers; `dim` demoted to derived display-only. Luna F8 stored `dim` as a `"WIDTHxHEIGHT"` string only — a retrofit parses `dim` once to populate the three integer fields and then keeps `dim` for human audit.
- `photoInventory[].eligibleRoles` added as an eight-role closed enum (`heroBackground | heroPlate | ownerPortrait | environmentalPortrait | detailShot | evidenceShot | gallery | credential`). Luna F8's singular `role: "heroBackground"` / `role: "heroPlate"` field retires because role *assignment* moves to `composition-plan.json` under the Composer split while *eligibility* stays plural on Phase 3's side.
- `photoInventory[].rejectionReason` added as optional human-readable detail; previously carried in `photoAssignments.rejectedWithReason`.
- `photoAssignments` top-level object retires entirely; per-photo eligibility on `photoInventory` entries supersedes. Luna F8's `heroCandidatesStrictLandscape` and `heroCandidatesSquareCroppable` arrays are absorbed by the `heroBackground` and `heroPlate` eligibility predicates — the two pool dimensions collapse into the role definitions themselves.
- `typography` block (Luna F8 carried `headingFont`/`bodyFont` scraped from the existing site) dropped entirely. The block had no current consumer in Phase 5 or Phase 5.5. Composer's font selection is persona-conditional per `CONFIG.fonts` and lives in `composition-plan.json`. If a future approval-gate "current-vs-proposed" font comparison surface ships, it will declare its own schema fields or re-run the Phase 1 font scrape at that time.
- `designChoices.heroBackground` / `heroBackgroundName` / `heroBackgroundReason` dropped entirely. The hero page background color is a deterministic derivation from `brandPalette.primary` hue warmth — same category as `primaryHover` — and is computed inline by Phase 5 at render per scope call #5 (derivations compute at Phase 5, profile carries inputs only). The hue-warmth derivation rule itself is flagged for authoritative citation in `composer-backlog.md` Active.
- Phase 4 decorations retire from `profile.json` — `design.*` (persona, heroMode, heroGlassVariant, videoAugmentation, signatureMicroInteraction, editorialLayouts, fullBleedPhoto, watermarkTarget, constraintsOK, constraintRelaxations, and all companion `*Reason` fields) and `designScore` move to `composition-plan.json`. See Stage II (c) Phase 2 authoring (`composition-plan-schema.md`) for the target schema.
- `previewUrl` and `deployment.*` declared as optional Phase-7 augmentation; Luna F8 has these populated but the schema makes clear they are not Phase 3 output and Phase 4-new must tolerate their absence.
- `licenseNumber` becomes required `string | null` (was omittable in the Luna F8 shape). `null` is the explicit absence marker; the requirement forces Phase 3 to make the captured-vs-typically-licensed distinction rather than silently omit.

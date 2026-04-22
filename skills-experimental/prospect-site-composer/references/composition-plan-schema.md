---
schemaVersion: 1.0
$schema: composition-plan
status: checkpoint-1-reviewed-pending-commit
---

# composition-plan-schema.md

Schema definition for `composition-plan.json`, the artifact Phase 4-new produces and Phase 5-new consumes. This is the new artifact the whole Composer architecture turns on — brain §4 names it as "complete-by-design — no implicit fallbacks."

**Relationship to other artifacts.** Phase 3 produces `profile.json` (facts, schema at `profile-schema.md`). Phase 4-new reads `profile.json`, makes all editorial decisions (persona, layouts, photo assignments, italic selections, voice zone assignments, pull-quote deployments, display-moment placements), and produces `composition-plan.json`. Phase 5-new reads `composition-plan.json` + `profile.json` and emits HTML/CSS/JS implementing only what the plan declares. Phase 5.5 reads both JSONs (never the DOM) to emit schemas, meta tags, and `llms.txt`. No editorial decisions happen in Phase 5; no facts are invented in Phase 4.

**Authority sources referenced throughout:**
- `typography-patterns.md` (Design's editorial framework — three voices, role classes, pull-quote heuristic §6, scale and breakpoints §7, 13 Phase 6 checks, persona-conditional tables, five personas × three voices)
- `voiceMap.md` (Design's zone-to-voice assignment — closed zone enum, three-voice × five-persona resolution)
- `emotional-arc.md` (five personas with machine keys, italic word classes per persona)
- `hero-patterns.md` (hero mode decision tree, hero background modes)
- `section-patterns.md` (section emission patterns)
- `image-handling.md` (photo role emission; role-hierarchy eligibility/assignment split pending per composer-backlog.md)

---

## §1 Envelope

Top-level required keys per brain §14.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `$schemaVersion` | string (format `major.minor`) | yes | Must equal `schemaVersion` declared in this file's frontmatter. Phase 4-new hard-errors on mismatch per brain §14. |
| `$schema` | const `"composition-plan"` | yes | Identifies which schema describes this file. |
| `businessSlug` | string | yes | Cross-references `profile.json.slug`. Must match exactly. |
| `generatedAt` | ISO 8601 timestamp | yes | Phase 4 emit time. |
| `generatedBy` | string | yes | Phase 4 version identifier (e.g., `"phase-4-v0.8-composer"`). |
| `profileSchemaVersion` | string | yes | `$schemaVersion` of the `profile.json` Phase 4 consumed. Phase 5-new hard-errors if this doesn't match the `profile.json`'s `$schemaVersion` at consumption time. Catches staleness across regenerations. |

---

## §2 Site-level design decisions

Fields that apply to the whole site, not per-page. Migrated from Luna F8's `profile.design.*` block per profile-schema scope call #1.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `persona` | enum | yes | One of `quiet-confidence` · `earned-pride` · `neighborhood-steady` · `urgent-service` · `modern-specialist`. Machine keys per `emotional-arc.md`. Display name mapping lives in `emotional-arc.md` (not duplicated here — `urgent-service` → "Rescue-ready" asymmetry documented there). |
| `personaReason` | string | yes | Narrative: how Phase 4 reached this persona. Three-input priority per SKILL.md Phase 4. |
| `signatureMicroInteraction` | enum | yes | Tier 1 signature (compositional, site-wide, one). See §2.1. |
| `signatureMicroInteractionReason` | string | yes | Narrative. |
| `microInteractions` | array of enum | yes | Tier 2 micro-interactions (motion, element-scoped, plural). Zero or more values. Per-persona defaults documented in `emotional-arc.md` (pending Stage III rewrite); schema does not enforce per-persona values. Empty array allowed. See §2.1. |
| `microInteractionsReason` | string | conditional | Required when `microInteractions` non-empty. Narrative. |
| `voicesInUse` | array of enum | yes | Subset of `["display", "body", "data"]`. Per Design's Stage I signoff — enables Phase 6 Check 12 (three-voice presence per page) and supports site-level schema expression that all three voices appear somewhere on the site. Expected value on any Composer build: `["display", "body", "data"]`; schema does not require all three at site level but flags builds missing a voice. |
| `pathConvention` | object | yes | URL path convention for generated pages. See §2.2. |
| `colorScheme` | object | yes | Phase 4 color application decisions. See §2.3. |

### §2.1 Signature (Tier 1) and micro-interactions (Tier 2)

Per Design Checkpoint 1 q1 follow-up: two-tier architecture. **Signature** is compositional, site-wide, and singular — the moment a reader remembers after closing the tab. **Micro-interactions** are motion, element-scoped, and plural — animation behaviors applied to specific elements or states. Neither displaces the other; they run alongside.

**Why two tiers.** A reader can notice many motion cues across a page without any of them being the thing they remember. The signature is singular by design — pick one compositional moment and commit. Motion runs alongside, enriching but not competing. `css-framework.md` Motion Restraint governs Tier 2; typography-patterns.md role classes define Tier 1 treatments.

#### Tier 1 — `signatureMicroInteraction` enum (compositional, singular)

Closed set of six values. Each Composer build declares exactly one site-wide signature.

| Value | Concept |
|---|---|
| `italic-color-shift` | Italicized accent-color-shifted span inside H1/H2 per `typography-patterns.md` Rule 1/Rule 2 and `.role-italic-signature` class. Typographic treatment, not an animation. Default signature for `quiet-confidence`, `earned-pride`, `modern-specialist` at three deployments; `neighborhood-steady` and `urgent-service` at two deployments minimum per Rule 1. |
| `watermark-numeral-offset` | Watermark numeral offset behind a filled numeral per `typography-patterns.md` Rule 4 — static positioning treatment. |
| `anchor-strip-pivot` | Voice-pivot anchor strip per `voiceMap.md` §3 — italic Fraunces pullquote + mono credit between hero and services. |
| `hero-glass-blur` | Glass-blur treatment on hero-heavy compositions. |
| `stat-row-ledger` | Stat-row ledger treatment — StatRow composed as a "signed" editorial moment per `typography-patterns.md` §5. |
| `none` | No signature. Reserved for editorial registers (typically Quiet Confidence at some build shapes) where a loud signature reads dishonest. |

#### Tier 2 — `microInteractions` array of enum (motion, plural)

Closed set of four values as of Stage II (c). Motion behaviors applied to specific elements or states. Array is required; empty array allowed; no per-persona values enforced in schema.

| Value | Concept |
|---|---|
| `eyebrow-reveal` | Scroll-entry reveal on `.role-data-eyebrow`. |
| `underline-bloom` | Hover behavior on inline links. |
| `mono-numeral-flip` | Viewport-entry reveal on `.role-data-numeral` or watermark. |
| `shimmer-hero-cta` | Shimmer loop on hero primary CTA button. **First-real-build editorial review pending** — "shimmer" reads as SaaS, not editorial; retention decision deferred to observation in a real build. Flag at approval gate when deployed. |

Per-persona defaults for both tiers documented in `emotional-arc.md`. Current `emotional-arc.md` persona-signature column is keyed to Composer's legacy motion-based tree (Tier 2 vocabulary); Stage III rewrites it to reference Tier 1 compositional signatures with a parallel Tier 2 micro-interactions column. Until that rewrite lands, Phase 4 logic supplies per-persona defaults inline; the schema carries the explicit values per build.

**Stage III cascade work** (logged to composer-backlog.md): `emotional-arc.md` persona-signature column rewrite; SKILL.md Phase 4 signature decision tree rewrite (lines 417–427) against compositional vocabulary; `css-framework.md` Motion Restraint review to confirm governs Tier 2 cleanly.

### §2.2 `pathConvention`

| Field | Type | Required | Purpose |
|---|---|---|---|
| `homePath` | const `"/"` | yes | Canonical home path. |
| `aboutPath` | string | yes | Default `"/about/"`. |
| `servicePathPattern` | string | yes | Default `"/services/{service-slug}/"`. Used by Phase 5-new to generate per-service sub-page paths. |
| `contactPath` | string | yes | Default `"/contact/"`. |
| `trailingSlash` | boolean | yes | Site-wide convention. Affects canonical URL emission. |

### §2.3 `colorScheme`

Phase 4 decides how the raw palette from `profile.json.brandPalette` is applied — not how derived tokens are computed (those live in Phase 5 inline per profile-schema scope call #5).

| Field | Type | Required | Purpose |
|---|---|---|---|
| `primaryUsage` | enum | yes | Site-wide primary application intensity. One of `accent-only` · `primary-heavy` · `dual-emphasis`. Affects how densely primary appears in headlines, CTAs, decorative marks. See provenance note + persona default-bias table below. |
| `darkVibrantAsDarkPrimary` | boolean | yes | True when DarkVibrant override applies per brain §6 PA.4 (populated `brandPalette.darkPrimary` taking precedence over derived hover). |
| `heroBackgroundDerivation` | const `"phase-5-inline-from-primary-hue"` | yes | Documentation field naming that hero page background is not a plan-level decision. Present so the schema is explicit about what Phase 4 does NOT decide here. Phase 5 computes from `profile.brandPalette.primary` hue warmth at render. |

**`primaryUsage` provenance note.** Derived from per-persona color-density bias. Not cited to a specific `typography-patterns.md` section — Chat-Claude inference, confirmed at Checkpoint 1 q7.

**Persona default-bias reference table.** Not schema-encoded (Phase 4 decides per build); documented here so Phase 4 has a starting point per persona and so the approval gate can surface deviations.

| Persona | Default `primaryUsage` |
|---|---|
| `quiet-confidence` | `accent-only` |
| `earned-pride` | `dual-emphasis` |
| `neighborhood-steady` | `accent-only` |
| `urgent-service` | `primary-heavy` |
| `modern-specialist` | `accent-only` |

---

## §3 `pages` — array of page entries

`pages` is an array of page objects. Every page the site emits has one entry. No implicit fallbacks — a page missing from this array is not rendered.

**Required pages** (hard-error on absence): `home`, `about`, `contact`.

**Conditionally required**: one page entry per service where that service has `category` in the emission-qualified set (Luna F8 produces service sub-pages for services matching `content-rules.md` criteria). The conditional is declared per-build by Phase 4 based on `profile.services[]` content-match.

Each page entry carries the fields in §4.

---

## §4 Per-page fields

Every page object carries these fields. Sub-sections below document sub-objects.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `pageKey` | enum | yes | `home` · `about` · `contact` · `service` (with `serviceSlug` required for the latter). |
| `serviceSlug` | string | conditional | Required when `pageKey === "service"`. Matches a slug from `profile.services[].slug`. |
| `path` | string | yes | Canonical path per `pathConvention`. |
| `canonicalUrl` | string (URL) | yes | Full canonical URL. Phase 5.5 emits to `<link rel="canonical">`. |
| `headingHierarchy` | object | yes | See §4.1. |
| `sections` | array of section objects | yes | Ordered. Each element is a tagged variant per §5. Phase 5 emits in array order. |
| `voiceZones` | array of zone assignments | yes | See §4.2. One entry per zone present on the page. |
| `photoAssignments` | array | yes | See §4.3. |
| `italicSelections` | array | yes | See §4.4. |
| `pullQuotes` | array (max length enforced) | yes | See §4.5. |
| `eyebrowDeployments` | array | yes | See §4.6. |
| `faq` | array of Q/A pairs | conditional | Required when `pageKey === "home"` or `"service"`. See §4.7. |
| `serviceDescriptions` | array | conditional | Required when `pageKey === "home"` (homepage services section) or `"service"` (the service's own description). See §4.8. |
| `displayMoment` | object | yes | See §4.9. Required on every page per Check 8. |
| `scaleContrast` | object | yes | See §4.10. |
| `voicesInUse` | array of enum | yes | Subset of `["display", "body", "data"]`. Required to include all three per Phase 6 Check 12 (three-voice presence per page). Schema enforces this structurally. Distinct from site-level `voicesInUse` at §2 — page-level enforces Check 12 per page; site-level is a build-wide expectation. |

### §4.1 `headingHierarchy`

Heading hierarchy contract per brain §7 item 2. Preserves SEO/GEO discipline and BLUF DOM-order.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `h1` | string | yes | The page's single H1 content. Exactly one H1 per page is a brain §7 hard rule. |
| `h2Sequence` | array of `{ id: string, text: string, sectionType: enum }` | yes | Ordered H2s. Each carries a stable ID for cross-reference by `italicSelections`, `eyebrowDeployments`, `pullQuotes.placementAfterSectionId`, etc. `sectionType` is one of the §5 section types, used for Phase 6 Check 4 validation (no eyebrow on banned types). |
| `h3Map` | object `{ [h2Id]: array of { id, text } }` | yes | Nested H3s per H2. Empty arrays allowed. |

Invariants (schema-enforced where possible):
- Exactly one `h1`.
- `h2Sequence` must not skip heading levels (no H4 before an H3, enforced structurally because H3s only exist under H2s).
- Each `h2Id` referenced elsewhere must exist in `h2Sequence`.

### §4.2 `voiceZones`

Array of zone assignments. Closed vocabulary per `voiceMap.md` — 15 zones (see §7). Each entry resolves to a single voice after Phase 4 applies persona bias.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `zone` | enum (15 closed values, §7) | yes | Zone machine key. |
| `defaultVoice` | enum (`closing-table` · `saturday-morning` · `front-porch`) | yes | Zone default per `voiceMap.md`. |
| `personaBiasApplied` | boolean | yes | True if persona bias overrode default. |
| `resolvedVoice` | enum (`closing-table` · `saturday-morning` · `front-porch`) | yes | Final voice for this zone on this page. Phase 5 stamps `data-voice="{resolvedVoice}"` on the section's rendered root per Design's `voiceMap.md` §Phase 6. |
| `biasReason` | string | conditional | Required when `personaBiasApplied === true`. |

Invariants:
- A zone may appear at most once per page (no duplicate `zone` keys within a page's `voiceZones` array).
- Conversion-critical zones (per `voiceMap.md` lines 186–196) ignore persona bias: `hero-headline`, `promo-bar`, `service-card-description`, `stats-section`, `faq-answer`, `featured-promotion`. Schema validates that `resolvedVoice === defaultVoice` and `personaBiasApplied === false` for these zones.

### §4.3 `photoAssignments`

Final role-slot photo assignments. Reads eligible candidates from `profile.photoInventory[].eligibleRoles[]` per brain §4 addendum.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `slot` | enum | yes | Editorial slot on the page: `hero-background` · `hero-plate` · `owner-portrait` · `services-grid/{service-slug}` · `about-lead` · `about-team` · `footer-brand` · `gallery-{index}` · etc. Closed enum pending §5 section-type enumeration. |
| `photoInventoryId` | string (profile.photoInventory ID) | conditional | Required when `placeholderFlag === false`. The ID of the photo assigned. |
| `placeholderFlag` | boolean | yes | Per Design Flag 6 at pre-draft. True when Phase 4 took the fallback-path-b (profile did not have a photo eligible for this role; Phase 5 renders a visible placeholder). The approval gate surfaces this flag so Ron can distinguish "Phase 4 chose this photo" from "Phase 4 chose a layout that doesn't need a photo." |
| `placeholderReason` | string | conditional | Required when `placeholderFlag === true`. Human-readable reason (e.g., "no `heroBackground`-eligible photos in inventory"). |
| `cropHint` | object | optional | Phase 5 crop hint (focal point, orientation preference). Optional — Phase 5 computes defaults from `profile.photoInventory` metadata if absent. |

### §4.4 `italicSelections`

One entry per H1 and H2 that carries an italic span. Per-heading, mirroring Design Flag 3's approval-state pattern.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `headingId` | string | yes | References `h1` or an entry in `h2Sequence`. |
| `italicWord` | string | yes | Exact word (or contiguous phrase) in the heading text that Phase 5 wraps in `<em>`. Case-sensitive match against heading text. |
| `personaWordClassAnnotation` | enum | yes | `matches` · `expected-class` · `banned-class-warning`. Check 9 soft-fail on anything but `matches`. Word classes per `emotional-arc.md` per-persona tables (e.g., quiet-confidence → precision verb/adjective). |
| `approvalState` | enum | yes | `proposed` · `confirmed` · `rejected`. Per brain §9 approval gate pattern. Phase 5 only renders `approvalState === "confirmed"` selections. |
| `alternativeWord` | string | optional | If Phase 4 has a second-choice within the same heading, carries it. Surfaces as pick-or-confirm at approval gate per brain §9. |

Invariants:
- At most one `italicSelections` entry per `headingId` (enforces Check 1 structurally — one italic span per H1/H2).
- An H1 or H2 with no entry in `italicSelections` has no italic span.

### §4.5 `pullQuotes`

Pull quote deployments per page. Schema enforces count limits structurally.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `sourceTestimonialId` | string (profile.testimonials ID) | yes | The testimonial this quote draws from. Must reference `profile.testimonials[].id`. |
| `extractedText` | string | yes | The exact extracted quote (8–20 words per Design's detection heuristic §6). Phase 5 renders verbatim. |
| `placementAfterSectionId` | string | yes | References an h2Id from `headingHierarchy.h2Sequence`. Phase 5 places the pull quote between the section ending with this H2 and the next section. |
| `rhetoricalSlot` | string | yes | Which persona word-class claim this quote foregrounds (per Design §6 heuristic rule 3). Enables Phase 6 verification of Design's "no two pull quotes fill the same rhetorical slot" rule. |
| `approvalState` | enum | yes | `proposed` · `confirmed` · `rejected`. Pattern mirrors `italicSelections`. |

Invariants (structural):
- Array max length = 1 when `sections.length <= 6`.
- Array max length = 2 when `sections.length >= 7` (scroll-depth threshold made explicit per Design Checkpoint 1 q5; resolves the previous "scroll-depth >6" prose ambiguity).
- No two entries with identical `rhetoricalSlot` on the same page.

### §4.6 `eyebrowDeployments`

| Field | Type | Required | Purpose |
|---|---|---|---|
| `sectionId` | string | yes | References a `sectionOpener`-type section via its ID. |
| `text` | string | yes | Eyebrow text (ALL CAPS rendering is Phase 5's concern, not stored upper-case here). |
| `register` | enum (`primary` · `mute`) | yes | Per typography-patterns.md §3 — `primary` = loud `--accent` color, `mute` = quiet `--font-data` with tracked caps. |

Invariants (structural):
- Array max length = 3 per page (Check 3 structural enforcement).
- Each `sectionId` must reference a section with `type === "sectionOpener"`. Schema rejects eyebrows attached to service grids, FAQ, contact form per Check 4.

### §4.7 `faq`

Ordered array of Q/A pairs. Phase 5.5 reads this to emit FAQPage JSON-LD per brain §7 item 3 (moves from DOM-read to plan-read, closes schema-HTML drift class of bug).

| Field | Type | Required | Purpose |
|---|---|---|---|
| `id` | string | yes | Stable ID. Used by Phase 5 for H3 anchor IDs. |
| `question` | string | yes | Rendered verbatim as H3 and as `Question.name` in FAQPage JSON-LD. |
| `answer` | string (markdown-flavored) | yes | Rendered verbatim. Phase 5 converts markdown to HTML; Phase 5.5 strips to plain text for `Question.acceptedAnswer.text`. |

Invariants:
- At least 3 entries required on home and service pages (Phase 3.5 alignment).

### §4.8 `serviceDescriptions`

Service descriptions as they appear in the page's rendered copy.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `serviceSlug` | string | yes | Cross-references `profile.services[].slug`. |
| `headline` | string | yes | Section headline (rendered as H3 in homepage services grid; H2 on service sub-page). |
| `description` | string | yes | Copy. Phase 5.5 reads for Service schema `description`. |
| `voiceAssignment` | enum (`closing-table` · `saturday-morning` · `front-porch`) | yes | Resolved voice for this service's copy. Per `voiceMap.md`, service card descriptions are `closing-table` with no persona bias. |

### §4.9 `displayMoment`

Per-page invariant declaration — every page must name which element carries the minimum display-scale moment per typography-patterns.md Check 8 (≥80px desktop, ≥56px mobile).

| Field | Type | Required | Purpose |
|---|---|---|---|
| `elementType` | enum | yes | `h1` · `h2` · `pull-quote` · `watermark-numeral` · `stat-numeral`. Identifies which on-page element carries the moment. |
| `elementId` | string | yes | Stable ID of the element (h1, h2Id, pullQuote index, etc.). |
| `targetDesktopPx` | integer | yes | Phase 4 declares the target size. Phase 5 renders at or above. Phase 6 Check 8 verifies rendered size ≥80. |
| `targetMobilePx` | integer | yes | As above; Check 8 verifies ≥56 rendered. |

Invariants:
- `targetDesktopPx >= 80`.
- `targetMobilePx >= 56`.
- `elementId` must resolve to an emitted element on the page. Phase 6 Check 8 cross-references after render.

### §4.10 `scaleContrast`

Scale contrast targets per typography-patterns.md §7. References role-class assignments, not pixel values.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `minimumRatio` | number | yes | Per-persona minimum contrast between display-voice and body-voice on the page. Persona-conditional from typography-patterns.md §7. Documentation points to authority; schema stores the resolved minimum Phase 4 picked. |
| `achievedRatio` | number | yes | Computed ratio Phase 4 reports given the role-class assignments declared in this page's sections. |
| `achievedBy` | string | yes | Narrative: which elements produce the ratio (e.g., "hero H1 `.role-display-hero` at 72px vs. body `.role-body-paragraph` at 16px = 4.5×"). |

Invariant: `achievedRatio >= minimumRatio`. Schema hard-fails below.

---

## §5 Section variants — tagged section types

Every entry in a page's `sections` array carries a `type` field with one of the values below. Section-specific fields follow the type. No implicit fallback section — a `type` value outside this enum is a schema error.

| `type` value | Appears on | Notes |
|---|---|---|
| `hero` | home (required), about/service (optional) | Page-opening. Hero mode decided from `profile.brandPalette` + `hero-patterns.md` decision tree. |
| `sectionOpener` | any page | **First-class tagged variant per Design Flag 1, role-class framing per Checkpoint 1 q2.** Carries eyebrow + H2 contract via role-class references. A page with no `sectionOpener` sections has no eyebrows. See §5.2. |
| `servicesGrid` | home (required) | Services grid. No eyebrow (Check 4). Photo assignments draw from `evidenceShot`-eligible photos filtered by service content-match (per profile-schema.md §11 prose). |
| `statRow` | home, about | Stats section. Single-value per cell per Design Flag 2 — Check 11 unfalsifiable by construction. See §5.1. |
| `testimonialsSection` | home, service | Testimonials. Avatar-only per Design's testimonial rule (Decision 4 of editorial review). |
| `featuredPullQuote` | any page (subject to §4.5 count limits) | Pull-quote deployment as a standalone section between other sections. Content references the page's `pullQuotes[]` entry. |
| `faqSection` | home, service | FAQ. No eyebrow (Check 4). Content references page's `faq[]` array. |
| `beforeAfter` | home (conditional on photo availability) | Before/after. Photo assignments use `evidenceShot` pairs. |
| `anchorStrip` | any page (at most one per page per `voiceMap.md` §3) | Voice-pivot anchor strip — italic Fraunces pullquote + mono credit between hero and services. |
| `trustSection` | home | Trust marquee. No eyebrow. |
| `contactForm` | contact (required), home (optional) | Contact form. No eyebrow (Check 4). |
| `footerSection` | all pages (required) | Footer. Always last section. Front Porch voice per `voiceMap.md`. |
| `aboutStory` | about | About page narrative body. |

### §5.1 `statRow` contract fields

Per Design Flag 2 — single value per stat cell.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `type` | const `"statRow"` | yes | Type discriminator. |
| `id` | string | yes | Section ID. |
| `stats` | array of `{ id, value, label }` | yes | One object per stat cell. |
| `stats[].value` | string | yes | The stat's value as rendered. Phase 5 renders this string in both the filled numeral position and the watermark position. Check 11 is unfalsifiable by construction — there is no separate watermark field to drift from. |
| `stats[].label` | string | yes | The stat's label copy. |

### §5.2 `sectionOpener` contract fields

Per Design Checkpoint 1 q2 — role-class framing. The four-axis parameterization from Composer's current typography.md §4 (eyebrowSize, headlineScale, italicPlacement, orientation) retires; SectionOpener is a `.role-data-eyebrow` element above a `.role-display-section` element with a proximity contract (≤24px, Check 2) between them.

| Field | Type | Required | Purpose |
|---|---|---|---|
| `type` | const `"sectionOpener"` | yes | Type discriminator. |
| `id` | string | yes | Section ID. Referenced by `eyebrowDeployments[].sectionId`. |
| `h2Id` | string | yes | References the H2 this opener introduces, from `headingHierarchy.h2Sequence`. |
| `eyebrowRoleClass` | const `"role-data-eyebrow"` | yes | Role class for the eyebrow element. Phase 5 emits the element with this class. |
| `h2RoleClass` | const `"role-display-section"` | yes | Role class for the H2 element. Phase 5 emits with this class. |
| `orientation` | enum (`eyebrow-above` · `tag-strip-inline`) | yes | Layout decision — which spatial arrangement the opener uses. Survives the axis retirement because it's a layout call, not a type-axis call. |
| `supportingContent` | object | optional | Optional supporting copy beneath H2 (lede, subhead, etc.). |

**Stage II (d) merge implication.** Composer's current typography.md §4 SectionOpener four-axis framing retires under role-class framing at the three-way merge. This will surface as a real conflict (axis-parameterized primitive vs. role-class assignment). Don't flatten at merge — surface to Design via Chat-Claude per three-way diff procedure. Logged to composer-backlog.md as Stage II (d) item.

### §5.3 Other section types

Stubs deferred per Design Checkpoint 1 q6. Each section type's contract fields to be specified after Checkpoint 1 closes. Priority order for follow-up authoring: hero, servicesGrid, testimonialsSection, aboutStory, remainder in any order. Authority in each case is `section-patterns.md` + `hero-patterns.md` + Design's `typography-patterns.md`. Deferred work logged to composer-backlog.md.

---

## §6 Layout variants — per-section-type allowed values

Per Design Checkpoint 1 q3 — per-section-type enum with allowed values, not a single site-wide enum. Rejects invalid layout × section-type combinations structurally (e.g., Layout D on a services grid is representable-but-nonsensical under a single enum; under per-section allowed values, it's a schema error).

Implementation via JSON Schema `oneOf` discriminated on `sections[].type`, allowed-values per section type:

| Section type | Allowed layouts | Default |
|---|---|---|
| `hero` | `A`, `C`, `D` | `D` (full-bleed) |
| `sectionOpener` | `A`, `C` | — |
| `servicesGrid` | `A`, `B` | — |
| `statRow` | `A`, `E` | `E` (watermark) |
| `testimonialsSection` | `A`, `B` | — |
| `featuredPullQuote` | `C` | `C` |
| `faqSection` | `A` | `A` |
| `beforeAfter` | `B`, `D` | — |
| `anchorStrip` | `C` | `C` |
| `trustSection` | `A` | `A` |
| `contactForm` | `A` | `A` |
| `footerSection` | `A` | `A` |
| `aboutStory` | `A`, `B`, `D` | — |

**Layout descriptions** (authority: Design's `typography-patterns.md` + `emotional-arc.md` per-persona layout bias):

| Layout | Description |
|---|---|
| `A` | Standard section with aligned typography. |
| `B` | Asymmetric composition. |
| `C` | Centered composition. |
| `D` | Full-bleed image with text overlay. |
| `E` | Watermark numeral with caption. |

**Per-page rule carried forward:** brain §4 / SKILL.md Phase 4's "3–5 distinct layouts per page" rule remains verifiable against this tighter per-section enum. The per-section enum narrows options per section; it doesn't change the per-page layout-distinctness requirement. Phase 4 picks 3–5 distinct layouts from {A, B, C, D, E}, assigns each section its layout from the allowed set for that section's type.

---

## §7 Voice zone vocabulary

Closed enum of 15 zones per Design Checkpoint 1 q4. `voiceMap.md`'s zone table groups paired zones for documentation readability (e.g., "Hero headline + subheadline" as one row; "FAQ questions and answers" as one row), but schema splits them because Phase 4 resolves voice per-zone and persona bias operates per-zone. The closed enum mirrors the resolution unit, not the documentation unit.

| Zone machine key | Default voice | Persona bias allowed |
|---|---|---|
| `hero-headline` | closing-table | no (conversion-critical — headline stays closing-table across all personas) |
| `hero-subheadline` | closing-table | yes (neighborhood-steady, urgent-service soften toward saturday-morning for subheadline only) |
| `promo-bar` | closing-table | no (conversion-critical) |
| `trust-marquee` | saturday-morning | yes (modern-specialist → dry closing-table variant) |
| `services-grid-header` | saturday-morning | yes (quiet-confidence → closing-table) |
| `service-card-description` | closing-table | no (conversion-critical) |
| `stats-section` | closing-table | no (conversion-critical) |
| `before-after-header` | closing-table | no |
| `testimonials-header` | saturday-morning | yes (earned-pride → closing-table proof-forward) |
| `featured-promotion` | closing-table | no (conversion-critical) |
| `faq-question` | closing-table | yes (neighborhood-steady opens FAQ section with saturday-morning lead) |
| `faq-answer` | closing-table | no (conversion-critical — answers stay closing-table across all personas) |
| `contact-form-header` | saturday-morning | yes (urgent-service → closing-table response-time claim) |
| `footer-tagline` | front-porch | no |
| `about-page-body` | front-porch | yes (earned-pride → claim-first opening; neighborhood-steady → front-porch heavy) |

**Note on Stage II (d) merge.** `voiceMap.md`'s zone table presentation groups `hero-headline`/`hero-subheadline` into one row and `faq-question`/`faq-answer` into one row for documentation readability. Schema splits both because differential persona-bias behavior lives on the subheadline (not headline) and on the question (not answer). The documentation grouping and schema split coexist — no edit to `voiceMap.md` needed, but the merged `voiceMap.md` reference file should note "Zone table groups paired zones for readability; schema enum splits them; Phase 4 resolves per split zone."

---

## §8 Photo role assignments — integration with profile.photoInventory

Phase 4 consumes `profile.photoInventory[].eligibleRoles[]` (closed enum of 8 roles per profile-schema §11) and produces per-slot assignments here in composition-plan. The eligibility-vs-assignment split means: profile.photoInventory declares what a photo COULD do; composition-plan declares what a photo DOES on this build.

Fallback behavior per brain §4 addendum:
- **Path (a):** Phase 4 selects a layout that doesn't require the missing role. No placeholder. Reflected in the page's `sections` array — the layout-requiring-missing-role section simply doesn't appear.
- **Path (b):** Phase 4 emits a placeholder-flagged assignment. `placeholderFlag === true`, `photoInventoryId` absent, `placeholderReason` required. Approval gate surfaces the flag; Ron sees a visible placeholder; Phase 5 renders a visible placeholder element rather than silently breaking the layout.

Schema rejects any `photoAssignments` entry where `placeholderFlag === false && photoInventoryId` is absent, and rejects any entry where `placeholderFlag === true && photoInventoryId` is present.

---

## §9 Schema versioning

Per brain §14. This file declares `schemaVersion: 1.0` in frontmatter. Every `composition-plan.json` carries `$schemaVersion: "1.0"` at top level.

Phase 5-new hard-errors on schema version mismatch at consumption time (compares `composition-plan.json.$schemaVersion` to this file's frontmatter `schemaVersion`). Phase 5-new also hard-errors if `composition-plan.json.profileSchemaVersion` doesn't match the `profile.json.$schemaVersion` being consumed alongside — catches staleness across regenerations.

Format: `major.minor`. Major increment = breaking change, invalidates prior plans. Minor increment = additive, prior plans remain consumable.

Version registry entry for composition-plan schema: `~/grm-automations/docs/composer/schema-versions.md` (seeded in Stage II (c)).

---

## §10 Phase 6 invariants — schema-enforced vs. post-render check

Summary of which of Design's 13 Phase 6 checks are expressed structurally in this schema vs. left as Phase 6 assertions after render. Classification confirmed at Checkpoint 1 (Design Part B).

| Check | Expressible in schema? | How / why |
|---|---|---|
| 1. Max one italic span per H1/H2 | Yes (structural) | `italicSelections` allows at most one entry per `headingId`. |
| 2. Eyebrow proximity ≤24px to H2 | No | CSS rendering concern. Phase 6 DOM check. |
| 3. Eyebrow count per page ≤3 | Yes (structural) | `eyebrowDeployments` array max length = 3. |
| 4. No eyebrow on banned section types | Yes (structural) | `eyebrowDeployments[].sectionId` must reference a section where `type === "sectionOpener"`. |
| 5. Service card numerals tabular-nums | No | CSS rendering. Phase 6 computed-style check. |
| 6. No `.role-body-*` computes to `--font-display` | No | CSS rendering. Phase 6 computed-style check. |
| 7. No `.role-data-*` computes to >40px | No | CSS rendering. Phase 6 computed-style check. |
| 8. Display moment per page (≥80px/≥56px) | Partially (structural + render) | `displayMoment` required per page in schema; `targetDesktopPx >= 80` schema invariant. Phase 6 verifies rendered size. |
| 9. Italic word vs. persona word-class | Soft (structural + human-auth) | `personaWordClassAnnotation` field forces Phase 4 to annotate. Human review at approval gate is authoritative. Soft classification confirmed at Checkpoint 1 q5 — ambiguous word-class cases are where editorial judgment earns its keep. |
| 10. Pull-quote deployment count | Yes (structural) | `pullQuotes` max length enforced: 1 when `sections.length <= 6`, 2 when `sections.length >= 7`. Threshold made explicit per Checkpoint 1 q5. **Implementation note for Code:** structural encoding via JSON Schema `if/then` on `sections.length` if validator supports; otherwise prose assertion + Phase 6 backup is acceptable. Code's call based on validator stack. |
| 11. Stats watermark consistency | Yes (unfalsifiable by construction) | `statRow.stats[].value` is single field — no separate watermark to drift. |
| 12. Three-voice presence per page | Yes (structural) | Per-page `voicesInUse` must include all three of `["display", "body", "data"]`. Distinct from site-level `voicesInUse` at §2. |
| 13. Mobile watermark treatment | No | CSS rendering. Phase 6 computed-style check. |

Structural (unfalsifiable): **1, 3, 4, 10, 11, 12.**
Partial (schema + Phase 6): **8, 9.**
Phase 6 only (rendered): **2, 5, 6, 7, 13.**

---

## §11 Migration from Luna F8

Fields in Luna F8's `profile.json.design.*` block and how they migrate to composition-plan.json:

| Luna F8 field | Destination | Notes |
|---|---|---|
| `design.persona` | `persona` | Same machine key enum. |
| `design.personaReason` | `personaReason` | |
| `design.heroMode` / `design.heroModeReason` | inside `sections[hero].mode` (per §5 hero contract — deferred) | Phase 4 decision preserved, routed to the hero section entry. |
| `design.heroGlassVariant` / `design.heroGlassVariantReason` | inside `sections[hero].glassVariant` (per §5 hero contract — deferred) | |
| `design.videoAugmentation` / `design.videoAugmentationReason` | inside `sections[hero].videoAugmentation` | |
| `design.signatureMicroInteraction` / `design.signatureReason` | `signatureMicroInteraction` (site-level) / `signatureMicroInteractionReason` | |
| `design.editorialLayouts` / `design.editorialLayoutsReason` | distributed across `pages[].sections[].layoutVariant` | Per-section rather than site-level. Page-level summary derivable. |
| `design.fullBleedPhoto` | `sections[...].photoAssignments` entry | Where applicable. |
| `design.watermarkTarget` | `sections[statRow].id` and/or `displayMoment.elementId` | Resolves depending on which use. |
| `design.constraintsOK` | site-level `constraintsOK: boolean` | New site-level field for approval-gate visibility. |
| `design.constraintRelaxations` | site-level `constraintRelaxations: []` | As today. |
| `designScore` | site-level `designScore: { categories, total, tier }` | As today. |

A Composer-era `composition-plan.json` will not look like Luna F8's `profile.design.*` block — it's restructured into per-page and per-section placement. Migration notes in this section document the shape change for future readers.

---

## §12 Deferred item carried forward

All eight Checkpoint 1 open questions resolved. One Stage II (d) merge flag carried forward for composer-backlog.md:

**Stage II (d) SectionOpener role-class framing conflict.** Per Checkpoint 1 q2 resolution, SectionOpener retires from axis-parameterized primitive (Composer's current typography.md §4) to role-class assignment (Design's typography-patterns.md framing). This will surface as a real three-way merge conflict at Stage II (d). Design's explicit instruction: don't flatten at merge — surface to Design via Chat-Claude per voiceMap.md README §"If you hit a merge conflict." Logged to composer-backlog.md as Active item.

---

## §13 Status and review history

- **Author:** Chat-Claude (Stage II (c) Phase 2 Chat-drafted tier per handoff plan).
- **Status:** Checkpoint 1 reviewed + q1 follow-up resolved, pending revision commit. Design conditional pass with eight answered questions plus two-tier architecture resolution on signatureMicroInteraction framework mismatch; revisions folded into this file.
- **Review history:**
  - Draft skeleton authored (v1) → forwarded to Design for Checkpoint 1.
  - Design Checkpoint 1 review received: seven pre-draft flags verified landed; §10 invariants classification confirmed; eight open questions answered; conditional pass.
  - Revisions folded into v2: §2.1 signatureMicroInteraction enum, §2.3 primaryUsage rename + persona default-bias table, §4.5 pull-quote threshold explicit, §5.2 role-class framing, §6 per-section allowed-values map, §7 zone count 15 with splits, §10 Check 10 validator note, §12 reduced to single carried item.
  - Code verification at commit time surfaced framework-level mismatch on signatureMicroInteraction (Composer's Phase 4 tree uses five motion-based values; Design's six are compositional). Different categories of thing, not naming substitution.
  - Design q1 follow-up resolution: two-tier architecture. Tier 1 signature (compositional, singular) = Design's six. Tier 2 microInteractions (motion, plural) = Composer's four relocated (shimmer-hero-cta pending first-real-build review). Cascade work (emotional-arc.md, SKILL.md Phase 4 tree, css-framework.md Motion Restraint) deferred to Stage III when Phase 4-new is authored. Path 1 architecturally via Path 3 commit mechanism.
  - Revisions folded into v3 (current): §2.1 rewrite with two-tier architecture, site-level fields table adds `microInteractions` + `microInteractionsReason`, §12 unchanged (q1 follow-up resolved, no carried item), §13 updated.
- **Next step:** Code under full authorship to commit this file as `references/composition-plan-schema.md`. Five backlog additions required at commit (one from Checkpoint 1 base review, four from q1 follow-up).

**Locked scope decisions carried into this revision** (no relitigation expected):
1. SectionOpener as first-class tagged section variant (Design Flag 1).
2. StatRow single-value per cell making Check 11 unfalsifiable (Design Flag 2).
3. Pull-quote deployments with approvalState mirroring italic-word pattern (Design Flag 3).
4. Scale contrast via role-class references, not pixel values (Design Flag 4).
5. Voice-zone closed enum of 15 values (Design Flag 5 + Checkpoint 1 q4 resolution).
6. placeholderFlag on fallback-path-b photo assignments (Design Flag 6).
7. Five-persona enum matching emotional-arc.md machine keys (profile-schema alignment).
8. `$schemaVersion` + `$schema` required envelope (brain §14).
9. Phase 4 `design.*` fields migrate here from profile.json per profile-schema scope call #1.
10. Photo assignments consume `profile.photoInventory[].eligibleRoles[]` per profile-schema §11.
11. SectionOpener role-class framing per Checkpoint 1 q2.
12. Per-section-type layout enum per Checkpoint 1 q3.
13. Pull-quote threshold structural at `sections.length >= 7` per Checkpoint 1 q5.
14. Check 9 soft classification with human override at approval gate per Checkpoint 1 q5.
15. `primaryUsage` enum `accent-only | primary-heavy | dual-emphasis` per Checkpoint 1 q7.
16. Per-zone stylistic directives NOT schema fields — Phase 5 latitude per Checkpoint 1 q8.
17. Two-tier signature architecture (Tier 1 compositional singular + Tier 2 motion plural) per Checkpoint 1 q1 follow-up resolution. Schema fields: `signatureMicroInteraction` enum (6 compositional values), `microInteractions` array of enum (4 motion values, shimmer-hero-cta under first-real-build review), `microInteractionsReason` conditional narrative.

---

*End of schema (Checkpoint 1 revised).*

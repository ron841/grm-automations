# Typography Patterns Reference

Part of the prospect-site skill v0.7.2. Loaded by Phase 4 at design approval (for persona → font-family selection), by Phase 5 at section generation (for role-class assignment, italic deployment, and pull-quote detection), and by Phase 6 at verification (for the type-system checks listed at the bottom of this file). This is the authority for how type is used on contractor preview sites — three voices, role classes, persona-conditional font selection, Phase 5 generation rules, Phase 6 verification.

---

## The load-bearing principle

**Variety across prospects comes from persona variety, not font-selection randomness.** Two prospects with the same persona should get the same font pairing by default. That is what makes the persona system legible. If future maintainers are ever tempted to add a "mix it up" knob to font selection, that sentence is the answer for why not.

The entire type system in this file is deterministic. Given a persona and a tier, the font selection is reproducible across builds. Overrides are explicit and traceable — either `CONFIG.fonts` names a specific family, or the tier gate unlocks paid families, or a named conflict pair triggers a walk-to-second-candidate. No hidden randomness, no timestamp-based selection, no aesthetic-variance knob. Variety comes from the five personas producing five different type voices, not from shuffling within a persona.

This principle governs every decision below. Read it once now and let it shape how you interpret the rest of the file.

---

## The three-voice type system

Three type voices exist on a contractor preview site. Each voice has one dedicated CSS custom property, one set of semantic role classes, and one font-family slot in the persona × voice matrix.

### Voice 1: Display (`--font-display`)

**What it is.** The editorial voice. Large headlines, pull quotes, watermark numerals, feature-well treatments. The voice the reader's eye lands on first and remembers last.

**When it leads.** H1 and H2 elements always. Pull quotes. Watermark numerals in stats sections. Large standalone numerals (pricing callouts, hero stats). Editorial captions on full-bleed imagery when the caption carries weight (not the sidebar captions on supporting photos).

**Weight and scale.** Typically 500-700 weight for headlines, 400-500 for pull quotes, 300-400 outlined for watermark numerals. Display sizes range 40-180px depending on role.

**Why it's called display, not heading.** A watermark numeral at 160px is not a heading — no H-tag wraps it, it doesn't outline the document, and it doesn't participate in the page's heading hierarchy. It is a *display-scale* typographic moment. The token name `--font-display` captures this; `--font-heading` would not.

### Voice 2: Body (`--font-body`)

**What it is.** The reading voice. Paragraphs, UI labels, nav links, form labels, section H3/H4/H5, card body copy, service descriptions, FAQ questions and answers, most caption text.

**When it leads.** Any sustained reading surface. Anything below H2 in the heading hierarchy. All UI chrome. Anything a reader scans rather than reads.

**Weight and scale.** 400 regular for body, 500-600 for emphasis, 600-700 for H3/H4. Body sizes range 14-20px depending on role; lede-paragraph treatment (see Role classes below) goes to 18-22px.

**Why it's called body, not text or sans.** "Body" names the role — the text the reader's body of attention lives in. "Text" is ambiguous (all type is text), "sans" is a category not a role, and "font-body" aligns symmetrically with `--font-display` and `--font-data`.

### Voice 3: Data (`--font-data`)

**What it is.** The metadata voice. Phone numbers, addresses, hours, license numbers, service-area enumeration, timestamps, metric callouts that need to read as information rather than language. Anything the reader treats as lookup rather than prose.

**When it leads.** Phone numbers and email addresses in nav and footer. Stats section captions ("AVERAGE GOOGLE RATING", "FIVE-STAR REVIEWS"). Eyebrow labels above H2s. License numbers. Service-area lists. Small caps tracked labels on editorial photo captions. Metadata blocks in the About page (founded year, headquarters location, service area). Form field labels in small tracked-caps treatment.

**Weight and scale.** 500-600 weight, often with `letter-spacing: 0.08em` or wider. Sizes range 10-14px. Occasionally 24-32px for larger metadata callouts. Never larger than 40px — data voice at display scale reads as computer-generated and breaks the editorial register.

**Why it's called data, not mono or metadata.** "Mono" is a category (monospace) not a role, and the data voice does not have to be monospace — a well-chosen geometric sans at small tracked-caps reads as data too. "Metadata" is accurate but long. "Data" names the role crisply and leaves the specific family choice (mono or geometric-sans-at-tracked-caps) to the persona tables below.

### How the three voices compose

A well-composed page uses all three voices in visible rotation. A page that uses only display and body reads like an overdecorated blog post. A page that uses only body and data reads like a UI with no voice. A page that uses all three reads editorial — display carries the rhetorical moments, body carries the reading experience, data carries the metadata and structural labels.

The composition rule: **every major section should contain at least two of the three voices, and most pages should contain all three voices at least once.** This is enforced in Phase 6 (see verification checks at bottom).

---

## Role classes

Each role class names a specific purpose on the page and maps to one of the three voices with a defined size, weight, tracking, and leading. Phase 5 uses role classes rather than raw CSS properties so voice assignment is consistent across pages and Phase 6 can verify it.

### Display-voice role classes

- `.role-display-hero` — H1 in the hero glass card. 48-72px depending on viewport. 600 weight. Line-height 1.05. `font-family: var(--font-display)`. Letter-spacing -0.01em.
- `.role-display-section` — H2 in any non-hero section. 36-56px depending on viewport. 600 weight. Line-height 1.1. `font-family: var(--font-display)`. Letter-spacing -0.01em.
- `.role-display-watermark` — Outlined numeral behind a filled stat. 120-180px depending on viewport. 300 weight, outlined via `-webkit-text-stroke` or SVG. `font-family: var(--font-display)`. Letter-spacing 0. **See Stats watermark rule below — this class specifically addresses the Luna v4 numbering bug.**
- `.role-display-pullquote` — Extracted testimonial or editorial quote set as a standalone typographic moment between sections. 28-40px italic. 400 weight. `font-family: var(--font-display)`. Always italic.
- `.role-display-lede` — First paragraph of a major editorial section (not hero, not cards). Larger than body paragraphs to introduce the section's reading rhythm. 20-24px. 400 weight. Line-height 1.5. `font-family: var(--font-display)` in non-italic regular. This is a transitional role — it's display-family but at reading-sized text.

### Body-voice role classes

- `.role-body-paragraph` — Standard paragraph copy. 16-18px. 400 weight. Line-height 1.6. `font-family: var(--font-body)`. Max line length 70 characters.
- `.role-body-emphasis` — Bold or medium-weight emphasis within paragraphs. 16-18px. 600 weight. `font-family: var(--font-body)`.
- `.role-body-h3` — Section subheadings below H2. 22-28px. 600 weight. Line-height 1.2. `font-family: var(--font-body)`.
- `.role-body-h4` — Tertiary headings (card titles, FAQ question text). 18-22px. 600 weight. `font-family: var(--font-body)`.
- `.role-body-ui` — Button labels, nav links, form labels when not tracked-caps. 14-16px. 500-600 weight. `font-family: var(--font-body)`.
- `.role-body-caption` — Small caption text under images (not editorial captions, which use `.role-data-caption`). 14px. 400 weight. `font-family: var(--font-body)`.

### Data-voice role classes

- `.role-data-eyebrow` — ALL CAPS label above an H2. 11-13px. 600 weight. Letter-spacing 0.12em. `font-family: var(--font-data)`. Only deployed on sections that genuinely introduce a new information mode (see Phase 5 eyebrow rule).
- `.role-data-caption` — Small caps tracked-caps editorial caption on a full-bleed photo. 11px. 500 weight. Letter-spacing 0.1em. `font-family: var(--font-data)`. Multi-line captions use `.role-body-caption` stacked below the data-caption title.
- `.role-data-stat-caption` — Caption under a stat number in the stats section. 11-13px. 600 weight. Letter-spacing 0.08em. UPPERCASE. `font-family: var(--font-data)`.
- `.role-data-metadata` — Phone number, address, hours, license number in nav and footer. 14-16px. 500 weight. Slight tracking, 0.02em. `font-family: var(--font-data)`. Tabular numerals (`font-variant-numeric: tabular-nums`) required.
- `.role-data-service-area` — Service-area town names in the contact section sidebar. 13-15px. 500 weight. 0.04em tracking. `font-family: var(--font-data)`.
- `.role-data-numeral` — Standalone filled stat numeral in the stats section (the "56" that sits in front of the watermark "56"). 56-72px. 700 weight. Tabular numerals. `font-family: var(--font-data)` OR `--font-display` depending on persona (see persona table).

### Italic signature role class

- `.role-italic-signature` — The italicized color-shifted word in an H1 or H2. Inherits size from its parent role class. Italic weight. Color shifted to `--brand-accent`. Deployed once per H1/H2, according to Phase 5 italic deployment rule. Not a voice of its own; a micro-treatment applied within an existing display role.

---

## Pull-quote detection heuristic

Phase 2 captures testimonials and customer quotes during prospect crawl. Most testimonials are set as uniform cards in the testimonials grid. One or two per page earn pull-quote treatment: extracted from the grid and set as a standalone editorial moment using `.role-display-pullquote`.

Phase 5 identifies pull-quote candidates during testimonials section generation using the following heuristic.

### Heuristic rules

A testimonial earns pull-quote treatment if **two or more** of the following are true:

1. **Quote length is 8-20 words.** Long enough to land rhetorically, short enough to set at 28-40px without wrapping more than twice. Quotes under 8 words are too slight; quotes over 20 words are too long for display treatment and stay in the card grid.
2. **Quote contains a specific named noun.** "Armando and his father," "the family team," "the 56 reviews." Generic quotes ("great service," "highly recommend") never earn pull-quote treatment regardless of length.
3. **Quote contains a claim the page's persona most wants to foreground.** Neighborhood steady wants family or generational claims. Earned pride wants review-count or longevity claims. Quiet confidence wants precision or correctness claims. Rescue-ready wants speed or response-time claims. Modern specialist wants technical-depth or specific-method claims.
4. **Quote is first-person and reads aloud naturally.** "I knew we were in good hands" reads well as a pull quote. "They did the thing and it was good" does not.
5. **No other quote on the page already fills the same rhetorical slot.** If two quotes both foreground "family team," only one gets pull-quote treatment; the other stays in the grid.

### Deployment rule

At most one pull quote per page on standard builds. Two pull quotes per page allowed only when the page is long (scroll depth >6 sections) and the two quotes serve different rhetorical slots. Never three or more — past two, pull quotes stop reading as editorial moments and start reading as hype decoration.

Pull quotes are placed **between sections**, not within the testimonials grid. A pull quote lives in the editorial gap between services and testimonials, or between testimonials and the promo callout, as a typographic bridge that makes the page read as designed rather than templated.

### Example (Luna v4 analysis)

Mikala Posley's testimonial — "From day one of meeting Armando and his father I knew we were in good hands. This family team pays extreme attention to details" — is pull-quote-eligible on Luna because: (a) extracting "knew we were in good hands. This family team pays extreme attention to details" hits the 8-20 word window, (b) contains "family team" which is Neighborhood steady's foregrounded claim, (c) reads aloud naturally, (d) no other quote on Luna's page fills the same rhetorical slot. Phase 5 should extract this quote between the services section and the stats section, set it in `.role-display-pullquote`, and leave the full quote in the grid for readers who want the complete testimonial.

---

## Persona-conditional font selection

Each of the five personas biases the selection of font families for display, body, and data voices. The tables below specify ordered candidate lists. Phase 4 picks the first available candidate, subject to the selection logic in `css-framework.md` (tier gate, CONFIG.fonts override, conflict-pair walk).

Licensing flags: **GF** = Google Fonts (free, CDN-available, build-time usable). **paid** = requires commercial license (not eligible on professional tier, eligible on premium tier and above).

### Persona 1: Quiet confidence

Character: precise, undemonstrative, evidence-first. The page feels like a well-kept workbench.

| Voice | Candidate 1 | Candidate 2 | Candidate 3 |
|---|---|---|---|
| Display | Source Serif 4 (GF) | Fraunces (GF) | Tiempos Text (paid) |
| Body | Inter (GF) | Source Sans 3 (GF) | Söhne (paid) |
| Data | IBM Plex Mono (GF) | JetBrains Mono (GF) | Söhne Mono (paid) |

**Why.** Transitional serif for display carries the "seasoned, precise" register without editorial flamboyance. Neo-grotesque sans for body is quiet and unassertive. Geometric mono for data reads as documentation rather than marketing. The persona's page should feel like a well-maintained service manual, not a brochure.

### Persona 2: Earned pride

Character: accomplished, evidence-first, lineage-aware. The page feels like a company portrait with the plaques visible.

| Voice | Candidate 1 | Candidate 2 | Candidate 3 |
|---|---|---|---|
| Display | Fraunces (GF) | Playfair Display (GF) | GT Super (paid) |
| Body | Inter (GF) | Work Sans (GF) | Söhne (paid) |
| Data | IBM Plex Mono (GF) | Space Mono (GF) | Söhne Mono (paid) |

**Why.** Display serif with more character than Quiet confidence — Fraunces or Playfair carry the "we have earned this" register without being showy. Body sans stays neutral so the display does the emotional work. Data voice stays similar to Quiet confidence because metadata is metadata regardless of persona.

### Persona 3: Neighborhood steady

Character: warm, civic, family-rooted. The page feels like a letter from a neighbor who happens to be a craftsman.

| Voice | Candidate 1 | Candidate 2 | Candidate 3 |
|---|---|---|---|
| Display | Fraunces (GF) | Recoleta (paid) | DM Serif Display (GF) |
| Body | Inter (GF) | Nunito (GF) | Söhne (paid) |
| Data | Space Grotesk at tracked-caps (GF) | IBM Plex Mono (GF) | JetBrains Mono (GF) |

**Why.** Fraunces brings warmth through its soft-terminaled serif; Recoleta (paid) does the same thing harder if the tier allows. Body sans skews slightly rounder (Nunito as alternative) for family-business warmth. Data voice can skip mono entirely and use tracked-caps Space Grotesk — this persona's metadata reads as neighborhood directory rather than technical documentation. **This is the persona Luna currently runs.**

### Persona 4: Rescue-ready

Character: urgent, response-oriented, can-do. The page feels like the phone is already ringing.

| Voice | Candidate 1 | Candidate 2 | Candidate 3 |
|---|---|---|---|
| Display | Archivo (GF) | Barlow Condensed (GF) | Tobias (paid) |
| Body | Inter (GF) | Archivo (GF) | Söhne (paid) |
| Data | JetBrains Mono (GF) | IBM Plex Mono (GF) | Söhne Mono (paid) |

**Why.** Condensed sans display carries the urgency without shouting. Body sans can be the same family (Archivo) for structural economy — this persona rewards system-building over decorative layering. Data voice is mono-forward because response-time metadata ("30 min response," "same-day service") reads more credibly in mono than in tracked-caps.

### Persona 5: Modern specialist

Character: technical, confident, method-forward. The page feels like a specialist's practice — specific, narrow, deep.

| Voice | Candidate 1 | Candidate 2 | Candidate 3 |
|---|---|---|---|
| Display | Inter Tight (GF) | Söhne (paid) | Neue Haas Grotesk (paid) |
| Body | Inter (GF) | Söhne (paid) | Neue Haas Grotesk (paid) |
| Data | JetBrains Mono (GF) | IBM Plex Mono (GF) | Söhne Mono (paid) |

**Why.** This is the one persona that does not use a serif for display. Modern specialist reads more credibly in a tight neo-grotesque — Inter Tight as the free candidate, Söhne or Neue Haas as the paid walk-ups. The display-body pairing is deliberately close (both sans, both neo-grotesque family) to produce a technical, restrained feeling. Data voice is mono for the same reason as Rescue-ready: technical metadata reads credibly in mono.

---

## Named conflict pairs

When Phase 4's default candidate selection produces a display-body pairing with a known aesthetic or metric conflict, Phase 4 walks to the second candidate in whichever list has more alternatives. The conflict pairs below are enumerated so future maintainers can add or remove conflicts as a named list rather than rewriting the selection logic.

### Conflict pair 1: Fraunces display vs. Fraunces body

**Voice slot A's candidate:** Fraunces (display).
**Voice slot B's candidate:** Fraunces (body — not in current tables but possible via CONFIG.fonts override).
**Why they conflict:** Using the same family for display and body collapses the display-body contrast to a weight-and-size difference only. Works for some editorial brands but defeats the three-voice type system.
**Which voice walks to #2:** Body walks to Inter. Display stays Fraunces.

### Conflict pair 2: Playfair Display vs. Nunito

**Voice slot A's candidate:** Playfair Display (display, Earned pride).
**Voice slot B's candidate:** Nunito (body, Neighborhood steady alternative).
**Why they conflict:** Playfair's high-contrast Didone forms against Nunito's soft-terminaled humanist body reads as mismatched — one is formal-editorial, the other is warm-rounded. Happens only when Neighborhood steady's body candidate gets overridden by CONFIG.fonts to a persona that prefers Playfair-class display.
**Which voice walks to #2:** Body walks to Inter. Display stays Playfair.

### Conflict pair 3: Archivo display vs. Archivo body

**Voice slot A's candidate:** Archivo (display, Rescue-ready).
**Voice slot B's candidate:** Archivo (body, Rescue-ready alternative).
**Why they conflict:** Same-family display and body is normally the conflict, but Rescue-ready specifically *wants* this — its persona rewards structural economy. This is the one conflict pair that is **allowed** when both slots are Archivo, to the exception above. Phase 4 does not walk.
**Which voice walks to #2:** Neither. This pair is allowed.

### Conflict pair 4: Inter Tight display vs. Inter body

**Voice slot A's candidate:** Inter Tight (display, Modern specialist).
**Voice slot B's candidate:** Inter (body, Modern specialist).
**Why they conflict:** Same superfamily, different optical size. Normally a conflict; for Modern specialist it's the intent. Phase 4 does not walk.
**Which voice walks to #2:** Neither. This pair is allowed.

### Conflict pair 5: Two transitional serifs in display and data

**Voice slot A's candidate:** Source Serif 4 (display, Quiet confidence).
**Voice slot B's candidate:** Any transitional serif assigned to data via CONFIG.fonts override.
**Why they conflict:** Data voice must read as lookup, not as prose. A transitional serif in data voice collapses the reading/lookup distinction and the page loses its information hierarchy.
**Which voice walks to #2:** Data walks to its mono candidate. Display stays the transitional serif.

If a future conflict is observed in a build, add it as Conflict pair 6 following the same format.

---

## Phase 5 generation rules

### Rule 1: Italic signature deployment

Every page whose persona is Quiet confidence, Earned pride, or Modern specialist must deploy the italic-color-shift signature micro-interaction **exactly three times** within the main content column, distributed as: once in the hero H1, once in a section H2 in the upper-middle of the page, and once in a section H2 in the lower half. For Neighborhood steady and Rescue-ready, the minimum is **two deployments** — hero and one additional section H2.

### Rule 2: Italic word selection heuristic

**Italicize the word the persona most wants the reader to hear.** Not any word in the headline. Not a random adjective. The word that carries the sentence's emotional weight for the selected persona.

- Quiet confidence: precision words. "Done *right*." "Wired *to code*." "Built *correctly*." Never emotional words.
- Earned pride: claim words. "*56* five-star reviews." "*Three* generations." "*Fifty* years." Prefer numerals or longevity words.
- Neighborhood steady: identity words. "One *family team*." "Our *neighbors*." "*Leesburg* painters." Prefer noun phrases that name relationships or place.
- Rescue-ready: speed words. "*Same-day* quotes." "*30-minute* response." "Call *now*." Prefer urgency or temporal words.
- Modern specialist: method words. "*Infrared* diagnosis." "*Spray-finished* cabinets." "*Laser-leveled* installation." Prefer technical-method words that claim specialization.

**Banned italic selections** (apply across all personas):

- The business name if it already appears emphasized elsewhere on the page
- Generic adjectives ("great," "excellent," "quality")
- Imperative verbs in contact/CTA zones ("Tell us," "Call today") — those read as pull quotes, not signatures
- Price numerals in italic — reads as pull quote, not signature
- The word "not" when it's doing rhetorical negation work (keep "not" in roman; italicize the word *after* it that carries the redefined meaning)

**Phase 6 verification of italic word selection** is soft — automated check cannot reliably judge whether "family team" is the right word for Neighborhood steady vs. some other word. The check confirms one italic span exists per H1 and H2 at the specified distribution; human review during Phase 4 design approval confirms word selection is correct.

### Rule 3: Eyebrow deployment

Eyebrow labels (`.role-data-eyebrow`) are used to mark editorial transitions, not to decorate every section. Deploy on **at most 3 sections per page**, and only on sections that:

1. Introduce a new information mode (narrative → data, services → testimonials, marketing → contact), OR
2. Anchor a location claim (e.g., "LEESBURG · CENTRAL FLORIDA" on hero)

**Service grids, FAQ sections, and contact forms do not take eyebrows.** Testimonials and stats sections may take eyebrows; if both appear on the same page, only one gets one. The hero location-claim eyebrow always counts against the budget.

### Rule 4: Stats watermark numbering

**The outlined watermark numeral and the filled numeral in a stats section must be the same number.** Not the display-order index ("01, 02, 03"). Not the section number. The stat's actual value.

If the stat is "56 five-star reviews," the watermark is "56" at 140-180px outlined and the filled numeral is "56" at 56-72px. Stacked or offset-overlapping, both rendering the same value.

This rule specifically addresses the Luna v4 bug where the stats section rendered "04, 02, 03, 04" (display-order indices) behind "4.9★, 56, 18, 2" (actual values). The outlined-watermark-of-index treatment is a valid editorial pattern in magazine feature-well design but wrong for stats — the reader's eye goes to the large number first and finds a meaningless index, then to the small number and finds the real value, then has to mentally discard the first read.

**Implementation.** Phase 5 writes the stats section with `.role-display-watermark` containing the stat value and `.role-data-numeral` containing the same stat value, stacked or offset-overlapping via CSS positioning. Both display the same value string.

### Rule 5: Pull-quote deployment

Apply the Pull-quote detection heuristic (above). At most one pull quote per standard page; at most two on scroll-depth >6 pages when serving different rhetorical slots.

Pull quotes live between sections, not inside testimonials grids. Set in `.role-display-pullquote`.

### Rule 6: Lede paragraph deployment

The first paragraph of the hero subhead, the first paragraph of the prep/process editorial section, and the first paragraph of the contact section get `.role-display-lede` treatment — 20-24px, display-family regular weight, line-height 1.5 — instead of standard `.role-body-paragraph` treatment.

This is a small composition move with big rhythm effect. Without lede treatment, every paragraph on the page reads at the same size and weight and the page flattens. With lede treatment, the opening paragraph of each major section has a visible "breath" before the body copy begins.

**Not every section gets a lede.** Service cards do not have ledes. FAQ answers do not have ledes. The lede is reserved for sections where the reader is entering a new reading surface and needs a transition into the body.

### Rule 7: Minimum display-scale moment per page

Every page must contain at least one `.role-display-*` element with computed font-size ≥80px on desktop, ≥56px on mobile. If the page has no H1 (rare — only on some service sub-pages) and no stats watermark, Phase 5 must add a display-scale moment (typically a pull quote or a large callout numeral) to satisfy this minimum.

Rationale: the display moment is what separates an editorial page from a template. Without one, the page reads as "nice design," not "someone designed this."

### Rule 8: Mobile watermark breakpoint

On viewports ≤480px, `.role-display-watermark` either (a) shrinks to 80-100px and sits behind the filled numeral with reduced opacity, (b) moves to a corner of the stat cell and reduces to 56-72px, or (c) is dropped entirely in favor of the filled numeral at full size.

The Luna v4 build showed watermark-and-filled-numeral overlapping illegibly on mobile because the desktop treatment (watermark sitting behind-and-slightly-offset) doesn't have room to breathe at 375px viewport. Phase 5 writes a mobile-specific CSS block for watermark treatment, selected per-persona:

- Quiet confidence, Modern specialist: use (a) — reduced opacity, shrunken, stays behind.
- Neighborhood steady, Earned pride: use (b) — moves to corner, reduced size, treated as editorial chapter-number rather than watermark.
- Rescue-ready: use (c) — dropped entirely. Rescue-ready rewards speed over editorial; the mobile page should not spend vertical space on decorative watermarks.

### Rule 9: Voice-role compatibility

- Body copy never uses `--font-display`. Never. Including "elegant body" variants. The one exception is `.role-display-lede`, which uses `--font-display` at reading sizes for the specific rhythmic purpose named above.
- Data voice never appears in H1 or H2. Data is metadata; headings are language. If a page seems to need a "data heading" (e.g., "56 FIVE-STAR REVIEWS" as a section header), use `.role-display-section` with `.role-data-eyebrow` above it instead.
- Display voice never appears at sizes below 20px unless it's the italic-signature span nested inside a display-role element.

---

## Phase 6 verification checks

Phase 6 verifies typography compliance before ship. Implementation details live in Phase 6's spec; the checks below are what Phase 6 asserts.

### Check 1: Max one italic span per H1/H2

Every H1 and H2 on every page contains at most one italic span. Hard fail on two or more — that means Phase 5 deployed the italic-signature micro-interaction incorrectly.

### Check 2: Eyebrow proximity to H2

Every `.role-data-eyebrow` element sits within 24px (vertical margin) of its paired H2. Hard fail on >24px — that means the eyebrow got decoupled from its H2 and reads as a floating label.

### Check 3: Eyebrow count per page

Per-page count of `.role-data-eyebrow` elements is ≤3. Soft fail (warning) on 4+ — the page is shippable but eyebrow-heavy.

### Check 4: No eyebrow on banned sections

No `.role-data-eyebrow` element sits above an H2 inside a service grid, FAQ section, or contact form. Soft fail.

### Check 5: Service card numeral format

All numerals inside service cards use `font-variant-numeric: tabular-nums`. Hard fail — tabular numerals are required for numeric grids so columns align.

### Check 6: Body copy font-family check

No element with `.role-body-*` class computes to a font-family that resolves to `var(--font-display)` or its downstream family. Hard fail on any match — that means a body element got display font applied.

### Check 7: Data voice scale check

No element with `.role-data-*` class computes to `font-size > 40px`. Hard fail — data voice above 40px reads as display and breaks the three-voice system.

### Check 8: Minimum display-scale moment per page

Every page has at least one element with computed `font-size ≥80px` on desktop viewport (1440) and `≥56px` on mobile viewport (375). Hard fail on missing.

### Check 9: Italic word selection (soft)

For each italic span inside an H1 or H2, the italicized word is flagged against the persona's approved word-class list (precision / claim / identity / speed / method). Soft fail with a warning listing the italicized word and the expected word class. Human review during Phase 4 or Phase 7 confirms.

### Check 10: Pull-quote deployment count

Per-page count of `.role-display-pullquote` elements is ≤1 on scroll-depth ≤6, ≤2 on scroll-depth >6. Hard fail on higher counts.

### Check 11: Stats watermark-numeral consistency

For each stats cell, the text content of `.role-display-watermark` equals the text content of `.role-data-numeral` within the same cell. Hard fail on mismatch. **This directly addresses Luna v4's 01/02/03/04 bug.**

### Check 12: Three-voice presence per page

Every page contains at least one `.role-display-*`, at least one `.role-body-*`, and at least one `.role-data-*` element. Hard fail on missing — a page using only two voices is incomplete.

### Check 13: Mobile watermark treatment

On viewport 375, `.role-display-watermark` elements either (a) compute to `font-size ≤100px`, (b) compute to `display: none`, or (c) sit at `position: absolute` with offsets indicating corner placement. Hard fail on watermarks that render at desktop size on mobile.

---

## Cross-references

- `voiceMap.md` — the three *copy* voices (Closing Table / Saturday Morning / Front Porch) that this file's three *type* voices render. Voice map picks the words; typography patterns pick the fonts, weights, sizes, and rhythm.
- `emotional-arc.md` — the five personas that bias both voice selection and font selection. The persona-conditional font tables in this file depend on the personas defined there.
- `css-framework.md` — font-loading strategy, CSS custom property declarations for `--font-display` / `--font-body` / `--font-data`, tier-gate logic, and Phase 4 font-selection algorithm that reads this file's candidate tables.
- `section-patterns.md` — the specific section layouts that use these role classes. Includes the stats section spec that must be updated to enforce the watermark-numeral-consistency rule (Rule 4 and Check 11 above).
- `content-rules.md` — pattern templates (headlines, CTAs, service descriptions) produced in the voices defined in `voiceMap.md` and set in the type system defined here.
- `SKILL.md` Phase 4 — design approval workflow that selects persona and font families.
- `SKILL.md` Phase 5 — section generation workflow that deploys role classes, italic signatures, eyebrows, pull quotes, and ledes according to the rules above.
- `SKILL.md` Phase 6 — verification workflow that runs the 13 checks above.

---

## Version

v0.7.2. First version of this file. Replaces inline type-token placeholder references (`--font-heading` / `--font-body`) in `css-framework.md` with the three-token system (`--font-display` / `--font-body` / `--font-data`). Extracts voice-related concerns into `voiceMap.md`; pattern templates and universal rules remain in `content-rules.md`.

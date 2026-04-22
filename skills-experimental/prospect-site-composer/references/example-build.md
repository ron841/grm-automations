# Example Build: Annotated Reference Page

**Status note (2026-04-22).** This worked example predates Composer's Stage II restructure from tier-keyed to persona-conditional architecture. It accurately documents pre-Composer-era skill behavior; the underlying architecture has since shifted — font selection is now persona-conditional per `typography.md §11` and `CONFIG.fonts`; spacing is now persona-base × tier-multiplier per `css-framework.md CONFIG.spacing`; the `.tier-premium` / `.tier-professional` / `.tier-standard` CSS class cascade has retired (replaced by `class="persona-{kebab-key}"` as a dev-tools identifier). A Composer-era reference build through the restructured phases is logged to `composer-backlog.md` for authoring post-Stage-II. Treat this example as documenting prior state, not current state, when the file's illustrative content conflicts with current authority in `typography.md`, `voiceMap.md`, `css-framework.md`, or `anti-slop-rules.md`.

Part of the prospect-site-composer skill. Loaded by Phase 5 at the start of site generation as a pattern-match reference. Every section of this document is a worked example of a homepage section, annotated with which rules it satisfies and why it is composed the way it is. When Phase 5 is deciding how to render a section, pattern-match against the relevant example here before falling back to the literal rule text in `section-patterns.md` or `hero-patterns.md`.

The LLM generating against this skill is better at composing-from-example than at composing-from-rules. This file is the example.

The reference business is a synthetic but realistic composite: **Tucci Electric**, a residential and commercial electrician in Dunnellon FL, owner Ben Tucci, licensed EC13012345, 18 years in business, 147 Google reviews at 4.9 stars, strong photo library including owner work-in-progress shots and before/after panel upgrades. Scored 72/100 (Premium tier). All facts in this example are illustrative — the rules this example demonstrates are real.

---

## Design plan (output of Phase 4 for this reference build)

```
Tier: Premium (72/100)
Hero mode: glass-crossfade (6 hero-candidate landscape photos, 1600px+)
Glass card variant: wide (Premium tier)
Video augmentation: no
Brand colors: primary #C23616 (brick red from logo), accent #2C3A4B (slate)
Typography: Fraunces Display / Inter Body (banned fonts avoided per anti-slop-rules.md)
Signature micro-interaction: italic-color-shift (Premium + serif-display pairing)
Editorial layouts (page): A (FAQ offset), C (contact 70/30), E (stats watermark)
Full-bleed photo: none (no secondary hero plate qualifying; Layout D omitted this build)
Watermark numeral target: stats
```

This design plan is the output of Phase 4 for the reference build. Every section below implements a piece of this plan.

---

## Section 1: Sticky nav

**Role in rule system.** Standard pattern from `section-patterns.md`. Not an editorial layout — navigation is always centered-symmetric because readers expect it there. The nav is where the site earns the right to be editorial elsewhere.

**Composition.**

- Left: Tucci Electric wordmark in `--font-display` at 20px, italic on the E in "Electric" (the site-wide italic signature appears here in the brand lockup as a static preview of what users will see throughout).
- Center: five links — Services, About, Reviews, FAQ, Contact. 15px `--font-body`, tracked 0.02em, all-caps optional at Premium tier. Active state: 2px underline in `--color-primary`.
- Right: click-to-call block with (352) 555-0142 in tabular-lining mono, prefixed by a small phone glyph inheriting `currentColor` (not accent — see Rule E1). Phone is the only element in the nav that is a call-to-action and it is styled as a hyperlink with underline-on-hover, not as a button.

**Anti-slop rules satisfied.**

- Rule E1 (single accent discipline): accent color appears only on the active-page underline and on the italic "E" of "Electric," nowhere else in the nav.
- No hamburger menu at desktop widths — horizontal links with full labels. Hamburger appears only at < 900px.
- Phone number is a real captured number, never a (555) placeholder (anti-slop banned-placeholder list).

---

## Section 2: Hero (glass-crossfade mode, wide variant)

**Role in rule system.** Hero is governed by `hero-patterns.md`, not by the editorial layouts module. Full spec in that file; this example focuses on how the hero composes with the rest of the page.

**Composition.**

- Background: six hero-candidate photos crossfading at 7s per photo, 1s dissolve. All six are role-tagged `heroPlate` by Phase 3. Two are Ben at a panel, two are completed panel installations with the cover off (evidence of work), two are the service truck in a Dunnellon driveway.
- Overlay: linear-gradient(180deg, rgba(0,0,0,0.15) 0%, rgba(0,0,0,0.55) 100%) for legibility.
- Glass card (wide variant): centered, 880px max-width, `backdrop-filter: blur(24px) saturate(1.2)`.
  - Eyebrow: `DUNNELLON FL · LICENSED EC13012345` in `--font-data`, 12px, uppercase, tracked 0.08em, `--color-primary`.
  - Headline: "Residential and commercial electric, done *right* the first time." Set in `--font-display` at 64px (Premium wide variant default). The word "right" is italicized in `--color-primary`. This is the site-wide signature micro-interaction.
  - Subhead: "Ben Tucci has run panel upgrades, service calls, and new-construction rough-ins across Marion County for 18 years." 18px `--font-body`, `--color-text`, max-width 60ch.
  - CTAs: "Get a free quote" (primary, `--color-primary` background, shimmer-loop banned here because signature is italic-color-shift not shimmer) and "Call (352) 555-0142" (secondary, ghost button with 1px `--color-primary` border).
- Eyebrow entry animation: 400ms fade-up, 400ms after page load. This is the entry choreography; the rest of the hero is static.

**Rules satisfied.**

- Hard rule 4 (one hero structural pattern, data-driven mode).
- Scale contrast rule (css-framework.md): 64px headline, 12px eyebrow. Ratio 5.3x — passes the ≥5 threshold.
- Motion restraint: exactly one signature micro-interaction (italic-color-shift on the word "right") and one entry animation (eyebrow fade-up). No scroll-reveal, no hover bounces, no card tilts.
- Image-handling.md role rules: the six crossfade photos are all `heroPlate` role. No `detailShot` or `evidenceShot` in the crossfade — those photos belong in later sections.

---

## Section 3: Trust marquee

**Role in rule system.** `section-patterns.md` standard. Not an editorial layout (centered-stacked is correct here). Thin strip, `--space-section-compact` (60px) padding.

**Composition.**

- Background: `--color-background-alt` (off-white, not accent — Rule E1).
- Content: horizontally-scrolling marquee, 30s loop, `linear` easing (permitted for ambient loops).
- Badges: "EC13012345 · Florida DBPR," "18 years in business," "4.9 ★ Google (147 reviews)," "BBB A+ rated," "Licensed, bonded, insured." Each badge is text-only, `--font-data` 14px, separated by thin vertical hairlines (`--rule-hairline`).
- No logos, no SVG icons, no badge illustrations. Text + rules read as editorial documentation; logo salad reads as template.

**Rules satisfied.**

- Rule E2 (rules, not boxes): badges separated by hairlines, not wrapped in rounded pill cards.
- Anti-slop: every credential in the marquee is a real captured fact from `profile.json.credentials`. Never fabricated.

---

## Section 4: Services grid (Bento asymmetric)

**Role in rule system.** `section-patterns.md` Bento. Already asymmetric by construction (featured 2x2 + standard cards), so this section does NOT need to apply an editorial layout from the module — the Bento IS the editorial choice.

**Composition.**

- Section header: centered-stacked. Eyebrow "WHAT WE DO" in mono 12px accent; h2 "Electric work for the Nature Coast" in 48px display with "Nature Coast" italicized in `--color-primary` (second instance of the signature, in a headline rather than a CTA context).
- Grid: 4-column at desktop, 2-column at tablet, 1-column at mobile.
  - Featured card (2x2): "Panel upgrades and service rewiring." Photo: evidence shot of a completed panel, captioned `BROWNFIELD ACRES, CITRUS COUNTY / MARCH 2026` in mono 12px.
  - Standard card 1: "New-construction rough-in." Icon-only (no photo) because no evidence shot qualifies and a stock photo is banned.
  - Standard card 2: "Commercial tenant build-outs." Evidence shot of a commercial panel, captioned with location.
  - Standard card 3: "Generator and EV charger installs." Icon-only.
- Card composition: 4:3 photo top, 1px `--color-border` hairline, then eyebrow (service category) in mono 11px accent, h3 in display 22px, one-line body in `--font-body` 16px, `→` link-arrow on hover (transform: translateX(2px), 150ms ease-out, within motion restraint rules).

**Rules satisfied.**

- Image-handling.md one-hero-weight rule: only the featured card is hero-weight within this section. The three standard cards are evidence-weight or icon-only.
- Rule E3 (captions on photos): both evidence shots have mono captions naming the location.
- Rule E1: accent color appears in eyebrow labels and italic headline word, nowhere else in the grid. Card borders are `--color-border` hairlines, not accent.

---

## Section 5: Stats section (the mandatory dark section, Layout E watermark)

**Role in rule system.** `section-patterns.md` mandatory dark section + Layout E (watermark numerals) from the editorial layouts module.

**Composition.**

- Background: `--color-dark-primary` (deep slate, a darker tone of the secondary brand color). Full-bleed section, `--space-section` padding.
- Layout: 4-column grid on desktop, 2x2 on tablet, stacked on mobile.
- Each of the 4 cells contains:
  - An outlined watermark numeral in the top-left — 01, 02, 03, 04. `color: transparent; -webkit-text-stroke: 2px var(--color-border-dark)` at 160px in `--font-display` with lining-nums. This is the Layout E signature.
  - Stat value below the numeral: "18" / "147" / "4.9" / "100%" in display 72px, white, tabular-lining numerals.
  - Stat label: "Years in business" / "Google reviews" / "Average star rating" / "Licensed and insured." Mono 13px, uppercase, tracked 0.08em, `--color-text-muted-on-dark`.
  - Hairline rule between cells: vertical 1px `rgba(255,255,255,0.1)` on desktop, horizontal at tablet.

**Rules satisfied.**

- Rule E4 (outlined watermark numerals): numbered sequence uses outlined stroke-only numerals, not filled circles.
- Rule E2 (rules, not boxes): cells separated by hairline rules, not card wrappers.
- Scale contrast: 160px outlined numeral, 72px stat value, 13px mono label. Display-to-caption ratio is 12x — strong intentional contrast.
- Rule E5 (no middle-weight display): stat values are 72px (display-weight), labels are 13px (caption-weight), no 24px "medium" fillers.

---

## Section 6: Before/after gallery

**Role in rule system.** `section-patterns.md` standard gallery frame. Card treatment permitted here (per Rule E2 exceptions).

**Composition.**

- Three before/after pairs, each a horizontal-drag slider (CSS-only, no JS animation library).
- Each pair captioned below the slider in mono: `PANEL UPGRADE · OCALA, FL · FEB 2026`, `SERVICE ENTRANCE REBUILD · DUNNELLON, FL · JAN 2026`, `COMMERCIAL LIGHTING RETROFIT · CITRUS SPRINGS, FL · DEC 2025`.
- Each caption includes the specific fact the photos prove (location + project type + date).

**Rules satisfied.**

- Rule E3 (captions required): every photo captioned with project type, location, date.
- Motion restraint: drag slider is user-initiated, not passive animation.
- Image-handling.md: all six photos (three pairs) are role-tagged `evidenceShot`, never hero plate, never stock.

---

## Section 7: Testimonials (centered card grid)

**Role in rule system.** `section-patterns.md` testimonials, card-grid variant (not the editorial Layout A variant — this build uses Layout A on FAQ instead, and Rule 2 of the editorial layouts module caps repeats).

**Composition.**

- Section header: centered. Eyebrow "FROM CUSTOMERS" mono accent; h2 "147 five-star reviews and counting." Italic on "five-star" is banned here (signature already deployed twice — hero, services h2; a third deployment would over-use the signature).
- 3-column grid of testimonial cards. Each card: quote body in `--font-body` 17px, reviewer first name + last initial + location + date in mono 12px, 5-star row (SVG stars inheriting `currentColor` at `--color-dark-primary`, NOT accent — Rule E1).
- No reviewer photos. Google profile avatars banned because they look templated; first-name + location + date reads as more specific documentation.
- Hairline rule above the reviewer attribution inside each card (Rule E2 hybrid — cards are permitted here but the internal separator is still a rule, not a divider with accent color).

**Rules satisfied.**

- Rule E1 (accent discipline): stars are `--color-dark-primary`, not accent. Only the eyebrow uses accent in this section.
- Anti-slop: every testimonial is a real captured testimonial from `profile.json.testimonials`, never fabricated.

---

## Section 8: FAQ (Layout A — offset headline, editorial)

**Role in rule system.** Editorial Layout A from the editorial layouts module in `section-patterns.md`. This is the first of three editorial layouts on the page.

**Composition.**

- 12-column grid.
- Left block (columns 2-6): section headline "Questions we hear from Marion County homeowners." Italic on "Marion County" in `--color-primary` (third and final signature deployment on the page — italic color-shift). h2 at 44px `--font-display`.
- Right block (columns 7-12): 8 FAQ rows. Each row is a question in `--font-display` 22px, an answer in `--font-body` 17px below (initially collapsed to 2 lines with fade-out mask), and a `+` toggle that expands the answer via max-height transition (the permitted exception to the layout-animation ban, per motion restraint rules).
- Between rows: `--rule-hairline` separator. No card wrappers. No alternating backgrounds.
- Column 1 is deliberately empty. Negative space is the composition.

**Rules satisfied.**

- Editorial Layout A applied.
- Rule E2 (rules, not boxes): FAQ rows separated by hairlines, not card-wrapped.
- Motion restraint: FAQ expand uses `max-height` with ease-out 200ms (the one permitted layout-property transition).
- Scale contrast inside the section: 44px headline, 12px eyebrow-equivalent (the +/- toggle label). Contrast clears threshold.

---

## Section 9: Featured promotion callout (Layout C — 70/30 split)

**Role in rule system.** Editorial Layout C from the module. Second editorial layout on the page.

**Composition.**

- 12-column grid.
- Primary block (columns 1-8): "Service call special — $89 diagnostic, waived if we do the repair." h2 in `--font-display` 36px, body in `--font-body` 17px, CTA button "Book now" at 18px with shimmer-loop banned (signature micro-interaction budget already spent on italic-color-shift).
- Secondary block (columns 10-12): sidebar fact list in mono 13px uppercase, tracked 0.08em. Three facts: "VALID THROUGH APR 30 2026," "MARION COUNTY SERVICE AREA," "LICENSED EC13012345." Each preceded by a `→` glyph inheriting currentColor. Separated by 8px gaps, no rules needed (list is short enough).
- Column 9 is empty gutter.

**Rules satisfied.**

- Editorial Layout C applied.
- Rule E1: accent color appears only on the h2 and the CTA background. Sidebar is dark-primary and body-muted, not accent.
- Anti-slop: the $89 diagnostic is a real promotion captured in `profile.json.promotion`, not invented.

---

## Section 10: Contact form (standard centered-stacked — intentionally non-editorial)

**Role in rule system.** `section-patterns.md` contact form. The three-layouts-per-page minimum is already met (Bento services, stats watermark, FAQ offset, promo 70/30 — that's four editorial compositions). Contact form reverts to centered-stacked because over-using editorial layouts flattens their effect. Rule 1 of the module specifies *at least* three, not exactly three; Rule 2 caps repeats; both are honored.

**Composition.**

- Section header centered. h2 "Get a free quote" 48px display; subhead "Most quotes returned within 2 hours during business hours."
- Form: 2-column grid on desktop (first name / last name, phone / email, service type / ZIP), then a full-width message textarea, then a full-width submit button.
- Field labels in mono 12px uppercase, tracked 0.08em, ABOVE the input (not inside as placeholder — placeholder-only labels fail accessibility and the anti-slop rules in content-rules.md).
- Input borders: 1px `--color-border`. Focus state: 2px `--color-primary` border — the one place in the form where accent appears (Rule E1 exception for focus states).

**Rules satisfied.**

- Rule E1: accent on focus ring only, not on labels, not on the submit button background (which is `--color-dark-primary`, a deliberate choice to make the form feel more documentary and less marketing-CTA).
- Accessibility: labels are persistent, not placeholder-only.

---

## Section 11: Footer

**Role in rule system.** `section-patterns.md` footer. Not an editorial layout (footer is always centered-columnar).

**Composition.**

- Background: `--color-dark-primary`.
- 4-column grid on desktop: (1) brand block with wordmark + one-line tagline + one environmental portrait of Ben captioned `BEN TUCCI · OWNER · DUNNELLON FL`, (2) services list, (3) service areas list, (4) contact block with phone + email + hours.
- Hairline rule above the footer (1px rgba(255,255,255,0.1)).
- Between footer columns: no rules (negative space is sufficient at desktop; mobile stacks with hairlines between sections).
- Bottom bar: copyright year (auto-current), license number, "Licensed, bonded, insured." No GRM attribution, no "site by" credit (anti-slop hard rule).

**Rules satisfied.**

- Rule E3 (every photograph captioned): environmental portrait has name + role + location caption.
- Image-handling.md: environmental portrait in the footer is Phase 3 role-tagged `environmentalPortrait`, not evidence, not stock.
- Anti-slop: no em dashes (hard rule 10) — the word "bonded" is separated from its peers by commas.

---

## Page-level composition checks (Phase 6 verification dry-run)

After all 11 sections are generated, Phase 6 runs these checks against the full page. The reference build passes all of them:

| Check | Reference build result |
|---|---|
| At least one display moment ≥80px on the page | Pass — hero headline at 64px (wide variant in Premium tier clears threshold via 80px at desktop) + stats watermark numerals at 160px |
| At least one caption moment ≤14px in mono | Pass — marquee badges at 14px mono, stat labels at 13px mono, form labels at 12px mono, photo captions at 12px mono |
| Scale contrast ratio ≥ 5x | Pass — max 160px (watermark numeral) / min 11px (standard card eyebrow) = 14.5x |
| At least 3 editorial layouts on the page | Pass — Layout A (FAQ), Layout C (promo), Layout E (stats) |
| No layout repeats more than twice | Pass — each of A, C, E used exactly once |
| Layout D (full-bleed) used at most once | Pass — not used this build (no qualifying secondary hero plate) |
| Exactly one signature micro-interaction, used site-wide | Pass — italic color-shift used on hero headline word, services h2 word, and FAQ headline word (3 uses of one signature, not 3 different signatures) |
| Accent color appearances ≤12 per page | Pass — counted 9 (nav active underline, hero eyebrow, hero headline italic, hero primary CTA, services eyebrow, services h2 italic, promo h2, promo CTA, FAQ headline italic) |
| Every non-hero photo has a caption | Pass — all evidence shots in services + before/after + footer portrait captioned |
| One hero-weight photo per section | Pass — services grid has one featured (hero-weight), others evidence or icon-only; before/after has three pairs of equal-weight evidence (correct for this section); testimonials have no photos |
| No em dashes | Pass — grep returns zero in both UTF-8 and HTML-entity encodings |
| All credentials cross-check against profile.json | Pass — EC13012345 verified, 18 years verified, 147 reviews verified |

---

---

# Sub-page example A: About page (Tucci Electric)

Sub-pages compose differently from homepages. The arc compresses (4-6 sections instead of 11), the Layout D economics shift (the photo budget is separate, so full-bleed is often more available than on the homepage), and one persona tends to dominate the page more heavily than on the homepage where the persona has to modulate across a longer arc.

The About page for Tucci Electric runs the same persona as the homepage (Quiet confidence) but carries it differently. Where the homepage showed evidence of the craft, the About page shows evidence of the person. The photography budget shifts: environmental portraits (which were secondary on the homepage) become primary here, and the persona's italic signature treatment appears on locality rather than on precision.

## About page design plan (Phase 4 output)

```
Page type: About sub-page
Persona: quiet-confidence (inherited from homepage persona)
Editorial layouts (page): A (offset headline), D (full-bleed, if qualifying photo exists), E (watermark milestones)
Full-bleed photo: tucci-vincent-ben-panel-job-2019.jpg (role: environmentalPortrait, secondary hero plate)
Watermark numeral target: milestones (founding year, years in business, generations)
Signature micro-interaction: italic-color-shift (inherited)
Hero mode: sub-page hero (simplified — single photo + glass card, no crossfade)
```

## Section A1: Sub-page hero (simplified)

**Role in rule system.** Sub-page heroes do not use the homepage's crossfade or parallax modes. The sub-page hero is one photo + one glass card + one headline + one sub-headline. Smaller scale than the homepage hero — 60vh minimum height instead of 100vh, glass card default variant regardless of tier.

**Composition.**

- Background: single environmental portrait of Ben Tucci at a panel in a Dunnellon home. Role-tagged `heroPlate` at Phase 3. Subtle darken overlay (rgba(0,0,0,0.45) flat, no gradient — the About page hero is more documentary than the homepage's gradient-overlay drama).
- Glass card: default variant, 640px max-width, left-aligned (not centered — About page hero is off-axis to signal it is not the homepage).
  - Eyebrow: `ABOUT TUCCI ELECTRIC` in mono 12px accent.
  - Headline: "Eighteen years of residential and commercial electric on the Nature Coast." 48px display. Italic on *Nature Coast* (Quiet confidence persona, italic word carries locality on the About page rather than precision — the persona modulates by section type).
  - Subhead: "Ben Tucci founded the company in Dunnellon in 2008 after nine years running commercial jobs for a Gainesville contractor. He answers the phone." 17px body.
- No CTAs on the sub-page hero. About pages are read, not actioned. The phone number lives in the nav; the About page hero does not compete with it.

**Rules satisfied.**

- Persona-conditional close inversion: the About page hero's italic signature word shifts to locality (*Nature Coast*) because on the About page the reader's question is "who and where" rather than "what and how well." Quiet confidence carries through but modulates.
- Motion: eyebrow fade-up only, same as homepage hero. The signature micro-interaction budget is page-level, not site-level — it can appear in the same places as the homepage (3 times maximum on the About page as well).
- Scale contrast: 48px headline + 12px eyebrow = 4x ratio. Below the 5x threshold. About page must compensate by including a display moment ≥80px elsewhere on the page — which it does in the milestones section (Layout E watermark numerals at 160px). See A3.

## Section A2: Offset-headline story (Layout A)

**Role in rule system.** Editorial Layout A from the module. First and primary editorial composition on the About page.

**Composition.**

- 12-column grid.
- Left block (columns 2-6): section headline "We wire the buildings we grew up around." Italic on *grew up around* (second signature deployment on the About page, italic word carrying biographical specificity). 36px display.
- Right block (columns 7-12): the story. Four short paragraphs, 17px body, max-width 60ch. Content:
  - Paragraph 1: Ben's background. Nine years with a Gainesville commercial contractor, 2008 founding, Dunnellon as home base.
  - Paragraph 2: What the business does now. Residential + commercial, Marion and Citrus and west Levy counties, one truck plus a service van, no subcontractors.
  - Paragraph 3: A specific project story. One paragraph describing a specific panel upgrade or commercial build-out that illustrates the standard of work. Real details: building type, scope, outcome.
  - Paragraph 4: One sentence on how to reach Ben. The About page closes its own narrative loop before the page does.
- Column 1 empty. Negative space.

**Rules satisfied.**

- Layout A applied.
- Persona (Quiet confidence): short declarative sentences, specific facts, one italic signature word, no self-praise. Paragraph 3 is the specific project story that Quiet confidence benefits from — the specificity is doing the work the persona asks for.
- Rule E3: no photos in this section, so no caption requirement fires.
- One signature micro-interaction, used correctly: italic-color-shift appears in the hero headline + this section's headline + one more section's headline (see A5). Three deployments across the About page, same cadence as homepage.

## Section A3: Milestones (Layout E watermark)

**Role in rule system.** Editorial Layout E from the module. Second editorial composition on the About page. Carries the page's ≥80px display moment.

**Composition.**

- Section header: centered-stacked. Eyebrow "MILESTONES" mono accent; h2 "The dates that matter." 36px display.
- 4-column grid at desktop, 2x2 at tablet, stacked at mobile.
- Four milestone cells. Each cell has the same structure as the homepage stats but with biographical content:
  - Cell 1: Watermark numeral `1999` outlined (stroke 2px `--color-border`, 160px display). Below it: "First day on a commercial panel job." Mono 13px caption.
  - Cell 2: Watermark `2008`. "Tucci Electric founded in Dunnellon."
  - Cell 3: Watermark `2014`. "First commercial tenant build-out at Ocala Commons."
  - Cell 4: Watermark `2024`. "Second truck added; Ben's nephew joins as apprentice."
- Hairline rules between cells (vertical on desktop, horizontal at tablet), same as homepage stats.
- Background: `--color-background-alt` (off-white strip, not dark). About page milestones do not use the dark-section treatment — the documentary persona benefits from staying in the light-background vocabulary.

**Rules satisfied.**

- Rule E4: outlined watermark years with `@supports` fallback (color: --color-border, then transparent when stroke is supported). Years used as numerical labels — this is the legitimate Layout E application on the About page.
- Scale contrast: 160px watermark years, 36px h2, 13px mono captions. Ratio 12x. Page clears the threshold on this section alone.
- Rule E2: cells separated by hairlines, not cards.

## Section A4: Full-bleed photo break (Layout D)

**Role in rule system.** Editorial Layout D from the module. Third editorial composition on the About page. Appears on the About page because the photo economics are different from the homepage — Tucci has a strong environmental portrait of Ben + his father Vincent working together on a 2019 service call that qualifies as a secondary hero plate and was not used on the homepage.

**Composition.**

- Full-bleed photograph, 100vw, 70vh minimum.
- Photograph: Ben and Vincent Tucci at a residential panel, 2019. Both visible, both actively working. Neither posed. Role-tagged `environmentalPortrait` but qualifies as `heroPlate` for Layout D purposes because resolution and composition clear the heroPlate thresholds.
- Overlay: `linear-gradient(180deg, rgba(0,0,0,0.25) 0%, rgba(0,0,0,0.65) 100%)` for legibility.
- Caption block: positioned in columns 2-7 of the grid overlay, bottom-aligned 80px from footer of the section.
  - Pull quote in display serif 36px, white: "My dad still shows up on panel jobs when we need a second pair of eyes."
  - Attribution in mono 12px, white at 80% opacity: `— BEN TUCCI / OWNER / DUNNELLON FL`
- No other content on this section. The photo + quote is the whole composition.

**Rules satisfied.**

- Layout D applied. One full-bleed per page, this is the one.
- Rule E3 (caption): the pull quote + attribution IS the caption, in the editorial-variant form. This is how captions scale when the photo is the entire section.
- Persona (Quiet confidence): the quote is a specific biographical fact, the attribution is mono-precise, the tone is calm. Persona carries through even at peak visual moments.
- One hero-weight photo per section: satisfied trivially — the section is one photo.
- Page-arc note: Layout D lands at approximately 65% through the About page (after the hero, the story, and the milestones). This is the emotional peak of the About page and the natural inflection into the close.

## Section A5: Service areas and philosophy (Layout A variant)

**Role in rule system.** Second application of Layout A on this page. Rule 2 of the editorial layouts module allows a layout to repeat up to twice; this is the second (and final) Layout A deployment.

**Composition.**

- 12-column grid.
- Left block (columns 2-5): section headline "Where we work, and how." 32px display. Italic on *how* (third signature deployment, the italic closes the page's italic-word cadence — locality in hero, biographical in story, method here).
- Right block (columns 6-12): two sub-blocks stacked.
  - Sub-block 1: "Service areas." Marion County, Citrus County, west Levy County, portions of northern Lake County. Set as a list with hairline rules between entries. Mono 13px.
  - Sub-block 2: "How we work." 4-6 sentences describing the philosophy: no subcontractors, every job quoted in person, licensed journeyman on every service call, 18 years of repeat customers. 17px body.

**Rules satisfied.**

- Layout A (second and final deployment on the About page).
- Rule E2: service areas list uses hairline rules, not card wrappers.
- Persona: "how we work" is the Quiet confidence persona's value statement — specific refusals ("no subcontractors"), specific requirements ("licensed journeyman on every service call"), no aspirational language.

## Section A6: Contact invitation (centered-stacked, persona-conditional close)

**Role in rule system.** About page close. Quiet confidence persona's close feeling is "quiet invitation — if you want to talk, we're here." The close composition reflects that.

**Composition.**

- Section header centered. h2 "Get in touch." 36px display, no italic signature (signature budget exhausted).
- Below the h2: a short paragraph. Two sentences. "Ben answers the phone weekdays between 7am and 6pm. If he's on a ladder, you'll get Rachel in the office and a callback inside the hour." 17px body, centered, max-width 60ch.
- Below the paragraph: phone number in display 48px, tabular-lining mono numerals, with tel: anchor. `(352) 555-0142`. Centered.
- Below the phone: one line of mono 12px caption: `OR EMAIL BEN DIRECTLY AT BEN@TUCCIELECTRIC.COM`.
- No form. No CTA button. The close is the phone number and the implicit permission to call.

**Rules satisfied.**

- Persona close pattern (Quiet confidence): "phone number is the primary CTA, no fake urgency." Delivered.
- Anti-slop: phone number is a real captured number, not (555) placeholder. Email is a real captured email.

## About page composition check (Phase 6 dry-run)

| Check | About page result |
|---|---|
| At least one ≥80px element | Pass — milestone watermark years at 160px |
| At least one ≤14px mono element | Pass — eyebrow, milestone captions, service area list, close caption |
| Scale contrast ratio ≥5x | Pass — 160px / 12px = 13.3x |
| At least 3 editorial layouts | Pass — Layout A (twice), Layout D (once), Layout E (once). 3 distinct. |
| No layout repeats more than twice | Pass — A used twice, D once, E once |
| Layout D at most once per page | Pass — used once |
| Persona carried through six load-bearing decisions | Pass — hero italic on locality, offset-headline italic on biographical specificity, milestone content biographical not craft, Layout D quote biographical not technical, service-areas list form (not cards), close is phone-primary no form |
| One signature micro-interaction, used site-wide | Pass — italic-color-shift three times, same signature as homepage |
| Accent color appearances ≤12 | Pass — counted 6 (nav active, hero eyebrow, hero italic, milestones eyebrow, service areas h2 italic, philosophy italic) |
| Every non-hero photo captioned | Pass — Layout D has pull-quote + attribution; no other photos |

---

# Sub-page example B: Service sub-page (Panel Upgrades)

Service sub-pages have the tightest arc of any page type — 4 to 5 sections, a specific conversion goal (book this service), and a tighter scope (one trade capability rather than the full services grid). The persona modulates most visibly here because the page is short enough that every decision matters.

The Panel Upgrades service sub-page for Tucci Electric retains Quiet confidence but compresses the arc. The page proves competence in this one capability, answers the specific objections prospects have about panel work, and invites the booking call. It does not retell the business's story — that's what the About page is for.

## Service sub-page design plan (Phase 4 output)

```
Page type: service sub-page
Service: Panel upgrades and service rewiring
Persona: quiet-confidence (inherited from homepage; service sub-pages inherit unless overridden)
Editorial layouts (page): A (offset headline for FAQ), C (70/30 split for process), B (image-bleed for evidence divider)
Full-bleed photo: none (Layout D omitted — sub-page hero already uses a hero plate; a second full-bleed would over-weight the page)
Watermark numeral target: process (3-step)
Signature micro-interaction: italic-color-shift (inherited)
Hero mode: sub-page hero (single photo + glass card, smaller scale)
```

## Section B1: Sub-page hero

**Composition.**

- Background: single evidence shot of a completed residential panel upgrade (cover off, clean wiring visible). Role-tagged `evidenceShot` but clears the heroPlate resolution threshold so it can carry a sub-page hero.
- Overlay: `linear-gradient(180deg, rgba(0,0,0,0.2) 0%, rgba(0,0,0,0.6) 100%)`.
- Glass card: default variant, 640px max-width, left-aligned.
  - Eyebrow: `SERVICE · PANEL UPGRADES` mono 12px accent.
  - Headline: "Panel upgrades and service rewiring, permitted and inspected." 36px display. Italic on *permitted and inspected* (Quiet confidence persona — italic carries the proof, not the promise).
  - Subhead: "Residential 100A to 200A upgrades. Commercial service entrance rebuilds. Every job pulled, inspected, and signed off by the county." 17px body.
  - Primary CTA: "Book a site evaluation" — button in `--color-primary` background at 18px. Leads to contact form with service pre-filled.
  - Secondary CTA: "Call (352) 555-0142" — ghost button with `--color-primary` border.

**Rules satisfied.**

- Service sub-page CTA convention: "Book a [specific action for this service]" as primary, call as secondary. More specific than the homepage's "Get a free quote" because the reader is already service-qualified.
- Persona: italic on proof language ("permitted and inspected") — Quiet confidence persona privileges evidence over selling.
- Scale contrast: 36px + 12px = 3x. Below threshold. Compensation comes in Section B3 (process watermark at 160px). Service sub-page hero is intentionally smaller than homepage hero, so the display-moment budget shifts to a later section.

## Section B2: Process (Layout C 70/30 split)

**Role in rule system.** Editorial Layout C from the module. First and primary editorial composition on the service sub-page.

**Composition.**

- 12-column grid.
- Primary block (columns 1-8):
  - Eyebrow "HOW A PANEL UPGRADE WORKS" mono accent.
  - h2 "Most upgrades done in one day, one permit, one inspection." 32px display. Italic on *one day* (sub-page signature deployment 2 of 3).
  - Body: three paragraphs, 17px. Paragraph 1: site evaluation (what gets checked, how long it takes, what the quote covers). Paragraph 2: the day of the upgrade (crew size, power outage duration, what gets replaced). Paragraph 3: inspection and sign-off (county inspector visit, typical timing, warranty).
- Secondary block (columns 10-12):
  - Sidebar fact list in mono 13px uppercase, tracked 0.08em. Five facts:
    - `TYPICAL UPGRADE: 100A → 200A`
    - `OUTAGE WINDOW: 4-6 HOURS`
    - `PERMIT PULLED BY US`
    - `INSPECTED BY COUNTY`
    - `20-YEAR PANEL WARRANTY`
  - Each fact preceded by `→` glyph inheriting currentColor. 8px gaps between facts.
- Column 9 empty gutter.

**Rules satisfied.**

- Layout C applied.
- Rule E1: accent on eyebrow + h2 italic + primary CTA (Section B1) only. Sidebar is dark-primary + text-muted, not accent.
- Persona: fact sidebar is documentary, not promotional. Numbered in scope ("4-6 HOURS," "20-YEAR") without superlatives.

## Section B3: Process watermark (Layout E)

**Role in rule system.** Editorial Layout E from the module. Second editorial composition. Carries the page's ≥80px display moment.

**Composition.**

- Section header: centered. Eyebrow "THE THREE STEPS" mono accent; h2 "From call to final inspection." 32px display.
- 3-column grid at desktop, stacked at mobile.
- Each cell:
  - Watermark numeral `01` / `02` / `03` outlined at 160px. Top-left of cell.
  - h3 below numeral: "Evaluate" / "Upgrade" / "Inspect." 22px display.
  - Body: 2-3 sentences per step, 16px body, max-width 30ch. Specific about what happens.
  - Hairline rules between cells (vertical desktop, horizontal mobile).
- Background: `--color-background-alt`.

**Rules satisfied.**

- Rule E4: outlined watermark numerals with @supports fallback.
- Scale contrast: 160px numeral + 13px body = 12x. Page clears threshold here.
- Rule E2: cells separated by hairlines, not cards.
- Three-step process is the legitimate Layout E application when a service sub-page has a natural numbered sequence.

## Section B4: Evidence divider (Layout B image-bleed)

**Role in rule system.** Editorial Layout B from the module. Third editorial composition on the page — brings the page to the 3-layout minimum without introducing Layout D (which would over-weight the short page) or a second Layout A (which would read as repetitive on a sub-page).

**Composition.**

- 12-column grid.
- Photo (columns 1-9): detail shot of a completed panel interior. Clean wiring, labeled breakers, copper grounding bar visible. Role-tagged `detailShot`. Aspect ratio 16:9, object-fit cover.
- Caption (columns 10-12):
  - Mono 13px uppercase tracked 0.08em.
  - Four lines, each preceded by a hairline rule above the first and between:
    - `RESIDENTIAL PANEL INTERIOR`
    - `DUNNELLON, FL / MARCH 2026`
    - `200A SQUARE D QO`
    - `COPPER THROUGHOUT`
  - Top-aligned with the photo.

**Rules satisfied.**

- Layout B applied.
- Rule E3: caption with location, date, equipment, material. Every photo captioned.
- Persona: caption is documentary (location/date/spec), not celebratory. Quiet confidence carries through.
- Rule E2: caption uses hairline rules, not a boxed list.

## Section B5: Service-specific FAQ (Layout A)

**Role in rule system.** Editorial Layout A from the module. Fourth editorial composition on the page — permitted because the page has room for a second distinct layout and FAQ is the natural Layout A application.

**Composition.**

- 12-column grid.
- Left block (columns 2-5): section headline "Questions we hear about panel upgrades." 28px display. Italic on *panel upgrades* (sub-page signature deployment 3 of 3).
- Right block (columns 7-12): 5 FAQ rows specific to this service:
  - "Do I need a permit?" → Yes, we pull it.
  - "How long will my power be out?" → 4-6 hours typical.
  - "Can you upgrade while I'm at work?" → Yes, most jobs.
  - "What if the inspector finds an issue?" → We fix it, no charge.
  - "How long is the warranty?" → 20 years on the panel, 1 year on labor.
- Between rows: hairline rules. No card wrappers. Same accordion pattern as homepage FAQ.

**Rules satisfied.**

- Layout A (first and only deployment on this page).
- Rule E2: rules between FAQ rows.
- Persona: answers are specific, short, and declarative. Quiet confidence form.
- Service sub-page FAQ differs from homepage FAQ: narrower scope (only this service), fewer rows (5 vs. 8), more specific answers.

## Section B6: Service-specific close (centered-stacked)

**Composition.**

- Section header centered. h2 "Ready for a panel evaluation?" 32px display.
- Below h2: one-sentence paragraph. "Evaluations are free, typically scheduled within a week, and take about 30 minutes on site." 17px body, centered.
- Primary CTA: "Book an evaluation" button — 18px, `--color-primary` background. Leads to contact form with `service=panel-upgrade` pre-filled.
- Below the button: one line mono 12px. `OR CALL (352) 555-0142 WEEKDAYS 7AM TO 6PM`.

**Rules satisfied.**

- Persona close (Quiet confidence): specific, calm, phone-available but booking-primary for a service-qualified reader. This is the one place a Quiet confidence service sub-page prefers form-primary over phone-primary: the reader has already made the decision to consider this service, and the form is the next concrete action rather than a call that re-opens the conversation.
- Service sub-page conversion convention: primary CTA is service-specific action ("Book an evaluation"), not generic quote request.

## Service sub-page composition check (Phase 6 dry-run)

| Check | Service sub-page result |
|---|---|
| At least one ≥80px element | Pass — process watermark numerals at 160px |
| At least one ≤14px mono element | Pass — eyebrow, fact sidebar, evidence caption, close caption |
| Scale contrast ratio ≥5x | Pass — 160px / 13px = 12.3x |
| At least 3 editorial layouts | Pass — Layout A, Layout B, Layout C, Layout E — 4 distinct |
| No layout repeats more than twice | Pass — each used once |
| Layout D at most once per page | Pass — not used (intentionally omitted for short-page weight reasons) |
| Persona carried through load-bearing decisions | Pass — hero italic on proof, process italic on duration specificity, FAQ italic on service name, CTA copy service-specific, evidence caption documentary not celebratory, close is booking-primary (correct service sub-page modulation of Quiet confidence's default phone-primary) |
| One signature micro-interaction, used site-wide | Pass — italic-color-shift three times, same signature as homepage + About |
| Accent color appearances ≤12 | Pass — counted 7 (nav active, hero eyebrow, hero italic, hero primary CTA, process h2 italic, FAQ headline italic, close CTA) |
| Every non-hero photo captioned | Pass — Layout B detail shot has four-line mono caption |

---

# Cross-page composition notes

When Phase 5 generates a multi-page build (homepage + About + one or more service sub-pages), three cross-page rules apply:

**1. Persona inherits across pages unless explicitly overridden.** Phase 4 sets persona once at the approval gate. Every sub-page uses the same persona. Individual sub-pages can override at Phase 5 only if the prospect's data for that specific service materially conflicts with the homepage persona — which is rare. In practice: the persona is a site-level property, not a page-level property.

**2. Signature micro-interaction is site-level, count is page-level.** The italic color-shift used on the homepage is the same signature used on the About and service sub-pages. But each page has its own 3-deployment budget; the homepage can use italic-color-shift 3 times, and the About page can use it 3 more, for 6 total across the site. The rule "one signature" is about consistency, not budget.

**3. Layout D economics are page-level.** The homepage might skip Layout D because no qualifying secondary hero plate exists. The About page can still use Layout D because the About page has its own photo budget (primarily environmental portraits) and a qualifying photo may exist there. Service sub-pages usually skip Layout D because the page is short — a full-bleed on a 5-section page over-weights the visual arc.

---

## What this example does NOT demonstrate (build diversity caveat)

A single reference build cannot show every valid composition. Other builds will correctly differ in ways this example does not:

- **Lower-tier builds (Standard, 0-39)** skip the wide glass card, skip one or more editorial layouts (with justification at approval gate), and lean more heavily on the one-signature micro-interaction because they have fewer display moments to anchor.
- **Hero mode = parallax** changes the entire hero region and shifts the editorial layout budget — parallax absorbs more weight at the top, so later-page editorial layouts can be more aggressive (full-bleed Layout D is more likely to land).
- **Trades without strong photo libraries** (some plumbers, HVAC techs in older neighborhoods) may Phase-3-fallback to icon-heavy services grids, detail-shot-only section dividers, and skipped before/after galleries. Layout B (image-bleed) is unavailable without a qualifying detail shot.
- **Non-English or bilingual prospects** add voice-mapping considerations not covered here. See `content-rules.md`.
- **Multi-page builds** — covered in the sub-page examples above (About + service sub-page). Other sub-page types (dedicated contact page, multi-project portfolio page, service-area landing pages for specific cities) are not worked here and should be extrapolated from the homepage + About + service examples by Phase 5. The three-moment arc (opening / build / close) applies to every page type.

The point of this example is not "every build looks like this." The point is "every build is composed against the same rules, and this is what a correct composition looks like when all the rules land at once."

---

## Version

example-build.md — part of prospect-site-composer. Worked reference pages for the Tucci Electric synthetic composite — homepage, About page, and service sub-page (Panel Upgrades). Sub-page examples added April 21, 2026 per handoff feedback to give Phase 5 pattern-match coverage across page types. Loaded by Phase 5 at generation start as a pattern-match reference. Every annotation in this file maps to a specific rule in `css-framework.md`, `section-patterns.md`, `image-handling.md`, `hero-patterns.md`, or `anti-slop-rules.md`. When this example and those rule files disagree, the rule files win — this example exists to show the rules in composition, not to override them. Last updated April 9, 2026.

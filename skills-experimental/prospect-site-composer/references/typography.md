# typography.md

Typography authority for the prospect-site-composer skill. Loaded by Phase 4 at design approval (for persona → font-family selection), by Phase 5 at section generation (for role-class assignment, italic deployment, pull-quote detection, scale enforcement), and by Phase 6 at verification (for the thirteen checks listed at the bottom of this file).

Stage II (d) three-way merge output — production baseline (Composer's pre-merge file, F5-era + Wave 2 retrofits) × Design in-flight (`composer-stage-ii-typography-source/typography-patterns.md`) × this merged file. Revision log at the bottom enumerates all twelve resolved conflicts.

---

## The load-bearing principle

**Variety across prospects comes from persona variety, not font-selection randomness.** Two prospects with the same persona should get the same font pairing by default. That is what makes the persona system legible. If future maintainers are ever tempted to add a "mix it up" knob to font selection, that sentence is the answer for why not.

Authoritative anchor: `COMPOSER_BRAIN.md §1`. The principle governs every decision below and is the reason the persona-conditional font tables, the role-class vocabulary, and the tier-application discipline all compose into a coherent editorial system rather than a set of aesthetic knobs.

The entire type system in this file is deterministic. Given a persona and a tier, the font selection is reproducible across builds. Overrides are explicit and traceable — either `CONFIG.fonts` names a specific family, or the tier gate unlocks paid families, or a named conflict pair triggers a walk-to-second-candidate. No hidden randomness, no timestamp-based selection, no aesthetic-variance knob.

---

## Naming convention (meta-rule)

All typographic primitives in this skill are named in three layers:

1. **Role name** — what the primitive *is* in the system. `SectionOpener`, `StatRow`, `FeaturedPullquote`, `AnchorStrip`, `TagStrip`. Role names are skill-level and stable across brands.
2. **Semantic alias** — what the primitive *does* on a given page. `services-header`, `reviews-header`, `equine-opener`. Semantic aliases are per-section and readable; they map onto role names 1:1.
3. **Instance override** — what the primitive *tweaks* in one specific place. A class modifier, a CSS custom property override, a scoped variant. Overrides absorb per-section specificity without polluting the role name.

The role-alias-override layering is the answer to the readability-vs-consolidation tradeoff. Role names keep the system coherent; semantic aliases keep the HTML readable; instance overrides keep per-section tweaks from fracturing the primitive.

When reading this document, treat every primitive name (`SectionOpener`, `StatRow`, etc.) as the role name. Semantic aliases and overrides are authorial.

---

## 1. The three-voice type system

Three type voices exist on a contractor preview site. Each voice has one dedicated CSS custom property, one set of semantic role classes, and one font-family slot in the persona × voice matrix.

### Voice 1: Display (`--font-display`)

**What it is.** The editorial voice. Large headlines, pull quotes, watermark numerals, feature-well treatments. The voice the reader's eye lands on first and remembers last.

**When it leads.** H1 and H2 elements always. Pull quotes. Watermark numerals in stats sections. Large standalone numerals (pricing callouts, hero stats). Editorial captions on full-bleed imagery when the caption carries weight.

**Weight and scale.** Typically 500-700 weight for headlines, 400-500 for pull quotes, 300-400 outlined for watermark numerals. Display sizes range 40-180px depending on role.

**Why it's called display, not heading.** A watermark numeral at 160px is not a heading — no H-tag wraps it, it doesn't outline the document, and it doesn't participate in the page's heading hierarchy. It is a *display-scale* typographic moment. The token name `--font-display` captures this; `--font-heading` would not.

### Voice 2: Body (`--font-body`)

**What it is.** The reading voice. Paragraphs, UI labels, nav links, form labels, section H3/H4/H5, card body copy, service descriptions, FAQ questions and answers, most caption text.

**When it leads.** Any sustained reading surface. Anything below H2 in the heading hierarchy. All UI chrome. Anything a reader scans rather than reads.

**Weight and scale.** 400 regular for body, 500-600 for emphasis, 600-700 for H3/H4. Body sizes range 14-20px depending on role; lede-paragraph treatment goes to 18-22px.

**Why it's called body, not text or sans.** "Body" names the role — the text the reader's body of attention lives in. "Text" is ambiguous (all type is text), "sans" is a category not a role, and `--font-body` aligns symmetrically with `--font-display` and `--font-data`.

### Voice 3: Data (`--font-data`)

**What it is.** The metadata voice. Phone numbers, addresses, hours, license numbers, service-area enumeration, timestamps, metric callouts that need to read as information rather than language. Anything the reader treats as lookup rather than prose.

**When it leads.** Phone numbers and email addresses in nav and footer. Stats section captions ("AVERAGE GOOGLE RATING", "FIVE-STAR REVIEWS"). Eyebrow labels above H2s. License numbers. Service-area lists. Small caps tracked labels on editorial photo captions. Metadata blocks in the About page (founded year, headquarters location, service area). Form field labels in small tracked-caps treatment. Filled stat numerals (the "56" in a stats cell).

**Weight and scale.** 500-600 weight, often with `letter-spacing: 0.08em` or wider. Sizes range 10-14px for labels and metadata. Stat numerals go 56-72px. Never larger than 40px for non-numeral data usage — data voice at display scale reads as computer-generated and breaks the editorial register.

**Why it's called data, not mono or metadata.** "Mono" is a category (monospace) not a role, and the data voice does not have to be monospace — a well-chosen geometric sans at small tracked-caps reads as data too. "Metadata" is accurate but long. "Data" names the role crisply and leaves the specific family choice (mono or geometric-sans-at-tracked-caps) to the persona tables below.

Data voice absorbs what earlier Composer drafts enumerated as separate Eyebrow and Stat-numerals tiers. The three-voice system subsumes those into the Data voice role classes (`.role-data-eyebrow`, `.role-data-stat-caption`, `.role-data-numeral`) while preserving all the per-element rules previously authored.

### How the three voices compose

A well-composed page uses all three voices in visible rotation. A page that uses only display and body reads like an overdecorated blog post. A page that uses only body and data reads like a UI with no voice. A page that uses all three reads editorial — display carries the rhetorical moments, body carries the reading experience, data carries the metadata and structural labels.

The composition rule: **every major section should contain at least two of the three voices, and most pages should contain all three voices at least once.** This is enforced in Phase 6 Check 12 (three-voice presence per page).

### The voices don't blend — discipline rule

A headline doesn't get eyebrow tracking. Body copy doesn't get mono capitals. Stat numerals don't get body weight. The *job* of each voice is what keeps the system legible. When a designer reaches for one voice to do another voice's work — say, italicizing a headline in a "callout color" to make it feel like an eyebrow — the system flattens. Don't do that.

---

## 2. Scale relationships

Typography at the scale of a site — not a single page — is a relationship problem, not a sizing problem. The question is never "how big should this be" in isolation. It's "what ratio does this hold to the things around it."

### Ratio reasoning

Pick a ratio and commit. The A Quality Pool homepage (F5) uses roughly a 1.25 scale across the body-voice tier and a looser, more expressive scale across the display-voice tier:

- **Body voice** — 13px → 14px → 15px → 16px → 17px → 18px italic → 19px italic. Most transitions are 1-2px. The body tier is tight on purpose — reading comfort lives in small steps.
- **Display voice** — 28px → 32px → 42px → 48px → 56px → 88px → 148px. Sparser and more expressive. Display type is a performance, not a conversation.
- **Data voice eyebrow sub-register** — 9px → 10px → 11px. Three sizes total. Don't invent more.

The ratio isn't mathematical in the Fibonacci/modular-scale sense — it's tonal. Moves between sizes should feel like moves in a melody. If two tiers feel the same, one of them is wrong.

### vw coefficients

Display type scales with `vw`. Coefficients for this skill cluster in 7–9vw for primary display, 5–6vw for secondary display, 3–4vw for tertiary. These are authorial ranges, not mathematical constants — hero headlines lead at 8vw; section openers step down to 5–6vw; pullquotes sit at 3–4vw. Brands with a quieter voice may center their coefficients a point lower; brands with louder voice a point higher. The range holds across the builds this skill has produced.

### min(max()) vs. clamp() — viewport-range-aware authoring

`clamp(min, preferred, max)` is the obvious tool for responsive type. It's also a trap.

A headline with `clamp(56px, 7.5vw, 104px)` ceilings out at 1386px of viewport. At 1440px, 1600px, 1920px — every common desktop width clients actually view a production site on — the type size is frozen at 104px while the canvas keeps growing. The headline reads proportionally lighter at 1920px than at 1386px. Editorial at preview width, "dramatic website" at production width.

The fix is to stop thinking about clamp as "a value between two bounds" and start thinking about it as "a function whose output must still feel right at the viewport the client will actually use." For display type, that usually means:

```css
font-size: min(148px, max(56px, 8vw));
```

`max(56px, 8vw)` is the live scaling relationship. `min(148px, ...)` is the ceiling, positioned deliberately above the "real" desktop range so the scaling is still active at 1440–1920px, but guards against runaway sizing at 4K+ displays.

**Rule.** For display type that must carry visual weight across the common desktop range, set the ceiling above 1920px × (vw coefficient). For the 8vw rule above, that's 8vw × 1920 = 154px — pick 148–160 as a ceiling.

Use `clamp()` for body-voice type where the scaling range is narrow and the ceiling is meaningful. Use `min(max())` for display-voice type where the ceiling exists only to guard against 4K surprises.

---

## 3. Role classes

Each role class names a specific purpose on the page and maps to one of the three voices with a defined size, weight, tracking, and leading. Phase 5 uses role classes rather than raw CSS properties so voice assignment is consistent across pages and Phase 6 can verify it.

### Display-voice role classes

- `.role-display-hero` — H1 in the hero glass card. 48-72px depending on viewport. 600 weight. Line-height 1.05. `font-family: var(--font-display)`. Letter-spacing -0.01em.
- `.role-display-section` — H2 in any non-hero section. 36-56px depending on viewport. 600 weight. Line-height 1.1. `font-family: var(--font-display)`. Letter-spacing -0.01em.
- `.role-display-watermark` — Outlined numeral behind a filled stat. 120-180px depending on viewport. 300 weight, outlined via `-webkit-text-stroke` or SVG. `font-family: var(--font-display)`. Letter-spacing 0. See Stats watermark rule (§7 StatRow and Rule 4 below).
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

- `.role-data-eyebrow` — ALL CAPS label above an H2. 11-13px. 600 weight. Letter-spacing 0.12em. `font-family: var(--font-data)`. Only deployed on sections that genuinely introduce a new information mode (see Rule 3). Two-register color variants documented in §4 below (`.role-data-eyebrow--primary` loud wayfinding register, `.role-data-eyebrow--mute` quiet meta register).
- `.role-data-caption` — Small caps tracked-caps editorial caption on a full-bleed photo. 11px. 500 weight. Letter-spacing 0.1em. `font-family: var(--font-data)`. Multi-line captions use `.role-body-caption` stacked below the data-caption title.
- `.role-data-stat-caption` — Caption under a stat number in the stats section. 11-13px. 600 weight. Letter-spacing 0.08em. UPPERCASE. `font-family: var(--font-data)`.
- `.role-data-metadata` — Phone number, address, hours, license number in nav and footer. 14-16px. 500 weight. Slight tracking, 0.02em. `font-family: var(--font-data)`. Tabular numerals (`font-variant-numeric: tabular-nums`) required.
- `.role-data-service-area` — Service-area town names in the contact section sidebar. 13-15px. 500 weight. 0.04em tracking. `font-family: var(--font-data)`.
- `.role-data-numeral` — Standalone filled stat numeral in the stats section (the "56" that sits in front of the watermark "56"). 56-72px. 700 weight. Tabular numerals. `font-family: var(--font-data)` OR `var(--font-display)` depending on persona (see persona tables in §11).

### Italic signature role class

- `.role-italic-signature` — The italicized color-shifted word in an H1 or H2. Inherits size from its parent role class. Italic weight. Color behavior governed by the em-inherits-color rule (§5) except for the two canonical em-on-dark exceptions. Deployed once per H1/H2, according to Rule 1 italic deployment rule below. Not a voice of its own; a micro-treatment applied within an existing display role.

---

## 4. Mono eyebrow system — two registers

The data-voice tier is where typography becomes information architecture. Eyebrows (`.role-data-eyebrow`) carry a two-register color system that separates wayfinding from meta.

### Sizing and tracking

- 11-13px + 0.12em tracking — section eyebrows, the loudest register. Matches `.role-data-eyebrow` spec.
- 10px + 0.14em tracking — section tags, operational tags, stat labels in bright context.
- 9px + 0.18em–0.2em tracking — captions, photo credits, quiet meta.
- Case: always uppercase (one explicit exception for photo-credit attribution in the Front Porch footer — see `voiceMap.md §Front Porch footer`). Tracking expands to compensate for the visual tightness of caps. At 9px, 0.2em tracking; at 11px, 0.12em. Smaller sizes need more tracking.

### Color — two registers, not one

A single eyebrow color flattens the tier. The **loud** register (`--primary` — the bright brand color) carries wayfinding weight: section eyebrows, navigation phone, CTAs. The **quiet** register (`--mute` — a neutral gray) carries meta: photo captions, dates, credits, secondary mono lines in paired layouts.

Expressed as role-class modifiers so `composition-plan.json` can declare the register per-eyebrow (per `composition-plan-schema.md §4.6 eyebrowDeployments[].register`):

```css
.role-data-eyebrow--primary { color: var(--primary); }  /* wayfinding */
.role-data-eyebrow--mute    { color: var(--mute); }     /* meta */
```

**The bug this rule fixes.** In the first pass of the A Quality Pool homepage (F5), every mono element used `--primary`. The tier had no quiet register. Introducing `--mute` as a secondary mono color gave the tier an inside voice, which let the loud register actually carry weight.

### Placement

Eyebrows always precede their headline. 12–22px of margin between eyebrow and headline — enough gap to read as a distinct tier, close enough to read as paired. Maximum 24px per Phase 6 Check 2. Never use eyebrows as post-headline captions; that's a different typographic move (the caption pattern) and it uses the quiet register via `.role-data-caption`.

---

## 5. Italic discipline

Italic is voice, not decoration.

### One italic run per headline

Every H1 and H2 gets at most one italic span. "*Central Florida.*" "*One pool phone number.*" Each headline picks the phrase that carries the emotional weight and italicizes that phrase. Two italic runs per headline is a tell — the designer didn't commit to which phrase mattered most. Phase 6 Check 1 enforces this structurally.

This rule generalizes. Pick the phrase. Italicize it. Move on.

### em inherits color (the rule, codified)

Headline italic runs inherit the headline's color. They do not shift to an accent color. Italic is the shape move; color shift would be a second, redundant move.

```css
.role-display-hero em,
.role-display-section em,
.role-italic-signature {
  color: inherit;
  font-style: italic;
  font-weight: 300;
}
```

Weight 300, because a lighter italic weight distinguishes the italic run from the roman run without requiring a color change.

**One exception, two canonical locations.** Italic runs inherit color *unless the headline color and italic emphasis produce insufficient contrast*. The one exception is italic on a dark navy background, where inherited white italic is indistinguishable from roman. The exception appears in two canonical places on the A Quality Pool F5 homepage: the Equine navy band and the Front Porch footer. Both are navy backgrounds, both use `--accent` for italic runs. Same exception, two instances.

No other exceptions. A "brand accent" color shift on italic runs in non-dark contexts is the failure mode this rule was written to prevent.

### Body italic

Body italic runs always inherit color and italic weight. They're a typographic pause, not a voice move. The body voice doesn't get the italic-as-voice treatment — that's reserved for display.

```css
.role-body-paragraph em,
.role-body-caption em {
  font-style: italic;
  color: inherit;
}
```

### Italic pullquote sizing

When a pullquote is set in italic display-voice at display scale, the size lives in its own tier between headline and body:

- Featured pullquote: 30–44px, weight 300, italic. Set via `.role-display-pullquote`.
- Review card quote: 16–18px, weight 300, italic.
- Anchor-strip pullquote: 22–28px, weight 300, italic.

The italic pullquote is the one body-adjacent moment that gets display treatment. It's a voice pivot — the page steps from information-delivery mode into testimony mode, and the italic at display size signals that pivot before the reader's brain parses the words. Don't mix italic pullquote with decorative quote marks; the italic does the quote-signaling on its own (see §16 Ornament rule).

---

## 6. SectionOpener — role-class framing

SectionOpener is not a parameterized primitive with CSS axes. It is a role-class composition: a `.role-data-eyebrow` element paired with a `.role-display-section` element under a ≤24px proximity contract (Phase 6 Check 2). Phase 4 declares orientation; Phase 5 emits the role-class pair.

### Composition

```html
<div class="section-opener">
  <div class="role-data-eyebrow role-data-eyebrow--primary">The full pool environment</div>
  <h2 class="role-display-section">Eight services. <em>One pool phone number.</em></h2>
</div>
```

### Orientation

Two orientations produce the SectionOpener: **`eyebrow-above`** stacks the eyebrow (`.role-data-eyebrow`) above the H2 (`.role-display-section`) with ≤24px vertical margin (Phase 6 Check 2); **`tag-strip-inline`** runs the eyebrow as a sibling-inline element beside the H2, with horizontal separation rather than vertical. The role classes are identical across orientations; only the spatial relationship differs. Phase 5 picks orientation per `composition-plan.json`'s `sections[].orientation` field; eyebrow sizing follows the role class and does not vary by orientation.

### TagStrip variant (signature + operational)

Tag strips sit above a bordered content block and read as an index entry rather than a prose opening. Used for numbered service sections, case studies, multi-part compositions. The tag strip itself is data-voice, full-bleed across the card top, with a primary-register left-label and a mute-register right-label.

```css
.signature-tag {
  padding: 14px 36px;
  background: var(--page);
  border-bottom: 1px solid var(--line);
  display: flex;
  justify-content: space-between;
  font-family: var(--font-data);
  font-size: 10px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--primary);
}
.signature-tag .mute { color: var(--mute); }
```

This is the strongest structural motif in the system. When in doubt about how to frame a content block, reach for the tag strip.

### F5 canonical instances

Four SectionOpener instances on the A Quality Pool F5 homepage are reference implementations, not skill-level enumerations — future brands may produce different instance counts from the same composition:

- **Services header** — mono eyebrow above (primary register), italic counter-phrase inline inside H2.
- **Signature section** — mono tag strip + large display-voice headline, no italic.
- **Reviews header** — mono eyebrow (primary register), italic counter-phrase on new line.
- **Equine band** — mono eyebrow (primary register), two-line headline with italic on second line (navy background; italic takes `--accent` per em-on-dark exception).

---

## 7. StatRow — contrast pair

Large display-voice numerals + small data-voice labels, plus the stats-watermark-consistency rule. The contrast isn't decoration — it's the whole content of the stat row.

### Composition

```html
<div class="stat-cell">
  <div class="role-display-watermark">56</div>
  <div class="role-data-numeral">56</div>
  <div class="role-data-stat-caption">FIVE-STAR REVIEWS</div>
</div>
```

```css
.role-data-numeral {
  font-family: var(--font-data);
  font-size: 48px;
  color: var(--darkmuted);
  font-weight: 400;
  line-height: 1;
  font-variation-settings: 'opsz' 48;
  letter-spacing: -0.02em;
  font-variant-numeric: tabular-nums;
}
.role-data-stat-caption {
  font-family: var(--font-data);
  font-size: 9px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--mute);
  margin-top: 10px;
}
```

### Rules

- Numeral scale must be ≥4× the caption scale. At 48px / 9px, that's 5.3×. At 32px / 10px, 3.2× — not enough; the tier collapses.
- Numeral weight should be 400 or lighter. Bold numerals at display scale feel like pricing tables, not editorial. The serif silhouette carries the weight.
- Caption color lives in the quiet data-voice register (`--mute`). Loud captions would fight the numerals.
- Hairline dividers between stats on desktop echo the meta-grid rhythm elsewhere on the page. `border-left: 1px solid var(--line)` on every stat except the first.

### Stats watermark numbering (Rule 4)

**The outlined watermark numeral and the filled numeral in a stats section must be the same number.** Not the display-order index ("01, 02, 03"). Not the section number. The stat's actual value.

If the stat is "56 five-star reviews," the watermark is "56" at 140-180px outlined and the filled numeral is "56" at 56-72px. Stacked or offset-overlapping, both rendering the same value.

This rule specifically addresses the Luna F8 bug where the stats section rendered "04, 02, 03, 04" (display-order indices) behind "4.9★, 56, 18, 2" (actual values). The outlined-watermark-of-index treatment is a valid editorial pattern in magazine feature-well design but wrong for stats — the reader's eye goes to the large number first and finds a meaningless index, then to the small number and finds the real value, then has to mentally discard the first read.

**Phase 6 Check 11 is unfalsifiable by construction** in the Composer architecture: `composition-plan.json`'s `statRow.stats[].value` is a single field; Phase 5 renders the same string in both `.role-display-watermark` and `.role-data-numeral` positions. There is no separate watermark field to drift from.

### Mobile

On viewports ≤480px, stat rows stack vertically with horizontal hairline dividers between. Numeral scale drops to 36–42px; caption stays 9px. Don't shrink the caption to maintain proportion — the caption is already at legibility floor. Mobile watermark treatment per Rule 8 below, selected per-persona.

---

## 8. Body measure and line-height

### Measure

Cap paragraph width at **56–62 characters**. Inside cards: 44–48ch. Italic display pullquotes: 20–28ch for visual drama.

The `ch` unit is how to author this. Not px. Px doesn't survive font changes; ch does.

### Line-height

- Body-voice paragraphs: **1.65–1.7**. Never below 1.6.
- Display-voice headlines: **0.98–1.12**. Display wants tightness.
- Italic pullquotes: **1.2–1.4**. Middle ground.
- Data-voice eyebrow / meta: **1.45–1.8**. Mono wants air between lines at small caps.

### When measure and wrap collide

See §17 Structural HTML contracts. If a CSS measure produces an ugly wrap in compound phrases, the fix is to widen the measure, not to fight the browser's wrap algorithm with `hyphens: manual`. The browser's wrap is doing its job; the measure was wrong.

---

## 9. Mobile scaling rules

Mobile is not desktop-shrunk-down. Mobile is its own typographic problem.

### H1 scaling — aggressive, not proportional

At narrow viewports, the H1 should be *more* prominent relative to its surrounding content than on desktop. The hero photo often disappears on mobile, the CTA bar pins to the bottom of the viewport, and the headline becomes the single most important visual on the screen.

**Rule.** `clamp(44px, 9vw, 64px)` minimum for `.role-display-hero`. Don't design mobile H1s at 32px "to save space." The headline earns the space.

### Stat-row stacking

At tablet breakpoints (980px), stat rows stay in three columns but tighten. At phone breakpoints (540px), stat rows stack vertically and each stat gets a thin horizontal divider below it. Don't maintain three-column stat rows at phone widths; the numerals compress below tier-legibility.

### Mobile watermark breakpoint (Rule 8)

On viewports ≤480px, `.role-display-watermark` either (a) shrinks to 80-100px and sits behind the filled numeral with reduced opacity, (b) moves to a corner of the stat cell and reduces to 56-72px, or (c) is dropped entirely in favor of the filled numeral at full size.

Phase 5 writes a mobile-specific CSS block for watermark treatment, selected per-persona:

- **Quiet confidence, Modern specialist** — use (a): reduced opacity, shrunken, stays behind.
- **Neighborhood steady, Earned pride** — use (b): moves to corner, reduced size, treated as editorial chapter-number rather than watermark.
- **Urgent service (Rescue-ready)** — use (c): dropped entirely. This persona rewards speed over editorial; the mobile page should not spend vertical space on decorative watermarks.

Phase 6 Check 13 verifies rendered mobile watermark: computed `font-size ≤100px` OR `display: none` OR `position: absolute` with corner offsets.

### Body measure adaptation

At mobile, `max-width: 56ch` naturally narrows because the viewport is narrower than 56 characters of body type. No explicit mobile override needed for measure; the constraint is self-enforcing.

### Padding

Mobile padding on sections: `24px` horizontal, `48–64px` vertical. Desktop: `40–56px` horizontal, `72–88px` vertical. Vertical padding carries more weight on mobile because the viewport is taller-than-wide and vertical rhythm is what the reader experiences.

---

## 10. Font loading discipline

Fraunces is a variable font and commonly lands as the display-voice candidate across multiple personas. Treat the axes deliberately.

### Variable axes to pin

Fraunces exposes:

- `wght` — weight (300–700)
- `opsz` — optical size (9–144)
- `SOFT` — softness (stylistic)
- `WONK` — wonkiness (stylistic)

**Pin `opsz` to match the rendered size.** This is the single most important font-loading rule. A 48px stat numeral should render with `opsz: 48`; a 96px hero headline should render with `opsz: 96`. If you don't pin `opsz`, the browser picks a default and the large sizes render with optical proportions designed for body text. They look stretched.

### opsz across breakpoints

For fixed-size elements (stat numerals at 48px), pin opsz to the rendered size once. Single pin.

For display elements that scale 2× or more across viewports (hero headline scaling from 56px to 148px), a single mid-range opsz pin produces bad renders at one end of the range. The fix is to override opsz at the mobile breakpoint:

```css
.role-display-hero {
  font-size: min(148px, max(56px, 8vw));
  font-variation-settings: 'opsz' 96;
}
@media (max-width: 720px) {
  .role-display-hero {
    font-variation-settings: 'opsz' 56;
  }
}
```

**Heuristic.** If the scaled range of a display element spans 2× or more, override opsz at the breakpoint where the rendered size drops more than 30% below the desktop pin. Pick a mobile opsz value that approximates the rendered mobile size. Single breakpoint override is usually enough; three-step opsz ladders are rarely justified.

### Stylistic sets as signature

Fraunces's `ss01` (single-story `a`) and `ss02` (softer `g`) applied globally to every display element is the one typographic signature move in this system. It's a small detail — most readers won't notice consciously. But it distinguishes the display face from every Fraunces-default site on the web.

```css
.role-display-hero, .role-display-section, .role-display-pullquote, .role-display-watermark {
  font-feature-settings: "ss01" 1, "ss02" 1;
}
```

**Rule of thumb on stylistic sets.** Pick one or two and apply consistently. Three or more starts to feel like showing off. The restraint is the signature.

### Loading

Use Google Fonts or a self-hosted variable font file per `css-framework.md` `CONFIG.fonts`. `font-display: swap` on all faces. Preconnect to the font origin. Don't load weights you won't use. Font-loading fallback per `COMPOSER_BRAIN.md §6 PA.5`: if the persona-conditional heading font fails to load, fall back to `var(--font-body)` rather than system default.

---

## 11. Persona-conditional font selection

Each of the five personas biases the selection of font families for display, body, and data voices. The tables below specify ordered candidate lists. Phase 4 picks the first available candidate, subject to the selection logic in `css-framework.md` (tier gate, `CONFIG.fonts` override, conflict-pair walk).

Licensing flags: **GF** = Google Fonts (free, CDN-available, build-time usable). **paid** = requires commercial license.

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

**Why.** Fraunces brings warmth through its soft-terminaled serif; Recoleta (paid) does the same thing harder if the tier allows. Body sans skews slightly rounder (Nunito as alternative) for family-business warmth. Data voice can skip mono entirely and use tracked-caps Space Grotesk — this persona's metadata reads as neighborhood directory rather than technical documentation.

### Persona 4: Urgent service (Rescue-ready)

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

**Why.** This is the one persona that does not use a serif for display. Modern specialist reads more credibly in a tight neo-grotesque — Inter Tight as the free candidate, Söhne or Neue Haas as the paid walk-ups. The display-body pairing is deliberately close (both sans, both neo-grotesque family) to produce a technical, restrained feeling. Data voice is mono for the same reason as Urgent service: technical metadata reads credibly in mono.

---

## 12. Named conflict pairs

When Phase 4's default candidate selection produces a display-body pairing with a known aesthetic or metric conflict, Phase 4 walks to the second candidate in whichever list has more alternatives. The conflict pairs below are enumerated so future maintainers can add or remove conflicts as a named list rather than rewriting the selection logic.

### Conflict pair 1: Fraunces display vs. Fraunces body

**Voice slot A's candidate.** Fraunces (display).
**Voice slot B's candidate.** Fraunces (body — not in current tables but possible via `CONFIG.fonts` override).
**Why they conflict.** Using the same family for display and body collapses the display-body contrast to a weight-and-size difference only. Works for some editorial brands but defeats the three-voice type system.
**Which voice walks to #2.** Body walks to Inter. Display stays Fraunces.

### Conflict pair 2: Playfair Display vs. Nunito

**Voice slot A's candidate.** Playfair Display (display, Earned pride).
**Voice slot B's candidate.** Nunito (body, Neighborhood steady alternative).
**Why they conflict.** Playfair's high-contrast Didone forms against Nunito's soft-terminaled humanist body reads as mismatched — one is formal-editorial, the other is warm-rounded. Happens only when Neighborhood steady's body candidate gets overridden by `CONFIG.fonts` to a persona that prefers Playfair-class display.
**Which voice walks to #2.** Body walks to Inter. Display stays Playfair.

### Conflict pair 3: Archivo display vs. Archivo body

**Voice slot A's candidate.** Archivo (display, Urgent service).
**Voice slot B's candidate.** Archivo (body, Urgent service alternative).
**Why they conflict.** Same-family display and body is normally the conflict, but Urgent service specifically *wants* this — its persona rewards structural economy. This is the one conflict pair that is **allowed** when both slots are Archivo. Phase 4 does not walk.
**Which voice walks to #2.** Neither. This pair is allowed.

### Conflict pair 4: Inter Tight display vs. Inter body

**Voice slot A's candidate.** Inter Tight (display, Modern specialist).
**Voice slot B's candidate.** Inter (body, Modern specialist).
**Why they conflict.** Same superfamily, different optical size. Normally a conflict; for Modern specialist it's the intent. Phase 4 does not walk.
**Which voice walks to #2.** Neither. This pair is allowed.

### Conflict pair 5: Two transitional serifs in display and data

**Voice slot A's candidate.** Source Serif 4 (display, Quiet confidence).
**Voice slot B's candidate.** Any transitional serif assigned to data via `CONFIG.fonts` override.
**Why they conflict.** Data voice must read as lookup, not as prose. A transitional serif in data voice collapses the reading/lookup distinction and the page loses its information hierarchy.
**Which voice walks to #2.** Data walks to its mono candidate. Display stays the transitional serif.

If a future conflict is observed in a build, add it as Conflict pair 6 following the same format.

---

## 13. Pull-quote detection heuristic

Phase 2 captures testimonials and customer quotes during prospect crawl. Most testimonials are set as uniform cards in the testimonials grid. One or two per page earn pull-quote treatment: extracted from the grid and set as a standalone editorial moment using `.role-display-pullquote`.

Phase 4 identifies pull-quote candidates during composition-plan authoring using the following heuristic.

### Heuristic rules

A testimonial earns pull-quote treatment if **two or more** of the following are true:

1. **Quote length is 8-20 words.** Long enough to land rhetorically, short enough to set at 28-40px without wrapping more than twice. Quotes under 8 words are too slight; quotes over 20 words are too long for display treatment and stay in the card grid.
2. **Quote contains a specific named noun.** "Armando and his father," "the family team," "the 56 reviews." Generic quotes ("great service," "highly recommend") never earn pull-quote treatment regardless of length.
3. **Quote contains a claim the page's persona most wants to foreground.** Neighborhood steady wants family or generational claims. Earned pride wants review-count or longevity claims. Quiet confidence wants precision or correctness claims. Urgent service wants speed or response-time claims. Modern specialist wants technical-depth or specific-method claims.
4. **Quote is first-person and reads aloud naturally.** "I knew we were in good hands" reads well as a pull quote. "They did the thing and it was good" does not.
5. **No other quote on the page already fills the same rhetorical slot.** If two quotes both foreground "family team," only one gets pull-quote treatment; the other stays in the grid.

### Deployment rule

At most one pull quote per page on standard builds (pages with `sections.length <= 6`). Two pull quotes allowed only when the page has `sections.length >= 7` and the two quotes serve different rhetorical slots per Phase 6 Check 10 and `composition-plan-schema.md §4.5`. Never three or more — past two, pull quotes stop reading as editorial moments and start reading as hype decoration.

Pull quotes are placed **between sections**, not within the testimonials grid. A pull quote lives in the editorial gap between services and testimonials, or between testimonials and the promo callout, as a typographic bridge that makes the page read as designed rather than templated.

Voice-layering for the featured pullquote composition (the adjacent elements — eyebrow, title, attribution) is documented in `voiceMap.md §Featured pullquote testimonial — register consumer`. This file governs placement and detection; `voiceMap.md` governs the multi-voice composition around the quote.

### Example (Luna F8 analysis)

Mikala Posley's testimonial — "From day one of meeting Armando and his father I knew we were in good hands. This family team pays extreme attention to details" — is pull-quote-eligible on Luna F8 because: (a) extracting "knew we were in good hands. This family team pays extreme attention to details" hits the 8-20 word window, (b) contains "family team" which is Neighborhood steady's foregrounded claim, (c) reads aloud naturally, (d) no other quote on Luna's page fills the same rhetorical slot. Phase 4 should extract this quote between the services section and the stats section, set it in `.role-display-pullquote`, and leave the full quote in the grid for readers who want the complete testimonial.

---

## 14. Phase 5 generation rules

### Rule 1: Italic signature deployment

Every page whose persona is Quiet confidence, Earned pride, or Modern specialist must deploy the italic-signature micro-interaction **exactly three times** within the main content column, distributed as: once in the hero H1, once in a section H2 in the upper-middle of the page, and once in a section H2 in the lower half. For Neighborhood steady and Urgent service, the minimum is **two deployments** — hero and one additional section H2.

### Rule 2: Italic word selection heuristic

**Italicize the word the persona most wants the reader to hear.** Not any word in the headline. Not a random adjective. The word that carries the sentence's emotional weight for the selected persona.

- Quiet confidence: precision words. "Done *right*." "Wired *to code*." "Built *correctly*." Never emotional words.
- Earned pride: claim words. "*56* five-star reviews." "*Three* generations." "*Fifty* years." Prefer numerals or longevity words.
- Neighborhood steady: identity words. "One *family team*." "Our *neighbors*." "*Leesburg* painters." Prefer noun phrases that name relationships or place.
- Urgent service: speed words. "*Same-day* quotes." "*30-minute* response." "Call *now*." Prefer urgency or temporal words.
- Modern specialist: method words. "*Infrared* diagnosis." "*Spray-finished* cabinets." "*Laser-leveled* installation." Prefer technical-method words that claim specialization.

**Banned italic selections** (apply across all personas):

- The business name if it already appears emphasized elsewhere on the page.
- Generic adjectives ("great," "excellent," "quality").
- Imperative verbs in contact/CTA zones ("Tell us," "Call today") — those read as pull quotes, not signatures.
- Price numerals in italic — reads as pull quote, not signature.
- The word "not" when it's doing rhetorical negation work (keep "not" in roman; italicize the word *after* it that carries the redefined meaning).

Phase 6 Check 9 verification is soft — automated check cannot reliably judge whether "family team" is the right word for Neighborhood steady vs. some other word. The check confirms one italic span exists per H1 and H2 at the specified distribution; human review at the Phase 4 approval gate confirms word selection is correct.

### Rule 3: Eyebrow deployment

Eyebrow labels (`.role-data-eyebrow`) are used to mark editorial transitions, not to decorate every section. Deploy on **at most 3 sections per page** (Phase 6 Check 3), and only on sections that:

1. Introduce a new information mode (narrative → data, services → testimonials, marketing → contact), OR
2. Anchor a location claim (e.g., "LEESBURG · CENTRAL FLORIDA" on hero).

**Service grids, FAQ sections, and contact forms do not take eyebrows** (Phase 6 Check 4). Testimonials and stats sections may take eyebrows; if both appear on the same page, only one gets one. The hero location-claim eyebrow always counts against the budget.

Register assignment (`--primary` loud wayfinding vs `--mute` quiet meta) follows §4 Mono eyebrow system. `composition-plan.json` declares the register per-eyebrow via `eyebrowDeployments[].register`.

### Rule 4: Stats watermark numbering

Covered in §7 StatRow. Summary: watermark and filled numeral render the same stat value; Phase 6 Check 11 is unfalsifiable by construction because `composition-plan.json` carries a single `value` field that Phase 5 emits into both positions.

### Rule 5: Pull-quote deployment

Apply the pull-quote detection heuristic (§13). At most one pull quote per standard page; at most two when `sections.length >= 7` and the quotes serve different rhetorical slots.

Pull quotes live between sections, not inside testimonials grids. Set in `.role-display-pullquote`. Voice-layering for the adjacent composition documented in `voiceMap.md`.

### Rule 6: Lede paragraph deployment

The first paragraph of the hero subhead, the first paragraph of the prep/process editorial section, and the first paragraph of the contact section get `.role-display-lede` treatment — 20-24px, display-family regular weight, line-height 1.5 — instead of standard `.role-body-paragraph` treatment.

This is a small composition move with big rhythm effect. Without lede treatment, every paragraph on the page reads at the same size and weight and the page flattens. With lede treatment, the opening paragraph of each major section has a visible "breath" before the body copy begins.

**Not every section gets a lede.** Service cards do not have ledes. FAQ answers do not have ledes. The lede is reserved for sections where the reader is entering a new reading surface and needs a transition into the body.

### Rule 7: Minimum display-scale moment per page

Every page must contain at least one `.role-display-*` element with computed `font-size ≥80px` on desktop, `≥56px` on mobile (Phase 6 Check 8). If the page has no H1 (rare — only on some service sub-pages) and no stats watermark, Phase 5 must add a display-scale moment (typically a pull quote or a large callout numeral) to satisfy this minimum.

Rationale: the display moment is what separates an editorial page from a template. Without one, the page reads as "nice design," not "someone designed this."

### Rule 8: Mobile watermark breakpoint

Covered in §9 Mobile scaling rules. Per-persona selection: (a) reduced-opacity-behind for Quiet confidence and Modern specialist, (b) corner-positioned for Neighborhood steady and Earned pride, (c) dropped for Urgent service. Phase 6 Check 13 verifies.

### Rule 9: Voice-role compatibility

- Body copy never uses `--font-display`. Never. Including "elegant body" variants. The one exception is `.role-display-lede`, which uses `--font-display` at reading sizes for the specific rhythmic purpose named in Rule 6.
- Data voice never appears in H1 or H2. Data is metadata; headings are language. If a page seems to need a "data heading" (e.g., "56 FIVE-STAR REVIEWS" as a section header), use `.role-display-section` with `.role-data-eyebrow` above it instead.
- Display voice never appears at sizes below 20px unless it's the italic-signature span nested inside a display-role element.

---

## 15. Phase 6 verification checks

Phase 6 verifies typography compliance before ship. Implementation details live in Phase 6's spec; the checks below are what Phase 6 asserts. Structural vs rendered classification mirrors `composition-plan-schema.md §10`.

### Check 1: Max one italic span per H1/H2 (hard fail — structural)

Every H1 and H2 on every page contains at most one italic span. Hard fail on two or more. Structurally enforced by `composition-plan.json`'s `italicSelections[]` at-most-one-per-headingId invariant.

### Check 2: Eyebrow proximity to H2 (hard fail — rendered)

Every `.role-data-eyebrow` element sits within 24px (vertical margin) of its paired H2. Hard fail on >24px — that means the eyebrow got decoupled from its H2 and reads as a floating label.

### Check 3: Eyebrow count per page (soft fail — structural)

Per-page count of `.role-data-eyebrow` elements is ≤3. Soft fail (warning) on 4+. Structurally enforced by `composition-plan.json`'s `eyebrowDeployments[]` max-length-3.

### Check 4: No eyebrow on banned sections (soft fail — structural)

No `.role-data-eyebrow` element sits above an H2 inside a service grid, FAQ section, or contact form. Soft fail. Structurally enforced by `composition-plan.json`'s `eyebrowDeployments[].sectionId` reference-to-sectionOpener-only invariant.

### Check 5: Service card numeral format (hard fail — rendered)

All numerals inside service cards use `font-variant-numeric: tabular-nums`. Hard fail — tabular numerals are required for numeric grids so columns align.

### Check 6: Body copy font-family check (hard fail — rendered)

No element with `.role-body-*` class computes to a font-family that resolves to `var(--font-display)` or its downstream family. Hard fail on any match — that means a body element got display font applied.

### Check 7: Data voice scale check (hard fail — rendered)

No element with `.role-data-*` class computes to `font-size > 40px`. Hard fail — data voice above 40px reads as display and breaks the three-voice system. Exception: `.role-data-numeral` at 56-72px is intentional stat-cell composition and is not flagged by this check.

### Check 8: Minimum display-scale moment per page (hard fail — structural + rendered)

Every page has at least one element with computed `font-size ≥80px` on desktop viewport (1440) and `≥56px` on mobile viewport (375). Structurally enforced by `composition-plan.json`'s `displayMoment.targetDesktopPx >= 80` and `targetMobilePx >= 56` invariants; Phase 6 verifies rendered size.

### Check 9: Italic word selection (soft fail — structural + human-auth)

For each italic span inside an H1 or H2, the italicized word is flagged against the persona's approved word-class list (precision / claim / identity / speed / method). Soft fail with a warning listing the italicized word and the expected word class. Human review during Phase 4 approval gate is authoritative.

### Check 10: Pull-quote deployment count (hard fail — structural)

Per-page count of `.role-display-pullquote` elements is ≤1 when `sections.length <= 6`, ≤2 when `sections.length >= 7`. Hard fail on higher counts. Structurally enforced in `composition-plan.json`'s `pullQuotes[]` max-length rules.

### Check 11: Stats watermark-numeral consistency (hard fail — unfalsifiable by construction)

For each stats cell, the text content of `.role-display-watermark` equals the text content of `.role-data-numeral` within the same cell. Unfalsifiable by construction in the Composer architecture: `composition-plan.json`'s `statRow.stats[].value` is a single field rendered into both positions. This directly addresses the Luna F8 "04" bug.

### Check 12: Three-voice presence per page (hard fail — structural)

Every page contains at least one `.role-display-*`, at least one `.role-body-*`, and at least one `.role-data-*` element. Hard fail on missing. Structurally enforced by per-page `voicesInUse: ["display", "body", "data"]` invariant in `composition-plan.json`.

### Check 13: Mobile watermark treatment (hard fail — rendered)

On viewport 375, `.role-display-watermark` elements either (a) compute to `font-size ≤100px`, (b) compute to `display: none`, or (c) sit at `position: absolute` with offsets indicating corner placement. Hard fail on watermarks that render at desktop size on mobile.

### Classification summary

- **Structural (unfalsifiable in composition-plan)**: 1, 3, 4, 10, 11, 12.
- **Partial (schema + rendered)**: 8, 9.
- **Rendered only**: 2, 5, 6, 7, 13.

---

## 16. Ornament rule

**Ornament derives from the type system or it doesn't belong.**

This is the single strictest rule in this document. If you're tempted to add a decorative element — a pull-quote mark, a section divider flourish, an underline swash, a drop cap — first ask: *is this expressible in the three-voice system (display / body / data)?* If yes, use the type system. If no, it doesn't belong.

### The rule in practice

A giant decorative `"` glyph in front of a pull quote, drawn in the display face, colored at 40% opacity, positioned absolutely in the upper-left of a card — this is textbook ornament. And it's textbook wrong. The pull quote is already italicized at display scale. The italic display serif is *already* doing the quote-signaling work. The giant `"` is redundant decoration.

Delete it. Let the typography do its job.

### What counts as type-derived ornament

- Hairline rules drawn with CSS borders using palette colors.
- Data-voice text acting as a caption strip.
- Typographic marks set in the display face (en dashes, asterisks, section marks) used *as content*, not as decoration. (Note: em dashes are banned in customer-facing copy per `content-rules.md` Universal GRM rules; this ornament allowance is about structural marks in layout primitives, not in voiced copy.)
- Background gradients that use palette colors.

### What doesn't

- SVG flourishes.
- Decorative glyph overlays.
- Emoji (this skill doesn't use emoji as a rule; exception only if a brand explicitly does).
- Drop caps (unless the brand voice genuinely calls for it).
- Drawn icons (inline SVG icons are fine; icons-as-decoration are not).

### Why this rule exists

Type-derived ornament means every decorative moment on the page is reinforcing the type system rather than competing with it. A page with type-derived ornament reads as more considered than a page with mixed ornament, even when the raw element count is lower. Restraint is the signature.

### Assumptions fail silently

This is the meta-principle that produced the em-color inconsistency earlier in the F5 build. The first pass assumed italic-runs-in-headlines would all follow the same rule implicitly. They didn't. The assumption produced two patterns from one mental model, and nothing caught it because there was no written rule.

**Rule of thumb for this skill.** If a typographic choice is going to appear in more than one place, write it down as a rule in the form "X always does Y." Don't rely on the author remembering. Assumptions fail silently; written rules fail loudly.

---

## 17. Structural HTML contracts

When CSS wrap is insufficient to produce the intended line break, the HTML `<br>` becomes structural, not decorative.

### §17.1 The working example

```html
<p class="hero-sub">
  Weekly service, custom construction, and from-green-to-clean recovery.<br>
  Marion and Lake County. Since 1990.
</p>
```

The `<br>` is structural. The rhetorical structure is two sentences: a services enumeration followed by a regional anchor. CSS measure alone can't produce that break reliably.

### §17.2 The rule

- `<br>` elements in voice-carrying display copy are **structural**. Code comments should mark them as such: `<!-- structural: rhetorical break, do not remove -->`.
- `<br>` elements in body copy or address blocks are **formatting** — flexible, reflowable.
- When generating new voice-carrying copy, identify rhetorical breaks and mark them as structural.

### §17.3 text-wrap: balance vs. structural <br>

`text-wrap: balance` is the generalizable CSS rule for display copy that needs even line distribution. Apply it to all headlines and short display paragraphs.

`balance` works well for 2-line display. For 3+ lines, balance still distributes evenly but does not enforce *rhetorical* structure — a three-line headline with a pivot on the second line may balance into a distribution where the pivot lands mid-phrase. In those cases, structural `<br>` is the guarantee.

Use balance for *comfort*, structural `<br>` for *intent*. When a headline both wants even distribution and has a rhetorical pivot, author the `<br>` for the pivot and let balance handle the rest.

```css
.role-display-hero,
.role-display-section,
.footer-porch-head {
  text-wrap: balance;
}
```

```html
<!-- Structural break: rhetorical pivot between two voice registers -->
<h2 class="role-display-section">
  A 4.2 from 54 reviews.<br>
  <em>And one quote that does the trust work.</em>
</h2>
```

### §17.4 Marker classes

The structural-HTML-contracts principle established in §17.2 generalizes beyond `<br>`. The underlying rule is broader:

> Semantic intent belongs in the layer that can express it correctly; marker classes document the intent for generation-time selection.

`<br>` is §17's reference case because rhetorical breaks happen to live in markup, and CSS has no mechanism for "break here in voice." But plenty of other intent categories fall under the same rule — orientation variants on the SectionOpener, label-scale selection on StatRow. When the behavior genuinely lives in HTML or in a role-class pair, the CSS layer is free to carry an empty marker class that documents *which* HTML pattern is in use, without duplicating or contradicting the behavior.

**Reference implementation — orientation marker for role-class SectionOpener.** Under the role-class framing (§6), orientation is a layout decision that changes spatial arrangement without changing role classes. Phase 5 may carry marker classes to pattern-match on at generation time:

- `.section-opener--orientation-eyebrow-above` — eyebrow stacked above H2 (vertical spacing).
- `.section-opener--orientation-tag-strip-inline` — eyebrow inline beside H2 (horizontal separation).

The modifiers carry zero CSS declarations of their own; the role classes `.role-data-eyebrow` and `.role-display-section` carry all the typography. The marker exists so Phase 5 generation can pattern-match on CSS class (deterministic, fast) rather than on HTML tree shape (fragile, slow). That's the whole job.

**Required comment block.** Marker classes must be documented as no-ops in the CSS file at the site of declaration. Without the comment, the next person to read the file will "fix" the empty classes by adding rules — breaking the pattern in a way that's hard to diagnose after the fact. The canonical comment form:

```css
/* Marker modifiers — intentionally empty. Orientation is HTML-authored
   per typography.md §17 (structural HTML contracts) and §6 (SectionOpener
   role-class framing). These classes exist for generation-time selection
   and self-documentation. Do not add declarations. */
.section-opener--orientation-eyebrow-above,
.section-opener--orientation-tag-strip-inline { /* no-op */ }
```

The comment cites the typography.md sections so the rule is discoverable from the CSS alone.

**When to reach for a marker class.** Any primitive where structural intent is worth selecting on at generation time but the visual behavior already lives in HTML or in role classes. When in doubt, the test is: would giving this class a CSS declaration duplicate or contradict what the HTML or role class already expresses? If yes, marker class. If no, it's a normal modifier — author the CSS.

---

## Appendix A: The exceptions principle

Every documented rule in this skill may have exceptions. Exceptions earn their place under a four-point frame:

1. **Broken outcome.** The rule, applied, produces a measurably bad result. Not "stylistically different" — bad. Unreadable at intended size. Invisible at intended contrast. Undermining the register it's meant to carry.
2. **Bounded context.** The exception is scoped to a specific, named context. Not "whenever it feels right." The em-on-dark exception is scoped to navy backgrounds. The 12px sentence-case attribution is scoped to the Front Porch footer with photo credits.
3. **Written reasoning.** The exception is documented with reasoning that justifies it. "Looks better" is not reasoning. "Uppercase at 12px is unreadable for multi-name photo credits" is reasoning.
4. **Not instance-scoped.** If an exception appears in exactly one place and only one place ever, it is probably a bug dressed as a feature. Genuine exceptions appear in a *class* of places — named, enumerable, reproducible.

Two exceptions meet this bar in the current skill:

- **em-on-dark** (§5 above): broken contrast on navy → italic inherits white → indistinguishable from roman. Scoped to navy backgrounds. Appears in two canonical places (Equine band, Front Porch footer).
- **12px sentence-case data-voice attribution** (`voiceMap.md §Front Porch footer — register consumer`): uppercase at 12px unreadable for multi-name credit strings. Scoped to Front Porch footer photo credits. Typographic in nature (case + tracking + size interaction) — owned here, referenced from voiceMap.md.

A third exception candidate that does NOT meet this bar: italic runs shifting to an accent color in non-dark contexts. No broken outcome (inherit-color italic reads fine on page-base). No bounded context (which sections? why?). No written reasoning beyond "brand voice." The original A Quality Pool homepage had this exception de facto — two headline classes shifted to `--accent`, two inherited. That is the failure mode this principle was written to catch.

**Relationship to the ornament rule and "assumptions fail silently" (§16).** The exceptions principle is the enforcement mechanism for those two rules. The ornament rule says "ornament derives from the type system." Assumptions-fail-silently says "write it down or it drifts." The exceptions principle says "and when you write down an exception, it clears these four points or it doesn't exist."

When authoring a new build and the urge to add an exception appears, apply the four points. If any of them fail, the exception isn't earned. Fix the rule or hold the line.

---

## Appendix B: Tier application — persona-conditional font selection is universal across tiers

**Persona-conditional font selection (§11 Persona-conditional font selection) is universal across every tier the skill ships.** Premium, Professional, Standard: every persona gets its Candidate 1 triple at every tier; paid candidates unlock at Premium via the tier gate in `css-framework.md`, but the free-tier Candidate 1 selection for each persona works at every tier without loss of editorial intent.

This expresses the load-bearing principle at the tier boundary: "Variety across prospects comes from persona variety, not font-selection randomness." Variety is the five personas × three voices persona-conditional matrix. Tiers differentiate on what falls outside that matrix — palette complexity, section density, motion layer, photographic treatment — not on whether the persona's font identity survives to the lower tiers.

The reasoning is floor-level, not ceiling-level. The persona-font identity is not a Premium feature that Professional builds can survive without — it's the thing that makes a skill-generated build read as editorial rather than as competent SaaS. Shipping Professional without persona-conditional font selection means Professional builds don't read as GRM. They read as generic. That erodes the brand floor, not the Premium ceiling, and no tier strategy is worth that trade.

### Where tier variation lives instead

Tiers differentiate on four dimensions, none of them persona-font identity:

| Dimension | Premium | Professional | Standard |
| --- | --- | --- | --- |
| **Palette complexity** | Full 4-axis palette + FP secondary accents where applicable | 3-color reduction | 2-color |
| **Section density** | 8–12 sections with SectionOpener variants | 5–7 sections | 3–5 sections |
| **Animation / motion layer** | Parallax + counted stats + scroll-driven reveals | Fades only | None |
| **Photographic treatment** | Two-axis gradient overlays, full-bleed | Flat crops | Solid-color stand-ins |

The persona-conditional font selection applies at every row. A Standard build on two colors, three sections, no motion, solid-color stand-ins still ships its persona's Candidate 1 display / body / data triple with `ss01` + `ss02` + opsz-pinned discipline where Fraunces is the selected display. That's the point.

### Corollary — universal authoring discipline

The stylistic-set signature (Fraunces `ss01` + `ss02` per §10 Stylistic sets as signature) and the opsz pinning rule apply universally across tiers to whichever persona selects Fraunces. They are discipline rules, not tier features. The persona-conditional tables pick the face; the stylistic sets and opsz pinning are how any Fraunces face is authored at any tier. A tier that drops opsz pinning or the stylistic sets is not a GRM tier.

Alternate serifs (Source Serif Pro, etc.) appearing in place of a persona's Candidate 1 are wrong-stack substitutions that lose the signature even when they look close — they are not tier fallbacks.

---

## Cross-references

- `voiceMap.md` — the three *copy* voices (Closing Table / Saturday Morning / Front Porch) that this file's three *type* voices render. Voice map picks the words; typography picks the fonts, weights, sizes, and rhythm. Featured pullquote voice-layering documented in `voiceMap.md`; pull-quote placement and detection documented here.
- `emotional-arc.md` — the five personas that bias both voice selection and font selection. The persona-conditional font tables in §11 depend on the personas defined there. Persona-signature column keyed to the Composer two-tier architecture per `composition-plan-schema.md §2.1`.
- `css-framework.md` — font-loading strategy, CSS custom property declarations for `--font-display` / `--font-body` / `--font-data`, tier-gate logic, Phase 4 font-selection algorithm that reads this file's candidate tables, `CONFIG.fonts` persona-conditional structure, color-derivation utilities (`derivePrimaryHover()`, `deriveDarkPrimary()`) and sentinel-default system.
- `section-patterns.md` — the specific section layouts that use these role classes.
- `content-rules.md` — pattern templates (headlines, CTAs, service descriptions) produced in the voices defined in `voiceMap.md` and set in the type system defined here; Universal GRM rules including the em-dash ban in customer output.
- `anti-slop-rules.md` — Rule E6 (no hardcoded brand-dependent defaults) governs the color-derivation hardening that makes `brandPalette.darkPrimary` sentinel-safe.
- `profile-schema.md` — `brandPalette` raw swatches consumed by Phase 5 for `--font-data` color register assignment; `photoInventory[].eligibleRoles` consumed for photo assignment.
- `composition-plan-schema.md` — `signatureMicroInteraction` (Tier 1) and `microInteractions` (Tier 2) architecture; `eyebrowDeployments[].register` field that consumes the two-register system from §4; `statRow.stats[].value` field that makes Check 11 unfalsifiable.
- `SKILL.md` Phase 4 — design approval workflow that selects persona and font families.
- `SKILL.md` Phase 5 — section generation workflow that deploys role classes, italic signatures, eyebrows, pull quotes, and ledes per the rules above.
- `SKILL.md` Phase 6 — verification workflow that runs the 13 checks in §15.
- `COMPOSER_BRAIN.md §1` — authoritative anchor for the load-bearing principle.
- `COMPOSER_BRAIN.md §6 PA.5` — font-loading fallback behavior.

---

## Revision log

### 2026-04-22 — Stage II (d) three-way merge

**Merge sources:**
- **Production baseline.** Composer's pre-merge `references/typography.md` (post Stage II (a) file copy from production + Stage II (b) Wave 1/Wave 2 retrofits and Option C token migrations). F5-era four-tier framing with SectionOpener axis-parameterized primitive and StatRow contrast pair.
- **Design in-flight.** `~/grm-automations/docs/composer-stage-ii-typography-source/typography-patterns.md` (v0.7.2). Three-voice type system with role classes, pull-quote detection heuristic, persona-conditional font tables, nine Phase 5 generation rules, thirteen Phase 6 verification checks.
- **Proposed merge output.** This file.

**Conflicts resolved (twelve):**

1. **A1 SectionOpener framing — Design arbitration.** Axis-parameterized primitive retired in favor of role-class framing (`.role-data-eyebrow` + `.role-display-section` under ≤24px proximity). Composer's orientation-gating insight preserved as §6 orientation prose. Marker-class example in §17.4 updated from `.section-opener--italic-*` to `.section-opener--orientation-*` to illustrate the marker-class concept against the new framing.
2. **A2 voiceMap zone table grouping — auto-resolved.** (Applied in merged voiceMap.md, not here.)
3. **B1 `--ff-*` → `--font-*` token sweep — auto-resolved.** Five pre-merge code-sample references in Composer's typography.md updated: `--ff-mono` → `--font-data` and `--ff-display` → `--font-display` in SectionOpener and StatRow composition examples. Wording otherwise preserved.
4. **B2 four-tier → three-voice framing — auto-resolved.** Design's three-voice system (Display / Body / Data) supersedes Composer's four-tier (Display / Body / Eyebrow / Stat numerals). Composer §1 technical content (scale relationships, ratio reasoning, vw coefficients, min(max) vs clamp) absorbs under §2 Scale relationships. Eyebrow absorbs into `.role-data-eyebrow` / `.role-data-caption` / `.role-data-stat-caption` role classes; Stat numerals absorb into `.role-data-numeral` and `.role-display-watermark` role classes. "Voices don't blend" discipline paragraph preserved in §1.
5. **B3 Fraunces-universal Appendix B rewording — auto-resolved.** Appendix B thesis rewritten from "Fraunces universal across tiers" to "persona-conditional font selection universal across tiers." Tier-differentiation table (palette complexity, section density, animation layer, photographic treatment) preserved verbatim. Stylistic-set and opsz-pinning discipline moved to Corollary as universal authoring rules applying to any Fraunces-selecting persona at any tier.
6. **C1 Anchor-strip pattern — auto-resolved via token-preservation.** (Applied in merged voiceMap.md, not here.)
7. **C2 Three-tier service composition — auto-resolved via token-preservation.** (Applied in merged voiceMap.md, not here.)
8. **C3 Pull-quote trigger — Design arbitration.** Design's 8-20-word + 2-of-5 heuristic wins. Composer voiceMap.md §4's ≥60-word rule retires. `promoted: true` override retires. Merged detection heuristic documented in §13 with persona-specific rhetorical-slot examples. If a future build surfaces need for a testimonial-spotlight editorial moment, it earns its own section type — not built now. `composition-plan-schema.md §4.5` stays as-is (already consistent with Design's heuristic).
9. **C4 Two-register eyebrow color system — auto-resolved via token-preservation.** Composer's two-register rule (loud `--primary` wayfinding vs quiet `--mute` meta) preserved in §4 with role-class modifier syntax (`.role-data-eyebrow--primary` / `.role-data-eyebrow--mute`) to match `composition-plan-schema.md §4.6 eyebrowDeployments[].register: enum('primary' | 'mute')`.
10. **C5 Load-bearing principle deduplication — auto-resolved.** Single canonical statement at the top of the file, citing `COMPOSER_BRAIN.md §1` as authoritative anchor.
11. **C6 Pullquote voice-layering split — auto-resolved.** Placement and detection (Design's Rule 5 + heuristic) live in this file at §13 and §14 Rule 5. Voice-layering composition breakdown (Closing Table eyebrow + Closing Table title with italic counter-phrase + Featured Pullquote at display-italic scale + Mono attribution) lives in `voiceMap.md` with cross-reference to §13 and §14 Rule 5 here.
12. **C7 Marker classes preservation — auto-resolved.** Composer §10.4 marker-class concept preserved at §17.4. Canonical example updated to orientation markers for role-class SectionOpener per A1 resolution.

**Design reviewer signoff.** Checkpoint 1 q1 follow-up, plus Stage II (d) arbitration on A1, B3, C3 — dated 2026-04-22. Design's signoff is the Stage II (d) arbitration response, not a separate file.

**Sentinel check (brain §12 Risk 3).** Rule E6 (color-derivation hardening, `anti-slop-rules.md` line 739) and `derivePrimaryHover()` / `deriveDarkPrimary()` / `#FF00FF` magenta sentinel (`css-framework.md` lines 194, 200, 385, 439) intact in their home files. Stage II (d) merge touches only `typography.md` and `voiceMap.md`; both of those home files unchanged by this merge.

---

## Version

v1.0 — Stage II (d) merge output, 2026-04-22. Supersedes Composer's pre-merge `references/typography.md` (production F5-era + Wave 2 retrofits) and archives `composer-stage-ii-typography-source/typography-patterns.md` (Design in-flight v0.7.2) as merge-input sources. Canonical authority for Composer typography from this point forward.

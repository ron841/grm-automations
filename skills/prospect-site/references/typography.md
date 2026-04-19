# typography.md

Rules for the GRM site-generator skill. Authored from the F5 / A Quality Pool typography pass, revised post-Code review.

---

## 0. Naming convention (meta-rule)

All typographic primitives in this skill are named in three layers:

1. **Role name** — what the primitive *is* in the system. `SectionOpener`, `AnchorStrip`, `StatRow`, `FeaturedPullquote`, `TagStrip`. Role names are skill-level and stable across brands.
2. **Semantic alias** — what the primitive *does* on a given page. `services-header`, `reviews-header`, `equine-opener`. Semantic aliases are per-section and readable; they map onto role names 1:1.
3. **Instance override** — what the primitive *tweaks* in one specific place. A class modifier, a CSS custom property override, a scoped variant. Overrides absorb per-section specificity without polluting the role name.

The role-alias-override layering is the answer to the readability-vs-consolidation tradeoff. Role names keep the system coherent; semantic aliases keep the HTML readable; instance overrides keep per-section tweaks from fracturing the primitive.

When reading this document, treat every primitive name (SectionOpener, StatRow, etc.) as the role name. Semantic aliases and overrides are authorial.

---

## 1. Scale relationships

Typography at the scale of a site — not a single page — is a relationship problem, not a sizing problem. The question is never "how big should this be" in isolation. It's "what ratio does this hold to the things around it."

### The four tiers

Every page in this skill carries four typographic tiers. Each has a job.

1. **Display.** Hero headlines, section openers, pull quotes. The loudest moments. Fraunces, variable-weight, variable-opsz. Scales by viewport.
2. **Body.** Paragraphs, descriptions, card copy. Inter. 15–17px at comfortable line-height. Reads, not performs.
3. **Eyebrow.** Mono tier. JetBrains Mono. 9–11px, uppercased, tracked. Wayfinding. Precise.
4. **Stat numerals.** Display face, set at a scale the display headlines aren't using. Paired with a mono caption that does the explaining.

The tiers don't blend. A headline doesn't get eyebrow tracking. Body copy doesn't get mono capitals. Stat numerals don't get body weight. The *job* of each tier is what keeps the system legible. When a designer reaches for one tier to do another tier's work — say, italicizing a headline in a "callout color" to make it feel like an eyebrow — the system flattens. Don't do that.

### Ratio reasoning

Pick a ratio and commit. The A Quality Pool homepage uses roughly a 1.25 scale across the body tiers and a looser, more expressive scale across the display tier:

- Body: 13px → 14px → 15px → 16px → 17px → 18px italic → 19px italic. Most transitions are 1-2px. The body tier is tight on purpose — reading comfort lives in small steps.
- Display: 28px → 32px → 42px → 48px → 56px → 88px → 148px. Sparser and more expressive. Display type is a performance, not a conversation.
- Eyebrow: 9px → 10px → 11px. Three sizes total. Don't invent more.

The ratio isn't mathematical in the Fibonacci/modular-scale sense — it's tonal. Moves between sizes should feel like moves in a melody. If two tiers feel the same, one of them is wrong.

### vw coefficients

Display type scales with vw. Coefficients for this skill cluster in 7–9vw for primary display, 5–6vw for secondary display, 3–4vw for tertiary. These are authorial ranges, not mathematical constants — hero headlines lead at 8vw; section openers step down to 5–6vw; pullquotes sit at 3–4vw. Brands with a quieter voice may center their coefficients a point lower; brands with louder voice a point higher. The range holds across the builds this skill has produced.

### min(max()) vs. clamp() — viewport-range-aware authoring

`clamp(min, preferred, max)` is the obvious tool for responsive type. It's also a trap.

A headline with `clamp(56px, 7.5vw, 104px)` ceilings out at 1386px of viewport. At 1440px, 1600px, 1920px — every common desktop width clients actually view a production site on — the type size is frozen at 104px while the canvas keeps growing. The headline reads proportionally lighter at 1920px than at 1386px. Editorial at preview width, "dramatic website" at production width.

The fix is to stop thinking about clamp as "a value between two bounds" and start thinking about it as "a function whose output must still feel right at the viewport the client will actually use." For display type, that usually means:

```css
font-size: min(148px, max(56px, 8vw));
```

`max(56px, 8vw)` is the live scaling relationship. `min(148px, ...)` is the ceiling, positioned deliberately above the "real" desktop range so the scaling is still active at 1440–1920px, but guards against runaway sizing at 4K+ displays.

**Rule.** For display type that must carry visual weight across the common desktop range, set the ceiling above 1920px × (vw coefficient). For the 8vw rule above, that's 8vw × 1920 = 154px — pick 148–160 as a ceiling.

Use `clamp()` for body type where the scaling range is narrow and the ceiling is meaningful. Use `min(max())` for display type where the ceiling exists only to guard against 4K surprises.

---

## 2. Italic discipline

Italic is voice, not decoration.

### One italic run per headline

Every headline gets at most one italic run. "*Central Florida.*" "*One pool phone number.*" Each headline picks the phrase that carries the emotional weight and italicizes that phrase. Two italic runs per headline is a tell — the designer didn't commit to which phrase mattered most.

This rule generalizes. Pick the phrase. Italicize it. Move on.

### em inherits color (the rule, codified)

Headline italic runs inherit the headline's color. They do not shift to an accent color. Italic is the shape move; color shift would be a second, redundant move.

```css
.hero-headline em,
.services-title em,
.reviews-title em,
.equine-headline em {
  color: inherit;
  font-style: italic;
  font-weight: 300;
}
```

Weight 300, because a lighter italic weight distinguishes the italic run from the roman run without requiring a color change.

**One exception, two canonical locations.** Italic runs inherit color *unless the headline color and italic emphasis produce insufficient contrast*. The one exception is italic on a dark navy background, where inherited white italic is indistinguishable from roman. The exception appears in two canonical places on the A Quality Pool homepage: the Equine navy band and the Front Porch footer. Both are navy backgrounds, both use `--accent` for italic runs. Same exception, two instances.

No other exceptions. A "brand accent" color shift on italic runs in non-dark contexts is the failure mode this rule was written to prevent.

### Body italic

Body italic runs always inherit color and italic weight. They're a typographic pause, not a voice move. The body tier doesn't get the italic-as-voice treatment — that's reserved for display.

```css
.signature-desc em,
.op-card-desc em {
  font-style: italic;
  color: inherit;
}
```

### Italic pullquote sizing

When a pullquote is set in italic Fraunces at display scale, the size lives in its own tier between headline and body:

- Featured pullquote: 30–44px, weight 300, italic.
- Review card quote: 16–18px, weight 300, italic.
- Anchor-strip pullquote: 22–28px, weight 300, italic.

The italic pullquote is the one body-adjacent moment that gets display treatment. It's a voice pivot — the page steps from information-delivery mode into testimony mode, and the italic at display size signals that pivot before the reader's brain parses the words. Don't mix italic pullquote with decorative quote marks; the italic does the quote-signaling on its own. (See the ornament rule.)

---

## 3. Mono eyebrow system

The mono tier is where typography becomes information architecture.

### Sizing and tracking

- 11px + 0.14em tracking — section eyebrows, the loudest mono register.
- 10px + 0.14em tracking — section tags, operational tags, stat labels in bright context.
- 9px + 0.18em–0.2em tracking — captions, photo credits, quiet meta.
- Case: always uppercase (one explicit exception; see §5 in voiceMap.md). Tracking expands to compensate for the visual tightness of caps. At 9px, 0.2em tracking; at 11px, 0.14em. Smaller sizes need more tracking.

### Color — two registers, not one

A single mono color flattens the tier. The loud register (`--primary` in the palette — the bright blue) carries wayfinding weight: section eyebrows, navigation phone, CTAs. The quiet register (`--mute` — a neutral gray) carries meta: photo captions, dates, credits, secondary mono lines in paired layouts.

```css
.eyebrow-loud { color: var(--primary); }  /* wayfinding */
.eyebrow-quiet { color: var(--mute); }    /* meta */
```

**The bug this rule fixes:** in the first pass of the A Quality Pool homepage, every mono element used `--primary`. The tier had no quiet register. Introducing `--mute` as a secondary mono color gave the tier an inside voice, which let the loud register actually carry weight.

### Placement

Eyebrows always precede their headline. 12–22px of margin between eyebrow and headline — enough gap to read as a distinct tier, close enough to read as paired. Never use eyebrows as post-headline captions; that's a different typographic move entirely (the caption pattern) and it uses the quiet register.

---

## 4. SectionOpener primitive

A primitive, not a recipe.

**Composition:** mono eyebrow + display headline + optional italic counter-phrase.

```html
<div class="services-header">
  <div class="services-eyebrow">The full pool environment</div>
  <h2 class="services-title">Eight services. <em>One pool phone number.</em></h2>
</div>
```

```css
.services-eyebrow {
  font-family: var(--ff-mono);
  font-size: 11px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--primary);
  margin-bottom: 14px;
}
.services-title {
  font-family: var(--ff-display);
  font-size: clamp(44px, 5vw, 56px);
  color: var(--darkmuted);
  line-height: 1.05;
  letter-spacing: -0.025em;
  font-weight: 400;
}
.services-title em {
  color: inherit;
  font-style: italic;
  font-weight: 300;
}
```

### Skill-level parameters

The SectionOpener primitive is parameterized on four axes at the skill level:

- **eyebrow size** — 10px or 11px
- **headline scale tier** — section-opener scale, equine scale, featured scale
- **italic placement** — inline inside the headline, on its own line, or absent
- **orientation** — eyebrow above headline, or tag strip inline (for numbered service patterns)

When generating a new section opener, pick the parameters; don't invent a new pattern.

### F5 instances (canonical examples)

The parameters above produce four instances on the A Quality Pool homepage. These are reference implementations, not skill-level enumerations — future brands may produce different instance counts from the same parameter grid.

- **Services header** — mono eyebrow above, italic counter-phrase inline.
- **Signature section** — mono tag strip + large Fraunces headline, no italic.
- **Reviews header** — mono eyebrow, italic counter-phrase on new line.
- **Equine band** — mono eyebrow, two-line headline with italic on second line (navy background; italic takes `--accent`).

### TagStrip variant (signature + operational)

Tag strips sit above a bordered content block and read as an index entry rather than a prose opening. Used for numbered service sections, case studies, multi-part compositions. The tag strip itself is mono, full-bleed across the card top, with a primary color left-label and a mute color right-label.

```css
.signature-tag {
  padding: 14px 36px;
  background: var(--page);
  border-bottom: 1px solid var(--line);
  display: flex;
  justify-content: space-between;
  font-family: var(--ff-mono);
  font-size: 10px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--primary);
}
.signature-tag .mute { color: var(--mute); }
```

This is the strongest structural motif in the system. When in doubt about how to frame a content block, reach for the tag strip.

---

## 5. StatRow — contrast pair

Large display numerals + small mono labels. The contrast isn't decoration — it's the whole content of the stat row.

```css
.hero-stat-num {
  font-family: var(--ff-display);
  font-size: 48px;
  color: var(--darkmuted);
  font-weight: 400;
  line-height: 1;
  font-variation-settings: 'opsz' 48;
  letter-spacing: -0.02em;
}
.hero-stat-label {
  font-family: var(--ff-mono);
  font-size: 9px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--mute);
  margin-top: 10px;
}
```

### Rules

- Numeral scale must be ≥4× the label scale. At 48px / 9px, that's 5.3×. At 32px / 10px, 3.2× — not enough; the tier collapses.
- Numeral weight should be 400 or lighter. Bold numerals at display scale feel like pricing tables, not editorial. The serif silhouette carries the weight.
- Label color lives in the quiet mono register (`--mute`). Loud labels would fight the numerals.
- Hairline dividers between stats on desktop echo the meta-grid rhythm elsewhere on the page. `border-left: 1px solid var(--line)` on every stat except the first.

### Mobile

On mobile, stat rows stack vertically with horizontal hairline dividers between. Numeral scale drops to 36–42px, label stays 9px. Don't shrink the label to maintain proportion — the label is already at legibility floor.

---

## 6. Body measure and line-height

### Measure

Cap paragraph width at **56–62 characters**. Inside cards: 44–48ch. Italic display pullquotes: 20–28ch for visual drama.

The `ch` unit is how to author this. Not px. Px doesn't survive font changes; ch does.

### Line-height

- Body paragraphs: **1.65–1.7**. Never below 1.6.
- Display headlines: **0.98–1.12**. Display wants tightness.
- Italic pullquotes: **1.2–1.4**. Middle ground.
- Eyebrow / mono: **1.45–1.8**. Mono wants air between lines at small caps.

### When measure and wrap collide

See the structural-HTML-contracts rule. If a CSS measure produces an ugly wrap in compound phrases, the fix is to widen the measure, not to fight the browser's wrap algorithm with `hyphens: manual`. The browser's wrap is doing its job; the measure was wrong.

---

## 7. Mobile scaling rules

Mobile is not desktop-shrunk-down. Mobile is its own typographic problem.

### H1 scaling — aggressive, not proportional

At narrow viewports, the H1 should be *more* prominent relative to its surrounding content than on desktop. The hero photo often disappears on mobile, the CTA bar pins to the bottom of the viewport, and the headline becomes the single most important visual on the screen.

**Rule:** `clamp(44px, 9vw, 64px)` minimum. Don't design mobile H1s at 32px "to save space." The headline earns the space.

### Stat-row stacking

At tablet breakpoints (980px), stat rows stay in three columns but tighten. At phone breakpoints (540px), stat rows stack vertically and each stat gets a thin horizontal divider below it. Don't maintain three-column stat rows at phone widths; the numerals compress below tier-legibility.

### Body measure adaptation

At mobile, `max-width: 56ch` naturally narrows because the viewport is narrower than 56 characters of body type. No explicit mobile override needed for measure; the constraint is self-enforcing.

### Padding

Mobile padding on sections: `24px` horizontal, `48–64px` vertical. Desktop: `40–56px` horizontal, `72–88px` vertical. Vertical padding carries more weight on mobile because the viewport is taller-than-wide and vertical rhythm is what the reader experiences.

---

## 8. Font loading discipline

Fraunces is a variable font. Treat the axes deliberately.

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
.hero-headline {
  font-size: min(148px, max(56px, 8vw));
  font-variation-settings: 'opsz' 96;
}
@media (max-width: 720px) {
  .hero-headline {
    font-variation-settings: 'opsz' 56;
  }
}
```

**Heuristic.** If the scaled range of a display element spans 2× or more, override opsz at the breakpoint where the rendered size drops more than 30% below the desktop pin. Pick a mobile opsz value that approximates the rendered mobile size. Single breakpoint override is usually enough; three-step opsz ladders are rarely justified.

### Stylistic sets as signature

Fraunces's `ss01` (single-story `a`) and `ss02` (softer `g`) applied globally to every display element is the one typographic signature move in this system. It's a small detail — most readers won't notice consciously. But it distinguishes the display face from every Fraunces-default site on the web.

```css
.hero-headline, .services-title, .equine-headline, /* etc */ {
  font-feature-settings: "ss01" 1, "ss02" 1;
}
```

**Rule of thumb on stylistic sets:** pick one or two and apply consistently. Three or more starts to feel like showing off. The restraint is the signature.

### Loading

Use Google Fonts or a self-hosted variable font file. `font-display: swap` on all faces. Preconnect to the font origin. Don't load weights you won't use.

---

## 9. Ornament rule

**Ornament derives from the type system or it doesn't belong.**

This is the single strictest rule in this document. If you're tempted to add a decorative element — a pull-quote mark, a section divider flourish, an underline swash, a drop cap — first ask: *is this expressible in Fraunces, Inter, or JetBrains Mono?* If yes, use the type system. If no, it doesn't belong.

### The rule in practice

A giant decorative `"` glyph in front of a pull quote, drawn in the display face, colored at 40% opacity, positioned absolutely in the upper-left of a card — this is textbook ornament. And it's textbook wrong. The pull quote is already italicized at display scale. The italic display serif is *already* doing the quote-signaling work. The giant `"` is redundant decoration.

Delete it. Let the typography do its job.

### What counts as type-derived ornament

- Hairline rules drawn with CSS borders using palette colors.
- Mono text acting as a caption strip.
- Typographic marks set in the display face (em dashes, en dashes, asterisks, section marks) used *as content*, not as decoration.
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

**Rule of thumb for this skill:** if a typographic choice is going to appear in more than one place, write it down as a rule in the form "X always does Y." Don't rely on the author remembering. Assumptions fail silently; written rules fail loudly.

---

## 10. Structural HTML contracts

When CSS wrap is insufficient to produce the intended line break, the HTML `<br>` becomes structural, not decorative.

### The working example

```html
<p class="hero-sub">
  Weekly service, custom construction, and from-green-to-clean recovery.<br>
  Marion and Lake County. Since 1990.
</p>
```

The `<br>` is structural. The rhetorical structure is two sentences: a services enumeration followed by a regional anchor. CSS measure alone can't produce that break reliably.

### The rule

- `<br>` elements in voice-carrying display copy are **structural**. Code comments should mark them as such: `<!-- structural: rhetorical break, do not remove -->`.
- `<br>` elements in body copy or address blocks are **formatting** — flexible, reflowable.
- When generating new voice-carrying copy, identify rhetorical breaks and mark them as structural.

### text-wrap: balance vs. structural <br>

`text-wrap: balance` is the generalizable CSS rule for display copy that needs even line distribution. Apply it to all headlines and short display paragraphs.

`balance` works well for 2-line display. For 3+ lines, balance still distributes evenly but does not enforce *rhetorical* structure — a three-line headline with a pivot on the second line may balance into a distribution where the pivot lands mid-phrase. In those cases, structural `<br>` is the guarantee.

Use balance for *comfort*, structural `<br>` for *intent*. When a headline both wants even distribution and has a rhetorical pivot, author the `<br>` for the pivot and let balance handle the rest.

```css
.footer-porch-head,
.services-title,
.reviews-title,
.equine-headline,
.hero-headline {
  text-wrap: balance;
}
```

```html
<!-- Structural break: rhetorical pivot between two voice registers -->
<h2 class="reviews-title">
  A 4.2 from 54 reviews.<br>
  <em>And one quote that does the trust work.</em>
</h2>
```

---

## Appendix A: The exceptions principle

Every documented rule in this skill may have exceptions. Exceptions earn their place under a four-point frame:

1. **Broken outcome.** The rule, applied, produces a measurably bad result. Not "stylistically different" — bad. Unreadable at intended size. Invisible at intended contrast. Undermining the register it's meant to carry.
2. **Bounded context.** The exception is scoped to a specific, named context. Not "whenever it feels right." The em-on-dark exception is scoped to navy backgrounds. The 12px sentence-case attribution is scoped to the Front Porch footer with photo credits.
3. **Written reasoning.** The exception is documented with reasoning that justifies it. "Looks better" is not reasoning. "Uppercase at 12px is unreadable for multi-name photo credits" is reasoning.
4. **Not instance-scoped.** If an exception appears in exactly one place and only one place ever, it is probably a bug dressed as a feature. Genuine exceptions appear in a *class* of places — named, enumerable, reproducible.

Two exceptions meet this bar in the current skill:

- **em-on-dark** (§2 above): broken contrast on navy → italic inherits white → indistinguishable from roman. Scoped to navy backgrounds. Appears in two canonical places (Equine band, Front Porch footer).
- **12px sentence-case mono attribution** (voiceMap.md §5): uppercase at 12px unreadable for multi-name credit strings. Scoped to Front Porch footer photo credits. Typographic in nature (case + tracking + size interaction) — owned here, referenced from voiceMap.md.

A third exception candidate that does NOT meet this bar: italic runs shifting to an accent color in non-dark contexts. No broken outcome (inherit-color italic reads fine on page-base). No bounded context (which sections? why?). No written reasoning beyond "brand voice." The original A Quality Pool homepage had this exception de facto — two headline classes shifted to `--accent`, two inherited. That is the failure mode this principle was written to catch.

**Relationship to the ornament rule and "assumptions fail silently" (§9).** The exceptions principle is the enforcement mechanism for those two rules. The ornament rule says "ornament derives from the type system." Assumptions-fail-silently says "write it down or it drifts." The exceptions principle says "and when you write down an exception, it clears these four points or it doesn't exist."

When authoring a new build and the urge to add an exception appears, apply the four points. If any of them fail, the exception isn't earned. Fix the rule or hold the line.

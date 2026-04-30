# CSS Framework Reference

Part of the prospect-site skill v0.8. Loaded by Phase 5 at the START of site generation, before any other CSS or HTML is written. Every other reference file depends on the tokens, variables, and primitives defined here.

This file owns:

1. The full CSS custom property system (section spacing, colors, typography, breakpoints)
2. Font loading strategy and the typography scale
3. Global reset and base styles
4. Shared animation keyframes used across sections
5. Tier-specific token overrides (Premium, Professional, Standard)
6. Accessibility defaults including reduced-motion handling
7. The vanilla JS animation toolkit (six animation primitives plus three supporting utilities)

Everything in this file gets written to `style.css` at the top, before any section-specific CSS. The JS primitives get written to `script.js` at the top, before any section-specific handlers.

---

## How Phase 5 uses this file

When Phase 5 begins site generation, it reads `profile.json` to determine tier, primary and accent colors, heading font family, hero mode, and which sections are rendering. Then it writes `style.css` in this order:

1. Font loading (`@import` or `<link>` in `<head>`)
2. CSS custom properties (`:root` block with all tokens, tier-specific overrides)
3. Reset and base styles
4. Shared keyframes
5. Hero mode CSS (from `hero-patterns.md`)
6. Section CSS (from `section-patterns.md`, in section order)
7. Accessibility and reduced-motion overrides

And writes `script.js` in this order:

1. DOMContentLoaded wrapper
2. IntersectionObserver setup for scroll-reveal
3. Animation primitives from the toolkit below (only the ones this build needs)
4. Event bindings and initialization

Sections that do not render on a particular build do not get their CSS included. Same for JS primitives. A build with no before/after gallery does not include the `beforeAfterCompare` primitive in `script.js`. Keep the output lean.

---

## CONFIG: The tunable knobs

This is the single source of truth for tier-level design decisions that Ron (or future Ron) might want to swap after seeing real builds. Every other section of this file references these constants by name. Change a value here, the whole framework respects it.

Phase 5 reads these values during site generation and writes them into the final `:root` block. Do NOT hardcode font family strings or tier-specific spacing values elsewhere in the file — always reference the config.

### Tier font pairs

```
// Per typography.md Appendix B: Fraunces + Inter + JetBrains Mono is
// universal across tiers. Tier entries below are structurally identical
// by design — the tier-indexed architecture is preserved for future
// per-tier weight tuning, but font identity is not a tier-differentiation
// dimension. --font-mono lives at :root (tier-invariant per 076ffec), so
// only heading and body appear in these tier entries.
CONFIG.fonts = {
  premium: {
    heading: "Fraunces",
    headingFallback: "\"Playfair Display\", Georgia, serif",
    body: "Inter",
    bodyFallback: "system-ui, -apple-system, sans-serif",
    // Google Fonts URL path segment:
    googleFontsPath: "Fraunces:opsz,wght@9..144,300..800&family=Inter:wght@300..800&family=JetBrains+Mono:wght@400;500"
  },
  professional: {
    heading: "Fraunces",
    headingFallback: "\"Playfair Display\", Georgia, serif",
    body: "Inter",
    bodyFallback: "system-ui, -apple-system, sans-serif",
    googleFontsPath: "Fraunces:opsz,wght@9..144,300..800&family=Inter:wght@300..800&family=JetBrains+Mono:wght@400;500"
  },
  standard: {
    heading: "Fraunces",
    headingFallback: "\"Playfair Display\", Georgia, serif",
    body: "Inter",
    bodyFallback: "system-ui, -apple-system, sans-serif",
    googleFontsPath: "Fraunces:opsz,wght@9..144,300..800&family=Inter:wght@300..800&family=JetBrains+Mono:wght@400;500"
  }
}
```

**When to change these:** after running a real calibration build (T&F Friday morning or any subsequent flagship) and deciding the tier font does not match the visual result on the screen. Edit the relevant `heading` value here, re-run the build, check the result. One-line change.

**On alternate font selections.** Per typography.md Appendix B, Fraunces is universal across tiers and cannot be swapped without losing the GRM typographic signature (ss01 + ss02 + opsz-pinned Fraunces). Historical alternate picks (Playfair Display, Merriweather, DM Sans, Manrope, etc.) are not tier fallbacks — they are wrong-stack substitutions that lose the signature even when they look close. A tier that drops Fraunces is not a GRM tier.

If a calibration build surfaces that Fraunces does not render well for a specific prospect, that is a visual-result concern worth raising with Design — not a per-tier config override. Tier calibration lives in palette complexity, section density, animation layer, and photographic treatment per Appendix B.

The full approved list and banned list live in `anti-slop-rules.md`. Never pick a font outside the approved list without updating that file first.

### Tier section spacing multipliers

```
CONFIG.spacing = {
  premium: {
    sectionMultiplier: 1.17,     // 140px from 120px base
    generousMultiplier: 1.14,    // 160px from 140px base
    heroSize: 84,                // Wide variant headline size
    heroSizeDefault: 64          // Default variant headline size
  },
  professional: {
    sectionMultiplier: 1.0,      // Uses base 120px
    generousMultiplier: 1.0,     // Uses base 140px
    heroSize: 72,                // Wide variant headline size
    heroSizeDefault: 56          // Default variant headline size
  },
  standard: {
    sectionMultiplier: 0.83,     // 100px from 120px base
    generousMultiplier: 0.86,    // 120px from 140px base
    heroSize: 56,                // Wide variant headline size
    heroSizeDefault: 44          // Default variant headline size
  }
}
```

**When to change these:** if Premium feels too roomy or Standard feels too cramped on a real build. Multipliers make global rhythm changes one-line edits.

### Dark section color

```
CONFIG.darkSectionColor = "#0A0A0A"  // Used by stats section and footer
```

Almost certainly never needs changing. Listed here so if it ever does need changing, there is one place to do it.

### Breakpoint

```
CONFIG.mobileBreakpoint = "980px"  // @media (max-width: 980px) for mobile overrides, per typography.md §7
```

Single breakpoint for v0.8. Do not add a tablet breakpoint without updating every section pattern file at the same time.

### Animation durations

```
CONFIG.animation = {
  numberTickerDuration: 2000,       // ms, stats number count-up
  crossfadeInterval: 6000,          // ms, hero crossfade slide cycle
  crossfadeTransition: 2000,        // ms, hero crossfade opacity transition
  marqueeDuration: 40,              // seconds, trust badge marquee loop
  shimmerInterval: 3,               // seconds, button shimmer loop
  scrollRevealDuration: 800         // ms, section fade-up duration
}
```

**When to change these:** if a client calls and says "the numbers count up too fast" or "the slideshow feels sluggish." Every animation timing lives here.

---

## CSS custom property system

Every design token lives as a CSS custom property on `:root`. Section CSS and hero CSS reference these variables by name. Never hardcode a color, spacing value, or font family inside a section rule.

### The complete `:root` block

```css
:root {
  /* ===== Colors ===== */
  /* Primary and accent come from node-vibrant analysis of the logo in Phase 1. */
  /* Dark primary is derived automatically in Phase 4 (HSL lightness reduced by 25%). */
  --color-primary: #2B4C9F;
  --color-primary-rgb: 43, 76, 159;
  --color-accent: #F5A623;
  --color-accent-rgb: 245, 166, 35;
  --color-dark-primary: #0F1A35;
  --color-dark-primary-rgb: 15, 26, 53;
  --color-background: #FAFAF8;
  --color-text: #1A1A1A;
  --color-text-muted: #555555;
  --color-border: rgba(0, 0, 0, 0.08);
  --color-white: #FFFFFF;
  --color-black: #0A0A0A;

  /* ===== Typography ===== */
  --font-heading: "Inter", system-ui, -apple-system, sans-serif;
  --font-body: "Inter", system-ui, -apple-system, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;

  /* Type scale (desktop) */
  --text-hero: 72px;               /* Hero headline, wide variant */
  --text-hero-default: 56px;       /* Hero headline, default variant */
  --text-section-title: 48px;      /* Section titles (services, testimonials, etc) */
  --text-display: 96px;            /* Stats numbers */
  --text-lg: 20px;                 /* Subtitles, large body */
  --text-md: 16px;                 /* Body text, form inputs */
  --text-sm: 14px;                 /* Captions, footer text */
  --text-xs: 12px;                 /* Eyebrows, badges */

  /* Font weights */
  --fw-regular: 400;
  --fw-medium: 500;
  --fw-semibold: 600;
  --fw-bold: 700;
  --fw-extrabold: 800;

  /* Line heights */
  --lh-tight: 1.05;                /* Large display headlines */
  --lh-snug: 1.2;                  /* Section titles */
  --lh-normal: 1.5;                /* Body text */
  --lh-relaxed: 1.6;               /* Long-form paragraphs */

  /* Letter spacing */
  --ls-tight: -1.5px;              /* Large display headlines */
  --ls-snug: -1px;                 /* Section titles */
  --ls-normal: 0;                  /* Body text */
  --ls-wide: 0.3px;                /* Small label text */
  --ls-wider: 1.5px;               /* Uppercase eyebrows, buttons */
  --ls-widest: 2px;                /* Stats section labels */

  /* ===== Section spacing ===== */
  /* Controls vertical rhythm across the whole homepage. Change these */
  /* to adjust global rhythm without touching individual sections.    */
  --space-section: 120px;          /* Default section padding */
  --space-section-compact: 60px;   /* Trust marquee, thin strips */
  --space-section-generous: 140px; /* Stats dark section */
  --space-section-promo: 100px;    /* Featured promotion callout */

  /* ===== Rhythm tokens (typography.md §7) ===== */
  /* Role-named padding tokens that carry the three-level rhythm hierarchy:   */
  /* section > tier > card. Values tokenized from typography.md §7 ranges     */
  /* (desktop 72-88v, mobile 48-64v) by picking specific points on each       */
  /* range. Use these inside sections/tiers/cards authored against the        */
  /* typography rule set; keep the older --space-section tokens for           */
  /* legacy layout sections that predate the rhythm system.                   */
  --section-padding-v: 80px;       /* Section vertical padding (top of range) */
  --tier-padding-v: 56px;          /* Gap between tiers inside a composition */
  --card-padding-v: 32px;          /* Card inner vertical padding */

  /* ===== Container widths ===== */
  --container-narrow: 860px;       /* FAQ, single-column content */
  --container-default: 1100px;     /* Contact, before/after */
  --container-wide: 1280px;        /* Services, testimonials, footer */

  /* ===== Border radii ===== */
  --radius-sm: 6px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 20px;
  --radius-2xl: 24px;
  --radius-pill: 999px;

  /* ===== Shadows ===== */
  --shadow-sm: 0 4px 12px rgba(0, 0, 0, 0.08);
  --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.10);
  --shadow-lg: 0 16px 40px rgba(0, 0, 0, 0.10);
  --shadow-xl: 0 20px 60px rgba(0, 0, 0, 0.15);
  --shadow-2xl: 0 24px 60px rgba(0, 0, 0, 0.25);

  /* ===== Transitions ===== */
  --transition-fast: 0.2s ease;
  --transition-base: 0.3s ease;
  --transition-slow: 0.8s ease;

  /* ===== Z-index scale ===== */
  --z-nav: 100;
  --z-promo-bar: 101;
  --z-mobile-cta: 99;
  --z-modal: 200;
}

/* Mobile breakpoint overrides */
@media (max-width: 980px) {
  :root {
    --text-hero: 44px;
    --text-hero-default: 40px;
    --text-section-title: 32px;
    --text-display: 64px;
    --text-lg: 16px;

    --space-section: 80px;
    --space-section-compact: 40px;
    --space-section-generous: 100px;
    --space-section-promo: 72px;

    /* Rhythm tokens — mobile values from typography.md §7 (48-64v range) */
    --section-padding-v: 56px;
    --tier-padding-v: 40px;
    --card-padding-v: 24px;
  }
}
```

### Variable naming rules

- Color tokens always start with `--color-`
- Typography size tokens always start with `--text-`
- Spacing tokens always start with `--space-`
- Font weight tokens always start with `--fw-`
- Line height tokens always start with `--lh-`
- Letter spacing tokens always start with `--ls-`
- Border radius tokens always start with `--radius-`
- Shadow tokens always start with `--shadow-`
- Transition tokens always start with `--transition-`
- Z-index tokens always start with `--z-`

**Intentional exception: rhythm tokens.** `--section-padding-v`, `--tier-padding-v`, and `--card-padding-v` use the role-named convention from typography.md §0 (role / alias / override) rather than the `--space-` prefix. They are design-layer role names, not general spacing tokens. The `--space-*` prefix remains the rule for every other spacing token on this page.

Never introduce a new token without following this pattern. Never reference a token that doesn't exist yet — Phase 5 should fail the build if it does.

---

## Phase 4 build-time color utilities (Node.js, not browser code)

**These two subsections document Node.js functions that Phase 4 runs at build time to compute CSS variable values. This is server-side code, not browser code.** The functions run once per build, take the raw hex colors from node-vibrant as input, and output the values that Phase 5 writes into the `:root` block of the generated `style.css`.

Placing them in this file because they are conceptually tied to the CSS variable system — they exist to produce correct CSS custom property values. But understand: nothing in `script.js` on a generated site ever calls these functions. They are tooling, not runtime.

### RGB variants for rgba() usage

Several places in the codebase need `rgba(var(--color-primary-rgb), 0.15)` for translucent backgrounds (hover states, focus rings, mesh gradient tints). This requires the color to be available as a comma-separated RGB string, not just a hex value.

Phase 4 must compute BOTH values for primary, accent, and dark-primary when writing the `:root` block:

```
--color-primary: #2B4C9F;
--color-primary-rgb: 43, 76, 159;
```

Use this conversion pattern in Phase 4:

```javascript
function hexToRgbString(hex) {
  const h = hex.replace('#', '');
  const r = parseInt(h.substring(0, 2), 16);
  const g = parseInt(h.substring(2, 4), 16);
  const b = parseInt(h.substring(4, 6), 16);
  return `${r}, ${g}, ${b}`;
}
```

### Deriving dark-primary from primary

The dark-primary is used for the footer background, testimonial author names, FAQ questions, and anywhere the primary color would be too saturated. It's derived automatically from the primary in Phase 4 by reducing HSL lightness by 25 percentage points (or more specifically, taking the primary and pulling it toward near-black).

Use this conversion pattern in Phase 4:

```javascript
function deriveDarkPrimary(hex) {
  // Convert hex to HSL, reduce lightness, convert back
  const h = hex.replace('#', '');
  let r = parseInt(h.substring(0, 2), 16) / 255;
  let g = parseInt(h.substring(2, 4), 16) / 255;
  let b = parseInt(h.substring(4, 6), 16) / 255;

  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  let hVal, sVal, lVal = (max + min) / 2;

  if (max === min) {
    hVal = sVal = 0;
  } else {
    const d = max - min;
    sVal = lVal > 0.5 ? d / (2 - max - min) : d / (max + min);
    switch (max) {
      case r: hVal = (g - b) / d + (g < b ? 6 : 0); break;
      case g: hVal = (b - r) / d + 2; break;
      case b: hVal = (r - g) / d + 4; break;
    }
    hVal /= 6;
  }

  // Reduce lightness by 25% but floor at 8% (near black)
  lVal = Math.max(0.08, lVal - 0.25);

  // Convert back to RGB then hex
  const hslToRgb = (h, s, l) => {
    if (s === 0) return [l, l, l];
    const hue2rgb = (p, q, t) => {
      if (t < 0) t += 1;
      if (t > 1) t -= 1;
      if (t < 1/6) return p + (q - p) * 6 * t;
      if (t < 1/2) return q;
      if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
      return p;
    };
    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;
    return [hue2rgb(p, q, h + 1/3), hue2rgb(p, q, h), hue2rgb(p, q, h - 1/3)];
  };

  const [rOut, gOut, bOut] = hslToRgb(hVal, sVal, lVal);
  const toHex = v => Math.round(v * 255).toString(16).padStart(2, '0');
  return `#${toHex(rOut)}${toHex(gOut)}${toHex(bOut)}`;
}
```

Phase 4 runs both conversions for every build and writes the results directly into the `:root` block.

### Contrast guarantee rules

Hero glass cards and section text must meet WCAG AA contrast (4.5:1 for body text, 3:1 for large text). Phase 6 check 13 verifies this by testing the computed contrast ratio of:

- Hero headline white text over the dark overlay (all hero modes)
- Testimonial quote text over white card background
- Stats number white text over `#0A0A0A` background
- Footer link text over `#0A0A0A` background
- Primary button white text over `var(--color-primary)` background

If any ratio fails, Phase 6 flags the build and suggests either darkening the overlay (hero) or using `--color-dark-primary` instead of `--color-primary` (buttons). It does not auto-fix, it reports.

---

## Typography system

### Font loading strategy

Google Fonts is the approved font source. Self-hosting is deferred — Google Fonts handles `font-display` and variable-font loading correctly.

Phase 5 reads `CONFIG.fonts.[tier].googleFontsPath` per the tier decision from Phase 4 and emits a three-link block in `<head>`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=[googleFontsPath-value]&display=swap">
```

The path value is used verbatim (SKILL.md:580) — no placeholder substitution. The three-font stack (Fraunces, Inter, JetBrains Mono) is universal across tiers per typography.md Appendix B; all three tier `googleFontsPath` values resolve to the same path. Fraunces and Inter use continuous variable-axis ranges (`wght@300..800`); JetBrains Mono uses discrete stops (`wght@400;500`). Weight 300 at the low end is required per typography.md §2's italic-em rule. Don't load weights primitives don't use (typography.md §8).

Fraunces variable paths include the opsz axis (`opsz,wght@9..144,300..800`). Primitives pin opsz per rendered size via `font-variation-settings: 'opsz' [N]` per §8's opsz discipline.

`<link rel="preload">` is NOT emitted. Preconnect + stylesheet with `display=swap` is the pattern — matches Google Fonts' recommended minimum. F5 and every Phase 5 build emit this three-link shape.

### Approved heading font — universal

| Tier         | Primary heading font | Fallback                         | Rationale |
|--------------|---------------------|----------------------------------|-----------|
| All tiers    | Fraunces            | Playfair Display, Georgia, serif | Modern serif with optical sizing and variable weights. Universal per typography.md Appendix B — the typographic signature (ss01 + ss02 + opsz pinning) requires Fraunces across all tiers. |

Per Appendix B, the font stack is universal and is not a tier-differentiation dimension. Tier variation lives in palette complexity, section density, animation layer, and photographic treatment.

### Approved body fonts by tier

| Tier         | Body font | Fallback |
|--------------|-----------|----------|
| All tiers    | Inter     | system-ui |

Inter is the body font for every tier. The heading font changes to signal tier, but the body stays consistent so reading experience is consistent. Do not mix body fonts across tiers — Inter is the only body font in v0.8.

### Banned fonts

Full list in `anti-slop-rules.md`. Summary:

- Roboto (Google default, signals AI-generated)
- Arial / Helvetica as primary (system font fallback only)
- Times New Roman (never, for any reason)
- Open Sans (overused, generic)
- Lato (overused, generic)
- Montserrat (overused, feels like a 2018 template)
- Any cursive, handwriting, or display font

### Type scale usage

The type scale tokens defined in `:root` map to specific section elements. Use them directly in section CSS rather than hardcoding sizes.

```css
.hero-headline {
  font-size: var(--text-hero-default);  /* 56px desktop, 40px mobile */
  font-family: var(--font-heading);
  font-weight: var(--fw-bold);
  line-height: var(--lh-tight);
  letter-spacing: var(--ls-tight);
}

.hero-glass-card--wide .hero-headline {
  font-size: var(--text-hero);  /* 72px desktop, 44px mobile */
}

.services-title {
  font-size: var(--text-section-title);  /* 48px desktop, 32px mobile */
  font-family: var(--font-heading);
  font-weight: var(--fw-bold);
  line-height: var(--lh-snug);
  letter-spacing: var(--ls-snug);
}

.hero-eyebrow {
  font-size: var(--text-xs);  /* 12px always */
  font-weight: var(--fw-semibold);
  letter-spacing: var(--ls-wider);
  text-transform: uppercase;
}
```

Section-specific hardcoded font sizes in `section-patterns.md` and `hero-patterns.md` should be migrated to use these variables in the final polish pass. For v0.7 first build they can stay hardcoded for clarity, but the variables are defined and ready.

---

## SectionOpener primitive

A skill-level typographic primitive that collapses four shipped F5 section-opener variants (services header, reviews header, equine band, signature) into one named pattern parameterized on four axes. Consolidation source: typography.md §4. Naming convention source: typography.md §0. Registered as part of the v0.8 Wave 2 primitive rollout.

The primitive replaces instance-level CSS blocks for each F5 variant — Phase 5 emits one role-named container with the axis-modifier classes that select the instance, rather than authoring `.services-header`, `.reviews-head`, `.equine-eyebrow + .equine-headline`, and `.signature-tag + .signature-headline` as four separate primitives.

### Role, alias, override — naming contract

Per typography.md §0, every primitive in this skill is named in three layers:

1. **Role name** — `section-opener`. Skill-level, stable across brands, never changes. The CSS class in the generated HTML.
2. **Semantic alias** — `services-header`, `reviews-header`, `equine-opener`, `signature-opener`. Per-section and readable. These can survive as additional classes alongside the role name for HTML readability — `class="section-opener ... services-header"` — but the role name is the load-bearing selector.
3. **Instance override** — per-build class modifiers, scoped CSS custom properties, or utility classes that tweak one specific instance without polluting the role name. Not authored at the primitive level; authored by Phase 5 when needed.

Implementations MUST use the role name. Aliases are optional and decorative. Overrides are additive; they never replace role-layer rules.

### Four parameters

Per typography.md §4. Each axis has a fixed enumeration of values. Phase 5 selects one value per axis when emitting an instance.

1. **Eyebrow size** (per typography.md §3 mono tier):
   - `10px` — quieter mono register for reviews, equine, tag-strip
   - `11px` — section-opener loud mono register for services

2. **Headline scale tier** (per typography.md §1 display ladder + ceiling rule):
   - `section` — `clamp(44px, 5vw, 56px)`, secondary display (5vw coefficient), used by services + reviews
   - `equine` — `min(144px, max(56px, 7vw))`, primary display (7vw coefficient), tier-3 Distinctive showcase. Ceiling 144 is rule-compliant per §1 (1920 × 7vw = 134.4 minimum); supersedes F5's pre-rule 128 per the 2026-04-20 scope-doc changelog.
   - `featured` — `clamp(38px, 4vw, 48px)`, tertiary display (4vw coefficient), tier-1 Signature ladder-capped

3. **Italic placement** (per typography.md §2 + §10):
   - `inline` — `<em>` inline inside headline flow
   - `newline` — `<em>` preceded by a structural `<br>` per typography.md §10
   - `none` — no `<em>` in this headline

4. **Orientation** (per typography.md §4):
   - `eyebrow-above` — mono eyebrow above display headline (services, reviews, equine)
   - `tag-strip` — split-flex mono row atop a bordered content block, headline lives inside the content block (signature + operational, per §4 TagStrip subsection)

Phase 5 never invents new axis values. If a new instance needs a value outside the enumeration above, the enumeration is extended in typography.md first; the primitive follows.

### CSS implementation

The CSS below gets written into `style.css` during Phase 5 whenever a build includes at least one section-opener instance. If a build contains zero instances, skip the block to keep output lean.

```css
/* =====================================================================
   SectionOpener primitive (typography.md §4)

   Four axes: eyebrow size | headline scale tier | italic placement |
   orientation. Em-on-dark exception per typography.md §2 + Appendix A
   is scoped to the .section-opener--on-dark modifier. Stylistic-set
   signature (ss01 + ss02) applied at the role-base per §8; inherits
   to display descendants. text-wrap: balance applied to the headline
   per §10.
   ===================================================================== */

/* Role base */
.section-opener {
  font-feature-settings: "ss01" 1, "ss02" 1;
}

/* ----- Elements ----- */

.section-opener__eyebrow {
  font-family: var(--font-mono);
  color: var(--color-primary);
  letter-spacing: 0.14em;
  text-transform: uppercase;
  line-height: 1.45;
  margin: 0 0 14px 0;
}

.section-opener__headline {
  font-family: var(--font-heading);
  color: var(--color-dark-primary);
  line-height: 1.05;
  letter-spacing: -0.025em;
  font-weight: 400;
  margin: 0;
  text-wrap: balance;
}

/* em inherits headline color by default (typography.md §2 rule codified).
   Weight 300 per §2 — the italic is the shape move; color shift would be
   a second, redundant move. Em-on-dark exception handled below. */
.section-opener__headline em {
  color: inherit;
  font-style: italic;
  font-weight: 300;
}

/* ----- Axis 1: Eyebrow size (§3 mono tier) -----
   Gated by orientation per typography.md §4 Axis applicability: applies
   only when orientation=eyebrow-above. The tag-strip-inline orientation
   carries its mono register on the tag-strip component itself, not on
   this axis. Phase 5 generation MUST reject eyebrow-size modifiers on
   tag-strip-inline containers rather than silently emit them. CSS-level
   gating via compound selector below is defense in depth; the
   generation-time contract is the primary enforcement. */
.section-opener--orientation-eyebrow-above.section-opener--eyebrow-11 .section-opener__eyebrow { font-size: 11px; }
.section-opener--orientation-eyebrow-above.section-opener--eyebrow-10 .section-opener__eyebrow { font-size: 10px; }

/* ----- Axis 2: Headline scale tier (§1 display ladder + ceiling rule) ----- */

/* Section scale — services, reviews. Secondary display, 5vw coefficient,
   ladder-capped at 56. Ladder-cap is intentional: section-openers are not
   required to scale past their ladder peak. */
.section-opener--headline-section .section-opener__headline {
  font-size: clamp(44px, 5vw, 56px);
  font-variation-settings: 'opsz' 56;
}

/* Equine scale — tier-3 Distinctive showcase. Primary display, 7vw.
   Ceiling 144: 1920 × 7vw = 134.4 minimum per §1; 144 sits rule-compliant
   and below hero's 148 ceiling for tier-3 < tier-1-primary hierarchy.
   Supersedes F5's pre-rule 128 per 2026-04-20 scope-doc changelog. */
.section-opener--headline-equine .section-opener__headline {
  font-size: min(144px, max(56px, 7vw));
  font-variation-settings: 'opsz' 88;
}

/* Featured scale — tier-1 Signature. Tertiary display, 4vw, ladder-cap 48.
   Ladder-cap intentional per tier-1 Closing-Table-companion intent. */
.section-opener--headline-featured .section-opener__headline {
  font-size: clamp(38px, 4vw, 48px);
  font-variation-settings: 'opsz' 48;
}

/* Marker modifiers — intentionally empty. Italic placement is HTML-authored
   per typography.md §10 (structural HTML contracts). These classes exist for
   generation-time selection and self-documentation. Do not add declarations. */
.section-opener--italic-inline,
.section-opener--italic-newline,
.section-opener--italic-none { /* no-op */ }

/* ----- Axis 4: Orientation ----- */

/* Orientation 4a: eyebrow-above — mono eyebrow sibling to headline.
   Services, reviews, equine. */
.section-opener--orientation-eyebrow-above {
  display: block;
}

/* Orientation 4b: tag-strip — split-flex mono row atop a bordered
   content block. Signature, operational. The tag-strip itself lives
   at the top of the container; the headline lives inside the content
   block below (authored by the block-level primitive in Wave 3).
   Per typography.md §4 TagStrip subsection. */
.section-opener--orientation-tag-strip {
  display: block;
}

.section-opener__tag-strip {
  padding: 14px 36px;
  background: var(--color-background);
  border-bottom: 1px solid var(--color-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--color-primary);
  line-height: 1.45;
}

.section-opener__tag-strip-label {
  /* Default label — left side, loud mono register (--color-primary). */
}

.section-opener__tag-strip-label--mute {
  /* Right-side muted label — quiet mono register (§3). */
  color: var(--color-text-muted);
}

/* ----- Em-on-dark exception (typography.md §2 + Appendix A) -----
   Bounded context: italic runs on navy/dark backgrounds where inherited
   color produces insufficient contrast. Two canonical locations per §2:
   Equine band (tier-3 Distinctive) and Front Porch footer. Front Porch
   footer is not a SectionOpener; Equine is. Scoped via explicit modifier
   .section-opener--on-dark rather than by parent context to keep the
   exception legible and bounded. */

.section-opener--on-dark .section-opener__headline {
  color: var(--color-white);
}

.section-opener--on-dark .section-opener__headline em {
  color: var(--color-accent);
}

.section-opener--on-dark .section-opener__eyebrow {
  color: var(--color-accent);
}

/* ----- Mobile breakpoints (typography.md §7) -----
   §7 authors 980 tablet and 540 phone. Primitive layout transitions land
   at those breakpoints. Mobile-max (980) and desktop-min (981) reconciled
   across css-framework.md per typography.md §7 (commits 83d088a, bef19f2). */

@media (max-width: 980px) {
  .section-opener--headline-section .section-opener__headline {
    font-size: clamp(32px, 5vw, 44px);
  }
  .section-opener--headline-equine .section-opener__headline {
    font-size: clamp(44px, 9vw, 64px);
    font-variation-settings: 'opsz' 56;
  }
  .section-opener--headline-featured .section-opener__headline {
    font-size: clamp(32px, 4vw, 40px);
  }
  .section-opener__tag-strip {
    padding: 12px 24px;
  }
}

@media (max-width: 540px) {
  .section-opener--headline-section .section-opener__headline {
    font-size: 36px;
  }
  .section-opener--headline-equine .section-opener__headline {
    font-size: 56px;
    font-variation-settings: 'opsz' 56;
  }
  .section-opener--headline-featured .section-opener__headline {
    font-size: 32px;
  }
}
```

### TagStrip orientation variant — markup contract

The tag-strip orientation has a specific markup shape. Per typography.md §4, the tag-strip sits atop a bordered content block that contains the headline inside — not above the strip. The block-level container (signature-body, operational-grid, etc.) is a Wave 3 composition primitive; this section specifies only the tag-strip itself.

Markup contract for tag-strip orientation:

```html
<!-- voice-map: closing-table -->
<section class="section-opener section-opener--headline-featured section-opener--italic-none section-opener--orientation-tag-strip">
  <div class="section-opener__tag-strip">
    <span class="section-opener__tag-strip-label">Signature build · 01</span>
    <span class="section-opener__tag-strip-label section-opener__tag-strip-label--mute">Custom pool construction</span>
  </div>
  <!-- Headline renders inside the Wave 3 block-level composition below -->
  <!-- <div class="tier-block"> <h3 class="section-opener__headline">Full design-build, inspected and signed.</h3> ... </div> -->
</section>
```

The tag-strip is full-bleed across the top of the bordered block; the left label carries the section number in the loud mono register (`--color-primary`), the right label carries the section name in the quiet mono register (`--color-text-muted`). Per typography.md §4: "When in doubt about how to frame a content block, reach for the tag strip."

### Voice-map HTML comment requirement

Per voiceMap.md §8 and the 2026-04-20 scope-doc changelog entry pinning the syntax, every generated section-opener instance MUST be preceded by a voice-map HTML comment:

```html
<!-- voice-map: [register] -->
<section class="section-opener ...">
  ...
</section>
```

Values: `closing-table` | `saturday-morning` | `front-porch` | `voice-pivot`. Kebab-case, verbatim from voiceMap §2. One comment per section, emitted at the top of every primitive container.

The comment is mandatory at generation time. Phase 5 MUST emit it when rendering any section-opener instance. The comment is the machine-legible register marker that sets up v0.8.1 register-aware copy generation without locking in the architecture now. In v0.8, copy generation remains register-agnostic per the 2026-04-20 Path A decision; the comment reserves the signal.

Phase 5 enforcement (grep verification that every `.section-opener` container is preceded by a `<!-- voice-map: -->` comment) is a Wave 4 gate concern, not a commit-time rule. This primitive spec defines the contract; the gate enforces it.

### F5 instances as canonical examples

Per typography.md §4's "F5 instances (canonical examples)" subsection: "These are reference implementations, not skill-level enumerations — future brands may produce different instance counts from the same parameter grid."

The four F5 instances map onto the four-axis parameterization as follows. Documentation only — the primitive replaces these instance-level CSS blocks, not duplicates them.

| F5 semantic alias | eyebrow | headline | italic    | orientation    | voice-map      |
|-------------------|---------|----------|-----------|----------------|----------------|
| services-header   | 11px    | section  | inline    | eyebrow-above  | closing-table  |
| reviews-header    | 10px    | section  | newline   | eyebrow-above  | closing-table  |
| equine-opener     | 10px    | equine   | newline   | eyebrow-above  | front-porch    |
| signature         | n/a     | featured | none      | tag-strip      | closing-table  |

The `signature` row marks eyebrow as `n/a` per typography.md §4 Axis applicability: tag-strip-inline orientation has no separate eyebrow element. The mono register that would otherwise be an eyebrow is carried by the tag-strip component itself — its font-size is a property of the tag-strip CSS rules, not this axis. Phase 5 generation MUST reject the eyebrow-size + tag-strip-inline combination rather than silently emit a no-op modifier.

### Phase 5 generation note

When Phase 5 emits a section-opener instance, it selects parameter values based on section purpose. For three-tier service composition (voiceMap.md §2d), the tier determines orientation and register:

- **Signature tier** → `--orientation-tag-strip`, voice-map `closing-table`
- **Operational tier** → `--orientation-tag-strip`, voice-map `saturday-morning`
- **Distinctive tier** → `--orientation-eyebrow-above`, voice-map `front-porch` (if human-voice specialty) OR `saturday-morning` (if operational specialty), per voiceMap.md §2d decision tree

For non-tier section openers (services header, reviews header, nav, promo callout, FAQ, contact), Phase 5 selects axes based on section role and per-section voice-map register declaration.

Register-aware parameter selection happens at the container level per the 2026-04-20 Path A decision — the primitive picks orientation and emits the voice-map comment, but copy inside the container remains register-agnostic in v0.8. Register-aware copy generation is v0.8.1 scope; the voice-map comments this primitive emits are the signal that enables it.

---

## StatRow primitive

A skill-level typographic primitive that renders a contrast pair of display numerals + mono labels — §5's "the contrast isn't decoration, it's the whole content of the stat row." Consolidation source: typography.md §5 plus Design's 2026-04-20 authorial pass. Register ownership: voiceMap.md §2a (Closing Table). Registered as part of the v0.8 Wave 2 primitive rollout alongside SectionOpener.

F5's `.hero-stats` + `.hero-stat-num` + `.hero-stat-label` trio is the canonical reference implementation. The primitive replaces that instance-level pattern with one role-named container and one optional compressed-variant modifier.

### Role, alias, override — naming contract

Per typography.md §0, StatRow follows the role/alias/override layering established for SectionOpener:

1. **Role name** — `statrow`. Skill-level, stable across brands, the load-bearing selector.
2. **Semantic alias** — `hero-stats`, `service-stats`, etc. Per-section and readable. May survive as additional classes for HTML readability.
3. **Instance override** — per-build class modifiers or scoped custom property overrides. Not authored at the primitive level.

### Parameters

Per typography.md §5 and Design's 2026-04-20 authorial pass, StatRow carries one canonical scale with a compressed variant. Not a multi-tier progression.

- **Numeral scale** — canonical 48px (implicit on the base `.statrow`) with a compressed variant `.statrow--numeral-36` for composition-constrained contexts

Per Design: *"StatRow has one scale (48px) with a compressed variant (36px). 48 is editorial default. 36 is the constrained variant — used when a composition can't hold the full cadence. There's no legitimate authorial reason to select [midrange]."* The primitive exposes one variant modifier, not a tier enumeration. Canonical is implicit on the base class; no `.statrow--numeral-48` is authored.

Non-parameters (authorial fixed values):

- **Label scale** — fixed at 9px per §5's "label is already at legibility floor." Not a modifier.
- **Column count** — hardcoded 3-col through desktop and tablet, 1-col only at ≤540px. Per Design's 2026-04-20 rhythm reasoning: StatRow is a three-beat stanza read left-to-right; the 3-col grid holds from desktop through tablet. F5 precedent matches; earlier "3/2/1" scope-doc text was unauthored and is superseded.
- **Register** — Closing Table per voiceMap.md §2a. StatRow always carries the Closing Table typographic signature; register is not parametrized.

### CSS implementation

The CSS below gets written into `style.css` during Phase 5 whenever a build includes at least one StatRow instance. Skip the block if a build contains zero instances.

```css
/* =====================================================================
   StatRow primitive (typography.md §5 + Design 2026-04-20 authorial pass)

   Display numerals + mono labels in a contrast pair. Two-scale model:
   canonical (48px, implicit on base .statrow) and compressed (36px,
   via .statrow--numeral-36 override). 4× ratio rule satisfied at both
   scales against the 9px label floor: 48/9=5.33×, 36/9=4.00×. Mobile
   values preserve the two-tier distinction: canonical → 42 at ≤540px,
   compressed → 36 (holds). Numeral weight 400 default per §5.
   Stylistic-set signature (ss01 + ss02) and opsz pinning inherited
   from typography.md §8 + Appendix B (universal per 6ec0f6d).
   ===================================================================== */

/* Role base — Closing Table register owned (voiceMap.md §2a).
   3-col grid holds through desktop and tablet per Design 2026-04-20.
   Hairline top-border echoes the meta-grid rhythm per §5. */
.statrow {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0;
  padding-top: 28px;
  border-top: 1px solid var(--color-border);
  font-feature-settings: "ss01" 1, "ss02" 1;
}

/* ----- Elements ----- */

.statrow__item {
  padding: 0 24px;
  border-left: 1px solid var(--color-border);
}

.statrow__item:first-child {
  border-left: 0;
  padding-left: 0;
}

/* Numeral — canonical 48px scale applies to the base .statrow (implicit).
   Compressed variant overrides via .statrow--numeral-36 below. */
.statrow__num {
  font-family: var(--font-heading);
  font-size: 48px;                        /* canonical; compressed overrides */
  font-weight: 400;                       /* §5: numeral weight 400 or lighter */
  line-height: 1;
  letter-spacing: -0.02em;
  color: var(--color-dark-primary);
  font-variation-settings: 'opsz' 48;
  margin: 0;
}

.statrow__label {
  font-family: var(--font-mono);
  font-size: 9px;                         /* §5: fixed at legibility floor */
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--color-text-muted);         /* §5: quiet mono register */
  line-height: 1.45;
  margin-top: 10px;
}

/* ----- Numeral-scale variant: compressed -----
   Used when composition constraints — narrow column, secondary section,
   tight vertical rhythm — demand a tighter cadence than canonical 48px
   allows. Per Design 2026-04-20: compressed is a variant of the canonical
   scale, not a "small" tier. 36/9 = 4.00× exactly, at §5's 4× floor.
   opsz pinned per §8. */

.statrow--numeral-36 .statrow__num {
  font-size: 36px;
  font-variation-settings: 'opsz' 36;
}

/* ----- Mobile breakpoint (typography.md §7: 540 phone) -----
   Column stack: 3-col → 1-col at ≤540px. Dividers flip from vertical
   to horizontal. Numeral scales per-variant at the stack breakpoint:
   canonical (48 desktop) → 42 phone per §5's mobile-range ceiling;
   compressed (36 desktop) → 36 phone (already at §5's floor, holds).
   Per-variant mobile preserves the two-tier intent at the breakpoint
   where hierarchy signals work hardest (Design 2026-04-20).

   Specificity resolves the cascade: .statrow__num = (0,1,0);
   .statrow--numeral-36 .statrow__num = (0,2,0). Compressed wins by
   specificity, not by source order, both inside and outside the
   media query. */

@media (max-width: 540px) {
  .statrow {
    grid-template-columns: 1fr;
  }
  .statrow__item {
    border-left: 0;
    border-top: 1px solid var(--color-border);
    padding: 12px 0;
  }
  .statrow__item:first-child {
    border-top: 0;
    padding-top: 0;
  }
  /* Canonical mobile — 42px per §5's mobile-range ceiling (Design 2026-04-20) */
  .statrow__num {
    font-size: 42px;
    font-variation-settings: 'opsz' 42;
  }
  /* Compressed mobile — holds at 36px (already at §5's floor) */
  .statrow--numeral-36 .statrow__num {
    font-size: 36px;
    font-variation-settings: 'opsz' 36;
  }
}
```

### 4× ratio rule — enforcement layers

Per typography.md §5: "Numeral scale must be ≥4× the label scale. At 48px / 9px, that's 5.3×. At 32px / 10px, 3.2× — not enough; the tier collapses."

The rule is a contract between numeral scale and label scale. CSS cannot programmatically enforce a cross-class ratio, so enforcement is layered:

1. **CSS level (defense in depth):** Both authored scales satisfy 4× against the 9px label — canonical 48/9=5.33×, compressed 36/9=4.00×. Mobile values likewise satisfy: canonical 42/9=4.67×, compressed 36/9=4.00×.
2. **Generation-time contract (primary):** Phase 5 MUST reject any StatRow instance that would violate the ratio. Custom numeral scales outside the authored canonical/compressed pair require authorial extension in typography.md §5 before the CSS primitive accepts them.

Same defense-in-depth pattern as SectionOpener's eyebrow-axis gating (816f58a): cascade-level enforcement where possible, generation-time contract primary.

### Column-count behavior

Hardcoded 3-col through desktop and tablet, 1-col at ≤540px. Per Design's 2026-04-20 authorial pass and F5 precedent. Not parametrized.

Design's rhythm reasoning: *"StatRow at 3-col is a line — three beats, read left-to-right, scanned as a stanza. Break the line at tablet into 2+1 and you've invented a new layout — a broken stanza where the third beat hangs alone. 1+1+1 at phone is fine; the eye already expects vertical at phone. 2+1 at tablet is the worst of both — neither line nor stack. Tablet width has the horizontal room to hold three beats. Let it."*

§5 authors the 3-col canonical pattern but does not enumerate alternate column counts. Adding a `--cols-N` modifier axis is deferred to future authorial extension. 4-col, 6-col, or other layouts would require authorial promotion in typography.md before the primitive accepts them.

### F5 instance as canonical example

Per typography.md §4's "F5 instances (canonical examples)" caveat (applies to all primitives): these are reference implementations, not skill-level enumerations. Future brands may produce different instance counts from the same parameter grid.

| F5 semantic alias | numeral scale        | column behavior         | voice-map     |
|-------------------|----------------------|-------------------------|---------------|
| hero-stats        | canonical (implicit) | 3-col → 1-col at ≤540px | closing-table |

F5 ships one StatRow instance (the hero stat row). Additional instances (service-tier stats, inline-band stats) are Wave 3 composition scope, not current F5 state.

### Voice-map HTML comment requirement

Per voiceMap.md §8 and voiceMap.md §2a (Closing Table register owns StatRow), every generated StatRow instance MUST be preceded by a voice-map HTML comment. Voice-map value is always `closing-table` for StatRow — StatRow is a canonical Closing Table instance per §2a, not register-parametrized.

Markup contract (canonical, implicit scale):

```html
<!-- voice-map: closing-table -->
<section class="statrow">
  <div class="statrow__item">
    <div class="statrow__num">36</div>
    <div class="statrow__label">Label 1</div>
  </div>
  <div class="statrow__item">
    <div class="statrow__num">4.2</div>
    <div class="statrow__label">Label 2</div>
  </div>
  <div class="statrow__item">
    <div class="statrow__num">2</div>
    <div class="statrow__label">Label 3</div>
  </div>
</section>
```

Compressed variant — add `.statrow--numeral-36` to the container class list when composition constraints demand the tighter cadence:

```html
<!-- voice-map: closing-table -->
<section class="statrow statrow--numeral-36">
  ...
</section>
```

The comment is mandatory at generation time. Phase 5 MUST emit it when rendering any StatRow instance. Phase 5 enforcement (grep verification that every `.statrow` container is preceded by a `<!-- voice-map: closing-table -->` comment) is a Wave 4 gate concern, not a commit-time rule.

### Phase 5 generation note

When Phase 5 emits a StatRow instance, it selects the scale by section context. The hero stat row uses the canonical scale (implicit — base `.statrow` alone, no variant modifier) per F5 precedent. Non-hero stat rows (service tier summaries, inline stat bands — Wave 3 composition scope) add `.statrow--numeral-36` when composition constraints demand compression. No `.statrow--numeral-48` class is emitted; canonical is implicit.

Generation constraints Phase 5 MUST enforce:

1. **4× ratio rule (§5):** both authored scales satisfy the ratio. Custom scales outside canonical/compressed require authorial extension in typography.md §5.
2. **Column-count + content:** at 3-col, a StatRow with fewer than 3 stats produces empty columns. Generation should author exactly 3 stats per row until a future `--cols-N` axis lands.
3. **Register invariance:** voice-map comment is always `closing-table`. StatRow is not a register-parametrized primitive.

Register-aware copy generation remains v0.8.1 scope per the 2026-04-20 Path A decision; the voice-map comment reserves the signal.

---

## Breakpoint system

v0.8 uses a two-breakpoint mobile-first system:

- **Mobile:** default styles, no media query needed
- **Desktop:** `@media (min-width: 981px)` for any desktop-specific rule

Or equivalently, the pattern used throughout the skill files is mobile overrides via `@media (max-width: 980px)` after desktop defaults. Both patterns produce the same result. Pick one and stick with it per file.

There is no separate tablet breakpoint in v0.8. The 981px break handles iPad portrait (768px → mobile layout) and iPad landscape (1024px → desktop layout) correctly for every section pattern. If a specific section needs tablet-specific treatment in a later version, add it there, not globally.

### Breakpoint rationale

- **981px:** Chosen because it falls between iPad portrait (768px) and iPad landscape (1024px), so iPads flip layouts on rotation without an awkward in-between state. Also comfortably above the widest common phone (iPhone Pro Max at 430px) with room to spare.

### Container widths

Used inside every section to constrain content width. Defined as custom properties in `:root`.

```css
.section-container-narrow { max-width: var(--container-narrow); }   /* 860px */
.section-container { max-width: var(--container-default); }         /* 1100px */
.section-container-wide { max-width: var(--container-wide); }       /* 1280px */
```

Usage guide:
- **860px narrow:** FAQ accordion, single-column long-form content
- **1100px default:** Contact form, before/after gallery, video augmentation
- **1280px wide:** Services grid, testimonials grid, footer, stats grid, nav

All containers are centered with `margin: 0 auto` and have side padding of `24px` desktop, `20px` mobile, to prevent content hitting the viewport edge.

---

## Global reset and base styles

Minimal reset, not a full Normalize.css. Only the rules we actually need for v0.8.

```css
*, *::before, *::after {
  box-sizing: border-box;
}

html {
  -webkit-text-size-adjust: 100%;
  scroll-behavior: smooth;
}

body {
  margin: 0;
  font-family: var(--font-body);
  font-size: var(--text-md);
  line-height: var(--lh-normal);
  color: var(--color-text);
  background: var(--color-white);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

h1, h2, h3, h4, h5, h6 {
  margin: 0;
  font-family: var(--font-heading);
  font-weight: var(--fw-bold);
  line-height: var(--lh-snug);
  color: var(--color-dark-primary);
}

p {
  margin: 0;
}

a {
  color: var(--color-primary);
  text-decoration: none;
  transition: color var(--transition-fast);
}

a:hover {
  color: var(--color-dark-primary);
}

img {
  max-width: 100%;
  height: auto;
  display: block;
}

button {
  font-family: inherit;
  font-size: inherit;
  cursor: pointer;
  border: none;
  background: none;
  padding: 0;
}

input, select, textarea {
  font-family: inherit;
  font-size: inherit;
}

ul, ol {
  padding: 0;
}

/* Respect prefers-reduced-motion globally */
@media (prefers-reduced-motion: reduce) {
  html {
    scroll-behavior: auto;
  }
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### Why this minimal reset

Full resets like Normalize.css or Tailwind Preflight add dozens of rules we don't need and make the generated CSS harder to read when Ron or a future developer wants to understand what's happening. The rules above handle the cases v0.8 actually hits: box-sizing for layout predictability, margin reset for headings and paragraphs, image defaults, button and form element font inheritance, and a global respect for reduced-motion.

---

## Shared keyframes

Used by multiple sections. Defined once at the top of `style.css` so they do not get duplicated.

```css
@keyframes shimmer {
  0%, 100% { transform: translateX(-100%); }
  50% { transform: translateX(100%); }
}

@keyframes marquee-scroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

@keyframes fade-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes pulse-subtle {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.85; }
}
```

### Usage

- **shimmer:** Nav phone button (`.nav-phone::before`), primary hero CTA (`.hero-btn-primary::before`), service card hover sweep (`.service-card::before`), testimonial card hover sweep (`.testimonial-card::before`). 3-second infinite loop with the button gradient effect from v0.5.
- **marquee-scroll:** Trust badges marquee (`.trust-marquee-track`). 40-second linear infinite loop. Uses the `-50%` endpoint because the marquee track contains duplicated content for seamless looping.
- **fade-up:** Scroll-reveal animations on sections. Triggered by JS IntersectionObserver adding `.visible` class which plays the keyframe once.
- **fade-in:** Simple opacity fade, used by the mesh gradient canvas on initial render.
- **pulse-subtle:** Reserved for emergency service badge if it needs attention grabbing without being obnoxious.

All keyframe animations respect `prefers-reduced-motion` through the global reset rule above.

---

## Tier-specific token overrides

After the base `:root` block, Phase 5 appends tier-specific overrides. Only the tokens that differ from the base get redefined.

### Premium tier (70-100 score)

```css
:root.tier-premium {
  --font-heading: "Fraunces", "Playfair Display", Georgia, serif;
  --text-hero: 84px;
  --text-hero-default: 64px;
  --text-section-title: 56px;
  --text-display: 112px;
  --space-section: 140px;
  --space-section-generous: 160px;
}

@media (max-width: 980px) {
  :root.tier-premium {
    --text-hero: 48px;
    --text-hero-default: 42px;
    --text-section-title: 36px;
    --text-display: 72px;
    --space-section: 88px;
    --space-section-generous: 108px;
  }
}
```

The `.tier-premium` class is applied to the `<html>` element in Phase 5 when tier is Premium. Using a class on `<html>` instead of duplicating the whole `:root` block keeps the CSS smaller and lets developer tools show the tier visually.

### Professional tier (40-69 score)

```css
:root.tier-professional {
  --font-heading: "Fraunces", "Playfair Display", Georgia, serif;
  /* All other tokens use the base values */
}
```

Professional is the default baseline — most tokens are already correct for Professional in the base `:root` block. The heading font resolves to Fraunces per typography.md Appendix B (universal across tiers).

### Standard tier (0-39 score)

```css
:root.tier-standard {
  --font-heading: "Fraunces", "Playfair Display", Georgia, serif;
  --text-hero: 56px;
  --text-hero-default: 44px;
  --text-section-title: 36px;
  --text-display: 72px;
  --space-section: 100px;
  --space-section-generous: 120px;
}

@media (max-width: 980px) {
  :root.tier-standard {
    --text-hero: 38px;
    --text-hero-default: 34px;
    --text-section-title: 28px;
    --text-display: 54px;
    --space-section: 72px;
    --space-section-generous: 88px;
  }
}
```

Standard uses Fraunces heading + Inter body per typography.md Appendix B (universal stack), with a smaller type scale for speed and hierarchy clarity and compressed vertical rhythm. Typography identity matches Premium and Professional; tier differentiation lives in palette, density, motion, and photographic treatment per Appendix B.

### Tier override application order

Phase 5 writes the tier override block IMMEDIATELY after the base `:root` block. Other CSS (section styles, hero styles) comes after. CSS cascade ensures the tier class wins over the base `:root` because of specificity — `:root.tier-premium` is higher specificity than `:root`.

The `<html>` element gets the appropriate class written by Phase 5:

```html
<html lang="en" class="tier-premium">
```

Only one tier class per build. Never apply two.

---

## Accessibility defaults

### Focus styles

Every interactive element gets a visible focus ring. The default browser focus ring is insufficient for brand-colored backgrounds.

```css
:focus-visible {
  outline: 3px solid rgba(var(--color-primary-rgb), 0.5);
  outline-offset: 2px;
}

/* Remove outline on mouse-down focus (keyboard focus only) */
:focus:not(:focus-visible) {
  outline: none;
}
```

The `:focus-visible` pseudo-class only activates on keyboard focus, not mouse clicks. This is the modern pattern that gives keyboard users visible focus without showing outlines on every mouse click.

### Reduced motion

The global reset already disables animations and transitions when `prefers-reduced-motion: reduce` is set. Additional section-specific handling:

```css
@media (prefers-reduced-motion: reduce) {
  /* Hero parallax: disable scroll-driven motion */
  .hero-parallax-row {
    transform: translateX(0) !important;
  }

  /* Crossfade slideshow: show first slide only */
  .hero-crossfade-slide:not(:first-child) {
    display: none;
  }

  /* Marquee: stop scrolling */
  .trust-marquee-track {
    animation: none !important;
    justify-content: center;
  }

  /* Mesh gradient canvas: hide (falls back to solid background) */
  .hero-mesh-canvas,
  .hero-mesh-canvas-full {
    display: none;
  }

  /* Mousemove parallax blobs: stop moving */
  .hero-mousemove-blob {
    transition: none !important;
    transform: none !important;
  }

  /* Number ticker: jump to final value instead of animating */
  .stats-number[data-target] {
    /* JS handles this by setting text content directly */
  }
}
```

### Skip-to-content link

Every generated page gets a skip-to-content link as the first child of `<body>`. Invisible until keyboard-focused.

```html
<a href="#main-content" class="skip-link">Skip to main content</a>
```

```css
.skip-link {
  position: absolute;
  top: -48px;
  left: 16px;
  height: 40px;
  background: var(--color-primary);
  color: var(--color-white);
  padding: 10px 20px;
  border-radius: var(--radius-md);
  font-weight: var(--fw-semibold);
  text-decoration: none;
  z-index: 1000;
  transition: top var(--transition-fast);
}

/* v0.7.3 hotfix #10 (2026-04-17): top was -40px with no height declared, which
   allowed the rendered element to expand to ~48px from font + padding and left
   an 8px brand-colored strip visible above the viewport. Explicit height: 40px
   plus top: -48px now guarantees the element sits fully above the fold until
   keyboard-focused. Observed on F1 (red), F4 (green), F5 (blue). */

.skip-link:focus {
  top: 16px;
}
```

Main content wrapper gets `id="main-content"` on the element that comes after the nav.

### Color contrast minimums

Enforced at generation time by Phase 4 color selection (before build) and verified at Phase 6 check 13 (after build).

- Body text: 4.5:1 minimum against its background
- Large text (18px+ or 14px+ bold): 3:1 minimum
- Non-text elements (icons, UI borders): 3:1 minimum
- Focus indicators: 3:1 minimum against adjacent colors

If node-vibrant returns a primary color that would fail contrast against white backgrounds (e.g., a light yellow), Phase 4 darkens it until it passes. The darkening algorithm is the same HSL-lightness-reduction used for deriving `--color-dark-primary`.

### Keyboard navigation for interactive components

- **Nav:** hamburger opens via keyboard (Enter/Space), closes via Escape
- **FAQ accordion:** native `<details>` element handles keyboard automatically
- **Before/after slider:** handle is tabbable, arrow keys move the clip-path 5% per press, Home/End jump to 0/100%, aria-valuenow updates on every change
- **Hero video dialog:** Escape closes the modal, focus trapped inside while open, focus returns to trigger button on close
- **Mobile nav drawer:** first link receives focus when drawer opens, Tab cycles through drawer links, Escape closes drawer

These rules live in the JS primitives below.

---

## Vanilla JavaScript animation toolkit

All animation and interactivity for v0.8 sites uses vanilla JavaScript. No React. No Vue. No jQuery. No animation libraries. The primitives below are everything the generated sites need.

Each primitive is a named function that Phase 5 includes in `script.js` only if the build needs it. A build with no before/after gallery omits the `beforeAfterCompare` function entirely.

### Primitive 1: numberTicker

Animates a number from 0 to a target value when the element scrolls into view. Used by the stats dark section. Critical architectural note: **only observes elements with a `data-target` attribute**. Elements without the attribute are left alone. This is the fix for the v0.6 "0 Years Licensed" bug where a static stat element was getting animated to zero.

```javascript
function numberTicker() {
  const targets = document.querySelectorAll('[data-target]');
  if (!targets.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const finalValue = parseInt(el.dataset.target, 10);
      if (isNaN(finalValue)) return;

      // Respect reduced motion: jump to final value immediately
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        el.textContent = finalValue.toLocaleString();
        observer.unobserve(el);
        return;
      }

      const duration = 2000;
      const startTime = performance.now();

      const tick = (now) => {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);
        // easeOutCubic
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = Math.floor(finalValue * eased);
        el.textContent = current.toLocaleString();
        if (progress < 1) {
          requestAnimationFrame(tick);
        } else {
          el.textContent = finalValue.toLocaleString();
        }
      };

      requestAnimationFrame(tick);
      observer.unobserve(el);
    });
  }, { threshold: 0.3, rootMargin: '0px 0px -50px 0px' });

  targets.forEach((el) => observer.observe(el));
}
```

**Key points:**
- Uses `querySelectorAll('[data-target]')` so elements without the attribute are never touched
- Each element only animates once (`observer.unobserve` after trigger)
- easeOutCubic for a natural deceleration curve
- `toLocaleString()` for comma-formatted numbers (50,000 instead of 50000)
- Respects reduced motion by jumping to final value immediately
- Threshold 0.3 means animation starts when 30% of the element is visible

### Primitive 2: crossfadeSlideshow

Cycles the `.active` class through a set of slides every 6 seconds. Used by the hero-crossfade mode and any section that needs a photo slideshow.

```javascript
function crossfadeSlideshow(containerSelector, interval = 6000) {
  const container = document.querySelector(containerSelector);
  if (!container) return;

  const slides = container.querySelectorAll('.hero-crossfade-slide');
  if (slides.length < 2) return;

  // Respect reduced motion: show only the first slide
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return;
  }

  let currentIndex = 0;
  slides[0].classList.add('active');

  setInterval(() => {
    slides[currentIndex].classList.remove('active');
    currentIndex = (currentIndex + 1) % slides.length;
    slides[currentIndex].classList.add('active');
  }, interval);
}
```

**Key points:**
- Takes a container selector so it can be used for any slideshow in any section
- Default interval 6000ms matches the hero spec
- Early returns if no container or fewer than 2 slides
- Reduced motion shows first slide only (no cycling)
- No unmount or cleanup logic because v0.8 sites are static HTML without SPA navigation

### Primitive 3: parallaxScroll

Translates elements vertically based on scroll position at a specified speed multiplier. Used by the hero-parallax mode for the rotated photo rows.

```javascript
function parallaxScroll(selector, speed) {
  const elements = document.querySelectorAll(selector);
  if (!elements.length) return;

  // Disable on mobile (performance and feel)
  if (window.innerWidth < 981) return;

  // Respect reduced motion
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  let ticking = false;

  const update = () => {
    const scrollY = window.scrollY;
    elements.forEach((el) => {
      const offset = scrollY * speed;
      el.style.transform = `translate3d(0, ${offset}px, 0)`;
    });
    ticking = false;
  };

  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(update);
      ticking = true;
    }
  }, { passive: true });
}

// Usage in hero-parallax mode:
// parallaxScroll('.hero-parallax-row-1', 0.3);
// parallaxScroll('.hero-parallax-row-2', -0.2);
```

**Key points:**
- Uses `requestAnimationFrame` throttling via the `ticking` flag to avoid running update on every scroll event
- Passive scroll listener for performance
- Disabled below 981px because parallax on small viewports feels janky and hurts performance
- `translate3d` triggers GPU compositing for smooth motion
- Two rows moving at opposite speeds (0.3 and -0.2) creates the depth illusion
- Negative speed means the element moves against the scroll direction

### Primitive 4: meshGradient

Canvas-based animated mesh gradient for hero-single-mesh and hero-pure-mesh modes. Renders flowing blobs in brand colors at 30fps.

```javascript
function meshGradient(canvasSelector, colors) {
  const canvas = document.querySelector(canvasSelector);
  if (!canvas) return;

  // Respect reduced motion: render a static frame only
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const ctx = canvas.getContext('2d');

  const resize = () => {
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);
  };

  resize();
  window.addEventListener('resize', resize);

  // Blob definitions: position, radius, color, velocity
  const blobs = colors.map((color, i) => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    radius: 300 + Math.random() * 200,
    color: color,
    vx: (Math.random() - 0.5) * 0.4,
    vy: (Math.random() - 0.5) * 0.4
  }));

  const render = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    blobs.forEach((blob) => {
      const gradient = ctx.createRadialGradient(
        blob.x, blob.y, 0,
        blob.x, blob.y, blob.radius
      );
      gradient.addColorStop(0, blob.color);
      gradient.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      if (!reducedMotion) {
        blob.x += blob.vx;
        blob.y += blob.vy;

        // Bounce off edges
        if (blob.x < 0 || blob.x > canvas.width) blob.vx *= -1;
        if (blob.y < 0 || blob.y > canvas.height) blob.vy *= -1;
      }
    });

    if (!reducedMotion) {
      requestAnimationFrame(render);
    }
  };

  render();
}

// Usage:
// meshGradient('.hero-mesh-canvas-full', ['#2B4C9F', '#F5A623', '#0F1A35']);
```

**Key points:**
- Handles device pixel ratio for sharp rendering on retina displays
- Accepts a colors array (pulled from brand palette in Phase 5)
- Each blob is a radial gradient with transparent edges — overlapping blobs blend naturally
- Blobs bounce off canvas edges to stay visible
- Reduced motion renders one static frame and stops
- No frame rate cap because `requestAnimationFrame` naturally respects display refresh

### Primitive 5: mousemoveParallax

Translates elements based on mouse position for the hero-pure-mesh blob layer. Creates a subtle depth effect without requiring photos.

```javascript
function mousemoveParallax(blobSelectors) {
  // blobSelectors is an array of [selector, speed] pairs
  // Example: [['.hero-mousemove-blob-1', 0.02], ['.hero-mousemove-blob-2', 0.04]]

  const pairs = blobSelectors.map(([sel, speed]) => {
    const el = document.querySelector(sel);
    return el ? { el, speed } : null;
  }).filter(Boolean);

  if (!pairs.length) return;

  // Skip on touch devices (no mouse events)
  if (window.matchMedia('(hover: none)').matches) return;

  // Respect reduced motion
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const centerX = window.innerWidth / 2;
  const centerY = window.innerHeight / 2;

  let ticking = false;

  document.addEventListener('mousemove', (e) => {
    if (ticking) return;
    ticking = true;

    requestAnimationFrame(() => {
      const dx = e.clientX - centerX;
      const dy = e.clientY - centerY;

      pairs.forEach(({ el, speed }) => {
        el.style.transform = `translate3d(${dx * speed}px, ${dy * speed}px, 0)`;
      });

      ticking = false;
    });
  });
}
```

**Key points:**
- Takes an array of `[selector, speed]` pairs so multiple blobs at different speeds can be controlled in one call
- Uses `(hover: none)` media query to detect touch devices and skip entirely (no mouse = no parallax)
- RAF throttling prevents running on every mousemove event (which fires at ~60hz on most systems)
- Movement is relative to viewport center, not absolute mouse coordinates
- The CSS transition on the blob elements (0.4s ease-out from section-patterns.md hero-mousemove-blob rule) smooths the movement so it doesn't feel twitchy

### Primitive 6: beforeAfterCompare

Drag slider for the before/after gallery. Handles mouse, touch, and keyboard interaction. Supports thumbnail navigation between multiple project pairs.

```javascript
function beforeAfterCompare(containerSelector) {
  const containers = document.querySelectorAll(containerSelector);
  if (!containers.length) return;

  containers.forEach(initCompare);

  // Thumbnail navigation
  const thumbs = document.querySelectorAll('.beforeafter-nav-thumb');
  const pairs = window.BA_PAIRS || []; // Phase 5 writes pair data as window.BA_PAIRS

  thumbs.forEach((thumb) => {
    thumb.addEventListener('click', () => {
      const target = parseInt(thumb.dataset.baTarget, 10);
      const pair = pairs[target];
      if (!pair) return;

      const compare = document.querySelector('.beforeafter-compare');
      compare.querySelector('.beforeafter-image-before').style.backgroundImage =
        `url('${pair.before}')`;
      compare.querySelector('.beforeafter-image-after').style.backgroundImage =
        `url('${pair.after}')`;

      // Reset slider to center
      compare.querySelector('.beforeafter-image-after').style.clipPath =
        'inset(0 50% 0 0)';
      compare.querySelector('.beforeafter-handle').style.left = '50%';
      compare.querySelector('.beforeafter-handle').setAttribute('aria-valuenow', '50');

      // Update active thumb
      thumbs.forEach((t) => t.classList.remove('active'));
      thumb.classList.add('active');
    });
  });
}

function initCompare(container) {
  const afterImage = container.querySelector('.beforeafter-image-after');
  const handle = container.querySelector('.beforeafter-handle');
  let isDragging = false;

  const updatePosition = (clientX) => {
    const rect = container.getBoundingClientRect();
    const x = clientX - rect.left;
    const percent = Math.max(0, Math.min(100, (x / rect.width) * 100));
    afterImage.style.clipPath = `inset(0 ${100 - percent}% 0 0)`;
    handle.style.left = `${percent}%`;
    handle.setAttribute('aria-valuenow', Math.round(percent).toString());
  };

  // Mouse events
  container.addEventListener('mousedown', (e) => {
    isDragging = true;
    updatePosition(e.clientX);
    e.preventDefault();
  });

  window.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    updatePosition(e.clientX);
  });

  window.addEventListener('mouseup', () => {
    isDragging = false;
  });

  // Touch events
  container.addEventListener('touchstart', (e) => {
    isDragging = true;
    updatePosition(e.touches[0].clientX);
  }, { passive: true });

  container.addEventListener('touchmove', (e) => {
    if (!isDragging) return;
    updatePosition(e.touches[0].clientX);
  }, { passive: true });

  container.addEventListener('touchend', () => {
    isDragging = false;
  });

  // Keyboard support on handle
  handle.addEventListener('keydown', (e) => {
    const current = parseInt(handle.getAttribute('aria-valuenow'), 10) || 50;
    let next = current;

    switch (e.key) {
      case 'ArrowLeft':
        next = Math.max(0, current - 5);
        break;
      case 'ArrowRight':
        next = Math.min(100, current + 5);
        break;
      case 'Home':
        next = 0;
        break;
      case 'End':
        next = 100;
        break;
      default:
        return;
    }

    e.preventDefault();
    afterImage.style.clipPath = `inset(0 ${100 - next}% 0 0)`;
    handle.style.left = `${next}%`;
    handle.setAttribute('aria-valuenow', next.toString());
  });
}
```

**Key points:**
- Handles mouse, touch, and keyboard — three separate interaction modes, all working on the same slider state
- Mousemove and mouseup listen on `window` not `container` so the user can drag past the edge without losing the drag
- Keyboard: arrow keys move 5% per press, Home/End jump to 0/100%
- aria-valuenow updates on every change for screen reader users
- Multiple pair support: Phase 5 writes `window.BA_PAIRS` as an array of `{before, after}` objects, thumbnail clicks swap the background images
- `{ passive: true }` on touch events because we don't need to call `preventDefault()` — the CSS `touch-action: pan-y` already handles the scroll conflict

### Supporting utility: scrollReveal

IntersectionObserver-based fade-up animation for sections as they scroll into view. Used globally by Phase 5 on every major section.

```javascript
function scrollReveal() {
  // Respect reduced motion: skip entirely, elements are already visible
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const targets = document.querySelectorAll('[data-reveal]');
  if (!targets.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -80px 0px' });

  targets.forEach((el) => observer.observe(el));
}
```

CSS companion (add to shared keyframes section above):

```css
/* Progressive enhancement: sections default visible.
   Only hide and animate when JS has confirmed it will reveal them.
   Root <html> gets class="js" via a head-inline script.
   Without that class, all [data-reveal] content is visible
   immediately — protects bots, Lighthouse, social preview
   scrapers, full-page screenshots, and no-JS environments.
   Grandview F4 2026-04-16 caught the invisible-below-hero bug
   this guard prevents. */

html.js [data-reveal] {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.8s ease, transform 0.8s ease;
}

html.js [data-reveal].revealed {
  opacity: 1;
  transform: translateY(0);
}

@media (prefers-reduced-motion: reduce) {
  html.js [data-reveal] {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
```

Phase 5 adds `data-reveal` to the top-level element of every major section during HTML generation.

### Required head-inline script for progressive-enhancement guard

The first element inside `<head>`, immediately after `<meta charset>`, must be this script:

```html
<script>document.documentElement.classList.add('js');</script>
```

This enables the `html.js [data-reveal]` progressive-enhancement guard defined in this file. The script runs synchronously before any rendering, so the reveal animations trigger normally when JS is available. When JS is absent, disabled, or slow (bots, scrapers, screenshots), the `js` class is never added and all `[data-reveal]` sections stay visible.

This script must appear on every generated page. Phase 5 HTML generation must include it in the base template.

Referenced from: SKILL.md Phase 5 (HTML generation).

### Supporting utility: navScrolled

Adds `.scrolled` class to the nav when the user scrolls past 40px. Used to transition the nav from transparent-ish to more opaque with a shadow.

```javascript
function navScrolled() {
  const nav = document.querySelector('.nav');
  if (!nav) return;

  let ticking = false;
  const threshold = 40;

  const update = () => {
    if (window.scrollY > threshold) {
      nav.classList.add('scrolled');
    } else {
      nav.classList.remove('scrolled');
    }
    ticking = false;
  };

  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(update);
      ticking = true;
    }
  }, { passive: true });

  update();
}
```

### Supporting utility: mobileNavToggle

Opens and closes the mobile nav drawer. Handles keyboard accessibility.

```javascript
function mobileNavToggle() {
  const hamburger = document.querySelector('.nav-hamburger');
  const links = document.querySelector('.nav-links');
  if (!hamburger || !links) return;

  let isOpen = false;

  const open = () => {
    isOpen = true;
    links.classList.add('open');
    hamburger.setAttribute('aria-expanded', 'true');
    // Focus first link for keyboard users
    const firstLink = links.querySelector('a');
    if (firstLink) firstLink.focus();
  };

  const close = () => {
    isOpen = false;
    links.classList.remove('open');
    hamburger.setAttribute('aria-expanded', 'false');
    hamburger.focus();
  };

  hamburger.addEventListener('click', () => {
    if (isOpen) close();
    else open();
  });

  // Escape key closes drawer
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && isOpen) close();
  });

  // Click outside closes drawer
  document.addEventListener('click', (e) => {
    if (!isOpen) return;
    if (!links.contains(e.target) && !hamburger.contains(e.target)) {
      close();
    }
  });
}
```

### The master script.js init block

Phase 5 writes a master initialization block at the top of `script.js` that only calls the primitives actually needed for the build:

```javascript
document.addEventListener('DOMContentLoaded', () => {
  // Always needed
  navScrolled();
  mobileNavToggle();
  scrollReveal();

  // Stats section
  numberTicker();

  // Conditional on hero mode
  if (document.querySelector('.hero-crossfade')) {
    crossfadeSlideshow('.hero-crossfade-slideshow');
  }
  if (document.querySelector('.hero-parallax')) {
    parallaxScroll('.hero-parallax-row-1', 0.3);
    parallaxScroll('.hero-parallax-row-2', -0.2);
  }
  if (document.querySelector('.hero-mesh-canvas')) {
    meshGradient('.hero-mesh-canvas', [
      'rgba(var(--color-primary-rgb), 0.6)',
      'rgba(var(--color-accent-rgb), 0.5)'
    ]);
  }
  if (document.querySelector('.hero-mesh-canvas-full')) {
    meshGradient('.hero-mesh-canvas-full', [
      'rgba(var(--color-primary-rgb), 0.8)',
      'rgba(var(--color-accent-rgb), 0.6)',
      'rgba(var(--color-dark-primary-rgb), 0.7)'
    ]);
    mousemoveParallax([
      ['.hero-mousemove-blob-1', 0.02],
      ['.hero-mousemove-blob-2', 0.04],
      ['.hero-mousemove-blob-3', 0.03]
    ]);
  }

  // Conditional on before/after gallery presence
  if (document.querySelector('.beforeafter-compare')) {
    beforeAfterCompare('.beforeafter-compare');
  }
});
```

Phase 5 generates this block dynamically based on what sections and hero mode the build includes. Primitives that aren't called get omitted from `script.js` entirely, keeping the file small.

---

## Reduced motion handling summary

Every animation in v0.8 respects `prefers-reduced-motion: reduce`. The handling strategy varies by animation type:

| Animation               | Reduced motion behavior |
|-------------------------|------------------------|
| numberTicker            | Jump to final value immediately |
| crossfadeSlideshow      | Show first slide only, no cycling |
| parallaxScroll          | Disabled entirely, elements stay in default position |
| meshGradient            | Render one static frame, no animation loop |
| mousemoveParallax       | Disabled entirely |
| beforeAfterCompare      | Works normally (user-initiated, not auto-playing) |
| scrollReveal            | Elements start at final state, no fade |
| Marquee scroll (CSS)    | Animation disabled via global CSS rule |
| Shimmer button effect   | Animation disabled via global CSS rule |

The global CSS reset handles most CSS-based animations through the `animation-duration: 0.01ms !important` pattern. JS primitives handle themselves by checking `matchMedia('(prefers-reduced-motion: reduce)').matches` at startup.

---

## Performance targets

v0.8 sites must hit these Lighthouse mobile scores for Phase 6 to pass:

- **LCP (Largest Contentful Paint):** under 2.5 seconds
- **Performance score:** 85 or higher
- **SEO score:** 95 or higher
- **Accessibility score:** 90 or higher
- **Best Practices score:** 90 or higher

The CSS framework is built to hit these targets through:

- Font preloading (removes render-blocking font load)
- CSS custom properties (smaller stylesheet than hardcoded values)
- Minimal reset (no Normalize.css bloat)
- Conditional JS inclusion (primitives only loaded if needed)
- GPU-accelerated transforms (translate3d on parallax elements)
- Passive scroll listeners (no scroll blocking)
- RequestAnimationFrame throttling on scroll and mousemove
- Image optimization handled in `image-handling.md` (WebP and AVIF via sharp)

If a build fails the LCP target, the most likely cause is a hero background image over 400KB. Check the image pipeline output first.

---

## Common mistakes

- Do not hardcode color values inside section CSS. Reference `var(--color-primary)` etc.
- Do not hardcode spacing values inside section CSS. Reference `var(--space-section)` etc.
- Do not introduce a new CSS custom property without adding it to this file and following the naming pattern.
- Do not include JS primitives for sections that aren't in the build (e.g., don't include `beforeAfterCompare` when there's no before/after gallery).
- Do not skip reduced-motion handling on a new animation. Every animation needs a reduced-motion path.
- Do not use a tablet breakpoint. v0.8 is mobile-first with a single 981px break.
- Do not load multiple heading fonts. Pick one per tier.
- Do not use `position: sticky` for the nav. Use `position: fixed`.
- Do not hardcode `rgba(43, 76, 159, 0.15)`. Use `rgba(var(--color-primary-rgb), 0.15)`.

---

## Version

css-framework.md v0.8, foundation file for prospect-site skill v0.8. Every other reference file depends on this one.

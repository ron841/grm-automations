# Hero Patterns Reference

Part of the prospect-site v1.0 build skill. Loaded by Phase 5 when the skill begins hero generation, in tandem with `section-patterns.md` (which covers every other homepage section).

This file contains the pixel-level spec for the hero region of every generated homepage: the shared Glassmorphism content layer (both size variants) and the three v1.0 background mode implementations. CSS variables (`--color-primary`, `--font-heading`, `--space-section`, etc.) come from `css-framework.md`. Vanilla JS animation primitives (cross-fade, mesh gradient) also live in `css-framework.md`.

## v1.0 mode catalog

v1.0 ships 3 hero modes, not 4. The reduction is grounded in F1–F8 prod-walk evidence at SIMPLIFY-close (4× glass-crossfade, 1× glass-single-mesh, 2× text-only, 1× single-static-photo, zero parallax / zero pure-mesh / zero video). Modes spec'd but never built represent (e) bloat in the canonical reference set, not under-implementation. The trimmed catalog: **glass-crossfade** (multi-photo cycling with glass card), **glass-single** (single-background with glass card; photo or mesh per P5 fallback), **text-only** (no glass card, no hero photo).

## Architecture

Every v1.0 hero has two layers:

1. **Content layer.** The Glassmorphism Trust Hero card. Used in glass-crossfade and glass-single; text-only ships without a card. The card comes in two size variants (default and wide), selected deterministically by character count.

2. **Background layer.** Varies by mode from the Phase 4 decision tree:
   - `glass-crossfade` — full-viewport cross-fade slideshow of 3-5 photos
   - `glass-single` — single-background mode with `data-bg-variant="photo|mesh"`, chosen deterministically by P5 fallback (photo present → photo variant; photo absent + dual-stop palette → mesh variant)
   - `text-only` — no glass card, no hero photo; brand wordmark anchors the band on a clean `--hero-bg` color

The content layer is identical across the two card-bearing modes. Only the background changes. This is the architectural discipline: one hero pattern, deterministic variation.

## Phase 4 hero-mode selection

The mode and the glass-card variant both fall through deterministically from data. No designer choice; no editorial override surface.

```
if hero_photo_qualified_count >= 3:
    mode = glass-crossfade
    photo_set = top 3-5 hero-qualified photos by score
    glass_card_variant = wide if (headline_chars + subhead_chars) > 120 else standard

elif hero_photo_qualified_count >= 1:
    mode = glass-single
    background = photo (single highest-scored hero-qualified photo)
    glass_card_variant = wide if (headline_chars + subhead_chars) > 120 else standard

else:
    # P5 fallback: photo absent, do not silently fail
    if profile.brandPalette has dual gradient stops:
        mode = glass-single
        background = mesh (CSS gradient mesh from palette)
        glass_card_variant = wide if (headline_chars + subhead_chars) > 120 else standard
    else:
        mode = text-only
```

**Rationale notes:**

- `hero_photo_qualified_count` derives from photo-discipline scoring at audit-side `image-handling.md`. Qualified = non-disqualified per the lawn-patch / classifier disqualifier list, with score above the hero-eligibility floor.
- The `>= 3` threshold for glass-crossfade preserves the multi-photo cycling premise; below 3, single-photo is the honest call.
- The mesh fallback inside glass-single is the only place mesh survives as a background option. It is conditional on dual-gradient palette presence (a deterministic data check), not a designer choice.
- text-only is the floor when neither photo nor palette can carry the hero band. The engine never silently fails; it falls through cleanly to text-only.

Save the resolved mode and variant to `profile-draft.json` under `designChoices.heroMode` and `designChoices.heroGlassVariant`. Phase 5 reads these and applies the appropriate classes and `data-bg-variant` attribute.

## Glass card variant selection

Wide vs. standard glass card variant is selected deterministically by character count of headline + subhead:

```
glass_card_variant = wide if (headline_chars + subhead_chars) > 120 else standard
```

Applies to both glass-crossfade and glass-single. text-only ships without a glass card and is not subject to this rule.

The 120-character threshold is the v1.0 canonical breakpoint. At and below 120 combined characters, the default card's 580px max-width and 56px headline carry comfortably; above 120, the wide variant's 680px max-width and 72px headline give the longer copy room without awkward wrapping. The rule is deterministic and data-derived — same family as the photo|mesh fallback inside glass-single. Voice is voice; structure is structure; selection follows data.

Save to `profile-draft.json` under `designChoices.heroGlassVariant`. Phase 5 reads this value and applies the modifier class (`hero-glass-card--wide`) when wide.

---

## Shared glass card content layer

This card renders in glass-crossfade and glass-single (not text-only). HTML structure is identical across both card-bearing modes; only the outer class modifier differs between default and wide.

### HTML structure

```html
<div class="hero-glass-card [hero-glass-card--wide]">
  <div class="hero-eyebrow">[CITY] · SINCE [YEAR]</div>
  <h1 class="hero-headline">
    Fifty years.<br>
    Two Tuccis.<br>
    One phone number.
  </h1>
  <p class="hero-sub">
    Residential, commercial, and industrial wiring across Marion County.
    Florida license EC13007855.
  </p>

  <div class="hero-stats-mini">
    <div class="hero-stat">
      <div class="hero-stat-value">50+</div>
      <div class="hero-stat-label">Years licensed</div>
    </div>
    <div class="hero-stat">
      <div class="hero-stat-value">4.6★</div>
      <div class="hero-stat-label">41 reviews</div>
    </div>
    <div class="hero-stat">
      <div class="hero-stat-value">24/7</div>
      <div class="hero-stat-label">Emergency</div>
    </div>
  </div>

  <div class="hero-ctas">
    <a href="tel:[phone]" class="hero-btn-primary">Call [phone formatted]</a>
    <a href="#contact" class="hero-btn-secondary">Get a quote</a>
  </div>

  <div class="hero-badge">
    <span class="hero-badge-stars">★ 4.6</span>
    <span class="hero-badge-count">41 Google reviews</span>
  </div>
</div>
```

The `hero-glass-card--wide` modifier class is applied when `designChoices.heroGlassVariant == "wide"`.

### Base CSS (shared by both variants)

```css
.hero-glass-card {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 580px;                    /* Default variant width */
  padding: 48px 44px 52px;             /* Default variant padding */
  background: rgba(255, 255, 255, 0.14);
  backdrop-filter: blur(24px) saturate(1.4);
  -webkit-backdrop-filter: blur(24px) saturate(1.4);
  border: 1px solid rgba(255, 255, 255, 0.28);
  border-radius: 24px;
  box-shadow:
    0 24px 60px rgba(0, 0, 0, 0.25),
    0 0 0 1px rgba(255, 255, 255, 0.08) inset;
  color: #ffffff;
}

/* Wide variant modifier */
.hero-glass-card--wide {
  max-width: 680px;
  padding: 56px 52px 60px;
}

.hero-eyebrow {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 1.8px;
  text-transform: uppercase;
  color: var(--color-accent);
  margin-bottom: 22px;
}

.hero-headline {
  font-family: var(--font-heading);
  font-size: 56px;                     /* Default variant headline size */
  font-weight: 700;
  line-height: 1.04;
  letter-spacing: -1.2px;
  margin: 0 0 24px 0;
  color: #ffffff;
}

/* Wide variant headline override */
.hero-glass-card--wide .hero-headline {
  font-size: 72px;
  letter-spacing: -1.6px;
  margin-bottom: 28px;
}

.hero-sub {
  font-size: 17px;
  line-height: 1.55;
  color: rgba(255, 255, 255, 0.88);
  margin: 0 0 32px 0;
  max-width: 460px;
}

.hero-glass-card--wide .hero-sub {
  font-size: 19px;
  max-width: 540px;
}

.hero-stats-mini {
  display: flex;
  gap: 28px;
  padding: 20px 0;
  margin-bottom: 32px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.hero-stat-value {
  font-family: var(--font-heading);
  font-size: 28px;
  font-weight: 700;
  color: #ffffff;
  line-height: 1;
}

.hero-glass-card--wide .hero-stat-value {
  font-size: 32px;
}

.hero-stat-label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.75);
  margin-top: 4px;
  letter-spacing: 0.3px;
}

.hero-ctas {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}

.hero-btn-primary,
.hero-btn-secondary {
  display: inline-flex;
  align-items: center;
  padding: 16px 30px;
  border-radius: 999px;
  font-weight: 600;
  font-size: 16px;
  text-decoration: none;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.hero-btn-primary {
  background: var(--color-primary);
  color: #ffffff;
  position: relative;
  overflow: hidden;
}

.hero-btn-primary::before {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(110deg, transparent 30%, rgba(255,255,255,0.35) 50%, transparent 70%);
  transform: translateX(-100%);
  animation: shimmer 3s infinite;
}

.hero-btn-secondary {
  background: transparent;
  color: #ffffff;
  border: 1.5px solid rgba(255, 255, 255, 0.4);
}

.hero-btn-primary:hover,
.hero-btn-secondary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
}

.hero-badge {
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  padding: 10px 14px;
  background: rgba(255, 255, 255, 0.96);
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.hero-badge-stars {
  color: #f5a623;
  font-weight: 700;
  font-size: 14px;
}

.hero-badge-count {
  color: #333;
  font-size: 11px;
  margin-top: 2px;
}

/* Mobile: both variants use the same mobile treatment */
@media (max-width: 899px) {
  .hero-glass-card,
  .hero-glass-card--wide {
    max-width: 100%;
    padding: 36px 28px 40px;
    border-radius: 20px;
  }
  .hero-glass-card .hero-headline,
  .hero-glass-card--wide .hero-headline {
    font-size: 40px;
    letter-spacing: -1px;
  }
  .hero-glass-card--wide .hero-headline {
    font-size: 44px;
  }
  .hero-stats-mini { gap: 18px; }
  .hero-stat-value { font-size: 22px; }
  .hero-glass-card--wide .hero-stat-value { font-size: 24px; }
}
```

---

## Mode: glass-crossfade (heroCandidates ≥ 3)

When Phase 3 captured 3 or more strong photos, the hero is a full-viewport cross-fade slideshow. Glass card floats centered over the cycling photos. Use the top 3-5 hero-qualified photos by score; never pad with stock.

### HTML

```html
<section class="hero hero-crossfade">
  <div class="hero-crossfade-slideshow">
    <div class="hero-crossfade-slide active" style="background-image: url('assets/photos/work/photo-01.jpg')" aria-label="[work description]"></div>
    <div class="hero-crossfade-slide" style="background-image: url('assets/photos/work/photo-02.jpg')" aria-label="[work description]"></div>
    <div class="hero-crossfade-slide" style="background-image: url('assets/photos/work/photo-03.jpg')" aria-label="[work description]"></div>
    <div class="hero-crossfade-slide" style="background-image: url('assets/photos/work/photo-04.jpg')" aria-label="[work description]"></div>
  </div>
  <div class="hero-crossfade-overlay"></div>
  <div class="hero-crossfade-content">
    <!-- shared glass card HTML -->
  </div>
</section>
```

### CSS

```css
.hero-crossfade {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  padding-top: 100px;
}

.hero-crossfade-slideshow {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.hero-crossfade-slide {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  opacity: 0;
  transition: opacity 2s ease-in-out;
}

.hero-crossfade-slide.active { opacity: 1; }

.hero-crossfade-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.35) 50%, rgba(0,0,0,0.6) 100%);
  z-index: 1;
}

.hero-crossfade-content {
  position: relative;
  z-index: 2;
  max-width: 1280px;
  margin: 0 auto;
  padding: 80px 24px 100px;
  display: flex;
  align-items: center;
  min-height: calc(100vh - 100px);
}
```

### JavaScript behavior

Uses the `crossfadeSlideshow` primitive from `css-framework.md`. Cycles the `.active` class every 6000ms. Exactly matches the number of photos captured (3-5), never padded with stock, never truncated.

### Rules

- Requires 3 or more photos from `photoAssignments.heroCandidates`. Use top 3-5 by score.
- Glass card variant (default or wide) selected deterministically by character count per the variant selection rule above.
- Interval is always 6000ms (6 seconds per slide).
- First slide has `.active` class at page load; cycling starts after 6 seconds.

---

## Mode: glass-single

Unified single-background mode. Replaces v0.8's separate `glass-single-mesh` and composer-v2's de-facto static-photo lockdown. Background variant is governed by P5 photo-discipline fallback and is deterministic from data, not a designer choice.

**When fired:** photo path → exactly 1 hero-qualified photo available (or qualified count `>= 1` AND glass-crossfade did not fire). Mesh path → zero hero-qualified photos AND `profile.brandPalette` provides dual gradient stops.

**Background variants (P5-governed):**

- **Photo variant:** single highest-scored hero-qualified photo as background. Dark gradient overlay applied for legibility.
- **Mesh variant:** CSS gradient mesh canvas emitted from `brandPalette.primary` + `brandPalette.darkPrimary` + `brandPalette.accent` per the existing mesh-canvas implementation. No photo is loaded.

**Glass card content layer:** identical to glass-crossfade. Inherits glass card variant selection (wide vs. standard) by character count.

### HTML — photo variant

```html
<section class="hero hero-single" data-bg-variant="photo">
  <div class="hero-single-bg" style="background-image: url('assets/photos/work/photo-01.jpg')"></div>
  <div class="hero-single-overlay"></div>
  <div class="hero-single-content">
    <!-- shared glass card HTML -->
  </div>
</section>
```

### HTML — mesh variant

```html
<section class="hero hero-single" data-bg-variant="mesh">
  <canvas class="hero-mesh-canvas" aria-hidden="true"></canvas>
  <div class="hero-single-content">
    <!-- shared glass card HTML -->
  </div>
</section>
```

The `data-bg-variant` attribute makes the variant inspectable at QA time and serves as the CSS hook for variant-specific styling (photo gets the overlay layer; mesh gets the canvas).

### CSS

```css
.hero-single {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  padding-top: 100px;
}

/* Photo variant */
.hero-single[data-bg-variant="photo"] .hero-single-bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  z-index: 0;
}

.hero-single[data-bg-variant="photo"] .hero-single-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.35) 100%);
  z-index: 1;
}

/* Mesh variant */
.hero-single[data-bg-variant="mesh"] {
  background: var(--color-dark-primary);
}

.hero-single[data-bg-variant="mesh"] .hero-mesh-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  opacity: 0.9;
}

/* Shared content positioning */
.hero-single-content {
  position: relative;
  z-index: 2;
  max-width: 1280px;
  margin: 0 auto;
  padding: 80px 24px 100px;
  display: flex;
  align-items: center;
  min-height: calc(100vh - 100px);
}
```

### JavaScript behavior

- **Photo variant:** static photo + CSS overlay. No JS animation required.
- **Mesh variant:** uses the `meshGradient` primitive from `css-framework.md`. Renders flowing blobs in brand colors on the canvas at 30fps. Colors pulled from `brandPalette.primary`, `brandPalette.accent`, and `brandPalette.darkPrimary`. Mesh colors always come from the palette, never hardcoded.

### Selection rules

- Mode fires when glass-crossfade does not fire AND a background source exists (photo or palette).
- Variant fires deterministically from the data: photo present → photo variant; photo absent + palette dual-stop → mesh variant.
- The variant is not a designer choice. It is a P5-governed data fall-through.

### Anti-patterns specific to glass-single

- Do not render glass-single with both photo and mesh layered. The variant is exclusive.
- Do not fall back to glass-single mesh when glass-crossfade should have fired (i.e., do not skip glass-crossfade because crossfade is "complex"). Mode selection is data-deterministic.
- Do not author headline/subhead copy that assumes a photo background and then ship the mesh variant. The glass card content must read clean against either variant.

---

## Mode: text-only

The engine's floor mode. Formalized at v1.0 from F4 (Grandview) + F6 (Oxford Lawn) prod patterns. Every prospect produces a hero band even when neither photo nor palette can carry the visual layer.

**When fired:** zero hero-qualified photos AND palette lacks dual gradient stops (single-color or no palette emitted).

**Structure:** the hero band ships without a glass card and without a hero photo. The brand wordmark, headline, subhead, stats trio, and CTA carry the band on a clean background derived from `palette.light` (or pure white when palette is absent).

**Background:** solid color from `palette.light` exposed via the `--hero-bg` custom property. No overlay, no gradient, no photo, no mesh.

**Wordmark placement:** the brand wordmark renders prominently as the first visual element, larger than its in-nav size. The wordmark is the visual anchor that replaces the photo or mesh treatment in the other modes.

**Headline + subhead:** identical content layer rules to the other modes (Closing Table register per `voiceMap.md`). Larger type sizing is permitted because the band has more visual breathing room without a glass card.

**Stats trio:** rendered inline below the subhead, not floated inside a glass card. Same content rules as the other modes.

**CTA:** primary CTA button rendered below the stats trio. Secondary CTA (if `profile.businessProfile.secondaryCTA` present) renders to the right or below per the existing CTA spacing rules.

### HTML

```html
<section class="hero hero-text-only">
  <div class="hero-text-only-content">
    <div class="hero-text-only-wordmark">
      <!-- brand wordmark, larger than nav size -->
    </div>
    <h1 class="hero-headline">[headline]</h1>
    <p class="hero-sub">[subhead]</p>
    <div class="hero-stats-mini">
      <!-- stats trio, inline -->
    </div>
    <div class="hero-ctas">
      <a href="tel:[phone]" class="hero-btn-primary">Call [phone formatted]</a>
      <a href="#contact" class="hero-btn-secondary">Get a quote</a>
    </div>
  </div>
</section>
```

### CSS

```css
.hero-text-only {
  --hero-bg: var(--color-light, #ffffff);
  position: relative;
  min-height: 100vh;
  background: var(--hero-bg);
  padding-top: 100px;
}

.hero-text-only-content {
  max-width: 1280px;
  margin: 0 auto;
  padding: 80px 24px 100px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: calc(100vh - 100px);
  color: var(--color-dark-primary);
}

.hero-text-only-wordmark {
  margin-bottom: 48px;
}

.hero-text-only .hero-headline {
  font-family: var(--font-heading);
  font-size: 64px;
  font-weight: 700;
  line-height: 1.04;
  letter-spacing: -1.4px;
  color: var(--color-dark-primary);
  margin: 0 0 24px 0;
}

.hero-text-only .hero-sub {
  font-size: 19px;
  line-height: 1.55;
  color: var(--color-dark-primary);
  opacity: 0.8;
  margin: 0 0 32px 0;
  max-width: 600px;
}

@media (max-width: 899px) {
  .hero-text-only .hero-headline {
    font-size: 40px;
    letter-spacing: -1px;
  }
}
```

### Selection rules

- Last-resort mode. Fires when glass-crossfade and glass-single (photo and mesh paths) both fail their data preconditions.
- Engine never silently fails. text-only is the deterministic fall-through, not a designer choice.

### Prod evidence (informational)

F4 Grandview Inc and F6 Oxford Lawn ship variants of this pattern. F4 emits hero classes `text-only`; F6 emits `hero-grid` + `hero-kicker`. v1.0 unifies under `hero hero-text-only`. Their prod patterns are reference; the v1.0 spec is canonical.

### Anti-patterns specific to text-only

- Do not ship text-only when a photo or palette mesh is available. The mode is the floor, not a stylistic choice.
- Do not use text-only as an excuse to skip the wordmark, the stats trio, or the CTA. The band does the same conversion work as the other modes; it just does it without a glass card.
- Do not center-align the entire content stack. The same left-aligned hierarchy from the other modes carries forward.

---

## Section spacing rules for the hero region

The hero always takes `min-height: 100vh` to fill the initial viewport.

Do NOT add `padding-top` or `margin-top` to the hero beyond the 100px allowance for the fixed nav. The hero fills the viewport; the nav overlays it. This is intentional.

---

## Common mistakes for the hero (all modes)

- Do not use a 4:3 aspect ratio photo card. The hero takes full viewport.
- Do not hardcode white background behind the glass card. The background IS the mode.
- Do not use 5+ slides in cross-fade beyond what Phase 3 captured. Never pad with stock.
- Do not omit the glass card in glass-crossfade or glass-single — both card-bearing modes use the same shared glass card content layer. (text-only ships without a glass card by design and is the floor mode; do not add a card to text-only either.)
- Do not use a photo with a watermark, logo, or baked-in text as hero background.
- Do not use `box-shadow` offset blocks behind the glass card (that was v0.5's pattern, not v1.0's).
- Do not apply the wide variant by hand. The variant is selected deterministically by character count; do not override it from prose authoring or at any approval gate. Voice is voice; structure is structure.
- Do not hardcode the headline font-size — use the shared glass card CSS which switches via the modifier class.
- Do not add a third button, `<small>` fragment, or disclaimer copy below the `<div class="hero-ctas">` block. The two buttons defined in the shared glass card content layer are the complete CTA. See `anti-slop-rules.md` > CTA trailing-fragment hallucination.

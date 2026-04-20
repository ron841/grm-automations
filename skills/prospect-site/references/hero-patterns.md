# Hero Patterns Reference

Part of the prospect-site skill v0.8. Loaded by Phase 5 when the skill begins hero generation, in tandem with `section-patterns.md` (which covers every other homepage section).

This file contains the pixel-level spec for the hero region of every generated homepage: the shared Glassmorphism content layer (both size variants), the four background mode implementations, and the optional video augmentation section. CSS variables (`--color-primary`, `--font-heading`, `--space-section`, etc.) come from `css-framework.md`. Vanilla JS animation primitives (cross-fade, parallax scroll, mesh gradient, mousemove parallax) also live in `css-framework.md`.

## Architecture

Every v0.8 hero has two layers:

1. **Content layer.** The Glassmorphism Trust Hero card. Same structural pattern in all four modes. Comes in two size variants (default and wide) selected by Phase 4.

2. **Background layer.** Varies by mode from the Phase 4 decision tree:
   - `parallax` — rotated grid of 6-8 project photos with scroll-driven motion
   - `glass-crossfade` — full-viewport cross-fade slideshow of 4-7 photos
   - `glass-single-mesh` — single background photo with animated mesh gradient overlay
   - `glass-pure-mesh` — pure mesh gradient in brand colors with mousemove parallax blobs

The content layer is identical across modes. Only the background changes. This is the architectural discipline: one hero pattern, deterministic variation.

## Glass card variant selection (Phase 4 logic)

Phase 4 picks between the default and wide glass card variants based on two deterministic structural conditions:

```
useWideVariant = false

IF heroMode == "parallax":
    useWideVariant = true
IF tier == "Premium" (score 70-100):
    useWideVariant = true

designChoices.heroGlassVariant = useWideVariant ? "wide" : "default"
```

Save to `profile-draft.json` under `designChoices.heroGlassVariant`. Phase 5 reads this value and applies the appropriate class.

**Why these two conditions:**

- **Parallax mode** specifically benefits from the wider card because the rotated photo grid background can absorb the extra card weight without visual competition. Other modes (cross-fade, mesh) can feel top-heavy with the wide card.
- **Premium tier** is a business judgment: higher-scoring brands deserve bigger type and more visual weight. Respects the tier work Phase 4 already does.

**Editorial override matters here.** Character count deliberately does NOT trigger the wide variant automatically. A 50-character headline like "Licensed plumbing in Ocala and Marion County since 2006" reads beautifully at 56px in the default card. A short 30-character headline on a Premium-tier brand might still deserve the wide variant. Auto-rules based on character count get it wrong in both directions. Instead, the Phase 4 approval gate accepts `override glass-variant:wide` or `override glass-variant:default` so Ron picks per-prospect when his editorial eye disagrees with the structural default.

No vibes inside the default selection. Full creative control at the approval gate.

---

## Shared glass card content layer

This card renders in all four hero modes. HTML structure is identical; only the outer class modifier differs between default and wide.

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

## Mode: parallax (heroCandidates ≥ 8, all high quality)

When Phase 3 captured 8+ strong landscape photos with zero disqualifiers, the hero becomes a scroll-driven parallax grid. Photos rotate at -6 degrees and move at different speeds as the user scrolls. Glass card floats over the grid with the wide variant (forced by the Phase 4 logic above).

### HTML

```html
<section class="hero hero-parallax">
  <div class="hero-parallax-grid">
    <div class="hero-parallax-row hero-parallax-row-1">
      <img src="assets/photos/work/photo-01.jpg" alt="[work description]">
      <img src="assets/photos/work/photo-02.jpg" alt="[work description]">
      <img src="assets/photos/work/photo-03.jpg" alt="[work description]">
      <img src="assets/photos/work/photo-04.jpg" alt="[work description]">
    </div>
    <div class="hero-parallax-row hero-parallax-row-2">
      <img src="assets/photos/work/photo-05.jpg" alt="[work description]">
      <img src="assets/photos/work/photo-06.jpg" alt="[work description]">
      <img src="assets/photos/work/photo-07.jpg" alt="[work description]">
      <img src="assets/photos/work/photo-08.jpg" alt="[work description]">
    </div>
  </div>
  <div class="hero-parallax-overlay"></div>
  <div class="hero-parallax-content">
    <!-- shared glass card HTML, wide variant class applied -->
  </div>
</section>
```

### CSS

```css
.hero-parallax {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  background: #0a0a0a;
  padding-top: 100px;
}

.hero-parallax-grid {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 100px 0;
  transform: rotate(-6deg) scale(1.3);
  transform-origin: center;
}

.hero-parallax-row {
  display: flex;
  gap: 20px;
  flex-shrink: 0;
  will-change: transform;
}

.hero-parallax-row-1 { transform: translateX(0); }
.hero-parallax-row-2 { transform: translateX(-60px); }

.hero-parallax-row img {
  width: 400px;
  height: 260px;
  object-fit: cover;
  border-radius: 16px;
  flex-shrink: 0;
}

.hero-parallax-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(0,0,0,0.65) 0%, rgba(0,0,0,0.45) 100%);
  z-index: 1;
}

.hero-parallax-content {
  position: relative;
  z-index: 2;
  max-width: 1280px;
  margin: 0 auto;
  padding: 80px 24px 100px;
  display: flex;
  align-items: center;
  min-height: calc(100vh - 100px);
}

@media (max-width: 899px) {
  .hero-parallax-grid { transform: rotate(-4deg) scale(1.6); }
  .hero-parallax-row img { width: 260px; height: 180px; }
}
```

### JavaScript behavior

Uses the `parallaxScroll` primitive from `css-framework.md`. On scroll:
- Row 1 translates at 0.3x scroll speed (moves down slightly as user scrolls down)
- Row 2 translates at -0.2x scroll speed (moves up, opposite direction)
- Creates depth illusion through velocity contrast
- Bound to `window.scroll` with `requestAnimationFrame` throttling
- Disabled on mobile (below 900px) because small viewports don't benefit and the motion can feel janky on low-power devices

### Rules

- Requires 8+ photos minimum from `photoAssignments.heroCandidates`
- All 8 photos must be landscape, minimum 1600px on the long edge, zero disqualifiers
- Glass card is always wide variant in this mode (forced by Phase 4)
- If fewer than 8 photos qualify, Phase 4 falls through to `glass-crossfade`

---

## Mode: glass-crossfade (heroCandidates ≥ 4)

When Phase 3 captured 4-7 strong photos, the hero is a full-viewport cross-fade slideshow. Glass card floats centered over the cycling photos.

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

Uses the `crossfadeSlideshow` primitive from `css-framework.md`. Cycles the `.active` class every 6000ms. Exactly matches the number of photos captured (4-7), never padded with stock, never truncated.

### Rules

- Requires 4-7 photos from `photoAssignments.heroCandidates`
- Glass card variant (default or wide) picked by Phase 4 logic independent of hero mode
- Interval is always 6000ms (6 seconds per slide)
- First slide has `.active` class at page load; cycling starts after 6 seconds

---

## Mode: glass-single-mesh (heroCandidates 1-3)

When Phase 3 captured only 1-3 decent photos, use the single best photo as background with an animated mesh gradient overlay on top. The mesh adds slow organic motion so the hero feels alive even though the photo is static.

### HTML

```html
<section class="hero hero-single-mesh">
  <div class="hero-single-bg" style="background-image: url('assets/photos/work/photo-01.jpg')"></div>
  <canvas class="hero-mesh-canvas" aria-hidden="true"></canvas>
  <div class="hero-single-mesh-overlay"></div>
  <div class="hero-single-mesh-content">
    <!-- shared glass card HTML -->
  </div>
</section>
```

### CSS

```css
.hero-single-mesh {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  padding-top: 100px;
}

.hero-single-bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  z-index: 0;
}

.hero-mesh-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  mix-blend-mode: overlay;
  opacity: 0.6;
  z-index: 1;
}

.hero-single-mesh-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.35) 100%);
  z-index: 2;
}

.hero-single-mesh-content {
  position: relative;
  z-index: 3;
  max-width: 1280px;
  margin: 0 auto;
  padding: 80px 24px 100px;
  display: flex;
  align-items: center;
  min-height: calc(100vh - 100px);
}
```

### JavaScript behavior

Uses the `meshGradient` primitive from `css-framework.md`. Renders flowing blobs in brand colors on the canvas at 30fps. Colors pulled from `brandPalette.primary`, `brandPalette.accent`, and `brandPalette.darkPrimary`. Mix-blend-mode overlay means the mesh colors blend with the background photo for an organic, painterly effect.

### Rules

- Use the highest-quality photo from `photoAssignments.heroCandidates[0]`
- Canvas opacity fixed at 0.6 to keep the photo visible underneath
- Mesh colors always come from the brand palette, never hardcoded

---

## Mode: glass-pure-mesh (heroCandidates 0)

Zero usable photos. Background is pure mesh gradient in brand colors plus a mousemove parallax layer with large blurred blobs. Glass card's trust content becomes the centerpiece since there is no photo to compete.

### HTML

```html
<section class="hero hero-pure-mesh">
  <canvas class="hero-mesh-canvas-full" aria-hidden="true"></canvas>
  <div class="hero-mousemove-layer">
    <div class="hero-mousemove-blob hero-mousemove-blob-1"></div>
    <div class="hero-mousemove-blob hero-mousemove-blob-2"></div>
    <div class="hero-mousemove-blob hero-mousemove-blob-3"></div>
  </div>
  <div class="hero-pure-mesh-content">
    <!-- shared glass card HTML -->
  </div>
</section>
```

### CSS

```css
.hero-pure-mesh {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  padding-top: 100px;
  background: var(--color-dark-primary);
}

.hero-mesh-canvas-full {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  opacity: 0.9;
}

.hero-mousemove-layer {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
}

.hero-mousemove-blob {
  position: absolute;
  width: 600px;
  height: 600px;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.4;
  will-change: transform;
  transition: transform 0.4s ease-out;
}

.hero-mousemove-blob-1 {
  top: -10%;
  left: -10%;
  background: var(--color-primary);
}

.hero-mousemove-blob-2 {
  top: 40%;
  right: -10%;
  background: var(--color-accent);
}

.hero-mousemove-blob-3 {
  bottom: -10%;
  left: 30%;
  background: var(--color-primary);
}

.hero-pure-mesh-content {
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

Uses the `mousemoveParallax` primitive from `css-framework.md`. On mouse move:
- Blob 1 translates at 0.02x of mouse delta
- Blob 2 translates at 0.04x of mouse delta
- Blob 3 translates at 0.03x of mouse delta
- Creates a subtle "living" feel without requiring any prospect photography

Falls back gracefully on touch devices (no mousemove events) where the static mesh canvas provides enough motion on its own.

### Rules

- No photos required
- Background color `var(--color-dark-primary)` ensures the mesh colors have contrast
- Use this mode when `photoAssignments.heroCandidates.length === 0` — this is the ultimate fallback

---

## Video augmentation (additive, not replacing)

When Phase 3 captured a video URL (any mode), append a Hero Video Dialog section BELOW the main hero but before the trust marquee. Do not replace the main hero. Most contractors will not have video. The ones who do get the upgrade.

### HTML

```html
<section class="hero-video-augment">
  <div class="hero-video-container">
    <div class="hero-video-eyebrow">WATCH US WORK</div>
    <h2 class="hero-video-title">See what 50 years of experience looks like on the job.</h2>
    <div class="hero-video-player" data-video-url="[url]">
      <img src="assets/photos/video-thumbnail.jpg" alt="Video thumbnail" class="hero-video-thumb">
      <button class="hero-video-play" aria-label="Play video">
        <svg viewBox="0 0 80 80" width="80" height="80" aria-hidden="true">
          <circle cx="40" cy="40" r="38" fill="rgba(255,255,255,0.2)" stroke="#fff" stroke-width="2"/>
          <polygon points="32,24 32,56 56,40" fill="#ffffff"/>
        </svg>
      </button>
    </div>
  </div>
</section>
```

### CSS

```css
.hero-video-augment {
  padding: var(--space-section) 24px;
  background: var(--color-background);
}

.hero-video-container {
  max-width: 1100px;
  margin: 0 auto;
  text-align: center;
}

.hero-video-eyebrow {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--color-primary);
  margin-bottom: 16px;
}

.hero-video-title {
  font-family: var(--font-heading);
  font-size: 44px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -1px;
  color: var(--color-dark-primary);
  margin: 0 0 48px 0;
}

.hero-video-player {
  position: relative;
  border-radius: 24px;
  overflow: hidden;
  aspect-ratio: 16 / 9;
  cursor: pointer;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease;
}

.hero-video-player:hover {
  transform: translateY(-4px);
}

.hero-video-thumb {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.hero-video-play {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: none;
  border: none;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.hero-video-play:hover {
  transform: translate(-50%, -50%) scale(1.1);
}

@media (max-width: 899px) {
  .hero-video-title { font-size: 28px; }
}
```

### JavaScript behavior

On click, opens a modal dialog with the video embedded. Uses the `videoDialog` primitive from `css-framework.md`. Supports YouTube, Vimeo, and direct mp4 URLs from the `data-video-url` attribute.

### Rules

- Only render if `phase3.videoUrl` is non-null in `profile.json`
- Video thumbnail should be either a still from the video or a high-quality project photo from `photoAssignments.heroCandidates[0]`
- Never use stock video footage
- This section is additive — it sits BELOW the main hero, before the trust marquee, and does not replace any mode

---

## Section spacing rules for the hero region

The hero always takes `min-height: 100vh` to fill the initial viewport. The video augmentation section (when present) uses the standard `var(--space-section)` padding from `css-framework.md`. No hero-specific overrides to those spacing variables.

Do NOT add `padding-top` or `margin-top` to the hero beyond the 100px allowance for the fixed nav. The hero fills the viewport; the nav overlays it. This is intentional.

---

## Common mistakes for the hero (all modes)

- Do not use a 4:3 aspect ratio photo card. The hero takes full viewport.
- Do not hardcode white background behind the glass card. The background IS the mode.
- Do not use 5+ slides in cross-fade beyond what Phase 3 captured. Never pad with stock.
- Do not omit the glass card. All four modes use the same glass card.
- Do not use a photo with a watermark, logo, or baked-in text as hero background.
- Do not use `box-shadow` offset blocks behind the glass card (that was v0.5's pattern, not v0.8's).
- Do not apply the wide variant to modes other than parallax unless Phase 4 selected it (character count or Premium tier).
- Do not hardcode the headline font-size — use the shared glass card CSS which switches via the modifier class.
- Do not add a third button, `<small>` fragment, or disclaimer copy below the `<div class="hero-ctas">` block. The two buttons defined in the shared glass card content layer are the complete CTA. See `anti-slop-rules.md` > CTA trailing-fragment hallucination.

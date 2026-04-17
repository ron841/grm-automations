# Section Patterns Reference

Part of the prospect-site skill v0.7. Loaded by Phase 5 when the skill begins section generation, in tandem with `hero-patterns.md` (which covers the hero region).

This file contains the pixel-level spec for every non-hero section of the generated homepage: nav, promo bar, trust marquee, services grid, stats section (the mandatory dark section), before/after gallery, testimonials, featured promotion callout, FAQ, contact form, footer, and mobile bottom CTA bar. CSS variables (`--color-primary`, `--space-section`, etc.) come from `css-framework.md`. Animation primitives (marquee, glare hover, shimmer button, before/after drag) also live in `css-framework.md`.

## Section order (reminder from SKILL.md Phase 5)

1. Sticky nav with click-to-call
2. Promo bar (if real promotion captured)
3. Hero (see `hero-patterns.md`)
4. Trust marquee (if real credentials captured)
5. Services grid (asymmetric Bento)
6. Stats section (mandatory dark section)
7. Before/after gallery (if before/after images captured)
8. Testimonials
9. Featured promotion callout (if real promotion captured)
10. FAQ accordion
11. Contact form
12. Footer
13. Mobile bottom CTA bar (mobile only)

## Section spacing system

Vertical rhythm is controlled by CSS custom properties defined in `css-framework.md`:

```css
:root {
  --space-section: 120px;              /* Default section padding (services, testimonials, FAQ, contact) */
  --space-section-compact: 60px;       /* Trust marquee and similar thin strips */
  --space-section-generous: 140px;     /* Stats dark section gets extra breathing room */
  --space-section-promo: 100px;        /* Featured promotion callout */
}

@media (max-width: 899px) {
  :root {
    --space-section: 80px;
    --space-section-compact: 40px;
    --space-section-generous: 100px;
    --space-section-promo: 72px;
  }
}
```

Every section below uses these variables. Never hardcode `120px` or `140px` as section padding in individual section CSS. This guarantees consistent rhythm across the whole homepage and makes global rhythm adjustments a one-line change.

---

## 1. Sticky Navigation

### Purpose

Primary navigation with logo, page links, and a persistent click-to-call phone button. On mobile, collapses to hamburger but the phone button stays visible because mobile is where most contractor calls come from.

### HTML structure

```html
<nav class="nav" role="navigation" aria-label="Main navigation">
  <div class="nav-container">
    <a href="/" class="nav-logo">
      <img src="assets/logo.png" alt="[Business Name]">
    </a>
    <ul class="nav-links">
      <li><a href="/">Home</a></li>
      <li><a href="/about.html">About</a></li>
      <li><a href="/services.html">Services</a></li>
      <li><a href="/testimonials.html">Testimonials</a></li>
      <li><a href="/contact.html">Contact</a></li>
    </ul>
    <a href="tel:[phone]" class="nav-phone">
      <span class="nav-phone-icon">📞</span>
      <span class="nav-phone-text">[phone formatted]</span>
    </a>
    <button class="nav-hamburger" aria-label="Open menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>
```

### CSS

```css
.nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  transition: background 0.3s ease, box-shadow 0.3s ease;
}

.nav.scrolled {
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.nav-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 32px;
}

.nav-logo img {
  height: 44px;
  width: auto;
}

.nav-links {
  display: flex;
  gap: 32px;
  list-style: none;
  margin: 0;
  padding: 0;
  flex: 1;
  justify-content: center;
}

.nav-links a {
  color: #1a1a1a;
  text-decoration: none;
  font-weight: 500;
  font-size: 15px;
  transition: color 0.2s ease;
}

.nav-links a:hover {
  color: var(--color-primary);
}

.nav-phone {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 12px 22px;
  background: var(--color-primary);
  color: #ffffff;
  text-decoration: none;
  font-weight: 600;
  font-size: 15px;
  border-radius: 999px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  position: relative;
  overflow: hidden;
}

.nav-phone::before {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(110deg, transparent 30%, rgba(255,255,255,0.3) 50%, transparent 70%);
  transform: translateX(-100%);
  animation: shimmer 3s infinite;
}

@keyframes shimmer {
  0%, 100% { transform: translateX(-100%); }
  50% { transform: translateX(100%); }
}

.nav-phone:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.nav-hamburger {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
}

@media (max-width: 899px) {
  .nav-links { display: none; }
  .nav-hamburger { display: block; }
  .nav-phone-text { display: none; }
  .nav-phone { padding: 12px 14px; }
  .nav-container { padding: 12px 20px; gap: 16px; }
}

.nav-links.open {
  display: flex;
  position: fixed;
  top: 72px;
  left: 0;
  right: 0;
  flex-direction: column;
  background: #ffffff;
  padding: 24px;
  gap: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}
```

### Rules

- Logo image goes in the nav, never as a hero background
- Phone button uses Shimmer Button treatment from Magic UI extracts
- Mobile hamburger opens a fullwidth drawer; phone button stays visible outside the hamburger at all times
- Nav gains `.scrolled` class after 40px of scroll (JS in `css-framework.md` animation toolkit)
- Nav height is fixed at ~76px on desktop, ~68px on mobile

### Common mistakes

- Do not let the phone button collapse into the hamburger on mobile
- Do not use `position: sticky` — use `position: fixed` so the nav stays visible during scroll-driven hero animations
- Do not hardcode the logo height; use `44px` on desktop and `40px` on mobile

---

## 2. Promo Bar

### Purpose

Thin top announcement strip for real captured promotions. Rendered ONLY if Phase 2 captured a real promotion with real pricing. Never invented.

### HTML

```html
<div class="promo-bar" role="banner">
  <div class="promo-bar-content">
    <strong>$450 Whole House Surge Arrestor Special.</strong>
    Do not be a victim of the next lightning storm.
    <a href="tel:[phone]">Call [phone formatted]</a>.
  </div>
  <button class="promo-bar-close" aria-label="Dismiss">×</button>
</div>
```

### CSS

```css
.promo-bar {
  background: var(--color-dark-primary);
  color: #ffffff;
  padding: 10px 24px;
  padding-top: calc(10px + env(safe-area-inset-top));
  text-align: center;
  font-size: 14px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 101;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.promo-bar-content {
  flex: 1;
  max-width: 1000px;
}

.promo-bar a {
  color: #ffffff;
  text-decoration: underline;
  font-weight: 600;
  margin-left: 8px;
}

.promo-bar-close {
  background: none;
  border: none;
  color: #ffffff;
  font-size: 24px;
  cursor: pointer;
  padding: 0 8px;
  opacity: 0.8;
}

.promo-bar-close:hover { opacity: 1; }

/* When promo bar exists, push nav down */
body.has-promo-bar .nav { top: 44px; }
body.has-promo-bar main { padding-top: 120px; }
```

### Rules

- iOS safe area padding is required (`env(safe-area-inset-top)`) to avoid clipping by Dynamic Island
- Content uses the exact pricing and wording from Phase 2 capture
- Dismissable (close button sets `display: none` and stores in sessionStorage)
- Push the nav down when promo bar is present

---

## 3. Trust Marquee

Only render if Phase 2 captured real credentials (license numbers, BBB, insurance, certifications, years in business).

### HTML

```html
<section class="trust-marquee">
  <div class="trust-marquee-track">
    <div class="trust-item">★ 4.6 Rating on Google</div>
    <div class="trust-item">Florida License EC13007855</div>
    <div class="trust-item">50+ Years in Business</div>
    <div class="trust-item">24/7 Emergency Service</div>
    <div class="trust-item">Licensed &amp; Insured</div>
    <!-- duplicate items for seamless loop -->
    <div class="trust-item">★ 4.6 Rating on Google</div>
    <div class="trust-item">Florida License EC13007855</div>
    <div class="trust-item">50+ Years in Business</div>
    <div class="trust-item">24/7 Emergency Service</div>
    <div class="trust-item">Licensed &amp; Insured</div>
  </div>
</section>
```

### CSS

```css
.trust-marquee {
  background: var(--color-background);
  padding: var(--space-section-compact) 0;
  overflow: hidden;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.trust-marquee-track {
  display: flex;
  gap: 64px;
  animation: marquee-scroll 40s linear infinite;
  width: max-content;
}

@keyframes marquee-scroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

.trust-item {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-dark-primary);
  white-space: nowrap;
  display: flex;
  align-items: center;
  letter-spacing: 0.3px;
}

.trust-marquee-track:hover {
  animation-play-state: paused;
}
```

### Rules

- Only render if 3+ real credentials captured
- Duplicate the item list exactly once for seamless loop
- Never fabricate credentials

---

## 4. Services Grid (Asymmetric Bento)

The asymmetric services grid is one of the main v0.7 wow-gap fixes. One featured service is larger and has a photo background. The rest are smaller cards in a Bento layout. Replaces the v0.6 uniform 4-column grid of identical cards.

### HTML

```html
<section class="services-section" id="services">
  <div class="services-container">
    <div class="services-header">
      <div class="services-eyebrow">OUR SERVICES</div>
      <h2 class="services-title">Twelve services. One licensed team.</h2>
      <p class="services-subtitle">Every job in [primary city] and [primary county].</p>
    </div>

    <div class="services-bento">
      <!-- Featured service: 2 cols wide x 2 rows tall -->
      <div class="service-card service-card-featured" style="background-image: url('assets/photos/services/featured.jpg')">
        <div class="service-card-overlay"></div>
        <div class="service-card-content">
          <div class="service-card-tag">FEATURED SPECIALTY</div>
          <h3 class="service-card-title">Whole House Surge Protection</h3>
          <p class="service-card-desc">Protect your flat screen TVs, appliances, and electronics from Florida lightning. $450 special, installed.</p>
          <a href="#contact" class="service-card-cta">Get a quote →</a>
        </div>
      </div>

      <!-- Standard service cards: 1 col x 1 row each -->
      <div class="service-card">
        <div class="service-card-icon-wrap">
          <!-- Lucide icon SVG for the service type -->
        </div>
        <h3 class="service-card-title-sm">Residential Electrical</h3>
        <p class="service-card-desc-sm">New construction, renovation, additions, and upgrades.</p>
      </div>

      <!-- Repeat for remaining services -->
    </div>
  </div>
</section>
```

### CSS

```css
.services-section {
  padding: var(--space-section) 24px;
  background: var(--color-background);
}

.services-container {
  max-width: 1280px;
  margin: 0 auto;
}

.services-header {
  text-align: center;
  margin-bottom: 64px;
}

.services-eyebrow {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--color-primary);
  margin-bottom: 16px;
}

.services-title {
  font-family: var(--font-heading);
  font-size: 48px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -1px;
  color: var(--color-dark-primary);
  margin: 0 0 16px 0;
}

.services-subtitle {
  font-size: 18px;
  color: #555;
  max-width: 560px;
  margin: 0 auto;
}

.services-bento {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: 220px;
  gap: 20px;
}

.service-card {
  padding: 32px 28px;
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: default;
}

.service-card::before {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(110deg, transparent 40%, rgba(255,255,255,0.5) 50%, transparent 60%);
  transform: translateX(-100%);
  transition: transform 0.8s ease;
}

.service-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.1);
}

.service-card:hover::before {
  transform: translateX(100%);
}

/* Featured service spans 2x2 */
.service-card-featured {
  grid-column: span 2;
  grid-row: span 2;
  background-size: cover;
  background-position: center;
  padding: 0;
  display: flex;
  align-items: flex-end;
  min-height: 460px;
}

.service-card-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(0,0,0,0) 40%, rgba(0,0,0,0.85) 100%);
}

.service-card-content {
  position: relative;
  z-index: 1;
  padding: 36px 32px;
  color: #ffffff;
  width: 100%;
}

.service-card-tag {
  display: inline-block;
  padding: 6px 12px;
  background: var(--color-primary);
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1px;
  margin-bottom: 16px;
}

.service-card-title {
  font-family: var(--font-heading);
  font-size: 32px;
  font-weight: 700;
  line-height: 1.1;
  margin: 0 0 12px 0;
}

.service-card-desc {
  font-size: 15px;
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 20px 0;
  max-width: 420px;
}

.service-card-cta {
  color: #ffffff;
  text-decoration: none;
  font-weight: 600;
  font-size: 15px;
  border-bottom: 2px solid var(--color-accent);
  padding-bottom: 2px;
}

/* Standard cards */
.service-card-icon-wrap {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: rgba(var(--color-primary-rgb), 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  color: var(--color-primary);
}

.service-card-title-sm {
  font-family: var(--font-heading);
  font-size: 20px;
  font-weight: 700;
  color: var(--color-dark-primary);
  margin: 0 0 8px 0;
  line-height: 1.2;
}

.service-card-desc-sm {
  font-size: 14px;
  line-height: 1.5;
  color: #555;
  margin: 0;
}

@media (max-width: 899px) {
  .services-bento {
    grid-template-columns: repeat(2, 1fr);
    grid-auto-rows: 200px;
  }
  .service-card-featured {
    grid-column: span 2;
    grid-row: span 2;
    min-height: 400px;
  }
  .services-title { font-size: 32px; }
}
```

### Rules

- Exactly one service is featured (2x2) per build. Usually the one Phase 2 captured as a "featured specialty" or "special offer"
- Featured service MUST have a photo background from `servicesGridPhotos`
- Standard service cards use Lucide icons matching the service type (icon library referenced in `css-framework.md`)
- Service descriptions are 1-2 sentences max, benefit-first, in Closing Table voice (per content-rules.md voice mapping)
- All captured services render. Never collapse 12 to 6.

### Common mistakes

- Do not use all icons, no photos — the featured card MUST have a photo
- Do not repeat the same icon across multiple services
- Do not use generic descriptions like "Quality service you can trust"
- Do not use more than one featured service per grid

---

## 5. Stats Section (THE DARK SECTION)

This is the mandatory dark section for the page. Placed between services and testimonials. Oversized numbers, near-black background, white text. It is the single rhythm reset of the page. Phase 6 check 10 enforces exactly one dark section per page and this is it.

### HTML

```html
<section class="stats-section">
  <div class="stats-container">
    <div class="stats-header">
      <div class="stats-eyebrow">BY THE NUMBERS</div>
      <h2 class="stats-title">Real work. Real results.</h2>
    </div>

    <div class="stats-grid">
      <div class="stats-item">
        <div class="stats-number" data-target="50">0</div>
        <div class="stats-label">Years Licensed</div>
      </div>
      <div class="stats-item">
        <div class="stats-number" data-target="41">0</div>
        <div class="stats-label">Google Reviews</div>
      </div>
      <div class="stats-item">
        <div class="stats-number-static">4.6★</div>
        <div class="stats-label">Average Rating</div>
      </div>
      <div class="stats-item">
        <div class="stats-number-static">24/7</div>
        <div class="stats-label">Emergency Service</div>
      </div>
    </div>
  </div>
</section>
```

### CSS

```css
.stats-section {
  padding: var(--space-section-generous) 24px;
  background: #0a0a0a;
  color: #ffffff;
  position: relative;
  overflow: hidden;
}

.stats-section::before {
  content: "";
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 20% 30%, rgba(var(--color-primary-rgb), 0.15) 0%, transparent 50%),
              radial-gradient(circle at 80% 70%, rgba(var(--color-accent-rgb), 0.1) 0%, transparent 50%);
  pointer-events: none;
}

.stats-container {
  max-width: 1280px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.stats-header {
  text-align: center;
  margin-bottom: 80px;
}

.stats-eyebrow {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--color-accent);
  margin-bottom: 16px;
}

.stats-title {
  font-family: var(--font-heading);
  font-size: 56px;
  font-weight: 700;
  line-height: 1.05;
  letter-spacing: -1.5px;
  margin: 0;
  color: #ffffff;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 40px;
  text-align: center;
}

.stats-item {
  padding: 20px 16px;
}

.stats-number,
.stats-number-static {
  font-family: var(--font-heading);
  font-size: 96px;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -3px;
  color: #ffffff;
  margin-bottom: 16px;
  background: linear-gradient(180deg, #ffffff 0%, rgba(255,255,255,0.7) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.stats-label {
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.7);
}

@media (max-width: 899px) {
  .stats-title { font-size: 36px; }
  .stats-grid { grid-template-columns: repeat(2, 1fr); gap: 24px; }
  .stats-number, .stats-number-static { font-size: 64px; }
}
```

### JavaScript: stats counter discipline

Every stat is either ANIMATED or STATIC. Animated stats have `data-target="[whole-number]"` and get animated from 0 to target by the `numberTicker` primitive in `css-framework.md`. Static stats have no `data-target` and are rendered as plain text (class `stats-number-static`).

**Critical:** The `numberTicker` animation function must only observe elements with a `data-target` attribute. Elements without `data-target` are left alone. This is the architectural fix for the v0.6 "0 Years Licensed" bug class and Phase 6 check 8 enforces it at build time.

### Rules

- Exactly 3 or 4 stats. Never more, never fewer.
- Real numbers only. Pulled from `profile.json`.
- Animated stats for whole numbers (years, review count, projects completed)
- Static stats for non-integer values (4.6★, 24/7, A+, license numbers)
- Background is always near-black (#0a0a0a). No other color allowed in this section.
- This is the ONLY dark section on the page. Phase 6 check 10 enforces this.

---

## 6. Before/After Gallery

Only render if Phase 3 captured at least one before/after image pair. Drag slider reveals the comparison. Supports multiple pairs via thumbnail navigation.

### HTML

```html
<section class="beforeafter-section">
  <div class="beforeafter-container">
    <div class="beforeafter-header">
      <div class="beforeafter-eyebrow">SEE THE DIFFERENCE</div>
      <h2 class="beforeafter-title">Real projects across Marion County.</h2>
    </div>

    <div class="beforeafter-compare" data-ba-index="0">
      <div class="beforeafter-image-before" style="background-image: url('assets/photos/before/01.jpg')"></div>
      <div class="beforeafter-image-after" style="background-image: url('assets/photos/after/01.jpg')"></div>
      <span class="beforeafter-label beforeafter-label-before">BEFORE</span>
      <span class="beforeafter-label beforeafter-label-after">AFTER</span>
      <div class="beforeafter-handle" role="slider" aria-label="Drag to compare" tabindex="0" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100">
        <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
          <path d="M8 5v14l-5-7zM16 5v14l5-7z" fill="currentColor"/>
        </svg>
      </div>
    </div>

    <!-- Thumbnail nav for multiple pairs, only if Phase 3 captured 2+ pairs -->
    <div class="beforeafter-nav" aria-label="Select project">
      <button class="beforeafter-nav-thumb active" data-ba-target="0" aria-label="Project 1">
        <img src="assets/photos/after/01.jpg" alt="">
      </button>
      <button class="beforeafter-nav-thumb" data-ba-target="1" aria-label="Project 2">
        <img src="assets/photos/after/02.jpg" alt="">
      </button>
    </div>
  </div>
</section>
```

### CSS

```css
.beforeafter-section {
  padding: var(--space-section) 24px;
  background: #ffffff;
}

.beforeafter-container {
  max-width: 1100px;
  margin: 0 auto;
}

.beforeafter-header {
  text-align: center;
  margin-bottom: 56px;
}

.beforeafter-eyebrow {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--color-primary);
  margin-bottom: 16px;
}

.beforeafter-title {
  font-family: var(--font-heading);
  font-size: 48px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -1px;
  color: var(--color-dark-primary);
  margin: 0;
}

.beforeafter-compare {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 10;
  border-radius: 24px;
  overflow: hidden;
  cursor: ew-resize;
  user-select: none;
  touch-action: pan-y;  /* Allow vertical scroll, capture horizontal drag for slider */
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

.beforeafter-image-before,
.beforeafter-image-after {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
}

.beforeafter-image-after {
  clip-path: inset(0 50% 0 0);
  transition: clip-path 0.05s linear;
}

.beforeafter-label {
  position: absolute;
  top: 24px;
  padding: 8px 16px;
  background: rgba(0, 0, 0, 0.75);
  color: #ffffff;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1.5px;
  border-radius: 6px;
  backdrop-filter: blur(4px);
}

.beforeafter-label-before {
  left: 24px;
}

.beforeafter-label-after {
  right: 24px;
}

.beforeafter-handle {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 50%;
  width: 4px;
  background: #ffffff;
  cursor: ew-resize;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.15);
  transform: translateX(-50%);
}

.beforeafter-handle::before {
  content: "";
  position: absolute;
  width: 56px;
  height: 56px;
  background: #ffffff;
  border-radius: 50%;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.beforeafter-handle svg {
  position: relative;
  z-index: 1;
  color: var(--color-dark-primary);
}

.beforeafter-handle:focus {
  outline: none;
}

.beforeafter-handle:focus::before {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3), 0 0 0 3px rgba(var(--color-primary-rgb), 0.4);
}

.beforeafter-nav {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-top: 32px;
  flex-wrap: wrap;
}

.beforeafter-nav-thumb {
  width: 88px;
  height: 64px;
  padding: 0;
  border: 2px solid transparent;
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  background: none;
  transition: border-color 0.2s ease, transform 0.2s ease;
}

.beforeafter-nav-thumb:hover {
  transform: scale(1.05);
}

.beforeafter-nav-thumb.active {
  border-color: var(--color-primary);
}

.beforeafter-nav-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

@media (max-width: 899px) {
  .beforeafter-title { font-size: 32px; }
  .beforeafter-compare { aspect-ratio: 4 / 3; }
  .beforeafter-handle::before { width: 48px; height: 48px; }
  .beforeafter-label { top: 16px; padding: 6px 12px; font-size: 11px; }
  .beforeafter-label-before { left: 16px; }
  .beforeafter-label-after { right: 16px; }
  .beforeafter-nav-thumb { width: 64px; height: 48px; }
}
```

### JavaScript behavior

Uses the `beforeAfterCompare` primitive from `css-framework.md`. Responsibilities:

- Mouse drag: track mouse X position, update `clip-path` on `.beforeafter-image-after` to match, update `.beforeafter-handle` left position
- Touch drag: same logic with touch events
- Keyboard: arrow keys move handle 5% per press, Home/End jump to 0/100%, update `aria-valuenow`
- Thumbnail nav click: swap `background-image` values on both `.beforeafter-image-before` and `.beforeafter-image-after`, reset clip-path to 50%, update active class on thumbnails
- Handle hover cursor visual feedback
- Initial state: clip-path at 50% (centered)

### Rules

- Only render if Phase 3 captured at least one before/after pair
- If multiple pairs captured, render the thumbnail nav. If only one pair, omit the nav entirely.
- Labels are always "BEFORE" and "AFTER" in uppercase, placed in corner overlays
- Aspect ratio is 16:10 desktop, 4:3 mobile to maximize usable image area
- Required for pressure washers, painters, roofers, pool builders, and remodelers. These verticals live or die on visual proof of quality.
- **Mobile scroll conflict:** The `.beforeafter-compare` container has `touch-action: pan-y` set in CSS. This tells the browser that horizontal drag belongs to the slider but vertical scroll stays with the page. Without this rule, mobile users try to drag the slider and accidentally scroll the page, or worse, both happen at once and the interaction feels broken.
- **Image preload for slow connections:** Both before and after images must be preloaded so the slider works immediately when scrolled into view. Add `<link rel="preload" as="image" href="assets/photos/before/01.jpg">` and the matching after image to the `<head>` of the generated HTML. Also set `loading="eager"` on the image elements if converting from background-image to `<img>` tags. Without preload, mobile users on slow connections see a broken-looking slider for 3 to 4 seconds while images fetch, and the first impression is "this website is broken."
- **Aspect ratio consistency between pairs:** Before and after photos in the same pair must match aspect ratio within 5 percent. If the before is 16:9 and the after is 4:3, the slider will crop or stretch one of them and the comparison looks off. Phase 3 enforces this in `image-handling.md` pair detection logic: pairs that fail the aspect ratio check are dropped, and the next-best pair is used instead. If no pair survives the check, the entire before/after section is omitted from the build and Phase 6 records "no before/after pairs matched aspect ratio requirements" as a soft warning (not a hard failure, the site still ships).
- **Before/after pair DETECTION** is covered in `image-handling.md` under "Before/After Pair Detection Logic." Phase 3 identifies pairs by filename conventions (`before-*` / `after-*`), adjacent position in a gallery with matching captions, or dedicated portfolio page markup. The pair detection rules live there because they are image pipeline logic, not section layout.
- **Thumbnail data via window.BA_PAIRS:** When multiple pairs render, Phase 5 writes an inline `<script>` tag in the homepage `<head>` defining `window.BA_PAIRS` as an array of `{before, after, caption}` objects matching the thumbnail order. The `beforeAfterCompare` primitive in `css-framework.md` reads this array when a user clicks a thumbnail, swapping the background images on the compare container. See SKILL.md Phase 5 "Cross-file integration points" for the exact script block format. If only one pair renders, `window.BA_PAIRS` is unnecessary and can be omitted.

---

## 7. Testimonials

Real first names, real cities, verbatim quotes. Minimum 4, target 6-8.

### HTML

```html
<section class="testimonials-section">
  <div class="testimonials-container">
    <div class="testimonials-header">
      <div class="testimonials-eyebrow">REAL REVIEWS</div>
      <h2 class="testimonials-title">What Marion County says about [Business].</h2>
      <div class="testimonials-rating">
        <span class="testimonials-stars">★★★★★</span>
        <span class="testimonials-rating-text">4.6 from 41 Google reviews</span>
      </div>
    </div>

    <div class="testimonials-grid">
      <div class="testimonial-card">
        <div class="testimonial-stars">★★★★★</div>
        <p class="testimonial-quote">T &amp; F Electric has done my electrical work for years. They're the only one I rely on in Dunnellon. Very prompt, great service, fair price.</p>
        <div class="testimonial-author">
          <div class="testimonial-name">Jack C.</div>
          <div class="testimonial-location">Dunnellon, FL</div>
        </div>
      </div>
      <!-- Repeat for all captured testimonials -->
    </div>
  </div>
</section>
```

### CSS

```css
.testimonials-section {
  padding: var(--space-section) 24px;
  background: var(--color-background);
}

.testimonials-container {
  max-width: 1280px;
  margin: 0 auto;
}

.testimonials-header {
  text-align: center;
  margin-bottom: 64px;
}

.testimonials-eyebrow {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--color-primary);
  margin-bottom: 16px;
}

.testimonials-title {
  font-family: var(--font-heading);
  font-size: 48px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -1px;
  color: var(--color-dark-primary);
  margin: 0 0 20px 0;
}

.testimonials-rating {
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

.testimonials-stars {
  color: #f5a623;
  font-size: 20px;
  letter-spacing: 2px;
}

.testimonials-rating-text {
  font-size: 15px;
  color: #555;
  font-weight: 500;
}

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
}

.testimonial-card {
  padding: 36px 32px;
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.testimonial-card::before {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(110deg, transparent 40%, rgba(255,255,255,0.6) 50%, transparent 60%);
  transform: translateX(-100%);
  transition: transform 0.8s ease;
  pointer-events: none;
}

.testimonial-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.08);
}

.testimonial-card:hover::before {
  transform: translateX(100%);
}

.testimonial-stars {
  color: #f5a623;
  font-size: 16px;
  letter-spacing: 2px;
  margin-bottom: 16px;
}

.testimonial-quote {
  font-size: 16px;
  line-height: 1.6;
  color: #333;
  margin: 0 0 24px 0;
  font-style: normal;
}

.testimonial-author {
  padding-top: 20px;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
}

.testimonial-name {
  font-weight: 700;
  font-size: 15px;
  color: var(--color-dark-primary);
}

.testimonial-location {
  font-size: 13px;
  color: #777;
  margin-top: 2px;
}

@media (max-width: 899px) {
  .testimonials-title { font-size: 32px; }
  .testimonials-grid { grid-template-columns: 1fr; gap: 20px; }
}
```

### Rules

- Every testimonial has a real first name (or first name + last initial)
- Every testimonial has a real city if captured, or "[Business's primary city]" if not captured
- Every quote is verbatim from Phase 2 capture
- Minimum 4, target 6-8, no maximum
- Never use "Happy Customer" or "Google Reviewer" as a name — if the name is unknown, do not include the testimonial
- Header shows real overall rating and real review count (from Google Places canonical values)
- Use Glare Hover effect on cards (Magic UI extract)

---

## 8. Featured Promotion Callout

Only render if Phase 2 captured a real promotion with real pricing.

### HTML

```html
<section class="promo-callout">
  <div class="promo-callout-container">
    <div class="promo-callout-content">
      <div class="promo-callout-eyebrow">LIMITED TIME</div>
      <h2 class="promo-callout-title">Whole House Surge Protection. $450.</h2>
      <p class="promo-callout-sub">Florida is the lightning capital of the United States. Do not be a victim of the next storm.</p>
      <a href="tel:[phone]" class="promo-callout-cta">Call [phone formatted]</a>
    </div>
  </div>
</section>
```

### CSS

```css
.promo-callout {
  padding: var(--space-section-promo) 24px;
  background: var(--color-primary);
  color: #ffffff;
  position: relative;
  overflow: hidden;
}

.promo-callout::before {
  content: "";
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 80% 50%, rgba(255,255,255,0.15) 0%, transparent 60%);
}

.promo-callout-container {
  max-width: 900px;
  margin: 0 auto;
  text-align: center;
  position: relative;
  z-index: 1;
}

.promo-callout-eyebrow {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 3px;
  text-transform: uppercase;
  opacity: 0.9;
  margin-bottom: 16px;
}

.promo-callout-title {
  font-family: var(--font-heading);
  font-size: 56px;
  font-weight: 800;
  line-height: 1.05;
  letter-spacing: -1.5px;
  margin: 0 0 20px 0;
}

.promo-callout-sub {
  font-size: 20px;
  line-height: 1.5;
  max-width: 640px;
  margin: 0 auto 36px;
  opacity: 0.92;
}

.promo-callout-cta {
  display: inline-flex;
  align-items: center;
  padding: 20px 40px;
  background: #ffffff;
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 700;
  font-size: 18px;
  border-radius: 999px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.promo-callout-cta:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
}

@media (max-width: 899px) {
  .promo-callout-title { font-size: 36px; }
  .promo-callout-sub { font-size: 16px; }
}
```

### Rules

- Use exact pricing from Phase 2
- Use exact wording from the prospect's own site, lightly tightened to Closing Table voice (per content-rules.md voice mapping: promos use Closing Table)
- Never invent a promotion
- Only one callout per homepage
- No trailing elements below the CTA. The promo-callout is a single-CTA section: the `<a class="promo-callout-cta">` is the final element. No `<small>` fine-print, no SMS opt-out copy, no secondary pill button. See `anti-slop-rules.md` > CTA trailing-fragment hallucination.

---

## 9. FAQ Accordion

5-7 FAQs, category-specific, addresses common objections for the vertical.

### HTML

```html
<section class="faq-section">
  <div class="faq-container">
    <div class="faq-header">
      <div class="faq-eyebrow">FAQ</div>
      <h2 class="faq-title">Common questions.</h2>
    </div>
    <div class="faq-list">
      <details class="faq-item">
        <summary class="faq-question">Do you offer 24/7 emergency service?</summary>
        <div class="faq-answer">Yes. T&amp;F Electric provides 24-hour emergency electrical service across Dunnellon, Ocala, and Marion County. Call (352) 465-4600 any time. Overtime charges apply for after-hours calls.</div>
      </details>
      <!-- Repeat for 4-6 more FAQs -->
    </div>
  </div>
</section>
```

### CSS

```css
.faq-section {
  padding: var(--space-section) 24px;
  background: #ffffff;
}

.faq-container {
  max-width: 860px;
  margin: 0 auto;
}

.faq-header {
  text-align: center;
  margin-bottom: 56px;
}

.faq-eyebrow {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--color-primary);
  margin-bottom: 16px;
}

.faq-title {
  font-family: var(--font-heading);
  font-size: 48px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -1px;
  color: var(--color-dark-primary);
  margin: 0;
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.faq-item {
  background: var(--color-background);
  border-radius: 16px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: box-shadow 0.3s ease;
}

.faq-item[open] {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
}

.faq-question {
  padding: 24px 28px;
  font-size: 18px;
  font-weight: 600;
  color: var(--color-dark-primary);
  cursor: pointer;
  list-style: none;
  position: relative;
  padding-right: 56px;
}

.faq-question::-webkit-details-marker { display: none; }

.faq-question::after {
  content: "+";
  position: absolute;
  right: 28px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 28px;
  font-weight: 400;
  color: var(--color-primary);
  transition: transform 0.3s ease;
}

.faq-item[open] .faq-question::after {
  content: "−";
}

.faq-answer {
  padding: 0 28px 24px;
  font-size: 16px;
  line-height: 1.6;
  color: #555;
}

@media (max-width: 899px) {
  .faq-title { font-size: 32px; }
  .faq-question { font-size: 16px; padding: 20px 24px; padding-right: 48px; }
}
```

### Rules

- 5-7 FAQs per build
- Generated from Phase 2 data plus category-specific templates in `content-rules.md`
- One-at-a-time expand by default (use `<details>` without `name` attribute — native toggle)
- Questions address: response time, licensing, emergency availability, pricing, warranty, service areas

---

## 10. Contact Form

For the full form HTML with Static Forms wiring, see `deployment.md`. CSS goes here.

### CSS

```css
.contact-section {
  padding: var(--space-section) 24px;
  background: var(--color-background);
}

.contact-container {
  max-width: 1100px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 60px;
  background: #ffffff;
  padding: 60px;
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.08);
}

.contact-form-wrap h2 {
  font-family: var(--font-heading);
  font-size: 40px;
  font-weight: 700;
  margin: 0 0 12px 0;
  color: var(--color-dark-primary);
}

.contact-form-wrap p {
  font-size: 16px;
  color: #555;
  margin: 0 0 32px 0;
}

.contact-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.contact-form input,
.contact-form select,
.contact-form textarea {
  padding: 16px 18px;
  border: 1.5px solid rgba(0, 0, 0, 0.12);
  border-radius: 12px;
  font-size: 16px;
  font-family: inherit;
  background: #ffffff;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.contact-form input:focus,
.contact-form select:focus,
.contact-form textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(var(--color-primary-rgb), 0.15);
}

.contact-form textarea {
  min-height: 120px;
  resize: vertical;
}

.contact-form button[type="submit"] {
  padding: 18px 32px;
  background: var(--color-primary);
  color: #ffffff;
  border: none;
  border-radius: 999px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  margin-top: 8px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.contact-form button[type="submit"]:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.contact-sidebar {
  padding: 32px;
  background: var(--color-background);
  border-radius: 16px;
}

.contact-sidebar h3 {
  font-family: var(--font-heading);
  font-size: 22px;
  margin: 0 0 24px 0;
  color: var(--color-dark-primary);
}

.contact-sidebar dl {
  margin: 0;
}

.contact-sidebar dt {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #777;
  margin-top: 20px;
}

.contact-sidebar dt:first-child { margin-top: 0; }

.contact-sidebar dd {
  margin: 6px 0 0 0;
  font-size: 16px;
  color: var(--color-dark-primary);
  font-weight: 500;
}

.contact-sidebar dd a { color: var(--color-primary); text-decoration: none; }

@media (max-width: 899px) {
  .contact-container {
    grid-template-columns: 1fr;
    padding: 32px 24px;
    gap: 32px;
  }
  .contact-form-wrap h2 { font-size: 28px; }
}
```

---

## 11. Footer

### HTML

```html
<footer class="footer">
  <div class="footer-container">
    <div class="footer-brand">
      <img src="assets/logo-footer.png" alt="[Business Name]" class="footer-logo">
      <p class="footer-tagline">Residential, commercial, and industrial electrical service in Dunnellon, Ocala, and Marion County.</p>
      <a href="tel:[phone]" class="footer-phone">[phone formatted]</a>
    </div>
    <div class="footer-col">
      <h4>Services</h4>
      <ul>
        <li><a href="/services.html">Residential</a></li>
        <li><a href="/services.html">Commercial</a></li>
        <li><a href="/services.html">Industrial</a></li>
        <li><a href="/services.html">Generators</a></li>
        <li><a href="/services.html">Surge Protection</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Service Areas</h4>
      <ul>
        <li>Dunnellon</li>
        <li>Ocala</li>
        <li>Belleview</li>
        <li>The Villages</li>
        <li>Silver Springs</li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Contact</h4>
      <ul>
        <li><a href="tel:[phone]">[phone formatted]</a></li>
        <li><a href="mailto:[email]">[email]</a></li>
        <li>[address]</li>
        <li>Mon-Fri 8am-5pm</li>
        <li>24/7 Emergency</li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <div>© [year] [Business Name]. [License info].</div>
    <div class="footer-attribution">Photos provided by Google. Contributors: [names].</div>
  </div>
</footer>
```

### CSS

```css
.footer {
  background: #0a0a0a;
  color: #ffffff;
  padding: 80px 24px 40px;
}

.footer-container {
  max-width: 1280px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 48px;
  padding-bottom: 48px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.12);
}

/* Logo renders in native brand colors on the dark footer.
   Previous filter: brightness(0) invert(1) flattened multi-color
   logos to white silhouettes. Grandview F4 2026-04-16 caught this
   — multi-color logos (gold wordmark + green palm + banner) became
   an empty white rectangle. If a prospect's source logo is pure
   monochrome and needs inversion for dark-footer contrast, handle
   per-site in Phase 5 as an exception, not as a template default. */
.footer-logo {
  height: 48px;
  margin-bottom: 20px;
}

.footer-tagline {
  font-size: 14px;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.7);
  margin: 0 0 20px 0;
  max-width: 340px;
}

.footer-phone {
  color: #ffffff;
  font-size: 20px;
  font-weight: 700;
  text-decoration: none;
}

.footer-col h4 {
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  color: #ffffff;
  margin: 0 0 20px 0;
}

.footer-col ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.footer-col a, .footer-col li {
  color: rgba(255, 255, 255, 0.65);
  text-decoration: none;
  font-size: 14px;
  transition: color 0.2s ease;
}

.footer-col a:hover { color: #ffffff; }

.footer-bottom {
  max-width: 1280px;
  margin: 0 auto;
  padding-top: 32px;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
}

@media (max-width: 899px) {
  .footer-container {
    grid-template-columns: 1fr 1fr;
    gap: 32px;
  }
  .footer-brand {
    grid-column: span 2;
  }
}
```

### Rules

- Footer is ALWAYS dark (#0a0a0a). This is separate from the mandatory stats section dark rule — the footer dark is structural, not rhythmic, and Phase 6 check 10 (dark section count) EXCLUDES the footer from the count.
- Photo attribution is mandatory when Google Places or Unsplash or Pexels photos are used (enforced by Phase 6 check 12)
- No "Site designed by" or any GRM attribution
- No "Built with Claude" or AI disclosure
- Real copyright year
- Real license info next to copyright

---

## 12. Mobile Bottom CTA Bar

Sticky at bottom of mobile viewport. Always visible while scrolling.

### HTML

```html
<div class="mobile-cta-bar">
  <a href="tel:[phone]" class="mobile-cta-primary">Call Now</a>
  <a href="#contact" class="mobile-cta-secondary">Get a Quote</a>
</div>
```

### CSS

```css
.mobile-cta-bar {
  display: none;
}

@media (max-width: 899px) {
  .mobile-cta-bar {
    display: flex;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 99;
    background: #ffffff;
    padding: 12px 16px;
    padding-bottom: calc(12px + env(safe-area-inset-bottom));
    gap: 10px;
    box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.1);
  }

  .mobile-cta-primary,
  .mobile-cta-secondary {
    flex: 1;
    text-align: center;
    padding: 14px 16px;
    border-radius: 999px;
    text-decoration: none;
    font-weight: 700;
    font-size: 15px;
  }

  .mobile-cta-primary {
    background: var(--color-primary);
    color: #ffffff;
  }

  .mobile-cta-secondary {
    background: transparent;
    color: var(--color-dark-primary);
    border: 1.5px solid var(--color-dark-primary);
  }

  /* Add bottom padding to body to prevent content cutoff */
  body { padding-bottom: 80px; }
}
```

### Rules

- Mobile only (hidden on desktop)
- Call Now is always primary (linked via tel:)
- iOS safe area padding for home indicator
- Body needs bottom padding on mobile to prevent content cutoff
- The bar renders exactly the two buttons defined in the HTML above. No trailing captions, no `<small>` tags, no "Or..." copy. See `anti-slop-rules.md` > CTA trailing-fragment hallucination.

---

## Loading order reminder

When Phase 5 generates the homepage, build sections in the order listed at the top of this file. For each section, the HTML structure, CSS, and content rules live in the section above. Hero comes from `hero-patterns.md`. Content values come from `profile-draft.json`. Typography tokens, color variables, and animation primitives come from `css-framework.md`. Voice templates and section-specific voice assignments (Closing Table / Saturday Morning / Front Porch) come from `content-rules.md`. Schema injection happens in Phase 5.5 after all HTML is generated.

If a section is optional (trust marquee, promo bar, before/after gallery, featured promotion callout), check the Phase 2 and Phase 3 data for the trigger conditions before rendering. Never render an empty or placeholder section.

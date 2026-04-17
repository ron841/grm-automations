# T&F Electric v07 — Flagship 1 Audit

**Date:** 2026-04-13
**URL:** https://tandf-electric-v07.vercel.app
**Aliases:** tandf-electric-v07.vercel.app, tandf-electric-v07-ron-7323s-projects.vercel.app
**Status:** Pre-edit baseline capture
**Auditor:** Claude (automated + manual review)

---

## Capture Inventory

| Category | Files | Notes |
|----------|-------|-------|
| Desktop full-page (1440w) | 6 pages | `desktop/*.png` |
| Mobile full-page (390w) | 6 pages | `mobile/*.png` |
| Hero above-fold (1440 + 390) | 12 shots | `hero/*.png` |
| Nav/logo close-up (1440 + 390) | 12 shots | `nav-logo/*.png` — text-based logo, no `<img>` |
| Footer close-up (1440 + 390) | 12 shots | `footer/*.png` |
| CSS background-image sections | 36 shots | `bg-images/*.png` (12 on index, 3 on services, 1 each on other pages, desktop+mobile) |
| OG image | 1 file | `og/og-image.png` — sourced from `gp-01.jpg` (Google Photos) |
| Site-review v1.1 output | JSON + MD + mobile screenshot | `site-review/` |

**Total captures: ~79 files**

---

## Site-Review v1.1 Results

| Check | Status | Severity | Detail |
|-------|--------|----------|--------|
| logo-is-image | PASS | soft | Tier-2 fallback: og:image present (gp-01.jpg) |
| og-image-brand-color | SKIP | hard | No --brand-primary provided |
| featured-service-image-rotation | **FAIL** | hard | `gp-09.jpg` appears on both homepage and services page |
| wow-gap-structural | PASS | hard | All 5 structural elements present (hero H1, stats, testimonials, services grid, CTA) |
| mobile-render-baseline | PASS | soft | 375x812 screenshot rendered, 322 KB |

**Summary: 3 pass / 1 fail / 0 warn / 1 skip**

---

## Self-Check: "Would I text this URL to a prospect tomorrow?"

**Verdict: Not yet. Close, but 3-4 things would make me hesitate.**

### BLOCKERS (fix before showing to anyone)

**B1. OG image missing on 4 of 6 pages**
- `services.html`, `about.html`, `testimonials.html`, `contact.html` have no `og:image` tag.
- Only `index.html` has an og:image. When subpages are shared on Facebook, LinkedIn, or iMessage, they render as bare text links with no preview image.

**B2. Twitter card tags missing on 5 of 6 pages**
- Only `index.html` has `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`.
- All other pages produce no rich card when shared on X/Twitter.

**B3. OG image is a raw Google Photo — not a branded composite**
- The og:image on index.html points to `assets/photos/google/gp-01.jpg` — an unbranded jobsite photo. A proper Flagship 1 should have a composited OG card with logo, tagline, and brand colors overlaid. This is the image that shows up when someone shares the link.

**B4. Featured service card image duplication (site-review FAIL)**
- `gp-09.jpg` is used as the featured service card image on BOTH the homepage and `services.html`. The site-review v1.1 scan flagged this as a hard fail. Featured images should not repeat across pages.

**B5. Logo is text-only — no `<img>` tag in header/nav**
- The header renders "T&F Electric" as styled text with `<span>` elements. There is no logo image file. The site-review passed this on a Tier-2 fallback (og:image exists), but for a flagship site we should have a proper logo mark. This affects brand perception and is the first thing a prospect sees.

### WARNINGS (should fix before launch, not emergency)

**W1. Form `replyTo` value is `@`**
- Both `index.html` (line 405) and `contact.html` (line 65) have `<input type="hidden" name="replyTo" value="@">`. StaticForms may treat this as "use submitter email" but it's ambiguous and could cause delivery issues.

**W2. No social media links anywhere on the site**
- Footer has brand, services, service area, and contact columns but zero social links. No Facebook, Google Business Profile, or Yelp link.

**W3. Testimonials have no dates**
- All 15 reviews on the testimonials page and 6 on the homepage show name and city but no date. Google reviews have dates — omitting them makes the reviews look less authentic.

**W4. All displayed testimonials are 5-star, but aggregate rating is 4.6**
- Every testimonial card shows 5 stars. The stated average is 4.6 from 41 reviews. Showing only perfect reviews when the average is lower feels cherry-picked.

**W5. `thanks.html` is missing skip-link and has no meta description or OG tags**
- While noindexed, it's an accessibility gap and produces a bare link if shared.

**W6. Service card background images lack accessibility attributes**
- Featured service cards on index.html and services.html use `background-image` CSS but have no `role="img"` or `aria-label`. Screen readers skip these entirely.

**W7. CTA inconsistency**
- Homepage featured card "Get a quote" links to `#contact` (in-page anchor). Services page featured card links to `contact.html` (separate page). Inconsistent UX.

**W8. Testimonials page has no section heading above the grid**
- Goes straight from hero to grid with no `<h2>`. Compare to homepage where the same section has "What Marion County says about T&F" as H2.

**W9. Footer uses `<h4>` tags for column headers**
- "Services", "Service Area", "Contact" are `<h4>` elements inside `<footer>`. SEO best practice is to use styled `<span>` or `<strong>` instead of heading tags in footer.

### NOTES (good to know, not urgent)

**N1. Copy quality is strong** — no AI red flags detected. Specific local details (Big Tree Road, Rainbow Springs, Generac, "phone number on the truck hasn't changed since 1976") read authentically.

**N2. No placeholder content** — zero instances of lorem ipsum, TODO, "coming soon", or template text.

**N3. Data consistency is excellent** — phone (352-465-4600), address (1737 SW Big Tree Rd), license (EC13007855), email (tandfelectric@gmail.com) all consistent across every page.

**N4. Contact form is complete** — name (required), phone (required), email (optional), service dropdown (11 options), message, honeypot spam trap, proper autocomplete attributes. Action URL set to StaticForms, redirect to thanks.html.

**N5. Schema markup is thorough** — Electrician org schema, FAQPage on index + services, BreadcrumbList on subpages, individual Review schema on testimonials.

**N6. Favicon exists** at `assets/favicon.ico`.

**N7. `robots.txt` and `sitemap.xml` both present** and correct.

**N8. `prefers-reduced-motion` fully respected** — CSS disables animations, JS skips slideshow and ticker.

**N9. Canonical URLs set on all indexable pages** (pointing to Vercel preview URLs — will need updating if custom domain is assigned).

**N10. Deployment protection is ON for hash URLs** — only the clean alias (tandf-electric-v07.vercel.app) is publicly accessible. The long deployment URLs redirect to Vercel login.

---

## Architecture Summary

| Aspect | Detail |
|--------|--------|
| Framework | Static HTML (no build tool) |
| Pages | 6: index, services, about, testimonials, contact, thanks |
| CSS | Single `style.css` |
| JS | Single `script.js` |
| Forms | StaticForms (hosted form backend) |
| Images | Google Business Profile photos (`assets/photos/google/gp-*.jpg`) |
| Hosting | Vercel (static deployment) |

---

## Recommended Fix Priority

| Priority | Item | Effort |
|----------|------|--------|
| 1 | Add og:image + twitter:card tags to all subpages | 15 min |
| 2 | Create branded OG composite image | 30 min (design) |
| 3 | Swap out `gp-09.jpg` on one page to fix image duplication | 5 min |
| 4 | Add real logo image to header | Needs logo file from prospect/Em |
| 5 | Add dates to testimonial cards | 15 min |
| 6 | Add social links to footer | 10 min (need URLs) |
| 7 | Fix `replyTo` value in forms | 2 min |
| 8 | Accessibility: add role/aria-label to bg-image cards, skip-link to thanks | 10 min |

---

*Report generated 2026-04-13. Captures stored in this directory. Do not edit captures — they are the pre-edit baseline.*

# The Storefront — Landing Page Brief
### For handoff to developer (or a new chat window)

---

## What this is

A landing page for **The Storefront** — Get Rooted Media's web-services offering for Marion County, Florida contractors (plumbers, HVAC, electricians, roofers, etc.).

**Target URL:** `getrootedmedia.com/web`
**Product pitch:** $800 to build, $150/month to maintain. Live in 14 days. Built to be recommended by AI assistants (ChatGPT, Claude, Perplexity) for local-service queries.
**Built by:** Get Rooted Media (Ron Kolb + Cameron), Ocala, FL.

---

## What's in this folder

| File | Purpose |
|---|---|
| `Landing.html` | The page itself — all markup + copy, ready to view in a browser. |
| `landing.css` | Page-specific styles. Imports tokens from `../colors_and_type.css`. |
| `HANDOFF.md` | Full developer brief — SEO schema, robots.txt checklist, analytics hooks, accessibility notes, implementation paths. |
| `BRIEF.md` | This file. |

The parent project folder also contains:
- `colors_and_type.css` — the shared GRM design-system tokens (brand colors, font stack, CSS variables). Already imported.
- `logos/` — the brand logo SVGs (including `Logo_Get Rooted Media-REV.svg` used in the header and footer).
- `components/layout/Nav.tsx` and `Footer.tsx` — the real Next.js site's header/footer. The landing page matches these 1:1 in structure.

---

## The argument the page makes (for copy context)

The page is structured as a slow-build argument for skeptical contractors who think their existing website is "fine":

1. **Hero (cream)** — A Belleview homeowner with a burst pipe at 9 PM doesn't scroll through Google ads. They ask ChatGPT. Almost zero chance it recommends your plumbing shop. Three data points follow: 527% YoY growth in AI-referred visits · 1.2% of home-services locations currently recommended by ChatGPT · 17% of AI-cited URLs also rank Page 1 on Google (your SEO agency isn't protecting you from this).

2. **The Shift (black)** — What changed. Search is a conversation now, not a list of blue links. Homeowners ask a question and get one answer back.

3. **The Diagnosis (cream)** — Why your current site gets skipped: no schema markup, stale content, generic copy, no FAQ pages, no authoritative signals.

4. **The Thirty-Second Test (teal)** — The decision moment. "Pull out your phone. Ask ChatGPT: 'Best [your trade] in Ocala.' If your name isn't the one it hands back, we should talk." CTAs: free preview OR call.

5. **What We Ship (cream)** — The concrete deliverables of The Storefront: FAQPage schema, LocalBusiness schema, fact-dense copy, local NAP consistency, quarterly content refresh, AI citation monitoring.

6. **Pricing (black)** — $800 setup. $150/month. What each tier includes.

7. **The Preview + Intake Form (teal)** — "We build a free preview of your homepage in 7 days. If you like it, we migrate to your domain. If you don't, nothing changes." Three-field intake form (name, trade, ZIP).

8. **Sign-off (cream)** — "We built Get Rooted Media out of Ocala because Marion County is full of good contractors whose phones ought to ring more than they do." Dual CTA: call us (352) 598-7289 OR book a 15-min call on Cal.com.

9. **Sources strip (cream, thin)** — Citations for the stats used above.

10. **Footer (black)** — Matches the site-wide `Footer.tsx` exactly.

---

## Design system — already in use

**Colors** (from `colors_and_type.css`):
- `--grm-cream` #FAF8F4 — page background, light sections
- `--grm-black` #1A1A1A — dark sections, primary text
- `--grm-teal`  #52B5CB — accents, CTAs, pull quotes
- `--grm-white` #FFFFFF

**Fonts** (Google Fonts, already loaded):
- **Merriweather** — display headlines (italic-capable serif)
- **Nunito** — body text (humanist sans)
- **Comfortaa** — uppercase eyebrows (wide, distinctive)
- **Grand Hotel** — the "The" script flourish (used in masthead, publication names)

**Section rhythm** (intentional — don't flatten):
cream → black → cream → teal → black → cream → teal → cream → black footer

---

## What's already wired

- ✅ Cal.com booking URL `https://cal.com/ron-kolb-cdlgsw/30min` (3 places)
- ✅ Phone `tel:3525987289` (3 places)
- ✅ Email `mailto:ron@getrootedmedia.com` (footer)
- ✅ Canonical URL `https://getrootedmedia.com/web`
- ✅ Real GRM logo (reversed white SVG) in header and footer
- ✅ Header matches site-wide `Nav.tsx` (dark bg, white logo, 4 nav links, pill teal CTA)
- ✅ Footer matches site-wide `Footer.tsx` (4 columns: Brand · Publications · Connect · CTA)
- ✅ Honeypot field on intake form (`name="company"` — reject if filled)
- ✅ `data-cta` analytics hooks on every CTA (`header-book`, `test-preview`, `footer-phone`, `footer-book`)
- ✅ `data-form="preview-intake"` on the intake form
- ✅ Semantic landmarks, form labels, accessible hidden honeypot
- ✅ Responsive breakpoints at 900 / 720 / 600 / 480px

---

## What the developer still needs to do

1. **Decide implementation path:**
   - **A — Port to Tailwind (recommended):** Rebuild as Next.js components under `components/sections/storefront/`. Use the HTML/CSS as pixel reference. Reuse existing tokens (`bg-grm-cream`, `bg-grm-black`, `text-grm-teal`, `font-merriweather`, `font-comfortaa`, `font-nunito`).
   - **B — Drop in as-is:** Use the HTML/CSS directly as a static page. Faster, but styling won't share hover/focus conventions with the rest of the site.

2. **Remove local header + footer** if embedding in the existing site shell — rely on global `<Nav />` and `<Footer />`. Keep the thin `<section class="sources-strip">` just above the global footer.

3. **Wire the intake form.** Change `<form action="#">` to post to HubSpot / Formspree / a Next API route. Honeypot is `name="company"` — reject submissions where it's filled.

4. **Add SEO meta + JSON-LD schema.** Full block is in `HANDOFF.md` § 3 — includes OG tags, Twitter card, `Service` schema, `LocalBusiness` schema, `FAQPage` schema, `Offer` pricing.

5. **Verify `robots.txt`** allows AI crawlers: GPTBot, ClaudeBot, Claude-SearchBot, PerplexityBot, Bingbot, Googlebot. The whole premise of this page breaks if they're blocked.

6. **Hook analytics.** Every CTA has a `data-cta` attribute. Fire GA4 events on click + form submit.

---

## Performance + accessibility targets

- **No JavaScript required.** Zero runtime dependencies.
- **Lighthouse target:** 95+ across Performance, Accessibility, Best Practices, SEO.
- **WCAG AA contrast** throughout. Teal-on-white and white-on-teal both verified.

---

## Contact

**Ron Kolb** — Get Rooted Media · ron@getrootedmedia.com · (352) 598-7289
**Site:** getrootedmedia.com · **This page lives at:** /web

---

## Notes for a fresh chat context

If you're picking this up in a new chat window, open `Landing.html` in a browser to see the page. Read `HANDOFF.md` for the full technical brief. The page is production-ready copy-wise; what remains is the dev work listed above.

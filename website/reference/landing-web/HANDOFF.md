# The Storefront — Landing Page (/web)
## Developer handoff

Target URL: **getrootedmedia.com/web**
Product: **The Storefront** — GRM's web services offering for Marion County contractors.

---

## Context for the dev

Your existing site (`grm-automations/website`, Next.js + Tailwind + custom tokens) already has a short Storefront teaser section at `components/sections/WebServices.tsx`. This landing page **replaces** the teaser with a full scrolling page. You have two implementation paths — either works:

**Path A — Port to Tailwind (recommended, matches the rest of the site):**
- Use `Landing.html` + `landing.css` as the canonical pixel reference
- Rebuild each section as a Next.js component under `components/sections/storefront/`
- Reuse existing tokens: `bg-grm-cream`, `bg-grm-black`, `text-grm-teal`, `font-merriweather`, `font-comfortaa`, `font-nunito`. They're already defined in the Tailwind config.
- Fonts already load from `app/layout.tsx`; do not re-import.

**Path B — Drop the HTML/CSS in as-is:**
- Place as a static page or route segment. Adjust the stylesheet import path.
- Faster, but the styling will not share hover/focus conventions with the rest of the site.

---

## 1. Files

- `Landing.html` — single self-contained page. All copy, markup, semantic structure.
- `landing.css` — page-specific stylesheet. Imports tokens from `../colors_and_type.css`.
- `../colors_and_type.css` — same tokens your Tailwind config is built from.

---

## 2. What to swap before launch

Search `Landing.html` for `DEV:` — every spot that needs your attention is commented.

| Location | Status |
|---|---|
| Book-call CTAs | ✅ Already wired to `https://cal.com/ron-kolb-cdlgsw/30min` (3 places) |
| Phone | ✅ Wired to `tel:3525987289` (3 places) |
| `<form action="#">` in the preview intake | ⬜ Point to your form handler (HubSpot form submit endpoint, Formspree, or a Next API route). Honeypot field is `name="company"` — reject submissions where it's filled. |
| Header | ⬜ If page lives inside the existing site shell, **remove** `<header class="site-header">` entirely and rely on the global Nav. |
| Footer | ⬜ Same — if using the global `<Footer />`, remove `<footer class="site-footer">`. But keep the Research + Sources block (move it above the global footer). |

---

## 3. SEO (the whole point of this page)

This page exists to rank for AI-search queries and convert. It has to practice what it preaches.

Add to `<head>`:

```html
<link rel="canonical" href="https://getrootedmedia.com/web">   ✅ already added
<meta property="og:title" content="The Storefront — Websites built to be recommended by AI">
<meta property="og:description" content="For Marion County contractors. $800 to build, $150 a month. Live in 14 days.">
<meta property="og:url" content="https://getrootedmedia.com/web">
<meta property="og:image" content="https://getrootedmedia.com/og/storefront.png">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
```

**Schema.org JSON-LD** (add inside `<head>`):

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Service",
      "@id": "https://getrootedmedia.com/web#service",
      "name": "The Storefront",
      "provider": {
        "@type": "LocalBusiness",
        "name": "Get Rooted Media LLC",
        "telephone": "+1-352-598-7289",
        "email": "ron@getrootedmedia.com",
        "address": {
          "@type": "PostalAddress",
          "addressLocality": "Ocala",
          "addressRegion": "FL",
          "addressCountry": "US"
        },
        "areaServed": "Marion County, FL"
      },
      "serviceType": "Website design and development for home-services contractors",
      "offers": [
        {"@type": "Offer", "name": "Setup", "price": "800", "priceCurrency": "USD"},
        {"@type": "Offer", "name": "Monthly", "price": "150", "priceCurrency": "USD", "priceSpecification": {"@type":"UnitPriceSpecification","billingIncrement":1,"unitText":"MONTH"}}
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "What is The Storefront?",
          "acceptedAnswer": {"@type": "Answer", "text": "A website built for Marion County contractors that is specifically optimized to be recommended by AI assistants like ChatGPT. Includes schema markup, fact-dense copy, and quarterly content refresh."}
        },
        {
          "@type": "Question",
          "name": "What does The Storefront cost?",
          "acceptedAnswer": {"@type": "Answer", "text": "$800 one-time setup fee, then $150 per month for hosting, updates, AI citation monitoring, and quarterly refresh."}
        },
        {
          "@type": "Question",
          "name": "How long does it take to build?",
          "acceptedAnswer": {"@type": "Answer", "text": "Your Storefront is live within 14 days of signing and receipt of the setup fee."}
        },
        {
          "@type": "Question",
          "name": "Do I get to see it before I sign?",
          "acceptedAnswer": {"@type": "Answer", "text": "Yes. We build a free preview of your homepage within 7 days. If you like it, we migrate. If you do not, nothing changes."}
        }
      ]
    }
  ]
}
</script>
```

**`robots.txt` verification** — `getrootedmedia.com/robots.txt` must allow:
- `User-agent: GPTBot` → Allow: /
- `User-agent: ClaudeBot` → Allow: /
- `User-agent: Claude-SearchBot` → Allow: /
- `User-agent: PerplexityBot` → Allow: /
- `User-agent: Bingbot` → Allow: /
- `User-agent: Googlebot` → Allow: /

If WordPress or a security plugin is currently 403'ing these, fix before launch. The whole premise of the page breaks otherwise.

---

## 4. Analytics

Every CTA has a `data-cta="..."` hook. Wire to your analytics layer (GA4 event, plausible, whatever you use):

| `data-cta` | Where |
|---|---|
| `header-book` | Top-right "Book a 15-min call" |
| `test-preview` | Teal "Thirty-second test" CTA — anchors to preview form |
| `footer-phone` | Bottom-left "Call Ron" tile |
| `footer-book` | Bottom-right "Book online" tile |

Intake form has `data-form="preview-intake"` — fire submit event on success, track referrer.

---

## 5. Design system

**Fonts** (loaded via `colors_and_type.css` and already in your Tailwind config):
- `Merriweather` — display / editorial headlines
- `Nunito` — body
- `Comfortaa` — uppercase eyebrows
- `Grand Hotel` — the "The" script flourish

**Colors**:
- `--grm-cream` #FAF8F4 — page bg, light bands
- `--grm-black` #1A1A1A — dark bands, primary text
- `--grm-teal`  #52B5CB — accents, CTAs, pull quotes
- `--grm-white` #FFFFFF

**Section rhythm** (cream → black → cream → teal → black — all intentional):
1. Hero (cream)
2. The shift (black)
3. The diagnosis (cream)
4. Thirty-second test (teal)
5. What we ship (cream)
6. Pricing (black)
7. The preview + intake form (teal)
8. Sign-off + dual CTA (cream)
9. Footer — sources + legal (black)

**Spacing**: section padding `96px 0` desktop / `64px 0` mobile. Container `max-width: 1160px`, `padding: 0 40px` / `0 24px`.

**Breakpoints**: `900px`, `720px`, `600px`, `480px`.

---

## 6. Accessibility

Already handled:
- Semantic landmarks (`<header>`, `<section>`, `<footer>`)
- All inputs have `<label>`s
- Honeypot is `aria-hidden="true"` and offscreen
- Color contrast: teal-on-white passes WCAG AA; white-on-teal passes AA; all body text passes AAA
- Phone and email links use `tel:` / `mailto:`

Verify after implementation:
- [ ] Focus states visible on all CTAs and form fields
- [ ] Form errors are announced
- [ ] Heading order: H1 = masthead "The Storefront.", H2s open each section

---

## 7. Performance targets

- No JavaScript required. Zero runtime deps.
- Fonts from Google Fonts (single request, cached by the site already).
- No images in the design — if a portrait of Ron lands later, serve AVIF with WebP fallback, `loading="lazy"`.

**Target: Lighthouse 95+ across Performance, Accessibility, Best Practices, SEO.**

---

## 8. Copy ownership

All copy is in `Landing.html` as plain text, editable without redeploy. The only inline tags inside copy are `<em>`, `<br>`, and `<span class="teal">`.

If Ron changes pricing or phone number, those appear in these spots:
- Pricing section: `$800` and `$150`
- Phone: three places (header, thirty-second-test meta, footer dual CTA)
- Email: two places (footer contact, this handoff doc)

---

## Questions

Ron: (352) 598-7289 · ron@getrootedmedia.com
Design reference: the full argument is preserved from `/field-brief/` in this project — that was the source sales sheet. This page is the web version for `/web`.

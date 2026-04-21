# SEO and GEO Reference

Part of the prospect-site skill v0.7. Loaded by Phase 5 during HTML generation and Phase 5.5 during structured data injection. Referenced by Phase 6 for verification.

This file owns every decision about how a generated contractor site becomes visible and citable in the AI-era search landscape. Schema.org structured data templates, semantic HTML discipline, BLUF content structure, robots.txt crawler access, sitemap generation, llms.txt inclusion, platform-specific optimization notes, and the Phase 5 and Phase 6 integration points.

The scope is specifically GEO (Generative Engine Optimization) first, traditional SEO second. Traditional SEO techniques (title tags, meta descriptions, sitemap submission) remain table stakes and are covered here, but the emphasis throughout is on making every generated site machine-readable and citation-ready for ChatGPT, Claude, Perplexity, Copilot, and Gemini. This is the competitive differentiator for GRM Web Services in the AI-era SMB market.

---

## The AI citation landscape

Search is bifurcating. Traditional Google organic results still drive the majority of discovery traffic to SMB websites, but AI-powered search is compounding rapidly. Industry research from early 2026 documents a 527 percent year-over-year growth in AI-referred sessions to business websites. Yet among home service businesses, only 1.2 percent of locations are recommended when users ask ChatGPT for local contractors. The gap between the opportunity and the current reality is the exact window GRM Web Services is built to close.

### Traditional SEO and AI citation are diverging

A critical finding from 2025-2026 industry analysis: only 17 percent of URLs cited by AI assistants overlap with Page 1 organic search results in traditional Google ranking. The two systems evaluate content differently. Traditional SEO rewards backlink authority, keyword alignment, and domain age. AI citation rewards content density, factual specificity, structural clarity, and machine-readable markup. A contractor site with strong schema, fact-dense first paragraphs, and clean semantic HTML can earn AI citations even without competitive backlink profiles or domain authority.

### The strategic thesis of GRM Web Services

The 17 percent overlap finding is not just a statistic. It is the entire commercial thesis of GRM Web Services, and every design decision in this skill traces back to it. Read this section carefully. It is the sales story GRM will tell for the next five years.

**The old game that GRM cannot win.** Traditional SEO for local contractors is a slow compounding game. A plumber who set up a WordPress site in 2015 and earned 200 backlinks from HomeAdvisor, Angi, Yelp, BBB, a few local chambers of commerce, and a few newspaper mentions has a moat. That moat took ten years to build. A new contractor agency trying to outrank that plumber on Google organic would need to build a comparable backlink profile from scratch, wait for Google to age the new domain, and hope the incumbent does not notice and respond. Under the old game, a year-one Marion County web agency cannot reasonably compete with an entrenched incumbent on traditional search rankings. The math does not work.

**The new game that GRM can win on day one.** Under the AI citation playbook, domain age does not matter. Backlink count does not matter. Google ranking position does not matter. What matters is: Schema.org markup completeness, fact density in the first 300 words of every page, FAQPage schema with specific local answers, semantic HTML discipline, and explicit AI crawler access. These are all technical implementation decisions that a well-built new site ships with on day one. A three-day-old contractor site built to GRM's v0.7 spec can outperform a ten-year-old incumbent site in AI citations starting the moment the crawlers index it. The incumbent's ten-year moat is worth nothing in this game. The incumbent's backlinks are worth nothing. The incumbent's domain age is worth nothing. The incumbent has no moat, because the incumbent is playing a different game and does not know it.

**The Marion County reality.** Of the contractor sites GRM has surveyed in Marion County so far (the batch list of 28 manually selected prospects plus the larger batch of 61 home services businesses), the overwhelming majority have: no Schema.org markup of any kind, no FAQPage schema, no semantic HTML beyond what WordPress themes produce by default, marketing filler in their first paragraphs instead of fact-dense content, WordPress security plugins that may be blocking AI crawlers, and no Bing Places for Business claim. Every single one of these is a gap GRM closes on day one of the client relationship. Every single one is a citation leak the incumbent does not even know they have.

**What this means for the sales conversation.** GRM is not pitching "a better website" to Marion County contractors. Better websites are a commodity and Wix can make one for $10 a month. GRM is pitching the only website in the contractor's entire competitor set that is engineered for the search landscape homeowners will actually use in 2026 and 2027. The pitch writes itself: "Your current site ranks fine on Google and gets you a few leads a month. That is fine. But when someone asks ChatGPT or Claude or Perplexity or Copilot for a plumber in Ocala, your site is invisible. Your biggest competitor is also invisible. The first contractor in Marion County to show up in AI search owns that query forever. We build that site for you."

**What this means for the skill.** Every technical decision in this file is in service of this thesis. The schema section is comprehensive because schema is the single highest-leverage AI citation factor. The BLUF section is strict because the first 300 words drive 44.2 percent of all citations. The robots.txt section is explicit about every AI crawler because blocking any one of them is a self-inflicted wound. The internal linking section exists because AI crawlers use links to build entity understanding. Every hard rule and every Phase 6 check is a tax the skill pays in exchange for preserving GRM's competitive moat. The moat is technical execution. The skill is the mechanism that makes technical execution repeatable at scale.

### The three findings that shape this file

Three specific research findings anchor every decision in this file:

1. **Schema.org structured data delivers approximately 36 percent improvement in AI citation rates.** This is the single highest-leverage technical optimization. FAQPage schema in particular is the strongest individual predictor of AI visibility across all schema types.

2. **The first 30 percent of a page generates 44.2 percent of all AI citations from that page.** AI systems read pages top-down and cite disproportionately from the opening. Every contractor page must lead with fact-dense answer-first content. The hero section and the first 300 words on any page are where the citation leverage concentrates.

3. **50 percent of content cited by AI assistants was published or updated within the previous 13 weeks.** Freshness is treated as a credibility signal. This is addressed primarily in `deployment.md` under the ongoing content refresh protocol, but seo-geo.md enforces the initial state (`<lastmod>` tags in the sitemap, `dateModified` in schema, timestamp on key pages).

### What this file does NOT try to do

- **Link building and domain authority work.** These are traditional SEO concerns and are out of scope for the generator skill. Ongoing backlink work is a client services offering documented in `deployment.md`.
- **Keyword research and content marketing strategy.** GRM may offer this as a paid add-on, but the v0.7 skill focuses on the markup and structural baseline, not on content strategy.
- **Paid search and advertising.** Handled separately in GRM's social and paid offerings.
- **Full site audits and technical SEO troubleshooting.** Those are manual consulting engagements.

The v0.7 skill's job is to produce sites that start from a structurally strong AI-citation position on the day they ship. Ongoing optimization is a client relationship, not a generator task.

---

## The 80/20 of AI citation for contractor sites

Ordered by impact-to-effort ratio based on current industry research. Phase 5 implements all of these by default on every generated site.

### 1. Comprehensive JSON-LD structured data with LocalBusiness and FAQPage

**Impact:** approximately 36 percent improvement in AI citation rates for sites with comprehensive schema. FAQPage is the single strongest predictor.
**Effort:** zero per-site effort. Phase 5 auto-generates all schema from `profile.json` captured data.
**Implementation section:** Schema.org implementation, below.

### 2. BLUF content structure on every page

**Impact:** the first 30 percent of every page drives 44 percent of citations. Structuring content to lead with facts is as important as the facts themselves.
**Effort:** zero per-site effort. Content rules in `content-rules.md` already enforce BLUF through the Closing Table voice and headline pattern rules. This file adds additional per-page BLUF enforcement.
**Implementation section:** BLUF content structure, below.

### 3. AI crawler access explicitly allowed in robots.txt

**Impact:** critical. A site that accidentally blocks GPTBot or PerplexityBot has zero chance of AI citation from those platforms regardless of content quality. Many WordPress sites and Cloudflare-protected sites block unknown bots by default.
**Effort:** zero per-site effort. Phase 5 writes the full allow-list robots.txt on every build.
**Implementation section:** AI crawler access, below.

### 4. Semantic HTML structure

**Impact:** improves AI parsing accuracy at no ongoing cost. LLMs use semantic elements (`<main>`, `<article>`, `<section>`, `<address>`) to build a mental model of page content.
**Effort:** Phase 5 uses semantic HTML throughout because it is already enforced by the section patterns in `section-patterns.md`. This file formalizes the discipline as a rule rather than a reflex.
**Implementation section:** Semantic HTML discipline, below.

### 5. XML sitemap with accurate lastmod dates

**Impact:** freshness signals feed citation weighting. A sitemap with current `<lastmod>` dates tells AI crawlers that content was recently updated and is more likely to be accurate.
**Effort:** Phase 5 auto-generates. Ongoing refresh is documented in `deployment.md`.
**Implementation section:** Sitemap and freshness signals, below.

### 6. Bing Places for Business claiming and optimization

**Impact:** Microsoft Copilot citations are heavily weighted toward Bing's index and Bing Places data. Most contractors have Google Business Profile but skip Bing entirely. This is a structural advantage GRM can deliver as part of onboarding.
**Effort:** this is a post-signing client task, not a generator task. Documented here for visibility and in `deployment.md` as part of the onboarding checklist.

### 7. llms.txt file

**Impact:** honestly limited. Current industry data shows approximately 10 percent adoption across 300,000 domains sampled, and llms.txt accounts for only 0.1 percent of AI crawler requests. The "llms.txt is dead" sentiment in the technical SEO community is increasingly common. But the file takes minutes to generate and does no harm.
**Effort:** Phase 5 auto-generates a minimal llms.txt per build.
**Implementation section:** llms.txt generation, below. Short section because the expected impact is small.

---

## Schema.org implementation (the centerpiece)

Every generated contractor site receives comprehensive JSON-LD structured data injected into the `<head>` of every page by Phase 5.5. Schema is the single highest-leverage technical optimization for AI citation. This section defines exactly which schema types to use, how Phase 5 populates them from `profile.json` captured data, and the validation rules Phase 6 enforces.

### Trade-specific @type mapping

Schema.org provides dedicated types for several contractor trades. Use the most specific type available. Trade-specific types give AI systems precise entity classification, which improves citation confidence.

| Vertical | Schema.org @type | Fallback |
|---|---|---|
| Electrician | `Electrician` | `HomeAndConstructionBusiness` |
| Plumber | `Plumber` | `HomeAndConstructionBusiness` |
| Roofer | `RoofingContractor` | `HomeAndConstructionBusiness` |
| HVAC | `HVACBusiness` | `HomeAndConstructionBusiness` |
| General contractor | `GeneralContractor` | `HomeAndConstructionBusiness` |
| Locksmith | `Locksmith` | `LocalBusiness` |
| Moving | `MovingCompany` | `LocalBusiness` |
| Pest control | `LocalBusiness` with category | `LocalBusiness` |
| Painter | `HomeAndConstructionBusiness` | `LocalBusiness` |
| Pressure washer | `HomeAndConstructionBusiness` | `LocalBusiness` |
| Pool service | `LocalBusiness` with category | `LocalBusiness` |
| Fencing | `HomeAndConstructionBusiness` | `LocalBusiness` |
| Landscaping | `LocalBusiness` with category | `LocalBusiness` |

For verticals without a dedicated type, use `HomeAndConstructionBusiness` or `LocalBusiness` and specify the service category through the `hasOfferCatalog` and `areaServed` fields. Phase 4 reads the vertical from Phase 2 captured data and sets `schema.businessType` in `profile.json`. Phase 5.5 reads this field when generating the JSON-LD block.

### The core LocalBusiness schema template

Every contractor homepage receives this schema injected into the `<head>` as JSON-LD. Every field is populated from captured `profile.json` data. Fields where captured data is missing are omitted rather than fabricated.

```json
{
  "@context": "https://schema.org",
  "@type": "[trade-specific type, e.g., Electrician]",
  "@id": "[canonical site URL]#organization",
  "name": "[business.name from profile.json, verbatim]",
  "description": "[business description, 120-160 characters, fact-dense, generated in Closing Table voice, includes license number and service area]",
  "url": "[canonical site URL]",
  "telephone": "[business.phone formatted as E.164, e.g., +13524654600]",
  "email": "[business.email if captured]",
  "foundingDate": "[business.foundingYear if captured, e.g., 1975]",
  "priceRange": "[business.priceRange if captured or inferred, e.g., $$]",
  "image": "[canonical URL to hero photo, 1200w WebP]",
  "logo": "[canonical URL to logo file]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[business.address.street]",
    "addressLocality": "[business.address.city]",
    "addressRegion": "[business.address.state, two-letter]",
    "postalCode": "[business.address.zip]",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "[business.geo.lat]",
    "longitude": "[business.geo.lng]"
  },
  "areaServed": [
    {
      "@type": "City",
      "name": "[service area city name]",
      "sameAs": "[Wikipedia URL for the city if available]"
    },
    {
      "@type": "County",
      "name": "[county name, e.g., Marion County]",
      "sameAs": "[Wikipedia URL for the county if available]"
    }
  ],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "[real captured rating, e.g., 4.6]",
    "reviewCount": "[real captured review count, e.g., 41]",
    "bestRating": "5",
    "worstRating": "1"
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "[captured hours start, e.g., 08:00]",
      "closes": "[captured hours end, e.g., 17:00]"
    }
  ],
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "[Trade] Services",
    "itemListElement": [
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "name": "[captured service name, verbatim]",
          "description": "[service description from content-rules.md service description templates, Closing Table voice]",
          "areaServed": "[primary service area]",
          "provider": {"@id": "[canonical site URL]#organization"}
        }
      }
    ]
  },
  "sameAs": [
    "[Facebook URL if captured]",
    "[Google Maps place URL from Google Places API]",
    "[Instagram URL if captured]"
  ]
}
```

### Populated example: T&F Electric

This is what Phase 5.5 writes into `index.html` for T&F Electric based on captured profile data. Every field is real and verifiable, no placeholders, no fabrication.

```json
{
  "@context": "https://schema.org",
  "@type": "Electrician",
  "@id": "https://tandf-electric-grm.vercel.app/#organization",
  "name": "T&F Electric",
  "description": "Licensed electrical contractor serving Dunnellon, Ocala, and Marion County since 1975. Residential, commercial, and industrial wiring. Florida license EC13007855.",
  "url": "https://tandf-electric-grm.vercel.app",
  "telephone": "+13524654600",
  "foundingDate": "1975",
  "image": "https://tandf-electric-grm.vercel.app/assets/photos/hero/photo-001-1200w.webp",
  "logo": "https://tandf-electric-grm.vercel.app/assets/logo.png",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[captured street address]",
    "addressLocality": "Dunnellon",
    "addressRegion": "FL",
    "postalCode": "[captured zip]",
    "addressCountry": "US"
  },
  "areaServed": [
    {
      "@type": "City",
      "name": "Dunnellon",
      "sameAs": "https://en.wikipedia.org/wiki/Dunnellon,_Florida"
    },
    {
      "@type": "City",
      "name": "Ocala",
      "sameAs": "https://en.wikipedia.org/wiki/Ocala,_Florida"
    },
    {
      "@type": "City",
      "name": "Belleview",
      "sameAs": "https://en.wikipedia.org/wiki/Belleview,_Florida"
    },
    {
      "@type": "City",
      "name": "The Villages",
      "sameAs": "https://en.wikipedia.org/wiki/The_Villages,_Florida"
    },
    {
      "@type": "City",
      "name": "Silver Springs",
      "sameAs": "https://en.wikipedia.org/wiki/Silver_Springs,_Florida"
    },
    {
      "@type": "County",
      "name": "Marion County",
      "sameAs": "https://en.wikipedia.org/wiki/Marion_County,_Florida"
    }
  ],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.6",
    "reviewCount": "41",
    "bestRating": "5",
    "worstRating": "1"
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "08:00",
      "closes": "17:00"
    }
  ],
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Electrical Services",
    "itemListElement": [
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "name": "Residential Electrical",
          "description": "Licensed residential electrical work for new construction, renovations, and additions across Marion County.",
          "areaServed": "Marion County, FL",
          "provider": {"@id": "https://tandf-electric-grm.vercel.app/#organization"}
        }
      },
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "name": "Whole House Surge Protection",
          "description": "Whole house surge protection to protect televisions, appliances, and electronics from Florida lightning. $450 special installation.",
          "areaServed": "Marion County, FL",
          "provider": {"@id": "https://tandf-electric-grm.vercel.app/#organization"}
        }
      }
    ]
  }
}
```

Notice what is missing: no fabricated email because T&F did not have one captured, no fabricated review counts (41 is the real captured count from Google Places), no made-up service descriptions, and `foundingDate` is the real 1975 not a round number. Schema integrity is non-negotiable.

### FAQPage schema — the strongest single predictor

FAQPage schema is the highest-impact schema type for AI citation. AI assistants love FAQ content because it maps directly to the question-answer format they use to generate responses. Every page with an FAQ section receives FAQPage schema injected alongside the LocalBusiness schema.

Phase 5.5 generates one FAQPage schema block per page with FAQs. The homepage gets one. Each service sub-page that has its own FAQ section gets its own FAQPage schema specific to that service. The main `services.html` page gets its own FAQPage schema with general service questions.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Do you offer 24/7 emergency electrical service?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. T&F Electric provides 24-hour emergency electrical service across Dunnellon, Ocala, and Marion County. Call (352) 465-4600 any time. Overtime charges apply for after-hours calls."
      }
    },
    {
      "@type": "Question",
      "name": "Are you licensed and insured in Florida?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. T&F Electric holds Florida electrical contractor license EC13007855 and carries full general liability insurance. The company has held this license continuously since 1975."
      }
    },
    {
      "@type": "Question",
      "name": "What areas do you serve in Marion County?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "T&F Electric serves Dunnellon, Ocala, Belleview, The Villages, Silver Springs, and Rainbow Lakes Estates. Same-day service is available across all service areas during business hours."
      }
    }
  ]
}
```

**Rules for FAQPage schema:**

- Every answer must contain specific verifiable facts (license numbers, real phone, real service area cities, real pricing when captured)
- Never fabricate prices, timelines, or warranty terms — if Phase 2 did not capture the information, omit that question rather than invent an answer
- Answers should be 2-4 sentences, long enough to be useful but short enough to be cited in full
- Use Closing Table voice (from content-rules.md): direct, mentor-precision, no filler
- Questions should match real homeowner queries in the vertical (see content-rules.md FAQ templates per vertical)
- A page may have 3-7 FAQs. Fewer than 3 defeats the purpose. More than 7 dilutes citation weight per FAQ.

Phase 5 reads the FAQ content from the rendered HTML of the FAQ accordion section. Phase 5.5 mirrors that HTML content into the FAQPage schema block. The two must match exactly — if the HTML shows one answer and the schema shows a different answer, AI systems detect the inconsistency and the page loses citation weight.

### Service schema for service sub-pages

When Phase 5 generates a service sub-page (per the conditional rule in `content-rules.md`), it includes a dedicated `Service` schema block in addition to the parent LocalBusiness schema.

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "@id": "https://tandf-electric-grm.vercel.app/services/whole-house-surge-protection#service",
  "serviceType": "Whole House Surge Protection",
  "name": "Whole House Surge Protection",
  "description": "Whole house surge protection installation for Florida homes. Protects televisions, appliances, HVAC systems, and electronics from lightning strikes and voltage spikes. Installed by licensed electricians across Marion County.",
  "provider": {
    "@id": "https://tandf-electric-grm.vercel.app/#organization"
  },
  "areaServed": [
    {"@type": "City", "name": "Dunnellon"},
    {"@type": "City", "name": "Ocala"},
    {"@type": "City", "name": "Belleview"},
    {"@type": "County", "name": "Marion County"}
  ],
  "offers": {
    "@type": "Offer",
    "price": "450.00",
    "priceCurrency": "USD",
    "priceValidUntil": "[reasonable expiration, e.g., end of current year]",
    "description": "$450 whole house surge protection special, installed"
  }
}
```

**Rules for Service schema:**

- Include `offers` with `price` only if Phase 2 captured real pricing. Never fabricate prices.
- `@id` links to the sub-page URL with `#service` fragment for unique identification
- `provider` links back to the main LocalBusiness using `@id` reference
- `areaServed` mirrors the LocalBusiness area served
- `serviceType` should match common search terms for the service

### BreadcrumbList schema for sub-pages

Service sub-pages and any nested pages receive BreadcrumbList schema to help AI systems understand site hierarchy.

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://tandf-electric-grm.vercel.app/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Services",
      "item": "https://tandf-electric-grm.vercel.app/services.html"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Whole House Surge Protection",
      "item": "https://tandf-electric-grm.vercel.app/services/whole-house-surge-protection.html"
    }
  ]
}
```

Phase 5 generates this automatically for every page that is not the homepage.

### Review schema for testimonials page

The standalone `testimonials.html` page receives individual `Review` schema for each captured testimonial. This is separate from the `AggregateRating` in the main LocalBusiness schema.

```json
{
  "@context": "https://schema.org",
  "@type": "Review",
  "itemReviewed": {
    "@id": "https://tandf-electric-grm.vercel.app/#organization"
  },
  "author": {
    "@type": "Person",
    "name": "Jack C."
  },
  "reviewRating": {
    "@type": "Rating",
    "ratingValue": "5",
    "bestRating": "5"
  },
  "reviewBody": "T & F Electric has done my electrical work for years. They're the only one I rely on in Dunnellon. Very prompt, great service, fair price.",
  "publisher": {
    "@type": "Organization",
    "name": "Google"
  }
}
```

**Rules for Review schema:**

- Only include reviews with real captured names (first name plus last initial is fine, no "Happy Customer")
- Only include reviews with real captured content (verbatim quote)
- Only include the real star rating as captured
- `publisher` identifies the source platform (Google, Facebook, etc.) if known
- Phase 5 outputs one Review schema block per real captured testimonial

### ImageObject schema for featured photos

Optional but useful for hero and featured photos. Attaches structured metadata including caption and photographer credit for Google Places sourced photos.

```json
{
  "@context": "https://schema.org",
  "@type": "ImageObject",
  "contentUrl": "https://tandf-electric-grm.vercel.app/assets/photos/hero/photo-001-1600w.webp",
  "caption": "T&F Electric technician at a job site in Dunnellon",
  "creditText": "Photo by John D. via Google",
  "copyrightNotice": "Photo contributed via Google Places"
}
```

Phase 5 outputs ImageObject schema only for photos with non-empty captions or attribution strings. Skips for general library photos.

### Schema validation rules

Before Phase 6 approves any build, every JSON-LD schema block must pass validation:

1. **Valid JSON-LD syntax.** Parseable as JSON with correct `@context` and `@type` fields.
2. **No fabricated facts.** Every `ratingValue`, `reviewCount`, `foundingDate`, `telephone`, and `address` field must come from actual captured `profile.json` data. Phase 6 cross-references schema values against `profile.json` and fails the build on any mismatch.
3. **No placeholder text.** No `[BUSINESS NAME]`, no `example.com`, no `555-5555`, no `[object Object]`, no `undefined`, no `null` strings.
4. **Required fields present.** LocalBusiness requires `name`, `address`, `telephone`, `url`. FAQPage requires `mainEntity` with at least one `Question`. Service requires `serviceType`, `provider`, `areaServed`.
5. **Trade-specific type matches vertical.** Phase 5.5 verifies the `@type` in the injected schema matches the vertical set by Phase 4 in `profile.json`.
6. **Phone numbers formatted as E.164.** Schema `telephone` field uses E.164 (`+13524654600`) not the display format.
7. **URLs are absolute.** All schema URLs use the canonical domain, not relative paths.

Phase 6 check 11 runs these validations against the generated HTML. If any check fails, the build fails.

---

## Semantic HTML discipline

AI parsers preferentially process content wrapped in semantic HTML elements. A page wrapped entirely in `<div>` tags forces the AI to infer structure from visual cues alone. Semantic HTML is a free quality signal that every generated site can deliver at zero ongoing cost.

### Required semantic elements

Every generated contractor page MUST use these semantic elements in their intended roles:

- **`<main>`** wraps the primary page content (everything except nav and footer). Exactly one `<main>` per page. Receives `id="main-content"` for the skip-to-content link from `css-framework.md`.
- **`<article>`** wraps the full homepage content and long-form content pages (about, service sub-pages). Represents a self-contained document.
- **`<section>`** wraps each distinct content section (services, testimonials, FAQ, contact, etc.). Every `<section>` includes an `aria-labelledby` attribute pointing to the section's heading ID.
- **`<header>`** wraps the sticky navigation and any page-level header content.
- **`<footer>`** wraps the footer region. One per page.
- **`<nav>`** wraps the navigation menu. Multiple `<nav>` elements allowed (main nav, footer nav) but each must have an `aria-label` distinguishing them.
- **`<address>`** wraps the business contact information in the footer. The `<address>` element is a semantic signal that the enclosed content is contact data, not body text.
- **`<time>`** wraps any date reference (e.g., business hours, founding year, copyright year) with a `datetime` attribute in ISO format.
- **`<picture>`** wraps all responsive images (per `image-handling.md`).
- **`<details>` and `<summary>`** for FAQ accordion items (per `section-patterns.md`).

### Heading hierarchy rules

- **Exactly one `<h1>` per page.** The `<h1>` contains the primary page claim, typically the hero headline on the homepage or the main subject on sub-pages.
- **`<h2>` for major sections.** Each top-level section (services, testimonials, FAQ, contact) uses `<h2>`.
- **`<h3>` for subsections within `<h2>` sections.** For example, individual service cards within the services section use `<h3>`.
- **`<h4>` and deeper** only when there is a genuine fourth or deeper level of content hierarchy. Rare on contractor sites.
- **Never skip heading levels.** If a section has `<h2>`, the next level must be `<h3>`, never `<h4>`.
- **Heading text is descriptive and specific.** "Our Electrical Services in Marion County" is citable. "What We Do" is not.

### Per-page heading structure (reference)

**Homepage `index.html`:**
```
<h1>Fifty years. Two Tuccis. One phone number.  [hero headline]
  <h2>Our Services
    <h3>Residential Electrical
    <h3>Commercial Electrical
    <h3>Whole House Surge Protection
    [etc. one h3 per service]
  <h2>Real Work. Real Results.  [stats section]
  <h2>See the Difference  [before/after]
  <h2>What Marion County Says About T&F Electric  [testimonials]
  <h2>Common Questions  [FAQ]
    <h3>[each FAQ question becomes an h3 inside a details element]
  <h2>Tell Us About the Job  [contact]
```

**Service sub-page (e.g., `services/whole-house-surge-protection.html`):**
```
<h1>Whole House Surge Protection in Marion County
  <h2>Why Florida Homes Need Surge Protection
  <h2>Our $450 Special Offer
  <h2>Common Questions About Surge Protection  [service-specific FAQ]
  <h2>Ready to Protect Your Home  [contact CTA]
```

**About page `about.html`:**
```
<h1>Ben and Wendy Tucci, Fifty Years in Dunnellon
  <h2>How T&F Electric Started
  <h2>Our Credentials
  <h2>Serving Marion County
```

### Descriptive link text

Every `<a>` element must have descriptive link text. AI systems use link text to determine the target's content and relevance.

- ✅ "Call (352) 465-4600"
- ✅ "Request a free quote"
- ✅ "Read customer reviews"
- ✅ "Learn about our generator installations"
- ❌ "Click here"
- ❌ "Read more"
- ❌ "Learn more"
- ❌ "Here"

The CTA templates in `content-rules.md` already enforce this for visible buttons. This rule extends it to every link on the page.

### ARIA and accessibility

Semantic HTML is primarily for AI parsing, but it also delivers accessibility benefits that Phase 6 check 13 verifies.

- Every `<nav>` has `aria-label` distinguishing it (e.g., `aria-label="Main navigation"`, `aria-label="Footer navigation"`)
- Every `<section>` has `aria-labelledby` pointing to a heading ID
- Every interactive element has a visible focus indicator (defined in `css-framework.md`)
- Every image has descriptive `alt` text (not empty, not "image", not "photo")
- The skip-to-content link targets the `<main>` element

---

## Internal linking patterns for AI crawlers

AI crawlers follow internal links to build entity understanding of a site. When GPTBot or ClaudeBot reads a homepage and then follows a link to a service sub-page, it associates the entity on the sub-page with the entity on the homepage. A well-linked site gives the AI system more context about the business's scope, expertise, and service coverage. A site with shallow or disconnected pages forces the AI to treat each page as an isolated unit, which weakens citation confidence.

Phase 5 implements internal linking patterns that reinforce entity understanding across every generated site. The principle: every page should link to at least three other pages on the site using descriptive anchor text, and every core entity (service name, city name, credential) should be linked consistently wherever it appears.

### Required internal linking patterns

**Homepage to service sub-pages (if generated).** Every service card in the services grid that has a corresponding sub-page links to that sub-page with the anchor text being the full service name. Example: the service card for "Whole House Surge Protection" links to `services/whole-house-surge-protection.html` with anchor text "Whole House Surge Protection" (the full service name, not "Learn More").

**Homepage to services.html.** The services grid section header contains a link to the full `services.html` page with anchor text like "See all electrical services" (specific, not generic).

**Homepage to contact.html.** The primary CTA, mobile bottom CTA, and footer all link to `contact.html`. The anchor text varies by context: "Call (352) 465-4600" in the header (tel: link), "Request a quote" in the hero, "Get in touch" in the footer.

**Services page to service sub-pages.** Each service row on `services.html` links to its corresponding sub-page (if generated) with the full service name as anchor text.

**Service sub-pages back to services.html.** The breadcrumb navigation at the top of every sub-page links back to `services.html` with anchor text "Electrical Services" (or trade-appropriate equivalent). BreadcrumbList schema reinforces this to AI crawlers.

**Service sub-pages to related sub-pages.** At the bottom of each service sub-page, a "Related services" section links to 2-3 other service sub-pages. This creates a dense internal linking graph that helps AI crawlers understand the full service catalog as a connected entity. Example: the panel-upgrades sub-page links to surge-protection, whole-home-generator, and electrical-inspection.

**Testimonials page to service sub-pages.** If a testimonial mentions a specific service, the service name is linked to the corresponding sub-page (if generated). Example: a testimonial that mentions "Ben installed our generator" has "generator" linked to `services/generators.html`.

**Footer navigation on every page.** The footer on every page contains a full site map of internal links organized into logical groups: Services (all major service pages), Company (About, Testimonials, Contact), and Service Area (links to any city or region pages if generated). This gives every AI crawler a consistent entry point to every page on the site from anywhere on the site.

### Anchor text discipline

AI crawlers use anchor text to understand what the linked page is about. The anchor text "Whole House Surge Protection" on a link to a surge protection page is vastly more useful than "click here" or "learn more". Phase 6 check 8 verifies that no generated link uses banned generic anchor text.

**Banned anchor text patterns (Phase 6 fails the build):**

- "click here"
- "read more"
- "learn more"
- "more info"
- "here"
- "this page"
- "continue"
- Any single-word generic link that is not itself a meaningful entity name

**Required anchor text patterns:**

- Service names use the full service name as anchor text
- City names use the full city name (e.g., "Dunnellon" not "our Dunnellon coverage")
- Contact links use the actionable phrase ("Request a quote", "Call (352) 465-4600")
- Credential links use the credential itself ("Florida license EC13007855")

### Link density guidance

Every generated page should have 3-8 internal links in the body content (not counting nav and footer). Too few links and the page feels isolated to crawlers. Too many links and the page feels like a link farm. The sweet spot for a contractor service page is 4-6 internal links naturally woven into the content.

Do not create artificial linking opportunities. If a paragraph does not naturally reference another entity on the site, do not force a link into it. The rule is: if the text mentions a service, city, or credential that has its own page or anchor, link it. If not, let the text stand.

### Phase 6 internal linking verification

Phase 6 check 8 verifies internal linking discipline on every page:

1. Every page has at least 3 internal links in body content (excluding nav and footer)
2. No banned anchor text patterns appear anywhere
3. Every service card that has a corresponding sub-page links to it with the full service name
4. Every breadcrumb link has descriptive anchor text
5. Every footer link group is complete (Services, Company, Service Area)

---

## BLUF content structure

BLUF (Bottom Line Up Front) is the most important content principle for AI citation. Research documents that the first 30 percent of a page drives approximately 44.2 percent of all AI citations. AI systems read top-down and cite disproportionately from the opening. Every page on every generated contractor site must lead with fact-dense, answer-first content.

### The first 300 words rule

On every page, the first 300 words (measured after the `<h1>`) must contain as many of the following fact categories as Phase 2 captured:

1. **Business name and what they do** (e.g., "T&F Electric provides residential, commercial, and industrial electrical services")
2. **Service area with specific city names** (e.g., "across Dunnellon, Ocala, Belleview, and The Villages in Marion County")
3. **Years in business or founding year** (e.g., "since 1975")
4. **License number with state** (e.g., "Florida license EC13007855")
5. **Star rating and review count** (e.g., "4.6 stars from 41 Google reviews")
6. **Insurance and bonding status** (e.g., "licensed, insured, and bonded")
7. **Key operational commitment** (e.g., "same-day service available, 24/7 emergency response")
8. **Primary contact method** (e.g., "Call (352) 465-4600 for a free quote")

A fact-dense first paragraph that weaves 5-8 of these categories into natural prose is highly citable. A marketing-filler first paragraph that says "we pride ourselves on quality service" contains zero citable facts and is invisible to AI assistants.

### Before and after example

**Before (marketing filler, zero citable facts):**

> Welcome to T&F Electric, your trusted partner for all your electrical needs. With years of experience and a commitment to excellence, we take pride in serving our community. Whether you need a simple repair or a complex installation, our team is dedicated to exceeding your expectations.

Count the citable facts: zero. This paragraph could apply to any electrical contractor anywhere. No AI system will cite it.

**After (BLUF, fact-dense, citable):**

> T&F Electric provides residential, commercial, and industrial electrical work across Dunnellon, Ocala, Belleview, The Villages, and Silver Springs. Ben and Wendy Tucci have held Florida license EC13007855 continuously since 1975, with 4.6 stars from 41 Google reviews. Same-day service is available for surge protection, panel upgrades, and generator installation. 24/7 emergency service at (352) 465-4600.

Count the citable facts: business name, three service categories, six service area cities, two owner names, license number, state, founding year, years in business (implied), review count, review rating, three specific service names, one operational claim (same-day), one emergency claim (24/7), one phone number. Fourteen citable facts in four sentences.

### Hero copy as primary citation real estate

The 44.2 percent finding has a direct implication that is easy to miss: on any contractor homepage, the hero headline and subheadline are literally the first content that AI crawlers encounter. They are not decorative elements. They are the single highest-value citation real estate on the entire site. A well-written hero pair is worth more in AI citation weight than the next six paragraphs of body content combined.

This reframes hero copy from a design decision to a citation decision. The hero is not where we write an aspirational brand statement. It is where we load the maximum density of citable facts into the minimum viable text.

**What this means for hero structure.** The hero headline + subheadline + stats mini-bar (if present) collectively form a fact-dense opening statement that should cover 4-6 of the 8 BLUF fact categories by itself, before the AI crawler reaches the first body paragraph. The first body paragraph then reinforces and expands on those facts.

**What good hero copy looks like under this lens:**

- **Headline (Closing Table voice, fact-pattern):** "Fifty years. Two Tuccis. One phone number."
  - Citable facts: years in business (50), identity (two owners, family name Tucci), singular contact method
- **Subheadline (Closing Table voice, service + location):** "Licensed electrical contractor serving Dunnellon, Ocala, and Marion County since 1975. Florida license EC13007855."
  - Citable facts: trade category (electrical), license status, three service area cities, county, founding year, state, specific license number
- **Stats mini-bar (if present):** "50 years · 41 five-star reviews · 24/7 emergency"
  - Citable facts: years, review count, rating tier, operational commitment

Between these three elements alone, an AI crawler reading the T&F hero captures: business name, owner family name, owner count, trade category, six service area locations, founding year, years in business, license number, review count, rating, and 24/7 emergency availability. That is 11+ citable facts in roughly 40 words, before the body content even starts.

**What bad hero copy looks like under this lens:**

- Headline: "Quality Electrical Work You Can Trust"
  - Citable facts: zero
- Subheadline: "Your local experts for all your electrical needs"
  - Citable facts: zero (the word "local" is too vague to cite)
- Stats mini-bar: missing

This hero is citation void. An AI crawler reading it extracts nothing useful and moves on.

**Cross-reference to other skill files.**

- `hero-patterns.md` defines the structural layout of the hero section. Use the layout primitives there.
- `content-rules.md` defines the Closing Table voice rules and the three headline patterns (real number + real fact + action, or time/identity/location, or service + place). Those voice rules exist specifically to produce fact-dense hero copy that maximizes citation density.
- When hero copy is written in Phase 5, the BLUF lens in this file governs. Hero copy that reads beautifully but contains zero citable facts fails Phase 6 check 7 (BLUF verification now includes hero content, see below).

**Phase 6 hero citation check.** Phase 6 check 7 is expanded to verify the hero specifically: the hero headline + subheadline + optional stats bar must collectively contain at least 4 of the 8 BLUF fact categories before the first body paragraph begins. A hero that contains fewer than 4 citable facts fails the build regardless of how polished the body content is. This is intentional. The hero is too valuable as citation real estate to waste on aspirational marketing.

### Per-page BLUF rules

**Homepage:** The first paragraph after the hero section must meet the 300-word rule. The hero itself already contains some of the fact categories (headline, subheadline, stats mini-bar), but the first body paragraph must reinforce them in full sentences that AI systems can extract as answer snippets.

**Service pages and service sub-pages:** The first paragraph after the sub-hero must contain the business name, the specific service being described, the service area, and at least three service-specific facts (pricing if captured, typical duration, specific brands used, specific warranties, etc.).

**About page:** The first paragraph must contain owner names (if captured), founding year, business location, primary service category, and the license number. The Front Porch voice makes this warm and scene-driven, but the facts must still be present.

**Services page (`services.html`):** The first paragraph must enumerate the full service list with specific service names, service area, and the license number. This is the page AI systems are most likely to cite when users ask "what services does T&F Electric offer".

**Contact page (`contact.html`):** The first paragraph must contain the phone number, email, street address, hours of operation, and the service area. This is the page AI systems cite when users ask "how do I contact T&F Electric".

**Testimonials page (`testimonials.html`):** The first paragraph must contain the aggregate rating, the review count, and the source platform (Google). Follow with individual testimonials that themselves contain location data (city names).

### Phase 6 BLUF enforcement

Phase 6 check 7 verifies BLUF structure on every generated page, with specific hero verification on the homepage:

**Hero content check (homepage only):**

1. The hero headline + subheadline + optional stats mini-bar collectively contain at least 4 of the 8 BLUF fact categories
2. No banned phrases from `content-rules.md` appear in the hero (e.g., "trusted", "quality you can count on", "your local experts")
3. The hero headline matches one of the three Closing Table headline patterns from `content-rules.md`
4. The primary CTA in the hero is an actionable phrase ("Call (352) 465-4600" or "Request a quote"), never "Learn More"

**Body content check (all pages):**

1. Count the words in the first 300 words of body content after the `<h1>`
2. Check for the 8 fact categories
3. Require at least 5 of 8 categories to be present if Phase 2 captured them (if the category was not captured, exclude from the requirement)
4. Flag any first-paragraph content that matches banned phrases from `content-rules.md` (e.g., "pride ourselves", "committed to excellence", "trusted partner")
5. Fail the build if fewer than 5 citable facts appear in the first 300 words

This is a hard gate. BLUF failure is the single most common reason a site fails AI citation even with perfect schema. Hero failure is the single most avoidable reason a homepage wastes its highest-value citation real estate.

---

## AI crawler access (robots.txt)

A site that accidentally blocks GPTBot or PerplexityBot has zero chance of citation from those platforms regardless of content quality. This is the most common avoidable failure in AI-era SEO. WordPress sites with default security plugins, Cloudflare-protected sites with default bot fighting, and sites hosted on platforms with aggressive crawler defaults all routinely block AI crawlers by accident.

Phase 5 writes the following `robots.txt` on every generated site. Phase 6 check 9 verifies the file exists and contains the required allow entries.

### The default robots.txt for every generated site

```
# robots.txt for [business name]
# Generated by GRM Web Services prospect-site skill

# AI Crawlers - Explicitly Allowed
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: DuckAssistBot
Allow: /

User-agent: YouBot
Allow: /

# Search Engine Crawlers
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: DuckDuckBot
Allow: /

User-agent: Slurp
Allow: /

User-agent: Baiduspider
Allow: /

# Default rule for any other crawler
User-agent: *
Allow: /

# Sitemap
Sitemap: [canonical site URL]/sitemap.xml
```

### Crawler identity notes

- **GPTBot** is OpenAI's general-purpose crawler for training data and search. Allowing GPTBot enables ChatGPT citations.
- **ChatGPT-User** is the real-time browsing crawler used when ChatGPT users ask for current information. Critical for real-time citations.
- **OAI-SearchBot** is OpenAI's dedicated search crawler (separate from training and browsing).
- **ClaudeBot**, **Claude-User**, and **Claude-SearchBot** are Anthropic's three crawler identities covering training, real-time retrieval, and search-augmented generation respectively.
- **anthropic-ai** is an older Anthropic crawler identity sometimes still used.
- **PerplexityBot** and **Perplexity-User** are Perplexity's primary crawlers. Perplexity is the most citation-heavy AI assistant.
- **Google-Extended** is Google's AI-specific crawler identity for Gemini training data. Different from Googlebot.
- **Applebot-Extended** is Apple's AI crawler for future Siri and Apple Intelligence features.
- **DuckAssistBot** is DuckDuckGo's AI assistant crawler.
- **YouBot** is You.com's AI crawler (smaller platform, but growing).

### Defensive patterns

Phase 6 check 9 does NOT just verify the robots.txt file exists. It actively tests crawler access by:

1. Fetching the deployed site with a `User-Agent: PerplexityBot` header and verifying a 200 response
2. Fetching with `User-Agent: GPTBot` and verifying 200
3. Fetching with `User-Agent: ClaudeBot` and verifying 200

If any of these return 403, 429, or other blocking responses, the build is flagged. The most common cause is Vercel firewall rules or Cloudflare bot fighting inherited from another project on the team. Phase 6 reports the specific crawler that got blocked so the fix is targeted.

### Never block these

Do NOT add any `Disallow` rules to block directories or files on a generated contractor site. Contractor sites are marketing content and every page should be crawlable. The only legitimate reason to block a path would be a contact form submission URL or an admin panel, neither of which exist on v0.7 static sites.

---

## Sitemap and freshness signals

### XML sitemap

Phase 5 generates `sitemap.xml` at the root of every site. The sitemap lists every generated page with accurate `<lastmod>` dates. AI crawlers use sitemaps for discovery and freshness assessment.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://tandf-electric-grm.vercel.app/</loc>
    <lastmod>2026-04-09</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://tandf-electric-grm.vercel.app/about.html</loc>
    <lastmod>2026-04-09</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://tandf-electric-grm.vercel.app/services.html</loc>
    <lastmod>2026-04-09</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://tandf-electric-grm.vercel.app/testimonials.html</loc>
    <lastmod>2026-04-09</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://tandf-electric-grm.vercel.app/contact.html</loc>
    <lastmod>2026-04-09</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://tandf-electric-grm.vercel.app/services/whole-house-surge-protection.html</loc>
    <lastmod>2026-04-09</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
</urlset>
```

**Priority values:**
- `1.0` for homepage
- `0.9` for services.html
- `0.8` for about.html and contact.html
- `0.7` for testimonials.html, service sub-pages, gallery.html, specials.html
- `0.5` for any supplementary pages

**Changefreq values:**
- `weekly` for homepage and testimonials page (review counts update)
- `monthly` for services, about, contact, and service sub-pages

Phase 5 writes the current build date as the `<lastmod>` for every page. On subsequent rebuilds (when Phase 5 is re-run with updated content), the lastmod updates to the new date. This is how the freshness signal propagates.

### The freshness principle

Industry research shows that 50 percent of content cited by AI assistants was published or updated within the previous 13 weeks. Freshness is treated as a credibility signal. A contractor site whose sitemap shows content last updated six months ago is less likely to be cited than one updated two weeks ago.

**For v0.7 builds,** Phase 5 writes the build date as lastmod on every page. This is accurate on the day the site ships.

**For ongoing client relationships (post-signing),** the quarterly content refresh protocol in `deployment.md` updates review counts, adds recent project photos, refreshes seasonal FAQ questions, and touches the lastmod dates. This is how GRM's hosting relationships deliver ongoing AI citation value.

### Sitemap submission

After deployment, the sitemap should be submitted to:

1. **Google Search Console** — feeds Gemini via Google's crawler
2. **Bing Webmaster Tools** — feeds Copilot via Bing's crawler
3. **No direct AI platform submission** — ChatGPT, Claude, and Perplexity do not accept sitemap submissions directly; they discover content through crawling and partner search APIs

Phase 5 does not automate sitemap submission because both Google and Bing require account authentication. This is a post-deployment client onboarding task documented in `deployment.md`.

---

## llms.txt generation

The llms.txt specification was proposed by Jeremy Howard of Answer.AI in September 2024 as a robots.txt-style file for AI assistants. The idea is sound: a markdown file at the root of the site that provides LLMs with a structured summary of the content, purpose, and key facts.

### The honest assessment

Current industry data shows llms.txt adoption at approximately 10 percent across a sample of 300,000 domains. More importantly, llms.txt accounts for only 0.1 percent of AI crawler requests. AI systems are overwhelmingly hitting regular HTML pages, not the llms.txt file. A growing "llms.txt is dead" sentiment in the technical SEO community reflects the practical reality that the file has not delivered measurable citation improvements.

Despite this, Phase 5 generates llms.txt on every build for three reasons:

1. **The cost is zero.** Generating a 20-30 line markdown file is negligible in build time.
2. **Future-proofing.** If AI platforms begin weighting llms.txt more heavily, generated sites already have it.
3. **Sales positioning.** GRM's positioning as an AI-era web agency is stronger when every deliverable includes llms.txt even if the current impact is small.

### llms.txt template

Phase 5 generates the following `llms.txt` at the root of every site:

```markdown
# [Business Name]

> [One-line business description in Closing Table voice. Includes service category, service area, and license number if captured. Example: Licensed electrical contractor serving Dunnellon, Ocala, and Marion County since 1975. Florida license EC13007855.]

## About

[Business Name] is a [years in business]-year-old [trade] business in [primary city], [state]. Owned by [owner names if captured]. Holds [license number with state]. [Operational claim: 24/7 emergency, same-day service, etc.]

## Services

- [Service 1 name]: [one-sentence description]
- [Service 2 name]: [one-sentence description]
- [Service 3 name]: [one-sentence description]
- [continue for all captured services]

## Service Area

[Business Name] serves [list of specific cities] across [county name]. [Additional service area notes if captured.]

## Contact

- Phone: [formatted phone number, e.g., (352) 465-4600]
- Email: [email if captured]
- Address: [full address if captured]
- Hours: [business hours]
- Emergency: [24/7 note if applicable]

## Credentials

- Florida License: [license number]
- Insurance: [insurance status if captured]
- Years in Business: [number]
- Reviews: [aggregate rating] from [review count] [source, e.g., Google]

## Key Pages

- [Homepage](https://[canonical url]/)
- [Services](https://[canonical url]/services.html)
- [Testimonials](https://[canonical url]/testimonials.html)
- [Contact](https://[canonical url]/contact.html)
- [About](https://[canonical url]/about.html)
- [Additional service sub-pages if generated]
```

### No llms-full.txt in v0.7

The spec also defines `llms-full.txt`, a comprehensive single-document version of the entire site content. v0.7 does NOT generate llms-full.txt because (a) AI systems rarely fetch it, (b) it duplicates content that already exists on the regular HTML pages, and (c) the marginal impact is not worth the build complexity. If adoption data shifts in v0.8 or later, the decision can be revisited.

### File location

`llms.txt` is placed at the root of the site: `https://[domain]/llms.txt`. This matches the robots.txt convention. Phase 6 check 10 verifies the file exists and is reachable via HTTP GET.

---

## Platform-specific optimization notes

Each AI assistant handles citation differently. These notes summarize current (early 2026) behavior and what GRM can influence per platform.

### ChatGPT (OpenAI)

**Crawlers:** GPTBot (training), ChatGPT-User (real-time browsing), OAI-SearchBot (dedicated search).

**Discovery layer:** ChatGPT primarily uses Bing's search index as its first-stage discovery, then retrieves and reads top-ranking pages for synthesis. This means Bing's ranking signals matter for ChatGPT citations.

**What GRM controls:**
- Allow all three crawler identities in robots.txt (default for v0.7)
- Comprehensive LocalBusiness and FAQPage schema (high-impact)
- BLUF content structure on first 300 words (ChatGPT favors pages with clear answers at the top)
- Clean semantic HTML (improves parsing accuracy)
- Bing Places for Business claim (indirect via Bing ranking)

**What GRM does not control:**
- ChatGPT's tendency to favor business directories (Yelp, Angi) for local queries means contractor sites must be dense and specific enough to outperform aggregator listings
- ChatGPT's inline citation format and link prominence

### Claude (Anthropic)

**Crawlers:** ClaudeBot (training), Claude-User (real-time), Claude-SearchBot (search-augmented), anthropic-ai (legacy).

**Discovery layer:** Claude uses multiple search providers and its own retrieval. Notably, Claude is more likely than ChatGPT to cite primary sources (the contractor's own site) over aggregator listings, provided the primary source has sufficient depth and structure.

**What GRM controls:**
- Allow all four crawler identities in robots.txt (default for v0.7)
- Deep content on service sub-pages (Claude rewards depth)
- Well-structured schema (FAQPage and Service are strongest for Claude)
- Semantic HTML with clear hierarchy

**What GRM does not control:**
- Claude's citation format (numbered footnotes at end of responses)
- Claude's source-weighting algorithms

### Perplexity AI

**Crawlers:** PerplexityBot, Perplexity-User.

**Discovery layer:** Perplexity uses its own web crawler plus partnerships with search providers. Perplexity is the most citation-heavy of the five AI assistants, typically citing 5-15 sources per response.

**What GRM controls:**
- Allow PerplexityBot in robots.txt (default for v0.7)
- Fact density in content (Perplexity explicitly favors verifiable claims)
- Specific numbers, license numbers, and credentials in BLUF content
- FAQPage schema with specific answers

**What GRM does not control:**
- Perplexity's citation ranking algorithm
- User search behavior on Perplexity

**Note:** Perplexity is the single highest-opportunity platform for contractor sites because of its citation density. A site optimized for Perplexity tends to perform well across all five platforms.

### Microsoft Copilot

**Crawlers:** Bingbot, plus GPT-based identities.

**Discovery layer:** Tightly integrated with Bing's search index. Inherits Bing's crawling and ranking infrastructure, then layers AI synthesis on top.

**What GRM controls:**
- Bingbot access in robots.txt (default for v0.7)
- Schema markup (Bing treats schema similarly to Google)
- **Bing Places for Business claim** — often-overlooked structural advantage since most contractors skip Bing entirely
- Traditional on-page SEO basics (title tags, meta descriptions, H1 structure)

**What GRM does not control:**
- Bing's ranking algorithm
- Microsoft Edge's Copilot integration timing

**Strategic note:** The Bing Places gap is a real advantage. Most Marion County contractors have Google Business Profile but not Bing Places. GRM can claim Bing Places during client onboarding and immediately improve Copilot citation odds. This is documented as a post-signing task in `deployment.md`.

### Google Gemini

**Crawlers:** Googlebot, Google-Extended.

**Discovery layer:** Google's search index and Knowledge Graph. Gemini's AI Overviews appear directly in Google search results, synthesizing from multiple sources.

**What GRM controls:**
- Google-Extended access in robots.txt (default for v0.7)
- Schema.org LocalBusiness markup (heavily weighted by Google)
- Google Business Profile optimization (primary signal for local queries)
- Reviews on Google (AggregateRating matters for Gemini's recommendations)

**What GRM does not control:**
- Google's ranking algorithm
- AI Overviews trigger logic

**Strategic note:** Google Business Profile is arguably the single most important asset for Gemini citation. Most contractors already have one, but optimization (complete profile, category accuracy, photo quality, service list specificity) is often neglected. This is documented as a post-signing task in `deployment.md`.

### Platform-specific quick reference

A summary of the highest-leverage action GRM controls for each platform. Use this table as a quick lookup when deciding where to invest effort on a specific client site.

| Platform | Primary discovery layer | Highest-leverage GRM action | Killer feature |
|---|---|---|---|
| ChatGPT | Bing index + OpenAI retrieval | BLUF content in first 300 words (ChatGPT favors direct answers at the top) | Comprehensive FAQPage schema |
| Claude | Multi-provider + Claude retrieval | Deep, structured service sub-pages (Claude rewards depth over aggregators) | Semantic HTML with clear hierarchy |
| Perplexity | Own crawler + partnerships | Fact density and verifiable claims (numbers, license, credentials) | Specific numbers in BLUF and FAQ answers |
| Copilot | Bing index | **Claim and optimize Bing Places for Business** (structural advantage) | LocalBusiness schema with complete fields |
| Gemini | Google index + Knowledge Graph | **Optimize Google Business Profile** (primary signal) | AggregateRating schema with real review data |

**Perplexity is the highest-ROI target for fact density work.** A site optimized for Perplexity tends to perform well across all five platforms because the fact-dense BLUF structure that Perplexity rewards also helps ChatGPT, Claude, and the others. When prioritizing effort, optimize for Perplexity first and the rest follow.

**Bing Places and Google Business Profile are the two external signals GRM must address during onboarding.** Neither is controlled by the generated site itself. Both are documented as client onboarding tasks in `deployment.md`. Skipping either one leaves a significant citation gap on Copilot (Bing) or Gemini (Google).

---

## Monitoring and measurement

Full monitoring and measurement implementation is covered in `deployment.md` under the client services and ongoing relationship section. This section gives a brief overview of the tools and the key metric.

### The key metric: AI-referred sessions

Track the percentage of website sessions referred from AI platforms. The AI referrer domains to monitor in analytics:

- `chat.openai.com`
- `chatgpt.com`
- `claude.ai`
- `perplexity.ai`
- `copilot.microsoft.com`
- `gemini.google.com`
- `you.com`
- `duckduckgo.com` (when AI Assist is used)

Any session referred from these domains represents an AI-driven visit. The 527 percent year-over-year growth in AI-referred sessions means this traffic source is small today but compounding fast.

### Tool landscape

The GEO (Generative Engine Optimization) tool category is young and evolving rapidly. Current options (early 2026):

- **Otterly.ai** — monitors brand mentions across AI platforms
- **Gauge** — tracks AI model perception and brand recommendations
- **LLMClicks.ai** — tracks AI referral traffic via analytics
- **Birdeye Search AI** — multi-location brand visibility
- **SE Ranking** — traditional SEO platform with AI visibility features
- **Frase** — content optimization for AI citation

**Recommended GRM stack for client services (documented in `deployment.md`):**
- One AI citation tracker (Otterly or Gauge) for ongoing monitoring
- Analytics segmentation of AI referral traffic (custom UTM or LLMClicks.ai)
- Traditional Google Analytics 4 with referrer filtering on AI domains

---

## Phase 5 integration points

Phase 5 generates the HTML structure of every page. Phase 5.5 injects structured data, llms.txt, robots.txt, and sitemap.xml after Phase 5 completes. This section documents the exact integration between content generation and SEO/GEO injection.

### Phase 5 responsibilities (content and structure)

1. **Write semantic HTML** on every page per the rules in the Semantic HTML discipline section above
2. **Enforce BLUF content structure** on the first 300 words of every page using the Closing Table voice rules from `content-rules.md`
3. **Write descriptive link text** on every `<a>` element (CTA templates already cover this)
4. **Use `<address>` for contact blocks** in the footer and contact page
5. **Use `<time>` with `datetime` attributes** for all date references
6. **Apply heading hierarchy rules** (one h1, never skip levels)
7. **Include ARIA labels** on nav and section elements

### Phase 5.5 responsibilities (structured data and meta)

Phase 5.5 runs AFTER Phase 5 completes HTML generation. It reads the generated HTML and `profile.json` together to inject structured data and related files.

1. **Generate LocalBusiness JSON-LD** with trade-specific @type and inject into homepage `<head>`
2. **Generate FAQPage JSON-LD** for every page with an FAQ section and inject into that page's `<head>`
3. **Generate Service JSON-LD** for every service sub-page and inject into the sub-page `<head>`
4. **Generate BreadcrumbList JSON-LD** for every non-homepage and inject into the respective page `<head>`
5. **Generate Review JSON-LD** for every real captured testimonial and inject into `testimonials.html` `<head>`
6. **Generate ImageObject JSON-LD** for featured photos with captions or attribution and inject appropriately
7. **Write meta tags** on every page: title, description (fact-dense, 150-160 characters), OpenGraph, Twitter Card
8. **Write canonical link tag** on every page
9. **Write `sitemap.xml`** at the site root with all generated pages and accurate lastmod dates
10. **Write `robots.txt`** at the site root with the full AI crawler allow list
11. **Write `llms.txt`** at the site root with the business summary

### Meta tag templates

Every page receives these meta tags in the `<head>`:

```html
<!-- Primary meta tags -->
<title>[Page-specific title, 50-60 characters, includes business name and primary keyword]</title>
<meta name="description" content="[Fact-dense description, 150-160 characters, includes license, location, phone if space allows]">
<link rel="canonical" href="[canonical URL for this page]">

<!-- OpenGraph -->
<meta property="og:type" content="website">
<meta property="og:title" content="[Same as page title or shorter variant]">
<meta property="og:description" content="[Same as meta description or shorter variant]">
<meta property="og:url" content="[canonical URL for this page]">
<meta property="og:image" content="[canonical URL to featured photo]">
<meta property="og:site_name" content="[Business name]">
<meta property="og:locale" content="en_US">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="[Same as og:title]">
<meta name="twitter:description" content="[Same as og:description]">
<meta name="twitter:image" content="[Same as og:image]">

<!-- Business-specific -->
<meta name="author" content="[Business name]">
<meta name="geo.region" content="US-FL">
<meta name="geo.placename" content="[Primary city]">
<meta name="geo.position" content="[latitude];[longitude]">
<meta name="ICBM" content="[latitude], [longitude]">
```

### Title tag patterns

Phase 5.5 generates page titles using these patterns:

- **Homepage:** `[Business Name] | Licensed [Trade] in [Primary City], [State]` — e.g., "T&F Electric | Licensed Electrician in Dunnellon, FL"
- **About page:** `About [Business Name] | [Primary City] [Trade] Since [Year]` — e.g., "About T&F Electric | Dunnellon Electrician Since 1975"
- **Services page:** `[Trade] Services | [Business Name] in [Primary City], [State]` — e.g., "Electrical Services | T&F Electric in Dunnellon, FL"
- **Service sub-page:** `[Service Name] | [Business Name] in [Primary City], [State]` — e.g., "Whole House Surge Protection | T&F Electric in Dunnellon, FL"
- **Testimonials page:** `Reviews | [Business Name] in [Primary City], [State]` — e.g., "Reviews | T&F Electric in Dunnellon, FL"
- **Contact page:** `Contact [Business Name] | [Primary City] [Trade]` — e.g., "Contact T&F Electric | Dunnellon Electrician"

Every title is under 60 characters where possible. Every title includes the business name, the trade, and the primary city. These are the three fact categories most likely to match user queries.

### Meta description patterns

Phase 5.5 generates meta descriptions using the BLUF principle:

- **Homepage:** `[Business Name] provides [services] across [service area] since [year]. [License number]. [Rating] stars from [reviews] reviews. Call [phone].`
- **Service sub-page:** `[Service Name] in [primary city], [state]. [Business Name] has provided [related service details] since [year]. Call [phone] for a free quote.`

Example for T&F Electric homepage: `T&F Electric provides residential, commercial, and industrial electrical work across Marion County since 1975. Florida license EC13007855. Call (352) 465-4600.` — 152 characters, fact-dense, citable.

---

## Phase 6 verification checks

Phase 6 verifies SEO and GEO implementation across multiple checks. These are hard gates: any failure blocks the build.

### Check 9: Crawler access verification

1. `robots.txt` file exists at site root
2. robots.txt contains Allow entries for all required AI crawlers (GPTBot, ChatGPT-User, ClaudeBot, Claude-User, Claude-SearchBot, PerplexityBot, Google-Extended)
3. Fetching the homepage with `User-Agent: PerplexityBot` returns 200
4. Fetching with `User-Agent: GPTBot` returns 200
5. Fetching with `User-Agent: ClaudeBot` returns 200
6. No Disallow rules that would block any generated page
7. Sitemap URL is referenced at the bottom of robots.txt

### Check 10: llms.txt verification

1. `llms.txt` file exists at site root
2. File contains business name, description, services list, contact info, and key pages
3. No placeholder text or unresolved templating
4. File is reachable via HTTP GET

### Check 11: Structured data validation

1. Every generated HTML page contains valid JSON-LD in the `<head>`
2. Homepage contains LocalBusiness schema with trade-specific @type
3. Every page with an FAQ section contains FAQPage schema matching the rendered HTML
4. Every service sub-page contains Service schema
5. Every non-homepage contains BreadcrumbList schema
6. Testimonials page contains Review schema for each captured testimonial
7. No fabricated facts: every `ratingValue`, `reviewCount`, `foundingDate`, `telephone`, and `address` field matches `profile.json` captured data
8. No placeholder text in any schema block
9. All schema URLs are absolute (use canonical domain)
10. Phone numbers in schema are E.164 format
11. Schema passes `schema.org` validator syntax check

### Check 7: BLUF content verification

1. First 300 words of body content (after `<h1>`) on every page contain at least 5 of the 8 fact categories from the BLUF content section
2. No banned phrases from `content-rules.md` appear in the first 300 words
3. Business name, primary city, and at least one credential (license, years, rating) appear in the first 150 words
4. Phone number appears in the first 300 words

### Check 8: Semantic HTML and internal linking verification

**Semantic HTML:**

1. Every page has exactly one `<h1>`
2. Every page uses `<main>`, `<header>`, `<footer>`, `<nav>`
3. Every `<section>` has an `aria-labelledby` attribute
4. Every `<nav>` has an `aria-label` attribute
5. Heading hierarchy never skips levels
6. `<address>` is used in the footer for business contact info

**Internal linking (see Internal linking patterns section):**

7. Every `<a>` element has descriptive link text (no "click here", "read more", "learn more", "more info", "here", "this page", "continue")
8. Every page has at least 3 internal links in body content (excluding nav and footer)
9. Every service card with a corresponding sub-page links to it using the full service name as anchor text
10. Every non-homepage has breadcrumb navigation with descriptive anchor text
11. Footer navigation on every page contains complete Services, Company, and Service Area link groups
12. If a service sub-page is generated, it contains a "Related services" section linking to 2-3 sibling sub-pages

### Check 14: Meta tag verification

1. Every page has a `<title>` element under 60 characters
2. Every page has a `<meta name="description">` element between 120 and 160 characters
3. Every page has a `<link rel="canonical">` element
4. Every page has OpenGraph tags (og:title, og:description, og:url, og:image)
5. Every page has a Twitter Card tag
6. Geo meta tags are present on the homepage

---

## What is deliberately not in v0.7

The AI citation research surfaced several high-value tactics that v0.7 does not implement. This section names them explicitly so nothing gets silently dropped. Each one is either a v0.8+ roadmap item or a deliberate scope boundary. When these tactics appear in client conversations or sales pitches, GRM should be able to speak to them with confidence and explain the reasoning.

### Marion County [Trade] Guide content hub (Tier 3 GEO tactic)

**What it is.** A long-form authoritative resource page (2,000+ words) about a specific trade in the local market, covering topics like: permit requirements in Marion County, typical cost ranges in 2026, seasonal considerations for Florida homes (lightning season, humidity, freeze events), how to choose a licensed contractor, warning signs of unlicensed operators, local code references. The Cowork research cites this as a Tier 3 implementation (high impact, higher effort) because content hubs of this depth are highly citable by AI assistants answering research queries like "how much does a whole house surge protector cost in Ocala" or "do I need a permit for water heater replacement in Marion County".

**Why v0.7 does not build it.** A content hub of this depth requires a fundamentally different Phase 2 data capture. The prospect-site skill v0.7 captures what a contractor has on their existing site plus what Google Places returns. It does not capture permit requirements from Marion County government, it does not capture Florida building code references, and it does not capture seasonal considerations specific to Central Florida. Adding content hub generation to v0.7 would require either a separate data source (which does not exist yet) or a research sub-workflow (which would blow out the scope of a single-session build).

**Roadmap.** This is a v0.8+ target. The v0.8 architecture may introduce a separate "content research" workflow that captures Marion County government, code, and seasonal data once, stores it centrally, and reuses it across every generated trade-specific content hub. That way the skill builds the hub in Phase 5 from a shared knowledge base rather than re-researching per prospect. Documented in more detail in `scale-architecture.md`.

**What GRM should say in sales conversations.** Content hubs are a premium add-on, not a baseline deliverable. A contractor who wants "Marion County Plumbing Guide" or "Ocala Electrical Licensing Explained" as a dedicated page on their site can get it as a billable add-on after v0.7 launches. It is not included in the base Elevate or Launch tier.

### Backlink building and domain authority work

**What it is.** The traditional SEO playbook: earning inbound links from business directories, local news sites, chamber of commerce listings, industry associations, and partner sites.

**Why v0.7 does not do this.** Backlink work is an ongoing operational activity, not a skill output. It is also fundamentally contrary to the strategic thesis of this file: the 17 percent overlap finding means AI citations do not care about backlinks. GRM is building for the new game, not the old one.

**What GRM should say in sales conversations.** Traditional SEO is still worth doing at a basic level (Google Business Profile, Bing Places, consistent NAP across citations, responsive to Google reviews). But backlink campaigns and link-building services are explicitly not part of the GRM value prop. If a prospect asks about backlinks, the answer is: "We focus on the search landscape that actually matters for contractors in 2026. The old backlink game takes three years to pay off. AI citations pay off the day the crawlers index your site. Your time and budget are better spent on what we build."

### Keyword research and content marketing strategy

**What it is.** Ongoing blog post production, long-tail keyword targeting, content calendars, and topical authority building.

**Why v0.7 does not do this.** Content marketing is a separate recurring engagement, not a one-time site build. GRM may offer it as a paid add-on in the future, but it is not part of v0.7.

**Roadmap.** v0.8+ may introduce a quarterly content refresh workflow that ties into the 13-week freshness cycle (documented in `deployment.md`). That workflow would generate a small number of fresh pages per quarter per client based on seasonal topics and captured site data. Not a full content marketing service, but enough to maintain the freshness signal that AI crawlers reward.

### AI share of voice monitoring and competitive intelligence

**What it is.** Tracking which contractors get recommended by each AI assistant for target queries (e.g., "best plumber in Ocala") and building competitive intelligence reports.

**Why v0.7 does not do this.** Monitoring is an ongoing client services activity, not a generator task. Full implementation is documented in `deployment.md` under the monitoring stack. The GEO tool landscape in this file gives GRM a starting point for tool selection.

**Roadmap.** Once GRM has 5+ paying clients, the monitoring stack becomes worth automating. Until then, manual checks via Otterly or Gauge on a monthly basis are sufficient.

### Multi-location or franchise support

**What it is.** Contractor businesses with multiple locations or service territories requiring per-location landing pages with unique local optimization.

**Why v0.7 does not do this.** Marion County contractors GRM is targeting are overwhelmingly single-location operators. Adding multi-location support would complicate the skill without matching the market reality.

**Roadmap.** If GRM wins a multi-location client (e.g., an HVAC chain with locations in Ocala, Gainesville, and The Villages), a v0.8+ extension can add per-location page generation. Not a v0.7 target.

### llms-full.txt generation

**What it is.** The extended version of the llms.txt spec that provides a comprehensive single-document version of the entire site's content, designed for LLM ingestion.

**Why v0.7 does not do this.** llms.txt itself has limited measured impact (0.1 percent of AI crawler requests, approximately 10 percent adoption). llms-full.txt has even less measured impact. Both files are low-cost to generate but high-cost to maintain correctly, and the current evidence does not support spending the effort on the full version.

**Roadmap.** If industry data shifts meaningfully (e.g., if llms.txt adoption crosses 30 percent and major AI platforms begin explicitly prioritizing it), revisit in a v0.8+ release. Until then, the minimal llms.txt in v0.7 is sufficient.

---

## Common mistakes to avoid

- **Do not fabricate any fact in schema, meta tags, or llms.txt.** Every value comes from `profile.json` captured data. Better to omit a field than invent one.
- **Do not use placeholder text in generated output.** No `[BUSINESS NAME]`, no `example.com`, no `555-5555`. Phase 6 fails the build on any placeholder detected.
- **Do not block any AI crawler in robots.txt.** The default robots.txt allows all known AI crawlers. Do not add Disallow rules without explicit reason.
- **Do not skip semantic HTML elements.** `<main>`, `<article>`, `<section>`, `<address>` are required, not optional.
- **Do not use marketing filler in the first 300 words of any page.** The BLUF rule is a hard gate.
- **Do not exceed 60 characters in title tags or 160 characters in meta descriptions.** Search results truncate past these limits.
- **Do not use relative URLs in schema or meta tags.** All URLs in structured data are absolute and use the canonical domain.
- **Do not forget to update lastmod dates on rebuilds.** Phase 5.5 must write the current date on every rebuild, not leave stale dates.
- **Do not create duplicate schema blocks.** One LocalBusiness per site, one FAQPage per page with FAQs, one BreadcrumbList per non-homepage.
- **Do not skip the telephone E.164 format in schema.** The display format `(352) 465-4600` is for visible text. The schema format is `+13524654600`.
- **Do not write filler FAQ content.** Every FAQ answer must contain specific verifiable facts. If Phase 2 did not capture enough facts to answer a question, drop the question rather than write filler.
- **Do not treat llms.txt as the centerpiece.** Current adoption and impact are limited. Schema and BLUF content carry the citation weight.
- **Do not use generic anchor text for internal links.** "Click here", "read more", and "learn more" fail Phase 6 check 8. Every link uses the full entity name as anchor text (service name, city name, credential, or actionable phrase).
- **Do not create isolated pages with no internal links.** Every generated page needs at least 3 internal links in body content so AI crawlers can build entity understanding.

---

## Self-check before Phase 5.5 marks SEO and GEO work complete

Before marking SEO and GEO injection complete, Phase 5.5 verifies:

- [ ] LocalBusiness schema is injected on the homepage with trade-specific @type
- [ ] FAQPage schema is injected on every page with an FAQ section, matching rendered HTML content
- [ ] Service schema is injected on every service sub-page
- [ ] BreadcrumbList schema is injected on every non-homepage
- [ ] Review schema is injected on testimonials.html for every real captured testimonial
- [ ] No fabricated facts anywhere in schema (cross-checked against profile.json)
- [ ] No placeholder text anywhere in schema or meta tags
- [ ] All schema URLs are absolute and use the canonical domain
- [ ] All phone numbers in schema are E.164 format
- [ ] Every page has a valid title tag under 60 characters
- [ ] Every page has a meta description between 120 and 160 characters
- [ ] Every page has canonical, OpenGraph, and Twitter Card tags
- [ ] robots.txt exists and allows all required AI crawlers
- [ ] sitemap.xml exists with accurate lastmod dates on every page
- [ ] llms.txt exists with populated business summary
- [ ] Phase 6 BLUF content check passes on every page
- [ ] Phase 6 semantic HTML check passes on every page
- [ ] Phase 6 structured data validation passes on every schema block
- [ ] Phase 6 internal linking check passes (no banned anchor text, 3+ internal links per page, complete footer navigation, breadcrumbs on all non-homepages)

---

## Version

seo-geo.md v0.7.0. Foundation file for Phase 5.5 structured data injection and Phase 6 verification. Based on industry research current through April 2026 including adoption and impact data on llms.txt, schema.org structured data, AI crawler behavior, and platform-specific citation patterns for ChatGPT, Claude, Perplexity, Copilot, and Gemini. When industry research updates significantly, this file should be re-reviewed for accuracy. Last research refresh: April 9, 2026.

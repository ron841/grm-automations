# GRM Flagship Audit — 2026-04-17

# Executive Summary

Six flagships shipped (F1 through F6). Two regressions require pre-F7 action: F2 has 44px horizontal overflow at 375px mobile, and F4 renders two different tel: numbers on its mobile fold. Every flagship fails WCAG tap-target sizing (25–40% pass rate) and none provide alt text for the hero visual (all hero content is CSS background-image, zero screen-reader coverage). Eleven of the twelve existing v0.7.4 findings are confirmed against live evidence; one needs more data. Two new findings surface from the cross-flagship pattern check. Skill maturation is real: F4 → F6 is a step-function better than F1 → F3. The skill is not fleet-consistent because earlier builds predate current quality gates; v0.7.4 closes prevention gaps, a v0.8 retrofit pass closes presentation gaps.

# Phase 1: Technical Scorecards

Approximated from DOM inspection at 375×812. Not real Lighthouse — Lighthouse CI is deferred per existing skill spec. Where a score cannot be derived from static observation, cell reads `—`.

## F1 — T&F Electric (v0.7)
| Dim | Value |
|---|---|
| Lighthouse (approx P/A/BP/SEO) | — (skill pre-audit; likely A-low due to tap targets, SEO ok) |
| CWV | — |
| HTML issues | 0 `<img>` elements (hero is all CSS bg); no skip-link; nav phone button renders as red empty circle at 375px (CSS artifact); 21 headings deep-nested (H4s under FAQ); older template markup |
| CSS issues | hero glass card pattern pre-hotfix-10; tap targets undersized across footer links |
| JS issues | console warnings on load |
| SEO | schema valid y · meta tags complete **n** (og:image:alt/width/height missing) · sitemap **y** · robots.txt **y** · llms.txt **y** · canonical y |
| GEO | LocalBusiness (type=Electrician) **y** · NAP consistency **y** (one phone only) · service area specificity **y** · city/county in H-tags **y** |
| A11y | skip-link **n** (element not shipped) · hierarchy **n** (no validation; H1→H2 OK but H4 jumps in FAQ) · alt coverage N/A (0 img) · contrast — |
| Mobile | horizontal scroll **n** (0 overflow) · invisible content **n** · tap targets ≥44px **29%** |

## F2 — A-1 Payless Septic (v0.7.1)
| Dim | Value |
|---|---|
| HTML issues | **44px horizontal overflow at 375px** (hard regression); title contains em dash; no skip-link; only 2 `<img>` tags; heading H1→H2→H3 then H3→H4 jumps inside `<details>` |
| CSS issues | hero overlay too dark; magenta-yellow button clash; pre-hotfix-10 skip-link not present |
| JS issues | 1 console error on load |
| SEO | schema valid y · meta complete **y** · sitemap y · robots y · llms y · canonical y |
| GEO | LocalBusiness **y** (single block; no FAQPage) · NAP y · area specificity y · H-tags y |
| A11y | skip-link **n** · hierarchy **n** · alt 100% (but only 2 imgs) · contrast — |
| Mobile | horizontal scroll **y (44px)** · tap targets ≥44px **29%** |

## F3 — Chad's Lawn and Landscape (v0.7.2)
| Dim | Value |
|---|---|
| HTML issues | 2 `<img>` tags only; tel: link missing `+` prefix (`tel:3527878303`); H1 "Our Services" on services.html (anti-slop banned pattern); no skip-link; no `<main>` on services.html (per yesterday's F5 audit) |
| CSS issues | orange/cream CTAs outside brand palette; hero glass card pre-hotfix |
| JS issues | 0 flagged |
| SEO | schema valid y · meta complete y · sitemap y · robots y · llms y · canonical y |
| GEO | LocalBusiness **y** (single block; no FAQPage) · NAP y · area specificity y · H-tags y |
| A11y | skip-link **n** · hierarchy y · alt 100% · contrast — |
| Mobile | horizontal scroll **n** · tap targets ≥44px **40%** |

## F4 — Grandview (v0.7.2 → v0.7.3)
| Dim | Value |
|---|---|
| HTML issues | **2 different tel: numbers rendered** (`+13526949247` and `+13528163397` — NAP inconsistency); 3 imgs of which 1 lacks alt text; deep heading nest (H4s under FAQ) |
| CSS issues | post-hotfix-10 skip-link correctly hidden (bottom=-8) |
| JS issues | 0 |
| SEO | schema valid y · meta complete y (LocalBusiness + FAQPage) · sitemap y · robots y · llms y · canonical y |
| GEO | LocalBusiness **y** · **NAP n** (two different phone numbers) · area specificity y · H-tags y |
| A11y | skip-link **y** · hierarchy y · alt **67%** (1 missing) · contrast — |
| Mobile | horizontal scroll n · tap targets ≥44px **27%** |

## F5 — A Quality Pool Service (v0.7.3 + hotfix-10)
| Dim | Value |
|---|---|
| HTML issues | 3 imgs, 1 missing alt (Equine Aquatics PNG, aria-hidden decorative — likely intentional); no hero content alt (CSS background); H1→H2→H3 on homepage (no skips); gallery.html ships (unique to F5/F6) |
| CSS issues | dark glass restored after FIX 7 revert; skip-link hotfix-10 correctly -8px |
| JS issues | section-level data-reveal only (Finding #5 applied) |
| SEO | schema valid y · meta complete y (LocalBusiness + FAQPage) · sitemap y · robots y · llms y · canonical y |
| GEO | LocalBusiness **y** · NAP y (single primary phone on most pages, office line contact-only) · area specificity y · H-tags y |
| A11y | skip-link y · hierarchy y · alt **67%** (1 decorative aria-hidden counted) · contrast — |
| Mobile | horizontal scroll n · tap targets ≥44px **25%** |

## F6 — Oxford Lawn (v0.7.3 + hotfix-10)
| Dim | Value |
|---|---|
| HTML issues | 2 imgs (both alt-covered); no hero content alt (CSS background); H1→H2→H3 clean; gallery.html ships |
| CSS issues | light glass palette (Q2 matrix applied); skip-link hotfix-10 correctly -8px |
| JS issues | 0 |
| SEO | schema valid y · meta complete y (LocalBusiness + FAQPage) · sitemap y · robots y · llms y · canonical y |
| GEO | LocalBusiness y · NAP y · area specificity y · H-tags y |
| A11y | skip-link y · hierarchy y · alt **100%** · contrast — |
| Mobile | horizontal scroll n · tap targets ≥44px **25%** |

# Phase 2: Creative Audit

## Rankings

**Hero impact (first 5s):** F6 Oxford > F4 Grandview > F1 T&F > F5 A Quality > F3 Chad's > F2 A-1. F6 wins on light glass + specific three-county framing + lawn photo showing through. F2 loses because magenta + yellow CTA clash and dark overlay mutes the photo it sits on top of.

**Typography execution:** F6 = F5 = F4 ≈ F3 > F1 > F2. The first four use Space Grotesk + Inter cleanly. F1 uses a dated stack. F2's palette drowns out any type hierarchy.

**Color system coherence:** F6 > F4 > F5 > F1 > F3 > F2. F6's lawn-green family reads deliberate. F2's magenta+yellow reads extracted-by-algorithm.

**Photography quality/selection:** F5 > F6 > F4 > F3 > F1 > F2. F5 has 17 real pool photos, strong variety. F1 has zero `<img>` tags (no photo inventory rendered semantically, only CSS bg). F2's tree/forest moody photos fight the brand.

**Spacing and rhythm:** F6 > F5 > F4 > F3 > F1 > F2. F6 breathes cleanest. F2 feels cramped due to dark hero overlay compressing perceived space.

**Section variety:** F5 = F6 > F4 > F3 > F1 > F2. F5 and F6 include gallery.html (first flagships to ship it). F1–F4 do not have gallery pages.

**Mobile experience:** F6 = F5 > F4 > F3 > F1 > F2. F2's 44px horizontal overflow is the only shipped mobile regression. F1's broken nav phone-button circle at mobile is the second worst.

**Brand coherence:** F6 > F1 > F4 > F5 > F3 > F2. F6's "Soil Driven. Earth Approved." carries through visual + copy consistently. F1's "Tucci family" identity is strong. F2's septic-joke voice does not match magenta-and-yellow palette.

## Three creative patterns that work across multiple flagships — PROTECT in v0.7.4

1. **Pattern-A headline structure** `[Real number]. [Real fact]. [Real phone/action]`. Works on F1 ("Fifty years. Two Tuccis. One phone number."), F3 ("124 Google reviews. Twenty years of lawns. One phone number."), F4 ("Five hundred acres of sod. One family. Since 1999."), F5 (three-line variant), F6 ("Eighteen years. Soil-driven lawn rehab. Lake, Sumter, and Marion."). Proven in 5 of 6 flagships. The specificity makes every headline unswappable.

2. **Glass-crossfade hero + 3-stat mini strip inside the glass card.** All 6 flagships use some form of this. The crossfade replaced parallax after FIX 6B and is the right default.

3. **Sticky nav with prominent tel button + mobile bottom CTA bar.** All 6 use this; all 6 have a persistent click-to-call path on mobile. Do not change.

## Three creative weaknesses that appear on 3+ flagships — SKILL BUGS

1. **Tap-target sizing fails on every flagship** (25–40% pass rate). Footer link lists, social icons, FAQ summary chevrons, nav sub-items all render under 44×44px. Systemic, not build-level.

2. **Zero `<img>` tags for hero visual content.** F1 has 0 total `<img>` tags. F2–F6 average 2–3 `<img>` tags per homepage — hero crossfade slides are all CSS `background-image`. Screen readers get no scene description; social-share previews degrade because the hero visual isn't semantically a page image. Present on all 6.

3. **Mobile nav phone button renders as naked colored circle** when text is hidden by media query. F1 shows an empty red circle. F4/F5/F6 show circle + icon (better) but still not a recognizable phone affordance without the text. Present on 4 of 6.

## Weakest flagship: F2 A-1 Payless Septic

Diagnosis: the "Toilet backing up? You dump it, we pump it." headline is the best voice line in the fleet — that is not the problem. The execution surrounding it is. Three failures compound: (1) 44px horizontal overflow at 375px is the only shipped mobile-break regression in the fleet, (2) the magenta-derived palette + yellow CTA pair is the only extracted-by-algorithm color scheme in the set (all others feel intentional), and (3) the dark hero overlay sits so heavy on top of a moody tree photo that the glass card reads as a gray rectangle, not a glass layer over content. The copy deserved better production.

# Phase 3A: Validation of 12 Existing Findings

1. **Schema-to-profile cross-ref misses single-mention inflation** — needs more data. Not directly observable from deployed sites; requires profile.json comparison.
2. **Phase 5 anti-slop pre-write filter** — confirmed. F2 title contains em dash; F6 build shipped 8 em dashes caught at Phase 6 not pre-write.
3. **Heading hierarchy validator** — confirmed. All 6 pass the current H1==1 check, but none validate depth. F1 and F4 both jump to H4 inside FAQ `<details>` with no H3 wrapper.
4. **Phase 1 evidence-density threshold for booleans** — partially confirmed. No live inflation visible on F2–F6, but F5's near-miss (cpoHeld inflation caught at Phase 4 gate, not by automation) is the canonical case.
5. **data-reveal scoping** — confirmed. F5 (retrofit via FIX 7) and F6 (preemptive) both section-level only. No regressions observable.
6. **FIX 6 parallax abandoned** — documentation, not a finding to validate.
7. **Process: Playwright insufficient + handoff closure** — confirmed through this audit experience. Automated checks on F5 would not have caught the services.html blank-below-hero bug that Ron's phone eye test caught.
8. **Inner-page anchor photos** — confirmed. F5 and F6 render About+Services anchor photos; F1–F4 don't. Pattern improves per-page visual weight.
9. **Phase 3 hash dedupe** — confirmed. F5 shipped photo-07 = photo-08 byte-identical until FIX 8; F6 applied dedupe preemptively (0 dupes found).
10. **GoDaddy sparse indexed content** — confirmed by F6 (Oxford Lawn has 2 indexed pages, high-quality content in both).
11. **Single-service Bento variant** — confirmed by F6 (adapted 1 featured + 4 standard grid for Oxford Lawn's one-service structure).
12. **Hours mismatch sales ammo** — confirmed by F6 (Oxford Lawn site 9-5 vs Google 8-6).

Drop from v0.7.4 scope: none.
Refine: #4 should explicitly include non-boolean credential fields (years-in-business, license number, etc.) since the same inflation class applies.

# Phase 3B: New Findings

### Finding #13 — Tap-target size fails systemically across every flagship
**Evidence.** F1 29% · F2 29% · F3 40% · F4 27% · F5 25% · F6 25% of interactive elements meet WCAG 44×44px minimum on mobile (375px viewport). Consistent pattern: footer link lists, social icons, nav dropdown items, FAQ summary chevrons, testimonial-card interior links all under-size. Not a single-build anomaly.
**Proposed patch.** Phase 6 check 15 expansion: measure every `<a>`, `<button>`, `<summary>` at 375px viewport and fail the build if more than 10% are under 44×44. css-framework.md additions: minimum `padding: 10px 14px` on footer `<li>` `<a>`, `min-height: 44px` on FAQ `<summary>`, increase social icon buttons from typical 32px to 44px.
**Priority.** ship-in-v0.7.4.

### Finding #14 — Hero visual has no alt text because hero slides use CSS background-image
**Evidence.** All 6 flagships render hero photos via `background-image: url(...)` on `<div class="hero-crossfade-slide">` or equivalent. F1 has zero `<img>` tags on the entire homepage. F2–F6 have 2–3 `<img>` tags each (logo + 1–2 others), not the hero content. Screen readers, AI crawlers, and social-share scrapers get no scene description from the visually dominant hero. Present on all 6.
**Proposed patch.** hero-patterns.md: require `aria-label` on each `.hero-crossfade-slide` describing the scene (e.g. `aria-label="Custom in-ground pool with travertine deck at golden hour"`). Alternative: add a visually-hidden `<p>` inside `.hero-crossfade-slideshow` listing the scenes. Phase 6 new check: every background-image hero slide must have either `aria-label` or an associated visually-hidden description. Pull the description text from the same alt text the gallery already uses for the same photo.
**Priority.** ship-in-v0.7.4.

# Phase 3C: Skill Maturation Timeline

F1 to F6 is a step-function improvement that clusters at two inflection points. F1 → F2 → F3 is the first era: single LocalBusiness schema block, no skip-link, no FAQPage, no inner-page anchor photos, no hash dedupe, pre-Hotfix-10 CSS. F4 → F5 → F6 is the second era: LocalBusiness + FAQPage + BreadcrumbList schemas, skip-link fixed via hotfix-10, anchor photos on inner pages (F5 onward), hash dedupe running in Phase 3 (F6 preemptive), anti-slop rules expanded. The maturation is clearest on SEO completeness (100% schema/sitemap/robots/llms coverage across all 6, but schema depth only in F4+), on mobile presentation (F1's broken nav phone and F2's 44px overflow are the only two shipped mobile-break defects in the fleet, both from era-one), and on brand coherence (era-two palettes feel intentional; era-one palettes on F1/F2 fight their copy). Where the skill is still weakest: tap-target sizing is a fleet-wide failure that survived every era, hero content has zero semantic alt coverage on every flagship, and the human eye-test gate that caught F5's services.html bug still isn't an automated check. v0.7.4 should close prevention gaps (hash dedupe as hard rule, anti-slop pre-write, heading hierarchy depth, tap-target enforcement, hero aria-label, evidence-density threshold). A v0.8 retrofit pass should backport hotfix-10 + FAQPage schema + skip-link + anchor photos + gallery page to F1/F2/F3 so the fleet stops reading as two eras.

---

End of audit. No patches applied. v0.7.4 patch cycle begins after Ron's review.

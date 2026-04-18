# Visuals

Screenshots from the live design project at 1280–1440px desktop widths. Each image is a full-page capture of the page that hosts the pattern.

## Files

### Round 1 additions (post-founder-review)

- `q1-typographic-classes-desktop.png` — **Three headline systems, one voice engine.** Class A (Editorial, Oxford-live), Class B (Operations-forward, fleet archetype), Class C (Emergency-urgent, storm-response archetype). See live page: `typographic-classes.html`.
- `q2-soil-references-desktop.png` — **Three ceiling references for the annotated cross-section.** Field-manual diagram · painterly strata plate · blueprint / engineering section. Concept only, stamped not-production. (Reference C "Wardian-case / terrarium" was killed during founder review — Oxford does core aeration but doesn't collect display samples, so the motif implied a practice they don't have.) See live page: `soil-cross-section-references.html`.

### Original Round 1 library

- `00-library-overview-all-22-patterns-desktop.png` — the library view. Every pattern card in isolation, with scale / mobile / voice chips. **The primary visual reference** — every pattern in the dossier maps to a card on this page.
- `applied-site-home-desktop.png` — Home. Hosts: editorial-metadata-rail, stat-row-editorial, voice-tagged-sections, service-area-ledger-dark, trust-band-marquee, soil-strata-hero, dropcap-editorial-prose.
- `applied-site-services-desktop.png` — Services. Hosts: numbered-service-cards, counter-list-what-we-dont-do, voice-tuned-counter-list.
- `applied-site-process-desktop.png` — Process. Hosts: interactive-process-stepper, annotated-soil-cross-section.
- `applied-site-about-desktop.png` — About. Hosts: timeline-ledger-dark, pull-quote-founder, dropcap-editorial-prose, photo-portraits-degrading.
- `mobile-compositions-home-services-contact.png` — Home / Services / Contact at 402px, side-by-side in phone frames. Demonstrates every mobile behavior called out in the spec cards.

## Pattern → primary visual map

| Pattern | Primary visual |
|---|---|
| editorial-metadata-rail | applied-site-home-desktop, applied-site-about-desktop |
| stat-row-editorial | applied-site-home-desktop |
| voice-tagged-sections | 00-library-overview (and every applied page) |
| service-area-ledger-dark | applied-site-home-desktop |
| numbered-service-cards | applied-site-services-desktop |
| interactive-process-stepper | applied-site-process-desktop |
| timeline-ledger-dark | applied-site-about-desktop |
| trust-band-marquee | applied-site-home-desktop |
| counter-list-what-we-dont-do | applied-site-services-desktop |
| review-masonry-rhythm | 00-library-overview (row 10) |
| before-after-slider | 00-library-overview (row 11) |
| filterable-gallery-tagged | 00-library-overview (row 12) |
| chip-selector-form | mobile-compositions (Contact column) |
| dropcap-editorial-prose | applied-site-home-desktop, applied-site-about-desktop |
| soil-strata-hero | applied-site-home-desktop |
| serif-display-headline-system | every applied-site-*-desktop |
| annotated-soil-cross-section | applied-site-process-desktop |
| pull-quote-founder | applied-site-about-desktop |
| magazine-issue-chrome | applied-site-home-desktop |
| review-theme-index | 00-library-overview (row 20) |
| photo-portraits-degrading | applied-site-about-desktop |
| voice-tuned-counter-list | applied-site-services-desktop |

## Mobile variants

All mobile behavior is demonstrated in `mobile-compositions-home-services-contact.png`. The three phones cover every pattern that ports to narrow widths and every narrow behavior noted in the spec cards.

Gated patterns (no mobile variant shipped in Round 1):
- `interactive-process-stepper` — mobile component TBD (horizontal chip + scroll-snap)
- `soil-strata-hero` — uses compact strata chip rail on Home mobile
- `annotated-soil-cross-section` — mobile variant TBD (stacked callouts, no arrows)

## Note

These are page-level captures, not per-pattern crops. The library view is the per-pattern isolation reference. If Code wants per-pattern crops, the library-overview image can be sliced deterministically by `.lib-row` — each row is 22 patterns × ~320px tall.

# Round 1 · Pattern Index

22 patterns from the Oxford Lawn ceiling concept.

## Summary by scale

| Scale | Count | Patterns |
|---|---|---|
| **Systemizable** | 14 | patterns 01–14 |
| **Bespoke** | 5 | patterns 15–19 |
| **Mixed** | 3 | patterns 20–22 |

## Priority ranking (build order for v0.8)

### Tier 1 — Land first (systemizable, high-leverage)
These are the highest-ROI patterns. They ship unchanged across all 50 future contractor builds.

1. **Editorial metadata rail** — `editorial-metadata-rail`
2. **Four-number editorial stat row** — `stat-row-editorial`
3. **Voice-tagged sections (eyebrow system)** — `voice-tagged-sections`
4. **Service-area ledger table (dark)** — `service-area-ledger-dark`
5. **Numbered horizontal service cards** — `numbered-service-cards`
6. **Interactive process stepper** — `interactive-process-stepper`
7. **Editorial timeline ledger (dark)** — `timeline-ledger-dark`
8. **Saturday Morning trust band marquee** — `trust-band-marquee`

### Tier 2 — Land second (systemizable, trade-conditional)

9. **Counter-list · what we don't do** — `counter-list-what-we-dont-do`
10. **Masonry review wall with rhythm** — `review-masonry-rhythm`
11. **Before/after compare slider** — `before-after-slider`
12. **Filterable gallery with trade tags** — `filterable-gallery-tagged`
13. **Chip-selector assessment form** — `chip-selector-form`
14. **Dropcap + editorial prose** — `dropcap-editorial-prose`

### Tier 3 — Ship with their systemizable path (bespoke)
Each of these has a Round-1 path attached. Build the pattern AND the investment plan.

15. **Soil-strata motif hero column** — `soil-strata-hero`
16. **Serif-display editorial headline system** — `serif-display-headline-system`
17. **Annotated soil cross-section** — `annotated-soil-cross-section`
18. **Pull-quote with founder attribution** — `pull-quote-founder`
19. **'Volume 18, Issue 1' editorial chrome** — `magazine-issue-chrome`

### Tier 4 — Mixed (structure first, content pipeline second)

20. **Review theme index (NLP-derived)** — `review-theme-index`
21. **Portrait / work-in-progress photo (degrading)** — `photo-portraits-degrading`
22. **Voice-tuned 'what we don't do' content** — `voice-tuned-counter-list`

## Dependencies

These patterns have a build order constraint:

- `editorial-metadata-rail` **must land first**. It is the structural spine of every page. 7 other patterns sit inside its grid.
- `voice-tagged-sections` must land before any bespoke-copy pattern (pull-quote-founder, counter-list-what-we-dont-do, voice-tuned-counter-list).
- `interactive-process-stepper` desktop variant must land before the mobile variant. Mobile variant is a separate component.
- `review-masonry-rhythm` must land before `review-theme-index` — the theme index lives under the masonry on the Reviews page.
- `photo-portraits-degrading` ingestion pipeline should land early; 6 patterns rely on it.

## Mobile gating

Three patterns need mobile variants built as separate components:

- `interactive-process-stepper` → horizontal chip bar + scroll-snap panels
- `soil-strata-hero` → compact strata chip rail
- `annotated-soil-cross-section` → stacked callouts, no arrows

## Voice audit (Round 1 addendum)

Every section tagged. Closing Table (14) carries thesis/services/process spine. Front Porch (5) quarantined to About + Home about-moment. Saturday Morning (7) handles trust bands, transitions, forms. No blending within a section. Full table in `/library.html#voice-audit`.

## Font audit (Round 1 addendum)

Three families. All load-bearing.

| Family | Role | Keep? |
|---|---|---|
| Newsreader | Display / headlines / dropcaps / quotes | ✓ |
| Public Sans | Body / form inputs | ✓ |
| JetBrains Mono | Eyebrows, rail, nav, stats, tables, trust band, form labels, footer — 17+ components | ✓ |

Public Sans Medium considered as mono replacement. Declined — flattens three-tier hierarchy to two.

## Open questions for Ron — **answered**

Round 1 review resolved all five. Full log: `DECISIONS.md`.

1. **Trade-class typographic system** → **shipped.** Three classes: Editorial (Oxford, live), Operations-forward (sketch, fleet archetype), Emergency-urgent (sketch, storm-response archetype). See `/typographic-classes.html`.
2. **Commissioned illustration pack** → **no commission.** Three ceiling references produced (A field-manual, B painterly plate, D blueprint). Reference C — Wardian-case — killed: Oxford does core aeration but doesn't collect display samples. See `/soil-cross-section-references.html`.
3. **Review-theme NLP pipeline** → ships from Code side, post-sales-kickoff. No design action. Pattern 20 ships as-is.
4. **Voice-interview onboarding** → stays founder-led for first 5 clients. "Voice-interview UI concept" moved to Round 2/3 backlog.
5. **Premium-tier feature flag** → Pattern 19 ships as-designed, flagged `Premium-tier-concept`. SKU decision deferred.

## Delivery

Zipped as `design-round-1-oxford.zip`. Drop into a Claude Code session with the build prompt from README.md.

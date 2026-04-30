# Prose Rules (§6) — for the executing Claude

These are the rules the executor applies when writing `prose.json` for a given
profile. One batched pass per page — think through all five slots before
committing, so the voice stays consistent across the page.

**Temperature guidance (option-b, executor pass):** default creative mode for
§6.1 through §6.3 and §6.5. Push more for §6.4 (manifesto) — that's the slot
where the page earns its personality.

**Output:** a single `prose.json` with five page-keyed top-level keys (`homepage` / `about` / `services` / `testimonials` / `contact`). The engine reads each page's prose from its own sub-dict — **including the homepage**; nothing about the prose is shared across pages at runtime. Author voice register can shift page-to-page if voiceMap §6 mapping says so, though for most prospects all five pages stay in the same register as the homepage.

**Schema confirmation (Deliverable 3 corrected, 2026-04-28).** Empirical test against `render.py` confirmed `ctx["prose"]` is set to `prose.get("homepage") or {}` at the homepage band-renderer entry point (`render.py` L2700 + L2872). All homepage slots — `h1`, `hero_kicker`, `hero_eyebrow`, `subhead`, `services_eyebrow`, `services_headline`, `testimonials_eyebrow`, `testimonials_headline`, `story_headline`, `story_lede`, `story_paragraphs`, `story_caption_*`, `story_img_alt`, `manifesto`, `service_taglines`, `pullquote`, `footer_tag`, `stats_band`, `faq_header`, `promo_callout`, `cta_band` — live under `prose.homepage.*`. `fixture-contract.md` §4 (the legacy v0.8-monolith-era flat schema) is preserved as a migration reference for v0.8 prospects whose prose.json was authored against the inline-generation path; v1.0 prospects author against the page-keyed shape below.

```json
{
  "homepage": {
    "h1": { "line1": "Excellence", "line2_italic": "is a", "line2_accent": "Lifestyle." },
    "hero_kicker": "Welcome home.",
    "hero_eyebrow": "Summerfield Florida · Est. Studio",
    "subhead": {
      "text": "A high end landscape {em}design build{/em} studio serving The Villages, Ocala, and Marion County &mdash; unique high end materials, award winning craft.",
      "em_phrase": "design build"
    },
    "services_eyebrow": "THE CRAFT",
    "services_headline":     { "text": "...", "em_phrase": "...", "accent_word": "..." },
    "testimonials_eyebrow": "FROM THE NEIGHBORS",
    "testimonials_headline": { "text": "...", "em_phrase": "...", "accent_word": "..." },
    "story_headline":        { "text": "...", "em_phrase": "...", "accent_word": "..." },
    "manifesto": {
      "headline": "We compose places. People stay in them.",
      "body": "Designed locally. Installed in-house. Maintained for years."
    },
    "service_taglines": [
      { "service_slug": "outdoor-living", "tagline": "Be the talk of the town year round with a patio and fire pit of your dreams." }
    ],
    "story_lede": "Unique high end materials, up to date on trends and methods. Award winning. A company that cares.",
    "story_paragraphs": ["Jason and Danielle Schmidt founded the studio...", "We train our team members each week..."],
    "story_caption_label": "Marion County · Residential",
    "story_caption_value": "A bench, a border, a place to sit at dusk.",
    "story_img_alt": "Studio team photo",
    "pullquote": {
      "quote": "Lost count of the people who have asked who did my landscaping and how great it looks.",
      "attribution_name": "Finallyfree",
      "attribution_context": "Talk Of The Villages Forum"
    },
    "footer_tag": "Excellence is a Lifestyle.",

    "stats_band":    { "eyebrow": "...", "title": "..." },
    "faq_header":    { "eyebrow": "...", "title": "..." },
    "promo_callout": { "eyebrow": "...", "headline": "...", "sub": "...", "cta": "..." },
    "cta_band":      { "eyebrow": "...", "headline": "...", "body": "...", "primary_label": "...", "secondary_label": "..." }
  },
  "about":         { "eyebrow": "...", "headline": {...}, "subhead": "...", "lede": "...", "story_paragraphs": [...], "story_img_alt": "...", "story_caption_label": "...", "story_caption_value": "...", "creds_lede": "...", "where_we_work": "...", "pullquote": "..." },
  "services":      { "eyebrow": "...", "headline": {...}, "subhead": "...", "overview_eyebrow": "...", "overview_title": "...", "overview_subtitle": "...", "detail_section_eyebrow": "...", "detail_section_title": "...", "service_detail_descriptions": [{...}, ...], "faq_header": { "eyebrow": "...", "title": "..." }, "faq": [{...}] },
  "testimonials":  { "eyebrow": "...", "headline": {...}, "subhead": "...", "site_section_title": "...", "google_section_title": "...", "pullquote_quote": "...", "pullquote_attr": "..." },
  "contact":       { "eyebrow": "...", "headline": {...}, "subhead": "...", "form_intro": "...", "form_lede": "...", "info_heading": {...} }
}
```

The engine uses these exact keys. Sections §6.1–§6.5 below define the homepage slot rules (which apply to all slots under `prose.homepage.*`); section §6.6 defines the inner-page slot rules.

**Note on additional homepage slots surfaced at Deliverable 3 verification:** `services_eyebrow`, `testimonials_eyebrow`, and `cta_band` are read by render.py but were not present in prior master examples. They are added here as canonical homepage slots; voice register and authoring rules follow voiceMap.md §6 (LABEL discipline for the eyebrow strings, §6.4 declarative-register rules for `cta_band` shape).

**Note on the `footer_tag` slot:** prior versions of this example used `porch_tag`. The engine reads `footer_tag` (`render.py` `render_footer` at L1590); `porch_tag` was a stale legacy name. Reconciled at Session 1 of v1.0 rewrite (Deliverable 3, 2026-04-28).

**Slot-shape conventions for inline-em display surfaces (v1.1 Session 1, 2026-04-30).** Display-headline-class slots emit through `_resolve_inline_em_text(value, wrap_class=None)` in `render.py`, which is shape-tolerant: it accepts either the em-phrase **dict shape** `{ "text": "...", "em_phrase": "..." }` OR a **string shape** with optional inline `<em>...</em>` or `{em}...{/em}` shorthand. Engine behavior is identical in either authoring direction; the resolver also guards against **double-wrap** (when the input text already contains `<em>` or `<span class="em-word">` markup, the em_phrase wrap step is skipped — pre-Patch-5 emit shipped nested wraps when an author included inline markup AND set `em_phrase` pointing at the same span).

The four call sites (and their canonical authoring shape, which authors should default to):

| Slot                                       | Page     | Canonical shape | Wrap class       |
|--------------------------------------------|----------|-----------------|------------------|
| `homepage.subhead`                         | homepage | dict            | `em-word`        |
| `homepage.cta_band.headline`               | homepage | string          | bare `<em>`      |
| `contact.info_heading`                     | contact  | dict            | bare `<em>`      |
| `contact.form_intro`                       | contact  | string          | bare `<em>`      |

The dict ↔ string equivalence is a render-time safety net; the per-slot canonical shape above is what §6.3 / §6.6 voice rules are written against. Author against the canonical shape; rely on the safety net only when migrating existing prose.json files between shapes.

**Engine-extension item #6 (post-Deliverable-3 correction):** Existing v0.8-era prose.json files (Volthom, F1-F8 flagships) are in the legacy flat shape and require migration to page-keyed before render.py produces non-fallback output. Migration is mechanical: wrap homepage slots under a `homepage` sub-key. Affects Session 2 Volthom validation — see Session 2 prompt for disposition options.

## §6.1 H1 hero headline

Two lines. Line 1 is roman, a single weighty noun or short phrase. Line 2 is
italic + roman mixed, ends with a period.

**Rules:**
- 5-10 words total across both lines
- End with a period, NEVER an exclamation
- Line 1: roman, uppercase-first, usually a noun. Examples: `Excellence`, `Forty Years`, `Built Right`, `Every Door`, `Rooted`.
- Line 2: starts with italic phrase (prep/article/short verb), ends with the "accent" word (gets the rust underline animation).
- The "accent word" in line 2 is always italic AND has the underline — the engine wraps it in `.accent-word`.
- Use the captured tagline verbatim if it fits the 2-line shape; otherwise extract the idea and reshape.

**Reference (JSL):**
```
Excellence           ← line 1, roman
is a Lifestyle.      ← "is a" italic, "Lifestyle." gets accent underline
```

**Trade variations to work from:**
- Roofing with 40 years history: "Forty Years / on the same route." (roman / italic-accent)
- Electrical family business: "The Panel / you only call once." (roman / italic-accent)
- Family landscape nursery: "Planted / on the same corner." (roman / italic-accent)
- Pool builder: "Still Water / for the whole family." (roman / italic-accent)

## §6.2 Hero subhead

One sentence. 18-26 words. Cormorant Garamond. One phrase italicized (the
discipline name or differentiator). Em-dash, NOT comma, before the trailing
differentiator.

**Rules:**
- Names what they do + where + a quality marker
- Italic phrase is the discipline name (e.g., "design build", "master electrician", "slate roofing") OR the differentiator ("fourth generation", "24-hour emergency")
- Em-dash separates the trailing differentiator clause
- Exactly ONE em-dash allowed (this is the only place em-dashes appear in the prose)

**Reference (JSL):**
> A high end landscape *design build* studio serving The Villages, Ocala, and Marion County — unique high end materials, award winning craft.

## §6.3 Display headlines (services, testimonials, story)

These are the big italic-weight-contrast section headers. One per band.

**Output shape:** one sentence ending in a period. Must contain:
- Exactly ONE italic-weight-contrast phrase (the engine wraps it in `<em>`)
- Exactly ONE accent-uline word (the engine wraps it in `<span class="accent-uline">`)

**Rules:**
- 6-14 words
- Italic phrase is usually a COUNT or a QUALITY adjective
- Accent word is usually the VERB or the PUNCHLINE
- Must reference a real fact from the band. No "We're the best." Use "Eighty four five star reviews."

**Inner-page exemption.** Display headlines on inner pages (about / services / testimonials / contact subpages) operate under a tightened shape: em_phrase remains required, but the accent_word slot drops AND the 6-14 word range relaxes to 3-7 words. Inner-page surfaces are em-only at shorter word count by canon — examples: `The credentials, <em>named</em>.` (4 words), `Where we <em>work</em>.` (3 words), `From <em>our site.</em>` (3 words), `Each trade, <em>by hand</em>.` (4 words). The shorter form is intentional: subpage-hero treatment doesn't underline a word the way homepage display headlines do, and inner-page emit shapes are structurally different (smaller scale, denser per-band layout). Homepage display headlines bind to the full §6.3 rule set; inner-page display headlines bind to em_phrase only at 3-7 words.

**Sparse-drop vs default-emit.** Two engine behaviors when prose is absent:

- **Default-emit surfaces** carry an engine fallback string. Authors can override; absence falls through to the (register-blessed) default. Engine defaults are register-blessed per LABEL discipline (voiceMap.md §6) and spectacle-wins; do not author "boring but correct" prose to override a register-blessed default — match the register or skip authoring.
- **Sparse-drop surfaces** carry no engine fallback. The h2 (or full section band) drops when prose is absent. Authors must populate the slot to ship the band. The sparse-drop is the engine's signal that this surface requires explicit authoring per prospect — generic engine voice would be louder than helpful here.

When authoring, check the surface in render.py (or this spec) before writing. A sparse-drop surface gets band/element drop on absence; a default-emit surface gets the engine default on absence. Match authoring intent to the surface behavior.

**Reference outputs:**
- Services: "Six disciplines, *one* design studio, one crew that <u>finishes</u> what it starts."
- Testimonials: "Eighty four *five star* reviews. <u>Not one</u> below."
- Story: "We are a *high end* landscape <u>design build</u> company."

Note for the testimonials headline: when rendering, the engine writes the
italic phrase first then the accent-uline phrase. Both can be two-word spans.
The key constraint is exactly one `<em>` and exactly one `.accent-uline` per
display headline — the §7 validator enforces this.

## §6.4 Manifesto register (voice principle — engine band REMOVED at v1.0 close)

**Engine status (Round-2 diagnostic Session 3 close, 2026-04-29):** the
`render_manifesto` band emit was REMOVED from the homepage band sequence
in render.py. The manifesto pattern stays as a voice principle but is no
longer an engine-emitted band on every prospect. Reason: the manifesto
band was a Volthom-arc Phase 5.0c addition that competed with `cta_band`
for the same warmth-surface attention budget. **Engine principle:** the
homepage ships ONE warmth surface, and that surface IS the conversion-
ladder cta_band. Decorative warmth bands degrade conversion.

**Voice principle preserved.** Prose authors who want the declarative
brand-pillar register can express it elsewhere — story_paragraphs,
service taglines, hero kicker — using the §6.4 register rules below.

---



Phase 5.0c (2026-04-26) restyled this band from the heritage italic-poetry
register to a declarative brand-pillar register. The old `.manifesto` was
italic-serif-centered and merged visually with the navy `.pullquote` band
directly above it on the homepage. The new `.manifesto-band` is sans-serif
left-aligned with an optional serif body — a clean rhetorical break from
the voice-of-customer pullquote register.

**Schema:**
```json
"manifesto": {
  "headline": "Short declarative line. Period-terminated.",
  "body":     "Optional supporting line. Period-terminated. Empty string drops the body."
}
```

**Rules — headline:**
- **The voice is the brand, not the customer.** This slot states what
  the company does, who it is, or what the customer gets — in the
  company's own first-person voice. If a sentence could plausibly
  be attributed to a happy customer in quotation marks, it belongs
  in a pullquote slot, not here.
- 1-2 short sentences. Period-terminated. Sans-serif (Figtree 700) at clamp(32-44px).
- Declarative claims, not poetry. The voice of the brand stating who it is /
  what it does / what the customer gets — not the voice of the customer.
- No italic. No quotation marks. No em-dashes. No exclamation points.
- Style reference: The Storefront's "We build it. We host it. We update it.
  You answer the phone." — short claims, period-terminated, declarative.
- Sentence-case (not title-case). Capitalize first word and proper nouns only.
- Direct address ("you ___") is allowed once, as the closing beat,
  to land the customer-implication. Not as the opening voice. The
  Storefront reference does this: three first-person beats, one
  second-person pivot to close.

**Rules — body (optional):**
- Empty string `""` drops the supporting line. Use empty when the headline
  is enough on its own.
- One short sentence OR 2-3 noun-phrase fragments separated by periods.
  Sans-serif (Figtree 400) at 17px.
- Same voice as headline — declarative, brand-statement register.
- 5-12 words.

**Reference (Volthom — current):**
```
headline: "We answer the phone. We finish what we start."
body:     "Master electrician. Licensed and insured. Family-operated."
```

**Trade variations (these are the examples Code will draw on for future prospects):**
- Roofing — `headline: "We protect houses. We honor warranties."` /
  `body: "Licensed. Insured. Three-generation family business."`
- Landscape — `headline: "We design the yard. We come back to keep it."` /
  `body: "In-house crews. Same designer start to finish. Maintenance contracts."`
- Pool service — `headline: "We balance water. We answer Saturdays."` /
  `body: "Weekly routes. Equipment installs. Same crew every visit."`
- HVAC — `headline: "We fix it on the first call. We service it after."` /
  `body: "24-hour emergency. Maintenance plans. NATE-certified techs."`

Pattern: declarative claim + period + declarative claim + period. The body
is a rhythm of credentials/practices/promises in the same brand-voice
register, not customer voice.

**What this slot is NOT:**
- **An italic-poetry strip.** This is the specific defect Phase 5.0c
  corrected. If the headline reads as poetry — line breaks for cadence,
  abstract verbs ("we craft," "we honor," "we carry") without an
  object — rewrite. Manifesto headlines name what the company does,
  in plain language, with periods.
- A pullquote (those are voice-of-customer, italic, attributed — see §6
  pullquote slots, separate)
- A tagline (one-line, no body — see `porch_tag`)
- Marketing copy. Brand-statement, not feature-list.

**Engine note:** `prose.manifesto.body` is optional but `prose.manifesto.headline`
is required for the manifesto-band to render. Empty/missing headline drops
the band entirely. The renderer at `render_manifesto` enforces this. The
manifesto-eyebrow defaults to "THE PROMISE" and is overridable via
`prose.manifesto.eyebrow` (Phase 6.0b).

**System-wide accent budget (applies to §6.3 display headlines + §6.6
inner-page headlines, not just §6.4):** italic-amber `<em>` accent words
inside Cormorant headings make the system feel editorial. They overuse
fast — three accents on one short page reads as decoration, not emphasis.
**Cap: one accent per section, max two per page.** When a page is shorter
than its peers (e.g. Contact), prefer fewer. When a page is longer (e.g.
About), one per section is plenty. The accent should always emphasize the
single word that earns it — the brand-truth word, the verb, the proper
noun — not whichever word looks pretty in italic. (Phase 6.0b — Design
audit Q2.)

## §6.5 Service tile italic taglines

One per service. Italic Cormorant line, 6-14 words, under the description,
separated by a hairline rule.

**Rules:**
- Use the audited tagline VERBATIM if the audit captured one for that service.
  The reference JSL uses "Be the talk of the town..." verbatim from the
  Villages Landscaping audit.
- If no audit tagline exists, compose a tagline that names the *experience* of
  the service, not the *deliverable*. 
  - Wrong: "We install landscape lighting with care."
  - Right: "The hours after sunset are when a garden earns its keep."
- No exclamation marks
- Pattern: a small image, a small claim, a small period

**Reference (JSL, partial):**
- Outdoor Living: *"Be the talk of the town year round with a patio and fire pit of your dreams."* (verbatim from audit)
- Water Features: *"Still water, moving water, a garden at rest."* (composed)
- Lighting: *"The hours after sunset are when a garden earns its keep."* (composed)

## Voice consistency rules (apply across all five slots)

These rules apply equally to **authored prose** in `prose.json` and to **engine-derived copy** produced by `resolve_*` helpers in `scripts/render.py` (FAQ answers, stats labels, promo callout copy, anything else the engine composes into customer-facing strings). A future resolver that emits a string is bound by these rules by default — there is no separate "engine voice"; engine output is voice.

- **No em dashes** except the §6.2 hero subhead. This is the hard house rule.
- **No corporate filler**: no "passionate about", "dedicated to", "committed to excellence", "value proposition", "one-stop shop", "your trusted partner", "leverage", "synergy", "stakeholders".
- **No manufactured warmth**: no exclamation points, no ellipses used for drama, no em-dashes-to-sound-conversational.
- **Specific nouns over categories**: "a patio and fire pit" beats "outdoor features". "Eighty four reviews" beats "many happy customers".
- **Real place names**: "The Villages, Ocala, Marion County" — never "our community".
- **Owner names are real**: if the owner is Jason Schmidt, call him Jason Schmidt, not "the owner".

## §6.6 Inner-page prose slots (about / services / testimonials / contact)

**Drift-prevention note (Session 2 close, 2026-04-28):** Engine defaults at several §6.6 surfaces ship richer than the spec examples below. Walkers reading deployed-Volthom (or other v0.8-era references) for these surfaces should validate against current `render.py` defaults, not against deployed text alone. Examples updated in this section reflect v1.0 engine behavior; the close-package-framing-inheritance failure mode (deployed v0.8 text carrying pre-spectacle-wins cleanliness-instinct artifacts) is the precedent this note prevents from recurring.

**Page-hero eyebrow + lede defaults (Session 2 spec-defect F1 codification):** `_resolve_page_hero_eyebrow_default(page_key, ctx)` and `_resolve_page_hero_lede_default(page_key, ctx)` in render.py ship register-blessed defaults for every inner page. Eyebrows: wayfinding constants per voiceMap.md §6 LABEL discipline (`HOW WE GOT HERE · SINCE {founding_year}` / `THE CRAFT · {SPELLED_COUNT} SERVICES` / `FROM THE NEIGHBORS · {REVIEW_COUNT} REVIEWS` / `VISIT · {CITY_STATE}`) with sparse-drop at qualifier interpolation level. Ledes: three-parallel-clause Closing Table register with profile-interpolation at clause-1 and em-italic locative-relational pivot at clause-3 — the where-pivot is the engine's signature register move at default-emit ledes. Both helpers fire only when `prose_page.headline.text` is present (per-prospect identity gates the page-hero band; band sparse-drops when h1 absent — no broken empty shells on fresh prospects).

Each inner page lives at a top-level key in `prose.json`. The §6.1–§6.5 rules
still apply within each page (§6.3 display headlines, §6.4-style fragmentary
poetry where it appears, voice consistency); the inner pages add their own
slot vocabulary.

Inner-page slots are classified by structural class and by voice register
per voiceMap.md §2. **Lede slots** split into two classes: **page-ledes** do
one job — frame the whole page in one sentence; word-count range 12-22.
**Section-ledes** do three jobs — frame a sub-section header above,
establish the section's central claim, set up the content block below;
word-count range 16-22, floor lifted because three jobs need more room
than one. Display-headlines, eyebrows, captions, attribution surfaces, and
section bodies have their own structural classes governed by §6, §6.3, and
voiceMap.md §6 spectacle-wins. Each slot below names its structural class
and voice register; where register inherits from page voice rather than
carrying its own, the inheritance is named.

**Shared across all four inner pages:**
- `eyebrow` — uppercase tracked label, ~3-6 words. Pattern: `"{LABEL} · {QUALIFIER}"`. Lives above the subpage hero headline. Examples: `"HOW WE GOT HERE · SINCE OCALA"`, `"THE CRAFT · SIX SERVICES"`, `"FROM THE NEIGHBORS · 199 REVIEWS"`, `"VISIT · OCALA, FL"`. Real qualifier (review count, location, service count) — never generic.
- `headline` — display-headline shape `{ "text": "...", "em_phrase": "..." }`. The §6.3 rules apply: 6-14 words, exactly one italic phrase. Inner-page headlines can drop the accent_word slot (subpage-hero treatment doesn't underline a word the way homepage display headlines do).
- `subhead` — one sentence, 18-32 words, plain string (not the homepage subhead-object shape). Sets the page premise. No em-dashes outside the subhead's own ID-marker.

**Register for shared slots inherits from page voice per voiceMap.md §2.** Example: services-page eyebrow/headline/subhead carry Closing Table on signature services, Saturday Morning on operational services. The display-headline `em_phrase` is voice-blessed per voiceMap.md §6 spectacle-wins regardless of inherited register.

**About:**

- `lede` — **page-lede.** One sentence, 12-22 words. **Closing Table register** — opens the page in credentialed framing. Functions as §6.3 lede. Often a verbatim or near-verbatim copy of homepage's `story_lede`.

- `story_paragraphs` — array of 3-5 paragraphs. **Front Porch register** — names the human beings doing the work, second-person warmth, sacred lines stay sacred per voiceMap.md §2c. Order: founder → method → crew → what-you-get.

- `story_img_alt` — alt text for the portrait image. Brief descriptive sentence, 8-15 words. Names the subject and the visible context. Functional copy — accessibility surface, not voice-bearing.

- `story_caption_label` — caption label paired with the portrait. Mono eyebrow surface — uppercase tracked, ~1-3 words (e.g., "Founder", "Owner-operator"). Spectacle-wins binds: mono register per voiceMap.md §6 spectacle-wins.

- `story_caption_value` — caption value paired with `story_caption_label`. Display face, weight 400, ~1-4 words (typically the owner's name). Spectacle-wins binds: display-face attribution per voiceMap.md §6 spectacle-wins.

  **Photo-context binding discipline (P14, Phase 0.5 close 2026-04-29).** The story-grid portrait priority chain is `ownerPortrait → teamIdentity → site-04 → sparse-drop` (render.py L2299-2320). When `ownerPortrait` is absent, the engine falls through to `teamIdentity` (crew + branded apparel + customer/context shots). The caption fields must reflect the photo that was actually selected, not the photo that was assumed at authoring time. Authoring person-named caption ("Member / Joel Testerman") against an absent owner-portrait while the engine binds a team-identity photo cross-contaminates the slot — the photo overlay names a person who isn't in the photo. Cleanest discipline: when the prospect lacks a confirmed `ownerPortrait`, default the caption to register-blessed photo-context-agnostic phrasing (location-anchored or work-anchored, never person-named). Examples that pass: `"On The Trucks" / "Twenty-five years."` (locative LABEL + time anchor), `"South Lake County" / "Family business."` (place + identity). Engine corollary v1.1: caption defaults derived from the photo source actually selected, with prose override available — tracked as P14 engine-extension backlog item.

- `creds_lede` — **section-lede.** One or two sentences, 16-22 words. **Closing Table register** — frames the cred-grid below in public-record, plain-stated credentialing voice per voiceMap.md §2a "Credentials stated plainly." Sets up 4-6 cred cells (License, Insurance, Award, Affiliation, Reviews, Experience). Sparse-drops with the cred-grid section when no cred-cells resolve.

- `where_we_work` — **section-lede.** One or two sentences, 16-22 words. **Closing Table register** — frames the where-we-work section below in coverage / service-area trust-carrying voice. Names places concretely per voiceMap.md §2b "Specifics, not abstractions."

- `pullquote` — single string, 12-24 words. **Voice-pivot register: Closing Table frame, featured-pullquote display-italic body, per voiceMap.md §3 + §4.** A voice-pivot pullquote lifts the about-page from the credentialed-and-named register of the story-grid into something more reflective — a single italic Fraunces line at clamp display scale, thin top/bottom borders, mono attribution. **Engine emit pending — render_about_page does not currently consume this slot. Tracked as B5 engine-extension item.**

**Services:**

- `overview_eyebrow` — caption-strip eyebrow above the bento-grid overview. **Spectacle-wins binds:** mono register per voiceMap.md §6 spectacle-wins. Engine default `"THE WHOLE SHOP"` (Session 1 B3 Step 3 wayfinding chain — homepage `THE CRAFT` → services overview `THE WHOLE SHOP` → services detail `ON THE BENCH`).

- `overview_title` — display-headline above the bento grid. 3-7 words with one em_phrase per §6.3 inner-page exemption (L112). **Closing Table register** — frames the at-a-glance view in trust-carrying voice. **Spectacle-wins binds:** display-headline em-only per §6.3 inner-page exemption; `accent_word` slot drops at inner-page surfaces per L112. Engine default `"Every trade, on <em>one page</em>."` (Session 2 evolved richer than v0.8 documented `"Everything we do, on one page."`).

- `overview_subtitle` — section-lede below `overview_title`. One sentence, 16-22 words. **Closing Table register** — frames the bento grid below in scannable summary voice. The only sentence in the overview cap-stack.

- `detail_section_eyebrow` — caption-strip eyebrow above the per-service detail blocks. Same shape as `overview_eyebrow`. **Spectacle-wins binds:** mono register. Engine default `"ON THE BENCH"` (Session 1 B3 Step 3 wayfinding chain — homepage `THE CRAFT` → services overview `THE WHOLE SHOP` → services detail `ON THE BENCH`).

- `detail_section_title` — display-headline above the per-service detail blocks. Same shape as `overview_title` (3-7 words, em-only per §6.3 inner-page exemption). **Closing Table register.** **Spectacle-wins binds:** display-headline em-only per §6.3 inner-page exemption (L112); `accent_word` slot drops at inner-page surfaces. Engine default `"Each trade, <em>by hand</em>."` (Session 2 evolved richer than v0.8 documented `"Each service, in plain language."`).

- `service_detail_descriptions[]` — one object per service in `profile.services.list`. Same array length, same slug order. **Register varies by service tier per voiceMap.md §2d** (Signature → Closing Table, Operational → Saturday Morning, Distinctive → Front Porch or Saturday Morning+). Each object:
  - `slug` — must match `profile.services.list[i].slug`.
  - `index_label` — `"01 · ELECTRICAL SERVICE & REPAIRS"` (numeric prefix + tracked label). **Spectacle-wins binds:** mono-tracked register per voiceMap.md §6 spectacle-wins.
  - `title` — short verb phrase, ends with period. **Spectacle-wins binds:** display-shape title. Often the same as homepage `service_taglines[i].tagline` since the service identity carries.
  - `description` — 35-70 words. Names what's done, who it's for, why it matters in plain language.
  - `bullets` — 3-5 short noun phrases. Concrete deliverables.
  - `tag` — 2-5 words, the kind of property/job. Examples: `"Older homes · Expanding loads"`, `"Lightning capital priority"`.

**Testimonials:**

- `site_section_title` — h2 display-headline framing the on-site testimonial section. **Spectacle-wins binds:** italic-pair attribution per voiceMap.md §6 spectacle-wins — em italic on the source noun. Engine default `"From <em>our site.</em>"` (Site 7 ratified flagship-canonical).

- `google_section_title` — h2 display-headline framing the Google reviews section. **Spectacle-wins binds:** italic-pair attribution per voiceMap.md §6 spectacle-wins — em italic on the source noun. Engine default `"From <em>Google.</em>"` (Site 7 ratified flagship-canonical).

- `pullquote_quote` — flat string. The single review that gets featured-block treatment per voiceMap.md §4. 12-24 words. **Voice-pivot register: Closing Table frame, featured-pullquote display-italic body, per voiceMap.md §3 + §4.** **Engine emit pending — `render_testimonials_page` does not currently consume this slot. Tracked as B5 engine-extension item.**

- `pullquote_attr` — flat string `"{Name}, {role and/or context}"`. Verbatim from source. **Never fabricate an attribution** (voiceMap.md §14). Mono attribution shape per voiceMap.md §4. **Engine emit pending — paired with `pullquote_quote`. Tracked as B5 engine-extension item.**

*Page-hero metrics (rating, review count, five-star tile) emit as engine-computed `metrics_html` from rating data — not an authored-prose slot. Documented here for completeness; not consumable via `prose.testimonials.*`.*

**Contact:**

- `form_intro` — h2 display-headline above the contact form. Current authored range: 2-4 words ending in period (Examples: `"Send it over."`, `"Tell us about the property."`). **Closing Table register** — frames the form in clear-CTA voice. **Spectacle-wins binds at the surface level** (h2 display-headline shape); §6.3 em + accent binding pending #6 conformance audit. Engine default `"Send a note"`.

  ***§6.3 conformance question:*** *this slot's current authored range (2-4 words) is below §6.3's documented 6-14 word floor for display headlines. Tracked for #6 categorical sweep — disposition pending between (α) lifting word-count to §6.3-conformant range with em_phrase requirement, or (β) adding short-form CTA-style display-headline exemption to §6.3.*

- `form_lede` — one paragraph, 25-50 words. **Closing Table register** — what happens after they submit, what counts as an emergency, what the response window looks like. Plain trust-carrying voice.

- `info_heading` — h2 display-headline above the chassis-data column. 4-8 words with one em_phrase. **Closing Table register** — frames the credentialing-data column in plain voice. **Spectacle-wins binds at the surface level** (h2 display-headline shape); §6.3 em + accent binding pending #6 conformance audit. Sparse-drops when not authored. Example shape mirrors about-page `<h2>The credentials, <em>named</em>.</h2>`.

  ***§6.3 conformance question:*** *this slot's documented word-count range (4-8) is below §6.3's documented 6-14 word floor for display headlines. Tracked for #6 categorical sweep — disposition pending between (α) lifting word-count to §6.3-conformant range with em_phrase requirement, or (β) adding short-form CTA-style display-headline exemption to §6.3.*

  **Dict-shape engine emit (P16, Phase 0.5 close 2026-04-29).** `info_heading` ships as the em-phrase dict shape `{ "text": "...", "em_phrase": "..." }`. The render path must unpack the dict into `<h2>{text-with-em-substituted}</h2>`; emitting the dict directly into an f-string calls `str()` on it and produces raw Python repr in the live HTML (the symptom: `{'text': 'How to reach us.', 'em_phrase': 'reach'}` rendered verbatim inside the `<h2>` on Testerman's contact page). Engine fix landed at render.py L2902 — dict-or-string branching with em-phrase substitution. The bare `<h2>` (no `class="display"`) is intentional: composer-system.css `.contact-info h2` and `.contact-info h2 em` own the italic-accent treatment for this surface; adding `class="display"` would double-style. Render-path corollary: any inner-page slot documented as the em-phrase dict shape (`headline`, `info_heading`) must be unpacked via `_render_display_headline()` or an inline em-substitution branch — never str()'d into a template literal. v1.1 audit-time grep gate (Phase 6) tracked as engine-extension item to catch the symptom class regardless of binding root cause.

The contact-info column (phone / email / address / hours / license) is **chassis data read from `profile.contact` and `profile.credentials`**, not prose. Don't author those; the engine pulls them from the profile.

The contact area-band summary is **chassis data read from `profile`** at the engine level. Don't author it as prose. (Per Design audit, this surface is intentionally abbreviated to single-line summary; the full "Where we work" treatment lives on the about page only.)

## §6.7 FAQ override (services page)

The services page can ship a `<section class="faq-section">` band with 5–7
question-and-answer items. The default behavior is **engine-derived**:
`resolve_faq(profile, prose)` reads `profile.credentials.licenseNumber`,
`profile.contact.serviceAreaCities[]`, `profile.services.list[]`,
`profile.contact.hours`, and `profile.contact.phone`, then composes items in
the order license → service area → service-driven (cap 4) → emergency → quote.
Voice register is hardcoded Front Porch / Closing Table.

**Optional author override.** If `prose["services"]["faq"]` is present and
non-empty, the engine returns it verbatim and skips derivation entirely (it's
all-or-nothing per page — no per-item override). Use the override slot when:

- A prospect's auto-derived FAQ reads flat or generic and you want to hand-tune
  voice.
- The audit captured a service whose `description` is too thin to support a
  credible 1-sentence answer, and you want to write better copy.
- The prospect uses unusual terminology (e.g. "lake-house standby" instead of
  "generator") and you want the questions to match how their customers
  actually ask.

**Schema:**

```json
"services": {
  ...,
  "faq": [
    { "q": "Are you licensed and insured?", "a": "Yes. Florida EC#13006598..." },
    { "q": "What areas do you serve?",      "a": "..." }
  ]
}
```

The longer-key form `{"question": "...", "answer": "..."}` is also accepted —
both shapes read.

**Rules when authoring the override:**

- 5–7 items. Match the §4 dropped-sections.md authorship rule.
- Every answer must be derivable from `profile` data (license, hours, service
  area, services list, founder bio, testimonials). The override is a voice
  seam, not a fabrication seam — universal voice rule §14 (never fabricate)
  still binds.
- Front-porch register: lead with the answer, plain language, second person
  where it earns it. No "We pride ourselves on" or "We are committed to". Give
  the receipt — license number, hours, real city names — not a brand line.
- No exclamation marks. No em-dashes (the §6.2 hero subhead is the only slot
  that gets them).
- If you only need to fix one item's voice, you still must list all the items
  you want shipped — there is no per-item override.

**When the prospect's auto-derivation reads thin and you'd rather not write a
full override**, the structural alternative is to extend the service-keyword
dispatch table (`FAQ_SERVICE_QA` in `scripts/render.py`) so the slug maps to a
question shape that fits the prospect's data. That helps every prospect with
the same slug; the prose override only fixes the one site.

## §6.9 — Phase 3b homepage band slots (stats, FAQ header, promo callout)

**Purpose.** Phase 3b adds four bands to the homepage (stats dark band, FAQ
band, promo callout, before/after) and a universal mobile CTA bar. Three of
those bands have authored copy with stable rule-compliant defaults. This
section is the voice surface for tuning that copy.

All four slots are optional; defaults fire when the slot is absent. All copy
is bound by §6 universals — the rules apply equally to engine-derived defaults
and authored prose (see commit `213da2a`). No em-dashes outside §6.2 hero
subhead, specific nouns over corporate filler, active voice, no exclamation
marks.

### Slot 1 — `prose.homepage.stats_band: { eyebrow, title }`

Header for the dark stats band (4-tile or 3-tile depending on whether
`resolve_distinguishing_stat` fires for the prospect).

- **Default (when absent):** eyebrow `"BY THE NUMBERS"`, title
  `"What the work looks like in numbers."`
- **When to override:** the prospect's distinguishing fact wants a different
  framing — e.g. a heritage-business that wants `"Five Generations" / "What
  the years look like in numbers."` Use the same shape (eyebrow + title);
  keep the title under 12 words.
- **Voice:** neutral declarative. The dark band is a numbers-receipt slot,
  not a sales pitch. No marketing puffery.

### Slot 2 — `prose.homepage.faq_header: { eyebrow, title }`

Header for the homepage FAQ band. The list itself comes from
`ctx["profile"]["faq"]` (the same 5–7 items services-page renders).

- **Default (when absent):** eyebrow `"FAQ"`, title `"Common questions."`
- **When to override:** the prospect's voice register makes "Common questions"
  read flat. A heritage-business might prefer `"Questions we've answered"`
  / `"What folks ask before they hire us."` Keep title under 10 words.

### Slot 3 — `prose.services.faq_header: { eyebrow, title }`

Header for the **services-page** FAQ band — distinct from the homepage so a
back-to-back read doesn't see identical eyebrows + titles.

- **Default (when absent):** eyebrow `"SERVICE QUESTIONS"`, title
  `"What homeowners ask before they call."`
- **Why two slots, not one:** giving services its own slot now is cheaper
  than discovering at Phase 5 that page-distinct copy is needed and
  refactoring then. Both pages render the same FAQ items; only the headers
  differ.
- **Same items, different framing:** services-page copy can lean a touch
  more transactional (`"What we install"` / `"How fast we respond"` ) since
  visitors there are already in service-shopping mode. Homepage copy stays
  closer to first-meeting tone.

### Slot 4 — `prose.homepage.promo_callout: { eyebrow, headline, sub, cta }`

Voice-tuned override for the promo callout band. Only authored when
`profile.promotions.featuredPromo` is non-null — the profile carries the
data + dates, prose carries the voice.

- **Default behavior (when absent but `featuredPromo` present):** the engine
  copies the profile's `featuredPromo.eyebrow / headline / sub / cta`
  strings verbatim into the rendered band. Workable but flat.
- **When to override:** the audit captured the promo as a literal seasonal
  offer (`"Hurricane Season Generator Special!"`) and you want it to read
  in the prospect's house voice. Rewrite while keeping the dated facts —
  date range, price, scope — intact. Voice tuning, not fact tuning.
- **Voice constraints:**
  - No exclamation marks. The seasonal-urgency reflex pushes one in; resist.
  - Headline ≤ 9 words.
  - `sub` is one sentence, the why-now context.
  - `cta` is the button label only ("Call (352) 789-2454" or "Book the
    walk-through"). The href the engine wires to (tel: vs #contact) is
    derived from whether `cta` contains digits; you don't write the href.

### What is NOT a §6.9 slot (do not author)

- The mobile CTA bar copy. Engine-only — `Call {phone}` and `Get a Quote`.
  No prose seam. If a prospect needs a different secondary label than "Get
  a Quote", that's an engine change, not a prose change.
- The before/after band. Phase 3b ships the gate as a stub; full markup +
  CSS land at Phase 5 with the first prospect that has paired photos.
  No prose surface yet.
- The stats tile values themselves (199, 5.0★, 30+, 0). Derived by
  `resolve_stats_trio` and `resolve_distinguishing_stat` from profile data;
  prose tuning happens to the stats-band header, not the tile labels.

## Output consistency check before handing back

Read the full prose.json out loud once. It should sound like one writer wrote
one site about one business. If the homepage reads like a studio and the
manifesto reads like a law firm, rewrite the manifesto. The same check applies
across pages — if the about page voice diverges from the homepage voice, the
prose is wrong.

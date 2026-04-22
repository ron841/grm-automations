# voiceMap.md

Voice-map authority for the prospect-site-composer skill. Loaded by Phase 4 during composition-plan authoring (to resolve voice per zone with persona bias applied) and by Phase 5 before generating any copy in any zone (to state voice out loud per zone and author against register discipline). Paired with `typography.md`; where that document covers the mechanics of type and role classes, this one covers how voice distributes across a page and how the five emotional personas bias that distribution.

Stage II (d) three-way merge output — production baseline (Composer's pre-merge register-theory file) × Design in-flight (`composer-stage-ii-typography-source/voiceMap.md`, zone-to-voice table with persona bias) × this merged file. Revision log at the bottom enumerates all twelve resolved Stage II (d) conflicts; five land in voiceMap.md (A2, C1, C2, C3, C6).

---

## 1. Why this file exists

A site has more than one voice. A homepage that speaks in a single voice from hero to footer reads as corporate. A site with a voice map reads as *inhabited* — different parts of the page are authored by different registers, and the reader feels the shifts before they can name them.

Before v0.7.2, voice mapping lived inside `content-rules.md`, alongside headline patterns, CTA templates, service description structures, FAQ templates, and house formatting rules. That file was doing two jobs: defining *how each voice sounds* and defining *what specific patterns each voice produces in specific contexts*. The two jobs have different audiences — Phase 4/5 looking up "which voice does this specific zone use" versus Phase 5 looking up "what's the structure of a hero headline in Closing Table voice."

Separating them makes both files easier to reason about. `voiceMap.md` owns the zone-to-voice mapping, the voice definitions themselves, the persona-bias rules, the register-coupling discipline that spans beyond typography, and the specific composition patterns (anchor strip, featured pullquote, Front Porch footer, three-tier service composition) that are voice-shaped rather than type-shaped. `content-rules.md` retains the pattern templates — headlines, CTAs, service descriptions, FAQs, house formatting — that depend on voice but are not voice themselves.

**If there is ever a conflict between this file and `content-rules.md`, this file wins on voice definitions, zone assignments, and register-coupling rules. `content-rules.md` wins on pattern templates and formatting rules.**

### The register-extends-beyond-typography rule

The voice map assigns a **register** to each zone of the page. The register is not just copy — it's every surface the zone exposes. Link treatment, focus ring, border weight, background color, italic policy, measure width, mono eyebrow tone.

**Register extends beyond typography to include every rule on the page that carries voice.** If you scope register to type only, the voice shifts feel disconnected from the rest of the composition. If you scope it to every surface, the voice shifts feel intentional.

---

## 2. Relationship to GRM_VOICE_SKILL.md

GRM_VOICE_SKILL.md is the canonical source of truth for all six GRM voices. It lives at:

`https://github.com/ron841/grm-automations/blob/main/.claude/skills/GRM_VOICE_SKILL.md`

This file selects three of the six voices for contractor preview sites and specifies how they apply to the zones of a preview-site page. **If there is ever a conflict between this file and GRM_VOICE_SKILL.md on what a voice is, the voice skill wins.** If there is a conflict between this file and GRM_VOICE_SKILL.md on what voice a contractor-site zone uses, this file wins — the voice skill was written before the contractor-site use case existed, and zone assignment is this file's job.

---

## 3. The three voices used in contractor preview sites

Six voices exist in the GRM library. Three apply to contractor preview sites. Three do not.

### In scope for contractor preview sites

- **The Closing Table** (Voice 4 in the six-voice library) — primary voice. Sharp, data-forward, insight-driven. The voice of a mentor giving the real answer to someone making a hiring decision. The register where credentials live, where the phone number lives, where the CTA to call lives. Used for hero, stats, service cards, promo callouts, FAQ answers, and most conversion zones.
- **Saturday Morning** (Voice 5) — secondary voice. Clear, upbeat, informational. Grounded civic-booster voice. The business doing the work. Used for trust marquee labels, services grid header, testimonials section header, contact form header, and most transition zones.
- **The Front Porch** (Voice 1) — tertiary voice. Warm, people-first, scene-driven. The business *as people*. Used for footer tagline, About page body copy, and narrative warmth zones.

### Out of scope for contractor preview sites

Three voices remain in the GRM library for their intended use cases but are not used on contractor preview sites:

- **Plant Street** — first-person opinion voice for agent social media. Wrong POV for a business site (no first-person writer exists on a contractor homepage).
- **The Welcome Mat** — newcomer-oriented voice for homeowner guides. Wrong reader (contractor site readers are homeowners with a problem, not new arrivals).
- **The Deep Roots** — literary long-form voice for magazine cover features. Wrong length (contractor About pages are typically under 500 words, not 1,500+).

---

## 4. Voice definitions (Phase 5 quick reference)

Full voice definitions live in GRM_VOICE_SKILL.md. The summaries below exist so Phase 5 can reference the key rules without fetching the full skill file every time. Each voice definition includes its typographic signature, non-type surfaces (the "register extends beyond typography" rule), canonical instances, and copy discipline.

### Voice 4: The Closing Table (PRIMARY)

**Voice.** The business closing a deal. Certified, licensed, inspected, signed. Warm in its precision, like a mentor who gives the real answer instead of the polite one. Assumes a reader who is making a hiring decision and wants the real answer fast.

**Structure.** Contrarian insight or data point → specifics (numbers, named examples) → address the objection the reader is already thinking → concrete takeaway the reader can act on.

**Typographic signature.**

- Data-voice eyebrows in the loud register (`.role-data-eyebrow--primary`, `--primary` color).
- Display-voice headline at section-opener scale (`.role-display-section`).
- No italic in the headline — Closing Table is roman, not cursive (italic signature micro-interaction earns its own `.role-italic-signature` treatment per typography.md §5).
- Body copy at 15–16px, line-height 1.65–1.7.
- StatRow compositions (`.role-display-watermark` + `.role-data-numeral` + `.role-data-stat-caption`) appear here.

**Non-type surfaces.**

- Borders: `1px solid var(--line)`.
- Links: underlined with `border-bottom`, primary color, 2px offset.
- Focus rings: `2px solid var(--primary)`, 3px offset.
- Background: page base color. No gradient, no photo.
- Section padding: system default (72–88px vertical).

**Do.**

- Open with a contrarian observation or a data point.
- Short paragraphs, 2-3 sentences max.
- Use numbers and specifics.
- Active voice, present tense.
- End with an action the reader can take.

**Do not.**

- Use jargon to sound smart.
- Pad with background the reader already knows.
- Write puff copy.
- Use "at the end of the day" or other filler.

**Canonical instances.** Trust strip, nav, hero stat row, signature-tag + signature body copy, operational grid, FAQ answers.

**Sample output (T&F Electric hero):**

> Fifty years. Two Tuccis. One phone number.
>
> Residential, commercial, and industrial wiring across Marion County. Florida license EC13007855.

### Voice 5: Saturday Morning (SECONDARY)

**Voice.** Clear, upbeat, informational. Grounded civic-booster voice. Loves where they live and wants you to know what's happening. The business doing the work — weekly service on a Saturday, the pool getting brushed and balanced. Like a well-written email from a friend who is on every committee in town but is not annoying about it.

**Structure.** Lead with the news → one human detail that makes it interesting → brief context → practical details → close clean.

**Typographic signature.**

- Data-voice pair in card num: loud register (`--primary`) left, quiet register (`--mute`) right — per typography.md §4 two-register eyebrow system.
- Display-voice headline at card scale (28px) or section-opener scale where appropriate.
- Body copy short — 2–3 sentences max per card.
- Italic runs allowed in body-voice copy only, one per card, for the memorable phrase.
- Measure: 44–48ch per typography.md §8.

**Non-type surfaces.**

- Cards on a hairline grid — 1px between cards, white card fill, page-color gaps.
- No card shadows.
- Border-bottom on operational-tag strip matches Closing Table.
- Links inside cards: primary color, underline on hover, no default underline.

**Do.**

- Lead with news, then add the human angle.
- Include practical specifics.
- Write with genuine optimism.
- Keep sentences clean and forward-moving.
- Verbs up front. Specifics, not abstractions. "Drain, acid-wash, refinish, repair, rebalance" not "comprehensive pool restoration services."

**Do not.**

- Write like a press release.
- Use empty civic language.
- Forget the practical details.
- Use "Don't miss this!"

**Canonical instances.** Operational grid, signature-meta, gallery cards, trust marquee labels, services grid header, testimonials section header, contact form header.

**Sample output (contact form header):**

> Tell us about the job. We call back within one business hour during weekdays, and faster if it is an emergency.

### Voice 1: The Front Porch (TERTIARY)

**Voice.** Warm, people-first, scene-driven. The business *as people*. The writer shows up and notices the dog, the yard, the smell of the kitchen before asking a question. Sensory details do the heavy lifting. The subject is always a person first, a professional second. Randy keeps the pumps running. Matt keeps the chemistry right.

**Structure.** Scene opening → introduce through observation → backstory through specifics → close on community connection.

**Typographic signature.**

- Display-voice headline at footer scale (40–48px), weight 400, `text-wrap: balance`. Set via `.role-display-section` or a scoped Front Porch heading class.
- Italic runs on the *human* verbs.
- Italic color takes `--accent` on dark navy backgrounds. **This is the em-on-dark exception, and it is owned by `typography.md §5` — cross-referenced here, not duplicated.**
- Sub-copy in italic display-voice at 18–19px, line-height 1.5.

**Non-type surfaces.**

- Background: `--deep` (navy). Front Porch lives on dark. Every canonical instance of Front Porch on a homepage sits on a navy band.
- No borders inside Front Porch sections — the dark field does the containment.
- Links: white text, accent-color `border-bottom` on hover.
- Phone numbers at display scale (28–32px), white, weight 400.

**Do.**

- Open with a scene.
- Let subjects speak in their own words when captured.
- Use specific concrete nouns.
- Let emotion emerge from detail.
- End with community, not the individual.
- Names, not titles. "Randy" not "our repair technician." Second-person warmth where appropriate.

**Do not.**

- Open with a bio line.
- Use "passionate about."
- Flatten someone into their job title.
- Use exclamation points to manufacture warmth.

**Canonical instances.** Equine band, footer tagline, About page narrative body. Both navy canonical instances (Equine band, footer) couple background color to register — see §10 Register coupling rules.

**Sample output (T&F Electric About page opening):**

> Ben Tucci has walked through the same Dunnellon shop door for fifty years. The dog changes every decade or so. The Ford in the lot changes every eight. The phone number on the truck has not changed since 1975.
>
> Ben runs T&F Electric with his wife Wendy. Two Tuccis, one shop, fifty years of Marion County wiring. Most days they are on a job by eight in the morning. Some days they are on a job at two in the morning, because lightning does not wait for business hours in Florida.

---

## 5. Three-tier service composition (Signature / Operational / Distinctive)

Service pages rarely use a single register for every service. The A Quality Pool (F5) build surfaced a three-tier composition that every service-carrying page in this skill should follow. This section is a services-page adjunct to the zone-to-voice table in §6 — the zone table handles per-zone defaults and biases; this section handles how a services page decomposes into editorial tiers at authoring time.

**Signature** — one or two services that define the business. The hero services. Author in **Closing Table** register, at section-opener scale, with the signature-tag + bordered content block. These are the services a customer remembers.

**Operational** — the middle tier. Weekly recurring services, standard repairs, routine work. Author in **Saturday Morning** register, as a grid of cards with data-voice num tags. These are the services that pay the bills.

**Distinctive** — the odd one out. The specialty service, the one that earns the unusual photo and the standalone band. Author in **Front Porch** register if the specialty carries human-voice weight, or in **Saturday Morning** with expanded composition if it carries operational weight. These are the services that get remarked on.

### Decision tree for unfamiliar services

1. Is this service the one the business is known for? → Signature (Closing Table).
2. Is this service a weekly / routine / recurring line item? → Operational (Saturday Morning).
3. Is this service unusual, specialty, or voice-carrying? → Distinctive (Front Porch or Saturday Morning+).
4. Default if none of the above: Operational.

### Why written down

On A Quality Pool the three tiers emerged naturally (weekly + construction as signature, eight operational services, equine aquatics as distinctive). On the next build — commercial roofing, electrical, whatever — the tiers will *not* emerge naturally without this decision tree. The composition would drift into a flat grid of equally-weighted cards, which is the failure mode.

---

## 6. Zone-to-voice mapping

Phase 4 assigns voices by zone according to the table below. Every line of generated copy on a contractor site uses exactly one voice, determined by which zone it belongs to. Phase 5 must state the voice out loud before generating copy for that zone (see §8 Voice selection protocol).

The **Persona bias** column names how the page's selected emotional persona (from `emotional-arc.md`) tilts the voice choice when the default is ambiguous. See §7 Persona bias rules for the full treatment.

| Zone | Default voice | Why | Persona bias |
|---|---|---|---|
| Hero headline + subheadline | Closing Table | Data-forward, sharp, short punchy paragraphs. Matches the "real number, real fact, real action" headline patterns. | Neighborhood steady and Urgent service soften toward Saturday Morning for the subheadline only. Headline stays Closing Table across all personas. |
| Promo bar (if rendered) | Closing Table | Contrarian data point, specific pricing, clean close. | No persona bias. Promo bar is always Closing Table. |
| Trust marquee labels | Saturday Morning | Clean, informational, forward-moving. Credential statements are short and factual. | Modern specialist biases toward a drier Closing Table variant. Everyone else stays Saturday Morning. |
| Services grid section header | Saturday Morning | Transition headline announcing the services ahead. | Quiet confidence biases toward Closing Table. Earned pride, Neighborhood steady, Urgent service, Modern specialist stay Saturday Morning. |
| Service card descriptions | Closing Table | Mentor giving the real answer. 1-2 sentence benefit-first descriptions for hiring decisions. | No persona bias. Service card copy is always Closing Table. |
| Stats section (eyebrow, title, labels) | Closing Table | The voice literally built around numbers and specifics. Perfect match. | No persona bias. |
| Before/after section header | Closing Table | Proof is a data point. Contrarian mentor voice fits. | No persona bias. |
| Testimonials section header | Saturday Morning | Connects individual reviews to the community story. Upbeat and grounded. | Neighborhood steady biases harder into Saturday Morning with explicit place-name reference. Earned pride biases toward Closing Table with a proof-forward opening ("4.9 from 56 reviews" construction). |
| Featured promotion callout | Closing Table | Contrarian insight plus pricing plus specific action. | No persona bias. |
| FAQ questions and answers | Closing Table | Warm precision. Real answer instead of polite answer. | Neighborhood steady opens the FAQ section header with a Saturday Morning lead before the Closing Table answers begin. Answers themselves stay Closing Table across all personas. |
| Contact form headline + subhead | Saturday Morning | Upbeat informational. Lead with what happens when they submit. | Urgent service biases toward Closing Table with a response-time claim foregrounded ("We call back within the hour"). |
| Footer tagline | Front Porch | Warm, people-first, identity grounding. Creates a moment of warmth at the end of the page and echoes the About page voice. | No persona bias. Footer is always Front Porch. |
| About page (full long-form) | Front Porch | Scene-driven, people-first, specific concrete nouns. | Modern specialist allows one paragraph of technical precision (Closing Table voice) embedded in the otherwise-Front-Porch narrative. Earned pride opens with a claim rather than a scene. Neighborhood steady leans heavily into Front Porch throughout. Other personas stay pure Front Porch. |

### Zone table grouping note

The table above groups paired zones for documentation readability — `Hero headline + subheadline` appears as one row (different persona-bias behaviors for headline vs subheadline are noted in the bias column); `FAQ questions and answers` appears as one row (different bias on question header vs answer body noted in the bias column). `composition-plan-schema.md §7` splits these into 15 machine keys (`hero-headline`, `hero-subheadline`, `faq-question`, `faq-answer`, and eleven others) so that Phase 4's per-zone voice resolution operates at the split-zone granularity. The documentation grouping and the schema split coexist: this table is the authoring reference; the schema enum is the machine contract; Phase 4 resolves per split zone.

---

## 7. Persona bias rules

The five emotional personas defined in `emotional-arc.md` do not replace the voice map. They bias it. Each persona has a directional tilt across the mapping that expresses its emotional key without overriding voice at the zone level.

The relationship is: **voiceMap answers "what voice does this specific zone use." Persona answers "in ambiguous zones, which voice does this page lean toward, and how heavily."**

Personas do not override voice in conversion-critical zones (hero headline, stats, service cards, FAQ answers, promo callout, featured promotion) — those zones are always Closing Table regardless of persona. Personas affect voice choice in transition zones (section headers) and narrative zones (About page, footer tagline, testimonials header) where the default is softer.

### Persona → voice lean

- **Quiet confidence.** Leans Closing Table in the services grid header (instead of Saturday Morning default). Keeps Front Porch minimal on the About page. Produces a page that feels precise and undemonstrative.
- **Earned pride.** Leans Closing Table in the testimonials header with a proof-forward opening. Keeps Front Porch on the About page but opens with a claim rather than a scene. Produces a page that feels accomplished and evidence-first.
- **Neighborhood steady.** Leans Saturday Morning in the hero subheadline. Adds a Saturday Morning lead-in to the FAQ section header. Uses Front Porch heavily in the About page and footer. Produces a page that feels warm and civic.
- **Urgent service (Rescue-ready).** Leans Closing Table in the contact form headline with response-time claim. Keeps Saturday Morning minimal. Produces a page that feels urgent and response-oriented.
- **Modern specialist.** Leans a dry Closing Table variant in the trust marquee (instead of Saturday Morning default). Allows one technical-precision paragraph in Closing Table voice on the About page. Produces a page that feels technical and confident.

### Resolution rule when persona bias and zone default disagree

If the persona bias column names a voice different from the zone default, the persona bias wins. If the persona bias column says "No persona bias," the zone default wins regardless of persona.

### What personas do NOT do

Personas do not:

- Override voice in conversion zones (hero headline, stats, service cards, promo callout, FAQ answers, featured promotion).
- Create new voices or merge existing voices.
- Change which voices are in scope vs out of scope.
- Bias voice in zones where the bias column says "No persona bias."

Keeping this list short is load-bearing. Without it, persona creeps into voice selection in every zone and the voice map stops being meaningful.

---

## 8. Voice selection protocol for Phase 5

Before writing any zone of a contractor preview site, Phase 5 must:

1. Identify the zone (hero, services, stats, testimonials, etc.) — match against §6 zone table and `composition-plan-schema.md §7` closed enum.
2. Look up the default voice in the mapping table (§6).
3. Check the persona bias column for the page's selected persona.
4. State the voice out loud before generating copy: *"Writing the hero in Voice 4: The Closing Table."*
5. Generate the entire zone in that single voice from first word to last.
6. Never blend voices within a zone.
7. Never reassign a voice mid-zone.

**One piece equals one voice** is the rule in `GRM_VOICE_SKILL.md`. Adapted for contractor preview sites: **one ZONE equals one voice**. A contractor website is a multi-zone document, not a single piece, so voices can vary by zone purpose. Within a zone, one voice rules.

### Authoring order for a new page

1. **Lay out the voice map first.** Which zones are Closing Table? Saturday Morning? Front Porch? Voice pivot (anchor strip)? Write as HTML comments before styling. Cross-reference `composition-plan.json.pages[].voiceZones[]` for the resolved assignments.
2. **Pick backgrounds from the voice map.** Navy for Front Porch. Page base otherwise. See §10 Register coupling rules.
3. **Apply typography from `typography.md`** — role-class assignments per the voice of each zone.
4. **Author copy per register discipline** (§4 Voice definitions; §11 Copy discipline per register).
5. **Review for register coupling.** Does every surface carry the register? Borders, links, focus rings, data-voice tone?
6. **Check for exception drift.** Has an exception been introduced that isn't named in the voice map or in `typography.md` Appendix A? If yes, either promote it to a named exception with reasoning, or remove it. Silent exceptions are the most common failure mode.

**The failure mode to watch for.** A section that looks typographically right but feels flat — usually because the non-type surfaces are all authored in the default register rather than the zone's register. Check the border color. Check the link treatment. Check the background.

---

## 9. The voice-pivot anchor strip

A specific pattern that earns its own section.

Between the hero (Closing Table) and the services on the A Quality Pool F5 homepage sits a full-width strip containing one italic display-voice pullquote and a mono credit. This strip is the **voice pivot** — it lifts the page from the certified-licensed register of the hero into something more reflective, just for one sentence.

**Why it works.** The hero says "36 years." The footer says "Randy keeps the pumps running." Without the anchor strip, those two registers sit next to each other with only service cards between them, and the transition feels abrupt.

### Typographic signature

- Italic display-voice pullquote, 22–28px, weight 300, `--darkmuted`.
- Data-voice credit in a two-tone pair per `typography.md §4`.
- Thin borders top and bottom.
- Generous horizontal padding, modest vertical padding.

### Once per page — rule with reasoning articulated

An anchor strip is a register pivot. Register pivots consume reader attention budget — the reader's cognitive dwell-time on a voice shift before they can re-orient to the new register. That budget is finite per page. One pivot is felt as *deliberate;* two pivots means neither register holds the page long enough for the reader to settle into it, and the shifts read as vacillation rather than intention.

If a page genuinely needs two pivots, one of the underlying sections is probably in the wrong register — combine or reassign before adding a second strip.

### Schema integration

`composition-plan-schema.md §5` carries `anchorStrip` as a tagged section type. Phase 4 declares at most one per page per the once-per-page rule above; Phase 5 emits against the role-class composition and the `typography.md §5` italic pullquote sizing.

---

## 10. Register coupling rules

Rules that span registers and express the "register extends beyond typography" rule at the whole-page scale.

### Background color and register are coupled

Every background declares a register. On the A Quality Pool canonical F5 homepage:

- Page base (off-white / `--page`) → Closing Table or Saturday Morning.
- Navy (`--deep`) → Front Porch.

Four registers is the practical ceiling. Brands may earn a third background if it's declared in the voice map as a register. A page with an undeclared third background ("light gray section") reads as a page with three voices and one mistake.

The rule is not "two backgrounds and no more." The rule is **no silent backgrounds** — every background is a declared register, and new registers require explicit authoring in this document before they're used.

### Data-voice register follows voice register

- Closing Table sections use `--primary` for loud eyebrow register (`.role-data-eyebrow--primary`) and `--mute` for quiet meta (`.role-data-eyebrow--mute`).
- Saturday Morning sections use the same pairing.
- Front Porch sections on navy use `--accent` for loud register and `--deep-dim` for quiet meta.

The pairing — loud register + quiet register — is universal. The colors shift based on background. Schema integration: `composition-plan.json.eyebrowDeployments[].register` carries the explicit value per eyebrow.

### Italic follows register

- Closing Table: rare, one italic run per section at most, headlines only (and only via `.role-italic-signature` per the italic-signature micro-interaction when Tier 1 signature selection names it).
- Saturday Morning: per-card, one run, in body-voice copy.
- Front Porch: multiple runs in headlines, on accent color (per em-on-dark exception on navy backgrounds), celebratory.

---

## 11. Featured pullquote testimonial — register consumer

The testimonial pattern blends registers rather than choosing one. This section covers the voice-layering composition around a featured pullquote. Placement rules (between sections, not inside testimonials grids) and detection heuristic (Design's 8-20 word + 2-of-5 rule) live in `typography.md §13` and `typography.md §14 Rule 5`; this section governs the multi-voice composition that sits around the quote.

### Composition — four voice layers

- **Closing Table eyebrow** — the frame is trust-carrying. `.role-data-eyebrow--primary`.
- **Closing Table title with italic counter-phrase** — the page speaks in its institutional voice to frame the pullquote. `.role-display-section` with one `<em>` span per `typography.md §5 One italic run per headline`.
- **Featured Pullquote at display-italic scale** — the customer's voice, Front Porch typographically (italic, warm) but on page-base background rather than navy. Set via `.role-display-pullquote`.
- **Data-voice attribution** — back to Closing Table, naming names precisely. `.role-data-caption` with quiet register tracking.

### Typographic signature for the pullquote itself

- Pullquote: `clamp(30px, 3.3vw, 40px)`, italic, weight 300, `--darkmuted`, `max-width: 20ch`.
- Attribution name: display-voice face, 20px, weight 500.
- Attribution meta: data-voice, 10px, 0.12em tracking, quiet register.

**No decorative quote marks.** The italic display scale is doing the quote-signaling. Per `typography.md §16 Ornament rule`.

### Detection and placement

See `typography.md §13 Pull-quote detection heuristic` and `typography.md §14 Rule 5 Pull-quote deployment`. Design's 8-20 word + 2-of-5 heuristic is authoritative for which testimonials earn pullquote treatment; Rule 5 governs placement (between sections). This file governs the voice-layering composition for the pullquote and its surrounding frame once Phase 4 has identified it.

---

## 12. Front Porch footer — register consumer

The canonical Front Porch instance. The rules:

- Navy background (`--deep`).
- Display-voice headline at footer scale, italic on human verbs, accent color on italic runs (em-on-dark exception — owned by `typography.md §5`).
- Phone number at display scale (28–32px), white, weight 400.
- Data-voice column labels in accent color.
- Attribution copy at 12px, line-height 1.6, **sentence case** — the one place on the page where sentence case appears in a data-voice surface. This is an exception to the uppercase rule in `typography.md §4`, earned by length (photo credits with names are unreadable at 12px uppercase). The four-point exceptions principle is documented in `typography.md Appendix A`.

The Front Porch footer consolidates three rules: italic-on-dark with color shift, display phone number, sentence-case data-voice attribution.

---

## 13. Copy discipline per register

Which lines earn italic runs, and which stay prose.

### Sacred lines (italic earned)

- Front Porch headline: italic on the warm verb. "Randy *keeps* the pumps running."
- Hero headline: italic on the regional anchor or emotional phrase. "of pools in *Central Florida*."
- Section-opener italic counter-phrase: "Eight services. *One pool phone number.*"
- Featured pullquote: entire quote italic at display scale.

### Prose (italic withheld)

- Body descriptions inside service cards.
- Trust-strip content.
- Stat labels and data-voice captions.
- Button text and CTAs.

### The generalizable rule

**Italic is earned by voice, not by emphasis.** If a line is italicized to "make it pop," the italic is wrong. If a line is italicized because it carries a voice shift that the italic shape reinforces, the italic is right.

When in doubt: read the paragraph aloud. If the italic phrase would naturally get a small pause or vocal lift, italic is earned.

Phase 6 Check 1 enforces "one italic span per H1/H2" structurally via the `composition-plan.json.italicSelections[]` at-most-one-per-headingId invariant. Check 9 verifies italicized word against the persona's word-class list per `emotional-arc.md` (soft fail; human review at Phase 4 approval gate is authoritative).

---

## 14. Universal GRM rules that apply across all voices

These rules govern customer-facing output regardless of voice. They live authoritatively in `content-rules.md` (see Universal GRM rules section) as a synced excerpt from `GRM_VOICE_SKILL.md`. The short list:

- No em dashes in customer output.
- Real numbers, real names, real specifics — never invented.
- No corporate jargon, no AI tells (see banned-words list in `content-rules.md`).
- Active voice, present tense preferred.
- Short paragraphs (2-3 sentences typical).
- One piece equals one voice (adapted: one zone equals one voice).

If these rules conflict with anything above, the universal rules win. A Closing Table hero is not allowed to use em dashes even though nothing in the Closing Table definition forbids them — the universal ban overrides.

See `content-rules.md` for the full universal rules list and the current banned-words vocabulary.

---

## 15. Phase 6 voice verification checks

Phase 6 verifies voice compliance before ship. The following checks are required:

- **Zone-voice assignment check.** For each zone on each page, Phase 6 asserts that the generated copy matches the zone's assigned voice. Implementation: Phase 5 stamps each zone's section-root with `data-voice="{resolvedVoice}"` during generation; Phase 6 reads the attribute and cross-references against this file's mapping table and `composition-plan.json.voiceZones[]`.
- **Universal-rules check.** Every customer-facing string is scanned for em dashes, banned phrases (from `content-rules.md` banned-words list), and AI tells. Hard fail on any match.
- **Persona-bias consistency check.** The page's selected persona must be declared once in `composition-plan.json.persona` and the resolved voice for each zone must match the persona-bias column of this file's mapping table. Soft fail — warns, does not block ship — because persona bias is directional, not absolute, and over-enforcement produces brittle builds.
- **Zone-voice-mixing check.** Within a single zone, no sentence-level voice mixing is permitted. Implementation: a zone whose declared voice is Closing Table cannot contain phrasing patterns (opening scene construction, sensory-detail-heavy sentences, "passionate about" framing) that only appear in Front Porch or Saturday Morning definitions.

These checks complement the thirteen typographic Phase 6 checks in `typography.md §15`; together they cover voice and type compliance at the whole-page scale.

---

## 16. Open questions for future rounds

These are deliberate gaps. Flag when the work surfaces them.

- **A fourth register for long-form content.** If this skill generates blog posts or case studies, a long-form reading register may be needed.
- **Form register.** Contact forms and estimate requests currently inherit Closing Table by default; whether form-labels-in-tracked-caps warrants a distinct authoring register is open.
- **The specialty-subdomain question.** Equine Aquatics on the A Quality Pool homepage is a Front Porch section carrying a specialized voice (Marion horse country, specialized aquatic services). Whether "specialty subdomain" is a modifier on Front Porch or a fourth register is the most pressing open question in this document. The next build with a specialty service (historic-home electrical, commercial roofing on a residential brand, etc.) will force the resolution. Until then: treat specialty as a Front Porch modifier and flag the specific instance in the build notes.

---

## Appendix reference: the exceptions principle

The skill's exceptions principle — the four-point frame that determines whether an exception is earned (broken outcome / bounded context / written reasoning / not instance-scoped) — lives in **`typography.md` Appendix A**. Both named exceptions in the current skill are fundamentally typographic: em-on-dark is a color-on-italic rule, and the 12px sentence-case data-voice attribution is a case-and-tracking rule.

When authoring a new voice-map register, a new background, or a new specialty context, check `typography.md` Appendix A before introducing an exception. If the four points don't all hold, the exception isn't earned — fix the rule or hold the line.

---

## Cross-references

- `typography.md` — the three *type* voices (display / body / data) that express this file's three *copy* voices (Closing Table / Saturday Morning / Front Porch) visually. Voice map picks the words; typography picks the fonts, weights, sizes, and rhythm. Pull-quote detection heuristic (§13) and placement (§14 Rule 5) live there; pull-quote voice-layering composition lives here (§11).
- `emotional-arc.md` — the five personas that bias voice selection in ambiguous zones. Read together with this file; neither works alone.
- `content-rules.md` — universal GRM rules, banned words, headline patterns, CTA templates, service description templates, FAQ templates per vertical, house formatting. The pattern templates and enforcement rules this file's voices produce content *for*.
- `GRM_VOICE_SKILL.md` — canonical source of truth for all six GRM voices. This file cites three of them and specifies contractor-site zone assignments.
- `composition-plan-schema.md §7` — closed 15-zone voice vocabulary. Schema enum that Phase 4 resolves against this file's zone table.
- `composition-plan-schema.md §4.2` — per-page `voiceZones[]` array with `zone`, `defaultVoice`, `personaBiasApplied`, `resolvedVoice`, `biasReason`. Where Phase 4's zone-voice resolution lands on disk.
- `composition-plan-schema.md §5` — `anchorStrip` tagged section type backed by §9 here.
- `SKILL.md` Phase 5 — voice selection protocol and how to state voice out loud before generating copy.
- `SKILL.md` Phase 6 — voice verification checks and the hard-fail vs soft-fail ladder.

---

## Revision log

### 2026-04-22 — Stage II (d) three-way merge

**Merge sources:**
- **Production baseline.** Composer's pre-merge `references/voiceMap.md` (post Stage II (a) file copy from production). Register-theory file organized around three registers (Closing Table / Saturday Morning / Front Porch) with canonical instances, three-tier service composition (Signature / Operational / Distinctive), voice-pivot anchor strip, featured pullquote composition, Front Porch footer, register coupling rules, and copy discipline per register.
- **Design in-flight.** `~/grm-automations/docs/composer-stage-ii-typography-source/voiceMap.md` (v0.7.2). Zone-to-voice mapping as a 14-row table keyed by zone with persona-bias column, five-persona bias rules, Phase 5 voice selection protocol, universal GRM rules, four Phase 6 voice verification checks.
- **Proposed merge output.** This file.

**Conflicts resolved (five applied in this file; remaining seven applied in `typography.md`):**

1. **A2 voiceMap zone table grouping note — auto-resolved.** §6 carries Design's 14-row zone table verbatim with a note immediately below naming that `composition-plan-schema.md §7` splits `Hero headline + subheadline` and `FAQ questions and answers` into 15 machine keys for Phase 4's per-split-zone resolution. Documentation grouping and schema split coexist.
2. **C1 Anchor-strip pattern preservation — auto-resolved via token-preservation.** Composer §3 voice-pivot anchor strip preserved verbatim at §9 here with reasoning articulated ("register pivots consume reader attention budget; one pivot is deliberate, two reads as vacillation"). `composition-plan-schema.md §5` depends on this as the `anchorStrip` section-type authority.
3. **C2 Three-tier service composition preservation — auto-resolved via token-preservation.** Composer §2d Signature / Operational / Distinctive composition preserved at §5 here as a services-page adjunct to Design's zone table. Decision tree for unfamiliar services preserved verbatim.
4. **C3 Pull-quote trigger — Design arbitration.** Composer §4's old ≥60-word + credibility-marker heuristic retires. `promoted: true` override retires. Design's 8-20-word + 2-of-5 heuristic (now in `typography.md §13`) wins. §11 in this file documents the voice-layering composition around the pullquote; detection and placement live in `typography.md`. If a future build surfaces need for a testimonial-spotlight editorial moment, it earns its own section type — not built now.
5. **C6 Pullquote voice-layering split — auto-resolved.** Voice-layering composition breakdown (Closing Table eyebrow + Closing Table title with italic counter-phrase + Featured Pullquote at display-italic scale + Data-voice attribution) at §11 here. Placement and detection cross-referenced to `typography.md §13` + `typography.md §14 Rule 5`.

**Also folded in from Design in-flight:**
- Zone-to-voice mapping table (§6) as machine-readable authority for Phase 4.
- Phase 5 voice selection protocol step list (§8) — merged with Composer's authoring-order checklist.
- Universal GRM rules (§14) — synced excerpt from `content-rules.md`.
- Phase 6 voice verification checks (§15) — zone-voice assignment via `data-voice` attribute, universal-rules check, persona-bias consistency, zone-voice-mixing.
- Out-of-scope voice enumeration (§3) — Plant Street, Welcome Mat, Deep Roots explicitly named as out-of-scope.
- Numbered voice identifiers (Voice 4, Voice 5, Voice 1 from GRM_VOICE_SKILL.md six-voice library) per §2 Relationship to GRM_VOICE_SKILL.md.
- "Urgent service (Rescue-ready)" naming absorbed across persona references — machine key per `emotional-arc.md`, display name per Design.

**Also preserved from Composer pre-merge:**
- Register-theory framing at §1 (register extends beyond typography rule).
- Front Porch footer composition (§12) with 12px sentence-case attribution exception.
- Copy discipline per register — sacred lines vs prose (§13).
- Register coupling rules (§10) — background/register, data-voice/register, italic/register coupling.
- Open questions for future rounds (§16).
- Appendix reference to `typography.md` Appendix A exceptions principle.

**Design reviewer signoff.** Checkpoint 1 q1 follow-up, plus Stage II (d) arbitration on A1, B3, C3 — dated 2026-04-22. Design's signoff is the Stage II (d) arbitration response, not a separate file.

---

## Version

v1.0 — Stage II (d) merge output, 2026-04-22. Supersedes Composer's pre-merge `references/voiceMap.md` (production F5-era register-theory file) and archives `composer-stage-ii-typography-source/voiceMap.md` (Design in-flight v0.7.2) as merge-input sources. Canonical authority for Composer voice mapping from this point forward.

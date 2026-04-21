# Voice Map Reference

Part of the prospect-site skill v0.7.2. Loaded by Phase 5 whenever it begins writing copy for a new section, and by Phase 6 as the authority for voice compliance checks. This is the zone-to-voice mapping authority — which of the three contractor-site voices governs which zone of the page, how each voice sounds, and how the five emotional personas bias voice selection in ambiguous zones.

---

## Why this file exists

Before v0.7.2, voice mapping lived inside `content-rules.md`, alongside headline patterns, CTA templates, service description structures, FAQ templates, and house formatting rules. That file was doing two jobs: defining *how each voice sounds* and defining *what specific patterns each voice produces in specific contexts*. The two jobs have different audiences — Phase 5 looking up "which voice am I in right now" versus Phase 5 looking up "what's the structure of a hero headline in Closing Table voice."

Separating them makes both files easier to reason about. `voiceMap.md` owns the zone-to-voice mapping, the voice definitions themselves, and the persona-bias rules. `content-rules.md` retains the pattern templates — headlines, CTAs, service descriptions, FAQs, house formatting — that depend on voice but are not voice themselves.

**If there is ever a conflict between this file and `content-rules.md`, this file wins on voice definitions and zone assignments. `content-rules.md` wins on pattern templates and formatting rules.**

---

## Relationship to GRM_VOICE_SKILL.md

GRM_VOICE_SKILL.md is the canonical source of truth for all six GRM voices. It lives at:

`https://github.com/ron841/grm-automations/blob/main/.claude/skills/GRM_VOICE_SKILL.md`

This file selects three of the six voices for contractor preview sites and specifies how they apply to the zones of a preview-site page. **If there is ever a conflict between this file and GRM_VOICE_SKILL.md on what a voice is, the voice skill wins.** If there is a conflict between this file and GRM_VOICE_SKILL.md on what voice a contractor-site zone uses, this file wins — the voice skill was written before the contractor-site use case existed, and zone assignment is this file's job.

---

## The three voices used in contractor preview sites

Six voices exist in the GRM library. Three apply to contractor preview sites. Three do not.

### In scope for contractor preview sites

- **The Closing Table** — primary voice. Sharp, data-forward, insight-driven. The voice of a mentor giving the real answer to someone making a hiring decision. Used for hero, stats, service cards, promo callouts, FAQ answers, and most conversion zones.
- **Saturday Morning** — secondary voice. Clear, upbeat, informational. Grounded civic-booster voice that connects the business to the community without being saccharine. Used for trust marquee labels, services grid header, testimonials section header, contact form header, and most transition zones.
- **The Front Porch** — tertiary voice. Warm, people-first, scene-driven. The voice of someone who notices the dog before the business card. Used for footer tagline, About page body copy, and narrative warmth zones.

### Out of scope for contractor preview sites

Three voices remain in the GRM library for their intended use cases but are not used on contractor preview sites:

- **Plant Street** — first-person opinion voice for agent social media. Wrong POV for a business site (no first-person writer exists on a contractor homepage).
- **The Welcome Mat** — newcomer-oriented voice for homeowner guides. Wrong reader (contractor site readers are homeowners with a problem, not new arrivals).
- **The Deep Roots** — literary long-form voice for magazine cover features. Wrong length (contractor About pages are typically under 500 words, not 1,500+).

---

## Voice definitions (Phase 5 quick reference)

Full voice definitions live in GRM_VOICE_SKILL.md. The summaries below exist so Phase 5 can reference the key rules without fetching the full skill file every time.

### Voice 4: The Closing Table (PRIMARY)

**Description.** Sharp, clean, insight-driven. Assumes a reader who is making a hiring decision and wants the real answer fast. Warm in its precision, like a mentor who gives the real answer instead of the polite one.

**Structure.** Contrarian insight or data point → specifics (numbers, named examples) → address the objection the reader is already thinking → concrete takeaway the reader can act on.

**Do.**

- Open with a contrarian observation or a data point
- Short paragraphs, 2-3 sentences max
- Use numbers and specifics
- Active voice, present tense
- End with an action the reader can take

**Do not.**

- Use jargon to sound smart
- Pad with background the reader already knows
- Write puff copy
- Use "at the end of the day" or other filler

**Sample output (T&F Electric hero):**

> Fifty years. Two Tuccis. One phone number.
>
> Residential, commercial, and industrial wiring across Marion County. Florida license EC13007855.

### Voice 5: Saturday Morning (SECONDARY)

**Description.** Clear, upbeat, informational. Grounded civic-booster voice. Loves where they live and wants you to know what's happening. Like a well-written email from a friend who is on every committee in town but is not annoying about it.

**Structure.** Lead with the news → one human detail that makes it interesting → brief context → practical details → close clean.

**Do.**

- Lead with news, then add the human angle
- Include practical specifics
- Write with genuine optimism
- Keep sentences clean and forward-moving

**Do not.**

- Write like a press release
- Use empty civic language
- Forget the practical details
- Use "Don't miss this!"

**Sample output (contact form header):**

> Tell us about the job. We call back within one business hour during weekdays, and faster if it is an emergency.

### Voice 1: The Front Porch (TERTIARY)

**Description.** Warm, people-first, scene-driven. The writer shows up and notices the dog, the yard, the smell of the kitchen before asking a question. Sensory details do the heavy lifting. The subject is always a person first, a professional second.

**Structure.** Scene opening → introduce through observation → backstory through specifics → close on community connection.

**Do.**

- Open with a scene
- Let subjects speak in their own words when captured
- Use specific concrete nouns
- Let emotion emerge from detail
- End with community, not the individual

**Do not.**

- Open with a bio line
- Use "passionate about"
- Flatten someone into their job title
- Use exclamation points to manufacture warmth

**Sample output (T&F Electric About page opening):**

> Ben Tucci has walked through the same Dunnellon shop door for fifty years. The dog changes every decade or so. The Ford in the lot changes every eight. The phone number on the truck has not changed since 1975.
>
> Ben runs T&F Electric with his wife Wendy. Two Tuccis, one shop, fifty years of Marion County wiring. Most days they are on a job by eight in the morning. Some days they are on a job at two in the morning, because lightning does not wait for business hours in Florida.

---

## Zone-to-voice mapping (v0.7.2)

Phase 5 assigns voices by zone according to this table. Every line of generated copy on a contractor site uses exactly one voice, determined by which zone it belongs to. Phase 5 must state the voice out loud before generating copy for that zone.

The **Persona bias** column names how the page's selected emotional persona (from `emotional-arc.md`) tilts the voice choice when the default is ambiguous. See the persona-bias section below for full details.

| Zone | Default voice | Why | Persona bias |
|---|---|---|---|
| Hero headline + subheadline | Closing Table | Data-forward, sharp, short punchy paragraphs. Matches the "real number, real fact, real action" headline patterns. | Neighborhood steady and Rescue-ready soften toward Saturday Morning for the subheadline only. Headline stays Closing Table across all personas. |
| Promo bar (if rendered) | Closing Table | Contrarian data point, specific pricing, clean close. | No persona bias. Promo bar is always Closing Table. |
| Trust marquee labels | Saturday Morning | Clean, informational, forward-moving. Credential statements are short and factual. | Modern specialist biases toward a drier Closing Table variant. Everyone else stays Saturday Morning. |
| Services grid section header | Saturday Morning | Transition headline announcing the services ahead. | Quiet confidence and Earned pride bias toward Closing Table. Neighborhood steady and Rescue-ready stay Saturday Morning. Modern specialist stays Saturday Morning. |
| Service card descriptions | Closing Table | Mentor giving the real answer. 1-2 sentence benefit-first descriptions for hiring decisions. | No persona bias. Service card copy is always Closing Table. |
| Stats section (eyebrow, title, labels) | Closing Table | The voice literally built around numbers and specifics. Perfect match. | No persona bias. |
| Before/after section header | Closing Table | Proof is a data point. Contrarian mentor voice fits. | No persona bias. |
| Testimonials section header | Saturday Morning | Connects individual reviews to the community story. Upbeat and grounded. | Neighborhood steady biases harder into Saturday Morning with explicit place-name reference. Earned pride biases toward Closing Table with a proof-forward opening ("4.9 from 56 reviews" construction). |
| Featured promotion callout | Closing Table | Contrarian insight plus pricing plus specific action. | No persona bias. |
| FAQ questions and answers | Closing Table | Warm precision. Real answer instead of polite answer. | Neighborhood steady opens the FAQ section header with a Saturday Morning lead before the Closing Table answers begin. Answers themselves stay Closing Table across all personas. |
| Contact form headline + subhead | Saturday Morning | Upbeat informational. Lead with what happens when they submit. | Rescue-ready biases toward Closing Table with a response-time claim foregrounded ("We call back within the hour"). |
| Footer tagline | Front Porch | Warm, people-first, identity grounding. Creates a moment of warmth at the end of the page and echoes the About page voice. | No persona bias. Footer is always Front Porch. |
| About page (full long-form) | Front Porch | Scene-driven, people-first, specific concrete nouns. | Modern specialist allows one paragraph of technical precision (Closing Table voice) embedded in the otherwise-Front-Porch narrative. Other personas stay pure Front Porch. |

### Voice selection protocol for Phase 5

Before writing any zone of a contractor preview site, Phase 5 must:

1. Identify the zone (hero, services, stats, testimonials, etc.)
2. Look up the default voice in the mapping table above
3. Check the persona bias column for the page's selected persona
4. State the voice out loud before generating copy: *"Writing the hero in Voice 4: The Closing Table."*
5. Generate the entire zone in that single voice from first word to last
6. Never blend voices within a zone
7. Never reassign a voice mid-zone

**One piece equals one voice** is the rule in `GRM_VOICE_SKILL.md`. Adapted for contractor preview sites: **one ZONE equals one voice**. A contractor website is a multi-zone document, not a single piece, so voices can vary by zone purpose. Within a zone, one voice rules.

---

## Persona bias rules (how personas tilt voice selection)

The five emotional personas defined in `emotional-arc.md` do not replace the voice map. They bias it. Each persona has a directional tilt across the mapping that expresses its emotional key without overriding voice at the zone level.

The relationship is: **voiceMap answers "what voice does this specific zone use." Persona answers "in ambiguous zones, which voice does this page lean toward, and how heavily."**

Personas do not override voice in conversion-critical zones (hero headline, stats, service cards, FAQ answers, promo callout) — those zones are always Closing Table regardless of persona. Personas affect voice choice in transition zones (section headers) and narrative zones (About page, footer tagline, testimonials header) where the default is softer.

### Persona → voice lean

- **Quiet confidence.** Leans Closing Table in the services grid header (instead of Saturday Morning default). Keeps Front Porch minimal on the About page. Produces a page that feels precise and undemonstrative.
- **Earned pride.** Leans Closing Table in the testimonials header with a proof-forward opening. Keeps Front Porch on the About page but opens with a claim rather than a scene. Produces a page that feels accomplished and evidence-first.
- **Neighborhood steady.** Leans Saturday Morning in the hero subheadline. Adds a Saturday Morning lead-in to the FAQ section header. Uses Front Porch heavily in the About page and footer. Produces a page that feels warm and civic.
- **Rescue-ready.** Leans Closing Table in the contact form headline with response-time claim. Keeps Saturday Morning minimal. Produces a page that feels urgent and response-oriented.
- **Modern specialist.** Leans a dry Closing Table variant in the trust marquee (instead of Saturday Morning default). Allows one technical-precision paragraph in Closing Table voice on the About page. Produces a page that feels technical and confident.

### Resolution rule when persona bias and zone default disagree

If the persona bias column names a voice different from the zone default, the persona bias wins. If the persona bias column says "No persona bias," the zone default wins regardless of persona.

### What personas do NOT do

Personas do not:

- Override voice in conversion zones (hero headline, stats, service cards, promo callout, FAQ answers)
- Create new voices or merge existing voices
- Change which voices are in scope vs out of scope
- Bias voice in zones where the bias column says "No persona bias"

Keeping this list short is load-bearing. Without it, persona creeps into voice selection in every zone and the voice map stops being meaningful.

---

## Universal GRM rules that apply across all voices

These rules govern customer-facing output regardless of voice. They live authoritatively in `content-rules.md` (see Universal GRM rules section) as a synced excerpt from `GRM_VOICE_SKILL.md`. The short list:

- No em dashes in customer output
- Real numbers, real names, real specifics — never invented
- No corporate jargon, no AI tells (see banned-words list in `content-rules.md`)
- Active voice, present tense preferred
- Short paragraphs (2-3 sentences typical)
- One piece equals one voice (adapted: one zone equals one voice)

If these rules conflict with anything above, the universal rules win. A Closing Table hero is not allowed to use em dashes even though nothing in the Closing Table definition forbids them — the universal ban overrides.

See `content-rules.md` for the full universal rules list and the current banned-words vocabulary.

---

## Phase 6 voice verification checks

Phase 6 verifies voice compliance before ship. The following checks are required:

- **Zone-voice assignment check.** For each zone on each page, Phase 6 asserts that the generated copy matches the zone's assigned voice. Implementation: Phase 5 tags each zone's copy block with a `data-voice` attribute during generation; Phase 6 reads the attribute and cross-references against this file's mapping table.
- **Universal-rules check.** Every customer-facing string is scanned for em dashes, banned phrases (from `content-rules.md` banned-words list), and AI tells. Hard fail on any match.
- **Persona-bias consistency check.** The page's selected persona must be declared once in `profile.json` and the resolved voice for each zone must match the persona-bias column of this file's mapping table. Soft fail — warns, does not block ship — because persona bias is directional, not absolute, and over-enforcement produces brittle builds.
- **Zone-voice-mixing check.** Within a single zone, no sentence-level voice mixing is permitted. Implementation: a zone whose declared voice is Closing Table cannot contain phrasing patterns (opening scene construction, sensory-detail-heavy sentences, "passionate about" framing) that only appear in Front Porch or Saturday Morning definitions.

---

## Cross-references

- `emotional-arc.md` — the five personas that bias voice selection in ambiguous zones. Read together with this file; neither works alone.
- `typography-patterns.md` — the three-voice *type* system (display / body / data) that expresses this file's *copy* voice system visually. Voice map picks the words; typography patterns pick the font, weight, size, and rhythm those words render in.
- `content-rules.md` — universal GRM rules, banned words, headline patterns, CTA templates, service description templates, FAQ templates per vertical, house formatting. The pattern templates and enforcement rules this file's voices produce content *for*.
- `GRM_VOICE_SKILL.md` — canonical source of truth for all six GRM voices. This file cites three of them and specifies contractor-site zone assignments.
- `SKILL.md` Phase 5 — voice selection protocol and how to state voice out loud before generating copy.
- `SKILL.md` Phase 6 — voice verification checks and the hard-fail vs soft-fail ladder.

---

## Version

Extracted from content-rules.md in v0.7.2. Previously content-rules.md lines 39-82 (voice mapping), 181-257 (voice definitions in brief), and 59-82 (Voices NOT used + Voice selection protocol). Content-rules.md now cross-references this file for voice authority; pattern templates, universal rules, banned words, and FAQ templates remain in content-rules.md.

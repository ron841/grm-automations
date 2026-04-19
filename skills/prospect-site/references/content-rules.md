# Content Rules Reference

Part of the prospect-site skill v0.7. Loaded by Phase 5 when the skill begins generating any copy. This file governs every word that ends up on a generated contractor preview site.

## Critical distinction before you read any further

The em-dash ban and the strict Plant Street voice rules apply ONLY to template strings and example outputs that end up as customer-facing copy on a generated site. Meta-commentary throughout this file (explanations, rationales, "when to use this" notes) can use em dashes freely because it is GRM internal documentation, not customer output. If a rule appears inside a code block or in quotation marks as an example output, it follows GRM voice rules. Everything else is internal and can use normal writing conventions.

---

## Relationship to GRM_VOICE_SKILL.md

**GRM_VOICE_SKILL.md is the canonical source of truth for GRM voice.** It lives at:

`https://github.com/ron841/grm-automations/blob/main/.claude/skills/GRM_VOICE_SKILL.md`

That skill defines six voices (The Front Porch, Plant Street, The Welcome Mat, The Closing Table, Saturday Morning, The Deep Roots) with full do's and don'ts, sample rewrites, publication mapping, and universal rules. If there is ever a conflict between something in this file and GRM_VOICE_SKILL.md, **the voice skill wins**.

This file does not duplicate the voice skill. It does three things on top of it:

1. **Maps specific voices to specific sections of a contractor preview site** (the v0.7 use case was not contemplated when the voice skill was written, so the mapping happens here).
2. **Documents the universal GRM rules and banned words list** as a synced excerpt so Phase 5 can enforce them without network access. This excerpt must stay in sync with the voice skill manually. When the voice skill updates, update this file too.
3. **Provides contractor-specific patterns** that do not exist in the voice skill: headline patterns, CTA templates, service description templates, FAQ templates per trade vertical, and house formatting rules for phone numbers, hours, license numbers, and years in business.

## Relationship to voiceMap.md (v0.8+)

<!--
Reconciliation framing (voiceMap.md owns register identity and surface rules;
content-rules.md owns copy discipline, sample outputs, and DO/DO NOT patterns)
is a Wave 1 authoring decision pending Design confirmation in v0.8 Wave 5 prose pass.
If Design reads this division differently, reconcile before Wave 3 cites registers by name.
-->

`references/voiceMap.md` is the canonical source for **register identity** on contractor preview sites — which surfaces (type, borders, link treatment, focus rings, backgrounds, italic policy) belong to each register, how registers couple to backgrounds, when the voice-pivot anchor strip fires, and how the three-tier service composition (Signature / Operational / Distinctive) maps services to registers.

This file is canonical for **copy discipline** inside each register on contractor sites — which section gets which register, approved headline patterns, CTA templates, sample outputs, DO/DO NOT lists, banned phrases.

When a voiceMap.md rule and a content-rules.md rule appear to conflict, voiceMap.md wins for surface/visual identity and content-rules.md wins for copy voice. If they genuinely conflict on the same axis, flag it — that is drift and the rule needs synthesis, not silent resolution.

---

## THE critical clarification: "Plant Street voice" meant two different things

In earlier GRM planning documents (the State of Play, the Saturday Night Addendum, earlier versions of the prospect-site skill), the phrase "Plant Street voice" was used as shorthand for "the GRM editorial voice rules for contractor websites" — no em dashes, real numbers, specific nouns, no filler, no AI tells.

**That usage was loose and wrong.** In GRM_VOICE_SKILL.md, Plant Street is ONE of six specific voices, and it is explicitly a **first-person opinion voice** for agent social media. Sample: "I've watched three houses on my street go up for sale this year." Plant Street has a writer with an "I" and personal stake. That structure does not work for a contractor's own homepage because a contractor website has no first-person writer.

**What the earlier documents were actually describing** are the GRM UNIVERSAL RULES that apply to all six voices (no em dashes, specific nouns, real numbers, banned phrases, no AI tells). Those universal rules are the GRM house style. Individual voices sit on top of them.

**For v0.7 and forward:** when you see "Plant Street voice" in old planning documents, mentally translate it to "GRM universal rules." When you see "Plant Street voice" in content-rules.md or in GRM_VOICE_SKILL.md, it refers specifically to the first-person opinion voice, which is NOT used in contractor preview sites.

---

## Voice mapping for contractor preview sites (v0.7)

Phase 5 assigns voices by section according to this table. Every line of generated copy on a contractor site uses exactly one voice, determined by which section it belongs to. Phase 5 must state the voice out loud before generating copy for that section (the voice skill's Step 5 rule).

| Section | Voice | Why |
|---|---|---|
| Hero headline + subheadline | **Closing Table** | Data-forward, sharp, short punchy paragraphs. Matches the "real number, real fact, real action" headline patterns. |
| Promo bar (if rendered) | **Closing Table** | Contrarian data point, specific pricing, clean close. |
| Trust marquee labels | **Saturday Morning** | Clean, informational, forward-moving. Credential statements are short and factual. |
| Services grid section header | **Saturday Morning** | Transition headline that announces the services ahead. Soft call: could be Closing Table. Currently Saturday Morning for voice variety. |
| Service card descriptions | **Closing Table** | Mentor giving the real answer. 1-2 sentence benefit-first descriptions for hiring decisions. |
| Stats section (eyebrow, title, labels) | **Closing Table** | The voice literally built around "numbers and specifics". Perfect match. |
| Before/after section header | **Closing Table** | Proof is a data point. Contrarian mentor voice fits. |
| Testimonials section header | **Saturday Morning** | Connects individual reviews to the community story. Upbeat and grounded. |
| Featured promotion callout | **Closing Table** | Contrarian insight ("do not be a victim") plus pricing plus specific action. |
| FAQ questions and answers | **Closing Table** | Warm precision. Real answer instead of polite answer. Exactly what a homeowner wants from a contractor FAQ. |
| Contact form headline + subhead | **Saturday Morning** | Upbeat informational. Lead with what happens when they submit. |
| Footer tagline | **Front Porch** | Warm, people-first, identity grounding. Creates a moment of warmth at the end of the page and echoes the About page voice. |
| About page (full long-form) | **Front Porch** | Scene-driven, people-first, specific concrete nouns. The voice skill's sample output is under 200 words and works at that length for owner stories. |

### Voices NOT used in v0.7

Three voices from GRM_VOICE_SKILL.md are intentionally not used on contractor preview sites:

- **Plant Street** — first-person opinion voice, wrong POV for a business site
- **The Welcome Mat** — newcomer-oriented voice, wrong reader (contractor site readers are homeowners with a problem, not new arrivals learning the area)
- **The Deep Roots** — literary long-form voice that the voice skill explicitly reserves for 1,500+ word pieces, which contractor About pages typically are not

These three voices remain in the GRM voice library for their intended use cases (agent social media, homeowner guides, magazine cover features). They are simply out of scope for the prospect-site skill.

### Voice selection protocol for Phase 5

Before writing any section of a contractor preview site, Phase 5 must:

1. Identify the section (hero, services, stats, testimonials, etc.)
2. Look up the voice in the mapping table above
3. State the voice out loud before generating copy: *"Writing the hero in Voice 4: The Closing Table."*
4. Generate the entire section in that single voice from first word to last
5. Never blend voices within a section
6. Never reassign a voice mid-section

The "one piece = one voice" rule from GRM_VOICE_SKILL.md is adapted here for contractor websites: **one SECTION equals one voice**. A contractor website is a multi-section document, not a single piece, so voices can vary by section purpose. But within a section, one voice rules.

---

## Universal GRM rules (synced excerpt from GRM_VOICE_SKILL.md)

These rules apply to ALL six voices and to every line of copy on every generated section of every contractor preview site. Phase 5 enforces them during generation. Phase 6 check 4 verifies them at build time via grep and structural analysis.

1. **Specificity over generality.** Name the street. Name the restaurant. Name the city. Name the license number. "Dunnellon electrician" beats "local electrician". "Florida license EC13007855" beats "fully licensed".

2. **Concrete nouns over abstract ones.** "Front porch" beats "outdoor living space". "Panel upgrade" beats "electrical improvement". "989 five-star reviews" beats "stellar reputation".

3. **Active voice.** "She sold 47 homes" not "47 homes were sold by her". "Ben wired the panel" not "The panel was wired by Ben". Present tense where possible.

4. **Earned emotion over stated emotion.** Show the moment. Do not label the feeling. Never describe work as "heartwarming", "inspiring", or "truly remarkable".

5. **One idea per paragraph.** White space is not wasted space. Paragraphs are 1-3 sentences in most sections, never more than 4.

6. **Real quotes over paraphrasing.** Let people talk in their own words. Testimonials use verbatim quotes from Phase 2 capture. Never paraphrase a testimonial.

7. **Every piece must contain at least one local reference a non-local would not understand.** Marion County names, specific street references, named neighborhoods, Florida-specific context (lightning capital, hurricane prep, The Villages).

8. **No AI tells.** See banned words list below.

---

## Banned words and phrases (synced from GRM_VOICE_SKILL.md)

Every line of generated copy is checked against this list during Phase 5 generation. Phase 6 check 4 runs a grep pass at build time and fails the build if any banned phrase appears in generated HTML.

### Corporate jargon and AI tells

- "In today's [anything]" / "In the ever-changing landscape" / "In this day and age"
- "It's important to [anything]" / "It is important to note"
- "When it comes to" / "At the end of the day"
- "Passionate about" / "Dedicated to" / "Committed to excellence"
- "Navigate" (metaphorical) / "Leverage" (as verb) / "Unlock" (as metaphor)
- "Game-changer" / "Dive into" / "Deep dive" / "Robust" / "Seamless" / "Seamlessly"
- "Elevate" / "Utilize" / "Thrilled to announce" / "Don't miss out!"
- "Something for everyone" / "Hidden gem" / "Vibrant community" / "Nestled in"
- "Boasts" / "Stunning" / "Curated" / "Unique" / "Authentic" / "Journey"
- "Experience" (as verb) / "Discover" / "Explore" + abstract noun / "Transform"
- "Empower" / "Holistic" / "Personalized" / "Cutting-edge" / "Next-level"
- "Moving forward" / "In the realm of" / "As we navigate" / "Touch base"
- "Take it to the next level" / "Truly" / "Heartwarming" / "Inspiring" (as label)
- "Strive to" / "Pride ourselves on" / "Going the extra mile" / "Exceed expectations"
- "100% satisfaction guaranteed" / "Your satisfaction is our priority"
- "Stakeholders" / "Synergy" / "Value proposition" / "Ecosystem" / "Touchpoint"
- "Circle back" / "Low-hanging fruit" / "Move the needle" / "Boil the ocean"
- "Turnkey solution" / "Scalable" (non-technical) / "Best in class" / "Top-notch"
- "State of the art" / "World-class" / "Industry-leading" / "Second to none"
- "Premier" / "Unparalleled" / "Unmatched"
- "One-stop shop" / "Full-service" / "Your trusted partner"
- "Your local [anything]" / "The company you can trust" / "Quality you can count on"
- "We're here for you" / "We've got you covered" / "Look no further"
- "We understand that" / "Rest assured" / "Let us help you"
- "Whether you need" / "Whether you're looking for"
- "From start to finish" / "Above and beyond" / "Every step of the way"
- "Around the clock" (use "24/7" only if literally true)

### Banned credential and trust claims (conditional on profile.json)

The following words and phrases must NEVER appear in generated output unless profile.json contains the specific credential, number, or issuing body that supports the claim.

Agents will reach for these words to fill "confidence slots" in titles, hero copy, og:title, meta descriptions, and JSON-LD even when Phase 1/2 did not capture supporting data. Phase 6 check 3 (Banned output check) greps for each of these. Any hit without a corresponding profile.json field fails the build.

Banned unless captured:

    "Licensed"        requires profile.license_number
    "Insured"         requires profile.insurance_carrier or insurance_note
    "Bonded"          requires profile.bond_number or bond_note
    "Certified"       requires profile.certifications[] (non-empty)
    "Accredited"      requires profile.accreditations[] (non-empty)
    "Award-winning"   requires profile.awards[] (non-empty)
    "Award winning"   same — also banned without hyphen
    "Trusted"         generic trust label — always banned standalone
    "Premier"         generic superlative — always banned
    "Leading"         generic superlative — always banned
    "Top-rated"       requires review data that supports it
    "Top rated"       same — also banned without hyphen
    "Best in [area]"  always banned unless from quoted testimonial
    "#1 in [area]"    always banned unless profile.ranking_source

Agents must not paraphrase around this list. "Fully licensed" counts. "Licensed professionals" counts. "A licensed contractor" counts. The word "licensed" itself is the trigger. Same pattern applies to every other term — any sentence containing the banned root fails check 3 unless the supporting profile field exists.

If the prospect's own website uses one of these claims, Phase 1 must capture the supporting data and store it in the appropriate profile.json field. Only then may the generated site repeat the claim. If Phase 1/2 cannot verify, the claim does not ship.

Grandview F4 2026-04-16 context: agent-generated title read "Licensed Ocala Landscaping Since 1999" — "Licensed" was fabricated. Chad F3 2026-04-16 context: agent-generated hero copy read "124 five-star reviews" — the "124" was correct but the "five-star" was fabricated (actual rating 4.4/5). This list stops both patterns at the banned-phrase grep layer.

### CTA trailing-fragment hallucinations (HTML slop)

Hallucinated structural elements that leak into generated HTML even when no template authorizes them. Claude Code pattern-matches on "this is a CTA section" and invents training-data-style fine-print, SMS opt-out copy, or secondary buttons that are not defined in `section-patterns.md` or `hero-patterns.md`. Bug 2 from A-1 Payless Septic flagship (2026-04-15). Every instance is slop.

- `<small>` — any appearance of the tag. The GRM design system has zero legitimate uses of `<small>`. Every instance in generated HTML is a hallucination.
- `Reply within` — SMS disclaimer opener ("Reply within 24 hours" and variants). Never belongs beneath a CTA.
- `Reply STOP` — SMS opt-out language. Contractor sites do not send marketing texts; this copy is pure pastiche.
- `Or reply` — trailing "Or reply..." fallback copy invented beneath CTA buttons.

Phase 6 check 3 greps for all four patterns. Any hit fails the build.

### The test for any phrase not on this list

If the phrase could appear verbatim on a competitor's homepage in the same vertical, it fails. If the phrase only makes sense for THIS specific prospect with THEIR specific captured facts, it passes.

---

## Banned characters in customer output

**Em dashes.** House rule. Never. Use commas, periods, or sentence breaks instead. This is the single most recognizable AI punctuation tell. Phase 6 check 4 greps for both the UTF-8 em dash character and the HTML entity `&mdash;` and fails the build on any hit.

**Ellipses for drama.** "Something big is coming..." reads as AI hesitation. Use a period and start a new sentence.

**Exclamation points for manufactured warmth.** One in a real emergency callout is fine. Zero is usually better. Three in a single headline is never.

**Semicolons in body copy.** Not banned for being wrong, banned for being overkill. Break the sentence in two.

**Colons for dramatic single-word reveals.** "There's one thing every top contractor has: consistency." Banned. Colons are for lists and formal introductions only.

**Hyphen strings.** "A community-first, results-driven, locally-rooted approach." Banned. Rewrite as plain sentences.

**Oxford comma.** House style: ALWAYS use the Oxford comma. "Residential, commercial, and industrial wiring." Not "Residential, commercial and industrial wiring."

**ALL CAPS except for eyebrow text and button labels.** Eyebrow text ("OUR SERVICES", "BY THE NUMBERS") is uppercase by design. Button labels can be uppercase. Body copy is never all caps.

**Emoji.** Never. Not in headlines, not in testimonials, not in CTAs, not in FAQs. No exceptions.

---

## The anti-AI test

Apply this to every paragraph before it ships. Phase 5 runs the test during generation. Phase 6 check 5 flags anything suspicious.

1. **Read it aloud.** If it sounds like a chatbot, rewrite it.
2. **Swap the business name.** If the paragraph could apply to any business in any industry by swapping one word, rewrite it.
3. **Remove the specific nouns.** If you can remove every proper noun and the paragraph still makes sense, it has no specific nouns and needs rewriting.
4. **Reverse the claim.** If the claim's opposite is obviously absurd ("we pride ourselves on quality work" — nobody says they take pride in bad work), the claim has no content and needs replacing.

The grep pass in Phase 6 catches banned phrases mechanically. The four human-judgment tests above catch the soft failures that grep cannot see. Both are required.

---

## The three voices in brief (for Phase 5 reference)

Full voice definitions live in GRM_VOICE_SKILL.md. These short summaries exist so Phase 5 can reference the key rules without fetching the full skill file every time.

**Cross-reference.** The subsections below cover **copy discipline** — structure, DO/DO NOT, sample outputs. Surface-level register identity (type scale, italic policy, borders, link treatment, focus rings, backgrounds, mono register) lives in `voiceMap.md §2a/2b/2c`. When authoring a section, read both.

### Voice 4: The Closing Table (PRIMARY voice for v0.7 contractor sites)

**Description:** Sharp, clean, insight-driven. Assumes a reader who is making a hiring decision and wants the real answer fast. Warm in its precision, like a mentor who gives the real answer instead of the polite one.

**Structure:** Contrarian insight or data point → specifics (numbers, named examples) → address the objection the reader is already thinking → concrete takeaway the reader can act on.

**DO:**
- Open with a contrarian observation or a data point
- Short paragraphs, 2-3 sentences max
- Use numbers and specifics
- Active voice, present tense
- End with an action the reader can take

**DO NOT:**
- Use jargon to sound smart
- Pad with background the reader already knows
- Write puff copy
- Use "at the end of the day" or other filler

**Sample output (for T&F Electric hero):**

> Fifty years. Two Tuccis. One phone number.
>
> Residential, commercial, and industrial wiring across Marion County. Florida license EC13007855.

### Voice 5: Saturday Morning (SECONDARY voice for v0.7 contractor sites)

**Description:** Clear, upbeat, informational. Grounded civic-booster voice. Loves where they live and wants you to know what's happening. Like a well-written email from a friend who is on every committee in town but is not annoying about it.

**Structure:** Lead with the news → one human detail that makes it interesting → brief context → practical details → close clean.

**DO:**
- Lead with news, then add the human angle
- Include practical specifics
- Write with genuine optimism
- Keep sentences clean and forward-moving

**DO NOT:**
- Write like a press release
- Use empty civic language
- Forget the practical details
- Use "Don't miss this!"

**Sample output (for a contact form header):**

> Tell us about the job. We call back within one business hour during weekdays, and faster if it is an emergency.

### Voice 1: The Front Porch (TERTIARY voice for v0.7 contractor sites)

**Description:** Warm, people-first, scene-driven. The writer shows up and notices the dog, the yard, the smell of the kitchen before asking a question. Sensory details do the heavy lifting. The subject is always a person first, a professional second.

**Structure:** Scene opening → introduce through observation → backstory through specifics → close on community connection.

**DO:**
- Open with a scene
- Let subjects speak in their own words when captured
- Use specific concrete nouns
- Let emotion emerge from detail
- End with community, not the individual

**DO NOT:**
- Open with a bio line
- Use "passionate about"
- Flatten someone into their job title
- Use exclamation points to manufacture warmth

**Sample output (for T&F Electric About page opening):**

> Ben Tucci has walked through the same Dunnellon shop door for fifty years. The dog changes every decade or so. The Ford in the lot changes every eight. The phone number on the truck has not changed since 1975.
>
> Ben runs T&F Electric with his wife Wendy. Two Tuccis, one shop, fifty years of Marion County wiring. Most days they are on a job by eight in the morning. Some days they are on a job at two in the morning, because lightning does not wait for business hours in Florida.

---

## Headline patterns (Closing Table voice)

Five approved headline patterns for the hero glass card. Phase 5 picks the best pattern based on what Phase 2 captured. If a pattern's required data is missing, fall through to the next pattern in order. Pattern E is the universal fallback and always works.

All patterns are written in Closing Table voice per the section mapping above.

### Pattern A: The Proof Stack

**Structure:** `[Real number]. [Real fact]. [Real phone or action].`

Three short punchy sentences stacked in the glass card, separated by `<br>` tags in HTML. Reads like a telegram. Maximum density, minimum filler.

**Examples:**

- Johnson Brothers Plumbing: *"989 five-star reviews. One phone number."*
- T&F Electric: *"Fifty years. Two Tuccis. One phone number."*
- Pat Myers Electric: *"948 reviews. All five stars. One call."*
- Starr's & Stripes PowerWash: *"619 five-star reviews. Zero streaks. Same-day quotes."*

**Required data from Phase 2:** at least one strong quantitative claim (review count, years in business, projects completed, or service count).

**When to use:** any prospect with strong quantitative proof. This is the strongest pattern and should be tried first.

### Pattern B: The Time Identity Place

**Structure:** `[Time frame]. [Identity]. [Location].`

Three noun phrases stacked. Works especially well for family-owned businesses where the owners ARE the brand.

**Examples:**

- T&F Electric: *"Fifty years. Two Tuccis. One phone number."* (doubles as Pattern A)
- Johnson Brothers Plumbing: *"Since 2006. Two brothers. All of Marion County."*
- Hefner Plumbing: *"Three generations. One family. Marion County plumbing."*

**Required data:** years in business OR founding year, plus owner identity (family name, generational claim, or founding story) from the Phase 2 About page.

**When to use:** family-owned businesses, businesses with strong owner branding, or businesses where multi-decade continuity is the main differentiator.

### Pattern C: The Service Place

**Structure:** `[Specific service] in [specific place].`

One sentence, specific service, specific location. The safest fallback because every contractor has a service and a place.

**Examples:**

- Johnson Brothers Plumbing: *"Licensed plumbing in Ocala and Marion County since 2006."*
- T&F Electric: *"Licensed electrical work across Dunnellon, Ocala, and The Villages since 1975."*
- Starr's & Stripes PowerWash: *"Pressure washing across Marion County with zero streaks, zero damage, zero excuses."*

**Required data:** service category (always available from Phase 2), city or region (always available from Phase 1 address or Phase 2 service area). Optional: founding year, license number.

**When to use:** universal fallback. If Patterns A, B, and D cannot find their required data, Pattern C always works.

### Pattern D: The Promise Proof

**Structure:** `[Operational promise]. [Proof behind the promise].`

Two sentences. The first states a specific operational claim. The second backs it up with data. Works when the prospect's main differentiator is operational rather than historical.

**Examples:**

- T&F Electric: *"Same-day emergency service, seven days a week. Since 1975."*
- Lucaya Pools: *"Your pool clean every week. 271 five-star reviews say we show up."*
- Getter Done Fence: *"Fences installed in one weekend. 328 reviews say we finish on time."*

**Required data:** a specific operational claim from Phase 2 (24/7 service, same-day response, warranty length, finish time) AND either a review count, review rating, or years in business for the proof.

**When to use:** when the prospect's main competitive advantage is operational (speed, availability, guarantee) rather than scale or longevity.

### Pattern E: The Location Authority

**Structure:** `[Location] calls [business] for [specific service benefit]. [Proof or identity].`

Two sentences. Asserts local authority by naming the place where the reader lives.

**Examples:**

- Johnson Brothers Plumbing: *"Marion County calls Johnson Brothers when the water stops moving. 989 five-star reviews and counting."*
- Pat Myers Electric: *"Ocala calls Pat Myers when the lights go out. 948 reviews, all five stars."*

**Required data:** none hard-required. Works with just business name and location.

**When to use:** when none of Patterns A through D fit well, or when the prospect operates primarily in one identifiable community and authority within that community is the strongest available angle.

### Pattern selection logic for Phase 5

Phase 5 uses this deterministic logic to generate a **candidate headline** that becomes the default shown at the Phase 4 approval gate. The candidate is not final. Ron reviews the candidate at the gate alongside the other design choices and can override it with a different pattern or a custom headline if the candidate lacks punch.

```
CANDIDATE SELECTION:

IF yearsInBusiness captured AND ownerIdentity captured AND phone captured:
    TRY Pattern A (if quant data available) OR Pattern B
ELIF yearsInBusiness captured AND reviewCount captured:
    TRY Pattern A
ELIF operationalPromise captured AND (reviewCount OR yearsInBusiness):
    TRY Pattern D
ELIF primaryCity captured:
    TRY Pattern C (always works if city captured)
ELSE:
    FALL BACK to Pattern E
```

Phase 5 tries Pattern A first. If required data is missing, falls through. Pattern C or E always work as universal fallbacks.

**Editorial override at the Phase 4 approval gate.** The gate displays the candidate headline with the pattern name ("Pattern A: Proof Stack") and a prompt: `Accept candidate, try different pattern, or provide custom headline?` Ron can:

- Type `yes` to accept the candidate
- Type `try Pattern B` (or C, D, E) to regenerate with a different pattern
- Type `custom: Your actual headline here.` to override with a manual headline that bypasses pattern generation entirely

Manual overrides are checked against the banned words list and the em-dash rule but are otherwise preserved verbatim. This is the same editorial override pattern used for the glass card variant decision. Automated pattern generation handles 80 percent of builds, editorial override handles the 20 percent where the automated pick lacks punch or where Ron has a specific editorial instinct.

---

## Subheadline patterns (Closing Table voice)

The hero subheadline sits below the main headline in the glass card. 1-2 sentences. Its job is to expand the headline with specifics the headline could not fit.

### Structure

- **Single-sentence subheadline:** one fact + one credential. Example: *"Residential, commercial, and industrial wiring across Marion County. Florida license EC13007855."*
- **Two-sentence subheadline:** one fact + one credential. Break into two sentences when they read better separated. Example: *"Same-day service, seven days a week across Dunnellon, Ocala, and The Villages. Florida license EC13007855, insured and bonded."*

### Required content

Every subheadline should contain at least two of the following:

1. Primary service (e.g., "electrical wiring", "licensed plumbing", "pressure washing")
2. Service areas (e.g., "Dunnellon, Ocala, and Marion County")
3. License number (e.g., "Florida license EC13007855")
4. Years or founding ("since 1975")
5. An operational claim ("24/7 emergency service", "same-day quotes", "twelve-month warranty")

Never pad a subheadline with filler to hit a word count. Two facts beat five words of filler.

---

## CTA templates (mixed voices)

Every CTA on a contractor preview site is an action verb plus a specific outcome. The reader should know exactly what happens when they click.

### Approved CTA patterns

| CTA text | Voice | When to use |
|---|---|---|
| `Call (352) 555-1234` | Closing Table | Hero primary button, nav phone button, mobile bottom bar. Always tel: linked. |
| `Get a free quote` | Closing Table | Hero secondary button, services page, mid-page CTAs. Jumps to contact form. |
| `Request service` | Saturday Morning | Contact form submit button when the prospect sells services not products. |
| `Schedule a free estimate` | Closing Table | Hero secondary or services page, especially for larger project verticals (roofing, fencing, pools). |
| `Text us now` | Saturday Morning | Mobile-only CTA for prospects who accept SMS. sms: linked. |
| `See our work` | Saturday Morning | Gallery or before/after link from hero or services. |
| `Read the reviews` | Saturday Morning | Links to testimonials page or Google reviews. |

### Banned CTA phrases

These CTA phrases fail because they do not tell the reader what happens next:

- "Learn More"
- "Click Here"
- "Get Started"
- "Find Out More"
- "Discover"
- "Explore"
- "Contact Us" (too generic, use "Call [phone]" or "Get a quote" instead)
- "Submit"
- "Sign Up"

---

## Service description templates (Closing Table voice)

Service card descriptions are 1-2 sentences, benefit-first, concrete nouns. Generated from Phase 2 captured service lists with light Closing Table tightening.

### Length rules

- **Standard service card:** 1 sentence, 12-20 words
- **Featured service card (2x2 Bento):** 1-2 sentences, 15-35 words, can include a specific benefit or guarantee

### Structure patterns

**Pattern: [Service]. [Concrete outcome or scope].**
- *"Whole house surge protection. Protect your flat screen TVs, appliances, and electronics from Florida lightning."*
- *"Panel upgrades for older Ocala homes. From 100-amp to 200-amp service in one day."*
- *"Pressure washing for driveways, walkways, and pool decks. Safe on concrete, pavers, and stone."*

**Pattern: [Service] for [specific audience or situation].**
- *"Residential electrical work for new construction, renovations, and additions across Marion County."*
- *"Commercial plumbing for Ocala restaurants, offices, and retail buildings."*
- *"Emergency roofing tarp installs for storm damage before the adjusters arrive."*

**Pattern: [Service]. [Operational promise].**
- *"Generator installations. Turnkey with your choice of brand, propane or natural gas."*
- *"Tankless water heater conversions. Same-day service across Dunnellon and Ocala."*
- *"Weekly pool cleaning. We show up the same day every week, rain or shine."*

### Rules

- Service name is verbatim from Phase 2 capture, never paraphrased or rebranded
- Description is 1-2 sentences, benefit-first
- At least one concrete noun per description (brand, material, location, specific outcome)
- No generic descriptions like "quality work you can trust" or "professional service"
- If Phase 2 captured 12 services, generate 12 descriptions, do not collapse

---

## Section content rules

Each section has specific content requirements beyond voice. Phase 5 enforces these during generation.

### Hero glass card

- Eyebrow: `[PRIMARY CITY] · SINCE [YEAR]` (uppercase, spaced bullet). If no founding year captured, use `[PRIMARY CITY]` alone.
- Headline: one of the five Patterns above, Closing Table voice
- Subheadline: 1-2 sentences, Closing Table voice, required content per subheadline rules
- Stats mini-bar: exactly 3 stats (years, reviews, hours/emergency, or similar real numbers)
- Primary CTA: `Call [formatted phone]`
- Secondary CTA: `Get a quote`
- Badge (top-right corner): star rating + review count if captured

### Trust marquee

- 5-7 short credential labels
- Real credentials only (license numbers, BBB, insurance, certifications, years)
- Labels are 3-8 words each
- Examples: `★ 4.6 Rating on Google`, `Florida License EC13007855`, `50+ Years in Business`, `24/7 Emergency Service`, `Licensed & Insured`
- Duplicate the label set once for seamless marquee loop

### Services grid

- Section eyebrow: `OUR SERVICES` (or vertical-specific equivalent like `ELECTRICAL SERVICES`)
- Section title: Saturday Morning voice, 1 sentence. Examples: *"Twelve services. One licensed team."* or *"Every job, every day, across Marion County."*
- Section subtitle: 1 sentence, practical. Example: *"Residential, commercial, and industrial work from Dunnellon to The Villages."*
- Service cards: one per captured service, Closing Table voice, service description templates above
- Featured card (2x2): exactly one per grid, background photo, 2-sentence description

### Stats section (THE dark section)

- Section eyebrow: `BY THE NUMBERS`
- Section title: Closing Table voice, 1 sentence. Examples: *"Real work. Real results."* or *"Fifty years in four numbers."*
- Stats: exactly 3 or 4, real numbers only from Phase 2 capture
- Animated stats (whole numbers): use `data-target` attribute for the numberTicker primitive
- Static stats (non-integer values like 4.6★, 24/7, A+): plain text, no `data-target`

### Before/after gallery

- Section eyebrow: `SEE THE DIFFERENCE`
- Section title: Closing Table voice, 1 sentence. Example: *"Real projects across Marion County."*
- Only renders if Phase 3 captured at least one before/after pair
- Labels on slider: always `BEFORE` and `AFTER` uppercase

### Testimonials

- Section eyebrow: `REAL REVIEWS`
- Section title: Saturday Morning voice, 1 sentence. Example: *"What Marion County says about T&F Electric."*
- Rating line: real star count and real review count (`4.6 from 41 Google reviews`)
- Cards: every captured testimonial with real first name, city, verbatim quote, star rating

### Featured promotion callout

- Eyebrow: `LIMITED TIME` or `SPECIAL OFFER`
- Title: Closing Table voice, 1-2 sentences. Example: *"Whole House Surge Protection. $450."*
- Subtitle: 1 sentence context. Example: *"Florida is the lightning capital of the United States. Do not be a victim of the next storm."*
- CTA: `Call (formatted phone)`
- Only renders if Phase 2 captured a real promotion with real pricing

### FAQ accordion

- Section eyebrow: `FAQ`
- Section title: Closing Table voice, 1 sentence. Example: *"Common questions."* or *"Real answers, not polite ones."*
- 5-7 questions per prospect, generated from FAQ templates per vertical below

### Contact form

- Section title: Saturday Morning voice, 1 sentence. Example: *"Tell us about the job."*
- Subtitle: 1 sentence with operational promise. Example: *"We call back within one business hour during weekdays, and faster if it is an emergency."*
- Side panel: real phone, email, address, hours from Phase 2 capture

### Footer

- Brand section tagline: Front Porch voice, 1-2 sentences, warm and identity-grounding. Example: *"Ben and Wendy Tucci have run T&F Electric out of the same Dunnellon shop for fifty years. The phone number on the truck has not changed since 1975."*
- Copyright year: current year from Phase 4
- License info: real license number next to copyright

---

## Standalone pages and service sub-pages

v0.7 contractor sites always generate the five required pages: `index.html`, `about.html`, `services.html`, `testimonials.html`, `contact.html`. Some prospects also have deeper site architectures with dedicated sub-pages per service, dedicated project galleries, or specific landing pages that do not fit into the five-page required set. This section defines how Phase 5 handles those.

### Required standalone pages (already in SKILL.md Phase 5)

- `index.html` — the homepage, full spec above
- `about.html` — company story, owner profile, credentials, history
- `services.html` — full services list with descriptions
- `testimonials.html` — reviews and testimonials
- `contact.html` — contact form, map, hours, service area

These five exist on every build. They are essentially homepage sections broken out to their own pages. A standalone page uses the same section patterns from `section-patterns.md` with a page-specific lead section replacing the homepage hero. Voice assignments per section match the homepage mapping table above: About page gets Front Porch, services page uses Closing Table for service descriptions and Saturday Morning for the section header, and so on.

### Optional standalone pages (already spec'd in SKILL.md Phase 5)

- `gallery.html` — renders if Phase 3 captured 6+ quality project images
- `specials.html` — renders if a real featured promotion was captured with real pricing
- `emergency.html` — renders if 24/7 emergency service is a major differentiator

### Service sub-pages (NEW in v0.7, conditional generation)

Some prospects have dedicated sub-pages for specific services. T&F Electric has seven: Residential, Commercial, Industrial, Generators, Panel Upgrades, Surge Protection, and Landscape Lighting. A painter might have Interior Painting, Exterior Painting, and Cabinet Refinishing. Phase 5 must handle these intentionally.

**The conditional rule.** Phase 5 generates a service sub-page IF all three conditions are met:

1. The prospect's existing site has a dedicated page for that service (not just a section on the main services page)
2. Phase 2 captured at least 250 words of original content from that page (not boilerplate, not duplicated from the homepage or main services page)
3. At least ONE of: a unique photo for this service, a unique testimonial specifically mentioning this service, pricing or package info specific to this service, or process details the main services page does not cover

If all three conditions hit, Phase 5 writes `services/[service-slug].html` (note the subdirectory). The homepage services grid card for that service links to the sub-page. If any condition fails, the service rolls into the homepage services grid card and no sub-page is generated. This rule honors the "never fabricate" constraint: we only build depth when the prospect already has real depth.

**Service slug format.** Lowercase, hyphenated, no special characters. Examples: `residential-electrical`, `whole-house-surge-protection`, `interior-painting`, `panel-upgrades`. Phase 5 derives the slug from the captured service name with standard slugification.

**Sub-page structure.** A service sub-page is NOT a full homepage. It is a focused landing page for one specific service. Sections in order:

1. **Nav** — shared component, identical to homepage
2. **Sub-hero** — simpler than homepage hero. No four-mode glass card. A single section with: eyebrow (`[SERVICE NAME] IN [PRIMARY CITY]`), headline (Closing Table voice, 1 sentence specific to this service), subheadline (1-2 sentences with credentials and operational claim), single photo background if captured for this service, two CTAs (`Call [phone]` and `Get a quote`). Full pixel-level spec will be added to `section-patterns.md` during polish pass.
3. **Main content block** — the captured sub-page content, Closing Table voice, preserving specific facts verbatim. 300-800 words typical. Uses the standard 860px narrow container from css-framework.md.
4. **Service-specific proof** — if Phase 2 captured testimonials that specifically mention this service, render 2-3 of them as a card strip. Same testimonial card styling as the homepage testimonials section. If no service-specific testimonials exist, omit this block entirely.
5. **Service-specific FAQ** — 3-5 questions from the vertical FAQ templates, filtered to questions relevant to this specific service. Closing Table voice. Uses the same accordion pattern as the homepage FAQ section.
6. **Contact CTA section** — not the full contact form. A simplified callout with the headline *"Ready to talk about your [service name]?"*, the real phone number, and a button linking to `/contact.html`. Saturday Morning voice for the headline.
7. **Footer** — shared component, identical to homepage

**Sub-page voice mapping.** Same as the homepage mapping by section purpose:

| Sub-page section | Voice |
|---|---|
| Sub-hero eyebrow, headline, subheadline | Closing Table |
| Main content block | Closing Table |
| Service-specific proof (testimonials) | Verbatim customer voice in quotes, Saturday Morning for header |
| Service-specific FAQ | Closing Table |
| Contact CTA callout | Saturday Morning |
| Footer tagline | Front Porch |

**Sub-page content rules.**

- Never fabricate content to fill a sub-page. If Phase 2 captured 250 words, use those 250 words. Do not pad.
- Preserve all specific facts verbatim: brand names, license numbers, pricing, warranty terms, process steps.
- Rewrite generic AI-sounding copy in Closing Table voice, but preserve the factual content.
- Service name at the top of the sub-hero is verbatim from Phase 2, never rebranded.
- Primary photo is the best photo Phase 3 assigned to this specific service, or a neutral hero photo from the prospect's general library if no service-specific photo exists.
- If the sub-page content includes a service-specific promotion or pricing, render it prominently in the main content block.

### Pages explicitly OUT of scope for v0.7

Phase 5 does NOT generate these page types in v0.7 regardless of what Phase 2 captured:

- **Location sub-pages.** "Ocala Electrician", "Dunnellon Electrician", "The Villages Electrician" as separate pages. These are SEO plays. The homepage and footer already name all service areas. Dedicated location pages are deferred to v0.8 as a paid client upsell.
- **Blog pages, news pages, resource pages.** Most contractors do not have substantive blog content. When Phase 2 captures a blog link, Phase 5 ignores it. A dedicated blog becomes a v0.8 feature for clients who want ongoing content marketing.
- **Financing pages, warranty pages, insurance pages.** These roll into homepage sections (promo callout, FAQ, trust marquee) rather than getting standalone pages. A financing offer goes in the featured promotion callout with the partner name and terms. A warranty commitment goes in the FAQ. Insurance goes in the trust marquee.
- **Separate project portfolio pages.** If Phase 3 captured 6+ project images, they render in `gallery.html` and optionally in the homepage before/after section. No separate per-project portfolio pages.
- **Team or staff pages.** Owner content goes on the About page. If a prospect has a dedicated team page with multiple staff bios, the content rolls into the About page team section. No separate `team.html`.

### Decision table for Phase 5

When Phase 5 evaluates Phase 2's captured pages against the standard site structure, use this decision table:

| Captured page type | Phase 5 handling |
|---|---|
| Homepage | → `index.html` |
| About page | → `about.html` |
| Main services page | → `services.html` |
| Individual service sub-page with 250+ words | → `services/[slug].html` (conditional) |
| Individual service sub-page with under 250 words | Roll into homepage and services.html card for that service |
| Testimonials or reviews page | → `testimonials.html` |
| Contact page | → `contact.html` |
| Gallery or portfolio page | → `gallery.html` (if 6+ images) |
| Specials or promotions page | → `specials.html` (if real pricing captured) |
| Blog or news page | Ignored in v0.7 |
| Financing page | Content rolled into promo callout on homepage |
| Warranty page | Content rolled into homepage FAQ |
| Insurance page | Content rolled into trust marquee |
| Location sub-pages | Ignored in v0.7 (deferred to v0.8) |
| Team or staff page | Content rolled into about.html team section |
| Employment or careers page | Ignored in v0.7 |
| Coupons or discounts page | Rolled into promo callout if real pricing captured |

When a prospect has a captured page type not listed above, Phase 5 asks: does this content fit into an existing homepage section? If yes, roll it in. If no, report to Ron at the Phase 4 approval gate and let him decide whether to generate a custom standalone page for that build.

### Sub-page self-check (adds to the general self-check list)

Before marking sub-pages complete, Phase 5 verifies:

- [ ] Every generated sub-page has at least 250 words of real captured content
- [ ] Every sub-page links back to homepage via the nav
- [ ] Every sub-page's services grid card on the homepage links to the sub-page URL
- [ ] No sub-page was generated for a service where Phase 2 captured only boilerplate or minimal content
- [ ] Every sub-page's contact CTA links to `/contact.html`, not a duplicated contact form
- [ ] Every sub-page uses the Closing Table voice for content and Saturday Morning for the contact CTA callout

---

## FAQ templates per vertical

Nine verticals covered. Each vertical has 7 FAQ templates. Phase 5 picks 5-7 per build based on which questions Phase 2 captured real answers for. Answers are filled in from `profile.json` data, never fabricated.

All FAQ content uses Closing Table voice: warm precision, real answers instead of polite answers, no filler.

### Electrician FAQ templates

1. **Q:** Do you offer 24/7 emergency electrical service?
   **A structure:** Yes/no answer → service area → phone number → any conditions (overtime charges, minimum call-out fee)
   **Only include if:** Phase 2 captured whether emergency service is offered

2. **Q:** Are you licensed and insured in Florida?
   **A structure:** Yes + exact license number + insurance confirmation + years holding license
   **Only include if:** Phase 2 captured license number

3. **Q:** How quickly can you come out for a service call?
   **A structure:** Response time commitment → service area → what counts as emergency
   **Only include if:** Phase 2 captured response time or operational claims

4. **Q:** Do you service older homes in Ocala and Marion County?
   **A structure:** Yes → specific older home services (knob-and-tube replacement, aluminum wiring, panel upgrades) → experience with historic homes
   **Only include if:** Phase 2 captured residential electrical service

5. **Q:** Can you install a whole house generator?
   **A structure:** Yes → brands offered → fuel types (propane, natural gas) → installation timeline
   **Only include if:** Phase 2 captured generator services

6. **Q:** What does a panel upgrade cost?
   **A structure:** Price range if Phase 2 captured it → what is included → timeline
   **Only include if:** Phase 2 captured panel upgrade services. If no pricing captured, omit this FAQ.

7. **Q:** Do you offer financing for larger electrical projects?
   **A structure:** Yes/no → financing partner name → typical terms
   **Only include if:** Phase 2 captured financing options. Never fabricate a financing partner.

### Plumber FAQ templates

1. **Q:** Do you offer 24/7 emergency plumbing?
   **A structure:** Yes/no → service area → phone → after-hours pricing

2. **Q:** Are you licensed and insured in Florida?
   **A structure:** Yes + license number + insurance + years licensed

3. **Q:** How long will a water heater replacement take?
   **A structure:** Same-day typical, brand options, tankless vs tank, warranty

4. **Q:** Do you install tankless water heaters?
   **A structure:** Yes → brands → gas vs electric → typical install day length

5. **Q:** Can you handle slab leaks?
   **A structure:** Yes → detection method → repair approach → typical timeline
   **Only include if:** Phase 2 captured slab leak service

6. **Q:** Do you offer a warranty on your work?
   **A structure:** Warranty length → what is covered → what voids it
   **Only include if:** Phase 2 captured warranty terms. Never fabricate.

7. **Q:** What is your service area?
   **A structure:** List of cities from Phase 2 service area capture

### Pressure washer FAQ templates

1. **Q:** Can you clean pavers without damaging them?
   **A structure:** Yes → PSI used → soft wash vs pressure wash explanation → sealer reapplication offered

2. **Q:** Do you do house soft wash?
   **A structure:** Yes → chemical safety → safe for plants → algae kill guarantee

3. **Q:** How much does pressure washing a driveway cost?
   **A structure:** Price range if captured → size factors → prep required
   **Only include if:** Phase 2 captured pricing. Never fabricate.

4. **Q:** Can you remove rust stains from concrete?
   **A structure:** Yes/no → treatment type → guarantee on removal

5. **Q:** Do you work on commercial buildings?
   **A structure:** Yes/no → largest project size → scheduling for after-hours

6. **Q:** How often should I pressure wash my house in Florida?
   **A structure:** Once a year recommended → algae climate → sooner if black streaks visible

7. **Q:** Are you insured?
   **A structure:** Yes → general liability coverage amount → worker comp status

### Roofer FAQ templates

1. **Q:** Do you work with insurance claims?
   **A structure:** Yes → process description → assistance with adjuster meetings

2. **Q:** How long does a roof replacement take?
   **A structure:** 1-3 days typical depending on size → weather dependent → cleanup commitment

3. **Q:** What roofing materials do you install?
   **A structure:** Shingle brands, metal, tile options from Phase 2

4. **Q:** Do you offer a labor warranty on top of the manufacturer warranty?
   **A structure:** Length of labor warranty → what is covered
   **Only include if:** Phase 2 captured warranty terms

5. **Q:** Can you do emergency tarp installs?
   **A structure:** Yes → response time → cost structure for emergency calls

6. **Q:** Are you licensed and insured?
   **A structure:** Florida roofing license number + insurance confirmation

7. **Q:** Do you offer free estimates?
   **A structure:** Yes → how to schedule → what the estimate includes

### Pool FAQ templates

1. **Q:** Do you offer weekly pool maintenance?
   **A structure:** Yes → weekly visit scope → chemicals included → pricing structure if captured

2. **Q:** Can you handle green pool recovery?
   **A structure:** Yes → typical timeline → cost factors → prevention after cleanup

3. **Q:** Do you build new pools or only service existing ones?
   **A structure:** Yes/no to new builds → design process if applicable → timeline

4. **Q:** What brands of equipment do you service?
   **A structure:** Pump, filter, heater brands from Phase 2

5. **Q:** Can you install a pool heater?
   **A structure:** Yes → gas vs electric vs heat pump → brand options → sizing consultation

6. **Q:** Do you service salt water pools?
   **A structure:** Yes → cell cleaning → salt level monitoring → conversion consultations

7. **Q:** What is your service area?
   **A structure:** List of cities from Phase 2 capture

### Painter FAQ templates

1. **Q:** Do you do interior and exterior painting?
   **A structure:** Yes → residential and commercial → exterior wash and prep included

2. **Q:** What brands of paint do you use?
   **A structure:** Brands from Phase 2 capture → premium vs contractor grade options

3. **Q:** How long will an interior paint job take?
   **A structure:** Room count based → prep time → cure time before furniture moves back

4. **Q:** Do you move furniture?
   **A structure:** Yes/no → what gets covered → prep requirements for homeowner

5. **Q:** Do you offer a warranty on your paint work?
   **A structure:** Warranty length → what is covered → peeling, fading, adhesion terms
   **Only include if:** Phase 2 captured warranty

6. **Q:** Can you do cabinet painting?
   **A structure:** Yes/no → spray vs brush → primer and finish coats → typical timeline

7. **Q:** Do you offer free estimates?
   **A structure:** Yes → how to schedule → on-site visit standard

### Pest control FAQ templates

1. **Q:** Do you treat for termites?
   **A structure:** Yes → treatment methods → warranty → monitoring plans

2. **Q:** Are your treatments safe for pets and kids?
   **A structure:** Yes → return time after application → product certifications

3. **Q:** Do you offer monthly, quarterly, or one-time service?
   **A structure:** Plan options from Phase 2 → pricing structure if captured → contract terms

4. **Q:** Can you treat rodent problems?
   **A structure:** Yes → trapping vs baiting approach → sealing and exclusion service

5. **Q:** Do you handle wildlife like raccoons or squirrels?
   **A structure:** Yes/no → trapping and relocation → attic cleanup after removal

6. **Q:** What pests are covered in your standard plan?
   **A structure:** List from Phase 2 capture: ants, roaches, spiders, silverfish, etc.

7. **Q:** Do you offer same-day service for emergencies?
   **A structure:** Yes/no → phone for emergency line → what qualifies as emergency

### HVAC FAQ templates

1. **Q:** Do you offer 24/7 emergency AC repair?
   **A structure:** Yes/no → response time → after-hours fees

2. **Q:** How often should I change my AC filter in Florida?
   **A structure:** Every 1-3 months → climate factors → pet households more frequent

3. **Q:** Do you offer maintenance plans?
   **A structure:** Plan tiers from Phase 2 → what is included → pricing if captured

4. **Q:** What AC brands do you install?
   **A structure:** Brands from Phase 2 → warranty length → efficiency ratings

5. **Q:** How long does a new AC install take?
   **A structure:** Typical 1-day install → equipment size factors → ductwork considerations

6. **Q:** Do you do duct cleaning?
   **A structure:** Yes/no → method → indoor air quality benefits

7. **Q:** Do you offer financing for a new system?
   **A structure:** Yes/no → financing partner name → typical terms
   **Only include if:** Phase 2 captured financing

### Fencing and landscaping FAQ templates

1. **Q:** What fence materials do you install?
   **A structure:** Wood, vinyl, aluminum, chain link from Phase 2 → pros and cons

2. **Q:** How long will a fence install take?
   **A structure:** 1-3 days typical → yard size factor → permit and dig requirements

3. **Q:** Do you pull permits and handle dig tickets?
   **A structure:** Yes → 811 utility marking → HOA coordination if needed

4. **Q:** What is your warranty?
   **A structure:** Labor and material warranty terms → what voids
   **Only include if:** Phase 2 captured warranty

5. **Q:** Can you match an existing fence on my property?
   **A structure:** Yes → material sourcing → color matching

6. **Q:** Do you do gates with automatic openers?
   **A structure:** Yes/no → brands → power source options

7. **Q:** Do you offer free estimates?
   **A structure:** Yes → on-site measurement included → typical turnaround

---

## House formatting style

Mechanical rules for how specific content types are written. Applied regardless of voice.

### Phone numbers

**Display format:** `(352) 465-4600`
- Parenthesized area code
- Space after closing paren
- Hyphen between prefix and line number
- No dots, no dashes before area code

**tel: link format:** `+13524654600` (E.164, no spaces or punctuation)

**Phone number in body copy:** use the display format, e.g., *"Call (352) 465-4600 any time."*

**Multiple phone numbers:** list each on its own line or separated by periods, never by "or". Example: *"Residential: (352) 465-4600. Commercial: (352) 465-4700."*

### Hours of operation

**Display format:** `Mon-Fri 8am-5pm`
- Hyphen between day range
- Space before time
- Lowercase am/pm
- Hyphen between start and end times
- No minutes unless non-zero (`8am-5:30pm` is fine)

**Multiple time blocks:** separate with comma. Example: *"Mon-Fri 8am-5pm, 24/7 Emergency"*

**Closed days:** state explicitly. Example: *"Mon-Fri 8am-5pm, Closed weekends"* (only if Phase 2 captured closed status, never assume).

**Fallback:** if Phase 2 captured no hours, omit the hours block entirely. Never fabricate.

### License numbers

**Display format:** `Florida License EC13007855`
- "Florida License" capitalized (state name spelled out, word "License" capitalized)
- License number follows with no hyphen or "#" sign
- License category prefix (EC, CFC, CAC, CGC, etc.) is part of the license number and stays uppercase

**In body copy:** *"Florida License EC13007855. Licensed and insured since 1975."*

**Multiple licenses:** list each on its own line. Example:

> Florida License EC13007855 (Electrical)
> Florida License CGC1509876 (General Contractor)

### Years and founding dates

**Founding year:** `Since 1975` (capitalized, no comma)
**Years in business:** `50 years` or `Fifty years` (spell out under 20, numeral over 20, house style preference is to spell out round numbers under 100)
**Decades:** `Over 30 years` or `Three decades` (pick one per build, never mix in same section)

**In headlines:** prefer spelled-out numbers for impact (*"Fifty years. Two Tuccis."* reads stronger than *"50 years. Two Tuccis."*).

**In body copy:** numerals for precision, spell out for rhythm. Both are fine.

### Business names

**Use what is on the prospect's actual site, verbatim.** Never normalize spacing or punctuation.

- T&F Electric (no spaces around ampersand, even if their site uses "T & F Electric" in some places, check what the header or logo uses)
- Johnson Brothers Plumbing (title case)
- Starr's & Stripes PowerWash (apostrophe, ampersand, PowerWash as one word because that is how they write it)

**Trademark and legal suffixes:** only include "LLC" or "Inc" if the prospect uses it on their public-facing marketing materials. Otherwise omit.

**DBA handling:** use the display name in visible copy. Legal name only in LocalBusiness schema if verifiable from a license record.

### Addresses

**Display format:** `2381 NW 53rd Ave Rd, Ocala, FL 34482`
- Street first
- City, State abbreviation (two-letter uppercase)
- ZIP code at end
- Comma separators

**Schema format:** break into `streetAddress`, `addressLocality`, `addressRegion`, `postalCode`, `addressCountry` per schema.org LocalBusiness spec (see `seo-geo.md`).

### Service areas

**In body copy:** list with Oxford comma. Example: *"Dunnellon, Ocala, Belleview, The Villages, Silver Springs, and Rainbow Lakes Estates."*

**In section header:** *"Serving all of Marion County."* or *"Across Dunnellon and Ocala."* (depending on how broad the service area is captured to be).

**In footer:** bullet list of cities, one per line.

**Approved Marion County place names** (use verbatim, with correct capitalization):

- Ocala
- Marion County
- Dunnellon
- Belleview
- The Villages (always with "The" and "V" capitalized)
- Silver Springs
- Rainbow Lakes Estates
- Ocklawaha
- Salt Springs
- Anthony
- Fort McCoy
- Reddick
- Summerfield
- McIntosh

For prospects outside Marion County, use whatever place name is verified from Phase 2 capture (address, service area page, testimonials). Never invent a service area.

---

## Prospect voice preservation vs replacement logic

When Phase 2 captures text directly from the prospect's existing site, there is a judgment call: preserve their voice verbatim, or replace with GRM voice rules?

### Always preserve verbatim

- **Testimonial quotes:** real customer words, never paraphrased, always verbatim
- **License numbers, dates, phone numbers, addresses:** factual data, never rewritten
- **Service category names:** use their exact service names, never rebrand (e.g., "Whole house surge protection" stays that exact phrase if that is how they wrote it)
- **Owner names, company names:** verbatim from their About page

### Always replace with GRM voice

- **Generic AI-sounding copy:** "We pride ourselves on quality work" → rewrite entirely
- **Filler phrases from the banned words list:** any instance triggers a rewrite
- **Section headers that read like templates:** "Welcome to Our Website" → replace with Closing Table voice
- **Hero headlines:** always generated fresh from the five patterns, never lifted from prospect site

### Use editorial judgment

- **Their About page story:** if the prospect wrote a great story about their founding, preserve the key facts and rewrite in Front Porch voice. If they wrote generic filler, replace entirely.
- **Their mission or values:** preserve if specific ("we answer the phone every call"), replace if generic ("committed to excellence").
- **Their FAQ questions:** use their questions if they captured good ones, generate from templates if their FAQ is generic or missing.

The rule: if their voice serves the customer, preserve it. If their voice sounds like AI or a 2015 template, replace it.

---

## Common mistakes to avoid

- **Do not use "Plant Street voice" as a synonym for "GRM voice rules."** Plant Street is a specific first-person opinion voice. Contractor sites use Closing Table, Saturday Morning, and Front Porch.
- **Do not blend voices within a single section.** If the services grid header is Saturday Morning and the service card descriptions are Closing Table, that is fine because they are different sections. But within the services grid header, all copy must be Saturday Morning, not a mix.
- **Do not fabricate facts to fit a headline pattern.** If Pattern A requires a review count and Phase 2 did not capture one, fall through to Pattern C. Never invent "hundreds of happy customers" to fit a pattern.
- **Do not collapse captured service lists.** If Phase 2 captured 12 services, generate 12 descriptions. Never consolidate to "general electrical work."
- **Do not use "local" or "your neighborhood" as a substitute for a real place name.** Specific nouns over abstract ones.
- **Do not write FAQ answers that apply to every business in the vertical.** Each answer must reference the specific prospect's captured facts (their phone, their service area, their license number, their warranty terms).
- **Do not fabricate FAQ content.** If an FAQ template asks about financing and Phase 2 did not capture financing info, omit that FAQ from the build. 5 real FAQs beat 7 with 2 fabricated.
- **Do not translate testimonials into Closing Table voice.** Testimonial quotes are verbatim customer words. They stay in the customer's voice.
- **Do not use em dashes anywhere in generated customer output.** Phase 6 check 4 greps for them and fails the build on any hit.
- **Do not skip the anti-AI test.** Every paragraph should pass all four tests before shipping.

---

## Self-check before Phase 5 marks content complete

Before marking any generated page content complete, verify:

- [ ] Every section has a voice assignment from the mapping table above
- [ ] Every section's copy matches its assigned voice
- [ ] No banned phrase from the banned words list appears anywhere
- [ ] No em dash appears anywhere in customer-facing output
- [ ] Every headline uses one of the five approved patterns
- [ ] Every CTA uses one of the approved CTA templates
- [ ] Every testimonial has a real first name, city, and verbatim quote
- [ ] Every service description references a captured service name verbatim
- [ ] Every FAQ answer references captured prospect facts, no fabricated data
- [ ] House formatting rules applied for phone numbers, hours, license numbers, and years
- [ ] Anti-AI test applied to every paragraph
- [ ] About page uses Front Porch voice, not Closing Table
- [ ] Footer tagline uses Front Porch voice
- [ ] Stats section uses Closing Table voice and only real numbers from Phase 2
- [ ] Featured promotion callout only rendered if real promotion captured, otherwise omitted

---

## Sales-ammunition categories (Phase 8 done-report)

Phase 8 done-report surfaces the following categories as sales talking points, populated from `profile.json` during the build:

- Broken internal links (from Phase 2 broken-link capture step)
- Stale copyright year in footer (from Phase 1 footer parse)
- Stale "since [YEAR]" or "[N] years in business" claims where the stated duration is materially shorter than the actual duration
- Missing JSON-LD schema (detected via Phase 1 HTML parse)
- Plugin-artifact `og:image` (tracking pixels, placeholder images, 1x1 transparent GIFs)
- Missing `tel:` link on phone numbers displayed as plain text
- Missing physical address despite being a local business (PO Box only, or no address at all)
- CMS age indicators (e.g., Elementor + WordPress of a certain vintage, Joomla/Drupal pre-modern versions)
- Social presence gaps (e.g., Facebook-only for a visual business that should have Instagram)

These are captured automatically during Phase 1 and Phase 2 and flow through `profile.json` to the Phase 8 report. Do not fabricate or speculate — only report what was verifiably captured.

---

## Version

content-rules.md v0.7.0. Synced with GRM_VOICE_SKILL.md v1.0 (March 22, 2026). When GRM_VOICE_SKILL.md is updated, this file must be manually re-synced for the universal rules and banned words list excerpt.

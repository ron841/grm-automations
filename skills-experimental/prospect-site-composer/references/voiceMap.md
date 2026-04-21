# voiceMap.md

Register-per-section rules for the GRM site-generator skill. Paired with typography.md; where that document covers the mechanics of type, this one covers how voice distributes across a page. Revised post-Code review.

---

## 1. The premise

A site has more than one voice. A homepage that speaks in a single voice from hero to footer reads as corporate. A site with a voice map reads as *inhabited* — different parts of the page are authored by different registers, and the reader feels the shifts before they can name them.

The voice map assigns a **register** to each section of the page. The register is not just copy — it's every surface the section exposes. Link treatment, focus ring, border weight, background color, italic policy, measure width, mono eyebrow tone.

**Register extends beyond typography to include every rule on the page that carries voice.** If you scope register to type only, the voice shifts feel disconnected from the rest of the composition. If you scope it to every surface, the voice shifts feel intentional.

---

## 2. The registers

Three first-class registers for the GRM site-generator skill.

### 2a. Closing Table

**Voice.** The business closing a deal. Certified, licensed, inspected, signed. The register where credentials live, where the phone number lives, where the CTA to call lives.

**Typographic signature.**
- Mono eyebrows in the loud register (`--primary`).
- Display headline at section-opener scale.
- No italic in the headline — Closing Table is roman, not cursive.
- Body copy at 15–16px, line-height 1.65–1.7.
- Stat rows appear here.

**Non-type surfaces.**
- Borders: `1px solid var(--line)`.
- Links: underlined with `border-bottom`, primary color, 2px offset.
- Focus rings: `2px solid var(--primary)`, 3px offset.
- Background: page base color. No gradient, no photo.
- Section padding: system default (72–88px vertical).

**Canonical instances.** Trust strip, nav, hero stat row, signature-tag + signature body copy, operational grid.

**Copy discipline.** Credentials stated plainly. Phone numbers in display face. Dates and certifications in mono captions. No italic on the core trust-carrying sentences.

---

### 2b. Saturday Morning

**Voice.** The business doing the work. Weekly service on a Saturday, the pool getting brushed and balanced. The voice that describes *what actually happens* in operational language.

**Typographic signature.**
- Mono pair in card num: loud register (`--primary`) left, quiet register (`--mute`) right.
- Display headline at card scale (28px).
- Body copy short — 2–3 sentences max per card.
- Italic runs allowed in body only, one per card, for the memorable phrase.
- Measure: 44–48ch.

**Non-type surfaces.**
- Cards on a hairline grid — 1px between cards, white card fill, page-color gaps.
- No card shadows.
- Border-bottom on operational-tag strip matches Closing Table.
- Links inside cards: primary color, underline on hover, no default underline.

**Canonical instances.** Operational grid, signature-meta, gallery cards.

**Copy discipline.** Verbs up front. Specifics, not abstractions. "Drain, acid-wash, refinish, repair, rebalance" not "comprehensive pool restoration services."

---

### 2c. Front Porch

**Voice.** The business *as people*. Randy keeps the pumps running. Matt keeps the chemistry right. The voice that names the human beings doing the work.

**Typographic signature.**
- Display headline at footer scale (40–48px), weight 400, `text-wrap: balance`.
- Italic runs on the *human* verbs.
- Italic color takes `--accent` on dark navy backgrounds. **This is the em-on-dark exception, and it is owned by typography.md §2 — cross-referenced here, not duplicated.**
- Sub-copy in italic Fraunces at 18–19px, line-height 1.5.

**Non-type surfaces.**
- Background: `--deep` (navy). Front Porch lives on dark. Every canonical instance of Front Porch on a homepage sits on a navy band.
- No borders inside Front Porch sections — the dark field does the containment.
- Links: white text, accent-color `border-bottom` on hover.
- Phone numbers at display scale (28–32px), white, weight 400.

**Canonical instances.** Equine band, footer. Both navy, both Front Porch. Background color and register are coupled — see §7.

**Copy discipline.** Names, not titles. "Randy" not "our repair technician." Second-person warmth where appropriate. Sacred lines stay sacred.

---

### 2d. Three-tier service composition (Signature / Operational / Distinctive)

Service pages rarely use a single register for every service. The A Quality Pool build surfaced a three-tier composition that every service-carrying page in this skill should follow.

**Signature** — one or two services that define the business. The hero services. Author in **Closing Table** register, at section-opener scale, with the signature-tag + bordered content block. These are the services a customer remembers.

**Operational** — the middle tier. Weekly recurring services, standard repairs, routine work. Author in **Saturday Morning** register, as a grid of cards with mono num tags. These are the services that pay the bills.

**Distinctive** — the odd one out. The specialty service, the one that earns the unusual photo and the standalone band. Author in **Front Porch** register if the specialty carries human-voice weight, or in **Saturday Morning** with expanded composition if it carries operational weight. These are the services that get remarked on.

**Decision tree for unfamiliar services.**
1. Is this service the one the business is known for? → Signature (Closing Table).
2. Is this service a weekly / routine / recurring line item? → Operational (Saturday Morning).
3. Is this service unusual, specialty, or voice-carrying? → Distinctive (Front Porch or Saturday Morning+).
4. Default if none of the above: Operational.

**Why written down.** On A Quality Pool the three tiers emerged naturally (weekly + construction as signature, eight operational services, equine aquatics as distinctive). On the next build — commercial roofing, electrical, whatever — the tiers will *not* emerge naturally without this decision tree. The composition would drift into a flat grid of equally-weighted cards, which is the failure mode.

---

## 3. The voice-pivot anchor strip

A specific pattern that earns its own section.

Between the hero (Closing Table) and the services on the A Quality Pool homepage sits a full-width strip containing one italic Fraunces pullquote and a mono credit. This strip is the **voice pivot** — it lifts the page from the certified-licensed register of the hero into something more reflective, just for one sentence.

**Why it works.** The hero says "36 years." The footer says "Randy keeps the pumps running." Without the anchor strip, those two registers sit next to each other with only service cards between them, and the transition feels abrupt.

**Typographic signature.**
- Italic Fraunces pullquote, 22–28px, weight 300, `--darkmuted`.
- Mono credit in a two-tone pair.
- Thin borders top and bottom.
- Generous horizontal padding, modest vertical padding.

**Once per page. Rule with reasoning articulated.**

An anchor strip is a register pivot. Register pivots consume reader attention budget — the reader's cognitive dwell-time on a voice shift before they can re-orient to the new register. That budget is finite per page. One pivot is felt as *deliberate;* two pivots means neither register holds the page long enough for the reader to settle into it, and the shifts read as vacillation rather than intention.

If a page genuinely needs two pivots, one of the underlying sections is probably in the wrong register — combine or reassign before adding a second strip.

---

## 4. Featured pullquote testimonial — register consumer

The testimonial pattern on the A Quality Pool homepage blends registers rather than choosing one.

**Composition.**
- Closing Table eyebrow — the frame is trust-carrying.
- Closing Table title with italic counter-phrase — the page speaks in its institutional voice to frame the pullquote.
- Featured Pullquote at display-italic scale — the customer's voice, Front Porch typographically (italic, warm) but on page-base background rather than navy.
- Mono attribution — back to Closing Table, naming names precisely.

### Pullquote trigger

Not every long testimonial should get featured-pullquote promotion. The rule:

- `promoted: true` flag on the testimonial record. **Overrides everything.** If a testimonial is promoted, it gets the featured pullquote treatment regardless of length.
- **In the absence of the flag**, heuristics evaluate as AND:
  - Length ≥ 60 words.
  - At least one **credibility marker**: institution reference, license citation, named third party (a professional, an inspector, a board), or a recognized work or award.

Length alone is insufficient. A 60-word testimonial without a credibility marker is a long review, not a featured pullquote. Credibility marker alone is insufficient — a one-sentence credential-rich quote is a caption, not a pullquote.

**Typographic signature.**
- Pullquote: `clamp(30px, 3.3vw, 40px)`, italic, weight 300, `--darkmuted`, `max-width: 20ch`.
- Attribution name: display face, 20px, weight 500.
- Attribution meta: mono, 10px, 0.12em tracking, quiet register.

**No decorative quote marks.** The italic display scale is doing the quote-signaling.

---

## 5. Front Porch footer — register consumer

The canonical Front Porch instance. The rules:

- Navy background.
- Display headline at footer scale, italic on human verbs, accent color on italic runs (em-on-dark exception — owned by typography.md).
- Phone number at display scale (28–32px), white, weight 400.
- Mono column labels in accent color.
- Attribution copy at 12px, line-height 1.6, sentence case — the one place on the page where sentence case appears in a mono-adjacent surface. This is an exception to the uppercase-mono rule in typography.md §3, earned by length (photo credits with names are unreadable at 12px uppercase).

The Front Porch footer consolidates three rules: italic-on-dark with color shift, display phone number, sentence-case mono attribution.

---

## 6. Copy discipline per register

Which lines earn italic runs, and which stay prose.

### Sacred lines (italic earned)

- Front Porch headline: italic on the warm verb. "Randy *keeps* the pumps running."
- Hero headline: italic on the regional anchor or emotional phrase. "of pools in *Central Florida*."
- Section-opener italic counter-phrase: "Eight services. *One pool phone number.*"
- Featured pullquote: entire quote italic at display scale.

### Prose (italic withheld)

- Body descriptions inside service cards.
- Trust-strip content.
- Stat labels and mono captions.
- Button text and CTAs.

### The generalizable rule

**Italic is earned by voice, not by emphasis.** If a line is italicized to "make it pop," the italic is wrong. If a line is italicized because it carries a voice shift that the italic shape reinforces, the italic is right.

When in doubt: read the paragraph aloud. If the italic phrase would naturally get a small pause or vocal lift, italic is earned.

---

## 7. Register coupling rules

Rules that span registers.

### Background color and register are coupled

Every background declares a register. On the A Quality Pool canonical homepage:
- Page base (off-white / `--page`) → Closing Table or Saturday Morning.
- Navy (`--deep`) → Front Porch.

Four registers is the practical ceiling. Brands may earn a third background if it's declared in the voice map as a register. A page with an undeclared third background ("light gray section") reads as a page with three voices and one mistake.

The rule is not "two backgrounds and no more." The rule is **no silent backgrounds** — every background is a declared register, and new registers require explicit authoring in this document before they're used.

### Mono register follows voice register

- Closing Table sections use `--primary` for eyebrows and `--mute` for meta.
- Saturday Morning sections use the same pairing.
- Front Porch sections on navy use `--accent` for eyebrows and `--deep-dim` for quiet meta.

The pairing — loud register + quiet register — is universal. The colors shift based on background.

### Italic follows register

- Closing Table: rare, one italic run per section at most, headlines only.
- Saturday Morning: per-card, one run, in body copy.
- Front Porch: multiple runs in headlines, on accent color, celebratory.

---

## 8. Implementation note for the skill

Authoring order for a new page:

1. **Lay out the voice map first.** Which sections are Closing Table? Saturday Morning? Front Porch? Voice pivot? Write as HTML comments before styling.
2. **Pick backgrounds from the voice map.** Navy for Front Porch. Page base otherwise.
3. **Apply typography from typography.md.**
4. **Author copy per register discipline.**
5. **Review for register coupling.** Does every surface carry the register? Borders, links, focus rings, mono tone?
6. **Check for exception drift.** Has an exception been introduced that isn't named in the voice map or typography.md? If yes, either promote it to a named exception with reasoning, or remove it. Silent exceptions are the most common failure mode.

**The failure mode to watch for.** A section that looks typographically right but feels flat — usually because the non-type surfaces are all authored in the default register rather than the section's register. Check the border color. Check the link treatment. Check the background.

---

## 9. Open questions for future rounds

These are deliberate gaps. Flag when the work surfaces them.

- **A fourth register for long-form content.** If this skill generates blog posts or case studies, a long-form reading register may be needed.
- **Form register.** Contact forms and estimate requests currently inherit Closing Table by default.
- **The specialty-subdomain question.** Equine Aquatics on the A Quality Pool homepage is a Front Porch section carrying a specialized voice (Marion horse country, specialized aquatic services). Whether "specialty subdomain" is a modifier on Front Porch or a fourth register is the most pressing open question in this document. The next build with a specialty service (historic-home electrical, commercial roofing on a residential brand, etc.) will force the resolution. Until then: treat specialty as a Front Porch modifier and flag the specific instance in the build notes.

---

## Appendix reference: the exceptions principle

The skill's exceptions principle — the four-point frame that determines whether an exception is earned (broken outcome / bounded context / written reasoning / not instance-scoped) — lives in **typography.md, Appendix A**. Both named exceptions in the current skill are fundamentally typographic: em-on-dark is a color-on-italic rule, and the 12px sentence-case mono attribution is a case-and-tracking rule.

When authoring a new voice-map register, a new background, or a new specialty context, check typography.md Appendix A before introducing an exception. If the four points don't all hold, the exception isn't earned — fix the rule or hold the line.

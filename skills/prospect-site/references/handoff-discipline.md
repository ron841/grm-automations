# handoff-discipline.md

Protocol for skill-file authoring and Design ↔ Code collaboration rounds. Authored from the v0.8 foundation round (April 18-19, 2026), where typography.md and voiceMap.md were produced through a four-lens loop that surfaced findings none of the lenses would have caught alone.

---

## 0. What this file governs

This file governs *how skill files get authored*, not *what the skill does at build time*. The prospect-site build flow (Phase 0 through deployment) never invokes the rules below — those rules govern future skill-file collaboration rounds, not the generation of a contractor site.

Runtime Claude authoring a prospect site does not need to read this file. A Claude authoring the next skill-file round (composition patterns, new validators, the next design-layer rule set) does.

---

## 1. The premise

A skill-file round authored by a single lens produces work with predictable blind spots. Design working alone flattens implementation fit. Code working alone flattens aesthetic intent. Triage working alone paraphrases both and loses precision on each.

The v0.8 foundation round (April 18-19) was the working example. typography.md and voiceMap.md were authored by Design, reviewed by Code, synthesized by triage, and arbitrated by Ron across four interleaved passes. The round surfaced:

- An AND-vs-OR heuristic error in the featured pullquote trigger (Design caught; Code's first-pass framing would have let a 60-word testimonial without credibility markers earn featured promotion).
- A source-of-truth ambiguity between voiceMap.md and the existing content-rules.md (Code caught on file adoption; triage had not flagged the overlap).
- Three near-miss handoffs where a zip was announced shipped but sat at a path that did not exist or contained different files than announced.
- A foundation-strip episode where Design's typography amp silently removed the SEO/GEO/schema/a11y/script-driver foundation from shipped HTML (Code's preservation gate caught; zero ship impact).
- A four-hour cache diagnostic on F5 that resolved to a vercel.json misconfiguration shipping as the skill's default template.

No single lens would have caught all of these. Multiple lenses did. The rules below codify how the multi-lens authoring loop runs from here.

---

## 2. The three-lens authorship pattern

### The four lenses

Every skill-file round passes through all four before tagging:

- **Primary author.** Composes the file in the author's voice, with reasoning intact. Never paraphrased through a second voice before reaching the reviewer.
- **Reviewer.** Examines the draft through the complementary lens (Code for Design-authored files, Design for Code-authored files). Classifies rules, flags concerns, proposes revisions without rewriting.
- **Triage synthesis.** Holds cross-document consistency, catches continuity drift, surfaces earlier-turn language that belongs in the document but didn't make it.
- **Arbitration.** Ron decides where Design and Code genuinely diverge.

The four lenses are non-optional. A file tagged before any of them has run is a draft dressed as shipped work.

### Design-layer vs. implementation-layer files

The lenses don't swap arbitrarily — they swap *by file type*.

**Design-layer files** are primary-authored by Claude Design. Typography rules, voice-register distribution, composition patterns, hero-mode decision trees, anything where the content is authorial judgment about aesthetic or rhetorical intent. Code reviews for implementation fit — classifies each rule as CSS token / pattern recipe / judgment call, flags items where the rule conflicts with existing skill machinery or where enforcement is underspecified.

**Implementation-layer files** flip the authorship. Phase 6 validators, MD5 dedupe specs, primitive implementations, rhythm-token values, anything where the content is mechanical enforcement of previously-authored rules. Code primary-authors. Design reviews for aesthetic-intent preservation — does the validator enforce the rule as Design wrote it, or does the implementation subtly bend the rule to something easier to code.

handoff-discipline.md itself is a Design-layer file. The three-lens pattern is an aesthetic judgment about how collaboration produces quality, not a mechanical enforcement rule.

### Direct-voice exchange

Authors speak directly to each other through the triage agent. Not paraphrased. Not summarized. The triage Claude ferries draft files from Design to Code and review notes from Code to Design verbatim.

Paraphrasing loses precision on both sides. When Code's review of typography.md was about to be paraphrased through triage before reaching Design, Ron's instinct — *"feed it directly to Design"* — preserved the exact language of Code's classification concerns. Design's response to that direct language was sharper than a response to a summary would have been. Evidence: the AND-vs-OR heuristic correction came from Code's exact framing, not from a summary of it.

### Why this exists

Authorial lenses each have sharp edges in one direction and blunt edges in another. Design's edge is aesthetic intent and authorial voice; Design's blunt edge is implementation surface. Code's edge is implementation fit; Code's blunt edge is authorial voice. Triage's edge is continuity; triage's blunt edge is origination. The arbitrator's edge is product priority.

A round that runs all four lenses uses each edge where it's sharp. A round that skips one uses another lens in an unsharp mode, and the unsharp work is exactly where the failures happen.

---

## 3. Foundation preservation

### The rule

**The deployed build is the source of truth. Any merge into a flagship build preserves the full SEO/GEO/schema/a11y/script-driver foundation.** Modify only the whitelist explicitly granted in the authoring prompt. Every other element — HTML structure, `<head>` contents, scripts, ARIA, data attributes, schema, meta tags — passes through unchanged.

This is a Hard Rule in the skill. See SKILL.md Rule #11, which points here.

### What counts as foundation

Thirteen items in the current skill. Any item absent from the deployed build after a Design-authored amp merges is a failure:

1. Meta description
2. Canonical link
3. OpenGraph tag block (10 tags — locked count, per v0.8 scope Tier 3 downgrade)
4. Twitter Card tags
5. JSON-LD LocalBusiness schema
6. GEO meta tags (ICBM, geo.position, geo.placename, geo.region)
7. Favicon link block
8. Font preconnect and font links
9. style.css stylesheet link
10. Skip-to-content link and ARIA landmarks
11. Form integrity — action URL, honeypot field, required fields
12. Script drivers (analytics, forms, interactive handlers)
13. Sitemap and robots references

*Verify this list against Code's enumerated foundation-item set. The count matches "13 of 13" from the F5 preservation-gate report but the specific items are a triage reconstruction.*

Code's merge-gate validates every item before the deploy command fires. An amp that passes compose but fails preservation is rejected, not deployed.

### Why this exists

The F5 A Quality Pool homepage is the evidence. Design's first typography-amp pass rebuilt the HTML body to carry the new type system and inadvertently rebuilt the head to the minimum needed to render a preview — which meant everything else in the original head fell off the checklist. Schema deleted. OpenGraph deleted. Canonical deleted. Structured data deleted.

Zero ship impact only because Code's preservation gate ran before deploy. Without the gate, the deploy would have shipped a site that passed visual review and silently broke every SEO and social-preview surface the site had carried at v0.7.2.

Design's own diagnostic: *the compose pass worked from the body outward; the head was rebuilt to minimum for preview; everything else fell off the checklist*. The rule exists because the failure mode is silent — nothing in the composed output announces what's missing.

### The enforcement layer

Authoring-layer rule: primary authors compose within an explicit whitelist (see §4). Head contents are outside the whitelist by default.

Validation-layer enforcement: Code's merge gate checks every foundation item before the commit that stages a deploy. Any missing item blocks the commit and surfaces the diff. Validation catches what authoring failed to preserve.

Two layers because one layer is never enough. Authoring discipline alone is too easy to drift. Validation alone catches failures after they've been committed. The pair is the minimum.

---

## 4. Whitelist-the-changes handoff frame

### The frame

Every Design-authoring prompt that touches a deployed build opens with this frame, stated as rules to the authoring Claude:

> The deployed build is the source of truth. You may modify [explicit whitelist — e.g., "the hero section body copy, the services grid headlines, and the footer attribution block"]. Every other element — HTML structure, `<head>` contents, scripts, ARIA, data attributes, schema, meta tags — passes through your output unchanged. If you need to touch something outside the whitelist, propose the change and wait for confirmation before executing.

### The inversion

The prior default was *compose freely, preserve implicitly*. The author produced output; a reviewer checked that nothing important had been dropped. Implicit preservation failed on F5 because the author's compose pass did not distinguish between "writing new copy" and "rebuilding the entire HTML document." Preservation was an afterthought, not a frame.

The whitelist frame inverts the default to *compose within a whitelist, everything else passes through untouched*. The author's working surface is explicit. Anything outside the surface is not up for modification. If the author's work genuinely requires touching something outside the surface — if the body copy change needs a new JSON-LD property, say — the author proposes the change and waits. The reviewer expands the whitelist or declines; the author does not expand the whitelist unilaterally.

### When to use

Every Design-authoring prompt that produces output against a deployed build. Every Design-authoring prompt that produces output against a previous Design-authored file. Every Code-implementation prompt that touches deployed build files.

Green-field composition — authoring a new file from an empty canvas — does not need the frame. The frame protects work that already exists, and is not a premise for new work.

### The propose-and-wait clause

*"If you need to touch something outside the whitelist, propose the change and wait."*

This clause is not optional. An author that unilaterally expands their own whitelist is not operating within the frame; they are operating as if no frame existed. The propose-and-wait clause is the whitelist's enforcement mechanism — without it, the whitelist is a suggestion.

Proposals expand the whitelist by named explicit item, not by category. *"I need to modify the canonical link to reflect the new slug"* is a proposal that expands the whitelist by one named item. *"I need access to the `<head>` block"* is a category-level request and gets declined — what the author actually needs is almost never the whole head.

---

## 5. Canonical artifact pattern

### The problem

Design operates in a chat environment without direct GitHub write access. Handing off a multi-file authorial round to Code requires a path Code can retrieve from.

Three failed paths during the v0.8 foundation round demonstrate what the canonical path has to displace:

- Design announced an amp-pass folder at a GitHub path that did not exist — Design had composed in its chat filesystem and not exported.
- Zip filenames drifted between Design's announcement and Ron's upload.
- A revision zip landed at a path Ron expected but that did not match Design's actual export.

Each resolved cleanly because Code validated source existence before starting work. Without that validation step, Code would have begun authoring against files that did not contain what Design believed they contained.

### The pattern

Design produces a zip per authoring pass, named `<round-slug>-<pass-label>.zip`. Examples from the v0.8 foundation round: `typography-voicemap-v0.8.1.zip`, `session-close-2026-04-19.zip`.

Ron drops the zip into `grm-design-handoffs/[build-slug]/` in the local filesystem. Code commits and pushes from there. Paste-inline is a fallback for one- or two-line edits only — any change larger than that goes through the zip path.

### The validation step

Before Code begins work on a handoff zip:

1. Confirm the file exists at the stated path.
2. Confirm the zip contains the files Design announced.
3. Confirm the files contain the content Design announced they would carry.

Any mismatch stops the work and flags Ron. **Do not work around missing source.** The three near-miss handoffs during the v0.8 foundation round resolved cleanly because Code refused to compose against absent or drifted source. Had Code synthesized from partial context, the resulting output would have been plausible prose grounded in assumptions rather than in Design's actual articulation.

### Why per-pass, not per-file

A zip per pass preserves the atomicity of the authoring round. typography.md and voiceMap.md were authored together; their post-review revisions landed together; response-to-code-review.md documented the joint revision pass. Splitting them into per-file handoffs would have fragmented the revision logic across three separate Design → Code transfers.

The unit of handoff is the authoring pass, not the file.

---

## 6. Handoff vocabulary

Three states. Named. Everyone means the same thing.

### The three states

- **Shipped.** Committed and pushed to the handoff repo. Visible at origin. Retrievable by URL. This is the strongest state.
- **Ready-for-review.** Rendered in a preview environment (Vercel preview deployment, local render, chat artifact) but not yet in the repo. Visually verifiable by the team; not yet a permanent record.
- **Draft.** Composed but not previewed. Exists only in an author's working context. Not verifiable by anyone except the author.

### Why this matters

The v0.8 foundation round produced a concrete vocabulary confusion: Design said *"shipped"* meaning *"rendered in preview."* Code and Ron heard *"committed and pushed."* The resulting conversation assumed a different world-state than actually existed, and the mismatch consumed minutes of clarification before the actual state was visible.

The three states are the minimum distinction. *Shipped* is about repo visibility, not preview rendering. *Ready-for-review* exists for the genuinely common case of work that's render-testable but not yet committed. *Draft* exists so that work-in-progress has its own honest label rather than being misrepresented as either of the stronger states.

### The mirror-cadence question

The v0.7.3 mirror pattern to grm-automations ran batch-by-release — accumulated commits pushed at a release tag boundary. The v0.8 Wave 1 pattern shifted to per-wave mirroring.

The shift was pragmatic, not principled. The v0.7.3 tail (hotfixes #10, #11, SKILL.md housekeeping) sat unmirrored for two days between April 17 and April 19, and on a read of grm-automations alone, the skill's actual state was not discoverable. Under the old *shipped* definition — committed and pushed to the handoff repo — none of the v0.7.3 tail was shipped during those two days, despite being live on every build run from the local skill directory.

Per-wave mirroring resolves the drift for v0.8. Whether it's the right cadence for every future skill round is an empirical question — too-frequent mirroring burns cycles on small commits; too-infrequent mirroring recreates the v0.7.3 gap. Preliminary call for v0.8 is per-wave; validate over the next two waves.

---

## 7. Scope-gate rule

Both sides of the authoring loop propose before executing.

### Design proposes scope extension before executing

A Design-authoring prompt scoped to *"the hero section"* that grows mid-compose to include the services section, the testimonials strip, and a new typography.md drop is not scoped work — it's scope creep dressed as composition. The correct behavior is to surface the proposed extension and wait.

Working example from the v0.8 foundation round: Design's F5 homepage amp prompt was initially scoped to the hero. The draft that returned included a services rework, a testimonials treatment, and an early draft of typography.md. All three extensions were valuable. None were in scope. The conversation paused to re-scope, and the extensions were either folded into named parallel work or deferred — but only because the extensions were visible. Had they landed silently in the hero deliverable, Code would have had to triage four authorial changes while reviewing what was supposed to be one.

### Code proposes phasing when context pressure becomes visible

Code estimates of execution time are unreliable. The v0.8 Wave 1 estimate was 10-13 hours; actual execution was under one. Pre-execution time estimates consistently diverge from actual execution by margins too wide to serve as a phasing trigger. A rule built on hour-estimates is a rule built on a number the Code lens does not reliably predict.

The real phasing trigger is context pressure observed during execution. Code surfaces a phasing proposal when the working context shows any of:

- Token consumption approaching a ceiling where quality would start to degrade if the session continued.
- Scope becoming materially larger than what the opening prompt framed, with the expansion visible only after execution began.
- Dependencies surfacing mid-execution that weren't in the original scope and that would benefit from separate review before proceeding.

Phasing is a response to observed state, not a prediction against the clock. A session that opens scoped to four items and stays scoped to four items runs to completion regardless of elapsed time. A session that opens scoped to four items and discovers at item three that item four actually requires a preceding item zero gets phased at that discovery — not because it's been running for a number of hours, but because the scope changed.

### Why both sides

Design's blind spot is scope. When Design composes, the composition invites adjacent composition — the hero wants context, the context wants a services tease, the tease wants a typography voice, and Design has produced four things when one was asked for.

Code's blind spot is scope-creep-under-execution. When Code executes, execution surfaces dependencies that weren't in the opening prompt — a primitive needs a test fixture that doesn't exist, a validator needs a data structure that hasn't been decided, a mechanical edit reveals an architectural question that wasn't flagged at scope-time. These discoveries are valuable — they're exactly what execution is supposed to surface — but they're also scope that wasn't in the original frame.

Both blind spots are failures of scope discipline at the prompt-to-execution boundary. The rule protects the boundary on both sides. The trigger on each side is the condition that reliably signals the blind spot, not the clock.

---

## 8. Authoring order for a skill-file round

1. **Classify the round by layer.** Design-layer or implementation-layer. The classification determines primary authorship.
2. **Frame the opening prompt with the whitelist.** Whitelist names modify-surfaces by explicit item. Anything outside the whitelist requires propose-and-wait.
3. **Primary author drafts.** In the author's voice, with reasoning intact. Delivered as a zip per the canonical artifact pattern.
4. **Validate the handoff artifact.** File exists at stated path, contents match announcement, pass is atomic.
5. **Reviewer lens examines the draft.** Complementary lens (Code for Design-authored, Design for Code-authored). Classifies rules, flags concerns, proposes revisions without rewriting.
6. **Triage synthesizes.** Cross-document consistency, continuity drift, earlier-turn language that belongs in the document but didn't make it.
7. **Ron arbitrates.** Where Design and Code genuinely diverge.
8. **Revision loop if needed.** Primary author revises in response to review notes. Revision pass delivered as a new zip, not as inline edits to the review notes.
9. **Commit to the skill repo when all four lenses have cleared.** Mirror to grm-automations per current cadence (per-wave as of v0.8).
10. **Vocabulary check at commit.** *Shipped* when the mirror lands on origin. *Ready-for-review* before the mirror. *Draft* before any preview exists.

### The failure mode to watch for

A skill file authored in one voice with the other three lenses collapsed into a single quick pass, then tagged. The prose reads as competent. The blind spots are invisible because the lenses that would have caught them did not run — or ran in an unsharp mode because the primary-author lens was doing their work too.

The cheapest signal of lens collapse: the review pass contains zero substantive revisions. A real review pass produces real revisions. A review pass that returns *"looks good, ship it"* is almost always a lens that did not actually read for its own edge.

---

## 9. Open questions

Deliberate gaps. Flag when the work surfaces them.

- **Mirror cadence validation.** Per-wave adopted for v0.8 pragmatically. Correct cadence across multiple v0.x rounds is an empirical question — revisit after v0.8 tags with at least two waves of mirror evidence.
- **Three-lens load on short prompts.** A two-line Design revision does not need all four lenses. Where the threshold sits — by line count, by file count, by scope of change — is not yet articulated. Observe the next few rounds; name the threshold when the pattern is visible.
- **Direct-voice exchange scaling.** Direct exchange worked during the v0.8 foundation round because there were two lenses authoring and one triage ferrying. If future rounds add a third authoring lens (a specialty reviewer, say), the direct-exchange pattern needs to accommodate more than two authorial voices without becoming a round-robin. Not urgent; flag for the first round that surfaces it.

---

## Appendix reference: the exceptions principle

The four-point frame for earning an exception to any documented rule — *broken outcome, bounded context, written reasoning, not instance-scoped* — lives in **typography.md, Appendix A**. Exceptions to handoff-discipline rules earn their place under the same frame.

One currently-flagged candidate exception: the v0.8 Wave 1 introduction of `--section-padding-v` / `--tier-padding-v` / `--card-padding-v` as rhythm tokens that break the established `--space-*` prefix convention in css-framework.md. Pending promotion to typography.md Appendix A under the four-point frame. *Broken outcome:* renaming the tokens would break traceability to the v0.8 scope and typography.md §7 ranges. *Bounded context:* rhythm-tier tokens only. *Written reasoning:* role-name faithfulness per typography.md §0 takes precedence at this tier. *Not instance-scoped:* applies to all three rhythm tokens.

When authoring a new handoff-discipline rule and the urge to add an exception appears, apply the four points. If any of them fail, the exception isn't earned. Fix the rule or hold the line.

---

*Authored April 19, 2026, as part of the v0.8 Wave 5 prose synthesis. Source material: the GRM session handoff of the same date, typography.md Appendix A, voiceMap.md §8, response-to-code-review.md, and the lived experience of the v0.8 foundation authoring round.*

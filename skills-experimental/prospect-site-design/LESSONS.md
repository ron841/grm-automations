# LESSONS.md

Institutional memory for the prospect-site skill. Every entry below is a lesson learned from a real build that went wrong, almost went wrong, or revealed a hidden assumption. Phase 8 of the skill appends to this file automatically when something unusual happens during a build. Manual entries can be added at any time when reflection produces insight.

This file has one job: prevent the same mistake twice. If a future build is about to repeat an old failure, the lesson should already be in this file in a form that triggers recognition.

## How to use this file

**Read before building.** Future Claude sessions should read LESSONS.md before starting a new prospect build. The seed entries below establish the patterns to recognize. As more entries accumulate, the file becomes the most concentrated guide to "what we have already learned the hard way."

**Append, don't rewrite.** Lessons are permanent. Once an entry is added, it stays. Entries can be UPDATED if new information clarifies the lesson, but the original date and source are preserved. The file grows over time.

**Categorize consistently.** Every entry uses one of the categories defined below. New categories can be added if they don't fit the existing ones, but only after checking that the existing categories truly don't match.

**Cross-reference to skill files.** Every entry that produced a change to the skill files names the file path and the section. This makes the lesson actionable, not just historical.

## Categories

- **COLOR** — color extraction, palette decisions, brand color discipline
- **TYPOGRAPHY** — font choices, font loading, hierarchy
- **COPY** — voice violations, generic phrases, headline patterns
- **PHOTOGRAPHY** — stock photo failures, image quality, photo source decisions
- **SCHEMA** — JSON-LD issues, fabricated facts, validation failures
- **VOICE** — voice rule violations, voice file confusion, voice mapping issues
- **WORKFLOW** — phase ordering, hand-offs, integration between skill files
- **DEPLOYMENT** — Vercel, DNS, SSL, hosting issues
- **INTEGRATION** — third-party services, MCP issues, API failures
- **STRATEGY** — commercial thesis decisions, pricing, market positioning
- **PROCESS** — meta-lessons about how Ron and Claude work together
- **DATA** — profile.json issues, Phase 2 capture quality, fabrication risks

## Entry format

Every entry follows this template:

```
### [DATE] — [CATEGORY] — [Short title]

**Source:** [Which build, which prospect, which session]
**Severity:** [minor | moderate | critical]

**The assumption:** [What we expected or believed]
**What actually happened:** [What went wrong or surprised us]
**The lesson:** [What we learned in plain words]

**The fix:**
- [Specific change made to a skill file, with path]
- [Or: process change, with description]

**Affected files:** [List of skill files that reference this lesson]
```

Severity levels:
- **minor** — small annoyance, no client impact, fix is straightforward
- **moderate** — caught before client impact but could have shipped
- **critical** — actually shipped to a client, or would have caused trust damage

---

## Seed entries

These are the foundational lessons from v0.6 (the previous generation that failed) and the v0.7 build session. They establish the format and the pattern for future entries.

**A note on attribution.** The v0.6-era entries (marked "Pre-v0.7") are reconstructed from the broader v0.6 four-pattern-collapse failure rather than from individually documented incidents. The lessons themselves are real and well-documented in the conversation history; the specific narrative arcs (e.g., "this exact thing happened on this exact build") are inferred from the broader pattern. v0.7-era entries (marked "2026-04") are direct documentation from this build session. Future Phase 8 appends should be direct documentation, not inference, because Phase 8 has access to the actual build context. This file's transparency about inferred vs documented attribution is itself a model for how future appends should attribute their sources.

### Pre-v0.7 — COLOR — Johnson Brothers "Florida Gator" miss

**Source:** v0.6 build, Johnson Brothers Plumbing rebuild attempt
**Severity:** critical

**The assumption:** Brand colors could be derived by reading the prospect's website CSS and matching the vibe of their trade category. For a Florida plumber, deep navy and amber felt right.

**What actually happened:** The chosen palette ended up looking like University of Florida Gator colors. Ron's reaction was immediate and unambiguous: wrong. The actual Johnson Brothers logo featured bright royal blue and sun yellow with a sun-in-the-O wordmark — completely different from the chosen palette. The skill had picked colors by reading text and ignoring the actual logo file.

**The lesson:** Color extraction must happen against the real logo file, not by vibe-matching the trade category or by reading site CSS in isolation. A logo is a visual asset and must be examined visually.

**The fix:**
- Phase 4 color extraction now uses node-vibrant against the actual downloaded logo file (`image-handling.md`, color extraction discipline section)
- Anti-slop rules explicitly ban vibe-matching colors (`anti-slop-rules.md`, banned color combinations section, "Florida Gator combo" named as a permanent anti-pattern)
- Phase 1 logo download is mandatory, not optional (`SKILL.md`, Phase 1)

**Affected files:** `anti-slop-rules.md`, `image-handling.md`, `SKILL.md`, `hero-patterns.md`

---

### Pre-v0.7 — WORKFLOW — The v0.6 four-pattern collapse

**Source:** v0.6 build session, four prospect sites generated in sequence
**Severity:** critical

**The assumption:** Hand-rolled Tailwind components built from positive instructions ("use Features 8 component pattern, use Bento grid for services, use Testimonial V2 for reviews") would produce visually distinct sites for different businesses because the businesses themselves were different.

**What actually happened:** Four prospect sites — an electrician, a plumber, a pressure washer, and a pool builder — were all generated and all looked identical. Same centered hero. Same three-column feature grid. Same testimonial carousel. Same rounded-corner blue buttons. The businesses were obviously different but the sites were not. The LLM had defaulted to the most statistically common pattern in its training data on every build, regardless of the input business.

**The lesson:** Positive instructions ("use this pattern") are not enough. Without explicit negative instructions ("never use this pattern"), the LLM drifts to defaults every time. The skill needs a no-fly zone for every category where defaults would produce slop: typography, color, layout, copy, photography, interaction patterns.

**The fix:**
- Created `anti-slop-rules.md` as a dedicated no-fly zone reference (494 lines, then expanded to 662)
- Phase 4 design engine now checks proposed font, color, and hero mode against banned lists before showing the approval gate
- Phase 5 generation filters banned copy patterns and component structures during generation
- Phase 6 verification runs an automated anti-slop sweep as a hard gate

**Affected files:** `anti-slop-rules.md` (new file), `SKILL.md`, `hero-patterns.md`, `section-patterns.md`, `content-rules.md`

---

### 2026-04 — SCHEMA — T&F fabricated HomeAdvisor reviews

**Source:** v0.7 build, T&F Electric flagship 1
**Severity:** critical

**The assumption:** When a prospect site needed trust signals and Phase 2 captured limited review data, the skill could generate plausible-sounding review platform mentions to fill the gap. An early T&F draft included "50+ HomeAdvisor Reviews at 5 Stars" as a trust badge.

**What actually happened:** T&F Electric had no HomeAdvisor presence whatsoever. The "50+ HomeAdvisor Reviews" line was fabricated entirely by the skill to fill an empty trust section. Ron caught it before deployment, but if it had shipped, a prospect could have called T&F asking about their HomeAdvisor reviews and discovered the lie. Trust damage would have been immediate and irreparable.

**The lesson:** No fabrication of any third-party platform presence ever. If Phase 2 did not verify that the prospect has an account on a review platform, the skill cannot mention that platform on the rebuild. An empty section is better than a fabricated section.

**The fix:**
- Added review source verification rule to Phase 2 (`SKILL.md`, Phase 2 capture rules)
- Specific platforms named in the verification rule: HomeAdvisor, Angi, Yelp, BBB, Better Business Bureau, Houzz, Thumbtack
- Schema validation in Phase 6 cross-checks every trust badge claim against `profile.json.credentials` (`seo-geo.md`, Phase 6 check 11)
- Anti-slop rules explicitly ban fabricated trust badges (`anti-slop-rules.md`, banned layout patterns section)

**Affected files:** `SKILL.md`, `seo-geo.md`, `anti-slop-rules.md`, `image-handling.md`

---

### 2026-04 — VOICE — Plant Street naming confusion

**Source:** v0.7 build session, voice system integration
**Severity:** moderate

**The assumption:** "Plant Street voice" was the universal voice rule set documented in older skill files and handoff documents. Every reference to Plant Street in those documents implied a single coherent voice that should be applied to all prospect site copy.

**What actually happened:** The actual GRM_VOICE_SKILL.md at `github.com/ron841/grm-automations/blob/main/.claude/skills/GRM_VOICE_SKILL.md` defined Plant Street as something specific and different: a first-person opinion voice used by Ron in his personal content. Applying Plant Street voice to a contractor site (where the voice should be the contractor's, not Ron's) would have been a category error. The older documents had been using "Plant Street" as loose shorthand for "Ron's voice rules in general," but that shorthand was incorrect.

**The lesson:** Voice files are precise. "Voice" is not a single thing; it is a system of distinct voices each with a specific application context. Skill files should map voice to section, not assume a single voice applies everywhere. Source-of-truth voice files (the actual skill files in the GitHub repo) win over shorthand references in older documents.

**The fix:**
- Voice mapping established in `content-rules.md`: Closing Table voice for hero/promos/cards/stats/before-after/FAQ/Tier A; Saturday Morning voice for marquees and section headers; Front Porch voice for footer and About page
- Plant Street, Welcome Mat, and Deep Roots voices explicitly named as NOT USED for contractor site generation
- Cross-references to GRM_VOICE_SKILL.md as the source of truth, with the warning that older handoff documents may use looser language

**Affected files:** `content-rules.md`, `SKILL.md`

---

### 2026-04 — DEPLOYMENT — T&F Vercel deployment troubleshooting

**Source:** v0.7 build, T&F Electric flagship 1 deployment
**Severity:** moderate

**The assumption:** The first Vercel deployment of T&F would work cleanly with default Vercel project settings. Plain HTML sites do not need build configuration.

**What actually happened:** The deployment failed initially because Vercel had inherited an old Build Command setting from a template, pointing at a build script that did not exist. After that was fixed, deployment failed again because Vercel's Root Directory was set to `./` while the project root was actually a subdirectory. Both issues were silent — the deployment "succeeded" in the sense that Vercel did not throw an error, but the served content was wrong (Vercel 404 page instead of the site).

The diagnostic loop was made worse because `web_fetch` against the Vercel URL returned stale cached HTML, making it look like the deployment was failing intermittently when in fact it was consistently broken and the cache was masking the state.

**The lesson:** Vercel deployment troubleshooting must check Build Command (must not point at a nonexistent script) and Root Directory (must match the actual project root, not `./`) before assuming any other cause. `web_fetch` cannot be trusted to confirm live deployment state because of caching; the Vercel dashboard and Ron's own browser are authoritative.

**The fix:**
- Added Phase 7 failure mode documentation for both Build Command and Root Directory misconfiguration (`deployment.md`, Common Phase 7 failures section)
- Added explicit warning that `web_fetch` returns stale cached HTML and cannot confirm live state (`deployment.md`, Phase 7 verification section)
- Added "check Vercel project Build Command and Root Directory before diagnosing other causes" to the troubleshooting decision tree

**Affected files:** `deployment.md`, `SKILL.md`

---

### 2026-04 — INTEGRATION — 21st.dev Magic MCP vendor bug

**Source:** v0.7 build session, throughout
**Severity:** moderate (would be critical if Plan B did not exist)

**The assumption:** The 21st.dev Magic MCP server would be available throughout the v0.7 build and provide live component code on demand from the 21st.dev component library.

**What actually happened:** The Magic MCP server failed to register tools in Claude Code sessions for weeks. Started with `logo_search` working, degraded to nothing working, vendor has not shipped a fix. The skill could not pull live 21st.dev components on demand. A GitHub issue on the vendor's repo (21st-dev/magic-mcp #49) is open with updated symptom data but no resolution.

**The lesson:** External service dependencies have failure modes outside GRM's control. The skill must have a Plan B that does not depend on the third-party service being available. For Magic MCP specifically, the Plan B is a local component reference library at `~/grm-sites-prospects/plan-b-reference/` containing shadcn-ui base-vega variant, magicui, and lucide icons.

The deeper lesson: do not plan around the third-party service returning. Treat Plan B as the long-term path. If the service is fixed and shipped, evaluate switching back as a non-urgent improvement, not a recovery.

**The fix:**
- Plan B reference library committed to local prospect folder with full documentation
- `SKILL.md` Phase 5 references the local library as the primary component source
- `scale-architecture.md` risk inventory names this as ongoing vendor bug risk with mitigation: assume Plan B is permanent

**Affected files:** `SKILL.md`, `scale-architecture.md`, `hero-patterns.md`, `section-patterns.md`

---

### 2026-04 — STRATEGY — The 17% AI/SEO overlap finding reshapes the thesis

**Source:** v0.7 build session, Cowork AI citation research
**Severity:** critical (in a positive direction)

**The assumption:** GRM Web Services was a "better contractor websites" play. The differentiator was technical execution quality, schema discipline, mobile responsiveness, and AI-citation readiness — but the underlying market was traditional SEO competition where GRM would need to outrank existing incumbents over time.

**What actually happened:** The Cowork research returned a finding that reshaped the entire commercial thesis: only 17% of URLs cited by AI assistants overlap with traditional Google Page 1 results. The two systems have diverged. AI citation rewards schema, BLUF content, semantic HTML, and crawler access — none of which depend on backlink authority or domain age. A new contractor site built to v0.7 spec can outperform a 10-year-old incumbent in AI citations starting on day one of indexing.

This is not a "better website" pitch. It is a "we play a different game where your incumbent has no moat" pitch. The strategic thesis shifted from execution differentiation to playing field differentiation.

**The lesson:** Research-grounded findings should reshape strategy, not just technical decisions. When Cowork delivers a finding that contradicts an assumption, treat the finding as authoritative and update the thesis accordingly. The 17% finding is the entire commercial story of GRM and should drive every sales conversation.

**The fix:**
- Strategic thesis section added to `seo-geo.md` framing the 17% finding as the GRM commercial north star
- "Marion County reality" paragraph added to `seo-geo.md` connecting the finding to the actual local prospect base
- Sales conversation script ("Your current site ranks fine on Google...") added to `seo-geo.md`
- All AI citation specific findings (36% schema improvement, 44.2% citation weight in first 30%, 50%/13 weeks freshness) treated as authoritative throughout the skill

**Affected files:** `seo-geo.md`, `scale-architecture.md`, plus all sales collateral that may eventually be derived from this finding

---

### 2026-04 — PROCESS — Sales copy contamination of skill files

**Source:** v0.7 build session, deployment.md and seo-geo.md drafting
**Severity:** moderate

**The assumption:** Sales framing, pitch language, and client communication templates that emerged during skill file drafting could be embedded in the skill files themselves as part of the technical documentation.

**What actually happened:** Ron flagged this explicitly partway through the build: skill files should be technical reference documents, not sales documents. The strategic thesis paragraphs, the scripted sales answers, the monthly client update email template — these were getting embedded in skill files where they would be useful to a future build but where they would also clutter the technical reference and bloat the skill context.

**The lesson:** Sales copy lives in chat output, not in skill files. When technical documentation work produces sales-flavored material as a byproduct, the byproduct gets surfaced in chat and Ron extracts it to a separate sales collateral document. Skill files stay clean technical references.

The exception: when sales-flavored framing serves a direct technical purpose in context (e.g., the strategic thesis section in `seo-geo.md` justifies the technical decisions in that file), it can stay in the skill file. The test: would Claude Code reading the file in 6 months understand the technical decisions worse without this text? If yes, keep it. If no, move it out.

**The fix:**
- Process rule established: sales copy is output in chat for Ron to copy-paste into a separate document, not embedded in skill files
- Existing sales-flavored content in `seo-geo.md` and `deployment.md` audited; the strategic thesis kept in seo-geo.md (justifies technical decisions); the monthly client update email template kept in deployment.md (it is the deliverable, not the pitch); other extracted material output as raw collateral in chat

**Affected files:** Process change applies to all future skill file drafting. No specific file change.

---

### Pre-v0.7 — TYPOGRAPHY — Inter as the silent default on every v0.6 build

**Source:** v0.6 build session, all four prospect sites
**Severity:** critical

**The assumption:** Without explicit font instructions in the skill, the LLM would pick fonts appropriate to each business — a different font for the electrician than the plumber, something serif and warm for a long-established family business, something sans and modern for a newer trade.

**What actually happened:** Every v0.6 site shipped with Inter as the heading font. Every single one. The LLM did not "choose" — it defaulted to Inter on every build because Inter is the most statistically common font in modern web design training data. The result was that every site looked identical not just in layout but in typography too. Inter-as-heading is the universal "this was made by AI" signal.

**The lesson:** Default behavior is the enemy. If the skill does not give explicit, tier-specific *heading font* instructions with banned alternatives, the LLM will pick the AI default every time. Specifying "use a nice font" is not enough. The skill must say "use Fraunces serif for Premium tier headings; use Space Grotesk for Professional tier headings; Inter is fine as the universal body font across all tiers because Inter as a body font is invisible to readers and doesn't signal slop on its own, but Inter as a heading font is the single clearest AI tell."

**The fix:**
- Tier-specific allowed heading font lists added to `anti-slop-rules.md` (banned fonts section)
- Inter explicitly permitted as the universal body font across all tiers (per `css-framework.md`)
- Inter banned as the heading font for Premium and Professional tiers; allowed as the heading font at Standard tier only because Standard's tier signal is simplicity, not heading distinctiveness
- Serif heading discipline mandatory for Premium tier (Fraunces default, Playfair Display / DM Serif Display / Instrument Serif as alternatives)
- Phase 4 design engine checks chosen heading font against banned list before showing the approval gate
- Phase 6 verification (`auto`) parses CSS for font-family declarations and fails the build if a Premium or Professional tier site uses Inter as the heading font

**Affected files:** `anti-slop-rules.md`, `css-framework.md`, `SKILL.md`, `hero-patterns.md`

---

### 2026-04 — COPY — The T&F headline pattern as the locked-in rule

**Source:** v0.7 build, T&F Electric flagship 1; Ron's creative decision
**Severity:** moderate (positive-discovery rather than failure-recovery)

**The assumption (going in):** Hero copy generated from Phase 2 captured data plus general voice rules ("be specific, use real numbers, name real places") would produce strong copy on the first pass. Voice rules were assumed to be sufficient guidance.

**What actually happened:** The T&F Electric hero copy that ended up shipping was Ron's locked-in creative choice: "Fifty years. Two Tuccis. One phone number." Three sentences, eleven words, eight citable facts (years in business, founder family name, owner count, singular contact method). The headline could not belong to any other business — replace "T&F Electric" with any other Marion County electrician and the sentences immediately stop fitting because the founder family name and the years in business are specific to T&F.

When Ron's choice was examined against the generic alternatives (the kind of "Trusted electrical contractors serving Marion County" hero that would have passed voice rules but failed the swap test), it became clear that voice rules alone were not sufficient. The hero copy needed an enforced structural pattern, not just a list of banned phrases.

**The lesson:** Voice rules that ban specific phrases ("passionate about", "trusted partner") are necessary but not sufficient. Copy can technically pass the voice ban list and still be slop because it fails the swap test. Three headline patterns must be enforced as the only allowed structures for hero headlines: (1) real number + real fact + action, (2) time frame + identity + location, (3) specific service + specific place. Ron's "Fifty years. Two Tuccis. One phone number." is the proof case for pattern (2). Without an enforced structural pattern, the LLM defaults to generic wishful copy that voice rules cannot catch.

**Note on attribution:** This entry documents a positive discovery (Ron's creative call established the rule) rather than a recovery from a specific failure. T&F did not necessarily ship a "generic version" first; Ron's choice was simply the standard from the start, and that choice retroactively defined the rule.

**The fix:**
- Three headline patterns made mandatory in `content-rules.md` (hero copy section)
- "Hero copy as primary citation real estate" subsection added to `seo-geo.md` (BLUF content structure section)
- Phase 6 BLUF verification expanded to check the hero specifically: must contain at least 4 of 8 BLUF fact categories before the body content begins (`seo-geo.md`, Phase 6 check 7)
- Anti-slop rules added the swap test as an explicit Phase 6 human check
- Ron's T&F headline preserved verbatim as the exemplar of pattern (2) in `content-rules.md`

**Affected files:** `content-rules.md`, `seo-geo.md`, `anti-slop-rules.md`, `hero-patterns.md`

---

### 2026-04 — DATA — T&F stats numbers wrong in the first build

**Source:** v0.7 build, T&F Electric flagship 1
**Severity:** moderate

**The assumption:** Phase 2 captured numbers (years in business, review count, project count) could be referenced directly in Phase 5 generation without re-validation. If Phase 2 said "50 years," Phase 5 could write "50 years" with confidence.

**What actually happened:** The first T&F build had stats numbers that were either rounded (50 years was correct, but the review count was off by several), guessed where Phase 2 had not actually captured a specific number, or carried over from a different prospect's data due to a context mix-up. Ron caught the numbers during review and corrected them before deployment, but the experience revealed that Phase 2 capture quality and Phase 5 number confidence cannot be assumed.

**The lesson:** Numbers shown on the site are the most checkable, most damaging facts to get wrong. A wrong year, a wrong review count, a wrong "since [date]" claim can be verified by anyone in 30 seconds and destroys trust immediately. Every visible number must be cross-checked against `profile.json` at Phase 5 generation time and at Phase 6 verification time. If a number cannot be sourced to a verified field in profile.json, it must be removed, not estimated.

**The fix:**
- Phase 3.5 silent data quality gate validates that all captured numbers (years, reviews, ratings, founding date) are present and properly formatted in profile.json before Phase 4 begins
- Phase 5 number generation rule: every visible number must reference a profile.json field by path; estimates and round numbers are forbidden unless the underlying data supports them exactly
- Phase 6 check 16 cross-checks every "since [year]" and "[N] years" claim against `profile.json.business.foundingDate` (`seo-geo.md`)
- BLUF content rules in `seo-geo.md` updated to specify that the 8 fact categories must reference real captured data, not generated estimates

**Affected files:** `SKILL.md`, `seo-geo.md`, `content-rules.md`

---

## End of seed entries

The eleven seed entries above span eleven of the twelve categories (PHOTOGRAPHY does not yet have a documented incident; an entry will be added when the first photography failure occurs in a real build). Together they establish the format firmly. Every future build that produces a lesson should append to this file using the same template. Phase 8 of the skill is responsible for the append automatically when the build encounters something unusual; manual appends are welcome at any time.

## Append rules

**When Phase 8 should append automatically:**

- A Phase 6 verification check failed during the build and a fix was applied
- A new prospect data pattern emerged that the skill did not anticipate (e.g., a contractor with 15 services instead of the expected 5-8)
- A workflow gap was identified that required deferring a Phase 7 task for manual handling
- An external service (Vercel, Static Forms, Google Places, MCP) failed in a new way
- Ron explicitly flagged something during the build review

**When manual appends are appropriate:**

- Reflection after a build reveals a hidden assumption that should be named
- A new lesson emerges from a client conversation that affects future builds
- Industry research updates a previous strategic decision
- A successful pattern proves itself enough times to warrant being named as a best practice

**When entries should NOT be added:**

- Trivial typo fixes or minor cosmetic changes
- One-off issues that are not generalizable
- Anything that is already covered by an existing entry (in that case, update the existing entry instead)

**When entries should be UPDATED rather than appended:**

- New information clarifies an existing lesson without contradicting it
- A previous lesson was fixed in a different way than originally documented and the fix should be updated
- An entry has become obsolete because the underlying issue no longer applies (mark as obsolete; do not delete)

## Pruning policy

**Lessons are never deleted.** Once an entry is added, it stays. Even when an entry becomes obsolete, it is marked obsolete rather than removed, because the historical record matters for understanding why the skill is the way it is.

The only time entries can be removed is during a major version rebuild (e.g., v0.7 → v1.0 if v1.0 is a fundamental rewrite). At that point, lessons that no longer apply to the new architecture can be archived to a separate `LESSONS_v0.x.md` file, but they are not destroyed.

---

## Version

LESSONS.md v0.7.0 seed file. Created April 9, 2026 at the end of the v0.7 build session. Eleven foundational entries spanning eleven of the twelve categories (PHOTOGRAPHY does not yet have a documented incident and will be added when one occurs). The format is established; future appends must follow the template above. Phase 8 is responsible for automatic appends; manual appends are welcome at any time. The file grows over time and is read at the start of every new build to remind the skill what has already been learned the hard way.

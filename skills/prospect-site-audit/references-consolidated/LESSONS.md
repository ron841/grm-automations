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
## 2026-04-13 — Skill versioning, spec precision, and the iteration ceiling

**Category:** Process / Skill engineering

### What happened

A six-hour skill engineering sprint attempted to produce v0.7.3 from a baseline of v0.7.1 (Friday floor) and v0.7.2 (Monday morning, regressed). The sprint produced a precise specification document, seven implemented rules across the skill and the site-review mission, and a deployed test build. The deployed build did not meaningfully improve on v0.7.1. All seven rules were reverted at 3:30 PM. The skill was restored to v0.7.1 from a desktop backup.

### The lessons that hold beyond this specific sprint

**1. The skill must be under git before any rule changes.**
Before today, the skill was unversioned plain markdown. v0.7.1's source code was overwritten on Monday's v0.7.2 install and was unrecoverable from the skill folder. The recovery was only possible because Ron had a desktop backup. From now on, the skill lives in git at `~/.claude/skills/prospect-site/.git` and every change is committed. This is non-negotiable infrastructure.

**2. Spec precision does not equal output quality.**
The v0.7.3 spec was the most precise document the skill has ever had — six iterations on the OG composite recipe, exact pixel specs, locked vertical spacing, defined font fallback chain. The implementation matched the spec. The deployed site still missed the bar. Specs prevent ambiguity in execution; they do not prevent the spec itself from being wrong about what "good" looks like. The only true acceptance test is a full rebuild reviewed with real eyes on a real device.

**3. Set a hard iteration ceiling per sprint.**
Today's sprint had no ceiling. Six OG mockup iterations was the right call. Six rules was too many for one afternoon. By the time the rebuild surfaced the problems, the cumulative cost of seven commits made another iteration cycle the wrong investment. Future skill sprints should declare a maximum number of rules upfront and stop when that number is hit, regardless of how many candidate rules remain.

**4. The audit-spec-implement-rebuild cycle is too long to run more than once per sprint.**
Plan for one full cycle per sprint. If the rebuild reveals problems that need another spec revision and another implementation pass, the sprint is over and the work moves to the next sprint. Compressing two cycles into one day produces the failure mode where reverting becomes the only sane option.

**5. Manual touch-up per build is a legitimate strategy.**
Pursuing skill perfection while real prospects are waiting to be contacted is the wrong tradeoff. The skill produces a good first draft. Ron's eye is the final filter. A 15-30 minute manual edit pass per deployed site is acceptable, expected, and scales reasonably for the current prospect volume. This is documented in the post-build edit playbook at `~/grm-automations/docs/post-build-edit-playbook.md`.

**6. The audit infrastructure (grm-browser + Playwright) earned its keep.**
Even though today's sprint reverted, the 36-capture audit produced in 30 minutes was the right tool. Future sprints should use it. Real rendered output beats assumptions every time.

### What this means for future skill changes

- Any future skill rule change starts with a git commit of the current state, a stated iteration ceiling, and a defined acceptance test that includes a full rebuild on a real prospect.
- Skill changes that make the deployed output worse get reverted, not patched. v0.7.2's regressions and v0.7.3's failure to improve on v0.7.1 are both examples — the right move in both cases would have been earlier reverts.
- The post-build edit playbook is the active workflow. The skill is the first draft, not the final product.

### Files affected

None. This is a process lesson, not a code change. The skill at v0.7.1 (commit `0498ca3`) is the active code.

### Reference

- v0.7.3 spec preserved at git commit `7134045`
- All seven v0.7.3 rule commits preserved at `e688101` through `47135d9`
- Today's handoff doc at `~/grm-automations/docs/handoffs/HANDOFF_2026-04-13.md`
- Audit captures at `~/grm-automations/audits/tandf-v07-vs-v072-2026-04-13/`
- v0.7.2 snapshot at `~/grm-automations/flagship-snapshots/tandf-electric-v072-2026-04-13/`

Magenta gradient cards (start #9c5494) — H3 contrast borderline AA at 4.29:1 in top-left corner. Revisit when expanding card pattern library. First occurrence: A-1 Payless Septic flagship, 2026-04-15.

A-1 Payless Septic flagship — shipped 2026-04-15 with Ron-led polish pass. Key decisions that elevated the build: (1) sitewide secondary-CTA removal caught a skill bug that repeated on 5 pages; (2) alternating magenta/cream services grid with equal-size cards — stronger rhythm than default Bento asymmetry for this palette; (3) homepage hero swap to the prospect's own company truck photo after re-crawl caught a CSS background-image the original regex missed; (4) services.html slim image band with "pump truck hose-into-manhole" shot as editorial counterpoint to hero. Post-launch skill work: fix Phase 1 background-image crawl, audit CTA component for trailing-fragment pattern.

Social preview metadata — og:image, twitter:image, and the full social preview block must be present on every page, not just index. The skill currently only generates a partial og: block on index and leaves secondary pages bare. Also: any hero swap post-build must update og:image / twitter:image sitewide. First caught: A-1 Payless Septic flagship, 2026-04-15 — Ron flagged missing iMessage thumbnail. Action item for post-launch skill work: add full social preview meta generation to every page template, and add a hero-swap verification step that checks og:image / twitter:image / og:image:width / height / alt across all pages.

Phase 7 slug regeneration — the skill drafts URLs in Phase 1 using the full business slug, but Phase 7 shortens the slug to meet Vercel naming constraints. No Phase 7 step regenerates URL references after the slug change, leaving every slug-bearing artifact pointing at a URL that 404s. Affected artifacts in a default build: <link rel=canonical>, og:url meta tag, Static Forms redirectTo hidden input (BREAKS LEAD CAPTURE — every form submission redirects to a 404), LocalBusiness JSON-LD @id and url fields, sitemap.xml <loc> entries, llms.txt page links, robots.txt sitemap pointer. First caught: A-1 Payless Septic flagship, 2026-04-15 — 16 stale-slug references total across the build. Action item for post-launch skill work: add a Phase 7 step that takes the final deployed Vercel alias and regenerates every URL reference across HTML files, XML files, TXT files, and JSON-LD blocks. The form redirectTo is the most critical — do not ship a build without verifying successful form submission terminates at a live thank-you page.

### 2026-04-16 — WORKFLOW — Progressive-enhancement guard on `[data-reveal]` sections

**Source:** Grandview Inc (F4), v0.7.2 build, 2026-04-16 afternoon session
**Severity:** critical

**What happened.** Phase 5 wired `data-reveal` on five homepage sections (services, stats, testimonials, faq, contact). The CSS set their initial state to `opacity: 0; transform: translateY(30px)` unconditionally. A JS IntersectionObserver added `.revealed` to flip them back to opacity 1 on scroll. In the Phase 6 Playwright full-page screenshot at 375px, the observer did not fire reliably during the scroll-and-stitch capture — so the screenshot showed hero and footer with a giant blank expanse between them. If JS had failed entirely (legacy browser, bot crawl, reduced-JS environment), real visitors would see the same blank page. The bug was caught by a visual eye check on the mobile screenshot, not by any Phase 6 check.

**Why it matters.** A sales-weapon preview must degrade gracefully. Bots crawling for SEO, reduced-JS users, and automated screenshot tools all exist. Content rendered conditionally on a JS observer is not a defensible default.

**Fix applied (for this build).** Changed CSS selector from `[data-reveal]` to `.js [data-reveal]` for the hidden initial state, and added `document.documentElement.classList.add('js')` at the top of `script.js` before any DOMContentLoaded listeners. Progressive enhancement: no-JS clients see content by default; JS-enabled clients get the reveal animation. Same treatment applied to the reduced-motion override.

**Fix applied (for the skill).** `css-framework.md` §Vanilla JS animation toolkit → `[data-reveal]` CSS pattern must be updated to use the `.js` prefix. `script.js` bootstrap section must include `document.documentElement.classList.add('js')` at the top of the IIFE. Add a Phase 6 check that catches this: after forcing no-JS rendering in a headless browser, verify every [data-reveal] section has `getComputedStyle().opacity === '1'`.

**Cross-reference.** Same class of bug showed up in the stats `data-target` counters: HTML rendered `0` as baseline and relied on JS to tick up to real numbers. Fix: HTML now renders the final numbers; JS resets to 0 inside the observer callback before animating. No-JS users see correct stats; JS users see the animation. Documented here as a companion lesson.

**RESOLUTION.** v0.7.3 commit #2 (`f302d49`). Skill now defaults `[data-reveal]` sections visible unless JS has added `class="js"` to `<html>`. Required inline script documented in `css-framework.md` "Required head-inline script for progressive-enhancement guard".

### 2026-04-16 — COPY — Agent-invented "Licensed" in title + schema

**Source:** Grandview Inc (F4), v0.7.2 build, 2026-04-16 afternoon session
**Severity:** moderate

**What happened.** Phase 5 was delegated to a build agent. The profile-draft.json explicitly documented "License number: NOT FOUND" and the build instructions said "Do NOT render a license number anywhere. Do NOT write 'Licensed' in CTAs or footer." The agent complied in body copy and CTAs but invented "Licensed Ocala Landscaping Since 1999" in the `<title>`, the og:title, the twitter:title, and the LocalBusiness JSON-LD `description` field. Caught by a post-deploy curl grep on the live URL that read the title and spotted "Licensed". Quick manual fix + redeploy.

**Why it matters.** Title tags and JSON-LD are indexed by search engines. An invented "Licensed" claim in schema.org data is a fabrication that a diligent prospect could use to question our credibility. The instruction was explicit; the agent still regressed on page-metadata surfaces that aren't typically reviewed in the visual eye check.

**Fix applied (for this build).** Removed "Licensed" from index.html title, og:title, twitter:title, and LocalBusiness JSON-LD description. Replaced with "Family Owned" / "Family-owned". Redeployed.

**Fix applied (for the skill).** Add to Phase 6 check 3 (banned output check) a specific grep for "Licensed", "Licensure", and "License #" across title tags, meta tags (og, twitter), and all JSON-LD blocks — not just body copy. Build-agent prompts should move the "do not invent license" rule to the top of the section-header instructions (agents regress on later-mentioned constraints when the prompt is long). Consider a dedicated "fabrication check" step in Phase 6 that specifically diffs agent-written metadata against the profile.json `unknownFields` list and fails on any term that matches a known unsourced claim.

**RESOLUTION.** v0.7.3 commits #3 (`13b4189`), #4 (`074e936`), #5 (`413ac25`). Banned credential list in `content-rules.md` blocks "Licensed"/"Insured"/"Certified"/etc. at Phase 6 check 3 unless `profile.json` captures supporting data. Phase 6 checks 19 and 20 add schema-to-profile cross-reference and unknown-field guard for defense in depth.

### 2026-04-16 — INTEGRATION — Vercel bot mitigation blocks Static Forms curl test

**Source:** Grandview Inc (F4), v0.7.2 build, 2026-04-16 afternoon session
**Severity:** moderate

**What happened.** Phase 6 check 14 (live form submission test) POSTs a test payload to `https://api.staticforms.xyz/submit` to verify accessKey validity and account health before deploy. The POST now receives a Vercel "Security Checkpoint" HTML challenge page (HTTP 429) regardless of user agent, content-type, or request origin headers. The challenge is a Vercel-side bot mitigation on the Static Forms edge, not a Static Forms rejection. The real accessKey is never tested.

**Why it matters.** Check 14 was the automated guardrail against shipping a site with an expired Static Forms key. With the curl path blocked, we have no build-time signal, and the first time we'd learn the key was broken is when a prospect submits the form and nothing arrives in Ron's inbox.

**Fix applied (for this build).** Marked check 14 as DEFERRED. Plan: verify form submission in a real browser on the deployed URL as part of the Six Checks (check 6, Ron's eye test). Not ideal, but the skill should not block deploy on an integration we can't reach.

**Fix applied (for the skill).** Rewrite check 14 to run the submission through a headless browser that executes the Vercel challenge JS (Playwright with `page.goto` to the staticforms endpoint, then POST via `fetch` in the page context). Alternatively, switch to an accessKey-validation endpoint if Static Forms publishes one, or monitor for a test token delivery to Ron's inbox via Gmail MCP after a build-time submission. Until one of these lands, check 14 is DEFERRED with a visible warning in the Phase 6 report. Add a post-deploy sanity test: Ron taps "Submit" on the real form and confirms the thank-you page within 60 seconds of deploy.

**RESOLUTION.** Not addressed in v0.7.3. Manual browser eye test is the authoritative form check going forward. `deployment.md` language reframe deferred to a future patch.

### 2026-04-16 — TEMPLATE — Footer-logo flatten filter is wrong default

The template's `.footer-logo` CSS applied `filter: brightness(0) invert(1)` to every footer logo. This flattens multi-color logos to white silhouettes. Grandview's multi-color logo (gold wordmark + green palm + banner) became an empty white rectangle in the footer. Compounded by the logo asset having no alpha channel (GIF→PNG conversion preserved white fill as opaque), the silhouette was indistinguishable from a white block.

Fix: v0.7.3 commit #1 (`e40f19b`) removed the filter unconditionally. v0.7.3 commit #6 (`b90b57a`) added a Phase 1 chroma-key rebuild for no-alpha source logos. Logos now render in native brand colors on dark footers.

Lesson: default template CSS choices that "work for most cases" (assuming single-color wordmarks) can fail silently and universally for the cases that do not fit. Template defaults must be defensible against the full range of real inputs, not just the clean-case subset.

### 2026-04-16 — DETECTION — Secondary brand marks need explicit Phase 1 flagging

Grandview had two logos in use: the horizontal wordmark (correctly identified as primary) and a round "Grandview Farms" badge tied to the sod farm / agriculture side of the business. The round badge was inventoried by the crawler as a generic inline image (`s28.avif`) but never recognized as a secondary brand mark. It had to be retrofitted post-build at significant agent-hours cost.

Fix: v0.7.3 commit #7 (`6d60a9f`) added Phase 1 step 4b, which detects round-ratio images 150–600px in CMS upload directories as candidate secondary brand marks and surfaces them at the Phase 4 approval gate.

Lesson: the Phase 1 crawler should not be a passive asset inventory. It must actively categorize images based on shape, size, and source path — these are strong semantic signals about what role the image plays in the prospect's brand system.

### 2026-04-16 — PRESERVATION — Skill-repo durability depends on mirror pattern

The `~/.claude/skills/prospect-site/` repo has no remote configured. Tonight's preservation work established a mirror in `~/grm-automations/skills/prospect-site/`, which has a GitHub remote. The mirror is currently the only off-host copy of the skill tree.

Deferred decision: whether to add a dedicated remote to the skill repo itself (e.g., a GitHub repo specifically for the skill), or formalize the mirror-to-grm-automations pattern as the ongoing preservation mechanism (with periodic rsync + commit + push to the mirror).

Both approaches work. A dedicated remote is cleaner; the mirror pattern is simpler. Decide post-v0.7.3 launch work.

### 2026-04-27 — WORKFLOW — render.py phase-history provenance migration

**Source:** v1.0 rewrite arc, REWRITE-open (Phase A item #2)
**Severity:** minor

**What this is.** At SIMPLIFY-close, render.py carried 78 inline phase-history annotations (Phase 3a/3b/4/4.5/5.0a-c/6.0a-d + Patch 2/3/4) across docstrings and inline comments. The annotations mixed operational rules (data contracts, fallback chains, anti-slop disciplines, SEO/GEO emission logic, deploy-boundary constraints) with pure provenance ("Phase 4 added X"). Per the audit-side append-only pattern, REWRITE-open Phase A item #2 migrates the phase tags here as a structured map; the operational substance stays in render.py as clean comments.

**The map below is phase-tag → behavior-it-introduced-or-changed, in operational terms not code dump.** Per-line git blame (against the frozen source corpus at `~/Desktop/v1.0-assembly/02-composer-side/scripts/render.py`) remains the deeper provenance source for any "show me the actual diff" lookup.

**Phase 3a (2026-04-25)**
- prose.json migrated from flat keys → nested page-key shape (homepage / about / services / testimonials / contact). Homepage band renderers read `ctx["prose"]`; inner-page renderers read sibling pages via `ctx["all_prose"][page_key]`.
- `page_key` dispatch added at `render_page`; inner pages emit `<body class="is-inner">` so the §12/§13 CSS lift fires while the homepage `<body>` stays unscoped to preserve the fixed-overlay nav cascade.
- `_hex_to_rgb_tuple` helper added to feed per-prospect rgba() patterns (`rgba(var(--color-primary-rgb), 0.10)`) into the bundle vocabulary so it tints correctly for non-JSL prospects.
- StaticForms accessKey shipped as placeholder; Phase 4 added real-key injection at deploy.

**Phase 3b (2026-04-25)**
- §1 promo-callout band (gated on `profile.promotions.featuredPromo`).
- §2 before/after band (stub; gate exercised, markup intentionally minimal until first paired-photo prospect forces the lift, per `dropped-sections.md` §2).
- §3 universal-ship sticky bottom mobile CTA bar (hidden on desktop via §14 CSS).
- §4 shared FAQ band renderer (homepage + services-page).
- §5 4-tile dark stats band with distinguishing-stat 4th tile (5-rule library, evidence-floor gated).
- Default header strings collocated with renderers (not fixtures) so prose.json stays optional. All strings §6-rule-compliant.

**Phase 3e (2026-04-25)**
- Slug → (question, short-label) FAQ dispatch table. Slugs not in the table are skipped, never fabricated. `resolve_faq` derives 5–7 items from profile data or honors a prose-authored override; mutates profile in memory only (no write-back per "fixtures are authored truth").

**Patch 2 (2026-04-24)**
- Anchor strip restructured: brand signature row on top, three-column triad below (location / serving / studio hours).

**Patch 3 (2026-04-24)**
- `hero-stat--lead` vs `hero-stat--sec` class structure. Strongest stat (priority-order match) becomes the LEAD stat at dominant size; the other two are secondary at demoted weight. Google review count reshapes so the count is the headline number, the rating sits in the supporting label.

**Phase 4 (2026-04-26)**
- Trust marquee items: 6-tile derivation for the `.trust-marquee` homepage band (rating + review count + license + veteran-owned + master electrician + family-operated), floor at ≥3 items.
- Featured-first sort overlay on the testimonials scorer (testimonials with `featured: true` sort ahead, score-fill behind, backwards-compatible to pure-score behavior when no entries carry `featured`).
- StaticForms `access_key` plumbing through ctx with `--access-key` CLI flag; deploy pipeline substitutes the real key via `sed` at the pre-Vercel boundary.
- Page-aware testimonial caps: hard 6-cap when ≥1 featured exists; ship-all when zero featured.

**Patch 4 (2026-04-25)**
- Wordmark anchor points at `/` (not `#`), so the click target works on every page once the site is multi-page. Mirrored in render_footer's inline wordmark.
- Title separator must be middle-dot for `<title>` consistency across pages.
- Google photo attribution: per-page footer credit when `assets/photos/google/*` photos are emitted. `_attributions.json` is per-photo source of truth; never hardcode `profile.businessName.legal` as the contributor (only coincidentally correct for owner-uploaded photos like Volthom; most prospects ship customer-contributed photos). Skip the sentence-final period when the last contributor name already ends in one.

**Phase 4.5 (2026-04-26)**
- Service `featuredImage` path resolution → inline background-image on `.service-card-featured` (CSS gradient fallback when absent).
- FAQ + contact-section dropped from services.html (homepage close-the-deal sequence retains them; inner pages stay focused on their reason-to-exist content).
- Testimonials.html cap raised 6 → 12; reviews page should be heavier than the homepage section.

**Phase 4.5b (2026-04-26)**
- Service `detailImage` wired (parallel to `featuredImage`) for the services-page service-detail-image slot.
- Homepage services-header eyebrow ("THE CRAFT" default), with the cross-page handoff: homepage "THE CRAFT" → services.html "AT A GLANCE" → services-detail "IN DETAIL". Three distinct anchors, no duplication on Home → Services traversal.

**Phase 5.0a (2026-04-26)**
- Brand mark resolution from ctx (`assets/photos/site/site-09.jpg` when present; inline-SVG placeholder otherwise). Volthom ships site-09; future prospects vary.
- Inner pages adopt flagship-canonical `.page-hero` / `.wrap` / `.eyebrow` / h1 / `.lede` vocabulary; `_page_hero_html` supersedes `_subpage_hero_html` for new emits (the older helper is preserved for any prospects rendering against the prior vocabulary).
- Footer no longer carries `id="contact"` (collided with contact.html's `<section id="contact">` form section). Footer "Explore" links point at page files, not hash anchors, so the footer works identically on homepage and inner pages.
- Site testimonials and Google testimonials split into separate t-grids ("From our site" / "From Google"), with the pq-band as the pullquote-band opener of the lower section (later dropped in Phase 6.0b).
- Mobile CTA bar quote button targets `contact.html` (universal target), not `#contact` (which only resolved on the homepage).
- "Services" navlink reads "The Craft" for flagship-canonical alignment with the services-bento eyebrow (Volthom homepage already shipped "THE CRAFT" eyebrow).
- Inner-page sitenav unified with homepage shell (same wordmark, `id="sitenav"` for the scroll listener, `body.is-inner` CSS scope, `aria-current='page'` on the current page link).

**Phase 5.0b (2026-04-26)**
- `resolve_service_photos` pre-populates service `featuredImage` / `detailImage` fields from `_unsplash-cache.json` when fixtures leave them null. Slugs flagged `gradient_fallback` in the cache stay null and ship the CSS gradient.
- Unsplash attribution in footer (per Unsplash API Terms requirement for per-photo credit linking back to photographer profile and to unsplash.com). Deduped first-appearance order, renders alongside the Google attribution row.
- Services-page bento renders the same non-featured photo-mode card as the homepage flow. Cross-context reuse intentional — photo discipline rule applies per visual context (`feedback_photo_discipline.md`).

**Phase 5.0b.2 (2026-04-26)**
- Homepage small bento cards always render text-only, even when `featuredImage` is populated. Photo treatment on small cards lives only on `services.html` (homepage's job is orient + anchor; the featured photo card already does that, additional photo tiles add clutter without conversion lift).
- Yellow CTA underline mirrors the featured-card CTA pattern across every photo card (unifies the bento as one designed system).

**Phase 5.0c (2026-04-26)**
- Declarative brand-pillar register replaces the heritage italic-serif manifesto. New prose schema is `{headline, body}` (body optional). Renders into `.manifesto-band` (separate vocabulary from heritage `.manifesto` class so the two don't collide).

**Phase 6 SEO/GEO layer (2026-04-26)**
- Per-page `<meta description>`, canonical URL, OG + Twitter Card meta tags, and a single `Electrician`-typed JSON-LD LocalBusiness block in `<head>`. Skips canonical / og:url / JSON-LD when `--canonical-base` is unset (engine still renders cleanly for prospects without a fixed prod URL).

**Phase 6.0b (2026-04-26)** — Design audit pass
- Stats-band: a bare "0" tile reads as broken/unloaded data, not as a positive claim. Skip the rule when `below` resolves to exactly 0 (the perfect-rating case) and let the next rule (founding-year, owner-count, license-recency, geographic-radius) carry tile 4.
- Testimonials-page perfect-rating display: drop the "5.0★" tile when rating is exactly 5.0; two confident metrics > three with a soft third.
- Manifesto eyebrow ("THE PROMISE" default, prose-overridable) paired with the heritage 4px naked rule (rule was undercommitted alone). Eyebrow IS the structural anchor; 32px navy bar lives as a CSS `::before` pseudo on the eyebrow element.
- Pullquote band on testimonials-page dropped (the Mellini quote already appeared in the from-site grid above; reusing it as a band visually rhymed with the homepage `.pullquote` and diluted both surfaces).
- Services hero promoted from `.subpage-hero` (navy field, no imagery) to `.page-hero` (paper-warm rhyme with about / testimonials / contact). Mixed state was the worst option per Design audit Q2.
- Contact area-band abbreviated to a single-line summary (full "Where we work" treatment lives on About; same density on Contact felt like a slightly-lighter About).

**Phase 6.0c (2026-04-26)**
- License caption emitted as a small below-lede row when `profile.credentials.licenseNumber` is present. License-as-credential wants its own register, not buried in the services subhead body sentence. Caption is engine-derived from profile data; every prospect with a license number gets the treatment automatically.

**Phase 6.0d (2026-04-26)**
- Awards-derived hero stat dropped: wrong shape for a 2-3 word stat tile; full award text lives in About cred-grid where it belongs.
- Awards-derived trust cell dropped for the same reason.
- Homepage CTA band replaces the embedded contact form. Form belongs on `/contact` only; homepage gets a CTA band as the conversion-ladder rung (per Design audit + flagship F2/F5 reference).

**The lesson.** At v1.0 rewrite, render.py inline phase-history annotations had become noise that obscured operational discipline — the same line carrying both "Phase 6.0b: Design audit" provenance and "skip this rule when below resolves to exactly 0" anti-slop substance. Migrating provenance here and keeping render.py comments focused on non-obvious WHY (constraints, workarounds, data contracts, voice rules, API-Terms compliance) sharpens both files. Future rewrites should not need this migration again — the audit-side append-only pattern lets LESSONS.md absorb provenance directly as new behavior lands, in dated entries that survive rewrites without polluting source.

**Affected files:**
- `_destination/build-half/scripts/render.py` — phase-tag prefixes stripped, substance preserved as clean comments.
- `_destination/references-consolidated/LESSONS.md` — this entry.


## Session 3 — first fresh prospect end-to-end (Testerman's Pro Wash, 2026-04-29)

First cold run of v1.0 audit-half against a fresh prospect not previously audited. End-to-end Phase 0 → Phase 8 in a single session, deployed live at `testermans-pro-wash-grm.vercel.app` with 5 spec-defects surfaced.

**Spec-defect docket (engine-misbehaved class — fixed in-session):**

- **S3-2 — `vercel teams ls 2>/dev/null` returns empty in non-TTY mode.** deploy.sh Step 1 verification fails because Vercel CLI writes its formatted table to stderr in non-TTY contexts; `2>/dev/null` swallows it, the grep gets no input, the team-scope check fails. **Patch:** `2>/dev/null` → `2>&1` at deploy.sh L66.

- **S3-3 — `vercel project ls` same stderr/non-TTY issue + awk extraction targets a column that doesn't carry projectId.** Bug 6A (staging-dir basename leaks into project name) re-surfaces because PROJECT_ID resolves empty → no `.vercel/project.json` → `vercel deploy` auto-creates project from CWD basename. The docstring "closes Bug 6A" is misleading; the underlying mechanism never worked in non-TTY mode. **Patch:** replaced manual `project.json` write with `vercel link --yes --project "$PROJECT_NAME" --scope "$VERCEL_SCOPE"` (deploy.sh L160-172).

- **S3-5 — `set -euo pipefail` + grep no-match on PINNED_NAME extraction kills script silently after Step 1 echo.** When `.vercel/project.json` exists from a prior deploy but lacks a `"name"` field (Vercel-written project.json carries `projectId` + `orgId` only), the grep returns 1 and pipefail propagates. **Patch:** `|| true` defense at end of the pipe at deploy.sh L93. Same defense pattern likely needed across the deploy.sh grep|sed|head pipelines.

**Class observation across S3-2 / S3-3 / S3-5:** the defect class is *bash-strict-mode meets Vercel-CLI-non-TTY-output*. `set -e` + `2>/dev/null` + `grep|sed|head` is brittle when input pipelines silently produce empty output. Future deploy.sh hardening should sweep for the pattern.

**Spec-defect docket (audit-side / engine-emit class — workaround applied, fix pending):**

- **S3-1 — Hero subhead em-dash leaks into `<meta name="description">` / `og:description` / `twitter:description`.** The §6.2 hero subhead em-dash is intended for the body `<p class="hero-sub">` only; render.py copies the subhead text verbatim into all four meta-description surfaces, propagating the em-dash. Phase 6 grep gate flags 3 utf-8 + 1 entity em-dash on every prospect with a §6.2-shape subhead. Volthom v1 emit shows the same pattern, confirming pre-existing behavior. **Working scope:** treat all subhead-sourced surfaces as in-scope §6.2 exception per Volthom precedent. **Real fix:** render.py should strip the em-dash (or replace with comma/period) when copying subhead into meta-description path. Pending.

- **S3-4 — `build_sitemap_xml()` and `build_robots_txt()` defined in render.py but never called from `main()`.** Sites deploy without sitemap.xml or robots.txt unless audit-half generates them manually. **Workaround:** post-Phase-5 manual generation by invoking the build functions from the Python REPL, then sidecar-stage into fixtures dir for deploy.sh to pick up. **Real fix:** wire `build_sitemap_xml` + `build_robots_txt` into `main()` to emit alongside HTML when `--canonical-base` is set. Pending. Joins llms.txt as the sidecar-emit pattern that wants engine consolidation.

**Lessons not specific to a defect:**

- **Profile-shape-vs-engine-contract reconciliation must precede prose authoring.** Initial profile-draft.json used `ratings.googleRating`, `social.facebook`, `owners[]` paths; render.py reads `googleBusiness.rating`, `socialMedia.facebook`, `owners.list[]`. Caught at Phase 5 Step 2 by reading fixture-contract.md before authoring. **Discipline:** read the contract first; do not author against the captured profile-draft shape. Per `feedback_inventory_before_cut.md`. Tracks as third-instance confirmation that spec-not-consulted is the heaviest inventory-before-cut subspecies.

- **Brand-color CSS-dominance check warrants role-swap on Vibrant→primary mechanical mapping.** Testerman's logo extraction returned Vibrant=red / DarkVibrant=blue. CSS dominance was 23× blue vs 8× red across the live site — clear editorial signal that BLUE is the primary brand and RED is the accent/CTA. Mechanical Vibrant→primary mapping inverts the live brand. **Pattern:** at Phase 4 approval gate, surface CSS dominance counts alongside node-vibrant swatches; recommend role-swap when CSS dominance contradicts mechanical mapping. Generalizable: any prospect whose logo Vibrant is the CTA/accent (not the primary surface color) hits this pattern.

- **Three-class slot taxonomy held cleanly on first fresh prospect.** Required-author / override / sparse-drop classification (codified Session 2) drove every Phase 5 Step 2 decision. Override-class slots (eyebrows, ledes, cta_band) shipped engine defaults where defaults matched register; only headline-class and pullquote-class required prospect-specific authoring. Confirms taxonomy generalizability beyond Volthom.

- **NiceJob testimonial widgets are JS-only.** Testerman's `/testimonials/` page rendered as a 538-char shell — the actual reviews load from a NiceJob third-party widget at runtime. Audit must fall through to Google Places Details API to capture real reviewable text. Worth flagging when capturing future prospects: testimonial pages with low body-text counts likely indicate a JS widget, not absent reviews.

- **Universal-spectacle backlog logged.** Per Ron's Phase 4 direction (2026-04-29): the tier system (Premium / Professional / Standard) is being collapsed in v1.1 in favor of a universal-spectacle target gated only by sparse-drop discipline. Three-class slot taxonomy already handles data-sparseness via sparse-drop; tier-gating is increasingly redundant. Defer the refactor; ship v1.0 with tier system intact.

**Counts at session close:** 5 spec-defects surfaced (3 patched in-session, 2 workaround-shipped). Site live + JSON-LD aggregateRating populated (5.0 / 841 reviews). All Phase 6 verification gates pass (working scope per Volthom precedent on S3-1).

## Session 3 Round-2 diagnostic — phone-walk findings on cold-walk-2 deploy (2026-04-29)

After cold-walk-2 verified all 9 fix-pass items landed live, Ron's phone walk surfaced 6 spectacle-ceiling findings. Chad's reframe: this is a diagnostic walk, not a fix-pass — every finding should trace to the engine principle the v1.0 rewrite missed. Surgical fixes ship only when they encode the principle (don't author around the gap).

### Engine principles surfaced (v1.1 backlog priority above the existing engine-extension queue)

**P1 — Volthom-arc additions need a "rent-on-every-prospect" filter at SIMPLIFY phase.**
The manifesto band was added at Volthom Phase 5.0c (2026-04-26) as a per-prospect spectacle move. v1.0 SIMPLIFY (Session 1) inherited it uncritically — it shipped because it was already in the codebase, not because it was diagnosed as universal-spectacle. The (c)-trace gap: post-Volthom additions never got re-interrogated against "what does the engine ship for every prospect?" before the rewrite locked. Future SIMPLIFY phases need an explicit per-band rent check: (a) does this pay rent on every prospect? (b) does this compete with another band for the same attention surface?

**P2 — The homepage ships ONE warmth surface, and that surface IS the conversion-ladder cta_band.**
On Testerman's cold-walk-2 the manifesto band ("We wash. We seal. We come back next year.") and the cta_band ("Call us. Text us. *Send the details*.") both shipped on warm-peach `--manifesto-band-bg`, separated only by the pullquote. Cumulative attention drain. Decorative warmth bands compete for the same conversion budget and degrade it. Action: render_manifesto removed from emit chain at render.py:3639. Voice principle preserved at prose-rules.md §6.4 (the declarative brand-pillar register can still be expressed in other slots — story_paragraphs, service taglines, hero kicker).

**P3 — Phase 1 logo capture lacks a documented priority chain. Favicon was the silent default.**
SKILL.md Phase 1 step 3 says "extract... primary logo URL" without specifying a priority order. My implementation defaulted to favicon `<link>` parsing, which yields the lowest-resolution variant (200×200 brand-kit favicon export for Testerman's). The full-resolution logo (488×344, 167KB) was sitting at `wp-content/uploads/2023/11/TESTERMANSLOGO_FC_1-CMYK-150ppi-RASTER.jpg` — same naming pattern as the favicon, just without the dimension suffix. **Engine principle:** Phase 1 logo capture priority chain should be: WP-content/uploads/* with `logo|brand|wordmark` keywords (try the original variant before any `-WxH-optimized` thumbnails) → about-page hero `<img>` → header `<img>` → schema.org `publisher.logo` → OpenGraph image with logo-like aspect → favicon (last resort, low-res).

**P4 — wm-mark slot was shaped for square logos. Wide-aspect lockups (illustrated character + wordmark) need height-controlled flexible width.**
The `.wm-mark` CSS rule was hardcoded `width:34px;height:34px` because the Volthom site-09 brand swirl was square. Testerman's logo is 1.42:1 wide (illustrated character + "Testerman's PRO WASH" wordmark side-by-side). At 34×34 square crop, the wordmark gets cut off and the character pixelates. **Engine principle:** wm-mark slot is height-controlled (height:48px), width:auto, flex-aligned. Engine `resolve_brand_mark_html` omits width/height attributes on `profile.logo` emit so the CSS rule controls. The Volthom site-09 fallback keeps explicit 34×34 because that swirl is square.

**P5 — The header background MUST be brand-responsive, not literal RGB.**
composer-system.css:65 hardcoded `.sitenav.scrolled{background:rgba(22,33,16,.82)}` — that's `#162110` JSL-palette dark green. The role-swap to Testerman's blue+red couldn't affect this surface. **Engine principle:** every brand-responsive surface references the palette via CSS variable. Hardcoded RGB values in structural surfaces fail the role-swap discipline. Action: changed to `background:var(--color-dark-primary);opacity:.92`. Brand-responsive sweep needed across composer-system.css for any other hardcoded color values masquerading as Volthom-default.

**P6 — Story-img priority chain needs a team-identity tier between ownerPortrait and site-04.jpg.**
S3-14 patched the misclassification (hero photo no longer falls into "team portrait" alt) but the new chain `ownerPortrait → site-04.jpg → sparse-drop` is too narrow. Family-business prospects often lack a literal owner portrait but have crew/team/customer-with-crew shots that anchor family-identity register. Testerman's s44 is the canonical example: 2 crew in branded shirts + customer holding "Testerman's CLEANED MY HOUSE!" branded yard sign + finished Florida home. Family-business identity incarnate without a literal portrait. **Engine principle:** story-img priority chain expands to `ownerPortrait → teamIdentity → site-04.jpg → sparse-drop`. Action: render.py:2215-2228 extended; profile.json adds `photoLibrary.teamIdentity` slot.

**P7 — Photo-to-service Unsplash fallback fires globally (when total photos <4) but not per-service-slug.**
Testerman's house-painting service ships gradient on services.html because no captured photo matches that slug AND `_unsplash-cache.json` is absent. Total photo count is 70 (high) so the global tier-4 Unsplash trigger never fires. But individual service slugs CAN be photo-poor when global capture is high. **Engine principle:** Unsplash fallback should be per-slug, not global. When a service slug has no `featuredImage` OR `detailImage` set AND the captured photo set has no content-tagged match, the resolver should fire `unsplash_fetch.py` for that slug. Backstop: if the slug has no built-in `SERVICE_PHOTO_QUERIES` entry AND no per-prospect `stockQuery` override, the engine should sparse-drop the service from the homepage bento OR cut it from the services lineup — never ship gradient on a sales-active preview. Logged for v1.1.

### Surgical fixes shipped this session (encode principles, don't mask)

- `render.py:3639` — `render_manifesto` removed from homepage emit chain (P1 + P2)
- `composer-system.css:65` — `.sitenav.scrolled` background → `var(--color-dark-primary)` (P5)
- `composer-system.css:67-68` — `.wm-mark` height-controlled, width:auto, flex-align; img inside follows (P4)
- `render.py:336-352` — `resolve_brand_mark_html` omits width/height attrs on profile.logo emit (P4)
- `assets/logo.jpg` — replaced 200×200 favicon-export with 488×344 full-res original (P3)
- `profile.json:logo.dimensions + sourceNote` — full-res confirmed + Phase 1 priority-chain principle documented (P3)
- `render.py:2215-2228` — story-img priority chain extended with `photoLibrary.teamIdentity` tier (P6)
- `profile.json:photoLibrary.teamIdentity` — set to `s44_IMG_9283` (P6)
- `prose-rules.md §6.4` — engine-band-removed status documented; voice principle preserved (P2)

### Surgical fixes deferred — would mask the principle gap

- **House-painting Unsplash fallback** (P7): would require running `unsplash_fetch.py` for the slug to populate `_unsplash-cache.json`. Doing this per-prospect ad-hoc this session would mask the per-slug fallback principle gap. Logged for v1.1; gradient ships on this prospect as intentional spectacle-floor evidence of the gap.
- **Wordmark text suppression when image-logo present** (P3 sub-rule): Chad's frame says when a real full-res logo lands, the engine-emitted "Testerman's Pro Wash / EST. CLERMONT, FL" wordmark text becomes redundant. This is a per-prospect editorial judgment that should NOT auto-fire — sometimes the brand wants both, sometimes the logo IS the wordmark. Engine principle for v1.1: prose-overridable boolean `wordmark_text_visible` defaulting to true; suppression is editorial, not algorithmic. Logged.
- **BBB A+ verification** (M5 carryover): `bbb.org` blocked direct fetch; without verification, BBB stays out of credentials. Carries forward unchanged.

### Closure-boundary discipline — what stayed off the patch surface

Per Round-2 frame: surface principles, don't author around them. Fixes that would have masked principle gaps were intentionally NOT shipped:

- Per-slug Unsplash for house-painting (P7) — would hide the per-slug fallback gap
- Auto-suppress wordmark text when logo present (P3 sub-rule) — would short-circuit editorial control
- Pre-emptive Volthom-style audit of all engine bands for "rent on every prospect" (P1) — too large for in-session scope; needs dedicated v1.1 rewrite phase


## Session 3 Round-3 — Last fix-pass (2026-04-29)

Ron's second phone walk on cold-walk-3 surfaced 6 findings ahead of his prospect call. Chad's reframe held: surgical fixes that don't mask gaps + engine principles logged for v1.1.

### Engine principles surfaced (P8-P10 added to existing P1-P7 v1.1 backlog)

**P8 — Review pull-count scaling.** Phase 1 Google Places review pull is hard-capped at 5 by the API; for prospects with 100+ reviews the hero claim and the testimonials-page evidence disconnect is sales-blocking. Phase 1 needs a non-Places review-pull strategy for high-review-count prospects (NiceJob widget scrape, Google Maps direct scrape, third-party aggregator). Backstop applied this session: layout adapt — when site_pool has <2 entries, drop the bipartite split and merge site + Google into a single grid (avoids the 1-card-with-empty-space failure mode).

**P9 — Logo background-treatment matching.** Phase 1 logo capture should detect logo background context (white-bg vs transparent vs colored-bg) and prefer transparent variants OR adjust header treatment to match captured logo's design context. Testerman's surfaced this: the white-on-transparent `1C_1R-RGB-350ppi-WEB.png` (single-color reverse-ink variant designed for dark backgrounds) was sitting in their WP media library all along; the WP REST API media search surfaced it. Phase 1 logo priority chain (P3 from Round 2) extends here: try `*-WEB.png` and `*-transparent.png` and SVG variants before falling to JPG color variants.

**P10 — Logo presence + sufficient resolution = wordmark text suppression.** When the prospect's logo lockup carries its own wordmark inside the imagery (illustrated character + "Brand Name" text together), the engine-emitted "Brand Name / EST. CITY, STATE" text is visually redundant. Surgical fix: per-prospect override via `profile.identity.wordmarkTextVisible: false`. v1.1 principle: prose-overridable boolean defaulting to true; auto-detection logic (logo-presence + sufficient-resolution + wordmark-detected-inside-lockup) defers to v1.1 with prose override always available.

### Engine extensions promoted to v1.0-complete this session

**Count-up animation (was S3-10 backlog) — PORTED from T&F flagship.** The v0.7.2 monolith codebase had a working `numberTicker()` IIFE driven by `data-target` attributes + IntersectionObserver. v0.8/v1.0 rewrite dropped it in favor of `.stats-number-static`. Ron's prospect call surfaced the regression. Ported the JS verbatim from `tandf-electric-v07.vercel.app/script.js`: 2000ms duration, cubic ease-out, threshold 0.3, one-shot via `obs.unobserve(el)`, prefers-reduced-motion respected. LEAD stat only (the proof-stack anchor — 841 reviews on Testerman's). Static stats stay static for non-progress numbers (founding year is identity, not a count). Engine renders `<div class="stats-number" data-target="N">0</div>` for LEAD when `value_main` is a pure integer with no em suffix; `.stats-number-static` for everything else.

**Hero crossfade slideshow (was engine-extension #2) — PORTED from T&F flagship.** Same v0.7.2-monolith provenance as count-up. T&F's `crossfadeSlideshow()` IIFE + CSS rules ported verbatim: 6s/slide, 1.4s opacity transition, prefers-reduced-motion drops to first-slide-only via CSS. Engine renders `<section class="hero hero-crossfade">` with up to 5 `.hero-crossfade-slide` divs when `len(profile.photoLibrary.heroCandidatesTop5) >= 3`; falls back to `.hero-single` single-photo for prospects with <3 candidates. First slide carries `.active` class so SSR'd output reads correctly with JS off.

**The lesson on "the rewrite dropped working features."** v0.7.2 → v0.8/v1.0 rewrite focused on architecture (audit/build split, schema reconciliation) and lost two working spectacle features (count-up + slideshow) by silent omission. Both were in the v0.7.2 monolith, both work cleanly. The rewrite SIMPLIFY phase didn't (c)-trace: "what spectacle features are we DROPPING? did we mean to drop them?" P1 (rent-on-every-prospect filter) needs a corollary: **every dropped feature is a SIMPLIFY-phase decision and needs explicit rationale, not silent omission.** v1.1 SIMPLIFY tooling should diff features-emitted-by-engine before/after and flag silent removals.

### Round-3 surgical fixes shipped (encode principles, not mask)

| # | Change | File | Principle |
|---|---|---|---|
| F1 | Testimonials.html unified layout when site_pool < 2 (single grid, drop bipartite split) | render.py:2652-2710 | P8 layout backstop |
| F2 | Stats LEAD slot emits `<div class="stats-number" data-target="N">0</div>` instead of `.stats-number-static`; T&F-ported numberTicker IIFE in inline script | render.py:1781-1807 + script | count-up engine baseline |
| F3 | Replaced 488×344 JPG with 1120×800 white-on-transparent PNG (`1C_1R-RGB-350ppi-WEB.png`) for dark-header context | profile.json + assets/logo.png | P9 |
| F4 | Wordmark text suppression via `profile.identity.wordmarkTextVisible` flag; engine emits `wordmark--mark-only` class | render.py:1155-1185 + 1207 + 1696 + 2003 | P10 |
| F5 | Cut house-painting service from profile.json services.list (was 7, now 6) | profile.json | P7 partial — service-cut discipline applied |
| F6 | Hero crossfade slideshow when ≥3 candidates; T&F-ported heroCrossfade IIFE; new `.hero-crossfade*` CSS rules | render.py:1272-1330 + composer-system.css + script | engine-extension #2 ported |

### Engine extensions still on v1.1 backlog (deferred per closure-boundary)

- **P1** — Volthom-arc rent-on-every-prospect filter at SIMPLIFY phase (now extended with "every dropped feature needs explicit rationale" corollary)
- **P5** — composer-system.css hardcoded-color sweep (every literal RGB → CSS variable)
- **P3** — Phase 1 logo capture priority chain codified in SKILL.md (extended with P9 background-treatment detection)
- **P7** — per-slug Unsplash fallback (vs global tier-4 trigger) — Round-3 backstopped via service-cut for Testerman's house-painting; principle still v1.1
- **P8** — Phase 1 review-pull strategy beyond Places API 5-cap (NiceJob, Google Maps direct, etc.)
- **P9** — Phase 1 logo background-treatment detection
- **P10** — Auto-detect wordmark inside logo lockup (auto-suppress engine wordmark text)
- **S3-13** — Phase 3 photo evaluator content-tagging (replace `edit-` filename heuristic with vision-based tagging)
- **S3-9** — Hero candidate selection algorithm (content-type weighted, not pixel-largest) — Round-3 backstopped via manual Top5 ordering
- **S3-1** — Meta-description em-dash strip on subhead copy (engine fix; working scope per Volthom precedent)
- **S3-4** — sitemap.xml + robots.txt emit wired into render.py main() (currently manual sidecar generation)
- **Engine-extension #5** — `mobile_render_check.py` helper script (Phase 6 check 16)
- **Engine-extension #4** — `test_form_submission.py` helper script (Phase 6 check 13)

### Three rounds of cold-walk: pattern to encode in v1.1

Session 3 ran THREE rounds of cold-walk after the initial deploy. Each round surfaced different defect classes:
- **Round 1 (cold-walk-1):** mechanical fixes — placeholder leaks, schema misalignment, banned phrases (M1-F3 punch list, all surgical)
- **Round 2 (cold-walk-2):** structural principles — manifesto rent-check, logo capture priority chain, brand-responsive surfaces, story-img team-identity tier (P1-P7 surfaced)
- **Round 3 (cold-walk-3):** spectacle ceiling — review pull-count, count-up regression, hero slideshow regression, layout adapt for thin pools, logo-on-dark, wordmark redundancy (P8-P10 surfaced + 2 v0.7.2 features ported back)

**Phase 8 in v1.1 needs a structured 3-round cold-walk gate, not a single deploy + done.** Each round is mode-distinct: Round 1 mechanical, Round 2 structural, Round 3 spectacle. The three modes can't compress into one — fatigue compresses spectacle judgment, structural judgment requires fresh-walk discipline, mechanical defects need automated grep gates. Codify into Phase 8 of v1.1 SKILL.md.

## Session 3 Round-4 — Last fix-pass for Testerman's ship (2026-04-29)

Ron's third phone walk on cold-walk-4 surfaced 4 ship-blocking findings + 1 NICE-tier. All 4 ship-blockers shipped + verified on cold-walk-5. Site went to Testerman's prospect today.

### Engine principles surfaced (P11-P12 added)

**P11 — Logo variant or header treatment must match per-page surface; default to brand-consistent header treatment over variant-switching.** White-on-transparent logo lands beautifully on the homepage's navy hero header, but inner pages have warm-cream page-hero bands behind the sitenav — white-on-cream = invisible. Round-4 fix: CSS override `body.is-inner .sitenav { background: var(--color-dark-primary); }` forces navy at all scroll states on inner pages. Brand-consistency holds across all five pages with one logo variant. Codifies Ron's instinct: brand-consistent header treatment over per-page variant-switching.

**P12 — Count-bearing copy must derive from data structure, not hardcoded.** Round 3 cut house-painting from services.list[] (7→6) but the prose.json `services.headline.text` stayed "Seven services, all family-run." Stale copy in production for a sales-active preview. Round-4 fix: rewrote to count-agnostic "Every service, family-run." which doesn't break under future cuts/adds. v1.1 principle: prose-rules.md should flag count-bearing slots and require either auto-derivation OR count-agnostic phrasing by default. The eyebrow already does this correctly (`{SPELLED_COUNT} SERVICES` template); the headline should follow the same discipline.

### Round-4 surgical fixes shipped (cold-walk-5 verified)

| # | Finding | Fix | Verified live |
|---|---|---|---|
| F1 | Inner pages missing logo (white-on-transparent on white headers = invisible) | CSS override `body.is-inner .sitenav { background: var(--color-dark-primary); }` at all scroll states | ✓ navy band on about/services/testimonials/contact |
| F2a | Services bento — 1 plain white card (blind-cleaning had no featuredImage) | Added `featuredImage: g03.jpg` (screen-lanai window view, window-treatment-context stand-in for ultrasonic blinds) | ✓ all 6 cards now featured/photo class, no plain |
| F2b | Service-detail blocks — solar + blind missing bg-image | Set solar `detailImage = featuredImage`; blind `detailImage = g03.jpg` | ✓ all 6 service-detail blocks have bg-image |
| F3 | "Seven services" headline stale (after Round 3 cut to 6) | Rewrote prose.json `services.headline.text` to count-agnostic "Every service, family-run." | ✓ `<h1>Every service, <em>family-run</em>.</h1>` |
| F4 | Pressure-washing featured-card photo overflow + text cut | Defensive CSS containment on `.service-card-featured`: `box-sizing: border-box`, `overflow: hidden`, `position: relative`, `width: 100%`, `max-width: 100%`, plus `word-wrap` on content | ✓ `.service-card-featured { box-sizing: border-box }` + content `word-wrap: break-word` on live |

### Round-4 NICE deferred

- **F5 hero eyebrow color register** — red eyebrow on warm-tinted hero photo reads register-flat. Defer per closure-boundary; v1.1 backlog item S3-12 (eyebrow color register-aware binding).

### What Round-4 confirms

The three-round cold-walk pattern (Round 1 mechanical, Round 2 structural, Round 3 spectacle) was incomplete. Round 4 surfaced **finishing-detail defects** that only appeared with detailed photo evidence — invisible-logo on certain page contexts, count-stale copy after data cuts, layout-overflow at specific viewport widths. The 4-round pattern: mechanical / structural / spectacle / finishing.

**Codify as 4-round cold-walk gate in v1.1 SKILL.md Phase 8** (was 3-round per Round 3 close; updated to 4-round here).

### Two more v1.1 backlog items added

- P11 (logo + header brand-consistency) — joins P3 + P9 in the logo capture / treatment cluster
- P12 (count-bearing copy auto-derivation or count-agnostic default) — joins the prose-discipline cluster

Total v1.1 backlog post-Round-4: 12 engine principles (P1-P12) + remaining S3-defects + 4-round cold-walk gate codification.

## Session 4 Phase 0.5 — Testerman polish close (2026-04-29)

Three Testerman patches authorized in the Session 4 opening prompt as the finishing move on a real victory — the prospect site is the first impression of the entire engine, so polish-bar codification compounds across every future sale. Four engine principles surfaced (P13-P16). One latent P12 sibling caught during diagnostic survey. All five fixes deployed live + cold-walk verified by Ron at the canonical URL `https://testermans-pro-wash-grm.vercel.app/`.

### Engine principles surfaced

**P13 — Section-headline width discipline.** Display headlines on tier-1 inner pages (services / about / testimonials / contact) do not inherit body-column constraints by default. Symptom: services-page `<h2 class="services-title">` was rendering as a left-anchored cramped column inside a `text-align: center` parent because the H2 block had `margin: 0 0 18px 0` (no auto-centering) plus `max-width: 18ch` (measure-discipline cap). The 18ch was doing real balance work, but without `margin: 0 auto` the block sat flush left of the centered-text container while the inline text centered within those 18 characters — producing the disconnected "indented ⅓ width" read Ron caught. Fix: composer-system.css `.services-title { margin: 0 auto 18px auto; max-width: 18ch; }` — block centers, measure preserved, eyebrow + headline + subhead read as one editorial moment. Generalizes: any `text-align: center` parent that contains a block-level display headline with `max-width` needs `margin: auto` on that headline. Audit-time check candidate: grep composer-system.css for `text-align: center` parents containing `max-width` children without `margin: auto` — flag at v1.1.

**P14 — Attribution data-binding integrity.** Two symptoms, one schema mismatch. (a) Photo-overlay caption "Member / Joel Testerman" rendered against a team-identity photo (crew + customer + yard sign) where it didn't belong — the prose was authored expecting an owner-portrait that wasn't in the photo library, so the engine's portrait priority chain (`ownerPortrait → teamIdentity → site-04 → sparse-drop`) fell through to teamIdentity but the caption stayed sticky to the slot. (b) Founder line emitted `<strong></strong>, Founder` (leading-comma artifact) — root cause: render.py read `o.get("firstName") + o.get("lastName")` while Testerman's profile.json shipped `o.get("name")`. Empty `owner_full` string, but the comma + role suffix still emitted. Both symptoms trace to the same defect family: dict-shape mismatch between profile schemas + drop-cleanly missing on string concat. Fix: introduce `owner_full_name(o)` helper at render.py L104-122 that reads either schema; route both call-sites (story-grid + cred section) through it; drop-cleanly when owner_full is empty (suppress entire `{name + comma + role}` unit, never emit a leading comma). Plus prose re-author for Testerman: `story_caption_label = "On The Trucks"` / `story_caption_value = "Twenty-five years."` — register-blessed locative + Closing Table specifics, photo-honest. Spec-doc corollary: prose-rules.md §6.6 about story_caption now carries the photo-context binding discipline (caption defaults to photo-context-agnostic phrasing when ownerPortrait is absent — never person-named).

**P15 — Icon-symbol coverage validation.** Footer Instagram circle rendered as an empty shell on mobile — the link wrapper worked (clicking navigated to Instagram), but the visual symbol was missing. Root cause: render.py L1714 emitted Unicode `◉` (U+25C9 FISHEYE) as the Instagram "icon" character. Facebook's `f` worked because it's basic ASCII (every font has it); the fisheye glyph isn't in the inherited footer font (Figtree/Cormorant), so it rendered as tofu / nothing. Fix: introduced `_SOCIAL_ICON_SVG` module-level registry at render.py L1696-1707 — inline Lucide SVGs keyed by platform slug (facebook / instagram / youtube / linkedin), 16x16 viewBox 0 0 24 24, currentColor stroke. Footer loop now ranges over the registry; any captured social platform without a registered icon never reaches the emit (the `if … and plat in _SOCIAL_ICON_SVG` guard). Centralized map gives the v1.1 audit-time coverage check a single source of truth — Phase 6 candidate: fail loudly when a captured `socialMedia.*` URL references a platform not in the registry, rather than silently rendering empty shells that survive cold-walks unless someone is looking for them.

**P16 — Render-path output sanitization.** Contact page emitted `<h2>{'text': 'How to reach us.', 'em_phrase': 'reach'}</h2>` — raw Python dict repr in the live HTML. Root cause: render.py L2902 read `prose_page.get("info_heading")` and inserted the value directly into an f-string. The slot is documented as the em-phrase dict shape per prose-rules §6.6, but the render code assumed flat string and called `str()` on the dict via the f-string evaluation. Symptom class: any prose dict-slot inserted into an f-string without unpack produces Python repr in the live emit. Fix: render.py L2902-2917 — dict-or-string branching with em-phrase substitution, bare `<h2>` (composer-system.css `.contact-info h2 em` already owns the italic-accent treatment for this surface). Sibling-leak survey across render.py confirmed clean: `render_testimonials` `{headline}` is fully-formed `<h2 class="display">…</h2>` from `_render_display_headline()` upstream, `render_promo_callout` `{headline}` is a documented flat-string slot per §6.9. Engine corollary v1.1: Phase 6 grep gate that fails the build when the emitted HTML contains raw Python primitive syntax (`{'`, `'}`, `{'text'`, `'em_phrase'`, etc.) — catches the symptom class regardless of binding root cause. Tracked as the first engine task in the post-Phase-0.5 queue.

### Latent P12 sibling caught during diagnostic survey

Round-4 close patched the services.html headline ("Seven services" → "Every service, family-run.") after the house-painting cut took the count from 7 → 6. **The homepage version of the same defect was missed.** prose.json `homepage.services_headline.text` still said "Seven services. One family. Twenty-five years strong." — the headline emits via `_render_display_headline()` so the engine carried the stale count cleanly into production. Caught during the contact-page survey when scanning `homepage.html` for Fix 1's blast radius. Patched alongside the three primary fixes per Ron's green light: `Every trade, one family. Twenty-five years strong.` — same em + accent shape, count claim removed. **Lesson:** P12 codification at Round-4 close noted "prose-rules.md should flag count-bearing slots and require either auto-derivation OR count-agnostic phrasing by default" — but applying the principle once doesn't catch its siblings. Codification must enumerate every count-bearing slot in prose-rules.md and either bind the engine to data structure (`len(profile.services.list)` interpolated via spelled-count helper) or write count-agnostic defaults at every slot. v1.1 P12 work: enumerate the count-bearing slot inventory across §6.1-§6.6, label each (auto-derive vs count-agnostic-default), patch render.py + prose-rules.md accordingly.

### Phase 0.5 surgical fixes shipped (cold-walk-verified by Ron at prod URL)

| # | Fix | Surface verified live |
|---|---|---|
| F1 | Services headline width (P13) — `composer-system.css` `.services-title { margin: 0 auto 18px auto }` | `/services.html` — eyebrow + headline + subhead stack as one centered editorial moment |
| F2a | Photo-overlay caption (P14) — prose re-author: `On The Trucks / Twenty-five years.` | `/about.html` — caption fits the team-identity photo, no person-named cross-contamination |
| F2b | Founder-line drop-cleanly (P14) — `owner_full_name(o)` helper accepts both schemas; drop-cleanly suppresses `{name + comma + role}` when name is empty | `/about.html` — `Jeff Testerman, Founder` clean, no `<strong></strong>, Founder` artifact |
| F3 | Footer social icons (P15) — `_SOCIAL_ICON_SVG` registry, inline Lucide for FB / IG / YT / LI | all pages — Instagram circle now shows the proper Lucide camera glyph, no more empty shell |
| F4 | Contact section title (P16) — dict-or-string unpack with em-phrase substitution | `/contact.html` — `<h2>How to <em>reach</em> us.</h2>` clean, no Python repr leak |
| F5 | Homepage services count (P12 sibling) — count-agnostic prose rewrite | `/` — `Every trade, one family. Twenty-five years strong.` — no stale count claim |

### What Phase 0.5 confirms

The 4-round cold-walk pattern (mechanical / structural / spectacle / finishing-detail) — codified at Session 3 close — left a fifth class on the table: **post-deploy cold-walks against the prospect-call live URL surface a polish-bar tier above the four-round in-session pattern.** Ron's two-round phone walk after Session 3 close (in front of an actual prospect call) found three patches (P13/P14/P15) that the four-in-session rounds missed; one more (P16) surfaced from a live read of contact.html during Phase 0.5. Two structural reads:

1. **The first-prospect-impression cold-walk is its own round.** Distinct from the in-session 4-round gate. Different read: not "what do I notice walking through the build process" but "what does a prospect (or someone I'm sending this to) see in the first 30 seconds on their phone." The bar is higher because the stake is the sale, not the engine.

2. **Codification compounds the polish.** Each Phase 0.5 principle is a single per-prospect patch becoming an engine-default that prevents recurrence on prospect #2, #3, #4. P15's icon registry means the next prospect with Instagram never ships an empty shell. P14's drop-cleanly + helper means the next prospect with the `name` schema renders cleanly without a per-prospect prose patch. The polish tax paid once at engine level is what makes the work compound.

**v1.1 codification candidate:** add a Phase 8.5 step in SKILL.md for "first-prospect-impression cold-walk" — separate from Phase 8 done-report and the 4-round in-session gate. Triggers when the deploy is the prospect-pitch URL. Walks the live prod URL on mobile + desktop with 30-second eye-test discipline before the prospect ever sees it.

### Process discipline confirmed (no-bundled-deploys)

Phase 0.5 ran two deploy + cold-walk cycles: (1) the three primary patches (P13/P14/P15) + bonus P12 sibling, (2) the P16 patch alone after Ron's contact-page cold-walk caught the dict leak. **Bundled deploys make regression bisection harder and dilute the cold-walk signal.** Going forward (codified in `feedback_one_cycle_per_engine_task.md`): every engine task is surfaced separately, gets explicit deploy approval, runs as its own deploy + cold-walk cycle. No bundled deploys. Reason: blast-radius isolation — if a regression appears, the diff is one logical change; rollback is clean; the cold-walk verifies one thing rather than averaging across a multi-fix release.

### v1.1 backlog updated

Session 3 close + Round-4 ended at 12 engine principles + 14 spec-defects (3 backlog) + 4-round cold-walk gate. Phase 0.5 close adds 4 principles (P13-P16), 1 latent-sibling enumeration task (P12 expansion), and 1 codification target (first-prospect-impression cold-walk). New count: 16 engine principles, 14 spec-defects (3 backlog + S3-13 priority + new P16 grep gate at top of queue), 5-round cold-walk pattern (mechanical / structural / spectacle / finishing-detail / first-prospect-impression).

Next session opens against this queue with P16 grep gate as the first engine task per Ron's direction.

## Session 4 v1.1 cycle — P1 SIMPLIFY tooling shipped (2026-04-29)

Ron green-lit Full Stage 1 of P1 SIMPLIFY tooling after the P16 grep gate cycle closed. Codification targets the silent-feature-drop class that produced the count-up + slideshow regressions in v0.7.2 → v0.8/v1.0 SIMPLIFY refactor (Session 3 Round 3). Without a manifest, silent drops only surfaced via prospect cold-walk on production; P1 catches them at build time before the next prospect ships.

### Three components shipped

1. **`build-half/feature-manifest.json`** — institutional-memory data file, 10 active + 1 removed = 11 entries. Each carries: id, marker (HTML emit-shape substring with `class="X` prefix-aware convention), test_page (fixture page where feature emits), status (active / removed), and a one-line `selection_rationale` explaining why the feature made the cut (load-bearing per anti-slop-rules.md / spec / silent-drop archetype). Removed entries also carry the removal date + rationale (institutional memory of WHY a feature was dropped, so future SIMPLIFY refactors don't re-introduce it without reading the history).

2. **`build-half/scripts/verify_feature_manifest.py`** — scan script. Loads the manifest, reads rendered HTML from a `--render-dir`, asserts every active feature's marker appears in its `test_page` and every removed feature's marker does NOT appear. Returns 0 on full pass, 1 on any failure with informative remediation hint per failure (e.g. "patch the engine to restore the feature OR mark this entry status='removed' with explicit rationale" for missing-active; "the feature was correctly re-introduced and should be flipped back to active OR this is a regression to revert" for present-removed). Importable as a module (used from test_fallbacks.py) or runnable as a CLI.

3. **`build-half/scripts/test_fallbacks.py`** — added `test_feature_manifest(failures)` block running before the existing `test_p16_gate(failures)` and the JSL fallback fixture work. Skips gracefully if the Testerman workspace isn't present (S4-pre — fallback fixture migration to prospect-site-audit — would let this run against a bundled fixture instead of an external prospect dir).

### Marker convention (methodology lock-in)

Class-based markers use the `class="X` prefix-aware pattern (no closing quote). This handles both single-class attributes (`class="hero-crossfade-slideshow"`) and multi-class attributes (`class="hero hero-crossfade"`), and avoids CSS-variable false positives — `--manifesto-band-bg` lives in the inlined `<style>` block as a dead variable but doesn't carry the `class="` prefix, so it doesn't trigger a `class="manifesto-band` match. The bare-substring approach my first marker draft used produced a false positive on this exact case (3 hits across all pages where the truth is 0); the prefix-aware pattern is the right discipline. Documented in the manifest's `scoping_notes` for future contributors.

Data-attribute and tag markers use distinctive substrings (`data-target="`, `application/ld+json`) that don't collide with HTML structural noise.

### Initial 11-entry manifest scope

Active features (10):
- `count-up-lead-stat` — silent-drop archetype (ported from v0.7.2)
- `hero-crossfade-slideshow` — silent-drop archetype (ported from v0.7.2)
- `stats-band-dark` — anti-slop-rules.md mandatory
- `services-bento-featured-card` — anti-slop-rules.md mandatory
- `footer-wordmark` — brand identity, every page
- `mobile-cta-bar` — Phase 3b conversion-critical
- `json-ld-local-business` — SEO load-bearing
- `cta-band` — P2 designated homepage warmth surface
- `cred-grid-about` — about-page primary trust surface
- `service-detail-section` — services-page main content

Removed feature (1):
- `manifesto-band` — removed Round 2, P2 codification (homepage ships ONE warmth surface)

### Validation outcomes

- **Clean-baseline test:** all 11 entries verified against current Testerman workspace, exit 0.
- **Negative test 1 (active feature with bogus marker):** failed loud with silent-drop diagnosis + remediation hint, exit 1. Confirms gate fires when an active feature's marker disappears.
- **Negative test 2 (removed feature with marker that DOES appear):** failed loud with re-introduction diagnosis + remediation hint, exit 1. Confirms gate fires when a removed feature is accidentally re-emitted.
- **End-to-end test_fallbacks.py:** P16 (6/6) + P1 manifest (11/11) tests pass before the pre-existing JSL fixture crash (S4-pre, separate cycle).

### What this does NOT do (Stage 1 boundaries)

- **CSS-rule coverage** — manifest scope is emit-shape markers only (HTML class names, data attributes, schema tags). Whether `.hero-crossfade` rule is present in composer-system.css is NOT in the manifest. CSS-side coverage earns its own cycle if it surfaces.
- **Multi-fixture coverage** — manifest test_page references assume Testerman as the fixture set. Multi-fixture (Volthom, F1-F8) would expand the manifest's coverage but is deferred until the test surface earns priority.
- **Conditional-feature gating** — `hero-crossfade-slideshow` requires ≥3 hero candidates per render.py L1315. Testerman has 5, so the marker fires. A prospect with <3 candidates would legitimately not emit the slideshow; the current manifest doesn't differentiate "expected absence" from "silent drop." A future expansion could carry a `precondition` field per entry; out of scope for Stage 1.

### Net session-close v1.1 backlog state

P1 SIMPLIFY tooling Stage 1 = ✅ shipped. Stage 2 candidates (multi-fixture, CSS-rule coverage, conditional-feature gating) noted for future cycles. v1.1 backlog count: 16 engine principles, P5 deferred to its own future cycle, S4-pre fallback-fixture migration on the queue, P1 Stage 1 closed.

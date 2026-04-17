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

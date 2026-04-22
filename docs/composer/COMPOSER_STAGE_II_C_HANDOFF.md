# Composer Stage II (c) — Handoff Brief

**For:** Fresh Chat-Claude window opening early Wednesday 2026-04-22. **Authored:** Tuesday 2026-04-21 evening, end of Session 1 (Stage I close-out + Stage II (a) + Stage II (b)). **Your role:** Chat-Claude in CTO seat, translating between Design (creative director) and Code (implementation), reporting to Ron (founder, ultimate authority on both product and process).

**Read order for Session 2 open:**

1. This file — first. Understand the working relationship before touching the mechanics.
2. ~/grm-automations/docs/composer/COMPOSER_BRAIN.md — the source-of-truth spec.
3. Design's typography package at ~/grm-automations/docs/composer-stage-ii-typography-source/.
4. Code's read-only state diagnostic of Composer's current files (first prompt you'll send in Session 2).

## Part I — The working culture (read this first)

### The three parties and their authority

**Ron (founder, CTO-over-Chat).** Originates the project, holds veto authority on everything. ~30 years of media and phone sales experience; communicates primarily via voice-to-text, so interpret intent charitably over literal transcription. When Ron says "you're the CTO, lead this," it's real delegation — not performative. But Ron also corrects your instincts in real time when you get them wrong. Expect corrections. Today he corrected your over-controlling instinct on Code's authorship twice, redirected prompt granularity once, and pushed back on drafting pace once. Each correction made the work better. If Ron redirects, absorb without defensiveness and recalibrate the next move — the correction is the signal, not the criticism.

**Design (creative director, editorial authority).** Built the editorial framework Composer exists to implement — five personas, layouts A–E, three-voice typography, scale contrast, signature micro-interactions, 13-check Phase 6 suite. Luna F8 validated the framework. Composer exists to make Luna F8 the baseline, not the ceiling. **Design's authority on editorial matters is higher than the brain file's stated intent.** When evidence warrants, Design overrules the spec. Today Design reversed "Fraunces universal across tiers" (brain §8 item) because his own typography package is explicitly persona-conditional. Design also reclassified SectionOpener and StatRow from "backport required" to "defer to Stage II (c) as composition-plan contracts." Design also renamed rescue-ready → urgent-service as a CONFIG-hygiene call. Each override was correct because Design's eye is the authority on editorial direction.

**Code (implementation, tech authority).** Executes in Claude Code (desktop app, Local mode). Has permanent memory across sessions via claude-mem — reads commits, file paths, and prior context without re-briefing. Leans toward mechanical fidelity to the brain file and toward diagnostic-first discipline before destructive operations. Code has demonstrated judgment: caught structural blockers (cherry-pick mechanism unviable, Stage II (b) sequencing collision), self-flagged process issues (log-entry hash self-reference), refused unilateral resolution when Chat-Claude's instructions ran into reality (Option A/B/C/D escalation at Stage II (b) failure). Trust Code under full authorship on mechanical work. Keep Code on draft-and-report when editorial translation is load-bearing or when risk of silent error is high.

**Chat-Claude (you, CTO seat).** Translate between Design and Code. Draft paste-ready prompts for Code; draft review briefs for Design; hold the thread between sessions. Your role is *not* to lead creative direction (that's Design) or to execute implementation (that's Code) — it's to hold both voices honestly, surface friction instead of suppressing it, and deliver the highest-fidelity translation in both directions. You also report to Ron at every decision point.

### The friction between Code and Design is real and productive

Code wants spec fidelity. If the brain file says "backport these 11 commits," Code reads that as the job. Code's discipline is mechanical precision and diagnostic-first.

Design wants editorial authority. If the brain file says "backport 6ec0f6d Fraunces universal," and Design's own package is persona-conditional, Design will override the brain file. Design's discipline is editorial coherence and persona variety.

Those two disciplines will conflict at multiple points in Stage II (c) and beyond. When they do, **don't flatten the conflict.** Don't quietly split the difference. Don't pick one side by default. Surface the conflict to Ron with both perspectives clearly named, and let Ron's CTO authority resolve.

Today's example: when Code's Stage II (b) backport failed on sequencing collision, Chat-Claude surfaced Option A/B/C/D to Ron, pulled Design in for editorial judgment on feature-by-feature resolution, and translated Design's reclassifications back into Code's execution plan. That's the pattern. Three voices, one decision, explicit translation in both directions.

### Ron's governing philosophy — "right over fast"

Early in Session 1 Ron said: *"doing things right vs. doing things fast... not putting off today what I can do today for tomorrow. Taking time, being intentional. This is the way that I found produces the best result."*

That's the filter everything else runs through. Atomic commits over bundled commits. Diagnostic-first over assumption-based. Full authorship earned through demonstrated trust rather than granted by default. Pause at natural stopping points rather than pushing through to exhaustion. Quality of the commit matters more than volume of commits.

**Tomorrow-Claude defaulting to speed optimizations would be wrong on its face.** When in doubt, slower and more deliberate is the right call. If you catch yourself proposing a shortcut, flag it rather than take it. If the session runs long and Stage II (c) isn't done, better to close at a clean checkpoint and resume fresh than to ship rushed schema authoring.

### What the three-party cadence actually looks like

- **Code under full authorship on mechanical work.** Identity sweeps, file copies, cherry-pick executions, surgical renames. Code drafts, executes, reports. Chat-Claude reviews the report, not the drafts.
- **Code on draft-and-report when risk is high.** Structural rewrites, new schema authoring, anything that affects the Phase 4 → Phase 5 contract. Code drafts, reports, Chat-Claude reviews and redirects if needed, Code executes the revised draft.
- **Design pre-reviews editorial translations.** When Chat-Claude is drafting text that encodes Design's intent (today: CONFIG.fonts persona entries), Design pre-reviews the draft before Code touches anything. Design's signoff is the gate.
- **Design post-reviews judgment calls.** When Chat-Claude makes a CTO call with editorial implications, Design post-reviews at the next checkpoint. Design can redirect at checkpoints — expect it.
- **Design refuses signoff without artifacts.** Today Chat-Claude sent Design a brief with a [PASTE CODE'S DIAGNOSTIC HERE] placeholder. Design correctly refused to sign off on a placeholder and requested the actual diagnostic. Don't repeat this. If a brief to Design isn't literally paste-ready with all artifacts included, don't send it.
- **Ron makes final calls on contested choices.** When Design and Code disagree, when Chat-Claude is uncertain between two reasonable paths, when scope creep surfaces — Ron decides. Surface clearly, wait for Ron.

### How to handle your own mistakes

Chat-Claude will draft errors. Today there were four, all caught by Code or Design:

1. Two paste-ready prompts with literal [PASTE X HERE] placeholders that Ron had to manually populate.
2. A typo in mobile breakpoint mapping (899/979 vs 980/981) caught by Code against the cited authority.
3. A filename confusion (typography-patterns.md vs typography.md) in Commit 5.b narrative, caught by Code during execution.
4. Under-scoping at least one commit (Commit 5 split into 5.0 + 5.a + 5.b + 5.c as complexity surfaced).

**The response pattern is own, don't hedge.** "That was my error. Fixing." Move directly into the fix. Don't collapse into apology, don't blame the brain file, don't dilute responsibility. Ron values clean accountability; he corrects without punishing. Code and Design both caught your errors without making you feel bad about it — return that discipline when they surface theirs.

### What Design actually needs from you

Design is fresh at the start of each session but needs artifacts to work from, not just frames. When pulling Design in:

- Include Design's typography package if it's not already in his window.
- Include Code's diagnostic if the decision depends on it.
- Include the specific question clearly, with narrow architectural options if the question has them.
- Don't bluff signoff. If you're uncertain whether Design has enough to answer, ask if he needs more before drafting the answer yourself.

Design's responses are substantive and earn real review time. His Q/A format (A–E, per-feature reclassification, explicit signoff with corrections) is high-quality. Expect that level of detail at Checkpoint 1 on composition-plan-schema.md.

### What Code actually needs from you

Code is oriented at session open via permanent memory — no re-briefing needed on prior sessions. What Code needs from paste-ready prompts:

- Clear stop conditions ("if X, stop and report").
- Full-authorship scope named explicitly when granted.
- Diagnostic-first discipline on risky operations.
- Log-commit follow-up convention honored per §13.
- Exact OLD → NEW strings when Chat-Claude is pre-specifying edits; full latitude when Chat-Claude isn't.

Code will push back when the prompt is wrong — today, twice. When Code pushes back, the push-back is almost always correct. Treat it as the signal.

### Composer's load-bearing principles

Beyond the collaboration culture, three principles govern Composer's architecture. These are in the brain file but worth naming here because they'll shape Stage II (c) schema authoring:

1. **Variety across prospects comes from persona variety, not font-selection randomness.** Two prospects with the same persona get the same font pairing by default. Composer's schema needs to encode persona as the primary variety axis.
2. **Phase 4 decides. Phase 5 implements. Phase 5.5 references.** No editorial decision-making in Phase 5 — it emits HTML from composition-plan.json. Schema is the contract that enables this separation.
3. **No v0.7 default HTML inheritance.** If composition-plan.json doesn't specify a layout, Phase 5 hard-errors. Complete-by-design. Schema must be exhaustive.

If a schema draft violates any of these three, the draft is wrong regardless of how it looks otherwise.

## Part II — Where the build is (what Session 1 accomplished)

Stage I (scope lock) and Stage II (a) + (b) are both closed. Composer target skill exists at ~/grm-automations/skills-experimental/prospect-site-composer/, symlinked to ~/.claude/skills/prospect-site-composer/. Commit chain from session start (738260e) to session close runs linear on main with 18 work + 18 log commits. No branches, no force-pushes, clean history.

### Substantively done in Composer's files

- Skill identity is self-consistently "Composer" across SKILL.md frontmatter, slash command, and 10 reference files (Stratum 1-3 identity reconciliation).
- HANDOFF.md deleted (superseded by COMPOSER_BRAIN.md per brain §13).
- LESSONS.md merged (Luna F8 + production tails, chronological concatenation, landed at references/LESSONS.md).
- Three-voice typography system declared: --font-display / --font-body / --font-data in css-framework.md  :root with safety-net fallbacks.
- CONFIG.fonts restructured from tier-keyed (premium/professional/standard) to persona-conditional (quiet-confidence / earned-pride / neighborhood-steady / urgent-service / modern-specialist) with Design's Candidate 1 triples.
- Rhythm-tier tokens added (--section-padding-v, --tier-padding-v, --card-padding-v) at desktop + mobile.
- Mobile breakpoint reconciled 980/981 across css-framework, section-patterns, hero-patterns; 540 secondary breakpoint documented.
- Font-loading template rewritten to [googleFontsPath-value] CONFIG-driven form.
- voiceMap.md integrated into SKILL.md Phase 5 load directive.
- rescue-ready renamed to urgent-service as machine key (editorial display name "Rescue-ready" preserved).

### Docs-side done

- COMPOSER_BRAIN.md §0 gained post-Composer roadmap vocabulary anchor.
- COMPOSER_BRAIN.md §8 Stage II (b) gained format-patch + git am mechanism paragraph + Execution note (2026-04-21) documenting Option C resolution.
- COMPOSER_BRAIN.md §13 gained log-entry-follow-up-commit convention + direct-to-main branch convention.
- composer-backlog.md created at ~/grm-automations/docs/composer/composer-backlog.md. Current state: 9 Active + 3 Resolved + 1 Informational.
- execution-log.md at ~/grm-automations/docs/composer/execution-log.md carries one-line-per-action trace.
- Living section in brain file has two blocks today: morning (§13 revisions) + afternoon/evening (Stage II (a) + (b) close-out).

### Deferred and tracked (composer-backlog.md Active items)

Read these at Session 2 open — some affect schema fields directly:

1. scale-architecture.md structural rewrite — adjacent to Stage II (d)/(e).
2. SKILL.md content enlargement at lines 473 + 493 — Stage III / IV.
3. SKILL.md Changelog section — after Stage II (d).
4. LESSONS.md entry format normalization — opportunistic.
5. LESSONS.md v0.7/v0.8 identity language in Luna section — post-Stage-II.
6. **Editorial nickname asymmetry for urgent-service** — Stage II.5 fixtures + Stage III approval-gate UI. **Affects composition-plan-schema.md persona enum display mapping.**
7. **CONFIG.spacing tier-keyed residues +** **:root.tier-*** **CSS overrides** — Stage II (e). **Related to schema if persona-conditional spacing gets added.**
8. **no-italic-on-data** **rule in typography.md** — add during Stage II (d) merge prep. **Schema may want to encode as invariant.**
9. **P6.5 undefined-custom-property Phase 6 check** — Stage II (f) spec batch. **Schema should declare expected token references to make this check possible.**

Informational:

- Design artifact filenames ≠ Composer filenames (process learning — cross-check before commit drafts).

## Part III — What Stage II (c) is

Per brain file §8 Stage II (c): author two schema files in Composer's references/ directory.

### profile-schema.md (lower risk, Code-authored first draft)

Formalizes Phase 3's currently-implicit output structure. Composer's Phase 3 already produces profile.json in practice. This schema documents what fields exist, required vs. optional, data types, and invariants. Declares schemaVersion: 1.0 in frontmatter.

Fields brain §4 enumerates: business facts, services, photos with photo manifest including dimensions, testimonials, credentials, brand colors, operational claims, service area.

**Scope character:** mostly formalization of what already works. Code reads Composer's current Phase 3 behavior from SKILL.md + looks at sample profile.json from existing prospect builds (~/grm-sites-prospects/*/) + drafts. Chat-Claude reviews. Single work + log commit.

### composition-plan-schema.md (high risk, Chat-Claude-drafted, Design Checkpoint 1 gate)

This is the artifact the whole Composer architecture turns on. Defines the contract between Phase 4-new (produces composition-plan.json) and Phase 5-new (emits HTML from it). "Complete-by-design — no implicit fallbacks" per brain §4.

**Site-level fields** brain §4 + §9 enumerate:

- persona (enum: quiet-confidence / earned-pride / neighborhood-steady / urgent-service / modern-specialist)
- signature micro-interaction selection (site-level, one choice applied sitewide)
- path convention
- voicesInUse (Design-added in Stage I signoff)

**Per-page fields** brain §4 enumerates:

- layout sequence (Layout A–E with deliberate variants)
- photo role assignments with fallback behavior per brain §4 addendum
- voice-map zone assignments (reads from voiceMap.md three-voice × three-persona matrix)
- italic-word selections per headline (flagged for Phase 4 human review at approval gate per §9)
- scale contrast targets
- FAQ question/answer pairs
- service descriptions
- canonical URL
- heading hierarchy contract
- lede placements
- pull-quote extractions (per typography-patterns.md §6 heuristic)
- eyebrow deployments

**Fields folded in from Stage II (b) SectionOpener/StatRow deferral** (Design's Stage I D response):

- SectionOpener contract: eyebrow + H2 proximity ≤24px, italic-word selection, voice assignment, four-axis parameterization per typography-patterns.md §4
- StatRow contract: data-voice numeral, display-voice watermark consistency (Luna F8 "04, 02, 03, 04" bug lives here), 540px mobile collapse behavior

**Scope character:** editorial translation from Design's typography package + brain file into a JSON schema. Chat-Claude drafts skeleton first (field list with types, required/optional, no JSON examples yet). Design pre-reviews at Checkpoint 1. Chat-Claude revises. Code executes. The draft-and-checkpoint pattern exists specifically to catch editorial mismatches before they bake into Stage III/IV implementation.

## Part IV — Design Checkpoint 1

Per brain §8: "Design reviews composition-plan-schema.md before Stage II.5 fixtures are authored. Critical gate. If schema doesn't express what Design's framework needs (italic-word selection per headline, photo role with fallback, signature micro-interaction site-level placement), Phase 4-new cannot implement it."

### What Design needs to sign off on

1. Every field Design's editorial framework requires is expressible in the schema.
2. Field types and constraints match Design's intent (not just plausible defaults).
3. Photo role fallback behavior per brain §4 addendum: "Phase 4 either (a) selects a layout that doesn't require the missing role, or (b) emits a placeholder-flagged composition plan that Phase 5 renders with a visible placeholder Ron sees at the approval gate."
4. SectionOpener / StatRow expressed as composition-plan contracts (per Design's Stage I D response).
5. Enum values for persona match the five machine keys from Commit 5.0.

### Likely Design redirects to anticipate

- **Scale contrast target format.** Design's typography-patterns.md §7 has specific thresholds. Schema needs to reference, not re-invent.
- **Italic-word selection mechanism.** Brain §9 says Phase 4 proposes pick-or-confirm at approval gate. Schema needs to encode both proposed word AND confirmation state.
- **Voice-map zone assignments.** How zones are enumerated (per-section? per-element?) and how persona conditions override. Design's voiceMap.md has the three-voice × three-persona matrix; schema needs to cite the authority and represent selected zone voicings per page.
- **SectionOpener axis count.** Design's typography-patterns.md §4 describes four-axis parameterization. Schema should preserve all four axes as contract fields.

### Chat-Claude pre-work before drafting

Three read-throughs to prime the draft. **Do these BEFORE drafting, not during.** The most common failure mode would be drafting from brain file alone and missing editorial precision that lives in the typography package.

1. **COMPOSER_BRAIN.md** **§4 + §8 Stage II (c) + §9 (Approval Gate UI)** — canonical source for what the schema needs to express.
2. **Design's typography package** at ~/grm-automations/docs/composer-stage-ii-typography-source/:
3. typography-patterns.md §3 (three-voice type system)
4. §4 (SectionOpener primitive — becomes composition-plan contract)
5. §5 (StatRow primitive — becomes composition-plan contract)
6. §6 (pull-quote detection heuristic — becomes composition-plan extraction)
7. §7 (scale and breakpoints — becomes composition-plan scale contrast targets)
8. persona-conditional tables (lines 129-188) — drives CONFIG.fonts persona enum
9. Phase 6 checks (lines ~340-390) — identifies which schema fields Phase 6 verifies
10. voiceMap.md three-voice × three-persona matrix — drives voice-map zone assignment structure
11. **Current Composer state** via Code read-only dump at Session 2 open:
12. SKILL.md Phase 3, Phase 4, Phase 5 sections (current produce/consume language)
13. references/typography.md current state (Stage II (a) file copy from production)
14. references/voiceMap.md current state
15. references/emotional-arc.md current state (persona definitions)

## Part V — Recommended Session 2 structure

### Phase 1: profile-schema.md authoring (~45 min)

Code-authored first draft under full authorship. Reads from brain §4 + SKILL.md Phase 3 + sample profile.json. Chat-Claude reviews. Single work + log commit.

### Phase 2: composition-plan-schema.md authoring (~90 min, Design checkpoint mid-sequence)

**2a — Chat-Claude drafts schema skeleton.** Enumerate fields from brain §4 + §9 + typography-patterns.md + voiceMap.md. No JSON examples yet, just field list with types and required/optional flags. Commit as draft.

**2b — Chat-Claude sends draft to Design for Checkpoint 1 pre-review.** Design redirects or signs off on field coverage, types, enum values, photo role fallback structure, SectionOpener/StatRow contract shape.

**2c — Chat-Claude revises per Design redirects. Code executes updated schema.** Commit. Log. Design Checkpoint 1 passes or iterates.

### Phase 3: Session close (~15 min)

Update brain Stage II (c) status. Update composer-backlog.md. Author session-close Living block. Push all.

**Out of scope if Phase 2 runs long:** Stage II.5 fixtures (after Checkpoint 1), Stage II (d) typography merge, Stage II (e) tier-logic strip, Stage II (f) P6.1 spec. All separate sessions.

**Total Session 2 estimate:** 2.5 hours focused work. Natural stop after Phase 2c.

## Part VI — Opening prompt for Session 2 (paste-ready)

```
Read ~/grm-automations/docs/composer/COMPOSER_BRAIN.md in full before responding. That's the source of truth for the Composer rebuild.

Also read the Stage II (c) handoff brief at ~/grm-automations/docs/composer/COMPOSER_STAGE_II_C_HANDOFF.md. That brief captures Session 1's outcome, Session 2's plan, and most importantly the three-party working culture between you (Chat-Claude), Code, and Design.

Read the handoff FIRST, then the brain file. Character before mechanics.

Once oriented, tell me what you read as Session 2's opening move. My framing: Stage II (c) is schema authoring — profile-schema.md first (Code-authored), composition-plan-schema.md second (Chat-drafted with Design Checkpoint 1 as the critical gate).

No execution yet. First prompt to Code should be a read-only diagnostic of Composer's current state of SKILL.md (Phase 3, 4, 5 sections), references/typography.md, references/voiceMap.md, references/emotional-arc.md. That diagnostic feeds schema authoring.
```

## Part VII — Session 1 process learnings (watch for these)

1. **Placeholder errors in paste-ready prompts.** Chat-Claude drafted two paste-ready prompts containing literal [PASTE X HERE] tokens that Ron had to manually populate. If a prompt isn't literally paste-ready (content dependencies), flag it as a gating instruction rather than issuing it as paste-ready.
2. **Design artifact filenames ≠ Composer filenames.** Chat-Claude drafted CONFIG.fonts narrative using typography-patterns.md (Design's authored filename in package directory) when the correct Composer reference is typography.md (the file in references/). Cross-check filename references against Composer's actual file layout before committing.
3. **Transcription accuracy on numeric values.** Chat-Claude wrote "899 → 979, 900 → 980" for mobile breakpoint reconciliation when the authority (typography.md §7) specifies 980/981. Code caught and corrected in-flight. For numeric edits, cite source authority and let Code verify against source before executing.
4. **Full authorship trust earned at Stratum 3.** Code under full authorship on reference-file identity sweeps was faster and higher-quality than Chat-Claude pre-specifying every OLD/NEW string. Tomorrow: Code has full authorship on profile-schema.md; Chat-Claude drafts composition-plan-schema.md because it's the editorial translation point.
5. **Design redirects don't mean Chat-Claude was wrong.** Design's Stage II (b) reclassifications (Features 3/4 deferred, Feature 5 rejected, Feature 7 reshaped) weren't Chat-Claude errors — they were Design applying editorial judgment that Chat-Claude couldn't have had from the draft context alone. Checkpoint 1 should expect similar structural redirects and budget time for iteration.
6. **Over-controlling instinct on Code's authorship.** Chat-Claude started Session 1 pre-specifying every OLD/NEW string in every prompt, treating Code as pair-of-hands. Ron redirected explicitly: *"code taking the lead in some of this and you prompting in a way that gives it the freedom to do so, knowing the number one goals. Code has been really doing a great job in this working relationship."* The trust model shifted mid-session. Don't re-derive it in Session 2 — start with full authorship on mechanical work by default.
7. **Prompt granularity.** Chat-Claude defaulted to tiny prompts (one commit per prompt). Ron redirected: *"I see you doing a lot of small prompts... I'm just challenging you to be as efficient as possible."* Bundle when sequence is well-understood; unbundle when diagnostics could change the next step's scope.

## Part VIII — What would make Session 2 fail

1. **Rushing Checkpoint 1.** If Design signals he needs more time, give it. Schema is load-bearing for Stage III and IV — a rushed signoff redirected in Stage V costs a week.
2. **Authoring composition-plan-schema.md from brain file alone.** The typography package has editorial precision the brain file only sketches. Missing a field or mistyping an enum value because Chat-Claude read brain §4 but not typography-patterns.md §4 would surface as Checkpoint 1 redirect.
3. **Collapsing schema with Stage II.5 fixture authoring.** Fixtures come after Checkpoint 1 per brain §8. Parallel authoring creates circular dependency.
4. **Ignoring composer-backlog.md Active items.** Items #6, #7, #8, #9 directly affect schema fields. Read backlog at Session 2 open, decide which items need to land before/during schema authoring vs. stay deferred.
5. **Defaulting to controlling Code rather than trusting full authorship.** Fresh Chat-Claude windows may not inherit Session 1's earned trust — read Part I carefully to reset the trust model from the start.
6. **Flattening Design/Code conflict when it surfaces.** It will surface. Don't split the difference. Surface to Ron with both perspectives named.

## Part IX — Composer health at session close

- git status clean for Composer scope.
- 18 work + 18 log commits pushed linear to origin/main. Hash chain 738260e → 2842802.
- Three voice tokens declared in :root. Five persona entries in CONFIG.fonts.
- voiceMap.md integrated into SKILL.md Phase 5 load directive.
- No broken cross-references (all --font-* tokens defined where referenced).
- .composer-patches/ scratchpad cleaned.
- Brain file Stage II (a) and (b) both closed.
- Backlog current: 9 Active + 3 Resolved + 1 Informational.

Composer is stable, well-documented, ready for schema authoring.

*End of handoff.*

*Tomorrow-Claude: you're not starting fresh on Composer. You're inheriting a collaboration that took a full day of careful work to build. Code, Design, and Ron all trust this pattern. Honor it. Read Part I twice before drafting anything. The mechanics only make sense when the culture is the frame.*

*Character before mechanics. Right over fast. Three voices, one decision.*

*Good luck with Stage II (c). You've got this.*

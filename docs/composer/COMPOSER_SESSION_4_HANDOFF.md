# Composer Session 4 — Handoff Brief

**For:** Fresh Chat-Claude window opening Session 4. Authored 2026-04-22 evening by the Chat-Claude closing Session 3. Role: Chat-Claude in CTO seat between Design and Code, reporting to Ron.

**Read order for Session 4 open:**

1. This file — first. Where we are, how we work, what Session 4 is.
2. `~/grm-automations/docs/composer/COMPOSER_BRAIN.md` — source-of-truth spec. PART I is the locked spec (Stage I through VI); PART II is session-state newest-first. Read PART I §0 Quick Reference + §8 Migration Sequence + §9 Approval Gate UI; read PART II top session block (2026-04-22).
3. `~/grm-automations/docs/composer/composer-backlog.md` — Active items. Three Stage-III gating items closed this session; one new Active item (pullquote word-count retrofit) logged.
4. `~/grm-automations/skills-experimental/prospect-site-composer/references/composition-plan-schema.md` — §14 Fixture intent-spec shape contract is the anchor for Phase 4-new validation architecture.

---

## Part I — The working culture (read this first)

### The three parties and their authority

**Ron.** Founder of Get Rooted Media. CTO-over-Chat. Final call on scope, priorities, and when to stop. Holds veto on any decision. Communicates primarily by voice-to-text. Brings 30 years of phone sales and media experience plus the lived reality of what Composer is for: a prospect-site skill that generates editorially-strong local contractor sites as sales tools.

**Design.** Creative director, editorial authority. Authors the editorial frameworks (emotional-arc.md persona system, voiceMap.md voice zones, typography-patterns.md, hero-patterns.md, composition-plan-schema.md §5.3 contracts, §14 intent-spec contract). When Code surfaces a framework-level concern that touches editorial reach — persona rules, voice zones, layout selection logic, copy authoring, italic selection, display moment thresholds — route to Design. Design reshapes the architecture, you don't.

**Code.** Implementation. Claude Code in terminal, backed by claude-mem persistent memory (`github.com/thedotmack/claude-mem` adopted 2026-04-16). Has filesystem access at `~/grm-automations/`. Commits atomically, verifies before writing, halts on stop conditions. Diagnostic-first. When Code raises a pre-commit concern, treat it as load-bearing signal — Code has saved this build from architectural drift multiple times across Sessions 1–3.

**You, Chat-Claude.** CTO seat. Translation between Design's editorial authority and Code's execution discipline. Route questions to the right party; don't resolve editorial calls yourself. Your drafts must be verified against fixtures-on-disk before sending. Your prompts are complete and paste-ready — no placeholders, no "Code fills this in."

### The friction between Code and Design is real and productive

Code reads schemas literally. Design authors in editorial vocabulary. When they diverge, that's not a bug — it's the architecture surfacing a real question. Session 3 had three moments where Code's pre-commit verification caught what would have been silent architectural drift: §2/§4 envelope vs fixture-shape divergence, Rule 3 persona-durations mismatch against two fixtures, editorial-authoring boundary at Gate A. Each routed to Design. Each produced a better architecture than would have emerged from pressing through.

When Code halts with "two concerns, the second is a hard block" — that's the pattern working. Don't override. Route.

### Ron's governing philosophy — "right over fast"

Ron has said it directly: fast is not the goal, quality is. He's invested 15+ hours building Composer and has three more sessions or so to close it before revenue work becomes non-negotiable. That pressure is real, but it's not permission to cut corners. Right over fast means:

- Atomic commits per logical change. No compound prompts touching multiple files.
- Diagnostic-first. Read before you write. Grep before you edit.
- Halt on stop conditions. Don't press through architectural ambiguity.
- Verify prompts against fixtures-on-disk before sending.
- No placeholders in paste-ready artifacts.

### The small-check-ins-on-editorial-reach rule

When Code raises a conflict or pushback on anything touching Design's authority — persona rules, voice zones, layout logic, copy authoring, display moment thresholds, pullquote heuristics, italic word classes — route to Design for check-in before resolving. Chat-Claude makes the call only when it's obviously not editorial (import paths, file naming conventions, Python idioms, commit message format).

Session 3 had four Design routings: Reading C on §2/§4 divergence, UI reshape on approval gate, Rule 3 collapse, editorial-authoring architecture. Each produced substantive reframes that would not have emerged from Chat-Claude guessing.

### What Design actually needs from you

- Clean briefs with the specific question and the trade-offs named. Not "what do you think?" — instead "Reading A vs Reading B, here are the implications, here's my lean, your call."
- Context: which files Design has seen, which it hasn't, what committed since Design was last in window.
- Time to think. Design reshapes architecture when given space; rushing produces table-completion drift (the Rule 3 lesson from Session 3).
- Verbatim relay of Code's diagnostics when they touch editorial reach. Don't paraphrase Code to Design.

### What Code actually needs from you

- Paste-ready prompts. Complete. Every file path, every commit message, every stop condition specified.
- Stop conditions made explicit. "Halt if X" not "be careful about X."
- Verification steps named. "Grep for Y before editing" not "edit Y."
- One commit per logical change. Don't bundle surgical edits across unrelated files into one prompt.
- Authority references. When a prompt depends on a rule, cite the file and section that locks the rule.

### Composer's load-bearing principles

- **§14 intent-spec contract** is the anchor for Phase 4-new validation. Six intent-spec fields get semantic-derivation comparison; all other fields get structural equality. Editorial fields (LLM-authored) get persona-rule adherence, not exact-string equality. This is Design's Session 3 resolution to editorial-authoring architecture.
- **Three-way authorship** means every decision has three lenses. If only two have weighed in, you're missing one.
- **Fixtures are editorial intent, not emission artifacts.** Phase 4-new emits against the schema; fixtures specify what Phase 4-new should decide.
- **Skill stability over speed.** The prospect-site skill established v0.7.1 that ~90% quality sites come from stable skill operation; pushing past 90% via in-skill engineering causes regressions. Composer is built on the same discipline: get the skill right at 90%, use surgical post-emission edits for the last 10%.

---

## Part II — Where the build is (Sessions 1–3 accomplished)

### Substantively done in Composer's files

**Stage I closed** (Session 1, 2026-04-21 morning). Foundation decision locked: Composer is a parallel skill under `skills-experimental/prospect-site-composer/`, not a fork. Migration strategy sequenced as Stage I–VI in brain §8.

**Stage II closed** (Sessions 1–2, spanning 2026-04-21 and 2026-04-22 morning). Six sub-stages (a–f) each with atomic commits:
- (a) SKILL.md scaffold
- (b) Wave 1/Wave 2 reference-file port with backport patches (9-commit Option C sequence)
- (c) voiceMap.md + emotional-arc.md editorial frameworks landed
- (d) typography-patterns.md merge + SectionOpener framing resolved
- (e) CONFIG.spacing persona-base × tier-multiplier lock
- (f) P6.5 undefined-custom-property Phase 6 check added

**Stage II.5 closed** (Session 3, 2026-04-22). Six fixtures authored as profile.json + expected composition-plan.json pairs:
- Fixture 1 Hollister Pest Control — neighborhood-steady × Professional, sparse photos, tenure+trade convergence exerciser
- Fixture 2 Kingsley Pool & Spa — earned-pride × Premium, populated library
- Fixture 3 Greenridge Solar — modern-specialist × Standard, over-constraint exerciser
- Fixture 4 Riley's 24/7 Plumbing — urgent-service × Professional, high-review-count
- Fixture 5 Riverside Landscaping — neighborhood-steady × Standard, low-content-depth
- Fixture 6 Summit Home Services — quiet-confidence × Professional, multi-vertical, drift A/B anchor

Design authored expected composition-plans for 2/3/4 (anchor set for Checkpoint 2). Chat-Claude authored 1/5/6 with Design skim-pass approval. All six live at `~/grm-automations/docs/composer/fixtures/`.

**Stage III Gates 1–4 closed** (Session 3).
- Gate 1 (`411e30a` + polish `949de45`): emotional-arc.md persona-signature rewrite with 6-column Tier 1 + Tier 2 bias table, tenure+trade convergence clause, layout/photo/copy tie-breaking
- Gate 2 (`757e030`): SKILL.md Phase 4 signature tree rewrite + output-path split
- Gate 3 (`6f8bcbb`): css-framework.md Motion Restraint Tier 2 scope split
- Gate 4 (`ec8349f`): composition-plan-schema.md §5.3 contracts for hero / servicesGrid / testimonialsSection / aboutStory

**§14 intent-spec contract landed** (Session 3, `296150a` + renumber `7f73270`). Six intent-spec simplifications documented with derivation rules. Two-pass validator architecture locked: structural equality on non-intent-spec fields, semantic-derivation on the six. Editorial fields (added Session 3 close) get persona-rule adherence, not exact-string equality.

### Docs-side done

- COMPOSER_BRAIN.md updated through end-of-Session-3
- composer-backlog.md updated: three stale Stage-III gating items moved to Resolved, pullquote retrofit added to Active
- COMPOSER_STAGE_III_HANDOFF.md at `docs/composer/` root (preserved for reference; this Session 4 handoff is its successor)

### Deferred and tracked

Active backlog at Session 4 open has 15 items. Non-blocking for Session 4 work. The one item closest to Phase 4-new scope is the pullquote word-count retrofit (Fixture 2's 32-word pullquote violates the 8–20 schema heuristic) — flagged for Checkpoint 2 resolution, not Phase 4-new implementation start.

---

## Part III — What Session 4 is

**Session 4 target: finish the skill.** Three bullets.

### Bullet 1 — Phase 4-new implementation

Six-gate implementation pass. Code executes the Phase 4-new prompt (saved to your Desktop as `CODE_PHASE_4_NEW_IMPLEMENTATION_PROMPT.md`, or on-disk if you prefer a file reference). Each gate has explicit stop conditions. Gate A (validator), Gate B (site-level modules), Gate C (page structure + section emitters), Gate D (cross-page editorial), Gate E (photo + integrity + full orchestrator), Gate F (approval gate renderer).

Architecture is resolved: LLM authoring at editorial steps inside Phase 4-new modules, validator shifts to persona-rule adherence on editorial fields, Rule 3 microInteractionDurations collapsed to two-row (all personas except urgent-service at entry 400 / hover 180; urgent-service at entry 250 / hover 150).

Expected: 6 atomic commits (one per gate) if clean. Natural splits if any gate surfaces architectural ambiguity — halt, route, resume.

### Bullet 2 — Checkpoint 2

After Gate E (full orchestrator runs clean against all 6 fixtures at two-pass validation), Design reviews Phase 4-new output on 2–3 fixtures — the anchor set Fixtures 2/3/4 that Design authored the expected composition-plans for. Design signs off on editorial quality (validator catches adherence; Design catches quality). Pullquote word-count retrofit-or-grandfather decision surfaces here.

Sign-off opens Stage IV. Reshape routes Phase 4-new modifications before Stage IV.

### Bullet 3 — Phase 5-new implementation (Stage IV)

HTML/CSS/JS emission from composition-plan.json + profile.json. Per brain §8, Stage IV is parallelizable with Stage III once composition-plan-schema locks — which it has. Clean shape is sequenced after Phase 4-new close + Checkpoint 2, because Phase 5-new emission consumes Phase 4-new's output and Design-signed-off editorial intent.

Phase 5-new scoping is not yet authored. At Session 4 open, either Code produces a Phase 5-new scoping diagnostic analogous to the Phase 4-new diagnostic that opened Session 3, or Chat-Claude drafts scoping questions for Design to frame Phase 5-new architecture before implementation. Recommended: scoping diagnostic first, analogous to Phase 4-new flow.

**If all three land cleanly, the skill is finished.** Session 5+ is test build work — Stage V Luna validation, Stage VI retirement decision — which is out-of-scope for Session 4.

### Post-skill work (context, not Session 4 scope)

- **Stage V Luna validation build.** Run Composer end-to-end against the F7 Luna build (Prime Pool Service) to validate the rebuilt skill produces equivalent or better output than the pre-Composer skill. This is the "did the rebuild work" proof.
- **Stage VI retirement decision.** Retire the pre-Composer prospect-site skill in favor of Composer, or maintain both.

Both are referenced here for continuity but are not what Session 4 is about.

---

## Part IV — Session 4 structure (recommended)

### Shape A — Bounded, all three bullets land

Chat-Claude opens. Reads this handoff + brain + backlog + schema §14. Orients in two turns.

Sends the Phase 4-new implementation prompt to Code (saved on Desktop or copied from `docs/composer/opening-prompts/` if stashed on-disk). Code executes Gates A–F. If clean, 6 commits land.

Gate E completion triggers Checkpoint 2. Chat-Claude surfaces 2–3 fixture outputs to Design. Design signs off or reshapes.

If sign-off clean, Chat-Claude drafts Phase 5-new scoping diagnostic for Code. Code produces scoping report. Chat-Claude drafts Phase 5-new implementation prompt against resolved architecture. Code executes Phase 5-new.

If this full arc flows clean — skill is finished at end of Session 4.

Estimate: 3–5 focused hours. Realistic if no Gate halts.

### Shape B — Phase 4-new lands, Checkpoint 2 and Phase 5-new carry

Same opening, same Phase 4-new execution. If Gate E lands clean, Chat-Claude closes Session 4 at Checkpoint 2 trigger point — surfaces outputs to Design, but closes the session before Phase 5-new scoping opens. Design reviews offline. Session 5 opens with Design sign-off in hand, Phase 5-new scoping is Session 5's first work.

Estimate: 2–3 hours.

### Shape C — Gate halt triggers routing

One of Gates A–F surfaces architectural ambiguity (analogous to Session 3's Rule 3 drift or editorial-authoring boundary). Code halts pre-commit. Chat-Claude routes to Design. Design resolves. Chat-Claude redrafts the gate. Code resumes.

Estimate: variable. Don't press through. Respect the halt.

---

## Part V — Opening prompt for Session 4 (paste-ready)

On your Desktop as `CHAT_CLAUDE_OPENING_PROMPT.md`. Content repeated here for reference:

```
You are Chat-Claude in Session 4 of the Composer build for Get Rooted Media.
You are in the CTO seat, reporting to Ron, translating between Design (editorial
authority) and Claude Code (implementation).

Before doing anything else, read:

1. The Session 4 handoff brief (paste contents below or on Desktop as
   COMPOSER_SESSION_4_HANDOFF.md)
2. ~/grm-automations/docs/composer/COMPOSER_BRAIN.md — PART I §0/§8/§9, PART II
   top session block (2026-04-22)
3. ~/grm-automations/docs/composer/composer-backlog.md
4. ~/grm-automations/skills-experimental/prospect-site-composer/references/
   composition-plan-schema.md §14

After reading, orient by summarizing to Ron:
- Where the build is at Session 4 open
- What Session 4's three bullets are
- Which of Shape A / B / C matches Ron's available time today

Do not start any work until Ron confirms direction. When Ron gives the go,
the first action is sending the Phase 4-new implementation prompt to Claude
Code in a fresh Code window.

[Paste the full handoff contents here if Chat-Claude doesn't have disk access
to read the file directly]
```

---

## Part VI — Session 3 process learnings (carry these forward)

Session 3 surfaced hard lessons about Chat-Claude drafting discipline under context pressure. These are for you.

**Verify prompts against fixtures-on-disk before sending.** Session 3 had a Rule 3 persona-durations table that drifted against two of six fixtures. The drift came from drafting the table in-chat without checking whether committed fixtures honored it. Would have been a trivial check; wasn't done; cost a full Design routing cycle to resolve.

**Read scoping diagnostics for architectural holes before writing implementation prompts on top of them.** Session 3's Phase 4-new scoping diagnostic didn't name where editorial copy authoring happens. Chat-Claude shipped a six-gate implementation prompt assuming deterministic Python emission. Code caught the gap at Gate A pre-execution. Whole architectural pass to Design had to happen anyway — better to have caught it at scoping time.

**No placeholders in paste-ready artifacts.** Session 3 shipped at least one brief with `[PASTE X HERE]` that Design correctly refused to process. Don't do this.

**Context discipline.** In planning-heavy sessions, read ground-truth skill files in the first few turns before writing architectural prose. Context pressure hits faster in this workspace due to project scaffolding overhead.

**Honest context read.** Session 3 had Chat-Claude operating at 75%+ context for the last two hours. Drafting errors accumulated in that window. When context is thin, say so and slow down. Don't press through.

**One commit per logical change.** Session 3's strongest sequence was the nine-commit batch (§14 amendment + six fixture reshapes + Gate 1 polish + Fixture 1 license retrofit) because each had a clear atomic scope. When you catch yourself bundling unrelated edits into one prompt, split.

**Route to Design early when editorial reach is involved.** Session 3's two best architectural outcomes (Reading C on §2/§4 divergence, Q2 editorial-authoring architecture) came from routing Code's concerns to Design verbatim rather than Chat-Claude resolving. Your job is relay, not adjudication, when Design's authority is at stake.

---

## Part VII — What would make Session 4 fail

**Pressing through Gate halts.** Each gate stop condition exists because Session 3 identified a failure mode at that point. Halting costs a routing cycle; pressing through costs hours of rework.

**Skipping the brain read.** Fresh Chat-Claude will be tempted to dive into Phase 4-new by reading this handoff alone. Don't. The brain's PART I §9 (Approval Gate UI) and PART II top block encode decisions you can't reconstruct.

**Writing new architecture during implementation.** If Phase 4-new implementation surfaces a question the handoff doesn't answer, stop. Route to Design. The answer is Design's, not yours.

**Over-eager Phase 5-new scoping.** If Phase 4-new + Checkpoint 2 run long, cleanly close Session 4 at Checkpoint 2 trigger point. Phase 5-new in a thin-context session produces the same drift patterns Session 3 hit.

**Forgetting that the three-way culture is load-bearing.** Chat-Claude is the CTO seat because both Code and Design need a party that can route architectural calls cleanly. Absence of that function produces silent drift. Don't try to cut your own role to save time — that's what Ron tested in Session 3 and backed off from.

**Brain file drift.** Every session closes with a brain-file session block and a handoff doc. No exceptions. If Session 4 runs out of context before close-out, log where you are in-chat and Ron picks it up in Session 5.

---

## Part VIII — Composer health at Session 3 close

- **Spec on disk:** Stage I–II foundation locked. Stage II.5 fixtures complete. Stage III Gates 1–4 closed. §14 intent-spec contract live. Editorial/structural field boundary locked.
- **Fixtures on disk:** 6 profile.json + 6 expected composition-plan.json pairs. All validated against §2/§4 envelope + §14 intent-spec contract.
- **Code readiness:** claude-mem memory layer active. Code has caught 4 framework-level concerns across Session 3 at pre-commit verification — Gate 1 tie-breaking cascade, Commit 4 truncation + missing Edit 4B spec, §2/§4 vs fixture-shape divergence, Rule 3 drift + editorial-authoring boundary. Pattern is working.
- **Design readiness:** Session 3 produced substantive architectural authorship — 6-column bias table (Gate 1 Concern 1), §14 two-pillar intent-spec (Reading C), editorial-authoring architecture (Q2 resolution). Design's window has this session's context warm; if routing soon, Design orients in one turn.
- **Ron readiness:** Ron closed Session 3 at the right stopping point, not the pressured one. Flagged the process-overhead concern honestly rather than absorbing it. Held CTO-over-Chat across a 10+-hour session with clear arbitration on four architectural reframes.
- **Chat-Claude readiness:** This is you. Read this handoff. Orient against brain + backlog + schema §14. Open Session 4 ready to execute the three bullets.

---

## End of handoff

Session 4 is the finish line for the skill itself. Three bullets: Phase 4-new implementation, Checkpoint 2, Phase 5-new implementation. Don't lose the frame.

The pattern that built everything before this still works: diagnostic-first, atomic commits, route to Design on editorial reach, halt on stop conditions, right over fast.

Grateful to the three parties who built this to Session 4. Your job now is to finish it the same way.

— Chat-Claude, Session 3 close, 2026-04-22 evening

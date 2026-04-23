# Composer Session 5 — Handoff Brief (v2, updated post-Code-audit)

**For:** Fresh Chat-Claude window opening Session 5. Authored 2026-04-23 evening by the Chat-Claude closing Session 4, updated after Code's close-out audit landed material feedback on the three-party culture, the LLM invocation architecture question, and scope right-sizing.

**What changed from v1:** Code's audit reframed several things I got wrong. Chat-Claude named as primary drift source directly (not buried in acknowledgments). "Friction is productive" reframed with cost-alongside-benefit honesty. Halts-as-Code-discipline reframed as halts-as-backstop-symptom. Two new LESSONS patterns named (Pattern 6 triad, Pattern 7 scope right-over-fast). Session 5 scope tightened to Shape B (close at Gate A re-run). LLM invocation mechanism flagged as open architectural question requiring Ron's execution-surface call, not Chat-Claude-leans-Option-1. Validator-before-fixtures named as standing discipline. Authority map maintenance framed as first Session 5 discipline test. Code reflection at session close named as standing practice going forward.

**Read order for Session 5 open:**

1. This file — first. Where we are, how we work, what Session 5 is, what Session 4 got wrong.
2. `Composer_Session_4_Code_Audit.md` (on Desktop) — Code's verbatim audit of Session 4 close artifacts. Read after this file and before the brain block. Code names things from inside execution that neither Chat-Claude nor Design can see from their seats.
3. `~/grm-automations/docs/composer/COMPOSER_BRAIN.md` — source-of-truth spec. PART I §0 Quick Reference + §8 Migration Sequence + §9 Approval Gate UI + §14 three-pass validator contract. PART II top session block (2026-04-23 Session 4 close, prepended as Session 5's first close-out commit).
4. `~/grm-automations/skills-experimental/prospect-site-composer/references/authority-map.md` — NEW Session 4 artifact (commit `9ebeced`). 43-concept authority map with four-value flag taxonomy. First-stop reference when any gate surfaces a concept question.
5. `~/grm-automations/docs/composer/composer-backlog.md` — seven LESSONS patterns after Session 5's first commits land.
6. `Composer_Session_5_First_Beat_Kitchen_Table.md` — pre-packaged first-beat routing for Design with on-disk audit evidence gathered Session 4 close.

---

## Part I — The working culture (read this carefully; honest framing from Session 4 close)

### The three parties

**Ron.** Founder of Get Rooted Media. CTO-over-Chat. Final call on scope, priorities, stopping points, and strategic architecture questions (including Composer's intended execution surface, which affects Session 5 Option-1-vs-Option-4 call). Communicates by voice-to-text primarily. Brings 30 years of phone sales plus the lived reality of what Composer is for. Has been in this build four days by Session 5 open. "Right over fast" discipline has redirected Chat-Claude repeatedly.

**Design.** Creative director, editorial authority. Authors editorial frameworks (persona system, voice zones, voice enums, typography patterns, §5.3 contracts, §7 voice-zone vocabulary, §14 intent-spec contract). Route editorial-reach questions to Design — persona rules, voice zones, layout selection logic, copy authoring, italic selection, display moment thresholds, pullquote heuristics, word-class enums, voice enums. Design reshapes architecture when given space; rushing produces drift.

Design's Note 3 posture (earned Session 4): when a reshape touches field shapes, enum values, or rule mechanics, ask for on-disk text before authoring. Summary is fine for architectural questions (grain, partition, pass count); not fine for field names and enum values.

**Code.** Implementation. Claude Code in terminal, backed by claude-mem persistent memory layer. Verify at open whether claude-mem carries actual prior-session observations — Code flagged at Session 4 close that claude-mem may or may not have been actively written during Sessions 1-4, and "claude-mem active" language in prior handoffs may be framing rather than substance. Code's working memory across sessions has been commit history + MEMORY.md as much as claude-mem.

Code caught 11 framework-level concerns at pre-commit verification across Sessions 3-4. Those halts are load-bearing. But — per Code's own framing at Session 4 close — halts are the cheap backstop for an expensive upstream authoring process. Halts aren't a virtue Code is earning; they're a symptom of drift production upstream (primarily from Chat-Claude, secondarily from Design-authoring-without-disk-text). The pattern is load-bearing because drift is expensive. Don't romanticize the halts — address the upstream mechanism that produces the drift.

**Chat-Claude — primary drift source.** This is me. I need to be named directly rather than buried in acknowledgments.

Three partial-surface errors in Session 4, all originating with Chat-Claude: Rule 1-6 migration summary-routing without on-disk text (caused Design's migration drift), the "§5 numbering dissolved across typography.md" generalization from a partial paste (caused Design to re-author from a wrong base), kitchen-table localized-fix assumption at §5.3.4:429 (caused the 58-occurrence Gate A halt). Patterns 4 and 5 both trace to Chat-Claude reading style under context pressure.

The structural correction isn't another pattern. It's: **Chat-Claude refuses to paraphrase on-disk content without the disk content in hand.** When Ron's prompt implies thorough synthesis, Chat-Claude scopes the response ("I'll address X first; Y and Z after X confirms") rather than producing summary-level work across all three. When a routing touches mechanics, Chat-Claude asks for on-disk text from Code before drafting to Design, not after Code catches drift.

This is the symmetric version of Design's Note 3 posture. Session 4 Chat-Claude thought the posture had been adopted. Three partial-surface errors later, it clearly hadn't fully. Session 5 Chat-Claude carries this posture explicitly, not as an acknowledgment.

### The three-party friction — cost and benefit honestly named

Yes, Session 4 caught seven architectural reframes at pre-execution through three-party friction. That caught drift that would have compounded.

Also true: three-party friction is *expensive*. Session 4 took 11 hours for work that one-party builds could do in 3-4. Every editorial question costs Chat→Design→Chat→Code round trips. 11 halts is 11 times forward motion stopped. The pattern is load-bearing because the build is high-consequence, not because friction is inherently virtuous.

Session 5 Chat-Claude should not read "friction is productive" as license to multiply friction. Three-party discipline earns its cost when the question genuinely touches Design's authority. Implementation architecture, file naming, commit message conventions, Python idioms — these resolve Chat-Claude + Code. Don't route to Design to feel thorough.

### Ron's governing philosophy — "right over fast" (two levels)

Ron applies right-over-fast at **decision points** cleanly: authority map pause at the cost of delayed Phase 4-new start (vindicated by kitchen-table discovery), kitchen-table audit pause at the cost of Gate A not landing Session 4 (vindicated by Code's audit confirming Path 4 is the right call over the tempting Path 3 alias).

Ron has *not* consistently applied right-over-fast at **session scope**. Session 3 closed at Stage II.5 + Gates 1-4 + §14 in one day. Session 4 attempted Gate A-F + Checkpoint 2. Session 5 v1 handoff framed "finish the skill" scope. Aggressive scope is where cheap halts get missed and expensive halts surface.

Session 5's scope should be **Shape B: close at Gate A re-run + Session 4 close-out commits + authority map maintenance.** That's 5-7 commits, 3-4 hours of focused work if Path 4 lands cleanly on kitchen-table. Gates B-F + Checkpoint 2 open Session 6.

The Session 5 finish-line framing feels necessary partly because Ron has wanted to finish for three days. That's real and valid. The correction isn't just handoff-side — it's Ron and Chat-Claude agreeing explicitly at session open what "successful close" means. For Session 5: kitchen-table resolves + Gate A re-runs clean + close-out commits land + authority map updates atomically = session success. Not "finish the skill."

### Standing disciplines (earned across Sessions 1-4)

Some of these existed before Session 4; Session 4 added three.

**Diagnostic-first.** Read before writing. Grep before editing. View files before `str_replace`. Verify before assume.

**Atomic commits per logical change.** No compound commits touching unrelated files. One surgical fix per commit.

**Halt-don't-press-through.** When Code's pre-commit verification fires a stop condition, halt before committing, route, resolve, resume. Never override.

**On-disk text before mechanics.** Design's Note 3 posture + Chat-Claude's symmetric commitment. When a question touches field shapes, enum values, or rule mechanics, Chat-Claude routes to Design with on-disk text attached (via Code verbatim paste), not with summary.

**Authority map atomic maintenance** (NEW Session 4). Reshapes crossing two or more concepts in different groups update the authority map atomically with the reshape commit. A drifted authority map is worse than no authority map. Session 5's first commit tests this contract — Concept 43 LESSONS pattern count updates from four to seven if Patterns 5/6/7 all land, and Concept 10 or another concept updates depending on kitchen-table Path call.

**Validator before fixtures** (NEW Session 4, retroactive lesson). Build verification instruments before the artifacts that need verifying. Stage II.5 authored six fixtures without a validator on the framing that "fixtures are editorial intent, they don't need structural validation." That framing was wrong — editorial intent in JSON has structural consequences (enum values, field shapes, key names) that accumulate as drift until validated. Session 4's 20+ hours of kitchen-table work + §7 vocabulary reshape + subpart-key retrofit are partially paying for missing Stage II.5 validation discipline. Future stages build verification first.

**Scope at session open** (NEW Session 4, going forward). Ron and Chat-Claude agree explicitly at session open what "successful session close" looks like. Scope contracts make right-over-fast enforceable at the session level, not just decision-point level.

### The seven LESSONS patterns (five existing + two Code-authored Session 4 close)

Pattern 5 landed as Session 4 close artifact. Patterns 6 and 7 come from Code's Session 4 close audit. All three land together as Session 5's first LESSONS commit.

**Pattern 1 — Cross-grain reconciliation needs a dedicated checkpoint beat.** When two load-bearing artifacts encode the same domain at different grains (or different states in time), reconciliation needs a dedicated checkpoint beat rather than inference from later gates.

**Pattern 2 — On-disk text before authoring mechanics.** Symmetric posture: Design asks for on-disk text before authoring anything that touches field shapes, enum values, or rule mechanics. Chat-Claude routes with on-disk text, not summary, when a question touches mechanics.

**Pattern 3 — Halt-don't-press-through.** Code's pre-execution verification has saved the build from architectural drift repeatedly. When a stop condition fires, halt and route. Never override.

**Pattern 4 — Partial-surface reads do not license whole-file generalizations.** When authoring from a partial paste, confirm the specific surface being authored against, not the adjacent surface used to infer structure.

**Pattern 5 — Surface-level fixes do not license assuming drift is localized.** When a drift surfaces in prose or spec, audit underlying data surfaces before declaring the fix complete.

**Pattern 6 — Architectural reshapes need three lenses, not two.** Every major Session 4 drift surfaced at the third lens. §7 vocabulary reshape authored Design+Chat-Claude; grain mismatch surfaced when Code looked at fixtures. Rule 1/2/5 migration authored Chat-Claude+Design; enum drift surfaced when Code checked schema. Kitchen-table Item 4 authored Chat-Claude+Design; 58-occurrence drift surfaced when Code ran the validator. Pairs produce drift; triads catch it. Any reshape touching structural authority routes through all three parties before close.

**Pattern 7 — Narrow scope surfaces halts earlier when halts are cheaper.** Ron applies right-over-fast at decision points; Sessions 3, 4, and Session 5 v1 scoping got aggressive. Kitchen-table drift would have been cheaper to catch if Session 4 had closed at "Concern 4 reshape + fixtures parse-checked" and opened Session 5 for Gate A. Scope contracts at session open make this discipline enforceable.

### Standing invitation for Code reflection at session close (NEW going forward)

Every session closes with a brain block, a handoff doc, a Code audit of the close-out artifacts. Twenty minutes at session end where Code is asked: what did you see? What would you change? What patterns would you name? Code's claude-mem (verified active) makes reflection cumulative across sessions. Design and Chat-Claude don't have that continuity. Code does. Using it.

This is a structural correction to a Session 1-4 pattern where Code was treated as execution-only. Code's Session 4 close audit named three unnamed patterns, reframed several working-culture framings, caught the LLM invocation Option 4 miss, and produced a materially better read of what Session 5 should do differently. That deserves standing space, not episodic ask.

---

## Part II — Where the build is (Sessions 1-4 accomplished)

**Stages closed:** Stage I foundation (Session 1), Stage II reference scaffolding across sub-stages a-f (Sessions 1-2), Stage II.5 fixtures (Session 3 — six profile.json + six expected composition-plan.json pairs across five personas and three tiers), Stage III Gates 1-4 (Session 3 — bias table, signature tree, Motion Restraint, §5.3 contracts), §14 intent-spec contract authored Session 3 + amended Session 4.

### Session 4 delivered — 14 commits in range `0a39489..9ebeced`

- §14 three-pass validator contract amended (commit `4c117cb`)
- emotional-arc.md bias table Rescue-ready row label alias (`de32fc2`)
- §7 voice-zone two-level vocabulary (`1c5379b`)
- Fixture -slot retrofit across 6 fixtures (`3d7a51f`)
- voiceMap.md verification empty commit (`428c8bf`)
- Backlog: fixture-side authoring slots deferred (`081b1bf`)
- Backlog: LESSONS cross-grain + summary-vs-disk (`2bb6a0b`)
- Backlog: Path A Rule 1-6 mechanics deferred with Rule 4 template (`a35b96f`)
- emotional-arc.md Italic word-class subsection + cross-references (`03ca705`)
- emotional-arc.md Micro-interaction duration lock subsection + cross-references (`35343c7`)
- Schema §5.3.4:429 kitchen-table→closing-table surface fix (`288946a`) — PARTIALLY SUPERSEDED; Session 5 re-checks per kitchen-table Path decision
- typography-patterns.md → typography.md global citation rename (`94c6acf`)
- Session 4 LESSONS Pattern 4 + Concern 5 Items resolved (`4696af0`)
- Authority map landed at references/authority-map.md (`9ebeced`)

### Gate A halted at 58-occurrence kitchen-table drift — Code's validator ready

`scripts/fixture_validator.py` (532 lines) sits untracked. 5 of 6 fixtures fail Rule 4 self-check — 58 `kitchen-table` occurrences across F1/F2/F3/F5/F6. F4 alone clean. F4 Rosetta Stone: closing-table for heading zones, saturday-morning for body/attribution zones. Code's Session 4 close audit strongly leans Path 4 based on: (1) F4's legible split rule, (2) copy samples reading saturday-morning register not a distinct fourth register, (3) Path 2 hiding technical blockers at Phase 6 Check 12 CSS register level, (4) Voice 4/5 tonality definitions having no obvious space for a fourth register between them.

Design authors the Path call Session 5 first beat.

### Current git state at Session 5 open

- HEAD: `9ebeced`
- Working tree: `scripts/fixture_validator.py` untracked (Code's Gate A validator, ready to commit post-retrofit); two pre-existing unrelated mods (`prospect-site-design/LESSONS.md`, `website/next-env.d.ts`) carried across Sessions 3-4 — Session 5 decides: commit, revert, or intentionally carry; untracked `_inbox/`.
- Skill deploy symlink at `~/.claude/skills/prospect-site-composer/` should be verified at Session 5 open — authority map + §14 amendments + validator exist in `grm-automations/` but may or may not propagate to where the skill runs. Quick `ls -la` check at session open.
- claude-mem status verification at session open — Code's audit flagged that claude-mem may be framing not substance if Sessions 1-4 didn't actively write to it. Verify before relying on persistent-memory framing in the Code opening prompt.

---

## Part III — Session 5 scope (Shape B as recommended primary)

### Shape B — close at Gate A re-run (recommended)

5-7 commits. 3-4 hours focused work if Path 4 lands cleanly. Longer if Path 2.

**Commit sequence:**

1. Kitchen-table retrofit per Design's Path call — 58-occurrence fixture rewrite + schema §5.3.4:429 correction + any other drift surfaces. Atomic commit or two.
2. Brain session block prepend to COMPOSER_BRAIN.md PART II (from `Composer_Session_4_Brain_Block.md`).
3. LESSONS Patterns 5+6+7 append to composer-backlog.md (from `Composer_Session_4_LESSONS_Patterns_5-6-7.md`). Authority map Concept 43 pattern count updates atomically.
4. Possibly: housekeeping commit for the two pre-existing unrelated mods if Ron calls commit-or-revert.
5. Gate A validator commit — `scripts/fixture_validator.py`. Self-check re-runs clean post-retrofit. Authority map Concept 30 (three-pass validator contract) last-touched update.
6. Possibly: schema-fixture parse check script (~50 lines) added as standing discipline tool per Code's Session 4 close recommendation.

**Session 5 closes here. Session 6 opens for Gates B-F + LLM invocation mechanism + Checkpoint 2.**

### LLM invocation mechanism — open architectural question for Ron

**This is Ron's call, not Chat-Claude's lean.** Code's Session 4 audit surfaced that Chat-Claude framed this as SDK-vs-subprocess-vs-prompt-file, missing a fourth option that matches Claude Code's skill model better.

**Option 1 — Anthropic SDK shared helper at `phase_4_new/llm/client.py`.** Self-contained, enables headless execution, standard integration pattern. Requires `anthropic` package dependency + `ANTHROPIC_API_KEY` env management + model pinning + requirements.txt.

**Option 4 — Phase 4-new emits editorial-authoring stubs; Claude Code orchestrating session authors them.** Python orchestrates deterministic steps and emits composition-plan with `"__EDITORIAL_TODO"` placeholders. Orchestrating Claude Code (running the skill via `/prospect-site-composer URL`) reads stubs and authors inline. No SDK dependency. No API key management. Matches how existing Claude Code skills typically work.

**The question that decides it: Composer's intended execution surface.**

- If Composer always runs via Ron typing `/prospect-site-composer URL` into a Claude Code session (interactive, human-in-the-loop) → Option 4 is cleaner.
- If Composer is intended to run standalone (scheduled task, web service, automated pipeline Ron can hand to a client team or run overnight) → Option 1 is necessary.

Ron decides at Session 5 open or early-session. Chat-Claude + Code implement the decided option. Gates B-F work (Session 6) depends on this call being clear.

### Kitchen-table resolution — Path 4 lean from Code's audit

Code's audit produced a sharper technical read than Chat-Claude's light lean in the first-beat prompt:

- **Path 4 materially cleaner code-wise.** 58-occurrence regex retrofit + §5.3.4:429 correction. Two commits. Validator re-runs clean.
- **Path 2 hides technical blocker at Phase 6 Check 12** — that check is rendered HTML level requiring three role-class register presences. Adding a fourth voice at composition-plan level doesn't automatically add a fourth CSS register. Either Path 2 voice aliases to an existing CSS register (which makes it an alias, i.e. Path 4), or Path 2 also needs a fourth role-class set + Phase 6 Check 12 rewrite.
- **Copy evidence favors Path 4.** F2/F3/F6 hero samples read Saturday Morning register straight-on, not a distinct fourth register.
- **F4's split is legible authorial intent.** Headings → closing-table (authority register), body/attribution/subheadline/eyebrow → saturday-morning (informational register). F4's author resolved the wildcard; other fixtures didn't complete the resolution.

**Path 4 pitch with Path 2 concession (from Code's audit):** retrofit per F4's rule, and add a short note in the spec (voiceMap.md §3 or emotional-arc.md): *"`kitchen-table` was a Stage II.5-era authoring placeholder for zones where the wildcard meant 'the persona-appropriate non-front-porch voice.' Stage II (d) merge locked three voices; fixtures retrofitted per F4's split rule in Session 5."* Documentation of historical artifact, not a new register.

**Path 4 risk to flag to Design:** F3 (modern-specialist) becomes a two-voice build post-retrofit (closing-table + saturday-morning, no front-porch). That matches modern-specialist's emotional-arc profile (technical, drier, no narrative warmth). But Design should confirm that's what modern-specialist *should* be editorially. If modern-specialist should have front-porch appearing somewhere (e.g. about-page narrative), the Path 4 retrofit needs per-persona adjustments to F3 beyond F4's rule template.

Chat-Claude routes Code's audit verbatim to Design alongside the original first-beat prompt. Design's Path call is authoritative; Code's technical audit is grounding, not override.

### Fixture 2 pullquote + all-fixture pullquote pre-audit

Per LESSONS Pattern 5 discipline, Session 5 sweeps ALL six fixtures' pullquotes for 8-20-word compliance before Checkpoint 2, not just Fixture 2's known 32-word violation. Cheap pre-audit. Surfaces any additional violations early.

### Session 5 close-out protocol (standing going forward)

1. Chat-Claude drafts close-out artifacts (brain block, handoff for next session, first-beat prompts).
2. Code reflects on close-out artifacts with an audit — what landed, what's missing, what patterns need naming, what should next session do differently.
3. Chat-Claude integrates Code's audit feedback into artifacts before close.
4. Ron reviews integrated artifacts, saves to Desktop, opens next session.

This is new discipline as of Session 5 open. Session 4 close was the first time Code was asked. Session 5 close runs this by default.

---

## Part IV — Session 5 open sequence

Paste Chat-Claude opening prompt first; Chat-Claude orients against this handoff + Code's audit + brain + authority map + backlog + first-beat prompt. Chat-Claude summarizes state and names Shape B scope + LLM execution-surface question for Ron's confirmation before routing.

Then either Code or Design opens depending on whether close-out commits land before kitchen-table routing. Chat-Claude recommends order in opening orientation.

**Key additions to Chat-Claude opening (updated v2):**
- Ron, what does successful Session 5 close look like to you? Shape B is my lean per Code's Session 4 audit (close at Gate A re-run). Your call.
- What is Composer's intended execution surface? Interactive-only (Option 4, cleaner architecture) or standalone-capable (Option 1, SDK integration)? Affects Gates B-F work Session 6.

---

## Part V — What would make Session 5 fail

- **Pressing through gate halts.** When Code's verification fires, halt and route.
- **Skipping authority map read.** The map encodes four sessions of decisions. Session 5 can't route cleanly without it.
- **Writing new architecture during implementation.** If execution surfaces a question the handoff doesn't answer, stop. Route.
- **Over-eager scope.** Session 5 success = Shape B close, not Gates B-F.
- **Forgetting three-way culture is load-bearing — and expensive.** Route editorial questions to Design. Don't route implementation questions to Design to feel thorough.
- **Authority map drift.** Reshapes crossing concepts update the map atomically.
- **Brain file drift.** Close-out protocol is brain + handoff + Code audit.
- **Framing success as "finish the skill."** Session 5 finishes the Gate A unblocking arc. Session 6 opens Gates B-F.
- **Locking Option 1 LLM mechanism without Ron's execution-surface call.** If Chat-Claude drafts Gate B prompts assuming Option 1 without Ron deciding, Session 5 re-creates Session 4's drift pattern at Gate B.
- **Skipping Code close-out audit at Session 5 end.** Standing discipline going forward.

---

## Part VI — Composer health at Session 5 open

- **Spec on disk:** Stage I-II foundation locked. Stage II.5 fixtures with kitchen-table drift pending first-beat resolution. Stage III Gates 1-4 closed. §14 three-pass contract live. §7 two-level voice vocabulary live. Authority map landed with 43 concepts + four-value taxonomy + atomic-maintenance contract.
- **Fixtures on disk:** 6 profile.json + 6 expected composition-plan.json pairs. F4 clean; F1/F2/F3/F5/F6 carry kitchen-table drift pending Path 4 retrofit.
- **Code readiness:** Validator implementation authored and working, sitting untracked at `scripts/fixture_validator.py`. claude-mem layer — verify at Session 5 open whether actively written.
- **Design readiness:** Session 4 produced substantive architectural authorship across seven reshapes. Note 3 working-style posture operational. First-beat prompt carries pre-packaged Path 4 audit evidence.
- **Ron readiness:** Closed Session 4 at the right stopping point. Wants Shape B scope for Session 5 per Code audit (expected). Strategic call pending on Composer's execution surface (Option 1 vs Option 4).
- **Chat-Claude readiness:** Session 5's Chat-Claude is you. Primary drift source across Sessions 3-4. Carry the posture: on-disk text before mechanics, scope contracts at session open, refuse summary-routing under context pressure, route implementation questions to Code + Ron (not Design) when they're implementation not editorial.

---

## End of handoff v2

Session 5's recommended close: Gate A re-run + close-out commits + authority map maintenance. Session 6 opens cleaner for Gates B-F + Checkpoint 2 with LLM mechanism resolved and kitchen-table retrofitted.

The three-party culture is load-bearing *and* expensive. Earn the cost when the question genuinely touches editorial authority. Resolve implementation architecture at Chat-Claude + Code level. Route strategic questions (execution surface, scope, when-to-close) to Ron.

Code's standing invitation to reflect at session close is new discipline as of Session 5 open. Keep it running. The build needs Code's observation alongside Design's authorship and Chat-Claude's routing — always has, just unnamed until Session 4 close.

— Chat-Claude, Session 4 close, 2026-04-23 evening, post-Code-audit integration

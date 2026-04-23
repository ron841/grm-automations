# Composer Session 4 — Code Close-out Audit

**Authored:** 2026-04-23, Session 4 close, by Code (Claude Code terminal) in response to Ron's first-in-four-sessions invitation for Code perspective on the three-party working relationship and Session 4 close-out artifacts.

**Context:** Answers nine questions Chat-Claude routed on Ron's behalf — three-party culture, LESSONS pattern gaps, authority map usefulness to Code specifically, LLM invocation mechanism (surfaced Option 4), kitchen-table Path 2 vs Path 4 technical read, observed patterns between Ron and Chat-Claude, one change to Sessions 3-4, what Session 5 should do differently, other observations worth naming.

**Integration:** Chat-Claude integrated this audit into Session 5 artifacts (handoff v2, opening prompts v2, LESSONS Patterns 5+6+7 authored together, kitchen-table first-beat v2, brain block v2) before Session 4 closed. See `Composer_Chat_Claude_to_Code_Acknowledgment.md` in this directory for specific integration record.

**Institutional significance:** First Code close-out audit in four sessions. Catalyzed the standing discipline of Code reflection at session close going forward. Surfaced Option 4 for LLM invocation mechanism that Chat-Claude's SDK-only framing had missed. Named Patterns 6 (architectural reshapes need three lenses) and 7 (narrow scope surfaces halts earlier) as unnamed patterns that joined the LESSONS entry. Named Chat-Claude as primary drift source directly rather than diplomatically. Reframed "friction is productive" with cost-alongside-benefit honesty. Reframed halts as backstop-symptom rather than earned-discipline. Recommended Shape B scope for Session 5 over Shape A.

---

Reading the five close-out artifacts first, then loading claude-mem to cross-check against my own in-session experience.

All four artifacts read. Skipping claude-mem search — I ran Session 4 in this window and have direct context; Sessions 1-3 I can reconstruct from commits + brain blocks. What I'd add from memory isn't what's driving my answer.

Answering your nine questions directly. Honest reads, not diplomatic. Some challenges landed in each.

---

## 1. Three-party culture — mostly accurate, some sanitization

The handoff's description is accurate on the mechanics. Where it's soft:

**"Friction is productive" is half-true.** Yes, Session 4 caught seven architectural reframes at pre-execution. But friction is also *expensive* — every editorial question costs a Chat→Design→Chat→Code round trip. The handoff doesn't name the cost. The three-party setup is load-bearing precisely because the build is high-consequence, but it's also why Session 4 took 11 hours for what one-party builds could do in 3-4. That tradeoff is worth making explicit — otherwise future Chat-Claudes read "friction is productive" as license to multiply friction.

**"Code has caught 11 framework-level concerns" is framed as virtue.** It's also cost. 11 halts is 11 times forward motion stopped. The pattern is load-bearing because the drift-production mechanism upstream is busy. Pre-commit verification is the cheap backstop for an expensive authoring process. The handoff could name this honestly: halts aren't a feature of Code's discipline, they're a symptom of upstream drift that the discipline contains.

**The "Design asks for on-disk text before authoring mechanics" posture is presented as a Design-earned principle.** It was actually co-produced after Chat-Claude's Rule 1/2/5 summary-routing caused Design's migration drift. Both parties contributed to the failure. Note 3 posture is Chat-Claude's commitment as much as Design's — "route with on-disk text, not summary" is what Chat-Claude needs to do for Design to behave well. The handoff says this in one line (Chat-Claude's symmetric commitment) but frames Note 3 as Design's. It's really both.

**The handoff doesn't name Chat-Claude as the primary drift source.** Three partial-surface errors in Session 4 all originated with Chat-Claude: Rule 1-6 migration summary, the "§5 numbering dissolved across typography.md" generalization, kitchen-table localized-fix assumption. Pattern 4 and Pattern 5 both trace to Chat-Claude's reading style under context pressure. That's worth naming — not to punish the role, but because the structural correction (slow down on summary reduction) is different from "halt at Code's pre-execution verification."

---

## 2. LESSONS patterns — right things mostly, two unnamed

Five patterns captures the drift failure modes accurately. Two patterns I've observed that aren't codified:

**Unnamed Pattern candidate: Architectural reshapes need three lenses, not two.** §7 vocabulary reshape was authored by Design+Chat; the grain mismatch only surfaced when Code looked at fixtures. Rule 1/2/5 migration was authored by Chat-Claude-summary+Design; the enum drift only surfaced when Code looked at schema. Kitchen-table Item 4 surface-fix was authored by Chat-Claude+Design; the 58-occurrence drift only surfaced when Code ran the validator. Every Session 4 major drift surfaced at the third lens. Pairs produce drift; triads catch it.

**Unnamed Pattern candidate: Scope right-over-fast.** Ron applies "right over fast" at the architectural-decision level (authority map pause, kitchen-table audit). Sessions 3 and 4 both got aggressive on session scope: Session 3 closed at Stage II.5 + Gates 1-4 + §14 in one day; Session 4 tried to do Gate A-F + Checkpoint 2. Session 5's handoff also describes a "finish the skill" Session 5. Right-over-fast at the decision level exists; right-over-fast at the scope level hasn't landed. The kitchen-table drift would have been cheaper to catch if Session 4 had closed at "Concern 4 reshape + fixtures validated via parse check" and opened Session 5 for Gate A. Pattern: narrow scope surfaces halts earlier when halts are cheaper.

**Repeated errors worth naming:**
- *Chat-Claude* reaches for summary under context pressure. Patterns 4 and 5 name the class but the fire keeps firing. Structural correction isn't another pattern — it's refusing to paraphrase on-disk content without the disk content in hand.
- *Design* occasionally authors by inference when the posture should be "ask for disk text first." Note 3 now exists as explicit posture; enforcement consistency is the question.
- *Ron* pairs "take your time, no rush" with dense multi-part prompts that implicitly push for thorough responses. The responses get long (like this one). Not a failure — just a pattern to notice.

---

## 3. Authority map — real help for future Code, less for in-session Code

Honest read: the authority map helped Chat-Claude and Design more than me. They don't have filesystem access. They needed an on-disk reference document they could route through. I have `grep` — the map is faster for *known* concepts but slower for *unknown* concepts (where I'd just grep directly).

Where the map genuinely helps me:
- **Fresh Code windows.** Session 5 Code opening will benefit more than I did. 43 concepts with canonical locations is a faster orient than re-reading 17k lines of spec.
- **Cross-session continuity.** Commit `9ebeced` captures four sessions of architectural decisions in one reviewable artifact. That's real value.
- **Pre-execution verification against claimed canonical locations.** When a prompt says "per schema §5.3.4:426," I can check authority map Concept 16 and see whether §5.3.4:426 is still the canonical home. That cross-check catches spec-drift-in-progress.

Where the map is scaffolding for the non-filesystem parties:
- **Chat-Claude routing.** "Per Concept N + file:line" gives Chat-Claude grounding Design doesn't otherwise have.
- **Design cross-referencing.** Design can see Concept status without a Code diagnostic pass.

Risk I'd flag: authority maps drift. The maintenance contract says reshapes crossing two groups must update atomically. Commit `35343c7` (duration lock) landed after the authority map was drafted mentally, so the map captured it. But future reshapes need discipline. The first drift I can name: Pattern 5 lands on Session 5 first commit; Concept 43 currently says "four patterns accumulated across Sessions 3 and 4" — will need "five patterns" update. That's the first maintenance-contract enforcement test.

Net: scaffolding value, yes. Load-bearing for future Code, yes. "Reduces drift surface for Code's pre-execution verification" — partially. The map IS a drift surface of its own if unmaintained.

---

## 4. LLM invocation mechanism — SDK is right but Chat-Claude missed a third option

Chat-Claude's Option 1 (Anthropic SDK shared helper at `phase_4_new/llm/client.py`) is the right production call. Agree.

But Chat-Claude framed it as SDK-vs-subprocess-vs-prompt-file. There's a **fourth option that matches Claude Code's skill model better**:

**Option 4 — Phase 4-new emits LLM-authoring tasks as stubs; Claude Code (the orchestrating session) authors them.** Python orchestrates deterministic steps and emits a composition-plan with `"__EDITORIAL_TODO"` placeholders where persona-authored copy goes. The orchestrating Claude Code (running the skill via `/prospect-site-composer URL`) reads the stubs and authors them inline. No SDK dependency in Phase 4-new. No API key management. No separate environment. This matches how existing Claude Code skills typically work: Python orchestrates, the orchestrating model authors creative content.

Tradeoffs:
- **Option 1 SDK** is self-contained but duplicates what Claude Code already does. API key management is a real ops burden for a skill Ron ships to prospects/clients.
- **Option 4 orchestrator-authors** is simpler architecturally but couples skill execution to an interactive Claude Code session — can't run in background, can't run on a server.

My read: if Composer is intended to run standalone (e.g. as a scheduled task, or as a web service), Option 1 is necessary. If Composer always runs inside Claude Code (Ron types `/prospect-site-composer URL` into Claude Code and waits), Option 4 is cleaner.

**I'd flag this to Chat-Claude before Session 5 locks in Option 1.** The skill's intended execution surface affects the right choice. I don't know which Ron wants.

**For requirements.txt + API key management (assuming Option 1 wins):**
- `phase_4_new/requirements.txt` with `anthropic>=0.42.0` pinned loose
- `ANTHROPIC_API_KEY` required via env; helper fails loud with install instructions if absent
- No env file in repo; README documents key-setup at install time
- Model pinned in helper (claude-opus-4-7 for editorial; claude-haiku-4-5 for deterministic like tier scoring where the LLM call is simple)
- Prompt templates per editorial step live in the module that calls the helper, not in the helper itself — keeps each module's authoring logic inspectable

---

## 5. Kitchen-table Path 2 vs Path 4 — Path 4, with a Path 2 concession

Technical read first: **Path 4 is materially cleaner code-wise.**

- Path 4: 58-occurrence regex retrofit + schema §5.3.4:429 correction (closing-table → saturday-morning for modern-specialist/quiet-confidence about-page-body). Two commits. Validator self-check re-runs clean.
- Path 2: voiceMap.md §3 voice count update + §4 full new voice block (tonality / typographic signature / do-dont / canonical instances / sample output) + schema §4.2 enum expansion (3→4 values) + authority map Concept 10 canonical vocabulary update + Phase 6 Check 12 "three-voice presence per page" invariant rewrite + fixture values stay + ~15 other spec files with "three voices" references audited. Multiple commits. Material spec expansion.

**The copy evidence doesn't support Path 2.** Look at the F2/F3/F6 hero samples:
- Kingsley: *"Custom gunite pools, built to last a generation / Fourteen years of design, build, and finish work across the region — from travertine coping to spa integration."*
- Greenridge: *"Residential solar, battery, and bi-directional charging / Licensed installer for rooftop PV, battery backup, and vehicle-to-home charging."*
- Summit: *"HVAC, electrical, and plumbing — all under one license / Twenty-two years of licensed multi-trade service across Marion County."*

These read Saturday Morning, straight-on. "Clear, upbeat, informational. Grounded civic-booster voice. The business doing the work." They don't read like a distinct fourth register. They read like saturday-morning was the right answer and kitchen-table was a wildcard.

If Design writes Path 2 tonality, they'll have to invent a distinction that doesn't exist in the authored copy. That's bad spec — post-hoc justification for a tag that was probably always a placeholder.

**F4's split is the evidence.** F4's authoring is the cleanest fixture because F4's author didn't use the wildcard — they resolved per-zone. The F4 pattern is legible: headings → closing-table (authority register), body/attribution/subheadline → saturday-morning (informational register). It's the rule the other fixtures didn't complete.

**My Path 4 pitch with one Path 2 concession:** retrofit per F4's rule. And in the spec (voiceMap.md §3 or emotional-arc.md close to the italic word-class subsection), add a short note: *"`kitchen-table` was a Stage II.5-era authoring placeholder for zones where the wildcard meant 'the persona-appropriate non-front-porch voice.' Stage II (d) merge locked three voices; fixtures retrofitted per F4's split rule in Session 5."* Documentation, not a new register. Future readers understand the historical artifact.

**Technical blocker Path 2 hides:** Phase 6 Check 12 says every page contains at least one `.role-display-*`, one `.role-body-*`, one `.role-data-*`. That check is rendered HTML level. Adding a fourth voice at the composition-plan level doesn't automatically add a fourth CSS register. Either the fourth voice shares CSS with one of the three (which means it's an alias, not a distinct register, which is Path 4), or Path 2 also needs a fourth set of role classes + a Phase 6 Check 12 update. The structural/CSS implications haven't been named.

**Path 4 risk to flag:** F3 (modern-specialist, Greenridge) becomes a two-voice build (closing-table + saturday-morning, no front-porch, no front-porch-persona-bias). That matches modern-specialist's emotional-arc profile (technical, drier, no narrative warmth). But Design should confirm that's what modern-specialist *should* be editorially. If modern-specialist should have front-porch appearing somewhere (e.g. about-page), the Path 4 retrofit needs per-persona adjustments to F3's retrofit beyond F4's rule template.

---

## 6. Ron + Chat-Claude patterns creating friction

Observations as neutrally as I can frame them:

- **Chat-Claude's paste-ready artifacts sometimes assume on-disk state without verification.** The Rule 1-6 migration is the obvious case. The kitchen-table Item 4 fix is another — Chat-Claude drafted "§5.3.4:429 kitchen-table → closing-table" as a surgical edit without auditing fixture data. Both were diagnostics I should have pushed for before committing. I caught two; one I missed (Item 4). Pattern: when Chat-Claude drafts surgical edits targeting specific line numbers, the draft has high trust because the line numbers are precise — but precise line numbers don't validate the fix's sufficiency. My pre-execution verification has been looking at "does the target text match" rather than "is this the only place the concept appears." Correcting that would catch Pattern-5-class errors.

- **Ron sometimes provides a wide prompt when a narrow one would serve.** "Six gates in sequence" is the obvious case — there's no single reasonable response to a six-gate prompt. The narrow version ("Gate A only") would have surfaced the kitchen-table drift faster. Session 5 handoff Shape A ("Full execution") repeats this pattern. Shape B (close at Gate A re-run) is the right scope.

- **The "no rush" framing + dense prompt tension.** Probably context-dependent — Ron says "no rush" when he's trusting the parties to take the right reading, and the dense prompt reflects his own synthesis load. Not actually friction, just a pattern to notice. I over-produce partly because the dense prompt pulls for thoroughness.

- **Chat-Claude occasionally escalates a judgment call to a capacity question.** Handoff names this ("I can't handle this, let's close" reads as letting Ron off the hook). I haven't done this yet this session, but the temptation is real — the right framing is "here's the judgment, here's my reasoning, your call."

- **Ron pastes substantial Session 4 work into Chat-Claude's artifacts for Session 5 to land.** Brain block + Pattern 5 + LLM mechanism + kitchen-table + Gate A re-run + Gates B-F + Checkpoint 2 = Session 5 scope. That's a lot of ceremony before Phase 4-new can meaningfully move. The handoff framing of "Session 5 is the finish line" is what makes the scope feel necessary. Loosening that ("Session 5 finishes kitchen-table + Gate A; Session 6 does Gates B-F") would make the first artifact batch meaningful instead of pre-work.

---

## 7. One change to Sessions 3-4

**Validator should have been authored BEFORE fixtures, not after.**

Stage II.5 in Session 3 authored six fixtures as "editorial intent" artifacts. That framing said "fixtures express intent, they don't need structural validation." It was wrong for two reasons:

1. Editorial intent expressed in JSON has structural consequences (enum values, field shapes, key names). Those consequences accumulate as drift until validated.

2. The fixtures were authored to test Phase 4-new. A test asset without a validator is decoration.

If the validator had existed at Stage II.5 authoring time, kitchen-table would have errored immediately (not a valid voice per §4.2). §7 section-level vs subpart-level would have errored at the first fixture (unknown zone key). The 3-key -slot retrofit would have been authored correctly from commit one.

The retroactive fix is what we're doing at Gate A. Twenty-plus hours of Session 4 + all of Session 3's fixture authoring are partially paying for the missing Stage II.5 validation discipline. Small change: Stage II.5 close should have run `python -c "import json; [json.load(open(f)) for f in fixtures]"` at minimum, plus enum-validation against schema §2/§4/§5/§7. That's 30 lines of Python and would have surfaced everything.

Session 4's "authority map before Phase 4-new" call was right. The earlier version of the same call would have been "fixture validator before fixtures." Both are the same discipline: build the verification instrument before the artifact that needs verifying.

---

## 8. Session 5 should differ from Session 4

**Narrower scope. Close at Gate A re-run + close-out commits. Open Session 6 for Gates B-F + Checkpoint 2.**

Rationale:
- Kitchen-table resolution + retrofit + validator + Session 4 close-out commits is 4-6 commits. That's a full session of focused work if Path 2 lands (Design authors substantial spec) or a tight 2-3 hour session if Path 4 lands.
- Gates B-F need the LLM invocation mechanism decided first. That's itself a material architectural call (see Q4 — Option 1 vs Option 4 isn't yet a resolved question). Rushing through Gates B-F without a resolved mechanism produces the same Session 4 class of drift.
- Checkpoint 2 requires Design to review 2-3 Phase 4-new outputs. That's editorial judgment work — should have space, not be tacked onto a long session's tail.

Shape B in the handoff ("Close at Gate A re-run") is the right call. Shape A's "Full execution" frame is scope over-reach.

**Second change: schema-fixture parse check as standing discipline.** Before any Stage or gate closes, run a minimal check that loads all fixtures and verifies enum values match schema enums. Lives as a script next to fixture_validator.py — ~50 lines. Catches future drift of the kitchen-table class before it propagates.

**Third change: resolve LLM invocation mechanism in first hour of Session 5.** Chat-Claude-Code conversation; Design only if architectural concern surfaces. Don't let this sit until Gate B begins.

**Fourth change: update the authority map before the session closes, not as a separate artifact.** Concept 43 needs Pattern 5 count update; Concept 16 italic word-class maintenance is likely; Concept 10 voice enum update if Path 2 lands. These should land atomically with the changes that trigger them, per the map's maintenance contract. Session 4's authority map close commit was the inaugural test; Session 5 is the first enforcement test.

---

## 9. Other things worth naming

- **Working tree has two pre-existing unrelated mods that have persisted across Sessions 3 and 4.** `skills-experimental/prospect-site-design/LESSONS.md` and `website/next-env.d.ts` — modified, not composer, not committed. Noise in every `git status`. Worth deciding: commit them, revert them, or intentionally carry them. Low priority but clutters the working-tree-clean signal.

- **The skill deploy symlink hasn't been verified this session.** Brain §0 says `~/.claude/skills/prospect-site-composer/` is symlinked from `~/grm-automations/skills-experimental/prospect-site-composer/`. Haven't checked the symlink lives. Session 5 might want to verify before Gate A commits — otherwise authority map + §14 amendments + validator exist in `grm-automations/` but don't propagate to where the skill runs.

- **`[Omitted long matching line]` truncation at composition-plan-schema.md:630.** That was my original audit miss. The tool's truncation hid the 18th typography-patterns.md citation. Worth noting in LESSONS as a pattern about tool-output-truncation drift: when `grep` returns "output too large" and previews are shown, the preview can mislead about completeness. I learned this mid-Session-4; Pattern 4 covered it class-level but the specific lesson (*"when tool output truncates, read the persisted file, don't trust the preview"*) might deserve its own note for future Code windows.

- **Fixture 2's 32-word pullquote is still pending at Checkpoint 2.** Per LESSONS Pattern 5 — if prose drift surfaces and data surfaces should be audited — we should sweep ALL fixture pullquotes for word-count compliance before Checkpoint 2, not just Fixture 2's. Maybe 1-2 other fixtures also carry violations. Would be cheap to pre-audit and avoid a Checkpoint 2 surprise.

- **Claude-mem observation:** the handoff says "claude-mem layer active — you carry persistent memory across sessions." That framing assumed claude-mem was being actively written by Sessions 1-4. I honestly don't know if that's been happening — I've been using auto-memory (MEMORY.md) and commit history as my institutional memory, not claude-mem observations. Session 5 Code opening might want to explicitly check that claude-mem has actual prior-session data, not assume. If it's empty, claude-mem is just framing not substance and the handoff should acknowledge.

---

## What I'd actually do at Session 5 open if I were driving

Open → orient against brain + authority map + backlog + Gate A halt state (20 min).

First beat: paste kitchen-table routing to Design. Design authors Path 4 per F4 split (my strong lean). Chat-Claude drafts retrofit prompt (1 hour if Path 4, 2-3 hours if Path 2).

Retrofit commits: Code runs 58-occurrence regex + §5.3.4:429 correction + fixture parse check. Two commits. Validator re-runs self-check clean.

Close-out commits: brain block + Pattern 5. Two commits.

LLM mechanism decision (flag Option 4 possibility to Chat-Claude before locking Option 1).

Gate A commits at `scripts/fixture_validator.py`. One commit. Authority map Concept 43 updates atomically.

**Close Session 5 here.** 5-7 commits. Maybe 3-4 hours of real work. Session 5 ends with Gate A green.

Session 6 opens for Gate B-F + Checkpoint 2 with a resolved LLM mechanism, a clean working tree, and the authority map reflecting Pattern 5 + whatever kitchen-table touched.

That's probably 20% less scope than Shape A contemplates, but it's the scope where halt conditions surface early and cheap. Right-over-fast at the scope level.

---

I'll stop here. Happy to go deeper on any of these — the LLM mechanism Option 4 especially deserves more treatment if Ron wants it, and the schema-fixture parse check is a concrete small thing I could draft. Your call.

# Composer Session 4 — Brain session block (v2, post-Code-audit integration)

**For:** COMPOSER_BRAIN.md PART II — LIVING. Prepend this block at the top of PART II, above the 2026-04-22 Session 3 close block, per PART II's newest-first convention.

**Commit message when landed in Session 5:** `composer: session 4 close — brain session block for 2026-04-23 full-day Session 4`

**v2 note:** Updated after Code's Session 4 close audit. Three changes: (1) "What's next" LLM invocation framing corrected to name Option 4 alongside Option 1 and Ron's execution-surface call as deciding question, not Chat-Claude's Option-1 lean; (2) Acknowledgments section adds Code audit contribution with specific naming of what the audit caught and reframed; (3) Known traps references the full seven-pattern LESSONS set (Pattern 5 landed Session 4 close; Patterns 6 and 7 authored by Code's audit).

---

## Session block — 2026-04-23 (full day — Session 4 spec-reshape arc + Gate A halt on kitchen-table drift + Code close-out audit)

**Window type:** Chat-Claude (CTO seat), full three-party session with Design and Code. ~11 hours plus Code close-out audit. Ron drove CTO-over-Chat across the full arc.

**Session arc:**

- Opened against Session 3 close handoff (COMPOSER_SESSION_4_HANDOFF.md). Target: finish the skill — Phase 4-new Gates A-F + Checkpoint 2 + Phase 5-new scoping.
- Opening Code check-in surfaced Concern 1 pre-execution: §14 as committed in `4c117cb` read two-pass; Q2 close had moved the contract to three-pass; implementation prompt carried three-pass; spec and prompt contradicted. Routed to Design.
- Design authored three-pass contract amendment for §14. First draft drifted on intent-spec field list (listed fixture-side authoring slots, not the on-disk six). Chat-Claude flagged drift; Design re-authored against on-disk §14.
- Concerns 2 + 3 + 4 surfaced in sequence: emotional-arc.md bias table "Rescue-ready" row label needed enum alias for machine lookup (Concern 2); Rule 1-6 mechanics live in implementation prompt not schema §14 (Concern 3, Path B deferred Path A); §7 voice-zone vocabulary authored at section-level, fixtures authored at section-subpart (Concern 4, two-level vocabulary + fixture retrofit).
- Concern 4 initial reshape: Design authored §14 three-pass migration including Rule 4 amendment but drifted on Rules 1/2/5 (referenced non-existent §2.4 tier contract, `pagePath/assetPath/fragmentConvention` fields not on disk, `tight/standard/expansive` scale enum not on disk). Code's pre-commit diagnostic caught divergence against on-disk §2.2 pathConvention, SKILL.md tier enums (Premium/Professional/Standard), and §4.10 scaleContrast emission shape. Chat-Claude routed diff back to Design.
- Root cause diagnosed: Chat-Claude routed to Design from summary rather than on-disk text. Design authored against summary. Summary's gaps became migration's gaps. Both parties named the pattern — Design's Note 3 working-style posture ("when a reshape touches Rule mechanics, §2 field shapes, §4 emission shapes, or SKILL.md tier enums, I should see the actual lines before authoring") + Chat-Claude's symmetric commitment (route with on-disk text, not summary, on mechanics questions).
- Design Option B call on Rules 1-6: mechanics stay in implementation prompt, §14 names the contract; Path A migration deferred to future session with Rule 4 as template shape. Preserves current architecture while closing drift surface.
- Concern 5 surfaced — Chat-Claude's recognition that three partial-surface errors in one session (the Rule 1-6 migration, the "§5 numbering dissolved" generalization about whole typography.md, and the third error landed later in the kitchen-table Gate A halt) meant the Composer spec needed an authority map artifact to prevent Drift's recurrence.
- Ron's "right over fast" call: press through to Phase 4-new, or author the authority map first. Ron chose authority map.
- Code ran 43-concept read-only diagnostic against disk. Chat-Claude synthesized the authority map from Code's raw material. Design reviewed 43 entries and signed off with four entry-level reshapes (multi-touch Last touched format with History sub-line, Concept 29 ambiguous→flagged, Concept 19 flagged→deferred, Concept 34 flag note sharpening). Authority map landed at `references/authority-map.md` (commit `9ebeced`).
- Phase 4-new execution opened. Code executed Gate A validator implementation (pure Python, 532 lines). Self-check ran against all 6 fixtures. **STOP CONDITION**: 5 of 6 fixtures failed Rule 4 voice-zone validation — 58 `kitchen-table` occurrences in inline `voiceZoneAssignments` across fixtures F1/F2/F3/F5/F6. F4 (urgent-service) alone was clean.
- Root cause: Session 4 Commit 3 (`288946a`, Item 4) fixed one surface visible in schema §5.3.4:429 prose where `kitchen-table` appeared as a default voice for modern-specialist/quiet-confidence `about-page-body`. The fix renamed that single prose occurrence to `closing-table`. The fix assumed kitchen-table was localized to that line. It wasn't. 58 occurrences lived in fixture data across 5 fixtures. LESSONS Pattern 4 (partial-surface reads don't license whole-file generalizations) validated itself two commits after being written down.
- Gate A halted. Code's validator implementation sits at `scripts/fixture_validator.py` untracked on disk, working code, ready to commit once kitchen-table resolves.
- Code ran Path 4 audit diagnostic (voice-tagged fixture slices + voiceMap.md §4 Voice 4 and Voice 5 full text + F4 per-zone voice matrix). F4 emerges as Rosetta Stone — F4 uses `closing-table` for headings and `saturday-morning` for body/attribution in exactly the zones F1/F2/F3/F5/F6 tag `kitchen-table`. kitchen-table does NOT alias to a single canonical voice — it splits across two depending on zone type. Resolution path: either Path 2 (admit kitchen-table as fourth voice with authored tonality) or Path 4 (per-zone retrofit using F4's split as rule template).
- Session 4 close called at Gate A halt + Path 4 audit completion.
- **Code close-out audit (NEW at Session 4 close, standing discipline going forward):** Ron prompted Code for perspective on the three-party working relationship and the close-out artifacts. First time in four sessions Code was asked to reflect rather than execute. Code's audit materially reframed Session 5 opening — named Chat-Claude as primary drift source directly (not buried in acknowledgments), surfaced Option 4 for LLM invocation mechanism (missed in v1 handoff), named Patterns 6 (triad lenses) and 7 (scope right-over-fast) as unnamed patterns, reframed "friction is productive" with cost-alongside-benefit honesty, reframed halts-as-discipline as halts-as-backstop-symptom, recommended Shape B (close at Gate A re-run) as Session 5 scope rather than Shape A (full execution). Chat-Claude integrated audit feedback into handoff v2, opening prompts v2, LESSONS addition (Patterns 5+6+7 instead of just Pattern 5). Standing invitation for Code close-out reflection adopted as discipline going forward.
- Handoff for Session 5 opens with on-disk audit evidence in hand plus Code's close-out audit as institutional instrument.

**What changed on disk:**

- §14 three-pass validator contract amended from Q2 close two-pass (commit `4c117cb`)
- emotional-arc.md bias table "Rescue-ready" row labeled with `(urgent-service)` enum alias (commit `de32fc2`)
- composition-plan-schema.md §7 voice-zone vocabulary reshaped to two-level (section-level 15-key + section-subpart 13-key) with subpart→section flatten mapping table (commit `1c5379b`)
- Six fixture composition-plan.json files retrofitted for -slot disambiguation on three keys (commit `3d7a51f`)
- voiceMap.md verification pass (empty commit, no-op) (commit `428c8bf`)
- Backlog entry: fixture-side authoring slots as §2 candidate (deferred) (commit `081b1bf`)
- Backlog entry: LESSONS cross-grain reconciliation + summary-vs-disk working-style (commit `2bb6a0b`)
- Backlog entry: Path A Rule 1-6 mechanics migration deferred with Rule 4 template preserved (commit `a35b96f`)
- emotional-arc.md gained "Italic word-class vocabulary (persona-indexed)" subsection (canonical home for 4-value enum {place, name, tenure, trade-term}) + schema §5.3.4 cross-reference + typography.md §15 Check 9 enum update (commit `03ca705`)
- emotional-arc.md gained "Micro-interaction duration lock (persona-indexed)" subsection (canonical two-row table) + css-framework.md cross-reference + SKILL.md discoverability pointer (commit `35343c7`)
- composition-plan-schema.md §5.3.4:429 kitchen-table→closing-table surface fix with §4.2 + voiceMap.md citation nit (commit `288946a`) — **SUPERSEDED PARTIALLY by kitchen-table drift discovery at Gate A; §5.3.4:429 may need correction pending Session 5 Path decision**
- typography-patterns.md → typography.md global citation rename across 17 live citations (14 clean + 2 Rule 1/Rule 2 semantic replacements + 1 Rule 4 specific-citation replacement) (commit `94c6acf`)
- Session 4 LESSONS update with Pattern 4 (partial-surface reads) + Concern 5 Items 1-4 marked Resolved (commit `4696af0`)
- Authority map landed at `references/authority-map.md` — 43 concepts, four-value flag taxonomy (clean/flagged/ambiguous/deferred), atomic-update maintenance contract (commit `9ebeced`)

**Full Session 4 commit range:** `0a39489..9ebeced` = 14 commits, all pushed to origin/main.

**What's in-flight:**

- `scripts/fixture_validator.py` — Code's Gate A validator implementation. 532 lines, three-pass contract, all six semantic-derivation rules, editorial-adherence pass. Untracked on disk. Working code. Ready to commit once kitchen-table resolves.

**What's next (Session 5 opens with):**

1. **Kitchen-table resolution.** Design reviews Code's Path 4 audit evidence (F4 Rosetta Stone pattern + fixture copy slices + voiceMap.md §4 Voice 4/5 verbatim) PLUS Code's Session 4 close audit technical framing (Path 2 Phase 6 Check 12 CSS register blocker; F3 post-retrofit two-voice build as Path 4 risk to confirm; Path 2 concession rides with Path 4). Design authors Path 2 (admit kitchen-table as 4th voice with tonality definition) or Path 4 (per-zone retrofit using F4's pattern as rule template). Session 5 first-beat prompt (on Desktop as `Composer_Session_5_First_Beat_Kitchen_Table.md` v2) gives Design evidence + Code's sharper technical read pre-packaged.

2. **Schema §5.3.4:429 re-check.** Session 4 Item 4 fix landed `closing-table` for modern-specialist/quiet-confidence about-page-body. Kitchen-table audit evidence suggests that may have been the wrong resolution — F4 uses `saturday-morning` for about-page-body zones. Design's Path call triggers re-evaluation of this line.

3. **LLM invocation mechanism for Gates B-F (OPEN ARCHITECTURAL QUESTION for Ron).** Code's Session 4 close audit surfaced that Chat-Claude's v1 framing (SDK-vs-subprocess-vs-prompt-file, Chat-Claude-leans-Option-1) missed Option 4 — Phase 4-new emits editorial-authoring stubs, Claude Code orchestrating session authors them inline. This matches how existing Claude Code skills typically work. The question that decides Option 1 vs Option 4: Composer's intended execution surface. Interactive-only via `/prospect-site-composer URL` command in Claude Code → Option 4 cleaner (no SDK dep, no API key management). Standalone-capable (scheduled task, client team automation, overnight pipeline) → Option 1 necessary. **Ron's strategic call at Session 5 open.** Chat-Claude + Code implement the decided option in Session 6 for Gates B-F.

4. **Gate A re-run.** After kitchen-table retrofit lands, Code re-runs validator self-check against all 6 fixtures. Expected clean. Gate A commits.

5. **Gates B-F execute** in sequence with LLM invocation mechanism specified (Option 1 or Option 4 per Ron's execution-surface call). Gate E triggers Checkpoint 2 (Design reviews 2-3 Phase 4-new outputs — Fixtures 2/3/4 anchor set). Post-sign-off, Stage IV Phase 5-new scoping opens.

**Open questions / deferred decisions:**

- Kitchen-table Path 2 vs Path 4 (Session 5 first beat)
- Schema §5.3.4:429 correction (tied to Path call)
- LLM invocation mechanism — Option 1 (SDK) vs Option 4 (orchestrator-authors) — Ron's execution-surface call
- Composer's intended execution surface — interactive-only vs standalone-capable — Ron strategic call
- Phase 5-new scoping (Stage IV) — opens post-Checkpoint 2
- Fixture 2 pullquote retrofit-or-grandfather (Checkpoint 2, deferred from Session 3)
- Two pre-existing unrelated working-tree mods (`prospect-site-design/LESSONS.md`, `website/next-env.d.ts`) persisting across Sessions 3-4 — Ron decides commit/revert/carry at Session 5 open
- Skill deploy symlink verification (`~/.claude/skills/prospect-site-composer/` → `~/grm-automations/skills-experimental/prospect-site-composer/`) — run `ls -la` at Session 5 open
- claude-mem persistent memory verification — was Sessions 1-4 actively writing observations, or is "claude-mem active" framing without substance

**Known traps for Session 5:**

- Patterns 4 and 5 validated themselves at scale (58 kitchen-table occurrences). Next partial-surface error will have similar or larger consequences. Both Design and Chat-Claude now have explicit working-style postures to guard against it — on-disk text before authoring mechanics, audit underlying data surfaces when spec drift surfaces in prose.
- **Pattern 6 (triad lenses) applies to Session 5 retrofit decisions.** Any kitchen-table resolution touching structural authority (schema §4.2 enum, voiceMap.md §3 voice count, authority map Concept 10) needs Design + Chat-Claude + Code all three before close. Pairs produce drift; triads catch it.
- **Pattern 7 (scope right-over-fast) applies to Session 5 close timing.** Shape B (close at Gate A re-run) is the recommended scope. Shape A (Gates A-F + Checkpoint 2) repeats Session 4's aggressive-scope pattern. Scope contracts at session open make this enforceable.
- The 58-occurrence kitchen-table drift is a pre-Stage-II-(d)-merge authoring residue. Pre-merge state was apparently a 4-voice framework; Stage II (d) merge locked 3 voices; fixtures didn't get the update. This is structurally similar to the §7 section-level vs section-subpart drift from earlier in Session 4 — spec authored at one state, fixtures authored at another, gap sat unexercised until Gate A tried to validate against both. LESSONS Pattern 1 (cross-grain reconciliation needs a dedicated checkpoint beat) applies with equal force to cross-state drift.
- If Path 2 lands, it's a genuine spec expansion (voice enum from 3 to 4), not a retrofit. Authority map Concept 10 canonical home reshapes; voiceMap.md §3 in-scope voice count changes; schema §4.2 enum expands. Plus Path 2 hides technical blocker at Phase 6 Check 12 CSS register level that Code's audit named — fourth voice at composition-plan level doesn't automatically add a fourth CSS register; either Path 2 aliases to existing register (which makes it Path 4 in disguise) or Path 2 also needs fourth role-class set + Check 12 rewrite. Material spec work.
- If Path 4 lands, it's a mechanical retrofit driven by F4's pattern. Risk Code's audit flagged: F3 (modern-specialist) becomes a two-voice build post-retrofit (closing-table + saturday-morning, no front-porch). Matches modern-specialist's emotional-arc profile but Design should confirm editorially.
- LLM invocation mechanism is NOT purely implementation architecture — it's Ron's strategic call on Composer's execution surface. Don't resolve at Chat-Claude + Code level without Ron's answer on interactive-only vs standalone-capable.
- Session 5 opens with material on-disk ground truth: authority map exists, fixture audit exists, Code's validator implementation exists, Code's close-out audit exists as institutional instrument. Lean on these rather than reconstructing from summary.

**Acknowledgments:**

- Ron held CTO-over-Chat across 11 hours of spec-reshape work, arbitrated seven architectural reframes cleanly (§14 contract, emotional-arc aliases, Rule 1-6 Path B deferral, §7 vocabulary, authority map scope, Gate A halt, Session 4 close timing), pushed back on Chat-Claude's framing when Chat-Claude was over-indexing on capacity vs. judgment, and chose "right over fast" at the authority map decision point. Right-over-fast got materially vindicated by the kitchen-table drift discovery — pressing through without the authority map would have compounded the error. Ron also caught the structural gap that Code had never been invited to reflect on the three-party relationship; his prompt for Code's close-out audit produced institutional instrument that reframed Session 5 opening materially.
- Design delivered substantive architectural authorship across four reshapes — §14 three-pass migration, §7 two-level vocabulary, Rule 4 template, authority map four-reshape polish. Design's Note 3 working-style posture (on-disk text before authoring mechanics) emerged from Session 4's drift pattern and now governs both parties going forward.
- Code caught six framework-level concerns across Session 4 at pre-commit verification preventing architectural drift: §14 three-pass contract contradiction, §7 vocabulary grain mismatch, Rule 1/2/5 on-disk divergence, §2.1:67 Rule 4 semantic mismatch, §5.3.4:630 historical-provenance vs live citation distinction, kitchen-table 58-occurrence fixture drift at Gate A. The halt-don't-press-through discipline is load-bearing. Code also executed the first close-out audit in Session 4 final hour — audit named Chat-Claude as primary drift source with directness that v1 handoff had buried; surfaced Option 4 for LLM invocation mechanism that Chat-Claude's SDK-only framing had missed; identified Patterns 6 (triad lenses) and 7 (scope right-over-fast) as unnamed patterns; reframed "friction is productive" with cost-alongside-benefit honesty; reframed halts as backstop-symptom rather than earned-discipline; recommended Shape B for Session 5 scope. Standing discipline for Code close-out reflection adopted going forward.
- Chat-Claude's drafting drift at context-pressure points (three partial-surface errors — Rule 1-6 migration, §5 numbering generalization, kitchen-table surface-fix assumption) cost round-trips. LESSONS Pattern 4 added at Session 4 mid-session; Patterns 5 (surface-level fixes don't license localized-drift assumption), 6 (triad lenses), 7 (scope right-over-fast) added at Session 4 close via Code's audit. Symmetric working-style posture to Design's Note 3 adopted: on-disk text before routing mechanics questions. Chat-Claude also integrated Code's close-out audit into Session 5 artifacts — handoff v2, opening prompts v2, LESSONS Patterns 5+6+7 together — before Session 4 closed. Session 4's close-out discipline was itself the first test of the new standing practice.

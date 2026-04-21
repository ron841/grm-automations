# Composer Stage II typography source material

This directory holds the source material for Composer's Stage II (d) typography merge. Two in-flight reference files that merge into production-sourced `typography.md` and `voiceMap.md` via the three-way diff procedure specified in the Composer spec.

If you are a fresh Claude Code window landing here cold, this README is enough context to execute the merge. You do not need to read the full Composer spec first — but the Composer spec is the authoritative source on procedure (Stage II (d)) and on risk mitigation (§10 Risk 1).

---

## What's in this directory

- `typography-patterns.md` — Design's v0.7.2 in-flight typography authority. Successor to production's `typography.md`. Three-voice type system (`--font-display` / `--font-body` / `--font-data`), persona-conditional font tables, italic-selection heuristic, pull-quote detection rules, stats-watermark consistency check, mobile watermark breakpoint, nine Phase 5 deployment rules, thirteen Phase 6 verification checks.
- `voiceMap.md` — Design's v0.7.2 in-flight voice map. Successor to production's `voiceMap.md`. Three-persona × three-voice matrix (Closing Table / Saturday Morning / Front Porch per persona), voice-selection heuristic per section type, banned-phrase list per voice.
- `README.md` — this file.

---

## Provenance

Both files were authored by Design (Chat-Claude working on editorial framework) during the v0.7.2 paused-rebuild window on 2026-04-21. The authoring was paused mid-stream when Composer scoping superseded the v0.7.2 point release. The files are complete as authored — they do not need Design revisions before merge. They are staged here because Composer's Stage II (d) requires them at a canonical disk path for the three-way diff merge procedure.

**What Design had in view when authoring:**
- Luna F8 findings from 2026-04-20/21, specifically: the "04, 02, 03, 04" stats watermark numbering bug, italic hero-only deployment (should be 2-3 per page), "Tell us" weak italic-word selection, logo sizing class of bug, reveal-animation class of bug, mobile promo-bar overlap.
- T&F and prior flagship findings on scale contrast, motion restraint, and signature micro-interaction discipline.
- The five persona system from `emotional-arc.md` (Quiet confidence, Earned pride, Neighborhood steady, Rescue-ready, Modern specialist) as the framing layer for both typography and voice decisions.

**What Design did NOT have in view:**
- Production's Q1/Q2/Q3 revision rounds of `typography.md` and `voiceMap.md`. These revisions happened without Design in the loop.
- Wave 2 retrofits landing in production on 2026-04-20 (SectionOpener, StatRow, rhythm tokens, `--font-mono` token, JetBrains Mono preload). Some of these touched `typography.md` and `voiceMap.md`.

The three-way diff procedure exists specifically to reconcile this gap.

---

## Three-way diff merge procedure (Stage II (d))

Composer spec §8 Stage II (d) and §10 Risk 1 are the authoritative source. Summarized here for directory self-containment:

1. **Three files enter the merge:**
   - (A) **Production baseline** — `~/.claude/skills/prospect-site-design/references/typography.md` (and same for `voiceMap.md`) after Stage II (a) file copies from production prospect-site into design-skill. This carries F5-era authoring plus Q1/Q2/Q3 revisions plus Wave 2 retrofits.
   - (B) **Design in-flight** — `typography-patterns.md` and `voiceMap.md` from this directory. Design's v0.7.2 authoring.
   - (C) **Proposed merge output** — new file authored by Code (or Chat-Claude) reconciling A and B.

2. **Default tie-breakers** (Design-specified during Stage I review):
   - Production wins on *wording* where Ron has already signed off on specific language. If production's `typography.md` has a sentence that Q3 revised to specific wording, that wording carries forward.
   - Design in-flight wins on *structure* (three-voice vs. two-voice token system, persona tables, new rules, new Phase 5/6 checks). Structural revisions supersede production's structure.
   - Where production has a token name or selector that Design's in-flight file doesn't reference but downstream files depend on, **preserve the token**. Document it in the merged file's revision log.

3. **Conflict surfacing.** If a sentence in production contradicts a structural revision in Design in-flight — for example, production says "two-voice system" and Design in-flight says "three-voice system" — this is not a tie-breaker case, it's a conflict. Do not silently resolve. Surface the conflict to Design via Chat-Claude for a judgment call. Composer spec §10 Risk 1 names this explicitly.

4. **Merge output writes to design-skill.** Final merged `typography.md` lands at `~/.claude/skills/prospect-site-design/references/typography.md`, replacing the production-copied baseline from Stage II (a). Same for `voiceMap.md`. The files in this directory stay as archival source and are not deleted.

5. **Revision log.** Append a merge-completion entry to the merged file's frontmatter: date, merge source (production baseline Q-revision + Design in-flight v0.7.2), conflict list resolved, Design reviewer signoff.

---

## What NOT to do

- **Do not rename `typography-patterns.md` to `typography.md` and copy it directly into design-skill**, skipping the merge. This loses production's Q1/Q2/Q3 revision language.
- **Do not treat these files as new additions** to design-skill (i.e., keep them alongside production's `typography.md` and `voiceMap.md` without merging). This creates two overlapping authority files in the same directory and Phase 5 will not know which to read.
- **Do not revise `typography-patterns.md` or `voiceMap.md` in this directory** as a way of resolving merge conflicts. These files are frozen as archival source. Revisions happen in the merged output at design-skill, not here.

---

## If you hit a merge conflict

Loop Chat-Claude (Design-facing) or Ron. Surface the conflict list with:

- File and section
- Production baseline wording
- Design in-flight wording
- Which tie-breaker category you think applies (wording / structure / token-preservation / genuine conflict)
- Your proposed resolution if you have one, or "needs Design judgment" if not

Do not ship a merge commit with unresolved conflicts. §10 Risk 1 mitigation is explicit on this: "Code surfaces conflict list before merge commit. Design reviews conflicts."

---

## Cross-references

- Composer spec §5 — lists these files as Stage II (d) source material.
- Composer spec §8 Stage II (d) — the merge procedure anchor.
- Composer spec §10 Risk 1 — the three-way diff risk mitigation this directory implements.
- `COMPOSER_BRAIN.md` (wherever Ron packages it) — higher-level Stage I orientation for Claude Code windows.

---

## Version

Directory v1.0, established 2026-04-21 during Composer Stage I scoping lock. Files frozen as archival source for Stage II (d) merge. Design signoff on readiness: confirmed 2026-04-21.

# Composer Backlog

Deferred work items surfaced during Composer development but held out of
their originating commits for scope/timing reasons. Living document.

Format: item + originating commit + reasoning for defer + target stage/
trigger for pickup.

## Active deferrals

### scale-architecture.md structural rewrite
- **Surfaced:** Stratum 3 identity sweep, 2026-04-21 (commit 5b2d650).
- **Why deferred:** 70+ v0.7/v0.8/v0.9/v1.0 references serve as section
  headers, stage gates, and trigger conditions. File is structurally a
  roadmap document, not a technical spec. Surface-level token swaps
  leave it semantically broken. Proper rewrite requires:
  - Reframe "v0.7 (current)" sections as "Composer (current)"
  - Reframe "v0.8 (automation of pain)" as "v0.8 Scale (deferred)"
  - Revisit Path A (lifestyle) / Path B (scale) decision tree in light
    of Composer as its own path
  - Evaluate whether the "files locked at v0.7" registry section should
    be deleted under Composer's formalized handoff contract per brain §4
- **Target pickup:** After Stage II (a) file copies + Stage II (d)
  typography merge land. By then the brain file's post-Composer roadmap
  vocabulary (§0) has full context from the merged files, and the Composer
  ↔ Scale boundary is concretely expressed in multiple places. Single
  dedicated commit.

### Content enlargement: SKILL.md lines 473 and 493
- **Surfaced:** SKILL.md body identity sweep, 2026-04-21 (commit 6c13f4f).
- **Why deferred:** Brain file §9 (Approval Gate UI, Phase 4) and §6
  P6.2 (13-check editorial suite) expand the content these sections
  describe. Version-tag drop was in-scope for identity sweep; content
  enlargement is Stage III/IV (Phase 4-new + Phase 5-new implementation)
  scope.
- **Target pickup:** Stage III (Phase 4-new) for line 473 approval gate
  UI; Stage IV (Phase 5-new) for line 493 editorial rules enumeration.

### SKILL.md Changelog section
- **Surfaced:** SKILL.md body identity sweep, 2026-04-21 (commit 6c13f4f).
- **Why deferred:** Design-skill stripped production's Changelog section
  during its install. Composer inherits the stripped tail. Composer
  deserves its own Changelog starting with Stage II entries. Net-new
  section to author, not an identity-drop pass.
- **Target pickup:** After Stage II (d) typography merge lands — once
  the substantive reference-file changes are in, seed the Changelog
  with a consolidated Stage II entry pointing at the stage-gate commit
  hashes.

### LESSONS.md entry format normalization
- **Surfaced:** LESSONS.md merge, 2026-04-21 (commit 1ef0f16).
- **Why deferred:** Appended entries across April 13–April 21 use three
  different formats: (a) full template with Source/Severity/Assumption/
  What happened/Lesson/Fix/Affected files, (b) loose paragraphs (April
  15 A-1 Payless entries), (c) hybrid with Source+Severity headers but
  different body sub-headings (April 16 Grandview entries), (d)
  ## section with ### sub-entries (April 21 Luna). Normalization to the
  11-seed-entry template would improve readability but is a distinct
  logical change from the merge.
- **Target pickup:** Opportunistic. Can be done any time post-Stage II.
  Not blocking.

### LESSONS.md v0.7/v0.8 identity language in Luna section
- **Surfaced:** LESSONS.md merge, 2026-04-21 (commit 1ef0f16).
- **Why deferred:** Luna section heading carries "(v0.7)" parenthetical
  (line 480 in merged file); multiple Luna sub-entries say "Action for
  v0.8: ..." (lines 492, 500, 514 in merged file). Both references
  are factually accurate historical markers (Luna F8 was design-skill-era
  v0.7-derived; "v0.8" in those entries referred to the original v0.8
  scope that is now v0.8 Composer or v0.8 Scale (deferred)). Rewriting
  during merge would bundle two logical changes.
- **Target pickup:** Dedicated identity pass on LESSONS.md, after Stage
  II close-out. Can bundle with the "Action for v0.8" clarification
  (which items are now Composer-Stage commitments vs. v0.8 Scale
  deferred vs. already-resolved in Component A patch inventory §6).

## Resolved deferrals

### LESSONS.md merge (root → references/)
- **Originally surfaced:** Stage II (a) file copies, 2026-04-21 (commit c175551).
- **Resolved:** 2026-04-21 (commit 1ef0f16). Disjoint-tail chronological
  concatenation: shared 349-line core + production's April 13–16 tail +
  Composer root's April 21 Luna tail = 512-line merged file at
  `references/LESSONS.md`. Root LESSONS.md deleted via git rename
  (66% similarity detected). All institutional memory preserved; zero
  dedupe required (tails were fully disjoint).

### handoff-discipline.md identity-language sweep
- **Originally surfaced:** Stage II (a) file copies, 2026-04-21
  (commits c175551 / d680a3d). Surprise #5 in Stage II (a) final report.
- **Resolved:** 2026-04-21 (commit db7dc8d). Diagnostic surfaced just
  one D-classification (load-bearing identity) hit at line 9
  ("prospect-site build flow" → "prospect-site-composer build flow")
  and 16 E-classification (historical narrative) references that were
  preserved as factual production-evolution context. The file is
  fundamentally a meta-document about how production's v0.8 foundation
  round was conducted, so its v0.7/v0.8 references are HISTORICAL
  rather than current-skill self-id.

---

**Convention for this file:**
- Add deferrals as they surface. Include originating commit hash for
  traceability.
- When a deferral is picked up, move it from Active to Resolved, add
  resolution commit hash, and a one-line note on what got done.
- Chat-Claude reviews this file at the start of every Composer session
  to avoid losing track of deferred work across session boundaries.

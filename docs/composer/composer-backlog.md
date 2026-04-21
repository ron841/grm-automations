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

### LESSONS.md merge (root → references/)
- **Surfaced:** Stage II (a) file copies, 2026-04-21 (commit c175551).
- **Why deferred:** Composer has a LESSONS.md at root (385 lines,
  inherited from design-skill install, includes Luna F8 build lessons:
  Vercel SSO PATCH workaround, AI-slop stock imagery rejection,
  DarkVibrant brand-token override insight). Production's
  references/LESSONS.md (473 lines) is the canonical destination per
  brain §8 Stage II (a) but contains its own accumulated tail (Grandview
  brand-mark detection, skill-repo mirror pattern, v0.7.3 hotfix
  lineage). First ~50 lines of both files are byte-identical (shared
  lineage); tails diverged. A naive copy-and-replace would lose 3+
  substantive Luna F8 lessons. Keeping both files creates dual-authority
  confusion at Phase 8 append time.
- **Target pickup:** Single dedicated commit. Walk both file tails
  past the shared-lineage boundary, deduplicate any overlapping
  entries, integrate production's unique tail entries into Composer's
  existing LESSONS.md content, move merged result to
  `references/LESSONS.md` per brain §8, delete root location. Result:
  one canonical LESSONS.md at `references/LESSONS.md` containing both
  design-skill-era and production-era institutional memory.
- **Trigger:** Before Stage II.5 fixtures are authored (Phase 8 append
  semantics need to be unambiguous before the first Composer build runs).

## Resolved deferrals

*(None yet. Items move here with resolution commit hash when picked up.)*

---

**Convention for this file:**
- Add deferrals as they surface. Include originating commit hash for
  traceability.
- When a deferral is picked up, move it from Active to Resolved, add
  resolution commit hash, and a one-line note on what got done.
- Chat-Claude reviews this file at the start of every Composer session
  to avoid losing track of deferred work across session boundaries.

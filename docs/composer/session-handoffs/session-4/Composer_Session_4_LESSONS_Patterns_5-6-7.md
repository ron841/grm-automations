# LESSONS Patterns 5, 6, 7 addition — for composer-backlog.md

**For:** Append to the existing LESSONS entry in composer-backlog.md (the one added in commit `2bb6a0b` and extended with Pattern 4 in commit `4696af0`). Patterns 5, 6, 7 follow Pattern 4 as new bullets inside the same LESSONS entry's body.

**Commit message when landed in Session 5:** `composer: backlog — LESSONS Patterns 5+6+7 (surface-level fix scope, triad lens discipline, narrow scope enforcement)`

**Note:** Pattern 5 was drafted at Session 4 close by Design before Code's close-out audit. Patterns 6 and 7 emerged from Code's audit of Session 4 close artifacts. All three land together as Session 5's first LESSONS commit. Authority map Concept 43 pattern count updates atomically from four to seven.

---

## Pattern 5 text to append (verbatim)

```
- **Surface-level fixes do not license assuming drift is
  localized.** When a drift surfaces in prose or spec,
  audit the underlying data surfaces (fixtures, CSS,
  generated output) before declaring the fix complete.
  Session 4 Item 4 fixed a `kitchen-table` reference at
  schema §5.3.4:429 prose (commit `288946a`) on the
  assumption the drift was localized to that line. It
  wasn't — 58 occurrences lived in fixture data across
  5 of 6 fixtures, discovered at Gate A validator self-
  check (halt before commit `9ebeced+1`). Pattern 4
  (partial-surface reads do not license whole-file
  generalizations) named the error class two commits
  before the Gate A halt validated it at scale. The
  working-style correction: when spec prose is fixed for
  a specific concept drift, immediately audit the data
  surfaces that reference that concept (fixtures,
  downstream specs, generated artifacts) before closing
  the fix as resolved. Applies to Design, Chat-Claude,
  and Code symmetrically.
```

---

## Pattern 6 text to append (verbatim)

```
- **Architectural reshapes need three lenses, not two.**
  Every major Session 4 drift surfaced at the third lens.
  §7 vocabulary reshape was authored Design+Chat-Claude;
  the grain mismatch only surfaced when Code looked at
  fixtures. Rule 1/2/5 migration was authored
  Chat-Claude-summary+Design; the enum drift only
  surfaced when Code looked at schema. Kitchen-table
  Item 4 surface-fix was authored Chat-Claude+Design;
  the 58-occurrence drift only surfaced when Code ran
  the validator. Pairs produce drift; triads catch it.
  The working-style correction: any reshape touching
  structural authority (schema fields, enum values, rule
  mechanics, fixture shape) routes through all three
  parties before close — Design authors editorially,
  Chat-Claude drafts with on-disk text, Code verifies at
  pre-commit. Skipping one lens because a pair thinks
  they have the concept covered is the mechanism by
  which Session 4's seven architectural reframes all
  reached pre-execution. Third lens isn't insurance; it
  is the catch surface the first two cannot provide.
```

---

## Pattern 7 text to append (verbatim)

```
- **Narrow scope surfaces halts earlier when halts are
  cheaper.** Ron applies right-over-fast discipline at
  decision points (authority map pause, kitchen-table
  audit pause) cleanly. Sessions 3, 4, and Session 5's
  v1 handoff scoping got aggressive at the *session* level.
  Session 3 closed Stage II.5 + Gates 1-4 + §14 in one
  day. Session 4 attempted Gate A-F + Checkpoint 2.
  Session 5 v1 framed "finish the skill" scope. Kitchen-
  table drift would have been cheaper to catch if Session
  4 had closed at "Concern 4 reshape + fixtures parse-
  checked" and opened Session 5 for Gate A. The working-
  style correction: scope contracts at session open. Ron
  and Chat-Claude explicitly agree what "successful
  session close" looks like at session open — not "finish
  the skill," but a specific set of commits the session
  lands. Scope contracts make right-over-fast enforceable
  at the session level, not just decision-point level.
  Narrower scope surfaces halts inside the session while
  they are still cheap; aggressive scope pushes halts
  past close where they become cross-session debt.
```

---

## Where this lands

The LESSONS entry in composer-backlog.md's Active section currently carries four patterns (post `4696af0`):

1. Cross-grain reconciliation needs a dedicated checkpoint beat (from `2bb6a0b`)
2. Design asks for on-disk text before authoring mechanics / Chat-Claude routes with disk state not summary (from `2bb6a0b`)
3. Code's halt-don't-press-through discipline is load-bearing (from `2bb6a0b`)
4. Partial-surface reads do not license whole-file generalizations (from `4696af0`)

Patterns 5, 6, 7 land as bullets 5, 6, 7 inside the same entry, following Pattern 4. Same atomic LESSONS observation entry, not a new entry.

Code applies via `str_replace` on the existing Pattern 4 bullet — replace the closing of Pattern 4's block text with Pattern 4's closing + the Pattern 5 text + Pattern 6 text + Pattern 7 text inserted as consecutive bullets.

The session date tag at the end of the entry ("Added 2026-04-23, Session 4") stays as-is; Patterns 5-7 are all Session 4 patterns (Pattern 5 caught at Gate A halt; Patterns 6-7 authored by Code at Session 4 close audit). No date tag update needed.

## Authority map Concept 43 atomic update

Per authority map maintenance contract, when LESSONS pattern count changes, Concept 43's vocabulary line updates atomically. Current Concept 43 reads:

> **Vocabulary:** four patterns accumulated across Sessions 3 and 4 — (1) cross-grain reconciliation needs dedicated checkpoint beat; (2) Design asks for on-disk text before authoring mechanics / Chat-Claude routes with disk state not summary; (3) Code's halt-don't-press-through discipline preserved across gates; (4) partial-surface reads do not license whole-file generalizations

Updates to:

> **Vocabulary:** seven patterns accumulated across Sessions 3 and 4 — (1) cross-grain reconciliation needs dedicated checkpoint beat; (2) Design asks for on-disk text before authoring mechanics / Chat-Claude routes with disk state not summary; (3) Code's halt-don't-press-through discipline preserved across gates; (4) partial-surface reads do not license whole-file generalizations; (5) surface-level fixes do not license assuming drift is localized; (6) architectural reshapes need three lenses not two; (7) narrow scope surfaces halts earlier when halts are cheaper

And Concept 43's Last touched updates to: `Session 5, commit [new hash] (Patterns 5+6+7 added)`.

Both the LESSONS entry update and the Concept 43 update land in the same atomic commit.

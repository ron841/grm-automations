# Code-layer observations — 2026-04-16 session

Observations from the execution layer after a ~10-hour sustained session: morning skill patches (Bugs 2/4/5), afternoon Grandview F4 build, evening v0.7.3 ship (9 commits, 3 batches), four-site retrofit, F3 a11y fix, content audit. Not covered elsewhere in tonight's write-ups.

---

## a) Tool-use patterns

**Repeated three-call idiom that ran ~11 times tonight.** The shape: `Read` target area → `Edit` → `Bash git add / git commit / git log -1 --oneline`. Ran once per v0.7.3 commit. Efficient because each iteration's confirmation fed the next batch's pre-flight. Would not have batched — the atomic-commit structure was the point.

**Read-before-Edit friction on the same file repeatedly.** Edit requires reading first, and my context doesn't always remember that I read SKILL.md ten minutes ago. Several Edit attempts tonight errored out with "File has not been read yet" and required a follow-up Read. Examples: SKILL.md re-edited in Batches A/B/C (four of the nine commits touch SKILL.md), each transition needed a fresh Read. Not harmful, but adds round-trips.

**Grep → Read → Edit triad was the workhorse of verification.** Pattern: `grep -n "target pattern" file` to find exact line numbers, `Read` with `offset`/`limit` to confirm surrounding context matches spec expectations, `Edit` with wide-enough `old_string` to disambiguate. This pattern ran for every commit in Batches A/B/C1 and caught real structural drift twice (F3 had no `prefers-reduced-motion` block at all; Phase 2 had 5 steps not 4 in the Batch C1 renumber).

**Rsync + single-file commit + push was the fastest step of the night.** Each preservation/mirror cycle: rsync `<200ms>`, git add `<100ms>`, git commit `<500ms>`, git push `~3s`. Cost of the preservation pattern is negligible. This justifies doing it more often, not less.

**Could have been batched but wasn't: per-site live-verification curls.** For F1/F2/F3/F4 retrofits, I ran four separate bash blocks for live verification instead of one templated loop. Not harmful (each site needed its own eye-test pause), but if Ron ever asks for bulk retrofit with no per-site pause, a single loop over all four URLs would cut 4× network round-trips to 1.

**Skipped but shouldn't have: observation-layer diagnostic early.** I only noticed claude-mem had zero observations during the end-of-day audit (Layer 1 of the audit request). A `list_corpora` + sample-observations check at session start would have caught it 10+ hours earlier. Worth adding to morning setup.

---

## b) Pre-edit verification — catch vs. ceremony

**Caught real drift:**

- **Batch A commit #2** — spec assumed `section-patterns.md` had a canonical `<head>` template. Grep found 2 references to injecting things into `<head>` but no canonical template. Verification caught a wrong-premise step before I authored against nothing.
- **Batch C1 Phase 2 step numbering** — spec said "renumber step 5 to step 7, insert broken-link as new 6." Read of the pre-existing Phase 2 showed step 4 was already "save to draft" (not absent as spec assumed). Final numbering was 5/6, not 6/7.
- **F3 retrofit** — spec predicted "v0.7.2-era builds inherit the footer-logo filter." Grep showed F1/F2/F3 all had zero `brightness(0)` hits. Only F4 had the filter. Verification overturned a false premise.
- **F4 retrofit** — verification caught that F4's tonight-build had inline-patched the bug with `.js` (class selector) instead of `html.js` (spec pattern) + the classList.add was inside external `script.js` (FOUC-causing) instead of inline `<head>` (synchronous). Normalization pass was driven entirely by this verification step.

**Ceremony:**

- **Batches B commits #3/#4** — verifying "Corporate jargon section ends around line 138 and CTA trailing-fragment begins around 140" on files that hadn't been touched since `7227ff8`. Zero drift risk. Still worth doing for cost-of-insurance reasons, but 0% catch rate across both checks.
- **Phase 6 count sentence re-verification** in Batch C2 — "nine categories" check ran at pre-flight even though Batch B's commit had set it and nothing had touched Phase 6 since. Low catch odds.

**Honest ratio:** about 40% genuine catch, 60% ceremony by count. But the catches were all high-severity (would have produced broken commits or bad output). Ceremony runs are cheap — ~5 seconds each. Keep both.

---

## c) Drafting-vs-execution state drift

Smaller patterns that didn't rise to session-stop level but are worth flagging:

**URL / hostname convention drift (surfaced at F1 retrofit).** Retrofit spec assumed `tandf-electric.vercel.app`. Actual live URL was `tandf-electric-v07.vercel.app`. Similarly, local dir was `tandf-electric-v07/`, not `tandf-electric/`. F2 had a similar miss: spec path was `a-1-payless-septic/`, actual was `a-1-payless-septic-service-inc/`. Drafting layer assumed a naming convention; execution found the actual names by `ls`.

**Partial-truth assumptions in specs.** Multiple tonight-spec examples where Opus's spec was truthful about *what exists on disk* but incomplete about *what state it's in*:
- v0.7.3-spec.md: on disk = truthful; implementation history = "already reverted" (not stated in spec; caught only by git-log recon).
- F4's inline patch from the build session: spec said "likely already fixed"; reality was "fixed with a divergent pattern that would have failed strict-uniformity checks."
- claude-mem status: "available" = true; "capturing observations" = false. Drafting assumed working; execution found it empty.

**Numbered-list assumptions.** Twice tonight, specs instructed "insert step N, renumber step N+1 to step N+2" based on an assumed step count. Actual step counts differed both times (Phase 2 in Batch C1; the Phase 6 check-18 collision in the v0.7.3-spec.md from April 13). Fix: whenever drafts do renumbering, include a "verify the current step count first" instruction — which tonight's Batch C1 spec did explicitly, and which caught the mismatch.

**Truncation at message boundaries.** Two specs arrived truncated at paste boundaries: Batch C2 (cut at "profile.json unknownFields[] + a") and Step 2 of F3 a11y (cut at "Place it immediately"). Execution layer's correct move in both cases was to stop and request resend. Truncations at multi-thousand-character specs are predictable enough that drafts could build in natural chunk boundaries (i.e., draft the multi-step spec as multiple messages from the start, rather than hoping one big paste survives).

---

## d) Three-layer relay under sustained load

**Where it held up:**

- **Atomic commit discipline across 3 batches + 9 commits.** Every batch's final report included the exact SHAs it produced. Next batch's spec opened with "Verified SHAs to reference." This is a typed handoff between stages. Zero SHA drift across the 9-commit sequence — every reference was correct when it landed in the next batch's opening matter.
- **Read-only recon steps as a hinge.** Prompts #30 and #34 (read-only inventory + ground-truth recon) were the highest-leverage prompts of the night. They converted Opus's assumed state into execution-verified state before any edit began. If I had to reduce the session to its three most important prompts, those two and the Phase 1 Grandview palette-override prompt would be the set.
- **Stop-and-report protocol.** Tonight had 3 stop-and-report moments: F1 URL mismatch, Batch C2 truncation, F3 a11y spec truncation. All three were caught cleanly without material loss. The cost of stopping was ~30 seconds of round-trip; the cost of proceeding-anyway in any of them would have been a mislabeled commit or a misapplied patch.

**Where it strained:**

- **Context decay between drafts and execution.** Opus's drafts are written from their context, which may be hours behind execution's current state. Tonight this showed up in stale SHA references (caught), stale path assumptions (caught), and in the drafting layer not seeing that I had flagged F4's divergent pattern until I surfaced it inside the batch.
- **Asymmetric verification speed.** Execution runs verifications in seconds via grep/curl. Drafting's verification happens when Opus reads the next Ron-relayed output — which can lag by minutes. During a 3-batch sequence tonight, that lag put drafting's picture of HEAD one or two commits behind execution's HEAD at various moments. The "Verified SHAs to reference" pattern closed this gap but doesn't eliminate it.
- **Prompt length vs. paste reliability.** Batch C2 and Step 2 of F3 a11y both arrived truncated. The longer the spec, the higher the odds of hitting a paste/message boundary. Recommended pattern: Opus pre-splits specs into batch-boundary-sized chunks from the start, rather than crafting monolithic specs that Ron has to chunk manually.

**Unsolicited observation about relay efficiency.** The three-layer relay is slower than a two-layer relay but produces higher-quality output, not because either AI layer is necessarily smarter but because the two layers catch different error classes: Opus catches semantic/strategic drift (palette swap, v0.7.3 spec currency); Code catches mechanical drift (duplicate lines, render artifacts, SHA typos). The relay pattern converts what would be one layer's blind spot into two layers' overlapping vision. Tonight's catches split roughly evenly: ~3 semantic catches (Opus via Ron), ~3 mechanical catches (Code at pre-commit diff stat).

---

## Summary

Tonight's execution layer feels most compressed at: (1) post-message-boundary truncation recovery, (2) file-state-verification-before-edit loops that recur on the same file, (3) URL/path convention assumptions that need actual `ls` confirmation. Those three are where small investments in spec discipline would compound most.

Everything else held up under load better than I expected when Ron said "nine commits tonight."

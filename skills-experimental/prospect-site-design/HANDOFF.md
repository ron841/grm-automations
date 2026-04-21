# Handoff Brief: v0.7 Editorial Upgrade Implementation

For the agent picking this up in the next chat. Read this before touching any file.

## Your job

Ron has an existing `prospect-site` skill at v0.6 that produces Vercel-deployed preview sites for home-services contractor prospects. The zip you are receiving is the v0.7 edit — a set of additions and refinements to the skill's reference files plus two new files. Your job is to land these changes into the live skill repo cleanly, commit them, and help Ron run the first 2-3 real builds against the updated skill so we can see whether the edits produce materially better sites.

Do this carefully. The edits interlock. A half-applied v0.7 will be worse than v0.6.

## What changed in v0.7

Five structural additions plus one major new concept:

1. **Photo role hierarchy** in `references/image-handling.md` — every accepted photo gets role-tagged at Phase 3 (heroPlate / detailShot / environmentalPortrait / evidenceShot) and Phase 5 uses the role for section assignment, not just the content-type tag. Includes a one-hero-per-section rule that Phase 6 enforces.

2. **Editorial asymmetric layouts module** in `references/section-patterns.md` — five named layouts (A: offset headline, B: image-bleed, C: 70/30 split, D: full-bleed, E: watermark numeral) with defaults, selection rules, and a three-layouts-per-page minimum.

3. **Scale contrast + visible grid + motion restraint** in `references/css-framework.md` — a new set of enforced rules: every page hits ≥80px and ≤14px type moments; hairline rules replace boxed cards in most list sections; only four CSS properties may transition; exactly one "signature micro-interaction" per site.

4. **Editorial discipline rules E1-E5** in `references/anti-slop-rules.md` — single accent color discipline, rules-not-boxes defaults, every-photo-captioned, outlined watermark numerals, no middle-weight display type.

5. **Phase 4 editorial proposal** in `SKILL.md` — signature micro-interaction, editorial-layout set, full-bleed photo assignment, watermark target, and emotional register are now declared at Phase 4 and shown in the approval gate for Ron to review before Phase 5 generates anything.

Plus two new reference files:

- `references/example-build.md` — a fully annotated reference homepage (Tucci Electric synthetic composite) showing every rule in composition. Loaded by Phase 5 at generation start as a pattern-match reference.
- `references/emotional-arc.md` — page-level emotional pacing via five registers (Quiet confidence, Earned pride, Neighborhood steady, Rescue-ready, Modern specialist) with a register-to-layout bias table. Loaded by Phase 4 for register selection and Phase 5 to carry the register through section decisions.

## Order of operations for tomorrow

Do not try to run a build before the repo is consistent. The sequence:

1. **Unzip the v0.7 folder and diff it against Ron's live skill repo.** The edits are additive — nothing was deleted — but some existing sections in `css-framework.md`, `section-patterns.md`, `anti-slop-rules.md`, `image-handling.md`, and `SKILL.md` were extended in place. Review each diff before committing.

2. **Commit the v0.7 edits in a single atomic commit.** Message suggestion: `v0.7 editorial upgrade: photo roles, editorial layouts, scale contrast, motion restraint, emotional register`. One commit makes rollback easy if something is wrong.

3. **Pipeline integrations listed below.** None of the v0.7 rules fire unless the pipeline is updated. Four changes are required; they are in priority order below.

4. **Run a first real build** against a known prospect (Tucci Electric or equivalent) with the `--auto` flag off so you hit the approval gate and can see the new declared editorial choices. Do not deploy it. Capture the approval-gate output and the generated HTML; compare the output against `references/example-build.md` to see whether Phase 5 is pattern-matching correctly.

5. **If the first build looks right, run two more** on different registers — a Rescue-ready trade (emergency plumber) and an Earned pride trade (pool builder). The register comparisons are where you see whether the emotional-arc document is actually tuning Phase 5's decisions or being ignored.

## Pipeline integrations required (in priority order)

These are the gaps between what the reference files describe and what the skill currently does. None of them are hard to implement; all of them are required for v0.7 to actually work.

### 1. Phase 3 writes role tags

The photo role hierarchy in `image-handling.md` describes a Phase 3 algorithm that runs role assignment after quality scoring and disqualifier rejection but before content-type tagging. Phase 3 needs to be updated to:

- Run the role-assignment pseudocode from `image-handling.md` after the existing quality score pass
- Write `role: "heroPlate" | "detailShot" | "environmentalPortrait" | "evidenceShot" | null` onto each photo record in `profile.json.photos`
- Enforce at most one role per photo (priority: hero > environmental > evidence > detail)
- Surface the distribution in the Phase 3 report so Ron can see how many of each role were tagged

If Phase 3 currently does photo processing inline in `SKILL.md` rather than in a separate pipeline step, the role-assignment logic goes inline at the same point.

### 2. Phase 4 editorial choices written to profile-draft.json

Five new fields under `profile-draft.json.design`:

- `register` — string enum (one of five)
- `signatureMicroInteraction` — string enum (one of five)
- `editorialLayouts` — array of layout ids (A, B, C, D, E)
- `fullBleedPhoto` — filename or null
- `watermarkTarget` — string enum or null

Phase 4 selection logic for each is in `SKILL.md` Phase 4 section. Emotional register selection specifically uses `emotional-arc.md` trade-mapping table.

### 3. Phase 5 reads register and example-build.md at generation start

At the top of Phase 5, before any section renders:

- Load `references/emotional-arc.md` and read the register-to-layout bias table
- Load `references/example-build.md` as pattern-match reference
- Carry the register value through every section decision (photo selection, copy tone within existing voice rules, layout tie-breaking)

Phase 5 does not add new logic for every register-specific decision — the register biases existing decisions rather than branching into register-specific codepaths. The exception is the close composition (register-specific close feelings in `emotional-arc.md`), which Phase 5 should treat as a register-conditional branch for the Contact section framing.

### 4. Phase 6 verification additions

Phase 6 gains the following automated checks. Add them to the existing check list:

- Scale contrast ratio (max font-size / min font-size) per page ≥ 5x
- At least one element on the page at ≥80px
- At least one text element at ≤14px in mono or uppercase
- `var(--color-primary)` + `var(--color-primary-hover)` occurrences ≤12 per page
- At least 3 editorial layouts per page
- No editorial layout repeated more than twice
- Layout D (full-bleed) used at most once per page
- Every non-hero, non-full-bleed photograph has a caption element
- Exactly one signature micro-interaction deployed site-wide (count distinct signature types, not deployments)
- Standard tier builds must include Layout E OR have an explicit constraintRelaxation

Phase 6 does NOT check emotional register or "feels like us" — those are human-only checks. Do not add fake verification for them; it will corrupt the point of the emotional-arc document.

## Known issues I caught during the audit (already fixed in the zip)

These were in my first draft of the edits and I caught and fixed them before handoff. Documenting so you do not re-introduce them:

- Token vocabulary mismatch: I initially used `--color-bg`, `--color-body`, `--color-body-muted` which did not exist. Fixed to `--color-background`, `--color-text`, `--color-text-muted`. Also added two new tokens the edits needed: `--color-background-alt`, `--color-border-dark`, `--color-text-on-dark`, `--color-text-muted-on-dark`, `--color-primary-hover`. All declared in `css-framework.md` :root block.
- Scale contrast threshold conflict: the ≥80px rule conflicted with Standard tier hero (44px max). Fixed by requiring Standard tier builds to include Layout E (watermark numerals produce 120-240px elements).
- Signature selection tree referenced signals the pipeline does not capture (logo glyph character, stats content type). Simplified to use only captured signals (tier, hero mode, service count). Mono-numeral-flip is still a valid signature but only reachable via `override signature:mono-numeral-flip` at approval.
- `-webkit-text-stroke` has no Firefox fallback in older versions. Added `color: var(--color-border)` as base + `@supports (-webkit-text-stroke: ...)` to flip to transparent.
- CSS Grid `grid-column` positioning requires `.editorial-grid` to be the direct parent of the columned elements. Documented explicitly in `section-patterns.md`.

## Known issues I did NOT fix (flag for Ron and you)

These are real but lower-priority, and they need Ron's input before I make calls on them:

- The approval gate now shows five editorial-design fields plus the existing score breakdown, hero mode, glass variant, headline candidate, and colors. That is a lot of information to absorb on one screen. If Ron finds it overwhelming in practice, consider a two-screen approval gate (first screen: score + hero + register; second screen: editorial choices). Do not split it preemptively — let Ron run a few real approvals and see.
- The emotional-arc register selection has a priority-order preference (captured copy tone > tenure+trade > default mapping) but the "captured copy tone" heuristic is not fully specified because the existing Phase 1 capture does not extract a tone classification. If the default-mapping fallback produces wrong registers in practice, Phase 1 needs a tone-classification pass added. For now, the priority order simply skips rule 1 when tone classification is unavailable.
- The `constraintRelaxations` field is written to `profile-draft.json` but the profile.json schema has not been formally updated. If Ron's schema is typed (TypeScript, Zod, Pydantic), add the new fields: `design.register`, `design.signatureMicroInteraction`, `design.editorialLayouts`, `design.fullBleedPhoto`, `design.watermarkTarget`, `design.constraintRelaxations`. Plus `photos[].role` from pipeline integration 1.

## Context you should know

A few things worth carrying into your work that are not in the spec files:

**Ron is the operator, Ben Tucci is an illustrative composite.** The example-build.md uses "Tucci Electric" as a synthetic reference. This is not a real prospect; it is a pedagogical composite. Do not treat the facts in example-build.md as a schema for Phase 1 capture — treat them as an illustration of what correct output looks like.

**The v0.6 failure was homogeneity.** Four different trades produced four sites that looked identical. v0.7 is an anti-homogeneity update. The editorial layouts, photo roles, and emotional registers are all structured to differentiate builds from one another, not just to make any single build better. When you are evaluating whether v0.7 is working, compare builds *across* prospects, not just within one.

**The escape hatch is load-bearing.** The "over-constraint escape hatch" in Phase 4 is not an edge case; it is the mechanism that keeps the rules from becoming brittle. Some prospects genuinely do not have enough photos, services, or content to satisfy every rule. The escape hatch lets Ron see the conflict explicitly and choose which rule to relax for that build. Encourage Ron to use it when appropriate; discourage him from treating it as a failure mode.

**The "feels like us" test is the final gate, not a nicety.** A build that passes every automated check but produces an evaluative response ("this is a nice design") rather than an emotional one ("this feels like us") is a build that will not sell. Phase 6 cannot detect this. Ron's final human check is the only filter that catches it. Do not ship a build that fails it even if every automated check passed. Regenerate.

**What I was watching for while writing this.** Three traps in spec work like this: (1) writing rules so tight they cannot be jointly satisfied, (2) writing rules the pipeline cannot actually enforce because they reference signals the pipeline does not capture, (3) writing rules that produce correctness without producing beauty. I tried to address all three — the escape hatch for trap 1, the simplified signature tree for trap 2, the emotional-arc document for trap 3. I do not know if I got all three right. The first 2-3 real builds are the test.

**The most likely failure mode of v0.7.** Builds will pass every Phase 6 check, Ron will run the "feels like us" test, and he will say "it feels more designed than v0.6 but it still doesn't feel like *this specific business*." If that happens, the fix is not in the rule files. The fix is in Phase 1 capture — getting more specific facts, more distinctive language, more real-person quotes that the copy rules can anchor to. Watch for this and flag it if you see it.

**The least likely failure mode that would be worst if it happened.** Phase 4 declares a register and a set of editorial layouts, Ron approves, Phase 5 generates — and the output does not actually reflect the register because Phase 5 reads the register value but does not condition any decisions on it. This would be a silent failure that passes every check. To detect it: generate two builds with different registers against the same prospect data (e.g., one as Quiet confidence, one as Earned pride) and compare. If the two builds are substantially identical, Phase 5's register-conditional logic is not firing. Fix by explicitly routing register through the register-to-layout bias table lookups in `emotional-arc.md`.

## Suggested first message to Ron when you start the chat

Something like:

> I've read through the v0.7 zip and the handoff brief. Before I start committing, I want to confirm: (1) you want me to land all v0.7 edits as a single commit against your live skill repo, (2) I should implement the four pipeline integrations in priority order, and (3) our first test is a real build against [prospect name] with --auto off so we can see the approval gate. Sound right?

That gives Ron a clear yes-or-reroute moment before anything commits.

## What success looks like after tomorrow's session

- v0.7 edits committed to Ron's skill repo cleanly
- All four pipeline integrations implemented (or explicitly deferred with Ron's agreement)
- At least one real build run end-to-end, approval gate captured, output compared against example-build.md
- If time permits: two more builds on different registers, compared for visible differentiation
- A short note from Ron in chat at the end: "this feels like us" or "this feels like a nice design" on the first-build output. Either answer is useful. The first means ship v0.7 as-is. The second means we iterate.

Good luck. Call Ron's attention to anything that feels off the moment you notice it. Small clarifications before committing are worth ten corrections after.

---

## Version

handoff-brief.md v0.7.0. Written at v0.7 handoff to give the next implementation agent a full briefing. Read before touching any file.

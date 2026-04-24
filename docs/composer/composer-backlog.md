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

### Editorial nickname asymmetry for urgent-service persona
- **Surfaced:** Commit 5.0 rescue-ready → urgent-service rename, 2026-04-21
  (commit e6b27d7).
- **Why deferred:** "Rescue-ready" (display name) ↔ `urgent-service`
  (machine key) is now the only persona where display name ≠
  kebab-of-display-name. Other 4 personas have direct mapping
  (quiet-confidence, earned-pride, neighborhood-steady,
  modern-specialist). Stage II.5 fixtures and Stage III approval-gate
  UI will need to handle the asymmetric mapping.
- **Target pickup:** Stage II.5 (profile.json fixtures) and Stage III
  (Phase 4-new approval gate UI).

### Post-Stage-II-(e) F1-F8 spot-check on persona-base × tier-multiplier math
- **Surfaced:** Stage II (e) tier-logic strip, 2026-04-22 (commit 4e70a0b).
- **Why deferred:** Luna F8 spot-check (quiet-confidence persona ×
  Professional tier) against shipped `style.css` values reveals
  material drift on three of four spacing values under the new
  persona-base × tier-multiplier architecture: `--space-section`
  holds steady at 120px (0% drift); `--space-section-generous` at
  161px vs shipped 140px (+15%); `--text-hero` at 88px vs shipped
  72px (+22%); `--text-hero-default` at 80px vs shipped 56px (+43%).
  Three values exceed the 10% tolerance threshold, triggering this
  tuning backlog item per Ron's Stage II (e) instruction. Editorial
  question: does Quiet confidence's persona base (heroSize 5.5rem,
  heroSizeDefault 5.0rem) produce an editorially desirable result
  at 88/80px, or did the shipped 72/56px represent the actual target
  and the new persona base needs Design re-tuning? A Luna F8 rebuild
  through the new CONFIG.spacing values would answer the aesthetic
  question on a real page. Until that rebuild happens, the new
  values ship as Design-authored and render differently from Luna
  F8's historical output on every future quiet-confidence +
  Professional build.
- **Target pickup:** Stage II (e) follow-up, Stage II (f), or the
  first Composer-era build that selects quiet-confidence persona.
  Alternative: include F1-F7 checks (A Quality Pool, Chad's Lawn,
  T&F Electric, Grandview, Oxford Lawn, A-1 Payless, Prime Pool)
  for broader persona × tier coverage before tuning decisions land.

### Composer-era reference build authoring pass
- **Surfaced:** Stage II (e) tier-logic strip, 2026-04-22 (commit 4e70a0b).
- **Why deferred:** `references/example-build.md` currently documents
  pre-Composer-era skill behavior via the status-note header added in
  this commit. The file's illustrative content (Tucci Electric as
  Premium-tier reference, tier-keyed CSS examples, pre-Composer Phase
  4 output shapes) accurately records prior state but is now
  inconsistent with current authority in `typography.md §11`,
  `voiceMap.md`, `css-framework.md` CONFIG.fonts + CONFIG.spacing, and
  `anti-slop-rules.md` persona-group framing. Author a Composer-era
  worked example through the restructured phases with explicit
  persona selection, `composition-plan.json` excerpts, and current
  Phase 5 emission patterns. Candidate source: one of F1-F8
  flagships with real Phase 3 → Phase 4 → Phase 5 excerpts.
- **Target pickup:** Post-Stage-II, possibly alongside first
  Composer-era sales build where the authoring effort produces
  both the reference file and the live prospect deliverable.
  Scope estimate: 800-1200 lines.

### P6.1 implementation — execution filling pending
- **Surfaced:** Stage II (f) P6.1 spec + stub commit, 2026-04-22
  (commit 2650ac1).
- **Why deferred:** Stage II (f) committed the specification and a
  structured Python stub — full function signatures, docstrings, logic
  skeletons, constant defaults, CLI arg wiring — so a follow-up
  execution-filling session can complete the implementation without
  rediscovering the design. Remaining work: Playwright reuse wiring
  (launch session, navigate + capture per viewport, per-section DOM
  query), Pillow/numpy pixel-analysis logic (per-section bounding-box
  crop, RGB-distance comparison against computed background color),
  computed-color edge-case handling (transparent ancestor walk,
  background-image dominant-color sampling, ambiguous-multilayer
  flag), static-blank vs scroll-dependent probe branch (scrollIntoView
  + 800ms reveal wait + re-capture + re-analyze), JSON + human-summary
  emission. Every `NotImplementedError` in `scripts/rendered_content_check.py`
  marks a spot the execution fill needs to complete. The spec is
  binding; implementation can deviate from proposed internals (Pillow
  vs numpy, sync vs async Playwright context) as long as the JSON
  emission contract, CLI signature, and threshold classification
  match `references/phase-6-integration.md §3`.
- **Target pickup:** Stage III Phase 4-new integration (P6.1 runs as
  part of the Phase 6 gate that validates Phase 5-new's emission), or
  a standalone pass if a build's P6.2 soft-fail count needs P6.1
  integration sooner. Also viable: a dedicated P6.x implementation
  sprint that fills P6.1, P6.2, P6.3, P6.4 together after Stage II
  closure so the Phase 6 aggregator can be authored against four
  complete implementations rather than four spec stubs.

### no-italic-on-data rule in typography.md
- **Surfaced:** Design's Commit 5.b pre-review — "Worth adding as an
  implicit rule in typography.md §4 if not already there — 'data voice
  is always roman' as a one-liner."
- **Why deferred:** typography.md is the Stage II (d) three-way merge
  output. Adding to Composer's current typography.md now would be
  edited away in the merge. Add to Design's typography-patterns.md
  section on data voice before Stage II (d), or add as a merge-time
  addition to the output file.
- **Target pickup:** Stage II (d) three-way merge preparation or
  execution.

### P6.5 undefined-custom-property Phase 6 check
- **Surfaced:** Design's Commit 5.b pre-review (E.5 recommendation).
  Secondary recommendation for a Phase 6 check catching any CSS custom
  property referenced in emitted output but undefined in
  css-framework.md. Would catch the class-of-bug that --font-mono,
  --font-display, and --font-data all fell into during Composer's
  pre-Option-C state.
- **Why deferred:** Stage II (f) spec batch per brain §8 Stage II (f)
  "P6.1 implementation spec." Batch additional P6.x specs alongside.
- **Target pickup:** Stage II (f).

### image-handling.md role-hierarchy language needs eligibility/assignment split
- **Surfaced:** Stage II (c) profile-schema.md authoring, 2026-04-22.
- **Why deferred:** `image-handling.md` line 123 says "A single photo can
  hold at most one role. Multi-role tagging is not allowed because role
  assignment is about editorial hierarchy, not content category." Under
  Composer's architecture that statement is true for *assignment*
  (composition-plan.json, singular) but not for *eligibility*
  (profile.json `eligibleRoles`, plural per profile-schema.md §10.1). The
  prose needs updating to name the distinction — eligibility plural on
  Phase 3's side, assignment singular on Phase 4's side, with the
  "at most one role" rule applying to the assigned output rather than
  the per-photo capability record. Without the update, the next reader
  of image-handling.md will read a contradiction against profile-schema.md
  and guess which is authoritative.
- **Target pickup:** Stage II (d) typography merge pass (image-handling.md
  sits adjacent to the merge targets) or Stage II (e) tier-logic strip.

### Hero background hue-warmth derivation rule needs authoritative cited source
- **Surfaced:** Stage II (c) profile-schema.md authoring, 2026-04-22
  (Design-flagged during Flag 3a review).
- **Why deferred:** Phase 5 computes the hero page background color from
  `brandPalette.primary` hue warmth — Luna F8 example: primary `#db542c`
  at HSL hue 14° → warm off-white `#faf7f2`. The mapping from hue band
  to off-white value is an editorial derivation rule that isn't written
  down anywhere authoritative today (Luna F8's `designChoices.heroBackground`
  carried the output but not the rule). profile-schema.md §9 and §15
  state that the derivation computes inline at Phase 5 per scope call #5
  — but "computes inline" without a cited rule means each implementor
  re-derives and drift accumulates across builds. Write down the
  hue-band → off-white-value mapping (cool / warm / neutral bands,
  fallback for greyscale brands, behavior on high-chroma brands) in
  `image-handling.md`, a new `references/color-derivations.md`, or the
  Stage II (d) typography merge output — wherever derivation rules
  naturally live post-merge.
- **Target pickup:** Stage II (d) typography merge, or the first site
  build post-Composer launch where the rule needs to be re-derived by
  Phase 5 code.

### composition-plan-schema.md §5.3 per-section-type contracts deferred
- **Surfaced:** Stage II (c) Phase 2 composition-plan-schema.md
  authoring, 2026-04-22 (Checkpoint 1 q6 resolution).
- **Why deferred:** Schema lands with `statRow` (§5.1) and
  `sectionOpener` (§5.2) contract fields authored. The remaining
  tagged section types enumerated in §5 (`hero`, `servicesGrid`,
  `testimonialsSection`, `featuredPullQuote`, `faqSection`,
  `beforeAfter`, `anchorStrip`, `trustSection`, `contactForm`,
  `footerSection`, `aboutStory`) need their own per-type contract
  field tables before Stage III Phase 4-new implementation begins.
  Priority order per Design: hero first (Luna F8
  profile.design.heroMode + heroGlassVariant + videoAugmentation
  migrate here), servicesGrid second (photo assignment filtering
  against evidenceShot eligibility), testimonialsSection third,
  aboutStory fourth, remainder in any order. Authority per section:
  `section-patterns.md` + `hero-patterns.md` + Design's
  `typography-patterns.md`.
- **Target pickup:** Stage II (c) follow-up pass after this commit
  lands, or defer to Stage II (d) if scoping permits.

### First-real-build editorial review — shimmer-hero-cta retention
- **Surfaced:** Stage II (c) Phase 2 composition-plan-schema.md
  q1-follow-up resolution, 2026-04-22.
- **Why deferred:** composition-plan-schema §2.1 Tier 2 enum includes
  `shimmer-hero-cta` as one of four motion micro-interactions. Design's
  editorial note: "shimmer" reads as SaaS, not editorial, and may not
  survive an aesthetic pass regardless of the Tier 2 category. Flag at
  approval gate on any build where Phase 4 selects shimmer-hero-cta;
  Design reviews the effect on the live rendered site before locking
  shimmer-hero-cta as a permanent Tier 2 value. Retention decision is
  a live-site editorial judgment that can't be made from the schema
  alone.
- **Target pickup:** First build where Phase 4 selects
  `shimmer-hero-cta` — Design review on deployed preview URL.

### Phase 6 P6.2 implementation — Check 17 split
- **Surfaced:** Stage III Gate 3 Motion Restraint scope split,
  2026-04-22 (commit 6f8bcbb).
- **Why deferred:** Legacy `css-framework.md` Motion Restraint
  section carried a Phase 6 Check 17 assertion ("verifies that no
  more than one of the approved signatures is present") keyed to
  the retired five-value signature enum. Gate 3 replaced that
  subsection with the Tier 2 motion micro-interactions rule;
  Check 17 text disappeared alongside. Design recommends the
  check split into two when P6.2 implementation is authored:
  17a Tier 1 `site.signatureMicroInteraction` singular emission
  (exactly one value from the six-value enum); 17b Tier 2
  `site.microInteractions` array contains only approved values
  (subset of the four-value enum) with no over-emission. Check
  17 is not one of the 13 P6.2 editorial-suite hard-fail checks
  in `composition-plan-schema.md §10`; the split is editorial
  direction for future P6.2 implementation, not a schema field
  change.
- **Target pickup:** Phase 6 P6.2 implementation (currently stub
  per Stage II (f)). Bundle with broader Check 17a/17b test-author
  pass when P6.2 spec fills in.

- **Fixture 2 pullquote word-count retrofit-or-grandfather.**
  Fixture 2 Kingsley composition-plan (commit 1ea2408)
  home-page pullQuotes[0].extractedText is 32 words;
  composition-plan-schema §4.5 / typography-patterns.md §6
  heuristic specifies 8-20 word bound. Per Design's
  Session 3 Q2 close: fixtures are authored intent; Phase
  4-new LLM authoring honors 8-20 bound. Decision at
  Checkpoint 2 when Design reviews Phase 4-new output
  against fixtures: retrofit Fixture 2's pullquote within
  bound, OR grandfather 32-word quote as fixture-authored
  exception. Non-blocking for Phase 4-new implementation
  start. (Added 2026-04-22, Session 3 close.)

- **Fixture-side authoring slots as a named §2 concept
  (deferred).** Design surfaced in Session 4 Concern 1
  reshape that fixture-side intent authoring slots
  (personaIntent, voiceZoneIntent[], italicIntent[],
  pullQuoteIntent, eyebrowIntent[], microInteractionIntent)
  could land as a canonical named concept in
  composition-plan-schema.md §2, where fixture shape
  specification lives. Distinct from the six intent-spec
  fields in §14, which are the structural-derivation
  output set. Not authored now — flagged so if Phase 4-new
  execution surfaces a need to reference these slots by
  canonical name, the reshape has a known home. (Added
  2026-04-23, Session 4.)

- **LESSONS — cross-grain reconciliation + summary-vs-disk
  working-style (process observations).** Session 4
  surfaced three spec-vs-spec drifts at Gate A pre-
  execution. Pattern 1 — when two load-bearing artifacts
  encode the same domain at different grains,
  reconciliation needs a dedicated checkpoint beat rather
  than inference from later gates (§7 section-level vs
  fixture subpart-level was the exercised case; §14
  two-pass vs Q2 three-pass was the earlier case this
  session). Pattern 2 — when a reshape touches field
  shapes, enum values, or rule mechanics, Design asks for
  on-disk text before authoring; Chat-Claude routes with
  diagnostic-first disk state rather than summary;
  neither party authors mechanics from summary. Summary
  routing is fine for architectural questions (grain,
  partition, pass count); it is not fine for field names
  and enum values. Pattern 3 — Code's pre-execution
  verification pattern caught all three drifts cleanly;
  the halt-don't-press-through discipline is load-bearing
  and should be preserved across future gates. Pattern 4 —
  **Partial-surface reads do not license whole-file
  generalizations.** Session 4 surfaced this pattern
  twice after the original entry landed. When authoring
  against a spec file from a partial paste, confirm the
  specific surface being authored against, not the
  adjacent surface used to infer structure. Applies
  symmetrically to Design and Chat-Claude. The
  "typography.md §5 dissolved its numbering" read was
  true for §5 specifically but false as generalization
  to the whole file (§7 and §9 preserved numbering);
  the Rule 1-6 migration from Chat-Claude's summary
  introduced drift on three rules; both errors came
  from partial-surface reads generalized to whole-file
  assumptions. (Added 2026-04-23, Session 4 close.)

  - **Pattern 4 path-check sub-discipline (Session 5 close-out).**
    When Chat-Claude authors any Code-facing prompt or editorial
    routing referencing file paths, explicitly ls or grep the
    paths against disk before the reference lands in text.
    Note 3 posture (on-disk text before authoring mechanics)
    covers the general case; path-check is the mechanical form
    at the file-reference surface. Session 5 logged three
    Pattern 4 catches (kitchen-table surface-fix, Call 1
    profile-schema field shapes, Call 3 §14 partition + Rule 4
    citation); path-check would have caught the citation-class
    catches at pre-authoring. (Added 2026-04-24, Session 5
    close-out.)

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

- **Watch-surfaces (pattern candidates, pending recurrence).**
  Observed behaviors that may be drift classes worth pattern-
  naming. Candidates land here on first observation; promote
  to ratified LESSONS patterns on Session-to-Session recurrence.

  - **Watch-surface 1 (Session 5 close-out).** Self-flagged
    uncertainty is a halt trigger, not a ship caveat. Observed
    in v1 Implementation Prompt close-out drafting: Chat-Claude
    correctly self-flagged reconstructed-template status and
    path uncertainty but shipped v1 with the self-flag embedded
    rather than halting to resolve. The close-loop discipline:
    when self-flagging during close-out drafting, halt and
    resolve before save rather than shipping with the flag
    attached. Adjacent to Pattern 3 (halt-don't-press-through)
    at Code's verification surface, but operating on a different
    surface (close-out drafting) with a different halt-trigger
    (self-observed uncertainty, not external catch). Promotion
    condition: if Session 6 or later Chat-Claude encounters
    similar reconstructed/uncertain content during close-out
    drafting and self-flag-ships again, promote to Pattern 8
    with name honoring the surface distinction. (Added
    2026-04-24, Session 5 close-out.)

- **Rule 1-6 derivation mechanics migration to §14
  deferred (Path A).** Session 4 Concern 4 reshape
  evaluated two paths for where detailed Rule 1-6
  mechanics live — schema §14 as single source of truth
  (Path A) vs. implementation prompt carrying mechanics
  with §14 naming the contract (Path B). Session 4 took
  Path B to unblock Phase 4-new execution. Design's
  amended Rule 4 text from Concern 4 reshape stands as
  the template shape (input / emission / validator
  behavior / derivation step / error class) for the
  future migration. When Path A is picked up in a later
  session, Rule 4's authored template applies to the
  other five rules; migration content comes from the
  implementation prompt's existing Rule 1-6 block, NOT
  from re-authoring. Cross-check required at migration
  time: on-disk §2.2 pathConvention shape, SKILL.md
  tier enums (Premium / Professional / Standard), §4.10
  scaleContrast emission shape. (Added 2026-04-23,
  Session 4 Concern 4 close, Option B path.)

## Resolved deferrals

- **Session 4 Concern 5 Item 1 — italic word-class
  canonical home.** Resolved via composer: Item 1
  italic word-class resolution commit 03ca705. 4-value
  enum {place, name, tenure, trade-term} canonical in
  emotional-arc.md's "Italic word-class vocabulary
  (persona-indexed)" subsection; schema §5.3.4 and
  typography.md §15 Check 9 cross-reference.

- **Session 4 Concern 5 Item 2 — typography-patterns.md
  → typography.md global rename.** Resolved via composer:
  Item 2 citation rename commit 94c6acf. 17 live
  citations renamed; 3 merge-log references in typography
  .md itself retained pointing at Stage II archive.

- **Session 4 Concern 5 Item 3 — micro-interaction
  duration canonical lock.** Resolved via composer: Item
  3 duration lock commit 35343c7. Two-row lock canonical
  in emotional-arc.md "Micro-interaction duration lock
  (persona-indexed)" subsection; css-framework.md and
  SKILL.md cross-reference.

- **Session 4 Concern 5 Item 4 — kitchen-table voice
  enum drift.** Resolved via composer: Item 4 voice
  correction commit 288946a. Schema §5.3.4 line 429
  kitchen-table → closing-table; optional inline
  citation nit applied.

### CONFIG.spacing tier-keyed residues + tier-class CSS overrides
- **Originally surfaced:** Commit 5.b CONFIG.fonts persona-conditional
  restructure, 2026-04-21 (commit 6cfd6df).
- **Resolved:** 2026-04-22 (commit 4e70a0b). Stage II (e) tier-logic
  strip executed under full authorship with Design arbitration on
  three editorial-reach items (CONFIG.spacing refactor, glass-variant
  rationale, anti-slop Block A persona-group refactor). Design
  authored per-persona base values for all five personas;
  `CONFIG.spacing` refactored to two-axis architecture (persona base
  × tier multiplier). Phase 5 computes final values at build time
  and emits directly into base `:root`. Three `:root.tier-*`
  cascade-override blocks retired. Glass-variant selection stays
  tier-keyed per `typography.md §Appendix B` section-density
  treatment. `anti-slop-rules.md` banned-fonts section reframed from
  tier-keyed to persona-group-keyed (serif-display vs. sans-display)
  per new `typography.md §11.Persona groupings for font discipline`
  subsection. `<html class="tier-*">` emission replaced with
  `class="persona-{kebab-key}"`. Luna F8 spot-check flags three of
  four values drift >10% (new Active backlog item for tuning).
  Composer-era example-build.md rewrite deferred (new Active backlog
  item).

### Stage II (d) typography.md three-way merge — SectionOpener framing conflict
- **Originally surfaced:** Stage II (c) Phase 2 composition-plan-schema.md
  authoring, 2026-04-22 (Checkpoint 1 q2 resolution).
- **Resolved:** 2026-04-22 (commit fc0ebfa). Stage II (d) three-way
  merge executed under full authorship with Design arbitration on
  three conflicts (A1 SectionOpener framing, B3 Fraunces-universal
  rewording, C3 pull-quote trigger). Axis-parameterized SectionOpener
  primitive retired; role-class assignment (`.role-data-eyebrow` +
  `.role-display-section` with ≤24px proximity contract) adopted in
  merged typography.md §6. Composer's orientation-gating insight
  preserved as prose. Marker-class canonical example in §17.4 updated
  from `.section-opener--italic-*` to `.section-opener--orientation-*`.
  Nine auto-resolvables (A2, B1, B2, C1, C2, C4, C5, C6, C7) applied
  per README default tie-breakers. Sentinel check (Rule E6 + Check 18)
  passed — home files untouched by merge. Merged typography.md: 952
  lines; merged voiceMap.md: 532 lines. Stage II (a) file copies
  retired as superseded by merge output.

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

### Stage II (b) — Wave 1/Wave 2 backports via cherry-pick mechanism
- **Originally surfaced:** Brain file §8 Stage II (b) enumeration
  (12 source commits; 10 backport operations).
- **Resolved:** 2026-04-21 via 9-commit Option C sequence under Design
  editorial direction:
  - `6ae7d89` / `ac6ec6b` (C.1 --font-mono → --font-data rename)
  - `c7bedaf` / `d78846e` (C.2 rhythm-tier tokens)
  - `3987637` / `137bf46` (C.3 mobile breakpoint reconciliation 900 → 980 + 540 secondary)
  - `9694f05` / `f9d5075` (C.4 font-loading template rewrite)
  - `e6b27d7` / `dd1d151` (C.5.0 rescue-ready → urgent-service rename)
  - `64f0129` / `f453afa` (C.5.a token migration --font-heading → --font-display + --font-data declaration)
  - `6cfd6df` / `12fdcf8` (C.5.b CONFIG.fonts tier-keyed → persona-conditional restructure)
  - `3a57ac6` / `fd47500` (C.5.c typography-patterns.md → typography.md cross-reference fix)
  - `c6b48ff` / `51fe68e` (C.6 voiceMap.md integration point in SKILL.md Phase 5)

  Note: original format-patch + git am mechanism (clarified in commit
  16b7cab as the correct backport mechanism per brain §8 mechanism
  revision) proved unviable in execution due to a sequencing collision
  — Stage II (a) Phase 2 file copies pulled production HEAD state of
  typography.md and voiceMap.md (already containing all Wave 1/Wave 2
  additions), and Stratum 3 identity sweep modified css-framework.md /
  SKILL.md / content-rules.md / deployment.md in-place. The Wave 1
  patches could not apply onto a baseline that didn't match what they
  expected (file-already-exists for typography/voiceMap; patch-no-apply
  for the Stratum-3-modified files). Option C substantive additions
  under Design editorial direction replaced the mechanical backport;
  features 3 (SectionOpener) and 4 (StatRow) deferred to Stage II (c)
  as composition-plan schema contracts rather than component primitive
  retrofits per Design's read; feature 5 (Fraunces universal) rejected
  as superseded by persona-conditional CONFIG.fonts (urgent-service
  uses Archivo, modern-specialist uses Inter Tight, etc.). Features 1,
  6 (renamed --font-mono → --font-data), 7, 8, 9, 10 landed.

### Stage III — emotional-arc.md persona-signature column rewrite (two-tier)
- **Originally surfaced:** Stage II (c) Phase 2
  composition-plan-schema.md q1-follow-up resolution, 2026-04-22.
- **Resolved:** 2026-04-22 Session 3. Gate 1 411e30a landed the
  6-column Tier 1 + Tier 2 bias table, tenure+trade convergence
  clause, and layout/photo/copy tie-breaking paragraphs. Gate 1
  polish 949de45 hoisted the Hero calibration subsection and
  promoted signature-rule bullets to standalone paragraphs per
  Flag A + Flag B. Persona defaults now reference Tier 1
  compositional vocabulary (italic-color-shift,
  watermark-numeral-offset, anchor-strip-pivot, hero-glass-blur,
  stat-row-ledger, none) with parallel Tier 2 motion defaults per
  persona.

### Stage III — SKILL.md Phase 4 signature decision tree rewrite
- **Originally surfaced:** Stage II (c) Phase 2
  composition-plan-schema.md q1-follow-up resolution, 2026-04-22.
- **Resolved:** 2026-04-22 Session 3 (commit 757e030). Phase 4
  signature selection tree rewritten as Tier 1 six-rule resolution
  + Tier 2 persona-default-plus-additive resolution. Legacy
  five-value motion-based tree retired. Line 429 output path split
  to composition-plan.site.signatureMicroInteraction (singular,
  six-value enum) + composition-plan.site.microInteractions
  (array, four-value enum). Authority split: Tier 1 definitions
  live in typography-patterns.md, Tier 2 in css-framework.md
  Motion Restraint section.

### Stage III — css-framework.md Motion Restraint review
- **Originally surfaced:** Stage II (c) Phase 2
  composition-plan-schema.md q1-follow-up resolution, 2026-04-22.
- **Resolved:** 2026-04-22 Session 3 (commit 6f8bcbb). Motion
  Restraint section heading gained "(Tier 2 micro-interactions)"
  scope suffix. Legacy "one signature micro-interaction" rule
  + 5-value list retired; replaced with "Tier 2 motion
  micro-interactions rule" subsection documenting the four
  approved Tier 2 values (eyebrow-reveal, underline-bloom,
  shimmer-hero-cta, mono-numeral-flip). Closing paragraph notes
  Tier 1 compositional signatures migrate to typography-patterns.md
  role-class territory. Durations subsection gains rescue-ready
  250ms entry bullet per emotional-arc.md persona bias.

## Informational notes (process learnings, not deferrals)

### Design artifact names ≠ Composer filenames
- **Surfaced:** Commit 5.c surgical fix, 2026-04-21 (commit 3a57ac6).
- **Lesson:** Chat-Claude drafted CONFIG.fonts narrative using
  "typography-patterns.md" (Design's package filename at
  `~/grm-automations/docs/composer-stage-ii-typography-source/`) when
  the correct Composer reference is "typography.md" (the file Stage
  II (a) Phase 2 copied from production into `references/`, and Stage
  II (d) three-way merge output will land at the same path).
  Design's package filenames are authorship sources, not destination
  names. Chat-Claude should cross-check every reference to
  Design-authored artifact names against Composer's actual file
  layout before including in commit drafts.
- **No action item.** Process discipline note for future Commit drafts.

---

**Convention for this file:**
- Add deferrals as they surface. Include originating commit hash for
  traceability.
- When a deferral is picked up, move it from Active to Resolved, add
  resolution commit hash, and a one-line note on what got done.
- Chat-Claude reviews this file at the start of every Composer session
  to avoid losing track of deferred work across session boundaries.

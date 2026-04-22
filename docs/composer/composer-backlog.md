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

### CONFIG.spacing tier-keyed residues + tier-class CSS overrides
- **Surfaced:** Commit 5.b CONFIG.fonts persona-conditional restructure,
  2026-04-21 (commit 6cfd6df).
- **Why deferred:** Grep showed premium/professional/standard still
  tier-keyed in CONFIG.spacing (css-framework.md lines 123/129/135) and
  three `:root.tier-*` CSS override blocks (lines 869/896/907 +
  900/911/922/927/938/949/964/969) with tier-class naming throughout
  Phase-5 documentation. Stage II (e) tier-logic strip scope per
  brain §8. Whether to strip CONFIG.spacing or refactor to
  persona-conditional spacing is a Stage II (e) design call.
- **Target pickup:** Stage II (e).

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

### Stage III — emotional-arc.md persona-signature column rewrite (two-tier)
- **Surfaced:** Stage II (c) Phase 2 composition-plan-schema.md
  q1-follow-up resolution, 2026-04-22.
- **Why deferred:** `references/emotional-arc.md` persona table's
  "Signature" column is keyed to Composer's legacy five motion-based
  values (italic-color-shift, eyebrow-reveal, underline-bloom,
  shimmer-hero-cta, mono-numeral-flip). composition-plan-schema §2.1
  establishes a two-tier architecture — Tier 1 signature (six
  compositional values) and Tier 2 micro-interactions (four motion
  values). emotional-arc.md persona defaults need to reference the
  Tier 1 compositional vocabulary, with a parallel Tier 2
  micro-interactions column documenting per-persona motion defaults.
  Schema ships with the forward spec; emotional-arc.md is a consuming
  reference that catches up when Phase 4-new is authored.
- **Target pickup:** Stage III Phase 4-new implementation.

### Stage III — SKILL.md Phase 4 signature decision tree rewrite
- **Surfaced:** Stage II (c) Phase 2 composition-plan-schema.md
  q1-follow-up resolution, 2026-04-22.
- **Why deferred:** SKILL.md Phase 4 signature selection tree (lines
  417–427, five-value motion-based tree) is Composer's inherited
  Phase 4-old. Stage III rewrites Phase 4 as Phase 4-new against
  composition-plan-schema. The Tier 1 compositional vocabulary
  replaces the five-value motion tree; a separate Tier 2
  micro-interactions selection step is added with per-persona defaults
  drawn from emotional-arc.md (which itself is being rewritten per
  adjacent Stage III item above).
- **Target pickup:** Stage III Phase 4-new implementation.

### Stage III — css-framework.md Motion Restraint review
- **Surfaced:** Stage II (c) Phase 2 composition-plan-schema.md
  q1-follow-up resolution, 2026-04-22.
- **Why deferred:** `references/css-framework.md` "Motion Restraint"
  section defines the five motion-based values today. Under the
  two-tier architecture, Motion Restraint should govern Tier 2
  micro-interactions cleanly and not reference Tier 1 signatures
  (which are compositional/typographic, not motion — they belong in
  typography-patterns.md's role-class territory). Review the section
  at Stage III to confirm scope and cut any Tier 1 references that
  slipped in during the legacy five-value era.
- **Target pickup:** Stage III Phase 4-new implementation.

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

## Resolved deferrals

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

# Composer authority map

This file names the canonical on-disk location for every
load-bearing concept in the Composer spec. When authoring
a reshape that touches any concept below, read this file
first to locate the concept's canonical home. Author
against that location; update this file if the canonical
home moves.

Concepts are grouped by functional layer. Each entry
names: canonical location (file + section + line range),
vocabulary or enum (if applicable), cross-references
(other files that reference or depend on the concept),
status (clean / flagged / ambiguous / deferred), last
touched (session + commit hash if post-Session-1),
history (prior session touches when concept has
multi-touch lineage), and flag note (if status differs
from clean).

Flag taxonomy:

- **clean** — canonical home established; no spec-
  integrity risk
- **flagged** — contradiction, drift, fragile reference,
  or incomplete-but-resolvable concept with a named
  resolution path
- **ambiguous** — canonical home is unnamed or
  distributed AND the resolution path is itself unclear;
  the concept needs architectural decision before a
  single canonical home can be declared
- **deferred** — intentionally off-canonical per an
  explicit architectural call with a named checkpoint
  or session for revisit; the flag note names when to
  revisit

Distinction between flagged and ambiguous: flagged
carries a known resolution even when resolution hasn't
executed yet. Ambiguous carries no known resolution —
the architectural question itself is open.

**Maintenance contract:** reshapes that cross two or
more concepts in different groups must update this file
atomically with the reshape commit, not as a follow-up.
A drifted authority map is worse than no authority map.

---

## Group 1 — Site-level structural concepts

### Concept 1. Tier enums
**Canonical:** SKILL.md:296-300 (Tier assignment section)
**Vocabulary:** Premium (70-100), Professional (40-69), Standard (0-39)
**Cross-references:**
- composition-plan-schema.md:360 — heroGlassVariant tier-gating references Premium
- composition-plan-schema.md:403 — Layout D tier-gating references Premium
- css-framework.md — tier-conditional CSS
- All six fixture composition-plan.json files carry site.tier as Premium/Professional/Standard string

**Status:** clean
**Last touched:** pre-Session-1 (production-era authoring)

### Concept 2. Tier assignment rubric (scoring)
**Canonical:** SKILL.md:286-300 (Scoring rubric + Tier assignment sections)
**Vocabulary:** Five 20-point categories (Copy Language, Visual Quality, Business Maturity, Site Sophistication, Brand Intentionality); total /100 → tier thresholds per Concept 1
**Cross-references:**
- Phase 4-new implementation prompt Rule 2 cites these lines as authority for assign_tier.py

**Status:** clean
**Last touched:** pre-Session-1

### Concept 3. Persona enums
**Canonical:** emotional-arc.md:304 (Persona selection section)
**Vocabulary:** quiet-confidence, earned-pride, neighborhood-steady, urgent-service, modern-specialist
**Cross-references:**
- composition-plan-schema.md:426 — italic bias per persona (uses display alias "Rescue-ready (urgent-service)" post-de32fc2)
- emotional-arc.md:238-242 — bias table row labels with display names
- Phase 4-new implementation prompt Rule 2 + select_persona.py module spec

**Status:** clean
**Last touched:** Session 4, commit de32fc2 (Rescue-ready row label alias for urgent-service enum join)

### Concept 4. Persona selection logic
**Canonical:** emotional-arc.md:266-304 (Persona selection section)
**Vocabulary:** three-input priority — (1) captured copy tone, (2) tenure+trade convergence, (3) trade-category default mapping
**Cross-references:**
- emotional-arc.md:276-299 — trade-category table
- Phase 4-new implementation prompt select_persona.py module spec

**Status:** clean
**Last touched:** Session 3, Gate 1 commit 411e30a

### Concept 5. Signature micro-interaction enums
**Canonical:** composition-plan-schema.md §2.1 lines 54-82
**Vocabulary:** Tier 1 = 6 compositional values + "none" (italic-color-shift, watermark-numeral-offset, anchor-strip-pivot, hero-glass-blur, stat-row-ledger, none); Tier 2 = 4 motion values (eyebrow-reveal, underline-bloom, mono-numeral-flip, shimmer-hero-cta)
**Cross-references:**
- emotional-arc.md:236-242 — Tier 1/Tier 2 persona defaults column in 6-column bias table
- css-framework.md Motion Restraint — Tier 2 governance
- typography.md §5, §7 — Tier 1 typographic treatment authority
- Phase 4-new implementation prompt resolve_signatures.py module spec

**Status:** clean (selection tree logic documented in implementation prompt per Concept 31; enum values canonical in schema)
**Last touched:** Session 4, commit 94c6acf (citation rename to typography.md)
**History:** pre-Session-1 (enum authoring); Session 3 Gate 2 commit 757e030 (signature tree rewrite in SKILL.md)

### Concept 6. Micro-interaction duration lock
**Canonical:** emotional-arc.md "Micro-interaction duration lock (persona-indexed)" subsection (inserted post-6-column bias table)
**Vocabulary:** two-row lock — all personas except urgent-service at entry 400 / hover 180; urgent-service at entry 250 / hover 150
**Cross-references:**
- css-framework.md Durations and easing — implementation commentary with wider acceptable ranges (150-200ms hover, 400-600ms entry); lock table authoritative for composition-plan.json
- SKILL.md:438 — discoverability pointer to duration lock subsection
- emotional-arc.md:194 — Hero calibration table with inline per-persona durations (downstream interpretation)
- composition-plan-schema.md §14:681 — field name cited
- Phase 4-new implementation prompt Rule 3 validator

**Status:** clean
**Last touched:** Session 4, commit 35343c7 (Item 3 canonical lock)

### Concept 7. ColorScheme shape
**Canonical:** composition-plan-schema.md §2.3 lines 98-120
**Vocabulary:** fields primary, accent, darkPrimary, primaryUsage; primaryUsage enum {accent-only, primary-heavy, dual-emphasis}; persona default-bias table
**Cross-references:**
- profile-schema.md brandPalette (input)
- Phase 4-new implementation prompt set_color_scheme.py module spec

**Status:** clean
**Last touched:** pre-Session-1

### Concept 8. PathConvention shape
**Canonical:** composition-plan-schema.md §2.2 lines 88-96
**Vocabulary:** fields homePath (const "/"), aboutPath, servicePathPattern, contactPath, trailingSlash; intent shape = "kebab-case" string (fixture), emission = object (derivation per Phase 4-new implementation prompt Rule 1)
**Cross-references:**
- Phase 4-new implementation prompt Rule 1 derivation

**Status:** clean
**Last touched:** pre-Session-1

---

## Group 2 — Cross-cutting concepts

### Concept 9. Conversion-critical zone list (persona-bias immunity)
**Canonical:** voiceMap.md §7 Persona bias rules around line 269 (full list + bias exclusion logic)
**Vocabulary:** hero-headline, promo-bar, service-card-description, stats-section, faq-answer, featured-promotion
**Cross-references:**
- composition-plan-schema.md §4.2:186 — short list by line-number reference (fragile — see flag)
- voiceMap.md §6 — bias column "No persona bias" entries indicate these zones

**Status:** flagged
**Last touched:** pre-Session-1
**Flag note:** schema §4.2:186 cites voiceMap.md by line number range ("lines 186-196"), which breaks on any voiceMap.md reflow. Future nit: replace line-number ref with section-name reference. Not blocking any current gate.

### Concept 10. Voice enum values
**Canonical:** composition-plan-schema.md §4.2:179,181 (defaultVoice and resolvedVoice enum columns)
**Vocabulary:** closed three-value enum {closing-table, saturday-morning, front-porch}
**Cross-references:**
- voiceMap.md §3 — in-scope/out-of-scope voice framing + kitchen-table historical note with surface-grammar-bound partition (end of §3, post-Session-5)
- voiceMap.md §4 — full voice-by-voice tonality definitions
- GRM_VOICE_SKILL.md (external — github) — canonical six-voice library source per voiceMap.md §2:29-33
- composition-plan-schema.md §5.3.4:429 + about-page-body-slot voice assignment note — about-page-body saturday-morning-all-personas rule (post-Session-5 kitchen-table resolution)

**Status:** clean
**Last touched:** Session 5 (Commit 2 kitchen-table resolution: §5.3.4 about-page-body saturday-morning-all-personas supersession + voiceMap §3 historical note with surface-grammar-bound partition)
**History:** pre-Session-1 (enum authoring); Session 4 commit 288946a (§5.3.4 kitchen-table → closing-table for modern-specialist/quiet-confidence + inline §4.2 citation nit)

### Concept 11. Role-class vocabulary
**Canonical:** typography.md §3 Role classes lines 119-154
**Vocabulary:** .role-display-* (hero, section, watermark, pullquote, lede), .role-body-* (paragraph, caption, measure), .role-data-* (eyebrow, numeral, stat-caption, metadata, service-area), .role-italic-* (signature, class-scoped variants)
**Cross-references:**
- composition-plan-schema.md §5.3.3:407 — testimonialsSection contract cites role classes
- composition-plan-schema.md §4.8 — italicSelections references role-italic-{class}
- composition-plan-schema.md §4.9 — displayMoment elementId + roleClass
- composition-plan-schema.md §5.2 — sectionOpener role-class framing
- composition-plan-schema.md §5.3.4:432 — .role-italic-{class} styling citation (post-Session-4 rename)

**Status:** clean
**Last touched:** Session 4, commit 94c6acf (citation rename to typography.md §3 references)

---

## Group 3 — Editorial concepts

### Concept 12. Voice-zone vocabulary — section-level
**Canonical:** composition-plan-schema.md §7 "Section-level zones" lines 495-501 (post-Session-4)
**Vocabulary:** 15 keys — hero-headline, hero-subheadline, promo-bar, trust-marquee, services-grid-header, service-card-description, stats-section, before-after-header, testimonials-header, featured-promotion, faq-question, faq-answer, contact-form-header, footer-tagline, about-page-body
**Cross-references:**
- composition-plan-schema.md §4.2:178 — voiceZones[].zone enum cites §7
- voiceMap.md §6 zone table — 14 grouped documentation rows mapping to the 15 keys
- Phase 4-new implementation prompt Rule 4 validator

**Status:** clean
**Last touched:** Session 4, commit 1c5379b (§7 two-level vocabulary reshape)

### Concept 13. Voice-zone vocabulary — section-subpart
**Canonical:** composition-plan-schema.md §7 "Section-subpart zones" lines 503-510 (post-Session-4)
**Vocabulary:** 13 keys — about-page-attribution, about-page-body-slot, about-page-heading, hero-eyebrow, hero-headline-slot, hero-primary-cta, hero-subheadline-slot, services-card-body, services-card-headline, services-grid-heading, testimonial-attribution, testimonial-body, testimonials-heading
**Cross-references:**
- All six fixture composition-plan.json files use these keys in inline voiceZoneAssignments post-retrofit 3d7a51f
- Phase 4-new implementation prompt Rule 4 validator

**Status:** clean
**Last touched:** Session 4, commit 1c5379b (reshape)
**History:** Session 4 commit 3d7a51f (fixture -slot disambiguation)

### Concept 14. Subpart → section voice-zone flatten mapping
**Canonical:** composition-plan-schema.md §7 "Subpart → section flatten mapping" lines 520-535 (post-Session-4)
**Vocabulary:** 13-row mapping table (subpart key → section-level key)
**Cross-references:**
- Phase 4-new implementation prompt Rule 4 validator consumes this table; mechanics live in prompt per Concept 31

**Status:** clean
**Last touched:** Session 4, commit 1c5379b

### Concept 15. Voice-map persona-bias metadata
**Canonical:** voiceMap.md §6 zone table lines 217-238 (per-zone bias directional rules) + §7 Persona bias rules lines 244-274
**Vocabulary:** per-persona directional rules keyed to §7 section-level zone vocabulary; conversion-critical zones (Concept 9) unchanged
**Cross-references:**
- composition-plan-schema.md §4.2:186 — cites voiceMap.md lines 186-196 (fragile line reference per Concept 9 flag)

**Status:** flagged
**Last touched:** pre-Session-1
**Flag note:** shared flag with Concept 9 on the line-number fragility of schema §4.2:186 citation. Non-blocking.

### Concept 16. Italic word-class vocabulary (persona-indexed)
**Canonical:** emotional-arc.md "Italic word-class vocabulary (persona-indexed)" subsection (inserted post-6-column bias table, pre-Notes section)
**Vocabulary:** closed 4-value enum {place, name, tenure, trade-term}; per-persona favored-class table (neighborhood-steady favors place+tenure; earned-pride favors name+trade-term; quiet-confidence favors tenure+trade-term; modern-specialist favors trade-term; urgent-service uses none — italic-color-shift is not Tier 1 for this persona)
**Cross-references:**
- composition-plan-schema.md §5.3.4:426 — italicPlacements class field cross-references this subsection post-Session-4
- typography.md §15 Check 9 — cites the 4-value enum post-Session-4
- voiceMap.md:426 — Phase 6 Check 1 prose cross-references this subsection via "persona's word-class list per emotional-arc.md"
- Phase 4-new implementation prompt select_italics.py module spec

**Status:** clean
**Last touched:** Session 4, commit 03ca705 (Item 1 canonical home + schema + typography.md updates)

### Concept 17. Persona bias table (6-column)
**Canonical:** emotional-arc.md Persona-to-layout bias table lines 232-243 (post-Gate-1 + Session-4 row label alias)
**Vocabulary:** 6 columns × 5 personas — Tier 1 compositional default, Tier 2 motion defaults, Editorial layouts (weighted), Photo role emphasis, Copy density; tie-breaking paragraphs at lines 256-262
**Cross-references:**
- Phase 4-new implementation prompt select_persona.py + resolve_signatures.py cite this table

**Status:** clean
**Last touched:** Session 4, commit de32fc2 (Rescue-ready row label alias)
**History:** Session 3 commits 411e30a + 949de45 (Gate 1 + polish)

### Concept 18. Typography pattern system
**Canonical:** typography.md (965 lines, 17 sections) covering three-voice system, scale, role classes, mono/italic/sectionOpener/StatRow patterns, persona-conditional font tables, Phase 5 generation rules, Phase 6 checks
**Vocabulary:** section ToC — §1 three-voice type system, §2 scale, §3 role classes, §4 mono eyebrow two-register, §5 italic discipline, §6 SectionOpener, §7 StatRow, §8 body measure, §9 mobile scaling, §10 font loading, §11 persona-conditional font selection, §12 conflict pairs, §13 pullquote heuristic, §14 Phase 5 generation rules (Rule 1-9 index), §15 Phase 6 verification checks, §16 ornament rule, §17 structural HTML contracts
**Cross-references:**
- 17 live citations from schema, SKILL.md, css-framework.md updated to typography.md references post-Session-4 (detail in commit 94c6acf)
- 3 merge-log references in typography.md itself (lines 5, 935, 965) correctly cite Stage II archive and remain unchanged
- composer-stage-ii-typography-source/typography-patterns.md — Stage II source-of-record archive (pre-merge Design in-flight v0.7.2)

**Status:** flagged
**Last touched:** Session 4, commit 94c6acf (17 live citation renames + 2 semantic replacements + 1 specific Rule 4 citation)
**History:** Stage II (d) merge output (pre-Session-1 era in Composer's session numbering)
**Flag note:** one historical-provenance reference at composition-plan-schema.md:630 (inside §12 Deferred item carried forward) retains the "typography-patterns.md" spelling because the text describes the pre-merge source as historical context, same pattern as typography.md merge-log references. Optional future nit: reshape the §630 prose to name the provenance explicitly (e.g. "Design's typography-patterns.md framing [Stage II (d) source, now merged into typography.md §3/§4]").

### Concept 19. Pullquote heuristic
**Canonical:** typography.md §13 Pull-quote detection heuristic lines 577-605
**Vocabulary:** 8-20 word bound + 2-of-5 signal rule; rhetorical-slot dedup
**Cross-references:**
- composition-plan-schema.md §4.5:216-231 — schema and budget per page
- voiceMap.md §11:363-385 — voice-layering composition, defers to typography.md for detection mechanics
- typography.md §14 Rule 5 — placement guidance
- composer-backlog.md — Fixture 2 pullquote word-count retrofit-or-grandfather decision (32-word quote vs. 8-20 bound); Checkpoint 2 resolution pending

**Status:** deferred
**Last touched:** Stage II (d) merge
**Flag note:** Fixture 2 Kingsley Pool carries a 32-word pullquote in its expected composition-plan; the 8-20 bound flags this as adherence failure. Per Design Q2 Session 3 close, fixtures are authored intent; Phase 4-new LLM authoring honors 8-20 bound. Retrofit-or-grandfather decision surfaces at Checkpoint 2 when Design reviews Phase 4-new output.

### Concept 20. Eyebrow deployment rules
**Canonical:** composition-plan-schema.md §4.6 line 233 (field schema) + §10 Phase 6 Checks 3 and 4 lines 585-586 (enforcement rules)
**Vocabulary:** eyebrowDeployments[] array with per-entry fields; count ≤3 per page; only on sectionOpener (banned on servicesGrid, FAQ, contact form)
**Cross-references:**
- Phase 4-new implementation prompt deploy_eyebrows.py module spec

**Status:** clean
**Last touched:** pre-Session-1

### Concept 21. Display moment thresholds
**Canonical:** composition-plan-schema.md §4.9 line 269 (field schema) + §10 Check 8 line 590 (threshold)
**Vocabulary:** targetDesktopPx >= 80, targetMobilePx >= 56
**Cross-references:**
- typography.md §15 Check 8 — rendered verification
- SKILL.md:527-548 — over-constraint escape hatch references threshold

**Status:** clean
**Last touched:** pre-Session-1

### Concept 22. Hero-pattern system
**Canonical:** hero-patterns.md (795 lines covering 4 hero modes + video augmentation)
**Vocabulary:** heroMode values implicit via section headings (parallax, glass-crossfade, glass-single-mesh, glass-pure-mesh); heroGlassVariant {none, narrow, wide} per composition-plan-schema.md §5.3.1:360
**Cross-references:**
- SKILL.md:302-346 — hero mode decision tree + glass card variant selection

**Status:** clean
**Last touched:** pre-Session-1

---

## Group 4 — Page / section concepts

### Concept 23. Section type enums
**Canonical:** composition-plan-schema.md §5 line 299 + §5.1/§5.2/§5.3 contracts; §5.3.1-§5.3.4 carry full contracts per Gate 4 ec8349f
**Vocabulary:** statRow (§5.1), sectionOpener (§5.2), hero (§5.3.1), servicesGrid (§5.3.2), testimonialsSection (§5.3.3), aboutStory (§5.3.4), featuredPullQuote, anchorStrip — plus 6 stub types (faqSection, beforeAfter, anchorStrip, trustSection, contactForm, footerSection) without §5.3 contracts
**Cross-references:**
- section-patterns.md (1970 lines) — design/composition notes per section type
- Phase 4-new implementation prompt emit_minimal_section.py handles stub types
- composer-backlog.md — §5.3 remainder contracts deferred

**Status:** deferred (6 stub section types)
**Last touched:** Session 5 (Commit 2 §5.3.4 about-page-body saturday-morning-all-personas supersession + about-page-body-slot voice assignment note)
**History:** pre-Session-1 (§5/§5.1/§5.2 authoring); Session 3 commit ec8349f (Gate 4 §5.3.1-§5.3.4 four contracts)
**Flag note:** 6 stub section types use fixture-observed shape in Phase 4-new; formal §5.3 contracts deferred until real-build demand per brain session block.

### Concept 24. Heading hierarchy contract
**Canonical:** composition-plan-schema.md §4.1 line 157
**Vocabulary:** {h1: string, h2Sequence: [{id, text, sectionType}]}
**Cross-references:**
- COMPOSER_BRAIN.md §7 item 2 — SEO/GEO heading hierarchy rules
- Phase 4-new implementation prompt emit_heading_hierarchy.py module spec

**Status:** clean
**Last touched:** pre-Session-1

### Concept 25. Photo role assignments + eligibility
**Canonical:** profile-schema.md §10.1 line 275 (8-role closed enum on eligibleRoles[]); composition-plan-schema.md §4.3 line 188 + §8 line 498 (assignment + fallback paths a/b)
**Vocabulary:** 8 roles on profile side; per-section photo-role expectations per §5.3; fallback-path-a (content-match success) vs fallback-path-b (content-match failure, placeholder)
**Cross-references:**
- image-handling.md (960 lines) — content-match heuristic + 4-role discipline
- COMPOSER_BRAIN.md §4 addendum — path-a/path-b contract
- Phase 4-new implementation prompt assign_photos.py module spec

**Status:** clean
**Last touched:** pre-Session-1

### Concept 26. Page-level voiceZones[] shape
**Canonical:** composition-plan-schema.md §4.2 line 172
**Vocabulary:** array of {zone (§7 15-enum), defaultVoice, personaBiasApplied, resolvedVoice, biasReason}
**Cross-references:**
- voiceMap.md §Phase 6 checks — reads data-voice attribute on rendered DOM
- composition-plan-schema.md §4.2:186 — line-number cross-reference to voiceMap.md (Concept 9/15 flag)
- Phase 4-new implementation prompt resolve_voice_zones.py module spec

**Status:** clean (shared line-number fragility per Concepts 9 and 15 remains on that single citation)
**Last touched:** pre-Session-1

### Concept 27. ScaleContrast shape
**Canonical:** composition-plan-schema.md §14:683 (intent-spec enum high/medium/low at fixture grain); composition-plan-schema.md §4.10 lines 285-295 (emission object {minimumRatio, achievedRatio, achievedBy})
**Vocabulary:** intent enum {high, medium, low}; emission fields per §4.10
**Cross-references:**
- typography.md §2 Scale relationships — persona-conditional minimum ratios authority
- typography.md §11 Persona-conditional font selection — cross-reference for ratio derivation
- Phase 4-new implementation prompt Rule 5 — threshold map high→7.0, medium→4.5, low→3.0; threshold-GE validator behavior

**Status:** clean
**Last touched:** Session 4, commit 94c6acf (§4.10 citations updated to typography.md §2)

### Concept 28. LayoutSequence shape + derivation
**Canonical:** composition-plan-schema.md §14:684 (field named in intent-spec list); no dedicated section
**Vocabulary:** ordered list of section-type enums per §5.3; derivation = sections.map(s => s.type)
**Cross-references:**
- Phase 4-new implementation prompt Rule 6 derivation

**Status:** clean (thin concept, minimal spec)
**Last touched:** Session 3, commit 296150a (§14 intent-spec listing)

### Concept 29. Constraint relaxation vocabulary
**Canonical:** SKILL.md §Over-constraint escape hatch lines 513-557 (examples and general pattern)
**Vocabulary:** constraintRelaxations[] array with {rule, detail, severity}; severity levels observed in fixtures {info, plus structural-blocker marks when constraintsOK=false}; rule-name enum NOT closed on disk — authored case-by-case
**Cross-references:**
- composition-plan-schema.md §14 editorial partition line 716 — detail prose is editorial; rule name is structural
- Phase 4-new implementation prompt detect_over_constraint.py module spec

**Status:** flagged
**Last touched:** pre-Session-1
**Flag note:** rule-name enum isn't closed. SKILL.md enumerates example reasons via the over-constraint escape hatch but does not define a complete list. Phase 4-new detectOverConstraint will emit rule names Phase 4-new chooses; validator Pass 1 compares fixture rule names to emitted rule names. May need closed enum before Phase 4-new emits at Gate E for adherence-check sanity. Flagged for Gate E resolution; non-blocking for Gates A-D.

---

## Group 5 — Validator / contract concepts

### Concept 30. Three-pass validator contract
**Canonical:** composition-plan-schema.md §14 lines 613-672 (three-pass architecture, editorial vs structural vs intent-spec partition, precedence note)
**Vocabulary:** Pass 1 structural equality; Pass 2 semantic derivation (6 intent-spec fields); Pass 3 editorial adherence
**Cross-references:**
- Phase 4-new implementation prompt Rules 1-6 (mechanics per Concept 31)
- Phase 4-new implementation prompt encodes ValidationResult + three mismatch classes
- scripts/fixture_validator.py — on-disk implementation (552 lines, self-check mode runs against F1-F6 fixtures per §14 three-pass contract; editorial-adherence pass skipped in self-check per Session 3 Q2 close)

**Status:** clean
**Last touched:** Session 5 (Commit 3 Gate A: fixture_validator.py landed on disk, self-check green on all 6 fixtures)
**History:** Session 4 commit 4c117cb (§14 amendment from Q2 close two-pass → three-pass)

### Concept 31. Rule 1-6 derivation mechanics
**Canonical:** Phase 4-new implementation prompt (paste artifact, not on disk) — contains detailed mechanics per Session 4 Option B
**Vocabulary:** Rule 1 pathConvention object-shape derivation; Rule 2 tier enum + side-channel; Rule 3 microInteractionDurations two-row lock lookup (also canonical in emotional-arc.md per Concept 6); Rule 4 voiceZone flatten per §7 mapping table; Rule 5 scaleContrast threshold map; Rule 6 layoutSequence derivation from sections
**Cross-references:**
- composition-plan-schema.md §14:624-629 — names six intent-spec fields routing to Pass 2; does not carry mechanics
- composer-backlog.md — Path A migration deferred, Rule 4 from Session 4 Concern 4 reshape as template shape (input/emission/validator/derivation/error-class) for future migration

**Status:** deferred
**Last touched:** Session 4, commit a35b96f (backlog entry for Path A deferral); Rule 4 text authored but lives in prompt not §14 per Option B call
**Flag note:** mechanics live in the implementation prompt per Option B. When Path A migration happens in a later session, Rule 4's template shape applies to the other five rules; migration content comes from the prompt's existing Rule 1-6 block, NOT from re-authoring. Cross-check required at migration time: on-disk §2.2 pathConvention shape, SKILL.md tier enums (Premium/Professional/Standard), §4.10 scaleContrast emission shape. Every future reshape touching Rules 1-6 mechanics is subject to prompt-schema drift class until Path A migrates.

### Concept 32. Editorial vs structural vs intent-spec field partition
**Canonical:** composition-plan-schema.md §14 partition table lines 714-718
**Vocabulary:** three-row table listing fields per partition
**Cross-references:**
- Phase 4-new implementation prompt field lists in architecture preamble (synchronized to §14 partition table)

**Status:** clean
**Last touched:** Session 4, commit 4c117cb

### Concept 33. Approval gate UI spec
**Canonical:** COMPOSER_BRAIN.md §9 lines 245-259 (core spec) + Phase 4-new implementation prompt Gate F section (three signed-off Session 3 reshapes: constraintsOK ordering, italic nomenclature, show-derivation command)
**Vocabulary:** per-section layout selection surface, voice-map zone assignment surface, per-page display-moment confirmation, italic-word review pick-or-confirm, eyebrow deployments surface, signature micro-interaction placement, scale contrast targets
**Cross-references:**
- Phase 4-new implementation prompt render_approval_gate.py module spec at Gate F

**Status:** clean
**Last touched:** Session 3 three reshapes (constraintsOK ordering above header, italic status nomenclature renames, show-derivation command)

### Concept 34. Phase 6 check suite
**Canonical (structural):** composition-plan-schema.md §10 lines 522-611 (13-check invariant table, structural vs rendered split)
**Canonical (editorial):** typography.md §15 lines 680-742 (13 editorial verification checks)
**Canonical (integration + P6.1-P6.4):** phase-6-integration.md (153 lines — P6.1 authored Stage II (f); P6.2-P6.4 spec-only)
**Vocabulary:** 13 checks per authoring surface; not contradictory but not trivially unified
**Cross-references:**
- SKILL.md Phase 6 lines 686-761 — check execution sequence
- COMPOSER_BRAIN.md §6 — Component A patch inventory references check structure

**Status:** flagged (three authoring surfaces)
**Last touched:** Stage II (f) authoring (P6.1)
**Flag note:** The 13-check count coincides across schema §10 and typography.md §15 but the two are different check sets; a reader must not treat them as the same 13. Three authoring surfaces total — structural invariants at schema §10, editorial checks at typography.md §15, integration/implementation at phase-6-integration.md. Future reshape consideration: unify into one canonical authority that cross-references implementation surfaces, or name the three authoring surfaces explicitly in a "Phase 6 check suite architecture" section. Non-blocking for current gates.

### Concept 35. SEO/GEO preservation contract
**Canonical:** COMPOSER_BRAIN.md §7 lines 152-172 (7-point contract)
**Vocabulary:** 7 preservation rules covering schema validity, heading hierarchy, structured data, canonical URLs, metadata, sitemap, robots
**Cross-references:**
- seo-geo.md (1431 lines) — implementation details
- phase-6-integration.md — Phase 6 Check 4 schema-HTML consistency

**Status:** clean
**Last touched:** Session 1 brain authoring

### Concept 36. Schema versioning approach
**Canonical:** COMPOSER_BRAIN.md §14 lines 333-348; composition-plan-schema.md §9:510; profile-schema.md §15:374
**Vocabulary:** $schemaVersion "1.0" top-level in instances + schemaVersion frontmatter in -schema.md files; registry at docs/composer/schema-versions.md seeded Stage II (c)
**Cross-references:**
- docs/composer/schema-versions.md — registry

**Status:** clean
**Last touched:** Stage II (c)

### Concept 37. Fixture intent-spec authoring slots
**Canonical:** backlog-only, no current authoritative text — referenced at composer-backlog.md as "Fixture-side authoring slots as a named §2 concept (deferred)" post-commit a35b96f
**Vocabulary:** if landed, would include personaIntent, voiceZoneIntent[], italicIntent[], pullQuoteIntent, eyebrowIntent[], microInteractionIntent
**Cross-references:**
- composer-backlog.md backlog entry (Session 4 Concern 4 sidebar flag)

**Status:** deferred
**Last touched:** Session 4, commit a35b96f (backlog flag)
**Flag note:** Design flagged during Concern 4 reshape that these fixture-side slots could land as a canonical named concept in composition-plan-schema.md §2 where fixture shape lives. Distinct from the six intent-spec fields in §14 (structural-derivation output set). Not authored — if Phase 4-new execution surfaces a need to reference these slots by canonical name, the reshape has a known home.

---

## Group 6 — Process / meta concepts

### Concept 38. Migration sequence (Stages I-VI)
**Canonical:** COMPOSER_BRAIN.md §8 lines 174-243
**Vocabulary:** Stage I scoping (closed 2026-04-21); Stage II reference files (closed Sessions 1-2); Stage II.5 fixtures (closed Session 3); Stage III Phase 4-new (in progress Session 4); Stage IV Phase 5-new (scoped for post-Session-4); Stage V Luna validation; Stage VI retirement decision
**Cross-references:**
- COMPOSER_BRAIN.md PART II session blocks — per-session progress against stages

**Status:** clean
**Last touched:** Session 4 brain session block 2026-04-22

### Concept 39. Handoff contract
**Canonical:** COMPOSER_BRAIN.md §4 lines 66-91
**Vocabulary:** three-stage contract Phase 3 → Phase 4-new → Phase 5-new → Phase 5.5 → Phase 6
**Cross-references:**
- handoff-discipline.md (291 lines) — operational/discipline rules

**Status:** clean
**Last touched:** Session 1 brain authoring

### Concept 40. Component A patch inventory
**Canonical:** COMPOSER_BRAIN.md §6 lines 105-150
**Vocabulary:** 6 patch items covering Phases 0-3, 5.5, 6-8 (P0.1-P8.1 naming)
**Cross-references:**
- SKILL.md Phase 6 lines 686-761 — implementation of Phase 6 patches

**Status:** clean
**Last touched:** Session 1 brain authoring

### Concept 41. Foundation decision
**Canonical:** COMPOSER_BRAIN.md §5 lines 92-103
**Vocabulary:** design-skill as foundation + Wave 1/Wave 2 backport (locked pre-Session-1 with Design + Code signoff)
**Cross-references:** none (architectural decision, not operationalized as ongoing reference)

**Status:** clean
**Last touched:** Session 1 brain authoring

### Concept 42. Stage V go/no-go rubric
**Canonical:** COMPOSER_BRAIN.md §10 lines 261-285; Stage VI at §11 line 287
**Vocabulary:** both pillars independently rated (Pillar 1 editorial Luna F8 baseline; Pillar 2 SEO/GEO Lighthouse ≥95 + schema validity); soft-fail review beat authored; retirement criteria Stage VI at §11
**Cross-references:**
- COMPOSER_BRAIN.md §6 Component A — P6.2 soft-fail review beat at Checkpoint 4

**Status:** clean
**Last touched:** Session 1 brain authoring

### Concept 43. LESSONS — accumulated session observations
**Canonical:** composer-backlog.md LESSONS section (Active list)
**Vocabulary:** seven patterns accumulated across Sessions 3 and 4 — (1) cross-grain reconciliation needs dedicated checkpoint beat; (2) Design asks for on-disk text before authoring mechanics / Chat-Claude routes with disk state not summary; (3) Code's halt-don't-press-through discipline preserved across gates; (4) partial-surface reads do not license whole-file generalizations; (5) surface-level fixes do not license assuming drift is localized; (6) architectural reshapes need three lenses not two; (7) narrow scope surfaces halts earlier when halts are cheaper
**Cross-references:**
- This authority map, the institutional instrument the LESSONS entries point toward

**Status:** clean
**Last touched:** Session 5 Commit 7 (watch-surface 1 added to composer-backlog.md LESSONS + Pattern 4 path-check sub-discipline sub-bullet atomic; Vocabulary unchanged since watch-surface 1 is candidate not pattern)
**History:** Session 4 commits 2bb6a0b (Patterns 1-3 LESSONS entry initial landing) + 4696af0 (Pattern 4 added); Session 5 Commit 5 (Patterns 5+6+7 added — surface-level fix scope, triad lens discipline, narrow scope enforcement; first enforcement test of authority map atomic maintenance contract); Session 5 close-out added watch-surface 1 (self-flag-ship) to composer-backlog.md pending recurrence, Concept 43 Vocabulary unchanged; Session 5 close-out added path-check sub-bullet under Pattern 4

---

*End of authority map. Next update triggers on the next reshape that touches two or more concepts in different groups per the maintenance contract above.*

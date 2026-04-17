# GRM v0.7.4 Patch Cycle — Session Handoff
# Date: 2026-04-17 evening → 2026-04-18 morning session
# Author: Claude (web session) → Claude Code (next session)
# Scope boundary: v0.7.4 patch cycle ONLY. No retrofit. No sales enablement work. No F7.

## STATE OF THE FLEET AS OF TONIGHT

Six flagships live, all sales-safe, all git-tracked. Zero known blocking bugs.

F1 T&F Electric · tandf-electric-v07-[hash].vercel.app · era-one · awaits v0.8 retrofit
F2 A-1 Payless Septic · a-1-payless-septic-grm.vercel.app · era-one · overflow hotfixed tonight · awaits v0.8 retrofit
F3 Chad's Lawn and Landscape · chads-lawn-and-landscape-grm.vercel.app · era-two · contact-grid hardened tonight
F4 Grandview Inc · grandview-inc-grm.vercel.app · era-two · grade-stakes footer phone hotfixed tonight · contact-grid hardened tonight
F5 A Quality Pool Service · a-quality-pool-service-grm.vercel.app · era-two · contact-grid hardened tonight
F6 Oxford Lawn · oxford-lawn-grm.vercel.app · era-two · contact-grid hardened tonight

Workspace slugs (verify against disk before any prompt references — slug drift caused one paused step tonight):
  ls ~/grm-sites-prospects/ confirms: tandf-electric-v07, a-1-payless-septic-service-inc, chads-lawn-and-landscape, grandview-inc, a-quality-pool-service-llc, oxford-lawn

Skill version: v0.7.3 + hotfixes #10 (skip-link) and #11 (Phase 0 git tracking). Changelog in SKILL.md is current as of tonight.

## v0.7.4 SCOPE — 18 FINDINGS

Execution order below is deliberate. Finding #24 goes first because it governs every later retrofit decision.

### TIER 1 — GOVERNANCE (must come first)

**Finding #24 — Retrofit doctrine decision tree.**
Context: F1, F2, F3 are era-one flagships that will be retrofit in the Sunday session. Without a written rubric for rebuild-vs-patch-vs-archive, scope will re-litigate mid-flight. Code surfaced this in reflection.
Patch: Create ~/.claude/skills/prospect-site/references/retrofit-doctrine.md. Define three paths — full regenerate, surgical patch, archive-and-rebuild — with triggers for each based on (a) age of original build, (b) number of era-divergence points vs current skill, (c) whether prospect was pitched from the preview URL. Decision authority: Ron unilaterally, skill provides recommended path.
Priority: must-ship. Governs Sunday.

### TIER 2 — PREVENTION GAPS (must-ship)

**Finding #2 — Em dash pre-write filter.**
Context: Chronic. F5 shipped 6 caught at Phase 6, F6 shipped 8 caught at Phase 6. Pre-write intent has failed two builds in a row. Em dashes are a Phase 5 generation problem masquerading as a Phase 6 catching problem.
Patch: Phase 5 generation rules — prohibit em dash character in any output string at generation time, not at Phase 6 validation time. Replace with appropriate punctuation or rephrase. Phase 6 check becomes redundant/backup rather than primary gate.

**Finding #3 — Heading hierarchy depth validator.**
Context: F1 and F4 both jump H2→H4 inside FAQ `<details>` with no H3 wrapper. Current Phase 6 validates H1=1 but not depth.
Patch: Phase 6 new check — parse heading sequence on every page, fail if any skip (H1→H3, H2→H4, etc.).

**Finding #4 — Evidence density threshold for claims.**
Context: F5 nearly shipped cpoHeld=true based on single source mention; caught at Phase 4 by Ron. Boolean credential fields AND non-boolean claims (years in business, specific numbers) need the same threshold.
Patch: Phase 1 data extraction — any boolean credential field or numeric claim must have evidence density ≥2 distinct source mentions before being promoted to profile.json. Single-mention claims flag for Phase 4 approval, not auto-inclusion.

**Finding #5 — data-reveal scoping as hard rule.**
Context: F5 shipped page-level .prose wrapper with data-reveal causing invisible mobile content. Currently a soft pattern; needs to be hard-rule.
Patch: Phase 5 generation — data-reveal attribute permitted on section-level elements only. Never on .prose, never on containers taller than ~5000px at 375px viewport width. Phase 6 check validates.

**Finding #9 — Hash dedupe as Phase 3 hard rule.**
Context: F5 shipped photo-07 byte-identical to photo-08 until caught at Phase 6. F6 applied dedupe preemptively (0 dupes found). Needs to be mandatory Phase 3 step, not optional.
Patch: Phase 3 photo inventory — SHA-256 every captured photo, reject byte-identical duplicates before hero slide selection. Mandatory.

**Finding #13 — Tap-target size enforcement.**
Context: 25-40% pass rate on WCAG 44×44px minimum across all six flagships. Systemic, not build-level. Footer links, social icons, FAQ chevrons, nav sub-items all under-size.
Patch: Phase 6 check 15 expansion — measure every `<a>`, `<button>`, `<summary>` at 375px viewport via Playwright, fail build if >10% under 44×44. css-framework.md additions: min padding on footer list items, min-height on FAQ summary elements, social icon buttons at 44px minimum.

**Finding #14 — Hero visual aria-label requirement.**
Context: All six flagships render hero photos via CSS background-image on crossfade slides. Zero screen reader coverage, zero semantic meaning for AI crawlers, degraded social-share metadata. Hero is the visually dominant content with zero alt text.
Patch: hero-patterns.md — every .hero-crossfade-slide element requires aria-label describing the scene. Pull text from same alt-text source the gallery already uses. Phase 6 check validates every background-image hero slide has aria-label or associated visually-hidden description.

**Finding #18 — Contact-grid minmax hardening in skill.**
Context: F2 shipped 44px mobile overflow from bare fr grid tracks. F3-F6 latent on same bug, patched tonight. Skill still produces the unhardened pattern.
Patch: section-patterns.md (or wherever contact section is specified) — contact-grid and contact-container tracks always wrapped in minmax(0, fr-value) on desktop and mobile.

**Finding #20 — Contact section class name canonicalization.**
Context: F3 uses .contact-grid, F4/F5/F6 use .contact-container. Same structural component, two class names depending on skill version. Cosmetic naming drift.
Patch: section-patterns.md — decide canonical name (.contact-container matches the majority and is more descriptive). All future builds use canonical. Document the prior name for retrofit reference.

### TIER 3 — MULTI-DIVISION SUPPORT (must-ship)

**Finding #15 — Multi-division phone surfaces rule.**
Context: Grandview F4 has two phones for two divisions. On grade-stakes.html, every phone surface (nav, hero, CTA, mobile CTA) resolved to the grade-stakes number EXCEPT footer brand-phone block, which retained the landscaping number. Hotfixed tonight.
Patch: Phase 5 HTML generation — when profile.json defines multiple phones tied to distinct divisions and a subpage represents a specific division, override the sitewide footer-phone default with the division phone for that subpage.

**Finding #16 — Multi-division footer tagline copy variant.**
Context: Current tagline "the phone number haven't changed" (singular) mismatches multi-division subpages where the footer phone differs from siblings.
Patch: content-rules.md — define a plural-aware tagline variant for businesses with multiple division phones. Phase 5 picks variant based on profile.json phone structure.

### TIER 4 — FLEET COHERENCE (must-ship)

**Finding #21 — Template rotation sets.**
Context: Meta descriptions, FAQ answers, hero subheads converge on detectable formulas across the fleet. Individually pass anti-slop; read as fleet, a prospect seeing two GRM sites would notice. Code surfaced in reflection.
Patch: content-rules.md — define 2-3 sanctioned templates per surface (meta description, FAQ closer, hero subhead). Phase 5 rotates selection based on project hash so two consecutive builds don't use the same template.

**Finding #8 — Inner-page anchor photos as hard rule.**
Context: F5 and F6 render About and Services anchor photos with strong pattern effect. F3-F4 do not. Currently soft pattern.
Patch: Phase 5 generation — if heroCandidates ≥ 6, About and Services pages receive anchor photos as mandatory, not optional. section-patterns.md documents the requirement.

**Finding #11 — Single-service Bento variant codified.**
Context: F6 Oxford Lawn adapted the services grid for a one-service business (1 featured + 4 standard rendering 3 sub-processes + free assessment). Worked well, not documented.
Patch: section-patterns.md — document the single-service Bento variant as a named pattern with the 1+4 structure. Phase 4 design plan auto-selects when profile.json services.length === 1.

**Finding #12 — Hours mismatch automated check.**
Context: F5 and F6 both had site-published hours differing from Google Places hours — valuable sales ammo. Currently caught manually at profile review.
Patch: Phase 2 addition — cross-check prospect site hours vs. Google Places hours, surface any mismatch to Phase 8 done-report as sales ammo.

### TIER 5 — INSTITUTIONAL MEMORY (must-ship)

**Finding #22 — Per-workspace STATUS.md and fleet-state.json.**
Context: Findings currently fragment across build-notes.md, LESSONS.md, and profile.json with no index. Hotfix #10 missed changelog because of this drift. Code surfaced in reflection.
Patch: Phase 8 generates STATUS.md per workspace with current state, deployment alias, known findings, last-modified timestamps. Fleet-level script generates fleet-state.json from all STATUS.md files. Single source of truth.

**Finding #23 — designOverrides[] structured capture.**
Context: Every Phase 4 override carries information the skill could use. Currently lives in conversation summary and nowhere else. Code surfaced in reflection.
Patch: Phase 4 approval gate — when Ron overrides any default, write structured record to profile.json designOverrides[] array with {at, what, chosen, rejected, reason}. Retrievable history even if skill doesn't auto-learn.

## OPERATING PRINCIPLES FOR THIS SESSION

These shaped tonight's work. Carry forward.

1. Diagnostic-first on every patch. Read-only investigation before any write. Report findings, wait for approval, execute.

2. Single-file-per-prompt discipline. Compound patches touching multiple files in one exchange get rejected. Clean rollback granularity per logical change.

3. Slug verification from disk as step zero. `ls ~/grm-sites-prospects/` and `ls ~/.claude/skills/prospect-site/` before any prompt references a path. Slug drift cost one paused step tonight.

4. Fix-it-right over fix-it-fast. If something seen during a patch is a real problem, fix it now. Don't defer to "later" cycles. Three times tonight Ron caught Claude deferring real problems; all three got fixed and the fleet is better for it.

5. Phase 6 catches assertible defects; phone catches felt defects. Don't assume automation is a substitute for the phone gate or vice versa. Both are required.

6. Automate the obvious, preserve judgment. Finding #4 automates the obvious (credential inflation). Phase 4 approval gate preserves judgment (taste, editorial framing, positioning). Do not over-optimize toward eliminating approval gates.

7. Git-tracked workspace commits before every redeploy. One logical change per commit. Hotfix workflow is documented in SKILL.md as of hotfix #11.

## SESSION SEQUENCE

Saturday AM: This session. v0.7.4 patch cycle ONLY. All 18 findings. Exit criterion: v0.7.4 tagged, changelog updated, all skill files committed, test build run if time permits.

Saturday PM: Ron works sales enablement independently (HubSpot teardown and rebuild, getrootedmedia.com Storefront landing page, additional sales assets). Claude available as support on demand.

Sunday: Separate Code session. F1/F2/F3 retrofit using retrofit-doctrine.md from Finding #24. Produces fleet-wide era-two coherence.

Later: F7 on v0.7.4.

## START OF SESSION DIAGNOSTICS

Before Finding #24 patch begins, confirm:

1. head -1 ~/.claude/skills/prospect-site/SKILL.md
2. cd ~/.claude/skills/prospect-site/ && git log --oneline -5
   Expected (newest first): 0b6c90d housekeeping, ee78068 v0.7.3 hotfix #11, b4591c8 v0.7.3 hotfix #10
3. ls ~/grm-sites-prospects/ — confirm six workspace slugs
4. Read this handoff doc in full before proposing patch #1

Wait for Ron's confirmation before beginning Finding #24.

## END OF HANDOFF

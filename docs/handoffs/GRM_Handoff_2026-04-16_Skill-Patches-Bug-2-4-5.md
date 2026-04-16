# GRM Handoff — Skill Patches: Bugs 2, 4, 5
**Session date:** April 16, 2026 (Thursday morning)
**Author:** Ron + Claude
**Session length:** ~2 hours
**Session summary:** Patched three v0.7.1 bugs before building flagships 3-6. Nine commits, zero scope creep.

## What shipped

Three bugs from the A-1 Payless Septic flagship (2026-04-15) are now fixed in the live skill at ~/.claude/skills/prospect-site/. All bugs were diagnosed with read-only diagnostics before any fix was written. The standing rule from Monday ("no skill engineering until sales kickoff") was deliberately revised for scoped, named fixes.

### Bug 2: CTA trailing-fragment hallucination (3 commits)
- **Root cause:** Claude Code hallucinates SMS-style fine-print below CTA buttons during Phase 5 generation. Not a template flaw — skill templates are clean.
- **Layer 1 (059f1f7):** Banned pattern added to anti-slop-rules.md with examples and v0.7 rules.
- **Layer 2 (a2cf01c):** Local reinforcement bullets at hero, promo-callout, and mobile bottom bar templates.
- **Layer 3 (7227ff8):** Phase 6 check #3 renamed from "GRM voice banned phrase check" to "Banned output check", expanded to grep for hallucinated HTML patterns (<small> tags, Reply within, Reply STOP, Or reply).

### Bug 4: Social metadata only on index (2 commits)
- **Root cause:** Skill's seo-geo.md template says "every page" but SKILL.md Phase 5.5 treated it as advisory. F1 shipped with 4 tags on secondary pages vs 14 on index; faq.html had zero.
- **Layer 1 (8eb6270):** Template upgraded to flagship standard (10 og + 5 twitter tags, adds og:image:width/height/alt and twitter:image:alt). SKILL.md Phase 5.5 mandate made non-negotiable.
- **Layer 2 (405bd69):** Phase 6 check #18 added — greps every page for the complete 15-tag block.

### Bug 5: Phase 7 slug regeneration (4 commits)
- **Root cause:** Phase 5 writes URLs using Phase 1 directory slug. Phase 7 may deploy under a different name. No step reconciled the mismatch. On A-1, 28 stale references including form redirectTo (breaks conversion funnel).
- **Layer 1a (7e57366):** SKILL.md Phase 7 step 4 added — slug reconciliation before deploy.
- **Layer 1b (a76bf09):** deployment.md Step 2.5 added — detailed reconciliation procedure.
- **Layer 2 (37d56b3):** Check 7.10 added — post-deploy stale-slug grep.
- **Layer 3 (498bf1f):** Done-report template shows reconciliation result.

## Skill state after this session

- Version: v0.7.1 + 9 patches (will be named v0.7.2 when ready)
- Phase 6 checks: 18 (was 17). Check #3 expanded, check #18 added.
- Phase 7 steps: 8 (was 7). Step 4 added.
- Phase 7 deployment checks: 10 (was 9). Check 7.10 added.
- Files modified: SKILL.md, anti-slop-rules.md, section-patterns.md, hero-patterns.md, content-rules.md, seo-geo.md, deployment.md

## What did NOT ship (deliberate scope decisions)

- Bug 1 (Phase 1 background-image crawl) — deferred, manual mitigation is cheap
- Bug 3 (magenta AA contrast) — caveat only, not a fix
- content-rules.md check-numbering drift (says "check 4" where SKILL.md says check #3) — logged for post-launch hygiene
- seo-geo.md check-numbering drift (internal "Check 14" doesn't match SKILL.md check #14) — logged for post-launch hygiene
- F1 `-v07` naming convention (predates `-grm` standard) — cosmetic, no action

## Next session opening sequence

1. Build F3: Chad's Lawn and Landscape (chadslawnandlandscape.com) as the validation build for all three bug fixes
2. Verify during F3: (a) zero <small> tags in generated HTML, (b) 15 social meta tags on every page, (c) slug reconciliation step fires or correctly reports no action needed
3. After F3 validates: retroactively update F2 (A-1 Payless Septic) with full social metadata, then assess F1 (T&F Electric)
4. Claude Code has Playwright available for visual auditing — use it during F3 polish pass
5. claude-mem is active — Claude Code will have session memory from today forward

## Tools and context

- claude-mem (github.com/thedotmack/claude-mem) adopted today as Claude Code's observation/memory layer
- Playwright available in Claude Code for page-level visual auditing
- F3 prospect: Chad's Lawn and Landscape, chadslawnandlandscape.com, scored 47/100 per prospect audit

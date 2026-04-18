# GRM Design Library

Source of truth for design patterns used by the prospect-site skill and
other GRM web properties. Populated by the Design → Code handoff loop
specified in the Round 1 feedback doc (Ron's Claude Design project,
April 18 2026).

## Workflow

1. Claude Design proposes patterns (per prospect or per exercise).
2. Design finalizes and ships a pattern dossier — zipped folder with spec
   cards, parent index, and visuals.
3. Ron reviews dossier, hands to Claude Code.
4. Code unpacks dossier into `rounds/round-N-[prospect]/` and begins
   implementation in a v0.8 pattern library branch.
5. Ron reviews live result, iterates with Design if needed.
6. Once a pattern is approved, its spec card moves from `rounds/round-N/`
   to `patterns/` as the canonical version.

## Folder structure

- `rounds/` — per-round dossiers from Design. Transient working directories.
  One folder per Design round, named `round-N-[prospect-or-topic]`.
- `patterns/` — canonical spec cards for approved patterns. Source of truth.
  One markdown file per pattern, matching `TEMPLATE-pattern-spec.md`.
- `TEMPLATE-pattern-spec.md` — blank spec card template. Design output
  validates against this structure.
- `TEMPLATE-round-index.md` — blank parent index template for each round
  folder's top-level index.

## First round

`rounds/round-1-oxford/` — placeholder for Round 1 Oxford pattern dossier.
Empty until Design ships.

## Related

- Prospect-site skill: `.claude/skills/prospect-site/`
- Voice skill: `.claude/skills/GRM_VOICE_SKILL.md`
- Brand rules: `brand/BRAND_RULES.md`

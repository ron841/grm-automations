# Design Round 1 — Oxford Lawn

Generated from the Oxford ceiling concept for GRM.

This dossier is the handoff artifact from Design to Code for Round 1. It contains one spec card per pattern, a parent index with build-order recommendations, and visual references.

## Structure

- `index.md` — parent pattern index with priority ranking, build order, open questions, and dependencies
- `patterns/*.md` — one spec card per pattern (22 patterns)
- `visuals/` — desktop + mobile screenshots per pattern (where applicable)

## How to use

Drop this entire folder into a Claude Code session with a paste-ready build prompt like:

> "Implement the patterns in this dossier into our v0.8 pattern-library branch. Start with the 'land first' set from index.md. Build in isolation — do not merge into the production skill until I approve each pattern live."

## Round 1 additions acknowledged

- Standalone pattern library view: see `/library.html` in the design project
- Mobile compositions: see `/mobile.html`
- Bespoke → systemizable paths: inline in each affected spec card under "Scale notes"
- Voice audit: `/library.html#voice-audit` + summarized in `index.md`
- Font audit: JetBrains Mono confirmed load-bearing across 17+ components; kept

## Round 1 Delivery

- 22 patterns total
- 14 systemizable (land first in v0.8)
- 5 bespoke (4 with named systemizable paths; soil-strata-hero has a vector-library path)
- 3 mixed (structure systemizable, content per-client)
- 3 mobile-gated (process stepper, soil strata hero, annotated cross-section) — all with planned variants

Contact: Ron Kolb, Get Rooted Media.
Date: April 2026.

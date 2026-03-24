# GRM Design Skill

## Trigger

Use this skill with /design before ANY creative work for Get Rooted Media.

## Data Sources

This skill uses a CSV database for design decisions. Load these files before any creative work:

- `.claude/skills/design/data/colors.csv` — approved palette with usage rules and banned colors
- `.claude/skills/design/data/typography.csv` — exact font, size, weight, and line-height for every text element
- `.claude/skills/design/data/ui-reasoning.csv` — anti-patterns specific to local media publishing with correct approaches
- `.claude/skills/design/data/styles.csv` — publication-specific personality for Closing Table vs Front Porch
- `.claude/skills/design/data/landing.csv` — website section guidance with visual treatment, copy direction, and conversion goals

## Required steps before building anything

Before writing any copy in this document, read .claude/skills/GRM_VOICE_SKILL.md and select the correct voice per the content-type mapping table.

### Step 1 — Load brand rules and CSV database

Read brand/BRAND_RULES.md and all 5 CSV files from .claude/skills/design/data/ — confirm:

- Primary dark: #090c0b
- Accent teal: #00b7ce
- Background: #FAF8F4
- No gold, no green, no generic real estate colors
- All typography sizes match typography.csv exactly
- Color pairings follow colors.csv never_use_with rules

### Step 2 — Review existing assets

Read these files from brand/assets/:

- logos/ — use these SVG files for all logo placements
- media-kits/ — match this visual standard
- publication-covers/ — match this photography style

### Step 3 — Confirm brand hierarchy

Every GRM document must show this hierarchy:

- GRM is the PUBLISHER (top of every document)
- Publication name is secondary (Closing Table, Front Porch)
- Content title is tertiary

Never let a content title outrank the GRM brand.

### Step 4 — Typography check

Reference typography.csv for exact values. Key rules:

- Cover titles: 36pt Bold Montserrat, white on dark bar
- Section headers: 24pt Bold, body text: 11pt Regular
- Proper word spacing — never merged words
- White text on #090c0b backgrounds
- #00b7ce for all accent text and callout elements
- Badge text: 10pt Bold, all caps, 1.5px letter-spacing
- Stat callouts: 48pt Bold teal numbers

### Step 5 — Photography direction

- Ocala/Marion County specific imagery always
- Horse farms, moss trees, springs, communities, families
- Never generic Florida stock photography
- Full bleed on cover and section opener pages
- Check ui-reasoning.csv for photo anti-patterns

### Step 6 — Publication personality check

Reference styles.csv to match the correct publication feel:

- Closing Table: authoritative, data-forward, professional
- Front Porch: warm, welcoming, community-forward

### Step 7 — Website sections (when building web pages)

Reference landing.csv for section-by-section guidance including visual treatment, copy direction, and conversion goals.

### Step 8 — Anti-pattern scan

Read ui-reasoning.csv and verify the design avoids all 12 documented anti-patterns before finalizing.

### Step 9 — State out loud before building

"Colors: #090c0b + #00b7ce + #FAF8F4 confirmed.
Logo: GRM SVG from brand/assets/logos/ confirmed.
Typography: sizes from typography.csv confirmed.
Publication personality: styles.csv checked.
Anti-patterns: ui-reasoning.csv scanned.
Brand hierarchy: GRM publisher confirmed.
Ready to build."

## Three-brand architecture

GRM has three brands — always design with this in mind:

GET ROOTED MEDIA (parent — black + teal, editorial)
├── THE CLOSING TABLE (agents — professional, authoritative)
└── THE FRONT PORCH (homeowners — warm, community)

Each publication has its own feel but shares the GRM parent brand DNA. Lead magnets and digital content should always show which publication they belong to AND that GRM is the publisher.

## Anti-patterns — never do these

Full list with reasoning in .claude/skills/design/data/ui-reasoning.csv. Summary:

- Dark forest green as primary color
- Gold as a main accent
- Logo as text instead of SVG file
- Generic real estate photography
- Words running together (font encoding issue)
- Empty bottom halves on pages (tombstoning)
- Content title bigger than GRM brand name on cover
- Half-filled pages — every page must be complete
- Badge collisions with headlines (min 8pt gap)
- Mountains or non-Florida terrain in any photo
- Duplicate photos across documents
- Unnecessary dark overlays on photos
- Em dashes in body copy
- Missing local Ocala/Marion County references

# GRM Design Skill
# Get Rooted Media — Design Advisor
# Built from Em Agency assets — March 2026
# Last updated: March 25, 2026

## Trigger
Use /design before ANY creative work for Get Rooted Media.

## Em Agency Is the Design Authority
All values in this skill come from Em Agency deliverables received March 2026.
If any AI-generated planning doc conflicts with Em Agency assets, Em Agency wins — always.

## Three-Brand Architecture
GRM has three brands. Design every piece with this hierarchy in mind:

GET ROOTED MEDIA (parent publisher — always on top, every page)
├── THE CLOSING TABLE (agents — bold, dark, authoritative, aerial photography)
└── THE FRONT PORCH (homeowners — warm, light, community, porch photography)

## Official Color System (Em Agency — LOCKED)
- #52B5CB — GRM Teal — primary accent, CTAs, dividers, teal O in Front Porch logo
- #E0A6A6 — Dusty Rose — Front Porch lifestyle sections ONLY
- #78AD4E — Sage Green — Front Porch pull quotes ONLY
- #9D8365 — Warm Brown — second O in Front Porch logo, earth tone accents
- #1A1A1A — Near Black — backgrounds, headers, body text
- #FFFFFF — White — text on dark, logo on dark
- #FAF8F4 — Warm Cream — page backgrounds, breathing space

BANNED FOREVER: #C9973A gold, #090C0B old black, #00B7CE old teal
Dusty Rose, Sage Green, and Warm Brown are Front Porch colors ONLY — never in Closing Table.

## Official Font System (Em Agency — LOCKED)
- Comfortaa — Display font. ALL CAPS for headlines and mastheads. Semibold for subheaders.
- Grand Hotel — Script accent. Used ONLY for 'The' above publication names. Nothing else.
- Merriweather Light / Italic — Editorial serif body. Feature articles, agent profiles, pull quotes.
- Nunito Regular — Body sans-serif. Body text, captions, navigation, labels, UI copy.
- Google Fonts URL: https://fonts.google.com/share?selection.family=Comfortaa:wght@400;600;700|Grand+Hotel|Merriweather:ital,wght@0,300;0,400;1,300;1,400|Nunito:wght@400;600;700

## Data Files — Load Before Any Creative Work
- data/colors.csv — official palette with usage rules and never-use-with rules
- data/typography.csv — exact font, size, weight, and line-height for every text element
- data/ui-reasoning.csv — 17 anti-patterns specific to GRM with severity ratings
- data/styles.csv — Closing Table vs Front Porch publication personality
- data/landing.csv — website section-by-section guidance with photo recommendations
- data/ux-guidelines.csv — 16 UX do/don't rules for the website build

## Required Steps Before Building Anything

### Step 1 — Identify which brand and publication
Confirm: Is this for GRM parent, The Closing Table, or The Front Porch?
This determines which colors, which photography style, and which voice applies.

### Step 2 — Load the right data files
For all work: colors.csv, typography.csv, ui-reasoning.csv
For publications: add styles.csv
For website: add landing.csv and ux-guidelines.csv

### Step 3 — Confirm color compliance
- Primary dark: #1A1A1A
- Accent teal: #52B5CB
- Background: #FAF8F4
- Dusty rose and sage green: Front Porch ONLY
- No gold anywhere

### Step 4 — Confirm typography hierarchy
- Display/Masthead: Comfortaa Bold ALL CAPS
- Script accent: Grand Hotel — only before 'The Closing Table' or 'The Front Porch'
- Body serif: Merriweather Light for editorial features
- Body sans: Nunito Regular for everything else
- Never Comfortaa for body text
- Never Grand Hotel outside of publication name treatment

### Step 5 — Select photography
Reference landing.csv for specific photo file recommendations.
Closing Table: aerial, architectural, professional, dark treatment acceptable
Front Porch: ground-level, family, community, warm golden light
Both: Marion County specific only — flat terrain, Spanish moss, horse farms

### Step 6 — Select voice
Reference GRM_VOICE_SKILL.md before writing any copy.
Closing Table content: Voice 4 (The Closing Table) or Voice 6 (The Deep Roots)
Front Porch content: Voice 1 (The Front Porch) or Voice 3 (The Welcome Mat)
Never mix voices within a single piece.

### Step 7 — Scan anti-patterns
Read ui-reasoning.csv. Check the CRITICAL and HIGH severity patterns first.
Confirm none are present in the planned design before building.

### Step 8 — State out loud before building
"Colors: #1A1A1A + #52B5CB + #FAF8F4 confirmed. Em Agency palette.
Publication: [CT or FP]. Color restrictions applied.
Fonts: Comfortaa display, Grand Hotel script (publication name only), Merriweather editorial, Nunito body.
Photography: Marion County specific, [aerial/ground-level] treatment.
Voice: [Voice number and name] selected.
Anti-patterns: ui-reasoning.csv scanned, none present.
Ready to build."

## Photo Asset Reference
Em Agency provided photography library. Key recommended photos:
- Hero (website): 1-Horse-Country-1.jpeg — two horses at golden hour, Spanish moss, flat terrain
- Downtown Ocala: 4-Ocala-1.jpeg — Ocala Square gazebo at golden hour
- Ocala park: 4-Ocala-2.jpeg — Tuscawilla Park, Spanish moss, lake reflection
- Front Porch publication: 6-Mag-Lifestyle-1.jpg — woman reading The Front Porch magazine
- Closing Table publication: 7-Closing-2.jpeg — The Closing Table magazine on dark table
- Ron (About page): DSC01296.JPG — outdoor warm smile, plaid shirt
- Cameron (About page): DSC01234.JPG — studio, linen blazer
- Ron + Cameron together: DSC01489.JPG — both outdoors, Florida sky

## Logo Files
Four SVG variants in brand/assets/logos/:
- Logo_Get_Rooted_Media-01.svg — primary logo with tree/roots/book icon + wordmark
- Logo_Get_Rooted_Media-02.svg — variant 2
- Logo_Get_Rooted_Media-03.svg — variant 3
- Logo_Get_Rooted_Media-04.svg — variant 4
Use -01 as default. Place at 220px wide, top-left of all pages and documents.

## Banned Forever
- Em dashes in any GRM copy (Voice Skill rule)
- Gold color in any design
- #00B7CE old teal (replaced by #52B5CB)
- #090C0B old black (replaced by #1A1A1A)
- Dusty rose or sage green in Closing Table materials
- Grand Hotel script for anything except 'The' before publication name
- Comfortaa for body text
- Generic non-Marion County photography
- Mountains or hills in any background photo

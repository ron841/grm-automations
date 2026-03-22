# GRM Fresh Chat Context

Last updated: Sunday March 22, 2026

## How to start any new session

Paste this into Claude:

"We are building Get Rooted Media. Read docs/GRM_Execution_Record.md from my GitHub repo ron841/grm-automations and tell me where we left off and what today's goal is."

## Current State

- FOUNDER v8: Final photo audit complete, pending Drive upload
- LISTINGS v4: Final photo audit complete, pending Drive upload
- Both PDFs passed Ronnie's visual approval (30 years magazine experience)
- Brand system fully locked in GitHub — BRAND_RULES, DESIGN_REVIEW, PDF_PRODUCTION_GUIDE all updated
- Florida Visual Identity rules locked — flat terrain, Spanish moss, no mountains

## Brand system location

All brand rules, assets, and design guides live in:
grm-automations/brand/

Key files:

- brand/BRAND_RULES.md — colors, fonts, logo rules
- brand/DESIGN_REVIEW.md — 4-step pre-build checklist
- brand/PDF_PRODUCTION_GUIDE.md — full PDF process
- brand/assets/logos/ — 4 SVG logo variants
- brand/assets/media-kits/ — CT and FP media kits
- brand/assets/publication-covers/ — cover comps
- .claude/skills/design/SKILL.md — /design skill

## Brand colors (never change these)

- Primary dark: #090c0b
- Accent teal: #00b7ce
- Background cream: #FAF8F4
- White: #FFFFFF
- NO gold, NO green, NO generic real estate colors

## Three-brand architecture

GET ROOTED MEDIA (parent publisher — always on top)
├── THE CLOSING TABLE (agents — professional)
└── THE FRONT PORCH (homeowners — warm)

## Logo placement spec (exact)

- File: Logo_Get_Rooted_Media-01.svg
- Width: 220px
- Position: 24px from left, 24px from top
- Color: white (#FFFFFF) on ALL paths
- Fallback: try 02, 03, 04 if 01 fails

## Contact info

- Ron Kolb — Publisher: 352-598-7289 / ron@getrootedmedia.com
- Cameron Cowart — Sales: 352-875-0326 / cameron@getrootedmedia.com

## Manus custom instruction (already set)

Before any creative task, read brand/DESIGN_REVIEW.md and review brand/assets/ before building anything.

## What's Next in Priority Order

1. Open new chat, upload both final PDFs for one last review
2. Approve and upload to Google Drive
3. Update content-plans/ with Drive links in Claude Code
4. Build 5 ManyChat keyword automations
5. Build ManyChat welcome DM
6. Create GRM_Design_System_Complete.md
7. Activate connector hit list: Cloudinary, Pinterest, Zapier, ElevenLabs

## PDF production process (short version)

1. Tell Manus: read brand/DESIGN_REVIEW.md first
2. Reference content from content-plans/ in repo
3. Test 1 solo > approve > 1 solo > approve > batch 3
4. Check cover, page 2, last page on every preview
5. Logo: use exact spec above or fix manually in Canva
6. Common fixes: merged words, empty page halves, pillar badge collisions, wrong colors

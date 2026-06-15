# GRM Fresh Chat Context

Last updated: Monday June 15, 2026

## How to start any new session

Paste this into Claude:

"We are building Get Rooted Media. Read these two files completely before saying anything:

https://raw.githubusercontent.com/ron841/grm-automations/main/docs/GRM_Execution_Record.md

https://raw.githubusercontent.com/ron841/grm-automations/main/docs/GRM_MASTER_CALENDAR.md

Also read the voice skill. It governs everything we write:

https://raw.githubusercontent.com/ron841/grm-automations/main/.claude/skills/GRM_VOICE_SKILL.md

Tell me where we left off and what today's goal is."

## Current state as of March 24

REELS: Reel 1 posted. Reels 2 and 3 filming today. Post schedule locked in GRM_MASTER_CALENDAR.md.

MANYCHAT: 4 flows LIVE with real Drive links in PLAYBOOK and FOUNDER. FOLLOWUP and Welcome DM still to build tomorrow — 5 min total.

PDF: Fully live and shareable.

SALES: Launch Monday March 30. Reel 4 posts same morning.

SATURDAY CARRYOVER STILL PENDING:
- Meta Developer App setup
- /meta-ads-campaign skill in Claude Code
- Website build (waiting on brand assets)

## Nightly call system — REDESIGNED June 15, 2026 (calls live on the Company)

The automation runs on GitHub Actions (`scripts/grm_daily_calls.py` via `.github/workflows/nightly-calls.yml`, Sun–Thu 23:30 UTC ≈ 7:30 PM ET). It no longer runs on Ron's Mac. As of June 15 the design changed fundamentally:

**Calls left the Task system.** A company is flagged for a calling day by the date property **`grm_next_call_date`**. Ron calls from a saved Companies view, **"Today's Calls"** (filter: `grm_next_call_date is today`). There are NO CALL tasks anymore.

**Tasks are EMAIL-ONLY.** The only tasks the system creates are the next-day `Email: [Company]` follow-ups generated from emails captured in notes the day before (contact auto-matched/created and associated to the company; add `name: First Last` next to the email to name the contact; @getrootedmedia.com ignored; contacts with an open EMAIL task skipped). Each run spot-checks 3 created EMAIL tasks for contact + company associations and fails loudly if any is missing.

**Callbacks unify into the 45.** A company note like `callback: Thursday`, `call back in 2 days`, `cb friday`, `callback 6/18`, or a line starting with `call <when>` stamps `grm_next_call_date` for that day and counts toward the 45 — not stacked on top.

**The 45 is a systematic tier blend, not random:** per day **A=13, B+=14, B=4, Untiered=14** (scaled to remaining slots after callbacks; New drawn first within each tier, then eligible Connected/Attempted/Not Now; shortfalls backfill A → B+ → B → Untiered).

**Status changes ONLY on real logged work** (root-cause fix for the old drift, where queuing a task flipped New→Attempted). The new `grm_last_call_date` tracks the last real dial. A nightly worked-detection pass checks each stamped day's companies for a note or CALL logged that day; if worked, sets `grm_last_call_date` and promotes New→Attempted. Scheduling never changes status.

**Calling cadence — no call status is an exit.** Only a booked **Deal** (meeting in pipeline) or **Not a Fit** removes a company from the pool. Re-dial intervals off `grm_last_call_date`: New = now, Connected = 2+ days, Attempted = 3+ days, Not Now = 14+ days.

**June 15 reset + reseed (done):** archived 180 NOT_STARTED CALL tasks (0 remain), reset all 550 companies to New (0 Attempted), created `grm_next_call_date` + `grm_last_call_date` properties, reseeded today with 45 companies (mix A:13 B+:14 B:4 U:14). One-time reset lives in `scripts/grm_reset_reseed.py` + the guarded `reset-reseed.yml` workflow (only runs when you type `RESET-AND-RESEED`).

**Unchanged:** HubSpot token in repo secret `HUBSPOT_TOKEN` (env only, never hardcoded). Manual nightly run: GitHub → Actions → "GRM Nightly Call List" → Run workflow.

## Brand system location

brand/BRAND_RULES.md — colors, fonts, logo rules
brand/DESIGN_REVIEW.md — 5-step pre-build checklist
brand/PDF_DESIGN_PLAYBOOK.md — full PDF build spec
brand/PDF_PRODUCTION_GUIDE.md — Manus build instructions
brand/templates/FOUNDER_PAGE_MAP.md — page layout template
.claude/skills/GRM_VOICE_SKILL.md — THE voice standard
.claude/skills/design/data/ — CSV design database

## Brand colors — never change

Primary dark: #090c0b
Accent teal: #00b7ce
Background cream: #FAF8F4
White: #FFFFFF

NO gold. NO green. NO generic real estate colors.

## Three-brand architecture

GET ROOTED MEDIA (parent publisher — always on top)
├── THE CLOSING TABLE (agents — professional)
└── THE FRONT PORCH (homeowners — warm)

## Logo placement spec

File: Logo_Get_Rooted_Media-01.svg
Width: 220px
Position: 24px from left, 24px from top
Color: white (#FFFFFF) on ALL paths
Fallback: try 02, 03, 04 if 01 fails

## Contact info

Ron Kolb — Publisher: 352-598-7289 / ron@getrootedmedia.com
Cameron Cowart — Sales: 352-875-0326 / cameron@getrootedmedia.com

## What is next in priority order

1. FOLLOWUP ManyChat flow — 2 minutes, Ron builds
2. New Follower Welcome DM — 5 minutes, Ron builds
3. Confirm Manus Instagram caption rewrites before March 31
4. Meta Developer App setup — Saturday carryover
5. /meta-ads-campaign skill in Claude Code
6. Website build — starts when brand assets arrive

## Known gaps and open items from March 24 session

AI PARTNER PLAYBOOK CONTENT — NOT IN GITHUB:
The Playbook Word docs were fed directly to Manus and exist only as a finished PDF in Google Drive. Raw content is not in the repo. If the PDF ever needs to be edited or rebuilt, Ron will need to re-upload the original Word docs.
PDF location: Google Drive > GRM Content Queue
File: GRM_AI_Partner_Playbook.pdf
Drive link: https://drive.google.com/file/d/17AMZ6oSZg1YdPl-BlYHo9Kya3NRPI1xN/view

MANUS INSTAGRAM CAPTIONS — CONFIRM BEFORE MARCH 31:
We instructed Manus to rewrite 5 Instagram captions to remove em dashes and reschedule posts to March 31 afternoon. This was never confirmed complete. Before March 31 open the Instagram scheduling task in Manus and approve the rewritten captions.

OLD CONTENT-PLAN PDFs — SCRAPPED:
The content-plans/ folder has outlines for LISTINGS, FOLLOWUP, NEWOWNER, and PLAYBOOK as separate lead magnet PDFs. These are scrapped. The AI Partner Playbook is now the single lead magnet for GRM. Do not build the old PDF outlines.

DESIGN ASSETS NOT IN GITHUB:
Ron's designer delivered logos, cover comps, and spread examples. These exist locally only. Upload them at the start of the website build session so Claude can see the actual design before writing any code.

COLOR PALETTE NEEDS RESOLUTION:
Website copy doc adds expanded palette beyond original 3 colors. Before website build starts, confirm which colors are live: gold #B8860B, midnight #1A1A2E, fern #4A6741, terracotta #C17B3A. Update Design Advisor colors.csv once confirmed.

21ST.DEV MCP NOT CONNECTED:
Sign up at 21st.dev, get free API key, add to Claude Code MCP settings before website build. Gives access to production-ready React components during build.

UX-GUIDELINES.CSV MISSING:
Design Advisor needs ux-guidelines.csv with 100 UX do/dont rules. Build this before website build starts.

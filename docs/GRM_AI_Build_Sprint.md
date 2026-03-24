# GRM AI Build Sprint — March 19-28 2026

Last updated: March 24 2026

## HOW TO USE THIS DOCUMENT

Every day has a goal, time estimate, numbered steps, and copy-paste prompts. Read the day's goal first, then work through steps in order.

## WEEK ONE — COMPLETE

### Thursday March 19 — DONE

Goal: One automated Claude skill running live in GitHub Actions

What was built:
- Anthropic API key created, saved as GitHub secret
- grm-automations repo created on GitHub
- content_calendar.py built and running
- GitHub Actions workflow live — runs every Sunday 9 PM Eastern
- First manual run confirmed green checkmark

### Friday March 20 — DONE

Goal: Manus running, viral video pipeline, Instagram scheduler, editor skill automated

What was built:
- Manus tested and confirmed working
- Viral reel analysis pipeline built
- @getrootedmedia Instagram scheduler connected
- editor_skill.py built, GitHub Actions workflow live Monday 8 AM
- Manus Sunday competitor intel recurring task set
- Google Drive, Canva, GitHub connectors activated in Manus

### Saturday March 21 — PARTIAL

Goal: Meta Ads campaign skill, Design Advisor skill, website docs

What was built:
- Brand system fully built (BRAND_RULES.md, DESIGN_REVIEW.md)
- FOUNDER lead magnet v14 approved as design benchmark
- 5 Instagram graphics built and scheduled
- ManyChat connected, MANYCHAT_API_KEY saved
- 5 content plans exist in content-plans/ folder

What was NOT built (carry forward):
- Meta Developer App setup
- /meta-ads-campaign skill
- Run test campaign in Meta Ads Manager
- Design Advisor CSV database (confirmed missing March 24)
- Pre-load 8 website architecture docs into Claude Code

### Sunday March 22 — DONE

Goal: Full system verified, brand assets, ready for website

What was built:
- GRM_VOICE_SKILL.md created from editorial study of The Local (Winter Garden FL), Good Life Ocala, Ocala Magazine
- Six named editorial voices derived and documented
- Brand system fully documented
- FOUNDER v14 approved, design benchmark confirmed

### Monday March 23 — DONE (Birthday session)

- CT and FP media kit editorial work using voice skill

### Tuesday March 24 — DONE

Goal: Fix automations, connect brand system, build ManyChat

What was built:
- Brand Voice Editor workflow path bug fixed (commit 8e2ef6d)
- All skills connected to GRM_VOICE_SKILL.md as single source
- Manus intel report unstuck and delivered
- docs/GRM_MASTER_CALENDAR.md created
- ManyChat flows: PLAYBOOK, FOUNDER, CLOSING, LISTINGS — LIVE
- AI Partner Playbook PDF built (28 pages) — in Google Drive
- Drive link: https://drive.google.com/file/d/17AMZ6oSZg1YdPl-BlYHo9Kya3NRPI1xN/view

What was NOT completed:
- FOLLOWUP keyword flow in ManyChat
- New Follower Welcome DM in ManyChat
- Design Advisor CSV database (confirmed missing)
- Manus Instagram captions rewrite — unconfirmed

## WEEK TWO — IN PROGRESS

### Wednesday March 25 (tomorrow)

Goal: Website build begins

Prerequisites:
- Design Advisor CSV database must be built first
- 8 website architecture docs must be loaded into Claude Code
- Brand assets received from creative team

Tech stack: Next.js 15, TypeScript, Tailwind CSS, shadcn/ui

Build section by section, approve each before moving on. Check mobile at 375px, 768px, 1280px after each section.

### Thursday March 26

Goal: Closing Table page, Front Porch page, Advertise page

### Friday March 27 (original Thursday in sprint)

Goal: About page, Contact page, full QA, deploy to Vercel

### Friday March 28

Goal: Meta Ads dashboard v1

Tech: Next.js, Tailwind, shadcn/ui, Supabase

Features: Meta API connection, campaign table, date filter, nightly Vercel cron sync

## SATURDAY CARRYOVER DETAIL

### Meta Developer App Setup (90 min)

1. Go to developers.facebook.com
2. Sign in with Facebook account managing GRM business
3. Click Get Started, accept developer terms
4. Click Create App, choose Other, choose Business
5. Name: GRM Ad Deployer
6. Select Business Portfolio with your ad account
7. Click Create App
8. Add Marketing API product
9. Go to business.facebook.com/settings > Users > System Users
10. Add system user: Claude Code Deployer, Admin role
11. Add Assets: Ad Accounts, grant Full Control
12. Generate New Token, select GRM Ad Deployer app
13. Permissions: ads_management, ads_read, pages_read_engagement, pages_manage_ads
14. Copy token immediately
15. Save to GitHub secrets as META_ACCESS_TOKEN
16. Save Ad Account ID (format: act_XXXXXXXXX)
17. Save Facebook Page ID

### /meta-ads-campaign Skill (30 min after Meta app done)

Paste into Claude Code:

"Install the /meta-ads-campaign skill at .claude/skills/meta-ads-campaign/SKILL.md. 6-phase pipeline: gather context, create campaign record, generate copy, generate UTM links, pre-deploy checklist, deploy to Meta with status PAUSED. Set up SQLite database for campaign records. Build .env template with META_ACCESS_TOKEN, META_AD_ACCOUNT_ID, FACEBOOK_PAGE_ID placeholders. Explain each phase in plain English as you build."

### Test Campaign (15 min after skill installed)

Run: /meta-ads-campaign get-rooted-media awareness

Answer prompts:
- Audience: Ocala FL, real estate agents, ages 28-55
- Budget: $5/day test only
- Landing page: getrootedmedia.com
- Video: existing Remotion MP4 render

Everything deploys PAUSED. Nothing spends money.

### Design Advisor CSV Database (20 min in Claude Code)

Create .claude/skills/design/data/ with 5 files. Read brand/BRAND_RULES.md and brand/PDF_DESIGN_PLAYBOOK.md first.

Files needed:
- colors.csv
- typography.csv
- ui-reasoning.csv
- styles.csv
- landing.csv

### Pre-load Website Docs (when docs are ready)

8 documents to load into Claude Code project context:

- Get Rooted Media Website Blueprint
- GRM Creative Brief from Em Agency
- Get Rooted Media Design System
- Get Rooted Media Visual Layouts
- Get Rooted Media Publication Pages
- Get Rooted Media Customer Personas
- Get Rooted Media User Journeys
- Get Rooted Media Page Copy
- GRM Website Build Guide

Push to main when done.

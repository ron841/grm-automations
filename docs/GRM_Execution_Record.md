# GRM Execution Record

The real story of what got built, what changed, and what Ron does each week.

---

## HOW TO USE THIS DOCUMENT

### Starting a new build session

When you start a new Claude chat for a build day:

1. Upload `GRM_Execution_Record.md` from your GitHub repo
2. Upload `GRM_AI_Build_Sprint.docx` — the original sprint plan
3. Tell Claude: **"We are building Get Rooted Media. Here is our execution record and our sprint plan. Review both and tell me where we left off and what today's goal is."**
4. Claude will orient itself, confirm the current state, and pick up exactly where we left off

### Ending a build session

Before closing any build day chat:

1. Tell Claude: **"We are done for today. Update the execution record with everything we built, any changes from the original plan, and Ron's ongoing actions from today's work."**
2. Claude will generate the full update
3. Paste it into Claude Code with: **"Update docs/GRM_Execution_Record.md with this content and push to GitHub"**
4. Confirm the push in GitHub
5. Download the updated `GRM_Execution_Record.md` from GitHub to your Desktop for tomorrow's session

### Where to find the file for tomorrow

- **GitHub:** github.com/ron841/grm-automations > docs > GRM_Execution_Record.md
- Click the file > click the download icon > save to Desktop
- Upload it at the start of your next Claude chat

### What this document contains

- Every day's build history — what was planned vs. what actually got built
- Every change from the original sprint plan with reasoning
- Ron's complete ongoing weekly actions from each build day
- Full system map — what's automated, what's semi-automated, what's manual
- Ready-to-deploy scripts waiting for the right moment

### The three documents that run GRM

| Document | Purpose |
|----------|---------|
| **GRM_Execution_Record.md** | Upload this to start every new chat session |
| **GRM_Build_Log.md** | Technical inventory of every script and automation |
| **GRM_Weekly_Playbook.md** | Your weekly operating checklist |

---

## THURSDAY MARCH 19 — COMPLETED ✅

**Original goal:** One automated Claude skill running live in GitHub Actions.

**What actually got built:**

- Anthropic API key created (GRM-Automation, saved in GitHub Secrets)
- grm-automations repo created on GitHub (github.com/ron841/grm-automations)
- `content_calendar.py` built — generates weekly Instagram content calendar for @getrootedmedia
- GitHub Actions workflow created — runs every Sunday at 9 PM Eastern automatically
- First manual workflow run successful — green checkmark confirmed

**What changed from the plan:** Nothing major — Thursday executed as written.

**Ron's ongoing actions from Thursday's build:**

- None — fully automated. Sunday 9 PM GitHub emails you when it runs.

---

## FRIDAY MARCH 21 — COMPLETED ✅

**Original goal:** Manus running, viral video pipeline built, Instagram scheduler live, editor skill automated.

**What actually got built:**

- Manus tested and confirmed working
- Viral reel analysis pipeline — Manus finds 5 reels weekly, transcribes and scores them
- Claude Code rewrites top 2 reels in GRM brand voice — scripts saved to GitHub
- @getrootedmedia confirmed as Professional account
- Meta Business Suite connected — @getrootedmedia linked
- Manus Instagram connector activated — can post directly to Instagram
- Manus Canva connector activated — creates branded graphics automatically
- Manus Google Drive connector activated — saves content to Drive
- `editor_skill.py` built — polishes content in GRM brand voice using Claude Haiku
- GitHub Actions editor workflow — runs every Monday 8 AM, reads Sunday's calendar, polishes Monday's post
- GRM Content Queue folder created in Google Drive
- Week 1 content calendar saved to GitHub and Drive
- Week 2 Monday agent humor post saved to GRM Content Queue in Drive
- Two reel scripts saved to GitHub (Reel A: NEWOWNER, Reel B: PLAYBOOK)
- Manus recurring Sunday 9 PM task — GRM Weekly Intel Report (viral reels + competitor sweep)
- Manus emails ron@getrootedmedia.com after each Sunday report with 3-bullet summary and Drive link
- GitHub failure notifications enabled — emails ron@getrootedmedia.com on any workflow failure
- Google Drive upload script saved at `scripts/google_drive_upload.py` — ready to deploy later
- `docs/GRM_Weekly_Playbook.md` created — weekly operating checklist
- `docs/GRM_Build_Log.md` created — full system inventory with Daily Build Protocol

**Additional discovery after initial build:**

- Manus GitHub connector confirmed working — Manus can read directly from `ron841/grm-automations` repo
- Google Drive manual transfer step eliminated — Manus pulls content straight from GitHub
- Monday 8:30 AM recurring Manus task set up — pulls latest GitHub files, generates Canva graphics, sends Ron a preview, publishes immediately on approval
- Weekly content time reduced to under 30 minutes total

**What changed from the original plan:**

- Manus cannot natively schedule to Instagram via Meta API — uses Manus Instagram connector instead (better)
- Added Google Drive bridge planning — deferred to Week 3 (Google Cloud setup required)
- Added Manus Canva connector — not in original plan, major upgrade
- Monday editor skill now reads from Sunday's calendar automatically — smarter than original hardcoded input
- Manus GitHub connector eliminates the manual Google Drive transfer step — major workflow simplification not in original plan

**Ron's ongoing actions from Friday's build:**

Every Sunday night:
- Read Manus intel email when it arrives at 9 PM
- Note top 3 takeaways for the week
- Check Google Drive > GRM Weekly Intel for full report

Every Monday morning:
- Check GitHub repo output folder for polished content
- Copy approved content to Google Drive > GRM Content Queue
- Label each file with day and post type

Once per week:
- Open Manus, go to GRM Content Queue in Drive
- Review Canva graphic previews for each post
- Approve and let Manus schedule to @getrootedmedia Instagram

Once per week:
- Film any pending reel content (check reel scripts in GitHub `output/viral_scripts/`)

**End of day code audit completed.** Fixed: error handling added to both Python scripts, Node.js deprecation warnings resolved by updating to `actions/checkout@v6` and `setup-python@v6`, `content_calendar.py` updated to save to `output/content_calendar/` completing the Sunday-to-Monday pipeline connection, unused import removed from `google_drive_upload.py`. Repo is clean, all workflows alert on failure, no hardcoded secrets.

**SYSTEMS VERIFIED BEFORE CLOSE:**

- Manus GitHub connector live tested — pulled `ron841/grm-automations` successfully, read `output/content_calendar/Week1_Content_Calendar_2026-03-21.md` confirmed
- Manus Google Drive write live tested — `TEST_connection_2026-03-21.md` saved to GRM Weekly Intel folder confirmed
- Task timing updated to prevent race conditions: Sunday Manus intel report moved to 9:30 PM Eastern, Monday Manus content workflow moved to 9:00 AM Eastern

**Final confirmed automation schedule:**

- **Sunday 9:00 PM** — GitHub content calendar generates
- **Sunday 9:30 PM** — Manus weekly intel report runs, saves to Drive, emails ron@getrootedmedia.com
- **Monday 8:00 AM** — GitHub editor skill polishes Monday post
- **Monday 9:00 AM** — Manus pulls GitHub, creates Canva graphics, previews to Ron, publishes on approval

All systems live tested and confirmed. Repo is clean. Ready for Saturday build.

---

## SATURDAY MARCH 22 — PARTIAL COMPLETE

**Goal:** Meta Developer App setup + /meta-ads-campaign skill + Design Advisor skill with CSV database

**Completed tonight:**

- Brand identity extracted from SVG files — exact hex codes: GRM Teal #00B7CE, GRM Dark #090C0B
- 5 AI-generated Instagram graphics built in Canva via Manus with GRM branding
- All 5 graphics saved to Canva account and Google Drive GRM Content Queue
- Graphics scheduled: Wed Mar 26, Fri Mar 28, Mon Mar 30, Wed Apr 1, Fri Apr 3 at 8 AM ET
- ManyChat account confirmed connected to @getrootedmedia
- `MANYCHAT_API_KEY` saved to GitHub Secrets
- Discovered 5 content plans already exist in `content-plans/` folder with full ManyChat keyword flows and PDF outlines
- 5 keywords: FOUNDER, LISTINGS, FOLLOWUP, NEWOWNER, PLAYBOOK

**NOT completed — Sunday morning task:**

- 5 PDFs need to be built in Canva (outlines exist in `content-plans/` folder)
- 5 PDFs need to be uploaded to Google Drive and links added to content plans
- 5 ManyChat keyword automations need to be built in ManyChat visual builder
- ManyChat welcome DM for new followers needs to be built
- Meta Developer App setup
- /meta-ads-campaign skill in Claude Code
- Design Advisor skill with CSV database

**Sunday morning order of operations:**

1. Build 5 PDFs in Canva using Manus — use outlines in `content-plans/` folder
2. Upload to Google Drive, get real links
3. Build 5 ManyChat keyword automations in visual builder
4. Build ManyChat welcome DM
5. Continue Saturday build doc items

---

## SUNDAY MARCH 22, 2026

### What we built

**Brand System — fully operational**

- Created `brand/BRAND_RULES.md` — permanent color, typography, logo, voice standards
- Removed gold (#C9973A) from palette — three colors only: #090c0b, #00b7ce, #FAF8F4
- Created `brand/DESIGN_REVIEW.md` — 4-step checklist all tools follow before any creative work
- Created `brand/assets/` folder structure with 9 design assets: 4 SVG logos, 2 media kits, business card, Front Porch cover comp, spread comps
- Created `.claude/skills/design/SKILL.md` — /design skill live in Claude Code
- Updated Manus custom instructions — reads brand rules and reviews assets before every creative session
- Added 4 Manus connectors: Pexels/Unsplash, ElevenLabs, Cloudinary, Pinterest

**FOUNDER Lead Magnet — in final render**

- 5 revision passes with Manus
- Key lessons learned: GRM brand is black + teal + cream, NOT forest green. Logo must be SVG not text. GRM is publisher above content title. No tombstoning.
- Final PDF pending approval — uploading to Google Drive next

**Three-brand architecture documented**

- GET ROOTED MEDIA (parent — always on top)
- THE CLOSING TABLE (agent audience)
- THE FRONT PORCH (homeowner audience)
- Locked into /design skill and BRAND_RULES.md

### What's next

- Approve FOUNDER PDF > upload to Google Drive > get shareable link
- Build remaining 4 PDFs: LISTINGS, FOLLOWUP, NEWOWNER, PLAYBOOK (batch last 3 after LISTINGS approved)
- Build 5 ManyChat keyword automations
- Build ManyChat welcome DM (agent vs homeowner paths)
- Saturday carryover: Meta Developer App, /meta-ads-campaign skill, Design Advisor skill

### Ron's ongoing weekly actions

- Sunday 9 PM: GitHub Actions generates weekly content calendar
- Monday morning: review competitor intel report
- Weekly: approve Manus Instagram scheduled posts
- Monthly: advertiser outreach for CT and FP

### Key contacts locked in

- Ron Kolb: 352-598-7289 / ron@getrootedmedia.com
- Cameron Cowart: 352-875-0326 / cameron@getrootedmedia.com

### FOUNDER decision — approved at v4

v4 approved for Drive upload and ManyChat deployment.

Remaining polish items deferred to next session:

- Cover: replace circle icon with full wordmark (Logo-01.svg)
- All pages: fix merged word spacing (font encoding issue)
- Pages 10/11: add CT and FP cover mockup thumbnails
- Pages 4/9/12: add editorial spread asset snippets
- Page numbers: GRM circle icon treatment

These require direct Canva editing or fresh targeted Manus session — one page at a time approach.

### Logo placement — final approach

After 5 revision rounds, discovered Manus struggles with SVG logo placement via Canva API. Two solutions:

**SOLUTION A — Manual (fastest right now):**
Open completed PDF in Canva editor, delete placeholder, upload Logo_Get_Rooted_Media-01.svg from Mac, place top left, 220px wide, white (#FFFFFF all paths). 5 minutes per PDF.

**SOLUTION B — Manus exact spec prompt (testing on LISTINGS):**
"Place Logo_Get_Rooted_Media-01.svg from brand/assets/logos/ Width: 220px. Position: 24px from left, 24px from top. Color: white (#FFFFFF) on ALL paths. Zoom in and confirm both tree symbol AND Get Rooted Media text visible before full render. Try 02/03/04 variants if 01 fails."

LISTINGS render in progress with Solution B test.

### AFTERNOON/EVENING SESSION COMPLETED

**Brand System — fully locked**

- `DESIGN_REVIEW.md` created with 4-step pre-build checklist
- `BRAND_RULES.md` updated with Photography Rules and Florida Visual Identity
- `PDF_PRODUCTION_GUIDE.md` updated with Common Failures table (12+ entries)
- Florida Visual Identity locked: flat terrain, Spanish moss, white fencing, golden light. Mountains, rocky terrain, generic urban photos explicitly banned.
- Same-document photo duplicate audit rule added
- Badge overlap rule added (8px minimum gap)
- Photo reuse rule added (no photo used more than once across series)

**FOUNDER Lead Magnet — v8, pending final approval**

- 8 revision passes completed
- All major issues resolved: spreads removed, badge overlaps fixed, MacBook photos removed, watermarks removed, Cameron Cowart Top 20 Agent attribution added to p4
- Final photo audit in progress — one duplicate photo being resolved
- Status: ONE MORE MANUS PASS then Drive upload

**LISTINGS Lead Magnet — v4, pending final approval**

- All major issues resolved: cover title fixed, p6 photo added, p8 quote repositioned, p9 photo replaced
- Final photo audit in progress — same pass as FOUNDER
- Status: ONE MORE MANUS PASS then Drive upload

**Connector Hit List — do after PDFs approved:**

- Cloudinary — photo processing and smart crop
- Pinterest — visual reference before builds
- Zapier — workflow automation
- ElevenLabs — confirm connected, activate voiceovers for reels

FOUNDER v11 and LISTINGS v7 approved final after full-day design session. PDF_DESIGN_PLAYBOOK.md created with complete Manus build standards: document specs, photo rules, Florida visual identity rules, badge spacing, pull quote rules, publication page rules, QA checklist, and output filename convention. These two PDFs are the approved reference templates for FOLLOWUP, NEWOWNER, and PLAYBOOK builds. Both ready for Google Drive upload and ManyChat deployment.

**Pending from today — carry to next session:**

- Drive upload both PDFs, get shareable links
- Update `content-plans/ai-as-co-founder-content-plan.md` and `content-plans/ai-listing-descriptions-content-plan.md` with Drive links
- Build 5 ManyChat keyword automations (FOUNDER, LISTINGS, FOLLOWUP, NEWOWNER, PLAYBOOK)
- Build ManyChat welcome DM (agent vs homeowner paths)
- Create `docs/GRM_Design_System_Complete.md` — full build journal
- Saturday carryover: Meta Developer App, /meta-ads-campaign skill, Design Advisor skill

---

## MONDAY MARCH 23, 2026 — BIRTHDAY SESSION

Ron's birthday. Limited build day by design.

What we worked on:

- Extended editorial session focused on The Closing Table and The Front Porch media kits
- Tightened copy on both media kits using GRM voice principles
- Applied Voice 4 (The Closing Table) to CT advertiser-facing copy
- Applied Voice 1 (The Front Porch) to FP homeowner copy
- This was the first session where the voice skill was applied directly to production media kit documents

Status: Media kit copy tightened. Files not pushed to GitHub this session. Ron has working copies.

Ron's action: No code work. Rest day earned.

---

## TUESDAY MARCH 24, 2026 — COMPLETED ✅

**Full day build session. Here is everything that was done.**

### Context loaded at start of session

- GRM_AI_Build_Sprint_UPDATED.docx uploaded and reviewed
- Confirmed Thursday March 19 and Friday March 20 fully complete
- Confirmed Saturday March 21 partially complete
- Confirmed Sunday March 22 brand and voice work complete
- GRM_VOICE_SKILL.md loaded and active for entire session
- FOUNDER lead magnet v11 and v14 uploaded and compared
- v14 confirmed as approved design benchmark going forward

### About the voice skill — full context

GRM_VOICE_SKILL.md was created Sunday March 22 through an editorial study session. Claude read issues of The Local (Winter Garden FL), Good Life Ocala, and Ocala Magazine. From that study, six named editorial voices were derived:

- Voice 1: The Front Porch — warm, scene-driven, homeowner stories
- Voice 2: Plant Street — first-person, opinionated, agent social
- Voice 3: The Welcome Mat — practical, insider-tip, newcomer guides
- Voice 4: The Closing Table — sharp, insight-driven, agent authority
- Voice 5: Saturday Morning — clear, upbeat, community events
- Voice 6: The Deep Roots — literary feature, long-form profiles

Full rules, banned words, punctuation laws, and voice selection protocol documented in .claude/skills/GRM_VOICE_SKILL.md

ONE PIECE = ONE VOICE. No blending. No switching. Ever.

### About the FOUNDER PDF versions

v11 = earlier version without full voice corrections
v14 = approved final version. Voice 4 throughout. Exact Census data used. No em dashes. No banned words. This is the design and copy benchmark for all future PDFs.

Design standard: #090c0b dark, #00b7ce teal, #FAF8F4 cream. Logo top left 220px white. Full bleed photography. Teal accent bar.

### Automation fixes

- Brand Voice Editor workflow path bug fixed
- Editor now reads from correct output/content_calendar/ directory
- Graceful skip added. Green checkmark even when no calendar found
- input/draft.md placeholder created
- Commit 8e2ef6d

### Brand system — fully connected for first time

- All four skills now point to single source of truth
- GRM_VOICE_SKILL.md is the only voice reference across all tools
- /editor skill inline rules removed, replaced with pointer
- /content-plan skill inline rules removed, replaced with pointer
- /design skill updated to read voice skill before any copy
- Five brand integration files pushed

### Design Advisor CSV database — built

- colors.csv — real GRM hex values with usage rules
- typography.csv — exact point sizes for every text element
- ui-reasoning.csv — anti-patterns for local media publishing
- styles.csv — CT vs FP visual personality differences
- landing.csv — section guidance for GRM website build

No placeholder data anywhere. All real values.

### Manus — unstuck and updated

- Weekly Intel Report ran Sunday but was stuck waiting for approval
- Email delivered to ron@getrootedmedia.com at 8:07 AM Tuesday
- Confirmed saved to Google Drive GRM Weekly Intel folder
- KEY INTEL THIS WEEK:
  1. "8 Gross Things" maintenance reel by @denise.foster.fl — 1119 likes, 4924 shares. Tough love seller walkthrough = highest performing content format right now. Adaptable for GRM.
  2. Florida AI home sale story — Cooper City homeowner sold via ChatGPT in 5 days, saved 3% commission. Perfect reaction reel opportunity defending local agent value in Marion County.
- Manus custom instructions updated with GRM_VOICE_SKILL.md URL: https://raw.githubusercontent.com/ron841/grm-automations/main/.claude/skills/GRM_VOICE_SKILL.md
- Manus Instagram posts rescheduled — start March 31 afternoon
- Manus rewriting 5 captions to remove em dashes per voice rules

### Social strategy — reviewed and locked

Social Rollout Strategy doc reviewed. 4-reel personal brand launch series confirmed:

- Reel 1: "I Walked Away" — POSTED ✅ performing well
- Reel 2: "What We Built" — filming today, post Wed March 26 7AM
- Reel 3: "Our Third Co-Founder" — filming today, post Fri March 28 7AM
- Reel 4: "Why It Actually Matters" — film Thu March 27, post Mon March 30 7AM

### AI Partner Playbooks — reviewed

Three playbooks reviewed from uploaded docs:

- Playbook 1: Core AI prompts for business building
- Playbook 2: Local Business Advantage — competitor intelligence, content visibility, advertiser demo stack
- Playbook 3: Personal Wealth and Career Toolkit

Content is complete. PDF design started in Manus today. Lead magnet strategy: PLAYBOOK keyword on Reel 3 delivers AI Partner Playbook PDF via ManyChat DM automatically.

### Master calendar — created and corrected

- docs/GRM_MASTER_CALENDAR.md created
- Automated posts start March 31 afternoon not April 6
- Weekly rhythm: mornings for reels, afternoons for automated posts
- Section 7 weekly rhythm table added
- Section 8 ManyChat flows table added
- Commits 0a37e00 and 8dfca24

### ManyChat flows — 4 of 6 live

docs/MANYCHAT_FLOWS.md created with all 6 flows documented. All copy written in correct GRM voice. No em dashes. No banned words. All keyword flows funnel toward CLOSING conversation.

- PLAYBOOK Keyword Flow — LIVE ✅
- FOUNDER Keyword Flow — LIVE ✅
- CLOSING Keyword Flow — LIVE ✅
- LISTINGS Keyword Flow — LIVE ✅
- FOLLOWUP Keyword Flow — TO BUILD (2 min task)
- New Follower Welcome DM — TO BUILD (5 min task)

Commit 1dff7b2

### Execution record updated

This document updated with complete March 24 session.

---

### Ron's action items before next session

TONIGHT — FILM:
- Reel 2 "What We Built" with Cameron. Outside, natural light, somewhere Ocala-feeling. Cameron speaks his own 1-2 lines naturally.
- Reel 3 "Our Third Co-Founder." Laptop open to real Claude conversation on screen. The visual of actual conversation makes it real.

THIS WEEK — POST:
- Wednesday March 26 at 7 AM: Post Reel 2
- Friday March 28 at 7 AM: Post Reel 3. Include keyword PLAYBOOK in caption.
- Thursday March 27: Film Reel 4. Solo, outside, golden hour.

NEXT WEEK:
- Monday March 30 at 7 AM: Post Reel 4. Sales calls begin same day.
- Monday March 31 afternoon: Automated FOUNDER post goes live.

MANYCHAT — FINISH BEFORE FRIDAY MARCH 28:

Build FOLLOWUP flow:
- Keyword: FOLLOWUP
- Message: "The agents who build durable businesses treat the closing as the starting line. If you want to see the 90 day follow up system the top producers in Marion County use, reply CLOSING and we will send you the details."

Build Welcome DM — Settings then Growth Tools then New Follower:
- Message: "Welcome to Get Rooted Media. We cover Marion County from two angles. The Closing Table for real estate professionals and The Front Porch for new homeowners. Reply AGENT or HOMEOWNER and we will make sure you get the right content."

PDF — COMPLETE ✅
AI Partner Playbook PDF built by Manus. 28 pages. All brand rules followed. Saved to Google Drive GRM Content Queue as GRM_AI_Partner_Playbook.pdf
Drive link: https://drive.google.com/file/d/17AMZ6oSZg1YdPl-BlYHo9Kya3NRPI1xN/view?usp=drivesdk
Ron action: Set sharing to "Anyone with the link can view" then update PLAYBOOK and FOUNDER ManyChat flows with real Drive link.

---

### Carry-forward to next session — Saturday carryover still not done

1. Meta Developer App setup (developers.facebook.com)
   - Create app: GRM Ad Deployer
   - Create system user: Claude Code Deployer with Admin role
   - Generate token — permissions: ads_management, ads_read, pages_read_engagement, pages_manage_ads
   - Save token to GitHub secrets as META_ACCESS_TOKEN
   - Save Ad Account ID (format act_XXXXXXXXX)
   - Save Facebook Page ID

2. /meta-ads-campaign skill in Claude Code
   - Install at .claude/skills/meta-ads-campaign/SKILL.md
   - SQLite database for campaign records and ad account mappings
   - .env template with META_ACCESS_TOKEN, META_AD_ACCOUNT_ID, FACEBOOK_PAGE_ID placeholders
   - 6-phase pipeline: gather context, create record, generate copy, generate UTM links, pre-deploy checklist, deploy PAUSED

3. Website build — waiting on brand assets from creative team
   - Assets expected: photos, finalized logo files, brand pack
   - Once received: update Design Advisor CSVs with any new values
   - Run /design on all 5 pages before writing a line of code
   - Tech stack: Next.js 15, TypeScript, Tailwind, shadcn/ui

---

### System status as of end of day March 24

AUTOMATED AND RUNNING:
- Sunday 9 PM: GitHub content calendar generates
- Sunday 9:30 PM: Manus intel report runs, saves to Drive, emails Ron
- Monday 8 AM: GitHub editor skill polishes Monday content

MANYCHAT LIVE:
- PLAYBOOK, FOUNDER, CLOSING, LISTINGS keyword flows active

SCHEDULED AND READY:
- Reels 2, 3, 4 filming and posting this week
- Automated Instagram posts starting March 31 afternoon
- Sales calls beginning March 30

WAITING:
- AI Partner Playbook PDF (Manus building now)
- FOLLOWUP flow and Welcome DM (5 min task for Ron)
- Meta Developer App and /meta-ads-campaign skill
- Brand assets from creative team for website build

---

## SYSTEM MAP — Everything Running as of March 21, 2026

### Automated (zero human action required)

- **Sunday 9 PM** — GitHub: `content_calendar.py` generates weekly calendar
- **Sunday 9 PM** — Manus: GRM Weekly Intel Report runs, saves to Drive, emails Ron
- **Monday 8 AM** — GitHub: `editor_skill.py` reads calendar, polishes Monday post, saves to repo

### Semi-automated (Ron approves, system executes)

- **Weekly content scheduling** — Ron moves content to Drive, Manus creates graphics and posts to Instagram

### Manual (Ron does these)

- Monthly advertiser outreach for The Closing Table and The Front Porch
- Filming reel content
- Print deadline management

### Ready to deploy when needed

- Google Drive auto-upload from GitHub (`scripts/google_drive_upload.py`)
- Full pipeline: GitHub > Drive > Manus > Instagram (Week 3)

# Get Rooted Media — Build Log

Last updated: 2026-03-21
Repository: `ron841/grm-automations`

## Daily Build Protocol

Every build day ends with these 5 steps — no exceptions:

1. **Update GRM_Build_Log.md** with everything built today
2. **Update GRM_Weekly_Playbook.md** with any new human actions
3. **Test every new automation** before closing out
4. **Push all changes to GitHub**
5. **Write tomorrow's goal** in the "Next Session Goal" field below

### Ron's Weekly Human Actions (non-negotiable)

- **Sunday 9 PM** — Read Manus intel email, note top 3 takeaways
- **Monday morning** — Review GitHub editor output, move to Google Drive
- **Once per week** — Film any pending reel content
- **Once per week** — Schedule approved posts in Manus
- **Once per month** — Advertiser outreach for both publications

---

This document tracks every script, automation, and tool built for Get Rooted Media's content operations. It's the single source of truth for what exists, what it does, and what's coming next.

**Next session goal:** Add `ANTHROPIC_API_KEY` to GitHub Secrets and test both workflows end-to-end. Set up Google Cloud service account if time allows.

---

## Build Session: March 21, 2026

Everything below was built or updated in a single session. This is the day the content automation pipeline went from a single calendar script to a full operating system.

### What was built (in order):

| Time | Commit | What |
|------|--------|------|
| 12:53 PM | `6b4da8c` | **Viral reel scripts** — Rewrote 2 top-scoring reels for GRM brand voice. Reel A (NEWOWNER pillar, CTA to The Front Porch) and Reel B (PLAYBOOK pillar, CTA to The Closing Table). Saved to `output/viral_scripts/GRM_Reel_Scripts_2026-03-21.md`. |
| 1:32 PM | `1830780` | **Brand voice editor script + workflow** — Created `editor_skill.py` (Claude Haiku 4.5, takes raw content, returns Short + Long versions in GRM voice). Created `editor-skill.yml` GitHub Actions workflow (Monday 8 AM ET, manual trigger with custom input). |
| 1:35 PM | `b09b957` | **Edited content output** — GitHub Actions bot committed auto-generated edited content to `output/edited_content_2026-03-21.md`. |
| 1:41 PM | `ad67687` | **Week 1 content calendar** — Full Mon–Fri shooting calendar with targets (Closing Table vs. Front Porch), formats (humor reels, B-roll, vlog, property tour), visual/audio direction, on-screen text, and full captions with hashtags. Saved to `output/content_calendar/Week1_Content_Calendar_2026-03-21.md`. |
| 2:40 PM | `a6710c1` | **Editor workflow upgrade** — Updated `editor-skill.yml` to auto-read from the latest content calendar instead of using hardcoded input. Uses awk to extract Monday's post. Added failure notification step. Sunday → Monday pipeline now fully automated. |
| 2:43 PM | `2131637` | **Google Drive upload script** — Created `scripts/google_drive_upload.py` with full setup instructions. Uses Google Cloud Service Account auth. Ready to deploy but not yet wired into workflows (pending credentials). |
| 2:47 PM | `98377f0` | **Playbook + build log** — Created `docs/GRM_Weekly_Playbook.md` (Sunday–Friday operating checklist with monthly reminders) and `docs/GRM_Build_Log.md` (this file). |

### Key decisions made:
- **Claude Haiku 4.5** for the editor script (fast, cheap, good enough for tone editing)
- **Claude Sonnet 4.6** for the calendar generator (needs more creativity for topic generation)
- **awk-based extraction** in the workflow to pull Monday's post from the calendar file — simple, no extra dependencies
- **Google Drive integration deferred** — script is built and ready, but setting up the Google Cloud service account is a separate 20-30 minute task that doesn't block anything else
- **No ManyChat integration yet** — noted for a future session

### What was NOT completed:
- `ANTHROPIC_API_KEY` not yet added to GitHub Secrets (both workflows need this to run)
- Google Cloud service account not yet created (blocks Drive upload)
- Editor script not tested end-to-end with a live API key (key was invalid during the session)

---

## Scripts

### content_calendar.py
- **Purpose:** Generates a weekly Instagram content calendar (5 posts, one per content pillar) using the Claude API.
- **Model:** Claude Sonnet 4.6
- **Output:** `output/weekly_calendar_[YYYY-MM-DD].md`
- **Content pillars covered:** FOUNDER, LISTINGS, PLAYBOOK, FOLLOWUP, NEWOWNER
- **How to run locally:** `export ANTHROPIC_API_KEY='...' && python content_calendar.py`

### editor_skill.py
- **Purpose:** Takes raw content (caption, blog excerpt, social post) and rewrites it in GRM's brand voice using the Claude API. Returns two versions: a Short Version (under 150 characters for Instagram) and a Long Version (full caption with hashtags).
- **Model:** Claude Haiku 4.5
- **Output:** `output/edited_content_[YYYY-MM-DD].md`
- **How to run locally:** `export ANTHROPIC_API_KEY='...' && python editor_skill.py "Your raw content here"`

### scripts/google_drive_upload.py
- **Purpose:** Uploads a file to a shared Google Drive folder via a Google Cloud Service Account.
- **Status:** Built but NOT active. Requires Google Cloud credentials to be configured first.
- **Dependencies:** `google-api-python-client`, `google-auth`
- **Required secrets:** `GOOGLE_SERVICE_ACCOUNT_KEY`, `GOOGLE_DRIVE_FOLDER_ID`
- **How to run:** `python scripts/google_drive_upload.py path/to/file.md`

---

## GitHub Actions Workflows

### Weekly Content Calendar
- **File:** `.github/workflows/weekly-content-calendar.yml`
- **Trigger:** Every Sunday at 1:00 AM UTC (Saturday 8 PM ET) + manual
- **What it does:**
  1. Checks out the repo
  2. Sets up Python 3.12
  3. Installs the `anthropic` package
  4. Runs `content_calendar.py` to generate 5 pillar-based Instagram posts
  5. Commits and pushes the output markdown file to `output/`
- **Required secret:** `ANTHROPIC_API_KEY`

### GRM Brand Voice Editor
- **File:** `.github/workflows/editor-skill.yml`
- **Trigger:** Every Monday at 1:00 PM UTC (8 AM ET) + manual with optional custom input
- **What it does:**
  1. Checks out the repo
  2. Sets up Python 3.11
  3. Installs the `anthropic` package
  4. Finds the most recent content calendar in `output/content_calendar/`
  5. Extracts the first post (Monday's content) using awk
  6. Passes it to `editor_skill.py` for brand voice editing
  7. Commits and pushes the polished output to `output/`
  8. On failure, logs troubleshooting guidance in the Actions UI
- **Required secret:** `ANTHROPIC_API_KEY`
- **Pipeline:** Sunday calendar output feeds directly into Monday's editor — no manual input needed.

---

## Automation Pipeline (how the pieces connect)

```
Sunday 1 AM UTC          Monday 1 PM UTC          (Manual)
      |                        |                      |
      v                        v                      v
content_calendar.py  -->  editor_skill.yml  -->  google_drive_upload.py
      |                        |                      |
      v                        v                      v
output/weekly_          output/edited_           Google Drive
calendar_[date].md      content_[date].md        (not yet connected)
```

**Sunday:** `content_calendar.py` generates the week's 5 Instagram posts and commits to the repo.

**Monday:** `editor_skill.yml` reads the latest content calendar, extracts Monday's post, polishes it through Claude in GRM's brand voice, and commits the Short + Long versions.

**Future:** `google_drive_upload.py` will push output files to a shared Google Drive folder for the team.

---

## Content Assets (not automated — manually created)

### Content Plans (`content-plans/`)
Five detailed content strategy plans, each with hooks, scripts, carousel outlines, freebie ideas, and ManyChat flows:

| File | Topic |
|------|-------|
| `ai-as-co-founder-content-plan.md` | Using AI as a business co-founder |
| `ai-listing-descriptions-content-plan.md` | AI-powered listing descriptions |
| `follow-up-system-content-plan.md` | Agent follow-up systems and CRM |
| `new-homeowner-first-90-days-content-plan.md` | New homeowner onboarding guide |
| `top-producers-social-media-content-plan.md` | Social media for top-producing agents |

### Article Drafts (`content/`)
Print publication article drafts and frameworks:

| File | Publication |
|------|-------------|
| `content/closing-table/march-how-top-agents-build-referral-networks-draft.md` | The Closing Table |
| `content/closing-table/march-how-top-agents-build-referral-networks-framework.md` | The Closing Table |
| `content/front-porch/march-silver-springs-state-park-draft.md` | The Front Porch |
| `content/front-porch/march-silver-springs-state-park-framework.md` | The Front Porch |

### Reel Scripts (`output/viral_scripts/`)
Shooting-ready scripts based on viral content analysis:

| File | Content |
|------|---------|
| `GRM_Reel_Scripts_2026-03-21.md` | Two reels: NEWOWNER (Marion County environmental angle, CTA to The Front Porch) and PLAYBOOK (lifestyle selling in Ocala, CTA to The Closing Table) |

### Content Calendar — Custom (`output/content_calendar/`)
Hand-built weekly calendars with full shooting directions:

| File | Content |
|------|---------|
| `Week1_Content_Calendar_2026-03-21.md` | Mon–Fri calendar: humor reels, educational B-roll, lifestyle vlog, lead-gen tour. Each post has target audience, format, visual/audio direction, on-screen text, and full caption with hashtags. |

### Remotion Video Project (`remotion-video/`)
A React-based video generation project using the Remotion framework. Contains source code, config, and build output for programmatic video creation. Separate git submodule.

---

## Connected Tools & Services

| Tool | Purpose | Status |
|------|---------|--------|
| **GitHub Actions** | Runs automated workflows on schedule | Active |
| **Claude API (Anthropic)** | Powers content generation and brand voice editing | Active (requires `ANTHROPIC_API_KEY` secret) |
| **Google Drive API** | Upload output files to shared Drive folder | Script built, not yet connected |
| **Remotion** | Programmatic video creation in React | Project scaffolded |

---

## What's Built

### Scripts & Automations
- [x] Content calendar generator (`content_calendar.py`) — built March 19
- [x] Brand voice editor (`editor_skill.py`) — built March 21
- [x] Google Drive upload script (`scripts/google_drive_upload.py`) — built March 21, not yet connected
- [x] Weekly content calendar workflow (Sunday auto-run) — built March 19
- [x] Brand voice editor workflow (Monday auto-run, reads from calendar) — built March 21, upgraded same day to auto-read from calendar

### Content Assets
- [x] 5 content plans across all pillars (`content-plans/`)
- [x] 2 article drafts + frameworks for March print issues (`content/`)
- [x] 2 viral reel shooting scripts with shot directions (`output/viral_scripts/`) — built March 21
- [x] Week 1 custom content calendar with full production notes (`output/content_calendar/`) — built March 21
- [x] Remotion video project scaffolded (`remotion-video/`)

### Documentation
- [x] Weekly operating playbook with end-of-day checklist (`docs/GRM_Weekly_Playbook.md`) — built March 21
- [x] Complete build log with session history (`docs/GRM_Build_Log.md`) — built March 21

## In Progress

- [ ] **`ANTHROPIC_API_KEY` in GitHub Secrets** — Required for both workflows to actually run. Blocked: need a valid API key (the one tested on March 21 had a doubled prefix and was invalid).
- [ ] **Google Drive integration** — Script built and fully commented. Blocked: need to create a Google Cloud service account (~20-30 min setup) and add credentials to GitHub Secrets.
- [ ] **End-to-end pipeline test** — Sunday calendar → Monday editor → output file. Need the API key in Secrets first.

## What's Next

- [ ] Add `ANTHROPIC_API_KEY` to GitHub Secrets and test both workflows
- [ ] Set up Google Cloud service account and wire `google_drive_upload.py` into workflows
- [ ] ManyChat integration for "Comment TOUR" lead-gen DM automation
- [ ] Remotion video templates for automated Reel generation from shooting scripts
- [ ] Engagement tracking dashboard or weekly metrics report
- [ ] Advertiser CRM or outreach tracking automation
- [ ] Content approval flow (e.g., Slack or email notification before posting)
- [ ] Manus AI integration for automated competitive intel and market research reports

# Get Rooted Media — Build Log

Last updated: 2026-03-21
Repository: `ron841/grm-automations`

This document tracks every script, automation, and tool built for Get Rooted Media's content operations. It's the single source of truth for what exists, what it does, and what's coming next.

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

- [x] Content calendar generator (`content_calendar.py`)
- [x] Brand voice editor (`editor_skill.py`)
- [x] Weekly content calendar workflow (Sunday auto-run)
- [x] Brand voice editor workflow (Monday auto-run, reads from calendar)
- [x] Google Drive upload script (ready to deploy)
- [x] 5 content plans across all pillars
- [x] 2 article drafts + frameworks for March print issues
- [x] 2 viral reel shooting scripts
- [x] Week 1 custom content calendar with full production notes
- [x] Remotion video project scaffolded
- [x] Weekly operating playbook (`docs/GRM_Weekly_Playbook.md`)

## In Progress

- [ ] Google Drive integration — Script built, needs service account credentials and workflow wiring
- [ ] `ANTHROPIC_API_KEY` in GitHub Secrets — Required for both workflows to run

## What's Next

- [ ] Wire `google_drive_upload.py` into both workflows after credentials are set up
- [ ] ManyChat integration for "Comment TOUR" lead-gen DM automation
- [ ] Remotion video templates for automated Reel generation from scripts
- [ ] Engagement tracking dashboard or weekly metrics report
- [ ] Advertiser CRM or outreach tracking automation
- [ ] Content approval flow (e.g., Slack or email notification before posting)

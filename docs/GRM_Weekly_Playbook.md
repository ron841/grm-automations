# Get Rooted Media — Weekly Operating Playbook

Last updated: 2026-03-21

This is the weekly operating rhythm for Get Rooted Media LLC. Follow this checklist every week to keep content flowing, automations running, and both publications on track.

---

## Sunday Night (30 min)

**Goal:** Set the week up so Monday morning runs itself.

- [ ] **Review the Manus intel report** — Check for trending topics, competitor moves, or market shifts in Marion/Sumter County real estate that should influence this week's content.
- [ ] **Check the auto-generated content calendar** — The `Weekly Content Calendar` GitHub Action runs every Sunday at 1:00 AM UTC (Saturday 8 PM ET). Verify the output file landed in `output/weekly_calendar_[date].md`.
  - If the workflow failed, manually trigger it: GitHub repo > Actions > Weekly Content Calendar > Run workflow.
- [ ] **Review and approve the 5 posts** — Read through each pillar post (FOUNDER, LISTINGS, PLAYBOOK, FOLLOWUP, NEWOWNER). Flag anything that needs a rewrite or local detail added.
- [ ] **Confirm the Monday content calendar file is in `output/content_calendar/`** — This is what the Monday editor workflow reads from. If you've built a custom calendar (like the Week 1 calendar), make sure it's committed and pushed.

---

## Monday Morning (20 min)

**Goal:** Review the polished content and move it into production.

- [ ] **Check the Brand Voice Editor output** — The `GRM Brand Voice Editor` GitHub Action runs every Monday at 8:00 AM ET (1 PM UTC). It reads the first post from the latest content calendar, polishes it through Claude, and saves it to `output/edited_content_[date].md`.
  - If the workflow failed, check Actions for the error. Common issues: missing API key, no calendar file found.
  - You can also run it manually with custom content: Actions > GRM Brand Voice Editor > Run workflow > paste your text.
- [ ] **Review the edited Short Version and Long Version** — The Short Version (under 150 chars) is for Instagram captions. The Long Version is the full post with hashtags.
- [ ] **Move approved content to Google Drive** — (Manual for now. Google Drive upload script is built at `scripts/google_drive_upload.py` but not yet connected — pending service account setup.)
- [ ] **Schedule Monday's post** — Copy the approved caption into your scheduling tool (Later, Buffer, or native Instagram).

---

## Tuesday through Friday (10 min/day)

**Goal:** Post, engage, and keep momentum.

- [ ] **Post the day's content** — Refer to the weekly content calendar for each day's pillar, topic, hook, caption, and hashtags.
- [ ] **Engagement check (morning + evening):**
  - Reply to every comment within 2 hours of posting
  - Check DMs — especially any "TOUR" or lead-gen keyword responses from Friday's post
  - Like and comment on 5-10 posts from local accounts (agents, businesses, community pages)
- [ ] **Story touchpoint** — Post at least one Story per day. Ideas: behind-the-scenes of content creation, local Ocala moments, polls about Marion County life, repost of a featured agent or homeowner.
- [ ] **Friday lead gen follow-up** — If Friday's post used a "Comment for link" CTA, make sure every commenter received the DM with property details (manually or via ManyChat if configured).

---

## Weekly Reminders

### Content Filming (block 2-3 hours once per week)

- [ ] **Batch film this week's Reels** — Use the shooting scripts in `output/viral_scripts/` for shot direction and format guidance.
- [ ] **Capture B-roll around Ocala** — Silver Springs, downtown square, horse farms, new construction along SR 200, World Equestrian Center. Keep a running library of local footage.
- [ ] **Film at least one talking-head clip** — Needed for PLAYBOOK and FOUNDER pillar posts. Natural light, porch or local backdrop.

### Content Review

- [ ] **Check content plans for upcoming topics** — Five content plans are ready in `content-plans/`:
  - AI as Co-Founder
  - AI Listing Descriptions
  - Follow-Up System
  - New Homeowner First 90 Days
  - Top Producers Social Media
- [ ] **Review article drafts** — Check `content/closing-table/` and `content/front-porch/` for any drafts or frameworks that need editing for the next print issue.

---

## Monthly Reminders (First Monday of Each Month)

### Advertiser Outreach

- [ ] **Review The Closing Table ad roster** — Confirm renewals for the upcoming monthly issue. Reach out to any lapsed advertisers.
- [ ] **Review The Front Porch ad roster** — Quarterly publication, so plan 2-3 months ahead. Identify new local businesses to pitch.
- [ ] **Send rate cards and media kits** — To any warm leads from Instagram DMs, networking events, or agent referrals.
- [ ] **Track ad revenue vs. targets** — Update your tracking spreadsheet or CRM.

### Publication Deadlines

- [ ] **The Closing Table** — Monthly. Confirm editorial content, ad placements, and print-ready files are submitted to the printer by the 15th (or your specific deadline).
- [ ] **The Front Porch** — Quarterly. Check if this month falls within a production window. If so, confirm editorial lineup and distribution plan.

---

## Quick Reference: Where Everything Lives

| What | Where |
|------|-------|
| Content calendar (auto-generated) | `output/weekly_calendar_[date].md` |
| Content calendar (manual/custom) | `output/content_calendar/` |
| Edited/polished content | `output/edited_content_[date].md` |
| Reel shooting scripts | `output/viral_scripts/` |
| Content plans (topic deep dives) | `content-plans/` |
| Article drafts | `content/closing-table/` and `content/front-porch/` |
| Automation workflows | `.github/workflows/` |
| Scripts | `editor_skill.py`, `content_calendar.py`, `scripts/` |

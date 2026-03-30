# GRM Next Steps — Post-Launch
Updated: March 30, 2026

Site is live at getrootedmedia.com.

---

## Priority 1 — Tracking (complete before driving any traffic)

Install Meta Pixel and GA4 on the site. Both must be live before any paid or organic campaigns begin so data is captured from day one.

**Prompt for next session:**

"Install Meta Pixel and GA4 on the GRM website. Add both to the Next.js root layout so they fire on every page. Use next/script with afterInteractive loading strategy. Store the Meta Pixel ID and GA4 Measurement ID as Vercel environment variables — never hardcoded in source files. Show the diff before committing."

---

## Priority 2 — Instagram Content Automation

The GitHub Actions weekly content calendar is already running every Sunday at 9pm Eastern. Manus viral video pipeline and @getrootedmedia Instagram scheduler need to be activated and tested end to end with a live reel.

---

## Priority 3 — Ads Dashboard v1

Meta only. Tech stack: Next.js, Tailwind, Supabase. Features: campaign data in a sortable table, date filter (last 7 days / last 30 days / this month), nightly Vercel cron sync. Build per sprint doc Stage 1 spec. Build only after tracking is confirmed live.

---

## Ongoing items

- Front Porch media kit cover — Em Agency must fix "quarterly" to "bi-monthly" before distribution
- Real photos of Ron and Cameron — for About page, pending from Em Agency
- Canonical tags — add to all pages in Next.js metadata config
- Confirm real Issue 1 cover story agent for The Closing Table article teaser — Cameron Cowart ruled out to protect editorial credibility

---

## Deployment reference for future sessions

- Repo: github.com/ron841/grm-automations — website lives in /website subfolder
- Vercel: ron-7323 account, project grm-website
- Pushing to main branch auto-deploys to getrootedmedia.com
- DNS: managed at IONOS — do not touch nameservers
- Calendly: cal.com/ron-kolb-cdlgsw/30min — live and wired to nav and contact page

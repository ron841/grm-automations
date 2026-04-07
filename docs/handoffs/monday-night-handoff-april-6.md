# Monday Night Handoff — April 6, 2026

## Storefront Launch and Vercel Recovery

Read this top to bottom Tuesday morning before doing anything else. It captures what shipped Monday night, what didn't, the Vercel ground truth that the GRM Brain had wrong (now fixed), and the exact sequence for Tuesday.

If anything here conflicts with the brain or earlier handoff docs, this document wins.

## What shipped tonight

**The Storefront landing page section is LIVE on getrootedmedia.com.** Third pillar on the homepage, slotted between The Front Porch and the stats stripe. Dark background, brand-correct typography, eyebrow with stacked teal divider matching the Our Story and Founding Partner pattern.

Final content as shipped:

- Eyebrow: THE STOREFRONT · MARION COUNTY (with teal divider line stacked underneath)
- Headline: The Storefront
- Tagline: We build it. We host it. We update it. You answer the phone.
- Body: 3 paragraphs, Plant Street voice, no banned phrases, no em dashes
- CTA: "See a free preview built for your business →" linking to cal.com/ron-kolb-cdlgsw/30min

Final commit hash for the section: 1dd10db on origin/main. The brain update commit: 366b55a.

The component file is `website/src/components/sections/WebServices.tsx` (named WebServices internally even though the public-facing name is The Storefront). Leave the filename alone to avoid breaking imports.

## What did NOT ship tonight

The 5-item Monday afternoon sales infrastructure list had the landing page as item 1. Items 2-5 are still untouched and need to ship Tuesday before Wednesday 7:15 AM first dial:

1. Service agreement PDFs (Tier 1 Elevate $1000+$250/mo, Tier 2 Launch $500-650+$100/mo)
2. Pricing one-pager PDF (side-by-side comparison, Plant Street voice, textable mid-call)
3. HubSpot web services pipeline setup (custom properties: preview_url, site_quality_score, call_status; split call queues for Ron 40 dials and Cameron 20 dials)
4. Pause old magazine call automation in HubSpot

Plus flagships 2 and 3 need to build Tuesday so Wednesday opens with three flagships (T&F + Ocala AC + Pat Myers or equivalent).

## The Vercel mess: what actually happened

We spent approximately two hours debugging a build failure that turned out to be a single misconfigured setting. Root cause: the Vercel project that serves getrootedmedia.com had two settings drifted from their correct values:

1. Build Command override was set to `npm run vercel-build` (a script that does not exist in package.json), causing 0ms instant failures
2. Root Directory was set to `./` (repo root) instead of `website` (the subfolder where Next.js code lives), causing build failures even after the build command was fixed

Both have been corrected in the Vercel dashboard. The site has now successfully deployed multiple times in a row, proving auto-deploy is healthy.

The brain has been updated with these facts (commit 366b55a) so future debug sessions can find them in the troubleshooting checklist.

## Vercel ground truth (corrected)

Three projects exist on the ron-7323's projects team:

- **`website`** — ACTIVE. Serves getrootedmedia.com. The real production project for the GRM company website. Auto-deploy is on. Root Directory = `website`. Build Command = default `npm run build`.
- **`tandf-electric`** — ACTIVE. Serves tandf-electric.vercel.app. Flagship 1, the web services proof of concept used in sales calls. **Do not touch under any circumstances.**
- **`grm-website`** — DORMANT. Last successful deploy March 30. The only true orphan. Was likely the original project name before the production project got renamed. Safe to delete in a future cleanup session, not urgent.

## Cleanup items added to the open list

Both real, neither urgent. Both for a future focused session, not Tuesday.

1. Delete the orphan `grm-website` Vercel project. 5-minute task in the dashboard.
2. Separate getrootedmedia.com out of grm-automations into its own dedicated repo. 30-60 minute task. Permanently eliminates cross-wiring between the company website and the prospect-skill web services automation work.

## Tuesday sequence (in order)

This is a heavy day. The sequence puts the highest-cognition work in the freshest part of the afternoon and saves the templated work for the evening.

1. Read this handoff doc top to bottom (5 min)
2. Bank of America business checking appointment for Get Rooted Media LLC (1-2 hours)
3. Stripe account setup with new routing and account numbers (30-45 min)
4. Create the six Stripe payment links and test each one (30-45 min)
5. Lunch and decompression (30-60 min)
6. Flagship 2 build: Ocala Air Conditioning and Refrigeration (2-3 hours, fresh afternoon)
7. Flagship 3 build: Pat Myers Electric or equivalent Tier 1 candidate (2-3 hours)
8. Sales infrastructure items 2-5 in one block: agreements, pricing one-pager, HubSpot pipeline, pause magazine automation (3-5 hours, evening)
9. Cameron final brief and confirm Wednesday availability (30 min)
10. Final mobile review of all three flagships and all sales materials (30 min)
11. Alarm set for Wednesday 6:30 AM. Sleep.

### Why flagships before sales infrastructure

Flagship building requires creative judgment: Plant Street voice on real prospect content, design tier decisions, approval gates, brand color extraction, real testimonial verification. That work needs Ron's fresh afternoon brain. Sales infrastructure (agreements, one-pager, HubSpot pipeline) is more templated and can be executed when tired but still focused.

### Why three flagships matters for Wednesday

T&F Electric alone is one proof point. T&F plus Ocala AC plus Pat Myers gives a three-flagship portfolio that covers two service verticals (electrician and HVAC) and demonstrates the skill works across categories. Three real preview URLs in the phone makes Wednesday morning calls dramatically stronger than two.

### Tuesday flagship build prep

Before starting flagship 2, run the Plan A daily health check on Magic MCP per plan-a-recovery-playbook.md. If Plan A is healthy, use real 21st.dev components for non-hero sections. If still broken, the Plan B reference library handles everything. Either way the hero comes from the flagship 1 pattern that is now encoded in the skill at v2.

Each flagship build should take 2-3 hours including Phase 1 deep capture, Phase 2 multi-page crawl, Phase 2.5 pre-migration SEO audit, Phase 3 photo collection, Phase 4 design engine and approval gate, Phase 5 site generation, Phase 6 deployment, Phase 7 lead record. Do not let any single flagship exceed 3 hours. If it stalls, ship what is built and move on.

## Tuesday morning first prompt

Paste this into a fresh Claude session as the first message Tuesday morning:

---

Good morning. The Storefront landing page shipped to getrootedmedia.com Monday night and the GRM Brain was updated the same night with corrected Vercel facts. Tuesday is heavy: bank, Stripe, payment links, then flagships 2 and 3 in the afternoon, then sales infrastructure items 2-5 in the evening. The goal is to walk into Wednesday 7:15 AM first dial with three flagships ready (T&F + Ocala AC + Pat Myers or equivalent) and the full closing infrastructure complete.

Read the Monday night handoff doc from the project files before responding so you have full context. Then walk me through exactly what to bring to the Bank of America business checking appointment and what to confirm with the BofA banker. One step at a time. Do not multitask. Push back if I try to combine steps. We will switch to flagship-build mode after I am back from the bank and Stripe is set up.

---

## What absolutely must NOT happen Tuesday

- Do not delete `tandf-electric` from Vercel. It is flagship 1.
- Do not delete or rename `website` from Vercel. It is the live company site.
- Do not separate the repo Tuesday. That is a future focused session.
- Do not start sales infrastructure before banking. Banking unlocks Stripe which unlocks payment links.
- Do not let any single flagship build exceed 3 hours. Ship what is built and move on.

## End of handoff

The Storefront is live. The Vercel debugging is over. The brain is updated. Tuesday is heavy but achievable: bank, Stripe, two more flagships, sales infrastructure stack, Cameron brief. Wednesday 7:15 AM first dial with three flagships in the phone and the full closing infrastructure ready to take a yes.

Sleep.

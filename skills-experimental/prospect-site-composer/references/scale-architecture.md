# Scale Architecture Reference

Part of the prospect-site skill v0.7. This is the north-star file, written last because it references everything else. Its audience is future-Ron, future GRM team members, and future Claude sessions that need to understand "why is the skill the way it is" and "what does the next version look like."

This file does not describe any code or any procedure the skill executes. It describes the architecture of GRM Web Services as a product and a business, the trade-offs baked into v0.7, and the roadmap from v0.7 to v1.0. It is the file to read when a decision feels larger than "how do I implement X" and closer to "is X something we should even be doing right now."

Every decision in this file traces back to one principle: **quality over scale at v0.7**. The entire v0.7 skill exists to produce 1-10 flagship-quality contractor sites that prove the commercial thesis. Scale comes after quality is proven, not before. Any pressure to add automation, self-service, or multi-client features before the first 3 flagship clients are live is pressure in the wrong direction and should be resisted.

---

## Table of contents

1. The v0.7 constraint surface
2. The scale ceiling framework
3. The v0.7 → v1.0 roadmap
4. Integration architecture for future add-ons
5. Technical debt inventory
6. Migration triggers
7. What NEVER changes
8. The v0.7 scale-readiness test
9. Scale metrics to track
10. When to abandon vs evolve
11. Integration with other skill files
12. Version

---

## The v0.7 constraint surface

v0.7 is deliberately small in scope. The deliberate smallness is the feature, not the bug. Every constraint below is a conscious choice to preserve quality and prevent premature scaling.

### What v0.7 does

- Generates a complete multi-page static site for a single contractor prospect from a captured data profile
- Produces fact-dense, voice-disciplined, schema-rich output engineered for AI citation
- Deploys to a Vercel preview URL that Ron can send to the prospect as a sales weapon
- Supports one prospect at a time, manually triggered
- Runs through 8 phases with hard gates at Phase 3.5, Phase 4 (approval), Phase 6 (verification), and Phase 7 (deployment)
- Enforces anti-slop rules across typography, color, layout, copy, photography, and interaction patterns

### What v0.7 explicitly does NOT do

Each of these is deferred with reasoning in a skill file or this document. None of them is silently dropped.

- **Multi-tenant operation.** The skill handles one prospect per run. Running the skill on multiple prospects in parallel is out of scope. Batch operations are out of scope.
- **Automated client onboarding.** Every signed deal requires manual execution of the 12-step onboarding checklist in `deployment.md`. No webhook-triggered pipeline in v0.7.
- **Client self-service.** Clients contact Ron for updates via text, email, or phone. There is no client portal, no update form, no self-service dashboard.
- **Automated quarterly refresh.** The quarterly refresh protocol in `deployment.md` is manual. Ron opens each client folder in turn and runs the refresh workflow through Claude Code.
- **Automated monthly monitoring reports.** Reports are produced manually from the four monitoring stack layers. At 5-10 clients this is reasonable. At 20+ clients it becomes the biggest time sink and is the first automation target.
- **Interactive site features.** No booking calendars, quote calculators, estimate forms, project filters, or any feature that requires client-side state management.
- **Client-side JavaScript frameworks.** Per `anti-slop-rules.md`, no React, Vue, Svelte, or equivalent in the generated output. v0.7 ships plain HTML only.
- **Multi-domain or franchise support.** Single-location, single-domain contractors only. v0.7 has no architecture for a client with 5 locations each needing localized pages.
- **Content marketing services.** The skill does not generate blog posts, newsletters, or ongoing content beyond the quarterly refresh.
- **Social media, paid advertising, photography, email marketing.** These are separate products from the website service and are not part of the v0.7 scope.
- **White-label reseller operations.** The skill is not yet structured for another agency to use it under their own brand.

### Why the constraints exist

Each constraint is a deliberate "don't do this yet" decision made to preserve the quality ceiling for v0.7. The pattern to recognize: when scope creep pressure appears ("can we also do X?"), the answer is almost always "X is a v0.8 or v0.9 concern, let's finish v0.7 first." The exceptions are rare and should be explicit CTO decisions documented here with dates and reasoning.

The cost of premature scaling is not theoretical. The v0.6 failure produced four identical-looking sites because the skill was trying to handle too many patterns at once. v0.7's single-hero-pattern discipline and heavy specification came from that lesson. The same lesson applies at the product level: trying to handle too many client states at once produces average outputs instead of flagship outputs.

---

## The strategic ambiguity: lifestyle business or real agency

This file is written to support two possible futures for GRM Web Services, and the choice between them does not need to be made in v0.7. Naming the ambiguity explicitly is more useful than pretending one path is the obvious right answer.

### Path A: Lifestyle business

GRM stays small. One operator (Ron) plus possibly one virtual assistant. Active client count caps somewhere between 20 and 50. Revenue grows by raising prices and adding selective add-ons rather than by adding clients. Ron's time stays balanced between sales, delivery, and life. The business is profitable per hour, fun, sustainable, and never needs a real team.

Under Path A, the v0.8 automation work still matters because it buys Ron's time back. The folder reorganization, the automated quarterly refresh, the centralized client dashboard all reduce Ron's per-client time so the lifestyle business runs cleanly. But v0.9 self-service features and v1.0 agency infrastructure become unnecessary. Ron handles every client personally because that is the lifestyle promise.

The Path A planning horizon is 30 clients. Decisions are made with the test: does this work for one operator serving 30 clients? Anything that requires a team is out of scope.

### Path B: Real agency

GRM grows into a multi-person operation. Active client count grows past 30 and continues to scale. Ron transitions from doing the work to running the team. Multiple specialists handle sales, design, delivery, and operations. Revenue grows by adding clients and adding service categories (social, paid, photography, content). At v1.0, GRM is a recognized Marion County (or beyond) digital agency with a team of 5-15 people.

Under Path B, every version in the roadmap matters. v0.8 buys the time to grow. v0.9 introduces the self-service features that scale beyond Ron's personal capacity. v1.0 builds the agency infrastructure. The planning horizon eventually extends to 100+ clients.

### Why the choice doesn't need to be made in v0.7

The v0.7 work, the v0.8 automation work, and the early Stage 3 transitions are identical for both paths. Both paths need flagship quality. Both paths need automated quarterly refresh at scale. Both paths need a centralized client dashboard. Both paths need backup infrastructure. The choice between Path A and Path B only starts to matter at the v0.9 boundary, when self-service dashboards and content hub generators become relevant for one path and not the other.

This means GRM has runway. The decision can be deferred until client count is at 10-15 and the actual signal is clearer. By that point Ron will know:

- Whether the work is fun or grinding
- Whether selling website services to Marion County contractors is sustainable or saturating
- Whether the monthly recurring revenue per client supports a team
- Whether Ron wants to spend the next 5 years running a team or running solo
- Whether the AI citation thesis is producing measurable client wins or staying theoretical

These are the inputs for the Path A vs Path B decision. None of them are knowable today. Forcing the decision now would be guessing.

### How this file handles the ambiguity

The roadmap below describes both paths in parallel where they diverge. v0.7 and v0.8 are universal. v0.9 and v1.0 are conditional on Path B; under Path A they are skipped or replaced with smaller iterations. Migration triggers are written to fire under either path with notes on which path they apply to. The "What never changes" principles apply regardless of path.

When Ron makes the Path A vs Path B decision, this file should be updated to remove the ambiguity and lock in the chosen path's roadmap. Until that decision, the file stays dual-pathed.

---

## The scale ceiling framework

GRM's journey from 1 flagship to scale has four distinct stages. Each stage has different architectural needs. Understanding which stage you are currently in is the single most important planning question. Note that under Path A (lifestyle business), Stage 4 is optional or skipped entirely; the framework still applies through Stage 3.

### Stage 1: Flagship execution (1-3 active sites)

**Where GRM is as of April 9, 2026.** One preview live (T&F Electric). Two more flagships targeted before active sales. The goal is proving the quality bar is repeatable, not proving scale is achievable.

Architectural needs: none beyond what v0.7 provides. Every decision is quality-focused. Speed is secondary. If a flagship takes two days instead of two hours, that is fine as long as the output is flagship quality.

What breaks at this stage: nothing. v0.7 is designed for this stage. The question is not "will the architecture hold" but "is the output quality high enough to sell confidently."

**Applies to:** both Path A and Path B identically.

### Stage 2: Early client operations (4-10 active clients)

**The first real stress test.** Ron has signed 4-10 clients. Each client is a live domain with monthly or buyout payment. The quarterly refresh cycle becomes a real commitment. Monthly monitoring reports become a real deliverable. Update requests start arriving.

Architectural needs: discipline more than code. Every client must be in HubSpot. Every client must have a `client-status.json` file. Every client must be on the monitoring stack. The folder structure is still flat but starting to feel crowded. The quarterly refresh takes a full afternoon but not a full day.

What breaks at this stage: nothing structural, but the "Ron does everything" model starts showing stress. Update requests that arrive during sales-call time get delayed. Monitoring reports that should take 30 minutes per client take 45. The first signs of needing automation appear.

Trigger for moving to Stage 3: when Ron's time is consistently more than 30% spent on operations (updates, monitoring, quarterly refresh) rather than sales, prospect building, or strategy. **Note: this 30% threshold is a starting heuristic, not a measured number. Refine based on actual experience by the time the trigger fires.**

**Applies to:** both Path A and Path B identically.

### Stage 3: Scale operations (10-30 active clients)

**The hardest transition for either path.** Manual workflows from Stage 2 stop scaling linearly. The quarterly refresh takes a full day. Update requests back up. Monitoring reports are consistently late. Ron is spending 60-70% of time on operations and deal flow is suffering.

Architectural needs: automation of painful repetition. This is v0.8 territory. Specifically:

1. Automated quarterly refresh workflow — Claude Code iterates over every client folder, runs the refresh procedure, produces a summary report
2. Automated monthly monitoring report generation — pulls from Plausible, Otterly, Search Console APIs and formats into the template
3. Automated Google review count sync — polls Google Places API, updates schema and site copy when review counts change significantly
4. Centralized client dashboard — a private web page showing all clients at a glance with status, last refresh, uptime, monthly invoice status
5. Pre-flight check automation — verifies all integrations work before starting a new prospect build
6. HubSpot pipeline sync — Stripe payment webhooks trigger HubSpot deal stage moves automatically

What breaks at this stage: the flat folder structure (need `_clients/`, `_prospects/`, `_archive/` split), the "Ron is the only person" model (need a virtual assistant or junior developer for operations), and the manual report generation (needs to be scripted).

Trigger for moving to Stage 4: **Path B only.** Active client count crosses 30, OR Ron is spending more than 50% of time on operations and decides to scale rather than cap. Under Path A (lifestyle), the lifestyle business stays in Stage 3 forever and the v0.8 automation work is what makes that sustainable.

**Applies to:** both Path A and Path B for the architectural needs above. Path A stops here.

### Stage 4: Agency operations (30-100+ active clients)

**Path B only.** GRM is a real agency. Ron is not the only person doing the work. A team of 2-5 handles operations, sales, design, and content. Specialization emerges. Process documentation matters more than code documentation.

Architectural needs: v0.9 and v1.0 territory. Specifically:

- Client self-service dashboard with login, metrics, update request form, invoice history
- Automated client onboarding pipeline (Stripe → contract → generation → deployment)
- Real support ticket system with SLA tracking (Linear, Shortcut, Freshdesk, or similar)
- Role-based access control for team members
- Backup and disaster recovery procedures
- Legal and compliance review of service agreements (especially if clients are in multiple states)
- Multi-location and franchise support for larger clients
- White-label reseller tier if GRM chooses to sell the skill to other agencies

What breaks at this stage: everything that was manual. The folder structure needs to be a real database. The code review process needs to exist. The brand needs to be protected at the product level, not just the site level.

Trigger for moving beyond Stage 4: at 100+ clients GRM is either a successful agency that continues to scale linearly, or it pivots (acquired, sold, franchised, or abandoned in favor of a different product). Not a planning horizon for v0.7.

**Applies to:** Path B only. Under Path A, this stage does not exist.

### The planning horizon

The scale ceiling that matters for v0.7 planning is **30 clients**. Not 10 (too small to justify architectural change), not 100 (too far to plan for, and only relevant under Path B). Every v0.7 decision is made with the test: does this work at 30 clients, and does it avoid painting v0.8/v0.9 into a corner?

The 30-client horizon works for both Path A and Path B because Path A caps somewhere in the 20-50 range and Path B passes through 30 on its way up. v0.7 work is identical in either case.

---

## The v0.7 → v1.0 roadmap

Four versions, four stages, four distinct architectural postures.

### v0.7 (current)

**Focus:** flagship quality at small scale.
**Target:** 1-10 active clients.
**What ships:** the skill as currently documented across 10 files and ~10,500 lines. Manual execution, single-prospect operation, quality-first discipline.

**Exit criteria for v0.7** (quality-based, not quantity-based; all must be true before v0.8 work begins):

- The first signed deal has been live on a custom domain for at least 30 days without a quality complaint
- The full client lifecycle (Stage 1 prospect → Stage 2 signed → Stage 2 live on custom domain → Stage 2 first quarterly refresh) has been executed once end-to-end with no major workflow gaps
- Zero shipped slop on any deployed preview or live client site (verified by Phase 6 hard gates)
- The 12-step onboarding checklist in `deployment.md` has been executed in full at least once with no items deferred or skipped
- The HubSpot pipeline is the working source of truth for at least one deal end-to-end
- No blocking technical debt (Google Places API key rotated, HubSpot pipeline configured, backup running)

These criteria are checkable at any client count. Whether GRM has 1 signed deal or 5, the criteria still test the same thing: did the workflow actually work, end to end, well enough to repeat? Volume metrics like "3 flagships sold" are not the right test because volume is downstream of quality. Quality is what gets tested here.

### v0.8 (automation of pain)

**Focus:** automate the judgment-light repetition that Stage 3 clients force onto Ron.
**Target:** 10-30 active clients.
**What ships:**

1. **Automated quarterly refresh workflow.** A Claude Code command that iterates over every client folder in `_clients/`, checks which clients are due for refresh based on `lastRefreshDate`, runs the refresh procedure, and produces a summary report. Reduces per-client refresh time from 10-15 minutes of manual attention to 2-3 minutes of automation plus human verification.
2. **Automated monthly monitoring report generation.** A script that pulls data from Plausible (via API), Otterly (via API), Google Search Console (via API), and Stripe (via API) and generates per-client monthly reports in the template format from `deployment.md`. Produces 30 reports in the time it used to produce 5.
3. **Centralized client dashboard.** A private web page (hosted internally at a password-protected URL or as a Notion database) showing every active client with: status, last refresh, uptime %, monthly sessions, contact form submissions, invoice status, next action due. Updated daily from a scheduled script.
4. **Pre-flight check automation.** A command that verifies all integrations before starting a new prospect build: Vercel CLI auth, Google Places API quota, Static Forms allowance, HubSpot pipeline state, Ron's local Node.js version. Fails fast if any integration is broken.
5. **HubSpot webhook pipeline sync.** Stripe payment events trigger HubSpot deal stage moves automatically. Removes the manual "move the deal to Signed" step that Ron currently does after every payment.
6. **Folder reorganization to `_clients/`, `_prospects/`, `_archive/` split.** The flat `~/grm-sites-prospects/` structure gets reorganized with the three subdirectories. Existing prospects migrated. SKILL.md path references updated.
7. **LESSONS.md cross-reference automation.** When a new lesson is added to LESSONS.md, the skill auto-tags it with affected file names and phases for easier reference in future builds.

**Exit criteria for v0.8:** Ron can run the quarterly refresh for 20 clients in one focused half-day. Monthly reports for 20 clients generate in under 2 hours of Ron time. HubSpot pipeline stage moves are automatic. Ron is spending less than 40% of time on operations.

**Applies to:** both Path A and Path B. Under Path A, v0.8 is the terminal version; the lifestyle business runs on v0.8 indefinitely.

### v0.9 (interactive features and self-service) — Path B only

**Path B only.** Under Path A (lifestyle business), v0.9 is skipped entirely and GRM stays on v0.8 forever. Read this section only if Path B is the chosen direction.

**Focus:** remove Ron from the Update Request loop entirely for most requests. Add interactive site features that clients increasingly ask for.
**Target:** 30-50 active clients.
**What ships:**

1. **Client self-service dashboard.** Clients log in via magic link (no password), see their own analytics, uptime, recent form submissions, and submit update requests. Reduces the "text Ron about everything" bottleneck.
2. **Client-initiated update request form.** Structured form that captures what the client wants changed, routes to a ticket system, and auto-assigns to the appropriate team member. Removes the manual HubSpot task creation Ron currently does.
3. **Interactive widget library.** Reusable vanilla-JS components for booking calendars, quote calculators, multi-step estimate forms, and project galleries with filtering. Each widget is a self-contained drop-in that can be added to any client site without introducing a framework for the whole site.
4. **Automated review acquisition workflow.** Integration with the client's customer database (via spreadsheet upload or simple CSV import) to send Google review request texts at the right moments in the job lifecycle.
5. **Content hub generator.** A separate Phase in the skill (Phase 9 perhaps) that generates Marion County trade-specific content hubs (e.g., "Marion County Plumbing Licensing Guide"). Uses a separate data capture workflow for permit requirements, cost ranges, and seasonal considerations. This is the Cowork Tier 3 recommendation deferred from v0.7.
6. **Multi-location support.** For clients with 2-5 locations, the skill generates per-location landing pages with localized LocalBusiness schema entries, local testimonials, and location-specific service area content.
7. **Client feedback and testimonial collection.** Automated workflow to request testimonials from satisfied clients and integrate new testimonials into the site on the next quarterly refresh.
8. **Add-on payment portal.** Clients can pay for project-level add-ons (new page, redesign, additional service sub-page) through a self-service Stripe portal rather than negotiating with Ron.

**Exit criteria for v0.9:** average update request turnaround under 24 hours without Ron's involvement. Client self-service dashboard handles 60% of client interactions. GRM has a second person handling 70% of operations, freeing Ron for sales and strategy.

### v1.0 (agency operations) — Path B only

**Path B only.** Under Path A (lifestyle business), v1.0 does not exist. Read this section only if Path B is the chosen direction.

**Focus:** GRM is a real agency with a real team, real process, and real infrastructure. Scale beyond 50 clients requires it.
**Target:** 50-100+ active clients.
**What ships:**

1. **Real support ticket system.** Linear or Freshdesk deployed with SLA tracking, automated escalation, and client-visible ticket history.
2. **Role-based access control for team members.** Multiple team members with different permission levels (sales, operations, design, admin).
3. **Automated client onboarding pipeline.** The 12-step onboarding checklist is fully automated for the parts that can be automated. Stripe payment → HubSpot move → domain setup webhook → Vercel project creation → Google Business Profile verification prompts → initial review push.
4. **CI/CD for site updates.** Every site update goes through a build pipeline that runs automated tests, Phase 6 verification, and deployment. No more manual `vercel --prod` from Ron's local machine.
5. **Backup and disaster recovery.** Every client site, every profile.json, every `client-status.json` backed up nightly to multiple locations. Documented recovery procedure.
6. **Legal and compliance review.** Service agreements reviewed by a business attorney. Privacy policies generated for every client site. CCPA and state-specific compliance where relevant.
7. **White-label reseller tier** (optional). Other agencies use the GRM skill to build sites under their own brand, paying GRM a per-build or monthly licensing fee.
8. **Multi-tenant infrastructure.** Client database replaces the folder structure. Real user authentication. Real permission isolation between team members.

**Exit criteria for v1.0:** GRM can onboard 5 new clients per week without breaking any existing client's service. The architecture supports multi-state expansion beyond Marion County. Ron is running a business, not executing individual builds.

---

## Integration architecture for future add-ons

Several product categories are being deliberately kept separate from the website service in v0.7, with the understanding that they may become GRM products in their own right later. Each one is named here so the architecture does not accidentally couple them to the website service in ways that make them hard to separate later.

### Social media management

**Status:** parked 60 days minimum from first closed deal. Likely v0.9+ target.

**Why separate from websites:** social media management is a fundamentally different service category. It has different deliverables (posts, engagement, analytics), different tools (Buffer, Hootsuite, Meta Business Suite), different pricing models (hours per month rather than hosting fees), and different skill requirements (content creation, community management). Bundling it into the website service would confuse both pricing and delivery.

**How it integrates:** shares the client relationship but has its own deal record, its own billing, and its own delivery cadence. A client can buy websites only, social only, or both. HubSpot tracks each as a separate deal.

### Paid advertising management

**Status:** parked indefinitely. Not a v0.9 target without specific client pull.

**Why separate:** paid advertising management is a high-risk, high-skill service where mistakes cost clients real money (wasted ad spend). It requires deep expertise in Google Ads, Meta Ads, and ad platform APIs. Offering it too early as an add-on risks reputational damage from poorly-managed campaigns.

**How it integrates:** if GRM ever offers this, it is a standalone product with its own deal type, its own monthly minimum (likely $500+), and its own delivery specialist. Not bundled with websites.

### Photography service

**Status:** likely v0.9 target as a partner relationship, not an in-house service.

**Why separate:** professional photography of the client's work is the single biggest gap in the current site generation quality. Real photos of real projects beat any stock photography per the anti-slop rules. But training GRM to be a photography agency is the wrong direction; GRM should partner with a local Marion County photographer who can be booked per-client at a flat rate ($500 for a half-day shoot, delivering 30 photos).

**How it integrates:** when a client signs, GRM offers the photography add-on as a $500 one-time fee. GRM coordinates the shoot with the partner photographer and receives the photos. The photos replace stock imagery in the client's site on the next refresh. The photographer owns their own business relationship; GRM is a booking and curation layer.

### AI consultation service

**Status:** v0.9+ potential. Currently embodied in this skill but not packaged as a standalone product.

**Why separate:** Ron's accumulated knowledge of AI citation is a real asset. Other Marion County business owners and even other agencies might pay for 60-minute consultations on their AI search strategy. Packaging this as a standalone service (hourly rate, flat-fee audits, or retainer) is worth considering once the core website service is stable.

**How it integrates:** would be a separate deal type in HubSpot with its own billing. Could be a feeder to the website service (audit reveals gaps, recommend GRM's site build as the fix).

### Content marketing service

**Status:** v0.9+ target if quarterly refresh workflow proves successful.

**Why separate:** ongoing blog post production, long-tail keyword content, and topical authority building are a different discipline from site generation. Requires writers, editors, and a content calendar. GRM's v0.7 skill produces the baseline content but does not sustain ongoing content output.

**How it integrates:** could be offered as a separate monthly retainer ($500-1000) on top of the website monthly fee. Deliverable: 2-4 fresh blog posts or resource pages per month, hand-written or Claude-assisted, integrated into the existing site.

### Email marketing integration

**Status:** not a GRM product. On-demand add-on only.

**Why separate:** email marketing platforms (Mailchimp, Klaviyo, ActiveCampaign) are specialized tools that clients who use them are already using. GRM's role is integration, not replacement. If a client uses Mailchimp, the contact form feeds Mailchimp. Otherwise, nothing.

**How it integrates:** a one-time integration setup ($100-200 add-on) that wires the Static Forms submission flow into the client's email platform via Zapier or Make.com.

### The shared pattern

Every future add-on is structured as: separate product, separate deal, separate billing, shared client relationship. The website service is the anchor that earns the client relationship. Everything else is an upsell that rides on top of the relationship without complicating the website service's pricing or delivery.

The architectural rule: do not bundle fundamentally different service categories into the website monthly fee. Bundling creates scope ambiguity and makes pricing impossible to explain.

---

## Data preservation as an architectural principle

This section is short but it ranks among the most important principles in the entire file. It establishes a rule that should drive backup, versioning, and migration decisions at every version of GRM.

**The principle:** `profile.json` files are the core institutional asset of GRM Web Services. Code can be rewritten. Data cannot.

Every `profile.json` in `~/grm-sites-prospects/[business-slug]/` represents 1-2 hours of manual research work: deep site crawling, Phase 2 multi-page extraction, Phase 3 photo curation, Phase 3.5 data quality validation, and the irreplaceable client-relationship context that Ron accumulated during the prospect interaction. The captured business name, the real owner names, the verified license numbers, the testimonials with real first names and cities, the captured services with real descriptions, the photo asset paths, the Google review counts at capture time — all of this is research output, not generated content.

If a `profile.json` is lost, none of it can be recovered without re-doing the research from scratch. The skill files can be restored from `grm-automations` on GitHub. The CSS framework, the section patterns, the SEO templates — all of these are version-controlled and recoverable. But the prospect-specific data lives only on Ron's local machine, and losing a prospect folder is permanent data loss.

This principle has four direct consequences for architecture decisions:

### Consequence 1: Backup is non-negotiable

The "no automated backup" item in the technical debt inventory is the highest-priority debt to resolve. Not because backup is fashionable infrastructure but because losing a single profile.json is worse than losing the entire skill codebase. Backup must be running before the second client signs.

### Consequence 2: profile.json structure changes are migrations, not refactors

When the v0.8 work introduces new fields to `profile.json` (e.g., `lastRefreshDate`, `monitoringSetup`, `bingPlacesClaimed`), the change cannot be a destructive rewrite. Existing profile.json files must be migrated to the new structure with their existing data preserved. Phase 1 of any v0.8+ skill run should include a migration check that detects an old-format profile.json and upgrades it before proceeding.

### Consequence 3: Data and code live separately

The `~/grm-sites-prospects/` tree (data) is never committed to the public `grm-automations` repo (code). The line between data and code is also the line between what gets backed up where. Code lives in GitHub. Data lives in private backup. Mixing them creates security risks (committing API keys) and organizational confusion (where does this file live?).

### Consequence 4: Migration paths are documented before they're needed

Every potential migration (Vercel → Netlify, Static Forms → Web3Forms, profile.json v1 → v2) should have a documented migration path written before the migration is needed, not after. The risk inventory above names several vendors where migration may eventually be necessary. For each, the migration steps should live in `deployment.md` so a future Ron (or future team member, or future Claude session) does not have to invent the procedure under time pressure during an outage.

### Why this is in scale-architecture.md and not deployment.md

`deployment.md` documents how backup and migration actually run in practice. This file documents why backup and migration are non-negotiable architectural concerns, not optional polish. The why has to be louder than the how, because the how is easier to defer when the schedule gets tight. Naming this as a constitutional principle means it cannot be deferred without an explicit version-bump decision documented here.

---

## Technical debt inventory

Things v0.7 knowingly defers. Each entry names the debt, the reason for deferral, and what it will cost to pick up later.

### Google Places API key rotation

**Debt:** the current API key is stored at `~/grm-sites-prospects/.env` and was exposed in a prior chat session. It has been flagged for rotation since that session but has not been rotated yet.
**Deferral reason:** rotation is a manual task that is not blocking the v0.7 skill build. It is blocking clean production operation.
**Cost to pick up:** 15 minutes. Generate new key in Google Cloud console, update the `.env` file, test a Places API call, confirm the skill works. Must happen before any client deployment that uses Google Places data.

### Flat folder structure

**Debt:** `~/grm-sites-prospects/` currently contains a mix of active prospects, one signed client (T&F when signed), the Plan B reference library, and the `.env` file. No separation.
**Deferral reason:** reorganizing now would break the skill's hardcoded path references and the cost outweighs the benefit at 1-3 active prospects.
**Cost to pick up:** 2-4 hours in v0.8. Create `_clients/`, `_prospects/`, `_archive/` subdirectories. Migrate existing prospects. Update SKILL.md path references. Update `deployment.md` references. Test with a known-good prospect.

### HubSpot pipeline setup

**Debt:** HubSpot is referenced throughout `deployment.md` as the source of truth for client state, but the pipeline has not yet been configured with the required stages and custom properties.
**Deferral reason:** HubSpot setup was deferred in the original v0.7 session to focus on the skill build.
**Cost to pick up:** 2-3 hours. Create the pipeline, add stages (Prospect, Preview Sent, Signed, Live, Delinquent, Offboarded), add custom properties (Preview URL, Pricing Tier, Deal Type, Monthly Amount, Buyout Option, Signed Date, Last Refresh Date), configure workflow automations. Must happen before closing the first deal.

### The `grm-website` Vercel orphan

**Debt:** an unused Vercel project named `grm-website` exists under the `ron-7323` team. Confirmed safe to delete in a prior session but has not been deleted.
**Deferral reason:** cleanup is not blocking anything.
**Cost to pick up:** 2 minutes. `vercel projects rm grm-website`. Not urgent.

### Magic MCP integration

**Debt:** the 21st-dev Magic MCP server that was originally planned to pull live 21st.dev component code has had vendor-side bugs preventing registration in Claude Code sessions. Plan B (local reference library at `~/grm-sites-prospects/plan-b-reference/`) is the active mode.
**Deferral reason:** vendor bug blocks resolution.
**Cost to pick up:** unknown. Depends on when 21st.dev ships a fix. Monitor the GitHub issue. If Magic MCP becomes functional, evaluate whether switching back from Plan B is worth the effort (possibly not; Plan B has been working).

### No automated backup of prospect folders

**Debt:** the `~/grm-sites-prospects/` tree lives only on Ron's local Mac. No automated backup exists. A hard drive failure would lose every client's site and every captured profile.
**Deferral reason:** no budget or time allocated in v0.7 for backup infrastructure.
**Cost to pick up:** moderate. Options: (1) scheduled rsync to an external drive, (2) nightly sync to a private GitHub repo per client (avoids committing secrets via gitignore discipline), (3) cloud backup via Arq or Backblaze. v0.8 target, before client count exceeds 5.

### No CI/CD for skill file changes

**Debt:** the skill files in `~/.claude/skills/prospect-site/` are edited directly on Ron's local machine with no version control beyond the `grm-automations` GitHub repo (which is committed to manually, not automatically).
**Deferral reason:** v0.7 is a single-developer project; CI/CD overhead outweighs benefit.
**Cost to pick up:** moderate. v0.9 target when the second team member starts editing skill files. Options: (1) pre-commit hooks that validate skill file changes, (2) PR-based review cycle on the grm-automations repo, (3) automated tests against a known-good prospect.

### No structured LESSONS.md accumulation

**Debt:** the LESSONS.md seed file (to be written next) establishes the format but does not yet have institutional lessons committed to it. Every v0.7 build produces zero, one, or more lessons and should append them automatically, but the workflow for appending is manual as of v0.7.
**Deferral reason:** the file does not exist yet.
**Cost to pick up:** negligible. Create the file with the seed format and let Phase 8 append to it on every build.

### No cross-file consistency checking

**Debt:** the 9 skill files reference each other constantly (e.g., `seo-geo.md` references Phase 5.5, which is documented in `SKILL.md`, which references `deployment.md` for Phase 7). If a change is made in one file without updating the others, inconsistencies accumulate.
**Deferral reason:** automated consistency checking is a v0.8 target. Currently Ron is the consistency checker.
**Cost to pick up:** significant. v0.9 target. Options: (1) a Claude Code command that reads every skill file and checks for cross-reference integrity, (2) structured metadata at the top of each file declaring its dependencies, (3) a shared glossary file that both documents terms and enforces definitions.

---

## Risk inventory

Technical debt is "things we chose to defer." Risks are "things that could go wrong and are outside GRM's control." Both deserve to be named explicitly. Each risk below has a likelihood, an impact, and a mitigation strategy. Review this inventory quarterly during the business review.

### Vendor risk: Static Forms shutdown

**The risk:** Static Forms is a small vendor. If they shut down, change pricing, or change terms, every contractor site that uses them for contact form submission would break or require migration.

**Likelihood:** medium. Small vendors have shorter expected lifetimes than large ones.

**Impact:** moderate. Contact form submission is the primary lead capture path; broken forms break the conversion funnel. But every prospect site uses the same form structure, so a migration to a new vendor would affect all clients simultaneously and could be executed via a single script.

**Mitigation:** keep the form structure portable. The current Static Forms wiring uses a standard HTML form with standard hidden fields; switching to Web3Forms (the runner-up backup vendor named in the Cowork research) would require swapping the action URL and the field names but not restructuring the form. Document the migration steps in `deployment.md` ahead of need.

### Pricing risk: Google Maps Platform credit reduction

**The risk:** Google Places API costs are currently absorbed by the $200/month Google Maps Platform free credit. At current usage (~$5/month for 30 active clients), GRM uses about 2.5% of the free credit. If Google reduces or eliminates the credit, the math changes.

**Likelihood:** low to medium. Google has signaled stability of the credit, but Google has also discontinued products on short notice in the past.

**Impact:** moderate. At the scale where the credit removal would matter (v0.9+), the per-client cost might be $0.50-2/month, which is absorbable into the monthly fee but tightens margins.

**Mitigation:** monitor Google Cloud billing monthly. If credit reduction is announced, evaluate alternatives (manual photo upload, scraping at the legal-clean tier, or building a local image library). Adjust pricing before the change takes effect, not after.

### Platform risk: Vercel Hobby tier restrictions

**The risk:** Vercel currently provides a generous free Hobby tier that supports unlimited deployments and bandwidth for personal projects. If Vercel restricts free usage, raises prices on the Pro tier, or eliminates the Hobby tier, GRM's hosting costs change.

**Likelihood:** low. Vercel's business model depends on developer adoption, and the Hobby tier is the primary acquisition funnel.

**Impact:** high if it happens. Every client site is hosted on Vercel. A price change would either pass to clients (raising the monthly fee) or cut into GRM margins.

**Mitigation:** keep the generated sites portable. Plain HTML/CSS/JS sites can be hosted on Netlify, Cloudflare Pages, GitHub Pages, or any static host with a few hours of migration work per client. Document the Vercel-to-Netlify migration steps in `deployment.md` ahead of need. The portability of plain HTML is a feature, not just a constraint.

### Vendor bug risk: 21st.dev Magic MCP

**The risk:** the Magic MCP server has been broken for weeks (vendor-side bug). Plan B (the local component reference library at `~/grm-sites-prospects/plan-b-reference/`) is the active mode and works, but it is a workaround.

**Likelihood:** ongoing. The vendor may or may not fix it.

**Impact:** low currently because Plan B works. Higher if Plan B reveals limitations as the skill evolves.

**Mitigation:** treat Plan B as the long-term path. Do not plan around Magic MCP returning. If Magic MCP is fixed and shipped, evaluate switching back as a non-urgent improvement, not a recovery. The architectural decision: assume Plan B is permanent. Anything else is upside.

### Single-person-of-failure risk: Ron

**The risk:** GRM in v0.7 and early v0.8 is 100% Ron-dependent. Ron getting sick, injured, taking a vacation, or facing any personal emergency stops all GRM operations. Existing clients have no continuity plan. New deals cannot close.

**Likelihood:** the question is not "if" but "when." Single-person operations have a 100% failure rate at some time horizon.

**Impact:** very high. Even a one-week absence creates client communication gaps, missed quarterly refreshes, and delayed update requests. A longer absence could lose clients permanently.

**Mitigation:** the only real mitigation is having a second person trained on at least the operational basics. Path A (lifestyle business) needs a virtual assistant who can handle update requests during Ron's absence. Path B inherently solves this through team building. Either way, this risk should drive the decision to bring in a second person earlier rather than later, even if pure economics would defer it.

Document fail-over procedures: who has access to what, where the credentials live, how a substitute would handle a client emergency. Even if Ron is the only operator today, a substitute could take over with documentation.

### Landscape shift risk: AI citation thesis becomes invalid

**The risk:** The Cowork AI citation research is current as of April 2026. The strategic thesis depends on findings holding: 17% overlap between AI citations and traditional SEO, 36% improvement from schema markup, 44.2% of citations from the first 30% of a page. If LLM vendors change what they prioritize in 6-12 months, the entire technical foundation may need to shift.

**Likelihood:** medium. AI search is in a rapid evolution period. Things that work today may not work in 18 months.

**Impact:** very high if it happens. The entire commercial thesis depends on these findings.

**Mitigation:** treat the AI citation research as time-bound. Re-validate the thesis every 6 months by re-running the Cowork research process. Track AI-referred sessions in client analytics monthly. If AI-referred traffic stops growing or starts declining, that is the early warning signal. Update `seo-geo.md` and the strategic framing in this file as the landscape shifts.

The deeper mitigation: do not over-commit to any single tactic. The skill builds sites with strong schema, semantic HTML, BLUF content, and AI crawler access. These are durable web fundamentals regardless of which AI platforms exist in the future. Even if the specific AI citation findings shift, the underlying disciplines hold.

### Market saturation risk: Marion County is finite

**The risk:** Marion County has a finite number of home services contractors. The current prospect list (61 in Batch 1) represents a meaningful fraction of the addressable market. At 30-50 active clients, GRM may be running out of qualified prospects in Marion County.

**Likelihood:** certain at sufficient scale. The question is how soon.

**Impact:** moderate. Hitting the Marion County ceiling forces a strategic decision: expand geographically, expand to other trade categories, or cap growth (which is fine under Path A).

**Mitigation:** track the addressable market actively. Maintain the prospect list and update it quarterly. When the active-client count exceeds 30% of the qualified prospect pool, plan for expansion: either to neighboring counties (Sumter, Lake, Citrus, Levy, Alachua) or to non-home-services categories (restaurants, dental practices, fitness studios).

Under Path A, market saturation is a feature, not a bug. A capped market enables a stable lifestyle business. Under Path B, geographic or category expansion becomes mandatory at the saturation threshold.

### Competitor copycat risk: no real moat beyond execution

**The risk:** the skill files and the strategic thesis are documented in this repository. Another local agency could read them, reverse-engineer the approach, and compete on identical terms. There is no technical or legal moat.

**Likelihood:** medium-low in the short term (small agencies are unlikely to find this work and execute on it within 6-12 months) but rising over time as AI citation becomes a more common topic.

**Impact:** moderate. Real competition would compress margins and slow client acquisition but would not destroy the business. The first-mover advantage in Marion County is real but not permanent.

**Mitigation:** the moat is execution speed and relationship trust, not the strategy itself. Move fast in the first 12 months to establish the GRM brand as the Marion County AI search agency. After that, the moat is the existing client base, the case studies, and the local relationships, not the technical playbook. If competitors emerge, they compete for new prospects; existing clients stay with GRM because of relationship, not technology.

Do not try to keep the skill files secret. The institutional learning embedded in them is the real value, and that learning compounds inside GRM faster than competitors can copy it.

### Client expectation mismatch risk: slow ROI realization

**The risk:** traditional SEO takes months to produce measurable results. AI citation is emerging but most contractor clients do not know how to measure it. A client at day 60 may say "I'm not seeing more leads, where's the ROI?" before the work has had time to compound.

**Likelihood:** high. This is the most common cause of client churn in any web services agency.

**Impact:** moderate per client. High if it becomes a pattern.

**Mitigation:** set expectations during the sales conversation explicitly. "AI search is growing 527% year over year and is currently 1-2% of total search traffic in your category. In 12 months it could be 5-10%. We are building you the foundation that captures that growth as it arrives, not chasing it after the fact." Frame the monthly fee as positioning, not direct lead generation.

The monthly client update email template in `deployment.md` is part of this mitigation. Visible communication about what GRM is doing each month makes the ongoing value tangible even when leads are slow to materialize. The quarterly refresh protocol gives the client something they can point to as evidence of work being done.

If a client churns at 60 days citing ROI, that is a signal to refine the sales conversation, not necessarily a failure of the work. Track churn reasons and use them to update the qualifier criteria for future prospects.

### Risk review cadence

Review this inventory quarterly during Ron's business review. For each risk:

1. Is the likelihood still accurate?
2. Is the impact still accurate?
3. Has anything changed that requires a new mitigation?
4. Are there new risks to add?

The risk inventory is a living document. New risks emerge as GRM scales. Old risks get retired as mitigations land.

---

## Migration triggers

Every architectural change in the roadmap has a trigger. Triggers are metric-based, not time-based, to avoid premature changes. "In six months we should build X" is weak. "When active client count crosses 15, we should build X" is enforceable.

| Trigger | Action | Rationale |
|---|---|---|
| Active client count crosses 5 | Deploy automated backup of prospect folders | Data loss risk becomes unacceptable |
| Quarterly refresh takes more than 4 hours per cycle | Build v0.8 refresh automation | Ron's time is the constraint |
| Monthly monitoring reports take more than 30 min per client | Build v0.8 report automation | Same |
| Active client count crosses 15 | Reorganize folder structure to `_clients/`, `_prospects/`, `_archive/` | Flat structure becomes confusing |
| Active client count crosses 20 | Hire second team member (VA or junior dev) for operations | One-person model breaks |
| Active client count crosses 30 | Deploy v0.9 self-service dashboard | Ron cannot personally handle every update request |
| Update request backlog exceeds 72 hours | Deploy v0.9 ticket system | Client satisfaction suffers |
| Active client count crosses 50 | Begin v1.0 agency infrastructure planning | Scale requires real process |
| Ron's operations time exceeds 50% of workweek | Hire operations lead | Sales time is more valuable |
| Any single client generates more than 20 update requests per month | Evaluate client fit; possibly flag as unprofitable | Some clients are not worth the monthly fee |

These triggers are the planning horizon. Check them quarterly during Ron's business review. When a trigger fires, act.

---

## What NEVER changes

A small number of principles stay constant from v0.7 to v1.0. These are the things that define GRM Web Services regardless of scale.

1. **Quality over scale.** Every version of the skill prioritizes output quality over throughput. Shipping a mediocre site to hit a quota is never the right answer. The eye test, the swap test, and the six-check self-test are non-negotiable at every scale.

2. **Fact-based content, zero fabrication.** Every fact on every generated site is either captured from the prospect's real data or omitted. This rule does not relax at v1.0. Scale does not justify making up testimonials, credentials, or services.

3. **GRM voice discipline** (Closing Table, Saturday Morning, Front Porch voice mapping per `content-rules.md`). The voice rules apply at every version. Banned phrases are banned at v1.0 just as they are at v0.7. Scale does not justify marketing filler.

4. **AI citation as the north-star metric.** The commercial thesis of GRM is built on the 17 percent gap between traditional SEO and AI citation. Every version of the skill must preserve the structural advantages that earn AI citations: comprehensive schema, BLUF content, semantic HTML, AI crawler access, FAQPage markup. Scale does not justify cutting corners on the technical foundation.

5. **The client owns their domain.** Domains always belong to clients, not GRM. Even at v1.0, when automated onboarding might register domains on a client's behalf as a convenience, the domain is registered under the client's name and control. This rule protects both sides of the relationship.

6. **Ron is accountable for every deliverable, even when he did not execute it.** At v0.7 Ron does everything. At v1.0 Ron has a team that handles most operations. But every client still belongs to Ron in the sense that Ron is ultimately responsible for the work that goes out under GRM's name. A team member's failure is Ron's to address.

7. **Transparency over convenience in pricing.** Pricing tiers are clear and public. No hidden fees, no surprise add-ons, no "we forgot to mention this charge." Clients always know what they pay and why. This rule applies at every scale.

These seven principles are the constitution. Everything else is policy, and policy can change. The constitution does not.

---

## Assumptions baked into this file

The roadmap, the migration triggers, and the constitutional principles all rest on a set of assumptions about the world and about GRM's market. Each assumption below is treated as fact in the rest of this file. None of them is permanent. Each one should be revisited at every quarterly business review and at every version bump.

Naming the assumptions explicitly serves two purposes: it makes them debatable rather than invisible, and it gives future-Ron a clear list to test against new evidence as the business evolves.

### The market assumptions

1. **Marion County is the target market in the near term.** Geographic expansion is deferred until Marion County is saturated or until a specific opportunity makes expansion compelling. The whole skill is calibrated for Marion County voice rules, Florida-specific regulations, local landmarks, and Marion County contractors. **When this changes:** if the addressable Marion County market is exhausted before client revenue justifies it, expand to neighboring counties (Sumter, Lake, Citrus, Levy, Alachua) one at a time, updating voice rules and regional details for each.

2. **Home services contractors are the target trade category.** Plumbers, electricians, HVAC, roofers, painters, fencers, pool builders, landscapers, pressure washers, pest control. The skill's preset patterns, FAQ templates, and component recommendations all assume home services. **When this changes:** other trade categories (restaurants, dental practices, fitness studios, professional services) would require different content patterns, different schemas, and different voice calibration. v0.9+ extension territory.

3. **Single-location contractors are the primary segment.** The skill has no architecture for multi-location businesses or franchises. Every business is treated as having one address, one phone, one service area. **When this changes:** v0.9 multi-location support is named in the roadmap. A specific large client needing it is the trigger.

4. **Marion County's home services market has 100-300 qualified prospects.** Based on the Batch 1 list of 61 home services businesses plus follow-up batches yet to be built. The exact number is unknown but is finite and bounded. **When this changes:** track the actual prospect pool quarterly. If qualified prospects are running low, expand or pivot.

### The commercial assumptions

5. **The AI citation thesis holds for at least 24 months.** The 17% overlap between AI citations and traditional SEO, the 36% improvement from schema markup, the 44.2% citation weight in the first 30% of a page — these findings are current as of April 2026 and are assumed to remain directionally true through April 2028. **When this changes:** re-run the Cowork research process every 6 months. If findings shift significantly, the seo-geo.md file gets a major update and the strategic framing in this file gets revisited.

6. **Contractors will pay $100-250/month for ongoing website service.** Pricing is set at Tier 1 Elevate ($1,000 setup + $250/month or $1,500 buyout) and Tier 2 Launch ($500-650 setup + $100/month or $800 buyout). **When this changes:** if monthly retention is poor at these prices, raise or lower to find the right level. If clients consistently buy out instead of staying monthly, the buyout price is too low or the monthly value proposition is too thin.

7. **Clients prefer monthly recurring over buyout.** The roadmap is structured to favor monthly clients because they generate predictable recurring revenue. **When this changes:** if buyout consistently outpaces monthly, adjust pricing or accept that the business model is one-time projects rather than recurring service. Either is viable, but they require different operational structures.

8. **Marion County contractors are reachable via cold outbound calling.** The Cameron-and-Ron dial strategy assumes that 60 dials/day produces 4 live conversations and 1 close per week. **When this changes:** if cold dialing produces poor conversion, switch to inbound (content marketing, SEO of GRM's own site, paid search) or referral (existing clients recommending GRM to peers). The skill works regardless of acquisition channel; only the sales workflow changes.

### The operational assumptions

9. **Photography is partner-sourced, not in-house.** The architecture assumes GRM books a local Marion County photographer for client photo shoots rather than buying camera equipment and learning photography. **When this changes:** if no suitable local photographer can be found, or if Ron decides photography is a core skill worth developing in-house, the photography service becomes a different product structure.

10. **Email marketing is not a GRM product.** The skill does not generate or manage email campaigns. **When this changes:** if a meaningful number of clients ask for email marketing as an add-on, evaluate adding it as a paid service with its own pricing and delivery workflow. Until then, email marketing is an integration ("we'll wire your contact form into your existing Mailchimp"), not a product.

11. **Client growth is linear or compounding, not stepwise.** The roadmap assumes GRM picks up 1-3 new clients per month under steady state, not 10 in one month and zero for three months. **When this changes:** if the growth pattern is highly variable, the operational stress points may not match the migration triggers. Re-calibrate triggers to fire on whichever metric is the leading indicator (active client count, weekly hours on operations, etc).

12. **Vendor stability holds for the v0.7 → v0.8 timeline.** Vercel, Static Forms, Google Places, HubSpot, Stripe, Plausible, and Otterly are all assumed to remain available, priced as expected, and operationally stable for the next 12-18 months. **When this changes:** the risk inventory above names each vendor and the migration path. If a vendor changes terms or shuts down, execute the documented migration.

### The strategic assumptions

13. **Path A vs Path B is a meaningful choice.** This file is dual-pathed because lifestyle and agency are both viable. The assumption is that Ron actually has the choice, that neither path is forced by external circumstances. **When this changes:** if external factors (financial pressure, family obligation, market force) force one path or the other, this file gets simplified to reflect the chosen path and the dual-path framing is removed.

14. **Quality is differentiating, not table stakes.** The strategic thesis assumes that AI-citation-optimized contractor sites are rare enough in Marion County that GRM's quality bar is a real competitive advantage. **When this changes:** if a competitor enters the same market with the same playbook, quality becomes table stakes and GRM's moat shifts to relationships, response time, and case studies rather than technical execution.

15. **Ron is the founder and the constraint, not just the operator.** The file assumes Ron is making strategic decisions about the business as well as executing on them. **When this changes:** if GRM brings in a co-founder, an investor, or a board, strategic decisions become shared, and this file should be updated to reflect the decision-making structure.

### Reviewing assumptions

At every quarterly business review, walk through the 15 assumptions above. For each one, ask:

1. Is this still true?
2. What new evidence has emerged?
3. Does anything need to change in the roadmap because this assumption shifted?
4. Are there new assumptions to add?

The goal is not to be right about every assumption. The goal is to know when an assumption breaks before the consequences become expensive.

---

## The v0.7 scale-readiness test

Before moving from v0.7 to v0.8, verify v0.7 is actually ready for the transition. "We built more features" is not a readiness test. "We proved the workflow works end-to-end" is.

### Exit criteria for v0.7 (must all be met before v0.8 work begins)

These are quality-based, not quantity-based. Whether GRM has 1 signed deal or 5, the criteria test the same thing: did the workflow actually work, end to end, well enough to repeat?

1. **First signed deal live for 30+ days without quality complaint.** At least one contractor client has paid the setup fee, gone through custom domain migration, and been live on their real domain for at least 30 days. No quality complaints from the client. The site is producing measurable activity (form submissions, calls, or analytics traffic).

2. **Full lifecycle executed end-to-end.** The entire client journey has been completed at least once for one client: prospect identified → preview generated → sales conversation closed → service agreement signed → setup fee paid → custom domain migration completed → 12-step onboarding finished → first quarterly content refresh executed (or scheduled if not yet at 13 weeks). No corners cut. No checklist items deferred or skipped.

3. **Zero shipped slop on any deployed asset.** No preview URL and no live client site contains any banned pattern from `anti-slop-rules.md`. Every shipped asset passes Phase 6 hard gates and the human-judgment six-check self-test. The quality bar holds under the pressure of real client delivery.

4. **HubSpot pipeline is the working source of truth for at least one deal.** The deal exists in HubSpot with correct stage, all custom properties populated (Preview URL, Pricing Tier, Deal Type, Monthly Amount, Buyout Option, Signed Date, Last Refresh Date), and linked documents (signed agreement, payment confirmation). No "mental tracking." No informal lists.

5. **Monthly monitoring report delivered for at least one client.** The first monthly client update email has been sent using the template from `deployment.md`. The four-layer monitoring stack (uptime, analytics, AI citation, search presence) is collecting data for the live client. The report process has been validated end-to-end.

6. **No blocking technical debt.** From the technical debt inventory above: Google Places API key has been rotated, HubSpot pipeline has been configured with the required stages and custom properties, and an automated backup of `~/grm-sites-prospects/` is running on at least a daily cadence. These items must be resolved before v0.8 work begins.

7. **The workflow is repeatable without skill changes.** Closing the second deal does not require modifying any skill file. The first signed client revealed any blocking workflow gaps, and those gaps were closed in v0.7 itself, not deferred to v0.8.

If any of these is not met, do not start v0.8 work. Finish v0.7 first. The temptation to start automating the next version before the current version is proven is the single biggest scope creep risk.

---

## Scale metrics to track

A small number of metrics that matter at every stage. Track them weekly during Ron's business review.

- **Active client count.** The primary scale metric. Every trigger above references this number.
- **Average quarterly refresh time per client.** Measured in minutes. Target: under 15 at v0.7, under 5 at v0.8.
- **Average monthly report generation time per client.** Target: under 15 minutes at v0.7, under 5 at v0.8.
- **Update request turnaround time, median.** Target: under 24 hours for Quick, under 5 days for Standard.
- **Update request backlog (oldest open request).** Target: under 48 hours at any scale.
- **Ron's weekly time split: sales vs operations vs strategy.** Target: 50/30/20 at v0.7, 60/20/20 at v0.8, 50/10/40 at v0.9 (with second team member handling operations).
- **Churn rate (monthly).** Target: under 5% at any scale.
- **Average monthly recurring revenue per client.** Target: $175 blended (mix of Elevate $250 and Launch $100).
- **Client NPS.** Target: over 50. Ask once per quarter.
- **AI citation hit rate.** Percentage of target queries for which each client is cited by at least one of the five AI assistants. Target: over 40% at 90 days post-launch.

These metrics are the dashboard. If any of them drifts significantly from target, investigate before shipping more features.

---

## When to abandon vs evolve

A real CTO question: at what point does the architecture need to be torn down and rebuilt instead of iterated?

The rule: iterate when the current architecture can be extended to meet the new need. Rebuild when extending the current architecture costs more than rebuilding from scratch.

### Signs that iteration is working

- New features ship in days, not weeks
- Code and documentation updates touch a small number of files per change
- Bug fixes are local and do not cascade across the skill
- Client onboarding speeds up over time as the team learns the process
- Ron's time per client decreases as scale increases

### Signs that a rebuild is needed

- New features consistently require changes in 5+ files
- Bug fixes trigger regressions elsewhere in the skill
- Onboarding a new client takes longer than it did six months ago
- Ron's time per client increases as scale increases (diseconomy of scale)
- The skill file count grows faster than the value delivered
- The institutional knowledge of how the skill works lives in Ron's head, not in the files
- A new team member takes more than two weeks to contribute meaningfully

When three or more rebuild signs are present, stop and plan a rebuild. A rebuild is not a failure; it is a planned transition to a new version that starts clean.

### What rebuilds look like

Rebuilds happen between major versions, not within a version. The relationship between iteration and rebuild depends on which path GRM is on:

- **Under Path A (lifestyle business),** v0.7 iterates to v0.8 and stops there. There is no v0.9 and no v1.0, so there is no rebuild. The v0.8 architecture is the terminal version. Iteration is the only mode.
- **Under Path B (real agency),** v0.7 iterates cleanly to v0.8 (automation of existing manual workflows) and v0.8 iterates cleanly to v0.9 (interactive features and self-service on top of the existing skill). The v0.9 → v1.0 transition is the one place a rebuild is likely, because agency infrastructure (multi-tenant database, role-based access control, real CI/CD, team collaboration) is a fundamentally different architecture than single-developer skill operation. v1.0 may need to be designed from scratch as agency software, with the v0.9 skill becoming one component of a larger system rather than the whole system.

The planning rule for both paths: every version should be written as if it will be thrown away and replaced in 12-18 months. This frees the current version from trying to anticipate every future need and lets the current version focus on what it actually has to do right now. Under Path A this rule is theoretical (v0.8 is terminal). Under Path B it is practical (v0.7 will be replaced, v0.8 will be replaced, v0.9 may be replaced).

---

## Integration with other skill files

This file is the north star. Other files in the skill package are either locked at v0.7 or are roadmap-aware, and this section documents the difference.

### Files that are locked at v0.7 (do not change without a version bump)

- `anti-slop-rules.md` — the banned patterns are permanent. Adding new bans is allowed; removing bans requires an explicit version review.
- `content-rules.md` — the voice rules (Closing Table, Saturday Morning, Front Porch) are constitutional and do not change.
- `SKILL.md` phases 1-8 — the phase structure is stable. Changing phase boundaries requires a version bump.

### Files that are roadmap-aware (can evolve with each version)

- `hero-patterns.md` — will get new hero patterns in v0.8+ if client diversity demands them.
- `section-patterns.md` — will get new sections (content hubs, interactive widgets) at v0.9.
- `css-framework.md` — the CONFIG block can add new variables as design needs evolve.
- `image-handling.md` — the photo pipeline may evolve (e.g., AI-powered quality scoring in v0.9).
- `seo-geo.md` — the AI citation landscape is evolving fast; this file gets re-reviewed every 6 months.
- `deployment.md` — the client lifecycle procedures will evolve as the team grows and automation increases.

### Files that exist to persist knowledge across versions

- `LESSONS.md` — the institutional memory file. Accumulates entries across every version, never deleted or reset.
- This file (`scale-architecture.md`) — updated with each version bump to reflect the new current state.

### Cross-file dependencies

- `SKILL.md` is the entry point. Every other file is loaded by a specific phase documented in `SKILL.md`.
- `deployment.md` bridges the skill work (Phases 1-8) and the operational work (client lifecycle). Any change to Phase 7 or Phase 8 in `SKILL.md` must be reflected in `deployment.md`.
- `anti-slop-rules.md` is referenced by `hero-patterns.md`, `section-patterns.md`, `css-framework.md`, `content-rules.md`, and `seo-geo.md`. A change to anti-slop rules affects all of these files.
- `seo-geo.md` references facts captured in Phase 2 via `profile.json`. Any change to `profile.json` structure must be reflected in `seo-geo.md` schema templates.

### When to update this file

Update `scale-architecture.md` whenever:

- A new major version is released (v0.8, v0.9, v1.0)
- A migration trigger fires and the corresponding action is taken
- The technical debt inventory changes (items resolved or new items added)
- The commercial thesis evolves meaningfully (e.g., if AI citation research produces new findings that reshape the strategy)
- A "never changes" principle is challenged and either reaffirmed or updated

Do not update this file for routine changes within a version. Routine updates belong in the relevant per-function file.

---

## Version

scale-architecture.md v0.7.0. The north-star file. Written April 9, 2026 at the end of the v0.7 build session. Its audience is future-Ron, future GRM team members, and future Claude sessions that need to understand "why is the skill the way it is" and "what does the next version look like." Every constraint, every deferral, every roadmap item is named with reasoning. This file should be updated at every major version bump. The scale ceiling framework, the roadmap, and the seven never-changes principles are the planning horizon for the next 24 months of GRM Web Services.

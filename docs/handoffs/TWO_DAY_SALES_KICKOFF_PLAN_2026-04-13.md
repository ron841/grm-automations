# TWO-DAY PLAN — SALES KICKOFF

**Drafted:** Monday 2026-04-13, ~11:00 AM
**North star:** Ron dials Wednesday 2026-04-15 after lunch. Cameron observes.
**Working window:** Monday afternoon + evening → full Tuesday → Wednesday AM → kickoff at lunch.

---

## Status at the time of this plan

### What shipped this morning (Stream 2 closed)

- `grm-browser` engine installed at `~/grm-automations/tools/grm-browser/` — four primitives (capture, extract, probe, compare). Playwright Chromium, 2s/domain politeness, 14-day cache prune. Smoke tests green.
- `site-review` mission v1 installed as thin wrapper — five checks: logo-is-image, og-image-brand-color, featured-service-image-rotation, wow-gap-structural, mobile-render-baseline.
- Commit `f56b7cc` pushed to `origin/main`.
- Known v1.1 patch items logged in commit: site-review blind to CSS `background-image` duplicates; Tier-2 logo check too permissive (accepts any og:image). Both non-blocking for this two-day window.

### Existing state (carried in from Friday handoff)

- v0.7.2 installed locally, not yet proven on a clean run against a fresh prospect. The T&F v07 rebuild (Monday afternoon block) doubles as that validation.
- T&F v07 live at `https://tandf-electric-v07.vercel.app` — site-review surfaced OG color 144° off brand (og:image is `gp-01.jpg`, sky-blue dominant). Built on v0.7.1 before the OG color rule existed.
- Flagship 1 at `https://tandf-electric.vercel.app` — untouched, stays as-is.
- Service agreements (Elevate + Launch), pricing one-pager, order form — already done. Not on the board.
- Cameron briefed. Observing Wednesday, no call materials needed from us.
- Prospect shortlist (~28 sites) ready. Ron picks F3, F4, F5, F6 at the start of each respective session.

---

## The board — everything getting done by Wednesday noon

### Flagships (Stream 1)
- **T&F v07 rebuild on v0.7.2** — same prospect, fresh generation, new Vercel project (e.g. `tandf-electric-v072`). Fixes OG color + logo-as-type + any featured-image duplication in one shot. Doubles as v0.7.2 validation.
- **F3, F4, F5, F6** — four new prospect builds from the shortlist. Target ~25 min build + quick review each.

### GRM website
- **The Storefront as a dedicated `/storefront` page** on getrootedmedia.com. Content largely exists in the homepage section; this is restructure + expand.
- **GEO story section** — synthesize the Cowork research doc on service industries + GEO into a narrative piece answering "why this matters for the owner." Positioned so the preview-site-plus-GEO-readiness pitch lands without needing verbal setup on the call.

### Sales ops
- Stop old magazine call automation in HubSpot (pause, not delete).
- Build web services pipeline in HubSpot with Elevate and Launch stages.

### Prospecting ops
- Dedicated session to build a clean round of prompts for Cursor / Manus / Cowork targeting service-industry categories that need GEO readiness + updated web presence. **Flexible slot: Monday evening OR late Tuesday.** Ron picks based on energy.

### Housekeeping (non-blocking, slotted where it fits)
- Rotate Google Places + Unsplash API keys. Update `~/grm-sites-prospects/.env`.
- File updated symptom comment on 21st-dev/magic-mcp #49.
- Add LESSONS.md entry: Places API legacy endpoint INTEGRATION lesson.
- Delete dormant `grm-website` Vercel orphan project.

### NOT on the board (correctly scoped out)
- Service agreement PDFs — done.
- Pricing one-pager — done.
- Cameron call materials — Cameron observes only Wednesday.
- Flagship snapshots repo — deferred to post-launch week.
- Skill doc drift (SKILL.md references to `scripts/mobile_render_check.py`) — cosmetic, not operational. Skip.
- Phase 6 integration of site-review into the skill — observation-only for now, full integration later.
- v1.1 site-review patches — logged, not blocking.

---

## Day-by-day sequencing

### MONDAY (today) — remaining

**Block 1 (now → ~1:30 PM): Walk.**
Already on the plan. Non-negotiable.

**Block 2 (~1:30 PM – 3:00 PM): T&F v07 rebuild = v0.7.2 validation.**
The load-bearing block of the whole two-day plan. If v0.7.2 produces a clean rebuild, the four-site Tuesday sprint is on. If it surfaces a v0.7.3 rework, Tuesday morning becomes rework first, then builds with whatever count fits.

Opener: *"Monday afternoon — T&F v07 rebuild on v0.7.2. Deploy target is a new Vercel project (e.g. `tandf-electric-v072`). This is the F2 validation run."*

Sequence:
1. Run `/prospect-site` against `https://www.tandfelectric.com/` deploying to new project.
2. After deploy, run `site-review` against the new URL as observation pass.
3. Verify the three v0.7.2 rules fired correctly:
   - Logo tiered capture grabbed the real logo (or fired the soft warning).
   - OG thumbnail renders in brand red, not sky blue.
   - Featured service cards on Home vs. Services show different images.
4. Compare against Friday's v07 build — any new gaps surfaced go into the v0.7.3 candidate list, not a same-day patch.

**Block 3 (~3:30 PM – 5:00 PM): HubSpot stop + API key rotation + small housekeeping.**
Low-creative cleanup. Good fit for post-build energy.

- Pause old magazine call automation in HubSpot (do not delete; preserve history).
- Rotate Google Places API key. Update `~/grm-sites-prospects/.env`. Confirm Phase 0 still passes.
- Rotate Unsplash API key. Same update path.
- Post updated symptom comment on 21st-dev/magic-mcp #49.
- Add LESSONS.md entry for Places API legacy endpoint.
- Delete dormant `grm-website` Vercel orphan project via Vercel dashboard.

**Block 4 (evening, optional): Prospecting prompts session OR rest.**
Ron's call based on energy. If energy is there, this is the natural tonight slot for the prompts work. If not, it slides to Tuesday evening with no cost.

---

### TUESDAY — full day

**Block 1 (~9:00 AM – 11:30 AM): F3 + F4 builds.**
If v0.7.2 validated clean Monday, these are pure volume. Back-to-back prospect runs with site-review observation on each. No skill edits mid-sprint — real-world observations log to a v0.7.3 candidate list, addressed only after all four builds are in.

Opener for each: *"Flagship [N] — prospect is [name] at [url]."*

**Block 2 (~12:30 PM – 3:00 PM): GRM website — Storefront page + GEO story.**
Single focused session, two deliverables on getrootedmedia.com:

- **Dedicated `/storefront` page.** Restructure + expand the existing homepage section content. Own page, own URL, linkable as a sales asset.
- **GEO story section.** Pull from the Cowork research doc. Focus: owner-centric "why this matters for your business" narrative, not "here's what GEO is." Lives on the Storefront page or the homepage — decided at session open based on flow.

**Block 3 (~3:30 PM – 5:30 PM): F5 + F6 builds.**
Two more prospect runs, same pattern as morning block.

**Block 4 (evening): HubSpot pipeline build + prospecting session (if not done Monday).**
- HubSpot web services pipeline — create stages aligned to Elevate and Launch tiers. Deal properties (tier, setup fee, monthly, buyout). Any basic automations (stage-change notifications, etc.).
- Prospecting prompts session if Monday evening got skipped. Otherwise just pipeline and call it a night.

---

### WEDNESDAY AM → LUNCH KICKOFF

**Block 1 (~9:00 AM – 11:00 AM): Final polish + slippage recovery.**
Whatever slid from Monday or Tuesday lands here. If nothing slid, use the block for:
- Brain file update (GRM_BRAIN.md) reflecting Wednesday state.
- Any final v0.7.3 rules decided from Tuesday observations.
- Cameron's preview URL pack — simple list of F3/F4/F5/F6 URLs + the T&F v072 rebuild, ready to reference while he observes.

**Block 2 (~11:00 AM – 12:00 PM): Pre-lunch ready check.**
- All flagship URLs loading correctly (run site-review against each as final check).
- HubSpot pipeline populated with the prospects from the shortlist.
- Storefront and GEO story sections live on getrootedmedia.com.
- Magazine automation confirmed paused.

**~12:00 PM: Lunch.**

**~1:30 PM: Sales kickoff.** Ron dials, Cameron observes.

---

## Honest risks

**Risk 1: T&F v07 rebuild surfaces a v0.7.3 rework.**
Mitigation: Tuesday morning becomes rework + a reduced build count (maybe F3 + F4 only, F5/F6 slip). Kickoff still viable with 3 new flagships instead of 4.

**Risk 2: Cowork GEO research doesn't synthesize cleanly into the GRM page.**
Mitigation: Ship a shorter version Tuesday and iterate post-kickoff. The page existing matters more than the page being perfect.

**Risk 3: HubSpot pipeline build takes longer than budgeted.**
Mitigation: Ship stages + deal properties Tuesday evening, defer automations to post-kickoff. Pipeline just needs to be there for Wednesday; polish comes later.

**Risk 4: Energy depletion from sprint pace.**
Mitigation: Monday walk is non-negotiable. Tuesday evening prospecting session is optional — skip it if needed and slot it post-kickoff.

---

## Session openers

- **Monday Block 2:** "Monday afternoon — T&F v07 rebuild on v0.7.2 as F2 validation. Deploy to new Vercel project."
- **Monday Block 3:** "Monday cleanup — HubSpot stop, API key rotation, housekeeping punch list."
- **Tuesday Block 1 (per build):** "Flagship [N] — prospect is [name] at [url]."
- **Tuesday Block 2:** "GRM website session — Storefront page + GEO story."
- **Tuesday Block 4:** "HubSpot pipeline build." (+ prospecting session if slotted here)
- **Prospecting session (whenever it lands):** "Prospecting prompts session — building the Cursor/Manus/Cowork prompt pack."
- **Wednesday Block 1:** "Wednesday polish + brain update. What slid from Tuesday, what still needs to land."

---

## Close-out protocol for THIS plan

1. Save this file to `~/grm-automations/docs/handoffs/TWO_DAY_SALES_KICKOFF_PLAN_2026-04-13.md`.
2. Upload the same file to the Google Drive handoffs folder.
3. Update `GRM_BRAIN.md` with a short block covering:
   - Stream 2 closed, commit `f56b7cc`.
   - `grm-browser` engine + `site-review` mission live, observation-only.
   - T&F v07 OG color bug identified (144° off), will be fixed by Monday afternoon rebuild.
   - v0.7.2 validation plan = T&F v07 rebuild.
4. Commit plan + brain update with a single message: `"Stream 2 close + two-day sales kickoff plan"`.
5. Push.

---

## Punch list carried forward (post-kickoff)

- v1.1 site-review patches (bg-image duplicate blindness, Tier-2 tightening).
- Flagship snapshots repo setup at `~/grm-automations/flagship-snapshots/`.
- Phase 6 integration of site-review into the prospect-site skill (currently standalone).
- SKILL.md reference cleanup (Phase 6 still references phantom `scripts/mobile_render_check.py`).
- Any v0.7.3 rules captured during the Tuesday builds.
- Cowork `prospect-audit` mission (built on grm-browser engine, deferred).
- HubSpot pipeline automations beyond basic stages.

---

*"Fifty years. Two Tuccis. One phone number."* — Friday's validation that the skill writes voice, not copy. Wednesday's job is to prove that voice converts.

# Tuesday Night Handoff — April 7, 2026

## Sales Pushed to Thursday, Wednesday is Execution Day

Read this first. Read this document top to bottom Wednesday morning before doing anything else. It captures what shipped Tuesday, the call to push first dial from Wednesday to Thursday, the exact Wednesday work plan, and the locked decisions that came out of today.

If anything in this document conflicts with the GRM Brain, the Monday Night Handoff, or anything in the project files, this document wins until the brain is updated Wednesday night.

## What shipped Tuesday

Real progress today even though the day did not go in the order originally planned.

- Bank of America business checking account opened for Get Rooted Media LLC. Routing and account numbers in hand.
- Stripe account active and ready to receive payments, EIN 41-4651972 attached.
- 21st.dev Magic MCP confirmed working in the Claude Code terminal session. The logo_search test returned a real structured response, end-to-end pipeline verified.
- SKILL.md patched to v0.5. Phase 3 rewritten with Google Places API as primary photo source plus vision-based curation, frontmatter rewritten to reflect actual skill behavior, version bumped from v0.1, GOOGLE_PLACES_API_KEY check added to prerequisites, conflicting Common Pitfall 4 deleted to match Hard Rule 4, all em dash voice violations cleaned up.
- GOOGLE_PLACES_API_KEY normalized in ~/grm-sites-prospects/.env file. Loads cleanly via source command, verified at 39 characters.
- Cursor round 2 prospect hunt completed. 20 Marion County prospects with substance evidence and presentation gap signals. Strongest leads: Iron Shield Heating & Air, VOLTHOM Electric, Ocala Roofing Inc.
- Flagship 2 retargeted from Ocala Air Conditioning to Central Florida Heating & Air based on Cursor round 1 certified evidence. Better data, stronger pitch shape.
- The Storefront one-pager designed in Canva via Manus, version 4 final. Editorial typography, no anchor image, GRM brand colors, Plant Street voice, locked phone number (352) 598-7289.
- The Storefront Tier 2 Service Agreement drafted as a 2-page Word doc. GRM logo branded, all 10 sections, $500 setup, $150 monthly, 90-day minimum, IP indemnification, liability cap at fees paid in prior 90 days. Plain English throughout.

## What did not ship Tuesday

The Tuesday plan called for flagships 2 and 3 plus all sales infrastructure plus mobile review plus first dial Wednesday morning. Most of that did not happen. The afternoon was eaten by skill patching, the prospect list iteration, and the back and forth on the one-pager and the agreement. Real work was happening, but not the work the schedule demanded.

- Stripe payment links creation and testing ($500 setup link, $150 monthly recurring link)
- Flagship 2 build: Central Florida Heating & Air
- Flagship 3 build: Iron Shield Heating & Air (recommended) or alternative
- HubSpot web services pipeline setup with custom properties (preview_url, site_quality_score, call_status)
- HubSpot call queue setup
- Old magazine call automation paused in HubSpot
- Manual Google Maps verification on the 2-3 prospects from Cursor round 2 with "Maps verification pending" notes
- Mobile review of all flagships and all sales materials

## The call: sales pushed to Thursday

Wednesday is no longer first dial day. Wednesday is execution day. First dial moves to Thursday at 7:15 AM.

The honest reasoning: walking into Wednesday at 7:15 AM with one flagship, no payment links, no signed agreements ready, and no HubSpot pipeline is a recipe for a bad first day. Better to take 24 hours, ship everything cleanly, and start dials Thursday with three flagships in the phone, full closing infrastructure ready, and a good night of sleep.

Thursday with three flagships and a clean closing kit beats Wednesday with one flagship and a half-built backend.

Nothing on the calendar after Thursday changes. The weekly target stays the same. Just a 24-hour shift on the start line.

## Wednesday work plan

In priority order. The first three are quick wins to lock the closing infrastructure. Then flagships through the afternoon and evening. Sleep early. Do not break this order without a real reason.

### First 10 minutes: verification checks (8:00 to 8:10)

Before touching any of the day's real work, run these four fast checks to confirm the foundation is intact. All four together take 10 minutes. If any of them fail, stop and fix before continuing.

- **Plan B reference library exists.** Run in terminal: `ls ~/grm-sites-prospects/plan-b-reference/` and confirm the directory exists and contains component reference files. If it is empty or missing, the Hard Rule 4 fallback is broken. Fix before building any flagships: populate the directory or rewrite the fallback plan in the skill file.
- **getrootedmedia.com/web loads.** Open getrootedmedia.com/web on your phone. The one-pager footer points prospects to this URL. If it returns a 404 or misroutes, either create the page or update the one-pager footer to point to getrootedmedia.com (the root homepage where The Storefront section already lives).
- **Flagship 1 is still live.** Open tandf-electric.vercel.app on your phone. Confirm the T&F site renders correctly, hero is intact, testimonials load. This is the URL Thursday's first dial will show prospects. No surprises on Thursday morning.
- **HubSpot login and state.** Log into HubSpot. Confirm you can access contacts, deals, and automation settings. Confirm the old magazine sequences are visible (you will pause them next). If HubSpot is locked out or behaving unexpectedly, that is the first thing to solve today.

### Morning (8:10 to 11:00)

HubSpot infrastructure while the brain is fresh.

- **Pause old magazine call automation.** In HubSpot, pause whatever sequences are still firing for the magazine business so they do not contaminate the web services queue. Do not delete, just pause.
- **HubSpot web services pipeline.** Build the pipeline with stages (Lead, Contacted, Preview Sent, Verbal Yes, Agreement Sent, Closed-Won, Closed-Lost). Add three custom properties: preview_url, site_quality_score, call_status. Split call queues per the existing dial strategy.
- **Test the pipeline with a fake lead.** Create a test contact, drag them through every stage end to end, confirm nothing breaks or stalls. Delete the test contact when done.

### Late morning to lunch (11:00 to 12:30)

- **Manual Maps verification.** Open Google Maps on a phone or browser and verify the 2-3 strongest "Maps verification pending" prospects from the Cursor round 2 list. Iron Shield first, then Ocala Roofing, then VOLTHOM. Confirm review count, rating, and most recent review date. 5 minutes per prospect.
- **Lunch and decompression.** Flagship building in the afternoon is the highest-judgment work of the day. Eat, walk, reset.

### Afternoon (1:30 to 5:30)

Flagship building. Fresh afternoon brain on the highest-judgment work of the day.

- **Run the Magic MCP verification protocol first.** Before kicking off flagship 2, run the 3-step MCP check below in the terminal. 5 minutes. Do not skip. See the "Magic MCP verification protocol" section after the Wednesday plan for the full procedure.
- **Flagship 2 build: Central Florida Heating & Air.** Build this one in the Claude Code terminal session (not the VS Code extension). Run the v0.5 skill against centralfloridaairinc.com. The skill now has Google Places API integration in Phase 3 and Magic MCP was confirmed working Tuesday night, so this is the first flagship to test the full pipeline. Target 2 to 3 hours including all phases. If anything stalls, ship what is built and move on.
- **Mobile review of flagship 2.** Open the Vercel preview URL on a phone. Walk through every section. Note any gaps for tomorrow morning, do not fix them tonight.

### Evening (6:00 to 8:30)

- **Flagship 3 build: Iron Shield Heating & Air.** Also built in the Claude Code terminal session. Run the v0.5 skill against ironshieldheatingandair.com. Three named owners (Victor Oquendo, William Stiles, Phillip Wisenbaker), 371 reviews, embedded Google reviews widget showing April 2026 dates. Strongest evidence on the entire prospect list. Target 2 to 3 hours. If Magic MCP was green for flagship 2 earlier, you can skip the re-check before this build unless something feels off.
- **Mobile review of flagship 3.** Same drill as flagship 2.

### Late evening: Stripe (8:30 to 9:00)

Stripe is deliberately the last work item of the day. The morning goes to HubSpot and verification. The afternoon and evening go to flagships. Stripe is quick and easy to set up and does not need a fresh brain, so it lands at the end while the flagships are the priority.

- **Create two Stripe payment links.** $500 one-time for the setup fee, $150 recurring monthly for The Storefront subscription. Test each one with a $1 charge to your own card to verify they work end to end, then refund. Save the links to a phone note for instant copy paste during Thursday calls.

### Wednesday close of day (9:00 to 10:00)

Final assembly before sleep.

- Three live Vercel URLs in your phone (T&F, Central Florida, Iron Shield) ready to text or share
- Final mobile walkthrough of all three flagship URLs one last time before sleep
- Stripe payment links saved in a phone note
- Service agreement Word doc saved to Desktop and to Drive
- The Storefront one-pager PDF path confirmed at ~/Desktop/Storefront/one-pager/v4 and ready to text or email
- HubSpot pipeline tested end to end and verified clean
- Alarm set for Thursday 6:30 AM
- Sleep

## Magic MCP verification protocol

Run this protocol in the terminal before kicking off any flagship build. Every time. No exceptions. Prior sessions lost hours rediscovering that Magic MCP status cannot be trusted from memory or from a single "claude mcp list" check. The server can show green and still have tools that do not load in session. Run the full 3-step check and you know for sure in 5 minutes.

### Step 1: Server registration check

In a regular Mac terminal, run:

```
claude mcp list
```

You should see a line like "magic: /usr/local/bin/npx -y @21st-dev/magic@latest - Connected" with a green checkmark. If the line is missing or shows red, the server is not registered and Plan A is broken. Skip to the troubleshooting section below.

### Step 2: In-session tool visibility check

The tricky part. A green server can still fail to load tools into a live session. Start an interactive Claude Code session:

```
claude
```

Accept the workspace trust prompt. Once you see the Claude Code prompt, paste this exactly:

> List every tool available to you right now whose name contains "magic" or starts with "mcp__". Just list the names, nothing else.

You should see at least these four magic tools in the output:

- mcp__magic__21st_magic_component_builder
- mcp__magic__21st_magic_component_inspiration
- mcp__magic__21st_magic_component_refiner
- mcp__magic__logo_search

If the four magic tools are missing, the server is registered but tools are not loading in session. This is the exact failure pattern we hit Friday night. Skip to the troubleshooting section below.

### Step 3: Live tool ping

Listing tools is not the same as calling tools. Prove end-to-end by asking for a real tool call. In the same session, paste:

> Call mcp__magic__logo_search with a search for "nike" and show me the raw response.

Claude Code will ask permission to call the tool. Approve once (do not grant blanket permission). The tool should return a structured JSON response. An empty icons array for a non-brand search is fine. What matters is that a real structured response comes back without error or hang.

If the ping returns real data, Plan A is fully green. Exit the session with /exit and proceed to the flagship build in a new terminal Claude Code session.

If the ping errors out, hangs, or returns nothing, MCP is broken even though the tools were listed. Skip to the troubleshooting section below.

### Troubleshooting when the check fails

The 30-minute decision tree. Do not spend longer than this on troubleshooting during a build day. If it is not fixed in 30 minutes, fall back to Plan B and build flagships with the reference library per Hard Rule 4.

- **First check: config file sanity.** Run `cat ~/.claude.json` and verify the magic entry exists with the right API key and the right command path (/usr/local/bin/npx absolute path, not bare "npx"). The config may have drifted.
- **Second check: source the env file.** Run `source ~/grm-sites-prospects/.env` and confirm `echo $GOOGLE_PLACES_API_KEY` returns the 39-character key. Some shell sessions lose env vars between terminal restarts.
- **Third check: upstream bug investigation.** Web search the GitHub issues for the 21st-dev/magic-mcp repo at github.com/21st-dev/magic-mcp/issues. Look for recent bug reports that match the exact symptom you are seeing. Two adjacent-symptom examples worth reading for context: Issue 23 reported "No tools available" in Cursor, and Issue 21 reported connection failures in Cline with VS Code. Those are different environments than the Claude Code CLI but similar failure modes, and the discussion threads sometimes point to real config fixes. If a recent issue matches your exact environment and symptom, the fix is likely upstream and waiting or working around is the right move.
- **Fourth check: restart the Claude Code CLI.** Close any running "claude" sessions, clear the terminal, start a fresh session. Sometimes session cache is the culprit.
- **Fifth check: reinstall the magic package.** Last resort. Run `npx -y @21st-dev/magic@latest` directly in the terminal to force a fresh install. Then restart and re-run the verification protocol from step 1.

### Fallback: Plan B

If troubleshooting does not resolve Magic MCP in 30 minutes, stop troubleshooting and fall back to Plan B. The skill file Hard Rule 4 explicitly permits this: when Magic MCP is unavailable, build with the reference library at ~/grm-sites-prospects/plan-b-reference/ rather than hand-rolling Tailwind from scratch. T&F Electric (flagship 1) was built on Plan B and closed successfully. Plan B is a production path, not a workaround.

Do not lose a day debugging Magic MCP when Plan B ships clean flagships.

### Where to build (settled)

All flagship builds happen in the Claude Code terminal session, not the VS Code extension. The terminal is where Magic MCP actually loads and works. This was proven Tuesday via the verification protocol above. The VS Code extension is fine for everyday code editing but not for skill execution or MCP-dependent work.

To start a terminal flagship build session: open a regular Mac terminal, run `claude`, accept the workspace trust prompt, run the MCP verification protocol, then trigger the skill with `/prospect-site "Business Name" https://their-site.com`.

## Thursday morning first-dial pre-flight

Run this checklist Thursday morning between 6:30 and 7:15 before the first dial.

- Phone fully charged
- Coffee made, water on the desk
- HubSpot open on phone and computer with web services pipeline loaded
- Three flagship URLs open in browser tabs and tested loading on phone
- Pricing one-pager open in a tab, ready to text mid-call
- Service agreement template open and ready to fill in client name, address, date
- Stripe payment links pasted in a phone note for instant access
- Quiet workspace
- First dial 7:15 AM sharp

## Locked decisions reference

Everything that got decided today. If a future Claude session ever questions any of these, this is the source of truth.

### Pricing

- Tier 2 setup fee: $500 one-time, due in full upon signing before any build work
- Tier 2 monthly fee: $150 per month, first payment when site goes live
- Term: 90-day minimum starting from the live date, then month-to-month with 30 days written notice
- Buyout option: Removed. Not on the one-pager, not in the agreement. If a prospect specifically asks, quote $1,500 on the call as a special request.
- Tier 1: On hold. Cannot define a $1,000 product until we have built a few flagships with Magic MCP and seen what the premium quality jump actually looks like.

### Product branding

- Product name: The Storefront
- Phone: (352) 598-7289
- Calendar booking: cal.com/ron-kolb-cdlgsw/30min
- Tagline: We build it. We host it. We update it. You answer the phone.

### Flagship roadmap

- Flagship 1: T&F Electric. Live at tandf-electric.vercel.app. Locked, used in sales calls, do not touch.
- Flagship 2: Central Florida Heating & Air (centralfloridaairinc.com). Build Wednesday afternoon. Replaces the original Ocala AC plan based on better certified evidence from Cursor round 1.
- Flagship 3: Iron Shield Heating & Air (ironshieldheatingandair.com). Build Wednesday evening. Strongest evidence on the entire round 2 list, three named owners, embedded April 2026 reviews on site.
- Flagship 4 (stretch goal, optional): VOLTHOM Electric (volthomelectric.com). Only if Wednesday flow allows. Otherwise build Thursday morning before dials or skip.

### Service agreement specifics

- Liability cap: Maximum liability limited to total fees paid by Client in the 90 days prior to the claim
- IP indemnification: Client warrants legal right to all content provided and indemnifies GRM against third-party IP claims
- Termination export fee: $300 one-time for Client to receive site files on termination
- Setup fee non-refundable: Yes, under any circumstances
- Governing law: Florida, Marion County courts

### Skill file state

- Version: v0.5
- Location on Mac: ~/.claude/skills/prospect-site/SKILL.md
- Phase 3: Google Places primary, Instagram secondary, prospect site tertiary, vision-based curation, auto hero pick with top 3 alternates saved
- Magic MCP status: Working in Claude Code terminal sessions, confirmed via logo_search test
- Plan B reference library: Available as fallback if Magic MCP fails mid-build (per Hard Rule 4)

## Lessons from today (capture for the brain)

Things that cost time today that should not cost time again. Worth adding to the GRM Brain Wednesday night.

- Magic MCP works in the terminal Claude Code, not the VS Code extension. Tuesday morning was lost to checking the wrong place. The CLI is the canonical way for Ron to use Claude Code with MCP servers. Future skill work and MCP testing happens in the terminal, not in the VS Code panel.
- The skill file workflow is GitHub plus Word doc on Desktop. Do not invent new ways to ferry skill files through chat (no base64 paste, no Cursor save-as workflows). Claude generates a Word doc, Ron saves it to Desktop, Claude Code reads it from Desktop and writes it to the right path. That is the workflow. Use it every time.
- Strict prospect filters kill yield. Cursor round 1 returned 1 prospect because the filters were too tight. Round 2 with loosened filters returned 20. The right move is loose filters with a manual verification step, not strict filters with zero verification needed.
- Do not iterate on visual design before content is approved. Tonight's service agreement could have shipped 90 minutes earlier if content approval had come before formatting iteration. Always lock content first, then design.
- Two-page contracts beat five-page contracts at this price point. A $500 service does not need a 5-page legal document. Plain English, fewer sections, tighter formatting, signature blocks inline. Same legal protection in half the space.
- Use the right tool for the job. Manus does Canva design well because it has the brand kit. Claude does Word docs well because it can generate them programmatically with logos embedded. Service agreements stay in Word because they get filled in per client. Marketing pieces go to Manus because they need brand-correct visual polish.

## Recoverable files inventory

All Tuesday outputs that should be saved or that exist in the chat for recovery if needed.

- SKILL.md v0.5: ~/.claude/skills/prospect-site/SKILL.md on Mac, also on chat outputs as SKILL_v0.5_PATCHED.docx
- The Storefront one-pager v4b: Saved on Ron's Mac at ~/Desktop/Storefront/one-pager/v4 (filename storefront_onepager_v4b_canva.pdf). Also in Canva edit history.
- Tier 2 service agreement v2 (2-page): The_Storefront_Service_Agreement_Tier_2_v2.docx in chat outputs
- Tier 2 service agreement v1 (5-page backup): The_Storefront_Service_Agreement_Tier_2.docx in chat outputs, backup in case a sophisticated prospect ever asks for the longer version
- Cursor round 2 prospect list: CSV pasted into chat, 20 prospects with substance and presentation gap evidence
- Cursor round 1 prospect list: Earlier in the chat, only 1 fully certified (Central Florida Heating & Air, now flagship 2)
- This handoff document: GRM_Tuesday_Night_Handoff.docx in chat outputs

## Wednesday morning first prompt

Paste this into a fresh Claude session Wednesday morning to kick things off. It loads the right context and gives one focused starting task.

---

Good morning. I read the Tuesday Night Handoff. Sales pushed to Thursday. Wednesday is execution day. The plan is: first 10 minutes of verification checks (Plan B reference library, getrootedmedia.com/web, flagship 1 still live, HubSpot state), then morning HubSpot pipeline work and pause magazine automation, then Maps verification on the round 2 prospects, then flagship 2 in the afternoon (Central Florida Heating and Air), then flagship 3 in the evening (Iron Shield), then Stripe payment links last. Walk me through exactly what to do for the first verification check (Plan B reference library), one step at a time. Do not skip ahead. I will report back after each step.

---

## End of handoff

Tuesday was not the day the original plan called for. It was the day where the foundation got real. Skill is patched and verified working. Closing kit (one-pager, agreement, payment infrastructure ready to be wired up) is locked. Prospect list is cleaned and quality-graded. Phone number is on every customer-facing piece.

Wednesday is heads down execution. Thursday is dials. The 24-hour shift is the right call.

Sleep well.

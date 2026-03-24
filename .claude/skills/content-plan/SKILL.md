---
name: content-plan
description: Generate a full multi-format content strategy plan for Get Rooted Media. Outputs hooks, reel scripts, carousel slides, freebie PDF outline, ManyChat config, and production checklist from a single topic.
argument-hint: [topic] [--account=getrootedmedia|ron_kolb|closing_table|cameron] [--freebie=yes|no] [--keyword=MANYCHAT_KEYWORD] [--collab=yes|no]
---
# Get Rooted Media — Content Plan Skill
## Overview
Generates a complete, execution-ready content plan from a single topic input, tailored for Get Rooted Media's four Instagram accounts and two publications (The Closing Table and The Front Porch). Output is a markdown file with 10 hooks, cell phone reel script, cell-phone-only reel script, carousel slide plan, freebie PDF outline, ManyChat automation config, Instagram collab strategy, and a full production checklist.
## Purpose
- Turn any topic into a ready-to-execute content plan in one command
- Generate 10 hook variations using proven psychological triggers
- Write reel scripts for Cell Phone Reel and Cell Phone Only Reel formats
- Build a carousel slide-by-slide content plan (1080x1350)
- Outline a freebie PDF that delivers real value to the target audience
- Configure ManyChat keyword-triggered DM automation
- Map Instagram collaboration strategy across all four accounts
- Output a production checklist and metrics tracking table
## Brand Context
### Company
- **Name:** Get Rooted Media LLC
- **Location:** Ocala, FL (Marion County)
- **Publications:** The Closing Table (monthly, top-producing real estate agents in Marion and Sumter Counties) and The Front Porch (quarterly, new homeowners)
- **Founder:** Ron Kolb — 30 years of sales experience, former VP of Sales, Certified xChange Guide
- **Sales Director:** Cameron Cowart (Ron's son)
- **Timeline:** Ron resigned from City Lifestyle in early February 2026 and launched Get Rooted Media approximately 4-5 weeks ago. The company is in early launch phase — first issues are being prepared, not yet published. Do not reference months of results or published issues unless confirmed by the user.
### Target Audiences
1. **Primary (The Closing Table):** Top 500 producing real estate agents — 350 in Marion County, 150 in Sumter County (The Villages). These are active, volume-producing agents sourced from Stellar MLS transaction data.
2. **Secondary (The Front Porch):** New homeowners in the Ocala/Marion County area.
3. **Tertiary:** Local business owners who are potential advertisers in both publications.
### Instagram Accounts
| Account | Voice | Role |
|---------|-------|------|
| @getrootedmedia | Brand hub. Professional, community-focused. | Main content home. Publishes all formats. Initiates collabs. |
| @ron__kolb | Personal. Founder story. Direct, authentic, conversational. 30 years of sales wisdom meets new venture energy. | Thought leadership, behind-the-scenes, personal brand reels. |
| @theclosingtableocala | Authority. Data-driven, agent-focused. | Agent-specific content, rankings, market insights, AI-for-agents tips. |
| @cameron_cowart | Young hustle. Learning in public, sales energy. | Day-in-the-life, outreach stories, next-gen perspective. |
### Brand Voice Rules
For all voice and copy standards, read .claude/skills/GRM_VOICE_SKILL.md before writing anything. That file is the only source of truth for voice.
- CTAs are confident and specific, never desperate: "Comment KEYWORD for the free guide" not "Don't miss out!!!"
- Emojis: Sparingly. Max 2 per caption. Never in hook text.
- Hashtags: 8-10 per post. Mix of local (#OcalaRealEstate #MarionCounty #TheVillagesFL) and topical.
## Input Requirements
### Required
1. **Topic** — the subject of the content (e.g., "AI prompts for listing descriptions", "what top producers do differently on social", "building a company with AI as co-founder")
### Optional
2. `--account=ACCOUNT` — primary posting account (default: getrootedmedia). Options: getrootedmedia, ron_kolb, closing_table, cameron
3. `--freebie=yes|no` — whether to include a PDF freebie section (default: yes)
4. `--keyword=WORD` — the ManyChat trigger keyword (default: derived from topic, ALL CAPS, one word)
5. `--collab=yes|no` — whether to generate Instagram collab strategy across accounts (default: yes)
6. `--audience=agents|homeowners|business` — target audience (default: agents)
## Execution Steps
### Step 1: Research Context
Before writing anything, gather:
1. Check for any existing content plans in the project folder to avoid topic duplication
2. Identify what angle on the topic would be most valuable to the specified `--audience`
3. If `--audience=agents`: frame everything through the lens of "how does this help a producing agent in Marion or Sumter County win more business?"
4. If `--audience=homeowners`: frame through "what does a new homeowner in Ocala need to know?"
5. If `--audience=business`: frame through "what does a local business owner need to understand about reaching customers?"
6. Identify 1-2 trending angles or timely hooks related to the topic
### Step 2: Generate the Plan
Generate a markdown file with ALL of the following sections:
---
### Section 1: Topic Summary
| Field | Value |
|-------|-------|
| Topic | [topic] |
| Primary Account | [--account value] |
| Target Audience | [--audience value] |
| ManyChat Keyword | [--keyword value] |
| Freebie Included | [yes/no] |
| Collab Post | [yes/no] |
| Date Generated | [current date] |
---
### Section 2: Hooks (10 Options)
Generate 10 hooks using these 10 types (one of each):
| # | Hook Type | Description |
|---|-----------|-------------|
| 1 | Trend Ride | Validate awareness of a current trend relevant to Ocala/FL real estate or the topic |
| 2 | Simplicity Promise | Remove the biggest barrier + time promise ("in 10 minutes", "with one tool") |
| 3 | Curiosity Gap | Make them feel like they are missing something their competitors know |
| 4 | Bold Claim | Lead with the outcome, promise to show how |
| 5 | Direct Question | Call out the exact audience segment + empathize with their pain |
| 6 | Contrarian | Break an assumption the audience holds (e.g., "You don't need a marketing team") |
| 7 | FOMO / Urgency | Social proof + helpful rescue ("Top agents in Marion County are already doing this") |
| 8 | Before-After | Relatable pain + clear upgrade path |
| 9 | Demo Tease | Promise a walkthrough or demo, create anticipation |
| 10 | Authority | Credibility-first — Ron's 30 years of sales, data from The Closing Table, local market knowledge |
For each hook, include:
- The hook line (spoken or as cover text)
- Type label
- Why it works (1 sentence)
- Best format: Cell Phone Reel, Cell Phone Only Reel, or Carousel
- Carousel cover version (adapted as a visual headline)
- Which account should post it (based on voice fit)
---
### Section 3: Format 1 — Cell Phone Reel (30-45 seconds)
This is the primary video format. Raw, one-take, shot on Ron's or Cameron's iPhone. Edited with captions in CapCut. Feels native to the platform.
Include:
- Specs table:
| Spec | Value |
|------|-------|
| Aspect Ratio | 9:16 |
| Duration | 30-45 seconds |
| Shot On | iPhone, handheld or propped |
| Editing | CapCut — auto-captions, trim only |
| Tone | Conversational, direct, like talking to a friend at a networking event |
| Music | None or subtle trending audio |
- Shooting instructions table:
| Element | Instruction |
|---------|-------------|
| Camera | iPhone front camera, eye level |
| Framing | Head and shoulders, slightly off-center |
| Lighting | Natural light facing you, or ring light |
| Audio | iPhone mic (quiet room) or lapel mic |
| Takes | Shoot 2-3, pick the most natural one |
| Location | Office, car, walking in downtown Ocala, or at a local spot |
- Framework: Hook (first 3 seconds) > Problem/Context > Solution/Tip > Proof or Example > CTA (comment keyword)
- Full one-take conversational script (~120 words). Must sound like speech, NOT copy. Use contractions, pauses, natural transitions.
- On-screen text overlays (max 3): opening hook text, key moment callout, CTA with keyword
- Instagram caption (ready to paste, with 8-10 hashtags, no placeholders)
- Which account posts this + collab tags
---
### Section 4: Format 2 — Cell Phone Only Reel (15-30 seconds)
Shortest format. Quick tip, one idea, punchy. Great for Cameron's account or for repurposing a single point from a longer piece.
Include:
- Specs: 9:16, 15-30 seconds, iPhone, no editing except CapCut captions
- Script (~60-80 words). One idea. Hook > Point > CTA. Done.
- On-screen text: Hook text + CTA only
- Instagram caption (shorter, 5-8 hashtags)
- Which account posts this
---
### Section 5: Format 3 — Carousel (5-10 slides)
Carousels are the highest-save-rate format. Each slide must earn its spot.
Include:
- Specs: 1080x1350px, slide count, clean/bold style
- Slide-by-slide content. Every slide must include:
  - Slide number
  - Headline (large, bold)
  - Body text or checklist items (specific, actionable — never vague)
  - Visual description (background color, layout notes)
  - Purpose (why this slide exists in the sequence)
- Structure:
  1. Cover slide — hook headline (from Section 2). Bold text, branded colors.
  2. Context slide — the "what" and "why" (1 slide)
  3. Instruction/value slides — the core content (checklist format, 3-5 items per slide, each item is a direct action: "Open Claude.ai" not "Use an AI tool")
  4. Proof/result slide — outcome stat, testimonial, or before/after
  5. CTA slide — "Comment [KEYWORD] and I'll send you the free [freebie name]" + follow prompt
- Instagram caption (ready to paste, 8-10 hashtags)
- Which account posts this + collab tags
- Canva template notes (if applicable)
---
### Section 6: Instagram Collaboration Strategy (if --collab=yes)
Map how this content gets distributed across all four accounts:
| Post | Primary Account | Collab With | Collab Rationale |
|------|----------------|-------------|------------------|
| Cell Phone Reel | [account] | [account(s)] | [why this collab makes sense] |
| Cell Phone Only | [account] | [account(s) or none] | [rationale] |
| Carousel | [account] | [account(s)] | [rationale] |
Include:
- Posting sequence (which goes first, stagger timing)
- Cross-promotion notes (e.g., "Ron posts reel Tuesday, Cameron shares to story Wednesday, Closing Table reposts carousel Thursday")
- Story reshare strategy for each account
---
### Section 7: Freebie PDF Outline (if --freebie=yes)
The freebie is the PDF guide delivered via ManyChat when someone comments the keyword.
Include:
- **Title** of the PDF (compelling, specific — "The Ocala Agent's AI Listing Description Toolkit" not "AI Guide")
- **File details:** target page count, format (designed PDF or clean markdown-to-PDF)
- **Table of Contents** — what each section covers:
  - Section 1: Brief intro (who this is for, what they'll get)
  - Sections 2-N: Step-by-step content covering the topic
  - Final section: About Get Rooted Media + The Closing Table CTA ("Want to be featured? Here's how")
- **Co-branding note:** If audience is agents, include a note that agents can request a co-branded version with their headshot/logo (this becomes a relationship-building touchpoint)
- **Hosting:** Google Drive shareable link (primary) or direct ManyChat attachment if under 10MB
Skip this section entirely if `--freebie=no`.
---
### Section 8: ManyChat Automation Config (if --freebie=yes)
Include:
- Flow overview (text description of the automation sequence)
- Workflow name: "{KEYWORD} DM"
- JSON config:
```json
{
  "name": "{KEYWORD} DM",
  "keyword": "{KEYWORD}",
  "commentReplies": [
    "Sending it your way right now! Check your DMs 📩",
    "It's headed to your inbox! Check DMs 🙌",
    "Just sent it! Let me know what you think 👊"
  ],
  "openingDM": "Hey! Thanks for grabbing the [FREEBIE NAME]. I put this together specifically for [AUDIENCE DESCRIPTION] in [Marion County / Sumter County / Ocala]. Here it is:",
  "buttonLabel": "Get the free guide",
  "followGateText": "Quick thing — follow @getrootedmedia so I can send this to you!",
  "deliveryDM": "Here's your copy of [FREEBIE NAME]. Hope it helps! If you want to see more like this, keep an eye on @getrootedmedia and @theclosingtableocala.",
  "linkLabel": "[FREEBIE NAME]",
  "linkUrl": "[GOOGLE_DRIVE_LINK]",
  "followUpDM": "Hey! Just checking — did you get a chance to look at [FREEBIE NAME]? If you found it useful, I'd love to hear what you thought. We publish The Closing Table every month featuring the top-producing agents in Marion and Sumter Counties. Would love to connect."
}
```
- Subscriber tag: `{keyword}_lead`
- Notes: The follow-up DM is the bridge to The Closing Table conversation. This is where cold followers become warm prospects.
Skip if `--freebie=no`.
---
### Section 9: Posting Strategy
| Day | Format | Account | Notes |
|-----|--------|---------|-------|
| Day 1 | Cell Phone Reel | [primary] collab [secondary] | Lead with video. Highest reach. |
| Day 3 | Cell Phone Only Reel | Cameron or Ron personal | Quick hit, different angle on same topic |
| Day 5 | Carousel | @getrootedmedia collab @theclosingtableocala | Highest save rate. Drives keyword comments. |
| Day 2, 4, 6 | Stories | All accounts | Behind-the-scenes, polls, reshares |
Include:
- 8-10 platform-relevant hashtags (mix local + topical):
  - Local: #OcalaRealEstate #MarionCountyFL #TheVillagesFL #OcalaFL #FloridaRealEstate
  - Topical: [3-5 relevant to topic]
- Best time to post: Based on audience (agents are most active early morning 6-8am and lunch 11:30-1pm)
- Accounts to tag (1-2 max, relevant local accounts or featured agents)
---
### Section 10: Content Format Comparison
| Metric | Cell Phone Reel | Cell Phone Only | Carousel |
|--------|----------------|-----------------|----------|
| Effort | Low | Lowest | Medium |
| Expected Reach | Highest | High | Medium |
| Save Rate | Low | Low | Highest |
| Authority Building | Medium | Low | High |
| Best For | Awareness, new followers | Quick engagement, story reshares | Keyword comments, freebie delivery |
| Repurpose To | TikTok, YouTube Shorts | TikTok, Stories | Pinterest, LinkedIn, Email |
---
### Section 11: Repurposing Matrix
| Platform | Source Format | Adaptation Needed |
|----------|-------------|-------------------|
| TikTok | Cell Phone Reel | Re-upload natively, adjust caption |
| YouTube Shorts | Cell Phone Reel | Re-upload, add end screen |
| Facebook (Get Rooted page) | Carousel | Upload as album or PDF carousel |
| LinkedIn (Ron's profile) | Carousel + caption rewrite | Professional tone, longer caption |
| Email newsletter | Freebie PDF + carousel summary | Embed carousel images, link to freebie |
| The Front Porch (if homeowner topic) | Freebie PDF adapted | Print-friendly version for publication |
| The Closing Table (if agent topic) | Key insights from plan | Sidebar feature or digital companion piece |
---
### Section 12: Production Checklist
**Pre-Production**
- [ ] Freebie PDF drafted and designed (or clean markdown converted)
- [ ] Freebie uploaded to Google Drive with shareable link
- [ ] ManyChat automation configured and tested (send test DM to yourself)
- [ ] Carousel slides designed in Canva (use slide-by-slide plan from Section 5)
- [ ] Reel scripts printed or loaded on teleprompter app
- [ ] Shooting location selected
- [ ] Ring light / lapel mic ready (if using)
**Production**
- [ ] Film Cell Phone Reel (2-3 takes)
- [ ] Film Cell Phone Only Reel (2-3 takes)
- [ ] Select best takes
**Post-Production**
- [ ] Edit Cell Phone Reel in CapCut (auto-captions, trim, hook text overlay)
- [ ] Edit Cell Phone Only Reel in CapCut (captions only)
- [ ] Export all at 1080x1920
**Publishing**
- [ ] Day 1: Post Cell Phone Reel with collab invite sent
- [ ] Day 1: Share to all stories
- [ ] Day 3: Post Cell Phone Only Reel
- [ ] Day 5: Post Carousel with collab invite sent
- [ ] Cross-post to TikTok, Facebook, LinkedIn per repurposing matrix
**Post-Launch**
- [ ] Monitor ManyChat DM delivery (check within 1 hour of posting)
- [ ] Respond to comments personally (first 30 minutes critical for algorithm)
- [ ] Track metrics at 24h and 7 days
- [ ] Follow up with high-engagement commenters personally
---
### Section 13: Metrics to Track
| Metric | Where to Find | What It Tells You |
|--------|--------------|-------------------|
| Views (per reel) | IG Insights > Reels | Reach and hook effectiveness |
| Completion Rate | IG Insights > Reels | Script quality — are people watching to the end? |
| Saves | IG Insights > Post | Content value — saves = "I want this later" |
| Shares | IG Insights > Post | Virality potential |
| Keyword Comments | Post comments | Freebie demand and CTA effectiveness |
| DMs Sent (ManyChat) | ManyChat dashboard | Automation working + actual lead capture |
| PDF Link Clicks | Google Drive or Bitly | Are people actually opening the freebie? |
| New Followers | IG Insights > Followers | Content attracting the right audience? |
| Profile Visits | IG Insights > Overview | Curiosity generated |
**Success Benchmarks:**
| Metric | Good | Great | Exceptional |
|--------|------|-------|-------------|
| Reel Views | 500+ | 2,000+ | 10,000+ |
| Completion Rate | 30%+ | 50%+ | 70%+ |
| Saves (carousel) | 20+ | 50+ | 100+ |
| Keyword Comments | 10+ | 30+ | 75+ |
| DMs Delivered | 10+ | 25+ | 50+ |
| New Followers (per post) | 5+ | 20+ | 50+ |
---
## Output
### Save the file
Save to: `content-plans/{topic-slug}-content-plan.md`
### Confirm to user
1. File path of the saved plan
2. Number of hooks generated (should be 10)
3. The ManyChat keyword
4. Number of carousel slides
5. Number of production checklist items
6. Collab strategy summary (which accounts, what sequence)
7. Freebie title and hosting status
## Quality Standards
Every plan MUST meet these standards before saving:
- [ ] All 10 hooks are distinct (no two use the same psychological trigger)
- [ ] Cell Phone Reel script is 100-130 words and sounds like natural speech (contractions, pauses, conversational transitions — NOT marketing copy)
- [ ] Cell Phone Only Reel script is 60-80 words, one idea, punchy
- [ ] Every carousel slide has specific, actionable content (no slide says "Use AI tools" — it says "Open Claude.ai, click New Chat, paste this prompt: [exact prompt]")
- [ ] Freebie outline includes a Closing Table / Get Rooted Media CTA in the final section
- [ ] ManyChat JSON config has all required fields populated with real copy (no placeholders)
- [ ] All Instagram captions are ready to paste — no [INSERT HERE] placeholders
- [ ] Hashtag mix includes at least 3 local Ocala/Marion/Sumter tags
- [ ] Collab strategy maps to at least 2 of the 4 accounts
- [ ] Production checklist covers pre-production through post-launch
- [ ] The follow-up DM naturally bridges to The Closing Table conversation
- [ ] Content is framed for the specified --audience (agents, homeowners, or business owners)
- [ ] Ron's voice comes through: direct, experienced, generous with knowledge, never corporate

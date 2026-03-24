name: editor
description: Research and generate a full editorial content framework for either The Closing Table or The Front Porch. Outputs headlines, article outline, opening paragraph, sidebar ideas, and word count breakdown. Run with /editor closing-table or /editor front-porch.
argument-hint: [publication: closing-table|front-porch] [topic?] [--month=MONTH] [--draft]
---

# Get Rooted Media — Editor Skill

## Overview

Generates a complete editorial content framework for one of Get Rooted Media's two publications. If a topic is provided, it builds the framework around that topic. If no topic is provided, it suggests three timely, audience-relevant options for the current month and waits for selection before proceeding.

## Publications

### The Closing Table
- **Type:** Monthly magazine
- **Audience:** Top-producing real estate agents, lenders, title companies, inspectors, photographers, and real estate service providers in Marion and Sumter Counties, FL
- **Tone:** Industry-insider, celebratory, peer-to-peer. Confident without being corporate. Reads like it was written by someone who has been in the room at the closing table — because it was.
- **Mission:** Celebrate the people who make deals happen. Turn competitors into a community. Give the real estate industry of Marion County a publication that reflects how good they actually are.
- **Content pillars:** Agent spotlights, market trends, industry best practices, behind-the-deal team features, local market data, professional development
- **Print specs:** Monthly, 850–1,000 copies mailed, 12 issues/year
- **Voice anchors:** "No one gets to the closing table alone." / "Behind every deal is a team."

### The Front Porch
- **Type:** Quarterly resource guide
- **Audience:** New homeowners in Marion County within their first 90 days of moving in. Often relocating from out of state. Unfamiliar with local vendors, services, and community. Excited but overwhelmed.
- **Tone:** Warm, practical, trusted neighbor. Not a coupon book. Not junk mail. Reads like advice from the most helpful person you've met since moving here — someone who actually knows the area and wants you to feel at home.
- **Mission:** Answer the question every new resident asks: "Who do you use for _______?" Give new homeowners a trusted guide they keep on the counter.
- **Content pillars:** Home services (HVAC, plumbing, landscaping), healthcare, schools, restaurants and date nights, community discovery, seasonal home tips, local hidden gems
- **Print specs:** Quarterly, 2,500+ copies per issue mailed to new homeowners, 4 issues/year
- **Voice anchors:** "You're home — but you're not rooted yet." / "Your HVAC will run 10 months a year in Florida. Trust us."

---

## Input Requirements

### Required
1. **Publication** — `closing-table` or `front-porch`

### Optional
2. **Topic** — the article subject (e.g., "staging tips for faster sales" or "finding a doctor after you move")
   - If omitted, the skill generates 3 topic suggestions for the current month and pauses for selection
3. `--month=MONTH` — target month for topic suggestions (default: current month)

### Example usage

```
/editor closing-table "how to build referral partnerships with lenders"
/editor front-porch "preparing your home for Florida summer"
/editor closing-table --month=June
/editor front-porch
```

---

## Execution Steps

### Step 1: Load Publication Context

Based on the publication argument, load the correct voice, audience, tone rules, and content pillars from the Publications section above. All output must match that publication's voice exactly — do not blend tones between the two.

### Step 2: Topic Selection (if no topic provided)

If no topic was passed, generate **3 topic suggestions** using these criteria:
- Relevant to the current month or upcoming season
- Directly useful to the target audience
- Not generic — specific to Marion County / Florida context where possible
- One should be evergreen, one seasonal, one trend-driven

Present the three options clearly and **stop**. Wait for the user to select one before proceeding.

### Step 3: Research Context

Before writing anything, gather relevant context:
1. Is there a seasonal angle? (Florida weather, real estate market cycles, local events)
2. What is the audience's likely pain point or question around this topic right now?
3. Are there Marion County or Sumter County specifics that make this more local and relevant?
4. What would a top-producing agent (Closing Table) or a new homeowner (Front Porch) actually need to walk away knowing?

### Step 4: Generate the Content Framework

Produce all five sections below in order.

---

#### Section 1: Headline Options (4 variations)

Generate 4 distinct headline options using different approaches:

| # | Approach | Description |
|---|----------|-------------|
| 1 | Outcome-led | Leads with the result the reader gets |
| 2 | Curiosity / Question | Makes the reader feel like they're missing something |
| 3 | Practical / How-To | Direct, useful, no fluff |
| 4 | Community / Local | Anchors the story to Marion County or the Get Rooted mission |

For each headline include:
- The headline text
- Approach label
- One sentence on why it works for this audience
- Best use (cover story, feature article, sidebar lead, or digital teaser)

---

#### Section 2: Word Count + Section Breakdown

Based on the topic and publication format, define:
- **Total word count target** (Closing Table features: 600–900 words / Front Porch guides: 400–700 words)
- **Section-by-section breakdown:**

| Section | Purpose | Word Count |
|---------|---------|------------|
| Opening | Hook the reader | ~80–120 words |
| [Section name] | [What it covers] | ~[X] words |
| [Section name] | [What it covers] | ~[X] words |
| [Section name] | [What it covers] | ~[X] words |
| Close / CTA | What the reader does next | ~60–80 words |

Adjust section count based on topic complexity. Closing Table articles may include a "By the Numbers" data callout section. Front Porch guides often work best as numbered lists or step-by-step formats.

---

#### Section 3: Article Outline

Full skeleton of the article with:
- All section headers (as they would appear in print)
- 2–4 bullet points under each section showing what goes there
- Any data points, local stats, or expert voices to seek out
- Notes on tone or approach for each section

---

#### Section 4: Opening Paragraph (Draft)

Write a complete, publish-ready opening paragraph that:
- Opens with a scene, a question, or a truth the reader immediately recognizes
- Matches the publication voice exactly (see Publications section)
- Does not start with "I" or a generic statement
- For The Closing Table: sounds like it came from inside the industry
- For The Front Porch: sounds like the most helpful neighbor you've ever had

This is a first draft — good enough to build from, strong enough to show a client.

---

#### Section 5: Sidebar + Callout Ideas

Generate 3 sidebar or callout options the designer can choose from:

| Type | Content |
|------|---------|

| Stat callout | A single compelling number with a one-line label |
| Quick tip box | 3–5 bullets the reader can act on immediately |
| Pull quote | A strong line pulled from the outline (or written as a likely quote) |

For each, include the actual content — not just the label.

---

### Step 5: Save the Framework

Save output to: `content/{publication}/{month}-{topic-slug}-framework.md`

Example: `content/closing-table/june-referral-partnerships-framework.md`

---

## Output Confirmation

After saving, confirm:
1. Publication targeted
2. Topic used
3. Headline count generated
4. File path saved to
5. Suggested next step

---

## Quality Standards

Before saving, verify every item:

- [ ] Headline options are meaningfully distinct — no two use the same structure
- [ ] Opening paragraph does NOT start with "I", "Are you", or a generic statement
- [ ] Voice matches the correct publication — Closing Table sounds like industry, Front Porch sounds like neighbor
- [ ] Word count targets are realistic for print (not blog-length)
- [ ] Sidebar content is written out fully — no placeholders
- [ ] Any Marion County / Florida specifics are accurate (do not invent statistics)
- [ ] Article outline gives enough direction to write from without being over-prescribed
- [ ] Output file is saved before confirming to user

---

## Brand Rules

For all voice and copy standards, read .claude/skills/GRM_VOICE_SKILL.md before writing anything. That file is the only source of truth for voice.

---

## Draft Mode (--draft flag)

When the `--draft` flag is added to any editor command, run the full framework generation first (Steps 1–5), then continue directly into full article draft mode without stopping.

### Example usage

```
/editor closing-table "how top agents build referral networks" --draft
/editor front-porch "Silver Springs State Park" --draft
```

### Draft Execution Steps

#### Step 1: Load the Framework

If a framework file already exists for this topic, load it from:
`content/{publication}/{month}-{topic-slug}-framework.md`

If no framework file exists, generate it first (full Steps 1–5 above), save it, then continue into drafting.

#### Step 2: Write the Full Article

Using the saved framework as the blueprint, write a complete, publish-ready article:

- Follow the section headers and outline exactly as defined in the framework
- Hit the word count targets for each section
- Match the publication voice throughout — do not drift
- Use the Opening Paragraph draft from the framework as the article opening (refine if needed, do not replace entirely)
- Incorporate the stat callout and pull quote from the framework naturally into the body
- Write every section fully — no placeholders, no "[insert stat here]" notes

#### Step 3: Format for Print

Format the final article as it would appear in the magazine:

**Closing Table format:**
- Headline (use the recommended headline from the framework, or ask user to pick)
- Subhead (one line, 10–15 words, expands on the headline)
- Body copy in sections with bold headers
- "By the Numbers" data callout box if included in framework
- Pull quote called out mid-article
- Sidebar content at the end

**Front Porch format:**
- Headline
- Subhead
- Intro paragraph
- Body copy — use numbered lists or step-by-step format where appropriate
- Tip box called out mid-article or at end
- Stat callout embedded naturally
- Warm closing paragraph with CTA

#### Step 4: Save the Draft

Save to: `content/{publication}/{month}-{topic-slug}-draft.md`

Example: `content/closing-table/march-referral-networks-draft.md`

#### Step 5: Confirm to User

1. Publication and topic
2. Final word count
3. Headline used
4. File path saved to
5. Suggested next step (e.g., "Review the draft, make edits, then it's ready for design layout.")

### Draft Quality Standards

- [ ] Article reads like a human wrote it, not an AI
- [ ] Voice is consistent from first word to last — no tonal drift
- [ ] Every section from the framework is represented in the draft
- [ ] Word count is within 10% of target
- [ ] No placeholder text anywhere in the document
- [ ] Pull quote and stat callout are integrated, not bolted on
- [ ] Closing paragraph gives the reader a clear next action
- [ ] Draft file is saved before confirming to user

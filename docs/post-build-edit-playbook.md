# Post-Build Edit Playbook

**Purpose.** The prospect-site skill produces a deployed first draft. Ron's eye is the final filter. This playbook documents the manual touch-up workflow that runs between "skill says done" and "ready to send to a prospect." Follow this for every prospect build until further notice.

**Author:** Ron + Claude
**Created:** 2026-04-13
**Active skill version:** v0.7.1 (commit `0498ca3`)
**Save location:** `~/grm-automations/docs/post-build-edit-playbook.md`

---

## When to use this playbook

After the skill reports a successful deploy and before the URL gets sent to any prospect. Every prospect site goes through this pass. No exceptions.

Typical time investment: 15-30 minutes per site.

---

## Required setup (one-time)

Confirm these are installed and working before the first touch-up:

- A code editor (VS Code, Sublime, or similar) with markdown and HTML syntax highlighting
- Vercel CLI authenticated on the `ron-7323` team (`vercel whoami` returns Ron, `vercel teams ls` shows ron-7323 active)
- Local Python 3 with Pillow (`python3 -c "import PIL; print(PIL.__version__)"` succeeds)
- An image editor for quick logo or photo crops (Preview on macOS is sufficient for crops; use Photoshop or Pixelmator if compositing is needed)

---

## Where files live

After the skill completes, every prospect's files are at:

```
~/grm-sites-prospects/[business-slug]/
  index.html              # Homepage
  about.html              # About page
  services.html           # Services overview page
  testimonials.html       # Testimonials page
  contact.html            # Contact page
  thanks.html             # Form submission thank-you page
  style.css               # Site-wide styles
  script.js               # Site-wide JavaScript
  llms.txt                # AI crawler index
  robots.txt              # Search crawler rules
  sitemap.xml             # Site map
  profile.json            # Final build manifest (read-only reference)
  assets/
    logo.png              # Nav and footer logo
    og-image.png          # Social card preview image
    favicon.ico           # Browser tab icon
    photos/
      [photo-slug]-400w.webp     # Each photo at 4 sizes
      [photo-slug]-800w.webp     # in WebP, AVIF, and JPEG
      [photo-slug]-1200w.webp    # fallback at 1200w
      [photo-slug]-1200w.jpg
      ... etc
```

The deployed Vercel site mirrors this folder one-to-one. Editing a file locally and redeploying replaces the live version.

---

## The standard touch-up checklist

Run through every item on this list for every build. Mark items that need fixing as you go, then do all fixes in one batch before the redeploy.

### Visual review on three devices

- [ ] Open the deployed URL on a desktop browser. Walk all 6 pages top to bottom.
- [ ] Open the deployed URL on Ron's phone. Walk all 6 pages top to bottom.
- [ ] Text the URL to yourself and check the iMessage preview thumbnail (this is the OG image test).

### Logo check

- [ ] Nav logo reads as the business's identity, not a generic graphic.
- [ ] Footer logo matches the nav logo.
- [ ] Logo is legible at 44px tall on desktop and 40px on mobile.
- [ ] If logo is bad: flag for fix (see "Common edits" below).

### Hero check

- [ ] Hero photo (or rotating photos) communicate the actual business.
- [ ] No kitchen-remodel-style photos that imply a service the business doesn't provide.
- [ ] Hero headline reads correctly and matches the prospect's voice.
- [ ] Phone number and CTAs are clearly visible and tappable on mobile.

### Service section check

- [ ] Featured service card uses a different photo than other service cards.
- [ ] Featured photo on Home page is different from featured photo on Services page.
- [ ] All listed services are real services the business actually provides.
- [ ] No invented services, no missing services Ron knows the business offers.

### Testimonials check

- [ ] All testimonial names are real first names (or first name + last initial), never "Happy Customer."
- [ ] Quotes are verbatim from the source (Google reviews, prospect's site, etc.).
- [ ] No invented testimonials.

### Contact check

- [ ] Phone number is correct in: nav, hero, footer, contact form, schema.
- [ ] Email address is correct.
- [ ] Address is correct (street, city, state, zip).
- [ ] Hours are correct, including emergency availability if applicable.
- [ ] Contact form submits to Ron's inbox (test with one real submission).

### OG / social card check

- [ ] Text the URL to yourself.
- [ ] Preview thumbnail in iMessage shows the business in a recognizable way.
- [ ] Brand color is present.
- [ ] If thumbnail looks bad: flag for OG image replacement (see "Common edits").

### Brand / voice check

- [ ] No "passionate about", "dedicated to", "leveraging" or other GRM banned phrases anywhere.
- [ ] No em dashes anywhere (the skill checks but verify).
- [ ] Headlines and CTAs sound like a real local contractor, not a chatbot.
- [ ] Place names (Ocala, Marion County, Dunnellon, etc.) are correct for this prospect's actual service area.

### License + credentials check

- [ ] Florida license number is correct (verify against state database if uncertain).
- [ ] Years in business are accurate.
- [ ] Owner names are spelled correctly.

---

## Common edits and how to make them

### Edit 1: Replace the logo

**When.** The skill's captured logo is illegible at nav size, missing the brand mark, or otherwise wrong.

**Steps.**

1. Acquire the correct logo asset. Sources in order of preference:
   - The business's website at higher resolution (right-click > Save As)
   - A Google Image search for the business name
   - A photo of the business's truck, sign, or storefront, cropped to the logo
   - Built from scratch in an image editor if no source exists
2. Save the new logo as `~/grm-sites-prospects/[business-slug]/assets/logo.png`. Overwrite the existing file.
3. The logo should be PNG with transparent background, roughly 400px wide on its longer dimension.
4. If the new logo's brand colors differ from what was extracted, flag it — the entire site's color scheme is derived from the original logo via node-vibrant. Replacing the logo without re-running color extraction will produce a color mismatch. For now, note the mismatch and decide whether to ship as-is or rerun the build.

### Edit 2: Replace the OG / social card image

**When.** The iMessage preview looks generic, has wrong color, or doesn't show the business.

**Steps.**

1. Pick a strong hero photo from `~/grm-sites-prospects/[business-slug]/assets/photos/`. Look for a JPEG at 1200w that shows the business clearly.
2. Open Preview (or any image editor). Resize to 1200x630.
3. Save as `~/grm-sites-prospects/[business-slug]/assets/og-image.png`. Overwrite the existing file.
4. Optional: composite a brand-color bottom bar with the business name and phone, per the b6 mockup recipe at `~/grm-automations/audits/tandf-v07-vs-v072-2026-04-13/og-mockups/variant-b6-final-polish.png`. The recipe is documented in the v0.7.3 spec (preserved at git commit `7134045` in the skill repo) and on Ron's desktop. Use it as a reference even though the v0.7.3 implementation was reverted.

### Edit 3: Swap a hero photo

**When.** A photo in the hero rotation doesn't communicate the business well (e.g., a kitchen photo on an electrician's site).

**Steps.**

1. Identify the bad photo's filename in `assets/photos/`.
2. Pick a replacement from elsewhere in `assets/photos/` or download a new photo from the business's Google Business Profile.
3. If the replacement is from elsewhere in `assets/photos/`, just edit the references in `index.html` (search for the bad filename, replace with the new one).
4. If the replacement is new, run it through Pillow to produce the standard 9-file output set (4 sizes × 2 modern formats + JPEG fallback at 1200w). Reference `~/grm-sites-prospects/[business-slug]/profile.json` to see what sizes the existing photos use.
5. Update `index.html` references to point at the new photo.

### Edit 4: Fix copy or service descriptions

**When.** A service description is wrong, a phone number has a typo, an owner's name is misspelled, etc.

**Steps.**

1. Open the affected `.html` file in your editor.
2. Use find-and-replace for anything that appears in multiple places (phone numbers, business name, etc.).
3. For single-location fixes, just edit the relevant section.
4. For phone number changes especially: verify the change in nav, hero CTA, footer, contact form, and the JSON-LD schema block in the `<head>`. The skill enforces consistency across all five locations and a typo in any one will look unprofessional.

### Edit 5: Adjust service order or remove a service

**When.** The skill captured a service that the business doesn't actually offer, or the order doesn't match the prospect's priorities.

**Steps.**

1. Open `index.html` and `services.html`.
2. The services live in a grid section. Find the service-card div(s) for the affected service.
3. To remove: delete the entire service-card div block.
4. To reorder: cut and paste the service-card divs in the desired order.
5. Ensure the featured service card is still distinct (uses a different photo than the others).

---

## Redeploying after edits

Once all edits are complete, redeploy:

```
cd ~/grm-sites-prospects/[business-slug]
vercel --prod --yes
```

The redeploy preserves the existing project URL. No new URL is generated.

After redeploy:

- [ ] Wait 30-60 seconds for the deploy to propagate.
- [ ] Reload the live URL on desktop and mobile.
- [ ] Verify the edits actually shipped (sometimes browser cache shows the old version — hard refresh with Cmd+Shift+R).
- [ ] Re-run the standard touch-up checklist on the redeployed version. Sometimes an edit introduces a new issue.

---

## What NOT to edit

These items can break the site or the SEO/GEO infrastructure if touched without care. Do not edit unless you know exactly what you're doing.

- **JSON-LD schema blocks in `<head>`.** Phase 5.5 generates these to validate against Google Rich Results. Editing them risks invalidating the schema and breaking AI search visibility.
- **OpenGraph and Twitter Card meta tags.** These reference the og-image.png. If you swap the image, you don't need to edit these. If you change the URL structure, you do — but URL structure changes should be rare.
- **Anything in `style.css` without testing on mobile.** Desktop-only CSS edits can break the mobile layout in non-obvious ways.
- **Scripts in `script.js`.** The hero crossfade, the scroll reveal animations, the before/after slider — all live here. Breaking these is easy and unobvious. If you need a script change, ask Claude before editing.
- **The `vercel.json` config (if present).** Build commands and routing rules. Wrong values produce silent deploy failures.

---

## Common edit patterns logged for v0.7.x improvement candidates

Track patterns across F3-F6 and beyond. If the same edit gets made on more than 3 builds in a row, it's a candidate for becoming a real skill rule in v0.7.4 or later.

| Pattern | Builds where it occurred | Candidate for skill rule? |
|---|---|---|
| Logo replacement (skill captured wrong/illegible logo) | T&F | Yes — eventually |
| OG image replacement (skill output too generic) | T&F | Yes — eventually |
| Service description tweaks | TBD | Watch |
| Hero photo swap | TBD | Watch |
| Phone number correction | TBD | Should never happen — flag if it does |

Update this table after every build.

---

## When a touch-up reveals a skill problem

If during touch-up you discover the skill produced something objectively wrong (not just suboptimal), log it. Don't try to fix the skill mid-week. The discipline is: skill engineering happens after Wednesday's kickoff, not during the build sprint.

Add the entry to:

```
~/.claude/skills/prospect-site/references/LESSONS.md
```

Format:

```
## YYYY-MM-DD — [Short title]

**Category:** [Skill bug / Skill limitation / Process / Edge case]

### What happened
[Description]

### Lesson
[Generalized takeaway]

### v0.7.x candidate fix
[Proposed rule, or "manual touch-up workaround acceptable"]
```

---

## Closing this playbook out

This playbook is a living document. After Wednesday's kickoff, review it against actual experience from F3-F6 and update:

- Any common edits that came up but aren't documented here, add to the "Common edits" section
- Any patterns in the tracking table that reached 3+ occurrences, decide whether they become v0.7.4 rule candidates
- Any "What NOT to edit" surprises that came up, add to that section

The goal is a playbook that gets sharper with every build, so by the time GRM has 30 active prospects, the touch-up takes 10 minutes instead of 30.

---

*End of playbook.*

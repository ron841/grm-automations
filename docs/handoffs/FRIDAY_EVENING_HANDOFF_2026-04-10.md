# FRIDAY EVENING HANDOFF — 2026-04-10

**Session window:** Friday April 10, 2026 — full day (morning audit → afternoon clean run → evening mobile review → evening skill improvement)

**Headline:** First fully clean end-to-end prospect-site skill run in project history. Zero intervention. Zero fabrication. Three real-world observations captured and shipped as v0.7.2 same night.

---

## What shipped today

### Morning session
- Audited, fixed, and installed **prospect-site skill v0.7.1** at `~/.claude/skills/prospect-site/`
- Phase 0 fully green — all 7 hard checks pass
- Google Places API unblocked by enabling the **legacy Places API** on the key alongside Places API New
  - New LESSONS.md candidate (category INTEGRATION): *"Google Places key restricted to 'Places API (New)' will REQUEST_DENIED legacy endpoint calls even when key is valid"*
- Prior skill backed up at `~/.claude/skills/prospect-site.backup.20260410-093850`

### Afternoon session — the clean run
- Invoked `/prospect-site` on T&F Electric (`https://www.tandfelectric.com/`)
- Deploy target: new Vercel project `tandf-electric-v07` (flagship `tandf-electric` untouched)
- **No stitch framing.** Clean end-to-end run on v0.7.1, skill standing on its own
- All phases completed without intervention: Phase 0 → 2.5 → 3 → 5 (build) → 6 (quality gates) → Vercel deploy

### Production verification — all 8 checks passed
| Check | Result |
|---|---|
| HTTP | 200 OK |
| Title | T&F Electric \| Licensed Electrician in Dunnellon, Ocala & Marion County, FL |
| H1 | Fifty years. Two Tuccis. One phone number. |
| Phone consistency | 8 tel: links, 15 display instances |
| Hero slides | 6 (1 container + 5 slides) ✓ |
| Dark stats section | 1 (exactly one) ✓ |
| Testimonials | 6 on homepage ✓ |
| FAQ items | 6 ✓ |
| Service cards | 10 service items + featured ✓ |
| JSON-LD | Electrician + FAQPage both parse, real data (EC13007855, 4.6/41, founded 1976) |
| Em dashes | **0** ✓ |
| Google photo attribution | Present ✓ |

**Live at:** `https://tandf-electric-v07.vercel.app`
**Flagship preserved at:** `https://tandf-electric.vercel.app` (untouched, as scoped)

### Why this run matters
- **Zero fabricated stats.** The Phase 2 review-source verification rule hardened after the prior T&F HomeAdvisor fabrication incident held. JSON-LD contains only real, verified data.
- **Zero em dashes.** Anti-slop content rules held.
- **Plant Street voice landed.** "Fifty years. Two Tuccis. One phone number." is real voice, not generic contractor filler.
- **Structural constraints held.** Exactly one dark stats section, six testimonials, six FAQ items, correct hero structure. No duplicate or missing sections.
- **Phone consistency intact** across tel: links and display instances — a known pain point in earlier versions.
- **Google Places photo attribution compliant.**

### Evening session — mobile review + v0.7.2 shipped
Walked T&F v07 on mobile. Three real-world observations captured — all skill-level issues, not site-level patches:

**Issue 1 — Logo reconstruction in type.** Skill attempted to rebuild T&F's brand mark in CSS/HTML type ("**T** &F Electric" in the nav) instead of downloading the real square logo from their hero. Conversion-killer on first impression.

**Issue 2 — OG thumbnail rendered in blue when brand is red.** Site renders correctly in red, but the social preview thumbnail used a hardcoded default blue instead of pulling from the captured brand palette. Undermines the "this is yours" pitch when Cameron shares the URL.

**Issue 3 — Featured service card image reuse across pages.** The Generator Installation featured card rendered with the *same photo* on both the Home page services preview and the Services page grid. With Unsplash API access, each instance should pull a different image from the same topical query — same service, same copy, different photo.

**All three fixes shipped same night as v0.7.2.**

---

## v0.7.2 install confirmation

**Backup:** `/Users/ronkolb/.claude/skills/prospect-site.backup.20260410-181329`

**Files modified (3):**
| File | Before | After | Δ |
|---|---|---|---|
| SKILL.md | 729 | 758 | +29 |
| references/image-handling.md | 833 | 928 | +95 |
| references/seo-geo.md | 1431 | 1478 | +47 |
| **Total** | **2993** | **3164** | **+171** |

**Version:** `# Prospect Site Generator (v0.7.2)` — confirmed at line 6 and in Version section line 734. Changelog entry dated 2026-04-10 added with three v0.7.2 rule entries.

**New rule sections:**
- `image-handling.md` line 837 — `## LOGO CAPTURE — TIERED WITH SOFT-WARNING FALLBACK`
  - Tier 1: extract `<img>` from header/hero/nav (alt text, filename, or parent element heuristics)
  - Tier 2: OG image, apple-touch-icon, or high-res favicon (min 128×128)
  - Tier 3: type-based wordmark **only** if Tiers 1 and 2 fail, with mandatory Phase 6 soft warning
  - Build does not hard-stop on logo capture failure
- `image-handling.md` line 896 — `## FEATURED SERVICE CARD IMAGE ROTATION`
  - Same featured service on multiple pages may share copy/structure, must use different images
  - Per-service image rotation list, expanding Unsplash query if needed
  - Phase 6 gate: hard fail if a featured service card image appears on more than one page
- `seo-geo.md` line 1435 — `## OG IMAGE COLOR — MUST PULL FROM CAPTURED BRAND PALETTE`
  - OG background must use `brand.colors.primary` from Phase 2 profile-draft
  - Hardcoded defaults forbidden; null fallback is neutral dark gray (#1a1a1a), never an accent color
  - Phase 6 gate: verify OG primary color matches captured brand primary within hue tolerance

**SKILL.md cross-references placed:**
- Line 179 (Phase 1 step 4) — logo tier rule
- Line 208 (Phase 2 step 5) — brand capture cross-ref
- Line 502 (Phase 5 Hard rules) — featured service card rotation
- Line 568 (Phase 5.5 SEO/GEO) — OG image color rule

**Sanity checks:** 18 balanced code fences in SKILL.md, all three new sections grep-visible by title, no full skill invocation run tonight (validation deferred to Flagship 2).

**v0.7.2 status:** Installed and believed correct. Not yet proven correct — validation happens on Flagship 2 next session.

---

## Next session agenda

1. **Validate v0.7.2 on Flagship 2** — select a fresh prospect from the ~28-site manually curated shortlist, run clean end-to-end, verify the three new rules actually fire correctly:
   - Does logo tiered capture grab the real logo? Does the soft warning fire when it can't?
   - Does the OG thumbnail render in the prospect's real brand color?
   - Do featured service cards on Home vs. Services show different images?
2. **Flagship 3** queued after Flagship 2 validation
3. **Sales infrastructure session** (separate scope) — service agreement PDFs (Elevate + Launch tiers), pricing one-pager, HubSpot pipeline, pause old magazine call automation, kick off Cameron's outbound call campaign

---

## Punch list (carried forward)

- **API key rotation** — both Google Places and Unsplash keys need rotation (Places was exposed in earlier session chat; Unsplash is hygiene)
- **HubSpot + backup soft warnings** in Phase 0 — noted, non-blocking, address when sales infrastructure session opens
- **Delete `grm-website` orphan Vercel project** — safe, deferred, still safe, still deferred
- **21st-dev/magic-mcp #49** — post updated symptom comment (Magic MCP tools no longer register in Claude Code sessions at all; vendor bug worsening)
- **LESSONS.md** — add the Places API legacy endpoint INTEGRATION entry

---

## What changed in the understanding of the skill tonight

Before tonight, the skill was "good, with known rough edges we'd patch per-site." After tonight, the skill is **a real system we harden from real-world feedback, not a template we babysit.** The difference matters: the v0.7.2 improvements apply to Flagship 2, Flagship 3, and every prospect build after. We stopped patching sites and started improving the skill that builds sites. That's the jump from craft to production.

---

## Commit steps

1. `FRIDAY_EVENING_HANDOFF_2026-04-10.md` → `grm-automations/docs/handoffs/`
2. Upload same file to Google Drive handoffs folder
3. Update `GRM_BRAIN.md`:
   - Mark v0.7.1 clean run as shipped
   - Mark v0.7.2 as installed (validation pending Flagship 2)
   - Add `tandf-electric-v07.vercel.app` as second T&F reference (flagship still at `tandf-electric.vercel.app`, untouchable)
   - Add LESSONS.md candidate (Places API legacy endpoint) to the lessons queue
4. No deferred cleanup tonight. Session closes clean.

---

*"Fifty years. Two Tuccis. One phone number." — the line that proved the skill could write voice, not copy.*

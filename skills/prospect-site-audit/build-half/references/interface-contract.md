# Interface Contract — audit-half → build-half (v1.0)

The boundary spec for the v1.0 split architecture. Audit-half captures and authors; build-half renders and deploys. This document defines what crosses the boundary, in what shape, where it's written, and what each side does when the contract breaks.

For slot vocabulary detail (every field on profile.json, every slot on prose.json, per-band fallback behavior, the testimonial merge + scoring rule), see [fixture-contract.md](fixture-contract.md) in this same directory. **This file is the boundary spec; fixture-contract.md is the detail reference.** They are not duplicates — interface-contract.md governs *what crosses the boundary and what happens when the contract breaks;* fixture-contract.md governs *the schema and per-field behavior.*

## 1. Inputs to build-half

Audit-half produces two artifacts in the prospect workspace at `~/grm-sites-prospects/[business-slug]/`. Build-half (`render.py`) reads both as required inputs.

### 1.1 profile.json — captured-facts file

Audit-half writes via Phase 1 (homepage capture), Phase 2 (multi-page crawl), Phase 3 (photo collection), Phase 3.5 (data quality gate), Phase 4 (designChoices block from approval gate), and Phase 5 Step 1 (promotion from `profile-draft.json` with `unknownFields[]` set).

- **Write path:** `~/grm-sites-prospects/[slug]/profile.json`
- **Schema:** see [fixture-contract.md §2](fixture-contract.md) for the full field inventory (required + optional tables) and §2.A for the testimonial merge + scoring rule.
- **Required fields** (build-half hard-warns or fails without these): `contact.phone`; one of `identity.siteTitle` / `identity.commandAliasName` / `businessName.primary`; `services.list[]` with ≥4 entries; one of `photoLibrary.heroCandidatesTop5[]` / `heroCandidatesAll[]`; one of `contact.addressConsensus` / `contact.addressCanonical`.
- **Optional fields:** silent default or band drop per fixture-contract.md §2.

### 1.2 prose.json — voice-blessed prose file

Audit-half authors via Phase 5 Step 2 against the slot vocabulary in fixture-contract.md §4 (homepage flat slots) and `references-consolidated/prose-rules.md` §6.6 (inner-page page-keyed slots).

- **Write path:** `~/grm-sites-prospects/[slug]/prose.json`
- **Voice contract:** authored against the four-reference set: `voiceMap.md` + `prose-rules.md` + `content-rules.md` + `anti-slop-rules.md`. The four references load as Phase 5 Step 0 (non-negotiable pre-flight) per audit-half SKILL.md hard rule #5.

**Schema (pure page-keyed is canonical).** prose.json uses page-keyed sub-dicts for ALL pages, including the homepage. Per Deliverable 3 of the Session 1 reconciliation (2026-04-28, corrected via empirical render.py test against Volthom prose.json):

- All prose lives under page-keyed sub-dicts: `prose.homepage.*`, `prose.about.*`, `prose.services.*`, `prose.testimonials.*`, `prose.contact.*`.
- `references-consolidated/prose-rules.md` §6.1–§6.6 documents the canonical per-slot rules (homepage rules apply under `prose.homepage.*`).
- [fixture-contract.md §4-LEGACY](fixture-contract.md) preserves the v0.8-era flat schema as a migration reference for prospects whose prose.json was authored against the v0.8 monolith path.

Existing v0.8-era prose.json files (e.g., Volthom's at `~/grm-sites-prospects/volt-home-electric/prose.json`) require re-authoring into page-keyed shape before render.py produces non-fallback output. The migration is mechanical: wrap homepage slots under a `homepage` sub-key.

### 1.3 Asset paths referenced from profile.json

profile.json fields under `photoAssignments.*`, `services.list[].featuredImage`, `services.list[].detailImage`, etc., reference paths in `~/grm-sites-prospects/[slug]/assets/photos/`. The render.py invocation uses `--photos-root` to resolve these relative to the prospect folder.

## 2. Outputs from build-half

`render.py` writes per-page HTML files plus three sidecar files. `deploy.sh` consumes everything in the prospect workspace at deploy time.

### 2.1 Per-page HTML files

`render.py --page [key] --out [path]` writes one HTML file per page key.

- **Default write path convention:** `~/grm-sites-prospects/[slug]/[page-key].html`
- **Page key set:** five canonical page keys per Deliverable 3 of the Session 1 schema reconciliation — `homepage` (default), `about`, `services`, `testimonials`, `contact`. render.py's `--page` argument accepts these values; `INNER_PAGE_KEYS` is the inner-page subset. `render.py` drops bands per fixture-contract.md §3 fallback rules when data is absent.
- **Output schema:** HTML5. When `--canonical-base` is supplied, embedded JSON-LD blocks (LocalBusiness, Service, FAQPage, Review) ship per `references-consolidated/seo-geo.md`.

### 2.2 Sidecar files emitted by render.py

When `--canonical-base` is supplied, render.py emits two sidecars:

- `sitemap.xml` at `~/grm-sites-prospects/[slug]/sitemap.xml`. Schema: sitemaps.org 0.9. One `<url>` entry per page key.
- `robots.txt` at `~/grm-sites-prospects/[slug]/robots.txt`. User-agent allow-all plus sitemap pointer.

When `--canonical-base` is empty, both sidecars are suppressed along with all canonical / OG URL / JSON-LD url emission.

### 2.3 Sidecar file emitted by audit-half

- `llms.txt` at `~/grm-sites-prospects/[slug]/llms.txt`. Schema: AnswerDotAI llms.txt spec. Audit-half authors at Phase 5.5.
- **Engine-extension item:** llms.txt has no producer in build-half today. Audit-half writes it for now. Future engine-extension absorbs llms.txt emission into render.py or deploy.sh.

### 2.4 What deploy.sh consumes

`deploy.sh` reads everything in `~/grm-sites-prospects/[slug]/` matching `*.html`, `sitemap.xml`, `robots.txt`, `llms.txt`. **Slug reconciliation runs at the deploy boundary** — deploy.sh rewrites stale `.vercel.app` references when the final Vercel alias differs from any `--canonical-base` value baked in by render.py at Phase 5. See `build-half/scripts/deploy.sh` source for the reconciliation procedure.

This is a third boundary in the pipeline (build-half → deploy) — it's outside the strict scope of this contract, but the slug-reconciliation behavior is load-bearing for audit-half's `--canonical-base` value choice at Phase 5.

## 3. Invocation command (canonical form)

audit-half invokes render.py once per page key from Phase 5 Step 3:

```bash
python3 build-half/scripts/render.py \
  --profile        ~/grm-sites-prospects/[slug]/profile.json \
  --prose          ~/grm-sites-prospects/[slug]/prose.json \
  --out            ~/grm-sites-prospects/[slug]/[page-key].html \
  --photos-root    ~/grm-sites-prospects/[slug] \
  --css-href       ../../css/composer-system.css \
  --canonical-base https://[slug]-grm.vercel.app \
  --page           [homepage | about | services | testimonials | contact]
```

**Required arguments:**

- `--profile` — path to profile.json
- `--prose` — path to prose.json
- `--out` — output path for the rendered HTML file

**Optional arguments and their effects:**

- `--photos-root` — root dir for resolving relative photo paths. Defaults to the profile's parent dir.
- `--css-href` — value for `<link rel="stylesheet" href=X>` in emitted HTML. Defaults to `../../css/composer-system.css`.
- `--canonical-base` — absolute prod URL (no trailing slash). When supplied, enables canonical / OG URL / JSON-LD url + image / sitemap.xml entry emission. Empty disables.
- `--page` — which page slot group to emit. Default: `homepage`. Inner-page choices come from `INNER_PAGE_KEYS` in render.py.
- `--access-key` — StaticForms accessKey embedded in the contact form's hidden `<input>` field. Defaults to placeholder. **deploy pipeline substitutes the real key via sed at the pre-Vercel boundary; real-key renders MUST NOT be committed.**

**Hand-off to deploy.sh** (post-Phase 6 pass): see audit-half SKILL.md Phase 7 for the canonical hand-off command shape.

## 4. Error states

### 4.1 What audit-half does when build-half fails

**render.py exit codes are unwired** (engine-extension item #1). The docstring at the top of render.py promises exit 1 (§7 validation failure) and exit 2 (data shape blocker), but `main()` returns 0 unconditionally — there are no `return 1` or `return 2` paths in the file. Audit-half does NOT depend on exit codes for failure detection.

**Audit-half failure detection runs at Phase 6 grep gates on the emitted HTML files, independently of render.py.** The 18 Phase 6 checks detect the failure modes render.py prints as warnings on stdout but doesn't gate on. The check list:

1. HTML validation (W3C HTML5)
2. Em-dash check (UTF-8 + HTML-entity encodings)
3. Banned output check (corporate jargon / AI tells / banned credential claims / CTA trailing-fragment hallucinations)
4. Link check (no 404s, no `href="#"` placeholders)
5. Image reference check
6. H1 count check (exactly one per page)
7. Mixed content check
8. Phone number consistency (5-location cross-reference)
9. Schema-to-profile cross-reference
10. Unknown-field guard
11. Photo attribution
12. Contact form HTML wiring
13. Contact form live submission test
14. Schema.org validation
15. Lighthouse CI gate (mobile thresholds)
16. Mobile render verification at 375px
17. Social metadata completeness
18. llms.txt existence and format

**Audit-half stops at any Phase 6 failure.** Does not hand off to deploy.sh. Reports to Ron with: which check failed, file and line context, recommended fix, whether the fix is automatic or requires Ron's input.

**Render.py warnings on stdout** are surfaced to Ron at Phase 5 Step 4 (eyeball walk + report). Warnings are advisory — they do not by themselves block hand-off, but they should be inspected before Phase 6.

### 4.2 What build-half does when prose.json is malformed

**JSON parse errors.** `render.py` reads prose.json via `json.load`. Malformed JSON raises `JSONDecodeError`, which crashes render.py with a Python traceback. No HTML output is produced. Audit-half catches this immediately at Phase 5 Step 3 (the render command fails to complete).

**Missing required slots.** render.py emits warnings to stdout but produces partial HTML output and still returns 0 (the engine-gap behavior). Audit-half catches missing-slot output at Phase 5 Step 4 (eyeball walk) and Phase 6 grep gates — partial bands, empty `<p>` elements, or dropped sections per fixture-contract.md §3 fallback rules.

**Schema-to-profile mismatches.** When prose.json claims a fact that profile.json does not back (e.g., a license-number reference in a display headline when profile.json's `unknownFields[]` includes `"license_number"`), Phase 6 check 10 (unknown-field guard) fails the build. The check greps emitted HTML for claim vocabulary tied to each unknown field, per `references-consolidated/anti-slop-rules.md` § "Unknown-field claim vocabulary."

**Voice-rule violations.** When prose.json contains banned phrases or em dashes outside the §6.2 hero-subhead exception, Phase 6 checks 2 (em-dash) and 3 (banned output) fail the build. The checks grep emitted HTML — render.py passes the violations through verbatim.

### 4.3 What build-half does when profile.json is malformed

**JSON parse errors.** Same as 4.2 — `JSONDecodeError` crashes render.py.

**Missing required fields.** Each required field in fixture-contract.md §2.1 has a documented failure mode (band drops, empty render, or §7 check failure). render.py emits warnings; audit-half catches at Phase 6.

**Field-shape mismatches.** When a field exists but with the wrong shape (e.g., `services.list` is a string instead of an array), render.py raises a Python exception during render. Audit-half catches at Phase 5 Step 3.

### 4.4 Photo path resolution failures

When profile.json references a photo path that does not resolve under `--photos-root` (broken symlink, missing file, typo in path), render.py emits a warning and may produce HTML with a broken `<img>` tag or missing `background-image`. Phase 6 check 5 (image reference check) detects and fails the build.

## 5. Engine-extension items affecting this contract

Five gaps documented at audit-half SKILL.md "Known engine-extension items" section. Surfaced at Session 1 of v1.0 rewrite (2026-04-28). Not blockers for v1.0 audit-half shipping.

1. **render.py exit codes unwired.** Affects §4.1. Audit-half cannot rely on exit codes; runs Phase 6 grep gates independently of render.py.

2. **render.py background-treatment expansion.** render.py currently emits only the single-photo hero treatment. The flagship walk (5 deployed sites, 2026-04-28) confirmed three background treatments are needed: slideshow (≥3 photos), single (1–2 photos, optional mesh-canvas overlay), mesh-only (0 photos). Audit-half captures photo data; engine picks treatment when the extension lands. Affects §3 — `--page` argument is unaffected, but the rendered hero shape is engine-gated.

3. **llms.txt has no producer in build-half.** Affects §2.3 — audit-half writes llms.txt at Phase 5.5; future engine extension absorbs it.

4. **`scripts/test_form_submission.py` missing.** Affects §4.1 Phase 6 check 13. Helper existed in the v0.7.2 monolith install; needs port to v1.0 audit-half scripts directory or fresh stand-up.

5. **`scripts/mobile_render_check.py` missing.** Affects §4.1 Phase 6 check 16. Same status as #4. **Also affects Session 2 prep:** mobile (375px) rendering of the three hero background treatments (single / slideshow / mesh-canvas) is unverified — first slideshow flagship validation in Session 2 surfaces this question.

6. **v0.8-era prose.json files require migration to page-keyed shape.** Existing v0.8 prospects (Volthom, F1-F8 flagships) have prose.json in flat homepage schema (h1 / hero_kicker / etc. at top level of prose.json). render.py's canonical schema is page-keyed (slots under `prose.homepage.*`). Migration is mechanical (wrap homepage slots under a `homepage` sub-key). Affects Session 2 Volthom validation — see Session 2 prompt for disposition options (re-author Volthom prose.json vs target a fresh prospect).

## Version

interface-contract.md v1.0, 2026-04-28. Authored at Session 1 of the v1.0 rewrite (Deliverable 2 of three). Updated at Deliverable 3 close, then **corrected late in Session 1 after empirical render.py verification surfaced that the previously-documented hybrid schema was a misread**. Pure page-keyed is canonical; v0.8-era flat schema is preserved as legacy/migration reference.

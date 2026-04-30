# Fixture Handoff Contract

The interface between an audit run (`/prospect-site` Phase 0-3.5) and the v2
composer. When Ron drops a profile-draft.json path here, this doc tells
the executing Claude exactly what to check and what to fill in.

## 1. Where the audit lands

`/prospect-site` run against any URL produces:

```
~/grm-sites-prospects/[business-slug]/
  profile-draft.json        ← the composer's input
  raw/                      ← captured HTML pages (composer ignores)
  assets/
    photos/
      google/               ← Google Places photos (up to 10)
      site/                 ← downloaded from the prospect's site
      instagram/            ← (usually empty)
      unsplash/             ← (usually empty)
```

The composer does not care about `raw/`. It reads `profile-draft.json` and
resolves photo paths relative to the prospect folder via `--photos-root`.

**Canonical drop-in command when a fresh audit lands:**

```bash
cd ~/.claude/skills/prospect-site-v2
mkdir -p fixtures/[slug]
ln -sf ~/grm-sites-prospects/[slug]/profile-draft.json fixtures/[slug]/profile.json
ln -sf ~/grm-sites-prospects/[slug]/assets            fixtures/[slug]/assets

# Author prose.json per the audit-side voice contract (voiceMap.md +
# content-rules.md + anti-slop-rules.md) against the slot vocabulary in §4
# below — one pass, all five slot groups. Save to fixtures/[slug]/prose.json.

python3 scripts/render.py \
  --profile fixtures/[slug]/profile.json \
  --prose   fixtures/[slug]/prose.json \
  --out     fixtures/[slug]/Homepage.html \
  --photos-root ~/grm-sites-prospects/[slug] \
  --css-href ../../css/composer-system.css

open fixtures/[slug]/Homepage.html
```

## 2. Fields the composer reads from profile-draft.json

Below: the exact JSON path, whether it is required, the engine function that
reads it, and what happens if it is missing. "Required" means the render
fails or falls back noisily. "Optional" means the render proceeds silently
using a default or by dropping the dependent band.

### Required — render fails or hard-warns

| JSON path | Required by | Failure mode if missing |
|---|---|---|
| `contact.phone` | nav CTA, hero CTA, anchor strip, footer | Phone renders empty. §7 check 7 fails. Surface at approval gate. |
| `identity.siteTitle` OR `identity.commandAliasName` OR `businessName.primary` | nav, title, wordmark, footer | Engine falls to literal string `"Business Name"`. Ugly. Approval gate should stop. |
| `services.list[]` | services band | If fewer than 4 entries, services band renders with missing tiles. §2.6 says error. |
| `photoLibrary.heroCandidatesTop5[]` OR `heroCandidatesAll[]` | hero band, pullquote bg | Hero renders with empty `background-image`. Surface at approval gate. |
| `contact.addressConsensus` OR `contact.addressCanonical` | footer, anchor strip | City/state derived from address. Without it, city_state falls to `"Marion County"` placeholder — visible mistake. |

### Optional — silent default or band drop

| JSON path | Consumed by | What happens if missing |
|---|---|---|
| `identity.tagline` | footer `p.tag` | Falls to `prose.footer_tag`, then to `"Excellence is a Lifestyle."` |
| `contact.email` | footer | Line is omitted from footer-contact. |
| `contact.hours.*` | anchor strip, footer | Anchor shows `"By appointment"`; footer renders whatever is present. |
| `contact.serviceAreaCities[]` | anchor strip | Falls to the raw city_state string. |
| `owners.list[]` | story band | Story band drops entirely (§4). Manifesto gets full-bleed role. |
| `team[]` | §2.4 stats trio (if ≥10) | That stat slot is skipped. |
| `testimonials.fromSite[]` + `testimonials.fromGoogleReviews[]` | testimonials band (3-up) | **Merged pool** (rev 2026-04-24, Volt patch). Engine concatenates both arrays, ranks by the specificity scoring rule in §2.A below, takes top 3. Band drops if <3 total testimonials ≥ 4 stars remain after ranking (§4). Site testimonials default to 5-star since the prospect curated them onto their own page. |
| `testimonials.fromSite[].featured` + `testimonials.fromGoogleReviews[].featured` (Phase 4 §1) | testimonials band + testimonials.html | **Optional editorial overlay** (bool). Sort order becomes featured-first → score-fill. Page-aware caps: homepage band stays 3-up (featured win the top slots); `testimonials.html` hard-caps at 6 when ≥1 featured present, else ship-all (Phase 3a fallback). When zero entries carry `featured`, behavior is identical to the prior pure-score sort — backwards-compatible. Curation pattern: Ron picks N strongest reviews from the pool; engine still scorer-ranks within the featured set so order is stable. |
| `googleBusiness.rating` + `.reviewCount` | stats trio, hero badge, trust cell | Badge omitted. Stats and trust pick next-priority items. |
| `credentials.licenseNumber` | stats trio (priority 6), trust | Skipped from stats pool. |
| `credentials.awards` | stats trio (priority 3), trust | Skipped from stats pool. |
| `credentials.yearsInBusiness` / `yearsInBusinessStated` | stats trio (priority 4), trust | Skipped. |
| `photoLibrary.galleryPhotoCount` | stats trio (priority 2 if ≥50), trust | Skipped from stats pool. |
| `socialMedia.facebook` / `instagram` / `youtube` | footer social links | Individual icons omitted. |
| `promotions.featuredPromo` (Phase 3b §1) | promo callout band | Null/absent → band drops (correct gating per dropped-sections.md §1). When present, schema is `{ eyebrow, headline, sub, cta, dateRange }`; the engine emits the `.promo-callout` band on the homepage. **This is an authored input** — unlike `profile.faq[]` which is derived by `resolve_faq` at render time, `featuredPromo` is the prospect's actual dated business promotion and the composer never invents one. Date-range expiry is NOT enforced at render time (Phase 5+ rule). Voice tuning lands in `prose.homepage.promo_callout`; the profile carries data, prose carries voice. |
| `photoLibrary.beforeAfterPairs[]` (Phase 3b §2) | before/after gallery band | Empty/absent → band drops. Each item is `{ before: <path>, after: <path>, caption?: <str> }`. Volthom + JSL both ship empty pairs and correctly drop the band. The first prospect with paired photos is the forcing function for full markup + CSS — see `dropped-sections.md` §2. |
| `googleBusiness.rating`/`reviewCount` + `credentials.licenseNumber`/`licenseType`/`veteranOwned`/`familyOperated`/`certifications` + `owners.list[].title` (Phase 4 §C) | trust marquee band | **Derived (not contract).** `resolve_trust_items(profile)` returns up to 6 short strings for the homepage `.trust-marquee` band 02. Sources mapped 1:1 from existing fields above. Floor: when fewer than 3 items resolve, the homepage flow falls back to `.anchor-strip` — Phase 3c persona-gating will replace the fallback with explicit dispatch. No new fixture-contract fields; this just documents which existing fields the resolver consumes. |
| `services.list[].tagline` | service tile `.svc-tag` | Falls to `prose.service_taglines[slug].tagline`. If neither present, tile renders without the italic line. |
| `services.list[].description` | service tile `.svc-desc` | Tile renders with empty `<p class="svc-desc"></p>`. Ugly but not fatal. |
| `services.list[].featuredImage` (Phase 4.5) | services-bento featured-card bg-image (homepage + services.html) | When unset AND `_unsplash-cache.json` has a `featured` pick for the slug, `resolve_service_photos` populates this from the cache (Phase 5.0b). When still unset after that pass, the featured-card ships the brand-blue CSS gradient. |
| `services.list[].detailImage` (Phase 4.5b) | service-detail block bg-image on services.html | Same population path as `featuredImage` — cache populates when unset. When still unset (or slug flagged `gradient_fallback`), the service-detail block ships the empty CSS-styled card. |
| `services.list[].stockQuery` (Phase 5.0b, optional) | `unsplash_fetch.py` per-prospect query override | When unset, falls to the built-in `SERVICE_PHOTO_QUERIES[slug]` table in `scripts/unsplash_fetch.py`. Use this only when a prospect's service slug doesn't match the default table (e.g. a slug like `whole-house-rewire` instead of `rewires`). |
| `services.list[].stockQueryBackup` (Phase 5.0b, optional) | `unsplash_fetch.py` backup query when primary returns <3 results | When unset, falls to the backup string in the default table. Backup is the second-chance angle for slugs whose primary query returns thin results — e.g. for `generators` the backup is `"residential backup power generator"`. |
| `identity.siteDescription` | trust cell "Weekly crew training" detection | Cell skipped from trust pool. |
| `brandPalette.*` | palette tokens | Falls to JSL reference palette (forest green + rust on cream). |
| `brandPalette.manifestoBand` (v2.0+, derived if absent) | `--manifesto-band-bg` CSS custom property on the manifesto band | The manifesto band reads its background from `var(--manifesto-band-bg, #f7f2e8)`. The render engine's `resolve_manifesto_band()` picks the value in this priority order: **(1)** if `brandPalette.background` is already a warm cream (min channel > 222 AND red >= blue), use it as-is — warm-palette brands like JSL land here; **(2)** else if `brandPalette.accent` or `brandPalette.primary` is warm (red is the dominant channel by ≥10), mix 88% fallback + 12% that color to produce a subtle brand-tuned warm cream — Volthom's navy-primary + amber-accent palette lands here and yields an amber-tinted cream; **(3)** else fall back to `#f7f2e8` (neutral editorial warm cream). The derivation note is preserved in the resolved palette as `manifesto_band_note` for debugging. |

### 2.A Testimonial merge + scoring rule (rev 2026-04-24)

When the testimonials band assembles its 3-up pool, the engine calls
`resolve_testimonials(profile)` in `scripts/render.py`. That function:

1. Concatenates `testimonials.fromSite[]` and `testimonials.fromGoogleReviews[]`
   into a single pool.
2. Filters to `rating >= 4` (site testimonials default to 5-star since the
   prospect curated them onto their own page; Google reviews carry explicit
   `rating`).
3. Scores each testimonial for specificity:
   - `+30` if `role` field present (named title: "CEO", "Comptroller, Prestige Auto")
   - `+20` if `location` field present (named place: "The Villages", "Summerfield")
   - `+0..15` — `min(len(quote) // 15, 15)` — long quotes signal substance
   - `+15` if the quote contains any project/trade noun from a cross-trade specificity list (generator, panel, pavers, pergola, shingle, paint, remodel, emergency, etc.). The full list lives in `_SPECIFIC_SIGNALS` in `render.py`.
   - `-10` if the quote is under 100 characters AND matches any stock-praise
     phrase ("great job", "awesome", "highly recommend", "top notch", etc.).
4. Sorts descending by score and takes the top 3.

The effect: a named-role CEO review with a specific project detail beats a
short "awesome service!" review even from Google. Volt's Paul Mellini (CEO,
Nature Coast Bank) and Clif Spears (Comptroller, Prestige Auto) score highest;
stock-praise short reviews fall to the bottom.

**Why this rule and not something simpler.** A naive "top 3 by rating" filter
treats all 5-star reviews as equal; in practice prospect sites curate their
strongest quotes on-page while Google captures a broader range of tone. Volt
surfaced the specific failure case — 7 strong site testimonials were being
ignored in favor of 5 shorter Google reviews. The scoring rule keeps the
engine deterministic but picks the quotes that read as real.

---

## 3. Fallback behavior by band (§4 of the brief, concrete)

| Band | Required inputs | Fallback when missing | Engine function |
|---|---|---|---|
| Nav | business name, phone | renders with empty phone href | `render_nav()` |
| Hero | hero photo, §6.1 H1, phone, stats trio | renders with empty bg if no photo; surface warning | `render_hero()` |
| Anchor | city, hours, phone | hours → "By appointment"; cities → city_state fallback | `render_anchor_strip()` |
| Services | `services.list[]` with ≥4 entries, §6.5 taglines | renders with whatever it has; missing desc → empty `<p>` | `render_services()` |
| Pullquote | at least 1 qualifying quote | band drops (returns empty string) | `render_pullquote()` |
| Manifesto | §6.4 prose all 4 lines | band drops if any of line1_italic, line2, line3 missing | `render_manifesto()` |
| Testimonials | ≥3 Google reviews ≥ 4 stars with quote | band drops | `render_testimonials()` |
| Trust | ≥4 strong stats after trio | band drops (returns empty string) | `render_trust()` |
| Stats (dark) | `stats_trio` non-empty (Phase 3b) | band drops if trio empty; emits 3-tile if `resolve_distinguishing_stat` returns `None`, 4-tile when a signal fires | `render_stats_band()` |
| Promo callout | `profile.promotions.featuredPromo` non-null (Phase 3b) | band drops cleanly | `render_promo_callout()` |
| Before/after | `profile.photoLibrary.beforeAfterPairs[]` length ≥ 2 (Phase 3b) | band drops cleanly | `render_before_after()` |
| FAQ (homepage + services) | `profile.faq[]` non-empty (Phase 3e populates via `resolve_faq`) | band drops; same data both pages, page-distinct headers | `render_faq()` |
| Story | owner names | band drops | `render_story()` |
| Footer | always rendered | social links omitted individually; email line omitted; etc. | `render_footer()` |
| Mobile CTA bar | always rendered (Phase 3b chrome) | "Call" half drops if `contact.phone` null; quote button always ships; hidden on desktop via §14 CSS | `render_mobile_cta_bar()` |

## 4. Prose.json contract (composer-authored)

Next to every `fixtures/[slug]/profile.json` there must be a
`fixtures/[slug]/prose.json` authored by the executing Claude against the
audit-side voice contract (voiceMap.md + prose-rules.md + content-rules.md +
anti-slop-rules.md).

**Canonical v1.0 schema is page-keyed.** All prose lives under page-keyed sub-dicts (`prose.homepage.*`, `prose.about.*`, `prose.services.*`, `prose.testimonials.*`, `prose.contact.*`). The canonical shape is documented in `prose-rules.md` §6.6 + §6.1–§6.5 (homepage rules apply under `prose.homepage.*`); §4.A and §4.B below summarize specific slot groups.

**Schema confirmation (Deliverable 3 corrected, 2026-04-28).** Empirical render.py test confirmed `ctx["prose"]` is set to `prose.get("homepage") or {}` at the homepage band-renderer entry point. The flat shape documented at §4-LEGACY below is the v0.8-monolith-era schema, preserved here as a migration reference for prospects whose prose.json was authored against the v0.8 inline-generation path (Volthom, F1-F8 flagships). v1.0 prospects do NOT author flat shape.

### 4-LEGACY — v0.8-era flat homepage schema (migration reference only)

The shape below is **legacy / pre-v1.0**. v0.8 prospects have prose.json on disk in this shape. v1.0 prospects do NOT author this shape — they author per `prose-rules.md` §6.6 with all homepage slots wrapped under `prose.homepage.*`.

Migration of an existing v0.8 prose.json to v1.0 page-keyed shape is mechanical: wrap every top-level homepage slot under a `homepage` sub-key.

Shape (preserved verbatim from v0.8 documentation):

```jsonc
{
  "h1":                    { "line1": "", "line2_italic": "", "line2_accent": "" },
  "hero_kicker":           "",                               // short, e.g. "Welcome home."
  "hero_eyebrow":          "",                               // "{City State} · Est. {founderType}"
  "subhead":               { "text": "", "em_phrase": "" },  // §6.2: 18-26 words, one em dash allowed
  "services_headline":     { "text": "", "em_phrase": "", "accent_word": "" },
  "testimonials_headline": { "text": "", "em_phrase": "", "accent_word": "" },  // optional if testimonials band drops
  "story_headline":        { "text": "", "em_phrase": "", "accent_word": "" },  // optional if story band drops
  "manifesto":             { "headline": "", "body": "" },                              // §6.4 declarative brand-pillar register; eyebrow optional, defaults to "THE PROMISE"
  "service_taglines":      [ { "service_slug": "", "tagline": "" } ],
  "story_lede":            "",                               // optional if story band drops
  "story_paragraphs":      [ "", "" ],                       // optional
  "story_caption_label":   "",                               // optional
  "story_caption_value":   "",                               // optional
  "story_img_alt":         "",                               // optional
  "pullquote":             { "quote": "", "attribution_name": "", "attribution_context": "" },  // optional if pullquote band drops
  "footer_tag":             ""                                // optional; falls to tagline then default
}
```

If a band's data is missing from the profile (e.g. no owners → story drops),
the corresponding prose sections can be omitted from prose.json. The engine
checks on the profile side, not the prose side, for band inclusion.

### 4.A Phase 3b homepage band slots (optional)

`prose.homepage` and `prose.services` may carry these optional slots; defaults
fire when absent (see audit-side content-rules.md for voice rules; default
strings live alongside the `render_*` helpers in `scripts/render.py`):

```jsonc
{
  "homepage": {
    "stats_band":    { "eyebrow": "", "title": "" },
    "faq_header":    { "eyebrow": "", "title": "" },
    "promo_callout": { "eyebrow": "", "headline": "", "sub": "", "cta": "" }
  },
  "services": {
    "faq_header":    { "eyebrow": "", "title": "" }
  }
}
```

`promo_callout` is only authored when `profile.promotions.featuredPromo` is
non-null. The profile carries data + dates; prose carries voice. If both
are present, prose wins per slot. The two `faq_header` slots produce
distinct copy on homepage vs services so back-to-back reads don't see
identical headers.

### 4.B Inner-page prose slots (page-keyed)

Inner-page prose lives under page-keyed sub-dicts in `prose.json`. The slot vocabulary is documented in `prose-rules.md` §6.6 — that file is canonical for the inner-page slot inventory; this file is canonical for the boundary shape.

```jsonc
{
  "about":         { "eyebrow": "...", "headline": {...}, "subhead": "...", "lede": "...", "story_paragraphs": [...], "story_img_alt": "...", "story_caption_label": "...", "story_caption_value": "...", "creds_lede": "...", "where_we_work": "...", "pullquote": "..." },
  "services":      { "eyebrow": "...", "headline": {...}, "subhead": "...", "overview_eyebrow": "...", "overview_title": "...", "overview_subtitle": "...", "detail_section_eyebrow": "...", "detail_section_title": "...", "service_detail_descriptions": [{...}, ...], "faq_header": { "eyebrow": "...", "title": "..." }, "faq": [{...}] },
  "testimonials":  { "eyebrow": "...", "headline": {...}, "subhead": "...", "site_section_title": "...", "google_section_title": "...", "pullquote_quote": "...", "pullquote_attr": "..." },
  "contact":       { "eyebrow": "...", "headline": {...}, "subhead": "...", "form_intro": "...", "form_lede": "...", "info_heading": {...} }
}
```

Required vs optional per slot, register inheritance, and engine fallback behavior all live in `prose-rules.md` §6.6. This file does not duplicate that detail.

## 5. What Ron does when he brings back a profile path

Per-fixture, one-time:

1. Hand me the path: `/Users/ronkolb/grm-sites-prospects/[slug]/profile-draft.json`.
2. I verify the profile loads and every required field is present. If any
   required field is missing, I stop and name it — do not invent.
3. I read the audit-side voice contract (voiceMap.md + content-rules.md +
   anti-slop-rules.md) and author `prose.json` in one pass against the §4
   slot vocabulary above, reading the profile's captured facts for every
   slot. Temperature-analog: default voice for the H1/subhead/display/tile
   slots; stretch for the manifesto slot.
4. I run `render.py`, inspect the output in a browser, and report.

No shell command Ron needs to run. Bringing the path and the trade register
(he can note "Volt is a young family-run electrical shop" etc.) is enough.

## 6. What the composer refuses to do

- Invent owner names, founding years, or license numbers. If the profile's
  `credentials.licenseNumber` is null, the trust cell doesn't mention
  licensing. The hero headline doesn't claim "licensed and insured" just
  because the trade usually is.
- Re-rank the service order. The services render in the order the audit
  captured them. If the audit order is wrong, fix the audit, not the render.
- Use an Unsplash stock photo in the hero. The §2.1 rule says hero photo
  must be from tier 1-3 sources (Google / site / Instagram). If none qualify,
  surface a warning and use the best candidate with a note — do not silently
  substitute stock.
- Render past a §7 validation failure. Phone not matching in 4 places =
  stop, do not ship.

## 7. Known edge cases seen so far

- **Text-wordmark site with no logo file** (JSL / The Villages Landscaping):
  `brandPalette.logoCaptured = false`. Palette falls to JSL reference. Ron
  can override later; for v1 this renders fine.
- **Business-name ambiguity** (domain vs legal name differ, e.g. JSL):
  Resolve by Ron setting `businessName.primary` in the profile. The composer
  reads that field first.
- **Address typo in one source** (JSL had 13990 vs canonical 13900):
  Composer reads `contact.addressCanonical` first. The audit should
  surface a discrepancy note but the composer trusts the canonical.

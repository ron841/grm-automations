# phase-6-integration.md

How Phase 6 verification checks wire together. Authored in Stage II (f) with P6.1 as the anchor; extends naturally as P6.2/P6.3/P6.4 implementation work lands.

Authority: `COMPOSER_BRAIN.md §6` (Component A patch inventory — Phase 6 section); `composition-plan-schema.md §10` (check-by-check structural-vs-rendered classification); `typography.md §15` (the thirteen editorial verification checks that P6.2 enforces).

---

## 1. Phase 6 purpose

Phase 6 is Composer's automated quality gate. It runs after Phase 5 emits HTML/CSS/JS and before Phase 7 deploys to Vercel. No Phase 6 check has any editorial judgment — every check is a mechanical assertion against the emitted output. If a check fires a hard fail, the build halts and the operator sees the specific failure. If soft fails accumulate past the pattern-rule budget (brain §6: ≥3 soft fails across P6.1 + P6.2 = build-level hard fail), the build halts.

The Phase 6 suite is a set of independent checks, each with its own scope, output format, and integration surface. They share one aggregator that tallies hard-fail + soft-fail counts across the suite and makes the ship / no-ship call.

## 2. Check inventory

Four Phase 6 check categories per brain §6:

| Check | Scope | What it verifies | Status |
|---|---|---|---|
| **P6.1 rendered-content** | Initial-paint painted-pixel ratio per `<section>` | No section renders blank at initial paint (< 5% painted pixels = hard fail; < 15% desktop/tablet or < 20% mobile = soft fail). Catches opacity:0, display:none, unmounted reveal, or other render-time failures that pass a naive DOM check but leave the page visually blank. | Stage II (f) stub — implementation spec complete, execution filling pending |
| **P6.2 editorial suite** | Thirteen typography + layout checks per `typography.md §15` | Italic count, eyebrow proximity, eyebrow count, banned-section eyebrows, tabular numerals, body font-family discipline, data-voice scale ceiling, display-moment minimum, italic word selection, pull-quote count, stats watermark consistency, three-voice presence, mobile watermark treatment. Six structural (unfalsifiable via composition-plan), two partial (schema + rendered), five rendered-only. | Spec complete at `typography.md §15` + `composition-plan-schema.md §10`; implementation pending post-Stage-II |
| **P6.3 composition-plan completeness** | Every emitted `<section>` traces back to a `composition-plan.json` entry | No silent fallback sections. Unmapped sections = hard fail. | Spec complete at brain §6; implementation pending |
| **P6.4 schema-HTML consistency** | Phase 5.5-emitted JSON-LD schemas match `composition-plan.json` and `profile.json` content | FAQPage schema question/answer pairs match plan-declared FAQ entries; Service schema descriptions match `serviceDescriptions[].description`; ImageObject dimensions match `profile.photoInventory[].widthPx`/`heightPx`. Any mismatch = hard fail. | Spec complete at brain §6 + brain §7; implementation pending |

Plus existing SEO/GEO checks preserved from prospect-site (brain §6 P5.5.3): BLUF content, semantic HTML + internal linking, AI crawler access, llms.txt content, structured data validation, meta tag verification. These run alongside P6.1-P6.4.

## 3. P6.1 — rendered-content check (implementation spec)

Implementation: `scripts/rendered_content_check.py`. Status: Stage II (f) stub with full function signatures, docstrings, and logic skeletons; execution filling pending.

### 3.1 What P6.1 consumes

- **Target URL.** The deployed preview URL (post-Phase-7) or a `file://` URL (pre-deploy, pointing at the Phase 5 emission directory's `index.html`). Phase 6 runs P6.1 pre-deploy by default so a failing build halts before Vercel emission; running post-deploy against the live preview is a deeper smoke test used at Stage V gate verification.
- **Optional threshold overrides.** CLI args for `--hard-fail-threshold`, `--soft-fail-threshold`, `--mobile-soft-fail-threshold`, `--bg-tolerance`. Defaults match brain §6 P6.1.
- **Playwright environment.** Reused from `~/grm-automations/tools/grm-browser/` — the `grm_browser` Python package is already installed editable with Chromium provisioned via `playwright install chromium`. No additional Playwright install needed.

### 3.2 What P6.1 emits

Machine-readable JSON to stdout (Phase 6 aggregator consumes this); human-readable summary to stderr (Ron and Code see this in terminal output).

JSON shape per viewport:

```json
{
  "url": "https://luna-master-painting-grm.vercel.app/",
  "viewports": [
    {
      "viewport": { "width": 1440, "height": 900 },
      "sections": [
        {
          "sectionId": "services-section",
          "paintedPixelRatio": 0.42,
          "classification": "pass",
          "staticBlankFlag": false,
          "scrollDependentFlag": false,
          "computedBackgroundColor": "#faf7f2",
          "boundingBox": { "x": 0, "y": 820, "width": 1440, "height": 680 }
        }
      ],
      "pageLevel": {
        "hardFailCount": 0,
        "softFailCount": 1,
        "totalSections": 8,
        "overallClassification": "soft-fail-contribution"
      }
    }
  ]
}
```

Three viewports per run: 375×667 (mobile), 768×1024 (tablet), 1440×900 (desktop). Heights are device-natural defaults (iPhone SE, iPad portrait, 16:10 desktop) — override at invocation via `--viewports`.

### 3.3 How P6.1 integrates with the Phase 6 aggregator

The Phase 6 aggregator (deferred spec — authored when P6.2 implementation lands) runs each check in order, collects their JSON outputs, and decides the build-level ship / no-ship outcome.

Aggregation contract:

| P6.1 viewport classification | Aggregator treats as |
|---|---|
| `hard-fail` (any viewport — `hardFailCount >= 1`) | **Build-level hard fail.** Halt immediately; no other check matters. |
| `soft-fail-contribution` (any viewport — `softFailCount >= 1`, no hard fails) | Soft-fail count contributes to the brain §6 pattern rule: if total soft fails across P6.1 + P6.2 across all viewports ≥ 3, build-level hard fail. Otherwise, log as warnings and proceed. |
| `pass` (all viewports) | No contribution. |

Soft fails are per-section per-viewport. A single section that soft-fails at all three viewports counts as three soft fails against the pattern-rule budget — this is intentional per brain §6 framing (a section blank on every viewport is a different signal than a section blank on mobile only).

The aggregator consumes P6.1's JSON via stdout pipe or by reading the output file. Implementation choice deferred to aggregator authoring.

### 3.4 Where P6.1 sits in the Phase 6 run order

Recommended order (deferred aggregator authoring will lock this):

1. **P6.3 composition-plan completeness** — cheapest (DOM walk + plan-JSON key match). Runs first; fails the build fastest if Phase 5 emitted a section not in the plan.
2. **P6.2 structural checks (1, 3, 4, 10, 11, 12)** — the six structural checks from `composition-plan-schema.md §10` that are unfalsifiable against the plan. Also cheap (JSON-level assertions). Run second.
3. **P6.1 rendered-content** — Playwright launch is expensive (~3-8 seconds per viewport); running it after cheaper checks means a cheaper-check failure halts the build before P6.1 ever launches Playwright.
4. **P6.2 rendered checks (5, 6, 7, 13)** — computed-style checks that share the Playwright session with P6.1. Run alongside or immediately after P6.1 using the same Playwright context to avoid relaunch cost.
5. **P6.2 partial checks (8, 9)** — schema-level assertion already ran in step 2; rendered verification runs here using the P6.1/P6.2 Playwright session.
6. **P6.4 schema-HTML consistency** — reads both JSON artifacts and the emitted HTML. Runs independently of Playwright.
7. **Existing SEO/GEO checks** (BLUF, semantic HTML, AI crawler access, llms.txt, structured data validation, meta tags) — preserved from prospect-site, integrated last.

If any step fires a hard fail, the aggregator halts the build and emits the combined failure report to stderr.

### 3.5 Ron's interaction with P6.1 output

P6.1 runs at two integration points:

**(a) Pre-Phase-7-deploy gate.** Every Composer build runs Phase 6 (including P6.1) before Vercel emission. If P6.1 fires a hard fail, the build halts and Ron sees the specific section(s) + viewport(s) in the terminal summary. Ron either fixes the underlying cause (a Phase 4 composition-plan error producing an opacity:0 section, a Phase 5 emission bug) or overrides the gate via an operator flag (deferred — requires aggregator authoring).

**(b) Approval gate summary (pre-Phase-5-emit).** A future enhancement — Phase 4's approval gate shows P6.1 results from the LAST build against the same slug as a continuity signal ("last build passed all viewports; last build had 1 soft-fail on mobile at the stats section"). Deferred; not in Stage II (f) scope. When implemented, Phase 4 reads `~/grm-sites-prospects/[slug]/verification/p6.1-previous.json` if present.

**Non-interactive CLI usage for one-off runs:**

```bash
python scripts/rendered_content_check.py --url https://luna-master-painting-grm.vercel.app/
```

Exits 0 on pass or soft-fail-contribution, 1 on hard fail, 2 on execution error (Playwright launch failed, URL unreachable).

### 3.6 Failure-mode handling

**Playwright timeout.** 30-second navigation timeout matches grm-browser default. On timeout, P6.1 exits with code 2 and emits `{"error": "navigation_timeout", "url": "...", "viewport": {...}}` to stderr. No retries — Phase 6 does not recover; the operator investigates. (Retries would mask intermittent Vercel deploy latency or Playwright flakiness — better to fail visibly.)

**Missing section IDs.** Sections without a DOM `id` attribute get a synthetic `section[N]` identifier where N is document order. The synthetic identifier is stable across runs of the same emitted HTML (document order doesn't change) but NOT across builds (a Phase 4 composition change that inserts a new section shifts all downstream indices). P6.1 reports the synthetic ID in its JSON output so the operator can locate the section; best practice is for Phase 5 to emit `id` on every `<section>` so the synthetic identifier is never needed.

**Transparent backgrounds.** Sections with `background-color: transparent` or `rgba(..., 0)` need ancestor walking to find the effective background. `scripts/rendered_content_check.py` `query_sections()` documents the walk — up the DOM until a non-transparent background is found, fall back to page body background if none. If the effective background is still ambiguous (multi-layer transparents with image backgrounds), P6.1 flags the section with `computedBackgroundColor: "ambiguous"` and lowers confidence in the painted-pixel classification by marking the section as soft-fail-only regardless of ratio (never hard-fail on an ambiguous-background section).

**Gradient or image backgrounds.** When a section has `background-image` (gradient or raster), single-color pixel comparison is wrong — the "background" varies across the region. P6.1 detects this via `getComputedStyle(el).backgroundImage !== "none"`, sets `backgroundImageDetected: true` in the section's JSON, and uses a different classification: sample the screenshot region itself for its own dominant color via Pillow, treat pixels within tolerance of that dominant color as "background", pixels outside as "painted." Less precise than a known solid-color background but handles the editorial reality that hero sections often have gradient or image backgrounds.

**Scroll-dependent-blank vs static-blank.** Per brain §6 + `scripts/rendered_content_check.py` `probe_scroll_reveal()`: if a section is blank at initial paint, programmatically scroll to it, wait 800ms for reveal animations, re-capture, re-analyze. If post-scroll ratio clears hard-fail threshold, section is scroll-dependent (not a failure — reveal-on-scroll is intended behavior per `css-framework.md` scrollReveal primitive). If still below threshold, section is static-blank (real failure). Both flags are set in the JSON output so the aggregator can reason about the distinction.

**Computed-color edge case: CSS custom property resolution.** Sections whose `background-color` is set via a CSS custom property (`var(--page)`) resolve to the computed final color via `getComputedStyle(el).backgroundColor` — Playwright/Chromium returns the resolved RGB string, not the `var(...)` reference. No special handling needed.

### 3.7 Out-of-scope for P6.1

P6.1 does not check:
- Text content legibility (font size, color contrast, line-height). That's Phase 6 accessibility checks, separate from P6.1.
- Image loading failures. If an `<img>` inside a section fails to load, the section's pixel analysis naturally fails (broken-image icons don't match the computed background), so P6.1 catches it indirectly. A dedicated image-load check is out of scope.
- Above-the-fold vs below-the-fold distinctions. P6.1 samples every section at its actual document position — a section that's blank below the fold at initial paint is still a failure if it's also blank after scroll-reveal probing.

## 4. Cross-references

- `scripts/rendered_content_check.py` — P6.1 implementation (Stage II (f) stub).
- `COMPOSER_BRAIN.md §6` — authoritative Phase 6 check inventory and pattern rule.
- `COMPOSER_BRAIN.md §7` — SEO/GEO preservation contract that the existing SEO/GEO Phase 6 checks (six checks preserved from prospect-site) enforce.
- `composition-plan-schema.md §10` — structural-vs-rendered classification for the thirteen P6.2 editorial checks.
- `typography.md §15` — authoritative thirteen-check P6.2 editorial suite with hard/soft classification per check.
- `css-framework.md` — `scrollReveal` primitive and Motion Restraint rules that P6.1's scroll-dependent-blank branch depends on for reveal-animation timing.
- `~/grm-automations/tools/grm-browser/` — Playwright environment P6.1 reuses. See its README for the `capture`/`extract`/`probe`/`compare` primitives that this integration borrows from.

## 5. Version

v0.1 — Stage II (f) authored 2026-04-22. P6.1 section (§3) is implementation-spec-complete with execution filling pending. P6.2/P6.3/P6.4 sections (§2 table rows) are placeholders; extend this document as those implementations land.

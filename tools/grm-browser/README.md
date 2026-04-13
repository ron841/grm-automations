# grm-browser

Browser automation toolkit for GRM prospect-site verification. Renders pages with JavaScript via Playwright's bundled Chromium and exposes four CLI primitives that each print a single JSON object to stdout.

**Engine only.** Missions like `site-review` and `prospect-audit` are not in this repo. They will be built later as thin wrappers over these four primitives.

## Install

```bash
cd ~/grm-automations/tools/grm-browser
pip install -e .
playwright install chromium
```

Requires Python 3.9+ and Pillow (pulled automatically by pip).

## Primitives

### 1. capture -- screenshot a URL

```bash
python -m grm_browser capture https://example.com --viewport 375x812 --full-page
```

| Flag | Default | Description |
|---|---|---|
| `--viewport` | `375x812` | Width x height in pixels |
| `--full-page` | `true` | Capture entire scrollable page |
| `--no-full-page` | | Viewport-only capture |
| `--out PATH` | auto (cache dir) | Output file path |

Output:
```json
{"path": "/Users/.../abc123.png", "viewport": "375x812", "bytes": 84201, "timestamp": "2026-04-13T..."}
```

### 2. extract -- structured data from a rendered page

```bash
python -m grm_browser extract https://example.com --what og-tags
```

`--what` options:

| Type | What it returns |
|---|---|
| `og-tags` | `og:image`, `og:title`, `og:description`, `twitter:image`, `twitter:title`, `twitter:description`, `theme-color` |
| `nav-images` | All `<img>` inside `<header>` or `<nav>` with src, alt, width, height |
| `service-card-images` | All `<img>` inside elements with class matching service/card, with src, nearest heading, containing section |
| `dom` | Full post-render HTML string |

Output:
```json
{"what": "og-tags", "url": "...", "data": {"og:image": "...", "og:title": "..."}}
```

### 3. probe -- HTTP metadata via browser navigation

```bash
python -m grm_browser probe https://example.com
```

Output:
```json
{"status": 200, "final_url": "...", "redirects": [], "ttfb_ms": 245.3, "total_ms": 1802.1, "headers": {...}}
```

On 429 or 503: outputs `{"error": "rate_limited", "status": 429, "url": "..."}` and exits with code 2. No retries.

### 4. compare -- two values, three modes

```bash
# Color: hue distance in HSL space
python -m grm_browser compare '#fd040a' '#c32030' --mode color

# Image: mean pixel difference (Pillow), normalized 0-1
python -m grm_browser compare screenshot1.png screenshot2.png --mode image

# Text: difflib SequenceMatcher ratio (use @file to read from disk)
python -m grm_browser compare "hello world" "hello there" --mode text
python -m grm_browser compare @file1.txt @file2.txt --mode text
```

| Mode | `similar` threshold |
|---|---|
| `color` | hue delta <= 15 degrees |
| `image` | similarity >= 0.95 |
| `text` | (no `similar` field, just `ratio`) |

## Cache

Location: `~/grm-browser-cache/`

Screenshots and other artifacts are cached with deterministic filenames (SHA-256 of URL + viewport). Files older than 14 days are automatically pruned on every CLI invocation.

The cache lives outside the repo, so no `.gitignore` entry is needed for it.

## Politeness

- **Per-domain delay:** 2.0 seconds between requests to the same host
- **User-Agent:** `GRM-Browser/0.1` appended to a standard Chrome UA string
- **Navigation timeout:** 30 seconds
- **Rate limiting:** On HTTP 429 or 503, hard-exit with code 2. No retries.
- **robots.txt:** Not parsed in v1.

## Smoke test

```bash
python tests/smoke_test.py
```

Runs five checks against `https://tandf-electric-v07.vercel.app`:

1. `probe` returns status 200 with TTFB under 3 seconds
2. `capture` at 375x812 produces a PNG larger than 10KB
3. `extract --what og-tags` returns a non-empty `og:image`
4. `extract --what nav-images` returns at least one image
5. `compare --mode color` correctly identifies two similar reds

Prints `[PASS]` or `[FAIL]` per check. Exits 0 only if all five pass.

## Missions

Missions are thin wrappers over the four primitives. They live in `grm_browser/missions/`.

### site-review

Five-check verification of a deployed prospect site.

```bash
python -m grm_browser.missions.site_review <url> --out <dir> \
    [--brand-primary #hex] [--services-path /services]
```

| Arg | Required | Default | Description |
|---|---|---|---|
| `<url>` | yes | | Deployed homepage URL |
| `--out <dir>` | yes | | Output directory (created if missing) |
| `--brand-primary` | no | | Brand primary hex for OG color check |
| `--services-path` | no | `/services` | Services page path relative to base URL |

**The five checks:**

| # | Check ID | Severity | What it does |
|---|---|---|---|
| 1 | `logo-is-image` | soft | Verifies nav has an `<img>` logo (Tier 1) or OG/favicon fallback (Tier 2); warns on text-only logo |
| 2 | `og-image-brand-color` | hard | Downloads og:image, extracts dominant non-neutral color, compares to brand primary via hue distance (<=15 deg) |
| 3 | `featured-service-image-rotation` | hard | Compares service card images between homepage and services page; fails if a featured card image appears on both |
| 4 | `wow-gap-structural` | hard | Parses DOM for five structural elements: hero H1, stats counter, testimonial, services grid (>=3 items), CTA with tel:/contact |
| 5 | `mobile-render-baseline` | soft | Captures mobile screenshot (375x812), verifies PNG > 10KB |

**Output files** (in `--out` directory):

- `site-review.json` -- structured report with all check results and summary counts
- `site-review.md` -- human-readable markdown with status badges and mobile screenshot as base64 data URI

**Exit codes:**

- `0` -- all checks pass, or mix of pass + warn + skip
- `1` -- any hard-severity check failed
- `2` -- mission-level error (URL unreachable, primitive crashed)

**Smoke test:**

```bash
python tests/smoke_site_review.py
```

Runs site-review against `https://tandf-electric-v07.vercel.app` and validates output structure (JSON exists, MD exists, 5 checks present, exit code not 2). Passes regardless of individual check outcomes.

**Phase 6 skill integration is deferred.** This mission runs as standalone observation for now. Wiring it into the prospect-site skill's Phase 6 verification pipeline is a future session.

## What is NOT in this repo

- `prospect-audit` mission (pre-build site analysis)
- Any prospect-site skill integration
- robots.txt parsing
- Real-Chrome (non-bundled) escape hatch

These will be built in future sessions as thin wrappers over the four primitives above.

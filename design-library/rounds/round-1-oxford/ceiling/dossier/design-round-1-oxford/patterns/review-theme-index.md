# Review theme index (NLP-derived)

`review-theme-index`

| Field | Value |
|---|---|
| Scale | **Mixed** |
| Mobile | ✓ Ports cleanly |
| Voice assignment | Closing Table |
| Pages used | Reviews |

## Purpose

'47 reviews mention on time · 34 mention straight answer' — NLP-derived theme index. Once pipeline is built, free for all clients.

## Rationale

'47 reviews mention on time / 34 mention straight answer.' Derived by Claude NLP pass at build time. Free for everyone once pipeline is built.

## Replaces (from F3 / F5 / F6 flagship)

No equivalent on F3/F5/F6.

## Structural outline

```html
<div class="theme-index">
  <div class="theme">
    <div class="n">47</div>
    <div class="l">reviews mention</div>
    <div class="t">on time</div>
  </div>
  …
</div>
```

## Design tokens used

--f-display 500 for numerals (3rem), --f-display italic for theme words, --f-mono for 'reviews mention' label

## Behavior notes

Static, prerendered.

## Responsive notes

3-column grid stacks on mobile.

## Constraints

Requires build-time NLP pipeline. If pipeline unavailable, suppress section.

## Code conversion notes

Build step: run Claude NLP pass over client's review corpus. Extract top 3 themes with counts. Cache results for 30 days. Suppress section if count < 10 reviews total.

## Scale notes · path from bespoke to systemizable

**MIXED · FIX: Build-time pipeline.** One-time Claude NLP ingest of every client's reviews at build. Extracts top 3 themes + counts. Once built, systemizable across all 50. Investment = ~1 day of Claude Code work on the ingest pipeline.

## Visual reference

- Desktop: `visuals/review-theme-index-desktop.png`
- Mobile: `visuals/review-theme-index-mobile.png`

---

_Round 1 · Oxford Lawn · GRM Design_

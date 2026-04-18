# Masonry review wall with rhythm

`review-masonry-rhythm`

| Field | Value |
|---|---|
| Scale | **Systemizable** |
| Mobile | ✓ Ports cleanly |
| Voice assignment | — (chrome, no copy) |
| Pages used | Home peek, Reviews |

## Purpose

Column-flow masonry review wall with 3-pattern rhythm (normal / feature / dark). Handles any review count. Pulls live from Google Places API.

## Rationale

Column-flow masonry with 3-pattern rhythm (normal / feature / dark). Pulls directly from Google Places API. Handles any review count.

## Replaces (from F3 / F5 / F6 flagship)

F3/F5/F6 use fixed 3-up or 6-up card grids that feel thin past 6 reviews.

## Structural outline

```html
<div class="review-masonry" data-column-count="3">
  <article class="review">…</article>
  <article class="review feature">…</article>
  <article class="review dark">…</article>
  <article class="review">…</article>
  …
</div>
```

## Design tokens used

CSS column-count 3/2/1. Feature variant: --cream-2 bg + serif pull-quote. Dark variant: --ink bg + --cream text. --f-display italic for review body. --f-mono for author+date line.

## Behavior notes

Pattern rhythm is computed at render: every 3rd card = feature, every 5th = dark (configurable). break-inside: avoid for cards.

## Responsive notes

Column count drops 3 → 2 → 1 at 1100px / 700px breakpoints.

## Constraints

Live Places API feed. Rate-limit + cache at build. Handle 5-star filter. Respect max-reviews cap per build (default 30).

## Code conversion notes

Build step fetches reviews, sorts by date desc, applies rhythm pattern. Review model: `{author, date, rating, text}`. No client-side API call — all reviews prerendered.

## Visual reference

- Desktop: `visuals/review-masonry-rhythm-desktop.png`
- Mobile: `visuals/review-masonry-rhythm-mobile.png`

---

_Round 1 · Oxford Lawn · GRM Design_

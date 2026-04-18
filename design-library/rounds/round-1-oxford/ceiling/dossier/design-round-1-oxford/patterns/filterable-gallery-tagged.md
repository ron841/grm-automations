# Filterable gallery with trade tags

`filterable-gallery-tagged`

| Field | Value |
|---|---|
| Scale | **Systemizable** |
| Mobile | ✓ Ports cleanly |
| Voice assignment | — (chrome, no copy) |
| Pages used | Gallery |

## Purpose

Masonry grid with location + process-stage filters. Tag schema swaps per trade.

## Rationale

Masonry grid with location + process-stage filters. Tag schema swaps per trade.

## Replaces (from F3 / F5 / F6 flagship)

F3's plain grid gallery; F5's unfiltered tile wall.

## Structural outline

```html
<section class="gallery">
  <nav class="filters">
    <button data-filter="all" class="active">All</button>
    <button data-filter="villages">The Villages</button>
    …
  </nav>
  <div class="masonry">
    <figure data-tags="villages dethatch"><img …/><figcaption>…</figcaption></figure>
    …
  </div>
</section>
```

## Design tokens used

--lawn-500 (active filter bg), --rule (filter borders), standard masonry column-count

## Behavior notes

Click filter → show/hide figures via [data-tags] match. Multi-filter AND-logic. URL hash persists filters for sharing.

## Responsive notes

Filter row: horizontal-scroll chip bar on mobile. Grid collapses 12-col → 6-col → 3-col.

## Constraints

Tag schema per trade-config. Photos need consistent aspect ratios per column. Captions are optional.

## Code conversion notes

Tag schema: `{filters: [{id, label, group}]}`. Groups can be 'town', 'stage', 'grass-type'. Multi-select within a group is OR; across groups is AND.

## Visual reference

- Desktop: `visuals/filterable-gallery-tagged-desktop.png`
- Mobile: `visuals/filterable-gallery-tagged-mobile.png`

---

_Round 1 · Oxford Lawn · GRM Design_

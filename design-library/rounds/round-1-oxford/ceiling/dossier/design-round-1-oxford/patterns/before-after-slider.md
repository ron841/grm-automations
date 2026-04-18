# Before/after compare slider

`before-after-slider`

| Field | Value |
|---|---|
| Scale | **Systemizable** |
| Mobile | ✓ Ports cleanly |
| Voice assignment | — (chrome, no copy) |
| Pages used | Gallery |

## Purpose

Drag-handle split before/after photo compare. Strong fit for visible-transformation trades; weak for HVAC/plumbing.

## Rationale

Drag-handle split. Strong for lawn rehab, pool resurfacing, electrical panel, landscape installs. Weak for HVAC/plumbing — flag as trade-conditional.

## Replaces (from F3 / F5 / F6 flagship)

No equivalent on F3/F5/F6.

## Structural outline

```html
<div class="before-after" data-handle="50">
  <img class="after" src="…" alt="After: reseeded lawn, 8 weeks later" />
  <div class="before-wrap"><img class="before" src="…" alt="Before: patchy Zoysia with thatch" /></div>
  <button class="handle" aria-label="Drag to compare" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100">…</button>
</div>
```

## Design tokens used

--lawn-500 (handle), --ink (handle border). Handle: 48px touch target.

## Behavior notes

Mouse drag or touch drag on handle moves the clip-path on .before-wrap. Keyboard: arrow keys move handle by 5% per press.

## Responsive notes

Touch events already wired. Handle grows to 48px on touch. No layout change.

## Constraints

Both images must be same dimensions and same framing. Photo pairing is a per-client content gate. WCAG: alt text on both images required; aria-valuenow on handle.

## Code conversion notes

Component hydrates on mount. Before images can be lazy-loaded (below fold). Handle position can persist in URL param for sharing (?before=30).

## Visual reference

- Desktop: `visuals/before-after-slider-desktop.png`
- Mobile: `visuals/before-after-slider-mobile.png`

---

_Round 1 · Oxford Lawn · GRM Design_

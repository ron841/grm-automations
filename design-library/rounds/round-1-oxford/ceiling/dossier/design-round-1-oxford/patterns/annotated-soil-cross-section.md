# Annotated soil cross-section

`annotated-soil-cross-section`

| Field | Value |
|---|---|
| Scale | **Bespoke** |
| Mobile | ⚠ Mobile-gated — see Responsive notes |
| Voice assignment | Closing Table |
| Pages used | Process |

## Purpose

Tall strata panel with labeled callouts showing where each step of the process acts. For Oxford: 'Step 1 acts here' → thatch layer, etc.

## Rationale

Tall strata panel + 'step 1 acts here / step 2 acts here' callouts. Labeled process diagram.

## Replaces (from F3 / F5 / F6 flagship)

F3/F5/F6 describe process in prose only.

## Structural outline

```html
<figure class="cross-section">
  <div class="strata-tall">
    <div class="layer l-thatch">Thatch</div>
    …
  </div>
  <aside class="callouts">
    <div class="callout" data-target="thatch"><b>Step 01</b>Dethatch acts here</div>
    …
  </aside>
</figure>
```

## Design tokens used

Same as soil-strata-hero. Callout arrows: --ink, --lawn-700. --f-mono for callout eyebrows.

## Behavior notes

Static. Callout arrows connect to strata layers visually (via SVG or CSS ::after).

## Responsive notes

MOBILE-GATED. The 'acts here →' arrow metaphor breaks when diagram stacks. Mobile variant: callouts stack under each band with inline 'step N' tag (no arrows).

## Constraints

Pattern exists for trades with literal cross-sections. Without a commissioned illustration pack (see Round 1 path), only Oxford ships this.

## Code conversion notes

Callouts model: `{target: 'thatch', step: '01', label: 'Dethatch acts here'}[]`. Arrows computed at render based on target layer's DOM position.

## Scale notes · path from bespoke to systemizable

**BESPOKE · FIX: Commissioned illustration pack.** Invest in ~15 annotated process diagrams (lawn soil, pool water column, septic drain field, HVAC ducting, electrical panel, plumbing riser, etc). Shared illustrator, shared style. One diagram per trade. Moves bespoke → systemizable for ~25 of 50 trades.

## Visual reference

- Desktop: `visuals/annotated-soil-cross-section-desktop.png`
- Mobile: (see compact mobile variant in design project)

---

_Round 1 · Oxford Lawn · GRM Design_

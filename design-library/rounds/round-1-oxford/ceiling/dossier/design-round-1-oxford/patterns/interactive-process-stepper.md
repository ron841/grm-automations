# Interactive process stepper

`interactive-process-stepper`

| Field | Value |
|---|---|
| Scale | **Systemizable** |
| Mobile | ⚠ Mobile-gated — see Responsive notes |
| Voice assignment | Closing Table |
| Pages used | Process |

## Purpose

Sticky left nav + animated right panel for sequenced trade processes. Lawn: dethatch → aerate → dress. HVAC: survey → duct → install → commission. Pool: drain → repair → resurface → fill.

## Rationale

Sticky left nav + animated right panel. Works for any sequenced trade: HVAC install, septic, pool remodel, electrical service upgrade.

## Replaces (from F3 / F5 / F6 flagship)

No equivalent on F3/F5/F6. They list services as siblings; we sequence.

## Structural outline

```html
<div class="stepper">
  <nav class="steps" aria-label="Process steps">
    <button data-step="0" class="active">01 · Dethatch</button>
    <button data-step="1">02 · Aerate</button>
    …
  </nav>
  <div class="panels">
    <section data-panel="0" class="active">…</section>
    …
  </div>
</div>
```

## Design tokens used

--ink (active nav button bg), --cream (active nav text), --lawn-500 (accent), --rule (inactive nav borders). Panel transitions: opacity 240ms ease.

## Behavior notes

Click a nav button → switch active panel with crossfade. Scroll nav is position:sticky top:120px. Keyboard: arrow keys navigate, Enter activates. No auto-advance.

## Responsive notes

Desktop: 2-col sticky nav + panel. MOBILE-GATED — the sticky-left pattern doesn't port. Mobile variant: horizontal chip bar + scroll-snap panels. Build as separate component.

## Constraints

WCAG AA: nav buttons must have aria-selected, panels must have role='tabpanel' and aria-labelledby, focus order: chips → active panel content. Respect prefers-reduced-motion (instant switch, no fade).

## Code conversion notes

Steps model: `{id, num, title, body, media?: {type, src}}`. Mobile variant is a different component; build script picks which to render based on viewport class. Active-step persists in URL hash for deep linking (#step-2).

## Visual reference

- Desktop: `visuals/interactive-process-stepper-desktop.png`
- Mobile: (see compact mobile variant in design project)

---

_Round 1 · Oxford Lawn · GRM Design_

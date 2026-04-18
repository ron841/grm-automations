# 'Volume 18, Issue 1' editorial chrome

`magazine-issue-chrome`

| Field | Value |
|---|---|
| Scale | **Bespoke** |
| Mobile | ✓ Ports cleanly |
| Voice assignment | — (chrome, no copy) |
| Pages used | Hero kicker, rails |

## Purpose

'Volume 18, Issue 1' magazine-issue metadata in nav zone. Editorial flourish; Premium-tier only.

## Rationale

Magazine-issue metadata in the nav zone. Playful, editorial. Works for specialists with a story. May read gimmicky for storm-response trades.

## Replaces (from F3 / F5 / F6 flagship)

No equivalent on F3/F5/F6.

## Structural outline

```html
<div class="issue-kicker">
  <span>VOL <b>18</b></span>
  <span>ISSUE <b>01</b></span>
  <span class="hide-mobile">SPRING 2026</span>
</div>
```

## Design tokens used

--f-mono 0.68rem 0.14em ls uppercase, --soil-2 color, --rule bottom border

## Behavior notes

Static. Last piece drops on mobile.

## Responsive notes

Kicker row wraps. Third span drops at <600px via .hide-mobile class.

## Constraints

Premium-tier only. Default off. Volume number derives from years-in-business. Issue number increments each build (stored in client state).

## Code conversion notes

Guard: `{tier: 'premium'} && render()`. Volume = current_year - founded_year. Issue tracked in build manifest.

## Scale notes · path from bespoke to systemizable

**BESPOKE · FIX: Paid-tier-only feature.** Ship on Premium-tier builds only. Ties to editorial-specialist typographic class. Paid-tier becomes the natural home for patterns that stretch past systemizable — gives us a price point for the ceiling.

## Visual reference

- Desktop: `visuals/magazine-issue-chrome-desktop.png`
- Mobile: `visuals/magazine-issue-chrome-mobile.png`

---

_Round 1 · Oxford Lawn · GRM Design_

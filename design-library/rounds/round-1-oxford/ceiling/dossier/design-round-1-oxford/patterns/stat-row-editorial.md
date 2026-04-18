# Four-number editorial stat row

`stat-row-editorial`

| Field | Value |
|---|---|
| Scale | **Systemizable** |
| Mobile | ✓ Ports cleanly |
| Voice assignment | — (chrome, no copy) |
| Pages used | Home hero, Reviews, About |

## Purpose

Four-number display-serif stat row. Replaces the generic 'about us' strip. Numerals are falsifiable data points pulled from GMB and config.

## Rationale

Display-serif numerals with mono labels. Years / reviews / rating / area. Replaces generic 'about us' blurb with falsifiable claims.

## Replaces (from F3 / F5 / F6 flagship)

F6 has a stat strip but uses sans numerals with no typographic weight. Falls into SaaS convention.

## Structural outline

```html
<div class="stats">
  <div class="stat"><div class="n">18</div><div class="l">Years serving</div></div>
  <div class="stat"><div class="n">132</div><div class="l">Verified reviews</div></div>
  …
</div>
```

## Design tokens used

--f-display (numerals, 500 weight, -0.03em letter-spacing), --f-mono (labels, 0.14em letter-spacing, uppercase), --step-4 (numeral size), --soil-2 (label color)

## Behavior notes

Static. Numerals clamp-scale with viewport. No animation.

## Responsive notes

Desktop: 4 columns. Tablet: 4 columns, numerals shrink. Mobile <420px: 2x2 grid.

## Constraints

Numerals must be real counts from GMB API at build time. No rounded-up marketing figures. If a stat is unavailable (new client, 0 reviews), drop that column rather than fake it.

## Code conversion notes

Build step fetches GMB review count + rating live. Years-in-business comes from site config. Service area count is computed from service-area JSON length.

## Visual reference

- Desktop: `visuals/stat-row-editorial-desktop.png`
- Mobile: `visuals/stat-row-editorial-mobile.png`

---

_Round 1 · Oxford Lawn · GRM Design_

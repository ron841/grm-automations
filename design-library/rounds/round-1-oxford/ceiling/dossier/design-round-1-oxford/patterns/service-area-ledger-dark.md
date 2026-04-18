# Service-area ledger table (dark)

`service-area-ledger-dark`

| Field | Value |
|---|---|
| Scale | **Systemizable** |
| Mobile | ✓ Ports cleanly |
| Voice assignment | Saturday Morning |
| Pages used | Home |

## Purpose

Dark editorial service-area table. Columns vary per trade. For Oxford: town / county / typical grass type / drive time.

## Rationale

Editorial table on stone background. Columns are trade-config: lawn = town/county/grass/drive time. Plumber = town/county/response/emergency hours.

## Replaces (from F3 / F5 / F6 flagship)

F3/F5/F6 use pill/chip clouds of service areas. Visually flat, no hierarchy.

## Structural outline

```html
<table class="data dark">
  <thead><tr><th>Town</th><th>County</th><th>Typical grass</th><th>Drive time</th></tr></thead>
  <tbody>
    <tr><td>The Villages</td><td>Sumter</td><td>Zoysia / Bahia</td><td>20 min</td></tr>
    …
  </tbody>
</table>
```

## Design tokens used

--ink (bg), --cream (text), --f-mono (all cells), --rule at rgba(cream,0.1) for row dividers. Header row: --lawn-500 color.

## Behavior notes

Static table. No sort, no filter — ordered by drive time.

## Responsive notes

Below 640px: table becomes a stack of cards. Each <tr> becomes a .m-ledger-row with title + data-row of labeled pairs.

## Constraints

Rows come from service-area JSON. Columns from trade-config. Drive times from Google Maps API at build time (not a dynamic fetch). No 'we serve the surrounding area' — named towns only.

## Code conversion notes

Trade config defines column schema: `{columns: [{key:'town', label:'Town'}, ...]}`. Service-area JSON provides row data per client. Build script enriches rows with drive times from Maps API, cached.

## Visual reference

- Desktop: `visuals/service-area-ledger-dark-desktop.png`
- Mobile: `visuals/service-area-ledger-dark-mobile.png`

---

_Round 1 · Oxford Lawn · GRM Design_

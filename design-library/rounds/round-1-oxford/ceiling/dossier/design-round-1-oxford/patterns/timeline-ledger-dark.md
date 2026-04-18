# Editorial timeline ledger (dark)

`timeline-ledger-dark`

| Field | Value |
|---|---|
| Scale | **Systemizable** |
| Mobile | ✓ Ports cleanly |
| Voice assignment | Closing Table |
| Pages used | About |

## Purpose

Editorial timeline ledger on dark — year / event / why-it-mattered. Every contractor has a story; this is where it lives.

## Rationale

Year / event / why-it-mattered table on dark. Every contractor has a story; flagships don't tell one.

## Replaces (from F3 / F5 / F6 flagship)

F3/F6 have no timeline. F5 has a prose paragraph that mentions dates.

## Structural outline

```html
<table class="data timeline dark">
  <thead><tr><th>Year</th><th>Event</th><th>Why it mattered</th></tr></thead>
  <tbody>
    <tr><td>2008</td><td>Oxford Lawn opens</td><td>Tom leaves a chemical-lawn job…</td></tr>
    …
  </tbody>
</table>
```

## Design tokens used

--ink (bg), --cream (text), --f-mono for year column (0.14em ls), --f-display italic for event titles

## Behavior notes

Static table. Optional row-hover dim.

## Responsive notes

Desktop: 3-col. Mobile: each row becomes a card with year as eyebrow, event as title, why-it-mattered as body.

## Constraints

Needs 4–8 entries. Fewer than 4 reads thin; more than 8 needs collapsing. Content comes from onboarding voice interview.

## Code conversion notes

Timeline model: `{year, event, why}[]`. Pulled from client-data.json. If array has <4 entries, section is hidden at build time.

## Visual reference

- Desktop: `visuals/timeline-ledger-dark-desktop.png`
- Mobile: `visuals/timeline-ledger-dark-mobile.png`

---

_Round 1 · Oxford Lawn · GRM Design_

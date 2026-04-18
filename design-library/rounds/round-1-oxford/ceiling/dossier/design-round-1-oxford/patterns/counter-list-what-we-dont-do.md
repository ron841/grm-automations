# Counter-list · what we don't do

`counter-list-what-we-dont-do`

| Field | Value |
|---|---|
| Scale | **Systemizable** |
| Mobile | ✓ Ports cleanly |
| Voice assignment | Closing Table |
| Pages used | Services |

## Purpose

Dark panel listing declined services. Reframes refusal as positioning. Differentiates specialists from broad offerings.

## Rationale

Dark panel listing declined services. Reframes refusal as positioning. Differentiates specialists from broad offerings.

## Replaces (from F3 / F5 / F6 flagship)

No equivalent on F3/F5/F6. Standard contractor site lists everything plus 'and more'.

## Structural outline

```html
<section class="dont-do dark">
  <div class="eyebrow">What we don't do</div>
  <h2>Things we'll point you elsewhere for.</h2>
  <table class="dont-table">
    <tr><td class="what">Weekly mowing</td><td class="why">We're project-based…</td></tr>
    …
  </table>
</section>
```

## Design tokens used

--ink (bg), --cream (text), --lawn-500 (eyebrow), --f-display italic for 'what' column

## Behavior notes

Static.

## Responsive notes

Desktop: two-column split (heading / table). Mobile: heading stacks above table. Table rows always two-column.

## Constraints

Content gate — requires voice-interview pass. If client can't articulate 3+ declined services cleanly, skip this section (handled at build).

## Code conversion notes

Section is optional per-client. `client.dontDoList` array with 3+ entries triggers render. Below threshold, section output suppressed.

## Visual reference

- Desktop: `visuals/counter-list-what-we-dont-do-desktop.png`
- Mobile: `visuals/counter-list-what-we-dont-do-mobile.png`

---

_Round 1 · Oxford Lawn · GRM Design_

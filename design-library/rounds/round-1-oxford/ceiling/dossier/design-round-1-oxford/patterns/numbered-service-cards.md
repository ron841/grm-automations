# Numbered horizontal service cards

`numbered-service-cards`

| Field | Value |
|---|---|
| Scale | **Systemizable** |
| Mobile | ✓ Ports cleanly |
| Voice assignment | Closing Table |
| Pages used | Services |

## Purpose

Horizontal service cards with large numeral, title, description, right-column meta. Default for process-based trades; degrades gracefully (un-numbered) for broader-offering trades.

## Rationale

Large numeral block + title + description + right-column meta. Process default, degrades to un-numbered for broad-offering trades.

## Replaces (from F3 / F5 / F6 flagship)

F5's 19-service tile wall. Loses hierarchy immediately past 6 cards.

## Structural outline

```html
<article class="service-card">
  <div class="num">01</div>
  <div class="body">
    <h3>Dethatch</h3>
    <p>Strip the dead mat…</p>
  </div>
  <aside class="meta"><b>Equipment</b>PowerRake 1400…</aside>
</article>
```

## Design tokens used

--f-display 500 -0.03em letter-spacing (numerals, 60px desktop / 44px mobile), --lawn-700 (numeral color), --rule (card border), --f-mono for meta labels

## Behavior notes

Optional hover: numeral color shifts ink → lawn-700. No JS required.

## Responsive notes

Desktop: 3-col (num / body / meta). Mobile: meta column drops below body; numeral shrinks 60px → 44px.

## Constraints

Step count is trade-variable. Card count rec: 3–6 max before reaching for pattern 05b (list-view degrade). Numerals only when the services are a sequence; otherwise render without .num.

## Code conversion notes

Card model: `{num?: string, title: string, body: string, meta?: [{label, value}]}`. Omitting `num` renders un-numbered variant. Meta array is optional.

## Visual reference

- Desktop: `visuals/numbered-service-cards-desktop.png`
- Mobile: `visuals/numbered-service-cards-mobile.png`

---

_Round 1 · Oxford Lawn · GRM Design_

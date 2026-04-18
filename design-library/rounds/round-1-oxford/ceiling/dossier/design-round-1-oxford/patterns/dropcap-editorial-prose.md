# Dropcap + editorial prose

`dropcap-editorial-prose`

| Field | Value |
|---|---|
| Scale | **Systemizable** |
| Mobile | ✓ Ports cleanly |
| Voice assignment | varies |
| Pages used | Home thesis, About |

## Purpose

Italic serif dropcap, 68ch measure, editorial prose class. Turns contractor copy into feature-reading.

## Rationale

Italic serif dropcap, 68ch measure, prose class. Turns contractor copy into feature-reading, not form fields.

## Replaces (from F3 / F5 / F6 flagship)

F3/F5/F6 use standard paragraph blocks at 80+ ch.

## Structural outline

```html
<div class="prose">
  <p><span class="dropcap">Y</span>ou can mow a dying lawn until the mower breaks…</p>
  <p>…</p>
</div>
```

## Design tokens used

--f-display italic, dropcap size 4.5em desktop / 2.8em mobile, line-height 0.85, --lawn-700 color, float:left, margin-right:0.15em

## Behavior notes

CSS-only.

## Responsive notes

Dropcap scales to 2.8em on mobile. Measure collapses to viewport width.

## Constraints

Needs a text block of 3+ paragraphs or the dropcap reads orphaned. Don't use on marketing copy — only editorial prose.

## Code conversion notes

Apply via class `.prose` on container. Dropcap applied via `:first-letter` pseudo or explicit <span class='dropcap'>. Prefer explicit span for control.

## Visual reference

- Desktop: `visuals/dropcap-editorial-prose-desktop.png`
- Mobile: `visuals/dropcap-editorial-prose-mobile.png`

---

_Round 1 · Oxford Lawn · GRM Design_

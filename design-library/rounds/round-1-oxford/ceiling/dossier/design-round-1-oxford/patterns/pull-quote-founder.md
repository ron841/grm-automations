# Pull-quote with founder attribution

`pull-quote-founder`

| Field | Value |
|---|---|
| Scale | **Bespoke** |
| Mobile | ✓ Ports cleanly |
| Voice assignment | Front Porch |
| Pages used | About |

## Purpose

Serif-italic pull quote with lawn-green left bar and attribution. Requires a founder who speaks like their work.

## Rationale

Serif-italic pull quote with lawn-green left bar. Requires a founder who talks like their work.

## Replaces (from F3 / F5 / F6 flagship)

F3/F5/F6 have generic 'About Us' narrative without attributed voice.

## Structural outline

```html
<blockquote class="pull-quote">
  <p>People call because the grass looks bad. Most of the time, the grass is a symptom.</p>
  <footer><b>Tom O'Brien</b>Founder, Oxford Lawn</footer>
</blockquote>
```

## Design tokens used

--lawn-700 (left bar 4px), --f-display italic 1.6rem, --f-mono for attribution line, padding-left 1.5rem, border-left 4px solid --lawn-700

## Behavior notes

Static.

## Responsive notes

Left bar holds. Quote reflows. No layout change.

## Constraints

Content gate only. Requires voice interview that produces 3+ quotable lines. If not available, skip.

## Code conversion notes

Content source: voice-interview transcript. Claude-extract quote-worthy lines at onboarding. Pattern opt-in per client.

## Scale notes · path from bespoke to systemizable

**BESPOKE · FIX: Voice-interview onboarding gate.** Build a 10-minute founder voice-interview protocol (Claude-led, transcribed). If interview yields 3+ quotable lines, enable this pattern. If not, section is skipped. Pattern becomes 'systemizable when content exists' — systemizable for ~60% of clients.

## Visual reference

- Desktop: `visuals/pull-quote-founder-desktop.png`
- Mobile: `visuals/pull-quote-founder-mobile.png`

---

_Round 1 · Oxford Lawn · GRM Design_

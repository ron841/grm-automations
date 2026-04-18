# Voice-tagged sections (eyebrow system)

`voice-tagged-sections`

| Field | Value |
|---|---|
| Scale | **Systemizable** |
| Mobile | ✓ Ports cleanly |
| Voice assignment | varies per section |
| Pages used | Sitewide |

## Purpose

Every section eyebrow declares its voice. Enforces one-section-one-voice discipline from GRM_VOICE_SKILL.md.

## Rationale

Every section eyebrow declares its voice. Enforces 'one section, one voice' and trains the reader to feel the shift.

## Replaces (from F3 / F5 / F6 flagship)

F3/F5/F6 use generic all-caps eyebrows with topical labels only. No voice signaling.

## Structural outline

```html
<section>
  <div class="eyebrow">Thesis · voice: The Closing Table</div>
  <h2 class="h-display">…</h2>
  …
</section>
```

## Design tokens used

--f-mono, 0.72rem, 0.18em letter-spacing, uppercase, --soil-2 color. Voice dot (optional): --lawn-700 / --front-porch / --saturday colors.

## Behavior notes

Static. Optional colored dot prefix per voice for visual signaling.

## Responsive notes

Eyebrow steps down one size at <600px. Voice name may wrap to second line.

## Constraints

Voice assignment is data, not decoration. Pulled from voices.json per section. Must match the copy actually written.

## Code conversion notes

Each page's content model has a `sections: [{id, voice, eyebrow, body}]` shape. Voice-to-color mapping is shared CSS vars. Voice-skill validation runs at build — if a section's tone doesn't match its declared voice (Claude check), build warns.

## Visual reference

- Desktop: `visuals/voice-tagged-sections-desktop.png`
- Mobile: `visuals/voice-tagged-sections-mobile.png`

---

_Round 1 · Oxford Lawn · GRM Design_

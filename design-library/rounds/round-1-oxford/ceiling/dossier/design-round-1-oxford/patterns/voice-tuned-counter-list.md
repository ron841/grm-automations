# Voice-tuned 'what we don't do' content

`voice-tuned-counter-list`

| Field | Value |
|---|---|
| Scale | **Mixed** |
| Mobile | ✓ Ports cleanly |
| Voice assignment | Closing Table |
| Pages used | Services |

## Purpose

The content side of pattern 09. Voice-tuned 'what we don't do' entries. Content pipeline, not a separate component.

## Rationale

Section is systemizable (see pattern 09). Content requires a client who can articulate what they decline and why.

## Replaces (from F3 / F5 / F6 flagship)

See pattern 09.

## Structural outline

```html
See pattern 09 (counter-list-what-we-dont-do).
```

## Design tokens used

See pattern 09.

## Behavior notes

See pattern 09.

## Responsive notes

See pattern 09.

## Constraints

Content gate via voice interview. Claude scores each declination on specificity — generic 'we don't do shoddy work' rejected; 'we don't do weekly mowing' accepted.

## Code conversion notes

Voice-interview prompt has a dedicated 'what-you-decline' section. Extracted declinations pass through voice tuner before rendering. Pattern + content ship together.

## Scale notes · path from bespoke to systemizable

**MIXED · FIX: Voice-interview trigger.** Section auto-ships only if voice interview scores 3+ declinations. Systemizable at pipeline level, bespoke at content level. Same interview as pull-quote pattern — no extra onboarding cost.

## Visual reference

- Desktop: `visuals/voice-tuned-counter-list-desktop.png`
- Mobile: `visuals/voice-tuned-counter-list-mobile.png`

---

_Round 1 · Oxford Lawn · GRM Design_

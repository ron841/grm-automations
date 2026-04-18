# Serif-display editorial headline system

`serif-display-headline-system`

| Field | Value |
|---|---|
| Scale | **Bespoke** |
| Mobile | ✓ Ports cleanly |
| Voice assignment | — (chrome, no copy) |
| Pages used | Sitewide |

## Purpose

Newsreader-based editorial headline system with italic accent phrases. Ships as one of three typographic classes.

## Rationale

Newsreader with italic accents. Reads as trade-journal editorial. Lands for craft specialists. Lands wrong on 24-hour emergency plumbing.

## Replaces (from F3 / F5 / F6 flagship)

F3/F5/F6 use Space Grotesk/Inter — SaaS-safe, reads generic.

## Structural outline

```html
<h1 class="h-display h1">
  Weak lawns don't need more grass.
  <em class="display-it">They need better soil.</em>
</h1>
```

## Design tokens used

--f-display (Newsreader 500), --f-display-it (Newsreader italic), --lawn-700 (italic accent color), letter-spacing -0.025em, line-height 1.02 for h1/h2

## Behavior notes

Pure typography. Italic em blocks can carry color accent.

## Responsive notes

Sizes via clamp(). H1: clamp(2.4rem, 5vw, 4.5rem). Italic accents survive.

## Constraints

Don't use this class on emergency/urgency trades. Pair with 'editorial-specialist' trade-class only.

## Code conversion notes

Trade-class selection at onboarding. 3 classes: editorial-specialist (this), operations-forward (Public Sans + Space Mono), emergency-urgent (Space Grotesk + Inter Tight). Class name applied at body level.

## Scale notes · path from bespoke to systemizable

**BESPOKE · FIX: Trade-class variants.** Ship 3 typographic classes: editorial-specialist (Newsreader / JetBrains / Public Sans), operations-forward (Public Sans / Space Mono / Public Sans), emergency-urgent (Space Grotesk / Inter Tight / Inter). Tag each contractor at onboarding. Moves from bespoke → systemizable for all 50 trades.

## Visual reference

- Desktop: `visuals/serif-display-headline-system-desktop.png`
- Mobile: `visuals/serif-display-headline-system-mobile.png`

---

_Round 1 · Oxford Lawn · GRM Design_

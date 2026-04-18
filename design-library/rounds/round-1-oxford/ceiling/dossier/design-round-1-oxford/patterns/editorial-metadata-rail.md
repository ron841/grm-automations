# Editorial metadata rail

`editorial-metadata-rail`

| Field | Value |
|---|---|
| Scale | **Systemizable** |
| Mobile | ✓ Ports cleanly |
| Voice assignment | all (chrome) |
| Pages used | Home, About, Services, Process, Gallery, Reviews, Contact |

## Purpose

Sticky left rail on all 7 page types. Carries file number, voice tag, subject, GPS, license, and an optional divot divider. It is the primary device that turns 'a contractor website' into 'a contractor editorial product'.

## Rationale

Sticky left-column meta. File number, voice tag, subject, GPS, license. Turns 'about this page' into 'about this file'. The single biggest structural gap vs F3/F5/F6.

## Replaces (from F3 / F5 / F6 flagship)

Replaces the generic opening kicker / eyebrow used on every flagship page.

## Structural outline

```html
<aside class="rail">
  <div><b>FILE 01</b>{PAGE_NAME}</div>
  <div class="divot"></div>
  <div><b>Voice</b>{SECTION_VOICE}</div>
  <div><b>{META_KEY}</b>{META_VALUE}</div>
  …
</aside>
```

## Design tokens used

--f-mono (labels), --soil-2 (label text), --ink (value text), --rule (horizontal dividers), --cream-2 (optional fill), --step--1 (font size), position: sticky; top: 100px

## Behavior notes

Sticky positioning within the editorial-grid parent. Does NOT become sticky on mobile — converts to a static meta-row.

## Responsive notes

Desktop: 180px-wide left column of a 2-col grid. Mobile (<780px): flattens to horizontal row above content; left-border rotates to top-border; meta items wrap with gap.

## Constraints

WCAG AA. Values must be real data (no 'Location: Somewhere, USA' placeholder text). License number is jurisdiction-configurable — skip line if client is in a no-license trade/state.

## Code conversion notes

Rail items come from a per-page config array `railMeta: [{label, value}]`. Site config provides: FILE_NUMBER, COORDINATES, LICENSE_NUMBER. Voice-per-section comes from voices.json. The `.divot` element is a visual-only separator — no text content, no ARIA role.

## Visual reference

- Desktop: `visuals/editorial-metadata-rail-desktop.png`
- Mobile: `visuals/editorial-metadata-rail-mobile.png`

---

_Round 1 · Oxford Lawn · GRM Design_

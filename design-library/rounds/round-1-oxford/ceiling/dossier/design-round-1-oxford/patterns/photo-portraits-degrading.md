# Portrait / work-in-progress photo (degrading)

`photo-portraits-degrading`

| Field | Value |
|---|---|
| Scale | **Mixed** |
| Mobile | ✓ Ports cleanly |
| Voice assignment | — (chrome, no copy) |
| Pages used | About, hero |

## Purpose

Founder portraits ideal; GMB truck-on-site → Instagram → placeholder as fallback chain.

## Rationale

Tom + Tracy portraits ideal. Falls back to GMB truck-on-site → Instagram → placeholder. Photography sourcing systemizable; quality per client bespoke.

## Replaces (from F3 / F5 / F6 flagship)

F3/F5/F6 rely on stock or mixed quality.

## Structural outline

```html
<figure class="portrait" data-source="founder|gmb|ig|placeholder">
  <img src="…" alt="Tom and Tracy, Oxford Lawn founders, on a Villages property, 2024" />
  <figcaption class="caption">…</figcaption>
</figure>
```

## Design tokens used

Standard image. Caption uses --f-mono 0.6rem uppercase.

## Behavior notes

Static.

## Responsive notes

Aspect ratio preserved. Single-column stack on mobile.

## Constraints

Source tier determines where it ships: portraits → hero positions, GMB → gallery, IG → ambient, placeholder → hidden. Alt text is content, not SEO.

## Code conversion notes

Ingestion pipeline: (1) check client.photos.portraits; (2) fall back to GMB places-photos API; (3) fall back to Instagram Graph; (4) final fallback is a branded placeholder SVG. Each source tier maps to acceptable slots — placeholders never appear in hero.

## Scale notes · path from bespoke to systemizable

**MIXED · FIX: GMB + Instagram ingestion pipeline + fallback hierarchy.** Systemizable as a fetch strategy. Quality per client is data-driven not design-driven. Pattern ships; quality budgets go to photo-scarce clients individually.

## Visual reference

- Desktop: `visuals/photo-portraits-degrading-desktop.png`
- Mobile: `visuals/photo-portraits-degrading-mobile.png`

---

_Round 1 · Oxford Lawn · GRM Design_

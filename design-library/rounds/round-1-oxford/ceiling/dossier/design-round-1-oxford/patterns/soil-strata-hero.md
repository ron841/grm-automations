# Soil-strata motif hero column

`soil-strata-hero`

| Field | Value |
|---|---|
| Scale | **Bespoke** |
| Mobile | ⚠ Mobile-gated — see Responsive notes |
| Voice assignment | — (chrome, no copy) |
| Pages used | Home, Process |

## Purpose

Stratified horizontal band representing trade-specific material cross-sections. Oxford: thatch/grass/root/compost/subsoil. Signature visual + divider + process diagram anchor.

## Rationale

Stratified horizontal band (thatch / grass / root / compost / subsoil). Signature visual + divider + process diagram.

## Replaces (from F3 / F5 / F6 flagship)

The F6 7-photo crossfade hero.

## Structural outline

```html
<div class="strata" aria-hidden="true">
  <div class="bands">
    <div class="layer l-thatch">Thatch · 0–1"</div>
    <div class="layer l-grass">Living grass</div>
    <div class="layer l-roots">Root zone · 1–4"</div>
    <div class="layer l-compost">Compost / loam · 4–8"</div>
    <div class="layer l-subsoil">Subsoil</div>
  </div>
</div>
```

## Design tokens used

--thatch, --lawn-500, --soil-1, --stone, --ink for layer colors. --f-mono uppercase 0.14em ls for labels.

## Behavior notes

Static visual. Can be used as divider (tall, vertical) or hero band (wide, horizontal).

## Responsive notes

MOBILE-GATED at full height. Mobile = compact strata chip rail (see mobile.html). Desktop: 200–400px tall horizontal strata. Mobile: 4 horizontal chip bands with label + depth/state pairs.

## Constraints

aria-hidden on decorative variant. Strata color palette must match soil reality — don't let these drift to decorative colors.

## Code conversion notes

This pattern has a trade-variant registry planned (see Round 1 bespoke path). For Round 1 Oxford build, ship only the soil variant. Build strata-variant component after.

## Scale notes · path from bespoke to systemizable

**BESPOKE · FIX: Vector asset library · stratified-band-motifs.** Build a reusable 'material cross-section' component with stratified-band variants per trade category: soil (lawn), water column (pool), earth profile (septic), structural assembly (roofing), panel assembly (electrical). Ships with ~10 trade variants. Moves from bespoke → systemizable for ~20 of 50 trades.

## Visual reference

- Desktop: `visuals/soil-strata-hero-desktop.png`
- Mobile: (see compact mobile variant in design project)

---

_Round 1 · Oxford Lawn · GRM Design_

# Chip-selector assessment form

`chip-selector-form`

| Field | Value |
|---|---|
| Scale | **Systemizable** |
| Mobile | ✓ Ports cleanly |
| Voice assignment | Saturday Morning |
| Pages used | Contact |

## Purpose

Chip-selector contact form. Chips map to services array. Trade-variable fields (grass type → fixture type → system type).

## Rationale

Chips for 'what do you need' map to services array. Grass-type dropdown becomes fixture-type / system for other trades.

## Replaces (from F3 / F5 / F6 flagship)

F3/F5/F6 use standard dropdown form. Chips increase tap targets and read friendlier on phone.

## Structural outline

```html
<form class="contact-form">
  <label>Your name</label><input name="name" required/>
  <label>Phone</label><input type="tel" name="phone" required/>
  <label>What do you need?</label>
  <div class="chips" role="group">
    <button type="button" class="chip" data-value="full-rehab">Full rehab</button>
    …
  </div>
  <label>Grass type</label>
  <select name="grass">…</select>
  <label>Tell us about the lawn</label><textarea name="notes"></textarea>
  <button type="submit" class="submit">Send the note</button>
</form>
```

## Design tokens used

--lawn-500 (chip active bg), --lawn-900 (chip active text + border), --rule (chip inactive border), --ink (submit bg), 44px min-height for all chips.

## Behavior notes

Chip toggles .on class + hidden input value. Form validates client-side. Submit → API → success state replaces form with confirmation.

## Responsive notes

Chip row wraps naturally. 44px tap targets. Form stacks to single column below 900px.

## Constraints

WCAG AA: chips are buttons (not divs), role='group' wrapper, aria-pressed on chips. Native form validation + custom :invalid styles. Honeypot field for spam.

## Code conversion notes

Chip options from trade-config. Form-submission endpoint is per-deployment (Netlify/Formspree/own). Success state is a single component swap, not a navigation.

## Visual reference

- Desktop: `visuals/chip-selector-form-desktop.png`
- Mobile: `visuals/chip-selector-form-mobile.png`

---

_Round 1 · Oxford Lawn · GRM Design_

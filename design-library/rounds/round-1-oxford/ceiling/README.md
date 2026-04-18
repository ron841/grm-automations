# Oxford Lawn — Round 1 static export

Frozen reference snapshot of the Round 1 design project. Deployable as-is to Vercel, Netlify, GitHub Pages, or any static host.

## What's inside

### Applied-site pages (Oxford Lawn ceiling concept)
- `index.html` — Home
- `about.html` — About
- `services.html` — Services
- `process.html` — Process
- `gallery.html` — Gallery
- `reviews.html` — Reviews
- `contact.html` — Contact

### Design-system review pages
- `library.html` — 22-pattern library view
- `mobile.html` — mobile compositions (Home / Services / Contact)
- `gap-catalog.html` — systemizable vs. bespoke audit
- `dossier.html` — Code handoff dossier

### Round 1 post-review additions
- `typographic-classes.html` — three headline-system sketches (Editorial / Operations / Emergency)
- `soil-cross-section-references.html` — three ceiling references for the annotated cross-section

### Supporting
- `styles/base.css` — full design system
- `scripts/` — shared nav/footer, library data, partials
- `dossier/design-round-1-oxford/` — the Code handoff dossier (22 spec cards, DECISIONS.md, index.md, visuals)

## Deploy

Zero build step. Drop the folder into:

```
vercel deploy oxford-ceiling-static-export
```

or push to GitHub and point Pages/Vercel at the repo root. All paths are relative.

## Fonts

Google Fonts are loaded via `<link>` — no local copies. Pages render identically online and offline (offline falls back to system fonts).

## Frozen as of

Round 1 handoff, post-founder-review (Q1–Q5 applied). Not a live site — this is a reference snapshot.

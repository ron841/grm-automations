# Round 1 — Decisions Log

Founder review, response to Round 1 open questions. Recorded verbatim so Round 2 has a clean starting point.

---

## Q1 · Typographic classes

**Decision:** Build all three typographic classes as sketches. Editorial-specialist is already on Oxford (Round 1 baseline). Add **Operations-Forward** and **Emergency-Urgent** as headline-system concepts applied to representative prospect archetypes — not full rebuilds.

**Status:** Shipped in Round 1. See `/typographic-classes.html` in project root.

**Scope delivered:**
- Class A — Editorial-specialist (reference, Oxford's current voice)
- Class B — Operations-forward, applied to archetype "Fleet Lawn Services Co."
- Class C — Emergency-urgent, applied to archetype "Storm Response / 24-Hr Tree & Turf"
- Comparison matrix across 9 axes

**Scope explicitly excluded:** Full site rebuilds, nav/footer/service pages, photography direction.

**Open for Round 2:** Does Oxford productize B or C as a sub-brand, or are these templates for other operators entirely? Class type is the same answer either way; the commercial question isn't.

---

## Q2 · Annotated soil cross-section

**Decision:** No illustrator commission in Round 1. Produce concept sketches as **ceiling references**, not production.

**Status:** Shipped. See `/soil-cross-section-references.html`. Every panel stamped "CEILING REFERENCE · NOT PRODUCTION."

**Scope delivered:** Three references — A. Field-manual diagram · B. Painterly strata plate · D. Blueprint / engineering section. Each with medium, palette, annotation system, reuse potential, risk, and cost estimate.

**Removed during founder review:** Reference C (Wardian-case / terrarium). Oxford does core aeration but doesn't collect or display soil samples — the motif implies a practice they don't have. Killed before shipping to Code.

**Recommendation (for Round 2 decision gate):** If commissioning, Reference B. If not, productize Reference D (code-drawable in-house). Do not ship both.

**Round 1 production art:** The existing code-drawn diagram on the Process page remains in place. These references do not replace it.

---

## Q3 · Review-theme NLP pipeline

**Decision:** Ships from Code side, **post-sales-kickoff**.

**Design implication:** Pattern `review-theme-index` (Pattern 20) ships in Round 1 as designed, populated with representative themes. The live NLP ingest is a post-sale engineering scope, not a design scope. No change to the pattern's spec card.

**Status:** No design action. Logged for Code handoff.

---

## Q4 · Voice-interview onboarding

**Decision:** Stays founder-led for the first 5 clients. Add "voice-interview UI concept" to **Round 2 or 3** design backlog — not Round 1.

**Design implication:** No voice-interview UI in Round 1. The existing `voice-tagged-sections` pattern covers the output surface (quoted founder voice surfaced in the site). The *capture* surface (interview tool, transcript editor, voice-to-pattern binding) is explicitly deferred.

**Status:** Deferred. Moved to Round 2/3 backlog.

---

## Q5 · Pattern 19 — Magazine issue chrome / Premium tier

**Decision:** Build Pattern 19 as-designed, flagged as **Premium-tier-concept**. Whether Premium is a real product SKU gets decided after seeing the pattern live.

**Design implication:** Pattern 19 (`magazine-issue-chrome`) ships in Round 1 exactly as designed. Spec card gets a `tier: Premium-tier-concept` flag. No other change.

**Status:** Ship as-is. Revisit post-Round-1 review.

---

## Carried forward to Round 2 backlog

| Item | Origin | Priority |
|---|---|---|
| Productize Class B or C (archetype template) | Q1 | High — depends on commercial direction |
| Commission decision: Ref B or productize Ref D | Q2 | Medium — pre-Round-2 |
| Voice-interview UI concept | Q4 | Low — after first 5 founder-led clients |
| Premium tier SKU decision | Q5 | Medium — post-live review |
| Review-theme NLP ingest UI (if needed) | Q3 | None — engineering-led |

---

## Not changed in Round 1

- All 22 library patterns ship as-is
- Oxford applied-site pages (Home, Services, Process, About) ship as-is
- Existing code-drawn soil diagram on Process page stays
- Editorial typographic class remains Oxford's voice

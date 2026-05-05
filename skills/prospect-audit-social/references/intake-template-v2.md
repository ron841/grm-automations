# Intake Template — v2.0

The canonical intake template populated by the audit skill or by a manual run. Every per-prospect `intake.md` follows this shape. Fields tagged with three states: filled-with-value / `[gap]` / `[scrape-failed]`.

This template is the contract between the audit stage and the synthesis stage. Synthesis cannot proceed past `[scrape-failed]` fields that materially affect voice or differentiator claims; either re-capture, or the field is reclassified `[gap]` with that decision documented.

---

# {BUSINESS_NAME} — Intake

> **Source tags inline:** *[API]* Places API · *[manual]* user capture · *[web]* public web search · *[FB]* Facebook · *[IG]* Instagram · *[scrape-Playwright]* Playwright DOM extraction · *[derived]* computed from captures · *[human]* requires human judgment

> **Capture method:** {audit-skill | manual} · **Run date:** {YYYY-MM-DD}

## §1 Identity

- **Business name (legal, as on GBP):** {name}
- **DBA / display name (if different):** {name or `[gap]`}
- **Tagline / slogan:** {tagline or `[gap]`} *[source]*
- **Owner full name:** {first last} *[FL registry verification]*
- **Owner story signal:** {one-sentence narrative based on review evidence + FB attribution + area code + LLC dates} *[derived]*
- **Year founded / years in business:** LLC filed {YYYY-MM-DD}; reviewer evidence suggests {N} years operating *[FL Division of Corporations + review mining]*
- **License & insurance status:** {captured | `[gap]` for walkthrough}

## §2 Location & Contact

- **Address:** {full street + city + state + zip} *[API]*
- **Phone:** {(XXX) XXX-XXXX} *[API]*
- **Email:** {address | `[gap]`}
- **Website:** {URL or "none (confirmed)"} *[API]*
- **Service area:** {primary listing + named neighborhoods or referral areas} *[API + review evidence]*

## §3 Hours & Availability

- **Regular hours:** {per-day hours} *[API]*
- **Emergency / 24-hour service flag:** {yes | no | `[gap]`}
- **Booking method:** {phone | online | in-person} *[API + review evidence]*

## §4 Categories & Services

- **GBP primary category:** {category} *[API]*
- **GBP secondary categories:** {list} *[API]*
- **Services list (synthesized from review evidence):**
  - {service 1} *[review N]*
  - {service 2} *[review M]*
  - ...

### §4a Voice — Owner Replies (first-class section)

- **Reply rate:** {N of M reviews carry owner replies}
- **Length distribution:**
  - Canned (<30 chars): {N}
  - Short (30-100): {N}
  - Medium (100-250): {N}
  - Detailed (>250): {N}
- **Recurring openers:** {top 3-5 phrases with occurrence counts}
- **Voice tone characterization:** {short paragraph: gratitude-first / family-framed / forward-looking / etc.}
- **Verbatim phrases worth lifting for synthesis:** {list of phrases ≥2 occurrences, suitable for connector copy}
- **Reply behavior tag:** {replies-to-all | replies-selectively | does-not-reply | unknown}

This subsection is canonical. Re-captures populate it in place; do not add a new subsection at the top of §Voice — Reviews.

## §5 Attributes & Credentials

- **GBP attributes:** {wheelchair accessible / women-owned / veteran-owned / family-owned / etc.} *[API]*
- **Certifications mentioned in reviews or social:** {list or `[gap]`}
- **Awards / recognition:** {list or `[gap]`}

## §6 Voice — Reviews

> **Capture status:** {N reviews captured with body text out of M total} · **Saturation:** {REACHED at #N | NOT REACHED} · **Source(s):** {GBP API + Playwright | + Birdeye | + Yelp | + FB recs}

> **Saturation analysis:**
> - Distinct job-noun categories plateau at review #{N} ({K} of {total} categories matched)
> - Distinct praise-pattern categories plateau at review #{N} ({K} of {total} categories matched)
> - {Both saturated by review #N | not yet saturated, additional sources warranted | corpus exhausted before saturation}

### Review N *[source, capture-date]*

- **Stars:** {1-5}
- **Reviewer:** {name}
- **Text:** "{verbatim review text, no edits}"
- **Owner reply** *(relative date)*: "{verbatim reply text}" or *none*

(Repeated for every captured review.)

## §7 Voice — Saturation tables

> Generated from the captured review corpus. Frequency = number of reviews matching the regex pattern for that category.

### Job-noun frequency (synthesis §3 services-list input)

| Job category | Reviews mentioning |
| --- | --- |
| {category 1} | {N} |
| {category 2} | {N} |
| ... | ... |

### Praise-pattern frequency (synthesis §4 differentiator input)

| Praise category | Reviews mentioning |
| --- | --- |
| {category 1} | {N} |
| {category 2} | {N} |
| ... | ... |

### Differentiator implications

- **{Differentiator 1}:** {strength assessment with evidence count}
- **{Differentiator 2}:** {strength assessment with evidence count}
- ...

## §8 Voice — Bio extracts

> Source: {FB tagline | IG bio | About page | other}

- **Tagline candidates** (verbatim): {list}
- **Owner story signals in bio:** {list or `[gap]`}
- **Years in business claims in bio:** {claim or `[gap]`}
- **Service mentions in bio:** {list or `[gap]`}
- **Personality markers:** {short paragraph}

## §9 Social Presence

### Facebook

- **Page URL:** {URL or `[gap]`}
- **About text in full:** "{verbatim or `[gap]`}"
- **Recent post excerpts:** {list of 5-10 or `[scrape-failed]`}
- **Recurring themes:** {list or `[scrape-failed]`}
- **Voice tone in posts:** {short paragraph or `[scrape-failed]`}
- **Follower count (page likes):** {N or `[gap]`}
- **Adjacent FB accounts:** {related personal pages or older brands}

### Instagram

- **Handle / URL:** {handle or `[gap]` or `[verification-deferred]`}
- **Bio in full:** "{verbatim or `[scrape-failed]`}"
- **Recent post captions:** {list or `[scrape-failed]`}
- **Recurring themes:** {list or `[scrape-failed]`}
- **Voice tone in posts:** {short paragraph or `[scrape-failed]`}
- **Follower count:** {N or `[scrape-failed]`}

### Social presence summary

- **Primary channel:** {FB | IG | both | neither}
- **Secondary channel:** {if any}
- **Activity level:** {high | medium | low | unknown}

## §10 Photos

> Captured: {N} from GBP at full native resolution + {N} from FB + {N} from IG

For each photo:

- **File:** {path}
- **Source:** {GBP-API | FB-Playwright | IG-Playwright | operator-supplied}
- **Provenance:** {owner-uploaded | customer-uploaded | both-attribution-known}
- **Subject:** {description or `[design-tagged]` for downstream}
- **Usability:** {hero-grade | section-grade | proof-grid-grade | weak | `[design-tagged]`}
- **Cross-references:** {if customer-uploaded, name the reviewer + review index}

(Repeated for every photo.)

## §11 Logo

- **Found:** {Yes | No}
- **Source:** {FB profile picture | operator-supplied | extracted from photo}
- **File saved at:** {path}
- **Quality:** {raster-low | raster-high | vector | `[gap]`}

## §12 Colors

- **Extracted from logo (k-means k=5):** {top 3-5 clusters with hex + frequency + confidence}
- **Extracted from uniforms / vehicles / signage:** {clusters or `[gap]`}
- **Proposed palette:** {primary + accent + paper variants}
- **Confidence:** {high | medium | low}

## §13 Trust Signals

- **Total reviews:** {N} *[API]*
- **Star rating:** {X.Y} *[API]*
- **Years on Google (rough):** {derived from earliest review} *[review evidence]*
- **FB follower count:** {N or `[gap]`}
- **IG follower count:** {N or `[gap]`}
- **FB check-in count:** {N or `[gap]`}
- **Years in business:** {LLC age + review evidence} *[derived]*

## §14 Differentiators (synthesized)

Ranked by evidence weight:

1. **{Differentiator 1}.** {one-sentence framing} *[evidence count]*
2. **{Differentiator 2}.** {one-sentence framing} *[evidence count]*
3. **{Differentiator 3}.** {one-sentence framing} *[evidence count]*

(Typically 3-5 ranked.)

## §15 Content Gaps Flagged

**Resolved this pass:**

- {item 1}
- {item 2}

**Still open (require walkthrough or manual capture):**

- {item 1}
- {item 2}

## §16 Capture Run Notes

- **Audit script version:** {version or "manual"}
- **Run date:** {YYYY-MM-DD}
- **Duration:** {minutes}
- **Successful captures:** {list}
- **Failures and retries:** {list}
- **Deferred to manual:** {list}

---

## Notes for the audit skill

- Every field above must be either populated or explicitly tagged with a deferred state.
- The `[scrape-failed]` versus `[gap]` distinction is critical. A `[gap]` is a real absence (the operator does not have a website, the LLC is too recent for years-in-business claims). A `[scrape-failed]` is debt — the data exists but capture did not retrieve it. Synthesis treats them differently.
- The §4a Voice — Owner Replies section is canonical first-class. Do not augment §6 Voice — Reviews with reply analysis at the top while leaving §4a as a placeholder; populate §4a in place.
- The §10 Photos section's three-axis tagging (source / provenance / subject+usability) is the contract. Customer-attributed photos rank above owner-uploaded for downstream slot assignment.
- §12 Colors runs k-means at audit time. Provisional palettes set during pack-authoring are wrong; the build extraction is the truth.
- §7 Saturation tables drive synthesis differentiator math. Synthesis differentiator claims must trace to ≥4 occurrences in §7 for paragraph weight, ≥10 for headline weight.

---

## What this template does not capture

- Synthesis-layer outputs (voice argument, persona resolution, section sequence). Design owns those.
- Content-inventory or slots. Design owns those.
- Build artifacts. Code owns those.
- Operator-confirmed values requiring walkthrough. The intake notes them as `pending-walkthrough` and the per-prospect README's Open Decisions table walks them.

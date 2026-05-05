# Three-State Tagging Discipline

Every field in `intake.md` carries one of three states. Conflating them is the most common audit-stage failure mode. This doc names the rule, the discriminator, and the failure case it traces to.

## The three states

### 1. Filled with a value

Confidently captured from API, scrape, derivation, or operator confirmation. The value is present and downstream stages reference it directly.

Examples:
- `Star rating: 4.9 [API]`
- `Reply rate: 43 of 44 reviews carry owner replies [scrape-Playwright]`
- `Year founded: LLC filed 2018-04-12; reviewer evidence suggests 7 years operating [FL Division of Corporations + review mining]`

### 2. `[gap]`

Capture attempted, source genuinely lacks the data. The absence is informational and may itself be a signal.

A `[gap]` is permanent for the run. It is what the public surfaces actually carry. Synthesis can build voice claims around a `[gap]` as long as the absence is real evidence, not a capture artifact.

Examples:
- `Website: none (confirmed) [API]` — the operator has no website. Real `[gap]`. The absence is the no-website-pipeline use case.
- `Tagline: [gap]` — the GBP listing has no tagline field set. Real `[gap]`. Synthesis writes around it.
- `Adjacent FB accounts: [gap]` — search returned no related personal pages. Real `[gap]`.
- `Recent IG posts: [gap]` — operator has IG handle but no recent posts. Real `[gap]`.

### 3. `[scrape-failed]` or `[low-confidence]`

Capture attempted, technical or semantic failure. The data exists but capture did not retrieve it. Retry is warranted; copy authored around the absence is wrong.

A `[scrape-failed]` is debt that needs paying. The next iteration of the audit (or operator walkthrough) should resolve it.

`[low-confidence]` is a softer variant: the capture succeeded but the result is ambiguous (a name match across multiple LLCs, a photo with missing attribution, a review with mixed sentiment that the regex could not classify cleanly).

Examples:
- `Owner full name: [low-confidence]` — registry returned 3 LLCs with similar names; manual disambiguation needed.
- `FB recent posts: [scrape-failed]` — Playwright reached the page but the posts feed did not render before timeout. Retry warranted.
- `Logo file: [scrape-failed]` — FB profile picture URL returned 404. The page exists; the picture endpoint failed.

## The discriminator

When a field is unpopulated, ask: **did the source carry the data, and capture missed it?**

- Yes → `[scrape-failed]` or `[low-confidence]`. The data exists. Retry, or operator walkthrough resolves it.
- No → `[gap]`. The data does not exist. Synthesis treats the absence as evidence.

The discriminator is the source's actual state, not the capture run's report.

## Why this matters

Conflating `[gap]` with `[scrape-failed]` is the most common failure mode at the audit-to-synthesis seam. The Yankee Handyman iter-1 lesson:

> **What happened:** Iteration 1 audit concluded "Anthony does not reply to Google reviews," based on the 5 reviews returned by the Places API where the reply field was empty. Synthesis treated the absence as voice signal and authored persona claims (low-ego, no register-shift evidence) around it. Iteration 2 re-scrape via Playwright DOM extraction surfaced 43 owner replies across 44 reviews. The Places API was simply truncating the reply field at the default capture depth.

The iter-1 fields were tagged as filled values (empty replies) but should have been `[scrape-failed]`. Synthesis built voice claims on capture artifacts. Iter-2 had to rebuild.

## Method-completeness rule

A `[gap]` is only valid when the capture method is known to be complete for that field. If the capture method may have truncated the data, the field is `[scrape-failed]` until a complete method is run.

For the audit skill specifically:
- Places API reviews field: known to truncate to 5 entries with possibly-empty reply text. Reviews from the Places API are NEVER tagged `[gap]` on reply absence. The discriminator is "did the Playwright all-reviews scrape see this review with no reply?"
- FB profile picture endpoint: known to return a default placeholder if no picture is set. A placeholder image is `[gap]`; a 404 is `[scrape-failed]`.
- IG bio: known to be present on every public profile. Empty IG bio is `[gap]`; an unreachable profile is `[scrape-failed]`.

When in doubt, prefer `[scrape-failed]` over `[gap]`. False-positive `[scrape-failed]` produces a retry; false-positive `[gap]` corrupts synthesis.

## Deferred states beyond the audit

Content-inventory and slots use additional deferred states that the audit does not produce:

- `pending-walkthrough` — operator confirmation is the resolution.
- `pending-image-review` — photo selection is the resolution.
- `pending-extraction` — mechanical extraction at build time is the resolution.

These are downstream-only. The audit emits filled values, `[gap]`, `[scrape-failed]`, or `[low-confidence]`, and nothing else.

## Forcing-function exit check

Phase 9 of the audit runs the exit check: every intake field is filled OR explicitly tagged. Zero ambiguous blanks. The check is the audit's contract with the seam to Synthesis.

If the exit check fails, the orchestrator exits non-zero with the failing field list. The audit does not ship a partial intake; the seam is forcing-function.

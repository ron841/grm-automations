# Deployment and Client Lifecycle Reference

Part of the prospect-site skill v0.7. Loaded by Phase 7 during preview deployment. Also serves as the operational playbook for the client lifecycle that begins after a preview converts to a signed deal.

This file has two distinct parts with different audiences. Part 1 is the deployment logic Claude Code executes automatically when Phase 6 verification passes. Part 2 is the client lifecycle playbook Ron executes manually (or semi-manually via Claude Code) once a prospect signs a service agreement. The two parts share infrastructure (the same Vercel project, the same Static Forms account, the same folder structure) but different workflows. The file structure below makes the audience split explicit.

Every procedure in this file has one of two labels:

- **[SKILL]** — automated, executed by Claude Code as part of the skill run
- **[OPS]** — manual or semi-manual, executed by Ron (or future GRM staff) outside the skill run

Do not blur the two. A procedure labeled OPS should not be automated by the skill without an explicit roadmap decision. A procedure labeled SKILL should not be silently run by a human; it is the skill's responsibility.

---

## Table of contents

1. Part 1: Preview deployment (Phase 7)
2. Part 2: Client lifecycle playbook (post-sale operations)
3. What is deliberately not in v0.7
4. Common mistakes to avoid
5. Self-check
6. Version

---

# PART 1 — PREVIEW DEPLOYMENT (PHASE 7)

Phase 7 runs after Phase 6 verification passes. Its job is to take the locally built site in `~/grm-sites-prospects/[business-slug]/` and deploy it to a unique, publicly reachable Vercel URL that Ron can text or email to the prospect as a sales weapon. Everything in this part is automated by the skill.

Phase 7 does NOT deploy to a client's real domain. That is a post-sale operation covered in Part 2 (Custom domain migration). Phase 7 always deploys to the Vercel-hosted preview URL only.

## Phase 7 preconditions

**[SKILL]** Before Phase 7 begins, verify:

1. Phase 6 completed with all hard gate checks green
2. `~/grm-sites-prospects/[business-slug]/` exists and contains the built site files
3. `profile-draft.json` exists in the same folder
4. Vercel CLI is installed and authenticated (`vercel whoami` returns the expected account)
5. Current Vercel team scope is `ron-7323` (`vercel teams ls` shows it as active)
6. The working directory is the prospect folder (`pwd` matches `~/grm-sites-prospects/[business-slug]`)

If any precondition fails, stop and report to Ron. Do not attempt deployment.

### Vercel team scope notes

Per the v0.7 working notes, the Vercel CLI authenticated under `ron-7323` cannot see projects that live under a different team scope. The older `grm-sites` and `website` projects live under `team_KCAi5VnxkXE0c5ERJWOb7jXE` per `.vercel/project.json` in the `website` folder. These are not accessible from a fresh session authenticated as `ron-7323`. This is intentional. Keep the preview deployments on `ron-7323` and the production `getrootedmedia.com` site on the other team. Do not attempt to migrate either direction without an explicit Ron decision.

If the CLI returns unexpected results (missing projects, permission errors, 404s on known projects), check team scope first with `vercel teams ls` before diagnosing anything else.

## Project naming convention

**[SKILL]** Every preview deployment uses the naming convention:

```
[business-slug]-grm
```

This produces a Vercel project name and a preview URL:

```
[business-slug]-grm.vercel.app
```

Examples:

- T&F Electric → `tandf-electric-grm` → `tandf-electric-grm.vercel.app`
- Johnson Brothers Plumbing → `johnson-brothers-plumbing-grm` → `johnson-brothers-plumbing-grm.vercel.app`
- Pat Myers Electric → `pat-myers-electric-grm` → `pat-myers-electric-grm.vercel.app`

### Why the `-grm` suffix

Two reasons:

1. **Namespace isolation.** The `-grm` suffix makes it obvious at a glance that the project is owned by Get Rooted Media. When Ron opens the Vercel dashboard and sees 30 projects, the `-grm` suffix keeps the GRM portfolio visually separated from any personal projects.
2. **Collision resistance.** Generic business slugs like `acme-plumbing` are likely to collide with existing Vercel projects owned by other users. The `-grm` suffix reduces collision probability dramatically.

### Collision handling

**[SKILL]** If the target project name is already taken on the `ron-7323` team, Phase 7 appends a numeric suffix:

```
[business-slug]-grm-2
[business-slug]-grm-3
```

Check for collisions before deploying:

```bash
vercel projects ls | grep "^[business-slug]-grm"
```

If the exact name appears, increment to the next available suffix. Document the chosen suffix in the deployment log output.

### Slug rules (recap from SKILL.md)

The business slug is derived from the business name:

1. Lowercase everything
2. Remove punctuation (`.`, `,`, `'`, `&`, `!`, `?`)
3. Replace spaces with hyphens
4. Remove duplicate hyphens
5. Strip leading and trailing hyphens
6. Remove common business suffixes (`llc`, `inc`, `co`, `company`, `corp`) if they appear at the end

Examples:

- "T&F Electric" → `tandf-electric`
- "Johnson Brothers Plumbing LLC" → `johnson-brothers-plumbing`
- "Starr's & Stripes Pressure Washing, Inc." → `starrs-and-stripes-pressure-washing`

The slug is set in Phase 1 when the prospect folder is created and never changes after that. If Phase 7 needs to correct a slug for any reason, it must rename the folder first, not deploy under a different name than the folder.

## Deployment workflow

**[SKILL]** The Phase 7 deployment sequence:

```bash
# Step 1: Confirm preconditions
cd ~/grm-sites-prospects/[business-slug]
vercel whoami
vercel teams ls

# Step 2: Check for name collision
vercel projects ls | grep "^[business-slug]-grm"

# Step 2.5: Slug reconciliation (Bug 5 fix — do NOT skip)
FINAL_ALIAS="[final-project-name].vercel.app"
# Grep generated files for any .vercel.app URL that doesn't match FINAL_ALIAS
# If stale references found, replace across all .html, sitemap.xml, robots.txt, llms.txt
# Verify zero stale references remain before proceeding to Step 3

# Step 3: Deploy with explicit project name
vercel --prod --yes --name [business-slug]-grm

# Step 4: Capture the returned production URL from stdout
# Vercel outputs a line like: https://[business-slug]-grm.vercel.app

# Step 5: Smoke test
curl -I https://[business-slug]-grm.vercel.app
curl -s https://[business-slug]-grm.vercel.app | grep -c "[business name]"
```

### Step-by-step detail

**Step 1** verifies the CLI environment. `vercel whoami` must return `ron-7323` or the expected current auth identity. `vercel teams ls` must show `ron-7323` as a team the current user has access to.

**Step 2** prevents collision with existing projects. Grep the output of `vercel projects ls` for the exact expected project name. If found, compute the next available suffix.

**Step 2.5** reconciles URL references before deployment. This step exists because Phase 5 writes URLs into generated HTML, XML, and TXT files using the Phase 1 directory slug (e.g., `a-1-payless-septic-service-inc-grm.vercel.app`), but Step 2 may have determined a different final project name (e.g., `a-1-payless-septic-grm` due to slug shortening, or `a-1-payless-septic-grm-2` due to collision). Without reconciliation, every URL-bearing artifact ships stale — including the form `redirectTo`, which sends every successful form submission to a 404 thank-you page.

The reconciliation procedure:

1. Compute the final alias: `https://[final-project-name].vercel.app`
2. Grep all `.html` files, `sitemap.xml`, `robots.txt`, and `llms.txt` for any `https://` URL containing `.vercel.app`
3. If every found URL already matches the final alias, no action needed — proceed to Step 3
4. If any found URL differs from the final alias, replace it with the final alias across all files. The seven artifact categories that carry URLs: `<link rel="canonical">` on every page, `<meta property="og:url">` on every page, `<input type="hidden" name="redirectTo">` on contact and index forms, JSON-LD `@id` and `url` fields in `<script type="application/ld+json">` blocks, `<loc>` entries in `sitemap.xml`, page links in `llms.txt`, and the `Sitemap:` pointer in `robots.txt`
5. After replacement, verify with a second grep that zero stale references remain
6. Log the reconciliation (old alias → new alias, count of replacements) for Phase 8

This step is the primary defense against Bug 5 (A-1 Payless Septic, 2026-04-15, 28 stale references in initial deploy). It runs before Step 3's deploy command so the first deploy pushes correct URLs — no double deploy required.

**Step 3** is the actual deployment. The flags matter:

- `--prod` deploys directly to the production environment of the Vercel project (not a preview branch). GRM preview URLs are production deployments of preview-purpose projects. This is intentional; it gives them stable URLs that Ron can share without worrying about preview branch expiration.
- `--yes` skips the interactive setup prompt. The first time a project is deployed, Vercel would normally ask questions about framework detection, build commands, and output directory. `--yes` accepts all the defaults. Because GRM sites are plain static HTML/CSS/JS, no build step is needed and Vercel's autodetection handles it cleanly.
- `--name [business-slug]-grm` sets the project name explicitly. Without this flag, Vercel generates a random project name based on the folder name, which is unreliable and not shareable.

**Step 4** captures the deployment URL from Vercel's stdout output. Parse the line that starts with `https://` and contains `.vercel.app`.

**Step 5** smoke tests the deployment. The `curl -I` confirms the server returns 200 OK. The `curl -s | grep -c` counts occurrences of the business name in the rendered HTML. If the count is zero, something deployed wrong and the file content is not the expected prospect site. Fail the build and report.

### Common Phase 7 failures and recovery

**Failure: `vercel` command not found**

The Vercel CLI is not installed or not in PATH. Report to Ron. Recovery: `npm install -g vercel` from the terminal, then retry Phase 7.

**Failure: authentication error**

`vercel whoami` returns an error or unexpected identity. Report to Ron. Recovery: `vercel login` and re-authenticate, then retry Phase 7.

**Failure: wrong team scope**

The deployment succeeds but the returned URL is under a different team namespace than expected. Report to Ron. Recovery: `vercel switch ron-7323` to change active team, then retry.

**Failure: collision detected but no resolution**

The collision handling logic chose a numeric suffix but the suffix is also taken. Report to Ron. Recovery: increment further (`-grm-3`, `-grm-4`) or ask Ron to pick a name manually.

**Failure: deployment returns 200 but content is wrong**

The smoke test count of business name occurrences is zero. This usually means the wrong folder was deployed, or the build directory mapping is wrong, or a caching issue. Report to Ron with the diff between expected and actual. Recovery: investigate the `vercel.json` and deployment logs in the Vercel dashboard.

**Failure: deployment returns 200 but curl I returns a Vercel 404 page**

This happens when Vercel deploys the project but the root document is not `index.html`. Check that `index.html` exists in the prospect folder root, not in a subdirectory. Recovery: if the site was built into a `dist/` or `public/` subdirectory, either move the files to the root OR create a `vercel.json` with the output directory configured.

### vercel.json configuration (if needed)

**[SKILL]** For the standard GRM prospect site (plain static HTML at the root of the prospect folder), no `vercel.json` is needed. Vercel autodetects the root-level `index.html` and serves it directly.

If Phase 5 generated the site into a subdirectory for any reason, Phase 7 writes a minimal `vercel.json` in the prospect folder root:

```json
{
  "outputDirectory": "public",
  "cleanUrls": true,
  "trailingSlash": false
}
```

- `outputDirectory` tells Vercel which folder to serve.
- `cleanUrls: true` serves `/about.html` as `/about` (removes the `.html` extension in URLs). This is a small polish that makes URLs feel more modern.
- `trailingSlash: false` prevents Vercel from auto-adding trailing slashes to URLs, which can cause canonicalization issues.

### Static asset headers

**[SKILL]** The `vercel.json` configures cache headers for static assets. Three rules, not one, because CSS/JS and images have different iteration cadences and a single catch-all breaks on iterative builds:

```json
{
  "headers": [
    {
      "source": "/(.*)\\.(css|js)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=300, must-revalidate"
        }
      ]
    },
    {
      "source": "/assets/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000"
        }
      ]
    },
    {
      "source": "/(.*).html",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=0, must-revalidate"
        }
      ]
    }
  ]
}
```

**Why three rules, not one.**

- **CSS and JS at the site root are non-content-hashed.** `style.css` and `script.js` keep the same filename across iterations, so `immutable` is broken-by-design — it tells browsers the URL never changes while the contents do. A 5-minute `max-age` with `must-revalidate` lets clients re-check on every session without nuking cache performance within a session. When v0.9 adds content-hashed filenames at build time, this rule moves back to long-lived immutable caching.
- **Images in `/assets/` are long-lived.** Photos, logos, and icons rarely change within a build lifecycle, and they are the bandwidth-heavy assets. Keep the one-year `max-age`, but drop `immutable` so revalidation remains possible if a photo does change. Images are the assets where cache longevity actually matters.
- **HTML always revalidates.** A homepage HTML edit must land immediately on the next load.

**Why this rule exists.** F5 A Quality Pool (April 2026) surfaced a four-hour cache-trap diagnostic caused by the original single-rule `/assets/(.*)` pattern at `max-age=31536000, immutable` catching `style.css` and `script.js`. F1–F4 didn't hit it because each build landed on a different alias; F5 was the first build with a second deploy onto the same alias with the same non-hashed filename, which is exactly the pattern every iterative flagship update will follow. The fix above ships with every v0.8+ build so iteration-breaking cache behavior stops being a trap to rediscover.

---

## Static Forms wiring

**[SKILL]** Every prospect site includes a contact form. Phase 5 generates the form markup. Phase 7 verifies the form is wired to the Static Forms account before deployment completes.

### The Static Forms account

GRM uses a single Static Forms account across all prospect sites. This is intentional: one account, one API key, one submission inbox. All submissions route to `ron@getrootedmedia.com`. The account details:

- **API key:** `sf_e0e200934d4f36c17a10d00c`
- **Endpoint:** `https://api.staticforms.xyz/submit`
- **Submission destination:** `ron@getrootedmedia.com`
- **Free tier allowance:** 500 submissions per month across all forms using this key

Per the Cowork research, Static Forms was chosen over Formspree (50/month), Web3Forms (250/month), Basin (100/month), and Getform (25-50/month) because 500 submissions per month gives GRM ~10x headroom compared to Formspree. At 30 prospect sites each generating 1-5 submissions per month, the total volume sits comfortably inside the free tier.

### Form markup template

**[SKILL]** Phase 5 writes the contact form with the following structure. Phase 7 verifies the structure before deploying.

```html
<form action="https://api.staticforms.xyz/submit" method="POST" class="contact-form">
  <input type="hidden" name="accessKey" value="sf_e0e200934d4f36c17a10d00c">
  <input type="hidden" name="subject" value="New contact from [Business Name] website">
  <input type="hidden" name="replyTo" value="@">
  <input type="hidden" name="redirectTo" value="https://[business-slug]-grm.vercel.app/thanks.html">

  <label for="name">Name <span aria-hidden="true">*</span></label>
  <input type="text" id="name" name="name" required autocomplete="name">

  <label for="phone">Phone <span aria-hidden="true">*</span></label>
  <input type="tel" id="phone" name="phone" required autocomplete="tel">

  <label for="email">Email</label>
  <input type="email" id="email" name="email" autocomplete="email">

  <label for="service">What do you need?</label>
  <select id="service" name="service">
    <option value="">Select a service</option>
    <!-- Populated from Phase 2 captured services -->
    <option value="Panel Upgrade">Panel Upgrade</option>
    <option value="Whole House Surge Protection">Whole House Surge Protection</option>
    <option value="Generator Installation">Generator Installation</option>
    <option value="Other">Other (describe below)</option>
  </select>

  <label for="message">Tell us what you're dealing with</label>
  <textarea id="message" name="message" rows="4"></textarea>

  <input type="text" name="honeypot" style="display:none" tabindex="-1" autocomplete="off">

  <button type="submit">Request a quote</button>
</form>
```

### Field-by-field explanation

**`accessKey`** — The Static Forms API key. This value is public (it appears in the rendered HTML and can be inspected by anyone), so there is nothing secret about it. Static Forms uses rate limiting and honeypot detection rather than key secrecy.

**`subject`** — The subject line of the email Ron receives when someone submits the form. Phase 5 populates this with `"New contact from [Business Name] website"` so Ron can see at a glance which client's site generated the submission. This matters a lot at scale: at 30 sites, a generic "New contact form submission" subject line is useless.

**`replyTo`** — Set to `"@"` which tells Static Forms to auto-populate the reply-to header with the submitter's email address. If Ron hits reply on the notification email, he replies directly to the person who filled out the form.

**`redirectTo`** — The URL the submitter is redirected to after a successful submission. Phase 5 generates a `thanks.html` page for every site. The redirect URL is the full preview URL at deploy time. During post-sale migration to a custom domain (Part 2), this value gets updated to point to the custom domain.

**`name`, `phone`, `email`, `service`, `message`** — The actual form fields the user fills out. `name` and `phone` are required (phone is critical because SMS follow-up is the primary conversion channel for home services). `email` is optional (some older homeowners don't use email). `service` is a dropdown populated from Phase 2 captured services. `message` is a free-text field.

**`honeypot`** — A hidden field that humans won't see or fill out but automated spam bots will fill. If Static Forms sees a value in `honeypot`, it silently drops the submission without emailing Ron. This is a standard anti-spam technique.

**`autocomplete`** — HTML autocomplete hints help mobile browsers pre-fill the form from the user's saved contact information. This is a conversion lift, especially on mobile where typing is painful.

### The thanks.html page

**[SKILL]** Phase 5 generates a `thanks.html` confirmation page that Static Forms redirects to after successful submission. Structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Thanks for reaching out — [Business Name]</title>
  <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
  <main class="thanks-page">
    <h1>Thanks. We got it.</h1>
    <p>[Business Name] will call or text you back within [response-time]. If you need us sooner, call us at <a href="tel:[phone-e164]">[phone-display]</a>.</p>
    <p><a href="/">Back to the home page</a></p>
  </main>
</body>
</html>
```

The `[response-time]` is customized per vertical: "within the hour" for plumbers and electricians (emergency work), "within one business day" for painters and fencers (non-urgent), "within 24 hours" as a safe default.

The phone number appears with a `tel:` link so it's tap-to-call on mobile.

### Phase 7 Static Forms verification

**[SKILL]** Before reporting deployment complete, Phase 7 verifies the contact form is wired correctly:

1. Open `contact.html` (or the contact section of `index.html` if contact is inline)
2. Verify `form action="https://api.staticforms.xyz/submit"` is present
3. Verify `<input type="hidden" name="accessKey" value="sf_e0e200934d4f36c17a10d00c">` is present with the exact key
4. Verify `<input type="hidden" name="subject"` contains the real business name, not placeholder
5. Verify `<input type="hidden" name="redirectTo"` points to the deployed preview URL with `/thanks.html` suffix
6. Verify `<input type="hidden" name="honeypot"` exists with `display:none`
7. Verify `phone` field has `required` attribute
8. Verify `thanks.html` exists in the deployed site root
9. Verify at least one service option in the dropdown matches a Phase 2 captured service (not placeholder)

If any check fails, Phase 7 fails and reports the specific gap. Do not deploy a broken contact form.

### Submission volume monitoring

**[OPS]** Static Forms' free tier is 500 submissions/month across the account. At 30 active sites each averaging 2-3 submissions/month, GRM uses about 60-90 of the 500 monthly allowance. Safe margin.

If GRM's active site count approaches 100 and monthly submissions exceed 300, consider either:

- Upgrading the Static Forms paid tier (check current pricing)
- Splitting the account into multiple API keys for billing isolation
- Moving heavy-volume clients to a dedicated backend (e.g., a client with 20+ submissions/month might warrant a custom form handler that tracks leads in a database)

For v0.7 scale (target: 10-30 clients), the free tier is sufficient and this is not a concern.

---

## Phase 7 verification checks

**[SKILL]** Before marking Phase 7 complete and handing off to Phase 8, run these verification checks. Each is a hard gate.

### Check 7.1: Deployment returned a URL

The Vercel CLI output contains a line starting with `https://` that ends in `.vercel.app`. Capture this URL.

### Check 7.2: URL returns 200

```bash
curl -I [captured-url]
```

The first line of the response headers must be `HTTP/2 200` or `HTTP/1.1 200 OK`.

### Check 7.3: Homepage contains business name

```bash
curl -s [captured-url] | grep -c "[business name]"
```

The count must be at least 3 (business name appears in at least 3 places: title, header, footer at minimum).

### Check 7.4: Homepage contains expected phone number

```bash
curl -s [captured-url] | grep -c "[phone with area code]"
```

The count must be at least 2 (phone appears in header and footer at minimum).

### Check 7.5: Critical pages resolve

For each of the required pages from Phase 5 (`about.html`, `services.html`, `testimonials.html`, `contact.html`), verify the page returns 200:

```bash
curl -I [captured-url]/about.html
curl -I [captured-url]/services.html
curl -I [captured-url]/testimonials.html
curl -I [captured-url]/contact.html
curl -I [captured-url]/thanks.html
```

### Check 7.6: robots.txt and sitemap.xml are reachable

```bash
curl -s [captured-url]/robots.txt | grep -c "Allow"
curl -s [captured-url]/sitemap.xml | grep -c "<urlset"
```

Both counts must be at least 1.

### Check 7.7: Contact form markup verification

Parse `contact.html` from the deployed site and verify the Static Forms wiring (see Static Forms verification section above).

### Check 7.8: Schema markup validates

```bash
curl -s [captured-url] | grep -A 50 'application/ld+json'
```

Extract the JSON-LD block and verify it parses as valid JSON. The skill does not need to run a full Schema.org validator; Phase 5.5 already validated before injection. This check is just a safety net to catch any post-deployment content corruption.

### Check 7.9: Lighthouse mobile smoke (optional but recommended)

If Lighthouse CLI is available locally, run a quick mobile audit:

```bash
lighthouse [captured-url] --only-categories=performance,seo,best-practices --emulated-form-factor=mobile --output=json --output-path=./lighthouse-report.json --quiet
```

Parse the JSON for:

- LCP (Largest Contentful Paint) under 2.5 seconds
- SEO score 95+
- Performance score 85+

If the check is not available in the deployment environment, skip it and let Ron run it manually as part of the six-check self-test.

### Check 7.10: Stale-slug verification (post-deploy)

Grep the deployed project directory for any `.vercel.app` reference that does not match the final deployed alias. This is the post-deploy safety net for Bug 5 — Step 2.5 should have reconciled all stale references before deployment, but this check catches anything that slipped through.

```bash
FINAL_ALIAS="[final-project-name].vercel.app"
grep -rn '\.vercel\.app' *.html sitemap.xml robots.txt llms.txt 2>/dev/null | grep -v "$FINAL_ALIAS"
```

Expected output: zero lines. Every `.vercel.app` reference in the project should match the deployed alias exactly.

If any stale reference is found: fix the affected file, redeploy with `vercel --prod --yes --name [final-project-name]`, and re-run this check. The most critical artifact to verify is the form `redirectTo` — a stale value there sends every form submission to a 404 thank-you page.

### If any Phase 7 check fails

**[SKILL]** Do not mark deployment complete. Report the specific failure to Ron with the captured URL, the failing check, and any relevant curl output. Options at that point:

1. Fix locally and redeploy to the same project name (subsequent `vercel --prod` deployments update the existing project)
2. Roll back to the previous deployment via `vercel rollback` (only if there was a previous good deployment)
3. Delete the project and restart Phase 5 if the failure is structural

Do not proceed to Phase 8 until Phase 7 passes cleanly.

---

# PART 2 — CLIENT LIFECYCLE PLAYBOOK (POST-SALE OPERATIONS)

Everything in this part is **[OPS]** work. It runs outside the skill, either manually or via Ron directing Claude Code through specific operations. The skill does not automatically execute any of this.

The lifecycle of a prospect that converts to a paying client has roughly six stages:

1. **Signing handshake** — agreement signed, payment processed, transition from "preview" to "client"
2. **Custom domain migration** — preview URL moves to the client's real domain (if they have one) or a new domain GRM registers on their behalf
3. **Onboarding checklist** — Bing Places, Google Business Profile, AI crawler access verification, monitoring setup
4. **Steady-state hosting** — monthly recurring relationship, update requests, quarterly content refresh
5. **Renewal or buyout** — the client either renews monthly or exercises the one-time buyout option
6. **Offboarding** — if the client leaves, how the handoff works cleanly

Each stage has its own section below.

## Stage 1: Signing handshake

**[OPS]** When a prospect says yes to the offer on a sales call, Ron must be able to send them the service agreement and payment link within 60 seconds. This is the single most time-sensitive moment in the entire lifecycle. Hesitation kills deals.

### The 60-second handshake

1. Prospect says yes on the call
2. Ron confirms pricing tier and buyout vs monthly (Elevate $1,000 setup + $250/mo or $1,500 buyout, Launch $500-650 setup + $100/mo or $800 buyout)
3. Ron sends the service agreement link via text or email
4. Ron sends the Stripe payment link for the setup fee
5. Prospect signs the agreement and pays the setup fee
6. Ron confirms receipt and promises the site will be on their domain within the agreed timeline

### Prerequisites for the handshake

The following must exist BEFORE the first sales call. These are still on the follow-up list as of the current session state:

- [ ] Service agreement PDF (Tier 1 Elevate version)
- [ ] Service agreement PDF (Tier 2 Launch version)
- [ ] Pricing one-pager PDF
- [ ] Stripe account active and linked to GRM business checking
- [ ] Six Stripe payment links (setup x2, monthly x2, buyout x2) tested and saved in phone quick-access notes
- [ ] HubSpot pipeline configured with "Signed" stage and deal record creation workflow
- [ ] Preview URL from Phase 7 ready to reference during the call

Without these, the handshake stalls and the deal dies.

### HubSpot deal record creation

**[OPS]** Once payment is confirmed, Ron creates a HubSpot deal record with:

- Contact record linked (the prospect's name, phone, email, business name)
- Deal stage: "Signed"
- Deal amount: setup fee + first month recurring (or buyout amount)
- Custom properties: Preview URL, Pricing tier, Buyout or Monthly, Signed date
- Attached files: signed service agreement PDF, payment confirmation

The HubSpot deal is the source of truth for the client's state through the rest of the lifecycle. If HubSpot says "Signed," the client is signed. If HubSpot doesn't have a deal record, no work happens on that client's site.

This discipline prevents the classic small-business mistake of losing track of who paid and who didn't. At 1-5 clients it feels like overkill. At 30 clients it is the difference between a business and a mess.

### Transition the prospect folder to client status

**[OPS]** Once signed, the prospect's folder in `~/grm-sites-prospects/[business-slug]/` gets marked as a client. Two things happen:

1. Add a `client-status.json` file to the folder with the signing date, tier, deal type (monthly or buyout), and HubSpot deal ID
2. Rename the folder OR leave it in place and rely on `client-status.json` as the marker

For v0.7, leave the folder in place under `~/grm-sites-prospects/`. Do not create a separate `~/grm-sites-clients/` tree. The split adds complexity without benefit at current scale. At 20+ active clients, consider a naming convention or a split directory, but not yet.

The `client-status.json` structure:

```json
{
  "status": "signed",
  "signedDate": "2026-04-09",
  "tier": "launch",
  "dealType": "monthly",
  "hubspotDealId": "12345678",
  "servicePlan": {
    "setupFee": 500,
    "monthlyFee": 100,
    "buyoutOption": 800
  },
  "previewUrl": "https://tandf-electric-grm.vercel.app",
  "productionDomain": null,
  "migrationScheduledDate": null,
  "notes": ""
}
```

Once the custom domain migration completes (Stage 2), `productionDomain` is updated with the real domain and `status` changes to `live`.

---

## Stage 2: Custom domain migration

**[OPS]** Most clients want their site on their real domain, not on a Vercel subdomain. Migration is the process of pointing their domain (existing or newly registered) at the Vercel project and configuring SSL, redirects, and production DNS. Executed manually by Ron, optionally with Claude Code running specific CLI commands.

### Migration scenarios

There are four common scenarios:

1. **Client has an existing domain and an existing site.** Most common. Example: client has `tfelectric.com` with an old WordPress site. Migration replaces the WordPress site with the GRM site on the same domain.
2. **Client has an existing domain but no existing site.** Rare but clean. Example: client registered `tfelectric.com` years ago but never built a site. Migration just points the domain at Vercel.
3. **Client has no existing domain.** GRM registers the domain on the client's behalf (or walks the client through registration). Migration then points the new domain at Vercel.
4. **Client wants a new domain alongside their existing one.** Example: client has `oldname.com` but wants to launch `newname.com`. Migration sets up the new domain and optionally sets up a 301 redirect from the old one.

Each scenario has different steps. The core mechanic (pointing DNS at Vercel) is the same. The surrounding steps differ.

### Scenario 1: Existing domain, existing site

**[OPS]** Most common scenario. Requires careful sequencing to avoid downtime.

**Step 1: Pre-migration audit of the existing site.** Before touching anything, capture what the client currently has:

```bash
# Capture current DNS
dig [client-domain] A +short
dig [client-domain] AAAA +short
dig [client-domain] CNAME +short
dig www.[client-domain] A +short
dig www.[client-domain] CNAME +short

# Capture current MX records (email - MUST be preserved)
dig [client-domain] MX +short

# Capture current TXT records (SPF, DKIM, DMARC, verification - MUST be preserved)
dig [client-domain] TXT +short

# Capture current NS (who hosts their DNS?)
dig [client-domain] NS +short
```

**Step 2: Identify the email host.** Look at the MX records. If the client uses Google Workspace (`aspmx.l.google.com`), Microsoft 365 (`*.mail.protection.outlook.com`), or another hosted email provider, the MX records MUST be preserved exactly. Changing them by accident will break the client's email, which is a business-ending event for the relationship.

Document the MX and TXT records in the client's `client-status.json` under a `preservedDnsRecords` key before any changes.

**Step 3: Inventory URLs on the existing site.** If the client's old site has pages that rank in Google, those URLs need to either exist on the new site or have 301 redirects to the equivalent new page. Use a tool like `xml-sitemaps.com` or a command-line crawler to enumerate the old site:

```bash
# Using wget recursive crawl to list URLs
wget --spider --recursive --no-verbose --no-directories \
  --no-parent --accept=html,htm [client-domain] 2>&1 \
  | grep -Eo 'http[s]?://[^ ]+' | sort -u > old-urls.txt
```

Map each URL in `old-urls.txt` to either an equivalent URL on the new site or to the new homepage (for pages that don't have equivalents). This becomes the 301 redirect map.

**Step 4: Add the custom domain to the Vercel project.**

```bash
cd ~/grm-sites-prospects/[business-slug]
vercel domains add [client-domain]
vercel domains add www.[client-domain]
```

Vercel will output the required DNS configuration for verification. It will be either an A record pointing to a specific IP, an ALIAS/ANAME record, or a CNAME depending on whether the client's DNS provider supports apex CNAMEs.

**Step 5: Configure redirects in vercel.json.** Add the 301 redirect map to the prospect folder's `vercel.json`:

```json
{
  "redirects": [
    {
      "source": "/old-page-slug",
      "destination": "/new-page-slug",
      "permanent": true
    },
    {
      "source": "/another-old-url",
      "destination": "/",
      "permanent": true
    }
  ],
  "cleanUrls": true,
  "trailingSlash": false
}
```

`permanent: true` produces a 301 redirect (which tells Google and AI crawlers that the old URL has permanently moved and they should update their index). Without `permanent: true`, Vercel produces a 302 temporary redirect, which is wrong for migration.

**Step 6: Redeploy with the updated vercel.json.**

```bash
vercel --prod --yes
```

Vercel will update the existing project with the new redirect configuration.

**Step 7: Set up the DNS changes in the client's DNS provider.** This is where Ron walks the client through logging into their DNS provider (GoDaddy, Namecheap, Cloudflare, whoever hosts their DNS) and making the changes Vercel specified. Ron should be on screen-share or a phone call for this. Do not let the client improvise. Specific changes:

1. Remove the old A record pointing to the old web host
2. Add the new A record pointing to Vercel's IP (or the CNAME Vercel provided)
3. Update the www CNAME if needed
4. **DO NOT TOUCH** the MX records (email)
5. **DO NOT TOUCH** the TXT records that are SPF/DKIM/DMARC (email authentication)
6. **DO NOT TOUCH** any TXT records that are domain verification for services the client uses (e.g., Google Workspace verification, Microsoft 365 verification)

**Step 8: Wait for DNS propagation.** DNS changes take between 5 minutes and 24 hours to propagate globally, depending on the TTL of the old records. Typically 30-60 minutes for most networks. During propagation, some users will see the new site and some will see the old site.

Use `dig` to confirm the new A record is resolving:

```bash
dig [client-domain] A +short
# Should return Vercel's IP, not the old host's IP

dig @8.8.8.8 [client-domain] A +short
# Double-check via Google's public DNS
```

**Step 9: Verify SSL is provisioned.** Vercel automatically provisions a Let's Encrypt SSL certificate once DNS is pointing at their infrastructure. Verify:

```bash
curl -I https://[client-domain]
# Should return 200 OK with a valid SSL cert
```

If the SSL cert isn't provisioning after 30 minutes, check the Vercel dashboard under Project → Settings → Domains for any verification errors.

**Step 10: Update the Static Forms redirectTo URL.** The contact form's `redirectTo` hidden field was set to the preview URL during Phase 7. Update it to point to the custom domain:

```html
<input type="hidden" name="redirectTo" value="https://[client-domain]/thanks.html">
```

Redeploy with the updated value.

**Step 11: Update profile.json and client-status.json.** Record the production domain, migration date, and any relevant notes. The `previewUrl` stays in profile.json as a historical reference but is no longer the primary URL.

**Step 12: Submit the new sitemap to Google Search Console and Bing Webmaster Tools.** These are covered in Stage 3 (Onboarding checklist) but initial submission happens here.

### Scenario 2: Existing domain, no existing site

**[OPS]** Easier than Scenario 1. Steps 1-2 are shorter (no old site to inventory), Steps 3 and 5 are skipped (no redirect map needed), everything else is identical.

### Scenario 3: No existing domain

**[OPS]** Additional work on top of Scenario 2. Ron either:

1. Walks the client through registering a domain on their own registrar (Namecheap, Google Domains/Squarespace Domains, Cloudflare Registrar). Ron should recommend a registrar but the domain is registered under the client's name, not GRM's.
2. Registers the domain on GRM's account as a service (charged back to the client or included in the setup fee). Document this clearly in the service agreement so ownership is unambiguous.

**Strong recommendation:** Domains should always be in the client's name, not GRM's. A registrar-owned domain is a client retention trap: the client can't leave easily because they don't technically own their own domain. This creates a relationship dependency that is bad for both parties in the long run.

If Ron must register on the client's behalf for convenience, the domain should be moved to the client's own registrar account within 60 days of signing. Document this in the agreement.

### Scenario 4: New domain alongside existing

**[OPS]** Runs Scenario 1 or 2 on the new domain, plus sets up a 301 redirect from the old domain to the new one. The old domain's DNS needs to be reconfigured to point at a service that serves the redirect. Easiest option: add the old domain to the same Vercel project as an additional domain, then configure `vercel.json` to 301-redirect all requests from the old domain to the new domain.

### Migration verification checklist

After migration, verify all of the following before declaring the client "live":

- [ ] `https://[client-domain]` returns 200 with the GRM site content
- [ ] `https://www.[client-domain]` returns 200 or 301-redirects to the canonical version
- [ ] SSL certificate is valid (no browser warnings)
- [ ] MX records are unchanged (email still works — test by sending Ron an email to the client's address)
- [ ] All pages from Phase 5 resolve (`/about`, `/services`, `/testimonials`, `/contact`)
- [ ] `robots.txt` and `sitemap.xml` are reachable and now contain the custom domain URLs
- [ ] Schema markup has been updated to reference the custom domain in all `@id`, `url`, and `sameAs` fields
- [ ] Static Forms `redirectTo` points to the custom domain
- [ ] 301 redirects from any old URLs resolve correctly
- [ ] `client-status.json` updated with `productionDomain` and `status: "live"`
- [ ] HubSpot deal record moved to "Live" stage

---

## Stage 3: Client onboarding checklist

**[OPS]** Once the site is live on the custom domain, the following onboarding tasks must be completed within the first two weeks. These are not automated by the skill. They are Ron's checklist.

### The 12-step onboarding checklist

**1. Google Business Profile verification and optimization.** Confirm the client has claimed their Google Business Profile. If not, walk them through claiming it. Once claimed, optimize:

- Business name matches the site header exactly (spelling, punctuation, casing)
- Category set to the most specific trade (e.g., "Plumber" not "Home services provider")
- Service area set to Marion County cities (Ocala, Dunnellon, Belleview, etc.)
- Hours of operation match the site footer
- Phone number matches the site (E.164 format in schema, display format in the listing)
- Website field points to the new custom domain
- At least 6 high-quality photos uploaded (pulled from the same photo set Phase 3 captured)
- Services list populated with real services from Phase 2

Google Business Profile is the primary signal for Google Gemini citations per the Cowork research. Skipping this step leaves meaningful Gemini citation weight on the table.

**2. Bing Places for Business claiming and optimization.** The Cowork research flagged Bing Places as a structural advantage because most contractors skip it entirely. Bing Places is the direct feeder for Microsoft Copilot citations.

Steps:
- Visit `bingplaces.com`
- Search for the client's business
- If the listing exists (imported from other sources), claim it
- If not, create a new listing
- Populate with the same information as the Google Business Profile: name, category, hours, phone, website, service area, services
- Upload the same photos
- Verify ownership (usually via postcard or phone verification)

**3. Google Search Console setup.** Add the custom domain as a property in Google Search Console:

- Visit `search.google.com/search-console`
- Add the property (choose "Domain" not "URL prefix" for full coverage)
- Verify ownership (DNS TXT record, preferred method for domain properties)
- Submit the sitemap.xml URL under Sitemaps
- Wait 24-48 hours for initial indexing to begin

Search Console is important not just for traditional SEO but because it gives GRM visibility into crawl errors, mobile usability issues, and indexing problems that could affect AI citation.

**4. Bing Webmaster Tools setup.** Same as Google Search Console but for Bing. Visit `bing.com/webmasters`, add the site, verify ownership, submit the sitemap.

**5. AI crawler access verification.** From the Cowork research, AI crawlers must not be accidentally blocked. Verify the live site with each crawler's user agent:

```bash
curl -A "Mozilla/5.0 (compatible; GPTBot/1.0; +https://openai.com/gptbot)" -I https://[client-domain]
curl -A "Mozilla/5.0 (compatible; ClaudeBot/1.0; +claudebot@anthropic.com)" -I https://[client-domain]
curl -A "Mozilla/5.0 (compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)" -I https://[client-domain]
curl -A "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)" -I https://[client-domain]
curl -A "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" -I https://[client-domain]
```

Each should return 200. If any return 403 or 429, check `robots.txt` (should be clean from Phase 5.5) and Vercel's firewall/bot filtering settings.

Vercel has a feature called "Bot Protection" that can block crawlers. If Bot Protection is enabled for the project, disable it or explicitly allow the AI crawler user agents. This is a common accidental block.

**6. Analytics setup.** Install a privacy-respecting analytics solution. GRM recommends:

- **Plausible Analytics** ($9/month per site, or a shared account across clients) — privacy-first, no cookie banner needed, clean dashboard
- **Umami** (self-hostable, free) — if GRM wants to run its own analytics infrastructure
- **Google Analytics 4** (free) — standard option, but requires cookie consent banners for European visitors

For v0.7, recommend Plausible. It's cheap, clean, and doesn't require cookie banners. Install the tracking script in the `<head>` of every page.

Configure custom reporting for:
- Total sessions
- Sessions by source (direct, organic, AI-referred)
- AI referrer domains as a segment: `chat.openai.com`, `chatgpt.com`, `claude.ai`, `perplexity.ai`, `copilot.microsoft.com`, `gemini.google.com`
- Contact form submissions (track `/thanks.html` pageviews as a conversion)

**7. AI citation monitoring setup.** Covered in detail in the Monitoring stack section below, but the initial setup happens here. Add the client to Otterly.ai or Gauge, configure target queries (e.g., "[trade] in [city]", "best [trade] in Marion County", "emergency [trade] Ocala"), and establish a baseline measurement.

**8. Initial Google review push.** Review count and rating are citable facts. The Cowork research confirms AI systems weight review data heavily. Set up a review acquisition workflow:

- Send the client a direct Google review link (format: `https://g.page/r/[PLACE_ID]/review`)
- Ask them to text this link to their 10 most recent satisfied customers
- Set a target: 10 new reviews in the first 30 days
- Update the site's review count and AggregateRating schema weekly during the first month, then monthly

**9. Contact form test submission.** Fill out the contact form on the live site with Ron's own information and verify the submission email arrives at `ron@getrootedmedia.com`. If it doesn't, debug Static Forms before any real leads can be lost.

**10. Mobile verification on the client's actual phone.** Ask the client to open the live site on their phone and test: tap-to-call from the hero, navigate to services, submit the contact form, see the thanks page. Any friction they report gets fixed immediately.

**11. Seasonal content check.** Is there seasonal content on the homepage that needs updating for the current month? Examples:

- Q4/Q1 (Nov-Feb): lightning preparedness, freeze protection for pipes, generator pre-season maintenance
- Q2 (Mar-May): spring AC tune-ups, pre-hurricane preparation, yard cleanup
- Q3 (Jun-Aug): hurricane season messaging, emergency availability, peak season lead times
- Transition months: check that messaging isn't stale

If the Phase 2 crawl captured the wrong season's promo, update it during onboarding.

**12. Client orientation walkthrough.** A 15-minute call or video explaining:

- How the site is structured
- Where their photos, testimonials, and services live
- How to request a change (the update workflow, Stage 4)
- What the quarterly content refresh looks like
- How to check their own analytics if they want to
- Who to call if something breaks (Ron's phone, 7-day-a-week response)
- When the first invoice hits for monthly clients (30 days from signing, or whatever the service agreement specifies)

This is the handshake that turns "we sold them a site" into "they're a client." Skipping it creates a relationship where the client feels like they paid for a deliverable and has no ongoing expectation of service, which undersells the recurring value GRM is delivering.

### Onboarding timeline

All 12 steps should be complete within 14 days of the site going live. Faster is better but 14 days is the hard deadline. HubSpot should have a task reminder set for day 14 that checks off the client as "Onboarded" and moves them to the "Steady State" stage.

If any onboarding step is skipped or delayed, it tends to stay skipped forever. The habit of completing all 12 on every client is the single biggest operational discipline in GRM's service delivery.

---

## Stage 4: Steady-state hosting

**[OPS]** Once a client is onboarded, they enter the monthly recurring relationship. GRM hosts the site, responds to update requests, runs the quarterly content refresh, monitors AI citations, and invoices monthly (or has collected buyout once).

### Sales callouts — use during qualifier and closing calls

**[OPS, SALES]** The included-versus-not-included boundary is not just operational. It is the single most important sales content in this file. Ron will reference this dozens of times per week during prospect calls. Readable directly from your phone during a live call.

**When a prospect asks "what do I get for the monthly fee":**

> You get everything it takes to keep your site running, fresh, and visible. That means hosting, your contact form routing to your phone, content updates whenever you need them, a full refresh every quarter so the search engines and AI platforms keep treating your site as current, monitoring that alerts us before you notice if anything goes down, and me on call when you need something. You text me, I fix it.

**When a prospect asks "what's not included":**

> A few things worth being clear on up front. Building new pages, major redesigns, writing blog posts, managing your Google Ads, running your social media, sending email campaigns — those are separate projects, quoted separately. The monthly fee covers keeping the site you're paying for today running great and staying fresh. If you want to add something big, just ask and I'll quote it. If it's small, it's included. I'm not going to nickel-and-dime you on typos.

**When a prospect asks "how fast do you respond":**

> If it's urgent — your site's down, your contact form broke, something is wrong — I'm on it same day, usually within the hour. If it's a normal change — update a phone number, fix a typo, swap out a photo — within one business day. If it's a bigger project — add a new section or a new page — I quote it within 48 hours and we set a timeline from there.

**When a prospect says "can I just pay once and own it":**

> Absolutely. That's the buyout option. For [Elevate tier $1,500 / Launch tier $800] you get the full source code, all your assets, and a handoff period where I walk you through everything. After that you're on your own for hosting and updates. Most clients stay monthly because the updates, the refreshes, and knowing you can text me with any question are worth more than the monthly fee. But the buyout is always there if that's what works for you.

**When a prospect asks "what if I want to leave":**

> Thirty days notice and we're square. I'll send you a copy of your site code as a goodwill thing. Your domain is yours, your Google Business Profile is yours, your reviews are yours, your photos are yours. Nothing is locked up. I build the relationship on the work being good enough that you don't want to leave, not on making it hard to leave if you do.

### Response commitments (authoritative, referenced throughout)

**[OPS]** Every mention of response time in this file — in sales conversations, in the monthly-included list, in the update workflow, in the client orientation — points to this single source of truth. If the commitment needs to change, it changes here once, and every other reference inherits the new value. Do not restate response times anywhere else in the file without a cross-reference.

**Definition: what counts as an emergency**

An emergency is any of the following, verified by Ron:

- Client's site returns a non-200 status code when fetched over HTTPS (down)
- Contact form submissions are not reaching `ron@getrootedmedia.com` (broken lead capture)
- SSL certificate is expired or invalid (browser warning visible to visitors)
- Domain has stopped resolving to Vercel (DNS break)
- Site is displaying content that does not match the built site (compromise, hijack, or deployment corruption)
- Client is facing a direct business-blocking issue rooted in the site (example: a permit inspector couldn't verify license info because the page is broken)

Anything else is not an emergency, regardless of how the client describes it. A client wanting to change their phone number before a big ad campaign tomorrow morning is urgent but not an emergency. A client wanting to add a testimonial before a Monday meeting is normal. Ron's discretion, but the list above is the default.

**Response commitment table**

| Category | What it means | Acknowledge within | Resolve within |
|---|---|---|---|
| Emergency | Per definition above | 1 hour (day or night) | Same day |
| Urgent | Client has a time-bound reason but site is functional | 4 hours (business hours) | Next business day |
| Quick request | Small change, no time pressure | 1 business day | 2 business days |
| Standard request | Moderate change requiring some thought | 1 business day | 5 business days |
| Project | Scoped change requiring quote | 4 hours (business hours) for acknowledgment, 48 hours for quote | Timeline negotiated |

**Business hours definition:** Monday through Friday, 7am to 7pm Eastern. Outside business hours, only Emergencies get response. Urgent and Quick requests received after 7pm get acknowledged the next business day.

**Ron's discretion clause:** For specific clients who consistently generate revenue and behave professionally, Ron can upgrade their informal responsiveness without changing the written commitments. But the written commitments are the floor. Never below.

**Cross-references:** Stage 4 "What GRM provides monthly" item 10 points here. Stage 4a "Turnaround targets" points here. Stage 3 client orientation step 12 points here. Sales callouts above reference this table conversationally.

### What GRM provides monthly

The monthly fee covers:

1. **Vercel hosting** — unlimited bandwidth under Vercel Hobby/Pro tier (currently Hobby is sufficient at this scale; upgrade to Pro if bandwidth exceeds Hobby limits)
2. **Domain DNS management** (if GRM registered the domain; otherwise client-managed)
3. **SSL certificate auto-renewal** (Vercel handles this automatically)
4. **Contact form backend** (Static Forms, no per-client cost)
5. **Content updates** — reasonable changes within the monthly scope (see update workflow below)
6. **Quarterly content refresh** — proactive updates every 13 weeks (freshness signal)
7. **AI citation monitoring** — passive monitoring via Otterly/Gauge
8. **Analytics reporting** — monthly summary (delivered automatically from Plausible or manually curated)
9. **Uptime monitoring** — automated alerts if the site goes down (covered in Monitoring stack below)
10. **Client support** — per the Response commitments table above. Emergency, urgent, quick, standard, and project categories with specific acknowledge and resolve commitments. This is the single authoritative definition of GRM's response promise to clients.

### What GRM does NOT provide monthly

The following are NOT included in the monthly fee and are billable add-ons or explicitly out of scope:

- **Major redesigns** — rebuilding the site with new layouts, new sections, or new functionality is a new project, not an update
- **New page creation** — adding a new service page or location page is an add-on charge ($150-300 depending on complexity)
- **Blog post writing** — monthly doesn't include content marketing; that's a separate service
- **SEO consulting calls** — quick questions over text are free; hour-long strategy calls are billable
- **Social media management** — not part of the web services offering (parked for future upsell)
- **Paid advertising management** — not part of the web services offering
- **Email marketing** — not in scope
- **Graphic design work beyond the site** — flyers, business cards, signage are separate

Set these expectations clearly during the Stage 3 client orientation walkthrough. The most common source of client friction at the 30-day mark is scope ambiguity: the client assumes monthly includes "everything" and Ron hasn't set the boundary. The 12-step orientation is where that boundary gets drawn.

---

## Stage 4a: Client update workflow

**[OPS]** Clients will request changes. The workflow for handling updates needs to be fast, predictable, and scalable.

### The update request flow

1. **Client contacts Ron** via text, email, or phone
2. **Ron logs the request** in HubSpot as a task on the client's deal record with the description, priority, and request date
3. **Ron categorizes the request** as Quick, Standard, or Project
4. **Ron executes (or schedules)** based on category
5. **Ron confirms completion** with the client
6. **HubSpot task marked complete** with resolution notes

### Request categories

**Quick (same-day or next-day turnaround):**
- Update a phone number
- Update hours of operation
- Fix a typo
- Update a price in a service description
- Update the featured promotion
- Update review count and rating
- Add/remove a testimonial (if real)

**Standard (2-5 business day turnaround):**
- Add a new testimonial with photo
- Swap out a batch of photos
- Update an FAQ answer
- Change a service description more substantially
- Update contact form service dropdown with new services
- Update seasonal content on the homepage

**Project (quoted separately, not covered by monthly):**
- Add a new page
- Add a new section to an existing page
- Restructure the nav
- Add new functionality (booking form, calculator, etc.)
- Rebrand (new colors, new fonts, new logo)
- Migrate to a new domain

### The execution path for Quick and Standard requests

**[OPS + Claude Code]** Ron opens a Claude Code session in the client's prospect folder and describes the change:

```
In ~/grm-sites-prospects/tandf-electric/, update the featured promotion 
on the homepage from "$450 whole house surge arrestor special" to 
"$395 whole house surge arrestor special for April only". Update 
services.html surge protection description to reference the new price.
Redeploy.
```

Claude Code:
1. Makes the edits in the prospect folder
2. Updates profile.json to reflect the change
3. Runs Phase 6 verification checks against the modified build
4. If Phase 6 passes, redeploys with `vercel --prod --yes`
5. Reports the deployment URL and a summary of changes to Ron

Ron verifies the change is live, confirms with the client, and marks the HubSpot task complete.

### Turnaround targets

- **Quick requests:** acknowledge within 2 hours, complete within 24 hours
- **Standard requests:** acknowledge within 4 hours, complete within 5 business days
- **Project requests:** acknowledge within 4 hours, quote within 48 hours, timeline negotiated

Missing these targets is the fastest way to erode client trust. Tracking them in HubSpot with task due dates is non-negotiable at scale.

---

## Stage 4b: Quarterly content refresh protocol

**[OPS]** Every 13 weeks, each client site gets a proactive content refresh. This is non-negotiable and is what keeps the freshness signal strong for AI citations per the Cowork research finding that 50 percent of AI-cited content was updated within 13 weeks.

### What gets refreshed every quarter

1. **Review count and AggregateRating** — pull the current Google review count and rating, update the hero stats bar, update the testimonials page summary, update the LocalBusiness schema AggregateRating
2. **Recent project or seasonal photo** — swap one photo on the homepage or services page for a more recent project shot (if the client has provided one) OR rotate the hero background image to reflect the current season
3. **Seasonal FAQ addition or rotation** — add or rotate one FAQ based on the current quarter (e.g., Q4 "How do I protect my pipes during a Florida freeze?", Q2 "Do you offer pre-hurricane electrical inspections?")
4. **Featured promotion update** — if the client has a current promotion, update the promo bar and the promotion schema; if not, remove the promo bar entirely rather than leaving a stale promo
5. **Sitemap lastmod dates** — refresh `<lastmod>` on every changed page in the sitemap
6. **Schema `dateModified`** — update the dateModified field in LocalBusiness and Service schemas
7. **Copyright year in footer** — verify it reflects the current year
8. **One fresh content block somewhere** — at minimum, one paragraph of fresh content is added, updated, or reworked on the site, ideally in the first 30 percent of a page (remember the 44.2 percent citation weight)

### The quarterly refresh execution

**[OPS + Claude Code]** Ron opens a Claude Code session for each client in sequence:

```
In ~/grm-sites-prospects/[client-slug]/, run the quarterly content refresh 
workflow. Current date is [date]. Previous refresh was [last-refresh-date]. 
Check Google Places API for updated review count and rating. Update the 
hero stats bar, the testimonials page header, and the LocalBusiness schema 
AggregateRating with the new numbers. Update the footer copyright year. 
Rotate the seasonal FAQ based on Q[1/2/3/4]. Redeploy and confirm the 
new lastmod date appears in the sitemap.
```

Target duration per client refresh: 10-15 minutes with Claude Code executing. At 30 active clients, the full quarterly refresh takes one focused day per quarter. That is a known cost and must be scheduled on the calendar.

### Tracking refreshes

HubSpot deal records should have a custom property `lastRefreshDate` that gets updated on every refresh. A HubSpot workflow sends Ron a reminder 90 days after the last refresh to schedule the next one. Clients that miss their refresh window get flagged.

### Making refreshes visible to clients

The quarterly refresh should be communicated to clients so they know GRM is actively working for them. A simple monthly or quarterly update email:

> Hey [client first name],
>
> Quick update on your site: this month we refreshed your Google review count (now showing [X] stars from [Y] reviews), updated the [seasonal FAQ / featured promotion / photo], and confirmed all your pages are indexing cleanly with Google, Bing, and the AI search platforms.
>
> [One line about any interesting metric: "You had X contact form submissions this month" or "Your site was cited by Perplexity for a search about 'plumber in Ocala' last week"].
>
> If you want to push anything new — a new testimonial, a current promotion, updated photos — just text me.
>
> Ron

This kind of communication is the difference between the client perceiving the monthly fee as "paying for nothing" versus "getting ongoing value." Even if the update is small, the act of communicating it matters.

---

## Monitoring stack deployment

**[OPS]** Post-onboarding, every client site is added to the GRM monitoring stack. The stack has four layers:

### Layer 1: Uptime monitoring

Purpose: alert Ron if a site goes down.

Tool: **UptimeRobot** (free tier: 50 monitors at 5-minute intervals) or **Better Uptime** (paid but slicker)

Setup: add each custom domain as an HTTP(S) monitor. Alert via email and SMS to Ron's phone. Set the alert delay to "after 2 consecutive failures" to avoid noise from brief network blips.

### Layer 2: Analytics

Purpose: track traffic, sources, and conversions.

Tool: **Plausible Analytics** (recommended) or Google Analytics 4 (if the client insists)

Setup: install the tracking script in the `<head>` of every page. Configure custom events for contact form submissions (track `/thanks.html` pageviews). Add AI referrer domains as a custom segment.

### Layer 3: AI citation monitoring

Purpose: track whether the client is being recommended by AI assistants for target queries.

Tool: **Otterly.ai** or **Gauge** (budget-dependent; start with free trials)

Setup: add the client business name and website. Configure 5-10 target queries per client (e.g., "plumber in Ocala", "emergency electrician Marion County", "licensed roofer Dunnellon FL"). Check weekly during the first month, monthly thereafter.

### Layer 4: Search presence

Purpose: monitor traditional search indexing, crawl errors, and ranking for key queries.

Tool: **Google Search Console** (free) + **Bing Webmaster Tools** (free)

Setup: complete during Stage 3 onboarding step 3 and 4. Check monthly for crawl errors, indexing issues, and search impressions.

### The monthly monitoring report

Once all four layers are deployed, Ron can produce a monthly client report pulled from these sources. Template:

```
[Client name] — [Month] [Year] summary

Uptime: [X]% (target 99.9%)
Sessions: [total] ([%] change from last month)
Top source: [direct/organic/AI/paid]
Contact form submissions: [count]

AI citations:
- ChatGPT: [cited Y/N for target queries]
- Claude: [cited Y/N for target queries]
- Perplexity: [cited Y/N, count]
- Copilot: [cited Y/N]
- Gemini: [cited Y/N]

Google search impressions: [count] ([%] change)
Top query: [query]

This month we updated: [summary of any changes]

Anything you'd like us to change or add next month?
```

At 5-10 clients, producing this report manually is fine. At 20+ clients, automate the pull (Plausible has a JSON API, Otterly has one, Search Console has one) and have Claude Code format the report per client.

---

## Stage 5: Renewal or buyout

**[OPS]** Clients on the monthly plan continue month-to-month. Clients on the buyout plan paid once and own the code.

### Monthly plan renewal

Nothing happens automatically. The monthly Stripe subscription charges each month. As long as payment clears, the client stays active. If payment fails, Stripe sends automated retry notifications for 7-14 days, then flags the account as delinquent.

Ron's workflow on delinquent accounts:

1. Stripe webhook (or manual Stripe dashboard check) flags the failed payment
2. Ron texts the client to let them know and offer to update their card
3. If payment isn't resolved within 14 days, the site is not deleted but service is paused (see Offboarding below)
4. HubSpot deal stage changes to "Delinquent"

### Buyout option exercise

Monthly clients can exercise the buyout option at any time. Pricing:

- **Elevate tier:** $1,500 buyout
- **Launch tier:** $800 buyout

What the buyout includes:

- Full source code (the prospect folder in a zip file or a git repo the client owns)
- All photo assets
- Domain transfer (if GRM registered it) or continued DNS management (if client owns it)
- 30-day handoff period where GRM answers questions about the code
- The client takes over hosting (they can keep it on Vercel under their own account, move to Netlify, or move to traditional hosting)

What the buyout does NOT include:

- Ongoing GRM maintenance or updates
- Ongoing AI citation monitoring
- Quarterly content refreshes
- Continued support calls

The client is free to come back for update projects in the future, billed at GRM's project rate.

### Buyout execution

1. Client requests buyout, payment processed via Stripe buyout link
2. Ron creates a fresh zip of `~/grm-sites-prospects/[client-slug]/` (excluding any sensitive files like `.env`) OR creates a private GitHub repo under the client's account with the full codebase
3. Ron sends the client a handoff document (template TBD in v0.8) with: where the code lives, how to edit it, how to redeploy, how to transfer the domain, who to call for future help
4. HubSpot deal stage changes to "Bought Out"
5. GRM stops all monitoring and quarterly refresh tasks for this client
6. The Vercel project is left live but management access is transferred to the client's Vercel account OR the code is fully migrated to the client's own Vercel account

The client retains the relationship even after buyout; future work is just billed differently.

---

## Stage 6: Offboarding

**[OPS]** If a client wants to leave entirely (not buyout, just stop), offboarding is the clean-handoff process.

### Reasons a client might leave

- Business closure (sad but it happens)
- Business sold to new owners who have a different vendor
- Client can't afford the monthly fee anymore
- Client chose a competing vendor (rare if GRM is delivering)
- Client went dark and stopped paying (delinquency)

### Offboarding steps

1. **Final invoice cleared or written off.** Any outstanding balance is either paid or written off.
2. **Client notified in writing of the offboarding date.** 30-day notice is standard.
3. **Final site snapshot delivered.** Client receives a zip of the final site code as a goodwill gesture (not required by the agreement, but the right thing to do). This is not a buyout — they don't own the domain transfer, they don't get handoff support, they just get a copy of the code they can do whatever they want with.
4. **Vercel project deleted** on the offboarding date. The domain stops resolving unless the client has already migrated it elsewhere.
5. **Google Business Profile and Bing Places left with the client.** These were the client's accounts, not GRM's. GRM removes any management access but does not delete the listings.
6. **Analytics and monitoring stopped.** Client is removed from Otterly/Gauge, Plausible, UptimeRobot.
7. **HubSpot deal record closed as "Offboarded".** Keep the record for historical reference and potential future re-engagement.
8. **Prospect folder archived.** Move `~/grm-sites-prospects/[client-slug]/` to `~/grm-archive/[client-slug]-offboarded-[date]/` for cold storage. Do not delete; keeping the archive lets GRM re-activate quickly if the client returns.

### The delinquent client path

If a client stops paying without communicating, the path is:

1. Day 0: payment fails, Stripe retries
2. Day 7: second Stripe retry fails, Ron texts the client
3. Day 14: third retry fails, Ron texts again with a clear "site will be paused at day 30 if not resolved"
4. Day 21: fourth retry fails, Ron calls the client and leaves a voicemail
5. Day 30: site paused (Vercel project set to redirect to a static "site under maintenance" page or taken offline)
6. Day 60: if still no communication or resolution, offboarding steps 1-8 execute and the relationship ends

This is not fun and should be rare. But at 20-30 clients, expect 1-2 delinquencies per year.

---

## White-label scale architecture

**[OPS + SKILL]** This section covers how the infrastructure scales from the current state (1 flagship, T&F) to 30+ active clients without breaking.

### The current state (April 2026)

- 1 flagship preview deployed (T&F Electric at `tandf-electric.vercel.app`)
- Skill v0.7 installed
- One Vercel account under `ron-7323` team
- One Static Forms account with one API key
- One Google Places API key (needs rotation per working notes)
- HubSpot account (pipeline setup pending)
- Local folder structure at `~/grm-sites-prospects/`
- GitHub repo `grm-automations` (private, for skill and playbook files; prospect data NOT committed)

### The 10-client target

At 10 active clients, no architectural changes are needed. The current stack handles 10 clients cleanly.

Disciplines to maintain at 10 clients:

- Every client has a `client-status.json` in their prospect folder
- Every client has a HubSpot deal record in "Live" or later stage
- Every client is in the monitoring stack (uptime, analytics, AI citation, search presence)
- Quarterly content refresh is scheduled on Ron's calendar
- No client data is committed to the public `grm-automations` repo

### The 30-client ceiling

At approximately 30 active clients, the manual workflow starts to strain. Signs that the ceiling is being hit:

- Quarterly refresh takes more than a full workday (means the per-client time must decrease via automation)
- Update requests are backing up (means the request intake and execution workflow needs a ticket system beyond HubSpot tasks)
- Ron is forgetting which client needs what (means the central dashboard needs to show per-client status at a glance)
- Monitoring reports take hours to assemble (means the monthly report generation must be automated)

Architectural changes needed at or before 30 clients:

1. **Automated quarterly refresh workflow.** A Claude Code command that iterates over every client folder, runs the refresh procedure, and produces a summary report. Drastically reduces per-client refresh time.
2. **Automated monthly monitoring report generation.** Pulls data from Plausible, Otterly, Search Console via their APIs and formats into the report template automatically.
3. **Client dashboard.** A private web page (or Notion page, or Airtable view) that shows all clients at a glance: status, last refresh date, last contact form submission, uptime, monthly invoice status. Updated daily from a script that runs against HubSpot, Plausible, and Stripe APIs.
4. **Ticket system beyond HubSpot tasks.** HubSpot tasks work for 10 clients. At 30, a dedicated ticket system (Linear, Shortcut, or similar) that GRM shares with clients for transparency may be worth it.
5. **Secondary team member.** At 30+ clients, Ron cannot be the only person executing updates. A second team member (virtual assistant, junior developer, or GRM hire) takes over execution while Ron handles sales and strategy.

### The 100-client future (v0.9+)

Not a v0.7 concern. But worth naming so the architecture doesn't paint itself into a corner.

At 100 clients, GRM is a real agency, not a one-person operation. The infrastructure needs:

- Multi-tenant dashboard for clients to view their own stats
- Automated client onboarding pipeline (Stripe → contract → Claude Code generation → deployment all wired together)
- CI/CD for site updates
- Backup and disaster recovery procedures
- Legal and compliance review of the service agreement terms
- A real support inbox with SLA tracking
- A team of 3-5 people

None of this is v0.7 work. It's roadmap context so the current decisions don't accidentally lock out the future. Documented in more detail in `scale-architecture.md`.

### Credential storage and secrets management

**[OPS]** As GRM scales, the secrets inventory grows. Currently tracked:

- Vercel CLI auth (stored locally in `~/.vercel`)
- Google Places API key (stored in `~/grm-sites-prospects/.env`, flagged for rotation per working notes)
- Static Forms API key (public, embedded in every form; no secrecy required)
- HubSpot API key (future, once pipeline is set up)
- Stripe API keys (future, once account is active)
- Plausible API token (future, once installed)
- Otterly/Gauge API token (future, once installed)

Storage rules:

1. **Never commit secrets to the public `grm-automations` repo.** Phase 7 and Phase 8 do not write any secrets into profile.json or any committed file.
2. **Use `.env` files for local secrets**, excluded from git via `.gitignore`.
3. **Document rotation dates in `~/.grm-secrets-rotation.md`** (local, not committed). Rotate any exposed secret within 7 days of exposure.
4. **At 30+ clients, move secrets to a password manager** (1Password Business, Bitwarden, or similar) with shared vault for GRM team members.

### Folder conventions at scale

**[OPS]** The `~/grm-sites-prospects/` directory currently holds everything: active prospects, signed clients, and the Plan B reference library. At scale, this needs structure:

```
~/grm-sites-prospects/
  .env                                # Shared secrets (gitignored)
  plan-b-reference/                   # Plan B component library
  _prospects/                         # Unsigned prospects
    [business-slug]/
      profile.json
      ...
  _clients/                           # Signed clients
    [business-slug]/
      profile.json
      client-status.json
      ...
  _archive/                           # Offboarded clients (cold storage)
    [business-slug]-offboarded-[date]/
```

The leading underscores on `_prospects`, `_clients`, and `_archive` keep the top-level folder listing clean.

**Do not reorganize to this structure in v0.7.** The T&F folder is currently at `~/grm-sites-prospects/tandf-electric/` and reorganizing now would break the skill's hardcoded paths. This is a v0.8 cleanup task when there are 3-5 clients signed and the pain of the flat structure becomes real. Noted here so it doesn't get forgotten.

---

## Phase 8 reference (post-deployment)

**[SKILL]** Phase 8 is covered in full in SKILL.md but briefly referenced here because it runs immediately after Phase 7 completes.

Phase 8 responsibilities:

1. Promote `profile-draft.json` to `profile.json` with the final `previewUrl` populated from Phase 7
2. Append an entry to `~/.claude/skills/prospect-site/LESSONS.md` if anything unusual happened during the build (this is the institutional memory loop)
3. Output the done report per the format in SKILL.md

Phase 8 does NOT perform any client lifecycle work. All Stage 1-6 operations in Part 2 of this file are triggered manually by Ron after a prospect converts, not automatically by Phase 8.

---

## What is deliberately not in v0.7

Following the same pattern as `seo-geo.md`, naming what is deferred so nothing silently drops.

### Automated client onboarding pipeline

**What it is.** The dream-state workflow where a prospect signs via Stripe, a webhook fires, Claude Code auto-runs the domain migration, onboarding checklist, and monitoring setup without Ron's involvement.

**Why v0.7 does not do this.** The onboarding checklist has 12 steps, most of which require human judgment (verifying DNS changes, confirming SSL, uploading Google Business Profile photos, running the orientation call). Automating it prematurely would produce broken handoffs. The better v0.7 play is to execute each step manually the first 10 times and document every gotcha, then automate the stable parts in v0.8.

**Roadmap.** v0.8 or v0.9, once 10+ clients have been onboarded manually and the gotchas are catalogued.

### Client self-service dashboard

**What it is.** A web portal where clients log in, see their own analytics, submit update requests, view their invoices, and manage their site without calling Ron.

**Why v0.7 does not do this.** At 1-10 clients, the ratio of Ron-to-client is close enough that direct communication is faster than self-service. A dashboard adds complexity without matching ROI. Also, contractors (the target market) are not known for loving web portals. Text-to-Ron is the native interaction mode.

**Roadmap.** v0.9+, after 30+ active clients.

### Automated review acquisition

**What it is.** A workflow where GRM automatically asks a client's recent customers for Google reviews via SMS or email, tracking responses and conversions.

**Why v0.7 does not do this.** Review acquisition at the contractor level requires integration with the client's own customer database, CRM, or POS system. Every client's system is different. Building a generic solution is a significant engineering effort. Instead, GRM walks clients through sending review requests manually during onboarding Stage 3 step 8.

**Roadmap.** v0.9+, and only if it becomes a differentiator clients are asking for.

### Multi-domain or subdomain architectures

**What it is.** Clients who want separate subdomains for different service areas (e.g., `ocala.tfelectric.com` and `dunnellon.tfelectric.com`) or separate domains for multiple business entities.

**Why v0.7 does not do this.** Single-location, single-domain contractors are the v0.7 market. Multi-domain architectures need different schema (per-location LocalBusiness entries), different sitemap structure, and different update workflows.

**Roadmap.** v0.8+ extension for specific high-value clients if the use case arises.

### Full ticket system with SLA tracking

**What it is.** A dedicated support ticket system (Linear, Freshdesk, Zendesk) with per-ticket SLA tracking, automated escalation, and client-visible ticket history.

**Why v0.7 does not do this.** HubSpot tasks are sufficient at the 10-client level. A ticket system is a 30+ client problem.

**Roadmap.** Evaluate at 20 active clients. Deploy at 30.

### Email marketing integration

**What it is.** Tying the contact form into a client's email marketing list (Mailchimp, Klaviyo, Constant Contact) so new leads are automatically added to their marketing automation.

**Why v0.7 does not do this.** Most Marion County contractors don't run email marketing. Adding integration to services they don't use is waste. If a client specifically asks, it can be a billable add-on.

**Roadmap.** On-demand add-on only.

---

## Common mistakes to avoid

- **Do not deploy to Vercel without running Phase 6 verification first.** Phase 7 preconditions are there for a reason.
- **Do not deploy to a custom domain in Phase 7.** Phase 7 always deploys to the Vercel preview subdomain. Custom domain migration happens in Part 2, Stage 2, and only after a deal is signed.
- **Do not commit prospect data or client data to the public `grm-automations` repo.** The repo is for skill files and playbook documents only. Prospect folders stay local.
- **Do not touch MX records or email-related DNS during custom domain migration.** Accidentally breaking a client's email is a relationship-ending mistake.
- **Do not skip the pre-migration DNS audit.** Always capture the current DNS state before making changes.
- **Do not register domains in GRM's name on behalf of clients.** Domains belong to the client. Registrar ownership is a retention trap that hurts both sides.
- **Do not issue a buyout without documenting the full handoff.** Buyout clients get the code, the assets, and a handoff document. Anything less is unprofessional.
- **Do not delete offboarded client folders.** Archive them. A client may return.
- **Do not promise onboarding turnaround times GRM cannot hit.** 14 days for the full 12-step checklist is the hard deadline. Do not promise 7 days.
- **Do not skip the quarterly content refresh.** The freshness signal is one of the four pillars of AI citation. Skipping refreshes erodes the competitive advantage over time.
- **Do not let delinquent clients linger.** The delinquency protocol exists for a reason. Follow it.
- **Do not deploy with a `.env` file committed.** Phase 7 should verify `.env` is in `.gitignore` and not in the deployed Vercel project.
- **Do not confuse [SKILL] and [OPS] labels.** A procedure labeled [OPS] should not be silently automated by the skill. A procedure labeled [SKILL] should not be manually executed by Ron outside the skill run.
- **Do not blur preview and production environments.** The preview URL (`[slug]-grm.vercel.app`) is for sales only. The production URL (custom domain) is what the client pays for. Never send a preview URL to an already-signed client as if it were their live site.

---

## Self-check before Phase 7 marks deployment complete

**[SKILL]** Before reporting Phase 7 done, verify:

- [ ] Vercel CLI authenticated on `ron-7323` team
- [ ] Project name follows `[business-slug]-grm` convention
- [ ] Collision check passed (or suffix applied)
- [ ] Slug reconciliation ran (Step 2.5) — if the final project name differs from the Phase 1 directory slug, all URL references were rewritten and verified zero stale references before deploy
- [ ] `vercel --prod --yes --name ...` completed with a returned production URL
- [ ] Check 7.1 through Check 7.8 and Check 7.10 passed
- [ ] Optional Check 7.9 Lighthouse smoke check ran or was skipped with notice
- [ ] Static Forms wiring verified on the live deployment
- [ ] Captured preview URL ready to hand to Phase 8
- [ ] Deployment log captured any warnings or anomalies for LESSONS.md

## Self-check before operations work declares a client "live"

**[OPS]** Before moving a HubSpot deal to the "Live" stage after custom domain migration:

- [ ] Custom domain resolves to the GRM site on HTTPS with a valid SSL cert
- [ ] www and apex both work (or one 301-redirects cleanly to the other)
- [ ] MX records are unchanged (client email confirmed working)
- [ ] All Phase 5 pages resolve on the custom domain
- [ ] robots.txt and sitemap.xml reference the custom domain
- [ ] Schema `@id` and `url` fields updated to the custom domain
- [ ] Static Forms `redirectTo` updated to the custom domain
- [ ] Any 301 redirects from old URLs tested and working
- [ ] `client-status.json` updated with `productionDomain` and `status: "live"`
- [ ] 12-step onboarding checklist scheduled (not yet complete, but scheduled)

---

## Version

deployment.md v0.7.0. Part 1 (Phase 7 preview deployment) is skill-automated and runs as part of every prospect-site build. Part 2 (client lifecycle playbook) is Ron-executed operations, not automated by the skill. The file deliberately separates the two audiences because blurring them would produce either broken automation (skill trying to run onboarding steps) or unscalable operations (Ron manually deploying preview sites). Every procedure is labeled [SKILL] or [OPS]. Last updated April 9, 2026. Next review when the first paying client goes live on a custom domain.

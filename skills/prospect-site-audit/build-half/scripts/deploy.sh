#!/usr/bin/env bash
# deploy.sh — v1.0 prospect-build preview deployment.
#
# Implements references/deployment.md Part 1 (Phase 7) end-to-end against the
# Vercel CLI scoped at ron-7323s-projects:
#
#   1. Verify preconditions (CLI auth, team scope, prospect dir present).
#   2. Resolve the canonical project name [business-slug]-grm with collision
#      handling (-grm-2, -grm-3, ...) per deployment.md L80-94.
#   3. Pre-create the Vercel project so the canonical URL is deterministic
#      (closes Bug 6A — staging-dir basename can no longer leak into the
#      project name on first deploy).
#   4. Run the slug-reconciliation gate (deployment.md Step 2.5 / L128-160):
#      grep every .vercel.app URL in the staged HTML/sitemap.xml/robots.txt/
#      llms.txt; if any differ from the final alias, rewrite to the final
#      alias before deploying. Bug 5 fix — do NOT skip.
#   5. Substitute the StaticForms placeholder accessKey in staged HTML and
#      rewrite CSS + asset paths to deploy-root-relative.
#   6. Deploy from the staging directory.
#
# All edits operate on a /tmp staging copy; the prospect-data dir and the
# build-skill repo stay clean of substituted secrets.
#
# Usage:
#   bash scripts/deploy.sh <prospect-slug> [--prod]
#
# Examples:
#   bash scripts/deploy.sh volthom            # preview deployment
#   bash scripts/deploy.sh volthom --prod     # production deployment
#
# StaticForms accessKey comes from STATICFORMS_ACCESS_KEY in the env. See
# audit-side references/deployment.md PART 1 §"Static Forms wiring" for the
# operational handling of the key.

set -euo pipefail

PROSPECT="${1:-}"
PROD_FLAG="${2:-}"

if [ -z "$PROSPECT" ]; then
  echo "Usage: bash scripts/deploy.sh <prospect-slug> [--prod]" >&2
  echo "Example: bash scripts/deploy.sh volthom --prod" >&2
  exit 1
fi

if [ -z "${STATICFORMS_ACCESS_KEY:-}" ]; then
  echo "ERROR: STATICFORMS_ACCESS_KEY env var must be set." >&2
  echo "See audit-side references/deployment.md PART 1 § Static Forms wiring" >&2
  echo "for the operational source of the per-account accessKey." >&2
  exit 1
fi

VERCEL_SCOPE="ron-7323s-projects"
SKILL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FIXTURE_DIR="$SKILL_ROOT/fixtures/$PROSPECT"
if [ ! -d "$FIXTURE_DIR" ]; then
  echo "ERROR: $FIXTURE_DIR does not exist." >&2
  exit 1
fi

# ----------------------------------------------------------------------------
# Step 1: Verify CLI environment per deployment.md L33-50.
# ----------------------------------------------------------------------------
echo "Step 1: Verifying Vercel CLI environment..."
vercel whoami >/dev/null 2>&1 || { echo "ERROR: vercel CLI not authenticated. Run 'vercel login' first." >&2; exit 1; }
vercel teams ls 2>&1 | grep -q "ron-7323" || {
  echo "ERROR: ron-7323 team not visible to this CLI auth. Check team scope." >&2
  exit 1
}

# Resolve the prospect-data directory via the fixture's `assets` symlink (the
# fixture-init authoritative pointer), with a deterministic fallback.
ASSETS_LINK="$FIXTURE_DIR/assets"
if [ -L "$ASSETS_LINK" ]; then
  ASSETS_TARGET="$(readlink "$ASSETS_LINK")"
  PROSPECT_DIR_FOR_VERCEL="$(dirname "$ASSETS_TARGET")"
else
  PROSPECT_DIR_FOR_VERCEL="$HOME/grm-sites-prospects/$PROSPECT"
fi

# ----------------------------------------------------------------------------
# Step 2: Resolve the canonical project name with collision handling per
# deployment.md L52-94. The fixture slug is the input; the project name is
# always [slug]-grm with a numeric suffix appended on collision.
# ----------------------------------------------------------------------------
BASE_PROJECT_NAME="${PROSPECT}-grm"
PROJECT_NAME="$BASE_PROJECT_NAME"

# Prefer the project name pinned in the prospect-data dir's .vercel/project.json
# (set on the first successful deploy); this is the deterministic re-deploy path.
PINNED_PROJECT_JSON="$PROSPECT_DIR_FOR_VERCEL/.vercel/project.json"
if [ -f "$PINNED_PROJECT_JSON" ]; then
  PINNED_NAME="$(grep -oE '"name"[[:space:]]*:[[:space:]]*"[^"]+"' "$PINNED_PROJECT_JSON" 2>/dev/null | sed -E 's/.*"name"[[:space:]]*:[[:space:]]*"([^"]+)".*/\1/' | head -1 || true)"
  if [ -n "${PINNED_NAME:-}" ]; then
    PROJECT_NAME="$PINNED_NAME"
    echo "Step 2: Reusing pinned project name from $PINNED_PROJECT_JSON: $PROJECT_NAME"
  fi
else
  # Fresh project — check for collisions on the team and pick the next free suffix.
  EXISTING_NAMES="$(vercel projects ls --scope "$VERCEL_SCOPE" 2>/dev/null | awk '{print $1}' || true)"
  if echo "$EXISTING_NAMES" | grep -qE "^${BASE_PROJECT_NAME}\$"; then
    SUFFIX=2
    while echo "$EXISTING_NAMES" | grep -qE "^${BASE_PROJECT_NAME}-${SUFFIX}\$"; do
      SUFFIX=$((SUFFIX + 1))
    done
    PROJECT_NAME="${BASE_PROJECT_NAME}-${SUFFIX}"
    echo "Step 2: $BASE_PROJECT_NAME taken; using $PROJECT_NAME"
  else
    echo "Step 2: $BASE_PROJECT_NAME available; using it"
  fi

  # Pre-create the project so the deploy URL is deterministic before any HTML
  # is written. Closes Bug 6A — without this, an unlinked first deploy lets
  # Vercel infer the project name from the staging-dir basename.
  echo "Step 2: Pre-creating Vercel project $PROJECT_NAME..."
  vercel project add "$PROJECT_NAME" --scope "$VERCEL_SCOPE" >/dev/null 2>&1 || {
    echo "WARN: 'vercel project add' returned non-zero; project may already exist or CLI lacks permission. Continuing." >&2
  }
fi

FINAL_ALIAS="https://${PROJECT_NAME}.vercel.app"

# ----------------------------------------------------------------------------
# Stage rendered HTML + sidecars + CSS + assets to /tmp.
# ----------------------------------------------------------------------------
STAGE_DIR="/tmp/grm-deploy-${PROJECT_NAME}-$$"
trap 'rm -rf "$STAGE_DIR"' EXIT
mkdir -p "$STAGE_DIR"

cp "$FIXTURE_DIR"/*.html "$STAGE_DIR/"
# Vercel serves /index.html at the deploy root; render emits Homepage.html.
if [ -f "$STAGE_DIR/Homepage.html" ]; then
  mv "$STAGE_DIR/Homepage.html" "$STAGE_DIR/index.html"
fi

# SEO/GEO sidecars per deployment.md L156-158: sitemap.xml + robots.txt +
# llms.txt all need to land at the deploy root if they exist.
for SIDECAR in sitemap.xml robots.txt llms.txt; do
  if [ -f "$FIXTURE_DIR/$SIDECAR" ]; then
    cp "$FIXTURE_DIR/$SIDECAR" "$STAGE_DIR/"
  fi
done

mkdir -p "$STAGE_DIR/css"
cp "$SKILL_ROOT/css/composer-system.css" "$STAGE_DIR/css/"

if [ -e "$FIXTURE_DIR/assets" ]; then
  cp -RL "$FIXTURE_DIR/assets" "$STAGE_DIR/"
fi

# Drop underscore-prefixed Unsplash workflow files from the staged assets;
# the deployed bundle only needs the final <slug>-{featured,detail}.jpg files.
if [ -d "$STAGE_DIR/assets/photos/unsplash" ]; then
  find "$STAGE_DIR/assets/photos/unsplash" -maxdepth 1 -name "_*" -exec rm -rf {} + 2>/dev/null || true
fi

# Link the staged dir to the resolved project so vercel deploy targets the
# right place. Use `vercel link` to write a valid .vercel/project.json with
# the correct projectId — replaces the prior manual extraction which broke
# in non-TTY mode because `vercel project ls 2>/dev/null` produced empty
# stdout (Vercel CLI writes its table to stderr; S3-2/S3-3 defect class).
mkdir -p "$STAGE_DIR/.vercel"
if [ -f "$PINNED_PROJECT_JSON" ]; then
  cp "$PINNED_PROJECT_JSON" "$STAGE_DIR/.vercel/project.json"
else
  (cd "$STAGE_DIR" && vercel link --yes --project "$PROJECT_NAME" --scope "$VERCEL_SCOPE" >/dev/null 2>&1) || {
    echo "WARN: vercel link failed; deploy may auto-create project from staging dir basename." >&2
  }
fi

# ----------------------------------------------------------------------------
# Step 2.5: Slug-reconciliation gate per deployment.md L128-160 (Bug 5 fix).
# Phase 5 may have written URLs using the fixture slug (e.g.
# volthom-grm.vercel.app) before we knew the final project name. Sweep every
# .vercel.app URL in HTML/XML/TXT and rewrite to FINAL_ALIAS if it differs.
# ----------------------------------------------------------------------------
echo "Step 2.5: Reconciling .vercel.app URL references to $FINAL_ALIAS..."
RECONCILE_COUNT=0
TARGETS=()
while IFS= read -r -d '' f; do
  TARGETS+=("$f")
done < <(find "$STAGE_DIR" -maxdepth 2 -type f \( -name "*.html" -o -name "sitemap.xml" -o -name "robots.txt" -o -name "llms.txt" \) -print0)

for f in "${TARGETS[@]}"; do
  # Extract every https://*.vercel.app[/...] URL; if any do not match FINAL_ALIAS,
  # rewrite the host portion in-place.
  STALE_HOSTS="$(grep -oE 'https://[a-z0-9-]+\.vercel\.app' "$f" | sort -u | grep -v "^${FINAL_ALIAS}\$" || true)"
  if [ -n "$STALE_HOSTS" ]; then
    while IFS= read -r STALE_HOST; do
      [ -z "$STALE_HOST" ] && continue
      # sed-friendly escape (ampersand only; URL chars are safe).
      ESCAPED_FROM="$(printf '%s' "$STALE_HOST" | sed 's/[&]/\\&/g')"
      ESCAPED_TO="$(printf '%s' "$FINAL_ALIAS" | sed 's/[&]/\\&/g')"
      sed -i.bak "s#${ESCAPED_FROM}#${ESCAPED_TO}#g" "$f"
      RECONCILE_COUNT=$((RECONCILE_COUNT + 1))
    done <<< "$STALE_HOSTS"
  fi
done
find "$STAGE_DIR" -name "*.bak" -type f -delete

# Verify zero stale references remain.
REMAINING="$(grep -REho 'https://[a-z0-9-]+\.vercel\.app' "$STAGE_DIR" --include="*.html" --include="sitemap.xml" --include="robots.txt" --include="llms.txt" 2>/dev/null | sort -u | grep -v "^${FINAL_ALIAS}\$" || true)"
if [ -n "$REMAINING" ]; then
  echo "ERROR: stale .vercel.app references remain after reconciliation:" >&2
  printf '  %s\n' $REMAINING >&2
  exit 1
fi
echo "Step 2.5: $RECONCILE_COUNT reconciliations applied; zero stale references remain."

# ----------------------------------------------------------------------------
# Step 3: Substitute the StaticForms placeholder accessKey, rewrite CSS link
# and asset paths to deploy-root-relative.
# ----------------------------------------------------------------------------
echo "Step 3: Substituting StaticForms accessKey in staged HTML..."
find "$STAGE_DIR" -maxdepth 1 -name "*.html" -type f -exec \
  sed -i.bak "s/REPLACE_WITH_STATICFORMS_KEY/$STATICFORMS_ACCESS_KEY/g" {} \;
find "$STAGE_DIR" -name "*.bak" -type f -delete

if grep -r "REPLACE_WITH_STATICFORMS_KEY" "$STAGE_DIR" >/dev/null 2>&1; then
  echo "ERROR: StaticForms placeholder still present after substitution." >&2
  exit 1
fi

echo "Step 3: Rewriting CSS link to deploy-root-relative path..."
find "$STAGE_DIR" -maxdepth 1 -name "*.html" -type f -exec \
  sed -i.bak 's#href="\.\./\.\./css/composer-system\.css"#href="/css/composer-system.css"#g' {} \;
find "$STAGE_DIR" -name "*.bak" -type f -delete

echo "Step 3: Rewriting asset paths to deploy-root-relative..."
find "$STAGE_DIR" -maxdepth 1 -name "*.html" -type f -exec \
  sed -i.bak -E "s#(src=\"|background-image:url\\(')(\\.\\./)+grm-sites-prospects/[^/]+/assets/#\\1/assets/#g" {} \;
find "$STAGE_DIR" -name "*.bak" -type f -delete

# ----------------------------------------------------------------------------
# Step 4: Deploy from the staging directory.
# ----------------------------------------------------------------------------
cd "$STAGE_DIR"
echo "Step 4: Deploying $PROJECT_NAME from $STAGE_DIR..."

VERCEL_ARGS=("--scope" "$VERCEL_SCOPE" "--yes")
if [ "$PROD_FLAG" = "--prod" ]; then
  VERCEL_ARGS+=("--prod")
fi

vercel deploy "${VERCEL_ARGS[@]}"

# Persist the resolved project link back into the prospect-data dir so the
# next deploy reuses the same project deterministically.
if [ ! -f "$PINNED_PROJECT_JSON" ] && [ -f "$STAGE_DIR/.vercel/project.json" ]; then
  mkdir -p "$(dirname "$PINNED_PROJECT_JSON")"
  cp "$STAGE_DIR/.vercel/project.json" "$PINNED_PROJECT_JSON"
  echo "Persisted project link to $PINNED_PROJECT_JSON for future deploys."
fi

echo ""
echo "✓ Deploy complete: $FINAL_ALIAS"
echo "✓ Verify the form on the deployed page submits cleanly."

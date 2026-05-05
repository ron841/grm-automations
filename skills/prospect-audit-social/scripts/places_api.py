"""
Places API v1 wrappers for the prospect-audit-social skill.

Two responsibilities:

1. fetch_place_details(place_id, api_key) -> dict
   GET /v1/places/{place_id} with a wide field mask. Returns the raw place
   record covering identity, contact, hours, categories, attributes, rating,
   reviews count, photos metadata, and accessibility. The whole record is
   saved to place-details-raw.json by the orchestrator.

2. fetch_photos(place_record, slug, business_name, api_key, out_dir) -> list[dict]
   Iterates place_record["photos"], downloads each at native resolution
   (maxHeightPx=4800 maxWidthPx=4800), tags provenance from
   authorAttributions[].displayName, writes the binary to
   <out_dir>/images/, and returns one metadata dict per photo plus the
   README.md catalogue.

The Places API v1 is the New Places API, not the legacy Maps API. The
endpoints used here:

  GET https://places.googleapis.com/v1/places/{place_id}
      Headers: X-Goog-Api-Key, X-Goog-FieldMask
      Returns: JSON

  GET https://places.googleapis.com/v1/{photo_resource_name}/media
      Query: maxHeightPx, maxWidthPx, key
      Returns: image bytes (the key is in the query string for media
      because the response is not JSON; this is the documented pattern).

The photo resource name is the photos[].name field returned by the place
details call. It looks like:
  places/ChIJ.../photos/AbCd...

Provenance discriminator:
  - authorAttributions[].displayName is the business displayName (case
    insensitive, ignoring LLC / Inc / LLC. / Co. / Corp suffix and
    punctuation): provenance = "owner-uploaded"
  - otherwise: provenance = "customer-uploaded" with the author name
    preserved in metadata.
  - if authorAttributions is missing or empty: provenance = "unknown"
    plus a [low-confidence] flag so the catalogue surfaces the gap.
"""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from urllib.parse import quote

import requests

PLACES_API_BASE = "https://places.googleapis.com/v1"

# Wide field mask. Everything we want into intake at audit time. The Places
# API charges by field-mask category, but at our volume the per-prospect
# cost stays well under target.
PLACE_FIELD_MASK = ",".join([
    "id",
    "types",
    "nationalPhoneNumber",
    "internationalPhoneNumber",
    "formattedAddress",
    "addressComponents",
    "location",
    "rating",
    "googleMapsUri",
    "regularOpeningHours",
    "currentOpeningHours",
    "businessStatus",
    "userRatingCount",
    "displayName",
    "primaryType",
    "primaryTypeDisplayName",
    "reviews",
    "accessibilityOptions",
    "websiteUri",
    "photos",
])


def _strip_entity_suffix(name: str) -> str:
    """Normalize a business name for owner-attribution comparison.

    Removes punctuation, common entity suffixes (LLC, Inc, Corp, Co), and
    lowercases. Used only for the photo-provenance match, not for display.
    """
    s = name.lower()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\b(llc|inc|corp|co|company|the)\b", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def fetch_place_details(place_id: str, api_key: str) -> dict:
    """Fetch the full place record. Raises on non-200."""
    url = f"{PLACES_API_BASE}/places/{quote(place_id, safe='')}"
    headers = {
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": PLACE_FIELD_MASK,
    }
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()


def _photo_provenance(photo: dict, business_display_name: str) -> tuple[str, str | None, bool]:
    """Tag a single photo's provenance.

    Returns (provenance, author_display_name_or_None, low_confidence_flag).
    """
    attrs = photo.get("authorAttributions", [])
    if not attrs:
        return ("unknown", None, True)

    # First attribution is the canonical author; secondaries are rare.
    author = attrs[0].get("displayName", "")
    business_norm = _strip_entity_suffix(business_display_name)
    author_norm = _strip_entity_suffix(author)

    if business_norm and business_norm in author_norm:
        return ("owner-uploaded", author, False)
    return ("customer-uploaded", author, False)


def fetch_photos(
    place_record: dict,
    slug: str,
    business_name: str,
    api_key: str,
    out_dir: Path,
    max_dim_px: int = 4800,
    photos_dir: Path | None = None,
) -> list[dict]:
    """Download every photo in place_record at native resolution and tag.

    Writes to photos_dir, defaulting to <out_dir>/images/ for v0.1
    compatibility. v0.2 callers pass <out_dir>/audit/photos/gbp/.

    Filename: NN-gbp-<owner|customer>-<slug>.jpg.

    Returns: list of dicts with keys
      file, source, provenance, author, width, height, photo_resource_name,
      low_confidence
    """
    images_dir = photos_dir if photos_dir is not None else (out_dir / "images")
    images_dir.mkdir(parents=True, exist_ok=True)

    photos = place_record.get("photos", [])
    if not photos:
        return []

    # Two-pass ordering: owner-uploaded first (NN 01..), then customer.
    # Reason: matches the convention in references/photo-capture-standard.md.
    tagged = []
    for p in photos:
        prov, author, low_conf = _photo_provenance(p, business_name)
        tagged.append({
            "raw": p,
            "provenance": prov,
            "author": author,
            "low_confidence": low_conf,
        })

    owner_first = [t for t in tagged if t["provenance"] == "owner-uploaded"]
    customer_then = [t for t in tagged if t["provenance"] == "customer-uploaded"]
    unknown_last = [t for t in tagged if t["provenance"] == "unknown"]
    ordered = owner_first + customer_then + unknown_last

    metadata = []
    for idx, t in enumerate(ordered, start=1):
        photo = t["raw"]
        name = photo["name"]  # places/PLACE/photos/PHOTO_ID
        prov_short = {"owner-uploaded": "owner",
                      "customer-uploaded": "customer",
                      "unknown": "unknown"}[t["provenance"]]
        filename = f"{idx:02d}-gbp-{prov_short}-{slug}.jpg"
        target = images_dir / filename

        # Photo media endpoint: API key in URL because response is binary.
        media_url = (
            f"{PLACES_API_BASE}/{name}/media"
            f"?maxHeightPx={max_dim_px}&maxWidthPx={max_dim_px}"
            f"&key={quote(api_key)}"
        )
        r = requests.get(media_url, timeout=60)
        if r.status_code != 200:
            # Per three-state-tagging.md: this is [scrape-failed], not [gap].
            metadata.append({
                "file": filename,
                "source": "GBP API",
                "provenance": t["provenance"],
                "author": t["author"],
                "width": photo.get("widthPx"),
                "height": photo.get("heightPx"),
                "photo_resource_name": name,
                "low_confidence": t["low_confidence"],
                "scrape_failed": True,
                "http_status": r.status_code,
            })
            continue
        target.write_bytes(r.content)
        metadata.append({
            "file": filename,
            "source": "GBP API",
            "provenance": t["provenance"],
            "author": t["author"],
            "width": photo.get("widthPx"),
            "height": photo.get("heightPx"),
            "photo_resource_name": name,
            "low_confidence": t["low_confidence"],
            "scrape_failed": False,
        })
        # Light pacing to be courteous to the API; well under the per-key
        # quota at v0.1 volume.
        time.sleep(0.15)

    return metadata


def write_photo_readme(metadata: list[dict], out_dir: Path) -> None:
    """Render images/README.md from the photo metadata list.

    Format matches references/photo-capture-standard.md.
    """
    images_dir = out_dir / "images"
    lines = ["# Photo Catalogue", "",
             "| File | Source | Provenance | Author | Width x Height | Notes |",
             "| --- | --- | --- | --- | --- | --- |"]
    for m in metadata:
        notes = []
        if m.get("scrape_failed"):
            notes.append(f"[scrape-failed] HTTP {m.get('http_status', '?')}")
        if m.get("low_confidence"):
            notes.append("[low-confidence] author attribution missing")
        notes_str = "; ".join(notes)
        author = m.get("author") or ""
        w = m.get("width") or "?"
        h = m.get("height") or "?"
        lines.append(
            f"| {m['file']} | {m['source']} | {m['provenance']} | {author} | {w} x {h} | {notes_str} |"
        )
    (images_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_api_key(env_path: Path = Path.home() / "grm-sites-prospects" / ".env") -> str:
    """Read GOOGLE_PLACES_API_KEY from the standard .env file."""
    if not env_path.exists():
        raise FileNotFoundError(f"Expected env file at {env_path}")
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("GOOGLE_PLACES_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise KeyError("GOOGLE_PLACES_API_KEY not found in env file")


# CLI entry point for ad-hoc verification. Not called by the orchestrator.
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("usage: places_api.py <place_id> <slug> <out_dir>", file=sys.stderr)
        sys.exit(2)
    place_id, slug, out_dir_str = sys.argv[1], sys.argv[2], sys.argv[3]
    out_dir = Path(out_dir_str).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    api_key = load_api_key()
    place = fetch_place_details(place_id, api_key)
    (out_dir / "place-details-raw.json").write_text(
        json.dumps(place, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    business_name = place.get("displayName", {}).get("text", slug)
    metadata = fetch_photos(place, slug, business_name, api_key, out_dir)
    write_photo_readme(metadata, out_dir)
    print(f"Place: {business_name}")
    print(f"Photos: {len(metadata)} (owner-uploaded: "
          f"{sum(1 for m in metadata if m['provenance'] == 'owner-uploaded')}, "
          f"customer-uploaded: {sum(1 for m in metadata if m['provenance'] == 'customer-uploaded')}, "
          f"unknown: {sum(1 for m in metadata if m['provenance'] == 'unknown')})")
    failed = [m for m in metadata if m.get("scrape_failed")]
    if failed:
        print(f"Failed to download: {len(failed)} (see README.md notes)")

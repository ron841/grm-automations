"""
Logo color extraction via k-means.

Per the spec:
  - k = 5
  - Background detection: most-frequent pixel value with high frequency
    margin -> exclude as background.
  - Top 3-5 clusters surfaced with hex codes + frequency percentage +
    confidence (inter-cluster distance + intra-cluster variance).
  - Save swatch.png as visual representation.

Implementation notes:
  - Downsample the logo to 200x200 to keep clustering fast. Color
    statistics are stable at this resolution for site palettes.
  - Convert RGBA to RGB by alpha-compositing onto white. PNG logos
    often carry transparency; we do not want transparency to count as
    a color cluster.
  - Background detection threshold: a single quantized color (rounded
    to a 16-step grid per channel) that accounts for >35% of pixels
    is treated as background and removed before clustering.
  - Confidence per cluster = sigmoid of (inter_cluster_distance /
    (intra_cluster_variance + epsilon)). High inter / low intra =
    high confidence.

Output JSON shape:
  {
    "clusters": [
      {"hex": "#aabbcc", "rgb": [170,187,204], "frequency_pct": 32.5, "confidence": 0.88},
      ...
    ],
    "background_excluded": {"hex": "#ffffff", "frequency_pct": 41.2} | null,
    "n_pixels_analyzed": int,
    "k": 5,
  }
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image
from sklearn.cluster import KMeans


def _rgb_to_hex(rgb) -> str:
    r, g, b = [int(round(float(x))) for x in rgb]
    return "#{:02x}{:02x}{:02x}".format(max(0, min(255, r)),
                                         max(0, min(255, g)),
                                         max(0, min(255, b)))


def _alpha_composite_on_white(img: Image.Image) -> Image.Image:
    """Flatten RGBA / palette images onto a white background."""
    if img.mode == "RGBA":
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        return bg
    if img.mode != "RGB":
        return img.convert("RGB")
    return img


def _downsample(img: Image.Image, target: int = 200) -> Image.Image:
    if max(img.size) <= target:
        return img
    img.thumbnail((target, target), Image.LANCZOS)
    return img


def _detect_background(pixels: np.ndarray,
                       quant_step: int = 16,
                       threshold: float = 0.35) -> tuple[np.ndarray | None, float]:
    """Find the most-frequent quantized color and return it if dominant.

    Returns (background_rgb, fraction_of_pixels) or (None, 0) when no
    single quantized color exceeds the threshold.
    """
    quant = (pixels // quant_step) * quant_step
    # Use a packed key for counting.
    keys = quant[:, 0].astype(np.int64) * 256 * 256 \
        + quant[:, 1].astype(np.int64) * 256 \
        + quant[:, 2].astype(np.int64)
    unique, counts = np.unique(keys, return_counts=True)
    if len(unique) == 0:
        return None, 0.0
    top_idx = int(np.argmax(counts))
    top_count = int(counts[top_idx])
    top_frac = top_count / float(len(pixels))
    if top_frac < threshold:
        return None, top_frac
    top_key = int(unique[top_idx])
    bg = np.array([
        (top_key // (256 * 256)) % 256,
        (top_key // 256) % 256,
        top_key % 256,
    ], dtype=np.uint8)
    return bg, top_frac


def _confidence(centers: np.ndarray, labels: np.ndarray,
                pixels: np.ndarray) -> list[float]:
    """Compute per-cluster confidence.

    confidence_i = sigmoid(inter_i / (intra_i + 1e-6))
      inter_i = mean Euclidean distance from center_i to other centers
      intra_i = mean Euclidean distance from pixels in cluster i to center_i
    """
    k = centers.shape[0]
    out = []
    for i in range(k):
        # Inter-cluster: mean distance to other centers.
        others = np.delete(centers, i, axis=0)
        if len(others) == 0:
            inter = 0.0
        else:
            inter = float(np.mean(np.linalg.norm(others - centers[i], axis=1)))
        # Intra-cluster: mean distance from cluster pixels to center.
        in_cluster = pixels[labels == i]
        if len(in_cluster) == 0:
            intra = 1e9
        else:
            intra = float(np.mean(np.linalg.norm(in_cluster - centers[i], axis=1)))
        ratio = inter / (intra + 1e-6)
        # Sigmoid normalized so ratio of ~1 maps to ~0.5, ~3 maps to ~0.95.
        sig = 1.0 / (1.0 + np.exp(-(ratio - 1.0) * 1.5))
        out.append(round(float(sig), 3))
    return out


def extract_palette(logo_path: Path, k: int = 5,
                     out_dir: Path | None = None,
                     bg_threshold: float = 0.35,
                     surface_top_n: int = 5,
                     swatch_size: tuple[int, int] = (500, 100)) -> dict:
    """Run k-means on logo pixels, return palette + write swatch + json.

    Returns the result dict (also written to out_dir/extraction.json
    when out_dir is provided).
    """
    img = Image.open(logo_path)
    img = _alpha_composite_on_white(img)
    img = _downsample(img, 200)
    pixels = np.asarray(img).reshape(-1, 3).astype(np.float64)

    # Background detection.
    bg, bg_frac = _detect_background(pixels.astype(np.uint8),
                                       quant_step=16,
                                       threshold=bg_threshold)
    if bg is not None:
        # Mask out anything close to the background (within Euclidean
        # distance 24 in RGB).
        dist = np.linalg.norm(pixels - bg, axis=1)
        non_bg = pixels[dist > 24]
    else:
        non_bg = pixels

    if len(non_bg) < k * 10:
        # Not enough pixels for stable k-means; fall back to
        # all-pixels-clustering. Tag as low-confidence.
        non_bg = pixels
        low_confidence_run = True
    else:
        low_confidence_run = False

    km = KMeans(n_clusters=k, n_init=4, random_state=42)
    labels = km.fit_predict(non_bg)
    centers = km.cluster_centers_
    counts = np.bincount(labels, minlength=k)
    fractions = counts / float(len(non_bg))

    confidences = _confidence(centers, labels, non_bg)

    # Sort clusters by frequency descending.
    order = np.argsort(-fractions)
    clusters = []
    for i in order[:surface_top_n]:
        clusters.append({
            "hex": _rgb_to_hex(centers[i]),
            "rgb": [int(round(float(c))) for c in centers[i]],
            "frequency_pct": round(float(fractions[i]) * 100, 2),
            "confidence": confidences[i] if not low_confidence_run else
                          round(confidences[i] * 0.5, 3),
        })

    result = {
        "clusters": clusters,
        "background_excluded": (
            {"hex": _rgb_to_hex(bg), "frequency_pct": round(bg_frac * 100, 2)}
            if bg is not None else None
        ),
        "n_pixels_analyzed": int(len(non_bg)),
        "k": k,
        "low_confidence_run": low_confidence_run,
    }

    if out_dir is not None:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "extraction.json").write_text(
            json.dumps(result, indent=2),
            encoding="utf-8",
        )
        # Render swatch.png: horizontal strip of the top clusters.
        n_swatch = len(clusters)
        if n_swatch:
            sw_w, sw_h = swatch_size
            band = sw_w // n_swatch
            swatch = Image.new("RGB", (band * n_swatch, sw_h), (255, 255, 255))
            for i, c in enumerate(clusters):
                tile = Image.new("RGB", (band, sw_h), tuple(c["rgb"]))
                swatch.paste(tile, (i * band, 0))
            swatch.save(out_dir / "swatch.png")

    return result


# CLI entry point.
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("usage: kmeans_palette.py <logo_path> <out_dir>", file=sys.stderr)
        sys.exit(2)
    logo_path = Path(sys.argv[1]).expanduser()
    out_dir = Path(sys.argv[2]).expanduser()
    res = extract_palette(logo_path, out_dir=out_dir)
    print(f"Logo: {logo_path}")
    print(f"  pixels analyzed: {res['n_pixels_analyzed']}")
    bg = res["background_excluded"]
    if bg:
        print(f"  background excluded: {bg['hex']} ({bg['frequency_pct']}% of source)")
    print(f"  top clusters:")
    for c in res["clusters"]:
        print(f"    {c['hex']}  freq {c['frequency_pct']}%  conf {c['confidence']}")
    print(f"  written: {out_dir}/extraction.json + {out_dir}/swatch.png")

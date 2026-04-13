"""Primitive 4: Compare two values in color, image, or text mode."""

import colorsys
import difflib
import json
import sys

from PIL import Image


def run(a, b, mode):
    """
    Compare *a* and *b* in the given *mode*.

    Modes:
        color  — hex strings, compute HSL hue distance
        image  — file paths, compute mean pixel diff (Pillow)
        text   — strings or @file paths, compute SequenceMatcher ratio
    """
    if mode == "color":
        return _color(a, b)
    elif mode == "image":
        return _image(a, b)
    elif mode == "text":
        return _text(a, b)
    else:
        print(json.dumps({"error": f"Unknown mode: {mode}. Choose from: color, image, text"}), file=sys.stderr)
        sys.exit(1)


def _hex_to_hsl(hex_str):
    """Convert '#rrggbb' to (h, s, l) where h is 0-360, s and l are 0-1."""
    h_str = hex_str.lstrip("#")
    r, g, b_ = (int(h_str[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b_)
    return h * 360, s, l


def _color(a, b):
    """Compare two hex colors by hue distance in HSL space."""
    ha, _, _ = _hex_to_hsl(a)
    hb, _, _ = _hex_to_hsl(b)
    delta = abs(ha - hb)
    if delta > 180:
        delta = 360 - delta
    similar = delta <= 15
    return {
        "mode": "color",
        "a": a,
        "b": b,
        "hue_delta_deg": round(delta, 2),
        "similar": similar,
    }


def _image(a, b):
    """Compare two images by mean absolute pixel difference, normalized 0-1."""
    img_a = Image.open(a).convert("RGB")
    img_b = Image.open(b).convert("RGB")

    # Resize b to match a if sizes differ
    if img_a.size != img_b.size:
        img_b = img_b.resize(img_a.size, Image.LANCZOS)

    pixels_a = list(img_a.getdata())
    pixels_b = list(img_b.getdata())

    total_diff = 0
    for pa, pb in zip(pixels_a, pixels_b):
        total_diff += abs(pa[0] - pb[0]) + abs(pa[1] - pb[1]) + abs(pa[2] - pb[2])

    # Max possible diff per pixel is 255*3, total pixels is len(pixels_a)
    max_diff = len(pixels_a) * 255 * 3
    mean_diff = total_diff / max_diff if max_diff > 0 else 0
    similarity = round(1.0 - mean_diff, 6)
    similar = similarity >= 0.95

    return {
        "mode": "image",
        "similarity": similarity,
        "similar": similar,
    }


def _text(a, b):
    """Compare two strings (or @file contents) by SequenceMatcher ratio."""
    text_a = _resolve_text(a)
    text_b = _resolve_text(b)
    ratio = difflib.SequenceMatcher(None, text_a, text_b).ratio()
    return {
        "mode": "text",
        "ratio": round(ratio, 6),
    }


def _resolve_text(val):
    """If val starts with '@', read file contents. Otherwise use as-is."""
    if val.startswith("@"):
        path = val[1:]
        with open(path, "r") as f:
            return f.read()
    return val

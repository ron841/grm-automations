"""CLI entry point for grm-browser primitives."""

import argparse
import json
import sys

from . import config


def main():
    config.ensure_cache_dir()
    config.prune_cache()

    parser = argparse.ArgumentParser(
        prog="grm-browser",
        description="Browser automation toolkit for GRM prospect-site verification.",
    )
    subs = parser.add_subparsers(dest="command", required=True)

    # -- capture --
    p_cap = subs.add_parser("capture", help="Screenshot a URL")
    p_cap.add_argument("url")
    p_cap.add_argument("--viewport", default="375x812")
    p_cap.add_argument("--full-page", action="store_true", default=True)
    p_cap.add_argument("--no-full-page", dest="full_page", action="store_false")
    p_cap.add_argument("--out", default=None)

    # -- extract --
    p_ext = subs.add_parser("extract", help="Extract structured data from a rendered page")
    p_ext.add_argument("url")
    p_ext.add_argument("--what", required=True, choices=["og-tags", "nav-images", "service-card-images", "dom"])

    # -- probe --
    p_prb = subs.add_parser("probe", help="HTTP metadata via browser navigation")
    p_prb.add_argument("url")

    # -- compare --
    p_cmp = subs.add_parser("compare", help="Compare two values")
    p_cmp.add_argument("a")
    p_cmp.add_argument("b")
    p_cmp.add_argument("--mode", required=True, choices=["color", "image", "text"])

    args = parser.parse_args()

    if args.command == "capture":
        from . import capture
        result = capture.run(args.url, args.viewport, args.full_page, args.out)
    elif args.command == "extract":
        from . import extract
        result = extract.run(args.url, args.what)
    elif args.command == "probe":
        from . import probe
        result = probe.run(args.url)
    elif args.command == "compare":
        from . import compare
        result = compare.run(args.a, args.b, args.mode)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

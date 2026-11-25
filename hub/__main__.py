"""`python -m hub` starts the site; `python -m hub --progress` prints what's saved."""

from __future__ import annotations

import argparse
import sys

from hub import DEFAULT_PORT, PROGRESS_FILE, REPO_ROOT, progress
from hub.server import HubConfig, create_server


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m hub", description=__doc__)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument(
        "--progress",
        action="store_true",
        help="print the saved answers and marks, then exit",
    )
    args = parser.parse_args(argv)
    # Windows consoles default to an older encoding that can't print ✓ ½ ✗.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    progress_path = REPO_ROOT / "hub" / PROGRESS_FILE
    if args.progress:
        try:
            print(progress.summary(progress_path))
        except progress.ProgressError as err:
            print(f"hub: {err}", file=sys.stderr)
            return 1
        return 0

    config = HubConfig(
        docs_dir=REPO_ROOT / "docs", progress_path=progress_path, port=args.port
    )
    try:
        server = create_server(config)
    except OSError as err:
        print(f"hub: could not start on port {args.port}: {err}", file=sys.stderr)
        print("hub: is it already running in another terminal?", file=sys.stderr)
        return 1
    print(f"Learning hub: http://127.0.0.1:{args.port}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())

from __future__ import annotations

import argparse
import json
import sys

from .config import Settings
from .runner import run_hunt


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Threat hunting model automation for FortiSIEM"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of threat news items to process",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    settings = Settings.from_env()

    result = run_hunt(settings, limit=args.limit)
    output = [response.payload for response in result.responses]
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

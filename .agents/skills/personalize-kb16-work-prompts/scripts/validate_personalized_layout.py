#!/usr/bin/env python3
"""Validate a personalized KB16 WORK-prompt layout against its base and profile."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from personalize_work_prompts import (
    DEFAULT_MAX_BYTES,
    PROMPT_SLOT_COUNT,
    ValidationError,
    macro_block_bytes,
    read_json,
    require,
    validate_layout,
    validate_profile,
)


def validate_against_base(candidate: dict, base: dict) -> None:
    validate_layout(base)
    candidate_copy = json.loads(json.dumps(candidate))
    base_copy = json.loads(json.dumps(base))
    candidate_copy["macros"][:PROMPT_SLOT_COUNT] = base_copy["macros"][:PROMPT_SLOT_COUNT]
    require(
        candidate_copy == base_copy,
        "personalized layout differs from the base outside macro slots 0-7",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--layout", type=Path, required=True, help="Personalized .layout.json")
    parser.add_argument("--base", type=Path, help="Base layout that must differ only in macros 0-7")
    parser.add_argument("--profile", type=Path, help="Profile whose prompt text must match the layout")
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES, help="Macro block byte limit, at most 512")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        require(0 < args.max_bytes <= DEFAULT_MAX_BYTES, "--max-bytes must be between 1 and 512")
        candidate = read_json(args.layout, "layout")
        validate_layout(candidate, max_bytes=args.max_bytes)

        if args.base:
            base = read_json(args.base, "base layout")
            validate_against_base(candidate, base)

        if args.profile:
            profile = read_json(args.profile, "profile")
            prompts = validate_profile(profile)
            expected = [prompt["text"] for prompt in prompts]
            require(candidate["macros"][:PROMPT_SLOT_COUNT] == expected, "layout macros do not match the profile")

        used_bytes = macro_block_bytes(candidate["macros"])
        checks = ["structure"]
        if args.base:
            checks.append("base diff")
        if args.profile:
            checks.append("profile")
        print(f"OK: {', '.join(checks)} valid; macro block {used_bytes}/{args.max_bytes} bytes")
        return 0
    except ValidationError as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

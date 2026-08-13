#!/usr/bin/env python3
"""Create a KB16-01 VIA layout with personalized WORK prompts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


EXPECTED_DEVICE = "KB16-01"
EXPECTED_VENDOR_PRODUCT_ID = 3490715137
EXPECTED_LAYER_COUNT = 4
EXPECTED_LAYER_SIZE = 20
EXPECTED_MACRO_COUNT = 16
EXPECTED_ENCODER_COUNT = 3
PROMPT_SLOT_COUNT = 8
DEFAULT_MAX_BYTES = 512
RECOMMENDED_FREE_BYTES = 32
WORK_LAYER = 3
WORK_HOLD_POSITION = 15
PROMPT_POSITIONS = (0, 1, 2, 3, 5, 6, 7, 8)
PROFILE_NAME = re.compile(r"[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?")
MACRO_KEYCODE = re.compile(r"MACRO\((\d+)\)")


class ValidationError(ValueError):
    """Raised when a profile or layout violates the KB16 contract."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValidationError(f"cannot read {label} {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"invalid JSON in {label} {path}: {exc}") from exc
    require(isinstance(value, dict), f"{label} root must be a JSON object")
    return value


def require_printable_ascii(value: str, label: str) -> None:
    require(value.isascii(), f"{label} must use printable ASCII")
    require(
        all(32 <= ord(character) <= 126 for character in value),
        f"{label} must not contain newlines, tabs, or control characters",
    )


def macro_block_bytes(macros: list[Any]) -> int:
    return sum(len(macro.encode("utf-8")) + 1 for macro in macros if isinstance(macro, str))


def warn_if_tight(used_bytes: int, max_bytes: int) -> None:
    free_bytes = max_bytes - used_bytes
    if free_bytes < RECOMMENDED_FREE_BYTES:
        print(
            f"WARNING: only {free_bytes} macro byte(s) remain; aim for at least {RECOMMENDED_FREE_BYTES} bytes of headroom",
            file=sys.stderr,
        )


def validate_layout(layout: dict[str, Any], max_bytes: int = DEFAULT_MAX_BYTES) -> None:
    require(layout.get("name") == EXPECTED_DEVICE, "layout name must be KB16-01")
    require(
        layout.get("vendorProductId") == EXPECTED_VENDOR_PRODUCT_ID,
        "layout vendorProductId must encode 0xD010:0x1601",
    )

    layers = layout.get("layers")
    require(isinstance(layers, list) and len(layers) == EXPECTED_LAYER_COUNT, "layout must have four layers")
    for layer_index, layer in enumerate(layers):
        require(isinstance(layer, list), f"layer {layer_index} must be an array")
        require(len(layer) == EXPECTED_LAYER_SIZE, f"layer {layer_index} must have 20 entries")
        require(all(isinstance(keycode, str) for keycode in layer), f"layer {layer_index} keycodes must be strings")

    for layer_index in range(WORK_LAYER):
        require(
            layers[layer_index][WORK_HOLD_POSITION] == "MO(3)",
            f"layer {layer_index} WORK key must remain MO(3)",
        )
    require(
        layers[WORK_LAYER][WORK_HOLD_POSITION] == "KC_TRNS",
        "WORK hold position must remain transparent on layer 3",
    )

    expected_positions = dict(zip(PROMPT_POSITIONS, range(PROMPT_SLOT_COUNT)))
    for position, slot in expected_positions.items():
        require(
            layers[WORK_LAYER][position] == f"MACRO({slot})",
            f"WORK position {position} must remain MACRO({slot})",
        )

    references: list[int] = []
    for layer in layers:
        for keycode in layer:
            match = MACRO_KEYCODE.fullmatch(keycode)
            if match:
                references.append(int(match.group(1)))
    require(sorted(references) == list(range(PROMPT_SLOT_COUNT)), "layout must reference macro slots 0-7 exactly once")

    macros = layout.get("macros")
    require(isinstance(macros, list) and len(macros) == EXPECTED_MACRO_COUNT, "layout must have 16 macro slots")
    for slot, macro in enumerate(macros):
        require(isinstance(macro, str), f"macro {slot} must be text")
        if macro:
            require_printable_ascii(macro, f"macro {slot}")
        if slot < PROMPT_SLOT_COUNT:
            require(bool(macro), f"referenced macro {slot} must not be empty")
    used_bytes = macro_block_bytes(macros)
    require(used_bytes <= max_bytes, f"macro block uses {used_bytes} bytes; limit is {max_bytes}")

    encoders = layout.get("encoders")
    require(isinstance(encoders, list) and len(encoders) == EXPECTED_ENCODER_COUNT, "layout must have three encoders")
    for encoder_index, encoder in enumerate(encoders):
        require(isinstance(encoder, list) and len(encoder) == EXPECTED_LAYER_COUNT, f"encoder {encoder_index} must define four layers")
        for layer_index, directions in enumerate(encoder):
            require(
                isinstance(directions, list)
                and len(directions) == 2
                and all(isinstance(keycode, str) for keycode in directions),
                f"encoder {encoder_index}, layer {layer_index} must have two keycodes",
            )


def validate_profile(profile: dict[str, Any]) -> list[dict[str, Any]]:
    name = profile.get("name")
    require(isinstance(name, str) and bool(PROFILE_NAME.fullmatch(name)), "profile name must be a lowercase hyphenated slug")

    description = profile.get("description")
    require(description is None or isinstance(description, str), "profile description must be text when present")

    prompts = profile.get("prompts")
    require(isinstance(prompts, list) and len(prompts) == PROMPT_SLOT_COUNT, "profile must contain exactly eight prompts")

    normalized: list[dict[str, Any]] = []
    seen_slots: set[int] = set()
    for index, prompt in enumerate(prompts):
        require(isinstance(prompt, dict), f"prompt entry {index} must be an object")
        slot = prompt.get("slot")
        label = prompt.get("label")
        text = prompt.get("text")
        require(isinstance(slot, int) and not isinstance(slot, bool), f"prompt entry {index} slot must be an integer")
        require(slot in range(PROMPT_SLOT_COUNT), f"prompt entry {index} slot must be 0-7")
        require(slot not in seen_slots, f"prompt slot {slot} appears more than once")
        seen_slots.add(slot)
        require(isinstance(label, str) and bool(label), f"prompt slot {slot} label must be nonempty text")
        require(len(label) <= 18, f"prompt slot {slot} label exceeds 18 characters")
        require_printable_ascii(label, f"prompt slot {slot} label")
        require(isinstance(text, str) and bool(text), f"prompt slot {slot} text must be nonempty")
        require_printable_ascii(text, f"prompt slot {slot} text")
        normalized.append({"slot": slot, "label": label, "text": text})

    require(seen_slots == set(range(PROMPT_SLOT_COUNT)), "profile must contain each prompt slot from 0 through 7")
    return sorted(normalized, key=lambda prompt: prompt["slot"])


def create_personalized_layout(
    source: dict[str, Any], prompts: list[dict[str, Any]], max_bytes: int = DEFAULT_MAX_BYTES
) -> dict[str, Any]:
    candidate = json.loads(json.dumps(source))
    for prompt in prompts:
        candidate["macros"][prompt["slot"]] = prompt["text"]
    validate_layout(candidate, max_bytes=max_bytes)
    return candidate


def markdown_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|")


def render_prompt_map(
    profile: dict[str, Any], prompts: list[dict[str, Any]], layout_name: str, used_bytes: int, max_bytes: int
) -> str:
    title = profile["name"].replace("-", " ").title()
    lines = [f"# KB16 WORK prompts: {title}", ""]
    description = profile.get("description")
    if description:
        lines.extend([description, ""])
    lines.extend(
        [
            "| Key | Macro | Label | Prompt |",
            "|---|---:|---|---|",
        ]
    )
    for prompt in prompts:
        slot = prompt["slot"]
        row = 1 if slot < 4 else 2
        column = slot + 1 if slot < 4 else slot - 3
        lines.append(
            f"| WORK R{row}C{column} | {slot} | {markdown_escape(prompt['label'])} | {markdown_escape(prompt['text'])} |"
        )
    lines.extend(
        [
            "",
            f"Source layout: `{layout_name}`",
            "",
            f"Macro storage: {used_bytes}/{max_bytes} bytes, including sixteen slot terminators.",
            "",
            "Each macro inserts text into the composer without submitting it.",
            "",
        ]
    )
    return "\n".join(lines)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--layout", type=Path, required=True, help="Source KB16-01 .layout.json")
    parser.add_argument("--profile", type=Path, required=True, help="WORK prompt profile JSON")
    parser.add_argument("--output", type=Path, help="Personalized .layout.json output")
    parser.add_argument("--prompt-map", type=Path, help="Optional Markdown prompt-map output")
    parser.add_argument("--dry-run", action="store_true", help="Validate without writing files")
    parser.add_argument("--in-place", action="store_true", help="Allow explicitly overwriting --layout")
    parser.add_argument("--force", action="store_true", help="Replace existing non-source output files")
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES, help="Macro block byte limit, at most 512")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        require(0 < args.max_bytes <= DEFAULT_MAX_BYTES, "--max-bytes must be between 1 and 512")
        source = read_json(args.layout, "layout")
        profile = read_json(args.profile, "profile")
        validate_layout(source, max_bytes=args.max_bytes)
        prompts = validate_profile(profile)
        candidate = create_personalized_layout(source, prompts, max_bytes=args.max_bytes)
        used_bytes = macro_block_bytes(candidate["macros"])
        warn_if_tight(used_bytes, args.max_bytes)

        if args.dry_run:
            require(args.output is None and args.prompt_map is None, "--dry-run cannot be combined with output paths")
            print(f"OK: profile {profile['name']} fits at {used_bytes}/{args.max_bytes} bytes")
            return 0

        require(args.output is not None, "--output is required unless --dry-run is used")
        source_path = args.layout.resolve()
        profile_path = args.profile.resolve()
        output_path = args.output.resolve()
        require(output_path != source_path or args.in_place, "refusing to overwrite the source without --in-place")
        require(output_path != profile_path, "--output must not overwrite the profile")
        require(
            output_path == source_path or not args.output.exists() or args.force,
            f"output already exists: {args.output}; use --force to replace it",
        )
        if args.prompt_map is not None:
            prompt_map_path = args.prompt_map.resolve()
            require(
                prompt_map_path not in {source_path, profile_path, output_path},
                "--prompt-map must differ from the layout, profile, and output paths",
            )
        require(
            args.prompt_map is None or not args.prompt_map.exists() or args.force,
            f"prompt map already exists: {args.prompt_map}; use --force to replace it",
        )

        write_text(args.output, json.dumps(candidate, indent=2, ensure_ascii=False) + "\n")
        if args.prompt_map:
            write_text(
                args.prompt_map,
                render_prompt_map(profile, prompts, args.layout.name, used_bytes, args.max_bytes),
            )

        outputs = [str(args.output)]
        if args.prompt_map:
            outputs.append(str(args.prompt_map))
        print(f"OK: wrote {', '.join(outputs)}; macro block {used_bytes}/{args.max_bytes} bytes")
        return 0
    except ValidationError as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"FAILED: cannot write output: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

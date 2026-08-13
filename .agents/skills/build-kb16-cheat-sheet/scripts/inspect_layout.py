#!/usr/bin/env python3
"""Normalize and validate a KB16-01 VIA layout for documentation work."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


GRID_INDICES = (
    (0, 1, 2, 3),
    (5, 6, 7, 8),
    (10, 11, 12, 13),
    (15, 16, 17, 18),
)
PRESS_INDICES = (4, 9, 14)
PRESS_NAMES = ("upper-left", "upper-right", "large-lower-right")


def load_object(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path}: root must be a JSON object")
        return {}
    return value


def usb_id(value: Any) -> str | None:
    if not isinstance(value, int) or value < 0 or value > 0xFFFFFFFF:
        return None
    return f"0x{value >> 16:04X}:0x{value & 0xFFFF:04X}"


def display_by_layer(
    manifest: dict[str, Any], layer_count: int, errors: list[str], warnings: list[str]
) -> dict[int, dict[str, Any]]:
    result: dict[int, dict[str, Any]] = {}
    display = manifest.get("layerDisplay")
    if not isinstance(display, dict):
        warnings.append("manifest has no layerDisplay object; OLED mapping is unverified")
        return result

    for oled, entry in display.items():
        if not isinstance(entry, dict):
            errors.append(f"manifest layerDisplay[{oled!r}] must be an object")
            continue
        via = entry.get("viaLayer")
        if not isinstance(via, int) or via not in range(layer_count):
            errors.append(f"manifest OLED {oled} has invalid VIA layer {via!r}")
            continue
        if via in result:
            errors.append(f"manifest maps multiple OLED values to VIA layer {via}")
            continue
        result[via] = {
            "oled": str(oled),
            "name": entry.get("name"),
            "behavior": entry.get("behavior"),
        }
    if len(result) != layer_count:
        warnings.append(
            f"manifest verifies {len(result)} of {layer_count} VIA layer display mappings"
        )
    return result


def normalize(
    layout_path: Path, manifest_path: Path | None
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    layout = load_object(layout_path, errors)
    manifest = load_object(manifest_path, errors) if manifest_path else {}

    layers = layout.get("layers")
    if not isinstance(layers, list):
        errors.append("layout layers must be an array")
        layers = []
    elif len(layers) != 4:
        errors.append(f"KB16 cheat sheet expects 4 layers; layout has {len(layers)}")

    valid_layers: list[list[str]] = []
    for index, layer in enumerate(layers):
        if not isinstance(layer, list) or len(layer) != 20:
            errors.append(f"layer {index} must contain 20 matrix entries")
            valid_layers.append([])
            continue
        if not all(isinstance(value, str) for value in layer):
            errors.append(f"layer {index} contains a non-string keycode")
        valid_layers.append([str(value) for value in layer])

    macros = layout.get("macros")
    if not isinstance(macros, list):
        errors.append("layout macros must be an array")
        macros = []
    elif len(macros) != 16:
        warnings.append(f"expected 16 macro slots; layout has {len(macros)}")
    for index, macro in enumerate(macros):
        if not isinstance(macro, str):
            errors.append(f"macro {index} is not text")
        elif "\n" in macro or "\r" in macro:
            warnings.append(f"macro {index} contains a newline and may submit text")

    encoders = layout.get("encoders")
    if not isinstance(encoders, list) or len(encoders) != 3:
        errors.append("layout must define exactly 3 encoders")
        encoders = []
    for encoder_index, encoder in enumerate(encoders):
        if not isinstance(encoder, list) or len(encoder) != len(layers):
            errors.append(
                f"encoder {encoder_index} must define rotations for all {len(layers)} layers"
            )
            continue
        for layer_index, directions in enumerate(encoder):
            if (
                not isinstance(directions, list)
                or len(directions) != 2
                or not all(isinstance(value, str) for value in directions)
            ):
                errors.append(
                    f"encoder {encoder_index}, layer {layer_index} must contain CCW/CW keycodes"
                )

    if manifest:
        layout_file = manifest.get("layoutFile")
        if layout_file and layout_file != layout_path.name:
            errors.append(
                f"manifest layoutFile is {layout_file!r}, not {layout_path.name!r}"
            )
        hardware = manifest.get("hardware")
        if isinstance(hardware, dict):
            manifest_id = hardware.get("vendorProductIdDecimal")
            if manifest_id is not None and manifest_id != layout.get("vendorProductId"):
                errors.append("layout and manifest vendor/product IDs differ")
            manifest_layers = hardware.get("layers")
            if manifest_layers is not None and manifest_layers != len(layers):
                errors.append("layout and manifest layer counts differ")

    displays = display_by_layer(manifest, len(layers), errors, warnings)
    referenced_macros: dict[int, list[str]] = {}
    normalized_layers: list[dict[str, Any]] = []

    for layer_index, layer in enumerate(valid_layers):
        if len(layer) != 20:
            continue
        grid = [[layer[index] for index in row] for row in GRID_INDICES]
        presses = {
            name: layer[index] for name, index in zip(PRESS_NAMES, PRESS_INDICES)
        }
        rotations: dict[str, dict[str, str] | None] = {}
        for encoder_index, name in enumerate(PRESS_NAMES):
            try:
                directions = encoders[encoder_index][layer_index]
                rotations[name] = {"ccw": directions[0], "cw": directions[1]}
            except (IndexError, TypeError):
                rotations[name] = None

        for row_index, row in enumerate(grid, start=1):
            for column_index, keycode in enumerate(row, start=1):
                match = re.fullmatch(r"MACRO\((\d+)\)", keycode)
                if match:
                    macro_index = int(match.group(1))
                    referenced_macros.setdefault(macro_index, []).append(
                        f"VIA {layer_index} R{row_index}C{column_index}"
                    )
                    if macro_index >= len(macros):
                        errors.append(f"{keycode} references a missing macro slot")
                    elif not macros[macro_index]:
                        errors.append(f"{keycode} references an empty macro slot")

                momentary = re.fullmatch(r"MO\((\d+)\)", keycode)
                if momentary:
                    target = int(momentary.group(1))
                    if target not in range(len(layers)):
                        errors.append(f"{keycode} on VIA {layer_index} targets a missing layer")
                    elif target <= layer_index:
                        warnings.append(
                            f"{keycode} on VIA {layer_index} may be masked by the active layer"
                        )

                switch = re.fullmatch(r"TO\((\d+)\)", keycode)
                if switch and int(switch.group(1)) not in range(len(layers)):
                    errors.append(f"{keycode} on VIA {layer_index} targets a missing layer")

        normalized_layers.append(
            {
                "via_layer": layer_index,
                "display": displays.get(layer_index),
                "grid": grid,
                "encoder_presses": presses,
                "encoder_rotations": rotations,
                "unused_matrix_position": layer[19],
            }
        )

    macro_rows = []
    for index, macro in enumerate(macros):
        macro_rows.append(
            {
                "index": index,
                "text": macro if isinstance(macro, str) else None,
                "referenced_by": referenced_macros.get(index, []),
            }
        )

    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "layout_path": str(layout_path),
        "manifest_path": str(manifest_path) if manifest_path else None,
        "device": layout.get("name"),
        "vendor_product_id_decimal": layout.get("vendorProductId"),
        "usb_id": usb_id(layout.get("vendorProductId")),
        "layers": normalized_layers,
        "macros": macro_rows,
        "custom_signals": manifest.get("customSignals") if manifest else None,
    }


def markdown_table(rows: list[list[str]]) -> list[str]:
    if not rows:
        return []
    widths = [max(len(row[index]) for row in rows) for index in range(len(rows[0]))]
    result = [
        "| " + " | ".join(value.ljust(widths[index]) for index, value in enumerate(rows[0])) + " |",
        "| " + " | ".join("-" * widths[index] for index in range(len(widths))) + " |",
    ]
    for row in rows[1:]:
        result.append(
            "| " + " | ".join(value.ljust(widths[index]) for index, value in enumerate(row)) + " |"
        )
    return result


def render_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# KB16 layout inspection",
        "",
        f"- Layout: `{data['layout_path']}`",
        f"- Manifest: `{data['manifest_path'] or 'not provided'}`",
        f"- Device: `{data['device']}`",
        f"- USB: `{data['usb_id'] or 'invalid'}`",
        f"- Result: `{'OK' if data['ok'] else 'FAILED'}`",
    ]
    for heading in ("errors", "warnings"):
        values = data[heading]
        if values:
            lines += ["", f"## {heading.title()}", ""]
            lines += [f"- {value}" for value in values]

    for layer in data["layers"]:
        display = layer["display"] or {}
        title = f"VIA {layer['via_layer']}"
        if display:
            title = (
                f"OLED {display.get('oled')} / {title} / "
                f"{display.get('name') or 'unnamed'} ({display.get('behavior') or 'unspecified'})"
            )
        lines += ["", f"## {title}", ""]
        grid_rows = [["", "Column 1", "Column 2", "Column 3", "Column 4"]]
        for index, row in enumerate(layer["grid"], start=1):
            grid_rows.append([f"Row {index}", *[f"`{value}`" for value in row]])
        lines += markdown_table(grid_rows)

        lines += ["", "### Encoders", ""]
        encoder_rows = [["Control", "CCW", "Press", "CW"]]
        for name in PRESS_NAMES:
            rotation = layer["encoder_rotations"].get(name) or {}
            encoder_rows.append(
                [
                    name,
                    f"`{rotation.get('ccw', 'unavailable')}`",
                    f"`{layer['encoder_presses'][name]}`",
                    f"`{rotation.get('cw', 'unavailable')}`",
                ]
            )
        lines += markdown_table(encoder_rows)

    referenced = [macro for macro in data["macros"] if macro["referenced_by"]]
    if referenced:
        lines += ["", "## Referenced macros", ""]
        macro_rows = [["Slot", "Used by", "Exact text"]]
        for macro in referenced:
            text = (macro["text"] or "").replace("|", "\\|")
            macro_rows.append(
                [str(macro["index"]), ", ".join(macro["referenced_by"]), text]
            )
        lines += markdown_table(macro_rows)

    signals = data.get("custom_signals")
    if isinstance(signals, dict) and signals:
        lines += ["", "## Manifest custom signals", ""]
        lines += markdown_table(
            [["Signal", "Intended command"], *[[str(k), str(v)] for k, v in signals.items()]]
        )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate and normalize a KB16-01 VIA layout for cheat-sheet authoring."
    )
    parser.add_argument("--layout", type=Path, required=True, help="VIA layout JSON")
    parser.add_argument("--manifest", type=Path, help="shortcut manifest JSON")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument(
        "--strict", action="store_true", help="return nonzero for warnings as well as errors"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data = normalize(args.layout.resolve(), args.manifest.resolve() if args.manifest else None)
    if args.format == "json":
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(data), end="")
    if data["errors"] or (args.strict and data["warnings"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

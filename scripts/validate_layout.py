#!/usr/bin/env python3
"""Validate the importable KB16 Codex layout and its manifest."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAYOUT_PATH = ROOT / "config" / "KB16-01_Codex_Desktop_v1.layout.json"
MANIFEST_PATH = ROOT / "config" / "KB16_Codex_Shortcut_Manifest.json"
README_PATH = ROOT / "README.md"
SETUP_PATH = ROOT / "docs" / "KB16_Codex_Desktop_Setup.md"


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        with path.open(encoding="utf-8") as handle:
            value = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(ROOT)}: root must be an object")
        return {}
    return value


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate() -> list[str]:
    errors: list[str] = []
    layout = load_json(LAYOUT_PATH, errors)
    manifest = load_json(MANIFEST_PATH, errors)
    if not layout or not manifest:
        return errors

    require(layout.get("name") == "KB16-01", "layout name must be KB16-01", errors)
    require(
        layout.get("vendorProductId") == 3490715137,
        "layout vendorProductId must encode 0xD010:0x1601",
        errors,
    )

    layers = layout.get("layers")
    require(isinstance(layers, list) and len(layers) == 4, "layout must have four layers", errors)
    if isinstance(layers, list):
        for layer_index, layer in enumerate(layers):
            require(
                isinstance(layer, list) and len(layer) == 20,
                f"layer {layer_index} must have 20 matrix entries",
                errors,
            )

    macros = layout.get("macros")
    require(isinstance(macros, list) and len(macros) == 16, "layout must have 16 macro slots", errors)
    if isinstance(macros, list):
        for macro_index, macro in enumerate(macros):
            require(isinstance(macro, str), f"macro {macro_index} must be text", errors)
            if isinstance(macro, str):
                require("\n" not in macro and "\r" not in macro, f"macro {macro_index} must not submit itself", errors)
        macro_bytes = sum(len(macro.encode("utf-8")) + 1 for macro in macros if isinstance(macro, str))
        require(macro_bytes <= 480, f"macro block is {macro_bytes} bytes; conservative limit is 480", errors)

    encoders = layout.get("encoders")
    require(isinstance(encoders, list) and len(encoders) == 3, "layout must have three encoders", errors)
    if isinstance(encoders, list):
        for encoder_index, encoder in enumerate(encoders):
            require(
                isinstance(encoder, list) and len(encoder) == 4,
                f"encoder {encoder_index} must define all four layers",
                errors,
            )
            if isinstance(encoder, list):
                for layer_index, directions in enumerate(encoder):
                    require(
                        isinstance(directions, list) and len(directions) == 2,
                        f"encoder {encoder_index}, layer {layer_index} must have two directions",
                        errors,
                    )

    if isinstance(layers, list) and len(layers) == 4 and all(isinstance(layer, list) for layer in layers):
        for layer_index in range(3):
            require(
                len(layers[layer_index]) > 15 and layers[layer_index][15] == "MO(3)",
                f"layer {layer_index} WORK key must be MO(3)",
                errors,
            )
        require(len(layers[3]) > 15 and layers[3][15] == "KC_TRNS", "WORK hold position must be transparent on layer 3", errors)
        require(layers[0][1] == "LCTL(LSFT(KC_V))", "CHAT Toggle Voice key must send Control-Shift-V", errors)
        require(layers[0][4] == "LGUI(KC_G)", "upper-left encoder press must retain Search chats", errors)
        require(layers[0][6] == "LGUI(LALT(KC_F13))", "CHAT Global Voice key must retain Command-Option-F13", errors)

        for layer_index, layer in enumerate(layers):
            for keycode in layer:
                if not isinstance(keycode, str):
                    continue
                momentary = re.fullmatch(r"MO\((\d+)\)", keycode)
                if momentary:
                    target = int(momentary.group(1))
                    require(
                        target > layer_index,
                        f"layer {layer_index} momentarily activates lower/equal layer {target}",
                        errors,
                    )
                switch = re.fullmatch(r"TO\((\d+)\)", keycode)
                if switch:
                    require(int(switch.group(1)) in range(4), f"invalid layer switch {keycode}", errors)
                macro = re.fullmatch(r"MACRO\((\d+)\)", keycode)
                if macro and isinstance(macros, list):
                    macro_index = int(macro.group(1))
                    require(macro_index < len(macros), f"invalid macro reference {keycode}", errors)
                    if macro_index < len(macros):
                        require(bool(macros[macro_index]), f"referenced macro {macro_index} is empty", errors)

        flattened = {keycode for layer in layers for keycode in layer if isinstance(keycode, str)}
        required_keycodes = {
            "LGUI(LALT(KC_F13))",
            "LCTL(LSFT(KC_V))",
            "LCTL(LALT(LGUI(KC_LBRC)))",
            "LCTL(LALT(LGUI(KC_RBRC)))",
            *(f"KC_F{number}" for number in range(13, 23)),
        }
        for keycode in sorted(required_keycodes):
            require(keycode in flattened, f"required custom signal {keycode} is absent", errors)
        require("KC_F23" not in flattened and "KC_F24" not in flattened, "unassigned F23/F24 must not appear", errors)

    require(manifest.get("layoutFile") == LAYOUT_PATH.name, "manifest layoutFile must name the current export", errors)
    hardware = manifest.get("hardware", {})
    require(hardware.get("vendorProductIdDecimal") == layout.get("vendorProductId"), "manifest and layout device IDs differ", errors)
    native_shortcuts = manifest.get("nativeShortcuts", {})
    require(native_shortcuts.get("toggleVoiceChat") == "Control-Shift-V", "manifest Toggle Voice shortcut is missing or stale", errors)

    expected_layers = {
        "1": (0, "CHAT", "default"),
        "2": (1, "CONTROL", "persistent"),
        "3": (2, "REVIEW", "persistent"),
        "4": (3, "WORK", "momentary"),
    }
    display = manifest.get("layerDisplay", {})
    for oled, (via_layer, name, behavior) in expected_layers.items():
        entry = display.get(oled, {})
        require(entry.get("viaLayer") == via_layer, f"OLED {oled} VIA layer mismatch", errors)
        require(entry.get("name") == name, f"OLED {oled} mode name mismatch", errors)
        require(entry.get("behavior") == behavior, f"OLED {oled} behavior mismatch", errors)

    expected_custom_signals = {
        "Command-Option-F13",
        "Control-Option-Command-[",
        "Control-Option-Command-]",
        *(f"F{number}" for number in range(13, 23)),
    }
    custom_signals = manifest.get("customSignals", {})
    require(set(custom_signals) == expected_custom_signals, "manifest custom signal set is incomplete or stale", errors)

    for path in (README_PATH, SETUP_PATH):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        require(LAYOUT_PATH.name in text, f"{path.relative_to(ROOT)} does not reference the current layout", errors)
        require("reasoning depth" not in text.lower(), f"{path.relative_to(ROOT)} uses stale reasoning-depth terminology", errors)

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print(f"FAILED: {len(errors)} validation error(s)", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("OK: KB16 Codex Desktop layout, manifest, and documentation are consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

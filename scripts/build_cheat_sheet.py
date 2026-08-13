#!/usr/bin/env python3
"""Build the KB16 cheat-sheet SVG pages and PDF from canonical source data."""

from __future__ import annotations

import argparse
import html
import json
import textwrap
from pathlib import Path

try:
    from reportlab.lib.pagesizes import landscape, letter
    from reportlab.pdfgen import canvas
except ImportError as exc:  # pragma: no cover - actionable CLI error
    raise SystemExit("reportlab is required to build the cheat-sheet PDF") from exc


VIEW_W = 1650
VIEW_H = 1275
BG = "#0A0B0D"
PANEL = "#E8A11A"
PANEL_STROKE = "#FFC247"
KEY = "#17191D"
KEY_STROKE = "#363A41"
ACCENT = "#152D33"
CYAN = "#36E9F5"
WHITE = "#F7F4ED"
MUTED = "#AEB5BE"
INK = "#111317"
BROWN = "#6F3D00"


KEYS: tuple[tuple[tuple[str, str], ...], ...] = (
    (
        ("NEW CHAT", "LGUI(KC_N)"),
        ("TOGGLE\nVOICE", "LCTL(LSFT(KC_V))"),
        ("QUICK CHAT", "LGUI(LALT(KC_N))"),
        ("COMMAND\nMENU", "LGUI(KC_K)"),
        ("DICTATION", "LCTL(LSFT(KC_D))"),
        ("GLOBAL\nVOICE", "LGUI(LALT(KC_F13))"),
        ("SEND", "KC_ENT"),
        ("ESC / STOP", "KC_ESC"),
        ("SIDEBAR", "LGUI(KC_B)"),
        ("OPEN\nFOLDER", "LGUI(KC_O)"),
        ("OPEN\nREVIEW", "LCTL(LSFT(KC_G))"),
        ("TERMINAL", "LCTL(KC_GRV)"),
        ("HOLD\nWORK", "MO(3)"),
        ("CONTROL", "TO(1)"),
        ("REVIEW", "TO(2)"),
        ("MODEL\nPICKER", "LCTL(LALT(LGUI(KC_M)))"),
    ),
    (
        ("EFFORT -", "LCTL(LALT(LGUI(KC_LBRC)))"),
        ("EFFORT +", "LCTL(LALT(LGUI(KC_RBRC)))"),
        ("MODEL\nPICKER", "LCTL(LALT(LGUI(KC_M)))"),
        ("PLAN\nMODE", "KC_F14"),
        ("FAST\nMODE", "KC_F15"),
        ("ATTACH\nFILES", "KC_F16"),
        ("APPROVE", "KC_F17"),
        ("DECLINE", "KC_F18"),
        ("PROJECT\nPICKER", "KC_F22"),
        ("COPY AS\nMARKDOWN", "KC_F19"),
        ("SIDE\nCHAT", "KC_F21"),
        ("CONTINUE\nNEW CHAT", "KC_F20"),
        ("HOLD\nWORK", "MO(3)"),
        ("CHAT", "TO(0)"),
        ("REVIEW", "TO(2)"),
        ("ESC / STOP", "KC_ESC"),
    ),
    (
        ("OPEN\nREVIEW", "LCTL(LSFT(KC_G))"),
        ("TOGGLE\nPANEL", "LGUI(LALT(KC_B))"),
        ("APPROVE", "KC_F17"),
        ("DECLINE", "KC_F18"),
        ("PREVIOUS\nCHAT", "LGUI(LSFT(KC_LBRC))"),
        ("NEXT\nCHAT", "LGUI(LSFT(KC_RBRC))"),
        ("COPY AS\nMARKDOWN", "KC_F19"),
        ("CONTINUE\nNEW CHAT", "KC_F20"),
        ("COPY", "LGUI(KC_C)"),
        ("FIND IN\nCHAT", "LGUI(KC_F)"),
        ("TERMINAL", "LCTL(KC_GRV)"),
        ("COMMAND\nMENU", "LGUI(KC_K)"),
        ("HOLD\nWORK", "MO(3)"),
        ("CHAT", "TO(0)"),
        ("CONTROL", "TO(1)"),
        ("ESC / STOP", "KC_ESC"),
    ),
    (
        ("SUMMARIZE", "MACRO(0)"),
        ("IMPLEMENT", "MACRO(1)"),
        ("REVIEW\nONLY", "MACRO(2)"),
        ("EXPLAIN", "MACRO(3)"),
        ("DIAGNOSE\nONLY", "MACRO(4)"),
        ("VERIFY", "MACRO(5)"),
        ("UPDATE\nDOCS", "MACRO(6)"),
        ("PLAN\nFIRST", "MACRO(7)"),
        ("COPY", "LGUI(KC_C)"),
        ("PASTE", "LGUI(KC_V)"),
        ("UNDO", "LGUI(KC_Z)"),
        ("REDO", "LGUI(LSFT(KC_Z))"),
        ("HOLD /\nRELEASE", "KC_TRNS"),
        ("CHAT", "TO(0)"),
        ("CONTROL", "TO(1)"),
        ("REVIEW", "TO(2)"),
    ),
)

ENCODERS = (
    (
        "UPPER-LEFT",
        ("EFFORT -", "MODEL PICKER", "EFFORT +"),
        ("LCTL(LALT(LGUI(KC_LBRC)))", "LCTL(LALT(LGUI(KC_M)))", "LCTL(LALT(LGUI(KC_RBRC)))"),
    ),
    (
        "UPPER-RIGHT",
        ("PAGE UP", "COMMAND MENU", "PAGE DOWN"),
        ("KC_PGUP", "LGUI(KC_K)", "KC_PGDN"),
    ),
    (
        "LARGE DIAL",
        ("PREVIOUS CHAT", "SEARCH CHATS", "NEXT CHAT"),
        ("LGUI(LSFT(KC_LBRC))", "LGUI(KC_G)", "LGUI(LSFT(KC_RBRC))"),
    ),
)

PRESS_INDEXES = (4, 9, 14)
MACRO_LABELS = ("Summarize", "Implement", "Review only", "Explain", "Diagnose only", "Verify", "Update docs", "Plan first")


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: root must be an object")
    return value


def grid_codes(layer: list[str]) -> list[str]:
    return [layer[row * 5 + column] for row in range(4) for column in range(4)]


def validate_sources(layout: dict, manifest: dict, setup_text: str, layout_path: Path) -> None:
    errors: list[str] = []
    if manifest.get("layoutFile") != layout_path.name:
        errors.append("manifest layoutFile does not name the selected layout")
    layers = layout.get("layers")
    if not isinstance(layers, list) or len(layers) != 4:
        errors.append("layout must contain four layers")
        layers = []
    for layer_index, expected in enumerate(KEYS):
        if layer_index >= len(layers) or not isinstance(layers[layer_index], list) or len(layers[layer_index]) != 20:
            errors.append(f"layer {layer_index} must contain 20 matrix entries")
            continue
        actual = grid_codes(layers[layer_index])
        for position, ((label, keycode), observed) in enumerate(zip(expected, actual, strict=True)):
            if observed != keycode:
                row, column = divmod(position, 4)
                errors.append(
                    f"{label.replace(chr(10), ' ')} expects {keycode} at VIA {layer_index} "
                    f"R{row + 1}C{column + 1}, found {observed}"
                )

    encoders = layout.get("encoders")
    for encoder_index, (name, _labels, expected_codes) in enumerate(ENCODERS):
        if not isinstance(encoders, list) or encoder_index >= len(encoders):
            errors.append(f"{name} encoder data is missing")
            continue
        for layer_index in range(4):
            rotations = encoders[encoder_index][layer_index]
            press = layers[layer_index][PRESS_INDEXES[encoder_index]] if layers else None
            observed = (rotations[0], press, rotations[1])
            if observed != expected_codes:
                errors.append(f"{name} differs on VIA layer {layer_index}: {observed!r}")

    macros = layout.get("macros")
    if not isinstance(macros, list) or len(macros) < 8 or any(not isinstance(value, str) or not value for value in macros[:8]):
        errors.append("WORK macros 0-7 must contain nonempty text")

    display = manifest.get("layerDisplay", {})
    expected_display = {
        "1": (0, "CHAT", "default"),
        "2": (1, "CONTROL", "persistent"),
        "3": (2, "REVIEW", "persistent"),
        "4": (3, "WORK", "momentary"),
    }
    for oled, (via, name, behavior) in expected_display.items():
        item = display.get(oled, {})
        if (item.get("viaLayer"), item.get("name"), item.get("behavior")) != (via, name, behavior):
            errors.append(f"OLED {oled} layer metadata is missing or stale")

    native = manifest.get("nativeShortcuts", {})
    if native.get("dictation") != "Control-Shift-D" or native.get("toggleVoiceChat") != "Control-Shift-V":
        errors.append("voice native-shortcut metadata is missing or stale")
    if manifest.get("customSignals", {}).get("Command-Option-F13") != "Global voice chat hotkey":
        errors.append("global voice custom signal is missing or stale")
    if manifest.get("customSignals", {}).get("Control-Option-Command-M") != "Open model picker":
        errors.append("model-picker custom signal is missing or stale")

    for phrase in ("Toggle Voice", "Global Voice", "Search chats", "WORK, momentary"):
        if phrase not in setup_text:
            errors.append(f"setup guide does not support displayed label: {phrase}")

    if errors:
        raise ValueError("Cheat-sheet source validation failed:\n- " + "\n- ".join(errors))


class SvgRenderer:
    def __init__(self, title: str, description: str):
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="11in" height="8.5in" viewBox="0 0 {VIEW_W} {VIEW_H}" role="img" aria-labelledby="title description">',
            f'<title id="title">{html.escape(title)}</title>',
            f'<desc id="description">{html.escape(description)}</desc>',
            f'<rect width="{VIEW_W}" height="{VIEW_H}" fill="{BG}"/>',
        ]

    def rect(self, x: float, y: float, w: float, h: float, fill: str, stroke: str | None = None, width: float = 1, radius: float = 0) -> None:
        stroke_attr = f' stroke="{stroke}" stroke-width="{width}"' if stroke else ""
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}"{stroke_attr}/>')

    def text(self, x: float, y: float, value: str, size: float, color: str, bold: bool = False, anchor: str = "start") -> None:
        weight = 800 if bold else 500
        self.parts.append(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
            f'style="font: {weight} {size}px -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif; fill: {color};">'
            f'{html.escape(value)}</text>'
        )

    def finish(self) -> str:
        return "\n".join([*self.parts, "</svg>", ""])


class PdfRenderer:
    def __init__(self, pdf_canvas: canvas.Canvas):
        self.canvas = pdf_canvas

    def rect(self, x: float, y: float, w: float, h: float, fill: str, stroke: str | None = None, width: float = 1, radius: float = 0) -> None:
        c = self.canvas
        c.setFillColor(fill)
        c.setStrokeColor(stroke or fill)
        c.setLineWidth(width)
        c.roundRect(x, VIEW_H - y - h, w, h, radius, fill=1, stroke=1 if stroke else 0)

    def text(self, x: float, y: float, value: str, size: float, color: str, bold: bool = False, anchor: str = "start") -> None:
        c = self.canvas
        c.setFillColor(color)
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        baseline = VIEW_H - y
        if anchor == "middle":
            c.drawCentredString(x, baseline, value)
        elif anchor == "end":
            c.drawRightString(x, baseline, value)
        else:
            c.drawString(x, baseline, value)


def text_lines(renderer: SvgRenderer | PdfRenderer, x: float, y: float, lines: list[str] | tuple[str, ...], size: float, color: str, *, bold: bool = False, anchor: str = "start", leading: float | None = None) -> None:
    step = leading or size * 1.25
    for index, line in enumerate(lines):
        renderer.text(x, y + index * step, line, size, color, bold=bold, anchor=anchor)


def wrap(value: str, width: int) -> list[str]:
    return textwrap.wrap(value, width=width, break_long_words=False, break_on_hyphens=False) or [""]


def draw_header(renderer: SvgRenderer | PdfRenderer, title: str, subtitle: str, page: str) -> None:
    renderer.text(45, 65, title, 45, WHITE, bold=True)
    renderer.text(45, 98, subtitle, 19, MUTED)
    renderer.text(1605, 65, page, 19, CYAN, bold=True, anchor="end")


def draw_key(renderer: SvgRenderer | PdfRenderer, x: float, y: float, label: str, accent: bool) -> None:
    renderer.rect(x, y, 143, 70, ACCENT if accent else KEY, CYAN if accent else KEY_STROKE, 2, 11)
    lines = label.splitlines()
    if len(lines) == 1:
        text_lines(renderer, x + 71.5, y + 41, lines, 17, WHITE, bold=True, anchor="middle")
    else:
        text_lines(renderer, x + 71.5, y + 29, lines, 16, WHITE, bold=True, anchor="middle", leading=21)


def draw_layer_panel(renderer: SvgRenderer | PdfRenderer, x: float, y: float, oled: str, meta: dict, labels: tuple[tuple[str, str], ...]) -> None:
    renderer.rect(x, y, 780, 430, PANEL, PANEL_STROKE, 3, 28)
    renderer.rect(x + 26, y + 24, 82, 58, INK, radius=10)
    renderer.text(x + 67, y + 65, oled, 31, CYAN, bold=True, anchor="middle")
    renderer.text(x + 126, y + 56, meta["name"], 27, INK, bold=True)
    renderer.text(x + 126, y + 81, f'VIA {meta["viaLayer"]} / {meta["behavior"].upper()}', 15, BROWN, bold=True)

    grid_x = x + 143
    grid_y = y + 94
    for position, (label, _keycode) in enumerate(labels):
        row, column = divmod(position, 4)
        accent = position >= 12 and (column < 3 or meta["name"] == "WORK")
        draw_key(renderer, grid_x + column * 151, grid_y + row * 78, label, accent)


def draw_page_one(renderer: SvgRenderer | PdfRenderer, manifest: dict) -> None:
    draw_header(renderer, "KB16 x CODEX", "PURE VIA / macOS / physical key map", "PAGE 1 / MAP")
    display = manifest["layerDisplay"]
    positions = ((35, 120), (835, 120), (35, 570), (835, 570))
    for index, ((x, y), oled) in enumerate(zip(positions, ("1", "2", "3", "4"), strict=True)):
        draw_layer_panel(renderer, x, y, oled, display[oled], KEYS[index])

    renderer.rect(35, 1025, 1580, 195, "#14161A", "#2D3239", 2, 24)
    for index, (name, labels, _codes) in enumerate(ENCODERS):
        x = 70 + index * 520
        renderer.rect(x, 1050, 470, 140, "#202329", "#3A3F47", 2, 18)
        renderer.text(x + 22, 1082, name, 21, CYAN, bold=True)
        renderer.text(x + 22, 1113, f"CCW  {labels[0]}", 16, WHITE, bold=True)
        renderer.text(x + 22, 1142, f"PRESS  {labels[1]}", 16, WHITE, bold=True)
        renderer.text(x + 22, 1171, f"CW  {labels[2]}", 16, WHITE, bold=True)
    renderer.text(1605, 1248, "OLED 1-4 maps directly to VIA 0-3 / WORK is held; CONTROL and REVIEW persist", 14, MUTED, anchor="end")


def draw_voice_card(renderer: SvgRenderer | PdfRenderer, x: float, title: str, shortcut: str, description: str, accent: bool = False) -> None:
    renderer.rect(x, 130, 500, 150, ACCENT if accent else "#17191D", CYAN if accent else "#363A41", 2, 20)
    renderer.text(x + 24, 168, title, 24, CYAN if accent else WHITE, bold=True)
    renderer.text(x + 476, 168, shortcut, 20, WHITE, bold=True, anchor="end")
    text_lines(renderer, x + 24, 207, wrap(description, 44), 18, MUTED, leading=24)


def draw_page_two(renderer: SvgRenderer | PdfRenderer, layout: dict, manifest: dict) -> None:
    draw_header(renderer, "KB16 x CODEX", "PROMPTS / BINDINGS / OPERATING NOTES", "PAGE 2 / REFERENCE")
    native = manifest["nativeShortcuts"]
    draw_voice_card(renderer, 35, "DICTATION", native["dictation"], "Inserts dictated text into the focused composer.")
    draw_voice_card(renderer, 575, "TOGGLE VOICE", native["toggleVoiceChat"], "Toggles voice chat while ChatGPT is focused.", accent=True)
    draw_voice_card(renderer, 1115, "GLOBAL VOICE", "Cmd-Opt-F13", "Configurable voice hotkey that works anywhere in macOS.")

    renderer.rect(35, 315, 750, 870, PANEL, PANEL_STROKE, 3, 26)
    renderer.text(65, 360, "ONE-TIME CUSTOM BINDINGS", 27, INK, bold=True)
    renderer.text(65, 389, "Record these signals in Settings > Keyboard Shortcuts.", 17, BROWN, bold=True)
    renderer.rect(60, 415, 700, 48, INK, radius=8)
    renderer.text(80, 447, "SIGNAL", 16, CYAN, bold=True)
    renderer.text(300, 447, "CHATGPT COMMAND", 16, CYAN, bold=True)
    custom = manifest["customSignals"]
    row_y = 472
    for row, (signal, command) in enumerate(custom.items()):
        fill = "#F5B642" if row % 2 == 0 else "#E8A11A"
        renderer.rect(60, row_y + row * 51, 700, 47, fill, radius=5)
        renderer.text(80, row_y + row * 51 + 31, signal, 17, INK, bold=True)
        renderer.text(330, row_y + row * 51 + 31, command, 17, INK)
    renderer.text(65, 1150, "Ctrl-Opt-Cmd-M opens Model Picker; Cmd-Opt-F13 is Global Voice.", 15, BROWN, bold=True)
    renderer.text(65, 1176, "Approve / Decline act on permission requests, not review diffs.", 15, BROWN, bold=True)

    renderer.rect(815, 315, 800, 610, "#14161A", "#2D3239", 2, 26)
    renderer.text(845, 360, "WORK PROMPTS / INSERTED TEXT", 27, CYAN, bold=True)
    macros = layout["macros"]
    for index, (label, macro) in enumerate(zip(MACRO_LABELS, macros[:8], strict=True)):
        column = index % 2
        row = index // 2
        x = 845 + column * 375
        y = 390 + row * 126
        renderer.rect(x, y, 345, 108, KEY, KEY_STROKE, 2, 14)
        renderer.text(x + 18, y + 31, f"{index + 1}. {label.upper()}", 18, WHITE, bold=True)
        text_lines(renderer, x + 18, y + 59, wrap(macro, 39), 16, MUTED, leading=20)
    renderer.text(845, 900, "Macros insert without submitting. Review Only, Diagnose Only, and Explain do not authorize edits.", 16, MUTED)

    renderer.rect(815, 950, 800, 235, "#14161A", "#2D3239", 2, 26)
    renderer.text(845, 993, "USE NOTES", 25, CYAN, bold=True)
    notes = (
        "Hold WORK from CHAT, CONTROL, or REVIEW; release to return to the previous mode.",
        "VIA cannot trigger per-diff Accept or Reject without matching ChatGPT commands.",
        "Leave unavailable custom commands unbound.",
    )
    for index, note in enumerate(notes):
        renderer.text(850, 1031 + index * 44, "-", 18, PANEL_STROKE, bold=True)
        text_lines(renderer, 872, 1031 + index * 44, wrap(note, 72), 17, WHITE, leading=20)
    renderer.text(
        1605,
        1248,
        f'Verified against ChatGPT desktop build {manifest.get("verifiedAppVersion", "unknown")} on {manifest.get("verifiedDate", "unknown")}',
        15,
        MUTED,
        anchor="end",
    )


def write_svg(path: Path, draw, *args) -> None:
    renderer = SvgRenderer("KB16 Codex Desktop cheat sheet", "Two-page KB16 key map and shortcut reference.")
    draw(renderer, *args)
    path.write_text(renderer.finish(), encoding="utf-8")


def write_pdf(path: Path, layout: dict, manifest: dict) -> None:
    page_size = landscape(letter)
    pdf = canvas.Canvas(str(path), pagesize=page_size, pageCompression=1)
    pdf.setTitle("KB16 Codex Desktop Cheat Sheet")
    pdf.setAuthor("KB16 Codex Desktop project")
    pdf.setSubject("Pure VIA key map, WORK prompts, encoders, and ChatGPT shortcut bindings")
    pdf.setCreator("scripts/build_cheat_sheet.py")
    for draw, args in ((draw_page_one, (manifest,)), (draw_page_two, (layout, manifest))):
        pdf.saveState()
        pdf.scale(page_size[0] / VIEW_W, page_size[1] / VIEW_H)
        renderer = PdfRenderer(pdf)
        renderer.rect(0, 0, VIEW_W, VIEW_H, BG)
        draw(renderer, *args)
        pdf.restoreState()
        pdf.showPage()
    pdf.save()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--layout", type=Path, default=Path("config/KB16-01_Codex_Desktop_v1.layout.json"))
    parser.add_argument("--manifest", type=Path, default=Path("config/KB16_Codex_Shortcut_Manifest.json"))
    parser.add_argument("--setup", type=Path, default=Path("docs/KB16_Codex_Desktop_Setup.md"))
    parser.add_argument("--output-dir", type=Path, default=Path("docs/cheat-sheet"))
    return parser


def main() -> int:
    args = build_parser().parse_args()
    layout = load_json(args.layout)
    manifest = load_json(args.manifest)
    setup_text = args.setup.read_text(encoding="utf-8")
    validate_sources(layout, manifest, setup_text, args.layout)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    map_svg = args.output_dir / "KB16_Codex_Desktop_Cheat_Sheet.svg"
    reference_svg = args.output_dir / "KB16_Codex_Desktop_Cheat_Sheet_Reference.svg"
    pdf_path = args.output_dir / "KB16_Codex_Desktop_Cheat_Sheet.pdf"
    write_svg(map_svg, draw_page_one, manifest)
    write_svg(reference_svg, draw_page_two, layout, manifest)
    write_pdf(pdf_path, layout, manifest)
    for path in (map_svg, reference_svg, pdf_path):
        print(f"Wrote {path} ({path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

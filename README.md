# KB16 Codex Desktop Macropad

A pure-VIA layout for the DOIO/KeebMonkey Megalodon KB16-01, designed for Codex in the ChatGPT desktop app on macOS. It turns the 16-key, three-knob pad into a task navigator, voice controller, prompt launcher, model/effort console, and review companion without firmware flashing or background automation.

## Current release: v2

Version 2 fixes cross-layer access, uses only current bindable ChatGPT desktop commands, and maps the hardware's OLED directly to four memorable modes:

| OLED | VIA | Mode | Purpose |
|---|---:|---|---|
| `1` | 0 | CHAT | Everyday navigation and composer controls |
| `2` | 1 | CONTROL | Model, effort, plan, Fast mode, and approvals |
| `3` | 2 | REVIEW | Review navigation and handoff actions |
| `4` | 3 | WORK | Momentary prompt and editing macros |

WORK is the highest-numbered layer, so holding it works correctly from CHAT, CONTROL, and REVIEW.

## Files

- [`outputs/KB16-01_Codex_Desktop_v2.layout.json`](outputs/KB16-01_Codex_Desktop_v2.layout.json) — current layout to import into VIA
- [`outputs/KB16_Codex_Desktop_Setup.md`](outputs/KB16_Codex_Desktop_Setup.md) — complete setup, binding, recovery, and test guide
- [`outputs/KB16_Codex_Desktop_v2_Cheat_Sheet.svg`](outputs/KB16_Codex_Desktop_v2_Cheat_Sheet.svg) — printable visual reference
- [`outputs/KB16_Codex_Shortcut_Manifest.json`](outputs/KB16_Codex_Shortcut_Manifest.json) — machine-readable v2 reference
- [`scripts/validate_layout.py`](scripts/validate_layout.py) — dependency-free structural and consistency validator
- [`outputs/KB16-01_Codex_Desktop_v1.layout.json`](outputs/KB16-01_Codex_Desktop_v1.layout.json) — retained legacy v1 backup

## Quick start

1. Connect the wired KB16-01 and open [VIA](https://usevia.app/) in a Chromium-based browser.
2. Back up the current device layout.
3. Load `outputs/KB16-01_Codex_Desktop_v2.layout.json`.
4. Follow the setup guide to bind Live Voice and the `F13`–`F22` control signals.
5. Print or keep the cheat sheet nearby while the layout becomes familiar.

The layout targets USB ID `0xD010:0x1601`. The native shortcuts were checked against the OpenAI command reference, and optional control commands were verified against ChatGPT desktop app build `26.803.61601` on 2026-08-13.

## Validate

Run:

```sh
python3 scripts/validate_layout.py
```

## Status

This is a personal, unofficial configuration and is not affiliated with DOIO, KeebMonkey, Work Louder, VIA, or OpenAI.

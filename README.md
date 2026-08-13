# KB16 Codex Desktop Macropad

A pure-VIA layout for the DOIO/KeebMonkey Megalodon KB16-01, designed for Codex in the ChatGPT desktop app on macOS. It turns the 16-key, three-knob pad into a task navigator, voice controller, prompt launcher, model/effort console, and review companion without firmware flashing or background automation.

## Current layout

The current v1 layout fixes cross-layer access, uses only current bindable ChatGPT desktop commands, and maps the hardware's OLED directly to four memorable modes:

| OLED | VIA | Mode | Purpose |
|---|---:|---|---|
| `1` | 0 | CHAT | Everyday navigation and composer controls |
| `2` | 1 | CONTROL | Model, effort, plan, Fast mode, and approvals |
| `3` | 2 | REVIEW | Review navigation and handoff actions |
| `4` | 3 | WORK | Momentary prompt and editing macros |

WORK is the highest-numbered layer, so holding it works correctly from CHAT, CONTROL, and REVIEW.

## Repository layout

- [`config/`](config/) contains the canonical VIA layout and machine-readable shortcut manifest.
- [`docs/KB16_Codex_Desktop_Setup.md`](docs/KB16_Codex_Desktop_Setup.md) is the complete setup, binding, recovery, and test guide.
- [`docs/cheat-sheet/KB16_Codex_Desktop_Cheat_Sheet.pdf`](docs/cheat-sheet/KB16_Codex_Desktop_Cheat_Sheet.pdf) is the print-ready two-page US Letter cheat sheet. The same folder contains the editable SVG pages and [`previews/`](docs/cheat-sheet/previews/) contains 150 dpi PNG renders.
- [`scripts/`](scripts/) contains the source-driven cheat-sheet builder and dependency-free layout validator.
- [`.agents/skills/`](.agents/skills/) contains the repository-specific Codex workflows for maintaining the cheat sheet and personalizing WORK prompts.

Key files:

- [`config/KB16-01_Codex_Desktop_v1.layout.json`](config/KB16-01_Codex_Desktop_v1.layout.json) — current layout to import into VIA
- [`config/KB16_Codex_Shortcut_Manifest.json`](config/KB16_Codex_Shortcut_Manifest.json) — machine-readable shortcut reference
- [`docs/cheat-sheet/KB16_Codex_Desktop_Cheat_Sheet.svg`](docs/cheat-sheet/KB16_Codex_Desktop_Cheat_Sheet.svg) and [`docs/cheat-sheet/KB16_Codex_Desktop_Cheat_Sheet_Reference.svg`](docs/cheat-sheet/KB16_Codex_Desktop_Cheat_Sheet_Reference.svg) — editable cheat-sheet pages
- [`scripts/validate_layout.py`](scripts/validate_layout.py) — dependency-free structural and consistency validator
- [`scripts/build_cheat_sheet.py`](scripts/build_cheat_sheet.py) — source-driven SVG and PDF generator that fails on stale mappings
- [`.agents/skills/personalize-kb16-work-prompts/SKILL.md`](.agents/skills/personalize-kb16-work-prompts/SKILL.md) — Codex skill for creating safe, role-specific WORK prompt packs
- [`.agents/skills/build-kb16-cheat-sheet/SKILL.md`](.agents/skills/build-kb16-cheat-sheet/SKILL.md) — repository skill for generating and QAing future printable cheat sheets

## Quick start

1. Connect the wired KB16-01 and open [VIA](https://usevia.app/) in a Chromium-based browser.
2. Back up the current device layout.
3. Load `config/KB16-01_Codex_Desktop_v1.layout.json`.
4. Follow the setup guide to bind Global Voice and the `F13`–`F22` control signals. Toggle Voice works natively.
5. Print or keep the cheat sheet nearby while the layout becomes familiar.

The layout targets USB ID `0xD010:0x1601`. The native shortcuts were checked against the OpenAI command reference, and optional control commands were verified against ChatGPT desktop app build `26.803.61601` on 2026-08-13.

## Personalize WORK prompts

This repository includes a Codex skill that turns a description of your repeated workflows into eight labeled WORK prompts, a reusable profile, a separate VIA layout, and a Markdown prompt map. Invoke it from a Codex task in this repository, for example:

```text
$personalize-kb16-work-prompts Make the WORK layer fit my Python debugging workflow.
```

The skill preserves the source layout by default, verifies that only macro slots 0–7 changed, rejects auto-submitting control characters, and enforces the conservative 512-byte macro-storage ceiling.

## Validate

Run:

```sh
python3 scripts/validate_layout.py
```

To rebuild the editable cheat-sheet pages and PDF after a layout change, install ReportLab and run:

```sh
python3 scripts/build_cheat_sheet.py
```

## Status

This is a personal, unofficial configuration and is not affiliated with DOIO, KeebMonkey, Work Louder, VIA, or OpenAI.

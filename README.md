# KB16 Codex Desktop Macropad

A VIA-only layout for the wired DOIO/KeebMonkey Megalodon KB16-01. It maps the pad's 16 keys and three clickable encoders to Codex controls in the ChatGPT desktop app for macOS. No firmware changes or background automation are required.

## Layout

The OLED number identifies the active mode:

| OLED | VIA layer | Mode | Behavior |
|---|---:|---|---|
| `1` | 0 | CHAT | Default chat and composer controls |
| `2` | 1 | CONTROL | Persistent model, effort, plan, and permission controls |
| `3` | 2 | REVIEW | Persistent review and handoff controls |
| `4` | 3 | WORK | Momentary prompt macros and editing keys |

WORK occupies the highest layer so it can be held from CHAT, CONTROL, or REVIEW.

## Install

1. Connect the wired KB16-01 and open [VIA](https://usevia.app/) in a Chromium-based browser.
2. Save a backup of the device's current layout.
3. Load [`config/KB16-01_Codex_Desktop_v1.layout.json`](config/KB16-01_Codex_Desktop_v1.layout.json).
4. Bind Global Voice, the Model Picker chord, and the `F14`-`F22` signals by following the [setup guide](docs/KB16_Codex_Desktop_Setup.md).
5. Keep the [cheat sheet](docs/cheat-sheet/KB16_Codex_Desktop_Cheat_Sheet.pdf) nearby until the layout is familiar.

The layout targets USB ID `0xD010:0x1601`. Documented command shortcuts were checked against the official command reference. Toggle Voice and custom command names were verified in ChatGPT desktop app build `26.803.61601` on 2026-08-13.

## Repository contents

| Path | Contents |
|---|---|
| [`config/`](config/) | Canonical VIA layout and shortcut manifest |
| [`docs/KB16_Codex_Desktop_Setup.md`](docs/KB16_Codex_Desktop_Setup.md) | Installation, bindings, tests, and recovery |
| [`docs/cheat-sheet/`](docs/cheat-sheet/) | Print-ready PDF, editable SVG pages, and PNG previews |
| [`scripts/`](scripts/) | Layout validator and cheat-sheet builder |
| [`.agents/skills/build-kb16-cheat-sheet/`](.agents/skills/build-kb16-cheat-sheet/) | Cheat-sheet maintenance workflow |
| [`.agents/skills/personalize-kb16-work-prompts/`](.agents/skills/personalize-kb16-work-prompts/) | WORK-prompt personalization workflow |

## Personalize WORK prompts

The included Codex skill creates eight prompt macros, a reusable profile, a prompt map, and a separate VIA layout:

```text
$personalize-kb16-work-prompts Make the WORK layer fit my Python debugging workflow.
```

It changes only macro slots 0-7, does not add auto-submit characters, and enforces the layout's macro-storage limit.

## Validate and rebuild

```sh
python3 scripts/validate_layout.py
python3 scripts/build_cheat_sheet.py
```

The builder requires ReportLab.

## Status

This is an unofficial personal configuration. It is not affiliated with DOIO, KeebMonkey, Work Louder, VIA, or OpenAI.

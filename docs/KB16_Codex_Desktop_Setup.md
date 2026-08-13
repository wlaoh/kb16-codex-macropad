# KB16 Codex Desktop Controller — Pure VIA

This layout turns the wired DOIO/KeebMonkey Megalodon **KB16-01** into a four-mode controller for Codex in the ChatGPT desktop app on macOS. It uses VIA only: no firmware flashing, `config.toml` changes, Hammerspoon rules, Shortcuts automations, or background services.

## Compatibility

- USB vendor ID: `0xD010`
- USB product ID: `0x1601`
- VIA device ID: `3490715137`
- Matrix: 4 rows × 5 columns
- Controls: 16 keys, three clickable encoders, four layers
- Verified ChatGPT desktop app build: `26.803.61601`
- Verification date: 2026-08-13

This does not target the older `0xFEED:0x6060` definition or the wireless KB16.

## Install the layout

1. Open [VIA](https://usevia.app/) in a Chromium-based browser.
2. Connect and authorize the wired KB16. Confirm VIA identifies it as **KB16-01**.
3. Open **Configure → Save + Load**.
4. Save the current device layout as a backup.
5. Choose **Load Saved Layout** and select `KB16-01_Codex_Desktop_v1.layout.json`.
6. Wait for **Successfully updated layout** before unplugging the pad.

The layout is stored on the KB16. Keep both your original backup and the current JSON.

## Read the hardware

The 4×4 key grid is on the left. The two small encoders are at the upper right, the OLED is below them, and the large dial is at the lower right.

The OLED uses one-based numbers while VIA uses zero-based layer indexes:

| OLED | VIA layer | Mode | Behavior |
|---|---:|---|---|
| `1` | 0 | CHAT | Default layer |
| `2` | 1 | CONTROL | Persistent until another mode is selected |
| `3` | 2 | REVIEW | Persistent until another mode is selected |
| `4` | 3 | WORK | Active only while WORK is held |

WORK is deliberately layer 3, the highest layer. That makes its momentary mappings accessible from every persistent mode. Reconnecting the pad returns it to CHAT.

## Configure ChatGPT desktop shortcuts

Native shortcuts work immediately. Global Voice and CONTROL actions use uncommon signals that must be recorded once.

### Voice controls

**TOGGLE VOICE** sends the native `Control-Shift-V` shortcut. It toggles voice chat while the ChatGPT app is focused and requires no custom binding.

**GLOBAL VOICE** works from anywhere in macOS. Open **Settings → Voice → Voice chat hotkey**, activate the shortcut field, and press the physical **GLOBAL VOICE** key. It sends `Command-Option-F13`.

Voice chat must begin in a new, empty chat or task. Dictation is separate and uses the native `Control-Shift-D` shortcut. Search chats remains available by pressing the large dial.

### CONTROL signals

Open **Settings → Keyboard Shortcuts**. For each available command below, search its exact name, activate its shortcut field, and perform the listed physical control on the KB16.

| Physical control | Signal | Exact command name |
|---|---|---|
| Upper-left knob counterclockwise | `⌃⌥⌘[` | Decrease reasoning effort |
| Upper-left knob clockwise | `⌃⌥⌘]` | Increase reasoning effort |
| Press upper-left knob or a Model picker key | `⌃⌥⌘M` | Open model picker |
| CONTROL row 1, column 4 | `F14` | Toggle plan mode |
| CONTROL row 2, column 1 | `F15` | Toggle Fast mode |
| CONTROL row 2, column 2 | `F16` | Attach files and folders |
| CONTROL row 2, column 3 | `F17` | Approve request |
| CONTROL row 2, column 4 | `F18` | Decline request |
| CONTROL row 3, column 2 | `F19` | Copy as Markdown |
| CONTROL row 3, column 4 | `F20` | Continue in new chat |
| CONTROL row 3, column 3 | `F21` | Open side chat |
| CONTROL row 3, column 1 | `F22` | Open project picker |

`Control-Option-Command-M` for the model picker and `Command-Option-F13` for Voice are separate signals. If a named command is unavailable in your app build or account, leave that signal unbound.

## Knobs — every mode

| Physical control | Counterclockwise | Press | Clockwise |
|---|---|---|---|
| Upper-left small knob | Effort down | Model picker | Effort up |
| Upper-right small knob | Page up | Command menu | Page down |
| Large lower-right dial | Previous chat | Search chats | Next chat |

## OLED 1 — CHAT

| | Column 1 | Column 2 | Column 3 | Column 4 |
|---|---|---|---|---|
| Row 1 | New chat | Toggle Voice | Quick chat | Command menu |
| Row 2 | Dictation | Global Voice | Send | Escape / interrupt |
| Row 3 | Sidebar | Open folder | Open Review | Terminal |
| Row 4 | Hold WORK | Enter CONTROL | Enter REVIEW | Model picker |

CHAT contains the high-frequency actions and is the power-on default.

## OLED 2 — CONTROL

| | Column 1 | Column 2 | Column 3 | Column 4 |
|---|---|---|---|---|
| Row 1 | Effort down | Effort up | Model picker | Plan mode |
| Row 2 | Fast mode | Attach files | Approve request | Decline request |
| Row 3 | Project picker | Copy as Markdown | Open side chat | Continue in new chat |
| Row 4 | Hold WORK | Return CHAT | Enter REVIEW | Escape / interrupt |

Approve and Decline apply to active permission requests. They do not accept or reject individual code-review diffs.

## OLED 3 — REVIEW

| | Column 1 | Column 2 | Column 3 | Column 4 |
|---|---|---|---|---|
| Row 1 | Open Review | Toggle Review panel | Approve request | Decline request |
| Row 2 | Previous chat | Next chat | Copy as Markdown | Continue in new chat |
| Row 3 | Copy | Find in chat | Terminal | Command menu |
| Row 4 | Hold WORK | Return CHAT | Enter CONTROL | Escape / interrupt |

Pure VIA cannot press the review UI's per-diff Accept or Reject buttons unless ChatGPT exposes them as keyboard-shortcut commands. The current layout intentionally avoids nonfunctional placeholder bindings.

## OLED 4 — WORK, momentary

Hold the bottom-left WORK key from CHAT, CONTROL, or REVIEW. Release it to return to the prior mode. Prompt macros insert text into the composer but never submit it.

| | Column 1 | Column 2 | Column 3 | Column 4 |
|---|---|---|---|---|
| Row 1 | Summarize | Implement | Review only | Explain |
| Row 2 | Diagnose only | Verify | Update docs | Plan first |
| Row 3 | Copy | Paste | Undo | Redo |
| Row 4 | Hold/release | Return CHAT | Enter CONTROL | Enter REVIEW |

### Macro text

1. `Summarize progress, blockers, and next steps.`
2. `Implement the change. Preserve unrelated work and verify it.`
3. `Review changes for bugs, risks, and missing tests. Do not edit.`
4. `Explain the code or problem and its key tradeoffs.`
5. `Diagnose the root cause. Do not edit; report evidence and a fix.`
6. `Run relevant tests. Investigate and summarize failures.`
7. `Update documentation for the current change.`
8. `Propose a concise plan before editing.`

The complete sixteen-slot macro block is kept below 480 UTF-8 bytes, including slot terminators, for conservative firmware compatibility.

## Five-minute verification

Test the pad after loading and binding:

1. Confirm the OLED shows `1` after reconnecting.
2. Enter CONTROL and REVIEW; confirm the OLED shows `2` and `3`.
3. Hold WORK from all three modes; confirm the OLED temporarily shows `4` and a macro key inserts text without submitting.
4. Turn and press all three knobs in CHAT.
5. In a new empty task, test Dictation, Toggle Voice, and Global Voice separately. Confirm Global Voice also works while another app is focused.
6. In CONTROL, test Model, Plan, Fast, Attach, Approve/Decline when a request is visible, and the handoff commands.
7. Open Review and verify native review-panel navigation. Do not expect per-diff Accept/Reject buttons from pure VIA.

## Recovery and troubleshooting

- If VIA reports a device mismatch, confirm the connected device is `0xD010:0x1601`.
- If VIA reports an incorrect macro count, restore your backup and enter the eight macro strings manually in VIA's Macros pane.
- If a custom action does nothing, confirm its exact command is still present in **Settings → Keyboard Shortcuts** and record the physical key again.
- If macOS intercepts a chord, use Keyboard Shortcuts' keystroke-search mode to locate the conflict.
- If a layer appears stuck, press Return CHAT or reconnect the pad.

## Sources

- [Official ChatGPT desktop command reference](https://learn.chatgpt.com/docs/reference/commands)
- [Official ChatGPT Voice guide](https://learn.chatgpt.com/docs/features/voice)
- [KeebMonkey KB16 product details](https://www.keebmonkey.com/en-gb/products/megalodon-triple-knob-macro-pad)
- [VIA application](https://usevia.app/)
- [QMK layer behavior](https://docs.qmk.fm/feature_layers)

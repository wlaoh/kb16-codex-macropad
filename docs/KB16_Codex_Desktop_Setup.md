# KB16 Codex Desktop setup

This layout maps the wired DOIO/KeebMonkey Megalodon KB16-01 to Codex controls in the ChatGPT desktop app for macOS. It uses VIA only: no firmware flashing, `config.toml` changes, Hammerspoon rules, Shortcuts automations, or background services.

## Compatibility

| Item | Value |
|---|---|
| USB vendor ID | `0xD010` |
| USB product ID | `0x1601` |
| VIA device ID | `3490715137` |
| Matrix | 4 rows x 5 columns |
| Physical controls | 16 keys and three clickable encoders |
| Layers | Four |
| Verified ChatGPT build | `26.803.61601` |
| Verification date | 2026-08-13 |

This layout does not support the older `0xFEED:0x6060` definition or the wireless KB16.

## Install

1. Open [VIA](https://usevia.app/) in a Chromium-based browser.
2. Connect the wired KB16-01 and authorize it. Confirm that VIA identifies it as **KB16-01**.
3. Open **Configure > Save + Load** and save a backup of the current layout.
4. Choose **Load Saved Layout** and select `KB16-01_Codex_Desktop_v1.layout.json`.
5. Wait for **Successfully updated layout** before unplugging the pad.

The KB16 stores the layout on the device. Keep the backup and a copy of the imported JSON.

## Controls and layers

The 4x4 key grid is on the left. The two small encoders are at the upper right, the OLED is below them, and the large dial is at the lower right.

The OLED is one-based; VIA layers are zero-based:

| OLED | VIA layer | Mode | Behavior |
|---|---:|---|---|
| `1` | 0 | CHAT | Default layer |
| `2` | 1 | CONTROL | Persistent until another mode is selected |
| `3` | 2 | REVIEW | Persistent until another mode is selected |
| `4` | 3 | WORK | Active only while WORK is held |

WORK is the highest layer, which lets its momentary mappings work from every persistent mode. Reconnecting the pad returns it to CHAT.

## Configure ChatGPT shortcuts

Most keys use built-in app shortcuts. Global Voice, Model Picker, and the `F14`-`F22` signals require one-time bindings.

### Voice

- **Toggle Voice** sends `Control-Shift-V` while ChatGPT is focused. This shortcut was verified in the app build listed above.
- **Global Voice** sends `Command-Option-F13`. In **Settings > Voice > Voice chat hotkey**, activate the shortcut field and press the physical **Global Voice** key.
- **Dictation** sends `Control-Shift-D` and inserts speech as composer text.

A voice chat must start in a new, empty chat or task. Press the large dial to Search chats; voice and chat search are separate actions.

### Custom command signals

Open **Settings > Keyboard Shortcuts**. Search for each command name, activate its shortcut field, and use the listed physical control.

| Physical control | Signal | Command name |
|---|---|---|
| Upper-left knob counterclockwise | `⌃⌥⌘[` | Decrease reasoning effort |
| Upper-left knob clockwise | `⌃⌥⌘]` | Increase reasoning effort |
| Upper-left knob press or Model Picker key | `⌃⌥⌘M` | Open model picker |
| CONTROL row 1, column 4 | `F14` | Toggle plan mode |
| CONTROL row 2, column 1 | `F15` | Toggle Fast mode |
| CONTROL row 2, column 2 | `F16` | Attach files and folders |
| CONTROL row 2, column 3 | `F17` | Approve request |
| CONTROL row 2, column 4 | `F18` | Decline request |
| CONTROL row 3, column 2 | `F19` | Copy as Markdown |
| CONTROL row 3, column 4 | `F20` | Continue in new chat |
| CONTROL row 3, column 3 | `F21` | Open side chat |
| CONTROL row 3, column 1 | `F22` | Open project picker |

`Control-Option-Command-M` opens Model Picker; `Command-Option-F13` remains the Global Voice hotkey. Command availability can vary by app version and account rollout. Leave unavailable commands unbound.

## Knobs

The knobs behave the same on every mode:

| Physical control | Counterclockwise | Press | Clockwise |
|---|---|---|---|
| Upper-left small knob | Effort down | Model Picker | Effort up |
| Upper-right small knob | Page up | Command Menu | Page down |
| Large lower-right dial | Previous chat | Search chats | Next chat |

## OLED 1 - CHAT

| | Column 1 | Column 2 | Column 3 | Column 4 |
|---|---|---|---|---|
| Row 1 | New chat | Toggle Voice | Quick chat | Command Menu |
| Row 2 | Dictation | Global Voice | Send | Escape / interrupt |
| Row 3 | Sidebar | Open folder | Open Review | Terminal |
| Row 4 | Hold WORK | Enter CONTROL | Enter REVIEW | Model Picker |

## OLED 2 - CONTROL

| | Column 1 | Column 2 | Column 3 | Column 4 |
|---|---|---|---|---|
| Row 1 | Effort down | Effort up | Model Picker | Plan mode |
| Row 2 | Fast mode | Attach files | Approve request | Decline request |
| Row 3 | Project Picker | Copy as Markdown | Open side chat | Continue in new chat |
| Row 4 | Hold WORK | Return CHAT | Enter REVIEW | Escape / interrupt |

Approve and Decline act on an active permission request. They do not accept or reject individual review diffs.

## OLED 3 - REVIEW

| | Column 1 | Column 2 | Column 3 | Column 4 |
|---|---|---|---|---|
| Row 1 | Open Review | Toggle Review panel | Approve request | Decline request |
| Row 2 | Previous chat | Next chat | Copy as Markdown | Continue in new chat |
| Row 3 | Copy | Find in chat | Terminal | Command Menu |
| Row 4 | Hold WORK | Return CHAT | Enter CONTROL | Escape / interrupt |

VIA cannot press the review UI's per-diff Accept or Reject buttons unless ChatGPT exposes matching keyboard commands.

## OLED 4 - WORK, momentary

Hold the bottom-left WORK key from CHAT, CONTROL, or REVIEW. Release it to return to the previous mode. The prompt macros insert text but do not submit it.

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

The full 16-slot macro block, including each slot terminator, remains below the conservative 480-byte limit.

## Verify the layout

1. Reconnect the pad and confirm that the OLED shows `1`.
2. Enter CONTROL and REVIEW; confirm that the OLED shows `2` and `3`.
3. Hold WORK from all three modes. Confirm that the OLED shows `4` only while held and that a macro inserts text without submitting.
4. Turn and press all three knobs in CHAT.
5. Start a new empty task and test Dictation, Toggle Voice, and Global Voice separately. Also test Global Voice while another app is focused.
6. In CONTROL, test Model Picker, Plan, Fast, Attach, Approve or Decline during a visible request, and the handoff commands.
7. Open Review and test its built-in navigation. Per-diff Accept and Reject are not available through this VIA layout.

## Troubleshooting

- **Device mismatch:** confirm that the connected device is `0xD010:0x1601`.
- **Incorrect macro count:** restore the backup, then enter the eight macro strings manually in VIA's Macros pane.
- **Custom action does nothing:** confirm that the command still appears in **Settings > Keyboard Shortcuts**, then record the physical signal again.
- **macOS intercepts a chord:** use the Keyboard Shortcuts keystroke-search mode to find the conflict.
- **Layer appears stuck:** press Return CHAT or reconnect the pad.

## Sources

- [ChatGPT desktop command reference](https://learn.chatgpt.com/docs/reference/commands)
- [ChatGPT Voice](https://learn.chatgpt.com/docs/features/voice)
- [KeebMonkey KB16 product details](https://www.keebmonkey.com/en-gb/products/megalodon-triple-knob-macro-pad)
- [VIA](https://usevia.app/)
- [QMK layer behavior](https://docs.qmk.fm/feature_layers)

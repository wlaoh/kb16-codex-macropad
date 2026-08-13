# KB16 Codex Desktop Controller — Pure VIA v1

This configuration is for the connected, automatically recognized **KB16-01** revision:

- USB vendor ID: `0xD010`
- USB product ID: `0x1601`
- VIA device ID: `3490715137`
- Matrix: 4 rows × 5 columns
- Controls: 16 keys, three clickable encoders, four layers

No Codex `config.toml` changes and no firmware flashing are required.

## Install the layout

1. Open [VIA](https://usevia.app/) in a Chromium-based browser.
2. Connect and authorize the KB16. Confirm VIA identifies it as **KB16-01**.
3. Open **Configure → Save + Load**.
4. Save the current layout first as a backup.
5. Select **Load Saved Layout** and choose `KB16-01_Codex_Desktop_v1.layout.json`.
6. Wait for **Successfully updated layout** before unplugging the pad.

The layout is stored on the KB16. Keep the JSON file as a recoverable backup.

## Required Codex shortcut setup

Most actions use Codex's native default shortcuts and work immediately. Two voice/agent groups use otherwise-unused function keys so they do not collide with macOS.

### Live Voice — required

In the ChatGPT desktop app, open **Settings → Voice → Voice chat hotkey** and press the KB16's **LIVE VOICE** key. It emits `Command-Option-F13`, satisfying Codex's requirement that the shortcut include Command, Control, or Option/Alt.

Voice chat must start from a new, empty task. Composer dictation is separate and works immediately through Codex's native `Control-Shift-D` shortcut.

### Agent controls — bind when available

Open **Settings → Keyboard Shortcuts**, search for the Codex command, click its shortcut field, and perform the corresponding physical action on the KB16:

| Physical action on the KB16 | Signal | Intended Codex command |
|---|---|---|
| Turn the **large/right knob counterclockwise** | `⌃⌥⌘[` | Decrease reasoning depth |
| Turn the **large/right knob clockwise** | `⌃⌥⌘]` | Increase reasoning depth |
| **Press the large/right knob** | `⌃⌥⌘M` | Open agent/model controls |
| AGENT layer: press row 3, column 3 | `F17` | Model selector |
| AGENT layer: press row 3, column 4 | `F18` | Mode selector |
| REVIEW layer: press row 1, column 3 | `F19` | Accept selected change |
| REVIEW layer: press row 1, column 4 | `F20` | Reject selected change |
| REVIEW layer: press row 2, column 1 | `F21` | Previous review change |
| REVIEW layer: press row 2, column 2 | `F22` | Next review change |
| REVIEW layer: press row 2, column 3 | `F23` | Accept all changes |
| REVIEW layer: press row 2, column 4 | `F24` | Reject all changes |

If a command is absent, leave that action unbound. The large knob uses uncommon three-modifier chords so macOS does not interpret its turns as brightness controls.

`F17` through `F24` are optional **button** signals on the AGENT and REVIEW layers—not knob directions. You do not need to configure them for the large effort knob.

## Physical map

The two small encoders are above the 4×4 key grid; the large encoder is on the right.

### Knobs — every layer

| Control | Counterclockwise | Press | Clockwise |
|---|---|---|---|
| Left/top encoder | Previous task | Search tasks | Next task |
| Center/top encoder | Page up | Command menu | Page down |
| Large/right encoder | Reasoning depth down (`⌃⌥⌘[`) | Agent/model controls (`⌃⌥⌘M`) | Reasoning depth up (`⌃⌥⌘]`) |

### Layer 0 — CHAT (default)

| | Column 1 | Column 2 | Column 3 | Column 4 |
|---|---|---|---|---|
| Row 1 | New task | Search tasks | Quick chat | Command menu |
| Row 2 | Dictation | Live Voice | Send | Interrupt/Escape |
| Row 3 | Sidebar | Open folder | Open Review | Terminal |
| Row 4 | Hold WORK | Enter AGENT | Settings | Keyboard shortcuts |

Hold **WORK** while pressing a workflow key. Release it to return to CHAT.

### Layer 1 — WORK (momentary)

Every prompt is inserted into the composer without sending it.

| | Column 1 | Column 2 | Column 3 | Column 4 |
|---|---|---|---|---|
| Row 1 | Summarize progress | Update docs | Implement change | Explain code/problem |
| Row 2 | Plan first | Explain like I'm five | Undo | Redo |
| Row 3 | Copy | Paste | Cut | Select all |
| Row 4 | Hold/release | Enter AGENT | Enter REVIEW | Return CHAT |

### Layer 2 — AGENT (persistent)

| | Column 1 | Column 2 | Column 3 | Column 4 |
|---|---|---|---|---|
| Row 1 | Reasoning down | Reasoning up | Agent controls | Command menu |
| Row 2 | Dictation | Live Voice | Send | Interrupt/Escape |
| Row 3 | Settings | Keyboard shortcuts | Model (`F17`) | Mode (`F18`) |
| Row 4 | Hold WORK | Return CHAT | Enter REVIEW | Quick chat |

### Layer 3 — REVIEW (persistent)

| | Column 1 | Column 2 | Column 3 | Column 4 |
|---|---|---|---|---|
| Row 1 | Open Review | Toggle Review panel | Accept (`F19`) | Reject (`F20`) |
| Row 2 | Previous change (`F21`) | Next change (`F22`) | Accept all (`F23`) | Reject all (`F24`) |
| Row 3 | Copy | Find in task | Terminal | Command menu |
| Row 4 | Hold WORK | Return CHAT | Enter AGENT | Interrupt/Escape |

## Macro text

The six workflow macros deliberately omit `Return`, so they never submit themselves:

1. `Summarize the progress so far and the remaining work.`
2. `Write or update the documentation for the current change.`
3. `Implement the requested change. Verify it in proportion to risk.`
4. `Explain the current code or problem clearly, including the important tradeoffs.`
5. `Before making changes, propose a concise implementation plan.`
6. `Explain this to me like I am five, without losing the important truth.`

## Recovery and compatibility

- This file targets **KB16-01 / `0xD010:0x1601`**, not the older `0xFEED:0x6060` definition and not the wireless KB16.
- VIA validates the connected device ID and layer length before writing. A device-mismatch error means the wrong revision is connected.
- The file assumes the standard VIA count of 16 macros reported by this firmware family. If VIA reports **incorrect number of macros**, restore the backup and configure the six macro strings manually in VIA's Macros pane; the key and encoder design remains valid.
- If a macOS shortcut is intercepted elsewhere, open **Settings → Keyboard Shortcuts**, switch the search field to keystroke mode, and check for conflicts.

## Sources

- [Official Codex/ChatGPT desktop keyboard shortcuts](https://learn.chatgpt.com/docs/reference/commands)
- [Official ChatGPT Voice setup](https://learn.chatgpt.com/docs/features/voice)
- [KeebMonkey KB16 product details](https://www.keebmonkey.com/en-gb/products/megalodon-triple-knob-macro-pad)
- [VIA application](https://usevia.app/)
- [VIA keyboard-definition specification](https://caniusevia.com/docs/specification/)

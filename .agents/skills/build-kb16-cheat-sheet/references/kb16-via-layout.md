# KB16-01 VIA layout reference

Use this reference to translate the VIA export into the visible hardware without
guessing. Verify project-specific names and behavior against the current files.

## Source priority

1. The layout JSON determines emitted keycodes and macro text.
2. The shortcut manifest assigns app meanings to custom signals and records the
   OLED/VIA relationship.
3. The setup guide supplies user-facing wording and limitations.
4. Existing visual artifacts supply styling only.

Record conflicts before resolving them. Prefer the higher-priority source for the
cheat sheet and do not silently modify the device layout.

## Matrix topology

The firmware exports each layer as a 4x5, row-major matrix. Sixteen positions are
the visible key grid, three positions are encoder presses, and one is unused.

| Matrix row | Grid columns 1-4 | Fifth position |
|---|---|---|
| 1 | indexes `0, 1, 2, 3` | index `4`: upper-left small knob press |
| 2 | indexes `5, 6, 7, 8` | index `9`: upper-right small knob press |
| 3 | indexes `10, 11, 12, 13` | index `14`: large lower-right dial press |
| 4 | indexes `15, 16, 17, 18` | index `19`: unused |

The physical chassis has the 4x4 keys on the left, two small clickable knobs at
the upper right, the OLED below them, and the large clickable dial at lower right.

## Encoder array

`encoders` is ordered by physical encoder, then VIA layer, then direction:

```text
encoders[encoder_index][via_layer][0] = counterclockwise
encoders[encoder_index][via_layer][1] = clockwise
```

Encoder indexes are upper-left small knob `0`, upper-right small knob `1`, and
large lower-right dial `2`. Press actions do not live in `encoders`; use matrix
indexes `4`, `9`, and `14`.

## Layer and macro semantics

- `TO(n)` persistently switches to VIA layer `n`.
- `MO(n)` activates layer `n` only while held.
- QMK resolves the highest active layer first. Flag a momentary target that is not
  higher than its source layer because it may be masked.
- `KC_TRNS` falls through to the next active lower layer.
- `KC_NO` is intentionally inactive.
- `MACRO(n)` inserts macro slot `n`; read its exact text from `macros[n]`.
- Empty macro slots are not actions. Macro strings containing Return/newline may
  submit text and require explicit warning.

## OLED numbering

The OLED often displays one-based values while VIA layers are zero-based, but this
is project metadata rather than a universal VIA rule. Require the manifest's
`layerDisplay` entries to establish each OLED value, VIA layer, mode name, and
behavior. If they are absent or conflicting, report the mapping as unverified.

## Keycode wording

Decode standard modifier wrappers only to verify prose already supported by the
setup guide or manifest:

- `LGUI`: Command on macOS
- `LALT`: Option on macOS
- `LCTL`: Control
- `LSFT`: Shift
- `KC_ENT`: Return/Enter
- `KC_ESC`: Escape
- `KC_F13` through `KC_F24`: raw function-key signals until bound in the app

Custom function keys do not reveal their intended ChatGPT commands. Obtain those
meanings from `customSignals` or the current setup guide.

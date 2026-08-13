# KB16-01 VIA layout reference

Use this reference to map a VIA export to the physical KB16-01. Verify project-specific labels against the layout, manifest, and setup guide.

## Matrix

Each layer is a row-major 4x5 matrix: 16 visible keys, three encoder presses, and one unused position.

| Matrix row | Grid columns 1-4 | Fifth position |
|---|---|---|
| 1 | indexes `0, 1, 2, 3` | index `4`: upper-left knob press |
| 2 | indexes `5, 6, 7, 8` | index `9`: upper-right knob press |
| 3 | indexes `10, 11, 12, 13` | index `14`: large-dial press |
| 4 | indexes `15, 16, 17, 18` | index `19`: unused |

The 4x4 key grid is on the left. The two small knobs are at the upper right, the OLED sits below them, and the large dial is at the lower right.

## Encoders

The `encoders` array is ordered by physical encoder, VIA layer, and direction:

```text
encoders[encoder_index][via_layer][0] = counterclockwise
encoders[encoder_index][via_layer][1] = clockwise
```

Encoder `0` is the upper-left knob, `1` is the upper-right knob, and `2` is the large dial. Presses are matrix indexes `4`, `9`, and `14`; they are not stored in `encoders`.

## Layer and macro codes

- `TO(n)` switches persistently to layer `n`.
- `MO(n)` activates layer `n` while held.
- QMK resolves the highest active layer first. A momentary target at or below its source layer may be masked.
- `KC_TRNS` falls through to the next active lower layer.
- `KC_NO` is inactive.
- `MACRO(n)` inserts `macros[n]`.
- An empty macro slot is not an action. Return or newline characters may submit composer text and require a warning.

## OLED numbering

OLED values are project metadata, not a VIA convention. Use the manifest's `layerDisplay` entries to verify the OLED value, VIA layer, mode name, and behavior. Report missing or conflicting mappings as unverified.

## Keycode names

Use modifier wrappers only to confirm labels already supported by the manifest or setup guide:

- `LGUI`: Command on macOS
- `LALT`: Option on macOS
- `LCTL`: Control
- `LSFT`: Shift
- `KC_ENT`: Return or Enter
- `KC_ESC`: Escape
- `KC_F13` through `KC_F24`: unassigned function-key signals until bound in the app

Function keys do not identify their ChatGPT commands. Read those names from `customSignals` or the setup guide.

# Changelog

## 2026-08-13

- Created the initial pure-VIA Codex macropad layout.
- Reordered modes to CHAT, CONTROL, REVIEW, and highest-priority momentary WORK.
- Fixed WORK access from persistent layers by changing every WORK hold to `MO(3)`.
- Replaced speculative per-diff review signals with commands exposed by the current ChatGPT desktop app.
- Renamed reasoning controls from depth to effort and mapped the large-dial press to Open model picker.
- Expanded the WORK layer to eight safe, non-submitting workflow prompts.
- Added a focused-app voice toggle while retaining the global voice hotkey, using the key slot previously duplicated by the Search encoder press.
- Added the one-based OLED to zero-based VIA layer legend.
- Corrected the physical knob descriptions to match the KB16 chassis.
- Added a printable visual cheat sheet, machine-readable shortcut manifest, validation script, and CI check.

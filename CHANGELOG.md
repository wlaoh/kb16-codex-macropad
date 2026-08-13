# Changelog

## Unreleased

- Reorganized the canonical layout and manifest under `config/`, the setup guide under `docs/`, and generated assets under `docs/cheat-sheet/`.
- Updated repository links, validators, builders, and skills for the new paths.
- Tightened the documentation, removed repeated guidance, and clarified which shortcuts are built in or user-bound.

## 2026-08-13

- Added the initial pure-VIA layout, setup guide, shortcut manifest, validator, CI check, and printable cheat sheet.
- Set the OLED modes to CHAT, CONTROL, REVIEW, and momentary WORK; mapped OLED `1`-`4` to VIA layers `0`-`3`.
- Made WORK accessible from every persistent layer with `MO(3)` and expanded it to eight non-submitting prompt macros.
- Replaced speculative review bindings with commands available in the verified ChatGPT desktop build. Approve and Decline now apply only to permission requests.
- Mapped the upper-left knob to reasoning effort and Model Picker, the upper-right knob to page navigation and Command Menu, and the large dial to chat navigation and Search Chats.
- Assigned `Control-Option-Command-M` to Model Picker and kept `Command-Option-F13` for Global Voice. Added a focused-app Toggle Voice key.

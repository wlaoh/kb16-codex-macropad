---
name: personalize-kb16-work-prompts
description: Personalize the eight WORK-layer macros in a KB16-01 Codex Desktop VIA layout, create a reusable prompt profile and prompt map, and verify that no hardware mapping changed. Use for KB16 WORK prompts, prompt buttons, macro text, and role-specific prompt packs. Do not use for other keyboards, firmware, key remapping, or shortcut changes.
---

# Personalize KB16 WORK prompts

Change only macro slots 0-7. Preserve the validated keymap, layers, encoders, shortcuts, and firmware limits.

## Workflow

1. Use `config/KB16-01_Codex_Desktop_v1.layout.json` unless the user names another KB16-01 layout.
2. Read [references/prompt-profile.md](references/prompt-profile.md).
3. Infer the repeated workflows from the request. Ask one short question only if the role or desired actions remain unclear.
4. Write exactly eight labels and eight complete prompts. Put frequent actions in the first row and state whether each prompt permits editing.
5. Save the profile as `profiles/<profile-name>.work-prompts.json` unless the user provides another path.
6. Validate the profile without writing a layout:

   ```sh
   python3 <skill-dir>/scripts/personalize_work_prompts.py \
     --layout <source.layout.json> \
     --profile <profile.work-prompts.json> \
     --dry-run
   ```

7. Write a separate layout and prompt map under `personalized/`:

   ```sh
   python3 <skill-dir>/scripts/personalize_work_prompts.py \
     --layout <source.layout.json> \
     --profile <profile.work-prompts.json> \
     --output <personalized.layout.json> \
     --prompt-map <personalized-prompts.md>
   ```

   Overwrite the canonical layout only when the user explicitly requests it.
8. Confirm that no field except `macros[0:8]` changed:

   ```sh
   python3 <skill-dir>/scripts/validate_personalized_layout.py \
     --layout <personalized.layout.json> \
     --base <source.layout.json> \
     --profile <profile.work-prompts.json>
   ```

9. If the personalized layout becomes the default, update the setup guide, any prompt metadata in the manifest, and cheat-sheet labels. Otherwise leave shared documentation unchanged.

## Constraints

- Preserve every layout field except `macros[0:8]`.
- Keep all 16 macro slots, including terminators, at or below 512 UTF-8 bytes; leave at least 32 bytes free when possible.
- Use printable ASCII with no tabs, newlines, carriage returns, or other control characters.
- Do not add Return or any auto-submit behavior.
- Keep labels at 18 characters or fewer.
- State no-edit boundaries in review, explanation, and diagnosis prompts.
- Write a new layout by default so the source remains recoverable.

## Handoff

Report the profile name, output paths, macro-byte usage, and validation result. Note that the user must still load the new layout into VIA and that macros insert text without submitting it.

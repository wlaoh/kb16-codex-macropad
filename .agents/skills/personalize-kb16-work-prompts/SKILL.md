---
name: personalize-kb16-work-prompts
description: Personalize the eight WORK-layer text macros in the KB16-01 Codex Desktop VIA .layout.json, generate a reusable prompt profile and prompt map, and verify that hardware mappings remain unchanged. Use when a user asks to change, rewrite, tailor, replace, or create KB16 WORK prompts, prompt buttons, macro text, or a role-specific prompt pack. Do not use for other keyboards, firmware flashing, arbitrary key remapping, or Codex shortcut changes.
---

# Personalize KB16 WORK Prompts

Tailor the eight prompt keys while preserving the validated KB16-01 keymap, layer behavior, encoders, shortcuts, and conservative firmware limits.

## Workflow

1. Locate the source layout. Prefer `outputs/KB16-01_Codex_Desktop_v1.layout.json` in this repository unless the user names another KB16-01 layout.
2. Read [references/prompt-profile.md](references/prompt-profile.md) before drafting a profile.
3. Infer the user's repeated workflows from the request. Ask one concise question only when the role or desired actions cannot be inferred safely.
4. Draft exactly eight short labels and eight complete prompt strings. Put the highest-frequency actions in the top row and make read-only versus editing behavior explicit.
5. Save the reusable profile as JSON. Default to `outputs/profiles/<profile-name>.work-prompts.json` in this repository.
6. Run a dry check before writing a layout:

   ```sh
   python3 <skill-dir>/scripts/personalize_work_prompts.py \
     --layout <source.layout.json> \
     --profile <profile.work-prompts.json> \
     --dry-run
   ```

7. Generate a separate personalized layout and Markdown prompt map. Do not overwrite the canonical layout unless the user explicitly asks to replace the default.

   ```sh
   python3 <skill-dir>/scripts/personalize_work_prompts.py \
     --layout <source.layout.json> \
     --profile <profile.work-prompts.json> \
     --output <personalized.layout.json> \
     --prompt-map <personalized-prompts.md>
   ```

8. Validate that only macro slots 0-7 changed:

   ```sh
   python3 <skill-dir>/scripts/validate_personalized_layout.py \
     --layout <personalized.layout.json> \
     --base <source.layout.json> \
     --profile <profile.work-prompts.json>
   ```

9. If the personalized layout becomes the repository default, update the setup guide, shortcut manifest if it gains prompt metadata, and cheat-sheet labels to match. Otherwise leave shared documentation unchanged and deliver the generated prompt map with the personalized layout.

## Safety Rules

- Preserve every layout field except `macros[0:8]`.
- Keep all sixteen VIA macro slots, including terminators, at or below 512 UTF-8 bytes. Aim to leave at least 32 bytes free for later wording changes.
- Use printable ASCII in macro text. Do not add newlines, carriage returns, tabs, or other control characters.
- Never append Return or otherwise make a prompt submit itself.
- Keep prompt labels at 18 characters or fewer.
- Make mutation boundaries explicit: prompts such as review or diagnosis should say when not to edit.
- Write a new output file by default and preserve the source as a recovery point.

## Handoff

Report the profile name, output paths, macro-byte usage, and validation result. Remind the user that the generated layout still needs to be loaded into VIA and that prompt macros insert text without submitting it.

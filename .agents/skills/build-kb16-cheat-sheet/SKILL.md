---
name: build-kb16-cheat-sheet
description: Create or refresh the printable KB16-01 Codex Desktop cheat sheet from the canonical VIA layout, shortcut manifest, setup guide, and existing visual assets. Use for the 4x4 key maps, three encoders, OLED-to-VIA layers, WORK macros, shortcut bindings, SVG source, PDF, PNG previews, source reconciliation, and render QA.
---

# Build a KB16 cheat sheet

Build from the current repository state. The layout JSON determines what the device sends; prose sources only assign names and instructions to those signals.

## Workflow

1. Read repository instructions and inspect `git status`. Preserve unrelated changes.
2. Select the layout named by the shortcut manifest. If `layoutFile` is absent, use the highest numeric version matching `config/KB16-01_Codex_Desktop_v*.layout.json`. Do not choose by modification time or treat a personalized layout as canonical unless the user names it.
3. Read [references/kb16-via-layout.md](references/kb16-via-layout.md), then inspect the selected sources:

   ```sh
   python3 .agents/skills/build-kb16-cheat-sheet/scripts/inspect_layout.py \
     --layout config/KB16-01_Codex_Desktop_v1.layout.json \
     --manifest config/KB16_Codex_Shortcut_Manifest.json \
     --format markdown --strict
   ```

   Adjust the paths for the selected version. Record any mismatch before editing and include its resolution in the handoff.
4. Reconcile sources in this order:

   - Layout JSON: keycodes, macro text, encoder rotation, and encoder presses.
   - Shortcut manifest: command names and OLED/VIA metadata.
   - Setup guide: labels, limitations, and binding steps.
   - Existing cheat sheets: appearance only.

   Do not alter the layout to resolve a documentation mismatch unless the user also requested a mapping change. Use the raw signal or mark it unassigned when no supported label exists. For claims about current ChatGPT commands, check official OpenAI documentation or the installed app; otherwise cite the repository's verified build and date.
5. Include all of the following:

   - The verified `OLED 1-4` to `VIA 0-3` mapping.
   - Four physical 4x4 key maps in row and column order.
   - Rotation and press actions for all three encoders.
   - WORK labels plus exact macro text or a clearly labeled faithful summary.
   - One-time bindings, material limitations, and held versus persistent layer behavior.
6. Use the existing yellow, black, and cyan visual system. Default to US Letter landscape. Keep text legible at 100% and preserve hierarchy in grayscale. Prefer the source-driven generator, require labels to match expected keycodes, and produce editable SVG plus PDF. Add 150 dpi PNG previews when practical.
7. Use the PDF skill for generation and QA. Render every page, inspect every render, and fix clipping, collisions, small text, or unclear hierarchy.
8. Run the final checks:

   - Re-run `inspect_layout.py --strict` and `scripts/validate_layout.py`.
   - Parse each SVG as XML and verify its dimensions, `viewBox`, and text content.
   - Check PDF page count, size, metadata, text bounds, and extracted labels with `pdfinfo`, `pdfplumber`, or `pypdf`.
   - Verify PNG dimensions and inspect the final render after the last build.
   - Run `git diff --check` and confirm every output is nonempty.
9. Update README or setup-guide links only for repository-owned outputs. Report the generated files, validations, and any source mismatch with its resolution.

## Guardrails

- Never infer a ChatGPT command from an `F13`-`F24` keycode.
- Keep encoder rotation separate from encoder-press matrix positions.
- Approve and Decline apply to permission requests unless current app sources explicitly document per-diff behavior.
- Verify OLED numbering from the manifest; do not assume it is one-based.
- Do not rewrite WORK macros as part of documentation work.
- Use existing cheat sheets as visual references, not mapping authorities.

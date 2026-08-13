---
name: build-kb16-cheat-sheet
description: Create or refresh polished printable cheat sheets for the DOIO/KeebMonkey KB16-01 Codex Desktop macropad from its VIA layout JSON, setup guide, shortcut manifest, and existing legend or visual artifacts. Use when Codex must document the KB16's 4x4 keys, three clickable encoders, OLED-to-VIA layer mapping, WORK macros, or custom ChatGPT shortcut bindings in editable SVG plus PDF or PNG delivery formats, with source reconciliation and render-based visual QA.
---

# Build a KB16 Cheat Sheet

Create the guide from the current repository snapshot. Treat the layout JSON as
the authority for what the device emits; use prose sources to name those signals.

## Workflow

1. Inspect repository instructions and `git status`. Preserve unrelated work.
2. Read `layoutFile` from the shortcut manifest and use that file when it exists.
   If the manifest omits it, select the highest numeric-version canonical
   `config/KB16-01_Codex_Desktop_v*.layout.json`. Pair it with the current setup
   guide, manifest, and matching visual artifacts. Do not select by modification
   time alone or treat a personalized layout as canonical unless the user names it.
3. Read [references/kb16-via-layout.md](references/kb16-via-layout.md), then run:

   ```sh
   python3 .agents/skills/build-kb16-cheat-sheet/scripts/inspect_layout.py \
     --layout config/KB16-01_Codex_Desktop_v1.layout.json \
     --manifest config/KB16_Codex_Shortcut_Manifest.json \
     --format markdown --strict
   ```

   Adjust paths for the selected version. Save or quote any inconsistencies in a
   work note before editing; report them to the user in the handoff.
4. Reconcile sources with this priority:

   - Layout JSON: keycodes, macro strings, encoder rotations, and encoder presses.
   - Shortcut manifest: intended app command and OLED/VIA metadata.
   - Setup guide: user-facing labels, limitations, and binding steps.
   - Existing legends: visual style and layout only.

   Do not change the device layout merely to make documentation agree unless the
   user also requests a layout fix. If a label cannot be supported, show the raw
   signal or mark it unassigned instead of inventing a shortcut.
   If the deliverable claims current ChatGPT command availability, refresh that
   claim from official OpenAI documentation or the installed app before authoring;
   otherwise retain and clearly label the repository's verified build and date.
5. Plan the information architecture before drawing. Include:

   - An explicit `OLED 1-4` to `VIA 0-3` legend verified from the manifest.
   - Four physical 4x4 key maps in row/column order.
   - Rotation and press behavior for all three physical encoders.
   - WORK prompt names and the exact macro text or a clearly marked faithful meaning.
   - Required one-time custom shortcut bindings and important limitations.
   - The relationship between held and persistent layers.
6. Match the yellow-and-black hardware with a restrained, high-contrast visual
   system. Default to US Letter landscape unless repository or user requirements
   say otherwise. Keep body text printable at 100%, use color as a supplement to
   labels, and retain strong contrast in grayscale.
7. Prefer a source-driven generator when the repository will maintain the guide.
   Pair every human label with an expected keycode or normalized layout entry and
   fail generation when the layout changes. Produce editable SVG source and a PDF;
   add 150 dpi PNG previews when practical.
8. Use the PDF skill for PDF creation and QA when available. Render every final PDF
   page to PNG, visually inspect every render, and iterate until no clipping,
   collisions, tiny text, or ambiguous hierarchy remains.
9. Run final checks:

   - Re-run `inspect_layout.py --strict` and the repository's layout validator.
   - Parse SVG as XML; verify page dimensions/viewBox and nonempty text elements.
   - Check PDF page count, page size, metadata, text bounds, and extracted labels
     with `pdfinfo`, `pdfplumber`, or `pypdf`.
   - Confirm PNG dimensions and inspect the final render after the last rebuild.
   - Run `git diff --check` and verify every final path is nonempty.
10. Update README or setup-guide links only when the generated artifacts belong in
    the repository. In the final response, list outputs, validations, and each
    source inconsistency plus its resolution.

## Accuracy guardrails

- Never infer a ChatGPT command solely from an `F13`-`F24` keycode.
- Keep encoder rotation separate from the encoder-press matrix slots.
- Do not describe permission Approve/Decline as per-diff review actions unless the
  current app sources explicitly say so.
- Do not assume OLED numbering is one-based; verify it against the manifest.
- Do not rewrite or expand WORK macro strings in the layout as part of documentation.
- Treat an existing cheat sheet as a style reference, never as mapping authority.

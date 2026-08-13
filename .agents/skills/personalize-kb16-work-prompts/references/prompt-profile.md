# KB16 WORK prompt profiles

Use a JSON profile to keep prompt intent separate from the VIA layout export. The updater maps macro slots to the first two rows of OLED 4 / VIA layer 3.

| Slot | Physical key |
|---:|---|
| 0 | WORK row 1, column 1 |
| 1 | WORK row 1, column 2 |
| 2 | WORK row 1, column 3 |
| 3 | WORK row 1, column 4 |
| 4 | WORK row 2, column 1 |
| 5 | WORK row 2, column 2 |
| 6 | WORK row 2, column 3 |
| 7 | WORK row 2, column 4 |

## Profile schema

```json
{
  "name": "python-maintainer",
  "description": "Frequent maintenance and debugging workflows",
  "prompts": [
    {
      "slot": 0,
      "label": "SUMMARIZE",
      "text": "Summarize completed work, blockers, and next steps."
    },
    {
      "slot": 1,
      "label": "IMPLEMENT",
      "text": "Implement the requested change. Preserve unrelated work and verify it."
    },
    {
      "slot": 2,
      "label": "REVIEW ONLY",
      "text": "Review the current changes for bugs, risks, and missing tests. Do not edit."
    },
    {
      "slot": 3,
      "label": "EXPLAIN",
      "text": "Explain the current code or problem and its key tradeoffs."
    },
    {
      "slot": 4,
      "label": "DIAGNOSE ONLY",
      "text": "Diagnose the root cause. Do not edit; report evidence and the recommended fix."
    },
    {
      "slot": 5,
      "label": "VERIFY",
      "text": "Run relevant tests. Investigate failures and summarize results."
    },
    {
      "slot": 6,
      "label": "UPDATE DOCS",
      "text": "Update documentation for the current change."
    },
    {
      "slot": 7,
      "label": "PLAN FIRST",
      "text": "Before editing, propose a concise implementation plan."
    }
  ]
}
```

`name` must be a lowercase hyphenated slug. `description` is optional. `prompts` must contain each slot from 0 through 7 exactly once. Labels must be printable ASCII and no longer than 18 characters. Prompt text must be nonempty printable ASCII with no control characters.

## Prompt design

- Write complete instructions that work against the current conversation and repository context without placeholders.
- Prefer eight distinct operations over small wording variants.
- Put frequent, general operations in slots 0-3 and specialized or safety-oriented operations in slots 4-7.
- State whether Codex may edit. Use language such as `Do not edit` for review, explanation, or diagnosis-only prompts.
- Include verification expectations in editing prompts when space permits.
- Keep wording compact. The complete sixteen-slot macro block must fit within 512 bytes; aim for 480 bytes or fewer so later wording changes have headroom.
- Avoid sensitive data, repository-specific secrets, shell commands, and temporary paths in reusable prompt profiles.

## Output naming

Use a recoverable source and a recognizable personalized output, for example:

```text
outputs/KB16-01_Codex_Desktop_v1.layout.json
outputs/profiles/python-maintainer.work-prompts.json
outputs/KB16-01_Codex_Desktop_v1.python-maintainer.layout.json
outputs/KB16-01_Codex_Desktop_v1.python-maintainer.prompts.md
```

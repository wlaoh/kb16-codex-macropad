# KB16 WORK prompt profiles

A profile keeps prompt intent separate from the VIA export. Slots 0-7 map to the first two rows of OLED 4 / VIA layer 3.

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

## Schema

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

`name` is a lowercase hyphenated slug. `description` is optional. `prompts` must contain every slot from 0 through 7 exactly once. Labels are printable ASCII with a maximum of 18 characters; prompt text is nonempty printable ASCII with no control characters.

## Writing rules

- Write standalone instructions with no placeholders.
- Use eight distinct operations; place the most frequent in slots 0-3.
- Say whether Codex may edit. Use `Do not edit` for read-only prompts.
- Include verification in editing prompts when space allows.
- Keep all 16 macro slots within 512 bytes and target 480 bytes or fewer.
- Do not include secrets, shell commands, or temporary paths.

## Paths

```text
config/KB16-01_Codex_Desktop_v1.layout.json
profiles/python-maintainer.work-prompts.json
personalized/KB16-01_Codex_Desktop_v1.python-maintainer.layout.json
personalized/KB16-01_Codex_Desktop_v1.python-maintainer.prompts.md
```

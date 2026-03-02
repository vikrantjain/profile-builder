---
name: linkedin-generate
description: >
  This skill should be used when the user asks to "generate LinkedIn content",
  "export profile for LinkedIn", "create LinkedIn-ready content",
  "format my experience for LinkedIn", "write my LinkedIn headline",
  "generate LinkedIn about section", "prepare LinkedIn update",
  or wants copy-paste-ready content formatted for LinkedIn's field constraints.
---

# LinkedIn Generate

Generate copy-paste-ready content for LinkedIn profile sections, formatted
to LinkedIn's character limits and plain-text constraints.

## When to Use

Invoke this skill to produce LinkedIn-formatted content from the master
profile. This can be a full LinkedIn profile export or a single section
(e.g., just the headline, just one experience entry). For reviewing an
existing LinkedIn profile against the master data, use the `linkedin-review`
skill instead.

## Workflow

### 1. Determine Scope

Ask or infer what the user needs:

- **Full export**: generate all LinkedIn sections
- **Single section**: e.g., "format my experience at Company X for LinkedIn"
- **Specific field**: e.g., "write me a LinkedIn headline"

### 2. Read Profile Sections

Read the relevant profile section JSON files from `sections/`. Consult
`profile-index.json` to discover available sections and their file paths.
Parse each JSON file and access fields directly from the `data` object.
For example: `data.full_name` from `sections/identity.json`,
`data.experience` array from `sections/experience.json`.

If required section JSON files do not exist, inform the user and suggest
running `/profile-init` or `profile-section` to generate them.

**TBD filtering applies during transformation (step 5), not here.**

### 3. Apply Presentation Preferences

Read `preferences.md` from the workspace root. If it exists:

1. Read the `## Global` section — these apply to all exports.
2. Read the `## LinkedIn` section (if present) — these are LinkedIn-specific.
3. Treat each preference as a binding directive during content transformation.
   Examples: "present experience as 20+ years" → use that framing; "don't
   highlight patents" → de-emphasize or omit; tone directives → adjust writing
   style accordingly.
4. LinkedIn-specific preferences take precedence over global if they conflict.

If `preferences.md` does not exist, proceed with default behavior.

### 4. Apply LinkedIn Constraints

Consult `${CLAUDE_PLUGIN_ROOT}/skills/linkedin-generate/references/linkedin-constraints.md` for:

- Character limits per field
- Formatting rules (plain text, no Markdown, bullet character `•`)
- Section mapping (which profile fields map to which LinkedIn fields)
- Best practices for content optimization

### 5. Transform Content

**TBD filtering:** Profile data may contain `TBD` as a placeholder value in
any field (indicating data not yet filled in by the user). When rendering
output, silently skip any value that is exactly `TBD` — do not render it.
If all items in a list are `TBD`, omit that list/block entirely.

For each target LinkedIn field:

- Convert Markdown formatting to plain text (remove `**`, `#`, `-` bullets).
- Replace Markdown bullet points with `•` characters.
- Trim or rewrite content to fit within character limits.
- Adapt tone: LinkedIn About section should be first-person, conversational.
- Include character count after each field so the user knows remaining budget.
- **Flatten project data into experience descriptions**: LinkedIn has no nested
  project structure. For experience entries with `projects[]`, incorporate each
  project's `contributions` and `impact` bullets into the job description text.
  Lead with impact items (quantifiable outcomes) as they are highest value for
  LinkedIn. Combine contribution + impact into concise bullets where possible
  (e.g., "Built X, resulting in Y% improvement").

### 6. Verify Preferences Compliance

Before writing output, re-read the applicable preferences and verify each one
is reflected in the generated content. If any preference was missed or
contradicted, revise the content before proceeding.

### 7. Write Output

Write the formatted content to `linkedin/`. Create the directory if
it does not exist.

For a full export, generate these files:

- `linkedin/headline.md` — Headline (220 chars max)
- `linkedin/about.md` — About/Summary section
- `linkedin/experience.md` — All experience entries
- `linkedin/skills.md` — Flattened skills list
- `linkedin/education.md` — Education entries
- `linkedin/certifications.md` — Certifications (if data exists)
- `linkedin/open-source.md` — Open source projects (if data exists)
- `linkedin/patents.md` — Patents (if data exists)
- `linkedin/languages.md` — Languages (if data exists)

For a single section or field, write only the relevant file.

Each file should include a header comment with the character limit and
current character count:

```
<!-- LinkedIn Headline | Limit: 220 chars | Used: 187 chars -->
```

### 8. Present to User

After writing files, display the generated content directly in the
conversation so the user can review and copy-paste immediately without
opening files.

## Output Checklist

Before finishing, verify:

- [ ] No Markdown formatting remains (no `**`, `##`, `- ` bullets)
- [ ] All fields are within LinkedIn's character limits
- [ ] Character counts are noted for each field
- [ ] Content written to `linkedin/`
- [ ] Content displayed in conversation for easy copy-paste
- [ ] Output honors all applicable presentation preferences (global + LinkedIn-specific)

## Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/skills/linkedin-generate/references/linkedin-constraints.md`** — Character limits, formatting rules, section mapping, and best practices

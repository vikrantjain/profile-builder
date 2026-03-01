---
name: hashnode-generate
description: >
  This skill should be used when the user asks to "generate Hashnode profile content",
  "export profile for Hashnode", "create Hashnode bio", "format my tagline for Hashnode",
  "update my Hashnode about page", "prepare Hashnode profile update",
  or wants copy-paste-ready content for their Hashnode profile fields
  (not blog articles).
---

# Hashnode Generate

Generate copy-paste-ready content for Hashnode profile fields, formatted
for Hashnode's profile settings. This skill covers profile metadata only
(bio, tagline, about page, tech stack, social links) — not blog articles.

## When to Use

Invoke this skill to produce Hashnode-formatted profile content from the
master profile. This can be a full profile export or a single field
(e.g., just the tagline, just the about page). For reviewing an existing
Hashnode profile against the master data, use the `hashnode-review` skill
instead.

## Workflow

### 1. Determine Scope

Ask or infer what the user needs:

- **Full export**: generate all Hashnode profile fields
- **Single field**: e.g., "write my Hashnode tagline" or "update my Hashnode about page"

### 2. Read Profile Sections

Read the relevant profile section files from `sections/`. Consult
`profile-index.md` to discover available sections. If section files do not
exist, read `profile.md` instead. Key sections:

- `sections/identity.md` — name, links, social profiles
- `sections/summary.md` — professional bio (adapt for Hashnode tone)
- `sections/skills.md` — tech stack for Hashnode tags

### 3. Apply Presentation Preferences

Read `preferences.md` from the workspace root. If it exists:

1. Read the `## Global` section — these apply to all exports.
2. Read the `## Hashnode` section (if present) — these are Hashnode-specific.
3. Treat each preference as a binding directive during content transformation.
   Examples: "present experience as 20+ years" → use that framing; "don't
   highlight patents" → de-emphasize or omit; tone directives → adjust writing
   style accordingly.
4. Hashnode-specific preferences take precedence over global if they conflict.

If `preferences.md` does not exist, proceed with default behavior.

### 4. Apply Hashnode Constraints

Consult `${CLAUDE_PLUGIN_ROOT}/skills/hashnode-generate/references/hashnode-constraints.md` for:

- Character limits per field
- Markdown support (Hashnode supports full Markdown in the about page)
- Field mapping from master profile to Hashnode profile fields
- Best practices for Hashnode profiles

### 5. Transform Content

**TBD filtering:** Profile data may contain `TBD` as a placeholder value in
any field (indicating data not yet filled in by the user). When rendering
output, silently skip any value that is exactly `TBD` — do not render it.
If all items in a list are `TBD`, omit that list/block entirely.

For each target Hashnode field:

- **Name**: use as-is from the master profile.
- **Tagline**: concise one-liner (max 150 chars). Adapt from the
  professional title or first line of summary.
- **Bio**: short paragraph (max 200 chars). Condense the professional
  summary into a brief overview.
- **About page**: full Markdown page. Expand the professional summary
  with skills, notable achievements, and links. Hashnode renders full
  Markdown here, so use headings, lists, bold, and links freely.
- **Tech stack**: map skills from the profile to Hashnode's tag format.
- **Social links**: extract GitHub, LinkedIn, Twitter/X, website URLs
  from identity data.

Include character count after each field so the user knows remaining budget.

### 6. Verify Preferences Compliance

Before writing output, re-read the applicable preferences and verify each one
is reflected in the generated content. If any preference was missed or
contradicted, revise the content before proceeding.

### 7. Write Output

Write the formatted content to `hashnode/`. Create the directory if
it does not exist.

For a full export, generate these files:

- `hashnode/tagline.md` — Tagline (150 chars max)
- `hashnode/bio.md` — Short bio (200 chars max)
- `hashnode/about.md` — Full about page (Markdown)
- `hashnode/tech-stack.md` — Tech stack tags
- `hashnode/social-links.md` — Social link URLs

For a single field, write only the relevant file.

Each file should include a header comment with the character limit (where
applicable) and current character count:

```
<!-- Hashnode Tagline | Limit: 150 chars | Used: 127 chars -->
```

### 8. Present to User

After writing files, display the generated content directly in the
conversation so the user can review and copy-paste immediately without
opening files.

## Output Checklist

Before finishing, verify:

- [ ] All fields are within Hashnode's character limits
- [ ] Character counts are noted for constrained fields
- [ ] About page uses proper Markdown formatting
- [ ] Content written to `hashnode/`
- [ ] Content displayed in conversation for easy copy-paste
- [ ] Output honors all applicable presentation preferences (global + Hashnode-specific)

## Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/skills/hashnode-generate/references/hashnode-constraints.md`** — Character limits, field mapping, formatting rules, and best practices

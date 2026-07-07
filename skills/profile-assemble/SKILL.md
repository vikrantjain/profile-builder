---
name: profile-assemble
description: >
  Render the canonical sections/*.json files into a single human-readable
  profile.md, using the placeholder substitution rules, section ordering, TBD
  filtering, and layout template references that produce correct output.
  Assembling profile.md is an optional, intentional action — it is NOT a
  prerequisite for any generate or review skill (those read sections/*.json
  directly). Because producing the consolidated document is a deliberate choice
  the user makes explicitly, this skill is invoked explicitly and is NOT
  auto-triggered: run it with /profile-assemble (canonical:
  /profile-builder:profile-assemble) when you want the whole profile as one
  document to read, print, or share.
disable-model-invocation: true
---

# Profile Assemble

Read structured JSON section files from `sections/`, render them through the
Markdown layout template, and produce a single complete profile document.

## When to Use

Invoke this skill when individually generated JSON section files need to be
combined into the unified `profile.md` document. Typical triggers: the user
has just finished creating or updating sections and wants to see the full
profile, or they explicitly ask for the assembled document.

Do not invoke this skill from within export or review skills — those read
section files directly and do not need an assembled profile.md.

## Workflow

### 1. Read the Index

Read and parse `profile-index.json` from the workspace root. This file contains:

- The **`identity`** object (name, title, email, links).
- The **`sections`** array listing all available section files with their paths.

If `profile-index.json` does not exist, inform the user to run `/profile-init`
or the `profile-section` skill first. Do not generate the index — it is created
upstream by `profile-init` and updated by `profile-section`.

### 2. Read the Layout Template

Read `${CLAUDE_PLUGIN_ROOT}/profile-layout.md`. This file contains the full Markdown
layout with `{{placeholder}}` syntax. It defines how JSON field values are
rendered into formatted Markdown for each section.

Also read the `placeholder_syntax` reference from
`${CLAUDE_PLUGIN_ROOT}/profile-template.md` for the substitution rules.

### 3. Determine Section Order

Assemble sections in this canonical order (matching the layout in
`${CLAUDE_PLUGIN_ROOT}/profile-layout.md`):

1. Identity header (from `sections/identity.json`)
2. Summary
3. Experience
4. Skills
5. Education
6. Certifications
7. Patents
8. Blog Posts
9. Open Source
10. Languages

### 4. Read and Validate Section Files

For each entry in the `sections` array:

- Read the JSON file at the `file` path specified in the entry.
- Parse the JSON. If the file is malformed (invalid JSON), report it as an
  error and skip this section.
- Extract the data object from the `data` key.
- Verify the `section` key matches the expected section name. If it does not
  match, warn the user (possible file mismatch) and continue using the data.
- If a section file is missing or empty, skip it silently — do not leave an
  empty heading in the output.

### 5. Render Each Section

For each section (in canonical order), render its content from the JSON data
using the corresponding section block from `${CLAUDE_PLUGIN_ROOT}/profile-layout.md`:

1. **Locate the section block** in the layout. Each section block starts with
   its `## Heading` and ends before the next `---` separator or `## Heading`.

2. **Apply placeholder substitution** using the section's JSON data:
   - `{{field}}` → replace with the string value of the named field
   - `{{#field}}...{{/field}}` → render the block only if field is non-null
     and non-empty
   - `{{^field}}...{{/field}}` → render only if field is null or absent
   - `{{#each list}}...{{/each}}` → repeat the block for each item in the
     JSON array
   - `{{.}}` → current item value inside an `#each` loop
   - `{{field | join ', '}}` → join array elements as comma-separated string
   - `{{field | default 'x'}}` → use field value or fallback
   - `{{field | capitalize}}` → capitalize first letter

3. **TBD filtering**: when substituting values, silently skip any string value
   that is exactly `"TBD"`. If all items in a list are `"TBD"`, omit the
   entire block. Collect a list of sections with TBD values to report after
   assembly.

4. After substitution, verify no `{{placeholder}}` tokens remain. If any
   remain, the section data is incomplete — warn the user.

### 6. Assemble the Document

Combine rendered sections into a single Markdown document:

- Start with the identity/contact header (rendered from
  `sections/identity.json` through the identity block of the layout).
- Append each rendered section in canonical order.
- Insert a horizontal rule (`---`) between every section.
- Do not insert a trailing `---` after the last section.
- Do not duplicate headings or add extra blank lines beyond what the layout
  specifies.

### 7. Write the Output

Write the assembled profile to `profile.md` in the workspace root.

## Handling Conflicts

If `profile.md` already exists, it will be overwritten with the newly
assembled version. The individual JSON section files in `sections/` remain
untouched — they are the source of truth.

## Output Checklist

Before finishing, verify:

- [ ] All JSON section files successfully parsed
- [ ] No `{{placeholder}}` tokens in the assembled output
- [ ] No empty sections (headings with no content)
- [ ] Horizontal rules between sections, none trailing
- [ ] Sections appear in canonical order
- [ ] TBD values silently skipped (not rendered in output)
- [ ] If any TBD values were encountered, warn the user which sections have incomplete data
- [ ] `profile.md` written to workspace root

## Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/profile-layout.md`** — Markdown rendering template for all sections
- **`${CLAUDE_PLUGIN_ROOT}/profile-template.md`** — Placeholder syntax reference and section order
- **`${CLAUDE_PLUGIN_ROOT}/profile-index-template.md`** — JSON schema reference for reading the index

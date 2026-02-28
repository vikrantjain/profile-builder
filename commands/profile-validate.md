---
name: profile-validate
description: "Validate profile documents against the template schema and interactively fix issues"
---

# Profile Validate

Check all profile documents (`profile-index.md`, section files, and `profile.md`
if assembled) against the canonical template schema for completeness, structural
correctness, and unfilled placeholders. Present findings and offer interactive
fixes with user approval.

## Workflow

### 1. Pre-flight Check

Verify `profile-index.md` exists in the workspace root.

- If it does not exist, inform the user and suggest running `/profile-init`
  first. Stop here.
- If it exists, proceed.

Load the canonical schema from `${CLAUDE_PLUGIN_ROOT}/profile-template.md` —
specifically the `fields`, `sections`, and `placeholder_syntax` blocks from the
frontmatter plus the Markdown layout below it.

Load `${CLAUDE_PLUGIN_ROOT}/profile-index-template.md` for index structure
reference.

### 2. Validate Profile Index

Read `profile-index.md` and check:

- **Identity header** — `full_name`, `title`, and `email` are present and
  non-empty in the header block.
- **Profile Sections table** — table exists with `Section`, `File`, and
  `Last Updated` columns. Each row has all three columns filled.
- **Date validity** — `Last Updated` values are valid date strings
  (YYYY-MM-DD format).
- **Data Sources table** (if present) — has `Platform`, `Handle`, and
  `Feeds Sections` columns with valid entries.

### 3. Validate Preferences File

If `preferences.md` exists in the workspace root:

- **Structure** — file has a `## Global` heading.
- **Valid platform headings** — any `##` headings besides `Global` use valid
  platform names: `LinkedIn`, `Resume`, `GitHub`, `Hashnode`.
- **No empty sections** — no `##` heading with zero bullet items under it.

If `preferences.md` does not exist, skip this step (preferences are optional).

### 4. Validate Section Files

For each section file listed in the Profile Sections table:

- **Existence** — file exists on disk at the referenced path.
- **No unfilled placeholders** — no `{{...}}` tokens remain in the file
  content.
- **No boundary horizontal rules** — file does not start or end with `---`.
- **Required fields present** — for sections with required fields per the
  `fields` schema in `profile-template.md`, verify the content includes those
  fields rendered and non-empty. Specifically:
  - `identity` — must contain full_name, title, email
  - `summary` — must contain a non-trivial summary paragraph
  - `experience` — each entry must have title, company, start_date, description; nested projects (if present) must each have name and description
  - `skills` — must have at least one category with items
- **Heading hierarchy** — headings match the expected level from the template
  layout (e.g., experience entries use `###`, section titles use `##`).

Additionally check:

- **Required sections exist** — `identity`, `summary`, `experience`, and
  `skills` must have corresponding section files on disk.
- **Orphan detection** — scan `sections/` directory for `.md` files not listed
  in the index manifest. These are orphan files.

### 5. Validate Assembled Profile

If `profile.md` exists in the workspace root:

- **No unfilled placeholders** — no `{{...}}` tokens remain.
- **No empty sections** — no `##` heading immediately followed by another `##`
  heading or end of file with no content in between.
- **Section order** — sections appear in the canonical order defined in the
  `sections` mapping of `profile-template.md`.
- **No boundary horizontal rules** — file does not start or end with `---`.

If `profile.md` does not exist, skip this step (it is generated on demand by
`profile-assemble`).

### 6. Present Findings

Group all issues into two categories:

- **Errors** — missing required section files, missing required fields,
  unfilled placeholders, structural violations (boundary `---`, broken heading
  hierarchy).
- **Warnings** — orphan section files, stale `Last Updated` dates (older than
  90 days), missing optional sections, `profile.md` out of sync or absent.

Present a summary first:

```
Validation Results: X errors, Y warnings
```

Then list each issue with:
- Severity (error/warning)
- File affected
- Description of the issue
- Whether it is auto-fixable

### 7. Temp File Cleanup

Scan `.profile/tmp/` for date-stamped session folders (format
`YYYY-MM-DD`). For each folder found:

- Report the folder name (date), sub-folders (source types), and total size.
- Identify folders older than 30 days as candidates for cleanup.

If stale folders exist, present them and ask the user which to delete:
- Offer to delete all stale folders at once, or individually.
- Delete only after explicit user approval.

If no `.profile/tmp/` directory exists or it is empty, skip this step.

### 8. Interactive Fix

For each **fixable** issue, in order of severity (errors first):

1. Describe exactly what will be changed.
2. Ask the user for approval before applying the fix.
3. Apply the fix and confirm.

Examples of fixable issues:
- Remove leading/trailing `---` from section files.
- Remove orphan files from `sections/`.
- Add missing section rows to the index manifest table.
- Update stale `Last Updated` dates after confirming content is current.

For **non-fixable** issues (missing data that requires user input), provide
actionable guidance:
- Missing required section → "Run `profile-section` for `<section>` to
  generate it."
- Unfilled placeholders → "Run `profile-section` for `<section>` to
  regenerate, or edit the file manually."
- Missing required fields within a section → "Run `profile-section` for
  `<section>` with the missing data."

### 9. Report Summary

After all fixes are applied (or skipped), present a final summary:

- Number of errors found and fixed.
- Number of warnings found and resolved.
- Remaining issues that need manual attention.
- Suggest running `profile-assemble` if section files were modified to
  regenerate `profile.md`.

## Scope Boundary

This command validates and fixes existing profile documents. It does NOT
generate new sections from scratch, invoke export skills, or run
`profile-assemble`. Those are separate user actions.

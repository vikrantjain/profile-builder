---
name: profile-validate
description: "Validate profile documents against the template schema and interactively fix issues"
---

# Profile Validate

Check all profile documents (`profile-index.json`, section JSON files, and
`profile.md` if assembled) against the canonical template schema for
completeness, structural correctness, and data integrity. Present findings
and offer interactive fixes with user approval.

## Workflow

### 1. Pre-flight Check

Verify `profile-index.json` exists in the workspace root.

- If it does not exist, inform the user and suggest running `/profile-init`
  first. Stop here.
- If it exists, proceed.

Load the canonical schema from `${CLAUDE_PLUGIN_ROOT}/profile-template.md` —
specifically the `fields`, `sections`, and `json_structure` blocks from the
frontmatter.

Load `${CLAUDE_PLUGIN_ROOT}/profile-index-template.md` for index JSON schema
reference.

Check if `sections/` contains any `.md` files (legacy format). If found,
report them as warnings: "These sections are in the old Markdown format.
Run `/profile-section` to regenerate them in JSON format, or run
`/profile-init` to rebuild all sections."

### 2. Validate Profile Index

Read and parse `profile-index.json`. Verify it is valid JSON, then check:

- **`identity` object** — `full_name`, `title`, and `email` are present and
  non-empty strings.
- **`sections` array** — each entry has `name` (string), `key` (string),
  `file` (string), and `last_updated` (string) fields, all non-empty.
- **File paths** — `file` values end in `.json`. Flag any `.md` paths
  as legacy format warnings.
- **Date validity** — `last_updated` values are valid date strings
  (YYYY-MM-DD format).
- **`sources` array** (if present) — each entry has `platform` (string),
  `handle` (string), and `feeds` (array of strings) fields with valid values.
- **Schema version** — compare `profile_version` in the index against
  `template_version` in `profile-template.md`. If they differ, flag as a
  warning: "Profile was built with schema vX.X but current template is vY.Y.
  Section files may have outdated field names or missing new fields. Schema
  drift checks in step 4 will identify specific issues."

### 3. Validate Preferences File

If `preferences.md` exists in the workspace root:

- **Structure** — file has a `## Global` heading.
- **Valid platform headings** — any `##` headings besides `Global` use valid
  platform names: `LinkedIn`, `Resume`, `GitHub`, `Hashnode`.
- **No empty sections** — no `##` heading with zero bullet items under it.

If `preferences.md` does not exist, skip this step (preferences are optional).

### 4. Validate Section Files

For each section entry in the `sections` array:

- **Existence** — file exists on disk at the referenced path (should be
  `.json`).
- **JSON validity** — file parses as valid JSON (no syntax errors, no
  trailing commas).
- **Envelope structure** — top-level object has `"section"` and `"data"`
  keys.
- **Section key match** — the `"section"` value matches the expected section
  name from the matching `sections` array entry (e.g., `"experience"` for the
  experience section file).
- **Required fields present** — for each required field in the section's
  field schema (from `profile-template.md`), verify the field exists in the
  `"data"` object and is not `null`. Fields with `"TBD"` values count as
  present but are flagged as warnings.
- **Type correctness** — verify list fields (`type: list`) are JSON arrays,
  object fields are JSON objects, string fields are strings.
- **Section-specific checks:**
  - `identity` — `data.full_name`, `data.title`, `data.email` are non-null
    strings
  - `summary` — `data.summary` is a non-empty string
  - `experience` — `data.experience` is a non-empty array; each entry has
    `title`, `company`, `start_date`, `description`; each project (if
    present) has `name`, `description`, and `contributions` (at minimum
    `["TBD"]`); `skills` and `impact` are optional. Each entry's
    `description` must be a list of bullet strings — if it is a single
    string (legacy format), flag it as a type error and offer to wrap it
    into a single-item list (auto-fixable; see Interactive Fix). The
    project-level `description` is a string by design — do not flag or wrap it.
  - `skills` — `data.skills.categories` is a non-empty array with at least
    one item having `name` and `items` fields
- **No Markdown in values** — scan string values for Markdown formatting
  characters (`**`, `##`, `- ` at start of string). Flag as warnings.
- **TBD scan** — scan all string values and array contents for the exact
  string `"TBD"`. Collect and report as warnings.
- **Schema drift** — compare the keys present in the section's `"data"`
  object (including nested `item_fields` keys within list entries) against
  the field definitions for that section in `profile-template.md`:
  - **Unknown keys** — keys in the JSON that do not match any field in the
    current template. These may be removed or renamed fields. Flag as
    warnings: "Unknown field `<key>` in `<file>` — not defined in current
    template. May be a renamed or removed field."
  - **Missing new required fields** — required fields in the template that
    are absent from the JSON (not present at all, not even as TBD). These
    may be fields added in a newer template version. Flag as errors:
    "Required field `<key>` missing from `<file>` — added in current
    template schema."
  - **Rename candidates** — when an unknown key and a missing field have
    similar names or identical types (e.g., `year` unknown + `graduation_year`
    missing), flag them together as a likely rename: "Possible rename:
    `<old_key>` → `<new_key>` in `<file>`." This helps the user and the
    interactive fix step offer targeted migrations.

Additionally check:

- **Required sections exist** — `identity`, `summary`, `experience`, and
  `skills` must have corresponding section files on disk.
- **Orphan detection** — scan `sections/` directory for `.json` files not
  listed in the index `sections` array. These are orphan files. Also scan for
  `.md` files — report separately as legacy format files.

### 5. Validate Assembled Profile

If `profile.md` exists in the workspace root:

- **No unfilled placeholders** — no `{{...}}` tokens remain.
- **No empty sections** — no `##` heading immediately followed by another `##`
  heading or end of file with no content in between.
- **Section order** — sections appear in the canonical order defined in the
  `sections` mapping of `profile-template.md`.

If `profile.md` does not exist, skip this step (it is generated on demand by
`profile-assemble`).

### 6. Present Findings

Group all issues into two categories:

- **Errors** — missing required section files, invalid JSON, missing
  envelope keys, missing required fields, type mismatches.
- **Warnings** — orphan files, legacy `.md` files, stale `last_updated`
  dates on the dynamic sections `blogs` and `open_source` (older than
  90 days — static sections change only when the user provides new data,
  so their age is never flagged), `profile.md`
  older than the most recently updated section file (out of sync — an
  absent `profile.md` is normal, not a warning; it is generated on demand
  by `profile-assemble`), `TBD` placeholder values (signals incomplete
  data that will be silently skipped by export skills), Markdown
  formatting in JSON string values.

Missing **optional** sections (patents, languages, etc.) are not warnings —
a user with no patents should not be nagged on every run. Mention them once
as an informational line at the end of the summary ("Optional sections not
present: patents, languages") and do not count them in the warning total.

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
- Remove orphan files from `sections/`.
- Add missing section entries to the index `sections` array.
- Update stale `last_updated` dates after confirming content is current.
- Update section `file` paths from `.md` to `.json` (if files were migrated).
- **Rename fields** — for rename candidates identified in schema drift
  detection, rename the JSON key in-place (preserving the value). E.g.,
  rename `year` → `graduation_year` in `sections/education.json`.
- **Remove unknown fields** — for unknown keys with no rename candidate,
  offer to remove them from the JSON. Show the current value so the user
  can judge whether the data should be moved elsewhere first.
- **Backfill missing required fields** — for new required fields with no
  rename candidate, add them with the TBD default (`"TBD"` or `["TBD"]`).
- **Wrap a stringified experience description** — if any
  `data.experience[].description` is a string instead of a list, wrap it into
  a single-item list (`"Led the platform team…"` → `["Led the platform
  team…"]`), preserving the text verbatim. Apply only to the experience
  entry's `description`, never to a project's `description` (a string by design).
- **Update schema version** — after all drift fixes are applied, update
  `profile_version` in `profile-index.json` to match the current
  `template_version`.

For **non-fixable** issues (missing data that requires user input), provide
actionable guidance:
- Missing required section → "Run `/profile-section` for `<section>` to
  generate it."
- Invalid JSON → "Run `/profile-section` for `<section>` to regenerate."
- Missing required fields within a section → "Run `/profile-section` for
  `<section>` with the missing data."

### 9. Report Summary

After all fixes are applied (or skipped), present a final summary:

- Number of errors found and fixed.
- Number of warnings found and resolved.
- Remaining issues that need manual attention.
- Suggest running `/profile-assemble` if section files were modified and the
  user wants to regenerate `profile.md`.

## Scope Boundary

This command validates and fixes existing profile documents. It does NOT
generate new sections from scratch, invoke export skills, or run
`profile-assemble`. Those are separate user actions.

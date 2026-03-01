---
name: profile-assemble
description: >
  This skill should be used when the user asks to "assemble my profile",
  "stitch sections together", "build full profile from sections",
  "combine profile sections", "create profile from section files",
  "merge profile sections", "finalize my profile", or wants to combine
  individually generated section files into a single complete Markdown
  profile document (profile.md).
---

# Profile Assemble

Combine individually generated section files from `sections/` into a single,
complete Markdown profile document.

## When to Use

Invoke this skill after sections have been generated or updated independently
via the `profile-section` skill and a unified profile document is needed — for
example, to export for LinkedIn, produce a resume, or generate platform-ready content.

## Workflow

### 1. Read the Index

Read `profile-index.md` from the workspace root. This file contains:

- The **identity/contact header** (name, title, email, links).
- The **manifest table** listing all available section files with their paths.

If `profile-index.md` does not exist, check whether section files exist in
`sections/`. If they do, generate the index first using
`${CLAUDE_PLUGIN_ROOT}/profile-index-template.md`. If no section files exist either, inform the user
to run `/profile-init` or the `profile-section` skill first.

### 2. Determine Section Order

Assemble sections in this canonical order (matching the layout in
`${CLAUDE_PLUGIN_ROOT}/profile-template.md`):

1. Identity header (from `profile-index.md` or `sections/identity.md`)
2. Summary
3. Experience
4. Skills
5. Education
6. Certifications
7. Patents
8. Blog Posts
9. Open Source
10. Languages

### 3. Read and Validate Section Files

For each section listed in the manifest:

- Read the file at the path specified in the manifest.
- If a section file is missing or empty, skip it silently — do not leave an
  empty heading in the output.
- Verify no `{{placeholder}}` tokens remain in any section file. If found,
  warn the user that the section may be incomplete.

### 4. Stitch the Document

Combine sections into a single Markdown document:

- Start with the identity/contact header from `profile-index.md`.
- Append each section in canonical order.
- Insert a horizontal rule (`---`) between every section.
- Do not insert a trailing `---` after the last section.
- Do not duplicate headings or add extra blank lines beyond what the layout
  specifies.

### 5. Write the Output

Write the assembled profile to `profile.md` in the workspace root.

## Handling Conflicts

If `profile.md` already exists, it will be overwritten with the newly
assembled version. The individual section files in `sections/` remain
untouched — they are the source of truth.

## Output Checklist

Before finishing, verify:

- [ ] No `{{placeholder}}` tokens in the assembled output
- [ ] No empty sections (headings with no content)
- [ ] Horizontal rules between sections, none trailing
- [ ] Sections appear in canonical order
- [ ] If any `TBD` values are present, warn the user which sections have incomplete data
- [ ] `profile.md` written to workspace root

## Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/profile-index-template.md`** — Template for generating/updating the index
- **`${CLAUDE_PLUGIN_ROOT}/profile-template.md`** — Canonical section order reference (layout below frontmatter)

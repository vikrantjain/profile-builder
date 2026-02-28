---
name: profile-section
description: >
  This skill should be used when the user asks to "generate a section",
  "update experience section", "rebuild my skills section", "regenerate
  certifications", "add a project to my experience", "update my blog posts",
  "refresh open source section", or wants to generate or update a single
  profile section independently without regenerating the entire profile.
---

# Profile Section

Generate or update a single profile section as a standalone Markdown file.
This enables targeted updates, parallel generation by multiple agents, and
efficient use of smaller context windows.

## Critical: This Is a Data Source, Not a Resume

The profile is a **comprehensive canonical data layer** — the single source of
truth from which downstream outputs (resumes, LinkedIn, GitHub READMEs) are
later generated. When building or updating a section:

- **Include every item** from the source data. Do not drop or omit jobs,
  projects, certifications, skills, or any other entries because they seem old,
  minor, or less relevant.
- **Preserve all information** — every fact, date, technology, metric, and
  detail must be retained. Do not lose information during rewording.
- **Improve clarity and conciseness** — reword, tighten, and restructure
  sentences for readability. Better phrasing and shorter sentences are
  encouraged, as long as no information is lost in the process.
- **Never apply resume heuristics** such as limiting to recent roles, dropping
  entries to fit a page length, or omitting details deemed unimportant.

If source data is genuinely ambiguous or duplicated, keep both entries and note
the ambiguity — let the user decide what to remove.

## When to Use

Invoke this skill when only one section of the profile needs to be created or
refreshed. For first-time setup of all sections, use the `/profile-init`
command. For stitching existing section files into a full document, use the
`profile-assemble` skill.

## Available Sections

The `sections` mapping in `${CLAUDE_PLUGIN_ROOT}/profile-template.md` defines all valid sections:

| Section | Output File | Key Fields |
|---------|-------------|------------|
| identity | `sections/identity.md` | full_name, title, email, phone, location, links |
| summary | `sections/summary.md` | summary, years_of_experience |
| experience | `sections/experience.md` | experience (list with nested projects) |
| skills | `sections/skills.md` | skills.categories, skills.soft |
| education | `sections/education.md` | education (list) |
| certifications | `sections/certifications.md` | certifications (list) |
| patents | `sections/patents.md` | patents (list) |
| blogs | `sections/blogs.md` | blogs (list) |
| open_source | `sections/open-source.md` | projects, contributions |
| languages | `sections/languages.md` | languages (list) |

## Workflow

### 1. Identify the Target Section

Determine which section the user wants to generate or update. If ambiguous,
ask the user to specify. Accept both the section key (e.g., `experience`) and
natural names (e.g., "work history", "jobs").

### 2. Load Only What Is Needed

Read `${CLAUDE_PLUGIN_ROOT}/profile-template.md` and extract only:

- The **field definitions** for the target section's fields (listed in the
  `sections` mapping under `fields`).
- The **Markdown layout snippet** for that section from the full layout below
  the frontmatter. Each section is bounded by `## Heading` and the next `---`
  or `## Heading`.
- The **placeholder syntax** reference.

Do not load or process other sections.

### 3. Gather Data

**Dynamic sections (blogs, open_source):** Check if `profile-index.md` exists
and contains a Data Sources table. If it does and the target section appears in
any source's `feeds` column, invoke the `profile-refresh` skill first to fetch
the latest data from configured platforms and update the section file. Then read
the updated section file as the baseline for any additional user-provided data.

**Static sections (all others):** Collect data from user-provided sources only.

If the section already exists as a file in `sections/`, read it to understand
what is being updated versus replaced.

For updates (adding entries to a list section like experience or open_source):

- Read the existing section file.
- Merge new entries with existing entries, preserving order (most recent first).
- Do not duplicate entries.

### 4. Render the Section

Apply the same rendering rules as full profile generation:

- Replace all `{{placeholder}}` tokens with real data.
- Follow the repeating block patterns for list fields.
- Preserve Markdown formatting and heading levels.
- Do **not** include horizontal rules (`---`) at the start or end of the
  section file — the assembler adds those during stitching.
- Output only the target section's Markdown — no frontmatter, no other sections.

### 5. Write the Output

Write the rendered section to the path specified in the `sections` mapping
(e.g., `sections/experience.md`).

### 6. Update the Index

After writing the section file, update `profile-index.md`:

- Update the manifest table row for this section with the current date as
  `last_updated`. If no row exists for this section, add one.
- If `profile-index.md` does not exist, inform the user to run
  `/profile-init` first to create the index.

## Output Checklist

Before finishing, verify:

- [ ] No `{{placeholder}}` tokens remain in the output
- [ ] Output contains only the target section — no other sections leaked in
- [ ] No `---` at the start or end of the file
- [ ] Section file written to the correct `sections/` path
- [ ] `profile-index.md` manifest updated with current date

## Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/profile-template.md`** — Field definitions, section mapping, and layout
- **`profile-index.md`** — Data Sources table for dynamic section refresh

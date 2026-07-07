---
name: profile-init
description: "Initialize a new professional profile by collecting data from user-provided sources and building all profile sections"
---

# Profile Init

Set up a new professional profile from scratch. Collect data from the user,
build all profile sections, and generate the profile index.

## Workflow

### 1. Check for Existing Profile

Check if `profile-index.json` or `sections/` already exist in the workspace.

- If they exist, warn the user that re-initializing will overwrite existing
  profile data. Ask for confirmation before proceeding.
- If `sections/` contains `.md` files (legacy format), note that
  re-initializing will replace them with `.json` files.
- If they do not exist, proceed.

### 2. Collect Data Sources

Ask the user what data sources they have available. Present these options:

- **Resume file** — path to a resume (PDF, DOCX, or Markdown)
- **GitHub profile URL** — e.g. `https://github.com/username`
- **LinkedIn profile URL** — e.g. `https://linkedin.com/in/username`
- **Blog platform** — Hashnode or Dev.to handle/URL
- **Additional text** — anything else they want included (patents, projects,
  certifications, etc.)

Accept whatever the user provides. Not all sources are required — the profile
is built from what is available.

### 3. Extract Platform Handles

From the provided URLs, extract handles for the `sources` array:

- GitHub URL `https://github.com/vikrant` → handle: `vikrant`
- Hashnode URL `https://vikrant.hashnode.dev` or handle `vikrant` → handle: `vikrant`
- Dev.to URL `https://dev.to/vikrant` or handle `vikrant` → handle: `vikrant`

Map each platform to the sections it feeds:

| Platform | Feeds |
|----------|-------|
| github | open_source |
| hashnode | blogs |
| devto | blogs |


### 4. Generate Profile Index

Generate `profile-index.json` early so it is available throughout the rest of
the workflow. Use the schema defined in
`${CLAUDE_PLUGIN_ROOT}/profile-index-template.md` to construct the JSON object:

- **`identity`** — name, title, email, links from the data collected so far
  (may be partial at this stage). Optional fields with no data use `null`.
- **`sections`** — start with an empty array `[]`. Each section will be added
  as it is built in step 6. The `profile-section` workflow updates the index
  after writing each section file.
- **`sources`** — one entry per configured platform with `handle` and `feeds`
  fields, using the handles extracted in step 3.

Write to `profile-index.json` in the workspace root.

### 5. Read and Parse Data Sources

Read the provided data sources:

- **Resume file:** Read the file and extract structured information for all
  profile fields (identity, experience, education, skills, certifications,
  patents, summary).
- **GitHub URL:** Use `gh` CLI or WebFetch to get the user's profile info,
  pinned repos, and bio.
- **LinkedIn URL:** Note the URL for the identity section. If Playwright MCP
  is available, fetch profile data. Otherwise, ask the user to provide
  LinkedIn content as text.
- **Blog platform:** Note the handle for Data Sources configuration. Actual
  blog posts will be fetched during the refresh step.

### 6. Build All Sections

**Important:** The profile is a comprehensive data source, not a resume. When
building sections, include **every** item from the collected sources — every
job, project, certification, skill, patent, and detail. Do not omit anything
for brevity or perceived relevance. Rewording for clarity and conciseness is
fine, but no information should be lost. Downstream export skills handle
tailoring; this step must capture everything.

For each section defined in the `sections` mapping of `${CLAUDE_PLUGIN_ROOT}/profile-template.md`,
generate the section file using the `profile-section` workflow:

1. Read the field definitions and JSON structure conventions for the section
   from `${CLAUDE_PLUGIN_ROOT}/profile-template.md`.
2. Re-read the source file(s) from disk and extract only the data relevant to
   this section. Do not rely on source data remaining in context from step 5 —
   always re-read from disk to avoid context-dependent data loss.
3. Map input data to all template fields — follow the field mapping rules in
   the `profile-section` skill (Step 4), including duration extraction for
   projects and populating required `contributions` (default `["TBD"]` if no
   work items can be extracted). Populate `impact` when quantifiable outcomes
   exist in the source data.
4. Build the JSON object with the mapped data — follow the JSON building rules
   in the `profile-section` skill (Step 5).
5. Write to the output path (e.g., `sections/experience.json`).
6. Update `profile-index.json` — add or update the section's entry in the
   `sections` array with `name`, `key`, `file`, and `last_updated`. If the
   section is `identity`, also sync the top-level `identity` object with the
   section data. Follow the index update rules in the `profile-section` skill
   (Step 7).

Process sections in this order:
1. identity
2. summary
3. experience
4. skills
5. education
6. certifications
7. patents
8. blogs
9. open_source
10. languages

Skip any **optional** section for which no data was collected — do not create
empty section files. The four **required** sections (identity, summary,
experience, skills) should always be generated: fill what data you have and use
the `TBD` convention (per the `profile-section` rules) for required fields with
no extractable data, rather than skipping the section. This keeps the output
consistent with `/profile-validate`, which treats these four as required and
flags them as errors when absent.

### 7. Verify Source Coverage

After building all sections, cross-reference the generated section files against
the original source data to ensure no important information was lost during
extraction. Process **one section at a time** to keep context bounded — do not
load all sections and all sources simultaneously.

For each section that has source data, perform the following:

#### 7a. Compare Source Against Section

1. Re-read the source file(s) from disk (e.g., the resume file) and identify
   all items relevant to this section.
2. Read and parse the generated JSON section file from disk.
3. **Count check** — compare item counts between source and section JSON
   arrays (e.g., number of jobs, degrees, certifications, skill categories,
   patents, languages). A count mismatch is an immediate signal that
   something was dropped.
4. **Item-level check** — for each item in the source, verify it appears in
   the section's JSON data. Flag any item that is missing or incomplete.

Common gaps to watch for:

- A job, degree, or certification present in the resume but absent from the
  section file
- Skills mentioned across experience entries or elsewhere in the resume but not
  captured in the skills section
- Contact info or profile links present in the source but missing from identity
- Patent details partially captured (e.g., title present but number missing)

#### 7b. Fix Gaps

For each flagged gap, update the section JSON file to include the missing
information. Follow the same JSON building rules as step 6.

#### 7c. Re-check

After fixes, re-read the section file and verify the gaps are resolved. If gaps
persist after two iterations for a section, present the remaining items to the
user and ask whether they should be included or are intentional omissions.
Accept the user's decision and move on to the next section.

### 8. Report Results

Summarize what was created:

- Number of sections generated.
- Which data sources were used.
- Any sections that were skipped due to missing data.
- Which dynamic sources (blogs, open_source) are configured in the `sources`
  array. Inform the user they can run `profile-refresh` to fetch latest data
  from these platforms when ready.

### 9. Validate Profile

Run the `/profile-validate` workflow to check all generated documents against
the template schema. Present any errors or warnings found and offer interactive
fixes before finishing.

## Scope Boundary

This command ends after validation. Do NOT invoke `profile-assemble`
or any export/review skill. The user will assemble or export when ready.

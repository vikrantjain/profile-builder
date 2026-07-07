---
name: profile-section
description: >
  Create or update a single profile section (experience, skills, education,
  certifications, patents, blogs, open source, identity, summary, languages)
  in the canonical sections/*.json data layer. Contains the required JSON
  envelope format, field-mapping rules, TBD placeholder conventions, and
  index-update logic — writing section data without these rules produces
  invalid output. Because it writes to the profile's source of truth, this
  skill is invoked explicitly and is NOT auto-triggered: run it with
  /profile-section (canonical: /profile-builder:profile-section) whenever you
  want to add or change profile data — e.g. "add my new certification",
  "update my experience", "I got promoted", "rebuild my skills".
disable-model-invocation: true
---

# Profile Section

Generate or update a single profile section as a standalone JSON data file.
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
- **Do not add information** — never fabricate, infer, or embellish details
  that are not present in the source data. If the input says "evaluating
  against production readiness criteria", do not expand that to "evaluating
  against production readiness criteria across 15+ dimensions". Rewording
  for clarity is allowed; introducing new claims, numbers, or qualifiers
  is not.
- **Improve clarity and conciseness** — reword, tighten, and restructure
  sentences for readability. Better phrasing and shorter sentences are
  encouraged, as long as no information is added or lost in the process.
- **Never apply resume heuristics** such as limiting to recent roles, dropping
  entries to fit a page length, or omitting details deemed unimportant.

If source data is genuinely ambiguous or duplicated, keep both entries and note
the ambiguity — let the user decide what to remove.

## When to Use

Invoke this skill when the user wants to create, update, or add entries to a
single section of their profile. Common scenarios:

- User provides new data (a resume snippet, job details, certification info)
  and wants it captured into the profile
- User wants to update an existing section with new information (new role,
  new project, updated skills)
- User asks to regenerate a section from scratch

For first-time setup of all sections at once, use the `/profile-init` command.
For rendering section files into a full Markdown document, use the
`profile-assemble` skill.

## Available Sections

The `sections` mapping in `${CLAUDE_PLUGIN_ROOT}/profile-template.md` defines all valid sections:

| Section | Output File | Key Fields |
|---------|-------------|------------|
| identity | `sections/identity.json` | full_name, title, email, phone, location, avatar_url, github, linkedin, website, twitter, years_of_experience |
| summary | `sections/summary.json` | summary |
| experience | `sections/experience.json` | experience (list with nested projects) |
| skills | `sections/skills.json` | skills.categories, skills.soft |
| education | `sections/education.json` | education (list) |
| certifications | `sections/certifications.json` | certifications (list) |
| patents | `sections/patents.json` | patents (list) |
| blogs | `sections/blogs.json` | blogs (list) |
| open_source | `sections/open-source.json` | projects, contributions |
| languages | `sections/languages.json` | languages (list) |

## Workflow

### 1. Identify the Target Section

Determine which section the user wants to generate or update. If ambiguous,
ask the user to specify. Accept both the section key (e.g., `experience`) and
natural names (e.g., "work history", "jobs").

### 2. Load Only What Is Needed

Read `${CLAUDE_PLUGIN_ROOT}/profile-template.md` and extract only:

- The **field definitions** for the target section's fields (listed in the
  `sections` mapping under `fields`), including all nested `item_fields`.
- The **JSON structure conventions** from the `json_structure` block.

Do not load the Markdown layout (`profile-layout.md`) — layout is only used
by `profile-assemble`. Do not load or process other sections' fields.

### 3. Gather Data

**Dynamic sections (blogs, open_source):** Check if `profile-index.json` exists
and contains a `sources` array. If it does and the target section appears in
any source's `feeds` list, invoke the `profile-refresh` skill first to fetch
the latest data from configured platforms and update the section file. Then read
the updated section file as the baseline for any additional user-provided data.

**Static sections (all others):** Collect data from user-provided sources only.

If the section already exists as a JSON file in `sections/`, read and parse it
to understand what is being updated versus replaced. If it exists as a legacy
`.md` file, use the user-provided data as the baseline — do not attempt to
parse old Markdown content.

For updates (adding entries to a list section like experience or open_source):

- Read and parse the existing JSON section file.
- Merge new entries with existing entries, preserving order (most recent first).
- Do not duplicate entries.

### 4. Map Input to All Template Fields

Systematically map the input data to **every** field defined in the template
for this section — not just the obvious ones. The user's input may use
different labels, formatting, or structure than the template expects.

For each field in the template schema (including nested `item_fields`):

1. **Scan the entire input** for data that matches the field's semantic meaning,
   regardless of how it is labelled. For example:
   - "Action/Achievement" bullets → `contributions` (work done) and/or `impact` (measurable outcomes)
   - Date ranges like "Dec 2025 – Jan 2026" → `duration` (for projects) or
     `start_date`/`end_date` (for experience)
   - "Technologies" / "Tech" / "Stack" / "Built with" → `tech_stack`
   - Phrases like "I used", "I personally worked with", "my tools", "skills I applied" → `skills` (what the person directly used, which may overlap with or be a subset of `tech_stack`; also captures practice-level skills not listed as technologies, e.g., "Vibe coding", "Prompt Engineering")
   - Role descriptions like "led", "sole developer", "tech lead" → `role`
   - URLs or repo links → `url`

2. **Attempt every field** — not just required ones. Optional fields (`required: false`)
   like `role`, `duration`, `tech_stack`, `url`, `location`, `type` carry valuable
   data that improves downstream exports. Treat them as "fill if extractable",
   not "skip unless obvious". For required fields with defaults (e.g., `contributions`
   defaults to `["TBD"]`), extract real values whenever possible and only fall
   back to the default when the input genuinely contains no relevant data.

3. **Separate description from work and impact**: The `description` field captures
   *what the project/role does*. Technical work, design decisions, and problems
   solved belong in `contributions`. Quantifiable outcomes, metrics, and business
   results belong in `impact`. If the input mixes all three, split them into the
   appropriate fields.

4. **Actively extract impact**: Do not treat `impact` as a passive optional field.
   Scan every piece of source data for quantifiable outcomes: percentages,
   time/cost savings, scale numbers (users, requests, records), adoption figures,
   before/after comparisons, SLA improvements, error rate reductions, and
   performance gains. Only leave `impact` empty after confirming that the source
   genuinely contains no measurable outcomes for this project.

5. **Do not silently discard data** that doesn't map to any field. If the input
   contains information with no matching template field, include it in the closest
   relevant field (usually `description`) and note the mismatch.

### 5. Build the JSON Object

Construct a JSON object with the following structure:

```json
{
  "section": "<section_key>",
  "data": {
    "<field_name>": "<value per schema>"
  }
}
```

Rules for building the data object:

- Use field names exactly as defined in `profile-template.md` (e.g.,
  `full_name`, `tech_stack`, `contributions`).
- **String fields** → JSON string value.
- **List fields** (`type: list`) → JSON array.
- **Nested object fields** (e.g., `skills.categories`, `open_source.projects`)
  → preserve nesting as JSON objects/arrays.
- **Required fields with no extractable data** → use `"TBD"` (string) or
  `["TBD"]` (for list fields). Do not use `null` for required fields.
- **Optional fields with no data** → use `null` or omit the key entirely.
  Do not set optional fields to `"TBD"`.
- **Dates** → write as the user provided them (e.g., `"Jan 2021"`). Do not
  convert to ISO 8601 — that is the responsibility of downstream skills.
- **No Markdown formatting in values** — values are raw data. Do not include
  `**bold**`, `## headings`, `- bullets`, or any other Markdown syntax in
  string values. Just write the plain text.

### Example Output

A completed `sections/education.json` looks like this:

```json
{
  "section": "education",
  "data": {
    "education": [
      {
        "degree": "Master of Science",
        "field": "Computer Science",
        "institution": "Stanford University",
        "graduation_year": "2018"
      }
    ]
  }
}
```

Note: `graduation_year` is optional and could be omitted or set to `null` —
never to `"TBD"`. Required fields with no data would use `"TBD"` instead.

### 6. Write the Output

Write the JSON object to the path specified in the `sections` mapping
(e.g., `sections/experience.json`). Validate the JSON is well-formed before
writing. If any required fields are missing from the data object (not even
set to TBD), add them with their TBD default before writing.

### 7. Update the Index

After writing the section file, update `profile-index.json`:

- Read and parse `profile-index.json`. Find the entry in the `sections` array
  whose `key` matches the target section. Update its `last_updated` to the
  current date in YYYY-MM-DD format and ensure its `file` path uses the `.json` extension. If no
  entry exists for this section, add one with `name`, `key`, `file`, and
  `last_updated`.
- **Identity sync:** If the target section is `identity`, also update the
  top-level `identity` object in `profile-index.json` with the corresponding
  fields from the section data (`full_name`, `title`, `email`, `phone`,
  `location`, `github`, `linkedin`, `website`, `twitter`). This keeps the
  lightweight identity snapshot in sync with `sections/identity.json`.
- Write the updated JSON back to `profile-index.json`.
- If `profile-index.json` does not exist, inform the user to run
  `/profile-init` first to create the index.

## Output Checklist

Before finishing, verify:

- [ ] JSON is valid and well-formed (no trailing commas, all strings quoted)
- [ ] All required fields present — either with real data or TBD convention
- [ ] Optional fields with no data are `null` or omitted — not set to TBD
- [ ] No Markdown formatting characters in string values (no `**`, `##`, `- `)
- [ ] `TBD` defaults used only where no extractable data exists in the input
- [ ] Output contains only the target section — no other sections' fields
- [ ] Section file written to the correct `sections/` path (`.json` extension)
- [ ] `profile-index.json` sections array updated with current date

## Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/profile-template.md`** — Field definitions, section mapping, and JSON structure conventions
- **`profile-index.json`** — Source configuration (`sources` array) for dynamic section refresh

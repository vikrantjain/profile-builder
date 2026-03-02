---
name: resume-generate
description: >-
  This skill should be used when the user asks to "generate a resume",
  "create a resume", "build a resume for this job", "tailor my resume",
  "make a resume from my profile", "make an ATS-optimized resume",
  "generate resume JSON", or wants a customized resume document generated
  from their profile data, optionally tailored to a specific job description.
---

# Resume Generate

Generate a tailored, ATS-optimized resume from the master profile, optionally
customized for a specific job description. Output as both Markdown (`resume.md`)
and JSON Resume format (`resume.json`). The Markdown is a polished, standalone
resume document. The JSON is a structured representation in the
[JSON Resume](https://jsonresume.org/schema) open standard, ready for import
into Reactive Resume, JSON Resume renderers, or any compatible tool.

## When to Use

Invoke this skill to produce a resume document. The user may provide a job
description to tailor the resume, or request a general-purpose resume. For
LinkedIn-specific content formatting, use the `linkedin-generate` skill instead.

## Workflow

### 1. Gather Inputs

Determine what the user needs:

- **Job description** (optional): if provided, tailor the resume to match.
  The user may paste it, provide a URL, or reference a file.
- **Target length**: default is 1-2 pages unless specified.
- **Sections to include/exclude**: by default, include all relevant sections.
- **ATS priority**: if the user mentions ATS, applicant tracking, or keyword
  optimization, apply enhanced ATS optimization in step 4.

### 2. Read Profile Data

Read the relevant profile section JSON files from `sections/`. Parse each
JSON file and access fields directly from the `data` object. If required section JSON files do not exist, inform the user and suggest
running `/profile-init` or `profile-section` to generate them. At minimum, read:

- `sections/identity.json` — name, contact info
- `sections/summary.json` — professional bio
- `sections/experience.json` — work history
- `sections/skills.json` — technical and soft skills
- `sections/education.json` — degrees

Optionally read certifications, open source, patents based on relevance.

### 3. Apply Presentation Preferences

Read `preferences.md` from the workspace root. If it exists:

1. Read the `## Global` section — these apply to all exports.
2. Read the `## Resume` section (if present) — these are resume-specific.
3. Treat each preference as a binding directive during content transformation.
   Examples: "present experience as 20+ years" → use that framing; "don't
   highlight patents" → de-emphasize or omit; tone directives → adjust writing
   style accordingly.
4. Resume-specific preferences take precedence over global if they conflict.
5. When a preference conflicts with job-description tailoring (step 4),
   the preference wins — it reflects the user's deliberate intent.

If `preferences.md` does not exist, proceed with default behavior.

### 4. Tailor Content

Consult `${CLAUDE_PLUGIN_ROOT}/skills/resume-generate/references/resume-conventions.md` for formatting rules,
tailoring strategy, and ATS optimization guidelines.

If a job description is provided:

- Extract key requirements (skills, experience level, qualifications).
- Reorder and prioritize skills that match the job requirements.
- Adjust the professional summary to align with the target role.
- Emphasize relevant achievements in experience bullets.
- De-emphasize or omit content not relevant to the role.

#### ATS Optimization

Apply the following to maximize ATS pass-through rate:

1. **Keyword gap analysis**: Extract hard skills, tools, certifications, and
   role-specific terms from the job description. Compare against the resume
   content. For each missing keyword that the user genuinely possesses (per
   the master profile), weave it into an appropriate bullet or skills line
   using exact-match phrasing from the JD.
2. **Standard section headings**: Use conventional headings that ATS parsers
   recognize: "Professional Summary", "Experience", "Skills", "Education",
   "Certifications". Avoid creative alternatives.
3. **Plain formatting**: No tables, columns, headers/footers, or images in
   the Markdown. Use simple bullet lists and standard heading hierarchy.
4. **Spell out acronyms once**: First occurrence should include both the full
   term and acronym, e.g., "Continuous Integration / Continuous Deployment (CI/CD)".
5. **Date format consistency**: Use "Mon YYYY" format (e.g., "Jan 2021")
   throughout for ATS date parsing.
6. **Keyword density**: Ensure the top 5-10 JD keywords each appear at least
   twice in the resume (naturally, not stuffed).

If no job description is provided, produce a general-purpose resume using
the full profile data, prioritizing recent and significant experience.
Apply items 2-5 from ATS optimization regardless.

### 5. Generate Markdown Resume

**TBD filtering:** Profile data may contain `TBD` as a placeholder value in
any field (indicating data not yet filled in by the user). When rendering
output, silently skip any value that is exactly `TBD` — do not render it.
If all items in a list are `TBD`, omit that list/block entirely.

Write the resume as Markdown to `resume.md`. This is a polished, standalone
resume document — not a plain-text dump of the JSON. Follow these rules:

- Use clean, professional Markdown formatting.
- Start each experience bullet with a strong action verb.
- Quantify achievements where possible.
- No personal pronouns ("I", "my").
- Past tense for previous roles, present tense for current.
- Target 1-2 pages of content (roughly 400-800 words).

### 6. Generate JSON Resume

Write a `resume.json` file in the [JSON Resume](https://jsonresume.org/schema)
open standard format. This file represents the same tailored content as
`resume.md` in a structured, machine-readable form.

Consult `${CLAUDE_PLUGIN_ROOT}/skills/resume-generate/references/json-resume-schema.md` for the complete
field mapping from profile data to JSON Resume fields.

Map the tailored content to JSON Resume sections:

- **basics**: name, label (title), email, phone, url, location, profiles
- **work**: one entry per role with name, position, startDate, endDate, summary, highlights (from contributions + impact)
- **education**: institution, studyType, area, startDate, endDate, score
- **skills**: one entry per category with name, level, keywords
- **certificates**: name, issuer, date, url
- **languages**: language, fluency
- **projects**: name, description, highlights (from contributions + impact), startDate, endDate, url

Omit empty sections entirely (do not include sections with empty arrays).

### 7. Verify Preferences Compliance

Before writing output, re-read the applicable preferences and verify each one
is reflected in the generated content. If any preference was missed or
contradicted, revise the content before proceeding.

### 8. Present to User

Display the generated resume content in the conversation and confirm where
files were written. Mention that `resume.json` can be imported into
[Reactive Resume](https://rxresu.me/), JSON Resume renderers, or any
compatible tool for visual formatting and PDF export.

## Output Checklist

Before finishing, verify:

- [ ] Resume is tailored to the job description (if provided)
- [ ] ATS optimization applied (standard headings, plain formatting, keywords present)
- [ ] All content is factual — sourced from the master profile, not fabricated
- [ ] Length is appropriate (1-2 pages equivalent)
- [ ] Markdown file written to `resume.md`
- [ ] JSON Resume file written to `resume.json` (valid against JSON Resume schema)
- [ ] Output honors all applicable presentation preferences (global + resume-specific)

## Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/skills/resume-generate/references/resume-conventions.md`** — Length rules, section order, tailoring strategy, ATS guidelines
- **`${CLAUDE_PLUGIN_ROOT}/skills/resume-generate/references/json-resume-schema.md`** — JSON Resume schema field mapping

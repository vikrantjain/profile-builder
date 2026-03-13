---
name: resume-generate
description: >-
  This skill generates a high-impact, strategically crafted resume tailored to
  a specific job description or target role. Use when the user asks to "generate
  a resume", "create a resume", "build a resume for this job", "tailor my resume",
  "make a resume from my profile", "make an ATS-optimized resume", "generate
  resume JSON", "create a CV", "write my curriculum vitae", "prepare a job
  application", "customize resume for this role", "update my resume", "shorten
  my resume", "resume for [company]", or wants a polished resume document
  produced from their profile data. Also trigger when the user provides a job
  description or job link and asks to apply, prepare application materials, or
  just says "resume for this". Trigger for any resume editing, refinement, or
  regeneration request — not just first-time generation.
---

# Resume Generate

Generate a high-impact, strategically crafted resume — not a data dump of profile
sections. The profile is a datastore; the resume is a persuasion document. Every
line should earn its place by demonstrating fit for the target role.

The primary output is `resume.md` — a PDF-ready Markdown document with
professional formatting that converts cleanly to PDF for immediate use.
Optionally, also generates `resume.json` in the
[JSON Resume](https://jsonresume.org/schema) open standard for import into
Reactive Resume or other resume builder tools.

## When to Use

Invoke this skill to produce a resume document. The user may provide a job
description to tailor the resume, or request a general-purpose resume. For
LinkedIn-specific content formatting, use the `linkedin-generate` skill instead.

## Core Philosophy

The profile sections are raw material — a comprehensive datastore of everything
the user has done. A resume is not a reformatted view of that data. It is a
**strategically composed narrative** that:

- **Selects** the most relevant achievements from a larger pool
- **Reframes** contributions in the language of the target role
- **Prioritizes** impact and outcomes over responsibilities
- **Omits** anything that doesn't strengthen the candidacy

A 20-year career with 8 roles and 30 projects might produce a resume with 4 roles
and 12 bullets. The craft is in choosing which 12 and making each one count.

## Workflow

### 1. Gather Inputs

Determine what the user needs:

- **Target role input** — The user may provide any of these (from most to
  least specific):
  - A full **job description** (pasted, URL, or file reference). If the user
    provides a URL, use WebFetch to retrieve the job description content.
  - A **role description** (e.g., "architect role at a big tech like Oracle",
    "senior backend engineer at a startup", "engineering manager at a Series B")
  - Nothing — general-purpose resume anchored to their current trajectory

  When the user provides a role description rather than a JD, infer the likely
  requirements: what skills, experience level, and achievements would a hiring
  manager for that role at that type of company expect? Use this inference the
  same way you would use an extracted JD. If the user hasn't provided either,
  ask if they have a target in mind — a targeted resume is dramatically more
  effective than a generic one.
- **Target length**: default is 1-2 pages unless specified. The user may
  request a specific page count (e.g., "2 page resume").
- **Sections to include/exclude**: by default, include all relevant sections.
- **ATS priority**: if the user mentions ATS, applicant tracking, or keyword
  optimization, apply enhanced ATS optimization in step 5. "ATS-friendly"
  in the request means apply all ATS rules aggressively.

### 2. Read Profile Data

If `resume.md` already exists, note it but always regenerate from profile
sections — fresh tailoring requires starting from the full data pool, not
a previously narrowed resume. The existing file will be overwritten.

Read `profile-index.json` to discover available sections and their file paths.
Then read the relevant section JSON files from `sections/`. Parse each JSON file
and access fields directly from the `data` object.

If required section JSON files do not exist, inform the user and suggest running
`/profile-init` or `profile-section` to generate them. At minimum, read:

- `sections/identity.json` — name, contact info
- `sections/summary.json` — professional bio
- `sections/experience.json` — work history
- `sections/skills.json` — technical and soft skills
- `sections/education.json` — degrees

Also read certifications, open source, patents, blogs, and languages if they
exist in the index — these may contain material worth surfacing depending on
role relevance.

### 3. Apply Presentation Preferences

Read `preferences.md` from the workspace root. If it exists:

1. Read the `## Global` section — these apply to all exports.
2. Read the `## Resume` section (if present) — these are resume-specific.
3. Treat each preference as a binding directive during content transformation.
   Examples: "present experience as 20+ years" → use that framing; "don't
   highlight patents" → de-emphasize or omit; tone directives → adjust writing
   style accordingly.
4. Resume-specific preferences take precedence over global if they conflict.
5. When a preference conflicts with job-description tailoring (step 5),
   the preference wins — it reflects the user's deliberate intent.

If `preferences.md` does not exist, proceed with default behavior.

### 4. Analyze the Target Role

This is the strategic foundation — do this before writing a single bullet.

Consult `${CLAUDE_PLUGIN_ROOT}/skills/resume-generate/references/resume-conventions.md`
for formatting rules, tailoring strategy, and ATS optimization guidelines.

**When a job description is provided:**

1. **Decompose the JD** — Extract:
   - Required hard skills and tools (exact terms)
   - Desired experience level and domain
   - Key responsibilities (what the role does day-to-day)
   - Success signals (what "great" looks like in this role)
   - Cultural/soft skill signals (leadership, collaboration, autonomy)

2. **Map profile to requirements** — For each JD requirement, identify the
   strongest matching evidence from the profile. Some profile data will map to
   multiple requirements; some requirements may have no direct match. This
   mapping drives every subsequent decision.

3. **Identify the narrative angle** — What story does this resume tell? The
   user may be a backend engineer applying for a platform role, or a tech lead
   applying for an architect position. The angle determines which experiences
   to foreground and how to frame them.

**When a role description is provided** (e.g., "architect at Oracle", "senior
SRE at a startup"):

1. **Infer likely requirements** — Based on the role title, company type, and
   seniority level, determine what a hiring manager would expect: technical
   depth vs breadth, scale of systems, leadership scope, domain expertise.
   A "startup architect" values breadth and speed; an "Oracle architect" values
   enterprise scale and standards.

2. **Map and angle** — Same as JD-based flow above. The inferred requirements
   serve the same purpose as extracted JD requirements.

**When no target is provided:**

Build a general-purpose resume anchored to the user's most recent/senior role.
Use the profile's `title` and `summary` to infer the target identity. Prioritize:
- Recent roles with the most quantifiable impact
- Skills that define their professional identity
- Achievements that demonstrate progression and scope

### 5. Craft the Resume Content

This is where raw profile data becomes a persuasion document.

**TBD filtering:** Profile data may contain `TBD` as a placeholder value in
any field (indicating data not yet filled in by the user). Silently skip any
value that is exactly `TBD`. If all items in a list are `TBD`, omit that
list/block entirely.

#### Professional Summary

Do not copy the profile's `summary` field verbatim. Construct a 2-3 sentence
summary that:
- Opens with a role-aligned identity statement (e.g., "Platform engineer with
  12 years building distributed systems at scale")
- Highlights 2-3 differentiators most relevant to the target role
- Closes with a scope/impact signal (team size, system scale, business outcome)

Draw from `summary.json`, `experience.json` (recent role highlights), and
`skills.json` to compose this — not from any single source.

**Tool/framework attribution**: When mentioning specific tools or frameworks in
the summary, verify which projects actually used them by checking the `tech_stack`
of individual projects — not the role-level `tech_stack`. A role may list many
technologies across all its projects, but specific claims (e.g., "leveraging X
to deliver Y") must match the project where Y actually happened. Misattributing
tools to the wrong achievements is a content fidelity violation.

#### Experience Bullets

The profile nests `contributions` and `impact` under `experience[].projects[]`.
Transforming this nested structure into flat, high-impact resume bullets is the
most important part of resume generation.

For each role to include:

1. **Collect raw material** — Gather all `contributions` and `impact` items
   from the role's `projects[]`, plus any top-level `description` bullets.
   This is the candidate pool, not the final list.

2. **Score for relevance** — Rate each bullet against the JD requirements
   mapping from step 4. Bullets that directly address a JD requirement score
   highest. Bullets with quantifiable impact score next. Generic responsibility
   statements score lowest.

3. **Combine contribution + impact** — Where a contribution and its
   corresponding impact naturally pair, fuse them into a single bullet
   (e.g., "Architected event-driven pipeline processing 2M events/day,
   reducing end-to-end latency by 40%"). A combined bullet is stronger than
   two separate ones.

4. **Reframe for the target role** — Adjust framing to speak the JD's
   language. If the JD emphasizes "scalability" and the source says "handled
   increased load", reframe to "scaled system to handle 10x traffic growth."
   Reframing means choosing the right lens — never fabricate or exaggerate.

5. **Select and order** — Pick 3-5 strongest bullets per role. Lead with the
   most impressive. Recent roles get more bullets; older roles get fewer.
   For a 1-2 page resume, total experience bullets across all roles should
   be roughly 12-20.

6. **Cut roles that don't contribute** — If a role adds nothing relevant to
   the target position, omit it entirely. A gap in employment history is
   better than a filler role that dilutes the narrative.

#### Skills Section

Do not flatten all profile skill categories into the resume unchanged.

1. **Select for relevance** — Include skills that match JD requirements first,
   then skills that support the narrative angle, then notable adjacent skills.
   Omit skills that are irrelevant to the target role.
2. **Match JD terminology** — Use the exact terms from the JD where they
   refer to the same skill (e.g., if JD says "Kubernetes" don't write "K8s").
3. **Group strategically** — Group by what makes sense for the target role
   (e.g., "Cloud & Infrastructure", "Languages", "Data & ML"), not necessarily
   by how the profile categorizes them.
4. **Order within groups** — Most relevant skills first within each group.

#### Other Sections

- **Education**: Include degrees. Keep minimal unless education is a JD
  requirement (e.g., "PhD required").
- **Certifications**: Include only those relevant to the target role.
  Prioritize certifications the JD mentions or implies.
- **Open Source**: Default to including when the target role values hands-on
  building — startups, IC architect roles, platform engineering, developer
  tools. Open source projects signal a builder who ships beyond their day job.
  Omit only when space is tight and the projects add no relevant signal (e.g.,
  applying for a pure management role, or the projects are in unrelated tech).
  When included, add a brief "Open Source" or "Projects" section after
  Experience with project name, one-line description, and tech stack.
- **Patents**: Include if relevant to the role or domain. De-emphasize if
  the user's preferences say so.
- **Languages**: Include if the role involves international work or the JD
  mentions language requirements.

#### ATS Optimization

Consult `${CLAUDE_PLUGIN_ROOT}/skills/resume-generate/references/resume-conventions.md`
(the "ATS Optimization" section) for full formatting rules, keyword strategy,
and keyword gap analysis steps.

Key points: use standard section headings, plain formatting (no tables/columns),
spell out acronyms on first use, consistent "Mon YYYY" dates, and run a keyword
gap analysis against the JD to weave in missing terms the user genuinely
possesses. When no JD is provided, still apply formatting and acronym rules.

### 6. Generate Markdown Resume

`resume.md` is the primary deliverable — designed for direct conversion to PDF
for immediate use. Formatting quality matters as much as content quality because
the user may convert this to PDF and submit it within minutes.

Write the resume to `resume.md` following these formatting rules:

#### Layout Structure

```
# Full Name

Contact line (email | phone | location | links)

---

## Professional Summary

2-3 sentence constructed summary.

## Skills

Grouped skill lines: **Category:** Skill1, Skill2, Skill3

## Experience

### Job Title
**Company** | Location | Mon YYYY - Mon YYYY

- Achievement bullet
- Achievement bullet

### Job Title
**Company** | Location | Mon YYYY - Present

- Achievement bullet

## Education

**Degree**, Field — Institution, YYYY

## Certifications

Name — Issuer, YYYY
```

#### Formatting Rules

- **Header**: `# Full Name` as the document title. Contact info on a single
  line below, separated by ` | `. Include email, phone (if available),
  location, and profile URLs (LinkedIn, GitHub). Use a horizontal rule `---`
  to separate the header from the body.
- **Section headings**: `## Section Name` for main sections. Use the standard
  headings: Professional Summary, Skills, Experience, Education, Certifications.
- **Experience entries**: `### Job Title` as sub-heading, with company, location,
  and dates on the line below in bold/pipe format. Bullets beneath as `-` items.
- **Skill groups**: Bold category name followed by colon and comma-separated
  skills on a single line. One line per category. No nested bullets. Separate
  each category line with a blank line so Markdown renders them as distinct
  lines — without blank lines, consecutive lines collapse into a single
  paragraph.
- **Education**: Compact — degree, field, institution, and year on one or two
  lines. No bullets unless there are notable achievements to list.
- **White space**: One blank line between sections. No extra blank lines within
  sections. Dense but readable.
- **No personal pronouns**: Never "I", "my", "we".
- **Tense**: Past tense for previous roles, present tense for current role.
- **Action verbs**: Every experience bullet starts with a strong action verb.
- **Length**: Match the user's requested page count. 1 page ≈ 400 words,
  2 pages ≈ 700-900 words. When the user says "2 page resume", use the full
  budget — don't produce a thin 1.5 page document.
- **No decorative elements**: No emoji, no Unicode symbols, no ASCII art.
  Plain Markdown that renders cleanly in any converter.

### 7. Generate JSON Resume (always — unless user explicitly declines)

Also write a `resume.json` file in the [JSON Resume](https://jsonresume.org/schema)
open standard format. This is a secondary output for users who want to import
into Reactive Resume or other resume builder tools for further visual polish.

Consult `${CLAUDE_PLUGIN_ROOT}/skills/resume-generate/references/json-resume-schema.md`
for the complete field mapping from profile data to JSON Resume fields. That
reference covers all sections (basics, work, education, skills, certificates,
publications/patents, languages, projects), date formats, and which sections
to omit.

Key rules:
- Map the **tailored** content (not raw profile data) — the JSON Resume must
  match `resume.md` exactly: same bullets, same summary, same skill ordering.
- Omit empty sections entirely (no empty arrays).
- Patents map to `publications` (closest semantic fit in JSON Resume schema).

### 8. Verify Before Writing

Before writing output, run these checks and revise content if any fail:

**Content fidelity** — For every quantified claim, verify it exists in the
source profile data. For every achievement that was qualified in the source
(projected, expected, targeted, estimated, almost), confirm the qualifier is
preserved — do not present projections as delivered results. For every action
verb, confirm it matches the actual contribution scope — "designed" should not
become "delivered", "helped develop" should not become "built." For every
tool or framework mentioned in connection with a specific achievement, verify
it appears in that project's `tech_stack` — not just the role's top-level
tech stack or a different project within the same role.

**Preferences compliance** — Re-read the applicable preferences and verify each
one is reflected in the generated content. If any preference was missed or
contradicted, revise before proceeding.

**Narrative coherence** — Read the resume top to bottom. Does it tell a coherent
story about why this person is a strong fit? Are there jarring jumps, redundant
bullets, or sections that feel disconnected from the target role?

### 9. Present to User

Confirm files written and summarize what was generated:
- `resume.md` — PDF-ready, convert with any Markdown-to-PDF tool
- `resume.json` — importable into [Reactive Resume](https://rxresu.me/) or
  other JSON Resume compatible tools for visual formatting

Provide a brief summary: roles included, word count, and tailoring strategy
(which JD requirements were addressed, which profile strengths were
foregrounded, and any JD requirements with no matching profile evidence).
Do not dump the full resume into the conversation — the user can read the
files directly. Show content inline only if the user asks to see it.

## Output Checklist

Before finishing, verify:

- [ ] Resume tells a coherent story about fit for the target role (not a data dump)
- [ ] Resume is tailored to the JD or role description (if provided)
- [ ] Professional summary was constructed (not copied from summary.json)
- [ ] Experience bullets were selected by relevance and impact (not all bullets included)
- [ ] Skills were curated for the target role (not a full flatten of profile categories)
- [ ] ATS optimization applied (standard headings, plain formatting, keywords present)
- [ ] All content is factual — sourced from the master profile, not fabricated
- [ ] Source qualifiers preserved (projected/expected/targeted/estimated/almost)
- [ ] Action verbs match actual contribution scope — no inflation
- [ ] Length matches requested page count (1 page ≈ 400 words, 2 pages ≈ 700-900 words)
- [ ] `resume.md` formatting is PDF-ready (proper header, sections, spacing, no decorative elements)
- [ ] `resume.json` written, matches `resume.md` content, and conforms to JSON Resume schema
- [ ] Output honors all applicable presentation preferences (global + resume-specific)

## Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/skills/resume-generate/references/resume-conventions.md`** — Length rules, section order, tailoring strategy, ATS guidelines
- **`${CLAUDE_PLUGIN_ROOT}/skills/resume-generate/references/json-resume-schema.md`** — JSON Resume schema field mapping

---
name: resume-generate
description: >-
  This skill generates an honest, well-organized resume from the user's profile
  data, drawing on all available sections. Use when the user asks to "generate
  a resume", "create a resume", "build a resume for this job", "make a resume
  from my profile", "make an ATS-optimized resume", "generate resume JSON",
  "create a CV", "write my curriculum vitae", "prepare a job application",
  "update my resume", "shorten my resume", "resume for [company]", or wants a
  polished resume document produced from their profile data. Also trigger when
  the user provides a job description or job link and asks to apply, prepare
  application materials, or just says "resume for this". Trigger for any resume
  editing, refinement, or regeneration request — not just first-time generation.
---

# Resume Generate

Generate an honest, well-organized resume from the user's profile data. The
resume reflects who the candidate actually is — not a version reshaped to mirror
a job description. A job description, when provided, informs which true things
to surface first; it does not change what is true.

**Resume is not a cover letter.** A cover letter argues fit by speaking directly
to a JD's language and priorities. A resume is a factual record of the
candidate's career that the reader can trust. Customization that makes the
resume read as written-for-this-JD undermines that trust. When tailoring would
require reframing the candidate's identity, restructuring their narrative around
JD keywords, or making the resume look bespoke for one role, do not do it.

The primary output is `resume.md` — a PDF-ready Markdown document. Also
generates `resume.json` in the [JSON Resume](https://jsonresume.org/schema)
open standard for import into Reactive Resume or compatible tools. For
LinkedIn-specific content formatting, use the `linkedin-generate` skill
instead.

## Core Philosophy

The profile sections are the source of truth — a comprehensive record of the
candidate's career across identity, summary, experience, skills, education,
certifications, open source, patents, blogs, and languages. The resume is a
condensed, well-ordered view of that record, drawing on **all** relevant
sections rather than only experience and skills.

A JD (when provided) is used for two things only:
- **Selection** — which true achievements, projects, and skills to surface
  given the role's focus
- **Ordering** — which to lead with so the most relevant evidence is easy to find

A JD is **not** used to:
- Reframe contributions in JD-specific language
- Inflate the role of a tool, technology, or domain beyond its real share
  of the candidate's work
- Reshape the candidate's identity around the role
- Insert keywords that don't reflect genuine experience

The honesty test: if the same candidate applied to a different but plausible
role, the resume should still read as a faithful representation of them — not
as a different document constructed for a different job. If a tailoring choice
would fail that test, do not make it. When in doubt, prefer the version that
reads as the candidate's own resume rather than one written for a JD.

A 20-year career with 8 roles and 30 projects might produce a resume with all
8 roles listed but only 12-18 bullets across them — recent and relevant roles
get more, older or less-relevant roles get one or two. The craft is in
choosing which bullets — using the candidate's own words and framing — not in
rewriting them to echo a JD.

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

If `resume.md` already exists, always regenerate from profile sections —
selection should start from the full data pool, not from a previously narrowed
resume. The existing file will be overwritten.

Read `profile-index.json` to discover available sections and their file paths.
Then read the relevant section JSON files from `sections/`. Parse each JSON file
and access fields directly from the `data` object.

If required section JSON files do not exist, inform the user and suggest running
`/profile-init` or `/profile-section` to generate them. At minimum, read:

- `sections/identity.json` — name, contact info
- `sections/summary.json` — professional bio
- `sections/experience.json` — work history
- `sections/skills.json` — technical and soft skills
- `sections/education.json` — degrees

Also read certifications, open source, patents, blogs, and languages if they
exist in the index. **Read all available sections by default** — a resume that
ignores half the candidate's profile under-represents them. Decide what to
include based on space and relevance, but the decision should be informed by
having seen everything.

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

2. **Map profile to requirements honestly** — For each JD requirement, identify
   the strongest **genuine** matching evidence from the profile. Some
   requirements will have strong matches, some weak, some none. Record this
   honestly — do not invent matches. Requirements with no honest match stay
   unmatched; the resume does not paper over the gap.

3. **Decide selection and ordering, not reframing** — The mapping informs which
   real experiences to surface and in what order. It does **not** authorize
   rewriting bullets to echo JD language, restructuring the candidate's
   identity, or promoting a minor skill to a defining one. If the candidate's
   actual narrative does not naturally align with the JD, the right answer is
   often a thinner match — not a manufactured one.

**When a role description is provided** (e.g., "architect at Oracle", "senior
SRE at a startup"):

1. **Infer likely requirements** — Based on the role title, company type, and
   seniority level, determine what a hiring manager would expect: technical
   depth vs breadth, scale of systems, leadership scope, domain expertise.
   A "startup architect" values breadth and speed; an "Oracle architect" values
   enterprise scale and standards.

2. **Map honestly, then select and order** — Same as the JD-based flow above:
   match real evidence to inferred requirements, leave honest gaps visible,
   and use the result for selection and ordering only.

**When no target is provided:**

Build a general-purpose resume anchored to the user's most recent/senior role.
Use the profile's `title` and `summary` to infer the target identity. Prioritize:
- Recent roles with the most quantifiable impact
- Skills that define their professional identity
- Achievements that demonstrate progression and scope

### 5. Craft the Resume Content

This step turns the curated material into the resume. Two principles govern
every decision:

**Proportional emphasis.** A tool or skill that appears in a small fraction
of the candidate's foregrounded projects (roughly under a third) belongs in
the skills list and in the bullets where it actually applied — not in the
summary's identity statement or as the lead of the first skill group, even
if the JD names it. When matching evidence is thin, leave the gap visible.

**Use the candidate's own words.** Bullets, summary lines, and skill names
should sound like the candidate. Light editing for clarity, brevity, or
active voice is fine. Wholesale rewording to match JD vocabulary is the
signature of a tailored resume and erodes credibility.

**TBD filtering.** Profile data may contain `TBD` as a placeholder value.
Silently skip any value that is exactly `TBD`. If all items in a list are
`TBD`, omit that list/block entirely.

#### Professional Summary

Construct a 2-3 sentence summary grounded in the candidate's actual identity
from `summary.json`. The summary should:
- Open with the candidate's real identity (their actual title, years, and
  domain) — not a JD-aligned identity. If the candidate is a backend engineer
  applying to a platform role, the summary still describes a backend engineer
  whose work is relevant to platform problems — not a "platform engineer."
- Highlight 2-3 genuine differentiators. When a JD is provided, prefer
  differentiators that happen to be JD-relevant *and* truly central to the
  candidate. Do not promote a minor capability to a differentiator just
  because the JD asks for it.
- Close with a real scope/impact signal (team size, system scale, business
  outcome) drawn from the profile.

Draw from `summary.json`, `experience.json` (recent role highlights), and
`skills.json` to compose this — staying close to the candidate's own framing.
Light editing for length and flow is fine; do not rewrite the candidate's
identity statement to match a JD.

**Tool/framework attribution**: When mentioning specific tools or frameworks in
the summary, prefer the project-level `skills` field (what the person personally
applied) over the project-level `tech_stack` (what the whole team used). If
`skills` is present, use it as the authoritative signal for personal
attribution. If absent, fall back to the project's `tech_stack`. Specific claims (e.g., "leveraging X to
deliver Y") must match the project where Y actually happened — not a different
project within the same role. Misattributing tools to the wrong achievements is
a content fidelity violation.

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

4. **Edit lightly, do not reframe** — Tighten bullets for clarity, brevity, and
   active voice. Preserve the candidate's own terminology and framing. Do not
   substitute JD vocabulary for the candidate's vocabulary unless the two
   genuinely refer to the same thing in the candidate's domain (e.g., "K8s"
   and "Kubernetes" are interchangeable; "handled increased load" and
   "architected for scalability" are not). When a quantifiable impact is
   already present in the source, lead with it; do not invent or estimate
   numbers that aren't there.

5. **Select and order** — Recent or directly relevant roles get 3-5 of their
   strongest bullets, leading with the most impressive. Older or less
   relevant roles get 1-2. For a 1-2 page resume, total experience bullets
   across all roles should be roughly 12-20.

6. **Keep employment continuity; trim the bullets, not the role** — If a role
   adds little to the target position, keep the role line (title, company,
   dates) and reduce it to one or two bullets rather than dropping it.
   Silently omitting a role creates an apparent employment gap, which on an
   honest resume looks worse than a thin entry. Only drop very early or
   short roles that the candidate has already pruned from their own profile
   narrative.

#### Skills Section

`skills.json` is the source of truth — it is the candidate's curated record
of what they have actually worked on. Project `tech_stack` lists in
`experience.json` describe the whole project's stack and may include
technologies the candidate did not personally use, so do **not** pull from
`tech_stack` into the Skills section.

1. **Start from `skills.json`** — Use its categories and items as the
   complete pool. Do not introduce skills from elsewhere.

2. **Curate within categories, don't drop categories** — Within each
   category, drop only items that are genuinely obsolete and would not be
   claimed today (e.g., Active Server Pages from 20 years ago) or items
   irrelevant to any plausible reading of the candidate's current
   profession.

   Do **not** drop entire categories just because a JD doesn't emphasize
   them. For an architect or engineer, categories like Databases, Messaging,
   Monitoring, Build & Testing, and Application Servers are part of the
   professional baseline — omitting them under-represents the candidate and
   makes the resume read as JD-shaped. A category is dropped only when it
   is genuinely outside the candidate's domain (rare).

3. **Use canonical terminology** — Where the JD and the profile refer to
   the same skill with different names, use the canonical industry term
   (e.g., "Kubernetes" rather than "K8s"). Do not substitute a JD-specific
   phrase for a skill the candidate would not naturally describe that way.

4. **Order within and across groups** — Within each group, list the
   strongest or most relevant items first. When a JD is provided, the most
   JD-relevant group can lead; otherwise default to the candidate's
   `skills.json` order.

#### Other Sections

- **Education**: Include degrees. Keep minimal unless education is a JD
  requirement (e.g., "PhD required").
- **Certifications**: Include those relevant to the target role; prioritize
  ones the JD mentions or implies. Drop certifications that have nothing to
  do with the role.
- **Open Source**: Default to including when the target role values hands-on
  building — startups, IC architect roles, platform engineering, developer
  tools. Omit only when space is tight and the projects add no relevant
  signal. When included, add a brief "Open Source" or "Projects" section
  after Experience with project name, one-line description, and tech stack.
- **Patents**: Include if relevant to the role or domain. De-emphasize if
  the user's preferences say so.
- **Blogs / Publications**: Include a short section when blog posts or
  technical articles demonstrate domain expertise relevant to the role
  (e.g., a backend candidate's distributed-systems writing). List 2-4 of
  the most relevant pieces with title and venue. Omit when nothing matches.
- **Languages**: Include if the role involves international work or the JD
  mentions language requirements.

#### ATS Optimization

Consult `${CLAUDE_PLUGIN_ROOT}/skills/resume-generate/references/resume-conventions.md`
(the "ATS Optimization" section) for full formatting rules, keyword strategy,
and keyword gap analysis steps.

Key points: use standard section headings, plain formatting (no tables/columns),
spell out acronyms on first use, consistent "Mon YYYY" dates. When a JD is
provided, run a keyword gap analysis and weave in only the missing terms the
candidate **genuinely possesses** — never insert keywords for skills the
candidate does not actually have. A keyword the candidate cannot defend in an
interview is a liability, not an optimization. When no JD is provided, still
apply formatting and acronym rules.

### 6. Generate Markdown Resume

`resume.md` is the primary deliverable — designed for direct conversion to PDF
for immediate use. Formatting quality matters as much as content quality because
the user may convert this to PDF and submit it within minutes.

Write the resume to `resume.md` following the layout structure and formatting
rules in the "Markdown Layout (resume.md)" section of
`${CLAUDE_PLUGIN_ROOT}/skills/resume-generate/references/resume-conventions.md`.
Read that section before writing the file — it defines the exact header block,
section heading set, experience entry format, and skill-group formatting.
The rules most often gotten wrong, worth restating here:

- **Skill groups**: one line per category ending with a backslash (`\`)
  continuation, no blank lines between categories (blank lines create visible
  gaps in PDF output). No trailing `\` on the last line.
- **Header**: `# Full Name`, then `email | location`, then a profile-links
  line with bare domain+path as link text, then `---`.
- **Length**: match the requested page count — 1 page ≈ 400 words, 2 pages
  ≈ 700-900 words. Use the full budget; don't produce a thin document.
- **No personal pronouns, no decorative elements**; past tense for previous
  roles, present for the current one; every bullet starts with an action verb.

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
- Map the **selected** content — the JSON Resume must match `resume.md`
  exactly: same bullets, same summary, same skill ordering.
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
it appears in that project's `skills` or `tech_stack` — not a different project within the same role.

**Tailoring honesty test** — Re-read the resume imagining the candidate sent
it for a *different but plausible* role with no edits. Does it still read as
a faithful representation of the candidate? If it reads as obviously
written-for-one-JD (identity reshaped, JD vocabulary woven throughout, a
single tool dominating the summary, claims that strain credibility), the
tailoring has gone too far. Pull back: restore the candidate's natural
framing, demote over-promoted skills, remove inserted JD keywords that don't
reflect genuine experience.

**Section coverage** — Confirm the resume draws on all relevant sections
available in the profile, not just experience and skills. Education,
certifications, open source, patents, and languages should be considered
and included where they add real signal.

**Proportional emphasis** — For each tool foregrounded in the summary's
identity statement or as the lead of the first skill group, count the
projects in the foregrounded roles where it actually appears. If under
roughly a third, demote it: keep it in the skills list and in the bullets
where it applied, but pull it out of the summary/lead position. The rule
governs anchoring, not inclusion — a minority-share tool still belongs
wherever it was genuinely used.

**Preferences compliance** — Re-read the applicable preferences and verify each
one is reflected in the generated content. If any preference was missed or
contradicted, revise before proceeding.

**Narrative coherence** — Read the resume top to bottom. Does it read as a
coherent professional record? Are there jarring jumps, redundant bullets, or
formatting inconsistencies? The goal is a clear, honest read — not a
JD-shaped argument.

### 9. Present to User

Confirm files written and summarize what was generated:
- `resume.md` — PDF-ready, convert with any Markdown-to-PDF tool
- `resume.json` — importable into [Reactive Resume](https://rxresu.me/) or
  other JSON Resume compatible tools for visual formatting

Provide a brief summary: roles included, word count, and (if a JD was
provided) which profile strengths were foregrounded and which JD
requirements have no matching profile evidence. Do not dump the full resume
into the conversation — the user can read the files directly. Show content
inline only if the user asks to see it.

## Output Checklist

Before finishing, verify:

- [ ] Reads as the candidate's own resume — would still feel honest if sent for a different but plausible role
- [ ] All available profile sections were considered (experience, skills, education, certifications, open source, patents, blogs, languages); included where they add real signal
- [ ] JD use (if any) limited to selection and ordering — no JD-driven reframing of identity, bullets, or skill names
- [ ] Summary uses the candidate's real identity; bullets use the candidate's own language with light editing only
- [ ] Skills include only what the candidate genuinely has — no inserted JD keywords for missing skills
- [ ] Foregrounded skills/tools reflect their real share of the candidate's work
- [ ] Source qualifiers preserved (projected/expected/targeted/estimated/almost); action verbs match actual contribution scope
- [ ] Employment continuity preserved — no silent role drops creating apparent gaps
- [ ] ATS-clean: standard headings, plain formatting, consistent "Mon YYYY" dates, no decorative elements
- [ ] Length matches requested page count (1 page ≈ 400 words, 2 pages ≈ 700-900 words)
- [ ] `resume.json` matches `resume.md` content and conforms to JSON Resume schema
- [ ] Output honors all applicable presentation preferences (global + resume-specific)

## Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/skills/resume-generate/references/resume-conventions.md`** — Length rules, section order, tailoring strategy, ATS guidelines
- **`${CLAUDE_PLUGIN_ROOT}/skills/resume-generate/references/json-resume-schema.md`** — JSON Resume schema field mapping

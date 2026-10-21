---
name: linkedin-generate
description: >
  This skill generates copy-paste-ready LinkedIn profile content from the master
  profile data. Use when the user asks to "generate LinkedIn content", "export
  profile for LinkedIn", "create LinkedIn-ready content", "format my experience
  for LinkedIn", "write my LinkedIn headline", "generate LinkedIn about section",
  "prepare LinkedIn update", "optimize my LinkedIn", "LinkedIn makeover",
  "what should my LinkedIn say", "prepare for LinkedIn", "update my LinkedIn",
  or wants any content formatted for LinkedIn's field constraints. Also trigger
  when the user mentions LinkedIn in the context of profile updates, job searching,
  or professional branding — even if they don't say "generate". For assessing
  the quality of the user's live LinkedIn profile and suggesting improvements,
  use the `linkedin-review` skill instead.
---

# LinkedIn Generate

Generate copy-paste-ready content for LinkedIn profile sections, formatted
to LinkedIn's character limits and plain-text constraints.

## Core Philosophy

LinkedIn is both a positioning platform and a professional network. The master
profile is a comprehensive datastore; LinkedIn content should create a clear
professional identity while preserving the networking value of the full career
history. Every field — from headline to skills list — should be constructed
strategically, not reformatted from the profile. A headline is not a trimmed
title. An About is not a restated summary. A skills list is not a category
flatten. Each field has a strategic job to do.

**Positioning vs. networking tradeoff** — Some fields (headline, about, skills)
are pure positioning: curate aggressively. But experience entries also serve a
networking function — former colleagues search by company name to reconnect, and
organization names improve discoverability. This means LinkedIn should include
all roles from the profile, even early-career ones, while adjusting the depth
of description by seniority (see Experience section). A resume also keeps role
lines for continuity, but it trims hard for one target. LinkedIn serves every
future searcher, so its entries can carry more of the career.

## Workflow

### 1. Determine Scope

Ask or infer what the user needs:

- **Full export**: generate all LinkedIn sections
- **Single section**: e.g., "format my experience at Company X for LinkedIn"
- **Specific field**: e.g., "write me a LinkedIn headline"

#### What to read for each scope

Full export requires all section files. For single-field requests, Claude still
needs context beyond the obvious source — the headline strategy draws from
title, summary, *and* experience. Here's the minimum read set for common
single-field requests:

| Request | Minimum sections to read |
|---------|--------------------------|
| Headline | identity, summary, experience, skills |
| About | identity, summary, experience, open-source (if central to identity) |
| Experience (one entry) | experience (target entry), skills |
| Experience (all) | experience, skills |
| Skills | identity, summary, experience, skills |
| Education | education |
| Certifications | certifications |
| Patents | patents |
| Languages | languages |

### 2. Read Profile Sections

Read the relevant profile section JSON files from `sections/`. Consult
`profile-index.json` to discover available sections and their file paths.
Parse each JSON file and access fields directly from the `data` object.
For example: `data.full_name` from `sections/identity.json`,
`data.experience` array from `sections/experience.json`.

If required section JSON files do not exist, inform the user and suggest
running `/profile-init` or `/profile-section` to generate them.

### 3. Apply Presentation Preferences

Read `preferences.md` from the workspace root. If it exists:

1. Read the `## Global` section — these apply to all exports.
2. Read the `## LinkedIn` section (if present) — these are LinkedIn-specific.
3. Treat each preference as a binding directive during content transformation.
   Examples: "present experience as 20+ years" → use that framing; "don't
   highlight patents" → de-emphasize or omit; tone directives → adjust writing
   style accordingly.
4. LinkedIn-specific preferences take precedence over global if they conflict.

If `preferences.md` does not exist, proceed with default behavior.

### 4. Apply LinkedIn Constraints

Consult `${CLAUDE_PLUGIN_ROOT}/skills/linkedin-generate/references/linkedin-constraints.md` for:

- Character limits per field
- Formatting rules (plain text, no Markdown, bullet character `•`)
- Section mapping (which profile fields map to which LinkedIn fields)
- Best practices for content optimization

### 5. Transform Content

This is where profile data becomes LinkedIn positioning. Two principles govern
every transformation:

**Content fidelity** — LinkedIn content must be accurate to the source data.
If an impact value is qualified in the source (e.g., "projected", "expected",
"targeted", "estimated", "almost"), retain that qualifier. Use the verb that
reflects what the person actually did — "designed", "co-developed", "led
architecture for" — not an inflated verb that implies sole ownership or
completed delivery. This matters because recruiters and hiring managers will
ask about these claims in interviews; inflated content creates a credibility
gap the user has to close.

**TBD filtering** — Profile data may contain `TBD` as a placeholder value.
Silently skip any value that is exactly `TBD`. If all items in a list are
`TBD`, omit that list/block entirely.

For each target LinkedIn field:

- Write plain text. LinkedIn renders no Markdown, so use `•` for bullets.
- Track each field's character count. Step 7 records it in the file header.

#### Headline

Do not take the profile's `title` field and shorten it to 220 chars.
Construct the headline from `title`, `summary`, and the most distinctive
aspects of the user's experience. Apply the Headline Strategy from the
linkedin-constraints reference: choose a formula pattern, include 3-5
searchable keywords, lead with role or differentiator in the first ~60 chars.
Most strong headlines use a good share of the 220 chars. A bare title wastes
the most-viewed field on LinkedIn. If a draft comes in short, ask whether
another keyword or domain signal would help a searcher. If the short version
is already sharp and distinctive, keep it rather than padding it.

#### About

Do not restate `summary.json` in prose. Apply the About Strategy from the
linkedin-constraints reference: hook (first 2-3 lines must stand alone before
"see more"), body drawing from experience highlights and domain context,
optional distinctive positioning, and a concrete call to action. Pull
achievement highlights from `experience.json`, not just `summary.json`. A
substantial career usually fills most of the 2,600-char budget, and a thin
About is a missed opportunity. Stop when the story is told, and do not pad to
reach a count. Respect any length or tone preference the user has set.

#### Experience

**Include every role from the profile.** Unlike resumes, LinkedIn serves a
networking purpose — former colleagues find each other by searching company
names. Dropping a role means losing that reconnection path. This is especially
true for well-known organizations or roles where meaningful work was done,
regardless of seniority level.

**Coverage.** Every project with quantifiable impact, business results,
international exposure, or methodology significance should be visible in its
role's entry. Lower-signal projects can share a bullet (e.g., "Designed
services integration layers for financial systems including the Child Trust
Fund and GFAS"). As a rough guide, a role usually needs about one bullet per
two projects. Use that figure to catch an under-covered role, not as a quota
to meet. The role-level `description` bullets are part of the raw material
too. They hold work that belongs to no single project.

**Character budget**: LinkedIn allows 2,000 chars per entry. A short entry
that leaves notable projects unrepresented usually means something was
skipped. Check it before moving on. A short entry for a short or early role
is fine.

For each experience entry:

1. **Flatten** — LinkedIn has no nested project structure. Take the role's
   `description` bullets, plus the best `contributions` and `impact` items
   from each project in `projects[]`, and convert them into flat bullets. Combine contribution + impact into a single
   concise bullet where it reads naturally (e.g., "Designed X, targeting Y%
   improvement"). Multiple lower-impact projects can share a bullet (e.g.,
   "Designed services integration layers for financial systems including the
   Child Trust Fund and Global Fund Administration System"). When attributing
   specific tools or frameworks to an achievement, prefer the project's
   `skills` field (what the person personally applied) over its `tech_stack`
   (what the whole team used). If `skills` is absent, fall back to
   `tech_stack`. This applies to **every role** including early-career
   entries — do not skip the flatten step for any role.
2. **Check coverage** — Check that every notable project shows up in the
   output. Add a bullet for any that is missing, or merge it into an existing
   bullet.
3. **Order** — Sort the resulting bullets by impact, most impressive first.
   Do not preserve the source order. `impact` bullets (quantifiable outcomes)
   generally rank higher than `contributions` bullets.
4. **Fit to budget** — The hard cap is 2,000 chars per entry. Condense
   bullets as needed to fit, but do not drop projects to meet the cap —
   shorten wording instead.

#### Skills

Do not flatten all skills from the profile into the output unchanged. Instead:

1. Identify the user's professional identity from their title, summary, and
   most recent/senior experience. Use this to anchor slot 1-5 choices.
2. Apply the Skills Strategy from the linkedin-constraints reference: order by
   role-defining → core domain → adjacent → soft/leadership. Drop skills that
   are obscure, redundant, or unlikely to be searched by recruiters. Do not
   over-prune named tools that recruiters actively search for, such as
   current AI development tools. Judge searchability by today's market, not
   by whether a tool feels like "just a tool". Likewise, a soft skill that is
   a genuine differentiator in the user's domain is not generic.
3. Normalize each skill name to the canonical LinkedIn/industry term
   (e.g., "Machine Learning" not "ML", "Node.js" not "NodeJS").
4. Deduplicate across profile categories before ordering.
5. LinkedIn allows up to 100 skills. Fill only as many slots as stay
   high-signal. A sharp list of 30–50 usually beats an exhaustive 100.
6. Briefly note the curation rationale (e.g., "Prioritized X, Y, Z as
   role-defining; dropped [obscure tool] as low recruiter search value") so
   the user understands the choices and can override if needed.

#### Education

For each education entry: map degree, field of study, institution, and
graduation year to LinkedIn's education fields. Keep it straightforward — no
embellishment beyond what the profile data contains. Include activities or
honors only if present in the source data.

#### Certifications

Include each certification with name, issuing organization, and year. If the
certification has an `id` (credential number), map it to LinkedIn's
Credential ID field; if it has a verification URL, map it to the Credential
URL field. Order by relevance to the user's current professional identity,
not chronologically.

#### Patents

Map each patent to LinkedIn's patent fields: title, patent number, status,
filing/grant dates, co-inventors. Include the abstract as the description.
Respect user preferences — if preferences say to de-emphasize patents, generate
the file but note this to the user.

#### Open Source Projects

Map notable open source projects to LinkedIn's Projects section. Include
project name, a one-line description, and URL. For projects where the user
has significant contributions or impact metrics, include a brief description
highlighting those.

#### Languages

Map each language entry directly. LinkedIn uses a proficiency picker
(Native, Professional working, etc.), so note the closest LinkedIn proficiency
level alongside each language.

### 6. Verify Before Writing

Before writing output, run two checks and revise content if either fails:

**Content fidelity spot-check** — Scan every quantified claim and action verb
in the output. Do any verbs overstate the source? Are any qualifiers dropped?
This is a fast pass against the principle stated in step 5 — not a re-read of
every rule, just a focused check on the areas most prone to drift.

**Preferences compliance** — Re-read the applicable preferences and verify each
one is reflected in the generated content. If any preference was missed or
contradicted, revise the content before proceeding.

### 7. Write Output

Write the formatted content to `linkedin/`. Create the directory if
it does not exist.

For a full export, generate these files:

- `linkedin/headline.md` — Headline (220 chars max)
- `linkedin/about.md` — About/Summary section
- `linkedin/experience.md` — All experience entries
- `linkedin/skills.md` — Curated skills list
- `linkedin/education.md` — Education entries
- `linkedin/certifications.md` — Certifications (if data exists)
- `linkedin/open-source.md` — Open source projects (if data exists)
- `linkedin/patents.md` — Patents (if data exists)
- `linkedin/languages.md` — Languages (if data exists)

For a single section or field, write only the relevant file.

Each file should include a header comment with the character limit and
current character count:

```
<!-- LinkedIn Headline | Limit: 220 chars | Used: 187 chars -->
```

### 8. Present to User

How to present depends on scope:

- **Single field or section**: Display the content inline so the user can
  review and copy-paste immediately.
- **Full export**: Summarize what was generated (list of files, character
  usage for constrained fields, skills curation rationale). Do not dump all
  9 files into the conversation — the user can read them directly. Show
  specific files inline only if the user asks.

For the skills section, always surface the curation rationale regardless
of scope — the user needs to understand and potentially override skill
choices.

## Output Checklist

Before finishing, verify:

- [ ] No Markdown formatting remains in output (no `**`, `##`, `- ` bullets)
- [ ] All fields are within LinkedIn's character limits
- [ ] Character counts are noted for each field
- [ ] Content written to `linkedin/`
- [ ] Headline was constructed from title + summary + experience (not just trimmed)
- [ ] About opens with a distinctive hook — not "I am a [title] with X years"
- [ ] Skills list was curated and ordered by impact, with rationale noted
- [ ] Source qualifiers and verb accuracy preserved (content fidelity)
- [ ] Output honors all applicable presentation preferences

## Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/skills/linkedin-generate/references/linkedin-constraints.md`** — Character limits, formatting rules, section mapping, and best practices

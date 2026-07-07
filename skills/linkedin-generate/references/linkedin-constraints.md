# LinkedIn Field Constraints

## Character Limits

| Field | Max Characters | Notes |
|-------|---------------|-------|
| Headline | 220 | Appears below name everywhere on LinkedIn |
| About / Summary | 2,600 | Supports line breaks, no Markdown |
| Job Title | 100 | Per experience entry |
| Company Name | 100 | Per experience entry |
| Job Description | 2,000 | Per experience entry, supports bullet points via copy-paste |
| Skills | 50 per skill | Up to 50 skills total, order matters (top 3 shown) |
| Education - Degree | 100 | e.g. "Bachelor of Science" |
| Education - Field of Study | 100 | e.g. "Computer Science" |
| Education - Activities | 500 | Optional |
| Certification Name | 255 | |
| Project Name | 255 | |
| Project Description | 2,000 | |
| Language Name | 100 | One entry per language; proficiency level selectable |

## Formatting Rules

- LinkedIn does NOT render Markdown. All formatting must be plain text.
- Line breaks are preserved when copy-pasted.
- Bullet points: use `•` (U+2022) or `▸` (U+25B8) characters, not Markdown `-`.
- Bold/italic: not supported in most fields. Use CAPS sparingly for emphasis.
- Links: paste full URLs; LinkedIn auto-links them in About and descriptions.
- Emojis: supported and commonly used in headlines and about sections.

## Section Mapping (Profile → LinkedIn)

| Profile Section | LinkedIn Field | Notes |
|----------------|----------------|-------|
| `sections/identity.json` → full_name | First Name + Last Name | Usually already set |
| `sections/identity.json` → title | Headline | Construct from title + summary + experience; see Headline Strategy |
| `sections/identity.json` → location | Location | City, Country format |
| `sections/summary.json` → summary | About | Construct narrative from summary + experience highlights; see About Strategy |
| `sections/experience.json` → each entry | Experience | One entry per role |
| `sections/education.json` → each entry | Education | One entry per degree |
| `sections/skills.json` → categories.items | Skills | Curate, prioritize by impact, and normalize; see Skills Strategy |
| `sections/certifications.json` → each entry | Licenses & Certifications | `id` → Credential ID field; `url` → Credential URL field |
| `sections/open-source.json` → projects | Projects | Map open_source.projects to LinkedIn Projects section |
| `sections/patents.json` → each entry | Patents | LinkedIn has a dedicated patents section |
| `sections/languages.json` → each entry | Languages | |

## Best Practices for LinkedIn Content

- **Headline**: Construct a positioning statement — not a trimmed job title. See Headline Strategy below.
- **About**: Write in first person with a narrative structure. Do not restate `summary.json`. See About Strategy below.
- **Experience descriptions**: Start each bullet with an accurate action verb that reflects the actual contribution scope (e.g., "designed", "led", "co-developed" — not inflated verbs like "secured" or "delivered" when the source says "designed" or "helped develop"). Quantify achievements where the source data includes numbers, but preserve any qualifiers from the source (e.g., "projected", "expected", "targeted", "estimated", "almost") — do not present estimates or projections as delivered results.
- **Skills**: Curate for impact and searchability — not a complete list. See Skills Strategy below.

## Skills Strategy for LinkedIn Impact

LinkedIn skills are not a data dump — they are a positioning tool. The goal is to
select and order skills that define the user's professional identity, match recruiter
and hiring manager search terms, and are likely to attract endorsements.

### Priority Ordering (within the 50-skill budget)

Order skills by professional impact, not by profile category:

1. **Role-defining skills** (slots 1–5): The 3–5 skills that most directly answer
   "what kind of professional is this person?" These become the user's visible
   identity on LinkedIn. Examples: "Machine Learning", "Product Management",
   "Cloud Architecture". These should come first.

2. **Core domain expertise** (slots 6–20): Deep technical or domain skills that
   substantiate the role identity. Typically the hard skills the user is known for.

3. **Adjacent and supporting skills** (slots 21–40): Broader skills, frameworks,
   platforms, and methodologies that round out the profile without diluting the
   core identity.

4. **Soft and leadership skills** (slots 41–50, optional): Only include if they
   are genuinely strong differentiators (e.g., "Team Leadership", "Executive
   Communication") — skip generic ones like "Teamwork" that add no signal.

### Name Normalization

Use the canonical LinkedIn / industry-standard name, not variations:

- Prefer "Node.js" over "NodeJS" or "node"
- Prefer "Machine Learning" over "ML"
- Prefer "Amazon Web Services (AWS)" or just "AWS" over "Amazon AWS"
- Prefer "React" over "ReactJS" or "React.js"
- Prefer "PostgreSQL" over "Postgres" or "PSQL"
- Match the exact casing and punctuation used by LinkedIn skill suggestions

### Curation Rules

- **50-slot budget is finite** — be selective. A shorter, sharper list beats an
  exhaustive dump. Drop obscure internal tools, project-specific codenames, and
  legacy technology unless it is genuinely still a key part of the user's work.
- **Favor searchable skills**: Recruiters search by well-known terms. An obscure
  skill that nobody searches for occupies a slot that a high-value skill could use.
- **Include AI development tools**: Vendor AI tools like Cursor, Amazon Q,
  Claude Code, and ChatGPT are increasingly searched by recruiters because they
  signal hands-on AI-augmented development capability. These belong in the
  adjacent/supporting tier, not dropped as "usage tools."
- **Avoid redundancy**: Don't add both "JavaScript" and "ES6" — pick the canonical
  one. Don't add both "AWS" and "Amazon EC2", "Amazon S3" unless slots permit.
- **Recency signal**: Skills from recent roles and projects carry more credibility
  than skills last used years ago. Prefer current expertise over historical breadth.
- **De-duplicate across profile categories**: The profile may organize skills into
  categories (Languages, Frameworks, Cloud, etc.). Flatten and deduplicate before
  ordering — the category structure is irrelevant on LinkedIn.

## Headline Strategy for LinkedIn Impact

The headline is the most-viewed field on LinkedIn — it appears in search results,
connection requests, comments, and the sidebar. A job title alone wastes this space.
The headline must be a constructed positioning statement, not a trimmed title field.

### What a Headline Must Do

1. Identify the role (so recruiters and peers know what you are)
2. Signal the differentiator (what sets you apart from others with the same title)
3. Include searchable keywords (LinkedIn's search indexes the headline heavily)

### Formula Patterns (choose the best fit for the user's profile)

**Role + Differentiator + Keywords**
`Staff Engineer | Distributed Systems & ML Infrastructure | Reliability at Scale`

**Role + Who You Help + Domain**
`Engineering Manager | Helping teams ship AI products | Platform & ML Infra`

**Keyword-dense with separators**
`Cloud Architect • AWS • Kubernetes • FinTech | Building secure, scalable infra`

**Outcome-first (for senior / leadership profiles)**
`Turning research into production ML | Principal Engineer | LLMs & Data Platforms`

### Construction Rules

- Do not just trim the profile's `title` field to 220 chars — that produces a
  title, not a headline. Construct the headline from `title` + `summary` + the
  most distinctive aspects of the user's experience.
- Use separator characters (`|`, `•`, `–`) to create scannable visual chunks.
- The first ~60 chars matter most — they are visible before truncation on mobile.
  Lead with the role or the strongest differentiator.
- Include 3–5 keywords drawn from the user's core skills and domain that recruiters
  in their target space are likely to search for.
- Avoid buzzwords with no signal value ("passionate", "innovative", "results-driven").
- 220-char limit: aim for 160–210 to leave breathing room and avoid truncation.

## About / Summary Strategy for LinkedIn Impact

The About section is 2,600 chars of narrative real estate — the only place on
LinkedIn where the user can tell their story rather than list facts. It must not
be a prose restatement of the summary field. It should make a reader want to
connect or reach out.

### Visible-Before-"See More" (first ~300 chars)

Only the first 2–3 lines are visible without clicking "see more". This is the hook.
It must stand alone and create enough curiosity or clarity to earn the click.

- **Do not** open with "I am a [title] with X years of experience." That is a
  resume opener — it signals nothing distinctive.
- **Do** open with what the person *does* or *builds* at a level of specificity
  that creates a clear mental image. Examples:
  - "I build the systems that make AI actually work in production."
  - "I've spent 15 years helping fintech companies not blow up under scale."
  - "My work sits at the intersection of compilers and distributed systems."

### Narrative Structure

1. **Hook** (lines 1–3, ~200–300 chars): Distinctive positioning statement.
2. **What you do and who you help** (1–2 short paragraphs): Describe the domain,
   the kinds of problems solved, and the type of organizations or teams the user
   works with. Pull from the most recent and significant experience entries —
   not just from `summary.json`.
3. **Achievement highlights** (3–5 bullets): Draw from the highest-impact bullets
   in `experience.json`. Follow the same content fidelity rules as experience —
   accurate verbs, preserved qualifiers.
4. **What makes you distinctive** (optional, 1 paragraph): Approach, philosophy,
   or something unusual about the career path that differentiates the user from
   other people with the same title.
5. **Call to action** (last 2–3 lines): What the person is open to (roles, projects,
   conversations) and how to reach them. Keep it concrete, not generic
   ("feel free to connect" adds no signal).

### Content Sources

The About section should draw from more than just `summary.json`:
- Lead experience highlights from `experience.json` (top impact bullets)
- Distinctive aspects of the user's role history or domain expertise
- Notable open source projects or patents if they are central to the user's identity

### Prose vs. Bullets

- The hook and positioning sections should be prose — they are personal voice.
- Achievement highlights work well as bullets (use `•`), but limit to 3–5 max.
- Do not make the entire About a bullet list — it reads like a second resume
  and loses the narrative voice that differentiates LinkedIn About from a CV.

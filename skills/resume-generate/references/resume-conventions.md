# Resume Conventions & Constraints

## General Rules

- **Length**: 1-2 pages for most professionals, up to 3 for senior/executive roles.
  1 page ≈ 400 words, 2 pages ≈ 700-900 words. When the user requests a specific
  page count, use the full budget — a "2 page resume" should not produce a thin
  1.5 page document.
- **Format**: Reverse chronological is the default unless the user requests
  functional or hybrid.
- **Customization**: When a job description is provided, customize the resume
  by **selecting** and **ordering** existing material — surfacing relevant
  experience, skills, and achievements first. Do not reframe the candidate's
  identity or rewrite bullets to echo JD language. A resume is not a cover
  letter; over-customization that makes it read as written-for-this-JD
  undermines credibility.

## Section Order (Standard)

1. Name and contact info (header)
2. Professional summary (2-3 sentences anchored to the candidate's real identity)
3. Skills (relevant to the target role, grouped)
4. Experience (reverse chronological, most recent first)
5. Education
6. Certifications (if relevant)
7. Open Source / Projects (if relevant and space permits)
8. Selected Writing / Publications (if blog posts or articles demonstrate relevant domain expertise)
9. Patents (if relevant)
10. Languages (if international relevance or JD mentions)

This order front-loads the most keyword-rich sections for ATS scoring.

## Content Guidelines

- **Action verbs**: Start each bullet with a strong action verb (Led, Designed,
  Implemented, Reduced, Increased, Architected, Migrated, Optimized, etc.)
- **Quantify**: Include metrics wherever possible (%, $, time saved, team size,
  users served, throughput, latency reduction)
- **Relevance**: Prioritize accomplishments relevant to the target role
- **Recency**: Most detail for recent roles (3-5 bullets), less for older roles
  (2-3 bullets). For a 1-2 page resume, total experience bullets across all roles
  should be roughly 12-20.
- **No personal pronouns**: Never use "I", "my", "we"
- **Tense**: Past tense for previous roles, present tense for current role
- **No decorative elements**: No emoji, no Unicode symbols, no ASCII art.
  Plain Markdown that renders cleanly in any converter.

## ATS Optimization

Applicant Tracking Systems parse resumes as plain text before scoring content.
Formatting issues cause parsing failures (resume gets dropped entirely).
Content issues cause low ranking (resume gets parsed but scored poorly).

### Formatting for ATS

- Use standard section headings that ATS parsers recognize: "Professional Summary",
  "Experience", "Skills", "Education", "Certifications". Avoid creative alternatives
  like "What I Do" or "My Journey."
- No tables, multi-column layouts, text boxes, or images
- No headers/footers (ATS often ignores them)
- Simple bullet lists with `-` prefix
- Standard date format: "Mon YYYY" (e.g., "Jan 2021 - Present") — consistent
  throughout for reliable ATS date parsing
- No Unicode decorators (arrows, checkmarks, etc.) — use plain text equivalents
- Spell out acronyms on first use: include both the full term and abbreviation,
  e.g., "Continuous Integration / Continuous Deployment (CI/CD)",
  "Amazon Web Services (AWS)"

### Keyword Strategy

- Extract exact phrases from the job description — ATS matches are often literal
  string comparisons, so use the JD's exact terminology
- Include both acronym and full form on first use
- Place highest-priority keywords in the Summary and Skills sections (parsed first)
- Distribute remaining keywords naturally across experience bullets
- Target at least 2 occurrences of each top-5 to top-10 keyword (naturally, not
  stuffed — each occurrence should be in a meaningful context)
- Never fabricate keywords — only include skills the user genuinely possesses
- When JD says "Kubernetes" don't write "K8s" — match the JD's exact form

### Keyword Gap Analysis

After drafting the resume, compare it against the JD:

1. Extract hard skills, tools, certifications, and role-specific terms from the JD
2. Compare against the resume content
3. For each missing keyword that the user genuinely possesses (per the master
   profile), weave it into an appropriate bullet or skills line using exact-match
   phrasing from the JD
4. Do not add keywords the user doesn't actually have — this is fabrication

When no JD is provided, still apply formatting rules and acronym expansion.

## Customization Strategy

When a job description is provided, customization is limited to selection and
ordering — never identity reshaping or bullet rewriting. SKILL.md is the
authoritative voice on this; this section is the operational checklist.

1. **Decompose** — Extract required skills, desired experience level, key
   responsibilities, success signals, and cultural/soft skill cues
2. **Map honestly** — For each requirement, identify the strongest **genuine**
   matching evidence from the profile. Some requirements will have strong
   matches, some weak, some none. Leave honest gaps visible — do not
   manufacture matches.
3. **Reorder** — Within each section, order by relevance to the role. Recent
   and directly relevant material leads.
4. **Edit, don't reframe** — Tighten bullets for clarity, brevity, and active
   voice using the candidate's own terminology. Do not substitute JD
   vocabulary for the candidate's vocabulary unless the two genuinely refer
   to the same thing in the candidate's domain (e.g., "K8s" / "Kubernetes"
   are interchangeable; "handled increased load" / "architected for
   scalability" are not).
5. **Trim, don't drop roles** — De-emphasize less-relevant material by giving
   it fewer bullets, but keep the role line (title, company, dates) so
   employment continuity is visible. Silently dropping roles creates apparent
   gaps that hurt credibility on an honest resume.

### Borderline cases

- **Tool used in roughly a third of foregrounded projects**: include in skills
  list and in the bullets where it actually applied; do not lead the summary
  or first skill group with it.
- **Recruiter message or short brief instead of a JD**: treat as a thin role
  description. Extract whatever signals are present (e.g., "Amazon Q
  consultant / trainer" implies hands-on Amazon Q experience and ability to
  teach), but do not invent requirements not stated.

## Edge Cases

### Career Gaps

Real gaps in the candidate's history (sabbatical, education, freelance,
caregiving) are recorded in the profile and should be included as the user
has framed them. Do not invent context. **Do not create artificial gaps** by
silently omitting roles for the sake of trimming — keep the role line and
reduce its bullets instead.

### Contract / Freelance Work

Group short engagements under a single "Independent Consultant" or "Freelance"
heading when they're with different clients. List the most impactful engagements
as sub-entries. If a single long-term contract looks like a regular role, format
it as one.

### Overlapping Roles

If the profile shows overlapping dates (e.g., part-time consulting while
full-time employed), keep both with accurate dates. The format handles this
cleanly.

### Very Long Careers (15+ years)

Early-career roles (10+ years ago) should be condensed to 1-2 bullets or a
single line with title, company, and dates. The detail budget goes to recent
roles. Consider omitting early roles entirely if they add no relevant signal.

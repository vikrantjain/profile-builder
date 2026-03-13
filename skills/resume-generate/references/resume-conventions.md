# Resume Conventions & Constraints

## General Rules

- **Length**: 1-2 pages for most professionals, up to 3 for senior/executive roles.
  1 page ≈ 400 words, 2 pages ≈ 700-900 words. When the user requests a specific
  page count, use the full budget — a "2 page resume" should not produce a thin
  1.5 page document.
- **Format**: Reverse chronological is the default unless the user requests
  functional or hybrid.
- **Tailoring**: Every resume should be tailored to a specific job description
  when one is provided. Emphasize relevant experience, skills, and achievements.

## Section Order (Standard)

1. Name and contact info (header)
2. Professional summary (2-3 sentences, tailored to target role)
3. Skills (relevant to the target role, grouped)
4. Experience (reverse chronological, most recent first)
5. Education
6. Certifications (if relevant)
7. Open Source / Projects (if relevant and space permits)
8. Patents (if relevant)

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

## Tailoring Strategy

When a job description is provided:

1. **Decompose** — Extract required skills, desired experience level, key
   responsibilities, success signals, and cultural/soft skill cues
2. **Map** — For each requirement, identify the strongest matching evidence
   from the profile. Some data maps to multiple requirements; some requirements
   may have no match.
3. **Reorder** — Skills and experience bullets ordered by relevance to JD
4. **Reframe** — Adjust language to match the JD's framing. If the JD emphasizes
   "scalability" and the source says "handled increased load", reframe to "scaled
   system to handle 10x traffic growth." Reframing means choosing the right
   lens — never fabricate or exaggerate.
5. **Trim** — De-emphasize or omit content that doesn't strengthen the candidacy.
   A gap in employment history is better than a filler role that dilutes the narrative.

## Edge Cases

### Career Gaps

Do not call attention to gaps. Simply list the roles with their dates. If a gap
is short (< 1 year), the date format "Mon YYYY" naturally minimizes visibility.
If the user has addressed a gap in their profile data (e.g., sabbatical, education,
freelance), include that context briefly.

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

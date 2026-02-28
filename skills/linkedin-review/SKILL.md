---
name: linkedin-review
description: >
  This skill should be used when the user asks to "review my LinkedIn",
  "check my LinkedIn profile", "audit my LinkedIn", "what should I improve
  on LinkedIn", "improve my LinkedIn", "make my LinkedIn more impactful",
  or wants a quality review of their current LinkedIn profile with
  actionable improvement suggestions for a high-impact presence.
---

# LinkedIn Review

Review the user's current LinkedIn profile to assess how effectively it
communicates their professional brand and produce **actionable improvement
suggestions** for maximum impact. The master profile serves as context
for the user's full background — it informs the quality review but is not
the primary focus.

This is a **quality and impact review**, not a data sync check. A brief
gap check is included to catch missing or outdated content, but the bulk
of the review evaluates how well each section sells the user's story and
provides concrete rewrite suggestions.

## Prerequisites

This skill requires the **Playwright MCP server** to be configured and
running, as LinkedIn requires browser-based access with authentication.
If Playwright MCP is not available, inform the user and suggest they
paste their LinkedIn content manually for a text-based review.

## When to Use

Invoke this skill when the user wants to improve their LinkedIn profile's
effectiveness — whether they've recently updated it or just want a fresh
assessment. For generating LinkedIn-ready content to paste, use the
`linkedin-generate` skill instead.

## Workflow

This skill uses a **two-phase approach** to avoid context overload and
ensure all content is captured — including content hidden behind "Show all"
and "See more" buttons.

---

### Phase 1: Scrape LinkedIn (Section-by-Section)

Use the Playwright MCP tools (configured in `.mcp.json` at the workspace
root) to extract content one section at a time. Save all extracted content
to `.profile/tmp/{YYYY-MM-DD}/playwright/` where `{YYYY-MM-DD}` is today's
date. Create this directory structure if it does not exist.

If Playwright MCP is unavailable, ask the user to provide their LinkedIn
content via copy-paste and skip to Phase 2.

#### 1.1 Navigate to Profile

Navigate to the user's LinkedIn profile URL (from `sections/identity.md`
or as provided by the user). Take a page snapshot to confirm the profile
loaded and to identify which sections are present.

#### 1.2 Scrape Each Section

Process LinkedIn sections **one at a time** in this order. For each section:

1. **Scroll** to the section on the page.
2. **Expand** all collapsed content within the section:
   - Click "…see more" / "…more" links on truncated text (About, experience
     descriptions, etc.)
   - Click "Show all N experiences" / "Show all N education" / "Show all N
     skills" / similar buttons to reveal the full list.
   - After clicking a "Show all" button, LinkedIn may navigate to a detail
     page. If so, expand any "…see more" links on that page, scrape all
     entries, then navigate back to the main profile.
3. **Snapshot** the expanded section (use `browser_snapshot`).
4. **Extract** the text content from the snapshot and save it to a
   dedicated file.
5. **Move on** to the next section.

**Sections to scrape (in order):**

| # | Section | Save to | Expand actions |
|---|---------|---------|---------------|
| 1 | Header (name, headline, location) | `header.md` | None needed |
| 2 | About | `about.md` | Click "…see more" if present |
| 3 | Experience | `experience.md` | Click "Show all N experiences", then "…see more" on each entry description |
| 4 | Education | `education.md` | Click "Show all N education" if present |
| 5 | Skills | `skills.md` | Click "Show all N skills" to get full list |
| 6 | Licenses & Certifications | `certifications.md` | Click "Show all" if present |
| 7 | Volunteer Experience | `volunteer.md` | Click "Show all" if present |
| 8 | Recommendations | `recommendations.md` | Click "Show all" / "Received" tab if present |
| 9 | Honors & Awards | `honors.md` | Click "Show all" if present |
| 10 | Projects | `projects.md` | Click "Show all" if present |
| 11 | Patents | `patents.md` | Click "Show all" if present |
| 12 | Languages | `languages.md` | Click "Show all" if present |
| 13 | Publications | `publications.md` | Click "Show all" if present |

Skip any section that does not exist on the profile. Note its absence —
missing high-impact sections (e.g., Recommendations, Volunteer) are worth
calling out as improvement opportunities in the quality review.

**Important scraping rules:**

- Always expand before capturing. Truncated content leads to incomplete
  reviews.
- When a "Show all" button opens a separate page/modal, scrape that page
  completely before navigating back.
- Save each file as plain text Markdown — no HTML.
- After all sections are scraped, close the browser to free resources.

#### 1.3 Close Browser

Once all sections are scraped and saved, close the browser. Playwright is
no longer needed. All subsequent steps work from local files only.

---

### Phase 2: Analyze and Review (Local Only)

All analysis in this phase reads from local files. No browser interaction.

#### 2.1 Read Scraped Content

Read each section file saved in `.profile/tmp/{YYYY-MM-DD}/playwright/`.

#### 2.2 Read Master Profile

Read the relevant profile sections from `sections/` to use as background
context — the master profile tells you what the user has done, achieved,
and is capable of, which informs how well their LinkedIn represents them.

#### 2.3 Apply Presentation Preferences

Read `preferences.md` from the workspace root. If it exists:

1. Read the `## Global` section — these apply to all reviews.
2. Read the `## LinkedIn` section (if present) — these are LinkedIn-specific.
3. Adjust review criteria based on preferences:
   - If a preference de-emphasizes a section, do not flag it as needing improvement.
   - If a preference specifies tone, evaluate existing content against that tone.
   - If a preference reframes data (e.g., "20+ years"), evaluate against that
     framing rather than raw data.
4. LinkedIn-specific preferences take precedence over global if they conflict.

If `preferences.md` does not exist, proceed with default review criteria.

#### 2.4 Quality Review

This is the core of the skill. For each LinkedIn section that has content,
evaluate its effectiveness and impact. Use the master profile as context
for the user's full background — it tells you what achievements, skills,
and experience are available to draw from.

Consult `${CLAUDE_PLUGIN_ROOT}/skills/linkedin-generate/references/linkedin-constraints.md` for
LinkedIn field limits and best practices.

Review each section in the same order as the scrape table. Sections
marked *(LinkedIn-only)* have no master profile counterpart — evaluate
them purely on quality and impact.

##### Header (name, headline, location)
- Does the headline go beyond a plain job title? A strong headline combines
  role + domain expertise + differentiator (e.g., "Staff Engineer |
  Distributed Systems & Cloud-Native Architecture | 3 Patents").
- Does the headline include keywords a recruiter or peer would search for?
- Is the headline within the 220-character limit while being substantive?

##### About
- Does it open with a compelling hook (not "I am a software engineer with
  X years of experience")?
- Is it written in first person with a confident, authentic voice?
- Does it tell a narrative arc — who you are, what drives you, what you
  deliver — rather than listing skills?
- Does it include quantifiable achievements or proof points?
- Does it end with a call to action or invitation to connect?
- Does it leverage the full 2,600-character limit effectively, or is it
  too thin?

##### Experience
- Do descriptions lead with strong action verbs and quantified outcomes
  (%, $, scale, impact) rather than listing responsibilities?
- Are bullet points concise and scannable (1–2 lines each)?
- Do entries highlight leadership, scope, and business impact — not just
  technical tasks?
- Are the most impressive achievements front-loaded in each entry?
- Is the level of detail proportional to recency and relevance (recent
  roles get more depth)?

##### Education
- Do entries include relevant activities, honors, or projects that add
  signal?
- Is the level of detail appropriate (recent or prestigious degrees get
  more depth)?

##### Skills
- Are the top 3 visible skills the most strategic and relevant ones (not
  generic like "Python" or "Communication")?
- Is the skill list comprehensive enough to appear in search results for
  target roles?
- Are skills ordered by relevance and endorsement strength?

##### Licenses & Certifications
- Are certifications current and relevant to career direction?
- Do entries include issuing organization and date to add credibility?

##### Volunteer Experience *(LinkedIn-only)*
- Does it add dimension to the professional story (leadership, community,
  values)?
- Are descriptions framed around impact and skills applied?

##### Recommendations *(LinkedIn-only)*
- Are there enough recommendations (at least 3–5) to provide social proof?
- Do they come from credible sources (managers, senior peers, clients)?
- Do they reinforce the professional brand conveyed in the headline and about?
- Are they specific (mentioning projects, outcomes, qualities) or generic?

##### Honors & Awards *(LinkedIn-only)*
- Are awards relevant and framed to support career narrative?
- Do entries include context (who gives the award, what it recognizes)?

##### Projects
- Are project descriptions framed around impact and outcomes, not just
  what the project does?
- Do descriptions mention technologies, scale, or adoption metrics?

##### Patents
- Are patent entries complete (title, patent office, number/status)?
- Are descriptions written to convey innovation and business impact, not
  just technical scope?

##### Languages
- Is the proficiency level accurate for each language?
- Are languages relevant to the user's target roles or market included?

##### Publications *(LinkedIn-only)*
- Are publications relevant to the user's professional brand?
- Do entries include co-authors, venue, and date for credibility?

##### Overall Profile Impression
- Does the profile tell a coherent professional story across sections?
- Is there a consistent theme or personal brand running through headline,
  about, and experience?
- Would a recruiter scanning for 30 seconds understand the user's value
  proposition?
- Are there any sections that undermine the overall impression (e.g., a
  weak about section next to strong experience entries)?

#### 2.5 Gap Check

A brief check for notable omissions — not an exhaustive field-by-field
comparison. Flag only items that would meaningfully improve profile impact:

- Key achievements or roles from the master profile missing on LinkedIn
- Outdated information (old titles, ended roles still listed as current)
- Significant inconsistencies (different job titles, conflicting dates)

Do not flag minor wording differences or data that the user may have
intentionally omitted from LinkedIn.

Sections that exist only on LinkedIn (Recommendations, Volunteer Experience,
Honors & Awards, Publications) have no master profile counterpart — they get
a quality review only, no gap check.

#### 2.6 Generate Review Report

Produce a structured review report with these sections:

1. **Executive Summary** — 2–3 sentence overall assessment of profile
   effectiveness. State clearly whether the profile makes a strong
   impression, is adequate but underperforming, or needs significant work.

2. **Section-by-Section Review** — for each LinkedIn section:
   - **Current state**: brief description of what's there now
   - **Quality assessment**: how effective the existing content is at
     communicating the user's value
   - **Improvement suggestions**: concrete, specific changes — rewrite
     examples where possible ("change X to Y"), not vague advice
   - **Notable gaps** (if any): important missing content from the master
     profile that would improve this section

3. **Rewrite Suggestions** — for sections that would benefit most from
   improvement, provide before/after examples. Draft improved versions of:
   - Headline (full rewrite)
   - About section opening paragraph (rewrite or new draft)
   - 1–2 experience entry descriptions (rewritten bullets)
   - Top 3 skills reordering recommendation

4. **Priority Actions** — numbered list of the top 5–10 changes ranked by
   impact on profile effectiveness. Each item should state what to change,
   why it matters, and how much effort it takes (quick fix / moderate /
   significant rewrite).

#### 2.7 Verify Preferences Compliance

Before writing the report, re-read the applicable preferences and verify:
- Suggestions align with the user's stated preferences for tone and framing.
- Rewrite suggestions reflect the user's preferred style.
- Sections the user chose to de-emphasize are not flagged as needing work.
If any preference was missed or contradicted, revise the report before proceeding.

#### 2.8 Write Output

Write the review report to `linkedin-review.md` and display it
in the conversation.

## Output Checklist

Before finishing, verify:

- [ ] All expandable sections were expanded before scraping (no truncated content)
- [ ] Each scraped section saved to its own file in `.profile/tmp/{YYYY-MM-DD}/playwright/`
- [ ] Browser closed after scraping — analysis used only local files
- [ ] Quality review is the primary focus — every section assessed for impact
- [ ] Concrete rewrite suggestions are provided (not just "improve X")
- [ ] Before/after examples included for headline, about, and at least
      one experience entry
- [ ] Character limits noted where relevant
- [ ] Priority actions are ranked by impact
- [ ] Report written to `linkedin-review.md`
- [ ] Review criteria and suggestions honor all applicable presentation preferences

## Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/skills/linkedin-generate/references/linkedin-constraints.md`** — LinkedIn field limits and formatting rules

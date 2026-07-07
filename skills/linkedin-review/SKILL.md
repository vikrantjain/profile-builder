---
name: linkedin-review
description: >
  Review and assess the quality of the user's current LinkedIn profile with
  actionable improvement suggestions. Use when the user asks to "review my
  LinkedIn", "check my LinkedIn profile", "audit my LinkedIn", "what should
  I improve on LinkedIn", "improve my LinkedIn", "make my LinkedIn more
  impactful", "how does my LinkedIn look", "is my LinkedIn good enough",
  "LinkedIn profile feedback", "critique my LinkedIn", "rate my LinkedIn",
  or wants a quality assessment of their LinkedIn presence. Also trigger when
  the user mentions LinkedIn in the context of wanting feedback, improving
  their professional brand, or preparing for a job search — even if they
  don't say "review". For generating LinkedIn-ready content to paste, use
  the `linkedin-generate` skill instead.
---

# LinkedIn Review

Review the user's current LinkedIn profile to assess how effectively it
communicates their professional brand and produce **actionable improvement
suggestions** with concrete rewrites. The master profile provides context
for the user's full background — achievements, skills, and experience that
the LinkedIn profile should be drawing from.

This is a **quality and impact review**, not a data sync check. The central
question for every section is: "Given what this person has actually done
(per the master profile), how well does their LinkedIn sell that story?"
A brief gap check catches missing or outdated content, but the bulk of the
review evaluates effectiveness and provides before/after rewrites.

**Data fidelity is critical.** When referencing the master profile in the
review or in rewrite suggestions, attribute achievements, tools, and
skills to the correct role and project. Cross-check each claim against the
specific `contributions`, `impact`, and `tech_stack` fields in the
relevant project entry. Do not generalize or merge details across roles —
e.g., if LangGraph was used in a Red-Team AI Agent project, do not
attribute it to architecture reviews that used Cursor and MCP.

## Prerequisites

This skill requires the **Playwright MCP server** to be configured and
running, as LinkedIn requires browser-based access with authentication.
If Playwright MCP is not available, use the **manual fallback** (see below).

## Workflow

Two phases: scrape the LinkedIn profile, then analyze it locally.

---

### Phase 1: Capture LinkedIn Content

#### Path A: Playwright MCP (preferred)

Use the Playwright MCP tools (configured in the plugin's root `.mcp.json`)
to extract content one section at a time. Save all extracted content
to `.profile/tmp/{YYYY-MM-DD}/playwright/` where `{YYYY-MM-DD}` is today's
date. Create this directory if it does not exist.

##### 1.1 Navigate and Handle Auth

Read `sections/identity.json` to get the user's LinkedIn URL (or use the
URL the user provides). Navigate to the profile page.

**Auth wall handling:** LinkedIn may show a login page or auth wall instead
of the profile. After navigating, take a snapshot and check for login
indicators (login form, "Sign in" button, "Join now", or a redirect to
`/login`). If detected:

1. Navigate to `https://www.linkedin.com/login` — the browser may have an
   existing session that auto-redirects to the feed. Take a snapshot to
   check.
2. If still on the login page (no active session), **ask the user to log
   in**. Tell them: "LinkedIn requires authentication. Please log in to
   your LinkedIn account in the browser window that just opened. Let me
   know when you're done." Use `AskUserQuestion` and wait for
   confirmation.
3. After the user confirms, take a snapshot to verify the login succeeded
   (look for feed content, profile elements, or navigation bar with the
   user's avatar). If still not logged in, ask once more with specific
   guidance: "It looks like the login didn't complete. Please make sure
   you've finished any 2FA or verification steps and the page shows your
   LinkedIn feed."
4. Once logged in, navigate back to the target profile URL.
5. Only fall back to Path B if the user explicitly says they cannot or do
   not want to log in via the browser.

##### 1.2 Full-Page Snapshot

After the profile loads, scroll to the bottom of the page (press `End` key
2–3 times) to trigger lazy-loading of all sections. Then save a full
snapshot to file:

```
browser_snapshot → save to .profile/tmp/{YYYY-MM-DD}/playwright/full-snapshot.md
```

**Important:** LinkedIn profile snapshots are typically 100K–300K characters,
which exceeds inline token limits. Always save to file using the `filename`
parameter rather than reading inline. Then use Grep to find section
headings and Read with line offsets to extract specific sections.

From the snapshot, identify which sections exist by searching for
`heading "SectionName"` patterns. Note which sections are present and
which are absent — absent sections feed directly into the Missing Sections
part of the review.

##### 1.3 Expand and Capture Each Section In Depth

The visible profile page only shows a preview of each section — truncated
descriptions, collapsed lists, and "Show all" links that hide the
majority of the content. A surface-level snapshot misses most of the
data. You must navigate into every section's detail page and expand
every collapsed element to get the full picture.

**General approach for each section below:**
1. On the main profile, find the section and click "Show all N …" (or
   similar) to navigate to its detail page (e.g., `/details/experience/`).
2. On the detail page, scroll to the bottom to load all entries.
3. Expand every "…more" / "see more" button on that page — each entry
   may have its own collapsed description.
4. Take a snapshot (save to file) and extract the full content.
5. Use `browser_navigate_back` to return to the main profile before
   moving to the next section.

If a section has no "Show all" link (all content is visible inline),
expand any "…more" buttons in place and capture from the main profile
snapshot.

Work through sections in this order:

1. **About** — On the main profile, click the "…more" link in the About
   section to reveal the full text. Capture the complete expanded text
   (needed for character count and narrative review).

2. **Experience** — Click "Show all N experiences" to navigate to the
   experience detail page. On that page:
   - Scroll to the bottom to load all roles (LinkedIn lazy-loads older
     entries).
   - Expand **every** role's "…more" description — not just recent roles.
     Older roles matter for career narrative review.
   - For roles with nested positions (company groups), expand each
     nested position's description too.
   - Take a snapshot and save the full content.
   - Navigate back to the main profile.

3. **Education** — Click "Show all N education" if present. Expand any
   "…more" descriptions (activities, honors, etc.). Capture and navigate
   back.

4. **Licenses & Certifications** — Click "Show all N licenses &
   certifications" if present. Capture all entries (name, issuer, date,
   credential ID). Navigate back.

5. **Skills** — Click "Show all N skills" to navigate to the skills
   detail page. This page groups skills by category and shows endorsement
   counts. Scroll to load all skill groups. Capture the complete list.
   Navigate back.

6. **Recommendations** — Click into the Recommendations section. Note
   the "Received" and "Given" tab counts. On the "Received" tab, expand
   every truncated recommendation ("…more"). Capture all recommendation
   text with author names and their relationship to the user. Navigate
   back.

7. **Patents** — Click "Show all N patents" if present. Capture each
   patent's title, number, date, and description. Verify the count
   against the master profile. Navigate back.

8. **Projects** — Click "Show all N projects" if present. Expand
   descriptions. Capture project names, descriptions, and collaborators.
   Navigate back.

9. **Volunteer Experience** — Click "Show all" if present. Expand
   descriptions. Capture roles, organizations, and descriptions.
   Navigate back.

10. **Honors & Awards** — Click "Show all" if present. Capture all
    entries. Navigate back.

11. **Publications** — Click "Show all" if present. Capture titles,
    publishers, dates, co-authors. Navigate back.

12. **Languages** — Capture language names and proficiency levels.

13. **Activity / Posts** — Note follower count and recent post topics
    from the main profile (no detail page needed).

14. **Any other sections** — If the profile has sections not listed above,
    apply the same expand-and-capture pattern.

**Do not skip sections.** If a "Show all" link exists, you must click it.
If an entry has a "…more" link, you must expand it. Partial data leads
to an incomplete review — the user is relying on you to see everything
on their profile.

##### 1.4 Save Section Files

Extract content from the snapshot (and any expanded sections) into
individual files. For each section present on the profile:

| # | Section | Save to | What to capture |
|---|---------|---------|-----------------|
| 1 | Header | `header.md` | Name, headline (full text + char count), location, connection count |
| 2 | About | `about.md` | Full expanded text (post "…more" click) |
| 3 | Experience | `experience.md` | Each role: title, company, dates, location, **full expanded description** text, skills tags. Must include all roles from the detail page, not just what was visible on the main profile. |
| 4 | Education | `education.md` | Each entry: degree, field, school, dates, activities/honors |
| 5 | Skills | `skills.md` | **All** skills from the detail page with endorsement counts, grouped by category |
| 6 | Certifications | `certifications.md` | Each entry: name, issuer, date, credential ID |
| 7 | Recommendations | `recommendations.md` | Count received/given, **full expanded text** of each recommendation with author name and relationship |
| 8 | Patents | `patents.md` | Each: title, number, date, description; note total count |
| 9 | Projects | `projects.md` | Each: name, description, collaborators |
| 10 | Volunteer | `volunteer.md` | Each: role, organization, dates, description |
| 11 | Honors & Awards | `honors.md` | Each: title, issuer, date, description |
| 12 | Publications | `publications.md` | Each: title, publisher, date, co-authors |
| 13 | Languages | `languages.md` | Each: language + proficiency level |
| 14 | Activity | `activity.md` | Follower count, recent post summary |
| 15 | Missing sections | `missing-sections.md` | List of absent sections |

Skip sections not present. Save as plain structured text — no HTML.

##### 1.5 Close Browser

Close the browser after all sections are scraped. Everything from here
works from local files only.

#### Path B: Manual Fallback

If Playwright MCP is not available, tell the user and ask them to paste
their LinkedIn content. Guide them on what to provide:

1. Ask the user to visit their LinkedIn profile and copy-paste the content
   of each section they want reviewed. At minimum: headline, about, and
   experience. More sections = more thorough review.
2. Save each pasted section to `.profile/tmp/{YYYY-MM-DD}/playwright/`
   using the same filenames as the scrape table above.
3. Remind the user to expand "see more" and "Show all" before copying,
   since truncated content limits review quality.

Then proceed to Phase 2 identically.

---

### Phase 2: Analyze and Review (Local Only)

All analysis reads from local files. No browser interaction.

#### 2.1 Read Scraped Content

Read each section file from `.profile/tmp/{YYYY-MM-DD}/playwright/`.

#### 2.2 Read Master Profile

Read `profile-index.json` to discover available sections and their paths.
Then read the section JSON files needed for review context. Parse each
file and access fields from the `data` object.

| Section file | What it provides for the review |
|---|---|
| `sections/identity.json` | Name, title, location, LinkedIn URL |
| `sections/summary.json` | Professional summary — benchmark for About |
| `sections/experience.json` | Roles, achievements, impact — benchmark for Experience |
| `sections/education.json` | Degrees, honors — benchmark for Education |
| `sections/skills.json` | Full skill inventory — benchmark for Skills |
| `sections/certifications.json` | Certs — benchmark for Licenses & Certifications |
| `sections/open-source.json` | Projects — benchmark for Projects |
| `sections/patents.json` | Patents — benchmark for Patents |
| `sections/languages.json` | Languages — benchmark for Languages |

If key section files don't exist, inform the user and suggest running
`/profile-init` or `profile-section` to generate them. The review can
still proceed for LinkedIn-only sections and general quality assessment,
but master-profile-informed insights will be limited.

#### 2.3 Load Presentation Preferences

Read `preferences.md` from the workspace root. If it exists:

1. Read `## Global` — applies to all reviews.
2. Read `## LinkedIn` (if present) — LinkedIn-specific overrides.
3. Adjust review criteria:
   - De-emphasized sections: don't flag as needing improvement.
   - Tone preferences: evaluate content against the user's preferred tone.
   - Data reframing (e.g., "20+ years"): evaluate against that framing,
     not raw data.
4. LinkedIn-specific preferences take precedence over global on conflicts.

If `preferences.md` does not exist, use default review criteria and note
in the report header: "No preferences file found — using default review
criteria." This makes it visible to the user that preferences were checked.

#### 2.4 Quality Review

This is the core of the skill. For each LinkedIn section, evaluate its
effectiveness at communicating the user's value. The master profile is the
lens — it tells you what achievements, skills, and experience the user
*could* be showcasing, which makes gaps in impact visible.

Consult `${CLAUDE_PLUGIN_ROOT}/skills/linkedin-generate/references/linkedin-constraints.md`
for LinkedIn field limits and best practices.

Rate each section on a 3-point scale and use the rating as a prefix:

- **Strong** — section effectively communicates value, minor tweaks at most
- **Needs work** — decent foundation but missing impact, clarity, or key content
- **Weak** — significantly underperforming or missing; priority rewrite

Review sections in scrape-table order. For each section, assess against
both general LinkedIn best practices and what the master profile reveals
the user *could* be saying. Sections marked *(LinkedIn-only)* have no
master profile counterpart — evaluate purely on quality and impact.

##### Header (headline, location)

The headline is the most-viewed field on LinkedIn. A plain job title wastes
this space.

- Does it go beyond a job title to include domain expertise + differentiator?
- Does it contain keywords recruiters in the user's space would search for?
- Is it substantive (160–210 chars ideal) without hitting the 220-char limit?
- **Master profile angle**: Compare against the user's title, summary, and
  top skills. Is the headline underselling what they actually do?

##### About

- Does the opening hook stand alone before the "see more" fold (~300 chars)?
  Avoid the "I am a [title] with X years" opener — it signals nothing distinctive.
- Does it tell a narrative (who, what drives them, what they deliver) rather
  than listing skills?
- Does it include proof points — quantified achievements drawn from experience?
- Does it end with a concrete call to action?
- Does it use the 2,600-char budget effectively, or is it too thin?
- **Master profile angle**: Are the user's most impressive achievements
  (from experience.json) reflected here? Is the narrative consistent with
  their summary?

##### Experience

- Do bullets lead with action verbs and quantified outcomes (%, $, scale)?
- Are bullets concise and scannable (1–2 lines each)?
- Do entries highlight leadership, scope, and business impact — not just
  technical tasks?
- Are the strongest achievements front-loaded in each entry?
- Is detail proportional to recency (recent roles get more depth)?
- **Master profile angle**: Compare each role's LinkedIn bullets against the
  master profile's `contributions` and `impact` fields. Are high-impact
  achievements buried, missing, or understated? Are any claims inflated
  beyond what the source data supports?

##### Education

- **Master profile angle**: Does LinkedIn reflect honors, activities, or
  projects from the master profile that would add signal? Is detail level
  appropriate for the degree's relevance?

##### Skills

- Are the top 3 visible skills strategic and role-defining (not generic)?
- Is the list comprehensive enough for recruiter search visibility?
- **AI development tools carry high market signal.** Tools like LangGraph,
  Claude Code, CrewAI, MCP, Cursor, and Amazon Q are increasingly searched
  by recruiters and signal hands-on AI-augmented capability. These should
  be treated as core or adjacent skills, not relegated to "nice to have."
- **Master profile angle**: Compare against the full skill inventory. Are
  high-value skills missing? Are obsolete or low-signal skills taking up
  slots that role-defining skills should occupy?

##### Licenses & Certifications

- **Master profile angle**: Are certifications from the master profile
  missing on LinkedIn? Are listed certs current and relevant?

##### Volunteer Experience *(LinkedIn-only)*

- Does it add dimension to the professional story (leadership, values)?
- Are descriptions framed around impact and skills applied?

##### Recommendations *(LinkedIn-only)*

- Are there enough (3–5 minimum) for credible social proof?
- Do they come from credible sources (managers, senior peers, clients)?
- Do they reinforce the brand in the headline and about, or are they generic?

##### Honors & Awards *(LinkedIn-only)*

- Are entries contextualized (who gives the award, what it recognizes)?

##### Projects

- **Master profile angle**: Are notable open-source projects from the master
  profile represented? Are descriptions framed around impact and outcomes?

##### Patents

- **Master profile angle**: Are all patents from the master profile listed?
  Do descriptions convey innovation and business impact?

##### Languages

- **Master profile angle**: Does the list match the master profile? Are
  proficiency levels accurate?

##### Publications *(LinkedIn-only)*

- Are entries relevant and complete (co-authors, venue, date)?

##### Overall Profile Coherence

- Does the profile tell a coherent story across sections — consistent theme
  from headline through about through experience?
- Would a recruiter scanning for 30 seconds understand the value proposition?
- Are there sections that undermine the overall impression (e.g., a weak
  about section next to strong experience)?
- **Master profile angle**: Is there a significant mismatch between how
  impressive the user's actual background is and how their LinkedIn
  presents it?

#### 2.5 Gap Check

A brief check for notable omissions — not exhaustive field-by-field
comparison. Flag only items that would meaningfully improve profile impact:

- Key achievements or roles from the master profile missing on LinkedIn
- Outdated information (old titles, ended roles listed as current)
- Significant inconsistencies (different job titles, conflicting dates)

Do not flag minor wording differences or data the user may have
intentionally omitted. Exclude any master profile value that is exactly
`"TBD"` or `["TBD"]` — these are unfilled placeholders.

Sections that exist only on LinkedIn (Recommendations, Volunteer,
Honors & Awards, Publications) get quality review only, no gap check.

#### 2.6 Verify Preferences Compliance

Before generating the report, re-read applicable preferences and verify:

- Suggestions align with the user's tone and framing preferences.
- Rewrite suggestions reflect the user's preferred style.
- De-emphasized sections are not flagged as needing work.

If any preference is missed or contradicted, adjust before proceeding.

#### 2.7 Generate Review Report

Produce a structured review report:

**1. Executive Summary**

2–3 sentence overall assessment. State clearly: strong impression,
adequate but underperforming, or needs significant work. Include a
one-line summary of the biggest opportunity (e.g., "The headline and about
section are underselling a very strong engineering background").

**2. Section-by-Section Review**

For each LinkedIn section that has content:

- **Rating**: Strong / Needs work / Weak
- **Current state**: brief description of what's there
- **Assessment**: how effective it is at communicating the user's value,
  informed by what the master profile reveals they *could* be saying
- **Suggestions with rewrites**: concrete changes — provide before/after
  text for anything rated Needs work or Weak. For the headline, about
  opening, and weakest experience entries, always provide a full rewrite
  draft. Include character counts for constrained fields.
- **Notable gaps** (if any): important missing content from the master
  profile that would improve this section

**3. Missing Sections**

Sections absent from LinkedIn that would add value, based on what exists
in the master profile (e.g., "You have 3 patents in your profile but no
Patents section on LinkedIn").

**4. Priority Actions**

Numbered list of the top 5–10 changes ranked by impact. Each item:
- What to change
- Why it matters
- Effort level: quick fix / moderate / significant rewrite

#### 2.8 Write Output

Write the review report to `linkedin-review.md` and display it in the
conversation.

## Output Checklist

Before finishing, verify:

- [ ] Every "…more" and "Show all" element expanded (no truncated content)
- [ ] All experience entries expanded (including older roles)
- [ ] Full-page snapshot saved to `.profile/tmp/{YYYY-MM-DD}/playwright/`
- [ ] Each section's content saved to individual files in same directory
- [ ] Browser closed after scraping — analysis used only local files
- [ ] Master profile read via `profile-index.json` to discover sections
- [ ] TBD values excluded from gap analysis
- [ ] Every section rated (Strong / Needs work / Weak)
- [ ] Before/after rewrites provided for headline, about, and weakest experience entries
- [ ] Character counts noted for constrained fields (headline, about)
- [ ] Priority actions ranked by impact
- [ ] Report written to `linkedin-review.md`
- [ ] All suggestions honor applicable presentation preferences

## Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/skills/linkedin-generate/references/linkedin-constraints.md`** — LinkedIn field limits and formatting rules

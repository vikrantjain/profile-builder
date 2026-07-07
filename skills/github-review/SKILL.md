---
name: github-review
description: >
  Review and assess the quality of the user's live GitHub profile with
  actionable improvement suggestions. Use when the user asks to "review my
  GitHub", "check my GitHub profile", "audit my GitHub", "how does my GitHub
  look", "is my GitHub good enough", "improve my GitHub profile", "make my
  GitHub more impressive", "GitHub profile feedback", "critique my GitHub",
  "what should I improve on GitHub", "compare GitHub with my profile", or
  wants a quality assessment of their GitHub presence. Also trigger when the
  user mentions GitHub in the context of wanting feedback, improving their
  developer brand, or preparing for a job search — even if they don't say
  "review". For generating a GitHub profile README from profile data, use
  the `github-generate` skill instead.
---

# GitHub Review

Review the user's live GitHub profile to assess how effectively it
communicates their builder credibility and produce **actionable improvement
suggestions** with concrete rewrites. The master profile provides context
for the user's full background — projects, contributions, and skills that
the GitHub profile should be drawing from.

This is a **quality and impact review, not a data sync check**. The central
question for every element is: "Given what this person has actually built
(per the master profile), how well does their GitHub presence sell that to
a developer audience?" A brief gap check catches missing or outdated
content, but the bulk of the review evaluates effectiveness and provides
before/after rewrites.

The audience matters: GitHub profile visitors are developers, hiring
engineers, and potential collaborators. They read code and judge substance.
Review against that bar — a profile can be complete and still land flat.

## Workflow

### 1. Fetch GitHub Profile Data

Use the `gh` CLI (preferred) or WebFetch to gather the live profile state.
Save all fetched content (API responses, extracted text) to
`.profile/tmp/{YYYY-MM-DD}/github/` where `{YYYY-MM-DD}` is today's date.
Create the directory if it does not exist.

- **Profile bio and metadata**: `gh api users/<username>` (or `gh api user`
  for the authenticated user) — bio, name, company, location, blog URL,
  follower counts.
- **Profile README**: `gh api repos/<username>/<username>/contents/README.md
  --jq .content | base64 -d`. A 404 means no profile README exists — that
  is itself a major finding, not an error.
- **Pinned repositories** (GraphQL — the REST API does not expose pins):

  ```
  gh api graphql -f query='
  query($login: String!) {
    user(login: $login) {
      pinnedItems(first: 6, types: REPOSITORY) {
        nodes {
          ... on Repository {
            name
            description
            url
            stargazerCount
            primaryLanguage { name }
            repositoryTopics(first: 10) { nodes { topic { name } } }
          }
        }
      }
    }
  }' -f login=<username>
  ```

- **Top repositories** (for pin candidates and hygiene review):
  `gh repo list <username> --limit 30 --json name,description,stargazerCount,repositoryTopics,updatedAt,isFork,isArchived`
- **Recent activity** (optional): `gh api users/<username>/events` — enough
  to judge whether the profile looks active.

If the `gh` CLI is unavailable or unauthenticated, fall back to WebFetch on
the public profile page and note in the report that pinned-repo and topic
data may be incomplete.

### 2. Read Master Profile

Read `profile-index.json` to discover available sections and their paths.
Then read the section JSON files needed for review context. Parse each file
and access fields from the `data` object.

| Section file | What it provides for the review |
|---|---|
| `sections/identity.json` | Name, title, GitHub URL — benchmark for bio |
| `sections/summary.json` | Professional summary — benchmark for README intro |
| `sections/skills.json` | Full skill inventory — benchmark for tech stack |
| `sections/open-source.json` | Projects and contributions — benchmark for pins and featured projects |
| `sections/experience.json` | Scale signals and domain depth the README could be using |
| `sections/blogs.json` | Posts the README could surface |

If key section files don't exist, inform the user and suggest running
`/profile-init` or `/profile-section` to generate them. The review can still
proceed as a general quality assessment, but master-profile-informed
insights will be limited.

### 3. Load Presentation Preferences

Read `preferences.md` from the workspace root. If it exists:

1. Read `## Global` — applies to all reviews.
2. Read `## GitHub` (if present) — GitHub-specific overrides.
3. Adjust review criteria:
   - De-emphasized sections: don't flag as needing improvement.
   - Tone preferences: evaluate content against the user's preferred tone.
   - Data reframing (e.g., "20+ years"): evaluate against that framing,
     not raw data.
4. GitHub-specific preferences take precedence over global on conflicts.

If `preferences.md` does not exist, use default review criteria and note in
the report header: "No preferences file found — using default review
criteria."

### 4. Quality Review

This is the core of the skill. For each element of the GitHub presence,
evaluate its effectiveness at communicating builder credibility. The master
profile is the lens — it tells you what projects, contributions, and skills
the user *could* be showcasing, which makes underselling visible.

Consult `${CLAUDE_PLUGIN_ROOT}/skills/github-generate/references/github-readme-conventions.md`
for README conventions, badge syntax, and layout best practices.

Rate each element on a 3-point scale and use the rating as a prefix:

- **Strong** — effectively communicates value, minor tweaks at most
- **Needs work** — decent foundation but missing impact, clarity, or key content
- **Weak** — significantly underperforming or missing; priority rewrite

##### Bio (the one-liner)

The bio appears in search results, hover cards, and org member lists — it
is read far more often than the README.

- Does it position the person technically ("builds X", "works on Y") rather
  than restating a job title?
- Does it fit the developer audience — specific, no corporate phrasing?
- **Master profile angle**: Compare against `identity.json` title and
  `summary.json`. Is the bio underselling what they actually build?

##### Profile README — above the fold

The first screenful (header, intro, start of tech stack) is what most
visitors see.

- Is there a profile README at all? Absence is the single biggest finding.
- Does the header subtitle establish a technical identity ("what kind of
  engineer") rather than an org-chart title?
- Does the intro open with a hook — a domain, a system type, a scale — that
  makes another developer curious? Avoid "I am a [title] with X years."
- **Master profile angle**: Does the intro use the scale signals and domain
  depth available in `experience.json` and `summary.json`?

##### Profile README — tech stack

- Is it curated (roughly 15–25 badges) or a wall of every tool ever touched?
- Grouped by function, consistent badge style, primary tools first?
- **Master profile angle**: Compare against `skills.json`. Are
  identity-defining skills missing? Are low-signal tools (Git, VS Code)
  taking slots?

##### Profile README — featured projects and contributions

- Do featured projects tell a story (what it does, key technical work,
  impact metrics) or just list repo links?
- Are external contributions surfaced? Community participation is a strong
  credibility signal.
- **Master profile angle**: Compare against `open-source.json`. Are the
  strongest projects and contributions from the master profile represented?
  Are descriptions weaker than the `contributions`/`impact` data available?

##### Pinned repositories

Pins are the six slots visitors scan first — they should be deliberate.

- Are all six slots used? Are they the *right* six given the master
  profile's projects (stars, impact, identity relevance)?
- Are forks or trivial repos occupying slots that original work should hold?
- **Master profile angle**: Cross-reference `open-source.json` projects
  against the pinned list; name specific swap candidates.

##### Repository hygiene (top repos)

For the top ~10 repos by stars/recency: do they have descriptions and
topics? A pinned or featured repo with no description undercuts the README
that points to it. Flag repos worth fixing — don't audit all of them.

##### Overall coherence

- Do bio, README, and pins tell one consistent story about what kind of
  engineer this is?
- Would a hiring engineer scanning for 30 seconds understand the value
  proposition?
- **Master profile angle**: Is there a significant mismatch between how
  impressive the user's actual work is and how the GitHub presence reads?

### 5. Gap Check

A brief check for notable omissions — not an exhaustive field-by-field
comparison. Flag only items that would meaningfully improve impact:

- Notable projects or contributions from `open-source.json` invisible on
  the profile (not pinned, not in the README)
- Outdated content (README referencing old roles or dead projects)
- Repos listed in the master profile that no longer exist on GitHub

Do not flag minor wording differences or data the user may have
intentionally omitted. Exclude any master profile value that is exactly
`"TBD"` or `["TBD"]` — these are unfilled placeholders.

### 6. Verify Preferences Compliance

Before generating the report, re-read applicable preferences and verify:

- Suggestions align with the user's tone and framing preferences.
- Rewrite suggestions reflect the user's preferred style.
- De-emphasized sections are not flagged as needing work.

If any preference is missed or contradicted, adjust before proceeding.

### 7. Generate Review Report

Produce a structured review report:

**1. Executive Summary** — 2–3 sentence overall assessment: strong
impression, adequate but underperforming, or needs significant work. Include
a one-line statement of the biggest opportunity.

**2. Element-by-Element Review** — For each element in section 4:

- **Rating**: Strong / Needs work / Weak
- **Current state**: brief description of what's there
- **Assessment**: how effective it is, informed by what the master profile
  shows they could be saying
- **Suggestions with rewrites**: concrete changes — provide before/after
  text for anything rated Needs work or Weak. Always provide a full rewrite
  draft for the bio and the README intro; for pins, name the exact
  pin/unpin swaps.

**3. Missing Elements** — Things absent from GitHub that the master profile
shows would add value (e.g., "no profile README", "3 strong projects from
your profile are neither pinned nor featured").

**4. Priority Actions** — Numbered list of the top 5–10 changes ranked by
impact. Each item: what to change, why it matters, and effort level
(quick fix / moderate / significant rewrite).

### 8. Write Output

Write the review report to `github-review.md` and display it in the
conversation.

## Output Checklist

Before finishing, verify:

- [ ] Fetched data saved to `.profile/tmp/{YYYY-MM-DD}/github/`
- [ ] Pinned repos fetched via GraphQL (or absence of pin data noted)
- [ ] Master profile read via `profile-index.json` to discover sections
- [ ] TBD values excluded from gap analysis
- [ ] Every element rated (Strong / Needs work / Weak)
- [ ] Before/after rewrites provided for bio and README intro (and any Weak element)
- [ ] Pin/unpin suggestions name specific repos from the master profile
- [ ] Priority actions ranked by impact with effort levels
- [ ] Report written to `github-review.md`
- [ ] All suggestions honor applicable presentation preferences

## Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/skills/github-generate/references/github-readme-conventions.md`** — GitHub README conventions and badge syntax

---
name: github-review
description: >
  This skill should be used when the user asks to "review my GitHub profile",
  "check my GitHub", "audit my GitHub profile", "compare GitHub with my
  profile", "what's missing on my GitHub", or wants their current GitHub
  profile reviewed against the master profile data to identify gaps and
  improvement opportunities.
---

# GitHub Review

Review the user's current GitHub profile by fetching it via the `gh` CLI
or WebFetch tool and comparing it against the master profile data.

## When to Use

Invoke this skill after the user has updated their GitHub profile and
wants to verify completeness against the master profile. For generating
a GitHub profile README from scratch, use the `github-generate`
skill instead.

## Workflow

### 1. Fetch GitHub Profile Data

Use the `gh` CLI or WebFetch to gather:

- **Profile bio and metadata**: `gh api user` for the authenticated user,
  or `gh api users/<username>` for a specific user
- **Profile README**: fetch `<username>/<username>/README.md` via the API
  (`gh api repos/<username>/<username>/contents/README.md`)
- **Pinned repositories**: fetch via the GitHub GraphQL API or by reading
  the profile page
- **Recent activity**: `gh api users/<username>/events --paginate` (optional)

Save all fetched content (API responses, extracted text) to
`.profile/tmp/{YYYY-MM-DD}/github/` where `{YYYY-MM-DD}` is today's
date. Create this directory structure if it does not exist.

If the `gh` CLI is not available, use WebFetch to read the public profile
page and extract visible content.

### 2. Read Master Profile

Read the relevant profile section JSON files from `sections/`. Parse each
JSON file and access fields directly from the `data` object. If required section JSON files do not exist, inform the user and suggest
running `/profile-init` or `profile-section` to generate them.

- `sections/identity.json` — bio, links
- `sections/summary.json` — professional summary
- `sections/skills.json` — tech stack
- `sections/open-source.json` — projects and contributions
- `sections/blogs.json` — blog posts

### 3. Apply Presentation Preferences

Read `preferences.md` from the workspace root. If it exists:

1. Read the `## Global` section — these apply to all reviews.
2. Read the `## GitHub` section (if present) — these are GitHub-specific.
3. Adjust review criteria based on preferences:
   - If a preference de-emphasizes a section, do not flag its absence as a gap.
   - If a preference specifies tone, evaluate existing content against that tone.
   - If a preference reframes data (e.g., "20+ years"), flag a gap only if the
     platform shows a contradictory value.
4. GitHub-specific preferences take precedence over global if they conflict.

If `preferences.md` does not exist, proceed with default review criteria.

### 4. Compare and Analyze

Compare the fetched GitHub state against the master profile:

- **Bio**: is the GitHub bio aligned with the profile summary?
- **Profile README**: does it reflect current skills, projects, and
  contributions from the master profile?
- **Pinned repos**: are the most notable repos from `sections/open-source.json`
  pinned?
- **Missing repos**: are repos listed in the profile actually present on
  GitHub?
- **Stale content**: does the README reference outdated projects or skills?

Consult `${CLAUDE_PLUGIN_ROOT}/skills/github-generate/references/github-readme-conventions.md`
for GitHub profile best practices.

### 5. Verify Preferences Compliance

Before writing the report, re-read the applicable preferences and verify:
- Gap analysis does not flag items the user chose to de-emphasize.
- Tone/style suggestions align with the user's stated preferences.
- Rewrite suggestions (if any) reflect the user's preferred framing.
If any preference was missed or contradicted, revise the report before proceeding.

### 6. Generate Review Report

Produce a structured review with:

- **Summary**: overall assessment of GitHub profile completeness
- **Profile README review**: what's good, what's missing, what's outdated
- **Pinned repos review**: suggestions for which repos to pin/unpin
- **Bio review**: suggested improvements
- **Specific suggestions**: concrete recommendations with priority ranking

### 7. Write Output

Write the review report to `github-review.md` and display it
in the conversation.

## Output Checklist

Before finishing, verify:

- [ ] Master profile sections read from JSON files
- [ ] TBD values in master profile excluded from gap analysis
- [ ] All findings reference specific master profile data
- [ ] Suggestions are actionable and specific
- [ ] Report written to `github-review.md`
- [ ] Review criteria and suggestions honor all applicable presentation preferences

## Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/skills/github-generate/references/github-readme-conventions.md`** — GitHub README conventions and badge syntax

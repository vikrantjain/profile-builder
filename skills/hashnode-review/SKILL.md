---
name: hashnode-review
description: >
  This skill should be used when the user asks to "review my Hashnode profile",
  "check my Hashnode", "audit my Hashnode profile", "compare Hashnode with my
  profile", "what's missing on my Hashnode", or wants their current Hashnode
  profile reviewed against the master profile data to identify gaps and
  improvement opportunities.
---

# Hashnode Review

Review the user's current Hashnode profile by fetching it via the Hashnode
public GraphQL API and comparing it against the master profile data.

## When to Use

Invoke this skill after the user has updated their Hashnode profile and
wants to verify completeness against the master profile. For generating
Hashnode-ready profile content to paste, use the `hashnode-generate` skill
instead.

## Workflow

### 1. Fetch Hashnode Profile Data

Use WebFetch to query the Hashnode public GraphQL API at
`https://gql.hashnode.com`. No authentication is required for public
profile data.

Determine the Hashnode username from `sections/identity.md` or ask
the user.

Fetch the profile with a query like:

```graphql
query {
  user(username: "<hashnode-username>") {
    name
    username
    tagline
    bio {
      text
    }
    profilePicture
    location
    availableFor
    socialMediaLinks {
      github
      twitter
      linkedin
      website
      stackoverflow
      facebook
      youtube
    }
    badges {
      name
      description
    }
    followersCount
    followingsCount
    posts(page: 1, pageSize: 10) {
      nodes {
        title
        slug
        publishedAt
        tags {
          name
        }
      }
    }
  }
}
```

Save all fetched API responses to `.profile/tmp/{YYYY-MM-DD}/hashnode/`
where `{YYYY-MM-DD}` is today's date. Create this directory structure if it
does not exist.

If the GraphQL API is unreachable, inform the user and suggest they
provide their Hashnode profile URL for a WebFetch-based fallback
(scrape the public profile page).

### 2. Read Master Profile

Read the relevant profile sections from `sections/`:

- `sections/identity.md` — name, links, social profiles
- `sections/summary.md` — professional summary
- `sections/skills.md` — tech stack
- `sections/blogs.md` — published blog posts

### 3. Apply Presentation Preferences

Read `preferences.md` from the workspace root. If it exists:

1. Read the `## Global` section — these apply to all reviews.
2. Read the `## Hashnode` section (if present) — these are Hashnode-specific.
3. Adjust review criteria based on preferences:
   - If a preference de-emphasizes a section, do not flag its absence as a gap.
   - If a preference specifies tone, evaluate existing content against that tone.
   - If a preference reframes data (e.g., "20+ years"), flag a gap only if the
     platform shows a contradictory value.
4. Hashnode-specific preferences take precedence over global if they conflict.

If `preferences.md` does not exist, proceed with default review criteria.

### 4. Compare and Analyze

Compare the fetched Hashnode state against the master profile:

- **Tagline**: is it aligned with the professional title/summary?
- **Bio**: does it reflect the current professional summary?
- **About page**: is it comprehensive and up to date? (if fetchable)
- **Tech stack tags**: do they match the skills in the master profile?
- **Social links**: are all relevant links present and correct?
- **Blog posts**: are posts listed in `sections/blogs.md` published on
  Hashnode? Are there posts on Hashnode not yet captured in the master
  profile?

Consult `${CLAUDE_PLUGIN_ROOT}/skills/hashnode-generate/references/hashnode-constraints.md`
for Hashnode profile best practices.

### 5. Verify Preferences Compliance

Before writing the report, re-read the applicable preferences and verify:
- Gap analysis does not flag items the user chose to de-emphasize.
- Tone/style suggestions align with the user's stated preferences.
- Rewrite suggestions (if any) reflect the user's preferred framing.
If any preference was missed or contradicted, revise the report before proceeding.

### 6. Generate Review Report

Produce a structured review with:

- **Summary**: overall assessment of Hashnode profile completeness
- **Profile fields review**: tagline, bio, about — what's good, what's
  missing, what's outdated
- **Tech stack review**: tags to add or remove
- **Social links review**: missing or incorrect links
- **Blog sync check**: posts on Hashnode not in master profile, and
  posts in master profile not on Hashnode
- **Specific suggestions**: concrete recommendations with priority
  ranking (high/medium/low)

### 7. Write Output

Write the review report to `hashnode-review.md` and display it in the
conversation.

## Output Checklist

Before finishing, verify:

- [ ] All findings reference specific master profile data
- [ ] Suggestions are actionable and specific
- [ ] Blog sync differences are listed in both directions
- [ ] Report written to `hashnode-review.md`
- [ ] Review criteria and suggestions honor all applicable presentation preferences

## Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/skills/hashnode-generate/references/hashnode-constraints.md`** — Hashnode profile field limits and formatting rules

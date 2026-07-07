---
name: hashnode-review
description: >
  Review and assess the quality of the user's live Hashnode profile with
  actionable improvement suggestions. Use when the user asks to "review my
  Hashnode", "check my Hashnode profile", "audit my Hashnode", "how does my
  Hashnode look", "improve my Hashnode profile", "Hashnode profile feedback",
  "critique my Hashnode", "is my blog profile good enough", "compare Hashnode
  with my profile", "what's missing on my Hashnode", or wants a quality
  assessment of their Hashnode presence. Also trigger when the user mentions
  Hashnode in the context of wanting feedback, growing their blog audience,
  or strengthening their technical writing brand — even if they don't say
  "review". For generating Hashnode-ready profile content to paste, use the
  `hashnode-generate` skill instead.
---

# Hashnode Review

Review the user's live Hashnode profile to assess how effectively it
establishes their writer identity and produce **actionable improvement
suggestions** with concrete rewrites. The master profile provides context
for the user's full background — the domains, systems, and projects their
Hashnode presence should be drawing credibility from.

This is a **quality and impact review, not a data sync check**. The central
question for every field is: "Given what this person has actually built and
written (per the master profile), how well does their Hashnode profile
convince a reader to click through and follow?" A brief gap check catches
missing or outdated content — and a blog sync check in both directions,
since blogs are a dynamic section — but the bulk of the review evaluates
effectiveness and provides before/after rewrites.

The audience matters: Hashnode readers are developers deciding in seconds
whether a writer knows their domain. The tagline and bio are the storefront;
review them with the weight they carry.

## Workflow

### 1. Fetch Hashnode Profile Data

Use WebFetch to query the Hashnode public GraphQL API at
`https://gql.hashnode.com`. No authentication is required for public
profile data.

Determine the Hashnode username from `sections/identity.json` or ask
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

Read `profile-index.json` to discover available sections and their paths.
Then read the section JSON files needed for review context. Parse each file
and access fields from the `data` object.

| Section file | What it provides for the review |
|---|---|
| `sections/identity.json` | Name, links, social profiles — benchmark for social links |
| `sections/summary.json` | Professional summary — raw material the tagline/bio should distill |
| `sections/skills.json` | Full skill inventory — benchmark for tech stack tags |
| `sections/experience.json` | Career depth and scale signals the about page could be using |
| `sections/open-source.json` | Projects — credibility signals for the about page |
| `sections/blogs.json` | Published posts — for the two-way sync check |

If key section files don't exist, inform the user and suggest running
`/profile-init` or `/profile-section` to generate them. The review can still
proceed as a general quality assessment, but master-profile-informed
insights will be limited.

### 3. Load Presentation Preferences

Read `preferences.md` from the workspace root. If it exists:

1. Read `## Global` — applies to all reviews.
2. Read `## Hashnode` (if present) — Hashnode-specific overrides.
3. Adjust review criteria:
   - De-emphasized sections: don't flag as needing improvement.
   - Tone preferences: evaluate content against the user's preferred tone.
   - Data reframing (e.g., "20+ years"): evaluate against that framing,
     not raw data.
4. Hashnode-specific preferences take precedence over global on conflicts.

If `preferences.md` does not exist, use default review criteria and note in
the report header: "No preferences file found — using default review
criteria."

### 4. Quality Review

This is the core of the skill. For each profile field, evaluate its
effectiveness at establishing writer credibility. The master profile is the
lens — it shows what domains, systems, and projects the user *could* be
drawing on, which makes a thin or generic profile visible as underselling.

Consult `${CLAUDE_PLUGIN_ROOT}/skills/hashnode-generate/references/hashnode-constraints.md`
for field limits and best practices.

Rate each field on a 3-point scale and use the rating as a prefix:

- **Strong** — effectively communicates value, minor tweaks at most
- **Needs work** — decent foundation but missing impact, clarity, or key content
- **Weak** — significantly underperforming or missing; priority rewrite

##### Tagline

The tagline appears on every post card and in search results — it is the
single most-seen field.

- Does it signal what the person builds and writes about, or is it a
  trimmed job title ("Senior Software Engineer at Acme")?
- Does it include 1–2 domain/technology signals a reader could match to
  their own interests?
- Is it using its budget well (aim 100–140 of the 150 chars) without
  being padded?
- **Master profile angle**: Compare against `summary.json` and
  `skills.json`. Is the tagline generic where the profile shows real
  specialization?

##### Bio

- Does it complement the tagline with a different angle (career depth,
  writing focus, a differentiator) rather than restating it?
- Does it make a reader think "this person has real experience behind
  their posts"?
- **Master profile angle**: Are the strongest credibility signals
  (years, scale, patents, notable projects) from `experience.json` and
  `summary.json` being used?

##### About page

- Is it a structured, scannable document (intro hook, what-I-write-about,
  tech stack, featured work, links) or a pasted corporate bio?
- Does the opening establish a technical identity specific enough to be
  interesting?
- Does it reward the reader who clicked through from a post — more depth,
  more links, recent articles?
- **Master profile angle**: Compare against `experience.json` and
  `open-source.json`. Is available substance (systems built, scale
  operated at, projects shipped) missing from the page?

##### Tech stack tags

- Curated to the 5–10 technologies the writer actually has opinions
  about, or a dump?
- Do the tags match what the person writes about (per their posts' tags)?
- **Master profile angle**: Compare against `skills.json` — are
  identity-defining technologies missing? Are generic tools wasting slots?

##### Social links

- Are the high-value links present (GitHub above all, for a technical
  writer; plus website/LinkedIn)? Are any broken or pointing to dead
  profiles?
- **Master profile angle**: Cross-check against `identity.json`.

##### Overall coherence

- Do tagline, bio, about page, and tags tell one consistent story about
  what this writer covers?
- Would a reader who liked one post immediately understand what following
  this writer gets them?
- **Master profile angle**: Is there a significant mismatch between how
  strong the user's actual background is and how the Hashnode profile
  reads?

### 5. Gap and Blog Sync Check

A brief check — not an exhaustive comparison. Flag only items that would
meaningfully improve impact:

- Missing or outdated profile fields (empty tagline, stale about page)
- Social links present in the master profile but absent on Hashnode

**Blog sync (both directions)** — blogs are a dynamic section, so this
check earns its place here:

- Posts on Hashnode not yet captured in `sections/blogs.json` → suggest
  running `profile-refresh`.
- Posts in `sections/blogs.json` attributed to Hashnode but not returned
  by the API → flag for the user (deleted, unpublished, or moved).

Exclude any master profile value that is exactly `"TBD"` or `["TBD"]` —
these are unfilled placeholders.

### 6. Verify Preferences Compliance

Before generating the report, re-read applicable preferences and verify:

- Suggestions align with the user's tone and framing preferences.
- Rewrite suggestions reflect the user's preferred style.
- De-emphasized sections are not flagged as needing work.

If any preference is missed or contradicted, adjust before proceeding.

### 7. Generate Review Report

Produce a structured review report:

**1. Executive Summary** — 2–3 sentence overall assessment: strong
impression, adequate but underperforming, or needs significant work.
Include a one-line statement of the biggest opportunity.

**2. Field-by-Field Review** — For each field in section 4:

- **Rating**: Strong / Needs work / Weak
- **Current state**: brief description of what's there
- **Assessment**: how effective it is, informed by what the master profile
  shows they could be saying
- **Suggestions with rewrites**: concrete changes — provide before/after
  text for anything rated Needs work or Weak. Always provide full rewrite
  drafts for the tagline and bio, with character counts. For tags, name
  the exact add/remove changes.

**3. Blog Sync Findings** — differences in both directions, with the
suggested action for each.

**4. Priority Actions** — Numbered list of the top 5–10 changes ranked by
impact. Each item: what to change, why it matters, and effort level
(quick fix / moderate / significant rewrite).

### 8. Write Output

Write the review report to `hashnode-review.md` and display it in the
conversation.

## Output Checklist

Before finishing, verify:

- [ ] Fetched API responses saved to `.profile/tmp/{YYYY-MM-DD}/hashnode/`
- [ ] Master profile read via `profile-index.json` to discover sections
- [ ] TBD values excluded from gap analysis
- [ ] Every field rated (Strong / Needs work / Weak)
- [ ] Before/after rewrites provided for tagline and bio, with character counts
- [ ] Tag suggestions name exact add/remove changes
- [ ] Blog sync differences listed in both directions with suggested actions
- [ ] Priority actions ranked by impact with effort levels
- [ ] Report written to `hashnode-review.md`
- [ ] All suggestions honor applicable presentation preferences

## Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/skills/hashnode-generate/references/hashnode-constraints.md`** — Hashnode profile field limits and formatting rules

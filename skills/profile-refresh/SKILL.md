---
name: profile-refresh
description: >
  This skill should be used when the user asks to "refresh my blogs", "refresh
  open source", "fetch latest blog posts", "update blogs from hashnode", "sync
  my open source data", "pull latest from github", "refresh sources", or wants
  to fetch the latest data from external platforms (GitHub, Hashnode, Dev.to)
  and update the corresponding profile sections. Also called by profile-section
  when building or updating dynamic sections (blogs, open_source).
---

# Profile Refresh

Fetch latest data from configured external platforms and update the
corresponding profile section files. Targets dynamic sections whose
content lives on external platforms and changes over time.

## When to Use

Invoke this skill when:

- The user explicitly asks to refresh or sync a dynamic section.
- The `profile-section` skill is building or updating a dynamic section
  (blogs, open_source) and needs current data from the source platform.

Do **not** invoke this skill from `profile-assemble` or any export/review
skill. Those consume section files as-is.

## Dynamic Sections

Only these sections have external sources:

| Section | Typical Sources |
|---------|----------------|
| blogs | Hashnode, Dev.to |
| open_source | GitHub (projects + contributions) |

All other sections (identity, summary, experience, skills, education,
certifications, patents, languages) are static — maintained from
user-provided data only.

## Tool Constraints

This skill must **not** use Playwright or any browser automation. All external
data fetching uses CLI tools and public APIs only:

- **GitHub** — `gh` CLI (via Bash) or GitHub REST API (via WebFetch)
- **Hashnode** — GraphQL API at `gql.hashnode.com` (via WebFetch)
- **Dev.to** — REST API at `dev.to/api` (via WebFetch)

## Workflow

### 1. Read Source Configuration

Read and parse `profile-index.json`. Locate the `sources` array. Each entry
contains:

- **`platform`** — the source type (github, hashnode, devto)
- **`handle`** — the user's username on that platform
- **`feeds`** — array of section keys this source feeds

If `profile-index.json` does not exist or has no `sources` array, inform
the user to generate the profile first or add source configuration to
their index.

### 2. Determine Target

Accept a section name from the user (e.g., `blogs`, `open_source`)
or `all` to refresh every dynamic section.

If the user says `all`, iterate through each unique section listed in the
`feeds` arrays. Otherwise, filter the `sources` array to entries whose `feeds`
include the target section.

### 3. Fetch Data from Sources

For each source that feeds the target section, fetch data using the
platform-specific method below.

#### GitHub

Use the `gh` CLI or GitHub REST API via WebFetch.

**Repositories** (feeds: open_source):

```
gh api /users/{handle}/repos --paginate -q '.[] | {name, description, html_url, language, stargazers_count, fork, archived, topics}'
```

- Exclude forks unless they have significant contributions (stars > 0 or
  the user is listed as a contributor).
- Include archived repos with `status: archived`.
- Sort by stargazers_count descending, then by updated_at descending.

**Contributions** (feeds: open_source):

```
gh api "/search/issues?q=author:{handle}+type:pr+is:merged+-user:{handle}&sort=created&order=desc&per_page=30"
```

- Only include merged PRs to repos the user does not own.
- Extract: project name, PR URL, title, repo description.

#### Hashnode

Use WebFetch to query the Hashnode GraphQL API.

**Endpoint:** `https://gql.hashnode.com`

**Query:**

```graphql
query {
  publication(host: "{handle}.hashnode.dev") {
    posts(first: 20) {
      edges {
        node {
          title
          url
          publishedAt
          brief
        }
      }
    }
  }
}
```

If the query returns no publication (null response), the user may have a custom
domain. Retry with the handle value used as-is in the `host` parameter (e.g.,
`publication(host: "blog.example.com")`) — the handle field in `sources` may
contain a full custom domain instead of a bare username.

- Map `publishedAt` to `published_on` (format: Mon YYYY).
- Map `brief` to `excerpt` (truncate to one sentence if longer).
- Set `platform` to "Hashnode".

#### Dev.to

Use WebFetch.

**Endpoint:** `https://dev.to/api/articles?username={handle}&per_page=30`

- Map `title`, `url`, `published_at` → `published_on`, `description` → `excerpt`.
- Set `platform` to "Dev.to".

### 4. Read Existing Section

Read the current section JSON file from `sections/` (e.g.,
`sections/blogs.json`). Parse the JSON and extract the data array from the
`data` object (e.g., `data.blogs` for blogs, `data.open_source.projects` and
`data.open_source.contributions` for open_source).

If the file does not exist, treat this as an initial population. If it exists
as a legacy `.md` file, treat the fetched data as the baseline — do not
attempt to parse old Markdown content.

### 5. Diff and Merge

Compare fetched data against existing section content:

- All comparisons are done on the parsed JSON arrays.
- **Match on natural key:** URL for blogs, URL for open_source projects,
  PR URL for contributions.
- **New entries:** Prepend to the list (most recent first).
- **Existing entries:** Update factual fields from the source (description,
  star count, language, topics) but preserve any manual enrichments the
  user has added (hand-written contributions/impact, custom descriptions that
  differ substantially from the API description).
- **Entries in profile but not in source:** Keep them. Never auto-remove.
  The user may have intentionally retained historical data.

### 6. Build the JSON Object

Read `${CLAUDE_PLUGIN_ROOT}/profile-template.md` and extract the field definitions and
`json_structure` conventions for the target section. Construct a JSON object
using the same rules as `profile-section` Step 5:

```json
{
  "section": "<blogs | open_source>",
  "data": {
    "<field_name>": "<merged data>"
  }
}
```

- Use field names exactly as defined in `profile-template.md`.
- List fields → JSON arrays. String fields → JSON strings.
- No Markdown formatting in values — values are raw data.
- Optional fields with no data → `null` or omit. Do not set optional fields to `"TBD"`.

### 7. Write and Update Index

- Write the JSON object to its output path (e.g., `sections/blogs.json`).
- Read and parse `profile-index.json`. Find or add the entry in the `sections`
  array for this section. Update `last_updated` to the current date in
  YYYY-MM-DD format and ensure `file` uses the `.json` extension. Write back to `profile-index.json`.

### 8. Report Changes

Summarize what changed:

- Number of new entries added.
- Number of existing entries updated.
- Total entries in the section.
- Any entries that could not be fetched (API errors, rate limits).

## Merge Strategy Summary

| Scenario | Action |
|----------|--------|
| Entry in source, not in profile | Add (prepend) |
| Entry in both, source has updates | Update factual fields, preserve manual enrichments |
| Entry in profile, not in source | Keep (never auto-remove) |
| Duplicate URLs across sources | Deduplicate, prefer the richer entry |

## Output Checklist

Before finishing, verify:

- [ ] JSON is valid and well-formed
- [ ] All required fields present — either with real data or `"TBD"` convention
- [ ] Optional fields with no data use `null` or are omitted (never `"TBD"`)
- [ ] No Markdown formatting characters in string values
- [ ] New entries appear before existing entries (most recent first)
- [ ] No entries were removed from the existing section
- [ ] Manual enrichments in existing entries are preserved
- [ ] Section file written to the correct `sections/` path (`.json` extension)
- [ ] `profile-index.json` sections array updated with current date
- [ ] Change summary reported to the user

## Reference Files

- **`profile-index.json`** — Source configuration (`sources` array) and section manifest (`sections` array)
- **`${CLAUDE_PLUGIN_ROOT}/profile-template.md`** — Field definitions, section mapping, and JSON structure conventions

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

## Critical: This Is a Data Layer Operation

The profile is a **comprehensive canonical data layer**. When refreshing
sections from external sources:

- **Include every item** returned by the API. Do not drop repos, posts, or PRs
  because they seem old or minor.
- **Preserve all existing entries** — never auto-remove items that are already
  in the profile but absent from the API response (deleted posts, transferred
  repos, etc.). The user may have intentionally retained them.
- **Do not fabricate data** — only write what the API returns. If a field is
  missing from the API response, set it to `null` (optional) or `"TBD"`
  (required) rather than inventing a value.

## When to Use

Invoke this skill when:

- The user explicitly asks to refresh or sync a dynamic section.
- The `profile-section` skill is building or updating a dynamic section
  (blogs, open_source) and needs current data from the source platform.

Do **not** invoke this skill from `profile-assemble` or any export/review
skill. Those consume section files as-is.

## Dynamic Sections

Only these sections have external sources:

| Section | Typical Sources | Output File |
|---------|----------------|-------------|
| blogs | Hashnode, Dev.to | `sections/blogs.json` |
| open_source | GitHub (projects + contributions) | `sections/open-source.json` |

All other sections are static — maintained from user-provided data only.

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
the user to run `/profile-init` first or manually add source configuration
to their index.

### 2. Determine Target

Accept a section name from the user (e.g., `blogs`, `open_source`)
or `all` to refresh every dynamic section.

If the user says `all`, iterate through each unique section listed in the
`feeds` arrays. Otherwise, filter the `sources` array to entries whose `feeds`
include the target section.

### 3. Fetch Data from Sources

For each source that feeds the target section, fetch data using the
platform-specific method below. If a fetch fails, report the error for that
source and continue with the remaining sources — a single failure should not
block the entire refresh.

#### GitHub

**Tool selection:** Try the `gh` CLI first (via Bash). If it is not installed
or not authenticated (`gh auth status` fails), fall back to the GitHub REST
API via WebFetch. Both approaches hit the same endpoints — the only difference
is the transport.

To detect availability, run:

```bash
gh auth status 2>&1
```

If this exits non-zero or the command is not found, use WebFetch for all
GitHub calls.

**Repositories** (feeds: open_source):

*With `gh` CLI:*

```bash
gh api "/users/{handle}/repos?per_page=100&sort=updated&direction=desc" \
  --paginate --slurp \
  --jq '[.[][] | {name, description, html_url, language, stargazers_count, fork, archived, updated_at, created_at}]'
```

Key points about `--paginate` and `--slurp`:
- `--paginate` follows `Link` headers to fetch all pages automatically.
- `--slurp` collects all pages into a single JSON array of arrays, which the
  `--jq` filter then flattens with `.[][]`.
- Without `--slurp`, each page outputs a separate JSON array — concatenated
  output is not valid JSON.

*With WebFetch (fallback):*

Fetch `https://api.github.com/users/{handle}/repos?per_page=100&sort=updated&direction=desc`.
The response is a JSON array. If the response includes a `Link` header with
`rel="next"`, follow it to fetch subsequent pages. Concatenate all page arrays
into one. Extract the same fields: `name`, `description`, `html_url`,
`language`, `stargazers_count`, `fork`, `archived`, `updated_at`, `created_at`.

Filter and sort the results:

- **Exclude forks** unless `stargazers_count > 0` (indicates the fork has
  independent traction). When in doubt, include the fork — the user can remove
  it manually.
- **Include archived repos** with `status: "archived"` in the output.
- **Sort** by `stargazers_count` descending, then `updated_at` descending.

For repos that appear significant (stars > 5 or non-fork), optionally fetch
topics in a follow-up call since the list endpoint does not return them:

```bash
gh api "/repos/{handle}/{repo_name}/topics" --jq '.names'
```

Or via WebFetch: `https://api.github.com/repos/{handle}/{repo_name}/topics`
(returns `{ "names": [...] }`).

Only do this for the top ~10 repos to avoid excessive API calls.

**Contributions** (feeds: open_source):

Fetch merged PRs to repos the user does not own.

*With `gh` CLI:*

```bash
gh api "/search/issues" \
  --method GET \
  -f "q=author:{handle} type:pr is:merged -user:{handle}" \
  -f "sort=created" -f "order=desc" -f "per_page=30" \
  --jq '.items | [.[] | {title, html_url, created_at, repository_url}]'
```

Using `-f` flags for query parameters avoids URL-encoding issues with spaces
and special characters.

*With WebFetch (fallback):*

Fetch `https://api.github.com/search/issues?q=author:{handle}+type:pr+is:merged+-user:{handle}&sort=created&order=desc&per_page=30`.
Extract `items` array from the response, then pick `title`, `html_url`,
`created_at`, and `repository_url` from each item.

The `repository_url` field provides the repo API URL from which you can
extract the project name (last path segment).

- Only include merged PRs to repos the user does not own.
- Extract: project name (from `repository_url`), PR URL (`html_url`), title.
- The search API returns at most 1000 results; 30 per page is a reasonable
  default for profile purposes.

**Note on unauthenticated requests:** The GitHub REST API allows unauthenticated
requests but enforces a lower rate limit (60 requests/hour vs 5000 with a
token). WebFetch calls are unauthenticated unless custom headers are added. If
you hit a 403 rate limit via WebFetch, inform the user and suggest installing
and authenticating the `gh` CLI (`gh auth login`) for higher limits.

**Field mapping to template:**

| API field | Template field (`open_source.projects`) |
|-----------|----------------------------------------|
| `name` | `name` |
| `description` | `description` |
| `html_url` | `url` |
| `language` | `tech_stack` (wrap in array: `[language]`) |
| `stargazers_count` | `impact` (e.g., `["{count} stars"]`) |
| `fork: false` + owned | `role`: `"owner"` |
| `archived: true` | `status`: `"archived"` |
| `archived: false` | `status`: `"active"` |

| API field | Template field (`open_source.contributions`) |
|-----------|----------------------------------------------|
| last path segment of `repository_url` | `project` |
| `html_url` | `url` |
| `title` | `description` |
| (always PR) | `type`: `"PR"` |

#### Hashnode

Use WebFetch to query the Hashnode GraphQL API.

**Endpoint:** `https://gql.hashnode.com`

**Query:**

```graphql
query {
  publication(host: "{handle}.hashnode.dev") {
    posts(first: 50) {
      edges {
        node {
          title
          url
          publishedAt
          brief
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}
```

**Pagination:** If `pageInfo.hasNextPage` is `true`, send a follow-up query
with `posts(first: 50, after: "{endCursor}")` to fetch the next page. Repeat
until `hasNextPage` is `false` or you have fetched 200 posts (safety cap).

**Custom domain fallback:** If the query returns `null` for `publication`,
the user may have a custom domain. Retry with the handle value used as-is in
the `host` parameter (e.g., `publication(host: "blog.example.com")`) — the
handle field in `sources` may contain a full custom domain instead of a bare
username.

**Field mapping to template:**

| API field | Template field (`blogs` item) |
|-----------|------------------------------|
| `title` | `title` |
| `url` | `url` |
| `publishedAt` | `published_on` (format: `Mon YYYY`) |
| `brief` | `excerpt` (truncate to one sentence if longer) |
| (hardcoded) | `platform`: `"Hashnode"` |

#### Dev.to

Use WebFetch.

**Endpoint:** `https://dev.to/api/articles?username={handle}&per_page=100`

**Pagination:** Dev.to supports `page` parameter. If the response returns
exactly `per_page` items, fetch the next page with `&page=2`, etc. Stop when
a page returns fewer items than `per_page` or you reach page 5 (safety cap).

**Field mapping to template:**

| API field | Template field (`blogs` item) |
|-----------|------------------------------|
| `title` | `title` |
| `url` | `url` |
| `published_at` | `published_on` (format: `Mon YYYY`) |
| `description` | `excerpt` |
| (hardcoded) | `platform`: `"Dev.to"` |

### 4. Read Existing Section

Read the current section JSON file from `sections/` (e.g.,
`sections/blogs.json`). Parse the JSON and extract the data array from the
`data` object (e.g., `data.blogs` for blogs, `data.open_source.projects` and
`data.open_source.contributions` for open_source).

- **File does not exist** — treat this as initial population (no merge needed,
  fetched data becomes the baseline).
- **File exists as legacy `.md`** — treat fetched data as the baseline. Do not
  attempt to parse old Markdown content.
- **File exists as `.json`** — parse and use for merge in the next step.

### 5. Diff and Merge

Compare fetched data against existing section content. All comparisons are
done on the parsed JSON arrays.

**Match on natural key:**

| Data type | Natural key |
|-----------|-------------|
| Blog posts | `url` |
| Open source projects | `url` |
| Contributions (PRs) | `url` |

**New entries** (in source, not in profile): Prepend to the list so the most
recent items appear first.

**Updated entries** (in both source and profile): Update only **factual fields**
from the API — these are fields the API is authoritative for:

| Section | Factual fields (always update from API) |
|---------|----------------------------------------|
| blogs | `title`, `url`, `published_on`, `platform` |
| open_source projects | `description` (see below), `url`, `tech_stack`, `status` |
| open_source projects | `impact` entries that are purely star/fork counts |
| contributions | `project`, `url`, `type` |

**Detecting manual enrichments:** Before overwriting a field, compare the
existing value against the API value:

- If the existing `description` contains content that the API description
  does not (extra sentences, technical details, context the user added), keep
  the existing value — it has been manually enriched.
- If the existing value is identical to or a substring of the API value, update
  it from the API (the source has more current data).
- `contributions` and `impact` arrays that contain entries not derivable from
  the API (hand-written work descriptions, manually added metrics) are always
  preserved. Only auto-generated impact values like star counts are updated.
- When in doubt, preserve the existing value. It is safer to keep stale manual
  content than to overwrite the user's work.

**Missing entries** (in profile, not in source): Keep them. Never auto-remove.
The user may have intentionally retained historical data, or the item may have
been removed from the platform but still belongs in the profile.

**Duplicates across sources** (e.g., same blog post on Hashnode and Dev.to):
Match by URL. If two entries have the same URL, keep one. If they have
different URLs but identical titles, keep both — they may be cross-posts with
platform-specific URLs.

### 6. Build the JSON Object

Read `${CLAUDE_PLUGIN_ROOT}/profile-template.md` and extract the field definitions and
`json_structure` conventions for the target section. Construct a JSON object:

```json
{
  "section": "<blogs | open_source>",
  "data": {
    "<field_name>": "<merged data>"
  }
}
```

Rules:

- Use field names exactly as defined in `profile-template.md`.
- List fields → JSON arrays. String fields → JSON strings.
- No Markdown formatting in values — values are raw data.
- Required fields with no data → `"TBD"` (string) or `["TBD"]` (list).
- Optional fields with no data → `null` or omit. Do not set optional fields
  to `"TBD"`.

### 7. Write and Update Index

- Write the JSON object to its output path (e.g., `sections/blogs.json`).
- Read and parse `profile-index.json`. Find or add the entry in the `sections`
  array for this section. Update `last_updated` to the current date in
  YYYY-MM-DD format and ensure `file` uses the `.json` extension. If no entry
  exists for this section, add one with `name`, `key`, `file`, and
  `last_updated`. Write back to `profile-index.json`.

### 8. Report Changes

Summarize what changed:

- Number of new entries added.
- Number of existing entries updated (with which fields changed).
- Total entries in the section after merge.
- Any sources that failed to fetch (with the error — e.g., "GitHub: 403 rate
  limit exceeded", "Hashnode: no publication found for handle 'xyz'").

## Error Handling

API calls can fail for various reasons. Handle these gracefully:

| Error | Action |
|-------|--------|
| **404 / user not found** | Report that the handle may be incorrect. Suggest the user check `profile-index.json` sources. Continue with other sources. |
| **403 / rate limit** | Report the rate limit. For `gh` CLI, suggest `gh auth status` to check token. For Hashnode/Dev.to, suggest waiting and retrying. Continue with other sources. |
| **Network error / timeout** | Report the failure. Continue with other sources. |
| **Empty response** (valid but no data) | This is not an error — the user may have no public repos/posts. Write the section with an empty array. Do not treat it as a failure. |
| **Malformed response** | Report that the API returned unexpected data. Skip this source and continue. |

If **all** sources for a target section fail, do not overwrite the existing
section file. Inform the user that the refresh could not complete and the
previous data is preserved.

## Merge Strategy Summary

| Scenario | Action |
|----------|--------|
| Entry in source, not in profile | Add (prepend) |
| Entry in both, factual fields changed | Update factual fields |
| Entry in both, has manual enrichments | Preserve enriched fields, update only factual fields |
| Entry in profile, not in source | Keep (never auto-remove) |
| Duplicate URLs across sources | Deduplicate, prefer the richer entry |
| All sources failed | Preserve existing section file unchanged |

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

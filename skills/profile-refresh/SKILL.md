---
name: profile-refresh
description: >
  Pulls new entries from external platforms (GitHub, Hashnode, Dev.to) into
  the user's dynamic profile sections (blogs, open_source). Use when the user
  asks to "refresh my blogs", "refresh open source", "fetch latest blog
  posts", "update blogs from hashnode", "sync my open source data", "pull
  latest from github", "refresh sources", "rescan readme for {repo}", or asks
  whether their blog or open-source data is up to date. Additive by default —
  new entries are added and existing curated entries are preserved. Also
  called by profile-section when building or updating dynamic sections.
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
- **Open source projects/contributions are not re-refreshed by default** —
  existing entries are left as the user has curated them; refresh's job is to
  surface new work. Opt-in re-refresh is available on explicit request (see
  "Diff and Merge"). Blogs continue to update factual fields from the API.

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

Each platform has a recipe doc in `references/`. Read the relevant doc
**before issuing any API call** — it carries the parameter choices, filters,
pagination logic, and field mappings. The summaries below cover only the
load-bearing decisions a workflow-level reader needs to see; everything else
lives in the reference.

#### GitHub — see `references/github.md`

Feeds `open_source` (projects + contributions). Recipe covers:

- Tool selection: prefer `gh` CLI; fall back to REST API via WebFetch if `gh`
  is missing or unauthenticated.
- Repository fetch (with `--paginate --slurp`), fork/archived filtering,
  star-then-recency sort.
- Topics fetch — top ~10 repos only.
- README fetch — used by the README enrichment step (see "README enrichment
  for tech_stack" below in this section).
- Contributions fetch — merged PRs to repos the user does not own.
- Field mapping for `open_source.projects` and `open_source.contributions`.

Two workflow-level constraints to keep in mind without opening the recipe:

- **Topics and README fetches are capped at ~10 repos** to avoid burning API
  budget.
- **Unauthenticated WebFetch is rate-limited at 60 req/hour.** If you hit a
  403, suggest `gh auth login` and continue with what you have.

##### README enrichment for tech_stack

> **Timing:** Invoked from Section 5 (Diff and Merge) *after* the existing
> section file has been read and the new-vs-existing diff is known. Do not
> fetch READMEs as part of the initial repo fetch — most repos are usually
> already in the profile, and fetching their READMEs only to discard the
> data wastes API budget.

README enrichment runs in only two cases:

1. **New project** being added during refresh — the project is in the API
   response but not in the existing section file, so `tech_stack` is being
   created from scratch and there is nothing to overwrite. Fetch the README
   so the user gets a meaningful starting list instead of a single language
   tag.
2. **Existing project**, but only when the user **explicitly asks** for it.
   Trigger phrases: "refresh open source and check the readmes", "enrich
   tech stack from github readmes", "rescan readme for {repo}", "update
   tech stack for {repo}". When opt-in is triggered, fetch the README for
   the targeted repos and merge extracted tech into the existing
   `tech_stack` per "Opt-in re-refresh of existing open_source entries" in
   Section 5. If the user does not name specific repos, default to the top
   ~10 by stars.

In a default refresh, do **not** fetch READMEs for existing projects and do
**not** modify their `tech_stack`. Silently rewriting curated lists on every
refresh would destroy the user's work.

For the README fetch recipe, what to extract, and how to combine it with
language + topics, see the "README — fetch and tech_stack extraction"
section of `references/github.md`.

#### Hashnode — see `references/hashnode.md`

Feeds `blogs`. Recipe covers the GraphQL query, pagination, the
custom-domain fallback, and field mapping.

#### Dev.to — see `references/devto.md`

Feeds `blogs`. Recipe covers the REST endpoint, pagination, and field
mapping.

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
recent items appear first. For new open_source projects, build `tech_stack`
using language + topics + README extraction (see "Combining into `tech_stack`
for a new project" in `references/github.md`). For new blog entries and
contributions, populate all factual fields from the API.

While merging, **track the set of tech_stack entries newly introduced to
the section** — that is, every tech in a new project's `tech_stack`, plus
any tech added during opt-in re-enrichment of an existing project. This
set is used by Section 8 to surface skills suggestions. Default refresh of
an existing project introduces no new tech (its `tech_stack` is untouched),
so the set stays empty for that case.

**Open source — existing entries are not refreshed by default.**

For open_source projects and contributions that already exist in the section
file (matched by `url`), leave the entry **completely untouched** during a
default refresh. Do not update `description`, `tech_stack`, `impact`,
`status`, `role`, or any other field — even if the API value differs.

The reasoning: a project's GitHub metadata is authoritative on the day it
was first added, but the user almost always edits these fields afterward to
reframe the project for their profile (sharper description, curated
`tech_stack`, manually added `impact` metrics, role notes). Re-applying API
values on every refresh would silently overwrite that work. The user is the
authority on how their existing projects are presented; refresh's job is
just to surface new work.

**Opt-in re-refresh of existing open_source entries.**

If the user explicitly asks to refresh a specific project (e.g., "update the
description on {repo} from github", "rescan readme for {repo}", "refresh
star count for {repo}"), do refresh the requested fields for the requested
projects only. Two flavors:

- *Field-targeted re-refresh* (`description`, `status`, star-count `impact`):
  overwrite the named field from the API value. Leave other fields alone.
- *Tech stack re-enrichment* ("rescan readme", "enrich tech stack"): fetch
  the README and merge extracted tech into the existing `tech_stack` as a
  union. Deduplicate case-insensitively (`React` and `react` are the same;
  `Next.js` and `nextjs` are the same). When a duplicate is found, **prefer
  the existing entry's casing** — it reflects how the user has chosen to
  present the technology. Append new entries to the end, preserving existing
  order. Never remove entries from `tech_stack` on re-enrichment — a tech
  the user added by hand may not appear in the current README but was still
  used.

**Blogs — existing entries: update factual fields, preserve enrichments.**

For blog entries that exist in both source and profile, update **factual
fields** the API is authoritative for: `title`, `url`, `published_on`,
`platform`. Preserve manually enriched fields (e.g., a hand-edited
`excerpt`).

Detecting manual enrichments on `excerpt`: if the existing value contains
content the API value does not (extra sentences, hand-written framing),
keep the existing value. If the existing value is identical to or a
substring of the API value, update from the API. When in doubt, preserve.

**Missing entries** (in profile, not in source): Keep them. Never auto-remove.
The user may have intentionally retained historical data, or the item may have
been removed from the platform but still belongs in the profile. The user
can manually remove entries (or ask you to remove them) if needed.

**Duplicates across sources** (e.g., same blog post on Hashnode and Dev.to):
Match by URL. If two entries have the same URL, keep the richer one — the
entry with more populated fields (excerpt, tags, etc.); when equally rich,
keep the existing profile entry. If they have different URLs but identical
titles, keep both — they may be cross-posts with platform-specific URLs.

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

**No-op detection:** Before writing, compare the merged JSON object against
the existing section file content. If they are identical (no entries added,
no entries updated), this is a no-op refresh:

- Do **not** rewrite the section file. Leaving it untouched preserves its
  mtime and avoids spurious diffs in version control.
- Do **not** bump `last_updated` in `profile-index.json`. Bumping it on a
  no-op would falsely imply the data changed today; if a user later sorts
  sections by `last_updated` to find stale data, the field needs to mean
  "data last actually changed," not "last checked."
- Skip straight to Step 8 (Report Changes).

**On actual change:**

- Write the JSON object to its output path (e.g., `sections/blogs.json`).
- Read and parse `profile-index.json`. Find or add the entry in the `sections`
  array for this section. Update `last_updated` to the current date in
  YYYY-MM-DD format and ensure `file` uses the `.json` extension. If no entry
  exists for this section, add one with `name`, `key`, `file`, and
  `last_updated`. Write back to `profile-index.json`.

### 8. Report Changes

Summarize the refresh outcome. The shape of the report depends on whether
anything changed:

**No-op refresh** (nothing added, nothing updated):

> Checked {sources}. No new entries found. Section unchanged since
> {existing last_updated}. Total entries: {N}.

**Refresh with changes:**

- Number of new entries added (with brief identifiers, e.g., "1 new
  contribution: camunda/connectors#7022").
- Number of existing entries updated, with which fields changed. For
  open_source this counts only opt-in re-refresh changes — default refresh
  never touches existing entries.
- Total entries in the section after merge.

**Failures (always report regardless of changes):**

- Any sources that failed to fetch, with the error (e.g., "GitHub: 403 rate
  limit exceeded", "Hashnode: no publication found for handle 'xyz'").

**Skills suggestions (only when new tech_stack entries were introduced):**

If the "newly introduced tech" set tracked in Section 5 is non-empty, surface
candidates the user might want to add to their `skills` section. Steps:

1. Read `sections/skills.json` (if it exists). Collect every entry in
   `skills.categories[*].items` plus `skills.soft` into a single set,
   normalized to lowercase.
2. For each tech in the newly introduced set, check whether it already
   appears in that set (case-insensitively, ignoring punctuation/spacing
   differences — `Next.js`, `nextjs`, and `next-js` all match).
3. Anything not already present is a candidate.

Report candidates grouped by their source project, in plain prose:

> **Skills suggestions:** Project `claude-session-profiler` introduced new
> tech not in your skills section: **Python**, **asciinema**, **uv**.
> Want me to add any of these via `profile-section`? You can also tell me
> which to skip (some build-tool entries may not be worth listing as
> skills).

If `sections/skills.json` does not exist, skip this step — the user has
not built their skills section yet, and `/profile-init` or `profile-section`
will populate it from scratch.

Do **not** modify `sections/skills.json` from this skill. Suggestions are
advisory; the user (or a follow-up `profile-section` call) is the authority
on what becomes a claimed skill.

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
| New entry in source, not in profile | Add (prepend). New open_source projects get `tech_stack` from language + topics + README. |
| Existing open_source entry (in both) | Leave untouched (default). Opt-in re-refresh per Section 5. |
| Existing blog entry (in both) | Update factual fields from API; preserve manual `excerpt` enrichments |
| Entry in profile, not in source | Keep (never auto-remove) |
| Duplicate URLs across sources | Deduplicate, prefer the richer entry |
| All sources failed | Preserve existing section file unchanged |

## Output Checklist

Before finishing, verify:

- [ ] JSON is valid and well-formed; required/optional field conventions respected (`"TBD"` only for required fields without data; optional fields use `null` or omission)
- [ ] No Markdown formatting characters in string values
- [ ] New entries prepended (most recent first); no entries removed
- [ ] If the merged content equals the existing file: no rewrite, no `last_updated` bump, no-op reported
- [ ] If content changed: section file written to the correct `sections/` path (`.json` extension) and `last_updated` bumped in `profile-index.json`
- [ ] Change summary reported to the user (per the Section 8 templates)
- [ ] If new tech_stack entries were introduced: skills suggestions surfaced (candidates not already in `sections/skills.json`); `skills.json` was not modified

## Reference Files

- **`profile-index.json`** — Source configuration (`sources` array) and section manifest (`sections` array)
- **`${CLAUDE_PLUGIN_ROOT}/profile-template.md`** — Field definitions, section mapping, and JSON structure conventions

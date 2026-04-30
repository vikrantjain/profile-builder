# GitHub Fetch Recipes

Recipes for fetching repository and contribution data from GitHub. Read this
file before issuing any GitHub API call — the parameter choices and
filters here are load-bearing.

## Tool selection

Try the `gh` CLI first (via Bash). If it is not installed or not
authenticated (`gh auth status` fails), fall back to the GitHub REST API
via WebFetch. Both approaches hit the same endpoints — the only difference
is the transport.

To detect availability:

```bash
gh auth status 2>&1
```

If this exits non-zero or the command is not found, use WebFetch for all
GitHub calls.

**Rate limit note:** Unauthenticated REST API requests are capped at 60/hour
vs 5000/hour with a token. WebFetch calls are unauthenticated unless custom
headers are added. If you hit a 403 rate limit via WebFetch, inform the user
and suggest installing and authenticating the `gh` CLI (`gh auth login`) for
higher limits.

## Repositories (feeds: open_source)

### With `gh` CLI

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

### With WebFetch (fallback)

Fetch `https://api.github.com/users/{handle}/repos?per_page=100&sort=updated&direction=desc`.
The response is a JSON array. If the response includes a `Link` header with
`rel="next"`, follow it to fetch subsequent pages. Concatenate all page arrays
into one. Extract the same fields: `name`, `description`, `html_url`,
`language`, `stargazers_count`, `fork`, `archived`, `updated_at`, `created_at`.

### Filter and sort

- **Exclude forks** unless `stargazers_count > 0` (indicates the fork has
  independent traction). When in doubt, include the fork — the user can
  remove it manually.
- **Include archived repos** with `status: "archived"` in the output.
- **Sort** by `stargazers_count` descending, then `updated_at` descending.

### Topics (top ~10 repos only)

For repos that appear significant (stars > 5 or non-fork), fetch topics in a
follow-up call since the list endpoint does not return them. Cap at the top
~10 repos to avoid excessive API calls.

```bash
gh api "/repos/{handle}/{repo_name}/topics" --jq '.names'
```

Or via WebFetch: `https://api.github.com/repos/{handle}/{repo_name}/topics`
(returns `{ "names": [...] }`).

### README — fetch and tech_stack extraction

Used for **new** projects (always) and **existing** projects (only when the
user opts in to re-enrichment). The decision of *when* to invoke this lives
in SKILL.md ("README enrichment for tech_stack"); this section covers *how*
to fetch and *what* to extract.

#### Fetching — with `gh` CLI

```bash
gh api -H "Accept: application/vnd.github.raw" "/repos/{handle}/{repo_name}/readme" 2>/dev/null
```

#### Fetching — with WebFetch (fallback)

Try `https://raw.githubusercontent.com/{handle}/{repo_name}/HEAD/README.md`
first. If that 404s, try `/README.rst` and `/README` (no extension). If all
fail, skip README enrichment for that repo.

If the README fetch fails (404, rate limit, malformed), fall back to
`[language]` plus topics for new projects. Do not block the refresh on
README failures.

#### What to extract

README enrichment is imperfect — it can pull in adjacent or example tech the
user did not actually work with. Use judgement and lean toward signals that
are most likely to reflect what the project actually uses. In rough order of
signal strength:

- **"Tech Stack" / "Built With" / "Technologies" / "Stack" / "Dependencies"
  sections** — bulleted lists under these headings are usually a clean,
  curated enumeration of the project's technologies. Strongest signal.
- **Badges** — `shields.io` and similar URLs encode the technology in the
  badge label (e.g., `img.shields.io/badge/Next.js-000?logo=nextdotjs`,
  `built%20with-React`). The label segment between `/badge/` and the next
  `-` or `?` is usually the tech name. Strong signal.
- **Install / setup commands** — `pip install ...`, `npm install ...`,
  `gem install ...`, `cargo add ...`, `go get ...`, `apt install ...`.
  Package names usually map to libraries or services worth listing.
- **Code fence languages** — fenced blocks tagged with `python`,
  `typescript`, `dockerfile`, `yaml`, `hcl`, `sql`, etc. indicate languages
  and tools used.
- **Explicit mentions in prose** — frameworks, databases, services, infra
  (Postgres, Redis, Kafka, Docker, Kubernetes, Terraform, AWS Lambda, etc.).
  Weakest signal — avoid pulling in generic English words or technologies
  merely compared against.

#### Combining into `tech_stack` for a new project

1. Start with the GitHub `language` field (the dominant language).
2. Add all `topics` from the topics fetch (if the topics call was made).
3. Add tech extracted from the README.
4. Deduplicate case-insensitively. Two entries that differ only in casing or
   in punctuation/spacing (`Next.js` vs `nextjs`, `Postgres` vs `PostgreSQL`)
   are the same technology — keep one. Prefer the casing as displayed in
   the README or topics, since those are usually how the user/community
   writes it.
5. Cap at 15 entries per project. If pruning is needed, prefer items that
   appear in multiple sources (language + topics + README) over items that
   appear in only one source.

#### Combining for opt-in re-enrichment of an existing project

The merge rules live in SKILL.md ("Opt-in re-refresh of existing
open_source entries") and take precedence. In short:

- Compute the union of the existing `tech_stack` and the newly extracted
  set.
- Deduplicate case-insensitively, **prefer the existing entry's casing**.
- Append new entries to the end, preserving existing order.
- Never remove entries on re-enrichment.

## Contributions (feeds: open_source)

Fetch merged PRs to repos the user does not own.

### With `gh` CLI

```bash
gh api "/search/issues" \
  --method GET \
  -f "q=author:{handle} type:pr is:merged -user:{handle}" \
  -f "sort=created" -f "order=desc" -f "per_page=30" \
  --jq '.items | [.[] | {title, html_url, created_at, repository_url}]'
```

Using `-f` flags for query parameters avoids URL-encoding issues with spaces
and special characters.

### With WebFetch (fallback)

Fetch `https://api.github.com/search/issues?q=author:{handle}+type:pr+is:merged+-user:{handle}&sort=created&order=desc&per_page=30`.
Extract `items` array from the response, then pick `title`, `html_url`,
`created_at`, and `repository_url` from each item.

### Extraction rules

- Only include merged PRs to repos the user does not own.
- Project name is the last path segment of `repository_url`.
- The search API returns at most 1000 results; 30 per page is a reasonable
  default for profile purposes.

## Field mapping to template

### `open_source.projects`

| API field | Template field |
|-----------|---------------|
| `name` | `name` |
| `description` | `description` |
| `html_url` | `url` |
| `language` + `topics` + README extraction | `tech_stack` for new projects only; existing projects' `tech_stack` is left untouched unless the user opts in (see SKILL.md merge logic) |
| `stargazers_count` | `impact` (e.g., `["{count} stars"]`) |
| `fork: false` + owned | `role`: `"owner"` |
| `archived: true` | `status`: `"archived"` |
| `archived: false` | `status`: `"active"` |

### `open_source.contributions`

| API field | Template field |
|-----------|---------------|
| last path segment of `repository_url` | `project` |
| `html_url` | `url` |
| `title` | `description` |
| (always PR) | `type`: `"PR"` |

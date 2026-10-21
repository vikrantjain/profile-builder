# Hashnode Fetch Recipe

Fetch blog posts from a Hashnode blog. Read this file before issuing any
Hashnode request.

Hashnode retired free GraphQL API access on 2026-05-13: every request to
`gql.hashnode.com` now needs a Pro plan, and an unauthenticated request
redirects to an announcement page instead of returning JSON. The public
blog feeds below need no authentication, so they are the default path.

## Resolve the blog host

The `handle` in `profile-index.json` `sources` is either a bare username or
a full custom domain.

- **Contains a dot** (e.g. `blog.example.com`) → use it as the host as-is.
- **Bare username** → the host is `{handle}.hashnode.dev`.

If the default host returns 404, the user probably has a custom domain. Ask
for it rather than guessing, and suggest storing it as the `handle`.

## Default path: RSS + sitemap

Use `curl -sL` via Bash. It returns the raw XML. WebFetch passes the page
through a summarizing model, which can drop or reword items, so use it only
when Bash is unavailable.

### 1. RSS feed: recent posts with metadata

`https://{host}/rss.xml` returns the 20 most recent posts. It has no
pagination. Each `<item>` carries `title`, `link`, `pubDate`, and
`description`.

### 2. Sitemap: the complete post list

`https://{host}/sitemap.xml` is a sitemap index whose `<loc>` entries point
to pages (`sitemap.xml?page=1`, `?page=2`, …). Each page lists post URLs.
Collect every `<loc>` across all pages. Drop the blog root and any non-post
URLs, such as `/tag/…`, `/series/…`, and static pages.

### 3. Fill in posts the RSS feed does not cover

A post can be in the sitemap but missing from both the RSS feed and
`sections/blogs.json`. For each such post, fetch the post page and read
its `<meta>` tags: `og:title`, `article:published_time`, and
`og:description`. On a first population of a long-running blog this can
mean many fetches. Do the most recent ~30 and tell the user how many
remain. They can ask for the rest.

## Optional path: GraphQL with a Pro token

If the user has a Hashnode Pro plan and a personal access token, GraphQL
returns everything in one paginated query. Use `curl`, because WebFetch
cannot send a POST:

```bash
curl -s -X POST https://gql.hashnode.com \
  -H "Content-Type: application/json" \
  -H "Authorization: $HASHNODE_TOKEN" \
  -d '{"query":"{ publication(host: \"{host}\") { posts(first: 50) { edges { node { title url publishedAt brief } } pageInfo { hasNextPage endCursor } } } }"}'
```

Follow `pageInfo.endCursor` with `posts(first: 50, after: "...")` until
`hasNextPage` is false. Never write the token to any file.

## Field mapping to template

| Source field | Template field (`blogs` item) |
|-----------|------------------------------|
| RSS `title` / `og:title` / GraphQL `title` | `title` |
| RSS `link` / sitemap `loc` / GraphQL `url` | `url` |
| RSS `pubDate` / `article:published_time` / GraphQL `publishedAt` | `published_on` (format: `Mon YYYY`) |
| RSS `description` / `og:description` / GraphQL `brief` | `excerpt` (trim to one sentence if longer; drop a trailing `…` truncation) |
| (hardcoded) | `platform`: `"Hashnode"` |

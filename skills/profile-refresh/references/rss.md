# RSS / Atom Fetch Recipe

Fetch blog posts from any blog that publishes an RSS or Atom feed. This
covers GitHub Pages (Jekyll, Hugo), Ghost, WordPress, Substack, Medium,
Hashnode, and most self-hosted blogs. Read this file before issuing any
request.

The `handle` in `profile-index.json` `sources` is the blog's URL. It may be
the site root (`https://janedoe.github.io`) or the feed itself
(`https://janedoe.github.io/feed.xml`).

Use `curl -sL` via Bash so you get the raw XML. WebFetch passes the page
through a summarizing model, which can drop or reword items, so use it only
when Bash is unavailable.

## 1. Find the feed

- **The handle is already a feed** if the response is XML with an `<rss>` or
  `<feed>` root. Use it.
- **Otherwise, read the site's HTML `<head>`.** Look for
  `<link rel="alternate" type="application/rss+xml" href="…">` or the
  `application/atom+xml` equivalent. Resolve a relative `href` against the
  site URL. If the page lists several feeds, prefer the site-wide posts feed
  over a per-tag or comments feed.
- **No `<link>` tag:** try the common paths. These are `/feed.xml` (Jekyll),
  `/index.xml` (Hugo), `/rss.xml` (Hashnode, Astro, Gatsby), `/atom.xml`,
  `/feed` (WordPress, Substack), and `/rss/` (Ghost).
- **Still nothing:** ask the user for the feed URL. Do not scrape the blog's
  HTML index instead.

When discovery was needed, tell the user the feed URL you found. Suggest
storing it as the `handle` so later refreshes skip discovery.

## 2. Read the feed

| Format | Post element | Title | URL | Date | Summary |
|--------|-------------|-------|-----|------|---------|
| RSS 2.0 | `<item>` | `title` | `link` | `pubDate` | `description` |
| Atom | `<entry>` | `title` | `<link rel="alternate">` `href` (or the `<link>` with no `rel`) | `published`, else `updated` | `summary`, else `content` |

Most feeds carry only recent posts. Jekyll's default is 10, and Hashnode's
is 20. Some feeds embed each post's full HTML in `description` or
`content`. Never copy that into the profile. Take one sentence from it for
`excerpt`.

## 3. Older posts: the sitemap

The feed alone is enough for a routine refresh, because new posts appear in
the feed first. Check the sitemap in these cases:

- First population, when `sections/blogs.json` does not exist yet.
- The oldest feed entry is newer than the newest entry in
  `sections/blogs.json`. Posts may have been published and pushed out of
  the feed since the last refresh.
- The user asks for a full sync.

Find the sitemap at `/sitemap.xml`, or from a `Sitemap:` line in
`/robots.txt`. A sitemap may be an index whose `<loc>` entries point to
child sitemaps. Follow them and collect every page `<loc>`.

Keep only post URLs. The feed shows what a post URL looks like on this blog,
such as `/posts/{slug}`, `/blog/{slug}`, or `/{YYYY}/{MM}/{DD}/{slug}`.
Keep sitemap URLs with the same shape. Drop the root, tag, category,
series, pagination, and static pages. If the shape is unclear, show the
user a sample and ask.

For each post URL that is in neither the feed nor `sections/blogs.json`,
fetch the page and read its `<meta>` tags:

- Title: `og:title`, else `<title>`.
- Date: `article:published_time`, else a `<time datetime>` in the article,
  else the sitemap `<lastmod>`. A `lastmod` date may be an edit date, so
  tell the user which posts were dated from it.
- Summary: `og:description`, else `<meta name="description">`.

On a long-running blog this can mean many fetches. Do the most recent ~30
and tell the user how many remain. They can ask for the rest.

If there is no sitemap, report how many posts the feed covers. Older posts
can be added by hand with `/profile-section`.

## Field mapping to template

| Source field | Template field (`blogs` item) |
|-----------|------------------------------|
| Title | `title` |
| URL | `url` (absolute; strip `utm_*` and other tracking parameters, since `url` is the merge key) |
| Date | `published_on` (format: `Mon YYYY`) |
| Summary | `excerpt` (strip HTML; trim to one sentence; drop a trailing `…` truncation) |
| See below | `platform` |

For `platform`, name the hosting service when the host identifies one, such
as `Hashnode` (`*.hashnode.dev`), `Medium`, `Substack`, or `Ghost`. For a
self-hosted blog, including GitHub Pages, use the blog's own name from the
feed's channel `<title>`. If that title is just the author's name, use
`Personal blog`.

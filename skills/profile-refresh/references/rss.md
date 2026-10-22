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

A handle without a scheme gets `https://`. Blogs often redirect, for
example from `*.github.io` to a custom domain. Take the final URL after
redirects (`curl -sL -w '%{url_effective}'`) as the blog's real host. The
feed and post URLs use that host.

## 1. Find the feed

- **The handle is already a feed** if the response is XML with an `<rss>` or
  `<feed>` root. Use it. Always identify the format from the root element.
  A `<link>` tag's `type` attribute is sometimes wrong, so a feed declared
  as `application/rss+xml` may be Atom.
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

When discovery was needed, or the handle redirected, tell the user the
final feed URL. Suggest storing it as the `handle` so later refreshes skip
discovery and redirects.

## 2. Read the feed

| Format | Post element | Title | URL | Date | Summary |
|--------|-------------|-------|-----|------|---------|
| RSS 2.0 | `<item>` | `title` | `link` | `pubDate` | `description` |
| Atom | `<entry>` | `title` | `<link rel="alternate">` `href` (or the `<link>` with no `rel`) | `published`, else `updated` | `summary`, else `content` |

Titles and summaries may contain HTML and entities such as `&apos;` or
`&#8217;`. Decode them to plain text.

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
series, pagination, and static pages.

Some blogs put posts directly under the root as `/{slug}/`. That is the
same shape as `/about/`, so the URL alone cannot tell them apart. In that
case, decide from the page itself. A post has `og:type` set to `article`
and a published time. A static page has `og:type` set to `website`. A
sitemap entry with no `<lastmod>` is also usually a static page. If you
still cannot tell, show the user a sample and ask.

For each post URL that is in neither the feed nor `sections/blogs.json`,
fetch the page and read its `<meta>` tags:

- Title: `og:title`, else `<title>`.
- Date: `article:published_time` (some themes write
  `og:article:published_time`), else a `<time datetime>` in the article,
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
feed title. That is `<channel><title>` in RSS and the top-level `<title>` in
Atom. If that title is just the author's name, use `Personal blog`.

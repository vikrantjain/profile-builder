# Dev.to Fetch Recipe

Fetch blog posts from Dev.to via the public REST API. No authentication
required.

Read this file before issuing any Dev.to call.

## Endpoint

`https://dev.to/api/articles?username={handle}&per_page=100`

Use WebFetch — there is no `gh`-equivalent CLI for Dev.to.

## Pagination

Dev.to supports a `page` query parameter. If the response returns exactly
`per_page` items, fetch the next page with `&page=2`, etc. Stop when a page
returns fewer items than `per_page` or you reach page 5 (safety cap).

## Field mapping to template

| API field | Template field (`blogs` item) |
|-----------|------------------------------|
| `title` | `title` |
| `url` | `url` |
| `published_at` | `published_on` (format: `Mon YYYY`) |
| `description` | `excerpt` |
| (hardcoded) | `platform`: `"Dev.to"` |

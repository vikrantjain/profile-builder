# Hashnode Fetch Recipe

Fetch blog posts from Hashnode via the public GraphQL API. No
authentication required.

Read this file before issuing any Hashnode call.

## Endpoint

`https://gql.hashnode.com` (POST, GraphQL)

Use WebFetch — there is no `gh`-equivalent CLI for Hashnode.

## Query

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

## Pagination

If `pageInfo.hasNextPage` is `true`, send a follow-up query with
`posts(first: 50, after: "{endCursor}")` to fetch the next page. Repeat until
`hasNextPage` is `false` or you have fetched 200 posts (safety cap).

## Custom domain fallback

If the query returns `null` for `publication`, the user may have a custom
domain. Retry with the handle value used as-is in the `host` parameter
(e.g., `publication(host: "blog.example.com")`) — the `handle` field in
`profile-index.json` `sources` may contain a full custom domain instead of a
bare username.

## Field mapping to template

| API field | Template field (`blogs` item) |
|-----------|------------------------------|
| `title` | `title` |
| `url` | `url` |
| `publishedAt` | `published_on` (format: `Mon YYYY`) |
| `brief` | `excerpt` (truncate to one sentence if longer) |
| (hardcoded) | `platform`: `"Hashnode"` |

# GitHub Profile README Conventions

## What Is a GitHub Profile README

A special repository named `<username>/<username>` with a `README.md` that
appears on the user's GitHub profile page. It supports full GitHub-flavored
Markdown.

## Formatting

- Full GitHub-flavored Markdown is supported (bold, italic, links, images,
  tables, code blocks, HTML).
- HTML is supported for advanced layouts (e.g., `<details>`, `<table>`,
  `<img align="right">`).
- Badges are common: use shields.io for tech stack, social links, stats.
- Keep it scannable — visitors spend seconds, not minutes.

## Common Sections

1. **Greeting / Introduction** — Brief one-liner about who you are
2. **Current Role / What You Do** — Title and focus area
3. **Tech Stack** — Languages, frameworks, tools (often as badges)
4. **Notable Projects** — 3-5 highlighted repos with descriptions
5. **Open Source Contributions** — Key contributions to other projects
6. **Blog Posts** — Recent articles (can be auto-updated with GitHub Actions)
7. **How to Reach Me** — Contact links

## Section Mapping (Profile → GitHub README)

| Profile Section | GitHub README Element |
|----------------|---------------------|
| `sections/identity.json` → full_name, title | Heading + intro line |
| `sections/summary.json` | Introduction paragraph |
| `sections/skills.json` → categories | Tech stack badges or list |
| `sections/open-source.json` → projects | Featured projects section |
| `sections/open-source.json` → contributions | Contributions section |
| `sections/blogs.json` | Recent blog posts list |
| `sections/identity.json` → github, linkedin, website, twitter | Contact/social links |

## Badge Format (shields.io)

```markdown
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazonaws&logoColor=white)
```

## Best Practices

- Keep it concise — aim for content that fits in one viewport without scrolling
- Lead with what makes you distinctive, not generic statements
- Link to actual repos rather than just listing project names
- Use consistent formatting throughout
- Avoid walls of text — use bullet points, badges, and visual breaks

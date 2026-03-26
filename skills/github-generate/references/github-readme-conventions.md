# GitHub Profile README Conventions

## What Is a GitHub Profile README

A special repository named `<username>/<username>` with a `README.md` that
appears on the user's GitHub profile page. It supports full GitHub-flavored
Markdown and inline HTML.

## Formatting Capabilities

- Full GitHub-flavored Markdown: bold, italic, links, images, tables, code
  blocks, task lists, footnotes.
- Inline HTML for advanced layouts: `<details>`, `<summary>`, `<table>`,
  `<img align="right">`, `<p align="center">`, `<br>`.
- GitHub renders Markdown in a constrained-width container (~888px). Design
  for this width — wide tables or long badge rows will wrap.
- Emoji shortcodes work (`:wave:` → :wave:) but use sparingly. A few in
  headers is fine; emoji in every line is visual noise.

## Layout Patterns

### Centered Header

```markdown
<h1 align="center">Hi, I'm Name</h1>
<p align="center">
  <em>Platform engineer building event-driven systems at scale</em>
</p>
```

### Left-Aligned Header (simpler, common)

```markdown
# Name

Platform engineer building event-driven systems at scale
```

### Section Dividers

Use horizontal rules (`---`) or `<br>` between major sections for visual
breathing room. Don't overuse — one between each major section is enough.

### Collapsible Sections

Use `<details>` for secondary content that shouldn't dominate the page:

```markdown
<details>
<summary>More about my experience</summary>

Content here — Markdown works inside details blocks.

</details>
```

Good candidates for collapsible: full project lists, contribution history,
extended tech stack, GitHub stats.

## Badge Format (shields.io)

### Basic Syntax

```
![Label](https://img.shields.io/badge/Label-Color?style=STYLE&logo=LOGO&logoColor=white)
```

### Style Options

| Style | Look | Best for |
|-------|------|----------|
| `flat` | Minimal, low-profile | Dense badge rows, inline use |
| `flat-square` | Flat with sharp corners | Compact layouts |
| `for-the-badge` | Large, bold | Statement badges, sparse layouts |

Pick one style and use it throughout. Mixing styles looks inconsistent.

### Common Tech Badge Colors

| Technology | Hex Color | Logo Name |
|-----------|-----------|-----------|
| Python | 3776AB | python |
| JavaScript | F7DF1E | javascript |
| TypeScript | 3178C6 | typescript |
| Go | 00ADD8 | go |
| Rust | 000000 | rust |
| Java | ED8B00 | openjdk |
| C# | 239120 | csharp |
| Ruby | CC342D | ruby |
| Swift | F05138 | swift |
| Kotlin | 7F52FF | kotlin |
| React | 61DAFB | react |
| Vue.js | 4FC08D | vuedotjs |
| Angular | DD0031 | angular |
| Next.js | 000000 | nextdotjs |
| Node.js | 339933 | nodedotjs |
| Django | 092E20 | django |
| Spring | 6DB33F | spring |
| FastAPI | 009688 | fastapi |
| Flask | 000000 | flask |
| AWS | 232F3E | amazonaws |
| GCP | 4285F4 | googlecloud |
| Azure | 0078D4 | microsoftazure |
| Docker | 2496ED | docker |
| Kubernetes | 326CE5 | kubernetes |
| Terraform | 844FBA | terraform |
| PostgreSQL | 4169E1 | postgresql |
| MongoDB | 47A248 | mongodb |
| Redis | FF4438 | redis |
| Kafka | 231F20 | apachekafka |
| GraphQL | E10098 | graphql |
| Git | F05032 | git |
| Linux | FCC624 | linux |
| Nginx | 009639 | nginx |

### Social / Contact Badges

```markdown
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/username)
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=flat&logo=twitter&logoColor=white)](https://twitter.com/username)
[![Website](https://img.shields.io/badge/Website-000000?style=flat&logo=safari&logoColor=white)](https://example.com)
```

Note: social/contact badges are clickable links (wrapped in `[![]()](url)`),
while tech stack badges are typically not linked.

## GitHub Stats Widgets

Optional — these add visual flair but can feel generic. Use only if the
user's stats tell a meaningful story (e.g., heavy commit activity, many
contributions to others' repos).

### GitHub Readme Stats

```markdown
![GitHub Stats](https://github-readme-stats.vercel.app/api?username=USERNAME&show_icons=true&theme=default)
```

### Top Languages

```markdown
![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=USERNAME&layout=compact)
```

### GitHub Streak

```markdown
![GitHub Streak](https://github-readme-streak-stats.herokuapp.com/?user=USERNAME)
```

**Guidance on stats widgets:** These are common but can backfire. A streak
widget showing gaps or a top-languages chart dominated by config files (JSON,
YAML) hurts more than it helps. Only include if the data tells a flattering
story and the user wants them — they're not included by default.

## Section Mapping (Profile → GitHub README)

| Profile Section | GitHub README Element |
|----------------|---------------------|
| `identity.json` → full_name, title | Header + subtitle |
| `summary.json` + `experience.json` | About / intro paragraph |
| `skills.json` → categories | Tech stack badges |
| `open-source.json` → projects | Featured projects section |
| `open-source.json` → contributions | Open source contributions |
| `blogs.json` | Recent blog posts list |
| `certifications.json` | Certifications badges (optional) |
| `identity.json` → github, linkedin, website, twitter | Connect section |

## Featured Project Formatting

### Card-Style (recommended for 3-5 projects)

```markdown
### [Project Name](https://github.com/user/repo)

One-line description of what the project does.

- Designed the event-driven architecture handling 2M messages/day
- Built plugin system adopted by 15+ community contributors

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Kafka](https://img.shields.io/badge/Kafka-231F20?style=flat&logo=apachekafka&logoColor=white)
```

### Compact List (for 5+ projects or secondary section)

```markdown
- **[Project Name](url)** — Description. `Python` `Kafka` `Docker`
- **[Another Project](url)** — Description. `TypeScript` `React`
```

## Best Practices

- **Above the fold matters** — The first screenful (header, intro, start of
  tech stack) is what most visitors see. Make it count.
- **Lead with what makes you distinctive** — Not generic statements like
  "passionate about code." Specific: what you build, what domain, what scale.
- **Link to actual repos** — Project names should be clickable links, not
  just text.
- **Curate the tech stack** — 15-25 badges is the sweet spot. Fewer than 10
  feels sparse; more than 30 becomes visual noise where nothing stands out.
- **Use consistent formatting** — One badge style, consistent heading levels,
  uniform project card format throughout.
- **Avoid walls of text** — Use bullet points, badges, and visual breaks.
  Paragraphs should be 2-4 sentences max.
- **Skip boilerplate** — "Welcome to my GitHub profile!" and "Feel free to
  check out my repos!" add nothing. Get straight to the substance.
- **Tone: conversational-technical** — How you'd introduce yourself at a
  conference, not a cover letter. First person is fine. Skip corporate
  language ("leveraging", "driving value", "stakeholder alignment").

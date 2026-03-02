---
name: github-generate
description: >
  This skill should be used when the user asks to "generate GitHub README",
  "create GitHub profile", "export profile for GitHub", "build my GitHub
  profile README", "update my GitHub bio", or wants a GitHub profile
  README.md generated from their master profile data.
---

# GitHub Generate

Generate a GitHub profile README.md from the master profile data, formatted
with GitHub-flavored Markdown, badges, and project highlights.

## When to Use

Invoke this skill to produce a `README.md` for the user's GitHub profile
repository (`<username>/<username>`). For reviewing an existing GitHub
profile against the master data, use the `github-review` skill instead.

## Workflow

### 1. Read Profile Data

Read the relevant profile section JSON files from `sections/`. Parse each
JSON file and access fields directly from the `data` object. Key sections:

- `sections/identity.json` — name, title, GitHub URL, social links
- `sections/summary.json` — professional bio (adapt for GitHub tone)
- `sections/skills.json` — tech stack for badges
- `sections/open-source.json` — projects and contributions to highlight
- `sections/blogs.json` — recent blog posts (if available)

If required section JSON files do not exist, inform the user and suggest
running `/profile-init` or `profile-section` to generate them.

### 2. Apply Presentation Preferences

Read `preferences.md` from the workspace root. If it exists:

1. Read the `## Global` section — these apply to all exports.
2. Read the `## GitHub` section (if present) — these are GitHub-specific.
3. Treat each preference as a binding directive during content transformation.
   Examples: "present experience as 20+ years" → use that framing; "don't
   highlight patents" → de-emphasize or omit; tone directives → adjust writing
   style accordingly.
4. GitHub-specific preferences take precedence over global if they conflict.

If `preferences.md` does not exist, proceed with default behavior.

### 3. Determine GitHub Username

Extract the GitHub username from the GitHub URL in the identity section.
This is needed for linking to repositories and for the profile repo name.

### 4. Generate README Content

**TBD filtering:** Profile data may contain `TBD` as a placeholder value in
any field (indicating data not yet filled in by the user). When rendering
output, silently skip any value that is exactly `TBD` — do not render it.
If all items in a list are `TBD`, omit that list/block entirely.

Consult `${CLAUDE_PLUGIN_ROOT}/skills/github-generate/references/github-readme-conventions.md` for formatting conventions,
section mapping, and badge syntax.

Build the README with these sections (skip any that lack data):

1. **Header**: Name as `# heading`, title/tagline as subtitle
2. **About**: Adapted summary — shorter and more casual than the profile
   summary, appropriate for GitHub's developer audience
3. **Tech Stack**: Skills rendered as shields.io badges grouped by category
4. **Featured Projects**: Top 3-5 repositories with name, description, and
   link. Source from `sections/open-source.json` projects. For each featured
   project, surface one or two notable `contributions` bullets describing key
   work, and any `impact` metrics (star count, downloads, adoption) as
   supporting details below the project link
5. **Contributions**: Notable open source contributions (if available)
6. **Recent Blog Posts**: Links to recent posts (if available)
7. **Connect**: Social links (LinkedIn, website, Twitter) as badges or links

### 5. Verify Preferences Compliance

Before writing output, re-read the applicable preferences and verify each one
is reflected in the generated content. If any preference was missed or
contradicted, revise the content before proceeding.

### 6. Write Output

Write the generated README to `github-readme.md`.

### 7. Present to User

Display the generated content in the conversation. Note that the user needs
to copy it to their `<username>/<username>` repository's `README.md`.

## Output Checklist

Before finishing, verify:

- [ ] All repo links point to valid GitHub URLs (based on profile data)
- [ ] Badges use correct shields.io format
- [ ] Content is concise — fits roughly in one viewport
- [ ] No profile data fabricated — all sourced from master profile
- [ ] File written to `github-readme.md`
- [ ] Output honors all applicable presentation preferences (global + GitHub-specific)

## Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/skills/github-generate/references/github-readme-conventions.md`** — Section mapping, badge format, and best practices

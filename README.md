# Profile Builder

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) plugin for managing professional profiles with AI. Collect data from multiple sources, generate a structured profile document, and export platform-ready content for LinkedIn, GitHub, Hashnode, and tailored resumes.

## What It Does

Profile Builder treats your professional profile as a **canonical data layer** — a single source of truth that decouples data collection from presentation.

```
Sources (resume, LinkedIn, GitHub, blog)
        ↓
   Master Profile (structured JSON sections)
        ↓
   Exports (LinkedIn copy, GitHub README, resume, Hashnode bio)
```

Instead of maintaining separate profiles on every platform, you maintain one master profile and generate platform-specific outputs from it.

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI installed and configured
- Node.js (for Playwright MCP, used by LinkedIn review)
- [`gh` CLI](https://cli.github.com/) (optional — for GitHub review and refresh)

## Installation

Profile Builder ships as a **standalone plugin repository** — [`vikrantjain/profile-builder`](https://github.com/vikrantjain/profile-builder). It also bundles its own `.claude-plugin/marketplace.json`, so the repo doubles as a single-plugin marketplace — no separate marketplace repo needed. Add it to your own setup one of three ways.

### Option 1 — Add this repo as a marketplace (recommended)

From within Claude Code:

```shell
/plugin marketplace add vikrantjain/profile-builder
/plugin install profile-builder@profile-builder
```

### Option 2 — Load from a local clone (quickest for development)

```shell
git clone https://github.com/vikrantjain/profile-builder.git
```

```shell
# Load it for the current Claude Code session:
claude --plugin-dir ./profile-builder
```

Plugin skills/commands are namespaced — they appear as `/profile-builder:profile-init`, `/profile-builder:profile-section`, etc. (the short `/profile-init` form also works when the name is unambiguous). Run `/reload-plugins` to pick up edits if you modify the plugin.

### Option 3 — Add it to your own marketplace

If you maintain a marketplace (any repo with a `.claude-plugin/marketplace.json`), add Profile Builder as a GitHub-sourced plugin entry:

```json
{
  "name": "profile-builder",
  "source": { "source": "github", "repo": "vikrantjain/profile-builder" }
}
```

Then install it from within Claude Code and activate:

```shell
/plugin install profile-builder@<your-marketplace>
/reload-plugins
```

## Quick Start

1. **Initialize your profile** — run the `/profile-init` command in Claude Code:

   ```
   /profile-init
   ```

   This walks you through collecting data from your resume, LinkedIn, GitHub, and blog platforms, then builds all profile sections.

2. **Generate exports** — ask Claude to generate content for a specific platform:

   - *"Generate my LinkedIn content"*
   - *"Create a resume tailored to this job description"*
   - *"Generate my GitHub profile README"*
   - *"Export my Hashnode profile content"*

3. **Review your profiles** — get actionable improvement suggestions:

   - *"Review my LinkedIn profile"*
   - *"Review my GitHub profile"*
   - *"Review my Hashnode profile"*

## Commands

| Command | Description |
|---|---|
| `/profile-init` | Interactive onboarding. Collects data sources, builds all sections, generates the profile index. Entry point for new users. |
| `/profile-validate` | Validate profile documents against the template schema. Checks for missing fields, unfilled placeholders, and structural issues. Offers interactive fixes. |
| `/linkedin-rec` | Generate a recommendation request message for a former colleague. Takes `[Name], [Company], [optional: project]` as arguments. |

## Skills

### Guidance

| Skill | What it does | Example prompts |
|---|---|---|
| `profile-guide` | Inspects your project's current state and recommends the single best next step; explains how the pieces fit together (advise-only — never runs other skills) | *"How do I use this plugin?"*, *"What should I do next?"*, *"What do I need before I can generate a resume?"* |

### Data Layer

These skills manage the master profile — the structured source of truth.

| Skill | What it does | Example prompts |
|---|---|---|
| `profile-section` | Generate or update a single profile section (writes to the data layer, so it's invoked explicitly) | Run `/profile-section`, then describe the change (e.g. *"add my new certification"*) |
| `profile-refresh` | Fetch latest data from external platforms (GitHub, Hashnode, Dev.to) | *"Refresh my blog posts"*, *"Sync my open source data"* |
| `profile-assemble` | Stitch section files into a single `profile.md` (optional output, invoked explicitly) | Run `/profile-assemble` when you want the whole profile as one readable document |

### Preferences

| Skill | What it does | Example prompts |
|---|---|---|
| `profile-preferences` | Store persistent presentation preferences that shape exports and reviews | *"Remember that I prefer a formal tone"*, *"My preference is to emphasize backend work"* |

### Generate (Profile → Platform Content)

These skills read from the master profile and produce platform-ready content.

| Skill | Output | Example prompts |
|---|---|---|
| `linkedin-generate` | `linkedin/` directory with per-section files | *"Generate my LinkedIn content"*, *"Write my LinkedIn headline"* |
| `resume-generate` | `resume.md` + `resume.json` ([JSON Resume](https://jsonresume.org/) format) | *"Generate a resume for this job"*, *"Make an ATS-optimized resume"* |
| `github-generate` | `github-readme.md` | *"Generate my GitHub profile README"* |
| `hashnode-generate` | `hashnode/` directory | *"Export my Hashnode profile content"* |

### Review (Fetch & Assess External Profiles)

These skills fetch your live profile from a platform, compare it against the master profile, and suggest improvements.

| Skill | Requirements | Example prompts |
|---|---|---|
| `linkedin-review` | Playwright MCP (bundled in `.mcp.json`) | *"Review my LinkedIn profile"* |
| `github-review` | `gh` CLI | *"Review my GitHub profile"* |
| `hashnode-review` | None (uses public GraphQL API) | *"Review my Hashnode profile"* |

## How It Works

### Profile Lifecycle

```
/profile-init  →  Collect data from sources  →  Build all sections  →  Generate index
                                                      ↓
                                            sections/*.json files
                                                      ↓
                             /profile-assemble  →  profile.md (optional)
                                                      ↓
                              Generate / Review skills consume sections/*.json directly
```

### File Structure (Generated)

After initialization, your workspace will contain:

```
profile-index.json        ← Hub file: identity, section manifest, data sources
sections/
  identity.json
  summary.json
  experience.json
  skills.json
  education.json
  certifications.json
  blogs.json              ← Dynamic (refreshable from Hashnode/Dev.to)
  open-source.json        ← Dynamic (refreshable from GitHub)
  ...
profile.md                ← Assembled full profile (generated on demand)
preferences.md            ← Presentation preferences (optional, user-managed)
```

### Dynamic Sections

Some sections track data from external platforms:

- **blogs** — sourced from Hashnode, Dev.to
- **open_source** — sourced from GitHub (projects + contributions)

Run *"Refresh my blog posts"* or *"Refresh my open source data"* to pull the latest. Other sections (experience, skills, education, etc.) are static and updated from user-provided data.

## Resume Generation

The `resume-generate` skill produces two formats:

- **`resume.md`** — Clean Markdown resume, optionally tailored to a specific job description
- **`resume.json`** — [JSON Resume](https://jsonresume.org/) schema, importable into [Reactive Resume](https://rxresu.me/) and other compatible tools

Provide a job description to get a tailored, ATS-optimized resume:

> *"Generate a resume tailored to this job posting: [paste URL or text]"*

## Configuration

### Playwright MCP

The plugin includes an `.mcp.json` that configures Playwright for LinkedIn review. This requires Node.js and runs automatically when the LinkedIn review skill is invoked.

### Preferences

Store persistent preferences that affect how exports and reviews are generated:

> *"Remember that I prefer a conversational tone on LinkedIn"*
> *"My preference is to always highlight cloud architecture experience"*

Preferences are saved to `preferences.md` and grouped by scope (Global, LinkedIn, Resume, GitHub, Hashnode).

## Project Structure

```
.claude-plugin/
  plugin.json                          ← Plugin manifest
commands/
  profile-init.md                      ← /profile-init command
  profile-validate.md                  ← /profile-validate command
  linkedin-rec.md                      ← /linkedin-rec command
skills/
  profile-guide/SKILL.md               ← Orientation & next-step guidance
  profile-section/SKILL.md             ← Generate/update a single section
  profile-refresh/SKILL.md             ← Fetch latest from external platforms
    references/                        ← Fetch recipes (github.md, hashnode.md, devto.md)
  profile-assemble/SKILL.md            ← Stitch sections into full profile
  profile-preferences/SKILL.md         ← Manage presentation preferences
  linkedin-generate/SKILL.md           ← Generate LinkedIn content
    references/                        ← LinkedIn field limits and formatting rules
  resume-generate/SKILL.md             ← Generate tailored resume
    references/                        ← Resume conventions + JSON Resume schema mapping
  github-generate/SKILL.md             ← Generate GitHub README
    references/                        ← README conventions and badge syntax
  hashnode-generate/SKILL.md           ← Generate Hashnode content
    references/                        ← Hashnode field limits and formatting rules
  linkedin-review/SKILL.md             ← Review LinkedIn profile
    references/                        ← Playwright scrape recipe
  github-review/SKILL.md               ← Review GitHub profile
  hashnode-review/SKILL.md             ← Review Hashnode profile
profile-template.md                    ← Canonical profile schema
profile-layout.md                      ← Markdown rendering template (used by profile-assemble)
profile-index-template.md              ← JSON schema for profile-index.json
CLAUDE.md                              ← Project instructions for Claude Code
.mcp.json                              ← MCP server config (Playwright)
```

## License

MIT

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Important: Preference Routing

When the user says "remember that...", "my preference is...", "always...", "never...",
or any similar phrasing related to how their profile data should be presented, exported,
or reviewed — **use the `profile-preferences` skill** to save the preference to
`preferences.md` in the workspace root. Do NOT save these as auto memory entries.
Auto memory is for operational notes only, not for user presentation preferences.

## Project Intent

This project is a **personal profile management system powered by AI agents**. The core idea:

1. **Collect** raw professional data from multiple sources (resume, LinkedIn, GitHub, blog posts, etc.)
2. **Generate** a comprehensive, structured profile document — richer than any single resume or platform profile
3. **Maintain** the profile over time with targeted section updates
4. **Consume** the profile as a single source of truth to produce downstream outputs: customized resumes for specific job descriptions, LinkedIn profile updates, GitHub profile READMEs, portfolio content, etc.

The profile document is a **canonical data layer** that decouples data collection from presentation. Downstream consumers don't re-scrape sources — they read from the profile.

## Project Overview

This is a Claude Code plugin (`profile-builder`) for managing professional profiles. It provides skills for generating, updating, and assembling Markdown profile documents, plus downstream skills for exporting to platforms and reviewing external profiles. There is no build system, test suite, or runtime — the project consists entirely of YAML/Markdown templates, Claude Code skill definitions, and utility scripts.

## Architecture

The project follows a **separation of schema and workflow**:

- **Templates** (`profile-template.md`, `profile-index-template.md`) are pure declarative data contracts — field definitions, section mappings, placeholder syntax, and Markdown layouts. They contain no procedural instructions.
- **Skills** (`skills/*/SKILL.md`) contain the workflow logic — how to gather data, render templates, write output files, and coordinate between modes.

### Profile Lifecycle

1. **Init** — `/profile-init` command collects data from user sources (resume, GitHub, LinkedIn, blog platforms), generates `profile-index.md` early (with data sources and an empty sections table that is populated incrementally), builds all section files, verifies source coverage (cross-references generated sections against original sources to catch missing information), and validates the output against the template schema. Dynamic section refresh is not automatic — init configures the data sources and informs the user to run `profile-refresh` when ready. This is the entry point for new users. Can be re-run to rebuild from scratch.
2. **Maintain** — `profile-section` builds or updates individual sections. It includes an intelligent field mapping step that scans input for all template fields (required and optional) using semantic matching — e.g., "Action/Achievement" bullets → `highlights`, date ranges → `duration`, technology lists → `tech_stack`. Required fields with no extractable data get a `TBD` placeholder default. For dynamic sections (blogs, open_source) it calls `profile-refresh` to fetch latest data from configured platforms. `profile-refresh` can also be invoked directly by the user at any time.
3. **Assemble** — `profile-assemble` stitches existing section files into a single `profile.md` on demand (e.g., before generating a resume or export).

### Key Files

- `profile-template.md` — The canonical schema. Contains `fields` (field definitions with types/hints), `sections` (maps each section to an output file and its dependent fields), `placeholder_syntax` (templating reference), and the full Markdown layout below the frontmatter.
- `profile-index-template.md` — Template for the hub file that lists identity/contact info and a manifest table of generated section files.
- `preferences.md` — User presentation preferences. Controls tone, emphasis, and framing in exports and reviews. Not used by data-layer skills. Created at runtime by the `profile-preferences` skill.
- Generated output (not checked in): `profile.md`, `profile-index.md`, `sections/*.md`.

### Template Conventions

- Templates use a Handlebars-like placeholder syntax (`{{field}}`, `{{#each list}}`, `{{#field}}...{{/field}}`).
- The `sections` mapping in `profile-template.md` is the single source of truth for which fields belong to which section and where section files are written.
- Section files must NOT include leading/trailing `---` — horizontal rules are added during assembly.
- **TBD convention**: Required fields with no extractable data from user input get `TBD` as a placeholder default (e.g., `highlights: ["TBD"]`). Data-layer skills write TBD values as-is. All generate/export skills silently skip any value that is exactly `TBD` during rendering. `profile-validate` warns about TBD values so users know which fields need enrichment.

## Plugin Structure

This is a Claude Code plugin with auto-discovered skills:

```
.claude-plugin/plugin.json         — Plugin manifest
commands/profile-init.md           — /profile-init command (interactive onboarding)
commands/profile-validate.md       — /profile-validate command (validate & fix profile docs)
skills/profile-preferences/        — Add/update/remove presentation preferences
skills/profile-section/            — Generate/update a single section
skills/profile-refresh/            — Fetch latest data from external platforms for dynamic sections
skills/profile-assemble/           — Stitch sections into complete profile
skills/linkedin-generate/          — Generate copy-paste-ready LinkedIn content
skills/resume-generate/            — Generate tailored, ATS-optimized resume (Markdown + JSON Resume)
skills/github-generate/            — Generate GitHub profile README
skills/hashnode-generate/          — Generate copy-paste-ready Hashnode profile content
skills/linkedin-review/            — Quality review of LinkedIn profile with improvement suggestions (needs Playwright MCP)
skills/github-review/              — Review GitHub against master profile (needs gh CLI)
skills/hashnode-review/            — Review Hashnode against master profile (uses GraphQL API)
linkedin/                          — LinkedIn export files (not checked in)
hashnode/                          — Hashnode export files (not checked in)
```

Skills use YAML frontmatter with `name` and `description` (third-person, with trigger phrases). Skill body uses imperative/infinitive writing style.

### Commands

- `/profile-init` — Interactive onboarding. Collects data sources, builds all sections, configures data sources, generates index. Entry point for new users.
- `/profile-validate` — Validate profile documents against the template schema. Checks for missing fields, unfilled placeholders, structural issues. Offers interactive fixes with user approval.

### Skill Categories

**Data layer** (profile as source of truth):
- `profile-section`, `profile-refresh`, `profile-assemble`

**Preferences layer** (persistent presentation directives):
- `profile-preferences` — manages `preferences.md`; consumed by export and review skills

**Generate layer** (profile → platform-ready content, no external access needed):
- `linkedin-generate`, `github-generate`, `hashnode-generate`, `resume-generate`
- All generate skills read `preferences.md` (if it exists) to apply user presentation directives.

**Review layer** (fetch external profile, assess quality and impact, suggest improvements):
- `linkedin-review` (requires Playwright MCP for browser access)
- `github-review` (uses `gh` CLI or WebFetch)
- `hashnode-review` (uses Hashnode public GraphQL API via WebFetch)
- All review skills read `preferences.md` (if it exists) to adjust quality review criteria.
- The master profile provides background context (what the user has achieved) but the primary focus is quality and impact of the platform profile, not data sync.

### Dynamic Sections and Refresh

Some profile sections track data that lives on external platforms and changes over time:

- **blogs** — sourced from Hashnode, Dev.to
- **open_source** — sourced from GitHub (projects + contributions)

These are called **dynamic sections**. Their source configuration (platform + handle) is stored in the **Data Sources** table of the user's `profile-index.md`, not in the plugin templates.

`profile-refresh` fetches latest data from configured sources and updates the corresponding section files. It can be invoked directly by the user or called internally by `profile-section` when building a dynamic section. It is never called by `profile-assemble` or any export/review skill — those consume section files as-is.

All other sections (identity, summary, experience, skills, education, certifications, patents, languages) are **static** — updated only from user-provided data.

### Presentation Preferences

Users can store persistent directives that shape how profile data is presented
in exports and reviews. Examples: tone preferences, section emphasis/de-emphasis,
experience framing, personality traits that affect language choices.

Preferences are stored in `preferences.md` at the workspace root. Each preference
is grouped under `## Global` (applies to every export/review skill) or a
platform-specific heading (`## LinkedIn`, `## Resume`, `## GitHub`, `## Hashnode`).

Preferences are consumed by export and review skills only. Data-layer skills
(`profile-section`, `profile-refresh`, `profile-assemble`) ignore preferences
entirely — they record data as-is.

Manage preferences via:
- The `profile-preferences` skill (natural language: "remember that...", "my preference is...")
- Direct editing of `preferences.md`

### Output Paths

- `linkedin/` — LinkedIn export files (one per section: headline.md, about.md, experience.md, skills.md, etc.)
- `resume.md` — Generated resume (Markdown, content-only)
- `resume.json` — Generated resume (JSON Resume schema, for import into Reactive Resume and compatible tools)
- `github-readme.md` — GitHub profile README
- `linkedin-review.md` — LinkedIn review report
- `github-review.md` — GitHub review report
- `hashnode/` — Hashnode export files (one per field: tagline.md, bio.md, about.md, tech-stack.md, social-links.md)
- `hashnode-review.md` — Hashnode review report
- `preferences.md` — Presentation preferences (user-managed, manually editable)
- `.profile/tmp/{YYYY-MM-DD}/{source}/` — Temporary/intermediate data organized by date and source (e.g., `playwright`, `github`, `hashnode`). One folder per day per source. Never for final user-facing output. Cleaned up by `/profile-validate` (folders older than 30 days).

### Bundled Skill Resources

Some skills include reference docs and scripts:
- `skills/linkedin-generate/references/linkedin-constraints.md` — LinkedIn field limits and formatting rules
- `skills/resume-generate/references/resume-conventions.md` — Resume formatting, tailoring strategy, ATS guidelines
- `skills/resume-generate/references/json-resume-schema.md` — JSON Resume schema field mapping
- `skills/github-generate/references/github-readme-conventions.md` — GitHub README conventions and badge syntax
- `skills/hashnode-generate/references/hashnode-constraints.md` — Hashnode profile field limits and formatting rules

### External Dependencies

- **Playwright MCP** — configured in `.mcp.json` at workspace root; required by `linkedin-review` for fetching LinkedIn profiles via browser automation
- **`gh` CLI** — used by `github-review` and `profile-refresh` for fetching GitHub profile data
- **Hashnode GraphQL API** — public API at `gql.hashnode.com`, used by `hashnode-review` and `profile-refresh` via WebFetch (no authentication required)

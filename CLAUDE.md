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

This is a Claude Code plugin (`profile-builder`) for managing professional profiles. It provides skills for generating structured JSON profile data, rendering it into Markdown documents, and exporting to platforms, plus skills for reviewing external profiles. There is no build system, test suite, or runtime — the project consists entirely of schema definitions, Markdown layout templates, Claude Code skill definitions, and utility scripts.

## Architecture

The project follows a **separation of schema and workflow**:

- **Schema** (`profile-template.md`) is the pure declarative data contract — field definitions, section mappings, JSON structure conventions, and placeholder syntax. It contains no procedural instructions and no Markdown layout.
- **Layout** (`profile-layout.md`) is the Markdown rendering template — used exclusively by `profile-assemble` to render JSON section data into the assembled `profile.md`. Contains `{{placeholder}}` syntax but no field definitions.
- **Index schema** (`profile-index-template.md`) defines the JSON structure for `profile-index.json`.
- **Skills** (`skills/*/SKILL.md`) contain the workflow logic — how to gather data, render templates, write output files, and coordinate between modes.

### Profile Lifecycle

1. **Init** — `/profile-init` command collects data from user sources (resume, GitHub, LinkedIn, blog platforms), generates `profile-index.json` early (with data sources and an empty sections array that is populated incrementally), builds all section files, verifies source coverage (cross-references generated sections against original sources to catch missing information), and validates the output against the template schema. Dynamic section refresh is not automatic — init configures the data sources and informs the user to run `profile-refresh` when ready. This is the entry point for new users. Can be re-run to rebuild from scratch.
2. **Maintain** — `profile-section` (invoked explicitly via `/profile-section`; it is `disable-model-invocation: true` to protect the data layer) builds or updates individual sections. It includes an intelligent field mapping step that scans input for all template fields (required and optional) using semantic matching — e.g., "Action/Achievement" bullets → `contributions` (work done) and `impact` (quantifiable outcomes), date ranges → `duration`, technology lists → `tech_stack`. Required fields with no extractable data get a `TBD` placeholder default. For dynamic sections (blogs, open_source) it calls `profile-refresh` to fetch latest data from configured platforms (if source configuration exists in `profile-index.json`). `profile-refresh` can also be invoked directly by the user at any time.
3. **Assemble** — `profile-assemble` reads JSON section files, renders them through the `profile-layout.md` template, and produces a single human-readable `profile.md` on demand. This is an **optional side-branch, not a prerequisite for anything**: every generate and review skill reads `sections/*.json` directly (discovered via `profile-index.json`) and none of them consume `profile.md`. Assemble only when the user explicitly wants the whole profile as one document to read or share.

### Key Files

- `profile-template.md` — The canonical field schema. Contains `fields` (field definitions with types/hints), `sections` (maps each section to a `.json` output file and its dependent fields), `json_structure` (envelope format and data rules), and `placeholder_syntax` (templating reference). No Markdown layout.
- `profile-layout.md` — The Markdown rendering template. Contains the full `{{placeholder}}` layout for all sections. Used exclusively by `profile-assemble` to render JSON section data into `profile.md`.
- `profile-index-template.md` — JSON schema definition for `profile-index.json` (the manifest and configuration hub).
- `preferences.md` — User presentation preferences. Controls tone, emphasis, and framing in exports and reviews. Not used by data-layer skills. Created at runtime by the `profile-preferences` skill.
- Generated output (not checked in): `profile.md`, `profile-index.json`, `sections/*.json`.

### Data Format

- Section files are **structured JSON**, not rendered Markdown. Each section file uses a `{ "section": "<key>", "data": { ... } }` envelope. Field names match the schema in `profile-template.md` exactly.
- The `sections` mapping in `profile-template.md` is the single source of truth for which fields belong to which section and where section files are written (`.json` paths).
- The Markdown rendering layout lives in `profile-layout.md` and is used only by `profile-assemble`. It uses Handlebars-like placeholder syntax (`{{field}}`, `{{#each list}}`, `{{#field}}...{{/field}}`).
- JSON values are raw data — no Markdown formatting characters (`**`, `##`, `- ` bullets) in string values.
- **TBD convention**: Required fields with no extractable data use `"TBD"` (string) or `["TBD"]` (list) in JSON. Optional fields with no data use `null` or are omitted — never set to TBD. Data-layer skills write TBD values as-is. All generate/export skills silently skip any value that is exactly `"TBD"` during rendering. `profile-validate` warns about TBD values so users know which fields need enrichment.

## Plugin Structure

This is a Claude Code plugin with auto-discovered skills:

```
.claude-plugin/plugin.json         — Plugin manifest
profile-template.md                — Canonical field schema (fields, sections, json_structure)
profile-layout.md                  — Markdown rendering template (used by profile-assemble)
profile-index-template.md          — JSON schema for profile-index.json
commands/profile-init.md           — /profile-init command (interactive onboarding)
commands/profile-validate.md       — /profile-validate command (validate & fix profile docs)
commands/linkedin-rec.md           — /linkedin-rec command (generate recommendation request message)
skills/profile-guide/              — Orientation & how-to guidance; recommends next step from project state (advise-only)
skills/profile-preferences/        — Add/update/remove presentation preferences
skills/profile-section/            — Generate/update a single section
skills/profile-refresh/            — Fetch latest data from external platforms for dynamic sections
skills/profile-assemble/           — Render JSON sections through layout into complete profile
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
- `/profile-validate` — Validate profile documents against the template schema. Checks JSON validity, required fields, type correctness, TBD values, and legacy `.md` files. Offers interactive fixes with user approval.
- `/linkedin-rec` — Generate a recommendation request message for a former colleague. Takes `[Name], [Company], [optional: project]` as arguments. Reads experience, identity, summary, and preferences to craft a personalized, concise message.

### Skill Categories

**Guidance layer** (orientation — advise-only, never runs other skills):
- `profile-guide` — inspects the project's actual current state and recommends the single best next step, and explains how the pieces fit together. Points to the right skill/command but never invokes it. Triggers on how-to and "what should I do next / which skill for X" questions, NOT on concrete action requests (those belong to the dedicated skill).

**Data layer** (profile as source of truth):
- `profile-section`, `profile-refresh`, `profile-assemble`
- **Invocation policy:** `profile-section` is `disable-model-invocation: true` — it writes to the canonical `sections/*.json` source of truth, so it is invoked **explicitly** (`/profile-section`) to prevent accidental data corruption from a misread intent. It is never auto-triggered and is not invoked programmatically by other skills. Do not re-enable model invocation on it. `profile-refresh` stays model-invocable (safe-by-default additive merge, no-op detection) and can still be called by `profile-section` for dynamic sections once the user has explicitly run it. `/profile-init` (a command) is the other explicit data writer.

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

These are called **dynamic sections**. Their source configuration (platform + handle) is stored in the `sources` array of the user's `profile-index.json`, not in the plugin templates.

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

- `profile.md` — Assembled full profile document (Markdown, generated on demand by `profile-assemble`)
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

- **Playwright MCP** — configured in `.mcp.json` at the plugin root (auto-loaded for the plugin); required by `linkedin-review` for fetching LinkedIn profiles via browser automation
- **`gh` CLI** — used by `github-review` and `profile-refresh` for fetching GitHub profile data
- **Hashnode GraphQL API** — public API at `gql.hashnode.com`, used by `hashnode-review` and `profile-refresh` via WebFetch (no authentication required)

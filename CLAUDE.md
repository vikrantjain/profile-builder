# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Preference Routing

When the user says "remember that...", "my preference is...", "always...", "never...",
or any similar phrasing about how their profile data should be presented, exported,
or reviewed — **use the `profile-preferences` skill** to save the preference to
`preferences.md`. Do NOT save these as auto memory entries. Auto memory is for
operational notes only, not user presentation preferences.

## Overview

`profile-builder` is a Claude Code plugin for managing professional profiles. It
collects raw professional data from many sources (resume, LinkedIn, GitHub, blogs),
generates a structured profile, maintains it with targeted section updates, and
consumes it to produce downstream outputs (resumes, LinkedIn copy, GitHub READMEs,
etc.). There is no build system, test suite, or runtime — the project is schema
definitions, layout templates, skill definitions, and a few utility scripts.

The profile is a **canonical data layer**: sources are collected once into
`sections/*.json`, and every downstream consumer reads those files directly rather
than re-scraping sources.

## Architecture

### Key Files

- `profile-template.md` — the canonical field schema: `fields`, `sections` (maps
  each section to its `.json` output file and dependent fields), `json_structure`,
  and `placeholder_syntax`. Declarative only — no procedural instructions, no layout.
- `profile-layout.md` — the Markdown rendering template (`{{placeholder}}` layout).
  Used exclusively by `profile-assemble`. No field definitions.
- `profile-index-template.md` — JSON schema for `profile-index.json`, the manifest
  and configuration hub.
- `preferences.md` — user presentation preferences; consumed by export/review skills
  only. Created at runtime by `profile-preferences`.
- Generated, not checked in: `profile.md`, `profile-index.json`, `sections/*.json`.

### Data Format

- Section files are structured JSON with a `{ "section": "<key>", "data": { ... } }`
  envelope. Field names match `profile-template.md` exactly.
- The `sections` mapping in `profile-template.md` is the single source of truth for
  which fields belong to which section and the `.json` output path.
- JSON values are raw data — no Markdown formatting (`**`, `##`, `- `) in strings.
- **TBD convention**: required fields with no extractable data use `"TBD"` or
  `["TBD"]`; optional fields use `null` or are omitted (never TBD). Data-layer skills
  write TBD as-is; generate/export skills silently skip any value that is exactly
  `"TBD"`; `profile-validate` warns about TBD values.

### Lifecycle

1. **Init** — `/profile-init` collects sources, generates `profile-index.json` early
   (data sources + a `sections` array populated incrementally), builds all section
   files, verifies source coverage, and validates output. It configures data sources
   and tells the user to run `profile-refresh` when ready. Entry point; re-runnable.
2. **Maintain** — `/profile-section` builds or updates one section, using semantic
   field mapping and TBD defaults for required fields with no data. For dynamic
   sections it calls `profile-refresh` if sources are configured.
3. **Assemble** — `/profile-assemble` renders sections through `profile-layout.md`
   into `profile.md` on demand. This is an **optional side-branch, not a prerequisite
   for anything** — every generate and review skill reads `sections/*.json` directly.

## Skills and Commands

### Commands

- `/profile-init` — interactive onboarding; collects sources, builds all sections,
  generates the index. Entry point for new users.
- `/profile-validate` — validate profile documents against the schema (JSON validity,
  required fields, types, TBD values, legacy `.md` files); offers interactive fixes.
- `/linkedin-rec` — draft a recommendation-request message; takes `[Name], [Company],
  [optional: project]`.

### Skill Layers

- **Guidance** — `profile-guide` inspects current project state and recommends the
  single best next step. Advise-only; never runs other skills. Triggers on how-to and
  "what next / which skill for X" questions, NOT on concrete action requests.
- **Data layer** — `profile-section`, `profile-refresh`, `profile-assemble`.
  - **Invocation policy:** `profile-section` and `profile-assemble` are
    `disable-model-invocation: true` — run only via `/profile-section` and
    `/profile-assemble`, never auto-triggered or invoked by other skills. Do not
    re-enable model invocation on either. `profile-refresh` stays model-invocable and
    may be called by `profile-section` for dynamic sections. `/profile-init` is the
    other explicit data writer.
- **Preferences** — `profile-preferences` manages `preferences.md`.
- **Generate** (profile → platform content, no external access) — `linkedin-generate`,
  `resume-generate`, `github-generate`, `hashnode-generate`. Each reads
  `sections/*.json` and `preferences.md`.
- **Review** (fetch the live external profile, assess quality, suggest improvements) —
  `linkedin-review` (Playwright MCP), `github-review` (`gh` CLI / WebFetch),
  `hashnode-review` (Hashnode GraphQL API). Each reads the live platform and
  `preferences.md`; the focus is quality and impact, not data sync.

## Dynamic Sections

`blogs` (Hashnode, Dev.to) and `open_source` (GitHub) are **dynamic** — they track
data that changes on external platforms. All other sections are **static**, updated
only from user-provided data. Source config (platform + handle) lives in the
`sources` array of the user's `profile-index.json`, not in the plugin templates.
`profile-refresh` fetches latest data and updates the section files; it is never
called by `profile-assemble` or any export/review skill.

## Preferences

Stored in `preferences.md`, grouped under `## Global` (applies everywhere) or a
platform heading (`## LinkedIn`, `## Resume`, `## GitHub`, `## Hashnode`). Consumed by
export and review skills only — data-layer skills (`profile-section`,
`profile-refresh`, `profile-assemble`) ignore them. Manage via `profile-preferences`
or by editing the file directly.

## External Dependencies

- **Playwright MCP** — configured in `.mcp.json` at the plugin root; required by
  `linkedin-review`.
- **`gh` CLI** — used by `github-review` and `profile-refresh`.
- **Hashnode GraphQL API** — public endpoint `gql.hashnode.com` (no auth); used by
  `hashnode-review` and `profile-refresh` via WebFetch.

## Conventions

- `.profile/tmp/{YYYY-MM-DD}/{source}/` — temporary/intermediate data, organized by
  date and source. Never for final output. Cleaned up by `/profile-validate` (folders
  older than 30 days).
- Skill frontmatter uses `name` and `description` (third-person, with trigger
  phrases). Skill bodies use imperative/infinitive style.

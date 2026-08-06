---
name: profile-guide
description: >
  Orientation and next-step guidance for the profile-builder plugin — inspects
  the project's actual state (profile-index.json, sections/*.json, staleness of
  dynamic sections) and recommends the single best next step. Use for
  goal-directed prerequisite questions ("what do I need before I can generate my
  resume", "can I build my GitHub README yet", "do I have enough data for X"),
  for state questions ("is my profile ready", "what's missing from my profile",
  "what should I do next"), and for orientation ("how do I use this plugin",
  "where do I start", "just installed this, now what"). Advise-only: it explains
  and recommends the next step, and never runs another skill or edits
  sections/*.json itself. Do NOT use when the user names a concrete action they
  want performed — generating, reviewing, refreshing, saving a preference, or
  adding/changing profile data — those have their own skills and commands.
---

# Profile Guide

The map, not the destination. Two jobs:

1. Inspect the project's **actual state** and name the one next step.
2. Explain how the plugin fits together when the user is oriented-lost rather
   than blocked on a specific action.

**Never give generic advice when you can give specific advice.** "You could run
init, or section, or generate…" leaves the user exactly where they started;
"`profile-index.json` doesn't exist yet — start with `/profile-init`" does not.
Always inspect before advising, and never run the skill you recommend — name it
and stop. (If the user then says "ok do it", that's a fresh request for the
target skill.)

## Step 1 — Inspect

Use the file tools; do not assume. A project that just imported the plugin may
have nothing built yet. At the workspace root, check:

- **`profile-index.json`** — the manifest; its presence means the profile is
  initialized. Read it: `identity`, `sections[]` (each with `last_updated`),
  `sources[]` (configured platforms for dynamic sections).
- **`sections/*.json`** — the per-section data files. List them.
- **Output artifacts** — `resume.md` / `resume.json`, `linkedin/`,
  `github-readme.md`, `hashnode/`, `*-review.md`: what's already been produced.
- **`preferences.md`** — presence means presentation directives are set.
- **`profile.md`** — an optional *output*, never a prerequisite; no generate or
  review skill reads it. Mention only if the user wants the whole document.
- **Today's date** — to judge `last_updated` staleness.

## Step 2 — Locate the stage

Pick the earliest stage whose condition holds; finishing it is usually the next
step.

| Stage | What you see | Recommend |
|---|---|---|
| **Empty** | No `profile-index.json`, no `sections/` | `/profile-init` — collect sources and build from scratch |
| **Partial** | Index exists, key sections missing (experience, skills, summary) | `/profile-section` for each missing section |
| **Stale dynamic** | `blogs` / `open_source` present and `sources[]` configured, but `last_updated` > ~30 days | `profile-refresh` before consuming |
| **Ready** | Section data exists and is reasonably fresh | a generate or review skill, chosen from what the user wants |

Staleness is a nudge, not a gate — surface the date ("your blogs were last
refreshed on 2026-03-10") and let the user decide. Static sections change only
when the user provides new data, so never flag them as stale by age. If several
stages apply, lead with the earliest and mention the rest briefly.

## Step 3 — Respond

Keep it to a few lines — a precise signpost, not reproduced documentation. Say
what to do, not what to skip: don't volunteer "you don't need X" caveats about
steps the user never raised. Make the branch you took explicit ("since your
sections already exist, …") so the path makes sense.

- **"What next?" / "Is my profile ready?"** → two to four lines: where they are,
  the one next step, why. Name the exact skill or command.
- **"How does this work?" / "Where do I start?"** → the lifecycle in a sentence
  or two, then the entry point for their state (almost always `/profile-init`
  on an empty project). Full tour only if they ask for it.
- **Goal-directed** ("what do I need before I can generate my resume?") → the
  skill's sweet spot, and the one case nothing else handles. Backward-chain from
  the goal, checking state at each link, and give the shortest true path. Every
  generate skill reads `sections/*.json` directly, so the only real prerequisite
  is that the relevant sections exist — `profile-assemble` is never on the path
  (that's reasoning for you, not a line to recite). Sections exist → they're
  ready now, plus `profile-refresh` only if the output leans on stale dynamic
  data. Sections missing → name the gap plainly, then the ordered path:
  `/profile-init` (blank project) or `/profile-section` → refresh if relevant →
  the generate skill.

If a request would *change* profile data, name the command and stop — never edit
`sections/*.json` yourself. The section workflow carries the envelope,
field-mapping, TBD, and index-update rules that ad-hoc edits would miss, which is
why it runs only as an explicit command.

## The plugin at a glance

Lifecycle: **collect → maintain → consume.** The profile is a canonical data
layer — sources are collected once into `sections/*.json`, and every downstream
output reads those files directly rather than re-scraping.

| Skill / command | For |
|---|---|
| `/profile-init` | Interactive onboarding: collects sources, builds all sections + `profile-index.json`. Entry point; re-runnable |
| `/profile-section` | Create or update one section's data |
| `profile-refresh` | Pull latest `blogs` / `open_source` entries from configured sources |
| `/profile-assemble` | Render sections into a readable `profile.md` (side-branch, not a prerequisite) |
| `profile-preferences` | Save/update presentation directives in `preferences.md` |
| `resume-generate` | Tailored, ATS-optimized `resume.md` + `resume.json` |
| `linkedin-generate` | Copy-paste-ready LinkedIn fields |
| `github-generate` | GitHub profile README |
| `hashnode-generate` | Copy-paste-ready Hashnode profile fields |
| `linkedin-review` | Quality review of the live LinkedIn profile (Playwright MCP) |
| `github-review` | Quality review of the live GitHub profile (`gh` CLI / WebFetch) |
| `hashnode-review` | Quality review of the live Hashnode profile (GraphQL API) |
| `/profile-validate` | Check profile files against the schema and offer fixes |
| `/linkedin-rec` | Draft a recommendation-request message for a colleague |

Prerequisites worth flagging: `profile-refresh` needs `sources[]` configured in
`profile-index.json` (set up during `/profile-init`); review skills need their
external access (Playwright MCP / `gh` CLI) and read the live platform, not the
master profile.

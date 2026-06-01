---
name: profile-guide
description: >
  Orientation and how-to guide for the profile-builder plugin. Inspects the
  current project's actual state and recommends the single best next step.
  Use whenever the user asks how the plugin works or what to do next:
  "how do I use this plugin", "how does profile-builder work", "where do I
  start", "I'm new here", "what's the workflow", "what should I do next",
  "what can this plugin do", "which skill do I use for X", "what does the
  profile-section skill do", "is my profile ready", "what's missing from my
  profile", "help me get started with my profile", "I imported this plugin,
  now what". Especially trigger on goal-directed path questions where the user
  names a desired output and asks what it takes to get there: "I want to
  generate my resume, what do I need to do", "what's the path to a LinkedIn
  update", "what do I need before I can build my GitHub README", "can I
  generate a resume yet". Also trigger when the user seems lost about the
  profile workflow, asks an open-ended "help me with my profile / resume /
  LinkedIn" without naming a concrete action, or wants to understand how the
  pieces fit together.
  This skill only advises — it explains and recommends, then lets the user run
  the recommended skill themselves. Do NOT trigger when the user clearly wants
  to perform a concrete action (generate a resume, refresh blogs, assemble the
  profile, review their GitHub, save a preference) — those requests belong to
  the dedicated skill for that action. This is the map, not the destination.
---

# Profile Guide

This skill helps users find their way around the profile-builder plugin. Its
two jobs are (1) explain how the plugin works and what each skill is for, and
(2) look at the project's **actual current state** and recommend the one next
step that moves the user forward.

The single most important behavior: **never give generic advice when you can
give specific advice.** The plugin's whole value is that the profile is a
canonical data layer with a clear lifecycle. A user who hears "you could run
init, or section, or generate…" is no better off than before they asked.
A user who hears "your profile-index.json doesn't exist yet — start with
`/profile-init`" knows exactly what to do. Always inspect before advising.

This skill **only advises**. It explains and recommends; it does not run other
skills. After giving guidance, name the skill or command the user should invoke
and let them trigger it. (If they then say "ok do it", that's a fresh request
the target skill will handle.)

## Step 1 — Inspect the project state

Always start here. The recommendation is only as good as your read of reality,
so gather signals before saying anything. Look for these, at the workspace root:

- **`profile-index.json`** — the manifest. Its presence means the profile has
  been initialized. Read it and note: `identity`, the `sections[]` array (each
  with a `last_updated` date), and the `sources[]` array (configured external
  platforms for dynamic sections).
- **`sections/*.json`** — the per-section data files. List them.
- **`profile.md`** — the assembled, human-readable full profile. Treat it as an
  optional *output* the user can read or share, **not** a prerequisite for
  anything. No generate or review skill reads it — they read `sections/*.json`
  directly. Only mention `profile.md` if the user actually wants the
  consolidated document.
- **Output artifacts** — `resume.md` / `resume.json`, `linkedin/`,
  `github-readme.md`, `hashnode/`, and any `*-review.md`. These show what the
  user has already produced.
- **`preferences.md`** — presence means the user has set presentation directives.
- **Today's date** — needed to judge staleness of `last_updated` values.

Use the file tools to check existence and read `profile-index.json`. Do not
assume; a project that imported the plugin may have nothing built yet.

## Step 2 — Identify the lifecycle stage

Map what you found to one of these stages. Pick the earliest stage whose
condition is met — the user's next step is usually to finish that stage.

| Stage | What you see | Recommend |
|---|---|---|
| **Empty** | No `profile-index.json` and no `sections/` | `/profile-init` to collect sources and build the profile from scratch |
| **Partial** | Index exists but key sections missing from `sections[]` (e.g. no experience, skills, or summary) | `/profile-section` to build each missing section |
| **Stale dynamic data** | `blogs` / `open_source` sections present, `sources[]` configured, but their `last_updated` is well in the past (rough rule: > ~30 days) | `profile-refresh` to pull latest entries before consuming the profile |
| **Ready to consume** | Section data exists and is reasonably fresh | A generate or review skill, chosen from what the user wants (see map below) |

A separate **"wants the full document"** situation: if the user asks to read,
share, or eyeball their entire profile as one file, recommend `profile-assemble`
to produce `profile.md`. This is its own goal, not a step toward generating a
resume/LinkedIn/etc. — those never need `profile.md`.

Staleness is a heuristic, not a gate. The ~30-day rule for dynamic data is a
nudge, not a rule — surface it ("your blogs were last refreshed on
2026-03-10") and let the user decide. Static sections (identity, experience,
education, etc.) only change when the user provides new data, so don't flag
them as "stale" by age.

If several conditions are true at once, lead with the earliest stage but
mention the others briefly so the user sees the path ahead.

## Step 3 — Respond

Tailor the shape of the answer to what was asked.

**Answer affirmatively — say what to do, not what to skip.** Much of this skill's
knowledge (like "generate skills read `sections/*.json`, so `profile-assemble`
isn't a prerequisite") is reasoning *you* use to choose the right path. It is not
something to recite to the user. Don't volunteer "you don't need X" caveats about
steps the user never raised — a pre-emptive negative just plants a doubt that
wasn't there and clutters the signpost. Mention `profile-assemble` / `profile.md`
only when the user actually brings it up, or when they're clearly about to assume
it's required (e.g. they ask "do I assemble before generating?"). Otherwise, lead
with the next action and stop.

**If the user asked "what should I do next?" / "is my profile ready?"** — give a
two- to four-line answer: where they are, the one next step, and why. Name the
exact skill or command. Example:

> Your profile is initialized and the static sections look complete, but your
> blogs and open-source data were last refreshed on 2026-02-10 — about 3.5
> months ago. Run **`profile-refresh`** to pull the latest, and you're ready to
> generate any output you like.

**If the user asked "how does this plugin work?" / "where do I start?"** — give a
short orientation: the lifecycle in a sentence or two, then point them to the
right entry based on state (almost always `/profile-init` for an empty project).
Don't dump the entire skill map unless they ask for the full tour.

**If the user named a desired output and asked what it takes** ("I want to
generate my resume, what do I need to do?", "can I build my GitHub README
yet?") — this is a goal-directed question, and it's the skill's sweet spot.
Backward-chain from the goal through its prerequisites, checking state at each
link, then give the shortest true path:

- *(Your internal model of the dependency — use it to pick the path, don't
  recite it.)* Every generate skill (`resume-generate`, `linkedin-generate`,
  `github-generate`, `hashnode-generate`) reads the **section JSON files**
  (`sections/*.json`) directly, discovering them via `profile-index.json`. So
  the only true prerequisite is that the relevant section data exists —
  `profile-assemble` is never on this path. The one optional improvement
  beforehand is `profile-refresh`, when the output depends on dynamic sections
  (`blogs`, `open_source`) that have gone stale.
- **If section data exists** → the user is ready now. Tell them to run the
  generate skill, plus a genuinely-unmet prerequisite if there is one (e.g.
  "your blogs are months old, so `profile-refresh` first if you want them
  current"). Don't invent steps and don't add a "no need to assemble" aside —
  just give the affirmative path.
- **If section data is missing or sparse** → name the gap plainly ("there's no
  profile data yet") and give the ordered path: build sections
  (`/profile-init` for a blank project, or `/profile-section` for specific
  ones) → refresh dynamic sources if relevant → the generate skill.

Make the branch you took explicit so the user understands *why* the path is
what it is ("since your sections already exist, you can go straight to…"
vs. "since there's no section data yet, start with…").

**If the user asked "which skill do I use for X?" / "what does Y do?"** — answer
from the skill map below, in one or two lines, plus the one prerequisite that
actually matters (e.g. "resume-generate reads your `sections/*.json` directly,
so you just need the relevant sections built — refresh first only if dynamic
data is stale").

Keep it tight. This skill earns its keep by being a precise signpost, not by
reproducing the documentation.

## Reference — the plugin at a glance

**Lifecycle:** collect → maintain → consume.

```
/profile-init  ──>  /profile-section  ─────────────>  generate / review
(collect all)      (maintain one)         ▲           (reads sections/*.json)
                          │                │
                          └── profile-refresh (pull latest blogs / open_source)

         profile-assemble ──> profile.md   (optional: a single readable
                                            document to view or share)
```

The profile is a **canonical data layer**: sources are collected once into
section JSON (`sections/*.json`), and every downstream output reads those
section files directly rather than re-scraping. `profile-assemble` is a
side-branch that stitches the sections into one human-readable `profile.md` —
useful when you want to *read* the whole profile, but never required to
generate a resume, LinkedIn content, a README, or a review.

**Skill map** — what each piece is for and when to reach for it:

*Setup & data layer*
- **`/profile-init`** — interactive onboarding. Collects data from resume,
  GitHub, LinkedIn, blogs; builds all sections; writes `profile-index.json`.
  The entry point for an empty project; can be re-run to rebuild.
- **`/profile-section`** — create or update one section's data. Invoked
  explicitly (it writes the canonical data layer, so it is not auto-triggered):
  run `/profile-section` for targeted edits like "add a certification" or
  "update my current role".
- **`profile-refresh`** — pull latest entries for dynamic sections (`blogs`,
  `open_source`) from configured sources. Additive by default; preserves
  curated fields. Run before consuming if dynamic data is stale.
- **`profile-assemble`** — render the section JSON files into a single
  human-readable `profile.md`. Use only when the user wants the whole profile
  as one document to read or share. Not a prerequisite for any generate or
  review skill — those read `sections/*.json` directly.

*Preferences*
- **`profile-preferences`** — save/update/remove persistent presentation
  directives (tone, emphasis, framing) in `preferences.md`. Consumed by
  generate and review skills, not by the data layer.

*Generate (profile → platform-ready content, no external access)*
- **`resume-generate`** — tailored, ATS-optimized resume (`resume.md` +
  `resume.json`). Best with a job description to tailor against.
- **`linkedin-generate`** — copy-paste-ready LinkedIn fields (headline, about,
  experience, skills…).
- **`github-generate`** — GitHub profile README (`github-readme.md`).
- **`hashnode-generate`** — copy-paste-ready Hashnode profile fields.

*Review (fetch the live external profile, assess quality, suggest improvements)*
- **`linkedin-review`** — quality review of the live LinkedIn profile (needs
  Playwright MCP).
- **`github-review`** — review the live GitHub profile against the master
  profile (needs `gh` CLI / WebFetch).
- **`hashnode-review`** — review the live Hashnode profile via the public
  GraphQL API.

*Commands*
- **`/profile-validate`** — check the profile files against the schema (JSON
  validity, required fields, TBD values, legacy `.md` files) and offer fixes.
- **`/linkedin-rec`** — draft a recommendation-request message for a former
  colleague.

**Prerequisites worth flagging when relevant:**
- Generate skills read `sections/*.json` directly (via `profile-index.json`) →
  they just need the relevant sections to exist. `profile-assemble` / `profile.md`
  is **not** a prerequisite for them.
- `profile-refresh` is the one optional pre-step before generating, and only
  when the output leans on dynamic sections (`blogs`, `open_source`) that have
  gone stale. It needs `sources[]` configured in `profile-index.json` (set up
  during `/profile-init`).
- Review skills need their external access (Playwright MCP / `gh` CLI) and
  read the live platform, not the master profile.

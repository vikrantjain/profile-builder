# CLAUDE.md

`profile-builder` is a Claude Code plugin: schema definitions, layout templates, skill
definitions, and a routing-eval harness. There is no build system, test suite, or runtime —
do not go looking for one, and do not invent a test command. `README.md` maps the skills and
commands; `evals/README.md` covers the harness.

This file loads only for sessions inside this repo. It never loads in a project where the
plugin is installed. A rule that must shape the plugin's behavior for its users belongs in a
skill, command, or template. Written here, it is silently never applied.

## Invariants

Breaking any of these produces output that looks correct.

- **`profile-template.md` is the single source of truth.** It owns which fields belong to
  which section, each section's display `name` and `.json` output path, and the JSON
  envelope, TBD, and no-Markdown-in-values conventions. Read it rather than restating it
  elsewhere. Where a skill and the template disagree, the template wins.
- **The profile is a canonical data layer.** Sources are collected once into
  `sections/*.json`, and every downstream consumer reads those files directly. No generate,
  review, or assemble skill re-scrapes a source or calls `profile-refresh`.
- **Keep the three templates separate.** `profile-template.md` is declarative — no
  procedural instructions, no layout. `profile-layout.md` holds layout only and is read
  solely by `profile-assemble`. `profile-index-template.md` holds the index schema.
- **`profile-section` and `profile-assemble` are `disable-model-invocation: true`.** Do not
  re-enable it on either. Both touch the source of truth, so they run only when the user
  types the command. `profile-refresh` stays model-invocable.
- **`profile.md` is never a prerequisite.** `/profile-assemble` is an optional side-branch;
  every generate and review skill reads `sections/*.json`.
- **Cross-file references use `${CLAUDE_PLUGIN_ROOT}`.** A relative path resolves against the
  working directory rather than the plugin cache, so the skill silently proceeds without its
  reference doc.
- **Source config for dynamic sections lives in the user's `profile-index.json`.** The
  `sources` array carries platform and handle. Never hardcode either into a plugin template
  or a skill.
- **`.profile/tmp/{YYYY-MM-DD}/{source}/` is scratch.** Never write final output there;
  `/profile-validate` deletes stale folders.
- **Examples use placeholders, never the maintainer's data.** Write `janedoe` and
  `example.com`, not a real handle, blog, or name. This repo is copied to every installing
  user's machine, so a real value ships the maintainer's identity and reads as a default.
  Eval fixtures follow the same rule; see `evals/README.md`.

## Scope

Edit only this repo. The maintainer's own profile workspace lives elsewhere and is managed
separately. Do not change it from a session here, even to apply something this plugin now
supports. Name the change and leave it to the user.

## Preference routing

`profile-preferences`' description must keep claiming "remember that…", "always…", and
"never…" directives, and must keep telling the model to use it instead of auto-memory. That
description is the only place the rule reaches installed users. Export and review skills read
only `preferences.md`, so a preference saved as a memory is silently never applied.
Data-layer skills ignore preferences by design.

## profile-guide's scope

`profile-guide` answers goal-directed prerequisite, state, and orientation questions, and
nothing else. It is not a redirector: a data-change or assemble request routes to
`/profile-section` or `/profile-assemble` from those entries' own descriptions. Ablation
measured the redirect mandate as dead weight, which is why it was removed. Read that result
in `evals/README.md` before widening the description again.

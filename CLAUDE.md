# CLAUDE.md

`profile-builder` is a Claude Code plugin: schema definitions, layout templates, skill
definitions, and a routing-eval harness. There is no build system, test suite, or runtime —
do not go looking for one, and do not invent a test command. `README.md` maps the skills and
commands; `evals/README.md` covers the harness.

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

## Preference routing

"remember that…", "my preference is…", "always…", "never…" — anything about how profile data
is presented, exported, or reviewed — **goes to the `profile-preferences` skill**, which
writes `preferences.md`. Never store these as auto-memory. Export and review skills read
`preferences.md`, so a preference filed anywhere else is silently never applied. Data-layer
skills ignore preferences by design.

## profile-guide's scope

`profile-guide` answers goal-directed prerequisite, state, and orientation questions, and
nothing else. It is not a redirector: a data-change or assemble request routes to
`/profile-section` or `/profile-assemble` from those entries' own descriptions. Ablation
measured the redirect mandate as dead weight, which is why it was removed. Read that result
in `evals/README.md` before widening the description again.

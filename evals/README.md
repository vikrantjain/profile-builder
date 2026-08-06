# Routing evals

Skill descriptions decide which skill fires, and nothing type-checks them. This
directory is the regression net for that: a set of realistic user messages, the
route each one should take, and a harness that measures what actually happens.

The point is to make claims about a description **falsifiable**. A skill's value
can be measured by deleting it and re-running, rather than assumed.

## Layout

| File | What it is |
|---|---|
| `profile-guide-trigger-evals.json` | 20 user messages, each with the `expected_route` it should take |
| `harness.py` | Builds the routing catalog from live frontmatter, writes prompts, scores responses |
| `run.sh` | End-to-end: build → route → score |

### Fixtures

Queries are deliberately messy — lowercase, typos, trailing context — because
clean phrasings don't discriminate between descriptions. All biographical detail
is **synthetic** (Jordan Rivera, Northwind Systems, Belmont Consulting, Fairmont
State University). Keep it that way: this repo is published and copied to every
installing user's machine, and the routing signal lives in the verbs, not the
proper nouns.

`expected_route` is a skill name (`resume-generate`) when the model should invoke
it directly, or a slash command (`/profile-section`) when the model can only tell
the user to run it. `should_trigger` is the narrower legacy question of whether
`profile-guide` specifically fires.

## Running

Requires the `claude` CLI on `PATH`. Python 3 stdlib is enough — `pyyaml` is used
when present, otherwise a built-in fallback parser handles this repo's
frontmatter. Both produce a byte-identical catalog.

```shell
./run.sh                    # both conditions, 40 model calls
REPEAT=5 ./run.sh           # 5 runs per query, to surface flaky routing
CONDITIONS="current" ./run.sh
WORK=./out ./run.sh         # keep artifacts instead of using a temp dir
```

Conditions are `current` (every skill as it exists on disk) and `ablated`
(identical, minus `profile-guide`). Each call runs from an empty scratch
directory, so the model sees only the catalog in the prompt — running from the
repo would pick up `CLAUDE.md` and score the project instructions instead of the
descriptions under test.

Inspect a catalog without spending calls:

```shell
python3 harness.py catalog current
python3 harness.py catalog ablated
```

## Result on 2026-08-06

Run against the shipped descriptions, 116 calls across 4 conditions:

```
current    20/20 routed as expected
ablated    17/20 routed as expected

3/20 routing outcomes differ -- queries [6, 7, 8]
  [06] just installed this profile-builder plugin, now what
  [07] I want to generate my resume for a job application, what do I need to do first?
  [08] is my profile ready or is something still missing?
```

**17 of 20 outcomes are identical with or without `profile-guide`.** Every
data-change and assemble query routed correctly to its own command without it,
and never invoked `profile-guide` even under the older, much longer description —
so the redirect mandate that description carried was dead weight, and was removed.

The three differing cases are all guidance questions. `[07]` is the clearest
justification for the skill existing: without it, `resume-generate` fires 5/5 and
generates against possibly-missing data. `[06]` and `[07]` are partial — the
ablated routes (`/profile-init`, `/profile-validate`) are plausible but blind to
actual project state and staleness.

That measurement is why `profile-guide`'s description is scoped to goal-directed
prerequisite, state, and orientation questions, and nothing else.

### Caveat

The harness gives the model an explicit `tell_user_to_run` slot that real Claude
Code does not. That almost certainly overstates how reliably the seven
data-change queries get their command named unprompted. Read the redirect finding
as "contributes very little," not "contributes exactly zero."

## Note on distribution

Plugins are copied wholesale to `~/.claude/plugins/cache`, so this directory does
land on installing machines. It is inert — only `skills/`, `commands/`, `agents/`,
and `hooks/` are discovered, so nothing here enters anyone's context. There is no
packaging exclude mechanism in the plugin spec; the cost is a few KB on disk.

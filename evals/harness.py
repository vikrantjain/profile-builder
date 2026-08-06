#!/usr/bin/env python3
"""Routing-eval harness for profile-builder skill/command descriptions.

Skill descriptions are the only part of this plugin that decides *which* skill
fires, and nothing type-checks them. This harness measures that routing directly:
it builds a catalog from the live frontmatter, asks a model to route each eval
query using only those descriptions, and scores the answer against the expected
route.

Two conditions are supported, so the value of a skill can be measured by removing
it rather than assumed:

    current  — every skill/command as it exists on disk right now
    ablated  — identical, minus profile-guide

Subcommands (see run.sh for the usual end-to-end invocation):

    catalog <condition>                 print the routing catalog
    prompts <condition> <outdir>        write one .prompt file per eval query
    score   <outdir> [condition ...]    score model responses in <outdir>
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EVALS = os.path.join(HERE, "profile-guide-trigger-evals.json")

CONDITIONS = ("current", "ablated")
ABLATE = "profile-guide"

PROMPT = """You are Claude Code. The user has the "profile-builder" plugin installed in their project. These are the plugin's available skills and commands:

{catalog}

The user's message is:
"{query}"

Decide how this request is handled, based ONLY on the descriptions above.

Respond with ONE line of JSON and nothing else, no markdown fence:
{{"invoke":"<skill name from the AUTO-INVOCABLE list, or NONE>","tell_user_to_run":"<command from the USER-TYPED ONLY list, or NONE>"}}

"invoke" is the skill you would auto-invoke yourself. "tell_user_to_run" is a command you would instead instruct the user to type (you cannot run those). Either may be NONE. Do not pick both unless you genuinely would do both."""


# --- frontmatter -----------------------------------------------------------

def _scalar(v):
    if len(v) > 1 and v[0] in "\"'" and v[-1] == v[0]:
        v = v[1:-1]
    return {"true": True, "false": False}.get(v, v)


def _fallback(block):
    """Minimal YAML subset: top-level scalars plus folded/literal block scalars.

    Covers everything this repo's frontmatter uses. Not a general YAML parser --
    it exists so the harness runs with a bare stdlib Python. Note that a naive
    regex does NOT work here: most descriptions are folded scalars ('>') and a
    line-oriented match silently truncates them at the first blank line.
    """
    data, key, buf = {}, None, []

    def flush():
        if key is not None:
            data[key] = " ".join(" ".join(buf).split())

    for line in block.splitlines():
        if line[:1] not in (" ", "\t") and ":" in line:
            flush()
            k, _, val = line.partition(":")
            k, val = k.strip(), val.strip()
            if val in (">", ">-", "|", "|-", ""):
                key, buf = k, []
            else:
                data[k] = _scalar(val)
                key, buf = None, []
        elif key is not None:
            buf.append(line.strip())
    flush()
    return data


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    try:
        import yaml
        return yaml.safe_load(m.group(1)) or {}
    except ImportError:
        return _fallback(m.group(1))


def norm(s):
    return " ".join((s or "").split())


# --- catalog ---------------------------------------------------------------

def build_catalog(condition):
    """Render the plugin's skills and commands as a routing catalog.

    Skills split on `disable-model-invocation`: those carrying it can only be
    typed by the user, so the model must recommend them rather than call them.
    Getting that split right is the whole point -- it is what lets the score
    distinguish "routed correctly" from "did the write itself".
    """
    auto, explicit = [], []
    for path in sorted(glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md"))):
        with open(path) as fh:
            fm = frontmatter(fh.read())
        name, desc = fm.get("name", ""), norm(fm.get("description"))
        if not name:
            continue
        if condition == "ablated" and name == ABLATE:
            continue
        if fm.get("disable-model-invocation"):
            explicit.append(f"- /{name}: {desc}")
        else:
            auto.append(f"- {name}: {desc}")

    for path in sorted(glob.glob(os.path.join(ROOT, "commands", "*.md"))):
        with open(path) as fh:
            fm = frontmatter(fh.read())
        name = os.path.basename(path)[:-3]
        explicit.append(f"- /{name}: {norm(fm.get('description'))}")

    return "\n".join(
        ["AUTO-INVOCABLE SKILLS (you may invoke these yourself when the description matches):"]
        + auto
        + ["", "USER-TYPED ONLY (you CANNOT invoke these; you may only tell the user to run them):"]
        + explicit
    )


# --- prompts ---------------------------------------------------------------

def load_evals():
    with open(EVALS) as fh:
        return json.load(fh)


def write_prompts(condition, outdir):
    catalog = build_catalog(condition)
    os.makedirs(outdir, exist_ok=True)
    evals = load_evals()
    for i, ev in enumerate(evals):
        dest = os.path.join(outdir, f"{condition}__{i:02d}.prompt")
        with open(dest, "w") as fh:
            fh.write(PROMPT.format(catalog=catalog, query=ev["query"]))
    return len(evals)


# --- scoring ---------------------------------------------------------------

def parse_response(text):
    """Pull the routing decision out of a model response.

    Returns the route the model chose, or None if the response was unparseable.
    A model that both invokes and recommends is scored on the invoke -- that is
    the action it actually took.
    """
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        obj = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    invoke = norm(str(obj.get("invoke", "NONE")))
    typed = norm(str(obj.get("tell_user_to_run", "NONE")))
    if invoke and invoke.upper() != "NONE":
        return invoke
    if typed and typed.upper() != "NONE":
        return typed if typed.startswith("/") else "/" + typed
    return "NONE"


def collect(outdir, condition, idx):
    """All responses for one (condition, query), across repeat runs."""
    routes = []
    pattern = os.path.join(outdir, f"{condition}__{idx:02d}*.json")
    for path in sorted(glob.glob(pattern)):
        with open(path) as fh:
            routes.append(parse_response(fh.read()))
    return routes


def score(outdir, conditions):
    evals = load_evals()
    present = [c for c in conditions
               if glob.glob(os.path.join(outdir, f"{c}__*.json"))]
    if not present:
        sys.exit(f"no model responses found in {outdir}")

    hits = {c: 0 for c in present}
    flaky = []
    rows = []

    for i, ev in enumerate(evals):
        expected = ev["expected_route"]
        cells = []
        for c in present:
            routes = collect(outdir, c, i)
            if not routes:
                cells.append("-")
                continue
            uniq = sorted(set(routes), key=str)
            if len(uniq) > 1:
                flaky.append((i, c, routes))
            top = max(uniq, key=routes.count)
            if top == expected:
                hits[c] += 1
            mark = " *" if len(uniq) > 1 else ("" if top == expected else " !")
            cells.append(f"{top}{mark}")
        rows.append((i, expected, cells))

    width = max([len(c) for c in present + ["expected"]]
                + [len(x) for _, e, cs in rows for x in cs + [e]]) + 2

    header = f"{'#':>3}  {'expected':<{width}}" + "".join(f"{c:<{width}}" for c in present)
    print(header)
    print("-" * len(header))
    for i, expected, cells in rows:
        print(f"{i:>3}  {expected:<{width}}" + "".join(f"{x:<{width}}" for x in cells))

    print()
    total = len(evals)
    for c in present:
        print(f"{c:<{width}} {hits[c]}/{total} routed as expected")

    if len(present) > 1:
        base = present[0]
        for c in present[1:]:
            diffs = [i for i in range(total)
                     if collect(outdir, base, i) and collect(outdir, c, i)
                     and max(set(collect(outdir, base, i)), key=collect(outdir, base, i).count)
                     != max(set(collect(outdir, c, i)), key=collect(outdir, c, i).count)]
            print(f"\n{base} vs {c}: {len(diffs)}/{total} routing outcomes differ"
                  + (f" -- queries {diffs}" if diffs else ""))
            for i in diffs:
                print(f"  [{i:02d}] {load_evals()[i]['query'][:70]}")

    if flaky:
        print("\nflaky (* above -- disagreed across repeat runs):")
        for i, c, routes in flaky:
            print(f"  [{i:02d}] {c}: {routes}")


# --- cli -------------------------------------------------------------------

def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    cmd = argv[1]

    if cmd == "catalog":
        cond = argv[2] if len(argv) > 2 else "current"
        print(build_catalog(cond))
    elif cmd == "prompts":
        if len(argv) < 4:
            sys.exit("usage: harness.py prompts <condition> <outdir>")
        n = write_prompts(argv[2], argv[3])
        print(f"{argv[2]}: wrote {n} prompts to {argv[3]}")
    elif cmd == "score":
        if len(argv) < 3:
            sys.exit("usage: harness.py score <outdir> [condition ...]")
        score(argv[2], argv[3:] or list(CONDITIONS))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv)

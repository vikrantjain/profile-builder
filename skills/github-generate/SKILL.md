---
name: github-generate
description: >
  Generate a GitHub profile README.md that establishes technical identity from
  master profile data. Use when the user asks to "generate GitHub README",
  "create GitHub profile", "export profile for GitHub", "build my GitHub
  profile README", "update my GitHub bio", "make my GitHub look good",
  "showcase my projects on GitHub", "developer portfolio README",
  "GitHub profile page", "tech stack badges", or wants a GitHub profile
  README.md generated from their master profile data. Also trigger when the
  user mentions GitHub in the context of developer branding, open source
  presence, or professional visibility — even if they don't say "generate"
  or "README".
---

# GitHub Generate

Generate a GitHub profile README.md from the master profile data — a
technical identity document built for the developer audience.

## Core Philosophy

A GitHub profile README is not a reformatted resume or a trimmed LinkedIn
About. It speaks to a fundamentally different audience: developers, hiring
engineers, open source maintainers, and potential collaborators. These people
read code, review PRs, and evaluate technical depth. They care about what you
build, how you think, and what you ship — not corporate job titles or
enterprise buzzwords.

The master profile is a comprehensive datastore. The GitHub README should
distill it into a **technical identity** — what kind of engineer are you,
what's your stack, what have you built, and where can people find your work.
Every section should earn its place by signaling builder credibility, not by
restating the resume.

**Above the fold matters.** GitHub renders the README on the profile page.
The first screenful — roughly the header, intro, and start of the tech
stack — is what most visitors see. Make it count: distinctive intro, clear
technical positioning, visual badges that communicate at a glance. Detailed
sections (projects, contributions, blog posts) live below and reward visitors
who scroll.

## Workflow

### 1. Determine Scope

Ask or infer what the user needs:

- **Full README**: generate the complete profile README
- **Single section**: e.g., "just update my tech stack badges" or "redo the
  featured projects"
- **Specific element**: e.g., "write me a better GitHub intro" or "add my
  blog posts"

For single-section requests, still read enough context to make good decisions
(see the read-set table below).

### 2. Read Profile Data

Read `profile-index.json` to discover available sections and their file paths.
Then read the relevant section JSON files from `sections/`. Parse each JSON
file and access fields directly from the `data` object.

#### What to read for each scope

Full README requires all available section files. For single-section requests:

| Request | Minimum sections to read |
|---------|--------------------------|
| Full README | identity, summary, experience, skills, open-source, blogs |
| Intro / About | identity, summary, experience |
| Tech Stack | identity, skills, experience (for context) |
| Featured Projects | identity, open-source, experience (for context) |
| Contributions | open-source |
| Blog Posts | blogs |
| Connect / Social | identity |

Key sections and what they provide:

- `sections/identity.json` — name, title, GitHub URL, social links
- `sections/summary.json` — professional bio (raw material for the intro)
- `sections/experience.json` — career context, domain expertise, scale signals
  (enriches the intro and provides framing for project highlights)
- `sections/skills.json` — tech stack for badges, grouped by category
- `sections/open-source.json` — projects and contributions to highlight
- `sections/blogs.json` — recent posts (if available)
- `sections/certifications.json` — notable certifications (badge-worthy ones)
- `sections/patents.json` — patents (if user wants to highlight)

If required section JSON files do not exist, inform the user and suggest
running `/profile-init` or `/profile-section` to generate them.

### 3. Apply Presentation Preferences

Read `preferences.md` from the workspace root. If it exists:

1. Read the `## Global` section — these apply to all exports.
2. Read the `## GitHub` section (if present) — these are GitHub-specific.
3. Treat each preference as a binding directive during content transformation.
   Examples: "present experience as 20+ years" → use that framing; "don't
   highlight patents" → omit; tone directives → adjust writing style.
4. GitHub-specific preferences take precedence over global if they conflict.

If `preferences.md` does not exist, proceed with default behavior.

### 4. Determine GitHub Username

Extract the GitHub username from the GitHub URL in the identity section.
This is needed for linking to repositories and for the profile repo name.

### 5. Generate README Content

**TBD filtering:** Profile data may contain `TBD` as a placeholder value in
any field (indicating data not yet filled in by the user). When rendering
output, silently skip any value that is exactly `TBD` — do not render it.
If all items in a list are `TBD`, omit that list/block entirely.

**Content fidelity:** The README must be accurate to the source data. If an
impact value is qualified in the source (e.g., "projected", "estimated"),
retain that qualifier. Use verbs that reflect what the person actually did —
"designed", "contributed to", "maintained" — not inflated verbs that imply
sole ownership of a team effort. Developers who read your README may also read
your commit history; inflated claims erode credibility fast in this audience.

Consult `${CLAUDE_PLUGIN_ROOT}/skills/github-generate/references/github-readme-conventions.md`
for formatting conventions, badge syntax, layout patterns, and stats widgets.

Build the README with these sections (skip any that lack data):

#### Header

`# ` heading with the user's name. Below it, a one-line subtitle — not the
corporate job title verbatim, but a technical positioning statement. Think
"what kind of engineer" rather than "what org chart box":

- Good: "Platform engineer building event-driven systems at scale"
- Good: "Full-stack developer | Open source contributor | Building tools for developers"
- Weak: "Senior Software Engineer at Acme Corp"

Draw from `identity.json` (title), `summary.json`, and `experience.json`
(recent role context) to construct this. If the user's profile shows they
build things, lead with what they build.

#### About

This is the intro paragraph — 2-4 sentences that establish technical identity.
Do not restate `summary.json` in prose. Construct it from multiple sources:

1. **Open with a hook** — What's distinctive about this person as an engineer?
   A domain they've spent years in, a type of system they specialize in, a
   problem space they keep returning to. This should be specific enough that
   another developer reads it and thinks "oh, that's interesting."
2. **Add technical depth** — Pull from `experience.json` to ground the intro
   in real work. Mention scale signals (systems serving millions, teams led,
   platforms built) where they exist in the source data. This is where
   `experience.json` earns its place — it provides the substance that
   `summary.json` alone can't.
3. **Close with current focus** — What are they building or exploring now?
   Current role context, open source focus, or learning direction.

The tone should be conversational-technical — how you'd introduce yourself
at a conference, not how you'd open a cover letter. First person is fine.
Skip corporate language ("leveraging", "driving value", "stakeholder
alignment").

#### Tech Stack

Skills rendered as shields.io badges. This section is visual — badges
communicate at a glance what the person works with. But visual noise from
too many badges is worse than too few.

Strategy:

1. **Curate, don't dump.** The profile's skills section may have 50+ skills
   across many categories. A GitHub README should show 15-25 badges — the
   tools this person actually reaches for. Prioritize by:
   - Languages and frameworks they actively use (recent experience signals this)
   - Infrastructure and platforms central to their work
   - Tools that signal their type of engineering (e.g., Terraform signals
     infrastructure-as-code thinking; PyTorch signals ML practitioner)
2. **Group by function**, not by the profile's category names. Good groups:
   "Languages", "Frontend", "Backend", "Cloud & Infrastructure", "Data & ML",
   "Tools". The groups should reflect how the developer thinks about their
   stack.
3. **Order within groups** — Primary/strongest tools first within each group.
4. **Use consistent badge style** — `flat` or `for-the-badge` throughout, not
   mixed. Consult the reference file for badge format and color codes.
5. **Skip the obvious** — Git, VS Code, and similar ubiquitous tools add no
   signal unless the user specifically wants them.

#### Featured Projects

The showcase section — this is where builder credibility lives. Source from
`sections/open-source.json` projects.

1. **Select 3-5 projects.** Pick by a combination of: technical
   impressiveness, relevance to the user's identity, and available impact
   metrics (stars, downloads, adoption). If the user has fewer than 3 open
   source projects, this section can include notable work projects that are
   publicly referenceable.
2. **For each project, include:**
   - Project name as a linked heading (`### [Project Name](url)`)
   - One-line description of what it does (from the project's `description`)
   - 1-2 notable `contributions` bullets describing key technical work
   - `impact` metrics as supporting details (star count, downloads, users)
     if available in the source data
   - Tech stack as inline badges or a brief tag line
3. **Order by impact** — most impressive or identity-defining project first.
4. **Don't just list repos.** A bare list of repo links with one-line
   descriptions is the minimum-effort pattern. The value of the README over
   the pinned repos is that it can tell the story — what you built, why it
   matters, and what the technical challenges were.

#### Open Source Contributions

Contributions to *other* projects — PRs merged, issues filed, docs written,
projects maintained. Source from `sections/open-source.json` contributions.

This section matters because it signals community participation — the person
doesn't just build their own things, they improve the ecosystem. Format as
a compact list:

- **[Project Name](url)** — What you did (PR type, description)

Keep to the 3-5 most notable. Skip if the user has no external contributions.

#### Recent Blog Posts

Links to recent posts from `sections/blogs.json`. Format:

- [Post Title](url) — Brief excerpt or topic

Include 3-5 most recent. Skip if no blog data exists.

#### Connect

Social links — LinkedIn, website, Twitter/X — as shields.io badges or
simple linked text. Keep compact. This section lives at the bottom and
should be minimal.

### 6. Verify Before Writing

Before writing output, run two checks and revise if either fails:

**Content fidelity spot-check** — Scan every quantified claim and action
verb in the output. Does anything overstate the source? Are any qualifiers
dropped? Were contributions attributed to the right projects? This is a
fast pass — focus on the areas most prone to drift.

**Preferences compliance** — Re-read the applicable preferences and verify
each one is reflected in the generated content. If any preference was missed
or contradicted, revise before proceeding.

### 7. Write Output

Write the generated README to `github-readme.md`.

### 8. Present to User

Display the generated content in the conversation. Note that the user needs
to copy it to their `<username>/<username>` repository's `README.md`.

If the README is long, show the above-the-fold portion (header through tech
stack) inline and summarize the rest — the user can read the full file
directly.

## Output Checklist

Before finishing, verify:

- [ ] Header has a technical positioning subtitle (not just a corporate title)
- [ ] About section was constructed from summary + experience (not just trimmed summary)
- [ ] Tech stack badges are curated (15-25, not a full dump) and grouped by function
- [ ] Featured projects include contributions and impact, not just repo links
- [ ] All repo links point to valid GitHub URLs (based on profile data)
- [ ] Badges use correct shields.io format with consistent style
- [ ] Above-the-fold content is strong (header + intro + tech stack)
- [ ] No profile data fabricated — all sourced from master profile
- [ ] Source qualifiers preserved (projected/estimated/targeted)
- [ ] File written to `github-readme.md`
- [ ] Output honors all applicable presentation preferences (global + GitHub-specific)

## Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/skills/github-generate/references/github-readme-conventions.md`** — Badge catalog, layout patterns, stats widgets, and formatting best practices

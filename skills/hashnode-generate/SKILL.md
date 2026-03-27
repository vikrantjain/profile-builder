---
name: hashnode-generate
description: >
  Generate copy-paste-ready Hashnode profile content from master profile data,
  optimized for a technical blog reading audience. Use when the user asks to
  "generate Hashnode profile content", "export profile for Hashnode", "create
  Hashnode bio", "format my tagline for Hashnode", "update my Hashnode about
  page", "prepare Hashnode profile update", "optimize my Hashnode profile",
  "Hashnode makeover", "what should my Hashnode say", or wants copy-paste-ready
  content for their Hashnode profile fields (not blog articles). Also trigger
  when the user mentions Hashnode in the context of developer branding, blog
  presence, or technical writing visibility — even if they don't say "generate".
---

# Hashnode Generate

Generate copy-paste-ready content for Hashnode profile fields, optimized for
the technical blog reading audience. This skill covers profile metadata only
(tagline, bio, about page, tech stack, social links) — not blog articles.

## Core Philosophy

Hashnode is a developer blogging platform. The audience is not recruiters or
hiring managers — it's developers, tech leads, and engineering managers who
read technical blogs, evaluate whether a writer knows their domain, and decide
whether to follow or subscribe. A Hashnode profile needs to establish the
writer's **technical credibility and writing voice** in seconds.

The master profile is a comprehensive datastore. The Hashnode profile should
distill it into a **writer identity** — what domains you're deep in, what
you've built, and why your perspective is worth following. Every field should
signal that this person ships real systems and writes about them from
experience, not that they hold a corporate title.

**Tagline and bio are the storefront.** On Hashnode, the tagline appears on
every blog post card and in search results. The bio appears on the profile
page below the name. Together, they're the first (often only) impression a
reader gets before deciding to click through. These two fields carry
disproportionate weight — invest accordingly.

**The about page is for readers who want depth.** Someone clicked through to
the profile because a blog post resonated. The about page should reward that
curiosity with substance — real systems built, domains explored, and a clear
sense of the writer's technical range and depth. It should feel like reading
a well-structured README, not a corporate bio.

## Workflow

### 1. Determine Scope

Ask or infer what the user needs:

- **Full export**: generate all Hashnode profile fields
- **Single field**: e.g., "write my Hashnode tagline" or "update my Hashnode about page"

#### What to read for each scope

Full export requires all available section files. For single-field requests,
context beyond the obvious source improves quality:

| Request | Minimum sections to read |
|---------|--------------------------|
| Tagline | identity, summary, skills, blogs |
| Bio | identity, summary, experience, blogs |
| About page | identity, summary, experience, skills, open-source, blogs |
| Tech stack | skills, experience (for context) |
| Social links | identity |

### 2. Read Profile Sections

Read the relevant profile section JSON files from `sections/`. Consult
`profile-index.json` to discover available sections and their file paths.
Parse each JSON file and access fields directly from the `data` object.

If required section JSON files do not exist, inform the user and suggest
running `/profile-init` or `profile-section` to generate them.

Key sections and what they provide:

- `sections/identity.json` — name, title, GitHub URL, social links
- `sections/summary.json` — professional bio (raw material, needs adaptation)
- `sections/experience.json` — career depth, domain expertise, scale signals
- `sections/skills.json` — tech stack for tags and about page content
- `sections/open-source.json` — projects and contributions (strong credibility signals)
- `sections/blogs.json` — recent posts (validates the writing identity)

### 3. Apply Presentation Preferences

Read `preferences.md` from the workspace root. If it exists:

1. Read the `## Global` section — these apply to all exports.
2. Read the `## Hashnode` section (if present) — these are Hashnode-specific.
3. Treat each preference as a binding directive during content transformation.
   Examples: "present experience as 20+ years" -> use that framing; "don't
   highlight patents" -> de-emphasize or omit; tone directives -> adjust writing
   style accordingly.
4. Hashnode-specific preferences take precedence over global if they conflict.

If `preferences.md` does not exist, proceed with default behavior.

### 4. Apply Hashnode Constraints

Consult `${CLAUDE_PLUGIN_ROOT}/skills/hashnode-generate/references/hashnode-constraints.md` for:

- Character limits per field
- Markdown support (Hashnode supports full Markdown in the about page)
- Field mapping from master profile to Hashnode profile fields
- Best practices for Hashnode profiles

### 5. Transform Content

This is where profile data becomes a Hashnode writer identity. Two principles
govern every transformation:

**Content fidelity** — Hashnode content must be accurate to the source data.
If an impact value is qualified in the source (e.g., "projected", "estimated"),
retain that qualifier. Use verbs that reflect what the person actually did —
"designed", "contributed to", "maintained" — not inflated verbs that imply
sole ownership. Technical readers are the hardest audience to bluff — they
notice when a "contributor" claims to have "architected" something solo.

**TBD filtering** — Profile data may contain `TBD` as a placeholder value.
Silently skip any value that is exactly `TBD`. If all items in a list are
`TBD`, omit that list/block entirely.

For each target Hashnode field:

#### Tagline

The tagline appears on every blog post card — it's the line readers see next
to the author's name before they decide whether the post is worth their time.
Do not take the profile's `title` field and trim it.

Construct the tagline to signal **what the person builds and writes about**:

1. **Lead with the engineering identity**, not the job title. "Platform
   engineer" is better than "Senior Software Engineer". "Building event-driven
   systems" is better than "Working at Acme Corp".
2. **Include 1-2 domain or technology signals** that tell readers what blog
   topics to expect. A reader scanning post cards should think "this person
   writes about things I care about."
3. **Keep it punchy.** Max 150 chars, plain text only. Aim for the 100-140
   range — enough to say something distinctive, not so long it gets clipped
   on mobile.

Examples of strong taglines:
- "Platform engineer | Building distributed systems with Go & Kubernetes"
- "Full-stack developer writing about React, Node.js, and developer tooling"
- "Cloud architect | AWS, Terraform, and the art of infrastructure as code"

Weak: "Senior Software Engineer at Acme Corp" (corporate, no topic signal)
Weak: "Passionate about technology" (generic, no specificity)

#### Bio

The bio appears below the name on the profile page — it's the reader's first
impression when they visit the profile. Max 200 chars, plain text only.

Do not restate the tagline. The bio should complement it with a different
angle:

1. **Add career depth** — years of experience, number of domains, or scale
   signals. Draw from `experience.json` to ground this in real work.
2. **Mention the writing angle** — If the user has blog data, reference what
   they write about. If not, reference the domain they'd write from.
3. **One differentiator** — what makes this writer's perspective unique?
   A patent holder, an open source maintainer, someone who's built systems
   at a specific scale?

The bio should make a reader think "this person has real experience behind
their posts."

#### About Page

The about page is the long-form profile — full Markdown supported, no hard
character limit. This is where the writer's full technical identity lives.

Do not paste the professional summary in prose and call it done. Build the
about page as a structured document that a technical reader can scan:

1. **Opening paragraph** (2-4 sentences) — Who are you as a technical
   professional, and what kind of systems do you build? Open with a hook
   that's specific enough to be interesting: a domain you've worked deeply
   in, a type of problem you specialize in, or a scale you've operated at.
   Draw from `summary.json` and `experience.json` — the experience data
   provides the substance that the summary alone can't. Tone should be
   conversational-technical — how you'd introduce yourself at a tech
   conference, not how you'd open a cover letter.

2. **What I Write About** — A brief section (3-5 bullet points or a short
   paragraph) describing the topics the reader can expect. Source from
   `blogs.json` post topics if available, or infer from skills and
   experience. This helps readers decide whether to follow. If blog data
   exists, mention the breadth: "I write about X, Y, and Z — from deep
   dives to practical tutorials."

3. **Tech Stack** — Skills rendered as a readable list or grouped by
   function. Don't dump every skill from the profile. Curate 10-15 core
   technologies that define the writer's stack, grouped meaningfully
   (Languages, Frameworks, Cloud & Infrastructure, Tools). This tells
   readers what technology perspective the blog posts come from.

4. **Featured Work** (if open-source data exists) — 2-4 notable projects
   or contributions with brief descriptions. Include links. Open source
   work is a strong credibility signal for a technical blogging audience —
   it proves the writer ships, not just opines.

5. **Recent Posts** (if blog data exists) — Links to 3-5 recent articles.
   This rewards the reader who clicked through to the profile from a post
   they liked — "here's more where that came from." Format as linked titles
   with a one-line description or topic tag.

6. **Connect** — Links to GitHub, LinkedIn, Twitter/X, personal website.
   Keep compact — a few lines at the bottom. Use Markdown links.

Sections without data should be omitted entirely, not left as empty headers.

#### Tech Stack Tags

Hashnode uses a tag system for the tech stack field. Each tag is a single
technology name.

1. **Curate to 5-10 core technologies.** The profile's skills section may
   list 50+. For Hashnode tags, select the technologies that define the
   writer's identity — what they actually build with and write about.
2. **Prioritize by blog relevance.** If the user has blog posts, weight
   technologies that appear in their writing. A Hashnode tech stack should
   signal "these are the technologies I have opinions about."
3. **Use canonical tag names** that match Hashnode's existing tag taxonomy
   (e.g., "JavaScript" not "JS", "Node.js" not "NodeJS").
4. **Skip the generic.** Git, VS Code, and other ubiquitous tools add no
   signal. Include technologies that differentiate.

#### Social Links

Extract matching URLs from `sections/identity.json` contact and social fields.
Map to Hashnode's supported link fields: GitHub, Twitter/X, LinkedIn, Website,
Stack Overflow, Facebook, YouTube.

### 6. Verify Before Writing

Before writing output, run two checks and revise content if either fails:

**Content fidelity spot-check** — Scan every quantified claim and action verb
in the output. Does anything overstate the source? Are any qualifiers dropped?
This is a fast pass against the fidelity principle — focus on the areas most
prone to drift.

**Preferences compliance** — Re-read the applicable preferences and verify each
one is reflected in the generated content. If any preference was missed or
contradicted, revise the content before proceeding.

### 7. Write Output

Write the formatted content to `hashnode/`. Create the directory if
it does not exist.

For a full export, generate these files:

- `hashnode/tagline.md` — Tagline (150 chars max)
- `hashnode/bio.md` — Short bio (200 chars max)
- `hashnode/about.md` — Full about page (Markdown)
- `hashnode/tech-stack.md` — Tech stack tags
- `hashnode/social-links.md` — Social link URLs

For a single field, write only the relevant file.

Each file should include a header comment with the character limit (where
applicable) and current character count:

```
<!-- Hashnode Tagline | Limit: 150 chars | Used: 127 chars -->
```

Include character count after each constrained field so the user knows
remaining budget.

### 8. Present to User

How to present depends on scope:

- **Single field**: Display the content inline so the user can review and
  copy-paste immediately.
- **Full export**: Summarize what was generated (list of files, character
  usage for constrained fields, tech stack tag choices). Do not dump all
  5 files into the conversation — the user can read them directly. Show
  specific files inline only if the user asks.

For the tech stack tags, always surface the curation rationale — the user
needs to understand and potentially override tag choices.

## Output Checklist

Before finishing, verify:

- [ ] Tagline was constructed from identity + skills + blog topics (not just trimmed title)
- [ ] Tagline signals what the person builds and writes about
- [ ] Bio complements the tagline with career depth and a differentiator
- [ ] About page was built as a structured document with scannable sections
- [ ] About page opens with a technical hook (not "I am a [title] with X years")
- [ ] About page includes "What I Write About" section (if blog data exists)
- [ ] Tech stack tags are curated (5-10, not a full dump) with rationale noted
- [ ] All fields are within Hashnode's character limits
- [ ] Character counts are noted for constrained fields
- [ ] About page uses proper Markdown formatting
- [ ] Content written to `hashnode/`
- [ ] No profile data fabricated — all sourced from master profile
- [ ] Source qualifiers preserved (projected/estimated/targeted)
- [ ] Output honors all applicable presentation preferences (global + Hashnode-specific)

## Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/skills/hashnode-generate/references/hashnode-constraints.md`** — Character limits, field mapping, formatting rules, and best practices

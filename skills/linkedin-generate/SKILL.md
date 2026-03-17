---
name: linkedin-generate
description: >
  This skill should be used when the user asks to "generate LinkedIn content",
  "export profile for LinkedIn", "create LinkedIn-ready content",
  "format my experience for LinkedIn", "write my LinkedIn headline",
  "generate LinkedIn about section", "prepare LinkedIn update",
  or wants copy-paste-ready content formatted for LinkedIn's field constraints.
---

# LinkedIn Generate

Generate copy-paste-ready content for LinkedIn profile sections, formatted
to LinkedIn's character limits and plain-text constraints.

## When to Use

Invoke this skill to produce LinkedIn-formatted content from the master
profile. This can be a full LinkedIn profile export or a single section
(e.g., just the headline, just one experience entry). For reviewing an
existing LinkedIn profile against the master data, use the `linkedin-review`
skill instead.

## Workflow

### 1. Determine Scope

Ask or infer what the user needs:

- **Full export**: generate all LinkedIn sections
- **Single section**: e.g., "format my experience at Company X for LinkedIn"
- **Specific field**: e.g., "write me a LinkedIn headline"

### 2. Read Profile Sections

Read the relevant profile section JSON files from `sections/`. Consult
`profile-index.json` to discover available sections and their file paths.
Parse each JSON file and access fields directly from the `data` object.
For example: `data.full_name` from `sections/identity.json`,
`data.experience` array from `sections/experience.json`.

If required section JSON files do not exist, inform the user and suggest
running `/profile-init` or `profile-section` to generate them.

**TBD filtering applies during transformation (step 5), not here.**

### 3. Apply Presentation Preferences

Read `preferences.md` from the workspace root. If it exists:

1. Read the `## Global` section — these apply to all exports.
2. Read the `## LinkedIn` section (if present) — these are LinkedIn-specific.
3. Treat each preference as a binding directive during content transformation.
   Examples: "present experience as 20+ years" → use that framing; "don't
   highlight patents" → de-emphasize or omit; tone directives → adjust writing
   style accordingly.
4. LinkedIn-specific preferences take precedence over global if they conflict.

If `preferences.md` does not exist, proceed with default behavior.

### 4. Apply LinkedIn Constraints

Consult `${CLAUDE_PLUGIN_ROOT}/skills/linkedin-generate/references/linkedin-constraints.md` for:

- Character limits per field
- Formatting rules (plain text, no Markdown, bullet character `•`)
- Section mapping (which profile fields map to which LinkedIn fields)
- Best practices for content optimization

### 5. Transform Content

**TBD filtering:** Profile data may contain `TBD` as a placeholder value in
any field (indicating data not yet filled in by the user). When rendering
output, silently skip any value that is exactly `TBD` — do not render it.
If all items in a list are `TBD`, omit that list/block entirely.

For each target LinkedIn field:

- Convert Markdown formatting to plain text (remove `**`, `#`, `-` bullets).
- Replace Markdown bullet points with `•` characters.
- Include character count after each field so the user knows remaining budget.
- **Headline: construct, don't trim**: Do not take the profile's `title` field
  and shorten it to 220 chars. Construct the headline from `title`, `summary`,
  and the most distinctive aspects of the user's experience. Apply the Headline
  Strategy from the linkedin-constraints reference: choose a formula pattern,
  include 3–5 searchable keywords, lead with role or differentiator in the
  first ~60 chars. Aim for 160–210 chars.
- **About: write a narrative, not a summary restatement**: Do not restate
  `summary.json` in prose. Apply the About Strategy from the linkedin-constraints
  reference: hook (first 2–3 lines must stand alone before "see more"), body
  drawing from experience highlights and domain context, optional distinctive
  positioning, and a concrete call to action. Pull achievement highlights from
  `experience.json`, not just `summary.json`. Use the full 2,600-char budget
  — a thin About is a missed opportunity.
- **Experience: flatten, then order, then cap**: For each experience entry:
  1. **Flatten** — LinkedIn has no nested project structure. Incorporate each
     project's `contributions` and `impact` bullets from `projects[]` into the
     job description as flat bullets. Combine contribution + impact into a single
     concise bullet where it reads naturally (e.g., "Designed X, targeting Y%
     improvement"). When attributing specific tools or frameworks to an
     achievement, prefer the project's `skills` field (what the person personally
     applied) over its `tech_stack` (what the whole team used). If `skills` is
     absent, fall back to `tech_stack`.
  2. **Order** — Sort the resulting bullets by impact, most impressive first.
     Do not preserve the source order. `impact` bullets (quantifiable outcomes)
     generally rank higher than `contributions` bullets.
  3. **Cap** — Limit to 3–5 bullets per role. If many projects contributed bullets,
     keep the 3–5 that best represent the user's contribution. More bullets dilute
     rather than reinforce impact.
- **Preserve source qualifiers**: If an impact value is qualified in the source
  (e.g., "projected", "expected", "targeted", "estimated", "almost"), retain
  that qualifier in the output. Do not present projections as delivered results.
- **Match verb to contribution scope**: Use the verb that reflects what the
  person actually did — "designed", "co-developed", "led architecture for" — not
  an inflated verb that implies sole ownership or completed delivery (e.g., avoid
  "secured", "delivered", "built" when the source says "designed" or "helped develop").
- **Skills: curate for impact, not completeness**: Do not flatten all skills
  from the profile into the output unchanged. Instead:
  1. Identify the user's professional identity from their title, summary, and
     most recent/senior experience. Use this to anchor slot 1–5 choices.
  2. Apply the Skills Strategy from the linkedin-constraints reference: order by
     role-defining → core domain → adjacent → soft/leadership. Drop skills that
     are obscure, redundant, or unlikely to be searched by recruiters.
  3. Normalize each skill name to the canonical LinkedIn/industry term
     (e.g., "Machine Learning" not "ML", "Node.js" not "NodeJS").
  4. Deduplicate across profile categories before ordering.
  5. Cap at 50. Prefer a tight, high-signal list over an exhaustive one.
  6. Briefly note the curation rationale (e.g., "Prioritized X, Y, Z as
     role-defining; dropped [obscure tool] as low recruiter search value") so
     the user understands the choices and can override if needed.

### 6. Verify Before Writing

Before writing output, run two checks and revise content if either fails:

**Content fidelity** — For every quantified claim that was qualified in the
source (projected, expected, targeted, estimated, almost), confirm the qualifier
is preserved in the output. For every action verb, confirm it matches the actual
contribution scope in the source — not inflated. Revise any bullet that fails
this check.

**Preferences compliance** — Re-read the applicable preferences and verify each
one is reflected in the generated content. If any preference was missed or
contradicted, revise the content before proceeding.

### 7. Write Output

Write the formatted content to `linkedin/`. Create the directory if
it does not exist.

For a full export, generate these files:

- `linkedin/headline.md` — Headline (220 chars max)
- `linkedin/about.md` — About/Summary section
- `linkedin/experience.md` — All experience entries
- `linkedin/skills.md` — Flattened skills list
- `linkedin/education.md` — Education entries
- `linkedin/certifications.md` — Certifications (if data exists)
- `linkedin/open-source.md` — Open source projects (if data exists)
- `linkedin/patents.md` — Patents (if data exists)
- `linkedin/languages.md` — Languages (if data exists)

For a single section or field, write only the relevant file.

Each file should include a header comment with the character limit and
current character count:

```
<!-- LinkedIn Headline | Limit: 220 chars | Used: 187 chars -->
```

### 8. Present to User

After writing files, display the generated content directly in the
conversation so the user can review and copy-paste immediately without
opening files.

## Output Checklist

Before finishing, verify:

- [ ] No Markdown formatting remains (no `**`, `##`, `- ` bullets)
- [ ] All fields are within LinkedIn's character limits
- [ ] Character counts are noted for each field
- [ ] Content written to `linkedin/`
- [ ] Content displayed in conversation for easy copy-paste
- [ ] Output honors all applicable presentation preferences (global + LinkedIn-specific)
- [ ] Source qualifiers preserved where present (projected/expected/targeted/estimated/almost)
- [ ] Action verbs match actual contribution scope — no inflation beyond what the source data supports
- [ ] Headline was constructed from title + summary + experience (not just trimmed from the title field)
- [ ] About opens with a distinctive hook — not "I am a [title] with X years of experience"
- [ ] Skills list was curated and ordered by impact (not an exhaustive category flatten)

## Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/skills/linkedin-generate/references/linkedin-constraints.md`** — Character limits, formatting rules, section mapping, and best practices

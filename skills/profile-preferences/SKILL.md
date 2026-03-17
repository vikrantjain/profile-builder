---
name: profile-preferences
description: >
  Save, update, remove, or list persistent presentation preferences that
  control how profile data appears in exports and reviews. This skill manages
  the preferences.md file — the central store for user directives about tone,
  voice, emphasis, framing, inclusions, exclusions, and platform-specific
  style rules. MUST be used whenever the user wants to persistently change
  how their profile content is presented: "remember that...", "my preference
  is...", "always/never...", "I want exports to sound...", "don't mention X",
  "emphasize Y", "tone down Z", "I am an introvert so...", "present my
  experience as 20+ years", "use first person for LinkedIn", "forget the
  preference about...", "show my preferences", "remove preference". Trigger
  for any directive about presentation style, personality-driven framing, or
  data display rules — even without the word "preference". Do not trigger for
  generating content, updating profile data, assembling documents, or reviewing
  external profiles.
---

# Profile Preferences

Manage persistent presentation preferences that shape how profile data is
presented in exports (LinkedIn, resume, GitHub, Hashnode) and reviews.
Preferences control tone, emphasis, framing, inclusions, and exclusions.
They do NOT affect the raw profile data layer — only downstream output.

## Presentation vs Operational

This skill handles **presentation preferences** — directives about how profile
content should appear in generated output. Examples:

- "Use a confident but not boastful tone" → presentation (affects export output)
- "Emphasize my cloud architecture experience" → presentation
- "Don't mention my role at CompanyX" → presentation (exclusion)
- "Lead with impact metrics in work experience" → presentation (framing)

These are NOT presentation preferences and should NOT be saved here:

- "Always commit after making changes" → operational instruction for Claude
- "Use vim keybindings" → tool preference
- "Run tests before pushing" → workflow preference

When ambiguous, ask: "Should I save this as a presentation preference that
affects your profile exports, or is this a general instruction for how I
should work?"

## Workflow

### 1. Determine the Operation

Infer from the user's message:

- **Add** — "remember that...", "my preference is...", "always/never...",
  "I want exports to...", "emphasize...", "tone down...", "don't mention..."
- **Update** — "change the preference about...", "actually make it...",
  "update the one about..."
- **Remove** — "forget the preference about...", "remove...", "stop
  applying the rule about..."
- **List** — "what are my preferences?", "show preferences"

### 2. Read Existing Preferences

Read `preferences.md` from the workspace root. If it does not exist:

- For **add**: create it with this initial structure:

  ```markdown
  # Presentation Preferences

  Preferences that shape how profile data is presented in exports and reviews.
  These do NOT affect the raw profile data — only downstream output.

  Edit manually or use the `profile-preferences` skill.

  ## Global
  ```

- For **update/remove/list**: inform the user no preferences file exists yet
  and offer to create one.

### 3. Determine Scope

Infer the platform from context. Only ask if genuinely ambiguous.

- "in LinkedIn", "for LinkedIn", "LinkedIn should..." → `## LinkedIn`
- "in resume", "for resume", "resume should..." → `## Resume`
- "on GitHub", "GitHub README should..." → `## GitHub`
- "on Hashnode", "Hashnode profile should..." → `## Hashnode`
- No platform mentioned → `## Global`

Platform headings map to skills:
- `## Global` → all export and review skills
- `## LinkedIn` → `linkedin-generate`, `linkedin-review`
- `## Resume` → `resume-generate`
- `## GitHub` → `github-generate`, `github-review`
- `## Hashnode` → `hashnode-generate`, `hashnode-review`

### 4. Check for Conflicts

Before adding or updating, scan existing preferences for:

- **Duplicates** — a preference that already says the same thing. If found,
  tell the user it already exists rather than adding a duplicate.
- **Overlaps** — a global preference that covers what the user is adding as
  platform-specific (or vice versa). Flag it: "You already have a global
  preference for formal tone. Want to keep the global one, replace it with
  this LinkedIn-specific one, or have both?"
- **Contradictions** — a preference that directly conflicts (e.g., "use
  casual tone" globally + "use formal tone" for LinkedIn is fine and
  intentional, but "use casual tone" + "use formal tone" in the same
  scope is a conflict). Ask the user which one to keep.

### 5. Execute the Operation

#### Add

1. Locate the target section heading. Create it if missing.
2. Append the preference as a bullet item.
3. Write the directive in clear, imperative language — short and specific.
4. Confirm what was saved and which skills will apply it.

**Good preference format:**
- `- Lead each work experience entry with a quantified impact statement.`
- `- Omit the CompanyX internship from all exports.`
- `- Use first person in narrative sections (About, Summary).`

**Avoid vague preferences:**
- `- Make it sound good.` → too vague to act on
- `- Be professional.` → not specific enough

If the user's phrasing is vague, distill it into something actionable and
confirm: "I'll save this as: '...' — does that capture what you mean?"

#### Update

1. Locate the preference by content match.
2. Replace the text. Move to a different section if scope changed.
3. Confirm the change.

#### Remove

1. Locate the preference by content match.
2. Remove the bullet item.
3. If the section has no remaining items, remove the heading too (except
   `## Global` which always exists).
4. Confirm removal.

#### List

1. Display all preferences grouped by section.
2. For each platform section, note which skills consume it.
3. If no preferences exist, say so.

### 6. Confirm

After any mutation, display the saved preference and its scope. For add/update,
note which export and review skills will apply it.

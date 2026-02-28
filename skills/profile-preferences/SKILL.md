---
name: profile-preferences
description: >
  This skill should be used when the user asks to "remember that",
  "my preference is", "when generating exports", "stop presenting",
  "forget the preference about", "update my preference", "add a
  presentation preference", "remove preference", "show my preferences",
  "list preferences", or wants to add, update, remove, or view
  presentation preferences that affect how profile data is presented
  in exports and reviews.
---

# Profile Preferences

Manage persistent presentation preferences that shape how profile data is
transformed for downstream exports (LinkedIn, resume, GitHub, Hashnode) and
reviews. Preferences do NOT affect the raw profile data layer — only how
data is presented in output documents.

## When to Use

Invoke this skill when the user expresses a presentation directive — tone,
emphasis, framing, inclusions, exclusions — or asks to view, update, or
remove an existing preference.

## Workflow

### 1. Determine the Operation

Infer from the user's message:

- **Add** — user says "remember that...", "my preference is...", "always...",
  "never...", "when generating...", "I prefer..."
- **Update** — user says "change the preference about...", "actually, make
  it...", "update the one about..."
- **Remove** — user says "forget the preference about...", "remove...",
  "stop applying the rule about..."
- **List** — user says "what are my preferences?", "show my preferences"

### 2. Read Existing Preferences

Read `preferences.md` from the workspace root. If it does not exist:

- For **add**: create it with this structure:

  ```markdown
  # Presentation Preferences

  Preferences that shape how profile data is presented in exports and reviews.
  These do NOT affect the raw profile data — only downstream output.

  Edit manually or use the `profile-preferences` skill.

  ## Global
  ```

- For **update/remove/list**: inform the user that no preferences file
  exists yet and offer to create one.

### 3. Determine Scope

Ask or infer what platform(s) the preference applies to:

- "in LinkedIn" or "for LinkedIn" → add under `## LinkedIn`
- "in resume" or "for resume" → add under `## Resume`
- "on GitHub" → add under `## GitHub`
- "on Hashnode" → add under `## Hashnode`
- No platform mentioned → add under `## Global`

Platform headings map to skills:
- `## Global` → all export and review skills
- `## LinkedIn` → `linkedin-generate`, `linkedin-review`
- `## Resume` → `resume-generate`
- `## GitHub` → `github-generate`, `github-review`
- `## Hashnode` → `hashnode-generate`, `hashnode-review`

### 4. Execute the Operation

#### Add

1. Locate the target section heading (`## Global`, `## LinkedIn`, etc.).
   If the heading does not exist, create it.
2. Append the preference as a bullet item under that heading.
3. Write the directive in clear, imperative language.
4. Confirm to the user what was saved and which skills will apply it.

#### Update

1. Locate the preference to update — by content match based on the user's
   description.
2. Replace the directive text. Move to a different section if scope changed.
3. Confirm the change.

#### Remove

1. Locate the preference — by content match.
2. Remove the bullet item.
3. If the section heading has no remaining items, remove the heading too
   (except `## Global` which should always exist).
4. Confirm removal.

#### List

1. Read and display all preferences grouped by section.
2. If no preferences exist, say so.

### 5. Confirm

After any mutation, display the updated preference and its scope.
For add/update, note which export and review skills will apply it.

## Output Checklist

Before finishing, verify:

- [ ] `preferences.md` exists and has valid structure
- [ ] `## Global` heading is present
- [ ] Platform headings use valid names (LinkedIn, Resume, GitHub, Hashnode)
- [ ] No empty sections (heading with no bullet items) except `## Global`
- [ ] User confirmed the saved/updated/removed preference

# LinkedIn Field Constraints

## Character Limits

| Field | Max Characters | Notes |
|-------|---------------|-------|
| Headline | 220 | Appears below name everywhere on LinkedIn |
| About / Summary | 2,600 | Supports line breaks, no Markdown |
| Job Title | 100 | Per experience entry |
| Company Name | 100 | Per experience entry |
| Job Description | 2,000 | Per experience entry, supports bullet points via copy-paste |
| Skills | 50 per skill | Up to 50 skills total, order matters (top 3 shown) |
| Education - Degree | 100 | e.g. "Bachelor of Science" |
| Education - Field of Study | 100 | e.g. "Computer Science" |
| Education - Activities | 500 | Optional |
| Certification Name | 255 | |
| Project Name | 255 | |
| Project Description | 2,000 | |

## Formatting Rules

- LinkedIn does NOT render Markdown. All formatting must be plain text.
- Line breaks are preserved when copy-pasted.
- Bullet points: use `•` (U+2022) or `▸` (U+25B8) characters, not Markdown `-`.
- Bold/italic: not supported in most fields. Use CAPS sparingly for emphasis.
- Links: paste full URLs; LinkedIn auto-links them in About and descriptions.
- Emojis: supported and commonly used in headlines and about sections.

## Section Mapping (Profile → LinkedIn)

| Profile Section | LinkedIn Field | Notes |
|----------------|----------------|-------|
| `sections/identity.md` → full_name | First Name + Last Name | Usually already set |
| `sections/identity.md` → title | Headline | Condense to 220 chars |
| `sections/identity.md` → location | Location | City, Country format |
| `sections/summary.md` → summary | About | Expand for LinkedIn's 2,600 char limit |
| `sections/experience.md` → each entry | Experience | One entry per role |
| `sections/education.md` → each entry | Education | One entry per degree |
| `sections/skills.md` → categories.items | Skills | Flatten all categories into a single list |
| `sections/certifications.md` → each entry | Licenses & Certifications | |
| `sections/open-source.md` → projects | Projects | Map open_source.projects to LinkedIn Projects section |
| `sections/patents.md` → each entry | Patents | LinkedIn has a dedicated patents section |
| `sections/languages.md` → each entry | Languages | |

## Best Practices for LinkedIn Content

- **Headline**: Lead with current role + key differentiator. Include relevant keywords.
- **About**: Write in first person. Open with a hook. Include a call to action at the end.
- **Experience descriptions**: Start each bullet with a strong action verb. Quantify achievements where possible (%, $, numbers).
- **Skills ordering**: Put most relevant/endorsed skills first — only top 3 are visible by default.

# Hashnode Profile Constraints

Field limits and formatting rules for Hashnode profile sections.

## Profile Fields

| Hashnode Field | Character Limit | Markdown | Master Profile Source |
|----------------|----------------|----------|----------------------|
| Name           | 50             | No       | `full_name` from `sections/identity.json` |
| Tagline        | 150            | No       | Derived from `title` or first line of `sections/summary.json` |
| Bio            | 200            | No       | Condensed from `sections/summary.json` |
| About (page)   | No hard limit  | Yes (full Markdown) | Expanded from `sections/summary.json`, `sections/skills.json` |
| Location       | 50             | No       | `location` from `sections/identity.json` |
| Tech Stack     | Tags (multi-select) | No  | Mapped from `sections/skills.json` categories |

## Social Links

Hashnode supports these social link fields in profile settings:

- GitHub URL
- Twitter/X URL
- LinkedIn URL
- Website/Blog URL
- Stack Overflow URL
- Facebook URL
- YouTube URL

All are optional. Extract matching URLs from the `sections/identity.json`
contact and social fields.

## Formatting Rules

### Tagline
- Plain text only, no Markdown or HTML.
- One-liner that describes the user's professional identity.
- Should be punchy and keyword-rich (visible on blog post cards).

### Bio
- Plain text, no Markdown.
- Appears below the name on the profile page.
- Keep concise — this is a preview, not the full story.

### About Page
- Full Markdown supported: headings, bold, italic, lists, links, code blocks, images.
- This is the user's long-form profile page on Hashnode.
- Can include sections like "About Me", "Tech Stack", "Open Source", "Connect".
- No character limit, but keep it scannable (avoid walls of text).

### Tech Stack Tags
- Hashnode uses a tag system for tech stack.
- Each tag is a single technology name (e.g., "JavaScript", "Docker", "AWS").
- Map from the skills categories in the master profile.
- Prefer widely-used tag names that match Hashnode's existing tag taxonomy.

## Best Practices

- **Tagline**: include your primary role and 1-2 key technologies
  (e.g., "Full-Stack Engineer | Go & Kubernetes").
- **Bio**: mention years of experience, current focus, and one differentiator.
- **About page**: use headings to break content into sections. Link to
  your blog posts, GitHub repos, and other profiles.
- **Tech stack**: select 5-10 core technologies. Too many dilutes the signal.
- **Social links**: fill in all that apply — they appear as icons on the profile.

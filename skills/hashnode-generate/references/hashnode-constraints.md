# Hashnode Profile Constraints

Field limits and formatting rules for Hashnode profile sections.

## Profile Fields

| Hashnode Field | Character Limit | Markdown | Master Profile Source |
|----------------|----------------|----------|----------------------|
| Name           | 50             | No       | `full_name` from `sections/identity.json` |
| Tagline        | 150            | No       | Constructed from `title`, `summary`, `skills`, and `blogs` topics |
| Bio            | 200            | No       | Constructed from `summary`, `experience`, and `blogs` context |
| About (page)   | No hard limit  | Yes (full Markdown) | Structured from `summary`, `experience`, `skills`, `open-source`, `blogs` |
| Location       | 50             | No       | `location` from `sections/identity.json` |
| Tech Stack     | Tags (multi-select) | No  | Curated from `sections/skills.json`, weighted by blog relevance |

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
- Appears on every blog post card next to the author name — this is the most
  frequently seen field across the platform.
- Should signal what the person builds and writes about — not their corporate
  title or employer.
- Include the engineering identity plus 1-2 technology or domain signals.
- Aim for 100-140 chars: long enough to be distinctive, short enough for
  mobile rendering.

### Bio
- Plain text, no Markdown.
- Appears below the name on the profile page.
- Should complement (not repeat) the tagline with career depth and a
  differentiator.
- A reader should finish the bio thinking "this person has real experience."

### About Page
- Full Markdown supported: headings, bold, italic, lists, links, code blocks, images.
- This is the user's long-form profile page on Hashnode.
- Structure as a scannable document with clear sections — technical readers
  skim before they commit to reading.
- Recommended sections: opening paragraph, "What I Write About", tech stack,
  featured work/open source, recent posts, connect links.
- Sections without data should be omitted, not left as empty headers.
- No character limit, but keep it scannable (avoid walls of text).

### Tech Stack Tags
- Hashnode uses a tag system for tech stack.
- Each tag is a single technology name (e.g., "JavaScript", "Docker", "AWS").
- Curate to 5-10 core technologies that define the writer's stack.
- Prioritize technologies the user actively writes about or builds with.
- Use canonical tag names that match Hashnode's existing tag taxonomy.
- Skip ubiquitous tools (Git, VS Code) that add no signal.

## Best Practices

- **Tagline**: lead with what you build, not where you work. Include 1-2
  technologies or domains that signal what readers can expect from your posts.
  Good: "Platform engineer | Go, Kubernetes, and distributed systems"
  Weak: "Senior Software Engineer at Acme Corp"
- **Bio**: add career depth (years, domains, scale) and one differentiator
  (open source maintainer, patent holder, specific domain expertise). Mention
  the writing angle if blog data exists.
- **About page**: build as a structured document, not a prose dump. Open with
  a technical hook. Include "What I Write About" to help readers decide to
  follow. Link to open source projects and recent posts.
- **Tech stack**: select technologies that define your perspective as a writer.
  Too many dilutes the signal; too few misses discoverability.
- **Social links**: fill in all that apply — they appear as icons on the profile
  and cross-link the writer's presence.

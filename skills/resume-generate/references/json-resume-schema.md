# JSON Resume Schema — Field Mapping

Generate `resume.json` conforming to the [JSON Resume](https://jsonresume.org/schema)
open standard (v1.0.0). This file can be imported into Reactive Resume, JSON Resume
renderers, or any compatible tool — which handle visual formatting and PDF export.

Schema URL: `https://jsonresume.org/schema`

With JSON section files, all profile fields are accessed directly from the
parsed JSON `data` object — no Markdown parsing required. For example,
`sections/experience.json` → `data.experience[]` gives the experience array
with `title`, `company`, `projects[].contributions`, `projects[].impact`, etc. as structured fields.

## Schema Structure

### basics (object)

| JSON Resume Field       | Profile Source              | Notes                                           |
|------------------------|-----------------------------|-------------------------------------------------|
| `name`                 | `identity.full_name`        | Direct map                                      |
| `label`                | `identity.title`            | Current role or target role title                |
| `email`                | `identity.email`            | Direct map                                      |
| `phone`                | `identity.phone`            | Omit if absent                                  |
| `url`                  | `identity.website`          | Personal website URL                            |
| `summary`              | `summary` section           | 2-3 sentence tailored bio                       |
| `location.city`        | `identity.location`         | Parse city from location string                 |
| `location.region`      | `identity.location`         | Parse state/region if present                   |
| `location.countryCode` | `identity.location`         | ISO-3166-1 ALPHA-2 if determinable              |
| `profiles[]`           | `identity.github`, etc.     | See profiles mapping below                      |

#### Profiles array

Map each social link from identity to a profiles entry:

```json
{
  "network": "GitHub",
  "username": "handle",
  "url": "https://github.com/handle"
}
```

Common networks: GitHub, LinkedIn, Twitter/X. Only include profiles present
in the identity section.

### work (array) — one entry per role

| JSON Resume Field | Profile Source                | Notes                                    |
|-------------------|------------------------------|------------------------------------------|
| `name`            | `experience[].company`       | Employer name                            |
| `position`        | `experience[].title`         | Job title                                |
| `location`        | `experience[].location`      | Omit if absent                           |
| `url`             | (not in profile schema)      | Omit — no company URL field exists       |
| `startDate`       | `experience[].start_date`    | ISO 8601: "YYYY-MM" or "YYYY-MM-DD"     |
| `endDate`         | `experience[].end_date`      | ISO 8601; omit if current role           |
| `summary`         | `experience[].description`   | Brief role overview (1 sentence)         |
| `highlights[]`    | `experience[].description` (parsed bullets) and/or aggregated from `experience[].projects[].contributions` + `experience[].projects[].impact` | Array of achievement strings. Skip any `TBD` values. If all items are `TBD`, omit the array. |

The profile schema has `contributions` and `impact` on nested projects
(`experience[].projects[].contributions` and `experience[].projects[].impact`),
not on experience entries directly. To populate `work[].highlights[]` in JSON Resume:

1. Parse the role's `description` into bullet points.
2. Aggregate non-TBD `contributions` from the role's projects.
3. Aggregate `impact` items from the role's projects — these are high-value
   bullets with quantifiable outcomes and should be prioritized.
4. Select the strongest bullets — start with action verbs, include metrics.
   Where possible, combine a contribution with its impact into a single bullet
   (e.g., "Built X → resulting in Y% improvement").
5. Match the tailored content from `resume.md`.

### education (array) — one entry per degree

| JSON Resume Field | Profile Source               | Notes                                   |
|-------------------|------------------------------|-----------------------------------------|
| `institution`     | `education[].institution`    | School name                             |
| `studyType`       | `education[].degree`         | e.g., "Bachelor", "Master", "PhD"       |
| `area`            | `education[].field`          | Field of study                          |
| `startDate`       | (not in profile schema)      | Omit — profile only has `graduation_year` |
| `endDate`         | `education[].graduation_year`| Convert year to ISO 8601: "YYYY"        |
| `score`           | (not in profile schema)      | Omit                                    |
| `courses[]`       | (not in profile schema)      | Omit                                    |

### skills (array) — one entry per category

| JSON Resume Field | Profile Source               | Notes                                   |
|-------------------|------------------------------|-----------------------------------------|
| `name`            | Skill category name          | e.g., "Languages", "Cloud & DevOps"     |
| `level`           | (inferred)                   | "Master", "Advanced", "Intermediate"    |
| `keywords[]`      | Skills in that category      | Array of individual skill strings       |

Group skills by category as they appear in the profile. When tailoring to a
job description, reorder categories and keywords to front-load JD matches.

### certificates (array) — one entry per certification

| JSON Resume Field | Profile Source                | Notes                                  |
|-------------------|------------------------------|----------------------------------------|
| `name`            | `certifications[].name`      | Certification name                     |
| `issuer`          | `certifications[].issuer`    | Issuing organization                   |
| `date`            | `certifications[].year`      | ISO 8601; convert year to "YYYY"       |
| `url`             | `certifications[].url`       | Verification URL; omit if absent       |

### languages (array) — one entry per language

| JSON Resume Field | Profile Source               | Notes                                   |
|-------------------|------------------------------|-----------------------------------------|
| `language`        | `languages[].language`       | Language name                           |
| `fluency`         | `languages[].proficiency`    | "Native speaker", "Fluent", "Advanced", "Intermediate", "Elementary" |

### projects (array) — for open source and notable experience projects

This array combines two profile sources:

1. **Open source projects** from `open_source.projects[]`
2. **Notable experience projects** from `experience[].projects[]` (when they
   are significant enough to highlight independently)

| JSON Resume Field | Profile Source                | Notes                                  |
|-------------------|------------------------------|----------------------------------------|
| `name`            | `*.name`                     | Project name                           |
| `description`     | `*.description`              | Brief description                      |
| `highlights[]`    | `*.contributions` + `*.impact` | Combine contributions and impact into achievement bullets. Skip any `TBD` values. If all items are `TBD`, omit the array. |
| `keywords[]`      | `*.tech_stack`               | Technologies used                      |
| `url`             | `*.url`                      | Repository or project URL; omit if absent |
| `startDate`       | `experience[].projects[].duration` (parsed) | ISO 8601; omit for open source projects or if unknown |
| `endDate`         | `experience[].projects[].duration` (parsed) | ISO 8601; omit for open source projects or if ongoing |
| `roles[]`         | `*.role`                     | e.g., "tech lead", "owner"; omit if absent |

Only include projects that are relevant to the target role (when a JD is
provided) or that are significant enough for a general resume.

### publications (array) — for patents

The JSON Resume schema has no native `patents` section. Map patents to
`publications`, which is the closest semantic fit (patents are published
intellectual property with identifiers, dates, and issuing bodies).

| JSON Resume Field | Profile Source                | Notes                                  |
|-------------------|------------------------------|----------------------------------------|
| `name`            | `patents[].title`            | Patent title                           |
| `publisher`       | `"United States Patent and Trademark Office"` or appropriate office | Issuing patent office |
| `releaseDate`     | `patents[].grant_date`       | ISO 8601; use grant date if available  |
| `url`             | `patents[].url` or construct from patent number | e.g., `https://patents.google.com/patent/US10585682B2` |
| `summary`         | `patents[].patent_number`    | Include patent number (e.g., "US Patent US10585682B2") |

Only include patents that appear in `resume.md`. If resume.md has a Patents
section, resume.json must have a corresponding `publications` array.

## Sections to Omit

Omit these JSON Resume sections entirely (do not include empty arrays):

- `volunteer` — unless the profile has volunteer data
- `awards` — unless the profile has awards data
- `publications` — unless patents are included in the resume (see patents mapping above)
- `interests` — not typically included in professional resumes
- `references` — "Available upon request" convention; omit from JSON

## Date Format

All dates must be ISO 8601: `"YYYY-MM-DD"` or `"YYYY-MM"` or `"YYYY"`.
Parse from the profile's natural-language dates (e.g., "Jan 2021" → "2021-01").

## Content Consistency

The JSON Resume content must match the tailored content in `resume.md`:
- Same contributions/impact bullets, same summary, same skill ordering
- The two files represent the same resume in different formats
- Do not add content to one that is missing from the other

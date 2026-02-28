# JSON Resume Schema — Field Mapping

Generate `resume.json` conforming to the [JSON Resume](https://jsonresume.org/schema)
open standard (v1.0.0). This file can be imported into Reactive Resume, JSON Resume
renderers, or any compatible tool — which handle visual formatting and PDF export.

Schema URL: `https://jsonresume.org/schema`

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
| `url`             | `experience[].company_url`   | Omit if absent                           |
| `startDate`       | `experience[].start_date`    | ISO 8601: "YYYY-MM" or "YYYY-MM-DD"     |
| `endDate`         | `experience[].end_date`      | ISO 8601; omit if current role           |
| `summary`         | `experience[].description`   | Brief role overview (1 sentence)         |
| `highlights[]`    | `experience[].highlights`    | Array of achievement strings (bullets)   |

Each highlight should start with an action verb, include metrics where
possible, and match the tailored content from `resume.md`.

### education (array) — one entry per degree

| JSON Resume Field | Profile Source               | Notes                                   |
|-------------------|------------------------------|-----------------------------------------|
| `institution`     | `education[].institution`    | School name                             |
| `studyType`       | `education[].degree`         | e.g., "Bachelor", "Master", "PhD"       |
| `area`            | `education[].field`          | Field of study                          |
| `startDate`       | `education[].start_date`     | ISO 8601                                |
| `endDate`         | `education[].end_date`       | ISO 8601                                |
| `score`           | `education[].gpa`            | Omit if absent or not relevant          |
| `courses[]`       | `education[].courses`        | Omit if absent                          |

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
| `date`            | `certifications[].date`      | ISO 8601                               |
| `url`             | `certifications[].url`       | Verification URL; omit if absent       |

### languages (array) — one entry per language

| JSON Resume Field | Profile Source               | Notes                                   |
|-------------------|------------------------------|-----------------------------------------|
| `language`        | `languages[].language`       | Language name                           |
| `fluency`         | `languages[].proficiency`    | "Native speaker", "Fluent", "Advanced", "Intermediate", "Elementary" |

### projects (array) — for open source / notable projects

| JSON Resume Field | Profile Source                | Notes                                  |
|-------------------|------------------------------|----------------------------------------|
| `name`            | `open_source[].name`         | Project name                           |
| `description`     | `open_source[].description`  | Brief description                      |
| `highlights[]`    | `open_source[].highlights`   | Key achievements or contributions      |
| `url`             | `open_source[].url`          | Repository or project URL              |
| `startDate`       | `open_source[].start_date`   | ISO 8601; omit if unknown              |
| `endDate`         | `open_source[].end_date`     | ISO 8601; omit if ongoing              |

Only include projects that are relevant to the target role (when a JD is
provided) or that are significant enough for a general resume.

## Sections to Omit

Omit these JSON Resume sections entirely (do not include empty arrays):

- `volunteer` — unless the profile has volunteer data
- `awards` — unless the profile has awards data
- `publications` — unless the profile has publications data
- `interests` — not typically included in professional resumes
- `references` — "Available upon request" convention; omit from JSON

## Date Format

All dates must be ISO 8601: `"YYYY-MM-DD"` or `"YYYY-MM"` or `"YYYY"`.
Parse from the profile's natural-language dates (e.g., "Jan 2021" → "2021-01").

## Content Consistency

The JSON Resume content must match the tailored content in `resume.md`:
- Same highlights/bullets, same summary, same skill ordering
- The two files represent the same resume in different formats
- Do not add content to one that is missing from the other

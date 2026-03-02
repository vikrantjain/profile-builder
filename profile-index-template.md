---
template_version: "2.0"
template_name: "Profile Index Schema"

description: >
  Schema for profile-index.json — the manifest and configuration hub for the
  profile system. This file is pure JSON (no Markdown rendering template).
  Skills read and write it programmatically.

output: "profile-index.json"

json_structure:
  profile_version:
    required: true
    type: string
    description: "Schema version, currently '2.0'"

  identity:
    required: true
    type: object
    description: "Lightweight identity snapshot for quick access. Kept in sync with sections/identity.json by profile-init and profile-section. Intentionally excludes display-only fields (avatar_url, years_of_experience) that live in the full identity section."
    fields:
      full_name:
        required: true
        description: "Full name or preferred display name"
      title:
        required: true
        description: "Current or most recent job title"
      email:
        required: true
        description: "Primary contact email address"
      phone:
        required: false
        description: "Contact phone number including country code"
      location:
        required: false
        description: "City and country, or 'Remote'"
      github:
        required: false
        description: "Full GitHub profile URL"
      linkedin:
        required: false
        description: "Full LinkedIn profile URL"
      website:
        required: false
        description: "Personal website or portfolio URL"
      twitter:
        required: false
        description: "Twitter/X profile URL"

  sections:
    required: true
    type: list
    description: "Manifest of generated profile sections. Updated by profile-section and profile-refresh after writing section files."
    item_fields:
      name:         { required: true, description: "Section display name, e.g. Experience, Skills" }
      key:          { required: true, description: "Section key matching profile-template.md sections block, e.g. experience, skills" }
      file:         { required: true, description: "Relative path to the section JSON file, e.g. sections/experience.json" }
      last_updated: { required: true, description: "Date the section was last generated or updated (YYYY-MM-DD)" }

  sources:
    required: false
    type: list
    description: "External platforms that feed dynamic profile sections (blogs, open_source). Used by profile-refresh to fetch latest data."
    item_fields:
      platform: { required: true, description: "Platform type: github, hashnode, devto" }
      handle:   { required: true, description: "Username or handle on the platform" }
      feeds:    { required: true, description: "Profile sections this source feeds, e.g. ['open_source', 'blogs']", type: list }

example: |
  {
    "profile_version": "2.0",
    "identity": {
      "full_name": "Jane Doe",
      "title": "Senior Software Engineer",
      "email": "jane@example.com",
      "location": "San Francisco, US",
      "github": "https://github.com/janedoe",
      "linkedin": "https://linkedin.com/in/janedoe",
      "twitter": "https://x.com/janedoe"
    },
    "sections": [
      { "name": "Identity", "key": "identity", "file": "sections/identity.json", "last_updated": "2026-02-25" },
      { "name": "Experience", "key": "experience", "file": "sections/experience.json", "last_updated": "2026-02-25" },
      { "name": "Skills", "key": "skills", "file": "sections/skills.json", "last_updated": "2026-02-25" }
    ],
    "sources": [
      { "platform": "github", "handle": "janedoe", "feeds": ["open_source"] },
      { "platform": "hashnode", "handle": "janedoe", "feeds": ["blogs"] }
    ]
  }
---

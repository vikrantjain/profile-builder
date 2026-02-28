---
template_version: "1.0"
template_name: "Profile Index Template"

placeholder_syntax:
  "{{field}}":                  "Insert the value of field here"
  "{{#field}}...{{/field}}":    "Render the block only if field has a value; omit entirely otherwise"
  "{{^field}}...{{/field}}":    "Render the block only if field is absent or null"
  "{{#each list}}...{{/each}}": "Repeat the block for every item in the list"

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
  available_sections:
    required: true
    type: list
    description: "List of profile sections that have been generated"
    item_fields:
      name:         { required: true, description: "Section display name, e.g. Experience, Skills" }
      file:         { required: true, description: "Relative path to the section file, e.g. sections/experience.md" }
      last_updated: { required: true, description: "Date the section was last generated or updated, e.g. 2026-02-25" }

  sources:
    required: false
    type: list
    description: "External platforms that feed dynamic profile sections (blogs, open_source). Used by profile-refresh to fetch latest data."
    item_fields:
      platform:  { required: true, description: "Platform type: github, hashnode, devto" }
      handle:    { required: true, description: "Username or handle on the platform" }
      feeds:     { required: true, description: "Profile sections this source feeds, e.g. open_source, blogs", type: list }
---

# {{full_name}}

**{{title}}**{{#location}} · {{location}}{{/location}}

{{email}}{{#phone}} · {{phone}}{{/phone}}{{#github}} · [GitHub]({{github}}){{/github}}{{#linkedin}} · [LinkedIn]({{linkedin}}){{/linkedin}}{{#website}} · [Website]({{website}}){{/website}}{{#twitter}} · [Twitter]({{twitter}}){{/twitter}}

---

## Profile Sections

| Section | File | Last Updated |
|---------|------|--------------|
{{#each available_sections}}
| {{name}} | `{{file}}` | {{last_updated}} |
{{/each}}

{{#sources}}
---

## Data Sources

| Platform | Handle | Feeds Sections |
|----------|--------|----------------|
{{#each sources}}
| {{platform}} | {{handle}} | {{feeds | join ", "}} |
{{/each}}
{{/sources}}

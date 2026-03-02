---
template_version: "2.0"
template_name: "User Profile Template"

placeholder_syntax:
  "{{field}}":                  "Insert the value of field here"
  "{{#field}}...{{/field}}":    "Render the block only if field has a value; omit entirely otherwise"
  "{{^field}}...{{/field}}":    "Render the block only if field is absent or null"
  "{{#each list}}...{{/each}}": "Repeat the block for every item in the list"
  "{{.}}":                      "Current item value inside an #each loop"
  "{{field | default 'x'}}":    "Use field value if present, otherwise use the fallback x"
  "{{list | join ', '}}":       "Render a list as a single comma-separated string"
  "{{field | capitalize}}":     "Render field value with first letter uppercased"

fields:
  # ── Identity ────────────────────────────────────────────
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

  avatar_url:
    required: false
    description: "URL to profile photo or avatar. Retained as a data field for non-Markdown consumers (e.g. LinkedIn, GitHub profile generators); not rendered in this Markdown layout."

  # ── Online Presence ─────────────────────────────────────
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

  # ── Professional ────────────────────────────────────────
  summary:
    required: true
    description: "2-4 sentence professional bio"
    hint: "Infer from experience, skills, and education if not explicitly provided"

  years_of_experience:
    required: false
    description: "Total years of professional experience"
    hint: "Calculate from experience entries if not provided"

  # ── Skills ──────────────────────────────────────────────
  skills:
    required: true
    description: "Skills grouped into agent-determined categories"
    categories:
      required: true
      type: list
      description: "Agent determines category names based on the user's skill set (e.g. Languages, Platforms, Databases, Tools, Methodologies)"
      item_fields:
        name:  { required: true, description: "Category label chosen by the agent" }
        items: { required: true, description: "List of skills in this category", type: list }
    soft:
      required: false
      type: list
      description: "Soft skills — leadership, communication, collaboration, etc."

  # ── Experience ──────────────────────────────────────────
  experience:
    required: true
    type: list
    description: "Work experience entries, most recent first"
    item_fields:
      title:         { required: true,  description: "Job title" }
      company:       { required: true,  description: "Company or organization name" }
      location:      { required: false, description: "Office location or Remote" }
      type:          { required: false, description: "Employment type: Full-time / Part-time / Contract / Freelance" }
      start_date:    { required: true,  description: "Start month and year, e.g. Jan 2021" }
      end_date:      { required: false, description: "End month and year. Omit if current role" }
      description:   { required: true,  description: "Key responsibilities and achievements. Use bullet points." }
      tech_stack:    { required: false, description: "Broad technologies, platforms, or infrastructure used across this role (e.g. AWS, Kubernetes, CI/CD). Project-specific stacks go in each project entry.", type: list }
      projects:
        required: false
        type: list
        description: "Notable projects undertaken in this role"
        item_fields:
          name:        { required: true,  description: "Project name" }
          description: { required: true,  description: "What the project does or achieved" }
          role:        { required: false, description: "Your role in the project, e.g. tech lead, sole developer" }
          duration:    { required: false, description: "Project timeframe, e.g. 'Dec 2025 – Jan 2026' or '3 months'. Parsed from date ranges in the input." }
          tech_stack:  { required: false, description: "Project-specific technologies (e.g. React, GraphQL, PostgreSQL)", type: list }
          contributions: { required: true, description: "What you did — technical work, design decisions, problems solved. Action-oriented bullets describing the work performed. Use 'TBD' as a single-item list if no contributions can be extracted.", type: list, default: ["TBD"] }
          impact:      { required: false, description: "Quantifiable outcomes — metrics, business results, performance gains, adoption numbers. Numbers-driven bullets. IMPORTANT: Always actively search the source data for measurable outcomes, percentages, scale numbers, time savings, cost reductions, adoption figures, and before/after comparisons. Only omit if genuinely no quantifiable data exists after thorough extraction.", type: list }
          url:         { required: false, description: "Link to project, repo, or demo (if public)" }

  # ── Education ───────────────────────────────────────────
  education:
    required: false
    type: list
    description: "Education entries, most recent first"
    item_fields:
      degree:           { required: true,  description: "Degree type, e.g. B.Sc., M.Sc., Ph.D." }
      field:            { required: true,  description: "Field of study or major" }
      institution:      { required: true,  description: "University or institution name" }
      graduation_year:  { required: false, description: "Year of graduation or expected graduation" }

  # ── Certifications ──────────────────────────────────────
  certifications:
    required: false
    type: list
    description: "Professional certifications"
    item_fields:
      name:    { required: true,  description: "Certification name" }
      issuer:  { required: true,  description: "Issuing organization" }
      year:    { required: false, description: "Year obtained" }
      expiry:  { required: false, description: "Expiry year, or 'No expiry' if lifetime credential" }
      url:     { required: false, description: "Credential verification URL" }

  # ── Patents ─────────────────────────────────────────────
  patents:
    required: false
    type: list
    description: "Granted or pending patents, most recent first"
    item_fields:
      title:          { required: true,  description: "Title of the invention" }
      patent_number:  { required: false, description: "Official patent number e.g. US11234567B2" }
      status:         { required: true,  description: "granted / pending / expired" }
      filed:          { required: false, description: "Year the patent was filed" }
      granted:        { required: false, description: "Year the patent was granted. Omit if pending." }
      inventors:      { required: false, description: "List of inventors", type: list }
      jurisdiction:   { required: false, description: "e.g. US, EU, WO (international)" }
      url:            { required: false, description: "Link to patent record e.g. Google Patents URL" }
      abstract:       { required: false, description: "One sentence describing the invention" }

  # ── Blogs ───────────────────────────────────────────────
  blogs:
    required: false
    type: list
    description: "Published blog posts or articles, most recent first"
    item_fields:
      title:        { required: true,  description: "Title of the blog post or article" }
      url:          { required: true,  description: "Link to the published post" }
      platform:     { required: false, description: "Publishing platform, e.g. Medium, Dev.to, personal blog" }
      published_on: { required: false, description: "Publication date, e.g. Mar 2024" }
      excerpt:      { required: false, description: "One sentence describing what the post is about" }

  # ── Open Source ─────────────────────────────────────────
  open_source:
    required: false
    description: "Open source work — owned/maintained projects and contributions to other projects"
    projects:
      required: false
      type: list
      description: "Open source projects you own, maintain, or significantly contribute to, most notable first"
      item_fields:
        name:        { required: true,  description: "Project or repository name" }
        description: { required: true,  description: "What the project does" }
        url:         { required: true,  description: "Link to the repository or project page" }
        role:        { required: true,  description: "owner / maintainer / contributor" }
        status:      { required: false, description: "Project status: active / completed / archived" }
        tech_stack:  { required: false, description: "Primary languages or technologies used", type: list }
        contributions: { required: false, description: "What you did — key technical work, features built, problems solved", type: list }
        impact:      { required: false, description: "Quantifiable outcomes — star count, downloads, adoption numbers, performance gains", type: list }
    # Note: 'contributions' below is a list of contribution records (objects with project/url/type/description).
    # This is unrelated to the 'contributions' field inside projects[].item_fields, which is a flat list of strings.
    contributions:
      required: false
      type: list
      description: "Contributions to other projects — PRs, reviews, issues, docs"
      item_fields:
        project:     { required: true,  description: "Name of the project contributed to" }
        url:         { required: false, description: "Link to the PR, issue, or commit" }
        type:        { required: true,  description: "PR / Issue / Review / Documentation / Maintainer" }
        description: { required: true,  description: "What you did and why it mattered" }

  # ── Languages ───────────────────────────────────────────
  languages:
    required: false
    type: list
    description: "Spoken or written languages"
    item_fields:
      language:    { required: true,  description: "Language name" }
      proficiency: { required: false, description: "e.g. Native, Fluent, Intermediate, Basic" }

# ════════════════════════════════════════════════════════════
# Modular Section Support
# ════════════════════════════════════════════════════════════
#
# The profile can be generated as a single document (mode: full) or as
# independent section files (mode: section) for targeted updates,
# parallel generation, and smaller-context agents.

json_structure:
  description: "Each section file is a JSON object with two top-level keys"
  envelope:
    section: "The section key name (e.g. 'experience', 'skills')"
    data: "An object whose keys are the field names defined in the fields block"
  rules:
    required_fields_no_data: "Use 'TBD' (string) or ['TBD'] (list). Do not use null for required fields."
    optional_fields_no_data: "Use null or omit the key entirely. Do not set optional fields to TBD."
    no_markdown_in_values: "Values are raw data — no **, ##, or - bullet formatting."
    dates: "Write as user provided (e.g. 'Jan 2021'). No ISO 8601 conversion at the data layer."
    tbd_rendering: "Generate and assemble skills silently skip values that are exactly 'TBD' or ['TBD'] during rendering. profile-validate warns about TBD values."

sections:
  identity:
    output: "sections/identity.json"
    fields: [full_name, title, email, phone, location, avatar_url, github, linkedin, website, twitter, years_of_experience]
    description: "Name, title, contact info, online presence links, and years of experience"
  summary:
    output: "sections/summary.json"
    fields: [summary]
    description: "Professional bio"
  experience:
    output: "sections/experience.json"
    fields: [experience]
    description: "Work history entries with responsibilities, tech stacks, and notable projects"
  skills:
    output: "sections/skills.json"
    fields: [skills]
    description: "Technical and soft skills grouped by category"
  education:
    output: "sections/education.json"
    fields: [education]
    description: "Degrees and academic background"
  certifications:
    output: "sections/certifications.json"
    fields: [certifications]
    description: "Professional certifications and credentials"
  patents:
    output: "sections/patents.json"
    fields: [patents]
    description: "Granted and pending patents"
  blogs:
    output: "sections/blogs.json"
    fields: [blogs]
    description: "Published blog posts and articles"
  open_source:
    output: "sections/open-source.json"
    fields: [open_source]
    description: "Open source projects and contributions"
  languages:
    output: "sections/languages.json"
    fields: [languages]
    description: "Spoken and written languages"
---

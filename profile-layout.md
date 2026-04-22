# {{full_name}}

**{{title}}**{{#location}} · {{location}}{{/location}}{{#years_of_experience}} · {{years_of_experience}} yrs experience{{/years_of_experience}}

{{email}}{{#phone}} · {{phone}}{{/phone}}{{#github}} · [GitHub]({{github}}){{/github}}{{#linkedin}} · [LinkedIn]({{linkedin}}){{/linkedin}}{{#website}} · [Website]({{website}}){{/website}}{{#twitter}} · [Twitter]({{twitter}}){{/twitter}}

---

## Summary

{{summary}}

---

## Experience

{{#each experience}}
### {{title}} — {{company}}{{#location}} · {{location}}{{/location}}
*{{start_date}} – {{end_date | default "Present"}}*{{#type}} · {{type}}{{/type}}

{{description}}

{{#projects}}
#### Projects

{{#each projects}}
**{{#url}}[{{name}}]({{url}}){{/url}}{{^url}}{{name}}{{/url}}**{{#role}} · *{{role}}*{{/role}}{{#duration}} · {{duration}}{{/duration}}

{{description}}

{{#tech_stack}}**Stack:** {{tech_stack | join ", "}}{{/tech_stack}}

{{#skills}}**Skills applied:** {{skills | join ", "}}{{/skills}}

{{#contributions}}
{{#each contributions}}
- {{.}}
{{/each}}
{{/contributions}}

{{#impact}}
**Impact:**
{{#each impact}}
- {{.}}
{{/each}}
{{/impact}}

{{/each}}
{{/projects}}

{{/each}}

---

## Skills

{{#each skills.categories}}
**{{name}}:** {{items | join ", "}}

{{/each}}
{{#skills.soft}}
**Soft Skills:** {{skills.soft | join ", "}}
{{/skills.soft}}

---

{{#education}}
## Education

{{#each education}}
### {{degree}} in {{field}}
{{institution}}{{#graduation_year}} · {{graduation_year}}{{/graduation_year}}

{{/each}}

---

{{/education}}

{{#certifications}}
## Certifications

{{#each certifications}}
- **{{#url}}[{{name}}]({{url}}){{/url}}{{^url}}{{name}}{{/url}}** — {{issuer}}{{#year}} · {{year}}{{/year}}{{#expiry}} – {{expiry}}{{/expiry}}{{#id}} · ID: {{id}}{{/id}}
{{/each}}

---

{{/certifications}}

{{#patents}}
## Patents

{{#each patents}}
### {{#url}}[{{title}}]({{url}}){{/url}}{{^url}}{{title}}{{/url}}
*{{status | capitalize}}*{{#patent_number}} · {{patent_number}}{{/patent_number}}{{#jurisdiction}} · {{jurisdiction}}{{/jurisdiction}}

{{#abstract}}{{abstract}}{{/abstract}}

{{#filed}}Filed: {{filed}}{{#granted}} · Granted: {{granted}}{{/granted}}{{/filed}}{{^filed}}{{#granted}}Granted: {{granted}}{{/granted}}{{/filed}}

{{#inventors}}**Inventors:** {{inventors | join ", "}}{{/inventors}}

{{/each}}

---

{{/patents}}

{{#blogs}}
## Blog Posts

{{#each blogs}}
### [{{title}}]({{url}})
{{#platform}}*{{platform}}*{{/platform}}{{#published_on}} · {{published_on}}{{/published_on}}

{{#excerpt}}{{excerpt}}{{/excerpt}}

{{/each}}

---

{{/blogs}}

{{#open_source}}
## Open Source

{{#open_source.projects}}
### Projects

{{#each open_source.projects}}
#### {{#url}}[{{name}}]({{url}}){{/url}}{{^url}}{{name}}{{/url}} · *{{role}}*{{#status}} · `{{status}}`{{/status}}

{{description}}

{{#tech_stack}}**Stack:** {{tech_stack | join ", "}}{{/tech_stack}}

{{#contributions}}
{{#each contributions}}
- {{.}}
{{/each}}
{{/contributions}}

{{#impact}}
**Impact:**
{{#each impact}}
- {{.}}
{{/each}}
{{/impact}}

{{/each}}
{{/open_source.projects}}

{{#open_source.contributions}}
### Contributions

{{#each open_source.contributions}}
- **{{#url}}[{{project}}]({{url}}){{/url}}{{^url}}{{project}}{{/url}}** *({{type}})* — {{description}}
{{/each}}
{{/open_source.contributions}}

---

{{/open_source}}

{{#languages}}
## Languages

{{#each languages}}
- **{{language}}**{{#proficiency}} — {{proficiency}}{{/proficiency}}
{{/each}}

{{/languages}}

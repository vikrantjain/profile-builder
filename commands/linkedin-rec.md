---
name: linkedin-rec
description: "Generate a personalized LinkedIn recommendation request message for a former colleague"
argument-hint: "[Name], [Company], [optional: project or area of collaboration]"
---

# LinkedIn Recommendation Request

Generate a LinkedIn recommendation request message to send to a former colleague.

## Input
The user will provide: $ARGUMENTS
Format expected: [Colleague Name], [Company], [optional: specific project or area of collaboration]

## Instructions

1. Read `profile-index.json` to confirm the profile exists and to discover the section file paths. If it — or the required sections below — cannot be found, tell the user to run `/profile-init` first, then stop. Otherwise read:
   - `sections/experience.json` — for role details, projects, contributions, and impact at the specified company
   - `sections/identity.json` — for the user's name
   - `sections/summary.json` — for overall profile context
   - `preferences.md` (if it exists) — for tone and framing directives

2. From the experience data, identify the role and projects at the specified company. If a specific project is mentioned, focus on that. Otherwise, select the 2-3 most impactful projects.

3. Generate a recommendation request message that:
   - Is warm but not overly formal — suited for a colleague relationship
   - Keeps an understated, straightforward tone (avoid superlatives and self-promotion)
   - Briefly mentions specific projects/contributions the colleague likely had visibility into
   - Asks them to focus on whatever aspects felt most relevant from their perspective
   - Offers to reciprocate
   - Is concise — no more than 150 words in the message body

4. After the message, include 2-3 short tips for personalising it further.

## Output
Provide the message in a copy-ready format.

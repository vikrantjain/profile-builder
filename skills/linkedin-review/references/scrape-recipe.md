# LinkedIn Scrape Recipe (Playwright MCP)

The full procedure for capturing a LinkedIn profile with the Playwright MCP
browser tools. Output: one file per profile section in
`.profile/tmp/{YYYY-MM-DD}/linkedin/` (today's date; create the directory if
it does not exist). The analysis phase reads only these files.

## 1. Navigate and Handle Auth

Read `sections/identity.json` to get the user's LinkedIn URL (or use the
URL the user provides). Navigate to the profile page.

**Auth wall handling:** LinkedIn may show a login page or auth wall instead
of the profile. After navigating, take a snapshot and check for login
indicators (login form, "Sign in" button, "Join now", or a redirect to
`/login`). If detected:

1. Navigate to `https://www.linkedin.com/login` — the browser may have an
   existing session that auto-redirects to the feed. Take a snapshot to
   check.
2. If still on the login page (no active session), **ask the user to log
   in**. Tell them: "LinkedIn requires authentication. Please log in to
   your LinkedIn account in the browser window that just opened. Let me
   know when you're done." Use `AskUserQuestion` and wait for
   confirmation.
3. After the user confirms, take a snapshot to verify the login succeeded
   (look for feed content, profile elements, or navigation bar with the
   user's avatar). If still not logged in, ask once more with specific
   guidance: "It looks like the login didn't complete. Please make sure
   you've finished any 2FA or verification steps and the page shows your
   LinkedIn feed."
4. Once logged in, navigate back to the target profile URL.
5. Only fall back to the manual paste path if the user explicitly says they
   cannot or do not want to log in via the browser.

## 2. Full-Page Snapshot

After the profile loads, scroll to the bottom of the page (press `End` key
2–3 times) to trigger lazy-loading of all sections. Then save a full
snapshot to file:

```
browser_snapshot → save to .profile/tmp/{YYYY-MM-DD}/linkedin/full-snapshot.md
```

**Important:** LinkedIn profile snapshots are typically 100K–300K characters,
which exceeds inline token limits. Always save to file using the `filename`
parameter rather than reading inline. Then use Grep to find section
headings and Read with line offsets to extract specific sections.

From the snapshot, identify which sections exist by searching for
`heading "SectionName"` patterns. Note which sections are present and
which are absent — absent sections feed directly into the Missing Sections
part of the review.

## 3. Expand and Capture Each Section In Depth

The visible profile page only shows a preview of each section — truncated
descriptions, collapsed lists, and "Show all" links that hide the
majority of the content. A surface-level snapshot misses most of the
data. You must navigate into every section's detail page and expand
every collapsed element to get the full picture.

**General approach for each section below:**

1. On the main profile, find the section and click "Show all N …" (or
   similar) to navigate to its detail page (e.g., `/details/experience/`).
2. On the detail page, scroll to the bottom to load all entries.
3. Expand every "…more" / "see more" button on that page — each entry
   may have its own collapsed description.
4. Take a snapshot (save to file) and extract the full content.
5. Use `browser_navigate_back` to return to the main profile before
   moving to the next section.

If a section has no "Show all" link (all content is visible inline),
expand any "…more" buttons in place and capture from the main profile
snapshot.

Work through sections in this order:

1. **About** — On the main profile, click the "…more" link in the About
   section to reveal the full text. Capture the complete expanded text
   (needed for character count and narrative review).

2. **Experience** — Click "Show all N experiences" to navigate to the
   experience detail page. On that page:
   - Scroll to the bottom to load all roles (LinkedIn lazy-loads older
     entries).
   - Expand **every** role's "…more" description — not just recent roles.
     Older roles matter for career narrative review.
   - For roles with nested positions (company groups), expand each
     nested position's description too.
   - Take a snapshot and save the full content.
   - Navigate back to the main profile.

3. **Education** — Click "Show all N education" if present. Expand any
   "…more" descriptions (activities, honors, etc.). Capture and navigate
   back.

4. **Licenses & Certifications** — Click "Show all N licenses &
   certifications" if present. Capture all entries (name, issuer, date,
   credential ID). Navigate back.

5. **Skills** — Click "Show all N skills" to navigate to the skills
   detail page. This page groups skills by category and shows endorsement
   counts. Scroll to load all skill groups. Capture the complete list.
   Navigate back.

6. **Recommendations** — Click into the Recommendations section. Note
   the "Received" and "Given" tab counts. On the "Received" tab, expand
   every truncated recommendation ("…more"). Capture all recommendation
   text with author names and their relationship to the user. Navigate
   back.

7. **Patents** — Click "Show all N patents" if present. Capture each
   patent's title, number, date, and description. Verify the count
   against the master profile. Navigate back.

8. **Projects** — Click "Show all N projects" if present. Expand
   descriptions. Capture project names, descriptions, and collaborators.
   Navigate back.

9. **Volunteer Experience** — Click "Show all" if present. Expand
   descriptions. Capture roles, organizations, and descriptions.
   Navigate back.

10. **Honors & Awards** — Click "Show all" if present. Capture all
    entries. Navigate back.

11. **Publications** — Click "Show all" if present. Capture titles,
    publishers, dates, co-authors. Navigate back.

12. **Languages** — Capture language names and proficiency levels.

13. **Activity / Posts** — Note follower count and recent post topics
    from the main profile (no detail page needed).

14. **Any other sections** — If the profile has sections not listed above,
    apply the same expand-and-capture pattern.

**Do not skip sections.** If a "Show all" link exists, you must click it.
If an entry has a "…more" link, you must expand it. Partial data leads
to an incomplete review — the user is relying on you to see everything
on their profile.

## 4. Save Section Files

Extract content from the snapshot (and any expanded sections) into
individual files. For each section present on the profile:

| # | Section | Save to | What to capture |
|---|---------|---------|-----------------|
| 1 | Header | `header.md` | Name, headline (full text + char count), location, connection count |
| 2 | About | `about.md` | Full expanded text (post "…more" click) |
| 3 | Experience | `experience.md` | Each role: title, company, dates, location, **full expanded description** text, skills tags. Must include all roles from the detail page, not just what was visible on the main profile. |
| 4 | Education | `education.md` | Each entry: degree, field, school, dates, activities/honors |
| 5 | Skills | `skills.md` | **All** skills from the detail page with endorsement counts, grouped by category |
| 6 | Certifications | `certifications.md` | Each entry: name, issuer, date, credential ID |
| 7 | Recommendations | `recommendations.md` | Count received/given, **full expanded text** of each recommendation with author name and relationship |
| 8 | Patents | `patents.md` | Each: title, number, date, description; note total count |
| 9 | Projects | `projects.md` | Each: name, description, collaborators |
| 10 | Volunteer | `volunteer.md` | Each: role, organization, dates, description |
| 11 | Honors & Awards | `honors.md` | Each: title, issuer, date, description |
| 12 | Publications | `publications.md` | Each: title, publisher, date, co-authors |
| 13 | Languages | `languages.md` | Each: language + proficiency level |
| 14 | Activity | `activity.md` | Follower count, recent post summary |
| 15 | Missing sections | `missing-sections.md` | List of absent sections |

Skip sections not present. Save as plain structured text — no HTML.

## 5. Close Browser

Close the browser after all sections are scraped. Everything from here
works from local files only.

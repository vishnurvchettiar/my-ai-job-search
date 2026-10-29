# Skill: /apply

When the user provides a job posting URL or text, execute this workflow:

## Step 1: Fetch & Integrity Check
- If URL given: fetch the posting content
- Check for red flags: salary not listed, no company name, vague responsibilities
- Report any integrity issues before proceeding

## Step 2: Evaluate Fit
Score each dimension 1-5 and give an overall recommendation:

| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Technical Skills Match | | |
| Experience Level Match | | |
| Domain / Industry Fit | | |
| Location / Remote Fit | | |
| Language Requirements | | |
| **OVERALL** | | |

- Score ≥ 3.5 → Recommend applying
- Score < 2.5 → Recommend skipping (explain why)
- Score 2.5-3.5 → User's call (highlight pros/cons)

## Step 3: Draft CV (if applying)
- Open `cv/cv_template.md`
- Reorder and emphasize skills/experience that match the JD
- Mirror keywords from the JD (for ATS)
- Save as `cv/cv_<CompanyName>_<RoleName>.md`

## Step 4: Draft Cover Letter
- Use `templates/cover_letter_template.md`
- First paragraph: Why THIS company (be specific, use company_research if available)
- Second paragraph: What you bring (tied to JD requirements)
- Third paragraph: Why you're a fit (concrete example from experience)
- Save as `cover_letters/cover_<CompanyName>_<RoleName>.md`

## Step 5: Review & Revise
- Review both documents against the JD one more time
- Check: no fabricated experience, no generic phrases, ATS keywords present
- Present final output to user

## Step 6: Record
- Add to `documents/job_tracker.csv`
- Create `company_research/<CompanyName>.md` if it doesn't exist

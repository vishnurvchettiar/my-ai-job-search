# Skill: /scrape

Search job portals for positions matching Vishnu Chettiar's profile.

## Profile Summary (for search)
- **Roles:** SDET, QA Automation Engineer, .NET Developer, Java Developer, Associate SDET
- **Skills:** C#, .NET, Blazor, Java, Selenium, Playwright, NUnit
- **Location:** India (open to remote)
- **Experience Level:** Junior to Mid-level

## Step 1: Run the Scraper
```bash
python job_scraper/job_scraper.py --query "SDET OR QA Automation" --location "India" --remote
```

## Step 2: Present Results
For each match found, present:
- Company name
- Role title
- Location / Remote status
- Brief fit assessment (1 line)
- URL

## Step 3: Rank by Fit
Sort by estimated fit score (highest first) based on profile match.

## Step 4: Prompt for Next Action
Ask: "Which one would you like to apply to? (Enter number or URL)"
Then hand off to `/apply`.

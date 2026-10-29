# Skill: /auto-apply

Full automated pipeline: Scrape → Rank → Evaluate → Tailor CV → Write Cover Letter → Write Cold Email → Record.

Run this when you want to process a batch of jobs in one shot.

## Pipeline

```
/auto-apply [optional: query] [optional: --limit N]
     │
     ▼
1. SCRAPE  ─────────────────────────────────────────
   Run job_scraper.py for SDET / QA / .NET roles
   Collect all matching listings (LinkedIn, Naukri, Indeed)
     │
     ▼
2. RANK  ────────────────────────────────────────────
   For each posting, score these 5 dimensions (1-5):
   • Technical Skills Match
   • Experience Level Match
   • Location / Remote Fit
   • Company Quality Signal
   • Salary Range Fit
   Discard anything scoring < 2.5 overall
   Sort remaining by score (highest first)
     │
     ▼
3. FOR EACH JOB (top N, default 5):
     │
     ├─► EVALUATE ──────────────────────────────────
     │   Full fit analysis (skills, experience, culture)
     │   Show: strengths, gaps, honest recommendation
     │
     ├─► DRAFT CV ──────────────────────────────────
     │   Mirror JD keywords for ATS
     │   Reorder experience sections to match role
     │   Save: cv/cv_<Company>_<Role>.md
     │
     ├─► DRAFT COVER LETTER ────────────────────────
     │   Specific opener (not generic)
     │   Tied to this company's product/need
     │   Save: cover_letters/cover_<Company>_<Role>.md
     │
     ├─► DRAFT COLD EMAIL ──────────────────────────
     │   To: Hiring Manager (if name found) or Recruiter
     │   Subject line + 150-word email body
     │   LinkedIn DM variant (80 words)
     │   Save: cover_letters/cold_email_<Company>_<Date>.md
     │
     └─► RECORD ────────────────────────────────────
         Add to documents/job_tracker.csv
         Status: "ready_to_send"
     │
     ▼
4. SUMMARY REPORT
   Show a table of all processed applications:

   | # | Company | Role | Score | CV | Cover | Cold Email | Status |
   |---|---------|------|-------|----|-------|-----------|--------|
   | 1 | ...     | ...  | 4.2   | ✅ | ✅    | ✅        | ready  |

5. NEXT STEPS
   For each "ready_to_send" application:
   - Apply via the job portal link
   - Send the cold email to the hiring manager
   - Connect on LinkedIn with the DM variant

## Options
- `--limit N`    Process top N jobs only (default: 5)
- `--query X`    Override search keywords
- `--location X` Override location (default: India)
- `--remote`     Filter for remote jobs only
- `--dry-run`    Scrape and rank only, no drafting

## Safety Rules
- NEVER fabricate experience or skills
- NEVER claim a certification you don't have
- If a gap is critical, flag it honestly in the evaluation
- Cold emails DRAFT only — you review before sending

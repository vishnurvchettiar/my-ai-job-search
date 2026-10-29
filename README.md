<p align="center">
  <img src="https://img.shields.io/badge/AI%20Job%20Search-Vishnu%20Chettiar-blue?style=for-the-badge" alt="AI Job Search"/>
</p>

# 🤖 My AI Job Search

*The job search that runs on your machine — personalized for Vishnu Chettiar.*

An AI-powered job application framework that uses your preferred AI agent (Antigravity, Claude Code, Gemini CLI) to evaluate job postings, tailor your CV, write cover letters, and prepare you for interviews.

---

## What this does

```
/setup           /scrape             /apply <url>
  |                 |                     |
  v                 v                     v
Fill in your    Search job           Evaluate fit
profile         portals              Score & recommend
  |                 |                     |
  v                 v                     v
Profile         Present matches      Draft CV + Cover Letter
files ready     with fit ratings     (tailored, ATS-optimized)
                    |                     |
                    v                     v
                Pick a match         Reviewer agent critiques
                → /apply             → Revise → Final output
```

Also includes a **Blazor web dashboard** to track applications, companies, and outcomes.

---

## Quick Start

### 1. Clone this repo
```bash
git clone https://github.com/vishnurvchettiar/my-ai-job-search
cd my-ai-job-search
```

### 2. Set up your profile
Open `AGENTS.md` and fill in or update your personal profile details.

### 3. Use with your AI agent

**With Antigravity IDE:**
```
/apply https://linkedin.com/jobs/view/...
```

**With Claude Code:**
```bash
claude
/apply https://linkedin.com/jobs/view/...
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/setup` | Populate your profile and prepare templates |
| `/apply <url or text>` | Evaluate fit, tailor CV, write cover letter |
| `/scrape` | Search job portals for matching positions |
| `/rank` | Batch-score scraped listings, return ranked shortlist |
| `/interview` | Prepare for an upcoming interview |
| `/outcome <result>` | Record the result of an application |
| `/upskill` | Identify skill gaps and suggest a learning plan |
| `/salary` | Look up salary benchmarks for a role/location |

---

## Project Structure

```
my-ai-job-search/
├── AGENTS.md                  # Your profile + AI agent instructions
├── README.md                  # This file
├── cv/                        # Resume variants (tailored per application)
├── cover_letters/             # Cover letters (one per application)
├── documents/                 # Source docs (original CV, certificates)
│   └── applications/          # Archive per company/role
├── company_research/          # Research notes per company
├── job_scraper/               # Job search scripts
├── templates/                 # Reusable CV / cover letter templates
├── upskill/                   # Skill gap plans & learning resources
├── dashboard/                 # Blazor web app — application tracker
└── .agents/skills/            # AI skill definitions
```

---

## Dashboard (Blazor Web App)

A local Blazor Server web dashboard to visually track:
- All applications (status: applied, interview, offer, rejected)
- Companies researched
- Upcoming interviews
- Skill gap progress

### Run the dashboard
```bash
cd dashboard
dotnet run
```
Open: `https://localhost:5001`

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Agent | Antigravity IDE / Claude Code / Gemini CLI |
| CV/Cover Letter | Markdown + Word templates |
| Dashboard | Blazor Server (.NET 9) |
| Job Scraper | Python 3 |
| Version Control | Git + GitHub |

---

## Candidate

**Vishnu Chettiar** | India
- 🎯 Target roles: SDET, QA Automation, .NET Developer, Java Developer
- 🛠️ Stack: C#, .NET, Blazor, Java, Selenium, Playwright
- 📧 GitHub: [vishnurvchettiar](https://github.com/vishnurvchettiar)

---

*Fork it, fill in your profile, and let AI handle the boring parts of job hunting.*

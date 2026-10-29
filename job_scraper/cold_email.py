#!/usr/bin/env python3
"""
cold_email.py - Cold email generator for Vishnu Chettiar's job search
Generates personalized cold email drafts to hiring managers/recruiters.

Usage:
  python cold_email.py --company "Infosys" --role "SDET" --recipient "John Doe"
  python cold_email.py --company "TCS" --role ".NET Developer" --linkedin
  python cold_email.py --batch targets.csv
"""

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
import textwrap

# ---------------------------------------------------------------------------
# Candidate profile
# ---------------------------------------------------------------------------
CANDIDATE = {
    "name": "Vishnu Chettiar",
    "phone": "[+91-XXXXXXXXXX]",
    "email": "[your.email@gmail.com]",
    "linkedin": "linkedin.com/in/vishnu-chettiar",
    "github": "github.com/vishnurvchettiar",
    "roles": ["SDET", "QA Automation Engineer", ".NET Developer", "Java Developer"],
    "top_skill": "building test automation frameworks with Selenium/Playwright in C# and Java",
    "achievement": "delivered a full-stack Blazor/.NET clinic management system with integrated test coverage",
}

OUTPUT_DIR = Path(__file__).parent.parent / "cover_letters"
TRACKER = Path(__file__).parent.parent / "documents" / "job_tracker.csv"

# ---------------------------------------------------------------------------
# Email templates
# ---------------------------------------------------------------------------
EMAIL_TEMPLATE = """\
Subject: {subject}

Hi {first_name},

{opener}

I'm {name}, a {role} with hands-on experience in {top_skill}. Most recently I {achievement}.

I'm exploring opportunities at {company} and would love to connect briefly — would you have 15 minutes this week for a quick call?

Best,
{name}
{phone} | {email} | {linkedin}
"""

LINKEDIN_TEMPLATE = """\
Hi {first_name}, I'm {name} — {role} with experience in {top_skill}. I came across {company} and was impressed by {company_note}. Would love to connect and explore if there's a fit for your team. Happy to share my CV!
"""

def generate_subject(company: str, role: str) -> str:
    subjects = [
        f"{role} with .NET/Automation experience — {company}",
        f"Experienced {role} interested in {company}",
        f"{company} × {role} — Quick intro",
    ]
    return subjects[0]

def generate_opener(company: str, company_note: str) -> str:
    if company_note:
        return f"I noticed {company_note} — it caught my attention and I wanted to reach out directly."
    return f"I've been following {company}'s work and was impressed by the team's approach to software quality."

def generate_email(company: str, role: str, recipient: str, company_note: str = "") -> dict:
    first_name = recipient.split()[0] if recipient else "there"
    subject = generate_subject(company, role)
    opener = generate_opener(company, company_note)
    
    email_body = EMAIL_TEMPLATE.format(
        subject=subject,
        first_name=first_name,
        opener=opener,
        name=CANDIDATE["name"],
        role=role,
        top_skill=CANDIDATE["top_skill"],
        achievement=CANDIDATE["achievement"],
        company=company,
        phone=CANDIDATE["phone"],
        email=CANDIDATE["email"],
        linkedin=CANDIDATE["linkedin"],
    )
    
    linkedin_msg = LINKEDIN_TEMPLATE.format(
        first_name=first_name,
        name=CANDIDATE["name"],
        role=role,
        top_skill=CANDIDATE["top_skill"],
        company=company,
        company_note=company_note or f"your work in software development",
    )
    
    return {
        "company": company,
        "role": role,
        "recipient": recipient,
        "subject": subject,
        "email": email_body,
        "linkedin_dm": linkedin_msg,
    }

def save_draft(draft: dict):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = OUTPUT_DIR / f"cold_email_{draft['company'].replace(' ','_')}_{date_str}.md"
    
    content = f"""# Cold Email Draft — {draft['company']} ({draft['role']})

Generated: {date_str}
Recipient: {draft['recipient']}

---

## 📧 Email (send to recruiter/hiring manager)

```
{draft['email']}
```

---

## 💼 LinkedIn DM (shorter version)

```
{draft['linkedin_dm']}
```

---

## ✅ Checklist before sending
- [ ] Personalize the opener with something SPECIFIC about the company
- [ ] Verify recipient name and email
- [ ] Review for any generic phrases
- [ ] Attach CV only if they ask (not in first email)
- [ ] Log in job_tracker.csv after sending
"""
    filename.write_text(content, encoding="utf-8")
    print(f"✅  Draft saved: {filename}")
    return filename

def record_tracker(company: str, role: str, status: str = "cold_email_drafted"):
    TRACKER.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Company": company,
        "Role": role,
        "URL": "",
        "Status": status,
        "FitScore": "",
        "Salary": "",
        "Notes": "Cold email approach",
    }
    file_exists = TRACKER.exists()
    with open(TRACKER, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def process_batch(csv_file: str):
    """Process a CSV file of targets: company,role,recipient,company_note"""
    results = []
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f"\n📩  Generating email for {row['company']} — {row['role']} ...")
            draft = generate_email(
                company=row.get("company", ""),
                role=row.get("role", "SDET"),
                recipient=row.get("recipient", "Hiring Manager"),
                company_note=row.get("company_note", ""),
            )
            save_draft(draft)
            record_tracker(draft["company"], draft["role"])
            results.append(draft)
    print(f"\n🎉  Generated {len(results)} cold email drafts!")
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Cold Email Generator — Vishnu Chettiar",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--company", help="Company name")
    parser.add_argument("--role", default="SDET", help="Target role")
    parser.add_argument("--recipient", default="Hiring Manager", help="Recipient name")
    parser.add_argument("--note", default="", help="Specific company note (product, news, etc.)")
    parser.add_argument("--batch", help="CSV file with batch targets")
    parser.add_argument("--linkedin", action="store_true", help="Also print LinkedIn DM variant")
    args = parser.parse_args()

    if args.batch:
        process_batch(args.batch)
        return

    if not args.company:
        parser.print_help()
        print("\n⚠️   Provide --company or --batch")
        return

    draft = generate_email(args.company, args.role, args.recipient, args.note)
    save_draft(draft)
    record_tracker(draft["company"], draft["role"])

    print("\n" + "="*60)
    print(draft["email"])
    if args.linkedin:
        print("\n--- LinkedIn DM ---")
        print(draft["linkedin_dm"])

if __name__ == "__main__":
    main()

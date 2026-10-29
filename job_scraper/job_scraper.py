#!/usr/bin/env python3
"""
job_scraper.py - AI Job Search scraper for Vishnu Chettiar
Searches LinkedIn, Naukri, and Indeed (India) for matching positions.

Usage:
  python job_scraper.py --query "SDET" --location "India" --pages 3
  python job_scraper.py --query ".NET Developer" --location "Bangalore" --remote
"""

import argparse
import json
import csv
import re
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration - Target job portals and default search terms
# ---------------------------------------------------------------------------
DEFAULT_QUERY = "SDET OR QA Automation OR .NET Developer OR Java Developer"
DEFAULT_LOCATION = "India"
OUTPUT_DIR = Path(__file__).parent.parent / "documents"
TRACKER_CSV = OUTPUT_DIR / "job_tracker.csv"

SEARCH_URLS = {
    "linkedin": "https://www.linkedin.com/jobs/search/?keywords={query}&location={location}&f_TPR=r604800",
    "naukri":   "https://www.naukri.com/{query}-jobs-in-{location}",
    "indeed":   "https://in.indeed.com/jobs?q={query}&l={location}",
    "glassdoor":"https://www.glassdoor.co.in/Job/jobs.htm?sc.keyword={query}&locT=N&locId=115",
}

def build_search_urls(query: str, location: str, remote: bool) -> dict:
    """Build search URLs for all configured portals."""
    q = query.replace(" ", "+")
    loc = location.replace(" ", "+").lower()
    urls = {}
    for portal, template in SEARCH_URLS.items():
        urls[portal] = template.format(query=q, location=loc)
        if remote:
            if portal == "linkedin":
                urls[portal] += "&f_WT=2"   # LinkedIn remote filter
    return urls

def print_search_links(query: str, location: str, remote: bool):
    """Print clickable search links — open these in your browser."""
    urls = build_search_urls(query, location, remote)
    print("\n" + "="*70)
    print(f"🔍  Job Search: '{query}' in '{location}'{'  [REMOTE]' if remote else ''}")
    print("="*70)
    print("\nOpen these links in your browser:\n")
    for portal, url in urls.items():
        print(f"  {portal.upper():12} → {url}")
    print()

def record_application(company: str, role: str, url: str, fit_score: str = "", notes: str = ""):
    """Add a job to the tracker CSV."""
    TRACKER_CSV.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Company": company,
        "Role": role,
        "URL": url,
        "Status": "applied",
        "FitScore": fit_score,
        "Salary": "",
        "Notes": notes,
    }
    file_exists = TRACKER_CSV.exists()
    with open(TRACKER_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
    print(f"✅  Recorded: {company} — {role}")

def main():
    parser = argparse.ArgumentParser(
        description="AI Job Search — Vishnu Chettiar",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--query", default=DEFAULT_QUERY, help="Job search keywords")
    parser.add_argument("--location", default=DEFAULT_LOCATION, help="Location filter")
    parser.add_argument("--remote", action="store_true", help="Filter for remote jobs")
    parser.add_argument("--record", nargs=3, metavar=("COMPANY", "ROLE", "URL"),
                        help="Record an application: --record CompanyName RoleName URL")
    args = parser.parse_args()

    if args.record:
        record_application(*args.record)
    else:
        print_search_links(args.query, args.location, args.remote)
        print("💡  Tip: After finding a job, run:")
        print("         /apply <url>   (in your AI agent)")
        print("    Or record manually:")
        print("         python job_scraper.py --record \"CompanyName\" \"RoleName\" \"https://...\"")

if __name__ == "__main__":
    main()

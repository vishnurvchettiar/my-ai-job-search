#!/usr/bin/env python3
"""
auto_apply.py - Full auto-apply pipeline orchestrator for Vishnu Chettiar

Steps:
  1. Search job portals (print links)
  2. Generate cold emails for batch targets
  3. Print a summary report

Usage:
  python auto_apply.py                     # Full pipeline
  python auto_apply.py --cold-email-only   # Only cold emails
  python auto_apply.py --search-only       # Only search links
  python auto_apply.py --targets my.csv    # Custom targets CSV
"""

import argparse
import subprocess
import sys
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent

def run_search(query: str, location: str, remote: bool):
    print("\n" + "="*70)
    print("STEP 1: JOB SEARCH LINKS")
    print("="*70)
    cmd = [sys.executable, str(BASE / "job_scraper.py"),
           "--query", query, "--location", location]
    if remote:
        cmd.append("--remote")
    subprocess.run(cmd)

def run_cold_emails(targets_csv: str):
    print("\n" + "="*70)
    print("STEP 2: COLD EMAIL GENERATION")
    print("="*70)
    cmd = [sys.executable, str(BASE / "cold_email.py"), "--batch", targets_csv]
    subprocess.run(cmd)

def print_summary():
    tracker = BASE.parent / "documents" / "job_tracker.csv"
    print("\n" + "="*70)
    print("SUMMARY REPORT")
    print("="*70)
    if tracker.exists():
        import csv
        with open(tracker, encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        today = datetime.now().strftime("%Y-%m-%d")
        today_rows = [r for r in rows if r.get("Date") == today]
        print(f"\n✅  Applications processed today: {len(today_rows)}")
        for r in today_rows:
            print(f"   • {r['Company']:25} {r['Role']:30} [{r['Status']}]")
    
    cl_dir = BASE.parent / "cover_letters"
    emails = list(cl_dir.glob("cold_email_*.md")) if cl_dir.exists() else []
    print(f"\n📧  Cold email drafts ready: {len(emails)}")
    for e in sorted(emails)[-5:]:
        print(f"   • {e.name}")
    
    print("\n🚀  NEXT STEPS:")
    print("   1. Review cold email drafts in cover_letters/")
    print("   2. Open job search links in your browser")
    print("   3. For each job you like: run /apply <url> in your AI agent")
    print("   4. Personalize and send cold emails")
    print("   5. Track responses in documents/job_tracker.csv")

def main():
    parser = argparse.ArgumentParser(description="Auto-Apply Pipeline — Vishnu Chettiar")
    parser.add_argument("--query", default="SDET OR QA Automation OR .NET Developer", 
                        help="Job search keywords")
    parser.add_argument("--location", default="India", help="Location filter")
    parser.add_argument("--remote", action="store_true", help="Remote jobs only")
    parser.add_argument("--targets", default=str(BASE / "batch_targets.csv"),
                        help="CSV file with cold email targets")
    parser.add_argument("--cold-email-only", action="store_true")
    parser.add_argument("--search-only", action="store_true")
    args = parser.parse_args()

    print("\n" + "🤖 " * 20)
    print("  MY AI JOB SEARCH — Auto-Apply Pipeline")
    print("  Candidate: Vishnu Chettiar")
    print("🤖 " * 20)

    if not args.cold_email_only:
        run_search(args.query, args.location, args.remote)

    if not args.search_only:
        if Path(args.targets).exists():
            run_cold_emails(args.targets)
        else:
            print(f"\n⚠️  Targets file not found: {args.targets}")
            print("   Create it or use --targets path/to/your.csv")

    print_summary()

if __name__ == "__main__":
    main()

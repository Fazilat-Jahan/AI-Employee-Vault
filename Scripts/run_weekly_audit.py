#!/usr/bin/env python3
"""
Script to run the weekly business audit and generate CEO briefing
"""
from Skills.business_auditor import run_weekly_audit

def main():
    print("Starting weekly business audit...")
    briefing_path = run_weekly_audit()
    print(f"Weekly briefing generated: {briefing_path}")

if __name__ == "__main__":
    main()
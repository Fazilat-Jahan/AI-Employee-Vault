#!/usr/bin/env python3
"""
Simple Task Scheduler for AI Employee Vault
Implements basic scheduling functionality to meet Silver Tier requirements
"""
import schedule
import time
import subprocess
import threading
from pathlib import Path

def run_watcher():
    """Run the main watcher script"""
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Running watcher...")
    try:
        result = subprocess.run(['python', 'watcher.py'],
                              capture_output=True, text=True, timeout=30)
        print(f"Watcher completed with return code: {result.returncode}")
        if result.stdout:
            print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Errors: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("Watcher timed out!")
    except Exception as e:
        print(f"Error running watcher: {str(e)}")

def run_gmail_watcher():
    """Run the Gmail watcher script"""
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Running Gmail watcher...")
    try:
        result = subprocess.run(['python', 'Scripts/gmail_watcher.py'],
                              capture_output=True, text=True, timeout=30)
        print(f"Gmail watcher completed with return code: {result.returncode}")
    except Exception as e:
        print(f"Error running Gmail watcher: {str(e)}")

def run_linkedin_watcher():
    """Run the LinkedIn watcher script"""
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Running LinkedIn watcher...")
    try:
        result = subprocess.run(['python', 'Scripts/linkedin_post.py'],
                              capture_output=True, text=True, timeout=30)
        print(f"LinkedIn watcher completed with return code: {result.returncode}")
    except Exception as e:
        print(f"Error running LinkedIn watcher: {str(e)}")

def start_scheduler():
    """Start the task scheduler with configured jobs"""
    # Schedule the main watcher to run every 5 minutes
    schedule.every(5).minutes.do(run_watcher)

    # Schedule Gmail watcher to run every 10 minutes
    schedule.every(10).minutes.do(run_gmail_watcher)

    # Schedule LinkedIn watcher to run hourly
    schedule.every().hour.do(run_linkedin_watcher)

    print("Scheduler started. Press Ctrl+C to stop.")
    print("Jobs scheduled:")
    print("- Main watcher: every 5 minutes")
    print("- Gmail watcher: every 10 minutes")
    print("- LinkedIn watcher: every hour")

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScheduler stopped by user.")

if __name__ == "__main__":
    start_scheduler()
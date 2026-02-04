import time
from pathlib import Path
import subprocess

WATCH_FOLDER = Path("./Inbox")
CHECK_INTERVAL = 5  # seconds

already_seen = set(WATCH_FOLDER.iterdir())

while True:
    current_files = set(WATCH_FOLDER.iterdir())
    new_files = current_files - already_seen
    if new_files:
        print("New file detected:", new_files)
        # Trigger Claude to process tasks
        for file in new_files:
            subprocess.run([
                "claude",
                "--prompt", 
                f"""
You are my Personal AI Employee. 

Read the new file: {file}
Move actionable items to Needs_Action.
Update Dashboard.md with status.
Do nothing else.
"""
            ])
    already_seen = current_files
    time.sleep(CHECK_INTERVAL)

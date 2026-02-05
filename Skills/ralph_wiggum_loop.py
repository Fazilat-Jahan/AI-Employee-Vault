"""
Ralph Wiggum Loop for AI Employee Vault
Implements Gold Tier requirement for autonomous multi-step task completion
"""
import time
import subprocess
from pathlib import Path
import json
from datetime import datetime

class RalphWiggumLoop:
    def __init__(self, max_iterations=10):
        self.max_iterations = max_iterations

    def run_loop(self, initial_prompt, completion_condition=None):
        """
        Run the Ralph Wiggum loop until completion condition is met or max iterations reached

        Args:
            initial_prompt: The initial task prompt to start the loop
            completion_condition: Function that takes task file path and returns True if complete
        """
        iteration = 0

        # Create a state file to track the loop progress
        state_file = Path("Loop_State") / f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        state_file.parent.mkdir(exist_ok=True)

        # Write the initial prompt to the state file
        state_file.write_text(initial_prompt)

        print(f"Starting Ralph Wiggum loop with prompt: {initial_prompt[:100]}...")

        while iteration < self.max_iterations:
            print(f"Iteration {iteration + 1}/{self.max_iterations}")

            # Call Claude Code to work on the task
            try:
                result = subprocess.run([
                    "claude",
                    "--prompt",
                    f"Continue working on this task: {initial_prompt}. Current state: {state_file.read_text()}. Continue working until complete."
                ], capture_output=True, text=True, timeout=300)  # 5 minute timeout

                if result.returncode != 0:
                    print(f"Claude returned with error: {result.stderr}")
                    iteration += 1
                    continue

            except subprocess.TimeoutExpired:
                print("Claude execution timed out, continuing loop")
                iteration += 1
                continue

            # Check if the task is complete
            if completion_condition:
                if completion_condition(state_file):
                    print("Completion condition met, exiting loop")
                    break
            else:
                # Default completion check: look for files moved to Done/
                if self._check_task_completion():
                    print("Task appears to be completed (files in Done/), exiting loop")
                    break

            iteration += 1
            time.sleep(2)  # Small delay between iterations

        if iteration >= self.max_iterations:
            print(f"Reached maximum iterations ({self.max_iterations}), stopping loop")

        return state_file

    def _check_task_completion(self):
        """
        Check if task is complete by looking for movement to Done/ folder
        This is the advanced Gold Tier completion strategy mentioned in the document
        """
        done_folder = Path("Done")
        if done_folder.exists():
            done_files = list(done_folder.glob("*.md"))
            if len(done_files) > 0:
                return True
        return False

    def run_with_promise(self, initial_prompt, promise_text="TASK_COMPLETE"):
        """
        Run the loop with promise-based completion strategy
        """
        iteration = 0
        state_file = Path("Loop_State") / f"promise_task_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        state_file.parent.mkdir(exist_ok=True)

        full_prompt = f"{initial_prompt}\n\nWhen you have completed the task, output exactly: <promise>{promise_text}</promise>"
        state_file.write_text(full_prompt)

        while iteration < self.max_iterations:
            print(f"Promise-based iteration {iteration + 1}/{self.max_iterations}")

            try:
                result = subprocess.run([
                    "claude",
                    "--prompt",
                    f"Continue working on this task: {state_file.read_text()}. Check your output to see if you've printed the promise yet."
                ], capture_output=True, text=True, timeout=300)

                # Check if the promise was fulfilled in the output
                if result.stdout and f"<promise>{promise_text}</promise>" in result.stdout:
                    print(f"Promise '{promise_text}' found, task complete!")
                    return True

                # Also check if it's in the state file (Claude might have written it there)
                if state_file.exists() and f"<promise>{promise_text}</promise>" in state_file.read_text():
                    print(f"Promise '{promise_text}' found in state file, task complete!")
                    return True

            except subprocess.TimeoutExpired:
                print("Claude execution timed out, continuing loop")

            iteration += 1
            time.sleep(2)

        print(f"Promise not achieved within {self.max_iterations} iterations")
        return False

def create_ralph_loop_script():
    """
    Create a standalone script for the Ralph Wiggum loop that can be called externally
    """
    script_content = '''#!/usr/bin/env python3
"""
Ralph Wiggum Loop Script
Standalone script to run the Ralph Wiggum loop for autonomous task completion
"""
import sys
import argparse
from pathlib import Path
from skills.ralph_wiggum_loop import RalphWiggumLoop

def main():
    parser = argparse.ArgumentParser(description="Ralph Wiggum Loop for autonomous task completion")
    parser.add_argument("prompt", help="Initial prompt for the task")
    parser.add_argument("--completion-promise", help="Promise text to look for completion")
    parser.add_argument("--max-iterations", type=int, default=10, help="Maximum number of iterations")

    args = parser.parse_args()

    loop = RalphWiggumLoop(max_iterations=args.max_iterations)

    if args.completion_promise:
        success = loop.run_with_promise(args.prompt, args.completion_promise)
        if success:
            print("Task completed successfully with promise!")
            sys.exit(0)
        else:
            print("Task not completed within iteration limit")
            sys.exit(1)
    else:
        # Use default completion condition (file movement to Done/)
        def completion_check(task_file):
            from pathlib import Path
            done_folder = Path("Done")
            if done_folder.exists():
                done_files = list(done_folder.glob("*.md"))
                return len(done_files) > 0
            return False

        state_file = loop.run_loop(args.prompt, completion_condition=completion_check)
        print(f"Loop completed, final state in: {state_file}")

if __name__ == "__main__":
    main()
'''

    script_path = Path("ralph_loop.py")
    script_path.write_text(script_content)

    # Make it executable
    script_path.chmod(0o755)

    return script_path

def setup_ralph_wiggum_infrastructure():
    """
    Set up the Ralph Wiggum loop infrastructure
    """
    # Create necessary directories
    Path("Loop_State").mkdir(exist_ok=True)

    # Create the standalone script
    script_path = create_ralph_loop_script()

    print(f"Ralph Wiggum loop infrastructure set up.")
    print(f"Script created at: {script_path}")
    print("Usage examples:")
    print(f"  python {script_path} 'Process all files in Needs_Action'")
    print(f"  python {script_path} 'Process invoices' --completion-promise 'ALL_INVOICES_PROCESSED' --max-iterations 5")

    return script_path

# Example usage functions
def run_invoice_processing_loop():
    """
    Example: Run a loop to process invoices until all are done
    """
    prompt = """
    Process all invoices in the Needs_Action folder:
    1. Read each invoice file
    2. Generate appropriate response
    3. Move completed invoices to Done folder
    4. Continue until all invoices are processed
    """

    def check_invoices_done(state_file):
        done_folder = Path("Done")
        needs_action_folder = Path("Needs_Action")

        if done_folder.exists():
            done_invoices = list(done_folder.glob("*invoice*"))
            if needs_action_folder.exists():
                remaining_invoices = list(needs_action_folder.glob("*invoice*"))
                return len(remaining_invoices) == 0 and len(done_invoices) > 0

        return False

    loop = RalphWiggumLoop(max_iterations=15)
    return loop.run_loop(prompt, completion_condition=check_invoices_done)

def run_client_communication_loop():
    """
    Example: Run a loop to handle client communications
    """
    prompt = """
    Handle all client communication tasks in Needs_Action:
    1. Read each client message
    2. Generate appropriate response based on Company_Handbook.md
    3. For sensitive matters, create approval request in Pending_Approval/
    4. Move completed tasks to Done/
    5. Continue until all client tasks are handled
    """

    def check_client_tasks_done(state_file):
        done_folder = Path("Done")
        needs_action_folder = Path("Needs_Action")

        if done_folder.exists():
            done_client_tasks = list(done_folder.glob("*client*")) + list(done_folder.glob("*email*"))
            if needs_action_folder.exists():
                remaining_client_tasks = list(needs_action_folder.glob("*client*")) + list(needs_action_folder.glob("*email*"))
                # We'll consider it done if we've processed some tasks and there are fewer remaining
                return len(done_client_tasks) > 0 and len(remaining_client_tasks) <= 2

        return False

    loop = RalphWiggumLoop(max_iterations=10)
    return loop.run_loop(prompt, completion_condition=check_client_tasks_done)
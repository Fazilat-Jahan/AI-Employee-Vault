"""
Task Processor Skill
Moves tasks from Inbox to Needs_Action and creates Plan files
"""
import os
from pathlib import Path

def process_task(task_file):
    """Process a single task from Inbox"""
    inbox_path = Path("Inbox")
    needs_action_path = Path("Needs_Action")

    # Move task from Inbox to Needs_Action
    task_src = inbox_path / task_file
    task_dst = needs_action_path / task_file

    if task_src.exists():
        task_src.rename(task_dst)
        return f"Moved {task_file} to Needs_Action"
    return f"Task {task_file} not found in Inbox"

def create_plan(task_file):
    """Create a plan file for a task"""
    plans_path = Path("Plans")
    needs_action_path = Path("Needs_Action")

    task_path = Path(needs_action_path) / task_file
    plan_filename = task_file.replace('.md', '_Plan.md')
    plan_path = plans_path / plan_filename

    if task_path.exists() and not plan_path.exists():
        # Create a basic plan template
        plan_content = f"""# Plan for {task_file}

## Objective
- Process the task from {task_file}

## Steps
1. Analyze the requirements
2. Execute necessary actions
3. Update status in Dashboard.md
4. Move to Done when complete

## Resources Needed
- Relevant documentation
- External API access if required
"""
        plan_path.write_text(plan_content)
        return f"Created plan: {plan_filename}"

    return f"Plan already exists or task not found: {task_file}"
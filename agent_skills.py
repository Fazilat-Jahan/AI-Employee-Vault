"""
Main Agent Skills Interface for AI Employee Vault
Coordinates all the skills to function as a unified system
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'Skills'))

from Skills.task_processor import process_task, create_plan
from Skills.dashboard_updater import update_dashboard, get_dashboard_status
from Skills.approval_handler import create_approval_request, check_approvals, approve_request

def execute_skill(skill_name, *args, **kwargs):
    """
    Execute a specific skill by name with given parameters
    """
    if skill_name == "process_task":
        return process_task(*args, **kwargs)
    elif skill_name == "create_plan":
        return create_plan(*args, **kwargs)
    elif skill_name == "update_dashboard":
        return update_dashboard(*args, **kwargs)
    elif skill_name == "get_dashboard_status":
        return get_dashboard_status(*args, **kwargs)
    elif skill_name == "create_approval_request":
        return create_approval_request(*args, **kwargs)
    elif skill_name == "check_approvals":
        return check_approvals(*args, **kwargs)
    elif skill_name == "approve_request":
        return approve_request(*args, **kwargs)
    else:
        raise ValueError(f"Unknown skill: {skill_name}")

def main():
    """
    Main entry point for the AI Employee system
    """
    print("AI Employee Vault System")
    print("========================")
    print("Available skills:")
    print("- process_task: Move task from Inbox to Needs_Action")
    print("- create_plan: Create a plan file for a task")
    print("- update_dashboard: Update the dashboard with status")
    print("- get_dashboard_status: Get current dashboard status")
    print("- create_approval_request: Create human approval request")
    print("- check_approvals: Check for pending approvals")
    print("- approve_request: Mark an approval as approved")

    # Example usage
    if len(sys.argv) > 1:
        skill = sys.argv[1]
        args = sys.argv[2:]

        try:
            result = execute_skill(skill, *args)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        print("\nUsage: python agent_skills.py <skill_name> [arguments]")
        print("Example: python agent_skills.py update_dashboard 'New task received'")

if __name__ == "__main__":
    main()
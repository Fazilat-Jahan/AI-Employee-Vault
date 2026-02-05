"""
Approval Handler Skill
Manages the human-in-the-loop approval workflow
"""
from pathlib import Path
import json
from datetime import datetime

def create_approval_request(task_name, action_details):
    """Create an approval request for sensitive tasks"""
    approvals_path = Path("Approvals")
    approvals_path.mkdir(exist_ok=True)

    # Create approval filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    approval_filename = f"Approval_{task_name.replace(' ', '_')}_{timestamp}.md"
    approval_path = approvals_path / approval_filename

    # Create approval request content
    approval_content = f"""# Approval Request

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Task:** {task_name}
**Action:** {action_details}

## Description
This action requires human approval before execution.

## Action Details
- Task: {task_name}
- Action: {action_details}
- Reason: Sensitive action requiring verification

## Options
- ✅ **APPROVE**: Execute the requested action
- ❌ **REJECT**: Cancel the requested action
- 🔄 **MODIFY**: Request changes to the action

## Instructions
To approve, move this file to the 'Approved' section or mark as 'APPROVED' below.
"""

    approval_path.write_text(approval_content)
    return f"Approval request created: {approval_filename}"

def check_approvals():
    """Check for pending approvals"""
    approvals_path = Path("Approvals")
    if not approvals_path.exists():
        return []

    approval_files = list(approvals_path.glob("*.md"))
    return [f.name for f in approval_files]

def approve_request(approval_file):
    """Mark an approval request as approved"""
    approval_path = Path("Approvals") / approval_file
    if approval_path.exists():
        # Read the current content
        content = approval_path.read_text()

        # Add approval status
        updated_content = content + f"\n\n**STATUS:** APPROVED on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

        # Write back the updated content
        approval_path.write_text(updated_content)

        # Move to a processed folder or rename to indicate approval
        approved_path = approval_path.parent / f"APPROVED_{approval_path.name}"
        approval_path.rename(approved_path)

        return f"Request approved: {approval_file}"

    return f"Approval file not found: {approval_file}"
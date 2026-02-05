"""
Dashboard Updater Skill
Updates the Dashboard.md file with status information
"""
from datetime import datetime
from pathlib import Path

def update_dashboard(status_update):
    """Update the dashboard with a status message"""
    dashboard_path = Path("Dashboard.md")

    current_content = ""
    if dashboard_path.exists():
        current_content = dashboard_path.read_text()

    # Find the Last Update section and add the new update
    lines = current_content.split('\n')
    new_lines = []
    last_update_found = False

    for line in lines:
        new_lines.append(line)
        if line.strip() == 'Last Update:':
            last_update_found = True
        elif last_update_found and line.startswith('- ') and not line.startswith('- '):
            # Insert the new update after the last update item
            new_lines.insert(-1, f'- {status_update}')
            last_update_found = False  # Reset flag

    # If we didn't find the Last Update section or didn't add the update, append it
    if last_update_found:
        # If we found Last Update but didn't add the update yet, add it now
        new_lines.append(f'- {status_update}')
    elif '- ' not in current_content or 'Last Update:' not in current_content:
        # If this is the first update, create the structure
        new_content = f"""# Dashboard

Status: Active

Last Update:
- {status_update}

## Summary
- Total tasks processed: 1
"""
        dashboard_path.write_text(new_content)
        return f"Dashboard updated with: {status_update}"

    # Update the summary section if it exists
    summary_idx = -1
    total_tasks = 0
    for i, line in enumerate(new_lines):
        if 'Total tasks processed:' in line:
            # Extract current count and increment
            try:
                current_count = int(line.split(':')[1].strip())
                total_tasks = current_count + 1
                new_lines[i] = f"- Total tasks processed: {total_tasks}"
            except:
                total_tasks = 1
                new_lines[i] = f"- Total tasks processed: {total_tasks}"
        elif '## Summary' in line:
            summary_idx = i

    # If no summary exists, create one
    if summary_idx != -1:
        # Look for the tasks processed line in summary, if not found add it
        found_summary_line = False
        for i in range(summary_idx, len(new_lines)):
            if 'Total tasks processed:' in new_lines[i]:
                found_summary_line = True
                break
        if not found_summary_line:
            new_lines.insert(summary_idx + 1, f"- Total tasks processed: {total_tasks}")
    else:
        # Append summary section
        new_lines.extend(['', '## Summary', f'- Total tasks processed: {total_tasks}', ''])

    # Write the updated content
    dashboard_path.write_text('\n'.join(new_lines))
    return f"Dashboard updated with: {status_update}"

def get_dashboard_status():
    """Get the current dashboard status"""
    dashboard_path = Path("Dashboard.md")
    if dashboard_path.exists():
        return dashboard_path.read_text()
    return "# Dashboard\n\nStatus: Empty"
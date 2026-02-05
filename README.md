# AI Employee Vault

A local-first, agent-driven AI system that automates personal and business workflows using Claude Code and Obsidian.

## Structure
```
AI Employee Vault/
├─ Inbox/               # Incoming tasks
├─ Needs_Action/        # Tasks ready for processing
├─ Done/                # Completed tasks
├─ Plans/               # Generated plan files
├─ Pending_Approval/    # Human approval required
├─ Approved/            # Approved actions
├─ Rejected/            # Rejected actions
├─ Logs/                # Audit logs
├─ Briefings/           # CEO briefings
├─ Scripts/             # Automation scripts
├─ Skills/              # Agent skills
├─ Dashboard.md         # Status and summary
├─ Company_Handbook.md  # Project guidelines
└─ Business_Goals.md    # Business objectives
```

## Tiers

### Bronze: Foundation
- Obsidian vault with Dashboard.md and Company_Handbook.md
- One working watcher script
- Claude Code reading/writing to vault
- Basic folder structure: /Inbox, /Needs_Action, /Done
- All AI as Agent Skills

### Silver: Functional Assistant
- Two+ watcher scripts (Gmail, LinkedIn)
- Automatic Plan.md creation
- MCP server for external actions
- Human-in-the-loop approval workflow
- Scheduling via cron/Task Scheduler

### Gold: Advanced Automation
- Cross-domain integration (Personal + Business)
- Odoo accounting system integration
- Social media integration (FB, IG, Twitter)
- Multiple MCP servers
- Weekly business audits & CEO briefings
- Error recovery & graceful degradation
- Comprehensive audit logging
- Ralph Wiggum loop for task completion
# Personal AI Employee (Digital FTE)

A local-first, agent-driven AI system designed to automate personal and business workflows. This project leverages **Claude Code** for reasoning and **Obsidian** as a local knowledge dashboard. It includes automation scripts, task processing, planning, and approval workflows to function as a full-time digital assistant.

---

## Project Overview

The Personal AI Employee is a "Digital FTE" (Full-Time Equivalent) that acts like a senior assistant: proactively managing tasks, generating plans, and updating a central dashboard. The system uses **watcher scripts** to monitor input sources and a **MCP server** for executing approved external actions.

---

## Project Structure

```

AI Employee Vault/
├─ Inbox/           # Incoming tasks
├─ Needs_Action/    # Tasks ready for processing
├─ Done/            # Completed tasks
├─ Plans/           # Generated plan files
├─ Approvals/       # Human-in-the-loop approval files
├─ Scripts/         # Automation scripts (Gmail, LinkedIn, MCP server)
├─ Dashboard.md     # Status and summary
├─ Company_Handbook.md  # Project guidelines and rules

```

---

## Bronze Tier: Foundation

Minimum viable deliverable includes:

- **Obsidian vault** with `Dashboard.md` and `Company_Handbook.md`  
- **One working watcher script** (Gmail or file system monitoring)  
- **Claude Code** successfully reading from and writing to the vault  
- Basic folder structure: `/Inbox`, `/Needs_Action`, `/Done`  
- All AI functionality implemented as **Agent Skills**

**Goal:** Establish a fully functional local workspace where tasks can be created, tracked, and processed by Claude.

---

## Silver Tier: Functional Assistant

Includes all Bronze requirements plus:

- Two or more **Watcher scripts** (e.g., Gmail + LinkedIn)  
- Automatic creation of **Plan.md** files for each new task  
- **MCP server** for external actions (emails, notifications)  
- **Human-in-the-loop approval workflow** for sensitive tasks  
- Basic scheduling via **cron** or **Task Scheduler**  
- Full integration with **Dashboard.md** for status updates  
- All AI functionality implemented as **Agent Skills**

**Goal:** Automate the monitoring, planning, and preliminary handling of tasks while allowing manual approval for sensitive actions.

---

## Workflow Summary

1. Watchers detect new tasks from external sources.  
2. Tasks are moved from **Inbox** → **Needs_Action**.  
3. Claude generates corresponding **Plan.md** files.  
4. Updates are logged in **Dashboard.md**.  
5. Sensitive tasks are sent to **Approvals/** for manual review before execution via MCP server.  

---

## Notes

- This system is **local-first**, meaning all task data is stored in the Obsidian vault.  
- `.py` scripts in the `Scripts/` folder handle automation logic.  
- Markdown files (`.md`) in the vault are automatically reflected in Obsidian for easy tracking.
```


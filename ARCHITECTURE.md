# AI Employee Vault Architecture

## Overview
This document describes the architecture of the AI Employee Vault system, a local-first, agent-driven AI system designed to automate personal and business workflows. The system leverages Claude Code for reasoning and Obsidian as a local knowledge dashboard.

## System Components

### 1. Foundation Layer (Local Engine)
- **Obsidian Vault**: Acts as the GUI (Graphical User Interface) and Long-Term Memory
  - Dashboard.md: Real-time summary of bank balance, pending messages, and active business projects
  - Company_Handbook.md: Contains "Rules of Engagement" (e.g., "Always be polite on WhatsApp," "Flag any payment over $500 for my approval")
- **Claude Code**: Runs in terminal, pointed at the Obsidian vault, uses File System tools to read tasks and write reports

### 2. Perception Layer (The "Watchers")
- **Comms Watcher**: Monitors Gmail and WhatsApp (via local web-automation or APIs) and saves new urgent messages as .md files in a /Needs_Action folder
- **Finance Watcher**: Downloads local CSVs or calls banking APIs to log new transactions in /Accounting/Current_Month.md
- **File System Watcher**: Monitors local file drops

### 3. Reasoning Layer (Claude Code)
- Reads from /Needs_Action and /Accounting folders
- Creates Plan.md files in Obsidian with checkboxes for next steps
- Uses Ralph Wiggum loop for multi-step task completion

### 4. Action Layer (The "Hands")
- **MCP Servers**: Model Context Protocol servers that expose specific capabilities Claude can invoke
  - email-mcp: Send, draft, search emails (Gmail integration)
  - browser-mcp: Navigate, click, fill forms (Payment portals)
  - calendar-mcp: Create, update events (Scheduling)
  - slack-mcp: Send messages, read channels (Team communication)

### 5. Orchestrator Layer
- **Orchestrator.py**: Master Python script that handles timing and folder watching
- **Watchdog.py**: Health monitor that restarts failed processes

## Gold Tier Features Implemented

### 1. Cross-Domain Integration (Personal + Business)
- Integrated personal communications (Gmail, WhatsApp) with business operations
- Unified dashboard showing both personal and business activities
- Shared workflow for processing both personal and business tasks

### 2. Odoo Accounting System Integration
- Created `Skills/odoo_integration.py` for connecting to Odoo Community Edition
- Implements JSON-RPC API calls to interact with Odoo's accounting features
- Supports creating invoices, expenses, and retrieving financial data
- Includes comprehensive audit logging for all Odoo interactions

### 3. Social Media Integration
- Created `Skills/social_media_integration.py` for Facebook and Instagram
- Includes posting capabilities and summary generation
- Added Twitter/X integration with posting and analytics
- All social media actions are logged for audit trail

### 4. Multiple MCP Servers
- Enhanced existing MCP server architecture to support multiple server types
- Separate MCP servers for different action types (email, social media, payments, accounting)

### 5. Weekly Business and Accounting Audit
- Created `Skills/business_auditor.py` for generating CEO briefings
- Automated weekly audit process that analyzes revenue, tasks, bottlenecks
- Generates Monday Morning CEO Briefing with executive summary
- Includes proactive suggestions and upcoming deadline tracking

### 6. Error Recovery and Graceful Degradation
- Implemented in `Skills/error_recovery.py` with:
  - Retry logic with exponential backoff
  - Graceful degradation patterns
  - Service monitoring and restart capabilities
  - Action queuing for later processing
  - Comprehensive error logging

### 7. Comprehensive Audit Logging
- Implemented in `Skills/audit_logger.py` with:
  - Structured logging following required format
  - Daily log files with retention policies
  - Audit report generation capabilities
  - Action tracking with approval status

### 8. Ralph Wiggum Loop for Autonomous Task Completion
- Implemented in `Skills/ralph_wiggum_loop.py` with:
  - Promise-based completion strategy
  - File-movement completion strategy (Gold Tier advanced method)
  - Iteration limits and timeout controls
  - Standalone script for external triggering

### 9. All AI Functionality as Agent Skills
- Organized all functionality into modular skills in the Skills/ directory:
  - `task_processor.py`: Handles task processing and movement
  - `dashboard_updater.py`: Updates dashboard status
  - `approval_handler.py`: Manages approval workflows
  - `odoo_integration.py`: Handles accounting system integration
  - `social_media_integration.py`: Manages social media posts
  - `business_auditor.py`: Generates business audits
  - `error_recovery.py`: Manages error handling
  - `audit_logger.py`: Handles comprehensive logging
  - `ralph_wiggum_loop.py`: Implements autonomous task completion

## Security Architecture

### Credential Management
- Never store credentials in plain text or in Obsidian vault
- Use environment variables for API keys
- Dedicated secrets manager for banking credentials
- Create .env file (added to .gitignore) for local development
- Rotate credentials monthly and after any suspected breach

### Sandboxing & Isolation
- Development Mode flag that prevents real external actions
- Dry Run support for all action scripts
- Separate accounts for testing during development
- Rate limiting for maximum actions per hour

### Permission Boundaries
- Auto-approve thresholds for different action categories
- Always require approval for sensitive actions
- Detailed approval matrix by action category

### Audit Logging
- Every action must be logged for review
- Logs stored in /Vault/Logs/YYYY-MM-DD.json
- Retention for minimum 90 days

## Deployment Architecture

### Local Setup
```
AI Employee Vault/
├─ Inbox/           # Incoming tasks
├─ Needs_Action/    # Tasks ready for processing
├─ Done/            # Completed tasks
├─ Plans/           # Generated plan files
├─ Pending_Approval/ # Human approval required
├─ Approved/        # Approved actions
├─ Rejected/        # Rejected actions
├─ Logs/            # Audit logs
├─ Briefings/       # CEO briefings
├─ Queued_Actions/  # Actions queued for later
├─ Error_Queue/     # Failed actions
├─ Loop_State/      # Ralph Wiggum loop state
├─ Scripts/         # Automation scripts
├─ Skills/          # Agent skills
├─ Dashboard.md     # Status and summary
├─ Company_Handbook.md  # Project guidelines and rules
├─ Business_Goals.md    # Business objectives and metrics
└─ ARCHITECTURE.md  # This document
```

### Continuous vs. Scheduled Operations
- **Scheduled Operations**: Daily briefing, weekly audits
- **Continuous Operations**: Watchers monitoring inputs
- **Project-Based Operations**: Specific project tasks

## Key Patterns

### Base Watcher Pattern
```python
class BaseWatcher(ABC):
    def __init__(self, vault_path: str, check_interval: int = 60):
        # Common initialization
        pass

    @abstractmethod
    def check_for_updates(self) -> list:
        '''Return list of new items to process'''
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        '''Create .md file in Needs_Action folder'''
        pass

    def run(self):
        # Common execution logic
        pass
```

### Human-in-the-Loop Pattern
Claude writes approval request files instead of acting directly:
- Creates approval request in /Pending_Approval/ folder
- Waits for human to move file to /Approved/ folder
- Executes action when approval file appears

### Ralph Wiggum Loop Pattern
- Claude works on task until complete
- Stop hook intercepts Claude's exit
- Checks if task file is in /Done/
- Blocks exit and reinjects prompt if not complete
- Continues until task is fully processed

## Lessons Learned

### Technical Challenges
1. **Process Management**: Standard Python scripts are fragile; require supervisor processes (PM2, supervisord, systemd) for reliability
2. **Error Handling**: Distinguishing between transient and permanent errors is crucial for robust automation
3. **State Persistence**: The Ralph Wiggum loop is essential for multi-step task completion
4. **Security**: Credential management and approval workflows are critical for safe autonomous operation

### Operational Insights
1. **Monitoring**: Continuous health checks and process restarts are essential
2. **Logging**: Comprehensive audit trails are necessary for debugging and compliance
3. **Graceful Degradation**: Systems should continue operating when individual components fail
4. **Human Oversight**: Regular review schedules are essential for maintaining system alignment

### Best Practices Established
1. **Modular Skills**: Breaking functionality into discrete, testable skills improves maintainability
2. **File-Based Communication**: Using the filesystem as a coordination mechanism between components
3. **Structured Logging**: Consistent log formats enable automated analysis and reporting
4. **Iterative Development**: Starting with manual processes and gradually automating increases reliability

## Future Enhancements

### Platinum Tier Considerations
- Cloud deployment with 24/7 operation
- Work-zone specialization (cloud for drafts, local for approvals)
- Multi-agent coordination with synced vault
- Direct A2A messaging while keeping vault as audit record

### Security Improvements
- Enhanced encryption for sensitive data at rest
- More granular permission controls
- Additional authentication mechanisms
- Improved anomaly detection

### Scalability Features
- Load balancing across multiple Claude instances
- Parallel processing of independent tasks
- Enhanced caching mechanisms
- Distributed processing capabilities
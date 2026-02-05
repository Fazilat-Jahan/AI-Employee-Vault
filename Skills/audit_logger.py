"""
Comprehensive Audit Logging for AI Employee Vault
Implements Gold Tier requirement for comprehensive audit logging
"""
import json
import logging
from datetime import datetime
from pathlib import Path
import os

class AuditLogger:
    def __init__(self):
        self.logs_dir = Path("Logs")
        self.logs_dir.mkdir(exist_ok=True)

    def log_action(self, action_type, actor, target, parameters, approval_status, approved_by, result):
        """Log an action following the required format"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "actor": actor,
            "target": target,
            "parameters": parameters,
            "approval_status": approval_status,
            "approved_by": approved_by,
            "result": result
        }

        # Create logs directory if it doesn't exist
        self.logs_dir.mkdir(exist_ok=True)

        # Log to daily file
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.logs_dir / f"{today}.json"

        # Read existing logs or create empty list
        logs = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                import ast
                try:
                    logs = ast.literal_eval(f.read())  # Safely parse the list
                except:
                    logs = []

        # Add new log entry
        logs.append(log_entry)

        # Write back to file
        with open(log_file, 'w') as f:
            f.write(str(logs))

        return log_entry

    def log_email_action(self, to, subject, body, approval_status, approved_by, result):
        """Log email-related actions"""
        return self.log_action(
            action_type="email_send",
            actor="claude_code",
            target=to,
            parameters={"subject": subject, "body_preview": body[:100]},
            approval_status=approval_status,
            approved_by=approved_by,
            result=result
        )

    def log_payment_action(self, recipient, amount, reason, approval_status, approved_by, result):
        """Log payment-related actions"""
        return self.log_action(
            action_type="payment",
            actor="claude_code",
            target=recipient,
            parameters={"amount": amount, "reason": reason},
            approval_status=approval_status,
            approved_by=approved_by,
            result=result
        )

    def log_file_operation(self, operation, filepath, parameters, approval_status, approved_by, result):
        """Log file operation actions"""
        return self.log_action(
            action_type=f"file_{operation}",
            actor="claude_code",
            target=filepath,
            parameters=parameters,
            approval_status=approval_status,
            approved_by=approved_by,
            result=result
        )

    def log_social_media_action(self, platform, content, approval_status, approved_by, result):
        """Log social media actions"""
        return self.log_action(
            action_type=f"{platform}_post",
            actor="claude_code",
            target=platform,
            parameters={"content": content[:100]},
            approval_status=approval_status,
            approved_by=approved_by,
            result=result
        )

    def log_odoo_action(self, operation, details, approval_status, approved_by, result):
        """Log Odoo-related actions"""
        return self.log_action(
            action_type=f"odoo_{operation}",
            actor="claude_code",
            target="odoo_system",
            parameters=details,
            approval_status=approval_status,
            approved_by=approved_by,
            result=result
        )

    def get_logs_for_date(self, date_str):
        """Retrieve logs for a specific date"""
        log_file = self.logs_dir / f"{date_str}.json"
        if log_file.exists():
            with open(log_file, 'r') as f:
                import ast
                try:
                    return ast.literal_eval(f.read())
                except:
                    return []
        return []

    def get_recent_logs(self, days=7):
        """Retrieve logs for the past N days"""
        from datetime import timedelta
        logs = []
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            day_logs = self.get_logs_for_date(date_str)
            logs.extend(day_logs)
        return logs

    def generate_audit_report(self, start_date, end_date):
        """Generate an audit report for a date range"""
        # This would aggregate logs between start and end dates
        # For now, we'll return a simple summary
        all_logs = self.get_recent_logs(30)  # Get last 30 days for demo

        report = {
            "start_date": start_date,
            "end_date": end_date,
            "total_actions": len(all_logs),
            "actions_by_type": {},
            "actions_by_actor": {},
            "approval_stats": {"approved": 0, "rejected": 0, "pending": 0},
            "failed_actions": 0
        }

        for log in all_logs:
            # Count by action type
            action_type = log["action_type"]
            report["actions_by_type"][action_type] = report["actions_by_type"].get(action_type, 0) + 1

            # Count by actor
            actor = log["actor"]
            report["actions_by_actor"][actor] = report["actions_by_actor"].get(actor, 0) + 1

            # Count approvals
            approval_status = log["approval_status"]
            if approval_status in report["approval_stats"]:
                report["approval_stats"][approval_status] += 1
            else:
                report["approval_stats"][approval_status] = 1

            # Count failed actions
            if log["result"] == "failed":
                report["failed_actions"] += 1

        return report

    def clean_old_logs(self, days_to_keep=90):
        """Clean logs older than specified days"""
        import shutil
        from datetime import timedelta

        cutoff_date = datetime.now() - timedelta(days=days_to_keep)

        for log_file in self.logs_dir.glob("*.json"):
            # Extract date from filename (assuming format YYYY-MM-DD.json)
            try:
                date_str = log_file.stem
                file_date = datetime.strptime(date_str, "%Y-%m-%d")

                if file_date < cutoff_date:
                    log_file.unlink()
            except ValueError:
                # Skip files that don't match the expected date format
                continue

def setup_logging_infrastructure():
    """Set up the complete logging infrastructure"""
    # Create necessary directories
    Path("Logs").mkdir(exist_ok=True)
    Path("Audit_Reports").mkdir(exist_ok=True)

    # Initialize the audit logger
    audit_logger = AuditLogger()

    # Example of logging different types of actions
    # These would be called from other parts of the system

    # Example email action log
    audit_logger.log_email_action(
        to="client@example.com",
        subject="Invoice #123",
        body="Please find attached your invoice...",
        approval_status="approved",
        approved_by="human",
        result="success"
    )

    # Example payment action log
    audit_logger.log_payment_action(
        recipient="Vendor ABC",
        amount=500.00,
        reason="Invoice #456",
        approval_status="approved",
        approved_by="human",
        result="success"
    )

    # Example file operation log
    audit_logger.log_file_operation(
        operation="create",
        filepath="/Vault/Invoices/2026-01_Invoice.pdf",
        parameters={"source": "generated", "size": "1.2MB"},
        approval_status="auto_approved",
        approved_by="system",
        result="success"
    )

    return audit_logger

# Global audit logger instance
audit_logger_instance = AuditLogger()

# Convenience functions to log actions from anywhere in the system
def log_email_action(to, subject, body, approval_status, approved_by, result):
    return audit_logger_instance.log_email_action(to, subject, body, approval_status, approved_by, result)

def log_payment_action(recipient, amount, reason, approval_status, approved_by, result):
    return audit_logger_instance.log_payment_action(recipient, amount, reason, approval_status, approved_by, result)

def log_file_operation(operation, filepath, parameters, approval_status, approved_by, result):
    return audit_logger_instance.log_file_operation(operation, filepath, parameters, approval_status, approved_by, result)

def log_social_media_action(platform, content, approval_status, approved_by, result):
    return audit_logger_instance.log_social_media_action(platform, content, approval_status, approved_by, result)

def log_odoo_action(operation, details, approval_status, approved_by, result):
    return audit_logger_instance.log_odoo_action(operation, details, approval_status, approved_by, result)
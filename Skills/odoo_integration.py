"""
Odoo Integration for AI Employee Vault
Implements Gold Tier requirement for accounting system integration
"""
import xmlrpc.client
import json
from datetime import datetime
from pathlib import Path

class OdooIntegration:
    def __init__(self, url, db, username, password):
        self.url = url
        self.db = db
        self.username = username
        self.password = password

        # Authenticate and get uid
        common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
        self.uid = common.authenticate(self.db, self.username, self.password, {})

        if not self.uid:
            raise Exception("Authentication failed")

        self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')

    def create_invoice(self, partner_id, invoice_lines, date=None):
        """Create an invoice in Odoo"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        invoice_vals = {
            'partner_id': partner_id,
            'move_type': 'out_invoice',
            'invoice_date': date,
            'invoice_line_ids': [(0, 0, line) for line in invoice_lines]
        }

        invoice_id = self.models.execute_kw(
            self.db, self.uid, self.password,
            'account.move', 'create',
            [invoice_vals]
        )

        return invoice_id

    def search_partners(self, domain):
        """Search for partners/customers in Odoo"""
        partner_ids = self.models.execute_kw(
            self.db, self.uid, self.password,
            'res.partner', 'search',
            [domain]
        )
        return partner_ids

    def get_partner_info(self, partner_id):
        """Get detailed information about a partner"""
        partner_data = self.models.execute_kw(
            self.db, self.uid, self.password,
            'res.partner', 'read',
            [partner_id], {'fields': ['name', 'email', 'phone', 'street', 'city', 'country_id']}
        )
        return partner_data[0] if partner_data else None

    def create_expense(self, expense_vals):
        """Create an expense record in Odoo"""
        expense_id = self.models.execute_kw(
            self.db, self.uid, self.password,
            'hr.expense', 'create',
            [expense_vals]
        )
        return expense_id

    def get_account_balance(self, account_id):
        """Get balance for a specific account"""
        account_data = self.models.execute_kw(
            self.db, self.uid, self.password,
            'account.account', 'read',
            [account_id], {'fields': ['name', 'current_balance']}
        )
        return account_data[0] if account_data else None

    def generate_report(self, report_name, data):
        """Generate a report in Odoo"""
        report = self.models.execute_kw(
            self.db, self.uid, self.password,
            'ir.actions.report', 'render',
            [report_name, data]
        )
        return report

def create_odoo_mcp_server():
    """Create an MCP server for Odoo integration"""
    # This would typically be implemented as a separate MCP server
    # For now, we'll create a wrapper class
    pass

def log_odoo_action(action_type, details, result):
    """Log Odoo actions for audit trail"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action_type": action_type,
        "details": details,
        "result": result,
        "system": "odoo_integration"
    }

    # Create logs directory if it doesn't exist
    logs_dir = Path("Logs")
    logs_dir.mkdir(exist_ok=True)

    # Log to daily file
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = logs_dir / f"{today}.json"

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
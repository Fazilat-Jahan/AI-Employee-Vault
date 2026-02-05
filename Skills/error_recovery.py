"""
Error Recovery and Graceful Degradation for AI Employee Vault
Implements Gold Tier requirement for error recovery and graceful degradation
"""
import time
import logging
from functools import wraps
from datetime import datetime
from pathlib import Path
import subprocess
import signal
import sys

class ErrorRecovery:
    def __init__(self):
        # Set up logging
        self.logger = logging.getLogger("AI_Employee_Error_Recovery")
        self.logger.setLevel(logging.INFO)

        # Create logs directory if it doesn't exist
        logs_dir = Path("Logs")
        logs_dir.mkdir(exist_ok=True)

        # Create file handler for error logs
        log_file = logs_dir / f"errors_{datetime.now().strftime('%Y-%m-%d')}.log"
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def with_retry(self, max_attempts=3, base_delay=1, max_delay=60):
        """Decorator to add retry logic with exponential backoff"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                last_exception = None

                for attempt in range(max_attempts):
                    try:
                        return func(*args, **kwargs)
                    except TransientError as e:
                        last_exception = e
                        if attempt == max_attempts - 1:
                            raise
                        delay = min(base_delay * (2 ** attempt), max_delay)
                        self.logger.warning(f'Attempt {attempt + 1} failed: {str(e)}, retrying in {delay}s')
                        time.sleep(delay)
                    except Exception as e:
                        # For non-transient errors, don't retry
                        self.logger.error(f'Non-transient error in {func.__name__}: {str(e)}')
                        raise

                raise last_exception
            return wrapper
        return decorator

    def graceful_degradation(self, fallback_func=None):
        """Decorator to handle graceful degradation"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except CriticalServiceUnavailable as e:
                    self.logger.error(f'Critical service unavailable: {str(e)}')
                    if fallback_func:
                        self.logger.info(f'Falling back to {fallback_func.__name__}')
                        return fallback_func(*args, **kwargs)
                    else:
                        # Queue action for later processing
                        self.queue_for_later(func.__name__, args, kwargs)
                        return None
                except Exception as e:
                    self.logger.error(f'Error in {func.__name__}: {str(e)}')
                    raise
            return wrapper
        return decorator

    def queue_for_later(self, func_name, args, kwargs):
        """Queue action for later processing when service is restored"""
        queue_dir = Path("Queued_Actions")
        queue_dir.mkdir(exist_ok=True)

        # Create a queue entry with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        queue_file = queue_dir / f"{func_name}_{timestamp}.json"

        queue_entry = {
            'function': func_name,
            'args': args,
            'kwargs': kwargs,
            'timestamp': datetime.now().isoformat(),
            'retry_count': 0
        }

        with open(queue_file, 'w') as f:
            import json
            json.dump(queue_entry, f, indent=2)

        self.logger.info(f'Action queued for later: {queue_file.name}')

    def process_queued_actions(self):
        """Process queued actions when services are restored"""
        queue_dir = Path("Queued_Actions")
        if not queue_dir.exists():
            return 0

        processed = 0
        for queue_file in queue_dir.glob("*.json"):
            try:
                with open(queue_file, 'r') as f:
                    import json
                    queue_entry = json.load(f)

                # Attempt to execute the queued action
                func_name = queue_entry['function']

                # Import the appropriate function based on name
                if func_name == 'send_email':
                    from Skills.email_handler import send_email
                    func = send_email
                elif func_name == 'post_to_social':
                    from Skills.social_media_integration import SocialMediaIntegration
                    # Assuming we have the integration instance
                    smi = SocialMediaIntegration()
                    func = getattr(smi, 'post_to_facebook')  # Simplified for example
                else:
                    # For other functions, we'd need to dynamically import
                    continue

                # Execute the function
                func(*queue_entry['args'], **queue_entry['kwargs'])

                # Remove the processed file
                queue_file.unlink()
                processed += 1
                self.logger.info(f'Processed queued action: {queue_file.name}')

            except Exception as e:
                self.logger.error(f'Failed to process queued action {queue_file.name}: {str(e)}')
                # Increment retry count
                queue_entry['retry_count'] += 1
                # If retry count is high, maybe move to error queue
                if queue_entry['retry_count'] > 5:
                    error_queue_dir = Path("Error_Queue")
                    error_queue_dir.mkdir(exist_ok=True)
                    error_file = error_queue_dir / queue_file.name
                    queue_file.rename(error_file)
                    self.logger.error(f'Moved failed action to error queue: {error_file.name}')

        return processed

class Watchdog:
    """Watchdog process to monitor and restart critical services"""

    def __init__(self):
        self.processes = {}
        self.logger = logging.getLogger("AI_Employee_Watchdog")

    def register_process(self, name, cmd, pid_file):
        """Register a process to be monitored"""
        self.processes[name] = {
            'cmd': cmd,
            'pid_file': Path(pid_file)
        }

    def is_process_running(self, pid_file):
        """Check if a process is running by PID"""
        if not pid_file.exists():
            return False

        try:
            with open(pid_file, 'r') as f:
                pid = int(f.read().strip())

            # Try to check if process exists (Unix/Linux)
            try:
                import os
                os.kill(pid, 0)  # Signal 0 doesn't kill, just checks if process exists
                return True
            except OSError:
                return False
        except (ValueError, FileNotFoundError):
            return False

    def start_process(self, name):
        """Start a registered process"""
        if name not in self.processes:
            self.logger.error(f'Process {name} not registered')
            return False

        proc_info = self.processes[name]
        cmd = proc_info['cmd']
        pid_file = proc_info['pid_file']

        try:
            # Start the process
            proc = subprocess.Popen(cmd.split())

            # Save PID to file
            pid_file.write_text(str(proc.pid))

            self.logger.info(f'Started process {name} with PID {proc.pid}')
            return True
        except Exception as e:
            self.logger.error(f'Failed to start process {name}: {str(e)}')
            return False

    def check_and_restart(self):
        """Check all registered processes and restart if needed"""
        restarted = []

        for name, proc_info in self.processes.items():
            pid_file = proc_info['pid_file']

            if not self.is_process_running(pid_file):
                self.logger.warning(f'{name} not running, restarting...')
                if self.start_process(name):
                    restarted.append(name)
                    self.notify_human(f'{name} was restarted')

        return restarted

    def notify_human(self, message):
        """Notify human about process restarts or issues"""
        # This could send an email, push notification, etc.
        self.logger.warning(f'HUMAN NOTIFICATION: {message}')
        # In a real implementation, this would trigger an alert mechanism

# Custom exception classes
class TransientError(Exception):
    """Error that might resolve itself (network timeout, rate limit, etc.)"""
    pass

class CriticalServiceUnavailable(Exception):
    """Critical service is unavailable"""
    pass

class AuthenticationError(Exception):
    """Authentication failed or token expired"""
    pass

class DataCorruptionError(Exception):
    """Data corruption detected"""
    pass

def setup_watchdog_monitoring():
    """Set up the watchdog monitoring for critical processes"""
    watchdog = Watchdog()

    # Register critical processes
    watchdog.register_process(
        name='orchestrator',
        cmd='python orchestrator.py',
        pid_file='/tmp/orchestrator.pid'
    )

    watchdog.register_process(
        name='gmail_watcher',
        cmd='python Scripts/gmail_watcher.py',
        pid_file='/tmp/gmail_watcher.pid'
    )

    watchdog.register_process(
        name='file_watcher',
        cmd='python watcher.py',
        pid_file='/tmp/file_watcher.pid'
    )

    # Monitor continuously
    while True:
        watchdog.check_and_restart()
        time.sleep(60)  # Check every minute

def log_error_event(error_type, details, severity='medium'):
    """Log error events for audit trail"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "error_type": error_type,
        "details": details,
        "severity": severity,
        "system": "error_recovery"
    }

    # Create logs directory if it doesn't exist
    logs_dir = Path("Logs")
    logs_dir.mkdir(exist_ok=True)

    # Log to daily file
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = logs_dir / f"errors_{today}.json"

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
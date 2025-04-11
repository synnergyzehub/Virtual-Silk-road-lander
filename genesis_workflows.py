#!/usr/bin/env python3
"""
Genesis Stack Workflow Manager

This script manages the startup and coordination of all Genesis Stack services.
It provides a unified interface for starting different service combinations
based on the role and needs of the user.
"""

import os
import sys
import time
import argparse
import subprocess
import signal
from datetime import datetime

# Default port configuration
DEFAULT_PORTS = {
    "license_api": 5001,
    "license_management": 8505,
    "welcome_server": 8090,
    "genesis_dashboard": 5000
}

class GenesisWorkflowManager:
    """Manager for Genesis Stack workflows."""
    
    def __init__(self):
        """Initialize the workflow manager."""
        self.processes = {}
        self.initialize_directories()
    
    def initialize_directories(self):
        """Initialize required directories."""
        directories = [
            "data/licenses",
            "data/npu_nodes",
            "data/governance_rules",
            "data/divine_filters",
            "data/license_assignments",
            "data/synadmin_registrations",
            "config"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        # Make scripts executable
        executables = [
            "tools/genesis_shell_terminal.py",
            "tools/register_npu_node.py",
            "tools/init_npu_governance.py",
            "tools/generate_synergyze_license.py",
            "tools/assign_license_to_npu.py"
        ]
        
        for executable in executables:
            if os.path.exists(executable):
                try:
                    os.chmod(executable, 0o755)
                except Exception:
                    pass
    
    def start_service(self, name, command, wait_for_port=None, background=True):
        """Start a service."""
        print(f"Starting {name}...")
        
        # Split command into args for subprocess
        if isinstance(command, str):
            command = command.split()
        
        # Start the process
        if background:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
        else:
            process = subprocess.Popen(command)
        
        self.processes[name] = process
        
        # Wait for port to be available if specified
        if wait_for_port:
            print(f"Waiting for {name} to be available on port {wait_for_port}...")
            self._wait_for_port(wait_for_port, timeout=30)
        
        return process
    
    def _wait_for_port(self, port, timeout=30):
        """Wait for a port to be available."""
        import socket
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                socket.create_connection(("localhost", port), timeout=1)
                print(f"Port {port} is available.")
                return True
            except (socket.timeout, ConnectionRefusedError):
                time.sleep(1)
        
        print(f"Timed out waiting for port {port}.")
        return False
    
    def stop_all_services(self):
        """Stop all running services."""
        print("Stopping all services...")
        
        for name, process in list(self.processes.items()):
            print(f"Stopping {name}...")
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"{name} stopped.")
            except subprocess.TimeoutExpired:
                print(f"{name} did not terminate gracefully, killing...")
                process.kill()
            except Exception as e:
                print(f"Error stopping {name}: {e}")
            
            del self.processes[name]
    
    def run_genesis_stack(self, include_dashboard=False):
        """Run the complete Genesis Stack services."""
        self.start_service(
            "License API",
            ["python", "run_license_api.py"],
            wait_for_port=DEFAULT_PORTS["license_api"]
        )
        
        self.start_service(
            "License Management",
            ["python", "run_license_management.py"],
            wait_for_port=DEFAULT_PORTS["license_management"]
        )
        
        self.start_service(
            "Welcome Server",
            ["python", "web_server.py", "--entity", "Default"],
            wait_for_port=DEFAULT_PORTS["welcome_server"]
        )
        
        if include_dashboard:
            self.start_service(
                "Genesis Dashboard",
                ["streamlit", "run", "genesis_dashboard.py", "--server.port", str(DEFAULT_PORTS["genesis_dashboard"])],
                wait_for_port=DEFAULT_PORTS["genesis_dashboard"]
            )
        
        # Start the Genesis Shell as the foreground process
        try:
            # First try to use the curses-based shell
            print("Starting Genesis Shell Interface...")
            subprocess.run(["python", "run_genesis_shell.py"])
        except Exception:
            # Fall back to the terminal-based shell
            print("Starting Genesis Shell Terminal Interface...")
            subprocess.run(["python", "tools/genesis_shell_terminal.py"])
    
    def run_npu_services(self):
        """Run the NPU governance services."""
        try:
            # Start the terminal-based shell for NPU management
            print("Starting NPU Terminal Interface...")
            subprocess.run(["python", "tools/genesis_shell_terminal.py"])
        except Exception as e:
            print(f"Error running NPU Terminal Interface: {e}")
    
    def run_entity_management(self):
        """Run the entity management services."""
        self.start_service(
            "License Management",
            ["python", "run_license_management.py"],
            wait_for_port=DEFAULT_PORTS["license_management"]
        )
        
        try:
            # Start the terminal-based shell for entity management
            print("Starting Entity Management Interface...")
            subprocess.run(["python", "tools/genesis_shell_terminal.py"])
        except Exception as e:
            print(f"Error running Entity Management Interface: {e}")
    
    def run_genesis_dashboard(self):
        """Run the Genesis Dashboard."""
        try:
            # Start the Genesis Dashboard
            print("Starting Genesis Dashboard...")
            subprocess.run([
                "streamlit", "run", "genesis_dashboard.py",
                "--server.port", str(DEFAULT_PORTS["genesis_dashboard"])
            ])
        except Exception as e:
            print(f"Error running Genesis Dashboard: {e}")

def main():
    """Main function to run the Genesis Stack workflow manager."""
    parser = argparse.ArgumentParser(
        description='Genesis Stack Workflow Manager',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Available workflows:
  stack       - Run the complete Genesis Stack services
  npu         - Run the NPU governance services
  entity      - Run the entity management services
  dashboard   - Run the Genesis Dashboard

Examples:
  python genesis_workflows.py stack      # Run the complete stack
  python genesis_workflows.py dashboard  # Run only the dashboard
        """
    )
    
    parser.add_argument(
        'workflow',
        choices=['stack', 'npu', 'entity', 'dashboard'],
        help='The workflow to run'
    )
    
    parser.add_argument(
        '--with-dashboard',
        action='store_true',
        help='Include the dashboard when running the stack workflow'
    )
    
    args = parser.parse_args()
    
    # Create the workflow manager
    manager = GenesisWorkflowManager()
    
    # Register signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        print("\nShutting down...")
        manager.stop_all_services()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run the selected workflow
    try:
        if args.workflow == 'stack':
            manager.run_genesis_stack(include_dashboard=args.with_dashboard)
        elif args.workflow == 'npu':
            manager.run_npu_services()
        elif args.workflow == 'entity':
            manager.run_entity_management()
        elif args.workflow == 'dashboard':
            manager.run_genesis_dashboard()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        manager.stop_all_services()

if __name__ == "__main__":
    main()
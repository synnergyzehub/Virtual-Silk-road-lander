#!/usr/bin/env python3
"""
Central Station - Genesis Stack Coordination System

This script serves as the central coordination point for the Genesis Stack services.
It manages the initialization, startup, and monitoring of all components in the
distributed Genesis system.
"""

import os
import sys
import time
import signal
import argparse
import subprocess
import threading
from datetime import datetime

class CentralStation:
    """
    Genesis Stack Central Coordination System
    
    Manages the initialization, startup, and monitoring of all Genesis Stack services.
    Provides a central interface for controlling the distributed system components.
    """
    
    def __init__(self):
        """Initialize the Central Station."""
        self.services = {}
        self.running = False
        self.log_file = "central_station.log"
        
        # Ensure required directories exist
        self.initialize_directories()
    
    def initialize_directories(self):
        """Initialize required directories for Genesis Stack."""
        directories = [
            "data",
            "data/licenses",
            "data/npu_nodes",
            "data/governance_rules", 
            "data/divine_filters",
            "data/license_assignments",
            "data/synadmin_registrations",
            "logs",
            "config"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        # Ensure scripts are executable
        executables = [
            "tools/genesis_shell_terminal.py",
            "tools/register_npu_node.py",
            "tools/init_npu_governance.py",
            "tools/generate_synergyze_license.py",
            "tools/assign_license_to_npu.py",
            "run_genesis_shell_terminal.py",
            "run_license_api.py",
            "run_license_management.py"
        ]
        
        for executable in executables:
            if os.path.exists(executable):
                try:
                    os.chmod(executable, 0o755)
                except Exception as e:
                    self.log(f"Warning: Failed to make {executable} executable: {e}")
    
    def log(self, message):
        """Log a message to both console and log file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        
        print(log_message)
        
        with open(self.log_file, "a") as f:
            f.write(log_message + "\n")
    
    def start_service(self, name, command, log_file=None, wait_for_port=None):
        """
        Start a service with the given command.
        
        Args:
            name: Service name
            command: Command to run (string or list)
            log_file: File to redirect output to
            wait_for_port: Port to wait for (if service listens on a port)
            
        Returns:
            subprocess.Popen: The process object
        """
        self.log(f"Starting service: {name}")
        
        # Convert command to list if it's a string
        if isinstance(command, str):
            command = command.split()
        
        # Open log file if specified
        log_redirect = None
        if log_file:
            log_dir = os.path.dirname(log_file)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            log_redirect = open(log_file, "w")
        
        # Start the process
        try:
            process = subprocess.Popen(
                command,
                stdout=log_redirect,
                stderr=subprocess.STDOUT if log_redirect else None,
                universal_newlines=True
            )
            
            self.services[name] = {
                "process": process,
                "command": command,
                "log_file": log_file,
                "wait_for_port": wait_for_port,
                "start_time": datetime.now()
            }
            
            self.log(f"Service {name} started with PID {process.pid}")
            
            # Wait for port to be available if specified
            if wait_for_port:
                self.wait_for_port(name, wait_for_port)
            
            return process
        except Exception as e:
            self.log(f"Error starting service {name}: {e}")
            if log_redirect:
                log_redirect.close()
            return None
    
    def wait_for_port(self, service_name, port, timeout=30):
        """Wait for a port to be available."""
        import socket
        
        self.log(f"Waiting for {service_name} to be available on port {port}...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                socket.create_connection(("localhost", port), timeout=1)
                self.log(f"{service_name} is available on port {port}")
                return True
            except (socket.timeout, ConnectionRefusedError):
                time.sleep(1)
        
        self.log(f"Timed out waiting for {service_name} on port {port}")
        return False
    
    def monitor_services(self):
        """Monitor running services and restart them if they crash."""
        while self.running:
            for name, service in list(self.services.items()):
                process = service["process"]
                returncode = process.poll()
                
                if returncode is not None:
                    self.log(f"Service {name} exited with code {returncode}")
                    
                    # Don't restart services that exited cleanly
                    if returncode != 0:
                        self.log(f"Restarting service {name}...")
                        
                        # Start the service with the same parameters
                        self.start_service(
                            name,
                            service["command"],
                            service["log_file"],
                            service["wait_for_port"]
                        )
            
            time.sleep(5)
    
    def start_monitoring(self):
        """Start the service monitoring thread."""
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_services)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop the service monitoring thread."""
        self.running = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=2)
    
    def start_all_services(self, entity_name="Default"):
        """Start all Genesis Stack services."""
        self.log("Starting Genesis Stack services...")
        
        # Start License API
        self.start_service(
            "License API",
            ["python", "run_license_api.py"],
            log_file="logs/license_api.log",
            wait_for_port=5001
        )
        
        # Start License Management
        self.start_service(
            "License Management",
            ["python", "run_license_management.py"],
            log_file="logs/license_management.log",
            wait_for_port=8505
        )
        
        # Start Welcome Server
        self.start_service(
            "Welcome Server",
            ["python", "web_server.py", "--entity", entity_name],
            log_file="logs/welcome_server.log",
            wait_for_port=8090
        )
        
        # Start monitoring thread
        self.start_monitoring()
        
        # Return to the caller to allow interaction
        self.log("All services started. Central Station is now monitoring.")
    
    def stop_all_services(self):
        """Stop all running services."""
        self.log("Stopping all services...")
        
        # Stop monitoring first
        self.stop_monitoring()
        
        # Stop each service
        for name, service in list(self.services.items()):
            self.log(f"Stopping {name}...")
            process = service["process"]
            
            try:
                process.terminate()
                process.wait(timeout=5)
                self.log(f"{name} stopped.")
            except subprocess.TimeoutExpired:
                self.log(f"{name} did not terminate gracefully, killing...")
                process.kill()
            except Exception as e:
                self.log(f"Error stopping {name}: {e}")
            
            # Close log file if it's open
            log_file = service.get("log_file")
            if log_file and hasattr(process, "stdout") and process.stdout:
                process.stdout.close()
            
            del self.services[name]
        
        self.log("All services stopped.")
    
    def run_genesis_shell(self):
        """Run the Genesis Shell terminal interface."""
        self.log("Starting Genesis Shell Terminal...")
        
        try:
            # Run the terminal-based shell
            subprocess.run(["python", "run_genesis_shell_terminal.py"])
        except KeyboardInterrupt:
            self.log("Genesis Shell Terminal closed.")
        except Exception as e:
            self.log(f"Error running Genesis Shell Terminal: {e}")
    
    def show_status(self):
        """Show the status of all running services."""
        self.log("=== Genesis Stack Service Status ===")
        
        if not self.services:
            self.log("No services are currently running.")
            return
        
        for name, service in self.services.items():
            process = service["process"]
            returncode = process.poll()
            
            if returncode is None:
                status = "RUNNING"
                runtime = datetime.now() - service["start_time"]
                runtime_str = str(runtime).split('.')[0]  # Remove microseconds
            else:
                status = f"EXITED ({returncode})"
                runtime_str = "N/A"
            
            self.log(f"{name}: {status}, PID: {process.pid}, Uptime: {runtime_str}")
        
        self.log("================================")

def main():
    """Main function to run the Central Station."""
    parser = argparse.ArgumentParser(
        description='Central Station - Genesis Stack Coordination System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Central Station manages the Genesis Stack services and provides a unified interface
for controlling the distributed Genesis ecosystem.

Example usage:
  python run_central_station.py --entity MyOrganization
  python run_central_station.py --shell-only
  python run_central_station.py --status
"""
    )
    
    parser.add_argument(
        '--entity',
        default="Default",
        help='Entity name for configuration (default: Default)'
    )
    
    parser.add_argument(
        '--shell-only',
        action='store_true',
        help='Run only the Genesis Shell terminal interface'
    )
    
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show status of running services and exit'
    )
    
    args = parser.parse_args()
    
    # Create Central Station
    station = CentralStation()
    
    # Register signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        print("\nShutting down Central Station...")
        station.stop_all_services()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        if args.status:
            # Show status and exit
            station.show_status()
        elif args.shell_only:
            # Run only the Genesis Shell
            station.run_genesis_shell()
        else:
            # Start all services
            station.start_all_services(args.entity)
            
            # Run the Genesis Shell terminal
            station.run_genesis_shell()
    except KeyboardInterrupt:
        print("\nShutting down Central Station...")
    finally:
        station.stop_all_services()

if __name__ == "__main__":
    main()
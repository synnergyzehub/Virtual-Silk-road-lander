#!/usr/bin/env python3
"""
Genesis Stack - Entity Services Launcher

This script launches all services for a specific entity in the Genesis Stack.
It reads the configuration from the entity's config directory and starts
the License API, License Management Interface, and Welcome Page Server.
"""

import os
import json
import argparse
import subprocess
import time
import signal
import sys

def load_entity_config(entity_name):
    """Load configuration for an entity."""
    entity_dir_name = entity_name.lower().replace(' ', '-')
    entity_config_dir = os.path.join('config', entity_dir_name)
    
    if not os.path.exists(entity_config_dir):
        print(f"Error: Configuration for entity '{entity_name}' not found.")
        print(f"Expected directory: {entity_config_dir}")
        return None
    
    # Load ports configuration
    ports_file = os.path.join(entity_config_dir, 'ports.json')
    if not os.path.exists(ports_file):
        print(f"Error: Ports configuration for entity '{entity_name}' not found.")
        print(f"Expected file: {ports_file}")
        return None
    
    try:
        with open(ports_file, 'r') as f:
            ports = json.load(f)
    except Exception as e:
        print(f"Error loading ports configuration: {e}")
        return None
    
    # Load API configuration
    api_file = os.path.join(entity_config_dir, 'api.json')
    if not os.path.exists(api_file):
        print(f"Error: API configuration for entity '{entity_name}' not found.")
        print(f"Expected file: {api_file}")
        return None
    
    try:
        with open(api_file, 'r') as f:
            api_config = json.load(f)
    except Exception as e:
        print(f"Error loading API configuration: {e}")
        return None
    
    # Load entity metadata
    entity_file = os.path.join(entity_config_dir, 'entity.json')
    if os.path.exists(entity_file):
        try:
            with open(entity_file, 'r') as f:
                entity_metadata = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load entity metadata: {e}")
            entity_metadata = {}
    else:
        entity_metadata = {}
    
    return {
        "entity_name": entity_name,
        "entity_dir_name": entity_dir_name,
        "config_dir": entity_config_dir,
        "ports": ports,
        "api_key": api_config.get("api_key"),
        "api_base_url": api_config.get("api_base_url"),
        "jwt_secret": api_config.get("jwt_secret"),
        "entity_metadata": entity_metadata
    }

def launch_services(entity_config, services=None):
    """Launch services for an entity."""
    if not entity_config:
        return False
    
    # Set environment variables
    os.environ["ENTITY_CONFIG_DIR"] = entity_config["entity_dir_name"]
    os.environ["EMPIRE_API_KEY"] = entity_config["api_key"]
    os.environ["JWT_SECRET"] = entity_config["jwt_secret"]
    
    # Create logs directory
    entity_logs_dir = os.path.join('logs', entity_config["entity_dir_name"])
    os.makedirs(entity_logs_dir, exist_ok=True)
    
    # Determine which services to launch
    if not services:
        services = ["license_api", "license_management", "welcome_page"]
    
    processes = []
    
    try:
        # Launch License API
        if "license_api" in services:
            license_api_port = entity_config["ports"]["license_api_port"]
            print(f"Starting License API on port {license_api_port}...")
            
            license_api_log = open(os.path.join(entity_logs_dir, 'license_api.log'), 'w')
            license_api_cmd = ["python", "run_license_api.py", "--port", str(license_api_port)]
            
            license_api_process = subprocess.Popen(
                license_api_cmd,
                stdout=license_api_log,
                stderr=license_api_log,
                env=os.environ
            )
            processes.append((license_api_process, license_api_log, "License API"))
            
            # Wait for License API to start
            print("Waiting for License API to start...")
            time.sleep(3)
        
        # Launch License Management Interface
        if "license_management" in services:
            license_management_port = entity_config["ports"]["license_management_port"]
            print(f"Starting License Management Interface on port {license_management_port}...")
            
            license_management_log = open(os.path.join(entity_logs_dir, 'license_management.log'), 'w')
            license_management_cmd = [
                "python", "run_license_management.py", 
                "--port", str(license_management_port),
                "--api-url", entity_config["api_base_url"]
            ]
            
            license_management_process = subprocess.Popen(
                license_management_cmd,
                stdout=license_management_log,
                stderr=license_management_log,
                env=os.environ
            )
            processes.append((license_management_process, license_management_log, "License Management"))
        
        # Launch Welcome Page Server
        if "welcome_page" in services:
            welcome_page_port = entity_config["ports"]["welcome_page_port"]
            print(f"Starting Welcome Page Server on port {welcome_page_port}...")
            
            welcome_page_log = open(os.path.join(entity_logs_dir, 'welcome_page.log'), 'w')
            welcome_page_cmd = ["python", "web_server.py", "--port", str(welcome_page_port)]
            
            welcome_page_process = subprocess.Popen(
                welcome_page_cmd,
                stdout=welcome_page_log,
                stderr=welcome_page_log,
                env=os.environ
            )
            processes.append((welcome_page_process, welcome_page_log, "Welcome Page"))
        
        # Wait for all processes to start
        print("All services started. Press Ctrl+C to stop.")
        
        # Print service URLs
        print("\nService URLs:")
        if "license_api" in services:
            print(f"License API: http://localhost:{entity_config['ports']['license_api_port']}")
        if "license_management" in services:
            print(f"License Management: http://localhost:{entity_config['ports']['license_management_port']}")
        if "welcome_page" in services:
            print(f"Welcome Page: http://localhost:{entity_config['ports']['welcome_page_port']}")
        
        # Keep running until interrupted
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\nStopping services...")
    finally:
        # Terminate all processes
        for process, log_file, service_name in processes:
            print(f"Stopping {service_name}...")
            process.terminate()
            log_file.close()
        
        # Wait for processes to terminate
        for process, _, service_name in processes:
            process.wait()
            print(f"{service_name} stopped.")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Launch services for an entity in the Genesis Stack.')
    parser.add_argument('entity_name', help='Name of the entity')
    parser.add_argument('--services', nargs='+', choices=['license_api', 'license_management', 'welcome_page'],
                       help='Services to launch (default: all)')
    
    args = parser.parse_args()
    
    entity_config = load_entity_config(args.entity_name)
    if entity_config:
        launch_services(entity_config, args.services)
    else:
        print(f"Failed to load configuration for entity '{args.entity_name}'.")
        sys.exit(1)

if __name__ == '__main__':
    main()
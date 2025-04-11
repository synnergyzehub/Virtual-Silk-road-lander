#!/usr/bin/env python3
"""
Run the License Management Interface with configuration support for multi-entity deployment.
"""

import os
import sys
import json
import argparse
import subprocess

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
    
    return {
        "entity_name": entity_name,
        "entity_dir_name": entity_dir_name,
        "config_dir": entity_config_dir,
        "port": ports.get("license_management_port", 8505),
        "api_key": api_config.get("api_key"),
        "api_base_url": api_config.get("api_base_url", "http://localhost:5001")
    }

def main():
    parser = argparse.ArgumentParser(description='Run the License Management Interface.')
    parser.add_argument('--port', type=int, help='Port to run the interface on (default: 8505 or from config)')
    parser.add_argument('--api-url', help='URL of the License API (default: http://localhost:5001 or from config)')
    parser.add_argument('--entity', help='Entity name to load configuration for')
    
    args = parser.parse_args()
    
    # Default values
    api_key = os.getenv('EMPIRE_API_KEY', 'emperorkey123')
    port = 8505
    api_url = "http://localhost:5001"
    
    # If entity is specified, load configuration
    if args.entity:
        entity_config = load_entity_config(args.entity)
        if entity_config:
            port = entity_config["port"]
            api_key = entity_config["api_key"]
            api_url = entity_config["api_base_url"]
    
    # Override with command line arguments if provided
    if args.port:
        port = args.port
    if args.api_url:
        api_url = args.api_url
    
    # Export environment variables
    os.environ['EMPIRE_API_KEY'] = api_key
    os.environ['API_BASE_URL'] = api_url
    
    print(f"Starting License Management Interface on port {port}...")
    
    # Run the streamlit app
    try:
        result = subprocess.run([
            "streamlit", "run", "license_management.py",
            "--server.port", str(port),
            "--server.address", "0.0.0.0",
            "--server.headless", "true"
        ], env=os.environ)
        if result.returncode != 0:
            print(f"Error running License Management Interface: {result.returncode}")
            sys.exit(result.returncode)
    except Exception as e:
        print(f"Error running License Management Interface: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
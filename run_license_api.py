#!/usr/bin/env python3
"""
Run the Secure Empire License API with configuration support for multi-entity deployment.
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
        "port": ports.get("license_api_port", 5001),
        "api_key": api_config.get("api_key")
    }

def main():
    parser = argparse.ArgumentParser(description='Run the Secure Empire License API.')
    parser.add_argument('--port', type=int, help='Port to run the API on (default: 5001 or from config)')
    parser.add_argument('--entity', help='Entity name to load configuration for')
    
    args = parser.parse_args()
    
    # Default API key
    api_key = os.getenv('EMPIRE_API_KEY', 'emperorkey123')
    port = 5001
    
    # If entity is specified, load configuration
    if args.entity:
        entity_config = load_entity_config(args.entity)
        if entity_config:
            port = entity_config["port"]
            api_key = entity_config["api_key"]
    
    # Override with command line arguments if provided
    if args.port:
        port = args.port
    
    # Export API key as environment variable
    os.environ['EMPIRE_API_KEY'] = api_key
    
    print(f"Starting Secure Empire License API on port {port}...")
    
    # Run the secure_empire_license_api.py script
    try:
        result = subprocess.run(
            ["python", "secure_empire_license_api.py", "--port", str(port)],
            env=os.environ
        )
        if result.returncode != 0:
            print(f"Error running Secure Empire License API: {result.returncode}")
            sys.exit(result.returncode)
    except Exception as e:
        print(f"Error running Secure Empire License API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
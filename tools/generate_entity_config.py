#!/usr/bin/env python3
"""
Genesis Stack - Entity Configuration Generator

This script generates configuration files for a new entity in the Genesis Stack.
It creates the necessary directory structure and configuration files based on templates.
"""

import os
import json
import argparse
import secrets
import shutil
from datetime import datetime

def generate_entity_id(entity_name, prefix="ENT"):
    """Generate a unique entity ID based on the entity name."""
    timestamp = datetime.now().strftime("%y%m%d")
    # Take first 4 characters of entity name (uppercase)
    name_part = ''.join(c for c in entity_name if c.isalnum())[:4].upper()
    return f"{prefix}-{name_part}-{timestamp}"

def generate_api_key():
    """Generate a secure API key."""
    return secrets.token_urlsafe(32)

def generate_jwt_secret():
    """Generate a secure JWT secret."""
    return secrets.token_urlsafe(32)

def sanitize_db_name(name):
    """Sanitize a name for use as a database name."""
    return 'empireos_' + ''.join(c.lower() for c in name if c.isalnum() or c == '_')

def assign_ports(entity_number):
    """Assign ports based on entity number."""
    return {
        "license_api_port": 5100 + entity_number,
        "brand_portal_port": 5100 + entity_number - 1,
        "license_management_port": 8600 + entity_number,
        "welcome_page_port": 8100 + entity_number,
        "digitalme_console_port": 8100 + entity_number + 5
    }

def create_entity_config(entity_name, entity_number, entity_id=None):
    """Create configuration files for a new entity."""
    # Create entity directory if it doesn't exist
    entity_dir_name = entity_name.lower().replace(' ', '-')
    entity_config_dir = os.path.join('config', entity_dir_name)
    os.makedirs(entity_config_dir, exist_ok=True)
    
    # Generate entity ID if not provided
    if not entity_id:
        entity_id = generate_entity_id(entity_name)
    
    # Generate API key and JWT secret
    api_key = generate_api_key()
    jwt_secret = generate_jwt_secret()
    
    # Sanitize database name
    db_name = sanitize_db_name(entity_name)
    
    # Assign ports
    ports = assign_ports(entity_number)
    
    # Create ports.json
    with open(os.path.join(entity_config_dir, 'ports.json'), 'w') as f:
        json.dump(ports, f, indent=2)
    
    # Create database.json
    db_config = {
        "database_name": db_name,
        "database_user": "empireos_user",
        "database_password": "secure_password",
        "database_host": "localhost",
        "database_port": 3306,
        "connection_string": f"mysql://empireos_user:secure_password@localhost:3306/{db_name}"
    }
    with open(os.path.join(entity_config_dir, 'database.json'), 'w') as f:
        json.dump(db_config, f, indent=2)
    
    # Create api.json
    api_config = {
        "api_key": api_key,
        "api_base_url": f"http://localhost:{ports['license_api_port']}",
        "api_timeout": 30,
        "api_retry_attempts": 3,
        "jwt_secret": jwt_secret,
        "jwt_expiry": 86400
    }
    with open(os.path.join(entity_config_dir, 'api.json'), 'w') as f:
        json.dump(api_config, f, indent=2)
    
    # Create entity.json with metadata
    entity_config = {
        "entity_id": entity_id,
        "entity_name": entity_name,
        "created_at": datetime.now().isoformat(),
        "config_version": "1.0",
        "subway_line": entity_number
    }
    with open(os.path.join(entity_config_dir, 'entity.json'), 'w') as f:
        json.dump(entity_config, f, indent=2)
    
    # Create data directory for entity
    entity_data_dir = os.path.join('data', entity_dir_name)
    os.makedirs(entity_data_dir, exist_ok=True)
    
    # Create logs directory for entity
    entity_logs_dir = os.path.join('logs', entity_dir_name)
    os.makedirs(entity_logs_dir, exist_ok=True)
    
    # Generate Certificate of Sovereignty
    cert_content = f"""
                           Certificate of Genesis Sovereignty

This certifies that {entity_name} has been officially onboarded to the Genesis Stack,
registered, and archived under sovereign digital governance.

Issued To: {entity_id}
Entity Name: {entity_name}
Date of Origin: {datetime.now().isoformat()}

Service Endpoints:
- License API: http://localhost:{ports['license_api_port']}
- Brand Portal: http://localhost:{ports['brand_portal_port']}
- License Management: http://localhost:{ports['license_management_port']}
- Welcome Page: http://localhost:{ports['welcome_page_port']}
- DigitalMe Console: http://localhost:{ports['digitalme_console_port']}

API Key: {api_key[:8]}************************

This certificate shall serve as a record of trust, governance, and origin, as recorded in the DigitalMe
Ledger Registry and enforced under ECG oversight.

                        Signed digitally by DigitalMe System | Empire Sovereign Console
"""
    
    with open(os.path.join(entity_data_dir, f"{entity_dir_name}_certificate.txt"), 'w') as f:
        f.write(cert_content)
    
    # Create a readme file with instructions
    readme_content = f"""
# {entity_name} - Genesis Stack Configuration

This directory contains configuration files for the {entity_name} entity in the Genesis Stack.

## Service Endpoints

- License API: http://localhost:{ports['license_api_port']}
- Brand Portal: http://localhost:{ports['brand_portal_port']}
- License Management: http://localhost:{ports['license_management_port']}
- Welcome Page: http://localhost:{ports['welcome_page_port']}
- DigitalMe Console: http://localhost:{ports['digitalme_console_port']}

## Configuration Files

- `ports.json`: Port configuration for services
- `database.json`: Database connection configuration
- `api.json`: API configuration including keys and secrets
- `entity.json`: Entity metadata

## Environment Variables

To use this configuration, set the following environment variables:

```bash
export ENTITY_CONFIG_DIR={entity_dir_name}
export EMPIRE_API_KEY={api_key}
export JWT_SECRET={jwt_secret}
```

## Starting Services

To start services for this entity, use:

```bash
python run_license_api.py --config config/{entity_dir_name}/config.json
python run_license_management.py --config config/{entity_dir_name}/config.json
python web_server.py --config config/{entity_dir_name}/config.json
```
"""
    
    with open(os.path.join(entity_config_dir, 'README.md'), 'w') as f:
        f.write(readme_content)
    
    print(f"Entity configuration for '{entity_name}' created successfully!")
    print(f"Entity ID: {entity_id}")
    print(f"Configuration directory: {entity_config_dir}")
    print(f"API Key: {api_key}")
    print(f"JWT Secret: {jwt_secret}")
    print("\nView the README.md file in the configuration directory for more information.")
    
    return {
        "entity_id": entity_id,
        "entity_name": entity_name,
        "config_dir": entity_config_dir,
        "ports": ports,
        "api_key": api_key
    }

def update_service_discovery(entity_info):
    """Update the service discovery file with the new entity."""
    service_discovery_file = 'config/service_discovery.json'
    
    # Create default service discovery if it doesn't exist
    if not os.path.exists(service_discovery_file):
        service_discovery = {"entity_registry": []}
    else:
        try:
            with open(service_discovery_file, 'r') as f:
                service_discovery = json.load(f)
        except:
            service_discovery = {"entity_registry": []}
    
    # Add the new entity to the registry
    entity_entry = {
        "id": entity_info["entity_id"],
        "name": entity_info["entity_name"],
        "license_api_url": f"http://localhost:{entity_info['ports']['license_api_port']}",
        "brand_portal_url": f"http://localhost:{entity_info['ports']['brand_portal_port']}",
        "license_management_url": f"http://localhost:{entity_info['ports']['license_management_port']}",
        "welcome_page_url": f"http://localhost:{entity_info['ports']['welcome_page_port']}",
        "digitalme_console_url": f"http://localhost:{entity_info['ports']['digitalme_console_port']}"
    }
    
    # Check if entity already exists
    for i, entity in enumerate(service_discovery["entity_registry"]):
        if entity["id"] == entity_info["entity_id"]:
            service_discovery["entity_registry"][i] = entity_entry
            break
    else:
        service_discovery["entity_registry"].append(entity_entry)
    
    # Save the updated service discovery
    os.makedirs(os.path.dirname(service_discovery_file), exist_ok=True)
    with open(service_discovery_file, 'w') as f:
        json.dump(service_discovery, f, indent=2)
    
    print(f"Service discovery updated with entity '{entity_info['entity_name']}'")

def main():
    parser = argparse.ArgumentParser(description='Generate configuration for a new entity in the Genesis Stack.')
    parser.add_argument('entity_name', help='Name of the entity')
    parser.add_argument('--entity-number', type=int, help='Entity number for port assignment (default: auto-increment)')
    parser.add_argument('--entity-id', help='Entity ID (default: auto-generated)')
    
    args = parser.parse_args()
    
    # Determine entity number if not provided
    if not args.entity_number:
        # Count existing entity directories
        existing_count = len([d for d in os.listdir('config') if os.path.isdir(os.path.join('config', d)) and d not in ['default', 'entity-template']])
        args.entity_number = existing_count + 1
    
    entity_info = create_entity_config(args.entity_name, args.entity_number, args.entity_id)
    update_service_discovery(entity_info)

if __name__ == '__main__':
    main()
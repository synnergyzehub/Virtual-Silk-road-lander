#!/usr/bin/env python3
"""
SynergyzeOS - License Generation Tool

This script generates a SynergyzeOS license for entities and assigns it to an NPU node.
SynergyzeOS licenses define the operational parameters and capabilities allowed
for entities running on the Genesis Stack.
"""

import os
import sys
import json
import argparse
import secrets
import hashlib
from datetime import datetime, timedelta

def load_entity_config(entity_name, config_dir="config"):
    """Load the configuration for an entity."""
    entity_dir_name = entity_name.lower().replace(' ', '-')
    entity_config_dir = os.path.join(config_dir, entity_dir_name)
    
    if not os.path.exists(entity_config_dir):
        print(f"Error: Configuration for entity '{entity_name}' not found.")
        print(f"Expected directory: {entity_config_dir}")
        return None
    
    # Load entity.json if it exists
    entity_file = os.path.join(entity_config_dir, 'entity.json')
    if os.path.exists(entity_file):
        try:
            with open(entity_file, 'r') as f:
                entity_config = json.load(f)
            return {
                "entity_name": entity_name,
                "entity_dir_name": entity_dir_name,
                "config_dir": entity_config_dir,
                "entity_id": entity_config.get("entity_id", f"ENT-{entity_name[:4].upper()}")
            }
        except Exception as e:
            print(f"Warning: Could not load entity metadata: {e}")
    
    # If entity.json doesn't exist, create minimal config
    return {
        "entity_name": entity_name,
        "entity_dir_name": entity_dir_name,
        "config_dir": entity_config_dir,
        "entity_id": f"ENT-{entity_name[:4].upper()}"
    }

def generate_license_id(entity_info):
    """Generate a unique license ID for the entity."""
    timestamp = datetime.now().strftime("%y%m%d")
    entity_part = entity_info["entity_id"]
    return f"SYN-{entity_part}-{timestamp}"

def generate_license_key():
    """Generate a secure license key."""
    return f"synos-{secrets.token_urlsafe(16)}"

def parse_modules(modules):
    """Parse the modules string into a list."""
    if isinstance(modules, str):
        module_list = [m.strip() for m in modules.split(",")]
    else:
        module_list = modules
    return module_list

def calculate_term_dates(term):
    """Calculate the start and end dates for the license term."""
    start_date = datetime.now()
    
    if isinstance(term, int) or term.isdigit():
        # If term is a number, interpret as days
        days = int(term)
        end_date = start_date + timedelta(days=days)
    elif term.lower() == "perpetual":
        # If term is perpetual, set end date to far future
        end_date = start_date + timedelta(days=36500)  # ~100 years
    elif term.lower() == "annual":
        # If term is annual, set end date to 1 year from now
        end_date = start_date + timedelta(days=365)
    elif term.lower() == "monthly":
        # If term is monthly, set end date to 30 days from now
        end_date = start_date + timedelta(days=30)
    elif term.lower() == "trial":
        # If term is trial, set end date to 14 days from now
        end_date = start_date + timedelta(days=14)
    else:
        # Default to 30 days
        end_date = start_date + timedelta(days=30)
    
    return {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat()
    }

def create_license(entity_info, modules, term, jurisdiction=None, license_dir="data/licenses"):
    """Create a SynergyzeOS license for an entity."""
    # Create license directory if it doesn't exist
    os.makedirs(license_dir, exist_ok=True)
    
    # Generate license ID and key
    license_id = generate_license_id(entity_info)
    license_key = generate_license_key()
    
    # Parse modules
    module_list = parse_modules(modules)
    
    # Calculate term dates
    term_dates = calculate_term_dates(term)
    
    # Determine jurisdiction
    if not jurisdiction:
        # Default to global jurisdiction
        jurisdiction = "GLOBAL"
    
    # Create license
    license_data = {
        "license_id": license_id,
        "license_key": license_key,
        "entity_id": entity_info["entity_id"],
        "entity_name": entity_info["entity_name"],
        "created_at": datetime.now().isoformat(),
        "issuer": "SynergyzeOS",
        "terms": {
            "start_date": term_dates["start_date"],
            "end_date": term_dates["end_date"],
            "auto_renew": False
        },
        "modules": module_list,
        "jurisdiction": jurisdiction,
        "status": "active",
        "features": {
            "divine_alignment": True,
            "computational_governance": True,
            "jurisdictional_compliance": True,
            "ethical_oversight": True
        },
        "limits": {
            "max_entities": 5,
            "max_users": 100,
            "max_transactions_per_day": 10000,
            "max_storage_gb": 250
        }
    }
    
    # Add module-specific configurations
    module_configs = {}
    
    for module in module_list:
        if module.lower() == "commerce":
            module_configs["commerce"] = {
                "payment_processing": True,
                "inventory_management": True,
                "order_fulfillment": True,
                "ethical_commerce_filter": True
            }
        elif module.lower() == "governance":
            module_configs["governance"] = {
                "multi_level_approval": True,
                "audit_trail": True,
                "compliance_reporting": True,
                "risk_assessment": True
            }
        elif module.lower() == "identity":
            module_configs["identity"] = {
                "federated_authentication": True,
                "role_based_access": True,
                "attribute_verification": True,
                "sovereign_identity": True
            }
        elif module.lower() == "manufacturing":
            module_configs["manufacturing"] = {
                "supply_chain_tracking": True,
                "quality_assurance": True,
                "inventory_optimization": True,
                "ethical_sourcing": True
            }
    
    license_data["module_configs"] = module_configs
    
    # Save license
    license_path = os.path.join(license_dir, f"{license_id}.json")
    with open(license_path, 'w') as f:
        json.dump(license_data, f, indent=2)
    
    # Generate license certificate
    cert_content = f"""
                     SynergyzeOS License Certificate

This certifies that {entity_info['entity_name']} has been granted a SynergyzeOS license
for use with the Genesis Stack.

License ID: {license_id}
License Key: {license_key}
Entity ID: {entity_info['entity_id']}
Entity Name: {entity_info['entity_name']}
Issue Date: {datetime.now().isoformat()}
Valid From: {term_dates['start_date']}
Valid To: {term_dates['end_date']}

Authorized Modules:
{', '.join(module_list)}

Jurisdiction: {jurisdiction}

This license enables the operation of Genesis Stack entities through the SynergyzeOS
platform with computational governance and divine alignment capabilities.

                   Signed digitally by SynergyzeOS | Empire Sovereign Console
"""
    
    cert_path = os.path.join(license_dir, f"{license_id}_certificate.txt")
    with open(cert_path, 'w') as f:
        f.write(cert_content)
    
    return {
        "license_id": license_id,
        "license_key": license_key,
        "license_path": license_path,
        "cert_path": cert_path,
        "license_data": license_data
    }

def register_license_with_synadmin(license_info, synadmin_dir="data/synadmin_registrations"):
    """Register the license with SynAdmin Cloud Portal."""
    # In a real implementation, this would make an API call to the SynAdmin Cloud Portal
    # For this example, we'll just create a local registration record
    
    os.makedirs(synadmin_dir, exist_ok=True)
    
    registration = {
        "license_id": license_info["license_id"],
        "entity_id": license_info["license_data"]["entity_id"],
        "entity_name": license_info["license_data"]["entity_name"],
        "registration_time": datetime.now().isoformat(),
        "status": "active",
        "verification_url": f"https://synadmin.empireos.cloud/license/verify/{license_info['license_id']}"
    }
    
    reg_path = os.path.join(synadmin_dir, f"{license_info['license_id']}_registration.json")
    with open(reg_path, 'w') as f:
        json.dump(registration, f, indent=2)
    
    print(f"License registered with SynAdmin Cloud Portal: {reg_path}")
    return registration

def main():
    """Main function to run the SynergyzeOS license generation script."""
    parser = argparse.ArgumentParser(description='Generate a SynergyzeOS license for an entity.')
    parser.add_argument('--entity', required=True, help='Name of the entity')
    parser.add_argument('--modules', required=True, help='Comma-separated list of modules to include in the license')
    parser.add_argument('--term', default="annual", help='License term (days or "perpetual", "annual", "monthly", "trial")')
    parser.add_argument('--jurisdiction', help='Jurisdiction for the license (default: GLOBAL)')
    
    args = parser.parse_args()
    
    # Load entity configuration
    entity_info = load_entity_config(args.entity)
    if not entity_info:
        print(f"Error: Could not load configuration for entity '{args.entity}'.")
        sys.exit(1)
    
    print(f"Generating SynergyzeOS license for {args.entity}...")
    
    # Create license
    license_info = create_license(entity_info, args.modules, args.term, args.jurisdiction)
    
    # Register with SynAdmin
    register_license_with_synadmin(license_info)
    
    print("\nSynergyzeOS License Generation Complete!")
    print(f"License ID: {license_info['license_id']}")
    print(f"License Key: {license_info['license_key']}")
    print(f"Entity: {entity_info['entity_name']} ({entity_info['entity_id']})")
    print(f"Term: {args.term}")
    print(f"Modules: {', '.join(parse_modules(args.modules))}")
    print(f"License File: {license_info['license_path']}")
    print(f"Certificate: {license_info['cert_path']}")
    print("\nNext steps:")
    print(f"1. Assign the license to an NPU node: python tools/assign_license_to_npu.py --license \"{license_info['license_id']}\" --node-id \"NPU-XXXX\"")
    print(f"2. Verify the license: python tools/verify_license.py --license \"{license_info['license_id']}\"")

if __name__ == "__main__":
    main()
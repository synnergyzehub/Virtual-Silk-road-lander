#!/usr/bin/env python3
"""
SynergyzeOS - NPU Node Registration Tool

This script registers a new Neural Processing Unit (NPU) node with the SynAdmin Cloud Portal.
The NPU node serves as the hardware component for running the computational governance rules
and license validation for Genesis Stack entities.
"""

import os
import sys
import json
import argparse
import secrets
import hashlib
from datetime import datetime

def generate_npu_hash(node_id, region):
    """Generate a unique hash for the NPU node."""
    seed = f"{node_id}:{region}:{datetime.now().isoformat()}"
    return hashlib.sha256(seed.encode()).hexdigest()

def create_npu_node_config(node_id, region, entities, output_dir="data/npu_nodes"):
    """Create configuration files for a new NPU node."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate unique node hash
    node_hash = generate_npu_hash(node_id, region)
    
    # Generate node API key
    node_api_key = secrets.token_urlsafe(32)
    
    # Parse entities list
    if isinstance(entities, str):
        entity_list = [e.strip() for e in entities.split(",")]
    else:
        entity_list = entities
    
    # Create node configuration
    node_config = {
        "node_id": node_id,
        "node_hash": node_hash,
        "region": region,
        "created_at": datetime.now().isoformat(),
        "api_key": node_api_key,
        "entities": entity_list,
        "status": "initialized",
        "capabilities": [
            "license_validation",
            "divine_alignment",
            "computational_governance",
            "ethical_oversight"
        ],
        "hardware_specs": {
            "npu_cores": 16,
            "memory": "64GB",
            "storage": "1TB",
            "architecture": "Genesis NPU v1.0"
        }
    }
    
    # Save node configuration
    config_path = os.path.join(output_dir, f"{node_id}.json")
    with open(config_path, 'w') as f:
        json.dump(node_config, f, indent=2)
    
    return {
        "node_id": node_id,
        "node_hash": node_hash,
        "config_path": config_path,
        "api_key": node_api_key
    }

def register_node_with_synadmin(node_info, synadmin_url=None):
    """Register the NPU node with SynAdmin Cloud Portal."""
    # In a real implementation, this would make an API call to the SynAdmin Cloud Portal
    # For this example, we'll just simulate the registration
    
    print(f"Registering NPU node {node_info['node_id']} with SynAdmin Cloud Portal...")
    print(f"Node Hash: {node_info['node_hash']}")
    
    # Create registration record
    registration = {
        "node_id": node_info["node_id"],
        "node_hash": node_info["node_hash"],
        "registration_time": datetime.now().isoformat(),
        "synadmin_url": synadmin_url or "https://synadmin.empireos.cloud"
    }
    
    # Save registration record
    reg_dir = "data/synadmin_registrations"
    os.makedirs(reg_dir, exist_ok=True)
    
    reg_path = os.path.join(reg_dir, f"{node_info['node_id']}_registration.json")
    with open(reg_path, 'w') as f:
        json.dump(registration, f, indent=2)
    
    print(f"Registration complete. Record saved to {reg_path}")
    return registration

def generate_certificate(node_info, output_dir="data/npu_certificates"):
    """Generate a certificate for the NPU node."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create certificate content
    cert_content = f"""
                     SynergyzeOS NPU Node Certificate

This certifies that NPU Node {node_info['node_id']} has been officially registered with the 
SynAdmin Cloud Portal and is authorized to perform computational governance operations 
for the Genesis Stack.

Node ID: {node_info['node_id']}
Node Hash: {node_info['node_hash']}
Region: {node_info.get('region', 'Unknown')}
Registration Date: {datetime.now().isoformat()}

API Key: {node_info['api_key'][:8]}************************

This certificate shall serve as a record of trust, governance, and origin, as recorded in the
SynAdmin registry and enforced under ECG oversight.

                   Signed digitally by SynAdmin | Empire Sovereign Console
"""
    
    # Save certificate
    cert_path = os.path.join(output_dir, f"{node_info['node_id']}_certificate.txt")
    with open(cert_path, 'w') as f:
        f.write(cert_content)
    
    print(f"Certificate generated and saved to {cert_path}")
    return cert_path

def main():
    """Main function to run the NPU node registration script."""
    parser = argparse.ArgumentParser(description='Register a new NPU node with SynAdmin Cloud Portal.')
    parser.add_argument('--node-id', required=True, help='Unique identifier for the NPU node (e.g., NPU-0001)')
    parser.add_argument('--region', required=True, help='Region code where the NPU node is deployed (e.g., IND-KA)')
    parser.add_argument('--entities', required=True, help='Comma-separated list of entities to be managed by this NPU node')
    parser.add_argument('--synadmin-url', help='URL of the SynAdmin Cloud Portal (optional)')
    
    args = parser.parse_args()
    
    # Create NPU node configuration
    node_info = create_npu_node_config(args.node_id, args.region, args.entities)
    
    # Register with SynAdmin
    registration = register_node_with_synadmin(node_info, args.synadmin_url)
    
    # Generate certificate
    cert_path = generate_certificate(node_info)
    
    print("\nNPU Node Registration Complete!")
    print(f"Node ID: {node_info['node_id']}")
    print(f"Node Hash: {node_info['node_hash']}")
    print(f"API Key: {node_info['api_key'][:8]}************************")
    print(f"Configuration: {node_info['config_path']}")
    print(f"Certificate: {cert_path}")
    print("\nNext steps:")
    print(f"1. Initialize NPU governance rules: python tools/init_npu_governance.py --node-id \"{node_info['node_id']}\" --ecg-key \"$ECG_KEY\"")
    print(f"2. Assign entities to the NPU node: python tools/assign_entities_to_npu.py --node-id \"{node_info['node_id']}\" --entities \"ENTITY1,ENTITY2\"")
    print(f"3. Configure SynergyzeOS license for the NPU node: python tools/config_synergyze_license.py --node-id \"{node_info['node_id']}\"")

if __name__ == "__main__":
    main()
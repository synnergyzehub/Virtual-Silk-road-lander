#!/usr/bin/env python3
"""
SynergyzeOS - License Assignment Tool

This script assigns a SynergyzeOS license to an NPU node, enabling the node to provide
computational governance services for the licensed entities.
"""

import os
import sys
import json
import argparse
from datetime import datetime

def load_license(license_id, license_dir="data/licenses"):
    """Load a SynergyzeOS license."""
    license_path = os.path.join(license_dir, f"{license_id}.json")
    
    if not os.path.exists(license_path):
        print(f"Error: License '{license_id}' not found.")
        print(f"Expected file: {license_path}")
        return None
    
    try:
        with open(license_path, 'r') as f:
            license_data = json.load(f)
        return license_data
    except Exception as e:
        print(f"Error loading license: {e}")
        return None

def load_npu_node_config(node_id, config_dir="data/npu_nodes"):
    """Load the configuration for an NPU node."""
    config_path = os.path.join(config_dir, f"{node_id}.json")
    
    if not os.path.exists(config_path):
        print(f"Error: Configuration for node '{node_id}' not found.")
        print(f"Expected file: {config_path}")
        return None
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"Error loading node configuration: {e}")
        return None

def assign_license(license_data, node_config, assignments_dir="data/license_assignments"):
    """Assign a license to an NPU node."""
    # Create assignments directory if it doesn't exist
    os.makedirs(assignments_dir, exist_ok=True)
    
    # Create assignment record
    assignment = {
        "license_id": license_data["license_id"],
        "node_id": node_config["node_id"],
        "entity_id": license_data["entity_id"],
        "entity_name": license_data["entity_name"],
        "assigned_at": datetime.now().isoformat(),
        "status": "active",
        "terms": license_data["terms"],
        "modules": license_data["modules"],
        "jurisdiction": license_data["jurisdiction"],
        "verification_hash": f"{license_data['license_id']}:{node_config['node_id']}:{datetime.now().isoformat()}"
    }
    
    # Save assignment
    assignment_path = os.path.join(assignments_dir, f"{license_data['license_id']}_{node_config['node_id']}_assignment.json")
    with open(assignment_path, 'w') as f:
        json.dump(assignment, f, indent=2)
    
    return {
        "assignment_path": assignment_path,
        "assignment": assignment
    }

def update_npu_licenses(node_id, license_id, config_dir="data/npu_nodes"):
    """Update the licenses assigned to an NPU node."""
    config_path = os.path.join(config_dir, f"{node_id}.json")
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Initialize licenses array if it doesn't exist
        if "licenses" not in config:
            config["licenses"] = []
        
        # Check if license is already assigned
        for license_entry in config["licenses"]:
            if license_entry.get("license_id") == license_id:
                license_entry["updated_at"] = datetime.now().isoformat()
                license_entry["status"] = "active"
                break
        else:
            # Add new license
            config["licenses"].append({
                "license_id": license_id,
                "assigned_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "status": "active"
            })
        
        # Update last modified time
        config["last_updated"] = datetime.now().isoformat()
        
        # Save updated configuration
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error updating node licenses: {e}")
        return False

def update_license_status(license_id, node_id, license_dir="data/licenses"):
    """Update the status of a license."""
    license_path = os.path.join(license_dir, f"{license_id}.json")
    
    try:
        with open(license_path, 'r') as f:
            license_data = json.load(f)
        
        # Initialize assignments array if it doesn't exist
        if "assignments" not in license_data:
            license_data["assignments"] = []
        
        # Check if assignment already exists
        for assignment in license_data["assignments"]:
            if assignment.get("node_id") == node_id:
                assignment["updated_at"] = datetime.now().isoformat()
                assignment["status"] = "active"
                break
        else:
            # Add new assignment
            license_data["assignments"].append({
                "node_id": node_id,
                "assigned_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "status": "active"
            })
        
        # Update last modified time
        license_data["last_updated"] = datetime.now().isoformat()
        
        # Save updated license
        with open(license_path, 'w') as f:
            json.dump(license_data, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error updating license status: {e}")
        return False

def notify_synadmin(license_id, node_id, assignment, synadmin_dir="data/synadmin_registrations"):
    """Notify SynAdmin Cloud Portal of the license assignment."""
    # In a real implementation, this would make an API call to the SynAdmin Cloud Portal
    # For this example, we'll just update the local registration records
    
    # Update license registration
    license_reg_path = os.path.join(synadmin_dir, f"{license_id}_registration.json")
    if os.path.exists(license_reg_path):
        try:
            with open(license_reg_path, 'r') as f:
                license_reg = json.load(f)
            
            # Add node to license registration
            if "assigned_nodes" not in license_reg:
                license_reg["assigned_nodes"] = []
            
            # Check if node is already assigned
            for node_entry in license_reg["assigned_nodes"]:
                if node_entry.get("node_id") == node_id:
                    node_entry["updated_at"] = datetime.now().isoformat()
                    break
            else:
                # Add new node
                license_reg["assigned_nodes"].append({
                    "node_id": node_id,
                    "assigned_at": datetime.now().isoformat()
                })
            
            # Save updated registration
            with open(license_reg_path, 'w') as f:
                json.dump(license_reg, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not update license registration: {e}")
    
    # Update node registration
    node_reg_path = os.path.join(synadmin_dir, f"{node_id}_registration.json")
    if os.path.exists(node_reg_path):
        try:
            with open(node_reg_path, 'r') as f:
                node_reg = json.load(f)
            
            # Add license to node registration
            if "assigned_licenses" not in node_reg:
                node_reg["assigned_licenses"] = []
            
            # Check if license is already assigned
            for license_entry in node_reg["assigned_licenses"]:
                if license_entry.get("license_id") == license_id:
                    license_entry["updated_at"] = datetime.now().isoformat()
                    break
            else:
                # Add new license
                node_reg["assigned_licenses"].append({
                    "license_id": license_id,
                    "entity_id": assignment["entity_id"],
                    "entity_name": assignment["entity_name"],
                    "assigned_at": datetime.now().isoformat()
                })
            
            # Save updated registration
            with open(node_reg_path, 'w') as f:
                json.dump(node_reg, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not update node registration: {e}")
    
    print(f"SynAdmin Cloud Portal notified of license assignment.")

def main():
    """Main function to run the license assignment script."""
    parser = argparse.ArgumentParser(description='Assign a SynergyzeOS license to an NPU node.')
    parser.add_argument('--license', required=True, help='ID of the license to assign')
    parser.add_argument('--node-id', required=True, help='ID of the NPU node to assign the license to')
    
    args = parser.parse_args()
    
    # Load license
    license_data = load_license(args.license)
    if not license_data:
        print(f"Error: Could not load license '{args.license}'.")
        sys.exit(1)
    
    # Load NPU node configuration
    node_config = load_npu_node_config(args.node_id)
    if not node_config:
        print(f"Error: Could not load configuration for node '{args.node_id}'.")
        sys.exit(1)
    
    print(f"Assigning license {args.license} to NPU node {args.node_id}...")
    
    # Assign license
    assignment_info = assign_license(license_data, node_config)
    
    # Update NPU node licenses
    update_npu_licenses(args.node_id, args.license)
    
    # Update license status
    update_license_status(args.license, args.node_id)
    
    # Notify SynAdmin
    notify_synadmin(args.license, args.node_id, assignment_info["assignment"])
    
    print("\nLicense Assignment Complete!")
    print(f"License ID: {license_data['license_id']}")
    print(f"Node ID: {node_config['node_id']}")
    print(f"Entity: {license_data['entity_name']} ({license_data['entity_id']})")
    print(f"Assignment Record: {assignment_info['assignment_path']}")
    print("\nNext steps:")
    print(f"1. Verify the license assignment: python tools/verify_license_assignment.py --license \"{args.license}\" --node-id \"{args.node_id}\"")
    print(f"2. Deploy entities to cloud shell: python tools/deploy_to_cloud_shell.py --entity \"{license_data['entity_name']}\" --region \"{node_config['region']}\" --npu \"{args.node_id}\"")

if __name__ == "__main__":
    main()
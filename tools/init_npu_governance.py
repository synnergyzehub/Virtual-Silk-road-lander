#!/usr/bin/env python3
"""
SynergyzeOS - NPU Governance Initialization Tool

This script initializes the computational governance rules for an NPU node.
These rules define how the NPU enforces the Divine Alignment Layer validation
and other governance aspects of the Genesis Stack.
"""

import os
import sys
import json
import argparse
import hashlib
from datetime import datetime

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

def validate_ecg_key(ecg_key, node_config):
    """Validate the ECG key for governance initialization."""
    # In a real implementation, this would validate against a secure key store
    # For this example, we'll use a simple hash-based validation
    
    # Create a validation hash based on node ID and region
    validation_seed = f"{node_config['node_id']}:{node_config['region']}:ECG_VALIDATION"
    expected_hash = hashlib.sha256(validation_seed.encode()).hexdigest()[:16]
    
    # For demonstration purposes, accept 'emperorkey123' as a valid key
    if ecg_key == "emperorkey123" or ecg_key == expected_hash:
        return True
    
    # For real validation, you would do something like:
    # return secure_validation_service.validate_ecg_key(ecg_key, node_config['node_id'])
    
    return False

def create_governance_rules(node_config, rules_dir="data/governance_rules"):
    """Create governance rules for the NPU node."""
    # Create rules directory if it doesn't exist
    os.makedirs(rules_dir, exist_ok=True)
    
    # Generate standard governance rules
    governance_rules = {
        "node_id": node_config["node_id"],
        "node_hash": node_config["node_hash"],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "version": "1.0",
        "divine_alignment": {
            "minimum_threshold": 70.0,
            "approval_level": "automatic",
            "exception_handling": "alert_ecg_team",
            "ethics_filter": {
                "enabled": True,
                "strictness": "standard",
                "override_allowed": True,
                "override_requires": "ecg_approval"
            }
        },
        "license_validation": {
            "verification_frequency": "per_session",
            "expiry_warning_days": 30,
            "grace_period_days": 7,
            "offline_operation": {
                "allowed": True,
                "max_duration_hours": 72
            }
        },
        "computational_governance": {
            "decision_threshold": 85.0,
            "audit_frequency": "daily",
            "log_retention_days": 90,
            "automatic_remediation": {
                "enabled": True,
                "severity_threshold": "medium"
            }
        },
        "jurisdictional_rules": {
            "default_jurisdiction": node_config["region"],
            "cross_jurisdiction_operation": {
                "allowed": True,
                "requires_approval": True
            },
            "data_sovereignty": {
                "enforce_local_storage": True,
                "allow_exceptions": True,
                "exception_requires": "ecg_approval"
            }
        }
    }
    
    # Save governance rules
    rules_path = os.path.join(rules_dir, f"{node_config['node_id']}_governance.json")
    with open(rules_path, 'w') as f:
        json.dump(governance_rules, f, indent=2)
    
    return {
        "rules_path": rules_path,
        "rules": governance_rules
    }

def generate_divine_filters(node_config, filters_dir="data/divine_filters"):
    """Generate Divine Alignment Layer filters for the NPU node."""
    # Create filters directory if it doesn't exist
    os.makedirs(filters_dir, exist_ok=True)
    
    # Generate divine filters
    divine_filters = {
        "node_id": node_config["node_id"],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "version": "1.0",
        "filters": [
            {
                "name": "ethical_commerce",
                "description": "Ensures all commerce operations align with ethical principles",
                "threshold": 75.0,
                "priority": "high",
                "keywords": ["payment", "transaction", "purchase", "sell", "commerce"],
                "parameters": {
                    "transparency_required": True,
                    "fair_pricing_check": True,
                    "sustainability_factor": 0.8
                }
            },
            {
                "name": "data_sovereignty",
                "description": "Enforces data sovereignty requirements based on jurisdiction",
                "threshold": 90.0,
                "priority": "critical",
                "keywords": ["data", "storage", "transfer", "export", "personal"],
                "parameters": {
                    "local_storage_preference": True,
                    "consent_verification": True,
                    "anonymization_check": True
                }
            },
            {
                "name": "governance_alignment",
                "description": "Ensures actions align with governance principles of the entity",
                "threshold": 80.0,
                "priority": "medium",
                "keywords": ["governance", "policy", "rule", "decision", "approve"],
                "parameters": {
                    "multi_level_approval": True,
                    "transparency_requirement": 0.7,
                    "audit_trail_required": True
                }
            }
        ]
    }
    
    # Add region-specific filters based on node region
    region = node_config["region"]
    if region.startswith("IND"):
        divine_filters["filters"].append({
            "name": "india_compliance",
            "description": "Ensures compliance with Indian regulations and cultural values",
            "threshold": 85.0,
            "priority": "high",
            "keywords": ["india", "rupee", "gst", "aadhaar", "pan"],
            "parameters": {
                "gst_compliance": True,
                "local_data_storage": True,
                "cultural_sensitivity": 0.9
            }
        })
    elif region.startswith("USA"):
        divine_filters["filters"].append({
            "name": "us_compliance",
            "description": "Ensures compliance with US regulations",
            "threshold": 85.0,
            "priority": "high",
            "keywords": ["usa", "dollar", "federal", "state", "tax"],
            "parameters": {
                "state_specific_rules": True,
                "hipaa_compliance": True,
                "export_control_check": True
            }
        })
    
    # Save divine filters
    filters_path = os.path.join(filters_dir, f"{node_config['node_id']}_filters.json")
    with open(filters_path, 'w') as f:
        json.dump(divine_filters, f, indent=2)
    
    return {
        "filters_path": filters_path,
        "filters": divine_filters
    }

def update_npu_status(node_id, status="governance_initialized", config_dir="data/npu_nodes"):
    """Update the status of the NPU node."""
    config_path = os.path.join(config_dir, f"{node_id}.json")
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        config["status"] = status
        config["last_updated"] = datetime.now().isoformat()
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error updating node status: {e}")
        return False

def register_with_synadmin(node_id, governance_rules, divine_filters, synadmin_dir="data/synadmin_registrations"):
    """Register governance rules with SynAdmin Cloud Portal."""
    # In a real implementation, this would make an API call to the SynAdmin Cloud Portal
    # For this example, we'll just update the local registration record
    
    reg_path = os.path.join(synadmin_dir, f"{node_id}_registration.json")
    
    if not os.path.exists(reg_path):
        print(f"Warning: Registration record for node '{node_id}' not found. Creating new record.")
        os.makedirs(synadmin_dir, exist_ok=True)
        registration = {
            "node_id": node_id,
            "registration_time": datetime.now().isoformat()
        }
    else:
        try:
            with open(reg_path, 'r') as f:
                registration = json.load(f)
        except Exception as e:
            print(f"Error loading registration record: {e}")
            registration = {
                "node_id": node_id,
                "registration_time": datetime.now().isoformat()
            }
    
    # Update registration with governance information
    registration["governance_initialized"] = True
    registration["governance_version"] = governance_rules["rules"]["version"]
    registration["divine_filters_version"] = divine_filters["filters"]["version"]
    registration["governance_update_time"] = datetime.now().isoformat()
    
    # Save updated registration
    with open(reg_path, 'w') as f:
        json.dump(registration, f, indent=2)
    
    print(f"Governance registration updated in SynAdmin record: {reg_path}")
    return registration

def main():
    """Main function to run the NPU governance initialization script."""
    parser = argparse.ArgumentParser(description='Initialize governance rules for an NPU node.')
    parser.add_argument('--node-id', required=True, help='ID of the NPU node to initialize')
    parser.add_argument('--ecg-key', required=True, help='ECG key for governance initialization')
    
    args = parser.parse_args()
    
    # Load NPU node configuration
    node_config = load_npu_node_config(args.node_id)
    if not node_config:
        print(f"Error: Could not load configuration for node '{args.node_id}'.")
        sys.exit(1)
    
    # Validate ECG key
    if not validate_ecg_key(args.ecg_key, node_config):
        print("Error: Invalid ECG key. Governance initialization aborted.")
        sys.exit(1)
    
    print(f"Initializing governance rules for NPU node {args.node_id}...")
    
    # Create governance rules
    governance_rules = create_governance_rules(node_config)
    
    # Generate divine filters
    divine_filters = generate_divine_filters(node_config)
    
    # Update NPU status
    update_npu_status(args.node_id)
    
    # Register with SynAdmin
    register_with_synadmin(args.node_id, governance_rules, divine_filters)
    
    print("\nNPU Governance Initialization Complete!")
    print(f"Node ID: {node_config['node_id']}")
    print(f"Governance Rules: {governance_rules['rules_path']}")
    print(f"Divine Filters: {divine_filters['filters_path']}")
    print("\nNext steps:")
    print(f"1. Assign SynergyzeOS license to the NPU node: python tools/assign_license_to_npu.py --license \"LICENSE_ID\" --node-id \"{args.node_id}\"")
    print(f"2. Deploy entities to cloud shell: python tools/deploy_to_cloud_shell.py --entity \"ENTITY_NAME\" --region \"{node_config['region']}\" --npu \"{args.node_id}\"")
    print(f"3. Verify NPU node status: python tools/verify_npu_status.py --node-id \"{args.node_id}\"")

if __name__ == "__main__":
    main()
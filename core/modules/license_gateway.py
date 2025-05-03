"""
License Gateway Module for Empire OS

- Issues and validates licenses for users and actions
- Manages license lifecycle (issuance, renewal, revocation)
- Implements divine principles (Justice, Mercy) in license issuance
- Logs all license activities to Divine Ledger
"""

import json
import time
from datetime import datetime, timedelta
import os
import hashlib
import random

# Divine principles that guide license issuance
DIVINE_PRINCIPLES = {
    "Al-Adl": "Justice",       # Fair, balanced outcomes
    "Ar-Rahman": "Mercy",      # Compassion beyond justice
    "Al-Hakim": "Wisdom",      # Long-term, considered decisions
    "Al-Alim": "Knowledge",    # Informed, data-driven decisions
    "Al-Muqsit": "Equity"      # Fair distribution of resources
}

# License types with permission levels
LICENSE_TYPES = {
    "Viewer": {
        "level": 1,
        "description": "Can view but not modify",
        "permissions": ["view_dashboards", "view_reports"]
    },
    "Operator": {
        "level": 2,
        "description": "Can perform standard operations",
        "permissions": ["view_dashboards", "view_reports", "execute_transactions", "generate_reports"]
    },
    "Governor": {
        "level": 3,
        "description": "Can govern realm and approve requests",
        "permissions": ["view_dashboards", "view_reports", "execute_transactions", 
                        "generate_reports", "approve_licenses", "modify_realm_settings"]
    },
    "Emperor": {
        "level": 4,
        "description": "Full system access across all realms",
        "permissions": ["*"]  # All permissions
    }
}

# License statuses
LICENSE_STATUS = {
    "APPROVED": "Full approval granted",
    "CONDITIONAL": "Approved with specific conditions",
    "PENDING": "Under review by governance",
    "DENIED": "Request denied",
    "REVOKED": "Previously granted license revoked",
    "EXPIRED": "License term has ended"
}

def issue_license(identity_context, transaction_context=None):
    """
    Issues a license based on identity context and transaction details
    
    Args:
        identity_context (dict): User identity information
        transaction_context (dict, optional): Transaction details
        
    Returns:
        dict: License details
    """
    if not identity_context:
        return {
            "approved": False,
            "status": LICENSE_STATUS["DENIED"],
            "reason": "Invalid identity context"
        }
    
    # Get user's role and license level
    role = identity_context.get('role')
    license_level = identity_context.get('license_level', 0)
    emotion = identity_context.get('emotion', 'neutral')
    realm = identity_context.get('realm', 'Unknown')
    
    # Map license level to type
    license_type = next((k for k, v in LICENSE_TYPES.items() if v["level"] == license_level), None)
    
    if not license_type:
        return {
            "approved": False,
            "status": LICENSE_STATUS["DENIED"],
            "reason": f"No license type found for level {license_level}"
        }
    
    # Basic license approval
    license_info = {
        "approved": True,
        "type": license_type,
        "permissions": LICENSE_TYPES[license_type]["permissions"],
        "holder": role,
        "realm": realm,
        "issued_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(days=30)).isoformat(),
        "status": LICENSE_STATUS["APPROVED"],
        "license_id": generate_license_id(identity_context)
    }
    
    # Apply divine principles to license if transaction context is provided
    if transaction_context:
        license_info = apply_divine_principles(license_info, identity_context, transaction_context)
    
    # Log the license issuance
    log_license_action(license_info)
    
    return license_info

def apply_divine_principles(license_info, identity_context, transaction_context):
    """
    Applies divine principles to modify license details based on context
    
    Args:
        license_info (dict): Base license information
        identity_context (dict): User identity information
        transaction_context (dict): Transaction details
        
    Returns:
        dict: Updated license information
    """
    # Extract relevant information
    transaction_type = transaction_context.get('type', '')
    transaction_impact = transaction_context.get('impact', 'low')
    transaction_urgency = transaction_context.get('urgency', 'low')
    transaction_quantity = transaction_context.get('quantity', 0)
    model = transaction_context.get('model', '')
    emotion = identity_context.get('emotion', 'neutral')
    
    # Apply Al-Adl (Justice) principle for high-impact transactions
    if transaction_impact == 'high':
        # Limit permissions or add conditions for high-impact transactions
        license_info["status"] = LICENSE_STATUS["CONDITIONAL"]
        license_info["conditions"] = ["Impact monitoring required", "Regular governance review"]
        license_info["divine_principle"] = "Al-Adl (Justice)"
        
        # Adjust expiration for high-impact transactions (shorter period)
        license_info["expires_at"] = (datetime.now() + timedelta(days=7)).isoformat()
    
    # Apply Ar-Rahman (Mercy) principle for certain emotions
    if emotion in ['regretful', 'remorseful', 'learning']:
        # More lenient conditions for those showing remorse or growth
        license_info["divine_principle"] = "Ar-Rahman (Mercy)"
        license_info["guidance"] = "Show mercy to those who seek to improve"
    
    # Apply Al-Hakim (Wisdom) for large quantities
    if transaction_quantity > 1000:
        license_info["status"] = LICENSE_STATUS["CONDITIONAL"]
        license_info["conditions"] = license_info.get("conditions", []) + [
            f"Initial batch limited to {min(500, transaction_quantity//10)} units"
        ]
        license_info["divine_principle"] = "Al-Hakim (Wisdom)"
        license_info["advice"] = "Trial rollout advised to ensure traceability and ESG impact."
    
    # Return the modified license
    return license_info

def validate_license(license_id, action, realm):
    """
    Validates if a license allows a specific action in a realm
    
    Args:
        license_id (str): License identifier
        action (str): Action to be performed
        realm (str): Realm where action will be performed
        
    Returns:
        bool: Whether the action is allowed
    """
    # This would normally check a database
    # For demo purposes, we're simplifying
    return True

def generate_license_id(identity_context):
    """Generate a unique license ID"""
    seed = f"{identity_context.get('role')}-{identity_context.get('realm')}-{datetime.now().isoformat()}"
    return hashlib.sha256(seed.encode()).hexdigest()[:24]

def log_license_action(license_info):
    """Log license actions to the divine ledger"""
    # Ensure data directory exists
    os.makedirs('data/ledger', exist_ok=True)
    
    # Create log entry
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": "license_issued" if license_info.get("approved") else "license_denied",
        "license_id": license_info.get("license_id"),
        "holder": license_info.get("holder"),
        "realm": license_info.get("realm"),
        "status": license_info.get("status"),
        "divine_principle": license_info.get("divine_principle", "None")
    }
    
    # Append to log file
    with open('data/ledger/license_ledger.jsonl', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

# For testing
if __name__ == "__main__":
    from digital_me import verify_identity, get_identity_context
    
    # Test credentials
    test_credentials = {
        "role": "factory-operator",
        "biometric": "simulated",
        "wallet": "0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE",
        "emotion": "purposeful"
    }
    
    # Test transaction
    test_transaction = {
        "type": "license-request",
        "model": "CMP",
        "quantity": 10000,
        "urgency": "medium",
        "impact": "medium"
    }
    
    # Verify identity
    identity_result = verify_identity(test_credentials)
    identity_context = get_identity_context(identity_result)
    
    # Issue license
    license_result = issue_license(identity_context, test_transaction)
    print(json.dumps(license_result, indent=2))
"""
Secure Empire License API

This module provides a Flask-based API for managing licenses in the Empire OS ecosystem,
with secure authentication and audit logging.
"""

from flask import Flask, request, jsonify
import json
import os
from datetime import datetime
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='license_api.log'
)
logger = logging.getLogger("license_api")

# Security configuration
API_KEY = os.getenv('EMPIRE_API_KEY', 'emperorkey123')  # Default for local testing

# In-memory storage (would be replaced with database in production)
licenses = {}
license_assignments = {}
digitalme_ledger = []
audit_log = []

# Database connection (commented out since we're using in-memory storage for demo)
"""
import mysql.connector

db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "youruser"),
    "password": os.getenv("DB_PASSWORD", "yourpass"),
    "database": os.getenv("DB_NAME", "empireos")
}

def get_db_connection():
    return mysql.connector.connect(**db_config)
"""

# Divine Alignment Layer parameters
ETHICAL_KEYWORDS = [
    "trust", "sustainability", "inclusion", "authenticity", "justice", 
    "transparency", "accountability", "fairness", "compassion", "honesty",
    "integrity", "respect", "equity", "benevolence", "morality"
]

# Load sample data if it exists
def load_sample_data():
    # Load a sample DigitalMe identity
    try:
        with open("digitalme_license_scope.json", "r") as f:
            digitalme_data = json.load(f)
            for license_data in digitalme_data.get("bound_licenses", []):
                licenses[license_data["license_id"]] = {
                    "brand": license_data["brand"],
                    "region": license_data["region"],
                    "modules": license_data["modules"],
                    "status": license_data["status"],
                    "role_map": license_data["role_map"]
                }
    except FileNotFoundError:
        logger.warning("No digitalme_license_scope.json found, using empty license store")
    
    # Load sample ledger entries
    try:
        with open("digitalme_action_ledger_log.json", "r") as f:
            ledger_entry = json.load(f)
            digitalme_ledger.append(ledger_entry)
    except FileNotFoundError:
        logger.warning("No digitalme_action_ledger_log.json found, using empty ledger")


# Authentication middleware
def require_api_key(func):
    def wrapper(*args, **kwargs):
        auth_token = request.headers.get('x-api-key')
        if request.method == 'OPTIONS':
            # Skip authentication for preflight requests
            return func(*args, **kwargs)
        if auth_token != API_KEY:
            logger.warning(f"Unauthorized API access attempt: {request.path}")
            return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


# License management endpoints
@app.route('/api/license/assign', methods=['POST'])
@require_api_key
def assign_license():
    data = request.json
    license_id = data.get("licenseId")
    assigned_to = data.get("assignedTo")
    role = data.get("role")
    module_scope = data.get("moduleScope")
    node = data.get("node")
    
    if not license_id or not assigned_to:
        return jsonify({"error": "licenseId and assignedTo are required"}), 400
    
    # Add the assignment
    assignment_key = f"{license_id}:{assigned_to}"
    license_assignments[assignment_key] = {
        "license_id": license_id,
        "assigned_to": assigned_to,
        "role": role,
        "module_scope": module_scope,
        "node": node,
        "timestamp": datetime.now().isoformat()
    }
    
    # If the license doesn't exist, create it
    if license_id not in licenses:
        licenses[license_id] = {
            "brand": node.split(":")[0] if ":" in node else "Unknown",
            "region": "Global",
            "modules": [module_scope] if module_scope else [],
            "status": "active",
            "role_map": {
                "role_type": role,
                "power_scope": ["read"],
                "granted_by": "Secure Empire License API",
                "approved_at": datetime.now().isoformat()
            }
        }
    
    # Create a ledger entry
    ledger_entry = {
        "digitalme_id": f"generated-{hash(assigned_to) % 10000:04d}",
        "session_id": f"SESSION-{hash(license_id + assigned_to) % 100000:05d}",
        "device": "API Assignment",
        "geo_location": "Global",
        "license_id": license_id,
        "role": role,
        "action": "license_assignment",
        "intent_token": f"TOK-{hash(datetime.now().isoformat()) % 1000000:06d}",
        "action_status": "approved",
        "timestamp": datetime.now().isoformat(),
        "validated_by": "Secure License API",
        "risk_score": 15,  # Low risk for normal assignment
        "notes": f"License {license_id} assigned to {assigned_to} as {role} for {module_scope}"
    }
    digitalme_ledger.append(ledger_entry)
    
    # Add to audit log
    audit_log.append({
        "license_id": license_id,
        "action_type": "ASSIGNMENT",
        "actor": assigned_to,
        "node_context": node,
        "created_at": datetime.now().isoformat(),
        "api_key_used": request.headers.get('x-api-key')[-4:] if request.headers.get('x-api-key') else None
    })
    
    logger.info(f"License {license_id} assigned to {assigned_to}")
    
    return jsonify({
        "status": "success", 
        "message": f"License {license_id} assigned to {assigned_to}",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/license/create', methods=['POST'])
@require_api_key
def create_license():
    data = request.json
    license_id = data.get("license_id")
    owner = data.get("owner")
    scope = data.get("scope", [])
    
    if not license_id or not owner:
        return jsonify({"error": "license_id and owner are required"}), 400
    
    # Create the license
    licenses[license_id] = {
        "brand": "Created via API",
        "region": "Global",
        "modules": scope,
        "status": "active",
        "role_map": {
            "role_type": "Owner",
            "power_scope": ["read", "write", "approve"],
            "granted_by": "License Create API",
            "approved_at": datetime.now().isoformat()
        }
    }
    
    # Add to audit log
    audit_log.append({
        "license_id": license_id,
        "action_type": "CREATION",
        "actor": owner,
        "node_context": "License API",
        "created_at": datetime.now().isoformat(),
        "api_key_used": request.headers.get('x-api-key')[-4:] if request.headers.get('x-api-key') else None
    })
    
    logger.info(f"License {license_id} created for {owner}")
    
    return jsonify({
        "message": "License created", 
        "license_id": license_id,
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/license/list', methods=['GET'])
@require_api_key
def list_licenses():
    return jsonify({
        "licenses": licenses,
        "assignments": license_assignments
    })


@app.route('/license/validate', methods=['POST'])
@require_api_key
def validate_license():
    data = request.json
    license_id = data.get("license_id")
    module = data.get("module")
    
    if license_id not in licenses:
        return jsonify({"valid": False, "reason": "License not found"}), 404
    
    license_data = licenses[license_id]
    
    # Check if module is in scope
    valid = True
    reason = None
    
    if module and module not in license_data.get("modules", []):
        valid = False
        reason = "Module not in scope"
    
    # Check if license is active
    if license_data.get("status") != "active":
        valid = False
        reason = f"License is {license_data.get('status')}"
    
    # Add to audit log
    audit_log.append({
        "license_id": license_id,
        "action_type": "VALIDATION",
        "actor": "API User",
        "node_context": f"Module: {module}",
        "created_at": datetime.now().isoformat(),
        "api_key_used": request.headers.get('x-api-key')[-4:] if request.headers.get('x-api-key') else None,
        "result": "Valid" if valid else f"Invalid: {reason}"
    })
    
    logger.info(f"License {license_id} validated: {valid}")
    
    if valid:
        return jsonify({
            "valid": True,
            "license_id": license_id,
            "brand": license_data.get("brand"),
            "region": license_data.get("region"),
            "status": license_data.get("status")
        })
    else:
        return jsonify({"valid": False, "reason": reason})


@app.route('/digitalme/ledger', methods=['GET'])
@require_api_key
def get_ledger():
    return jsonify(digitalme_ledger)


@app.route('/api/license/audit', methods=['GET'])
@require_api_key
def get_audit_log():
    return jsonify(audit_log)


@app.route('/license/<license_id>/audit', methods=['GET'])
@require_api_key
def get_license_audit(license_id):
    """Get audit log for a specific license"""
    if license_id:
        # Filter audit log by license ID
        license_audits = [entry for entry in audit_log if entry.get("license_id") == license_id]
        return jsonify({"audit_log": license_audits})
    return jsonify({"error": "License ID is required"}), 400


@app.route('/api/dal/align', methods=['POST'])
@require_api_key
def align_with_dal():
    """Check scope tags against the Divine Alignment Layer ethical keywords"""
    data = request.json
    scope_tags = data.get("scope_tags", [])
    
    if isinstance(scope_tags, str):
        # Handle comma-separated string
        scope_tags = [tag.strip().lower() for tag in scope_tags.split(",")]
    
    # Filter out empty tags
    scope_tags = [tag for tag in scope_tags if tag]
    
    if not scope_tags:
        return jsonify({
            "error": "No scope tags provided",
            "aligned": [],
            "misaligned": []
        }), 400
    
    # Check alignment with ethical keywords
    aligned = [tag for tag in scope_tags if tag in ETHICAL_KEYWORDS]
    misaligned = [tag for tag in scope_tags if tag not in ETHICAL_KEYWORDS]
    
    # Calculate alignment score (percentage)
    alignment_score = (len(aligned) / len(scope_tags)) * 100 if scope_tags else 0
    
    # Add to audit log
    audit_log.append({
        "license_id": data.get("license_id", "Unknown"),
        "action_type": "DAL_ALIGNMENT",
        "actor": data.get("requester", "API User"),
        "node_context": "Divine Alignment Layer",
        "created_at": datetime.now().isoformat(),
        "api_key_used": request.headers.get('x-api-key')[-4:] if request.headers.get('x-api-key') else None,
        "alignment_score": alignment_score
    })
    
    logger.info(f"DAL alignment check: {alignment_score:.1f}% aligned")
    
    # Return the alignment results
    return jsonify({
        "aligned": aligned,
        "misaligned": misaligned,
        "alignment_score": alignment_score,
        "ethical_keywords": ETHICAL_KEYWORDS
    })


# Enable CORS for local development
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,x-api-key')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


# Initialize sample data
load_sample_data()

if __name__ == '__main__':
    # Print the API key (in a real system, this would be distributed securely)
    print(f"Starting secure license API with key: {API_KEY}")
    app.run(host='0.0.0.0', port=5001)
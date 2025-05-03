from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# In-memory storage (would be replaced with database in production)
licenses = {}
license_assignments = {}
digitalme_ledger = []

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
        print("No digitalme_license_scope.json found, using empty license store")
    
    # Load sample ledger entries
    try:
        with open("digitalme_action_ledger_log.json", "r") as f:
            ledger_entry = json.load(f)
            digitalme_ledger.append(ledger_entry)
    except FileNotFoundError:
        print("No digitalme_action_ledger_log.json found, using empty ledger")


# License management endpoints
@app.route('/api/license/assign', methods=['POST'])
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
                "granted_by": "Genesis Dashboard",
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
        "validated_by": "Genesis Dashboard API",
        "risk_score": 15,  # Low risk for normal assignment
        "notes": f"License {license_id} assigned to {assigned_to} as {role} for {module_scope}"
    }
    digitalme_ledger.append(ledger_entry)
    
    return jsonify({
        "status": "success", 
        "message": f"License {license_id} assigned to {assigned_to}",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/license/list', methods=['GET'])
def list_licenses():
    return jsonify({
        "licenses": licenses,
        "assignments": license_assignments
    })


@app.route('/api/license/verify', methods=['POST'])
def verify_license():
    data = request.json
    license_id = data.get("license_id")
    module = data.get("module")
    role = data.get("role")
    
    if license_id not in licenses:
        return jsonify({"valid": False, "reason": "License not found"}), 404
    
    license_data = licenses[license_id]
    
    # Check if module is in scope
    if module and module not in license_data.get("modules", []):
        return jsonify({"valid": False, "reason": "Module not in license scope"})
    
    # Check if role matches
    if role and license_data.get("role_map", {}).get("role_type") != role:
        return jsonify({"valid": False, "reason": "Role mismatch"})
    
    # Check if license is active
    if license_data.get("status") != "active":
        return jsonify({"valid": False, "reason": f"License is {license_data.get('status')}"})
    
    return jsonify({
        "valid": True,
        "license_id": license_id,
        "brand": license_data.get("brand"),
        "region": license_data.get("region"),
        "status": license_data.get("status")
    })


@app.route('/digitalme/ledger', methods=['GET'])
def get_ledger():
    return jsonify(digitalme_ledger)


# Initialize sample data
load_sample_data()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample in-memory store for licenses
licenses = {}

@app.route('/license/create', methods=['POST'])
def create_license():
    data = request.json
    license_id = data.get("license_id")
    scope = data.get("scope", [])
    owner = data.get("owner")
    if not license_id or not owner:
        return jsonify({"error": "license_id and owner are required"}), 400
    licenses[license_id] = {
        "owner": owner,
        "scope": scope,
        "valid": True,
        "log": []
    }
    return jsonify({"message": "License created", "license_id": license_id})

@app.route('/license/validate', methods=['POST'])
def validate_license():
    data = request.json
    license_id = data.get("license_id")
    module = data.get("module")
    if license_id not in licenses:
        return jsonify({"error": "License not found"}), 404
    if module not in licenses[license_id]["scope"]:
        return jsonify({"valid": False, "reason": "Module not in scope"})
    return jsonify({"valid": True})

@app.route('/component/register', methods=['POST'])
def register_component():
    data = request.json
    license_id = data.get("license_id")
    component = data.get("component")
    if license_id in licenses:
        licenses[license_id]["log"].append({"component": component})
        return jsonify({"message": "Component registered"})
    return jsonify({"error": "License not found"}), 404

@app.route('/license/<license_id>/scope', methods=['GET'])
def get_scope(license_id):
    if license_id in licenses:
        return jsonify({"scope": licenses[license_id]["scope"]})
    return jsonify({"error": "License not found"}), 404

@app.route('/license/<license_id>/audit', methods=['GET'])
def get_audit(license_id):
    if license_id in licenses:
        return jsonify({"audit_log": licenses[license_id]["log"]})
    return jsonify({"error": "License not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

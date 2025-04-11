
from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)
API_KEY = os.getenv('EMPIRE_API_KEY', 'supersecretkey')  # Default for local testing

db = mysql.connector.connect(
    host="localhost",
    user="youruser",
    password="yourpass",
    database="empireos"
)

@app.route("/api/license/assign", methods=["POST"])
def assign_license():
    data = request.json
    headers = request.headers
    auth_token = headers.get('x-api-key')

    if auth_token != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    cursor = db.cursor()

    # Insert or update license_master
    cursor.execute("""
        INSERT INTO license_master (license_id, issued_to, module_scope)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE issued_to=%s, module_scope=%s
    """, (
        data["licenseId"], data["assignedTo"], data["moduleScope"],
        data["assignedTo"], data["moduleScope"]
    ))

    # Insert into role_registry
    cursor.execute("""
        INSERT INTO role_registry (digitalme_id, license_id, role_type)
        VALUES (%s, %s, %s)
    """, (
        data["assignedTo"], data["licenseId"], data["role"]
    ))

    # Insert into audit log
    cursor.execute("""
        INSERT INTO license_validation_log (license_id, action_type, actor, node_context, created_at)
        VALUES (%s, %s, %s, %s, NOW())
    """, (
        data["licenseId"], 'ASSIGNMENT', data["assignedTo"], data["node"]
    ))

    db.commit()
    return jsonify({"status": "License assigned and logged"}), 200

if __name__ == "__main__":
    app.run(debug=True)

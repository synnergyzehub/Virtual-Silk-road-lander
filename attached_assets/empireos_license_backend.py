
from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="youruser",
    password="yourpass",
    database="empireos"
)

@app.route("/api/license/assign", methods=["POST"])
def assign_license():
    data = request.json
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

    db.commit()
    return jsonify({"status": "License assigned"}), 200

if __name__ == "__main__":
    app.run(debug=True)


from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)
API_KEY = os.getenv('EMPIRE_API_KEY', 'supersecretkey')

db = mysql.connector.connect(
    host="localhost",
    user="youruser",
    password="yourpass",
    database="empireos"
)

@app.route("/api/license/alerts/<int:alert_id>/acknowledge", methods=["POST"])
def acknowledge_alert(alert_id):
    data = request.json
    acknowledged_by = data.get("acknowledged_by")

    if not acknowledged_by:
        return jsonify({"error": "Missing acknowledged_by field"}), 400

    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO license_alert_ack_log (alert_id, acknowledged_by)
        VALUES (%s, %s)
    """, (alert_id, acknowledged_by))

    cursor.execute("""
        DELETE FROM license_alert_log WHERE id = %s
    """, (alert_id,))

    db.commit()
    return jsonify({"status": "Alert acknowledged"}), 200

if __name__ == "__main__":
    app.run(debug=True)

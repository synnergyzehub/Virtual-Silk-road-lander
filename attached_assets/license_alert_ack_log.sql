
CREATE TABLE license_alert_ack_log (
  id INT AUTO_INCREMENT PRIMARY KEY,
  alert_id INT,
  acknowledged_by VARCHAR(255),
  acknowledged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (alert_id) REFERENCES license_alert_log(id) ON DELETE CASCADE
);

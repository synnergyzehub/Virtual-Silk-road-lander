
CREATE TABLE license_alert_log (
  id INT AUTO_INCREMENT PRIMARY KEY,
  license_id VARCHAR(255),
  alert_type VARCHAR(100),
  detail TEXT,
  triggered_by VARCHAR(255),
  triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

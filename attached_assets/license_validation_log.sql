
CREATE TABLE license_validation_log (
  id INT AUTO_INCREMENT PRIMARY KEY,
  license_id VARCHAR(255),
  action_type VARCHAR(100),
  actor VARCHAR(255),
  node_context VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Sample Data for Testing
-- =====================================================

USE pppoe_manager;

-- Sample Plans
INSERT INTO plans (name, description, download_speed, upload_speed, time_limit, price, plan_type) VALUES
('Guest 1 Hour', 'Basic internet for 1 hour', 1024, 512, 60, 2.00, 'hotspot'),
('Guest 4 Hours', 'Extended internet access', 2048, 1024, 240, 5.00, 'hotspot'),
('Daily Pass', 'Full day internet access', 5120, 2048, 1440, 10.00, 'hotspot'),
('PPPoE Basic', 'Home internet package', 10240, 5120, NULL, 25.00, 'pppoe'),
('PPPoE Premium', 'High-speed home internet', 20480, 10240, NULL, 45.00, 'pppoe'),
('Business Plan', 'Commercial internet service', 51200, 25600, NULL, 100.00, 'both');

-- Sample Users (password is 'password123' - we'll hash this properly later)
INSERT INTO users (username, password_hash, full_name, email, phone, plan_id, connection_type, balance) VALUES
('admin', 'temp_hash', 'System Administrator', 'admin@company.com', '+1234567890', 6, 'both', 0.00),
('guest001', 'temp_hash', 'Guest User 001', 'guest001@temp.com', NULL, 1, 'hotspot', 10.00),
('user001', 'temp_hash', 'John Doe', 'john@example.com', '+1234567891', 4, 'pppoe', 25.00),
('user002', 'temp_hash', 'Jane Smith', 'jane@example.com', '+1234567892', 5, 'pppoe', 45.00);

-- System Settings
INSERT INTO system_settings (setting_key, setting_value, description, setting_type) VALUES
('company_name', 'Your ISP Company', 'Company name for branding', 'string'),
('radius_server_ip', '127.0.0.1', 'RADIUS server IP address', 'string'),
('radius_secret', 'testing123', 'RADIUS shared secret', 'string'),
('mikrotik_api_ip', '192.168.1.1', 'MikroTik router IP address', 'string'),
('default_session_timeout', '3600', 'Default session timeout in seconds', 'integer'),
('enable_accounting', 'true', 'Enable usage accounting', 'boolean');
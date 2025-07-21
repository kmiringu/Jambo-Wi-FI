-- =====================================================
-- PPPoE + Hotspot Management Database Schema
-- =====================================================

-- Create database
CREATE DATABASE IF NOT EXISTS pppoe_manager 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE pppoe_manager;

-- =====================================================
-- 1. PLANS TABLE (Bandwidth and pricing packages)
-- =====================================================
CREATE TABLE plans (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Speed limits (in Kbps - Kilobits per second)
    download_speed INT NOT NULL COMMENT 'Download speed in Kbps',
    upload_speed INT NOT NULL COMMENT 'Upload speed in Kbps',
    
    -- Time limits
    time_limit INT NULL COMMENT 'Time limit in minutes, NULL = unlimited',
    
    -- Pricing
    price DECIMAL(10,2) DEFAULT 0.00 COMMENT 'Price in local currency',
    
    -- Plan type
    plan_type ENUM('pppoe', 'hotspot', 'both') DEFAULT 'hotspot',
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Indexes for faster queries
    INDEX idx_plan_type (plan_type),
    INDEX idx_active (is_active)
) COMMENT 'Internet service plans with bandwidth and pricing';

-- =====================================================
-- 2. USERS TABLE (Customer information)
-- =====================================================
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    
    -- Login credentials
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    
    -- User information
    full_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    
    -- Service configuration
    plan_id INT NOT NULL,
    connection_type ENUM('pppoe', 'hotspot', 'both') DEFAULT 'hotspot',
    
    -- Account status
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL COMMENT 'Account expiration, NULL = no expiration',
    last_login TIMESTAMP NULL,
    
    -- Billing
    balance DECIMAL(10,2) DEFAULT 0.00 COMMENT 'Account balance',
    
    -- Relationships
    FOREIGN KEY (plan_id) REFERENCES plans(id),
    
    -- Indexes
    INDEX idx_username (username),
    INDEX idx_active (is_active),
    INDEX idx_connection_type (connection_type),
    INDEX idx_expires (expires_at)
) COMMENT 'User accounts and customer information';

-- =====================================================
-- 3. SESSIONS TABLE (Active connections tracking)
-- =====================================================
CREATE TABLE sessions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    
    -- User information
    user_id INT NOT NULL,
    username VARCHAR(50) NOT NULL,
    
    -- Connection details
    connection_type ENUM('pppoe', 'hotspot') NOT NULL,
    ip_address VARCHAR(45) COMMENT 'IPv4 or IPv6 address',
    mac_address VARCHAR(17),
    nas_ip_address VARCHAR(45) COMMENT 'Network Access Server IP',
    
    -- Session timing
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP NULL,
    session_duration INT DEFAULT 0 COMMENT 'Duration in seconds',
    
    -- Data usage (in bytes)
    bytes_in BIGINT DEFAULT 0 COMMENT 'Downloaded bytes',
    bytes_out BIGINT DEFAULT 0 COMMENT 'Uploaded bytes',
    
    -- Session status
    session_status ENUM('active', 'stopped', 'timeout') DEFAULT 'active',
    terminate_cause VARCHAR(50),
    
    -- Relationships
    FOREIGN KEY (user_id) REFERENCES users(id),
    
    -- Indexes
    INDEX idx_user_sessions (user_id, start_time),
    INDEX idx_active_sessions (session_status, start_time),
    INDEX idx_username (username)
) COMMENT 'Real-time session tracking for active connections';

-- =====================================================
-- 4. ACCOUNTING TABLE (Historical usage data)
-- =====================================================
CREATE TABLE accounting (
    id INT PRIMARY KEY AUTO_INCREMENT,
    
    -- User information
    user_id INT NOT NULL,
    username VARCHAR(50) NOT NULL,
    
    -- Session details
    session_id VARCHAR(50),
    connection_type ENUM('pppoe', 'hotspot') NOT NULL,
    
    -- Timing
    session_start TIMESTAMP NOT NULL,
    session_end TIMESTAMP,
    session_time INT DEFAULT 0 COMMENT 'Total session time in seconds',
    
    -- Data usage
    bytes_in BIGINT DEFAULT 0,
    bytes_out BIGINT DEFAULT 0,
    total_bytes BIGINT GENERATED ALWAYS AS (bytes_in + bytes_out) STORED,
    
    -- Network details
    ip_address VARCHAR(45),
    nas_ip_address VARCHAR(45),
    
    -- Billing
    cost DECIMAL(10,2) DEFAULT 0.00,
    
    -- Termination
    terminate_cause VARCHAR(50),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Relationships
    FOREIGN KEY (user_id) REFERENCES users(id),
    
    -- Indexes for reporting
    INDEX idx_user_accounting (user_id, session_start),
    INDEX idx_date_range (session_start, session_end),
    INDEX idx_username (username)
) COMMENT 'Historical accounting data for billing and reporting';

-- =====================================================
-- 5. SYSTEM SETTINGS TABLE (Configuration)
-- =====================================================
CREATE TABLE system_settings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    description TEXT,
    setting_type ENUM('string', 'integer', 'boolean', 'json') DEFAULT 'string',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_setting_key (setting_key)
) COMMENT 'System configuration settings';
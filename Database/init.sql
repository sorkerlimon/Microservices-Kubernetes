CREATE DATABASE IF NOT EXISTS appdb;
CREATE USER 'user'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON appdb.* TO 'user'@'%';
FLUSH PRIVILEGES;

USE appdb;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO users (name, email, phone) VALUES
    ('John Doe', 'john@example.com', '555-1234'),
    ('Jane Smith', 'jane@example.com', '555-5678'),
    ('Bob Johnson', 'bob@example.com', '555-9012');

USE mysql;
SET FOREIGN_KEY_CHECKS = 0;
DROP DATABASE IF EXISTS portal_db;
SET FOREIGN_KEY_CHECKS = 1;
CREATE DATABASE portal_db;
USE portal_db;
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) NOT NULL UNIQUE,
  login_id VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  role ENUM('student','employee','manager','entrepreneur','jobseeker') NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  email VARCHAR(150),
  mobile VARCHAR(20),
  gender ENUM('male','female','other'),
  current_location VARCHAR(200),
  permanent_address VARCHAR(300),
  college_name VARCHAR(200),
  school_name VARCHAR(200),
  photo LONGBLOB,
  resume LONGBLOB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_student_user FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
);
SELECT * FROM users;
SELECT * FROM students;

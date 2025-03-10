CREATE DATABASE IF NOT EXISTS flask_blog_db;
USE flask_blog_db;

CREATE TABLE Contacts (
    sno INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(80) NOT NULL,
    email VARCHAR(50) NOT NULL,
    ph_no VARCHAR(15) NOT NULL,
    msg TEXT NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Posts (
    sno INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(80) NOT NULL,
    slug VARCHAR(50) NOT NULL UNIQUE,
    content TEXT NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    img_file VARCHAR(255)
);

CREATE TABLE User (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

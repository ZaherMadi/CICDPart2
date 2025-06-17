CREATE DATABASE ynov_ci; 
USE ynov_ci;
CREATE TABLE IF NOT EXISTS utilisateur (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(100),
  email VARCHAR(100)
);

INSERT INTO utilisateur (nom, email)
VALUES ('Zaher', 'zaher.madi@ynov.fr'),
       ('Test', 'test@example.fr');
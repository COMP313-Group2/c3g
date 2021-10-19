-- SQLite3 db
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS games;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE games (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
	userId INTEGER,
	name TEXT NOT NULL,
  FOREIGN KEY(userId) REFERENCES users(id)
);

-- Initialize data in db with example data
/* INSERT INTO users (name, email, password) */ 
/* 	VALUES ("hassan", "hassan149367@gmail.com", "Password0!"); */
/* INSERT INTO games (userId, name) */ 
/* 	VALUES (1, "blade_runner"); */


-- SQLite3 db
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS games;

CREATE TABLE users (
  userId INTEGER PRIMARY KEY AUTOINCREMENT,
  userName TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE games (
  gameId INTEGER PRIMARY KEY AUTOINCREMENT,
	userId INTEGER,
	gameName TEXT NOT NULL,
  FOREIGN KEY(userId) REFERENCES users(userId)
);

-- Initialize data in db with example data
INSERT INTO users (userName, email, password) 
	VALUES ("hassan", "hassan149367@gmail.com", "Password0!");
INSERT INTO games (userId, gameName) 
	VALUES (1, "Blade Runner");
INSERT INTO games (userId, gameName) 
	VALUES (1, "Excalibur's Quest");


INSERT INTO users (userName, email, password) 
	VALUES ("sarmad", "sarmad@gmail.com", "Password0!");
INSERT INTO games (userId, gameName) 
	VALUES (2, "Space Pong");


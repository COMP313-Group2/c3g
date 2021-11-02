-- SQLite3 db
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS stars;
DROP TABLE IF EXISTS comments;

CREATE TABLE users (
  userId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  userName TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE games (
  gameId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	userId INTEGER,
	gameName TEXT NOT NULL,
  FOREIGN KEY(userId) REFERENCES users(userId)
);

CREATE TABLE stars (
	userId INTEGER NOT NULL,
  gameId INTEGER NOT NULL,
	star INTEGER NOT NULL,
  PRIMARY KEY(userId, gameId),
  FOREIGN KEY(userId) REFERENCES users(userId),
  FOREIGN KEY(gameId) REFERENCES games(gameId)
);

CREATE TABLE comments (
	userId INTEGER NOT NULL,
  gameId INTEGER NOT NULL,
  date DATE DEFAULT CURRENT_TIMESTAMP,
	comment TEXT,
  FOREIGN KEY(userId) REFERENCES users(userId),
  FOREIGN KEY(gameId) REFERENCES games(gameId)
);

-- Future tables:
-- comments: __userid, gameid, date__, commentstring

-- Initialize data in db with example data
--INSERT INTO users (userName, email, password) 
	--VALUES ("hassan", "hassan149367@gmail.com", "Password0!");
--INSERT INTO games (userId, gameName) 
	--VALUES (1, "Blade Runner");
--INSERT INTO games (userId, gameName) 
	--VALUES (1, "Excalibur's Quest");
--
--
--INSERT INTO users (userName, email, password) 
	--VALUES ("sarmad", "sarmad@gmail.com", "Password0!");
--INSERT INTO games (userId, gameName) 
	--VALUES (2, "Space Pong");


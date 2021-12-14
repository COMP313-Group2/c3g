-- constraints not enforced by the db, and enabling it causes other issues
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS stars;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS tickets;

CREATE TABLE users (
  userId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	userName TEXT NOT NULL,
	userNameFirstChar TEXT AS (substr(userName,1,1)),
	role TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
	deleted BOOLEAN NOT NULL CHECK (deleted IN (0,1)) DEFAULT 0,
	country TEXT NOT NULL
);

CREATE TABLE admin (
	userId INTEGER NOT NULL PRIMARY KEY,
  date DATE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE games (
  gameId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	userId INTEGER,
	gameName TEXT NOT NULL,
	imageName TEXT NOT NULL,
	description TEXT NOT NULL,
	status INTEGER NOT NULL CHECK (status IN (0,1,2)) DEFAULT 2, -- 0 none, 1 deleted, 2 pending
  FOREIGN KEY(userId) REFERENCES users(userId) ON DELETE CASCADE
);

CREATE TABLE stars (
	userId INTEGER NOT NULL,
  gameId INTEGER NOT NULL,
	star INTEGER NOT NULL,
  PRIMARY KEY(userId, gameId),
  FOREIGN KEY(userId) REFERENCES users(userId) ON DELETE CASCADE,
  FOREIGN KEY(gameId) REFERENCES games(gameId) ON DELETE CASCADE
);

CREATE TABLE comments (
  commentId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	userId INTEGER NOT NULL,
  gameId INTEGER NOT NULL,
  date DATE DEFAULT CURRENT_TIMESTAMP,
	comment TEXT,
	commentIdRef INTEGER,
  FOREIGN KEY(commentIdRef) REFERENCES comments(commentId) ON DELETE CASCADE,
  FOREIGN KEY(userId) REFERENCES users(userId) ON DELETE CASCADE,
  FOREIGN KEY(gameId) REFERENCES games(gameId) ON DELETE CASCADE
);

CREATE TABLE tickets (
  ticketId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	userId INTEGER NOT NULL,
  date DATE DEFAULT CURRENT_TIMESTAMP,
	comment TEXT,
	resolved BOOLEAN NOT NULL CHECK (resolved IN (0,1)) DEFAULT 0,
	ticketIdRef INTEGER,
  FOREIGN KEY(ticketsIdRef) REFERENCES tickets(ticketsIdRef) ON DELETE CASCADE,
  FOREIGN KEY(userId) REFERENCES users(userId) ON DELETE CASCADE
);

-- Default values for system users
INSERT INTO users (userName, role, email, password, country) 
	VALUES ('admin', 'admin', 'admin@gmail.com', 'Password0)', 'CA');
INSERT INTO users (userName, role, email, password, country) 
	VALUES ('tech', 'tech', 'tech@gmail.com', 'Password0)', 'CA');

-- Testing values
INSERT INTO users (userName, role, email, password, country) 
	VALUES ('Hassan Shabbir', 'dev', 'hassan149367@gmail.com', 'Password0)', 'CA');
INSERT INTO users (userName, role, email, password, country) 
	VALUES ('Sarmad', 'player', 'sarmad@gmail.com', 'Password0)', 'CA');

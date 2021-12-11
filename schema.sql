-- constraints not enforced by the db, and enabling it causes other issues
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS stars;
DROP TABLE IF EXISTS comments;

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

/* TODO: work on creating a reply system */
/* drop table if exists rec; */
/* create table rec ( recId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, data TEXT, recIdRef INTEGER); */
/* insert into rec (recId, data) values (1, 'hi'); insert into rec (recId, data) values (3, 'meh'); insert into rec (recId, data) values (4, 'good job!'); insert into rec (recId, recIdRef, data) values (2, 1, 'hey'); insert into rec (recId, recIdRef, data) values (5, 4, 'thanks!'); insert into rec (recId, recIdRef, data) values (6, 3, 'who hurt you?'); insert into rec (recId, recIdRef, data) values (7, 3, 'yeah, who?'); */
/* select * from rec; */
/* select r.recId, r.data, ifnull(c.recId, r.recId) as grp, ifnull(c.recId, r.recId) <> r.recId as reply from rec r left outer join rec c on r.recIdRef = c.recId order by grp, c.recId; */


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
/* INSERT INTO comments (commentId, userId, gameId, date, comment, commentIdRef) VALUES (1, 4, 2, '20-FEB-10', 'cool game', NULL), (3, 5, 2, '20-FEB-10', 'thanks!', 1), (2, 4, 2, '20-FEB-10', 'love it!', NULL), (4, 6, 2, '20-FEB-10', 'yeah, it''s a great game', 1), (5, 3, 3, '20-FEB-10', 'rando game', NULL); */
/* SELECT a.commentId, a.userId, a.gameId, a.date, a.comment, a.commentIdRef, b.userId, b.date, b.comment, ifnull(a.commentIdRef, a.commentId) AS grp, ifnull(a.commentIdRef, a.commentId) <> a.commentId AS reply FROM comments AS a LEFT OUTER JOIN comments AS b ON a.commentIdRef = b.commentId WHERE a.gameId = 2 ORDER BY grp DESC, a.date ASC; */

/* ORDER BY ifnull(a.commentIdRef, a.commentId) DESC, b.date ASC; */
/* ifnull(a.commentIdRef, a.commentId) AS ord */
/* ORDER BY ifnull(a.commentIdRef, a.commentId); */

/* SELECT a.commentId AS acommentId, userName, a.date AS adate, a.comment AS acomment, a.commentIdRef, ifnull(a.commentIdRef, a.commentId), ifnull(a.commentIdRef, a.commentId) <> a.commentId AS reply, */
/* CASE */ 
/* 	WHEN a.commentIdRef IS NULL THEN a.commentId */
/* 	WHEN a.commentIdRef IS NOT NULL THEN ifnull((SELECT commentIdRef FROM comments WHERE commentId = a.commentIdRef), a.commentIdRef) */
/* END AS cs */
/* FROM comments AS a LEFT OUTER JOIN comments AS b ON a.commentIdRef = b.commentId JOIN users on users.userId = a.userId */
/* ORDER BY cs; */






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


/* insert into users (userId, userName, role, email, password) values (1, "hassan", "player", "hassan@gmail.com", "Password0)"); */
/* insert into games (gameId, userId, gameName, description) values (1,1,"space pong", "pong in space"); */

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


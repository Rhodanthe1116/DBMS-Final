/* create and use database */
DROP SCHEMA IF EXISTS mydb;
CREATE DATABASE mydb;
USE mydb;

/* create table */
CREATE TABLE Manager (
    manager_id INT PRIMARY KEY NOT NULL CHECK (manager_id > 0),
    name varchar(10) NOT NULL,
    age INT NOT NULL,
    nationality varchar(20),
    contract_date Date DEFAULT '2024-04-02'
);
/* insert */
INSERT INTO Manager
VALUES 
('1', 'Jackson', 45, 'USA', '2025-08-02'),
('2', 'Alex', 53, 'Japan', '2026-11-12'),
('3', 'Martin', 48, 'Korea', '2024-09-23');


/* create table */
CREATE TABLE ManagerResponsibility(
    id INT PRIMARY KEY NOT NULL,
    manager_id INT NOT NULL,
    responsibility varchar(20) DEFAULT 'recruitment' NOT NULL,
    FOREIGN KEY (manager_id) REFERENCES Manager(manager_id) 
);

/* insert */
INSERT INTO ManagerResponsibility
VALUES 
('1', '2', 'stragegy'),
('2', '3', 'recruitment'),
('3', '3', 'coaching'),
('4', '1', 'marketing');

/* create table */
CREATE TABLE Team(
    team_id INT PRIMARY KEY NOT NULL,
    team_name varchar(10) NOT NULL,
    established_date Date DEFAULT '1990-01-01',
    city varchar(10) NOT NULL,
    manager_id INT NOT NULL CHECK (manager_id > 0),
    FOREIGN KEY (manager_id) REFERENCES Manager(manager_id)
);

/* insert */
INSERT INTO Team
VALUES
('1', 'Yankees', '1890-11-22', 'New York', '1'),
('2', 'Dodger', '1920-12-11', 'LA', '2'),
('3', 'Red sox', '1940-08-01', 'Boston', '3');

/* create table */
CREATE TABLE Player(
    player_id INT PRIMARY KEY NOT NULL CHECK (player_id > 0),
    name varchar(10) NOT NULL,
    age INT NOT NULL,
    nationality varchar(20) DEFAULT 'USA',
    defend_role ENUM ('pitcher', 'catcher') DEFAULT 'pitcher' NOT NULL,
    team_id INT NOT NULL CHECK (team_id > 0),
    FOREIGN KEY (team_id) REFERENCES Team(team_id)
);

/* insert */
INSERT INTO Player
VALUES
('1', 'Otani', 25, 'Japan', 'pitcher', '2'),
('2', 'Kershaw', 31, 'USA', 'pitcher', '1'),
('3', 'Valender', 35, 'USA', 'catcher', '3'),
('4', 'Tax', 33, 'USA', 'catcher', '3');

/* create table */
CREATE TABLE Game(
    game_id INT PRIMARY KEY NOT NULL CHECK (game_id > 0),
    game_location varchar(10) NOT NULL,
    game_date Date NOT NULL,
    start_time Time NOT NULL DEFAULT '17:00:00',
    end_time Time NOT NULL DEFAULT '20:00:00',
    team1_id INT NOT NULL CHECK (team1_id > 0),
    team2_id INT NOT NULL CHECK (team2_id > 0),
    FOREIGN KEY (team1_id) REFERENCES Team(team_id),
    FOREIGN KEY (team2_id) REFERENCES Team(team_id)
);

/* insert */
INSERT INTO Game
VALUES
('1', 'New York', '2024-04-01', '17:00:00', '20:00:00', '1', '2'),
('2', 'LA', '2024-04-02', '18:30:00', '20:30:00', '2', '3'),
('3', 'Boston', '2024-04-03', '17:00:00', '21:11:25', '3', '1');

/* create table */
CREATE TABLE DefendPosition(
    position_id INT PRIMARY KEY NOT NULL,
    position_name ENUM ('L-O', 'R-O', 'M-O', 'F-I', 'S-I', 'T-I', 'C', 'P', 'F') NOT NULL DEFAULT 'L-O',
    defend_range INT NOT NULL DEFAULT '5',
    speed INT NOT NULL DEFAULT '5',
    defend_role ENUM ('Infielder', 'Outfielder') NOT NULL DEFAULT 'Infielder',
    noted varchar(20)
);

/* insert */
INSERT INTO DefendPosition
VALUES
('1', 'L-O', '15', '10', 'Outfielder', 'Left Outfielder'),
('2', 'R-O', '12', '8', 'Outfielder', 'Right Outfielder'),
('3', 'M-O', '10', '6', 'Outfielder', 'Middle Outfielder'),
('4', 'F-I', '5', '3', 'Infielder', '1st base infielder'),
('5', 'S-I', '5', '3', 'Infielder', '2nd base infielder'),
('6', 'T-I', '5', '3', 'Infielder', '3rd base infielder'),
('7', 'C', '5', '3', 'Infielder', 'Catcher'),
('8', 'P', '5', '3', 'Infielder', 'Pitcher');



/* create table */
CREATE TABLE Injury(
    injury_id INT NOT NULL,
    player_id INT NOT NULL,
    recover_time ENUM('2w','1m','3m','6m','1y') NOT NULL DEFAULT '2w',
    noted varchar(20),
    FOREIGN KEY (player_id) REFERENCES Player(player_id),
    PRIMARY KEY (player_id, injury_id)
);

/* insert */
INSERT INTO Injury
VALUES
('1', '1', '2w', 'ankle sprain'),
('2', '1', '1m', 'shoulder pain'),
('3', '3', '1y', 'knee pain');

/* create table */
CREATE TABLE PlayinGame(
    player_id INT NOT NULL,
    game_id INT NOT NULL DEFAULT '1',
    FOREIGN KEY (player_id) REFERENCES Player(player_id),
    FOREIGN KEY (game_id) REFERENCES Game(game_id),
    PRIMARY KEY (player_id, game_id)
);

/* insert */
INSERT INTO PlayinGame
VALUES
('1', '1'),
('2', '1'),
('3', '2');

/* create table */
CREATE TABLE TeamWLGame(
    game_id INT NOT NULL,
    team_id INT NOT NULL DEFAULT '1',
    win_loss ENUM('win', 'loss', 'tie') DEFAULT 'tie',
    FOREIGN KEY (game_id) REFERENCES Game(game_id),
    FOREIGN KEY (team_id) REFERENCES Team(team_id),
    PRIMARY KEY (game_id, team_id)
);

/* insert */
INSERT INTO TeamWLGame
VALUES
('1', '1', 'win'),
('1', '2', 'loss'),
('2', '3', 'tie');

/* create table */
CREATE TABLE PlayerRelationship(
    player1_id INT NOT NULL,
    player2_id INT NOT NULL,
    relationship ENUM('senior','junior') DEFAULT 'senior',
    FOREIGN KEY (player1_id) REFERENCES Player(player_id),
    FOREIGN KEY (player2_id) REFERENCES Player(player_id),
    PRIMARY KEY (player1_id, player2_id)
);

/* insert */
INSERT INTO PlayerRelationship
VALUES
('1', '2', 'senior'),
('2', '1', 'junior'),
('1', '3', 'senior');

/* create table */
CREATE TABLE PlayerinPosition(
    player_id INT NOT NULL CHECK (player_id > 0),
    position_id INT NOT NULL DEFAULT '1',
    FOREIGN KEY (player_id) REFERENCES Player(player_id),
    FOREIGN KEY (position_id) REFERENCES DefendPosition(position_id),
    PRIMARY KEY (player_id, position_id)
);

/* insert */
INSERT INTO PlayerinPosition
VALUES
('1', '1'),
('2', '2'),
('3', '3');

/* create table */
CREATE TABLE Infielder(
    infielder_id INT PRIMARY KEY NOT NULL,
    position_id INT NOT NULL,
    blocking_rate INT NOT NULL DEFAULT '90',
    FOREIGN KEY (position_id) REFERENCES DefendPosition(position_id)
);

/* insert */
INSERT INTO Infielder
VALUES
('1', '4', '85'),
('2', '5', '92'),
('3', '6', '90');

/* create table */
CREATE TABLE Outfielder(
    outfielder_id INT PRIMARY KEY NOT NULL,
    position_id INT NOT NULL,
    catching_rate INT NOT NULL DEFAULT '90',
    FOREIGN KEY (position_id) REFERENCES DefendPosition(position_id)
);

/* insert */
INSERT INTO Outfielder
VALUES
('1', '1', '85'),
('2', '2', '92'),
('3', '3', '90');


/* create two views (Each view should be based on two tables.)*/
CREATE VIEW ManagerView AS
SELECT
    M.manager_id,
    M.name AS manager_name,
    M.age,
    MR.responsibility
FROM
    Manager M
JOIN
    ManagerResponsibility MR ON M.manager_id = MR.manager_id;

CREATE VIEW PlayerGameView AS
SELECT
    P.player_id,
    P.name AS player_name,
    G.game_id,
    T.team_name,
    TWL.win_loss
FROM
    Player P
JOIN
    PlayinGame PG ON P.player_id = PG.player_id
JOIN
    Game G ON PG.game_id = G.game_id
JOIN
    Team T ON P.team_id = T.team_id
JOIN
    TeamWLGame TWL ON G.game_id = TWL.game_id AND T.team_id = TWL.team_id;


SELECT * FROM self;
SELECT * FROM Manager;
SELECT * FROM ManagerResponsibility;
SELECT * FROM Team;
SELECT * FROM Player;
SELECT * FROM Game;
SELECT * FROM DefendPosition;
SELECT * FROM Injury;
SELECT * FROM PlayinGame;
SELECT * FROM TeamWLGame;
SELECT * FROM PlayerRelationship;
SELECT * FROM PlayerinPosition;
SELECT * FROM Infielder;
SELECT * FROM Outfielder;

SELECT * FROM ManagerView;
SELECT * FROM PlayerGameView;

/***** homework 3 commands *****/

/* basic select */
SELECT * FROM Player WHERE NOT nationality = 'Japan' AND age > 31 OR defend_role='catcher';
/* basic projection */
SELECT name, age FROM Player;
/* basic rename */
SELECT name AS player, nationality AS nation FROM Player AS P WHERE P.age > 30;

/* equijoin */
SELECT P.name, team_name, city 
FROM Player AS P JOIN Team ON P.team_id = Team.team_id;
/* natural join */
SELECT P.name, T.team_name, T.city 
FROM Player AS P NATURAL JOIN Team AS T;
/* theta join */
SELECT G.game_id, G.game_location, G.game_date, team_name 
FROM Game AS G JOIN Team ON G.team2_id < Team.team_id AND G.team1_id = Team.team_id;
/* three table join */
SELECT P.name, T.team_name, G.game_location, G.game_date 
FROM Player AS P JOIN PlayinGame AS PG ON P.player_id = PG.player_id JOIN Game AS G ON PG.game_id = G.game_id JOIN Team AS T ON P.team_id = T.team_id;

/* aggregate */
SELECT team_id, COUNT(*), MAX(nationality), MIN(nationality) 
FROM Player GROUP BY team_id;
/* aggregate 2 */
SELECT team_id, AVG(age), SUM(age), COUNT(*) 
FROM Player GROUP BY team_id HAVING AVG(age) > 30;

/* in */
SELECT name, age FROM Player WHERE age IN (25, 31, 35);
/* in 2 */
SELECT name, age FROM Player WHERE age IN (SELECT age FROM Player WHERE team_id = 3);

/* correlated nested query */
SELECT name, age FROM Player AS P 
WHERE P.team_id IN (SELECT team_id FROM Team WHERE team_name = 'Yankees');
/* correlated nested query 2 */
SELECT name, age FROM Player AS P 
WHERE EXISTS (SELECT * FROM Team 
WHERE team_id = P.team_id AND team_name = 'Yankees');
/* correlated nested query 3 */
SELECT name, age FROM Player AS P 
WHERE NOT EXISTS (SELECT * FROM Team 
WHERE team_id = P.team_id AND team_name = 'Yankees');


CREATE TABLE t1 (a INT, b INT);
INSERT INTO t1 VALUES ROW(4,2), ROW(3,4);
CREATE TABLE t2 (a INT, b INT);
INSERT INTO t2 VALUES ROW(1,2), ROW(3,4);
/* union */
SELECT * FROM t1 UNION SELECT * FROM t2;
/* intersect */
SELECT * FROM t1 INTERSECT SELECT * FROM t2;
/* difference */
SELECT * FROM t1 EXCEPT SELECT * FROM t2;


CREATE TABLE student(ID INT, YEAR INT);
INSERT INTO student VALUES ROW(11, 3), 
ROW(12,3), ROW(13,4), ROW(14,4) ;
CREATE TABLE staff(ID INT, RANKING INT);
INSERT INTO staff VALUES ROW(15,22), 
ROW(16,23);
/* advance */
SELECT st.ID, st.YEAR, sf.RANKING FROM student AS st
LEFT JOIN staff AS sf ON st.ID = sf.ID
UNION
SELECT sf.ID, st.YEAR, sf.RANKING FROM student AS st
RIGHT JOIN staff AS sf ON st.ID = sf.ID;
/*  advance 2 */
SELECT DISTINCT sf.ID, st.YEAR, sf.RANKING FROM staff AS sf
LEFT JOIN student AS st ON st.ID = sf.ID;


/* drop database */
DROP DATABASE BaseballDB;
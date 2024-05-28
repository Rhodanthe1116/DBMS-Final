DROP DATABASE IF EXISTS mydb;

CREATE DATABASE mydb;

USE mydb;

-- posts	  users	     categories	category_post
-- id  	  id 	     id	          category_id
-- user_id  username	title	     post_id
-- title			
-- body	
CREATE TABLE
     IF NOT EXISTS posts (
          id VARCHAR(255),
          user_id VARCHAR(255),
          title VARCHAR(255),
          body VARCHAR(255)
     );

INSERT INTO
     posts (title)
VALUES
     ('投稿1');

CREATE TABLE
     IF NOT EXISTS users (id VARCHAR(255), username VARCHAR(255));

INSERT INTO
     users (username)
VALUES
     ('使用者1')
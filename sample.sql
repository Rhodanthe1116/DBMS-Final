DROP DATABASE IF EXISTS mydb;

CREATE DATABASE mydb;

USE mydb;


-- posts	  users	     categories	category_post
-- id  	  id 	     id	          category_id
-- user_id  username	title	     post_id
-- title			
-- body	


CREATE TABLE
     IF NOT EXISTS users (
          id VARCHAR(255),
          username VARCHAR(255),
          PRIMARY KEY (id)
     );


INSERT INTO
     users (id, username)
VALUES
     ('1', '使用者1');
     


CREATE TABLE
     IF NOT EXISTS posts (
          id VARCHAR(255),
          user_id VARCHAR(255),
          title VARCHAR(255),
          PRIMARY KEY (id),
          FOREIGN KEY (user_id) REFERENCES users (id)
     );
     

INSERT INTO
     posts (id, user_id, title)
VALUES
     ('1', '1', '投稿1'),
     ('2', '1', '投稿2');


COMMIT;

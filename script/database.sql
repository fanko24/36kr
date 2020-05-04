CREATE TABLE article_success(
    aid int AUTO_INCREMENT,
    id bigint NOT NULL,
    old_id int NOT NULL,
    title varchar(200), 
    summary varchar(500),
    author_id int DEFAULT 0, 
    publish_time bigint DEFAULT 0, 
    content mediumtext,
    type varchar(50),
    create_time datetime DEFAULT CURRENT_TIMESTAMP, 
    update_time datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
    primary key(id),
    index(id),  
    index(aid)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE article_fail(
    aid int AUTO_INCREMENT, 
    old_id int NOT NULL,
    type int NOT NULL DEFAULT 0,
    is_delete int DEFAULT 0,
    create_time datetime DEFAULT CURRENT_TIMESTAMP, 
    update_time datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
    primary key(old_id), 
    index(old_id), 
    index(aid)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE article_pass(
    aid int AUTO_INCREMENT, 
    old_id int NOT NULL,
    is_delete int DEFAULT 0, 
    create_time datetime DEFAULT CURRENT_TIMESTAMP, 
    update_time datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
    primary key(old_id), 
    index(old_id), 
    index(aid)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


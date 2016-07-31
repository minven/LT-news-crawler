CREATE DATABASE lt_news CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
CREATE TABLE news_sources (
    name varchar(50) DEFAULT NULL,
    page_id varchar(50) DEFAULT NULL,
    page_name varchar(255) DEFAULT NULL,
    PRIMARY KEY(id)
    );
CREATE TABLE news_posts (
    page_id varchar(50) not null,
    post_id varchar(50) not null,
    post_time datetime DEFAULT NULL,
    post varchar(1024) not null,
    post_url varchar(255) not null,
    fb_post_url varchar(255) not null,
    comments_numb int(4) default 0,
    UNIQUE KEY `uni_id` (`post_id`)
    );
CREATE TABLE comments (
    post_id varchar(50) not null,
    comment_id varchar(50) not null,
    commenter varchar(100) not null,
    commenter_id varchar(50) not null,
    comment_time datetime DEFAULT NULL,
    comment varchar(1024) not null,
    comment_count int(3) DEFAULT 0,
    comment_likes int(5) DEFAULT 0,
    app_name varchar(20) DEFAULT NULL,
    app_id varchar(50) DEFAULT NULL, 
    UNIQUE KEY `uni_id` (`comment_id`)
    );
-- RUN THIS ON ROOT
-- create user
CREATE USER project127 IDENTIFIED BY 'secret123';
-- create database
CREATE DATABASE project127;
-- granting access to user
GRANT ALL PRIVILEGES ON project127.* TO project127;

-- Go to project127 db
USE project127;
-- CREATING THE TABLES
-- defining user table
CREATE TABLE users (
    username VARCHAR(20) NOT NULL,
    first_name VARCHAR(15) NOT NULL,
    last_name VARCHAR(15) NOT NULL,
    PRIMARY KEY(username)
);
-- defining single transaction
CREATE TABLE transactions (    
    tid MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
    amount DECIMAL(10, 2) NOT NULL, 
    contribution DECIMAL(10, 2) NOT NULL DEFAULT 0,
    category VARCHAR(10) NOT NULL,
    date_created DATE NOT NULL,
    payer_username VARCHAR(20) NOT NULL,
    is_settled BOOLEAN NOT NULL DEFAULT 0,
    transaction_description TINYTEXT NOT NULL,
    PRIMARY key(tid),
    CONSTRAINT username_fk FOREIGN KEY(payer_username) REFERENCES users(username)
);

-- relationships
-- defining friend list
CREATE TABLE friends (
    username VARCHAR(20) NOT NULL,
    friend VARCHAR(20) NOT NULL,
    PRIMARY KEY(username, friend),
    CONSTRAINT friends_username_fk FOREIGN KEY(username) REFERENCES users(username),
    CONSTRAINT friends_friend_fk FOREIGN KEY(friend) REFERENCES users(username)
);

-- defining group 
CREATE TABLE groups (
    gid MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
    group_name VARCHAR(30) NOT NULL,
    PRIMARY KEY(gid)
);

-- defining group members
CREATE TABLE group_members (
    gid MEDIUMINT UNSIGNED NOT NULL,
    username VARCHAR(20) NOT NULL,
    PRIMARY KEY(gid, username),
    CONSTRAINT group_members_gid_fk FOREIGN KEY(gid) REFERENCES groups(gid),
    CONSTRAINT group_members_username_fk FOREIGN KEY(username) REFERENCES users(username)
);

-- defining group transactions
CREATE TABLE group_transactions (
    tid MEDIUMINT UNSIGNED NOT NULL,
    gid MEDIUMINT UNSIGNED NOT NULL,
    PRIMARY KEY(gid, tid),
    CONSTRAINT group_transactions_gid_fk FOREIGN KEY(gid) REFERENCES groups(gid),
    CONSTRAINT group_transactions_tid_fk FOREIGN KEY(tid) REFERENCES transactions(tid)
);

-- defining transactions with users
CREATE TABLE users_has_transactions (
    tid MEDIUMINT UNSIGNED NOT NULL,
    username VARCHAR(20) NOT NULL,
    paid BOOLEAN NOT NULL DEFAULT 0,
    PRIMARY KEY(tid, username),
    CONSTRAINT users_has_transactions_tid_fk FOREIGN KEY(tid) REFERENCES transactions(tid),
    CONSTRAINT users_has_transactions_username_fk FOREIGN KEY(username) REFERENCES users(username)
);
DROP TABLE IF EXISTS person;

CREATE TABLE person(
    name TEXT PRIMARY KEY NOT NULL,
    phone_no VARCHAR(20),
    email TEXT,
    picture BLOB
);
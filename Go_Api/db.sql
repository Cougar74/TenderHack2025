-- Create the library database.
CREATE DATABASE TenderHack;

-- Create tables.
CREATE TABLE Classifications (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);
CREATE TABLE Histories (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    query VARCHAR(255) NOT NULL,
    classificationId integer NULL,
    responce VARCHAR(4000) NULL,
    rating integer null,
    dateTimeCreate timestamp  default (now() at time zone 'utc') not null,
    FOREIGN KEY (classificationId) REFERENCES classifications (Id)

);


-- Create the library database.
CREATE DATABASE TenderHack;

-- Create tables.
CREATE TABLE Classifications (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Histories (
    id SERIAL PRIMARY KEY,
    user_uuid uuid NOT NULL,
    query VARCHAR(255) NOT NULL,
    classification_id integer NULL,
    responce VARCHAR(4000) NULL,
    rating integer null,
    date_time_create timestamp  default (now() at time zone 'utc') not null,
    FOREIGN KEY (classification_id) REFERENCES classifications (id)

);


--ADD DATA
INSERT INTO public.classifications(id,name) VALUES 
(1,'Вопросы о регистрации и управлении учетными записями'),
(2,'Котировочные сессии и закупки'),
(3,'Ошибки сайта'),
(4,'Работа с контрактами'),
(5,'Справочная информация и поддержка'),
(6,'Стандартные товарные единицы (СТЕ)'),
(7,'Технические вопросы и настройки');

-- phpMyAdmin SQL Dump
-- version 3.5.1
-- http://www.phpmyadmin.net
--
-- Хост: 127.0.0.1
-- Время создания: Ноя 14 2024 г., 14:07
-- Версия сервера: 5.5.25
-- Версия PHP: 5.3.13

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- База данных: `book`
--

CREATE DATABASE IF NOT EXISTS `forum` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `forum`;

-- --------------------------------------------------------

--
-- Структура таблицы `person`
--


CREATE TABLE IF NOT EXISTS authors (
    id INT(11) NOT NULL AUTO_INCREMENT,
    name TINYTEXT NOT NULL,
    passw TINYTEXT NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,  -- Changed to VARCHAR(255)
    url TEXT,
    about TEXT,
    photo TINYTEXT,
    putdate DATETIME DEFAULT NULL,
    last_time DATETIME DEFAULT NULL,
    statususer ENUM('user', 'moderator', 'admin') NOT NULL DEFAULT 'user',
    PRIMARY KEY (id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8 AUTO_INCREMENT = 1;


CREATE TABLE IF NOT EXISTS `sections` (
    id INT(11) NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    rule TEXT,
    logo TINYTEXT,
    pos INT(11) DEFAULT NULL,
    hide ENUM('show', 'hide') NOT NULL DEFAULT 'show',
    PRIMARY KEY (id)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;

CREATE TABLE IF NOT EXISTS themes (
    id INT(11) NOT NULL AUTO_INCREMENT,
    name TINYTEXT NOT NULL,
    id_author INT(11) NOT NULL,
    hide ENUM('show', 'hide') NOT NULL DEFAULT 'show',
    putdate DATETIME DEFAULT NULL,
    forum_id INT(11) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_author) REFERENCES authors(id) ON DELETE CASCADE,
    FOREIGN KEY (forum_id) REFERENCES sections(id) ON DELETE CASCADE
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;

CREATE TABLE IF NOT EXISTS posts (
    id INT(11) NOT NULL AUTO_INCREMENT,
    name TEXT NOT NULL,  -- Changed to TEXT to accommodate longer posts
    url TEXT,
    file TINYTEXT,
    author_id INT(11) NOT NULL,
    hide ENUM('show', 'hide') NOT NULL DEFAULT 'show',
    putdate DATETIME DEFAULT NULL,
    parent_post INT(11) DEFAULT NULL,
    theme_id INT(11) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE,
    FOREIGN KEY (theme_id) REFERENCES themes(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_post) REFERENCES posts(id) ON DELETE SET NULL -- Allows deleting parent post without deleting replies
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;

INSERT INTO authors (name, passw, email, url, about, photo, putdate, last_time, statususer) VALUES
('Иван Иванов', '123456', 'ivan@example.com', 'ivan', 'О себе...', 'photo1.jpg', NOW(), NOW(), 'user'),
('Петр Петров', '123456', 'petr@example.com', 'petr', 'Информация о Петре', 'photo2.png', NOW(), NOW(), 'moderator'),
('Сидор Сидоров', '123456', 'sidr@example.com', 'sidor', 'Биография Сидора', NULL, NOW(), NOW(), 'admin');




DROP DATABASE `library`;
CREATE DATABASE `library`;
USE `library`;

CREATE TABLE `kitapsec` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `current_price` DOUBLE(7, 2),
  `original_price` DOUBLE(7, 2),
  `quantity` INTEGER,
  `score` DOUBLE(2, 1),
  `link` VARCHAR(300),
  `image` VARCHAR(300), 
  -- These below are later to be dropped. --
  `name` VARCHAR(300) NOT NULL,
  `publisher` VARCHAR(100) NOT NULL,
  `number_of_page` INTEGER,
  `subject` ENUM ('sayısal', 'matematik', 'fen', 'fizik', 'kimya', 'biyoloji', 'sözel', 'türkçe', 'edebiyat', 'sosyal', 'tarih', 'coğrafya', 'felsefe', 'din', 'ingilizce', 'genel') NOT NULL,
  `grade` ENUM ('9.', '10.', '11.', '12.', 'tyt', 'ayt', 'ydt', 'lise') NOT NULL,
  `year` YEAR,
  `type` ENUM ('soru bankası', 'deneme', 'diğer') NOT NULL
);

CREATE TABLE `islerkitap` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `current_price` DOUBLE(7, 2),
  `original_price` DOUBLE(7, 2),
  `quantity` INTEGER,
  `score` DOUBLE(2, 1),
  `link` VARCHAR(300),
  `image` VARCHAR(300), 
  -- These below are later to be dropped. --
  `name` VARCHAR(300) NOT NULL,
  `publisher` VARCHAR(100) NOT NULL,
  `number_of_page` INTEGER,
  `subject` ENUM ('sayısal', 'matematik', 'fen', 'fizik', 'kimya', 'biyoloji', 'sözel', 'türkçe', 'edebiyat', 'sosyal', 'tarih', 'coğrafya', 'felsefe', 'din', 'ingilizce', 'genel') NOT NULL,
  `grade` ENUM ('9.', '10.', '11.', '12.', 'tyt', 'ayt', 'ydt', 'lise') NOT NULL,
  `year` YEAR,
  `type` ENUM ('soru bankası', 'deneme', 'diğer') NOT NULL
);

CREATE TABLE `kitapyurdu` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `current_price` DOUBLE(7, 2),
  `original_price` DOUBLE(7, 2),
  `quantity` INTEGER,
  `score` DOUBLE(2, 1),
  `link` VARCHAR(300),
  `image` VARCHAR(300), 
  -- These below are later to be dropped. --
  `name` VARCHAR(300) NOT NULL,
  `publisher` VARCHAR(100) NOT NULL,
  `number_of_page` INTEGER,
  `subject` ENUM ('sayısal', 'matematik', 'fen', 'fizik', 'kimya', 'biyoloji', 'sözel', 'türkçe', 'edebiyat', 'sosyal', 'tarih', 'coğrafya', 'felsefe', 'din', 'ingilizce', 'genel') NOT NULL,
  `grade` ENUM ('9.', '10.', '11.', '12.', 'tyt', 'ayt', 'ydt', 'lise') NOT NULL,
  `year` YEAR,
  `type` ENUM ('soru bankası', 'deneme', 'diğer') NOT NULL
);

CREATE TABLE `bkmkitap` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `current_price` DOUBLE(7, 2),
  `original_price` DOUBLE(7, 2),
  `quantity` INTEGER,
  `score` DOUBLE(2, 1),
  `link` VARCHAR(300),
  `image` VARCHAR(300), 
  -- These below are later to be dropped. --
  `name` VARCHAR(300) NOT NULL,
  `publisher` VARCHAR(100) NOT NULL,
  `number_of_page` INTEGER,
  `subject` ENUM ('sayısal', 'matematik', 'fen', 'fizik', 'kimya', 'biyoloji', 'sözel', 'türkçe', 'edebiyat', 'sosyal', 'tarih', 'coğrafya', 'felsefe', 'din', 'ingilizce', 'genel') NOT NULL,
  `grade` ENUM ('9.', '10.', '11.', '12.', 'tyt', 'ayt', 'ydt', 'lise') NOT NULL,
  `year` YEAR,
  `type` ENUM ('soru bankası', 'deneme', 'diğer') NOT NULL
);

CREATE TABLE `isemkitap` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `current_price` DOUBLE(7, 2),
  `original_price` DOUBLE(7, 2),
  `quantity` INTEGER,
  `score` DOUBLE(2, 1),
  `link` VARCHAR(300),
  `image` VARCHAR(300), 
  -- These below are later to be dropped. --
  `name` VARCHAR(300) NOT NULL,
  `publisher` VARCHAR(100) NOT NULL,
  `number_of_page` INTEGER,
  `subject` ENUM ('sayısal', 'matematik', 'fen', 'fizik', 'kimya', 'biyoloji', 'sözel', 'türkçe', 'edebiyat', 'sosyal', 'tarih', 'coğrafya', 'felsefe', 'din', 'ingilizce', 'genel') NOT NULL,
  `grade` ENUM ('9.', '10.', '11.', '12.', 'tyt', 'ayt', 'ydt', 'lise') NOT NULL,
  `year` YEAR,
  `type` ENUM ('soru bankası', 'deneme', 'diğer') NOT NULL
);

CREATE TABLE `sadecekitap` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `current_price` DOUBLE(7, 2),
  `original_price` DOUBLE(7, 2),
  `quantity` INTEGER,
  `score` DOUBLE(2, 1),
  `link` VARCHAR(300),
  `image` VARCHAR(300),
  -- These below are later to be dropped. --
  `name` VARCHAR(300) NOT NULL,
  `publisher` VARCHAR(100) NOT NULL,
  `number_of_page` INTEGER,
  `subject` ENUM ('sayısal', 'matematik', 'fen', 'fizik', 'kimya', 'biyoloji', 'sözel', 'türkçe', 'edebiyat', 'sosyal', 'tarih', 'coğrafya', 'felsefe', 'din', 'ingilizce', 'genel') NOT NULL,
  `grade` ENUM ('9.', '10.', '11.', '12.', 'tyt', 'ayt', 'ydt', 'lise') NOT NULL,
  `year` YEAR,
  `type` ENUM ('soru bankası', 'deneme', 'diğer') NOT NULL
);

CREATE TABLE `kitapsepeti` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `current_price` DOUBLE(7, 2),
  `original_price` DOUBLE(7, 2),
  `quantity` INTEGER,
  `score` DOUBLE(2, 1),
  `link` VARCHAR(300),
  `image` VARCHAR(300),
  -- These below are later to be dropped. --
  `name` VARCHAR(300) NOT NULL,
  `publisher` VARCHAR(100) NOT NULL,
  `number_of_page` INTEGER,
  `subject` ENUM ('sayısal', 'matematik', 'fen', 'fizik', 'kimya', 'biyoloji', 'sözel', 'türkçe', 'edebiyat', 'sosyal', 'tarih', 'coğrafya', 'felsefe', 'din', 'ingilizce', 'genel') NOT NULL,
  `grade` ENUM ('9.', '10.', '11.', '12.', 'tyt', 'ayt', 'ydt', 'lise') NOT NULL,
  `year` YEAR,
  `type` ENUM ('soru bankası', 'deneme', 'diğer') NOT NULL
);
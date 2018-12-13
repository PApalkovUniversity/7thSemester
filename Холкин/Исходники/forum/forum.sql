-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Хост: localhost
-- Время создания: Ноя 03 2018 г., 12:46
-- Версия сервера: 10.1.36-MariaDB
-- Версия PHP: 5.6.38

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `forum`
--

-- --------------------------------------------------------

--
-- Структура таблицы `message`
--

CREATE TABLE `message` (
  `id` int(11) NOT NULL,
  `kodoftopic` int(11) NOT NULL,
  `textmessage` text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `name_man` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `date_answer` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `message`
--

INSERT INTO `message` (`id`, `kodoftopic`, `textmessage`, `name_man`, `date_answer`) VALUES
(37, 39, 'Мое любимое озеро - Байкал', 'admin', '2018-11-03'),
(38, 40, 'Я бывал в Альпах', 'admin', '2018-11-03'),
(39, 41, 'Париж, а у вас?', 'admin', '2018-11-03'),
(40, 39, 'Мое тоже Байкал', 'Павел', '2018-11-03');

-- --------------------------------------------------------

--
-- Структура таблицы `topic`
--

CREATE TABLE `topic` (
  `id` int(11) NOT NULL,
  `kodofrazdel` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `name_creator` varchar(20) NOT NULL,
  `name_last_answer` varchar(20) NOT NULL,
  `date_last_answer` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `topic`
--

INSERT INTO `topic` (`id`, `kodofrazdel`, `name`, `name_creator`, `name_last_answer`, `date_last_answer`) VALUES
(36, 0, 'Озера России', 'admin', '', '2018-11-03'),
(37, 0, 'Горы России ', 'admin', '', '2018-11-03'),
(38, 0, 'Интересные места', 'admin', '', '2018-11-03'),
(39, 36, 'Ваше любимое озеро', 'admin', 'Павел', '2018-11-03'),
(40, 37, 'В каких горах вы бывали', 'admin', '', '2018-11-03'),
(41, 38, 'Какое самое интересное место, которое вы посещали?', 'admin', '', '2018-11-03');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `pass` varchar(40) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `role` varchar(10) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `name`, `pass`, `role`) VALUES
(1, 'admin', '827ccb0eea8a706c4c34a16891f84e7b', 'admin'),
(2, 'guest', 'ee11cbb19052e40b07aac0ca060c23ee', 'user'),
(10, 'Павел', '827ccb0eea8a706c4c34a16891f84e7b', 'user');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `message`
--
ALTER TABLE `message`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `topic`
--
ALTER TABLE `topic`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `message`
--
ALTER TABLE `message`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT для таблицы `topic`
--
ALTER TABLE `topic`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 24, 2025 at 06:54 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `code_hunter`
--

-- --------------------------------------------------------

--
-- Table structure for table `contacts`
--

DROP TABLE IF EXISTS `contacts`;
CREATE TABLE `contacts` (
  `sno` int(50) NOT NULL,
  `name` text NOT NULL,
  `email` varchar(50) NOT NULL,
  `ph_no` varchar(50) NOT NULL,
  `msg` text NOT NULL,
  `date` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contacts`
--

INSERT INTO `contacts` (`sno`, `name`, `email`, `ph_no`, `msg`, `date`) VALUES
(1, 'first post', 'firstpost@gmail.com', '123123123', 'first post', '2025-02-17 18:03:13'),
(2, 'coco', 'demo@gmail.com', '1231231231', 'demo', '2025-02-18 11:22:30'),
(3, 'fdf', 'demo1@gmail.com', '44444444444', 'fdds', '2025-02-18 11:23:44'),
(4, 'AA', 'aa@gmail.com', '7897897897', 'aa', '2025-02-18 14:38:09'),
(5, 'AA', 'aa@gmail.com', '7897897897', 'aa', '2025-02-18 14:59:33'),
(6, 'AA', 'aa@gmail.com', '7897897897', 'aa', '2025-02-18 14:59:38'),
(7, 'AA', 'aa@gmail.com', '7897897897', 'aa', '2025-02-18 15:01:43'),
(8, 'AA', 'demo@gmail.com', '7897897897', 'aa', '2025-02-18 15:02:07'),
(9, 'BB', 'bb@gmail.com', '1234561231', 'bb', '2025-02-19 10:26:23'),
(10, 'CC', 'cc@gmail.com', '7411477411', 'Test', '2025-02-19 15:48:46');

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

DROP TABLE IF EXISTS `posts`;
CREATE TABLE `posts` (
  `sno` int(50) NOT NULL,
  `title` text NOT NULL,
  `slug` varchar(30) NOT NULL,
  `content` text NOT NULL,
  `img_file` varchar(20) NOT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`sno`, `title`, `slug`, `content`, `img_file`, `date`) VALUES
(1, 'Learn Hunting!', 'first-post', 'A perfectly seared steak glistened on the plate in front of me. It didn’t yet hold the connections it would later represent in my mind, but it was the start. In the dancing candlelight of a dim Argentinian restaurant, at the age of 31, I made one of the best decisions of my life. If I was going to continue eating meat after this meal, financially supporting the killing of animals for food, I was going to be involved in the process. I would become a hunter.', 'hunt.jpeg', '2025-02-19 15:15:40'),
(2, 'Hunting and Gathering', 'second-post', 'Hunting and gathering constitute the oldest human mode of making a living, and the only one for which there is an uninterrupted record from human origins to the present. Correspondingly, there has been a lot of anthropological attention devoted to hunting and gathering with an initial confidence that one could directly observe human nature by studying hunter-gatherers. More recently, however, anthropologists have grown cautious not to draw analogies between present-day hunter-gatherers and those of the distant past too quickly. They also do not focus on hunting and gathering as isolated activities, but rather on the socio-cultural formations that have been found to be associated with them. Despite considerable regional diversity, there are recurrent themes in hunter-gatherer ethnography that show shared patterns beyond the ecology of foraging.', 'hunt1.jpeg', '2025-02-18 18:11:03'),
(3, 'Game Farms for New Hunters?', 'third-slug', '“This one is coming back,” I said to my wife, hardly looking up from the bowl of salsa in front me. Sure enough, the yellow flag flashed across the screen and landed lamely on the turf. The official announced that number 75, offense, was guilty of holding.  A ten-yard penalty was assessed as punishment for his transgression and the game resumed.\r\n\r\n“How did you see that penalty? Sometimes I feel like you and I are watching a different game,” my wife said.  I shrugged my shoulders and casually replied, “Well, I’ve seen that a thousand times.  The left tackle was getting beat and out of desperation he grabbed a fistful of jersey.” It was only a split second, but I was positive I saw it and the instant replay supported my claim.\r\n\r\nI’m no great football mind, let me assure you. I have, however, watched a couple thousand football games in my life and grew up with a dad who was a high functioning football-aholic. We lived, ate, and breathed football in my house for as long as I can remember.  Decades of exposure gradually imbued me with a fairly good eye for the game.  My wife isn’t less intelligent than me.  In fact, she’s much, much more intelligent than I am (her decision to marry me excluded). It’s just that the game is very fast, and it takes a long time to learn it.', 'hunt2.jpeg', '2025-02-18 18:21:44'),
(4, 'Gear Review: Hoo-Rag Bandanas', 'fourth-slug', 'I first wanted to check out the various options that Hoo-Rag had. Per their website, they offer over 250 different bandana styles, including hunting and fishing patterns, outdoor sports and fitness, tactical, and much more. Whatever your preference or situation, there’s likely a couple Hoo-Rag bandanas to choose from.\r\n\r\nThe bandanas are meant to be very versatile: you can use them as full or partial face masks, neck gaiters/scarves, beanies/head wraps, or even hat liners. They are constructed from a moisture-wicking polyester microfiber, are seamless, and have a UPF30 sun protection rating.', 'hunt3.jpeg', '2025-02-18 18:23:19'),
(5, 'A Hunter’s Guide', 'fifth-slug', 'Let’s imagine it’s deer season and you just shot a deer. Maybe your first. Great news, right? The bad news is you didn’t see or hear it fall. Now you have an agonizing dilemma on your hands and an important decision to make. Do you climb down and take up the deer blood trail right away or give the deer more time to expire? Your decision may impact whether you find the deer or not. So before you start blood trailing deer, especially if it’s your first time doing so, here are some important questions you need to answer.\r\n\r\nHow did the deer react? Was it running instead of bounding? Was it stumbling and crashing through the underbrush instead of jumping over it? Those are both usually good signs.\r\nHow did you feel about the shot? Were you shaking from nerves, or were you very calm and relaxed?\r\nHow were the weather conditions? High winds can affect arrows and bullets alike and may steer them off-course.', 'hunt4.jpeg', '2025-02-19 14:50:25'),
(6, 'The Hunger Games', 'six-slug', 'In the ruins of a place once known as North America lies the nation of Panem, a shining Capitol surrounded by twelve outlying districts. The Capitol is harsh and cruel and keeps the districts in line by forcing them all to send one boy and one girl between the ages of twelve and eighteen to participate in the annual Hunger Games, a fight to the death on live TV.', 'book.jpg', '2025-02-18 18:25:06');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `email` text NOT NULL,
  `password` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `name`, `email`, `password`) VALUES
(1, 'Akaza', 'demo@gmail.com', 'Akaza@789'),
(2, 'AA', 'aa@gmail.com', '123123');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `contacts`
--
ALTER TABLE `contacts`
  MODIFY `sno` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `sno` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

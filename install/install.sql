SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE TABLE IF NOT EXISTS `corpCache` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `corpID` varchar(128) NOT NULL,
  `corpTicker` varchar(10) NOT NULL,
  `corpName` varchar(255) NOT NULL,
  `corpRole` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `corpID` (`corpID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `corpRoles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `corpID` varchar(128) NOT NULL,
  `corpRole` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `corpID` (`corpID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `messageQueue` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message` varchar(2048) NOT NULL,
  `channel` varchar(64) NOT NULL,
  `guild` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `renameQueue` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `discordID` varchar(64) NOT NULL,
  `nick` varchar(128) NOT NULL,
  `guild` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `storage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(191) NOT NULL,
  `value` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `authUsers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `eveName` varchar(365) NOT NULL,
  `characterID` varchar(128) NOT NULL,
  `discordID` varchar(64) NOT NULL,
  `role` varchar(128) NOT NULL,
  `active` varchar(10) NOT NULL DEFAULT 'yes',
  `addedOn` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `characterID` (`characterID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `pendingUsers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `characterID` varchar(128) NOT NULL,
  `corporationID` varchar(128) NOT NULL,
  `allianceID` varchar(128) NOT NULL,
  `authString` varchar(128) NOT NULL,
  `active` varchar(10) NOT NULL,
  `dateCreated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

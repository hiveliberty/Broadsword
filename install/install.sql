SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE TABLE IF NOT EXISTS `corporation_cache` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `alliance_id` varchar(128) DEFAULT NULL,
  `corporation_id` varchar(128) NOT NULL,
  `corporation_name` varchar(255) NOT NULL,
  `corporation_role` varchar(255) NOT NULL,
  `corporation_ticker` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `corporation_id` (`corporation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `queue_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `channel_id` varchar(64) NOT NULL,
  `message` varchar(2048) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `queue_rename` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `discord_id` varchar(64) NOT NULL,
  `nick` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `storage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `s_key` varchar(191) NOT NULL,
  `s_value` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `s_key` (`s_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `discord_users_auth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `eve_name` varchar(365) DEFAULT NULL,
  `character_id` varchar(128) NOT NULL,
  `corporation_id` varchar(128) NOT NULL,
  `alliance_id` varchar(128) NOT NULL,
  `discord_id` varchar(64) NOT NULL,
  `active` varchar(10) NOT NULL DEFAULT 'no',
  `pending` varchar(10) NOT NULL,
  `added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `character_id` (`character_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `discord_users_cache` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `discord_id` varchar(64) NOT NULL,
  `is_authorized` varchar(10) NOT NULL DEFAULT 'no',
  `added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `discord_id` (`discord_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `token_storage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `character_id` varchar(128) NOT NULL,
  `token_access` varchar(255) DEFAULT NULL,
  `token_refresh` varchar(255) DEFAULT NULL,
  `updated` timestamp NULL DEFAULT NULL,
  `added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `character_id` (`character_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

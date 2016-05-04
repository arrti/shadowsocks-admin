-- ---
-- Globals
-- ---

-- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
-- SET FOREIGN_KEY_CHECKS=0;

-- ---
-- Table 'admin'
--
-- ---

DROP TABLE IF EXISTS `admin`;

CREATE TABLE `admin` (
  `id` INTEGER(11) NOT NULL AUTO_INCREMENT DEFAULT NULL,
  `email` TEXT NULL,
  `password` TEXT NOT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Foreign Keys
-- ---


-- ---
-- Table Properties
-- ---

ALTER TABLE `admin` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ---
-- Test Data
-- ---

-- INSERT INTO `admin` (`id`,`email`,`password`) VALUES
-- ('','','123456');
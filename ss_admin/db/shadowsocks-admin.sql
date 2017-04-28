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
  `id` INTEGER(11) NOT NULL AUTO_INCREMENT,
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

-- ---
-- PROCEDURE reset transfer
-- ---

DELIMITER $$

DROP PROCEDURE IF EXISTS `shadowsocks`.`reset_transfer`$$

CREATE PROCEDURE `shadowsocks`.`reset_transfer`()

    BEGIN
    UPDATE shadowsocks.user SET d=0, u=0;
    END$$

DELIMITER ;

-- ---
-- EVENT reset transfer on the 1st of each month at 01:00 AM
-- ---

DROP EVENT IF EXISTS e_sa_reset;

CREATE EVENT e_sa_reset
ON SCHEDULE EVERY 1 MONTH  STARTS
DATE_ADD(DATE_ADD(DATE_SUB(CURDATE(),INTERVAL DAY(CURDATE())-1 DAY), INTERVAL 1 MONTH),INTERVAL 1 HOUR)
DO call shadowsocks.reset_transfer();

create database  wxinfo;
use wxinfo;
CREATE TABLE IF NOT EXISTS `invite_info`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `group_puid` VARCHAR(60) ,
   `group_name` VARCHAR(60) NOT NULL,
   `inviter_name` VARCHAR(120) NOT NULL,
   `invitee_name` VARCHAR(120) NOT NULL,
   `is_used` bool default false,
   `addtime` int,
   PRIMARY KEY ( `id` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `punch_info`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `group_puid` VARCHAR(60),
   `group_name` VARCHAR(60) NOT NULL,
   `user_puid` VARCHAR(60) NOT NULL,
   `nick_name` VARCHAR(120) NOT NULL,
   `addtime` timestamp,
   PRIMARY KEY ( `id` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `group_info`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `group_puid` VARCHAR(60),
   `group_name` VARCHAR(60) NOT NULL,
   PRIMARY KEY ( `id` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `member_info`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `group_puid` VARCHAR(60),
   `group_name` VARCHAR(120) NOT NULL,
   `user_puid` VARCHAR(60) NOT NULL,
   `nick_name` VARCHAR(120) NOT NULL,
   `sex` VARCHAR(2) ,
   `city` VARCHAR(8) ,
   `age` INT UNSIGNED,
   PRIMARY KEY ( `id` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
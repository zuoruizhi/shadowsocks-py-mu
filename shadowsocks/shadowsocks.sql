-- -------------------------------------------
-- !!! WARNING !!!
-- It is not suggested to use this sql file.
-- Please import the one provided by SS-Panel.
-- -------------------------------------------
SET FOREIGN_KEY_CHECKS=0;

CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(32) NOT NULL,
  `pass` varchar(32) NOT NULL,
  `passwd` varchar(32) NOT NULL,
  `t` int(11) NOT NULL DEFAULT '0',
  `u` bigint(20) NOT NULL DEFAULT '0',
  `d` bigint(20) NOT NULL DEFAULT '0',
  `transfer_enable` bigint(20) NOT NULL,
  `port` int(11) NOT NULL,
  `switch` tinyint(4) NOT NULL DEFAULT '1',
  `enable` tinyint(4) NOT NULL DEFAULT '1',
  `method` varchar(20) NOT NULL DEFAULT 'aes-256-cfb',
  `type` tinyint(4) NOT NULL DEFAULT '1',
  `last_get_gift_time` int(11) NOT NULL DEFAULT '0',
  `last_rest_pass_time` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`,`port`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` (`email`, `pass`, `password`, `transfer_enable`, `port`) VALUES ('test@test.com', '123456', '0000000', '9320666234', '50000');

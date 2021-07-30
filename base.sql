-- --------------------------------------------------------
-- Servidor:                     127.0.0.1
-- Versão do servidor:           10.4.17-MariaDB - mariadb.org binary distribution
-- OS do Servidor:               Win64
-- HeidiSQL Versão:              11.2.0.6213
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Copiando estrutura para tabela functional.command
CREATE TABLE IF NOT EXISTS `command` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `class` varchar(64) DEFAULT NULL,
  `name` varchar(64) DEFAULT NULL,
  `value` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`),
  KEY `language` (`class`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4;

-- Copiando dados para a tabela functional.command: ~14 rows (aproximadamente)
/*!40000 ALTER TABLE `command` DISABLE KEYS */;
INSERT INTO `command` (`id`, `class`, `name`, `value`) VALUES
	(1, 'sql', 'select', 'SELECT\r\n    {{field}}');
INSERT INTO `command` (`id`, `class`, `name`, `value`) VALUES
	(2, 'sql', 'create', 'CREATE TABLE \n    {{name}}\n(\n{{field}}\n)');
INSERT INTO `command` (`id`, `class`, `name`, `value`) VALUES
	(3, 'sql', 'insert', 'INSERT INTO\n    {{table}} ({{field}})');
INSERT INTO `command` (`id`, `class`, `name`, `value`) VALUES
	(4, 'sql', 'update', 'UPDATE\n    {{table}}');
INSERT INTO `command` (`id`, `class`, `name`, `value`) VALUES
	(5, 'sql', 'from', 'FROM\n    {{table}}');
INSERT INTO `command` (`id`, `class`, `name`, `value`) VALUES
	(6, 'sql', 'join', '{{type}} JOIN\n    {{table}} ON {{table}}.{{identifier}} = {{subject}}.{{alias}}');
INSERT INTO `command` (`id`, `class`, `name`, `value`) VALUES
	(7, 'sql', 'where', 'WHERE\n    {{condition}}');
INSERT INTO `command` (`id`, `class`, `name`, `value`) VALUES
	(8, 'sql', 'and', 'AND\n    {{condition}}');
INSERT INTO `command` (`id`, `class`, `name`, `value`) VALUES
	(9, 'sql', 'values', 'VALUES\n    ({{value}})');
INSERT INTO `command` (`id`, `class`, `name`, `value`) VALUES
	(10, 'sql', 'delete', 'DELETE FROM\n    {{table}}');
INSERT INTO `command` (`id`, `class`, `name`, `value`) VALUES
	(11, 'sql', 'set', 'SET\n   {{value}}');
INSERT INTO `command` (`id`, `class`, `name`, `value`) VALUES
	(14, 'sql', 'insert into', '');
INSERT INTO `command` (`id`, `class`, `name`, `value`) VALUES
	(20, 'sql', 'left join', '');
INSERT INTO `command` (`id`, `class`, `name`, `value`) VALUES
	(21, 'sql', 'select from', '');
/*!40000 ALTER TABLE `command` ENABLE KEYS */;

-- Copiando estrutura para tabela functional.sub_command
CREATE TABLE IF NOT EXISTS `sub_command` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent` int(11) DEFAULT NULL,
  `child` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK__command` (`parent`),
  KEY `FK__command_2` (`child`),
  CONSTRAINT `FK__command` FOREIGN KEY (`parent`) REFERENCES `command` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK__command_2` FOREIGN KEY (`child`) REFERENCES `command` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4;

-- Copiando dados para a tabela functional.sub_command: ~5 rows (aproximadamente)
/*!40000 ALTER TABLE `sub_command` DISABLE KEYS */;
INSERT INTO `sub_command` (`id`, `parent`, `child`) VALUES
	(5, 14, 3);
INSERT INTO `sub_command` (`id`, `parent`, `child`) VALUES
	(6, 14, 9);
INSERT INTO `sub_command` (`id`, `parent`, `child`) VALUES
	(21, 20, 6);
INSERT INTO `sub_command` (`id`, `parent`, `child`) VALUES
	(22, 21, 1);
INSERT INTO `sub_command` (`id`, `parent`, `child`) VALUES
	(23, 21, 5);
/*!40000 ALTER TABLE `sub_command` ENABLE KEYS */;

-- Copiando estrutura para tabela functional.sub_command_parameter
CREATE TABLE IF NOT EXISTS `sub_command_parameter` (
  `sub_command` int(11) DEFAULT NULL,
  `parameter` varchar(32) DEFAULT NULL,
  `value` text DEFAULT NULL,
  `command` int(11) DEFAULT NULL,
  KEY `FK_sub_command_parameter_sub_command` (`sub_command`),
  KEY `FK_sub_command_parameter_command` (`command`),
  CONSTRAINT `FK_sub_command_parameter_command` FOREIGN KEY (`command`) REFERENCES `command` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_sub_command_parameter_sub_command` FOREIGN KEY (`sub_command`) REFERENCES `sub_command` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Copiando dados para a tabela functional.sub_command_parameter: ~1 rows (aproximadamente)
/*!40000 ALTER TABLE `sub_command_parameter` DISABLE KEYS */;
INSERT INTO `sub_command_parameter` (`sub_command`, `parameter`, `value`, `command`) VALUES
	(21, 'type', 'LEFT', NULL);
/*!40000 ALTER TABLE `sub_command_parameter` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;

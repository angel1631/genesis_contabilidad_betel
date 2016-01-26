-- MySQL dump 10.13  Distrib 5.5.46, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: genesis_contabilidad_betel
-- ------------------------------------------------------
-- Server version	5.5.46-0+deb8u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `acceso`
--

DROP TABLE IF EXISTS `acceso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acceso` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `clave` varchar(255) NOT NULL,
  `obser` varchar(1024) NOT NULL,
  `estado` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acceso`
--

LOCK TABLES `acceso` WRITE;
/*!40000 ALTER TABLE `acceso` DISABLE KEYS */;
INSERT INTO `acceso` VALUES (1,'ins_tipo_actividad','Acceso que servira para crear los distintos tipos de actividad que se pueden realizar',1),(2,'ins_cuenta','Acceso que servira para crear las distintas cuentas contables del sistema',1),(3,'ins_agrupador','Acceso que servira para crear los distintos agrupadores contables del sistema',1),(4,'ins_ingreso','Acceso que servira para crear los distintos ingresos que se hagan al sistema',1),(5,'ins_egreso','Acceso que servira para crear los distintos egresos que se hagan al sistema',1),(6,'ins_menu','permite insertar menus',1),(7,'upd_menu','actualizacion de menus',1),(8,'del_menu','eliminacion de menu',1),(9,'ins_acceso','ingreso de accesos',1),(10,'upd_acceso','actualizacion de acceso',1),(11,'del_acceso','eliminar accesos',1),(12,'admin','administracion de la aplicacion',1),(13,'ins_rol_acceso','administracion de los accesos que tienen los roles',1),(14,'upd_rol_acceso','actualiza los accesos que tiene un rol',1),(15,'del_rol_acceso','eliminar accesos que tiene los roles',1),(16,'logout','acceso para realizar logout de la aplicacion',1);
/*!40000 ALTER TABLE `acceso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `agrupador`
--

DROP TABLE IF EXISTS `agrupador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `agrupador` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(255) NOT NULL,
  `estatus` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agrupador`
--

LOCK TABLES `agrupador` WRITE;
/*!40000 ALTER TABLE `agrupador` DISABLE KEYS */;
/*!40000 ALTER TABLE `agrupador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cuenta`
--

DROP TABLE IF EXISTS `cuenta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cuenta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(255) NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `estatus` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cuenta`
--

LOCK TABLES `cuenta` WRITE;
/*!40000 ALTER TABLE `cuenta` DISABLE KEYS */;
INSERT INTO `cuenta` VALUES (1,'Caja chica de iglesia',100.00,1),(2,'Banco Industrial',0.00,1);
/*!40000 ALTER TABLE `cuenta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `egreso`
--

DROP TABLE IF EXISTS `egreso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egreso` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tipo_actividad` int(11) NOT NULL,
  `fecha_referencia` date DEFAULT NULL,
  `identificador_documento` varchar(200) NOT NULL,
  `observacion` varchar(1000) NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `agrupador` int(11) DEFAULT NULL,
  `cuenta` int(11) NOT NULL,
  `creado` datetime NOT NULL,
  `usuario` int(11) NOT NULL,
  `estatus` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_egreso__agrupador` (`agrupador`),
  KEY `idx_egreso__cuenta` (`cuenta`),
  KEY `idx_egreso__tipo_actividad` (`tipo_actividad`),
  CONSTRAINT `fk_egreso__agrupador` FOREIGN KEY (`agrupador`) REFERENCES `agrupador` (`id`),
  CONSTRAINT `fk_egreso__cuenta` FOREIGN KEY (`cuenta`) REFERENCES `cuenta` (`id`),
  CONSTRAINT `fk_egreso__tipo_actividad` FOREIGN KEY (`tipo_actividad`) REFERENCES `tipo_actividad` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `egreso`
--

LOCK TABLES `egreso` WRITE;
/*!40000 ALTER TABLE `egreso` DISABLE KEYS */;
INSERT INTO `egreso` VALUES (1,4,'2016-01-18','x24','se paga la luz de diciembre',250.00,NULL,1,'2016-01-18 10:07:44',1,1),(2,5,'2015-01-01','g2','se paga el agua de diciembre',100.00,NULL,1,'2016-01-18 10:07:44',1,1),(3,6,'2015-12-01','m24d','se paga a golan la alarma del mes de enero',344.50,NULL,1,'2016-01-18 10:07:44',1,1),(4,3,'2016-01-19','','se traslada de la caja al banco',100.00,NULL,1,'2016-01-19 09:07:34',1,1),(6,3,'2016-01-20','','traslado de prueba',125.00,NULL,1,'2016-01-20 05:57:43',1,0);
/*!40000 ALTER TABLE `egreso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingreso`
--

DROP TABLE IF EXISTS `ingreso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ingreso` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tipo_actividad` int(11) NOT NULL,
  `fecha_referencia` date DEFAULT NULL,
  `identificador_documento` varchar(200) NOT NULL,
  `observacion` varchar(1000) NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `agrupador` int(11) DEFAULT NULL,
  `cuenta` int(11) NOT NULL,
  `creado` datetime NOT NULL,
  `usuario` int(11) NOT NULL,
  `estatus` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_ingreso__agrupador` (`agrupador`),
  KEY `idx_ingreso__cuenta` (`cuenta`),
  KEY `idx_ingreso__tipo_actividad` (`tipo_actividad`),
  CONSTRAINT `fk_ingreso__agrupador` FOREIGN KEY (`agrupador`) REFERENCES `agrupador` (`id`),
  CONSTRAINT `fk_ingreso__cuenta` FOREIGN KEY (`cuenta`) REFERENCES `cuenta` (`id`),
  CONSTRAINT `fk_ingreso__tipo_actividad` FOREIGN KEY (`tipo_actividad`) REFERENCES `tipo_actividad` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingreso`
--

LOCK TABLES `ingreso` WRITE;
/*!40000 ALTER TABLE `ingreso` DISABLE KEYS */;
INSERT INTO `ingreso` VALUES (1,2,'2016-01-12','','ofrendas',444.00,NULL,1,'2016-01-12 09:33:15',1,1),(2,2,'2016-01-01','445-a','la recoleccion de ofrendas de enero 2016',8000.00,NULL,1,'2016-01-12 14:42:16',1,1),(3,3,'2016-01-19','','se traslada de la caja al banco',100.00,NULL,2,'2016-01-19 09:07:34',1,1),(5,3,'2016-01-20','','traslado de prueba',125.00,NULL,2,'2016-01-20 05:57:43',1,0);
/*!40000 ALTER TABLE `ingreso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu`
--

DROP TABLE IF EXISTS `menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(255) NOT NULL,
  `padre` int(11) DEFAULT NULL,
  `acceso` int(11) DEFAULT NULL,
  `posicion` tinyint(4) NOT NULL,
  `url` varchar(500) NOT NULL,
  `estado` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_menu__acceso` (`acceso`),
  KEY `idx_menu__padre` (`padre`),
  CONSTRAINT `fk_menu__acceso` FOREIGN KEY (`acceso`) REFERENCES `acceso` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu`
--

LOCK TABLES `menu` WRITE;
/*!40000 ALTER TABLE `menu` DISABLE KEYS */;
INSERT INTO `menu` VALUES (1,'Ingresos',NULL,4,1,'#',1),(2,'Insertar',1,4,1,'http://192.168.36.128/Ingreso/insert',1),(3,'Actualizar',1,NULL,2,'http://192.168.36.128/Ingreso/update',1),(4,'Eliminar',1,NULL,3,'http://192.168.36.128/Ingreso/delete',1),(5,'Egresos',NULL,5,2,'http://192.168.36.128/Egreso/insert',1),(6,'Insertar',5,5,1,'http://192.168.36.128/Egreso/insert',1),(7,'Actualizar',5,2,2,'http://192.168.36.128/Egreso/update',1),(8,'Traslados',NULL,NULL,3,'#',1),(9,'Insertar',8,NULL,1,'http://192.168.36.128/Traslado/insert',1),(10,'Menu',NULL,6,4,'http://192.168.36.128/Menu/insert',1),(11,'Insertar',10,6,1,'http://192.168.36.128/Menu/insert',1),(12,'Eliminar',5,NULL,3,'http://192.168.36.128/Egreso/delete',1),(13,'Anular',8,NULL,2,'http://192.168.36.128/Traslado/anular',1),(14,'Reportes',NULL,NULL,5,'#',1),(15,'Ingresos',14,NULL,1,'http://192.168.36.128/Reporte/ingresos',1),(16,'Egresos',14,NULL,2,'http://192.168.36.128/Reporte/egresos',1),(17,'Cuentas',14,NULL,3,'http://192.168.36.128/Reporte/cuentas',1),(18,'Cuentas',NULL,2,4,'#',1),(19,'Insertar',18,NULL,1,'http://192.168.36.128/Cuenta/insert',1),(20,'Actualizar',18,NULL,2,'http://192.168.36.128/Cuenta/update',1),(21,'Eliminar',18,NULL,3,'http://192.168.36.128/Cuenta/delete',1),(22,'Administracion',NULL,12,10,'#',1),(23,'Accesos',22,9,1,'#',1),(24,'Insert',23,9,1,'http://192.168.36.128/Acceso/insert',1),(25,'Actualizar',23,10,2,'http://192.168.36.128/Acceso/update',1),(26,'Eliminar',23,11,3,'http://192.168.36.128/Acceso/delete',1),(27,'Roles Accesos',22,13,2,'#',1),(28,'Insertar',27,13,1,'http://192.168.36.128/RoleAcceso/insert',1),(29,'actualizar',27,14,2,'http://192.168.36.128/RoleAcceso/update',1),(30,'Eliminar',27,15,3,'http://192.168.36.128/RoleAcceso/delete',1),(31,'Logout',NULL,16,8,'http://192.168.36.128/Security/logout',1);
/*!40000 ALTER TABLE `menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(255) NOT NULL,
  `estado` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'Administrador',1);
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_acceso`
--

DROP TABLE IF EXISTS `role_acceso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role_acceso` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role` int(11) NOT NULL,
  `acceso` int(11) NOT NULL,
  `estado` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_role_acceso__acceso` (`acceso`),
  KEY `idx_role_acceso__role` (`role`),
  CONSTRAINT `fk_role_acceso__acceso` FOREIGN KEY (`acceso`) REFERENCES `acceso` (`id`),
  CONSTRAINT `fk_role_acceso__role` FOREIGN KEY (`role`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_acceso`
--

LOCK TABLES `role_acceso` WRITE;
/*!40000 ALTER TABLE `role_acceso` DISABLE KEYS */;
INSERT INTO `role_acceso` VALUES (1,1,1,1),(2,1,2,1),(3,1,3,1),(4,1,4,1),(5,1,5,1),(6,1,6,1),(7,1,7,1),(8,1,8,1),(9,1,12,1),(10,1,9,1),(11,1,10,1),(12,1,11,1),(13,1,11,1),(14,1,13,1),(15,1,14,1),(16,1,15,1),(17,1,16,1),(18,1,7,1);
/*!40000 ALTER TABLE `role_acceso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `session`
--

DROP TABLE IF EXISTS `session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `session` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(255) NOT NULL,
  `usuario` int(11) NOT NULL,
  `ip` varchar(255) NOT NULL,
  `navegador` varchar(255) NOT NULL,
  `creado` datetime NOT NULL,
  `sesiones` tinyint(4) NOT NULL,
  `estado` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_session__usuario` (`usuario`),
  CONSTRAINT `fk_session__usuario` FOREIGN KEY (`usuario`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `session`
--

LOCK TABLES `session` WRITE;
/*!40000 ALTER TABLE `session` DISABLE KEYS */;
INSERT INTO `session` VALUES (1,'7845b3d153e83c09cd81e679bf4db5fa',1,'192.168.36.1','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36','2016-01-08 17:43:40',7,0),(2,'44b0ea5cfbb6f9e6a5d50b0975e2c71e',1,'192.168.36.1','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36','2016-01-11 06:43:28',2,0),(3,'04049a428204105c5557662024a842e1',1,'192.168.36.1','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36','2016-01-13 19:16:31',3,0),(4,'b22ad86f25072b8b483d3c0e46c1cec4',1,'192.168.36.1','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36','2016-01-15 06:00:38',1,0),(5,'e50529733ccc97a7a7654d54914c354b',1,'192.168.36.1','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36','2016-01-18 08:46:33',5,0),(10,'ca3dbf8d749e5c6e7dc19a4f18c02547',1,'192.168.36.1','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36','2016-01-21 13:30:01',5,1);
/*!40000 ALTER TABLE `session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_actividad`
--

DROP TABLE IF EXISTS `tipo_actividad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_actividad` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(255) NOT NULL,
  `estatus` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_actividad`
--

LOCK TABLES `tipo_actividad` WRITE;
/*!40000 ALTER TABLE `tipo_actividad` DISABLE KEYS */;
INSERT INTO `tipo_actividad` VALUES (1,'Diezmo',1),(2,'Ofrenda',1),(3,'Traslado',1),(4,'Pago Luz',1),(5,'Pago Agua',1),(6,'Pago Alarma',1),(7,'Pago Telefono',1);
/*!40000 ALTER TABLE `tipo_actividad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `traslado`
--

DROP TABLE IF EXISTS `traslado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `traslado` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ingreso` int(11) NOT NULL,
  `egreso` int(11) NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `creado` datetime NOT NULL,
  `usuario` int(11) NOT NULL,
  `observacion` varchar(1000) NOT NULL,
  `estatus` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_traslado__egreso` (`egreso`),
  KEY `idx_traslado__ingreso` (`ingreso`),
  CONSTRAINT `fk_traslado__egreso` FOREIGN KEY (`egreso`) REFERENCES `egreso` (`id`),
  CONSTRAINT `fk_traslado__ingreso` FOREIGN KEY (`ingreso`) REFERENCES `ingreso` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `traslado`
--

LOCK TABLES `traslado` WRITE;
/*!40000 ALTER TABLE `traslado` DISABLE KEYS */;
INSERT INTO `traslado` VALUES (2,5,6,125.00,'2016-01-20 05:57:43',1,'traslado de pruebatraslado de prueba',0);
/*!40000 ALTER TABLE `traslado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `mail` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `creado` datetime NOT NULL,
  `estado` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'Angel Guillen','angel1631@gmail.com','angel','2016-01-08 17:25:16',1);
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario_role`
--

DROP TABLE IF EXISTS `usuario_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuario_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario` int(11) NOT NULL,
  `role` int(11) NOT NULL,
  `estado` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_usuario_role__role` (`role`),
  KEY `idx_usuario_role__usuario` (`usuario`),
  CONSTRAINT `fk_usuario_role__role` FOREIGN KEY (`role`) REFERENCES `role` (`id`),
  CONSTRAINT `fk_usuario_role__usuario` FOREIGN KEY (`usuario`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario_role`
--

LOCK TABLES `usuario_role` WRITE;
/*!40000 ALTER TABLE `usuario_role` DISABLE KEYS */;
INSERT INTO `usuario_role` VALUES (1,1,1,1);
/*!40000 ALTER TABLE `usuario_role` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-01-24 18:50:47

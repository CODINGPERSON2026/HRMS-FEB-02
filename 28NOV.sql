-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: army_personnel_db
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `assigned_det`
--

DROP TABLE IF EXISTS `assigned_det`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assigned_det` (
  `army_number` varchar(15) DEFAULT NULL,
  `det_id` int DEFAULT NULL,
  `assigned_on` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `det_removed_date` datetime DEFAULT NULL,
  `det_status` tinyint(1) DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assigned_det`
--

LOCK TABLES `assigned_det` WRITE;
/*!40000 ALTER TABLE `assigned_det` DISABLE KEYS */;
INSERT INTO `assigned_det` VALUES ('778G',1,'2025-11-25 06:37:53','2025-11-26 03:31:33',0),('99226WE',8,'2025-11-25 06:45:03',NULL,1),('905CESR',4,'2025-11-26 02:35:04','2025-11-26 03:57:43',0),('9085CESR',2,'2025-11-26 03:10:02','2025-11-26 04:51:07',0),('778G',9,'2025-11-26 03:32:22',NULL,0);
/*!40000 ALTER TABLE `assigned_det` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assigned_personnel`
--

DROP TABLE IF EXISTS `assigned_personnel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assigned_personnel` (
  `army_number` varchar(15) NOT NULL,
  `det_id` int DEFAULT NULL,
  `assigned_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`army_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assigned_personnel`
--

LOCK TABLES `assigned_personnel` WRITE;
/*!40000 ALTER TABLE `assigned_personnel` DISABLE KEYS */;
INSERT INTO `assigned_personnel` VALUES ('1526',1,'2025-11-04 12:37:26');
/*!40000 ALTER TABLE `assigned_personnel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `children`
--

DROP TABLE IF EXISTS `children`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `children` (
  `id` int NOT NULL AUTO_INCREMENT,
  `personnel_id` int NOT NULL,
  `army_number` varchar(100) NOT NULL,
  `sr_no` int DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `class` varchar(100) DEFAULT NULL,
  `part_ii_order` varchar(100) DEFAULT NULL,
  `uid_no` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_army_number` (`army_number`),
  KEY `idx_personnel_id_children` (`personnel_id`),
  CONSTRAINT `children_ibfk_1` FOREIGN KEY (`personnel_id`) REFERENCES `personnel` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `children`
--

LOCK TABLES `children` WRITE;
/*!40000 ALTER TABLE `children` DISABLE KEYS */;
INSERT INTO `children` VALUES (1,1,'778G',1,'Alice Doe','2015-08-10','Class 5','P-II/2015/004','111111111111'),(2,2,'156WE',1,'Alice Doe','2015-08-10','Class 5','P-II/2015/004','111111111111'),(3,3,'1526WE',1,'Alice Doe','2015-08-10','Class 5','P-II/2015/004','111111111111'),(4,4,'9926WE',1,'Alice Doe','2015-08-10','Class 5','P-II/2015/004','111111111111'),(5,5,'99226WE',1,'Alice Doe','2015-08-10','Class 5','P-II/2015/004','111111111111'),(6,6,'966WE',1,'Alice Doe','2015-08-10','Class 5','P-II/2015/004','111111111111'),(7,7,'87CESR',1,'Alice Doe','2015-08-10','Class 5','P-II/2015/004','111111111111'),(8,8,'997CESR',1,'Alice Doe','2015-08-10','Class 5','P-II/2015/004','111111111111'),(9,10,'965CESR',1,'Alice Doe','2015-08-10','Class 5','P-II/2015/004','111111111111'),(10,12,'905CESR',1,'Alice Doe','2015-08-10','Class 5','P-II/2015/004','111111111111'),(11,13,'9085CESR',1,'Alice Doe','2015-08-10','Class 5','P-II/2015/004','111111111111'),(12,14,'25CESR',1,'Alice Doe','2015-08-10','Class 5','P-II/2015/004','111111111111'),(13,15,'165CESR',1,'Alice Doe','2015-08-10','Class 5','P-II/2015/004','111111111111'),(14,16,'775CESR',1,'Alice Doe','2015-08-10','Class 5','P-II/2015/004','111111111111'),(15,17,'984CESR',1,'Alice Doe','2015-08-10','Class 5','P-II/2015/004','111111111111'),(16,18,'994CESR',1,'Alice Doe','2015-08-10','Class 5','P-II/2015/004','111111111111'),(17,19,'99999CESR',1,'Alice Doe','2015-08-10','Class 5','P-II/2015/004','111111111111');
/*!40000 ALTER TABLE `children` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `personnel_id` int NOT NULL,
  `army_number` varchar(100) NOT NULL,
  `sr_no` int DEFAULT NULL,
  `course` varchar(255) DEFAULT NULL,
  `from_date` date DEFAULT NULL,
  `to_date` date DEFAULT NULL,
  `institute` varchar(255) DEFAULT NULL,
  `grading` varchar(100) DEFAULT NULL,
  `remarks` text,
  PRIMARY KEY (`id`),
  KEY `idx_army_number` (`army_number`),
  KEY `idx_personnel_id_courses` (`personnel_id`),
  CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`personnel_id`) REFERENCES `personnel` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES (1,1,'778G',1,'Basic Leadership Course','2011-01-01','2011-03-01','OTA Bangalore','A','Passed with distinction'),(2,2,'156WE',1,'Basic Leadership Course','2011-01-01','2011-03-01','OTA Bangalore','A','Passed with distinction'),(3,3,'1526WE',1,'Basic Leadership Course','2011-01-01','2011-03-01','OTA Bangalore','A','Passed with distinction'),(4,4,'9926WE',1,'Basic Leadership Course','2011-01-01','2011-03-01','OTA Bangalore','A','Passed with distinction'),(5,5,'99226WE',1,'Basic Leadership Course','2011-01-01','2011-03-01','OTA Bangalore','A','Passed with distinction'),(6,6,'966WE',1,'Basic Leadership Course','2011-01-01','2011-03-01','OTA Bangalore','A','Passed with distinction'),(7,7,'87CESR',1,'Basic Leadership Course','2011-01-01','2011-03-01','OTA Bangalore','A','Passed with distinction'),(8,8,'997CESR',1,'Basic Leadership Course','2011-01-01','2011-03-01','OTA Bangalore','A','Passed with distinction'),(9,10,'965CESR',1,'Basic Leadership Course','2011-01-01','2011-03-01','OTA Bangalore','A','Passed with distinction'),(10,12,'905CESR',1,'Basic Leadership Course','2011-01-01','2011-03-01','OTA Bangalore','A','Passed with distinction'),(11,13,'9085CESR',1,'Basic Leadership Course','2011-01-01','2011-03-01','OTA Bangalore','A','Passed with distinction'),(12,14,'25CESR',1,'Basic Leadership Course','2011-01-01','2011-03-01','OTA Bangalore','A','Passed with distinction'),(13,15,'165CESR',1,'Basic Leadership Course','2011-01-01','2011-03-01','OTA Bangalore','A','Passed with distinction'),(14,16,'775CESR',1,'Basic Leadership Course','2011-01-01','2011-03-01','OTA Bangalore','A','Passed with distinction'),(15,17,'984CESR',1,'Basic Leadership Course','2011-01-01','2011-03-01','OTA Bangalore','A','Passed with distinction'),(16,18,'994CESR',1,'Basic Leadership Course','2011-01-01','2011-03-01','OTA Bangalore','A','Passed with distinction'),(17,19,'99999CESR',1,'Basic Leadership Course','2011-01-01','2011-03-01','OTA Bangalore','A','Passed with distinction');
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detailed_courses`
--

DROP TABLE IF EXISTS `detailed_courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detailed_courses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `personnel_id` int NOT NULL,
  `army_number` varchar(100) NOT NULL,
  `sr_no` int DEFAULT NULL,
  `course_name` varchar(255) DEFAULT NULL,
  `from_date` date DEFAULT NULL,
  `to_date` date DEFAULT NULL,
  `remarks` text,
  PRIMARY KEY (`id`),
  KEY `idx_army_number` (`army_number`),
  KEY `idx_personnel_id_detailed_courses` (`personnel_id`),
  CONSTRAINT `detailed_courses_ibfk_1` FOREIGN KEY (`personnel_id`) REFERENCES `personnel` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detailed_courses`
--

LOCK TABLES `detailed_courses` WRITE;
/*!40000 ALTER TABLE `detailed_courses` DISABLE KEYS */;
INSERT INTO `detailed_courses` VALUES (1,1,'778G',1,'Advanced Infantry Course','2016-01-01','2016-03-01','Detailed due to injury'),(2,2,'156WE',1,'Advanced Infantry Course','2016-01-01','2016-03-01','Detailed due to injury'),(3,3,'1526WE',1,'Advanced Infantry Course','2016-01-01','2016-03-01','Detailed due to injury'),(4,4,'9926WE',1,'Advanced Infantry Course','2016-01-01','2016-03-01','Detailed due to injury'),(5,5,'99226WE',1,'Advanced Infantry Course','2016-01-01','2016-03-01','Detailed due to injury'),(6,6,'966WE',1,'Advanced Infantry Course','2016-01-01','2016-03-01','Detailed due to injury'),(7,7,'87CESR',1,'Advanced Infantry Course','2016-01-01','2016-03-01','Detailed due to injury'),(8,8,'997CESR',1,'Advanced Infantry Course','2016-01-01','2016-03-01','Detailed due to injury'),(9,10,'965CESR',1,'Advanced Infantry Course','2016-01-01','2016-03-01','Detailed due to injury'),(10,12,'905CESR',1,'Advanced Infantry Course','2016-01-01','2016-03-01','Detailed due to injury'),(11,13,'9085CESR',1,'Advanced Infantry Course','2016-01-01','2016-03-01','Detailed due to injury'),(12,14,'25CESR',1,'Advanced Infantry Course','2016-01-01','2016-03-01','Detailed due to injury'),(13,15,'165CESR',1,'Advanced Infantry Course','2016-01-01','2016-03-01','Detailed due to injury'),(14,16,'775CESR',1,'Advanced Infantry Course','2016-01-01','2016-03-01','Detailed due to injury'),(15,17,'984CESR',1,'Advanced Infantry Course','2016-01-01','2016-03-01','Detailed due to injury'),(16,18,'994CESR',1,'Advanced Infantry Course','2016-01-01','2016-03-01','Detailed due to injury'),(17,19,'99999CESR',1,'Advanced Infantry Course','2016-01-01','2016-03-01','Detailed due to injury');
/*!40000 ALTER TABLE `detailed_courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dets`
--

DROP TABLE IF EXISTS `dets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dets` (
  `det_id` int NOT NULL AUTO_INCREMENT,
  `det_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`det_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dets`
--

LOCK TABLES `dets` WRITE;
/*!40000 ALTER TABLE `dets` DISABLE KEYS */;
INSERT INTO `dets` VALUES (1,'Alpha Detachment'),(2,'Bravo Detachment'),(3,'Charlie Detachment'),(4,'Delta Detachment'),(5,'Echo Detachment'),(6,'Foxtrot Detachment'),(7,'Golf Detachment'),(8,'Hotel Detachment'),(9,'India Detachment'),(10,'Juliet Detachment');
/*!40000 ALTER TABLE `dets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `family_members`
--

DROP TABLE IF EXISTS `family_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `family_members` (
  `id` int NOT NULL AUTO_INCREMENT,
  `personnel_id` int NOT NULL,
  `army_number` varchar(100) NOT NULL,
  `relation` varchar(100) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `uid_no` varchar(50) DEFAULT NULL,
  `part_ii_order` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_army_number` (`army_number`),
  KEY `idx_personnel_id_family` (`personnel_id`),
  CONSTRAINT `family_members_ibfk_1` FOREIGN KEY (`personnel_id`) REFERENCES `personnel` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `family_members`
--

LOCK TABLES `family_members` WRITE;
/*!40000 ALTER TABLE `family_members` DISABLE KEYS */;
INSERT INTO `family_members` VALUES (1,1,'778G','Spouse','Jane Doe','1987-04-15','987654321098','P-II/2012/003'),(2,2,'156WE','Spouse','Jane Doe','1987-04-15','987654321098','P-II/2012/003'),(3,3,'1526WE','Spouse','Jane Doe','1987-04-15','987654321098','P-II/2012/003'),(4,4,'9926WE','Spouse','Jane Doe','1987-04-15','987654321098','P-II/2012/003'),(5,5,'99226WE','Spouse','Jane Doe','1987-04-15','987654321098','P-II/2012/003'),(6,6,'966WE','Spouse','Jane Doe','1987-04-15','987654321098','P-II/2012/003'),(7,7,'87CESR','Spouse','Jane Doe','1987-04-15','987654321098','P-II/2012/003'),(8,8,'997CESR','Spouse','Jane Doe','1987-04-15','987654321098','P-II/2012/003'),(9,10,'965CESR','Spouse','Jane Doe','1987-04-15','987654321098','P-II/2012/003'),(10,12,'905CESR','Spouse','Jane Doe','1987-04-15','987654321098','P-II/2012/003'),(11,13,'9085CESR','Spouse','Jane Doe','1987-04-15','987654321098','P-II/2012/003'),(12,14,'25CESR','Spouse','Jane Doe','1987-04-15','987654321098','P-II/2012/003'),(13,15,'165CESR','Spouse','Jane Doe','1987-04-15','987654321098','P-II/2012/003'),(14,16,'775CESR','Spouse','Jane Doe','1987-04-15','987654321098','P-II/2012/003'),(15,17,'984CESR','Spouse','Jane Doe','1987-04-15','987654321098','P-II/2012/003'),(16,18,'994CESR','Spouse','Jane Doe','1987-04-15','987654321098','P-II/2012/003'),(17,19,'99999CESR','Spouse','Jane Doe','1987-04-15','987654321098','P-II/2012/003');
/*!40000 ALTER TABLE `family_members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ideal_weights`
--

DROP TABLE IF EXISTS `ideal_weights`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ideal_weights` (
  `id` int NOT NULL AUTO_INCREMENT,
  `height_cm` int NOT NULL,
  `age_range` varchar(20) NOT NULL,
  `ideal_weight_kg` decimal(5,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=145 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ideal_weights`
--

LOCK TABLES `ideal_weights` WRITE;
/*!40000 ALTER TABLE `ideal_weights` DISABLE KEYS */;
INSERT INTO `ideal_weights` VALUES (2,156,'18-22',49.00,'2025-09-22 10:02:56'),(3,156,'23-27',51.00,'2025-09-22 10:02:56'),(4,156,'28-32',52.50,'2025-09-22 10:02:56'),(5,156,'33-37',53.50,'2025-09-22 10:02:56'),(6,156,'38-42',54.00,'2025-09-22 10:02:56'),(7,156,'43-47',54.50,'2025-09-22 10:02:56'),(8,156,'48-70',55.00,'2025-09-22 10:02:56'),(10,158,'18-22',50.00,'2025-09-22 10:02:56'),(11,158,'23-27',52.00,'2025-09-22 10:02:56'),(12,158,'28-32',54.00,'2025-09-22 10:02:56'),(13,158,'33-37',55.00,'2025-09-22 10:02:56'),(14,158,'38-42',55.50,'2025-09-22 10:02:56'),(15,158,'43-47',56.00,'2025-09-22 10:02:56'),(16,158,'48-70',56.50,'2025-09-22 10:02:56'),(18,160,'18-22',51.00,'2025-09-22 10:02:56'),(19,160,'23-27',53.00,'2025-09-22 10:02:56'),(20,160,'28-32',55.00,'2025-09-22 10:02:56'),(21,160,'33-37',56.00,'2025-09-22 10:02:56'),(22,160,'38-42',56.50,'2025-09-22 10:02:56'),(23,160,'43-47',57.00,'2025-09-22 10:02:56'),(24,160,'48-70',57.50,'2025-09-22 10:02:56'),(26,162,'18-22',52.50,'2025-09-22 10:02:56'),(27,162,'23-27',54.50,'2025-09-22 10:02:56'),(28,162,'28-32',56.00,'2025-09-22 10:02:56'),(29,162,'33-37',57.50,'2025-09-22 10:02:56'),(30,162,'38-42',58.00,'2025-09-22 10:02:56'),(31,162,'43-47',58.50,'2025-09-22 10:02:56'),(32,162,'48-70',59.00,'2025-09-22 10:02:56'),(34,164,'18-22',53.50,'2025-09-22 10:02:56'),(35,164,'23-27',55.50,'2025-09-22 10:02:56'),(36,164,'28-32',57.50,'2025-09-22 10:02:56'),(37,164,'33-37',59.00,'2025-09-22 10:02:56'),(38,164,'38-42',59.50,'2025-09-22 10:02:56'),(39,164,'43-47',60.00,'2025-09-22 10:02:56'),(40,164,'48-70',60.50,'2025-09-22 10:02:56'),(42,166,'18-22',55.00,'2025-09-22 10:02:56'),(43,166,'23-27',57.00,'2025-09-22 10:02:56'),(44,166,'28-32',59.00,'2025-09-22 10:02:56'),(45,166,'33-37',60.50,'2025-09-22 10:02:56'),(46,166,'38-42',61.00,'2025-09-22 10:02:56'),(47,166,'43-47',61.50,'2025-09-22 10:02:56'),(48,166,'48-70',62.00,'2025-09-22 10:02:56'),(50,168,'18-22',56.50,'2025-09-22 10:02:56'),(51,168,'23-27',58.50,'2025-09-22 10:02:56'),(52,168,'28-32',60.50,'2025-09-22 10:02:56'),(53,168,'33-37',62.00,'2025-09-22 10:02:56'),(54,168,'38-42',63.00,'2025-09-22 10:02:56'),(55,168,'43-47',63.50,'2025-09-22 10:02:56'),(56,168,'48-70',64.00,'2025-09-22 10:02:56'),(58,170,'18-22',58.00,'2025-09-22 10:02:56'),(59,170,'23-27',60.00,'2025-09-22 10:02:56'),(60,170,'28-32',62.00,'2025-09-22 10:02:56'),(61,170,'33-37',64.00,'2025-09-22 10:02:56'),(62,170,'38-42',64.50,'2025-09-22 10:02:56'),(63,170,'43-47',65.00,'2025-09-22 10:02:56'),(64,170,'48-70',65.50,'2025-09-22 10:02:56'),(66,172,'18-22',60.00,'2025-09-22 10:02:56'),(67,172,'23-27',61.50,'2025-09-22 10:02:56'),(68,172,'28-32',63.50,'2025-09-22 10:02:56'),(69,172,'33-37',65.50,'2025-09-22 10:02:56'),(70,172,'38-42',66.00,'2025-09-22 10:02:56'),(71,172,'43-47',66.50,'2025-09-22 10:02:56'),(72,172,'48-70',67.50,'2025-09-22 10:02:56'),(74,174,'18-22',61.00,'2025-09-22 10:02:56'),(75,174,'23-27',63.50,'2025-09-22 10:02:56'),(76,174,'28-32',65.50,'2025-09-22 10:02:56'),(77,174,'33-37',67.50,'2025-09-22 10:02:56'),(78,174,'38-42',68.00,'2025-09-22 10:02:56'),(79,174,'43-47',68.50,'2025-09-22 10:02:56'),(80,174,'48-70',69.00,'2025-09-22 10:02:56'),(82,176,'18-22',62.50,'2025-09-22 10:02:56'),(83,176,'23-27',65.00,'2025-09-22 10:02:56'),(84,176,'28-32',67.00,'2025-09-22 10:02:56'),(85,176,'33-37',69.00,'2025-09-22 10:02:56'),(86,176,'38-42',69.50,'2025-09-22 10:02:56'),(87,176,'43-47',70.00,'2025-09-22 10:02:56'),(88,176,'48-70',71.00,'2025-09-22 10:02:56'),(90,178,'18-22',64.00,'2025-09-22 10:02:56'),(91,178,'23-27',66.50,'2025-09-22 10:02:56'),(92,178,'28-32',68.50,'2025-09-22 10:02:56'),(93,178,'33-37',70.50,'2025-09-22 10:02:56'),(94,178,'38-42',71.50,'2025-09-22 10:02:56'),(95,178,'43-47',72.00,'2025-09-22 10:02:56'),(96,178,'48-70',72.50,'2025-09-22 10:02:56'),(98,180,'18-22',65.50,'2025-09-22 10:02:56'),(99,180,'23-27',68.00,'2025-09-22 10:02:56'),(100,180,'28-32',70.50,'2025-09-22 10:02:56'),(101,180,'33-37',72.50,'2025-09-22 10:02:56'),(102,180,'38-42',73.00,'2025-09-22 10:02:56'),(103,180,'43-47',74.00,'2025-09-22 10:02:56'),(104,180,'48-70',74.50,'2025-09-22 10:02:56'),(106,182,'18-22',67.50,'2025-09-22 10:02:56'),(107,182,'23-27',69.50,'2025-09-22 10:02:56'),(108,182,'28-32',72.00,'2025-09-22 10:02:56'),(109,182,'33-37',74.00,'2025-09-22 10:02:56'),(110,182,'38-42',75.00,'2025-09-22 10:02:56'),(111,182,'43-47',75.50,'2025-09-22 10:02:56'),(112,182,'48-70',76.50,'2025-09-22 10:02:56'),(114,184,'18-22',70.00,'2025-09-22 10:02:56'),(115,184,'23-27',71.50,'2025-09-22 10:02:56'),(116,184,'28-32',74.00,'2025-09-22 10:02:56'),(117,184,'33-37',76.00,'2025-09-22 10:02:56'),(118,184,'38-42',76.50,'2025-09-22 10:02:56'),(119,184,'43-47',77.50,'2025-09-22 10:02:56'),(120,184,'48-70',78.00,'2025-09-22 10:02:56'),(122,186,'18-22',70.50,'2025-09-22 10:02:56'),(123,186,'23-27',73.00,'2025-09-22 10:02:56'),(124,186,'28-32',75.50,'2025-09-22 10:02:56'),(125,186,'33-37',78.00,'2025-09-22 10:02:56'),(126,186,'38-42',78.50,'2025-09-22 10:02:56'),(127,186,'43-47',79.00,'2025-09-22 10:02:56'),(128,186,'48-70',80.00,'2025-09-22 10:02:56'),(130,188,'18-22',72.00,'2025-09-22 10:02:56'),(131,188,'23-27',75.00,'2025-09-22 10:02:56'),(132,188,'28-32',77.60,'2025-09-22 10:02:56'),(133,188,'33-37',79.50,'2025-09-22 10:02:56'),(134,188,'38-42',80.00,'2025-09-22 10:02:56'),(135,188,'43-47',81.00,'2025-09-22 10:02:56'),(136,188,'48-70',82.00,'2025-09-22 10:02:56'),(138,190,'18-22',73.50,'2025-09-22 10:02:56'),(139,190,'23-27',76.00,'2025-09-22 10:02:56'),(140,190,'28-32',78.50,'2025-09-22 10:02:56'),(141,190,'33-37',80.50,'2025-09-22 10:02:56'),(142,190,'38-42',81.00,'2025-09-22 10:02:56'),(143,190,'43-47',82.00,'2025-09-22 10:02:56'),(144,190,'48-70',83.00,'2025-09-22 10:02:56');
/*!40000 ALTER TABLE `ideal_weights` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `leave_details`
--

DROP TABLE IF EXISTS `leave_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leave_details` (
  `id` int NOT NULL AUTO_INCREMENT,
  `personnel_id` int NOT NULL,
  `army_number` varchar(100) NOT NULL,
  `sr_no` int DEFAULT NULL,
  `year` varchar(10) DEFAULT NULL,
  `al_days` int DEFAULT NULL,
  `cl_days` int DEFAULT NULL,
  `aal_days` int DEFAULT NULL,
  `total_days` int DEFAULT NULL,
  `remarks` text,
  PRIMARY KEY (`id`),
  KEY `idx_army_number` (`army_number`),
  KEY `idx_personnel_id_leave` (`personnel_id`),
  CONSTRAINT `leave_details_ibfk_1` FOREIGN KEY (`personnel_id`) REFERENCES `personnel` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leave_details`
--

LOCK TABLES `leave_details` WRITE;
/*!40000 ALTER TABLE `leave_details` DISABLE KEYS */;
INSERT INTO `leave_details` VALUES (1,1,'778G',1,'2024',20,10,5,35,'Utilized for family'),(2,2,'156WE',1,'2024',20,10,5,35,'Utilized for family'),(3,3,'1526WE',1,'2024',20,10,5,35,'Utilized for family'),(4,4,'9926WE',1,'2024',20,10,5,35,'Utilized for family'),(5,5,'99226WE',1,'2024',20,10,5,35,'Utilized for family'),(6,6,'966WE',1,'2024',20,10,5,35,'Utilized for family'),(7,7,'87CESR',1,'2024',20,10,5,35,'Utilized for family'),(8,8,'997CESR',1,'2024',20,10,5,35,'Utilized for family'),(9,10,'965CESR',1,'2024',20,10,5,35,'Utilized for family'),(10,12,'905CESR',1,'2024',20,10,5,35,'Utilized for family'),(11,13,'9085CESR',1,'2024',20,10,5,35,'Utilized for family'),(12,14,'25CESR',1,'2024',20,10,5,35,'Utilized for family'),(13,15,'165CESR',1,'2024',20,10,5,35,'Utilized for family'),(14,16,'775CESR',1,'2024',20,10,5,35,'Utilized for family'),(15,17,'984CESR',1,'2024',20,10,5,35,'Utilized for family'),(16,18,'994CESR',1,'2024',20,10,5,35,'Utilized for family'),(17,19,'99999CESR',1,'2024',20,10,5,35,'Utilized for family');
/*!40000 ALTER TABLE `leave_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `leave_status_info`
--

DROP TABLE IF EXISTS `leave_status_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leave_status_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `army_number` varchar(20) NOT NULL,
  `leave_type` varchar(50) NOT NULL,
  `leave_days` int NOT NULL,
  `request_sent_to` varchar(100) NOT NULL,
  `request_status` enum('Pending','Approved','Rejected') DEFAULT 'Pending',
  `approval_date` datetime DEFAULT NULL,
  `rejected_date` datetime DEFAULT NULL,
  `remarks` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leave_status_info`
--

LOCK TABLES `leave_status_info` WRITE;
/*!40000 ALTER TABLE `leave_status_info` DISABLE KEYS */;
INSERT INTO `leave_status_info` VALUES (1,'778G','AL',10,'OC','Approved','2025-11-25 02:59:52',NULL,'AL for 10 day(s)','2025-11-24 21:18:25','2025-11-24 21:29:52'),(2,'778G','AL',10,'OC','Pending',NULL,NULL,'AL for 10 day(s)','2025-11-24 21:42:38','2025-11-24 21:42:38');
/*!40000 ALTER TABLE `leave_status_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loans`
--

DROP TABLE IF EXISTS `loans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loans` (
  `id` int NOT NULL AUTO_INCREMENT,
  `personnel_id` int NOT NULL,
  `army_number` varchar(100) NOT NULL,
  `sr_no` int DEFAULT NULL,
  `loan_type` varchar(255) DEFAULT NULL,
  `total_amount` decimal(15,2) DEFAULT NULL,
  `bank_details` varchar(255) DEFAULT NULL,
  `emi_per_month` decimal(15,2) DEFAULT NULL,
  `pending` decimal(15,2) DEFAULT NULL,
  `remarks` text,
  PRIMARY KEY (`id`),
  KEY `idx_army_number` (`army_number`),
  KEY `idx_personnel_id_loans` (`personnel_id`),
  CONSTRAINT `loans_ibfk_1` FOREIGN KEY (`personnel_id`) REFERENCES `personnel` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loans`
--

LOCK TABLES `loans` WRITE;
/*!40000 ALTER TABLE `loans` DISABLE KEYS */;
INSERT INTO `loans` VALUES (1,1,'778G',1,'Home Loan',5000000.00,'SBI',25000.00,3000000.00,'Repaying on time'),(2,2,'156WE',1,'Home Loan',5000000.00,'SBI',25000.00,3000000.00,'Repaying on time'),(3,3,'1526WE',1,'Home Loan',5000000.00,'SBI',25000.00,3000000.00,'Repaying on time'),(4,4,'9926WE',1,'Home Loan',5000000.00,'SBI',25000.00,3000000.00,'Repaying on time'),(5,5,'99226WE',1,'Home Loan',5000000.00,'SBI',25000.00,3000000.00,'Repaying on time'),(6,6,'966WE',1,'Home Loan',5000000.00,'SBI',25000.00,3000000.00,'Repaying on time'),(7,7,'87CESR',1,'Home Loan',5000000.00,'SBI',25000.00,3000000.00,'Repaying on time'),(8,8,'997CESR',1,'Home Loan',5000000.00,'SBI',25000.00,3000000.00,'Repaying on time'),(9,10,'965CESR',1,'Home Loan',5000000.00,'SBI',25000.00,3000000.00,'Repaying on time'),(10,12,'905CESR',1,'Home Loan',5000000.00,'SBI',25000.00,3000000.00,'Repaying on time'),(11,13,'9085CESR',1,'Home Loan',5000000.00,'SBI',25000.00,3000000.00,'Repaying on time'),(12,14,'25CESR',1,'Home Loan',5000000.00,'SBI',25000.00,3000000.00,'Repaying on time'),(13,15,'165CESR',1,'Home Loan',5000000.00,'SBI',25000.00,3000000.00,'Repaying on time'),(14,16,'775CESR',1,'Home Loan',5000000.00,'SBI',25000.00,3000000.00,'Repaying on time'),(15,17,'984CESR',1,'Home Loan',5000000.00,'SBI',25000.00,3000000.00,'Repaying on time'),(16,18,'994CESR',1,'Home Loan',5000000.00,'SBI',25000.00,3000000.00,'Repaying on time'),(17,19,'99999CESR',1,'Home Loan',5000000.00,'SBI',25000.00,3000000.00,'Repaying on time');
/*!40000 ALTER TABLE `loans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marital_discord_cases`
--

DROP TABLE IF EXISTS `marital_discord_cases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `marital_discord_cases` (
  `id` int NOT NULL AUTO_INCREMENT,
  `personnel_id` int NOT NULL,
  `army_number` varchar(100) NOT NULL,
  `sr_no` int DEFAULT NULL,
  `case_no` varchar(100) DEFAULT NULL,
  `amount_to_pay` decimal(15,2) DEFAULT NULL,
  `sanction_letter_no` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_army_number` (`army_number`),
  KEY `idx_personnel_id_discord` (`personnel_id`),
  CONSTRAINT `marital_discord_cases_ibfk_1` FOREIGN KEY (`personnel_id`) REFERENCES `personnel` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marital_discord_cases`
--

LOCK TABLES `marital_discord_cases` WRITE;
/*!40000 ALTER TABLE `marital_discord_cases` DISABLE KEYS */;
INSERT INTO `marital_discord_cases` VALUES (1,1,'778G',1,'MD-001',10000.00,'SL/2023/001'),(2,2,'156WE',1,'MD-001',10000.00,'SL/2023/001'),(3,3,'1526WE',1,'MD-001',10000.00,'SL/2023/001'),(4,4,'9926WE',1,'MD-001',10000.00,'SL/2023/001'),(5,5,'99226WE',1,'MD-001',10000.00,'SL/2023/001'),(6,6,'966WE',1,'MD-001',10000.00,'SL/2023/001'),(7,7,'87CESR',1,'MD-001',10000.00,'SL/2023/001'),(8,8,'997CESR',1,'MD-001',10000.00,'SL/2023/001'),(9,10,'965CESR',1,'MD-001',10000.00,'SL/2023/001'),(10,12,'905CESR',1,'MD-001',10000.00,'SL/2023/001'),(11,13,'9085CESR',1,'MD-001',10000.00,'SL/2023/001'),(12,14,'25CESR',1,'MD-001',10000.00,'SL/2023/001'),(13,15,'165CESR',1,'MD-001',10000.00,'SL/2023/001'),(14,16,'775CESR',1,'MD-001',10000.00,'SL/2023/001'),(15,17,'984CESR',1,'MD-001',10000.00,'SL/2023/001'),(16,18,'994CESR',1,'MD-001',10000.00,'SL/2023/001'),(17,19,'99999CESR',1,'MD-001',10000.00,'SL/2023/001');
/*!40000 ALTER TABLE `marital_discord_cases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mobile_phones`
--

DROP TABLE IF EXISTS `mobile_phones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mobile_phones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `personnel_id` int NOT NULL,
  `army_number` varchar(100) NOT NULL,
  `sr_no` int DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `number` varchar(50) DEFAULT NULL,
  `service_provider` varchar(100) DEFAULT NULL,
  `remarks` text,
  PRIMARY KEY (`id`),
  KEY `idx_army_number` (`army_number`),
  KEY `idx_personnel_id_mobiles` (`personnel_id`),
  CONSTRAINT `mobile_phones_ibfk_1` FOREIGN KEY (`personnel_id`) REFERENCES `personnel` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mobile_phones`
--

LOCK TABLES `mobile_phones` WRITE;
/*!40000 ALTER TABLE `mobile_phones` DISABLE KEYS */;
INSERT INTO `mobile_phones` VALUES (1,1,'778G',1,'Personal','9876543210','Airtel','Active'),(2,2,'156WE',1,'Personal','9876543210','Airtel','Active'),(3,3,'1526WE',1,'Personal','9876543210','Airtel','Active'),(4,4,'9926WE',1,'Personal','9876543210','Airtel','Active'),(5,5,'99226WE',1,'Personal','9876543210','Airtel','Active'),(6,6,'966WE',1,'Personal','9876543210','Airtel','Active'),(7,7,'87CESR',1,'Personal','9876543210','Airtel','Active'),(8,8,'997CESR',1,'Personal','9876543210','Airtel','Active'),(9,10,'965CESR',1,'Personal','9876543210','Airtel','Active'),(10,12,'905CESR',1,'Personal','9876543210','Airtel','Active'),(11,13,'9085CESR',1,'Personal','9876543210','Airtel','Active'),(12,14,'25CESR',1,'Personal','9876543210','Airtel','Active'),(13,15,'165CESR',1,'Personal','9876543210','Airtel','Active'),(14,16,'775CESR',1,'Personal','9876543210','Airtel','Active'),(15,17,'984CESR',1,'Personal','9876543210','Airtel','Active'),(16,18,'994CESR',1,'Personal','9876543210','Airtel','Active'),(17,19,'99999CESR',1,'Personal','9876543210','Airtel','Active');
/*!40000 ALTER TABLE `mobile_phones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personnel`
--

DROP TABLE IF EXISTS `personnel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personnel` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `army_number` varchar(100) NOT NULL,
  `rank` varchar(100) NOT NULL,
  `trade` varchar(100) NOT NULL,
  `date_of_enrollment` date NOT NULL,
  `date_of_birth` date NOT NULL,
  `date_of_tos` date DEFAULT NULL,
  `date_of_tors` date DEFAULT NULL,
  `blood_group` varchar(10) NOT NULL,
  `religion` varchar(100) NOT NULL,
  `food_preference` varchar(50) NOT NULL,
  `drinker` varchar(10) NOT NULL,
  `civ_qualifications` text,
  `decoration_awards` text,
  `lacking_qualifications` text,
  `willing_promotions` varchar(10) NOT NULL,
  `i_card_no` varchar(100) DEFAULT NULL,
  `i_card_date` date DEFAULT NULL,
  `i_card_issued_by` varchar(255) DEFAULT NULL,
  `bpet_grading` varchar(50) DEFAULT NULL,
  `ppt_grading` varchar(50) DEFAULT NULL,
  `bpet_date` date DEFAULT NULL,
  `clothing_card` varchar(10) DEFAULT NULL,
  `pan_card_no` varchar(50) DEFAULT NULL,
  `pan_part_ii` varchar(100) DEFAULT NULL,
  `aadhar_card_no` varchar(20) DEFAULT NULL,
  `aadhar_part_ii` varchar(100) DEFAULT NULL,
  `joint_account_no` varchar(100) DEFAULT NULL,
  `joint_account_bank` varchar(255) DEFAULT NULL,
  `joint_account_ifsc` varchar(20) DEFAULT NULL,
  `home_house_no` varchar(255) DEFAULT NULL,
  `home_village` varchar(255) DEFAULT NULL,
  `home_phone` varchar(50) DEFAULT NULL,
  `home_to` varchar(255) DEFAULT NULL,
  `home_po` varchar(255) DEFAULT NULL,
  `home_ps` varchar(255) DEFAULT NULL,
  `home_teh` varchar(255) DEFAULT NULL,
  `home_nrs` varchar(255) DEFAULT NULL,
  `home_nmh` varchar(255) DEFAULT NULL,
  `home_district` varchar(255) DEFAULT NULL,
  `home_state` varchar(255) DEFAULT NULL,
  `border_area` varchar(10) DEFAULT NULL,
  `distance_from_ib` decimal(10,2) DEFAULT NULL,
  `height` decimal(10,2) DEFAULT NULL,
  `weight` decimal(10,2) DEFAULT NULL,
  `chest` decimal(10,2) DEFAULT NULL,
  `identification_marks` varchar(255) DEFAULT NULL,
  `court_cases` text,
  `loan` varchar(10) DEFAULT NULL,
  `total_leaves_encashed` int DEFAULT NULL,
  `participation_activities` text,
  `present_family_location` text,
  `prior_station` varchar(10) DEFAULT NULL,
  `prior_station_date` date DEFAULT NULL,
  `worked_it` varchar(10) DEFAULT NULL,
  `worked_unit_tenure` varchar(255) DEFAULT NULL,
  `med_cat` varchar(10) DEFAULT NULL,
  `last_recat_bd_date` date DEFAULT NULL,
  `last_recat_bd_at` varchar(255) DEFAULT NULL,
  `next_recat_due` date DEFAULT NULL,
  `medical_problem` text,
  `restrictions` text,
  `computer_knowledge` varchar(50) DEFAULT NULL,
  `it_literature` varchar(50) DEFAULT NULL,
  `kin_name` varchar(255) DEFAULT NULL,
  `kin_relation` varchar(100) DEFAULT NULL,
  `kin_marriage_date` date DEFAULT NULL,
  `kin_account_no` varchar(100) DEFAULT NULL,
  `kin_bank` varchar(255) DEFAULT NULL,
  `kin_ifsc` varchar(20) DEFAULT NULL,
  `kin_part_ii` varchar(100) DEFAULT NULL,
  `vehicle_reg_no` varchar(100) DEFAULT NULL,
  `vehicle_model` varchar(255) DEFAULT NULL,
  `vehicle_purchase_date` date DEFAULT NULL,
  `vehicle_agif` varchar(10) DEFAULT NULL,
  `driving_license_no` varchar(100) DEFAULT NULL,
  `license_issue_date` date DEFAULT NULL,
  `license_expiry_date` date DEFAULT NULL,
  `disability_child` varchar(10) DEFAULT NULL,
  `marital_discord` varchar(10) DEFAULT NULL,
  `counselling` text,
  `folder_prepared_on` date DEFAULT NULL,
  `folder_checked_by` varchar(255) DEFAULT NULL,
  `bring_family` varchar(10) DEFAULT NULL,
  `domestic_issues` text,
  `other_requests` text,
  `family_medical_issues` text,
  `quality_points` text,
  `strengths` text,
  `weaknesses` text,
  `detailed_course` varchar(10) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `company` varchar(100) DEFAULT NULL,
  `onleave_status` tinyint(1) DEFAULT '0',
  `detachment_status` tinyint(1) DEFAULT '0',
  `posting_status` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `army_number` (`army_number`),
  KEY `idx_personnel_army_number` (`army_number`),
  KEY `idx_personnel_name` (`name`),
  KEY `idx_personnel_rank` (`rank`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personnel`
--

LOCK TABLES `personnel` WRITE;
/*!40000 ALTER TABLE `personnel` DISABLE KEYS */;
INSERT INTO `personnel` VALUES (1,'ABC','778G','JCO','Infantry','2010-05-15','1985-03-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-23 07:27:16','2025-11-25 22:33:24','1 Company',0,0,0),(2,'Srivastav','156WE','Agniveer','Infantry','2010-05-15','2002-03-20','2015-01-10','2020-06-01','O+','Muslim','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 05:56:59','2025-11-25 01:47:34','1 Company',0,0,0),(3,'Vivek','1526WE','Agniveer','Infantry','2010-05-15','2001-03-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 05:57:55','2025-11-25 01:47:34','2 Company',0,0,0),(4,'Gugar','9926WE','Agniveer','Infantry','2010-05-15','1994-03-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 05:58:25','2025-11-25 01:47:34','4 Company',0,0,0),(5,'Abishek','99226WE','Agniveer','Infantry','2010-05-15','1960-03-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 06:00:05','2025-11-25 01:15:03','3 Company',0,1,0),(6,'Raju','966WE','Signal Man','Infantry','2010-05-15','1986-09-20','2015-01-10','2020-06-01','O+','Muslim','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 06:03:59','2025-11-25 21:42:21','3 Company',0,0,1),(7,'Rohit','87CESR','Signal Man','Infantry','2010-05-15','1989-09-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 06:04:31','2025-11-25 01:47:34','3 Company',0,0,0),(8,'Prateeq','997CESR','Signal Man','Infantry','2010-05-15','1967-09-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 06:05:21','2025-11-25 01:47:34','3 Company',0,0,0),(10,'Rahul','965CESR','Signal Man','Infantry','2010-05-15','1987-09-20','2015-01-10','2020-06-01','O+','Hindu','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 06:06:06','2025-11-25 01:47:34','2 Company',0,0,0),(12,'Hardik','905CESR','Signal Man','Infantry','2010-05-15','1997-09-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 06:06:35','2025-11-25 22:27:43','2 Company',0,0,0),(13,'Kurnal','9085CESR','Signal Man','Infantry','2010-05-15','1989-09-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 06:07:05','2025-11-25 23:21:06','2 Company',0,0,0),(14,'Gill','25CESR','OC','Infantry','2010-05-15','1987-09-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 06:07:40','2025-11-25 01:47:34','2 Company',0,0,0),(15,'Raju','165CESR','OC','Infantry','2010-05-15','1987-09-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 06:08:03','2025-11-25 01:47:34','1 Company',0,0,0),(16,'ABC','775CESR','Subedar','Infantry','2010-05-15','1999-09-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 06:18:15','2025-11-25 01:47:34','1 Company',0,0,1),(17,'ABC','984CESR','Subedar','Infantry','2010-05-15','1979-09-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 06:18:42','2025-11-25 01:47:34','1 Company',0,0,0),(18,'Aijaz','994CESR','Subedar','Infantry','2010-05-15','1990-09-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 06:19:13','2025-11-25 01:47:34','1 Company',0,0,0),(19,'Aijaz','99999CESR','Subedar','Infantry','2010-05-15','1990-09-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 09:44:27','2025-11-25 01:47:34','4 Company',0,0,0);
/*!40000 ALTER TABLE `personnel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personnel_sports`
--

DROP TABLE IF EXISTS `personnel_sports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personnel_sports` (
  `id` int NOT NULL AUTO_INCREMENT,
  `personnel_id` int NOT NULL,
  `army_number` varchar(50) NOT NULL,
  `sport_type` varchar(50) NOT NULL,
  `sport_name` varchar(100) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personnel_sports`
--

LOCK TABLES `personnel_sports` WRITE;
/*!40000 ALTER TABLE `personnel_sports` DISABLE KEYS */;
INSERT INTO `personnel_sports` VALUES (1,1,'ARMY001','Football','Football','2025-11-28 15:08:37'),(2,1,'ARMY001','Cricket','Cricket','2025-11-28 15:08:37'),(3,2,'ARMY002','Basketball','Basketball','2025-11-28 15:08:37'),(4,2,'ARMY002','Other','Table Tennis','2025-11-28 15:08:37'),(5,3,'ARMY003','Athletics','Athletics','2025-11-28 15:08:37'),(6,3,'ARMY003','Other','Badminton','2025-11-28 15:08:37'),(7,4,'ARMY004','Swimming','Swimming','2025-11-28 15:08:37'),(8,5,'ARMY005','Other','Volleyball','2025-11-28 15:08:37'),(9,5,'ARMY005','Other','Hockey','2025-11-28 15:08:37'),(10,11,'ARMY001545','Football','Football','2025-11-28 15:09:27');
/*!40000 ALTER TABLE `personnel_sports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `posting_details_table`
--

DROP TABLE IF EXISTS `posting_details_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `posting_details_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `army_number` varchar(15) NOT NULL,
  `action_type` varchar(10) NOT NULL,
  `posting_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `army_number` (`army_number`),
  CONSTRAINT `posting_details_table_ibfk_1` FOREIGN KEY (`army_number`) REFERENCES `personnel` (`army_number`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `posting_details_table`
--

LOCK TABLES `posting_details_table` WRITE;
/*!40000 ALTER TABLE `posting_details_table` DISABLE KEYS */;
INSERT INTO `posting_details_table` VALUES (1,'966WE','P2','2025-11-26 03:12:21');
/*!40000 ALTER TABLE `posting_details_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `punishments`
--

DROP TABLE IF EXISTS `punishments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `punishments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `personnel_id` int NOT NULL,
  `army_number` varchar(100) NOT NULL,
  `sr_no` int DEFAULT NULL,
  `punishment_date` date DEFAULT NULL,
  `punishment` varchar(255) DEFAULT NULL,
  `aa_sec` varchar(100) DEFAULT NULL,
  `remarks` text,
  PRIMARY KEY (`id`),
  KEY `idx_army_number` (`army_number`),
  KEY `idx_personnel_id_punishments` (`personnel_id`),
  CONSTRAINT `punishments_ibfk_1` FOREIGN KEY (`personnel_id`) REFERENCES `personnel` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `punishments`
--

LOCK TABLES `punishments` WRITE;
/*!40000 ALTER TABLE `punishments` DISABLE KEYS */;
INSERT INTO `punishments` VALUES (1,1,'778G',1,'2018-02-10','Red Ink','Section 39','Minor infraction'),(2,2,'156WE',1,'2018-02-10','Red Ink','Section 39','Minor infraction'),(3,3,'1526WE',1,'2018-02-10','Red Ink','Section 39','Minor infraction'),(4,4,'9926WE',1,'2018-02-10','Red Ink','Section 39','Minor infraction'),(5,5,'99226WE',1,'2018-02-10','Red Ink','Section 39','Minor infraction'),(6,6,'966WE',1,'2018-02-10','Red Ink','Section 39','Minor infraction'),(7,7,'87CESR',1,'2018-02-10','Red Ink','Section 39','Minor infraction'),(8,8,'997CESR',1,'2018-02-10','Red Ink','Section 39','Minor infraction'),(9,10,'965CESR',1,'2018-02-10','Red Ink','Section 39','Minor infraction'),(10,12,'905CESR',1,'2018-02-10','Red Ink','Section 39','Minor infraction'),(11,13,'9085CESR',1,'2018-02-10','Red Ink','Section 39','Minor infraction'),(12,14,'25CESR',1,'2018-02-10','Red Ink','Section 39','Minor infraction'),(13,15,'165CESR',1,'2018-02-10','Red Ink','Section 39','Minor infraction'),(14,16,'775CESR',1,'2018-02-10','Red Ink','Section 39','Minor infraction'),(15,17,'984CESR',1,'2018-02-10','Red Ink','Section 39','Minor infraction'),(16,18,'994CESR',1,'2018-02-10','Red Ink','Section 39','Minor infraction'),(17,19,'99999CESR',1,'2018-02-10','Red Ink','Section 39','Minor infraction');
/*!40000 ALTER TABLE `punishments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales`
--

DROP TABLE IF EXISTS `sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `liquor_sale` int NOT NULL,
  `grocery_sale` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales`
--

LOCK TABLES `sales` WRITE;
/*!40000 ALTER TABLE `sales` DISABLE KEYS */;
INSERT INTO `sales` VALUES (1,'2025-01-01',18000,12000),(2,'2025-01-02',17500,11800),(3,'2025-01-03',22000,13500),(4,'2025-01-04',24500,14200),(5,'2025-01-05',21000,12800),(6,'2025-01-06',16500,11000),(7,'2025-01-07',17000,11500),(8,'2025-01-08',22500,13000),(9,'2025-01-09',24000,14500),(10,'2025-01-10',26000,15000),(11,'2025-01-11',19500,12200),(12,'2025-01-12',20500,12500),(13,'2025-01-13',23000,13800),(14,'2025-01-14',25000,14000),(15,'2025-01-15',27000,15500),(16,'2025-01-16',17500,11800),(17,'2025-01-17',18500,12300),(18,'2025-01-18',23500,13700),(19,'2025-01-19',25500,14900),(20,'2025-01-20',26500,15200),(21,'2025-01-21',19000,12100),(22,'2025-01-22',20000,12600),(23,'2025-01-23',24000,13500),(24,'2025-01-24',26000,14800),(25,'2025-01-25',27500,15800),(26,'2025-01-26',18500,12000),(27,'2025-01-27',19500,12500),(28,'2025-01-28',24500,14000),(29,'2025-01-29',26500,15000),(30,'2025-01-30',28000,16000);
/*!40000 ALTER TABLE `sales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_items`
--

DROP TABLE IF EXISTS `store_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_items` (
  `item_id` int NOT NULL AUTO_INCREMENT,
  `store_id` int DEFAULT NULL,
  `qlp_no` varchar(50) DEFAULT NULL,
  `slp_no` varchar(50) DEFAULT NULL,
  `nomenclature` varchar(200) DEFAULT NULL,
  `au` varchar(20) DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  PRIMARY KEY (`item_id`),
  KEY `store_id` (`store_id`),
  CONSTRAINT `store_items_ibfk_1` FOREIGN KEY (`store_id`) REFERENCES `stores` (`store_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_items`
--

LOCK TABLES `store_items` WRITE;
/*!40000 ALTER TABLE `store_items` DISABLE KEYS */;
INSERT INTO `store_items` VALUES (3,7,NULL,NULL,'XYZ','nos',10);
/*!40000 ALTER TABLE `store_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stores`
--

DROP TABLE IF EXISTS `stores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stores` (
  `store_id` int NOT NULL AUTO_INCREMENT,
  `store_name` varchar(100) NOT NULL,
  `place` varchar(100) DEFAULT NULL,
  `incharge_name` varchar(100) DEFAULT NULL,
  `total_items` int DEFAULT '0',
  PRIMARY KEY (`store_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stores`
--

LOCK TABLES `stores` WRITE;
/*!40000 ALTER TABLE `stores` DISABLE KEYS */;
INSERT INTO `stores` VALUES (7,'ST1','Dighi',NULL,0);
/*!40000 ALTER TABLE `stores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tasks`
--

DROP TABLE IF EXISTS `tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tasks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_name` varchar(200) NOT NULL,
  `description` text,
  `priority` varchar(10) DEFAULT 'medium',
  `assigned_to` varchar(255) DEFAULT NULL,
  `assigned_by` varchar(255) DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  CONSTRAINT `tasks_chk_1` CHECK ((`priority` in (_utf8mb4'low',_utf8mb4'medium',_utf8mb4'high',_utf8mb4'urgent')))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasks`
--

LOCK TABLES `tasks` WRITE;
/*!40000 ALTER TABLE `tasks` DISABLE KEYS */;
INSERT INTO `tasks` VALUES (1,'Room alot','asdfdsaf','Medium','2342','CO','2025-11-28','2025-11-27 06:31:01'),(2,'WQEW','fsdaf','Medium','1212','CO','2025-11-29','2025-11-27 06:31:52'),(3,'Volley tournament','Arrange an volleyball tournament','High','342429','CO','2025-11-28','2025-11-28 14:45:32');
/*!40000 ALTER TABLE `tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `units_served`
--

DROP TABLE IF EXISTS `units_served`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `units_served` (
  `id` int NOT NULL AUTO_INCREMENT,
  `personnel_id` int NOT NULL,
  `army_number` varchar(100) NOT NULL,
  `sr_no` int DEFAULT NULL,
  `unit` varchar(255) DEFAULT NULL,
  `from_date` date DEFAULT NULL,
  `to_date` date DEFAULT NULL,
  `duty_performed` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_army_number` (`army_number`),
  KEY `idx_personnel_id_units` (`personnel_id`),
  CONSTRAINT `units_served_ibfk_1` FOREIGN KEY (`personnel_id`) REFERENCES `personnel` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `units_served`
--

LOCK TABLES `units_served` WRITE;
/*!40000 ALTER TABLE `units_served` DISABLE KEYS */;
INSERT INTO `units_served` VALUES (1,1,'778G',1,'1st Battalion','2010-05-15','2015-05-15','Platoon Commander'),(2,2,'156WE',1,'1st Battalion','2010-05-15','2015-05-15','Platoon Commander'),(3,3,'1526WE',1,'1st Battalion','2010-05-15','2015-05-15','Platoon Commander'),(4,4,'9926WE',1,'1st Battalion','2010-05-15','2015-05-15','Platoon Commander'),(5,5,'99226WE',1,'1st Battalion','2010-05-15','2015-05-15','Platoon Commander'),(6,6,'966WE',1,'1st Battalion','2010-05-15','2015-05-15','Platoon Commander'),(7,7,'87CESR',1,'1st Battalion','2010-05-15','2015-05-15','Platoon Commander'),(8,8,'997CESR',1,'1st Battalion','2010-05-15','2015-05-15','Platoon Commander'),(9,10,'965CESR',1,'1st Battalion','2010-05-15','2015-05-15','Platoon Commander'),(10,12,'905CESR',1,'1st Battalion','2010-05-15','2015-05-15','Platoon Commander'),(11,13,'9085CESR',1,'1st Battalion','2010-05-15','2015-05-15','Platoon Commander'),(12,14,'25CESR',1,'1st Battalion','2010-05-15','2015-05-15','Platoon Commander'),(13,15,'165CESR',1,'1st Battalion','2010-05-15','2015-05-15','Platoon Commander'),(14,16,'775CESR',1,'1st Battalion','2010-05-15','2015-05-15','Platoon Commander'),(15,17,'984CESR',1,'1st Battalion','2010-05-15','2015-05-15','Platoon Commander'),(16,18,'994CESR',1,'1st Battalion','2010-05-15','2015-05-15','Platoon Commander'),(17,19,'99999CESR',1,'1st Battalion','2010-05-15','2015-05-15','Platoon Commander');
/*!40000 ALTER TABLE `units_served` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(50) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'RAVI KUMAR','ravi@gmail.com','ravi@123','CO','2025-11-19 06:28:38'),(2,'RAHUL SINGH','rahul.oc@gmail.com','rahul@123','OC','2025-11-19 06:42:10'),(3,'SACHIN SHARMA','sachin.adj@gmail.com','sachin@123','ADJUTANT','2025-11-19 06:45:22'),(4,'MANOJ SINGH','manoj.jco@gmail.com','manoj@123','JCO','2025-11-18 04:52:55'),(5,'AKHILESH VERMA','akhil.jco@gmail.com','akhil@123','JCO','2025-11-18 06:15:33'),(6,'SUNIL KUMAR','sunil.or@gmail.com','sunil@123','OR','2025-11-17 03:48:20'),(7,'VIJAY KUMAR','vijay.or@gmail.com','vijay@123','OR','2025-11-17 09:10:11'),(8,'ARUN SHARMA','arun.clerk@gmail.com','arun@123','CLERK','2025-11-16 03:20:45'),(9,'ROHIT YADAV','rohit.clerk@gmail.com','rohit@123','CLERK','2025-11-16 05:42:30'),(10,'ADMIN USER','admin@gmail.com','admin@123','ADMIN','2025-11-15 07:55:00');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehicle_detail`
--

DROP TABLE IF EXISTS `vehicle_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicle_detail` (
  `vehicle_no` varchar(20) NOT NULL,
  `type` varchar(30) DEFAULT NULL,
  `class` varchar(10) DEFAULT NULL,
  `detailment` varchar(100) DEFAULT NULL,
  `dist_travelled` int DEFAULT NULL,
  `quantity` int DEFAULT '1',
  `bullet_proof` enum('Y','N') DEFAULT NULL,
  PRIMARY KEY (`vehicle_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle_detail`
--

LOCK TABLES `vehicle_detail` WRITE;
/*!40000 ALTER TABLE `vehicle_detail` DISABLE KEYS */;
INSERT INTO `vehicle_detail` VALUES ('JK152398','Truck','II','UNIT DUTY',10000,1,'Y'),('MH12YZ2022','Scorpio','V','CSO Duty',5000,1,'N'),('MH14SK2300','Truck','II','Unit duty',10000,1,'Y');
/*!40000 ALTER TABLE `vehicle_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `weight_info`
--

DROP TABLE IF EXISTS `weight_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `weight_info` (
  `troop_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `rank` varchar(50) DEFAULT NULL,
  `army_number` varchar(50) DEFAULT NULL,
  `actual_weight` float DEFAULT NULL,
  `age` int DEFAULT NULL,
  `height` float DEFAULT NULL,
  `company` varchar(100) DEFAULT NULL,
  `status_type` varchar(10) NOT NULL DEFAULT 'safe',
  `category_type` varchar(10) DEFAULT NULL,
  `restrictions` text,
  PRIMARY KEY (`troop_id`),
  UNIQUE KEY `army_number` (`army_number`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weight_info`
--

LOCK TABLES `weight_info` WRITE;
/*!40000 ALTER TABLE `weight_info` DISABLE KEYS */;
INSERT INTO `weight_info` VALUES (1,'john snow','AGNIVEER','12121',56,56,156,'3 Company','category','permanent','cannot run'),(2,'John Doe','Captain','JD12345',75.5,30,175,'2 Company','safe',NULL,NULL),(3,'Yawar','Havaldar','121132229',67,34,170,'3 Company','category','permanent','cannot drive'),(4,'Ubaid lone','JCO','0234032048',56,40,179,'2 Company','category','permanent','CANNOT WAIT PROPERLY'),(5,'G NARESH','JCO','023403204890',67,56,178,'4 Company','safe',NULL,NULL),(6,'GANESH','JCO','34809',67,56,167,'4 Company','category','permanent','THIS CANNOT READ'),(7,'tiku sharma','JCO','12',56,45,165,'2 Company','safe',NULL,NULL),(8,'zaheer','MAJOR','453343',67,56,170,'4 Company','safe',NULL,NULL),(9,'h r','JCO','15732589',173,32,176,'4 Company','safe',NULL,NULL),(10,'MANISH BAJPAI','JCO','48943948',67,45,180,'1 Company','safe',NULL,NULL),(11,'MURALI DHARAN','AGNIVEER','3438094830984',56,34,180,'4 Company','safe',NULL,NULL),(12,'STEVE SMITH','MAJOR','32943284',60,45,180,'1 Company','category','temporary','injury');
/*!40000 ALTER TABLE `weight_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-28 20:44:33

-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: army_personnel_db
-- ------------------------------------------------------
-- Server version	8.0.40

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
INSERT INTO `personnel` VALUES (1,'ABC','778G','JCO','Infantry','2010-05-15','1985-03-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-23 07:27:16','2025-10-28 07:15:45','1 Company'),(2,'Srivastav','156WE','Agniveer','Infantry','2010-05-15','2002-03-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 05:56:59','2025-10-28 07:15:57','1 Company'),(3,'Vivek','1526WE','Agniveer','Infantry','2010-05-15','2001-03-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 05:57:55','2025-10-28 07:16:07','2 Company'),(4,'Gugar','9926WE','Agniveer','Infantry','2010-05-15','1994-03-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 05:58:25','2025-10-28 07:16:37','4 Company'),(5,'Abishek','99226WE','Agniveer','Infantry','2010-05-15','1960-03-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 06:00:05','2025-10-28 08:04:41','3 Company'),(6,'Raju','966WE','Signal Man','Infantry','2010-05-15','1986-09-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 06:03:59','2025-10-28 07:16:55','3 Company'),(7,'Rohit','87CESR','Signal Man','Infantry','2010-05-15','1989-09-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 06:04:31','2025-10-28 07:17:00','3 Company'),(8,'Prateeq','997CESR','Signal Man','Infantry','2010-05-15','1967-09-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 06:05:21','2025-10-28 07:17:06','3 Company'),(10,'Rahul','965CESR','Signal Man','Infantry','2010-05-15','1987-09-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 06:06:06','2025-10-28 07:17:21','2 Company'),(12,'Hardik','905CESR','Signal Man','Infantry','2010-05-15','1997-09-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 06:06:35','2025-10-28 07:17:30','2 Company'),(13,'Kurnal','9085CESR','Signal Man','Infantry','2010-05-15','1989-09-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 06:07:05','2025-10-28 07:17:33','2 Company'),(14,'Gill','25CESR','OC','Infantry','2010-05-15','1987-09-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 06:07:40','2025-10-28 07:17:39','2 Company'),(15,'Raju','165CESR','OC','Infantry','2010-05-15','1987-09-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 06:08:03','2025-10-28 07:17:49','1 Company'),(16,'ABC','775CESR','Subedar','Infantry','2010-05-15','1999-09-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 06:18:15','2025-10-28 07:17:53','1 Company'),(17,'ABC','984CESR','Subedar','Infantry','2010-05-15','1979-09-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 06:18:42','2025-10-28 07:17:57','1 Company'),(18,'Aijaz','994CESR','Subedar','Infantry','2010-05-15','1990-09-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 06:19:13','2025-10-28 07:18:01','1 Company'),(19,'Aijaz','99999CESR','Subedar','Infantry','2010-05-15','1990-09-20','2015-01-10','2020-06-01','O+','Christian','Non-Vegetarian','No','BSc Computer Science','Gallantry Award 2018','Advanced Leadership Course','Yes','IC-45678','2020-01-01','Unit HQ','A','B+','2025-09-01','Yes','ABCDE1234F','P-II/2020/001','123456789012','P-II/2021/002','1234567890','State Bank of India','SBIN0001234','House 5, Lane 2','Greenville','+91-9876543210','Central Tehsil','Greenville PO','Greenville PS','Green Tehsil','NRS-001','NMH-002','Green District','Greenland','Yes',5.50,175.50,75.00,85.00,'Scar on left arm','None','Yes',30,'Sports and Drama','Delhi','Yes','2024-01-01','No','N/A','Yes','2024-06-15','Military Hospital','2026-06-15','Mild Asthma','No heavy lifting','Excellent','Good','Jane Doe','Spouse','2012-07-20','0987654321','HDFC Bank','HDFC0005678','P-II/2012/003','DL01AB1234','Toyota Innova','2020-03-10','Yes','DL-56789','2020-01-01','2030-01-01','No','No','Attended in 2023','2025-10-01','Sgt. Smith','Yes','None','Transfer to hometown','None','Improve mess facilities, gym upgrade, family quarters','Leadership, teamwork, discipline','Public speaking','No','2025-10-27 09:44:27','2025-10-28 07:18:08','4 Company');
/*!40000 ALTER TABLE `personnel` ENABLE KEYS */;
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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-29 10:39:17

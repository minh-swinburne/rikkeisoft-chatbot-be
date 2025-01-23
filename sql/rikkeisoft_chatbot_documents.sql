-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: rikkeisoft_chatbot
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
-- Table structure for table `documents`
--

DROP TABLE IF EXISTS `documents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `documents` (
  `id` char(36) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `file_type` varchar(50) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text,
  `categories` varchar(255) NOT NULL,
  `creator` char(36) NOT NULL,
  `created_date` date DEFAULT NULL,
  `restricted` tinyint(1) NOT NULL,
  `uploader` char(36) NOT NULL,
  `uploaded_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `creator` (`creator`),
  KEY `uploader` (`uploader`),
  CONSTRAINT `documents_ibfk_1` FOREIGN KEY (`creator`) REFERENCES `users` (`id`),
  CONSTRAINT `documents_ibfk_2` FOREIGN KEY (`uploader`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documents`
--

LOCK TABLES `documents` WRITE;
/*!40000 ALTER TABLE `documents` DISABLE KEYS */;
INSERT INTO `documents` VALUES ('075b414e-b346-43ec-8c60-8f3d7e1c4772','COS40005_Unit_Outline_DN_Jan2025.docx.pdf','pdf','COS40005 Unit Outline','A lot of text','Guidance,Training Materials,Technical Documentation','c24d9619-848d-4af6-87c8-718444421762','2025-01-10',0,'c24d9619-848d-4af6-87c8-718444421762','2025-01-13 10:29:45'),('0b7ead0a-bac2-4fb8-ab2f-33df0fd0f55a','image.pdf','pdf','PDF with no text','OCR test','Training Materials,Technical Documentation','c24d9619-848d-4af6-87c8-718444421762','2025-01-10',0,'c24d9619-848d-4af6-87c8-718444421762','2025-01-13 09:30:00'),('0dfa9ea0-9b50-44ca-88af-0b2e0ea09a1c','image.pdf','pdf','Image PDF','No text','Training Materials,Technical Documentation','c24d9619-848d-4af6-87c8-718444421762','2025-01-10',0,'c24d9619-848d-4af6-87c8-718444421762','2025-01-13 14:06:59'),('20fec429-7b9d-47e5-bc68-4adcdddeb72c','COS40005 Worklog - Week 2.pdf','pdf','Worklog week 2','Individual Worklog of COS40005','Reports,Procedures','c24d9619-848d-4af6-87c8-718444421762','2025-01-12',0,'c24d9619-848d-4af6-87c8-718444421762','2025-01-13 09:03:47'),('44a694c1-9aae-4801-ada4-10cdbd4f712b','image.pdf','pdf','PDF with no text','OCR test','Training Materials,Technical Documentation','c24d9619-848d-4af6-87c8-718444421762','2025-01-10',0,'c24d9619-848d-4af6-87c8-718444421762','2025-01-13 09:30:50'),('592c012c-d898-41c6-aa4d-e88d5317ba35','image.pdf','pdf','PDF with no text','OCR test','Training Materials,Technical Documentation','c24d9619-848d-4af6-87c8-718444421762','2025-01-10',0,'c24d9619-848d-4af6-87c8-718444421762','2025-01-13 09:20:39'),('6dd1e038-fd77-4027-85be-21069e280c0e','image.pdf','pdf','PDF with no text','OCR test','Training Materials,Technical Documentation','c24d9619-848d-4af6-87c8-718444421762','2025-01-10',0,'c24d9619-848d-4af6-87c8-718444421762','2025-01-13 09:59:53'),('90bb2b09-cf5d-4fb7-8433-c6f68b44c933','image.pdf','pdf','Image PDF','No text','Training Materials,Technical Documentation','c24d9619-848d-4af6-87c8-718444421762','2025-01-10',0,'c24d9619-848d-4af6-87c8-718444421762','2025-01-13 14:17:57'),('a42fdf38-5d5a-4baa-b691-9137a8b5f1a3','image.pdf','pdf','PDF with no text','OCR test','Training Materials,Technical Documentation','c24d9619-848d-4af6-87c8-718444421762','2025-01-10',0,'c24d9619-848d-4af6-87c8-718444421762','2025-01-13 10:04:20'),('b031578d-b213-49d5-a888-cc38b5cb5417','image.pdf','pdf','PDF with no text','OCR test','Training Materials,Technical Documentation','c24d9619-848d-4af6-87c8-718444421762','2025-01-10',0,'c24d9619-848d-4af6-87c8-718444421762','2025-01-13 09:04:44'),('bceb692c-2c70-47cb-a625-a3dca91f60ce','image.pdf','pdf','Image PDF','No text','Training Materials,Technical Documentation','c24d9619-848d-4af6-87c8-718444421762','2025-01-10',0,'c24d9619-848d-4af6-87c8-718444421762','2025-01-13 14:27:24'),('cf4593be-0ee6-4257-a9a5-79c27aa9ac61','SWE30003_Unit Outline_Jan_2025_V1 (2).pdf','pdf','SWE30003 Unit Outline','SWE30003 - Software Architecture and Design\r\nBA-CS at Swinburne Technology\r\nJanuary Semester, 2025','Guidance,Training Materials','c24d9619-848d-4af6-87c8-718444421762','2024-12-30',0,'c24d9619-848d-4af6-87c8-718444421762','2025-01-13 17:10:10'),('da803e96-1836-4c7c-805b-1bfbd230ab0f','COS40005 Worklog - Week 2.pdf','pdf','COS40005 Worklog - Week 2','','Reports,Procedures','c24d9619-848d-4af6-87c8-718444421762','2025-01-12',0,'c24d9619-848d-4af6-87c8-718444421762','2025-01-13 03:05:39');
/*!40000 ALTER TABLE `documents` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-16 10:42:32

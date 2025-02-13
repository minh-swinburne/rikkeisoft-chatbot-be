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
  `file_name` varchar(255) NOT NULL,
  `file_type` enum('pdf','docx','xlsx','html') NOT NULL,
  `link_url` text,
  `title` varchar(255) NOT NULL,
  `description` text,
  `creator` char(36) DEFAULT NULL,
  `created_date` date DEFAULT NULL,
  `restricted` tinyint DEFAULT '0',
  `uploader` char(36) DEFAULT NULL,
  `uploaded_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `last_modified` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `creator` (`creator`),
  KEY `uploader` (`uploader`),
  CONSTRAINT `documents_ibfk_1` FOREIGN KEY (`creator`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  CONSTRAINT `documents_ibfk_2` FOREIGN KEY (`uploader`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documents`
--

LOCK TABLES `documents` WRITE;
/*!40000 ALTER TABLE `documents` DISABLE KEYS */;
INSERT INTO `documents` VALUES ('50cb94b2-4a01-4978-b550-0c9dd7bb2b40','Configuration and credential file settings in the AWS CLI - AWS Command Line Interface.html','html','https://docs.aws.amazon.com/cli/v1/userguide/cli-configure-files.html','Configuration and credential file settings in the AWS CLI','This documentation is for Version 1 of the AWS CLI only. For documentation related to Version 2 of the AWS CLI, see the Version 2 User Guide.','c24d9619-848d-4af6-87c8-718444421762','2025-02-09',0,'c24d9619-848d-4af6-87c8-718444421762','2025-02-09 08:08:31','2025-02-09 08:08:31'),('835babdf-2b81-413e-aa71-61483b4cb3a5','progression-2023-tables.xlsx','xlsx',NULL,'progression-2023-tables','progression-2023-tables','c24d9619-848d-4af6-87c8-718444421762','2025-02-06',0,'c24d9619-848d-4af6-87c8-718444421762','2025-02-06 09:39:54','2025-02-06 09:39:54'),('88062a21-84f2-4015-9f5c-200fcdda6c33','COS40005 Sprint 1 Project Specification.docx','docx',NULL,'COS40005 Sprint 1 Project Specification','COS40005 Sprint 1','c24d9619-848d-4af6-87c8-718444421762','2025-02-06',1,'c24d9619-848d-4af6-87c8-718444421762','2025-02-06 09:39:10','2025-02-06 09:39:10'),('9465c7e0-8560-4c84-9d78-2b970c75db84','Markdown multiline code blocks in tables when rows have to be specified with one-liners - Stack Overflow.html','html','https://stackoverflow.com/questions/24190085/markdown-multiline-code-blocks-in-tables-when-rows-have-to-be-specified-with-one','Markdown multiline code blocks in tables when rows have to be specified with one-liners','','f7e0386e-8e56-464b-82ef-19747f6a9bae','2025-02-06',0,'c24d9619-848d-4af6-87c8-718444421762','2025-02-06 15:37:45','2025-02-06 15:37:45'),('dd43369c-575c-425a-aaa9-3ada0486cfa3','COS40005 Worklog - Week 2.pdf','pdf',NULL,'COS40005 Worklog - Week 2','','1642be2a-e3a9-4679-87eb-1365f9f470d0','2025-01-22',0,'c24d9619-848d-4af6-87c8-718444421762','2025-02-06 16:13:48','2025-02-12 17:14:38'),('f086ae23-dd83-4611-9ca0-04d75c9a9fb3','HTMLImageElement srcset property - Web APIs  MDN.html','html','https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/srcset#examples','HTMLImageElement: srcset property','','86ce47d5-0bf4-47c4-adb4-2be068e73580','2025-02-06',0,'c24d9619-848d-4af6-87c8-718444421762','2025-02-07 00:28:37','2025-02-07 00:28:37');
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

-- Dump completed on 2025-02-13 10:00:31

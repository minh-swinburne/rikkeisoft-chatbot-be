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
-- Table structure for table `chats`
--

DROP TABLE IF EXISTS `chats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chats` (
  `id` char(36) NOT NULL,
  `user_id` char(36) NOT NULL,
  `name` varchar(255) NOT NULL,
  `last_access` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `chats_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chats`
--

LOCK TABLES `chats` WRITE;
/*!40000 ALTER TABLE `chats` DISABLE KEYS */;
INSERT INTO `chats` VALUES ('01945c9c-50cf-7c99-91b1-4efefc51f08b','86ce47d5-0bf4-47c4-adb4-2be068e73580','Specialized Chat: Conversations Within Conundrums','2025-01-13 05:51:10'),('01945c9d-06cb-7221-85fb-1c210e064d80','86ce47d5-0bf4-47c4-adb4-2be068e73580','\"PulseForge\"','2025-01-13 05:48:32'),('01945c9d-aab6-770d-9fd1-d2e6842c5134','86ce47d5-0bf4-47c4-adb4-2be068e73580','Tool Talk: A Guide to Efficiency in Conversations','2025-01-13 05:51:51'),('01945c9e-4aef-7a44-bd3e-c52d0c4b12f0','86ce47d5-0bf4-47c4-adb4-2be068e73580','After analyzing the chat history, I generated a unique name that is relevant to the','2025-01-13 05:47:38'),('01945c9f-2951-7f07-a96f-8ffa5096e919','86ce47d5-0bf4-47c4-adb4-2be068e73580','New Chat','2025-01-13 05:25:22'),('01945caf-f562-7a5d-a293-e17156e016ab','86ce47d5-0bf4-47c4-adb4-2be068e73580','Markdown file with YAML','2025-01-13 05:51:39'),('01945cb2-21ab-7006-835d-fdca18a39ec6','86ce47d5-0bf4-47c4-adb4-2be068e73580','It seems like you started to type something, but it got cut off. Could','2025-01-13 05:46:16'),('01945cbb-3f6d-7fab-a0b1-336d2c32fa65','1642be2a-e3a9-4679-87eb-1365f9f470d0','Language Liaison Between Human and AI: Resource and Assistance for Solving Life','2025-01-13 05:57:10'),('01945f21-f105-7f4d-b69a-fff71fdbb61d','c24d9619-848d-4af6-87c8-718444421762','Understanding at the Interface of Technology and','2025-01-13 17:20:32'),('01945f53-d543-7ced-bbcb-96cdb1c90c9c','c24d9619-848d-4af6-87c8-718444421762','Minhwave','2025-01-14 13:36:41'),('0194646e-aca0-7239-ae5a-ddafc1fcf835','ddfa1b08-e3c0-4cca-84d7-ac70e60f856d','New Chat','2025-01-15 10:42:51'),('67763113-27cc-800f-a79c-3663c53de570','c24d9619-848d-4af6-87c8-718444421762','Birthday Gift for Father','2019-01-20 00:01:00'),('6776cdc6-cfa0-800f-bf3f-e3dedb47431f','c24d9619-848d-4af6-87c8-718444421762','New Chat','2025-01-13 15:34:02'),('a1e8d106-6589-4e45-97c6-f623d5824a49','c24d9619-848d-4af6-87c8-718444421762','Expert Marketing Strategies','2025-01-13 05:54:46'),('f0033470-99d2-4aa1-af8a-79b9e29e9dbf','c24d9619-848d-4af6-87c8-718444421762','The Crash 27','2025-01-13 14:04:42'),('f0cd3940-44ab-4f48-bcc9-d5f2dd3d833d','c24d9619-848d-4af6-87c8-718444421762','New Chat','2025-01-10 00:01:22');
/*!40000 ALTER TABLE `chats` ENABLE KEYS */;
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

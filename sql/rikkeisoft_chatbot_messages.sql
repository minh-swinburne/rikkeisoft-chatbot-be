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
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `id` char(36) NOT NULL,
  `chat_id` char(36) NOT NULL,
  `time` datetime DEFAULT CURRENT_TIMESTAMP,
  `role` varchar(50) NOT NULL,
  `content` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `chat_id` (`chat_id`),
  CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`chat_id`) REFERENCES `chats` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES ('01945c88-ed48-79cf-81c1-f9384404b28f','67763113-27cc-800f-a79c-3663c53de570','2019-01-20 00:00:00','user','What gifts should I give my father on his birthday?'),('01945c89-0069-7cb1-9ce8-ea415b2d2a30','67763113-27cc-800f-a79c-3663c53de570','2019-01-20 00:00:04','assistant','The ideal gift for your father\'s birthday depends on his interests, hobbies, and preferences. Here are some popular gift ideas:\n\n1. **Personalized items**: Engraved watch, monogrammed wallet, or a photo album with fond memories.\n2. **Tech gadgets**: Smartwatch, wireless headphones, or a high-tech smartphone accessory.\n3. **Experiences**: Tickets to a sporting event or a concert, a weekend getaway, or a fun activity he\'s always wanted to try (e.g., golfing, fishing, or cooking class).\n4. **Luxury grooming**: High-quality shaving kit, luxurious fragrances, or a rejuvenating spa day.\n5. **Hobby-related gifts**: If your father enjoys a particular hobby, consider gifting him something related, such as:\n	* For the outdoorsy type: camping gear, hiking equipment, or a new bike.\n	* For the foodie: cookbook, wine and cheese basket, or a kitchen appliance.\n	* For the sports enthusiast: autographed jersey, sports memorabilia, or a new piece of equipment.\n6. **Practical items**: A high-quality wallet, a leather bag, or a functional tool for his workshop or garage.\n7. **Subscription services**: Sign him up for a streaming platform, a monthly wine club, or a magazine subscription that aligns with his interests.\n\nRemember, the most important aspect of a gift is the thought and love behind it. Choose something that shows you care and pay attention to his interests and preferences.\n\nSources:\n- Various online gift guides and reviews (e.g., The Spruce, Wirecutter, and Esquire).\n- Personal experience and common gift-giving practices.'),('01945c89-1104-7028-a666-e3d6cd96d6cc','6776cdc6-cfa0-800f-bf3f-e3dedb47431f','2025-01-10 00:04:07','user','test'),('01945c8a-1cd6-7b7e-baf0-2af66a51304c','6776cdc6-cfa0-800f-bf3f-e3dedb47431f','2025-01-10 00:04:07','assistant','It seems like you\'re testing the system. Is there something specific you\'d like to know or discuss? I\'m here to help with any questions you might have.');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-13  5:03:52

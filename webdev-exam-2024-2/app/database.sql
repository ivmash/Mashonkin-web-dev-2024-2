-- MySQL dump 10.13  Distrib 8.4.0, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: std_2414_exam
-- ------------------------------------------------------
-- Server version	8.4.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `description` text,
  `year` year DEFAULT NULL,
  `publishing_house` varchar(100) DEFAULT NULL,
  `author` varchar(100) DEFAULT NULL,
  `pages` int DEFAULT NULL,
  `cover` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cover` (`cover`),
  CONSTRAINT `books_ibfk_1` FOREIGN KEY (`cover`) REFERENCES `covers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES (1,'Поколение П','За годы, прошедшие с момента выхода этого романа, в стране изменилось многое: исчезло ощущение безвластия, сменились заказчики и производители рекламы, «криэйторов» стали называть «копирайтерами», компьютерная реальность сделалась важнее телевизионной. Но не изменился культовый статус романа «Generation П»: несмотря на самую тесную связь со своим поколением и своей эпохой, притчевое начало в нем оказалось сильнее сиюминутного. Молодые люди по-прежнему узнают себя в Вавилене Татарском, а спиритические сеансы с команданте Че открывают им истину о природе человека и социума. ',1999,'    Азбука','Пелевин Виктор',320,1),(2,'Оно','В маленьком провинциальном городке Дерри много лет назад семерым подросткам пришлось столкнуться с кромешным ужасом - живым воплощением ада.\nПрошли годы... Подростки повзрослели, и ничто, казалось, не предвещало новой беды. Но кошмар прошлого вернулся, неведомая сила повлекла семерых друзей назад, в новую битву со Злом. Ибо в Дерри опять льется кровь, и бесследно исчезают люди. Ибо вернулось порождение ночного кошмара, настолько невероятное, что даже не имеет имени...',1986,'АСТ','Стивен Кинг',1184,2),(3,'Sapiens. Краткая история человечества','Сто тысяч лет назад Homo sapiens был одним из как минимум шести видов человека, живших на этой планете, - ничем не примечательным животным, которое играло в экосистеме роль не большую, чем гориллы, светлячки или медузы. Но около семидесяти тысяч лет назад загадочное изменение когнитивных способностей Homo sapiens превратило его в хозяина планеты и кошмар экосистемы. Как человек разумный сумел покорить мир? Что стало с другими видами человека? Когда и почему появились деньги, государства и религия? Как возникали и рушились империи? Почему почти все общества ставили женщин ниже мужчин? Как наука и капитализм стали господствующими вероучениями современной эры? Становились ли люди с течением времени счастливее? Какое будущее нас ожидает?',2022,'Синдбад','Харари Юваль',512,3);
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_and_genres`
--

DROP TABLE IF EXISTS `books_and_genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books_and_genres` (
  `id` int NOT NULL AUTO_INCREMENT,
  `book` int DEFAULT NULL,
  `genre` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `book` (`book`),
  KEY `genre` (`genre`),
  CONSTRAINT `books_and_genres_ibfk_1` FOREIGN KEY (`book`) REFERENCES `books` (`id`) ON DELETE CASCADE,
  CONSTRAINT `books_and_genres_ibfk_2` FOREIGN KEY (`genre`) REFERENCES `genres` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_and_genres`
--

LOCK TABLES `books_and_genres` WRITE;
/*!40000 ALTER TABLE `books_and_genres` DISABLE KEYS */;
INSERT INTO `books_and_genres` VALUES (1,1,3),(2,2,3),(3,3,8),(4,3,9);
/*!40000 ALTER TABLE `books_and_genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `covers`
--

DROP TABLE IF EXISTS `covers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `covers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `mime_type` varchar(100) DEFAULT NULL,
  `md5_hash` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `covers`
--

LOCK TABLES `covers` WRITE;
/*!40000 ALTER TABLE `covers` DISABLE KEYS */;
INSERT INTO `covers` VALUES (1,'gen_p.webp','image/webp','5fdc68b2dd0bb3a25b7a8b2cd9293545'),(2,'it.webp','image/webp','c1f0856a1b03e31b7281af58cac2023c'),(3,'sapiens.webp','image/webp','a5746939a39baa538def2534487c3170');
/*!40000 ALTER TABLE `covers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genres`
--

DROP TABLE IF EXISTS `genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genres` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genres`
--

LOCK TABLES `genres` WRITE;
/*!40000 ALTER TABLE `genres` DISABLE KEYS */;
INSERT INTO `genres` VALUES (1,'эпопея'),(2,'эпос'),(3,'роман'),(4,'повесть'),(5,'новелла'),(6,'рассказ'),(7,'пьеса'),(8,'очерк'),(9,'эссе'),(10,'опус'),(11,'ода');
/*!40000 ALTER TABLE `genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `id` int NOT NULL AUTO_INCREMENT,
  `book` int DEFAULT NULL,
  `user` int DEFAULT NULL,
  `grade` int DEFAULT NULL,
  `text` text,
  `date` date DEFAULT NULL,
  `status` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `book` (`book`),
  KEY `user` (`user`),
  KEY `status` (`status`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`book`) REFERENCES `books` (`id`) ON DELETE CASCADE,
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`user`) REFERENCES `users` (`id`),
  CONSTRAINT `reviews_ibfk_3` FOREIGN KEY (`status`) REFERENCES `statuses` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (1,3,1,5,'**очень интересно**','2024-06-23',2),(2,1,1,5,'рекомендую','2024-06-23',2),(3,2,1,4,'хорошая книга но страшно. оценка 4','2024-06-23',2);
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `text` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Administrator','суперпользователь, имеет полный доступ к системе, в том числе к созданию и удалению книг'),(2,'Moderator','может редактировать данные книг и производить модерацию рецензий'),(3,'User','может оставлять рецензии');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `statuses`
--

DROP TABLE IF EXISTS `statuses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `statuses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `statuses`
--

LOCK TABLES `statuses` WRITE;
/*!40000 ALTER TABLE `statuses` DISABLE KEYS */;
INSERT INTO `statuses` VALUES (1,'на рассмотрении'),(2,'одобрена'),(3,'отклонена');
/*!40000 ALTER TABLE `statuses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `login` varchar(100) DEFAULT NULL,
  `password_hash` varchar(200) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `surname` varchar(100) DEFAULT NULL,
  `patronymic` varchar(100) DEFAULT NULL,
  `role` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `role` (`role`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'misha','scrypt:32768:8:1$bxp4uua1Jjz5clrC$42f0591fa80cf334b867ee970c5653f640e79c84c9af6c4c8284b9cabe23f06f7da8b81db5a32c2243eb292a6a627983f147f3f3505331295e1a2f11bc1001a0','Михаил','Сидоров','Юзерович',3),(2,'anatoly','scrypt:32768:8:1$tlcws5Hc6upYSiBC$f7241cbe36e676c4efe899f53c4de21b9f5b11d7cc56c1f7e615a101a7c20f3977267de1ff9d2c03e6a907b967d56269b85f12e251f14b535cc603beb7498af5','Анатолий','Иванов','Модерович',2),(3,'admin','scrypt:32768:8:1$vWzgyymr5E8LUUO1$a9ae616873533ade2e77a0430c6c01a3fb82bdead825d880736df6d54a9432fce6cf7e8f185c92fb8a5a0c1bb0b6c5575c2125a72ab5b18cae7fc48b200b53af','Дмитрий','Петров','Админович',1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-23 18:31:05

-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: e_learning
-- ------------------------------------------------------
-- Server version	8.0.34

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
-- Table structure for table `account`
--

DROP TABLE IF EXISTS account;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account` (
  Account_No int NOT NULL AUTO_INCREMENT,
  Account_Type enum('student','instructor','administrator') NOT NULL,
  User_ID int DEFAULT NULL,
  Admin_ID int DEFAULT NULL,
  Instructor_ID int DEFAULT NULL,
  PRIMARY KEY (Account_No),
  KEY User_ID (User_ID),
  KEY Instructor_ID (Instructor_ID),
  KEY Admin_ID (Admin_ID),
  CONSTRAINT account_ibfk_1 FOREIGN KEY (User_ID) REFERENCES `user` (User_ID),
  CONSTRAINT account_ibfk_2 FOREIGN KEY (Instructor_ID) REFERENCES instructor (Instructor_ID),
  CONSTRAINT account_ibfk_3 FOREIGN KEY (Admin_ID) REFERENCES `admin` (Admin_ID)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES account WRITE;
/*!40000 ALTER TABLE account DISABLE KEYS */;
INSERT INTO account VALUES (4,'student',5,NULL,NULL),(5,'student',6,NULL,NULL),(7,'administrator',NULL,2,NULL),(8,'instructor',NULL,NULL,1),(9,'instructor',NULL,NULL,2),(11,'instructor',NULL,NULL,5),(12,'administrator',NULL,4,NULL),(13,'instructor',NULL,NULL,6),(14,'instructor',NULL,NULL,7);
/*!40000 ALTER TABLE account ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS admin;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  Admin_ID int NOT NULL AUTO_INCREMENT,
  Admin_Name varchar(20) NOT NULL,
  `Password` varchar(20) NOT NULL,
  PRIMARY KEY (Admin_ID)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES admin WRITE;
/*!40000 ALTER TABLE admin DISABLE KEYS */;
INSERT INTO admin VALUES (2,'Pratheek','password123'),(4,'admin','admin123');
/*!40000 ALTER TABLE admin ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `certificate`
--

DROP TABLE IF EXISTS certificate;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE certificate (
  Certificate_ID int NOT NULL AUTO_INCREMENT,
  Certificate_Date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  User_ID int NOT NULL,
  course_ID int DEFAULT NULL,
  PRIMARY KEY (Certificate_ID),
  KEY User_ID (User_ID),
  KEY fk_certificate_course (course_ID),
  CONSTRAINT certificate_ibfk_2 FOREIGN KEY (User_ID) REFERENCES `user` (User_ID),
  CONSTRAINT fk_certificate_course FOREIGN KEY (course_ID) REFERENCES course (Course_ID)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `certificate`
--

LOCK TABLES certificate WRITE;
/*!40000 ALTER TABLE certificate DISABLE KEYS */;
INSERT INTO certificate VALUES (1,'2023-11-22 01:10:40',5,17),(2,'2023-11-22 18:35:49',5,18),(3,'2023-11-22 20:59:14',5,18),(4,'2023-11-23 15:45:52',5,17);
/*!40000 ALTER TABLE certificate ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `content`
--

DROP TABLE IF EXISTS content;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE content (
  Content_ID int NOT NULL AUTO_INCREMENT,
  Content_Details varchar(100) DEFAULT NULL,
  Course_ID int NOT NULL,
  Admin_ID int NOT NULL,
  Approval_Status enum('Approved','Pending') NOT NULL,
  PRIMARY KEY (Content_ID),
  KEY Course_ID (Course_ID),
  KEY Admin_ID (Admin_ID),
  CONSTRAINT content_ibfk_1 FOREIGN KEY (Course_ID) REFERENCES course (Course_ID),
  CONSTRAINT content_ibfk_2 FOREIGN KEY (Admin_ID) REFERENCES `admin` (Admin_ID)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `content`
--

LOCK TABLES content WRITE;
/*!40000 ALTER TABLE content DISABLE KEYS */;
INSERT INTO content VALUES (13,'Design & Analysis of Algorithms',15,2,'Approved'),(14,'Software Engineering',16,2,'Approved'),(15,'Linear Algebra',17,2,'Approved'),(16,'Maths',18,2,'Approved'),(18,'Database Management Systems',20,2,'Approved'),(20,'Database Management Systems',22,2,'Approved');
/*!40000 ALTER TABLE content ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS course;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE course (
  Course_ID int NOT NULL AUTO_INCREMENT,
  course_name varchar(50) NOT NULL,
  Instructor_ID int NOT NULL,
  PRIMARY KEY (Course_ID),
  KEY Instructor_ID (Instructor_ID),
  CONSTRAINT course_ibfk_1 FOREIGN KEY (Instructor_ID) REFERENCES instructor (Instructor_ID)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES course WRITE;
/*!40000 ALTER TABLE course DISABLE KEYS */;
INSERT INTO course VALUES (15,'2023DAA210',2),(16,'2023SE215',2),(17,'2023LA123',1),(18,'2023MA123',1),(20,'2023DBMS210',2),(22,'UE21CS20AA',1);
/*!40000 ALTER TABLE course ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enrollment`
--

DROP TABLE IF EXISTS enrollment;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE enrollment (
  Enrollment_ID int NOT NULL AUTO_INCREMENT,
  User_ID int NOT NULL,
  Course_ID int NOT NULL,
  Course_Status enum('Completed','Ongoing') DEFAULT 'Ongoing',
  PRIMARY KEY (Enrollment_ID),
  KEY User_ID (User_ID),
  KEY Course_ID (Course_ID),
  CONSTRAINT enrollment_ibfk_1 FOREIGN KEY (User_ID) REFERENCES `user` (User_ID),
  CONSTRAINT enrollment_ibfk_2 FOREIGN KEY (Course_ID) REFERENCES course (Course_ID)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enrollment`
--

LOCK TABLES enrollment WRITE;
/*!40000 ALTER TABLE enrollment DISABLE KEYS */;
INSERT INTO enrollment VALUES (1,5,15,'Ongoing'),(2,5,16,'Ongoing'),(3,5,17,'Completed'),(4,5,18,'Completed'),(5,6,15,'Ongoing');
/*!40000 ALTER TABLE enrollment ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evaluation`
--

DROP TABLE IF EXISTS evaluation;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE evaluation (
  Test_ID int NOT NULL,
  Instructor_ID int DEFAULT NULL,
  Test_Grade varchar(1) DEFAULT NULL,
  Test_Response varchar(255) DEFAULT NULL,
  User_ID int NOT NULL,
  PRIMARY KEY (Test_ID),
  KEY Instructor_ID (Instructor_ID),
  CONSTRAINT evaluation_ibfk_1 FOREIGN KEY (Test_ID) REFERENCES test (Test_ID),
  CONSTRAINT evaluation_ibfk_2 FOREIGN KEY (Instructor_ID) REFERENCES instructor (Instructor_ID),
  CONSTRAINT evaluation_ibfk_3 FOREIGN KEY (Test_ID) REFERENCES test (Test_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evaluation`
--

LOCK TABLES evaluation WRITE;
/*!40000 ALTER TABLE evaluation DISABLE KEYS */;
INSERT INTO evaluation VALUES (12,1,'A','wegewgwgwgw',5),(13,1,'S','My answer',5),(14,1,'B','fpiwfpwejfwejfpqe',5),(15,1,'S','my answer',5),(16,1,'S','vwvwwfwgwrgwrgw',5),(17,1,'A','fwlfhfhw;j',5),(18,1,'S','Answer for final',5),(19,1,NULL,'My answer for the test',5);
/*!40000 ALTER TABLE evaluation ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=root@localhost*/ /*!50003 TRIGGER generate_certificate_after_grading AFTER UPDATE ON evaluation FOR EACH ROW BEGIN
    DECLARE is_final_test INT;
    
    IF NEW.Test_Grade = 'S' THEN
        SELECT final_test INTO is_final_test FROM Test WHERE Test_ID = NEW.Test_ID;
        
        IF is_final_test = 1 THEN
            INSERT INTO Certificate (User_ID, Course_ID, Certificate_Date)
            VALUES (NEW.User_ID, (SELECT Course_ID FROM Test WHERE Test_ID = NEW.Test_ID), NOW());

            UPDATE Enrollment 
            SET course_status = 'Completed' 
            WHERE User_ID = NEW.User_ID 
            AND Course_ID = (SELECT Course_ID FROM Test WHERE Test_ID = NEW.Test_ID);
        END IF;
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS feedback;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE feedback (
  Feedback_No int NOT NULL AUTO_INCREMENT,
  Test_ID int DEFAULT NULL,
  Feedback_Text text,
  PRIMARY KEY (Feedback_No),
  KEY Test_ID (Test_ID),
  CONSTRAINT feedback_ibfk_1 FOREIGN KEY (Test_ID) REFERENCES test (Test_ID),
  CONSTRAINT feedback_ibfk_2 FOREIGN KEY (Test_ID) REFERENCES test (Test_ID)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES feedback WRITE;
/*!40000 ALTER TABLE feedback DISABLE KEYS */;
INSERT INTO feedback VALUES (2,12,'Nice'),(3,13,'vvwvwrgwrgwrf'),(4,14,'Good job'),(5,15,'Good '),(6,16,'Nice'),(7,17,'lfhqefle'),(8,18,'Good');
/*!40000 ALTER TABLE feedback ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `instructor`
--

DROP TABLE IF EXISTS instructor;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE instructor (
  Instructor_ID int NOT NULL AUTO_INCREMENT,
  Instructor_Name varchar(20) NOT NULL,
  `Password` varchar(20) NOT NULL,
  PRIMARY KEY (Instructor_ID)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instructor`
--

LOCK TABLES instructor WRITE;
/*!40000 ALTER TABLE instructor DISABLE KEYS */;
INSERT INTO instructor VALUES (1,'John','john123'),(2,'Steve','steve123'),(4,'abc','abc123'),(5,'abc','abc1234'),(6,'Michael','michael123'),(7,'Michael','michael123');
/*!40000 ALTER TABLE instructor ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `support`
--

DROP TABLE IF EXISTS support;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE support (
  Admin_ID int NOT NULL,
  Support_No int NOT NULL AUTO_INCREMENT,
  Request varchar(255) NOT NULL,
  Reply varchar(255) NOT NULL,
  User_ID int NOT NULL,
  PRIMARY KEY (Support_No),
  KEY Admin_ID (Admin_ID),
  KEY User_ID (User_ID),
  CONSTRAINT support_ibfk_1 FOREIGN KEY (Admin_ID) REFERENCES `admin` (Admin_ID),
  CONSTRAINT support_ibfk_2 FOREIGN KEY (User_ID) REFERENCES `user` (User_ID)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `support`
--

LOCK TABLES support WRITE;
/*!40000 ALTER TABLE support DISABLE KEYS */;
INSERT INTO support VALUES (2,9,'Hey I need help in resolving an issue.','-',5);
/*!40000 ALTER TABLE support ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test`
--

DROP TABLE IF EXISTS test;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE test (
  Test_ID int NOT NULL AUTO_INCREMENT,
  User_ID int DEFAULT NULL,
  Course_ID int DEFAULT NULL,
  Test_Details varchar(255) DEFAULT NULL,
  Instructor_ID int DEFAULT NULL,
  Test_Status enum('Completed','Available') DEFAULT 'Available',
  final_test tinyint(1) NOT NULL,
  PRIMARY KEY (Test_ID),
  KEY Course_ID (Course_ID),
  KEY Instructor_ID (Instructor_ID),
  KEY User_ID (User_ID),
  CONSTRAINT test_ibfk_1 FOREIGN KEY (User_ID) REFERENCES `user` (User_ID),
  CONSTRAINT test_ibfk_2 FOREIGN KEY (Course_ID) REFERENCES course (Course_ID),
  CONSTRAINT test_ibfk_3 FOREIGN KEY (Instructor_ID) REFERENCES instructor (Instructor_ID),
  CONSTRAINT test_ibfk_4 FOREIGN KEY (User_ID) REFERENCES `user` (User_ID)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test`
--

LOCK TABLES test WRITE;
/*!40000 ALTER TABLE test DISABLE KEYS */;
INSERT INTO test VALUES (12,5,17,'wvvwwgwfgwgwg',1,'Completed',0),(13,5,17,'Final Examination',1,'Completed',1),(14,5,17,'fowgowofgwhpfwepfwhpfhwefwepfjqepf',1,'Completed',0),(15,5,18,'New Test',1,'Completed',1),(16,5,18,'fefwefwefwefwefwefwefwffrgrhtrh',1,'Completed',1),(17,5,17,'GKGKGK',1,'Completed',0),(18,5,17,'Final Test',1,'Completed',1),(19,5,17,'Test number 3',1,'Completed',0);
/*!40000 ALTER TABLE test ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS user;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  User_ID int NOT NULL AUTO_INCREMENT,
  Username varchar(20) NOT NULL,
  `Password` varchar(20) NOT NULL,
  PRIMARY KEY (User_ID)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES user WRITE;
/*!40000 ALTER TABLE user DISABLE KEYS */;
INSERT INTO user VALUES (5,'A','a'),(6,'Pratheek','pratheek');
/*!40000 ALTER TABLE user ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'e_learning'
--

--
-- Dumping routines for database 'e_learning'
--
/*!50003 DROP FUNCTION IF EXISTS GetCourseCountForInstructor */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=root@localhost FUNCTION GetCourseCountForInstructor(instructorID INT) RETURNS int
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE course_count INT;
    SELECT COUNT(*) INTO course_count FROM Course WHERE Instructor_ID = instructorID;
    RETURN course_count;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS GetStudentCountForCourse */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=root@localhost PROCEDURE GetStudentCountForCourse(IN courseID INT)
BEGIN
    SELECT COUNT(*) AS student_count FROM Enrollment WHERE Course_ID = courseID;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-26 21:08:41

CREATE DATABASE  IF NOT EXISTS `climate` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `climate`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: climate
-- ------------------------------------------------------
-- Server version	8.0.35

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
-- Table structure for table `0degree_cak`
--

DROP TABLE IF EXISTS `0degree_cak`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `0degree_cak` (
  `Datetime` int unsigned NOT NULL,
  `year_cak` varchar(45) NOT NULL DEFAULT ' ',
  `month_cak` varchar(45) NOT NULL DEFAULT ' ',
  `count_cak` varchar(45) NOT NULL DEFAULT ' ',
  `counthigh_cak` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `0degree_cle`
--

DROP TABLE IF EXISTS `0degree_cle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `0degree_cle` (
  `Datetime` int unsigned NOT NULL,
  `year_cle` varchar(45) NOT NULL DEFAULT ' ',
  `month_cle` varchar(45) NOT NULL DEFAULT ' ',
  `count_cle` varchar(45) NOT NULL DEFAULT ' ',
  `counthigh_cle` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `0degree_eri`
--

DROP TABLE IF EXISTS `0degree_eri`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `0degree_eri` (
  `Datetime` int unsigned NOT NULL,
  `year_eri` varchar(45) NOT NULL DEFAULT ' ',
  `month_eri` varchar(45) NOT NULL DEFAULT ' ',
  `count_eri` varchar(45) NOT NULL DEFAULT ' ',
  `counthigh_eri` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `0degree_mfd`
--

DROP TABLE IF EXISTS `0degree_mfd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `0degree_mfd` (
  `Datetime` int unsigned NOT NULL,
  `year_mfd` varchar(45) NOT NULL DEFAULT ' ',
  `month_mfd` varchar(45) NOT NULL DEFAULT ' ',
  `count_mfd` varchar(45) NOT NULL DEFAULT ' ',
  `counthigh_mfd` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `0degree_tol`
--

DROP TABLE IF EXISTS `0degree_tol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `0degree_tol` (
  `Datetime` int unsigned NOT NULL,
  `year_tol` varchar(45) NOT NULL DEFAULT ' ',
  `month_tol` varchar(45) NOT NULL DEFAULT ' ',
  `count_tol` varchar(45) NOT NULL DEFAULT ' ',
  `counthigh_tol` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `0degree_yng`
--

DROP TABLE IF EXISTS `0degree_yng`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `0degree_yng` (
  `Datetime` int unsigned NOT NULL,
  `year_yng` varchar(45) NOT NULL DEFAULT ' ',
  `month_yng` varchar(45) NOT NULL DEFAULT ' ',
  `count_yng` varchar(45) NOT NULL DEFAULT ' ',
  `counthigh_yng` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `100degree_cak`
--

DROP TABLE IF EXISTS `100degree_cak`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `100degree_cak` (
  `Datetime` int unsigned NOT NULL,
  `year_cak` varchar(45) NOT NULL DEFAULT ' ',
  `month_cak` varchar(45) NOT NULL DEFAULT ' ',
  `count_cak` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `100degree_cle`
--

DROP TABLE IF EXISTS `100degree_cle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `100degree_cle` (
  `Datetime` int unsigned NOT NULL,
  `year_cle` varchar(45) NOT NULL DEFAULT ' ',
  `month_cle` varchar(45) NOT NULL DEFAULT ' ',
  `count_cle` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `100degree_eri`
--

DROP TABLE IF EXISTS `100degree_eri`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `100degree_eri` (
  `Datetime` int unsigned NOT NULL,
  `year_eri` varchar(45) NOT NULL DEFAULT ' ',
  `month_eri` varchar(45) NOT NULL DEFAULT ' ',
  `count_eri` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `100degree_mfd`
--

DROP TABLE IF EXISTS `100degree_mfd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `100degree_mfd` (
  `Datetime` int unsigned NOT NULL,
  `year_mfd` varchar(45) NOT NULL DEFAULT ' ',
  `month_mfd` varchar(45) NOT NULL DEFAULT ' ',
  `count_mfd` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `100degree_tol`
--

DROP TABLE IF EXISTS `100degree_tol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `100degree_tol` (
  `Datetime` int unsigned NOT NULL,
  `year_tol` varchar(45) NOT NULL DEFAULT ' ',
  `month_tol` varchar(45) NOT NULL DEFAULT ' ',
  `count_tol` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `100degree_yng`
--

DROP TABLE IF EXISTS `100degree_yng`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `100degree_yng` (
  `Datetime` int unsigned NOT NULL,
  `year_yng` varchar(45) NOT NULL DEFAULT ' ',
  `month_yng` varchar(45) NOT NULL DEFAULT ' ',
  `count_yng` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `32degree_cak`
--

DROP TABLE IF EXISTS `32degree_cak`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `32degree_cak` (
  `Datetime` int unsigned NOT NULL,
  `year_cak` varchar(45) NOT NULL DEFAULT ' ',
  `month_cak` varchar(45) NOT NULL DEFAULT ' ',
  `count_cak` varchar(45) NOT NULL DEFAULT ' ',
  `counthigh_cak` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `32degree_cle`
--

DROP TABLE IF EXISTS `32degree_cle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `32degree_cle` (
  `Datetime` int unsigned NOT NULL,
  `year_cle` varchar(45) NOT NULL DEFAULT ' ',
  `month_cle` varchar(45) NOT NULL DEFAULT ' ',
  `count_cle` varchar(45) NOT NULL DEFAULT ' ',
  `counthigh_cle` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `32degree_eri`
--

DROP TABLE IF EXISTS `32degree_eri`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `32degree_eri` (
  `Datetime` int unsigned NOT NULL,
  `year_eri` varchar(45) NOT NULL DEFAULT ' ',
  `month_eri` varchar(45) NOT NULL DEFAULT ' ',
  `count_eri` varchar(45) NOT NULL DEFAULT ' ',
  `counthigh_eri` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `32degree_mfd`
--

DROP TABLE IF EXISTS `32degree_mfd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `32degree_mfd` (
  `Datetime` int unsigned NOT NULL,
  `year_mfd` varchar(45) NOT NULL DEFAULT ' ',
  `month_mfd` varchar(45) NOT NULL DEFAULT ' ',
  `count_mfd` varchar(45) NOT NULL DEFAULT ' ',
  `counthigh_mfd` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `32degree_tol`
--

DROP TABLE IF EXISTS `32degree_tol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `32degree_tol` (
  `Datetime` int unsigned NOT NULL,
  `year_tol` varchar(45) NOT NULL DEFAULT ' ',
  `month_tol` varchar(45) NOT NULL DEFAULT ' ',
  `count_tol` varchar(45) NOT NULL DEFAULT ' ',
  `counthigh_tol` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `32degree_yng`
--

DROP TABLE IF EXISTS `32degree_yng`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `32degree_yng` (
  `Datetime` int unsigned NOT NULL,
  `year_yng` varchar(45) NOT NULL DEFAULT ' ',
  `month_yng` varchar(45) NOT NULL DEFAULT ' ',
  `count_yng` varchar(45) NOT NULL DEFAULT ' ',
  `counthigh_yng` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `90degree_cak`
--

DROP TABLE IF EXISTS `90degree_cak`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `90degree_cak` (
  `Datetime` int unsigned NOT NULL,
  `year_cak` varchar(45) NOT NULL DEFAULT ' ',
  `month_cak` varchar(45) NOT NULL DEFAULT ' ',
  `count_cak` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `90degree_cle`
--

DROP TABLE IF EXISTS `90degree_cle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `90degree_cle` (
  `Datetime` int unsigned NOT NULL,
  `year_cle` varchar(45) NOT NULL DEFAULT ' ',
  `month_cle` varchar(45) NOT NULL DEFAULT ' ',
  `count_cle` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `90degree_eri`
--

DROP TABLE IF EXISTS `90degree_eri`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `90degree_eri` (
  `Datetime` int unsigned NOT NULL,
  `year_eri` varchar(45) NOT NULL DEFAULT ' ',
  `month_eri` varchar(45) NOT NULL DEFAULT ' ',
  `count_eri` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `90degree_mfd`
--

DROP TABLE IF EXISTS `90degree_mfd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `90degree_mfd` (
  `Datetime` int unsigned NOT NULL,
  `year_mfd` varchar(45) NOT NULL DEFAULT ' ',
  `month_mfd` varchar(45) NOT NULL DEFAULT ' ',
  `count_mfd` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `90degree_tol`
--

DROP TABLE IF EXISTS `90degree_tol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `90degree_tol` (
  `Datetime` int unsigned NOT NULL,
  `year_tol` varchar(45) NOT NULL DEFAULT ' ',
  `month_tol` varchar(45) NOT NULL DEFAULT ' ',
  `count_tol` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `90degree_yng`
--

DROP TABLE IF EXISTS `90degree_yng`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `90degree_yng` (
  `Datetime` int unsigned NOT NULL,
  `year_yng` varchar(45) NOT NULL DEFAULT ' ',
  `month_yng` varchar(45) NOT NULL DEFAULT ' ',
  `count_yng` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `monthly_cak`
--

DROP TABLE IF EXISTS `monthly_cak`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `monthly_cak` (
  `Datetime` int unsigned NOT NULL,
  `year` varchar(45) NOT NULL DEFAULT ' ',
  `month` varchar(45) NOT NULL DEFAULT ' ',
  `monthly_temp_avg` varchar(45) NOT NULL DEFAULT ' ',
  `monthly_precip_total` varchar(45) NOT NULL DEFAULT ' ',
  `monthly_snow_total` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `monthly_cle`
--

DROP TABLE IF EXISTS `monthly_cle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `monthly_cle` (
  `Datetime` int unsigned NOT NULL,
  `year` varchar(45) NOT NULL DEFAULT ' ',
  `month` varchar(45) NOT NULL DEFAULT ' ',
  `monthly_temp_avg` varchar(45) NOT NULL DEFAULT ' ',
  `monthly_precip_total` varchar(45) NOT NULL DEFAULT ' ',
  `monthly_snow_total` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `monthly_eri`
--

DROP TABLE IF EXISTS `monthly_eri`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `monthly_eri` (
  `Datetime` int unsigned NOT NULL,
  `year` varchar(45) NOT NULL DEFAULT ' ',
  `month` varchar(45) NOT NULL DEFAULT ' ',
  `monthly_temp_avg` varchar(45) NOT NULL DEFAULT ' ',
  `monthly_precip_total` varchar(45) NOT NULL DEFAULT ' ',
  `monthly_snow_total` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `monthly_mfd`
--

DROP TABLE IF EXISTS `monthly_mfd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `monthly_mfd` (
  `Datetime` int unsigned NOT NULL,
  `year` varchar(45) NOT NULL DEFAULT ' ',
  `month` varchar(45) NOT NULL DEFAULT ' ',
  `monthly_temp_avg` varchar(45) NOT NULL DEFAULT ' ',
  `monthly_precip_total` varchar(45) NOT NULL DEFAULT ' ',
  `monthly_snow_total` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `monthly_tol`
--

DROP TABLE IF EXISTS `monthly_tol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `monthly_tol` (
  `Datetime` int unsigned NOT NULL,
  `year` varchar(45) NOT NULL DEFAULT ' ',
  `month` varchar(45) NOT NULL DEFAULT ' ',
  `monthly_temp_avg` varchar(45) NOT NULL DEFAULT ' ',
  `monthly_precip_total` varchar(45) NOT NULL DEFAULT ' ',
  `monthly_snow_total` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `monthly_yng`
--

DROP TABLE IF EXISTS `monthly_yng`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `monthly_yng` (
  `Datetime` int unsigned NOT NULL,
  `year` varchar(45) NOT NULL DEFAULT ' ',
  `month` varchar(45) NOT NULL DEFAULT ' ',
  `monthly_temp_avg` varchar(45) NOT NULL DEFAULT ' ',
  `monthly_precip_total` varchar(45) NOT NULL DEFAULT ' ',
  `monthly_snow_total` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seasonally_cak`
--

DROP TABLE IF EXISTS `seasonally_cak`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seasonally_cak` (
  `Datetime` varchar(20) NOT NULL,
  `year` varchar(45) NOT NULL DEFAULT ' ',
  `season` varchar(45) NOT NULL DEFAULT ' ',
  `seasonal_temp_avg` varchar(45) NOT NULL DEFAULT ' ',
  `seasonal_precip_total` varchar(45) NOT NULL DEFAULT ' ',
  `seasonal_snow_total` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seasonally_cle`
--

DROP TABLE IF EXISTS `seasonally_cle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seasonally_cle` (
  `Datetime` varchar(20) NOT NULL,
  `year` varchar(45) NOT NULL DEFAULT ' ',
  `season` varchar(45) NOT NULL DEFAULT ' ',
  `seasonal_temp_avg` varchar(45) NOT NULL DEFAULT ' ',
  `seasonal_precip_total` varchar(45) NOT NULL DEFAULT ' ',
  `seasonal_snow_total` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seasonally_eri`
--

DROP TABLE IF EXISTS `seasonally_eri`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seasonally_eri` (
  `Datetime` varchar(20) NOT NULL,
  `year` varchar(45) NOT NULL DEFAULT ' ',
  `season` varchar(45) NOT NULL DEFAULT ' ',
  `seasonal_temp_avg` varchar(45) NOT NULL DEFAULT ' ',
  `seasonal_precip_total` varchar(45) NOT NULL DEFAULT ' ',
  `seasonal_snow_total` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seasonally_mfd`
--

DROP TABLE IF EXISTS `seasonally_mfd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seasonally_mfd` (
  `Datetime` varchar(20) NOT NULL,
  `year` varchar(45) NOT NULL DEFAULT ' ',
  `season` varchar(45) NOT NULL DEFAULT ' ',
  `seasonal_temp_avg` varchar(45) NOT NULL DEFAULT ' ',
  `seasonal_precip_total` varchar(45) NOT NULL DEFAULT ' ',
  `seasonal_snow_total` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seasonally_tol`
--

DROP TABLE IF EXISTS `seasonally_tol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seasonally_tol` (
  `Datetime` varchar(20) NOT NULL,
  `year` varchar(45) NOT NULL DEFAULT ' ',
  `season` varchar(45) NOT NULL DEFAULT ' ',
  `seasonal_temp_avg` varchar(45) NOT NULL DEFAULT ' ',
  `seasonal_precip_total` varchar(45) NOT NULL DEFAULT ' ',
  `seasonal_snow_total` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seasonally_yng`
--

DROP TABLE IF EXISTS `seasonally_yng`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seasonally_yng` (
  `Datetime` varchar(20) NOT NULL,
  `year` varchar(45) NOT NULL DEFAULT ' ',
  `season` varchar(45) NOT NULL DEFAULT ' ',
  `seasonal_temp_avg` varchar(45) NOT NULL DEFAULT ' ',
  `seasonal_precip_total` varchar(45) NOT NULL DEFAULT ' ',
  `seasonal_snow_total` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `snow_cak`
--

DROP TABLE IF EXISTS `snow_cak`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `snow_cak` (
  `Datetime` int unsigned NOT NULL,
  `year_cak` varchar(45) NOT NULL DEFAULT ' ',
  `month_cak` varchar(45) NOT NULL DEFAULT ' ',
  `sum_cak` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `snow_cle`
--

DROP TABLE IF EXISTS `snow_cle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `snow_cle` (
  `Datetime` int unsigned NOT NULL,
  `year_cle` varchar(45) NOT NULL DEFAULT ' ',
  `month_cle` varchar(45) NOT NULL DEFAULT ' ',
  `sum_cle` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `snow_eri`
--

DROP TABLE IF EXISTS `snow_eri`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `snow_eri` (
  `Datetime` int unsigned NOT NULL,
  `year_eri` varchar(45) NOT NULL DEFAULT ' ',
  `month_eri` varchar(45) NOT NULL DEFAULT ' ',
  `sum_eri` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `snow_mfd`
--

DROP TABLE IF EXISTS `snow_mfd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `snow_mfd` (
  `Datetime` int unsigned NOT NULL,
  `year_mfd` varchar(45) NOT NULL DEFAULT ' ',
  `month_mfd` varchar(45) NOT NULL DEFAULT ' ',
  `sum_mfd` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `snow_tol`
--

DROP TABLE IF EXISTS `snow_tol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `snow_tol` (
  `Datetime` int unsigned NOT NULL,
  `year_tol` varchar(45) NOT NULL DEFAULT ' ',
  `month_tol` varchar(45) NOT NULL DEFAULT ' ',
  `sum_tol` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `snow_yng`
--

DROP TABLE IF EXISTS `snow_yng`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `snow_yng` (
  `Datetime` int unsigned NOT NULL,
  `year_yng` varchar(45) NOT NULL DEFAULT ' ',
  `month_yng` varchar(45) NOT NULL DEFAULT ' ',
  `sum_yng` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `yearly_cak`
--

DROP TABLE IF EXISTS `yearly_cak`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `yearly_cak` (
  `Datetime` int unsigned NOT NULL,
  `year` varchar(45) NOT NULL DEFAULT ' ',
  `yearly_temp_avg` varchar(45) NOT NULL DEFAULT ' ',
  `yearly_precip_total` varchar(45) NOT NULL DEFAULT ' ',
  `yearly_snow_total` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `yearly_cle`
--

DROP TABLE IF EXISTS `yearly_cle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `yearly_cle` (
  `Datetime` int unsigned NOT NULL,
  `year` varchar(45) NOT NULL DEFAULT ' ',
  `yearly_temp_avg` varchar(45) NOT NULL DEFAULT ' ',
  `yearly_precip_total` varchar(45) NOT NULL DEFAULT ' ',
  `yearly_snow_total` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `yearly_eri`
--

DROP TABLE IF EXISTS `yearly_eri`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `yearly_eri` (
  `Datetime` int unsigned NOT NULL,
  `year` varchar(45) NOT NULL DEFAULT ' ',
  `yearly_temp_avg` varchar(45) NOT NULL DEFAULT ' ',
  `yearly_precip_total` varchar(45) NOT NULL DEFAULT ' ',
  `yearly_snow_total` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `yearly_mfd`
--

DROP TABLE IF EXISTS `yearly_mfd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `yearly_mfd` (
  `Datetime` int unsigned NOT NULL,
  `year` varchar(45) NOT NULL DEFAULT ' ',
  `yearly_temp_avg` varchar(45) NOT NULL DEFAULT ' ',
  `yearly_precip_total` varchar(45) NOT NULL DEFAULT ' ',
  `yearly_snow_total` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `yearly_tol`
--

DROP TABLE IF EXISTS `yearly_tol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `yearly_tol` (
  `Datetime` int unsigned NOT NULL,
  `year` varchar(45) NOT NULL DEFAULT ' ',
  `yearly_temp_avg` varchar(45) NOT NULL DEFAULT ' ',
  `yearly_precip_total` varchar(45) NOT NULL DEFAULT ' ',
  `yearly_snow_total` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `yearly_yng`
--

DROP TABLE IF EXISTS `yearly_yng`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `yearly_yng` (
  `Datetime` int unsigned NOT NULL,
  `year` varchar(45) NOT NULL DEFAULT ' ',
  `yearly_temp_avg` varchar(45) NOT NULL DEFAULT ' ',
  `yearly_precip_total` varchar(45) NOT NULL DEFAULT ' ',
  `yearly_snow_total` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-26 21:10:06

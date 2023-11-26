-- MySQL dump 10.13  Distrib 5.6.39, for Win64 (x86_64)
--
-- Host: localhost    Database: climate
-- ------------------------------------------------------
-- Server version	5.6.39

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
-- Table structure for table `0degree_cmh`
--

DROP TABLE IF EXISTS `0degree_cmh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `0degree_cmh` (
  `Datetime` int(10) unsigned NOT NULL,
  `year_cmh` varchar(45) NOT NULL DEFAULT ' ',
  `month_cmh` varchar(45) NOT NULL DEFAULT ' ',
  `count_cmh` varchar(45) NOT NULL DEFAULT ' ',
  `counthigh_cmh` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `0degree_cvg`
--

DROP TABLE IF EXISTS `0degree_cvg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `0degree_cvg` (
  `Datetime` int(10) unsigned NOT NULL,
  `year_cvg` varchar(45) NOT NULL DEFAULT ' ',
  `month_cvg` varchar(45) NOT NULL DEFAULT ' ',
  `count_cvg` varchar(45) NOT NULL DEFAULT ' ',
  `counthigh_cvg` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `0degree_day`
--

DROP TABLE IF EXISTS `0degree_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `0degree_day` (
  `Datetime` int(10) unsigned NOT NULL,
  `year_day` varchar(45) NOT NULL DEFAULT ' ',
  `month_day` varchar(45) NOT NULL DEFAULT ' ',
  `count_day` varchar(45) NOT NULL DEFAULT ' ',
  `counthigh_day` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `100degree_cmh`
--

DROP TABLE IF EXISTS `100degree_cmh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `100degree_cmh` (
  `Datetime` int(10) unsigned NOT NULL,
  `year_cmh` varchar(45) NOT NULL DEFAULT ' ',
  `month_cmh` varchar(45) NOT NULL DEFAULT ' ',
  `count_cmh` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `100degree_cvg`
--

DROP TABLE IF EXISTS `100degree_cvg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `100degree_cvg` (
  `Datetime` int(10) unsigned NOT NULL,
  `year_cvg` varchar(45) NOT NULL DEFAULT ' ',
  `month_cvg` varchar(45) NOT NULL DEFAULT ' ',
  `count_cvg` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `100degree_day`
--

DROP TABLE IF EXISTS `100degree_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `100degree_day` (
  `Datetime` int(10) unsigned NOT NULL,
  `year_day` varchar(45) NOT NULL DEFAULT ' ',
  `month_day` varchar(45) NOT NULL DEFAULT ' ',
  `count_day` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `32degree_cmh`
--

DROP TABLE IF EXISTS `32degree_cmh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `32degree_cmh` (
  `Datetime` int(10) unsigned NOT NULL,
  `year_cmh` varchar(45) NOT NULL DEFAULT ' ',
  `month_cmh` varchar(45) NOT NULL DEFAULT ' ',
  `count_cmh` varchar(45) NOT NULL DEFAULT ' ',
  `counthigh_cmh` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `32degree_cvg`
--

DROP TABLE IF EXISTS `32degree_cvg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `32degree_cvg` (
  `Datetime` int(10) unsigned NOT NULL,
  `year_cvg` varchar(45) NOT NULL DEFAULT ' ',
  `month_cvg` varchar(45) NOT NULL DEFAULT ' ',
  `count_cvg` varchar(45) NOT NULL DEFAULT ' ',
  `counthigh_cvg` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `32degree_day`
--

DROP TABLE IF EXISTS `32degree_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `32degree_day` (
  `Datetime` int(10) unsigned NOT NULL,
  `year_day` varchar(45) NOT NULL DEFAULT ' ',
  `month_day` varchar(45) NOT NULL DEFAULT ' ',
  `count_day` varchar(45) NOT NULL DEFAULT ' ',
  `counthigh_day` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `90degree_cmh`
--

DROP TABLE IF EXISTS `90degree_cmh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `90degree_cmh` (
  `Datetime` int(10) unsigned NOT NULL,
  `year_cmh` varchar(45) NOT NULL DEFAULT ' ',
  `month_cmh` varchar(45) NOT NULL DEFAULT ' ',
  `count_cmh` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `90degree_cvg`
--

DROP TABLE IF EXISTS `90degree_cvg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `90degree_cvg` (
  `Datetime` int(10) unsigned NOT NULL,
  `year_cvg` varchar(45) NOT NULL DEFAULT ' ',
  `month_cvg` varchar(45) NOT NULL DEFAULT ' ',
  `count_cvg` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `90degree_day`
--

DROP TABLE IF EXISTS `90degree_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `90degree_day` (
  `Datetime` int(10) unsigned NOT NULL,
  `year_day` varchar(45) NOT NULL DEFAULT ' ',
  `month_day` varchar(45) NOT NULL DEFAULT ' ',
  `count_day` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kcmh_daily`
--

DROP TABLE IF EXISTS `kcmh_daily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kcmh_daily` (
  `Datetime` int(10) unsigned NOT NULL,
  `Year` varchar(45) NOT NULL,
  `Month` varchar(45) NOT NULL,
  `Day` varchar(45) NOT NULL,
  `MaxT_Xmacis` varchar(45) NOT NULL DEFAULT ' ',
  `MinT_Xmacis` varchar(45) NOT NULL DEFAULT ' ',
  `Pcpn_Xmacis` varchar(45) NOT NULL DEFAULT ' ',
  `Snow_Xmacis` varchar(45) NOT NULL DEFAULT ' ',
  `SnowDepth_Xmacis` varchar(45) NOT NULL DEFAULT ' ',
  `MaxT_ncdc` varchar(45) NOT NULL DEFAULT ' ',
  `MinT_ncdc` varchar(45) NOT NULL DEFAULT ' ',
  `Pcpn_ncdc` varchar(45) NOT NULL DEFAULT ' ',
  `Snow_ncdc` varchar(45) NOT NULL DEFAULT ' ',
  `SnowDepth_ncdc` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kcmh_daily_xmacis`
--

DROP TABLE IF EXISTS `kcmh_daily_xmacis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kcmh_daily_xmacis` (
  `Datetime` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Year` varchar(45) NOT NULL,
  `Month` varchar(45) NOT NULL,
  `Day` varchar(45) NOT NULL,
  `MaxT` varchar(45) NOT NULL,
  `MinT` varchar(45) NOT NULL,
  `AvgT` varchar(45) NOT NULL,
  `Pcpn` varchar(45) NOT NULL,
  `Snow` varchar(45) NOT NULL,
  `SnowDepth` varchar(45) NOT NULL,
  `AvgTJan` varchar(45) NOT NULL,
  `AvgTFeb` varchar(45) NOT NULL,
  `AvgTMar` varchar(45) NOT NULL,
  `AvgTApr` varchar(45) NOT NULL,
  `AvgTMay` varchar(45) NOT NULL,
  `AvgTJun` varchar(45) NOT NULL,
  `AvgTJul` varchar(45) NOT NULL,
  `AvgTAug` varchar(45) NOT NULL,
  `AvgTSep` varchar(45) NOT NULL,
  `AvgTOct` varchar(45) NOT NULL,
  `AvgTNov` varchar(45) NOT NULL,
  `AvgTDec` varchar(45) NOT NULL,
  `AvgTJan1` varchar(45) NOT NULL,
  `TotPcpnJan` varchar(45) NOT NULL,
  `TotPcpnFeb` varchar(45) NOT NULL,
  `TotPcpnMar` varchar(45) NOT NULL,
  `TotPcpnApr` varchar(45) NOT NULL,
  `TotPcpnMay` varchar(45) NOT NULL,
  `TotPcpnJun` varchar(45) NOT NULL,
  `TotPcpnJul` varchar(45) NOT NULL,
  `TotPcpnAug` varchar(45) NOT NULL,
  `TotPcpnSep` varchar(45) NOT NULL,
  `TotPcpnOct` varchar(45) NOT NULL,
  `TotPcpnNov` varchar(45) NOT NULL,
  `TotPcpnDec` varchar(45) NOT NULL,
  `TotPcpnJan1` varchar(45) NOT NULL,
  `TotPcpnJul1` varchar(45) NOT NULL,
  `TotSnowJan` varchar(45) NOT NULL,
  `TotSnowFeb` varchar(45) NOT NULL,
  `TotSnowMar` varchar(45) NOT NULL,
  `TotSnowApr` varchar(45) NOT NULL,
  `TotSnowMay` varchar(45) NOT NULL,
  `TotSnowJun` varchar(45) NOT NULL,
  `TotSnowJul` varchar(45) NOT NULL,
  `TotSnowAug` varchar(45) NOT NULL,
  `TotSnowSep` varchar(45) NOT NULL,
  `TotSnowOct` varchar(45) NOT NULL,
  `TotSnowNov` varchar(45) NOT NULL,
  `TotSnowDec` varchar(45) NOT NULL,
  `TotSnowJan1` varchar(45) NOT NULL,
  `TotSnowJul1` varchar(45) NOT NULL,
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB AUTO_INCREMENT=20190112 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kcmh_monthly`
--

DROP TABLE IF EXISTS `kcmh_monthly`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kcmh_monthly` (
  `Datetime` int(10) unsigned NOT NULL,
  `Year` varchar(45) NOT NULL,
  `Month` varchar(45) NOT NULL,
  `Monthly_Temp_Avg` varchar(45) NOT NULL,
  `Monthly_Precip_Total` varchar(45) NOT NULL,
  `Monthly_Snow_Total` varchar(45) NOT NULL,
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kcmh_records`
--

DROP TABLE IF EXISTS `kcmh_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kcmh_records` (
  `Julian` int(11) NOT NULL,
  `Date` varchar(45) DEFAULT NULL,
  `Max1` int(11) DEFAULT NULL,
  `Max2` int(11) DEFAULT NULL,
  `Max3` int(11) DEFAULT NULL,
  `Max1Year` int(11) DEFAULT NULL,
  `Max2Year` int(11) DEFAULT NULL,
  `Max3Year` int(11) DEFAULT NULL,
  `Min1` int(11) DEFAULT NULL,
  `Min2` int(11) DEFAULT NULL,
  `Min3` int(11) DEFAULT NULL,
  `Min1Year` int(11) DEFAULT NULL,
  `Min2Year` int(11) DEFAULT NULL,
  `Min3Year` int(11) DEFAULT NULL,
  `LowMax1` int(11) DEFAULT NULL,
  `LowMax2` int(11) DEFAULT NULL,
  `LowMax3` int(11) DEFAULT NULL,
  `LowMax1Year` int(11) DEFAULT NULL,
  `LowMax2Year` int(11) DEFAULT NULL,
  `LowMax3Year` int(11) DEFAULT NULL,
  `HighMin1` int(11) DEFAULT NULL,
  `HighMin2` int(11) DEFAULT NULL,
  `HighMin3` int(11) DEFAULT NULL,
  `HighMin1Year` int(11) DEFAULT NULL,
  `HighMin2Year` int(11) DEFAULT NULL,
  `HighMin3Year` int(11) DEFAULT NULL,
  `PcpnMax1` float DEFAULT NULL,
  `PcpnMax2` float DEFAULT NULL,
  `PcpnMax3` float DEFAULT NULL,
  `PcpnMax1Year` int(11) DEFAULT NULL,
  `PcpnMax2Year` int(11) DEFAULT NULL,
  `PcpnMax3Year` int(11) DEFAULT NULL,
  PRIMARY KEY (`Julian`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kcmh_yearly`
--

DROP TABLE IF EXISTS `kcmh_yearly`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kcmh_yearly` (
  `Datetime` int(10) unsigned NOT NULL,
  `Year` varchar(45) NOT NULL,
  `Yearly_Temp_Avg` varchar(45) NOT NULL,
  `Yearly_Precip_Total` varchar(45) NOT NULL,
  `Yearly_Snow_Total` varchar(45) NOT NULL,
  `Yearly_Precip_Total_No_Missing` varchar(45) NOT NULL,
  `Yearly_Snow_Total_With_Missing` varchar(45) NOT NULL,
  PRIMARY KEY (`Datetime`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kcvg_daily`
--

DROP TABLE IF EXISTS `kcvg_daily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kcvg_daily` (
  `Datetime` int(10) unsigned NOT NULL,
  `Year` varchar(45) NOT NULL,
  `Month` varchar(45) NOT NULL,
  `Day` varchar(45) NOT NULL,
  `MaxT_Xmacis` varchar(45) NOT NULL DEFAULT ' ',
  `MinT_Xmacis` varchar(45) NOT NULL DEFAULT ' ',
  `Pcpn_Xmacis` varchar(45) NOT NULL DEFAULT ' ',
  `Snow_Xmacis` varchar(45) NOT NULL DEFAULT ' ',
  `SnowDepth_Xmacis` varchar(45) NOT NULL DEFAULT ' ',
  `MaxT_ncdc` varchar(45) NOT NULL DEFAULT ' ',
  `MinT_ncdc` varchar(45) NOT NULL DEFAULT ' ',
  `Pcpn_ncdc` varchar(45) NOT NULL DEFAULT ' ',
  `Snow_ncdc` varchar(45) NOT NULL DEFAULT ' ',
  `SnowDepth_ncdc` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kcvg_daily_xmacis`
--

DROP TABLE IF EXISTS `kcvg_daily_xmacis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kcvg_daily_xmacis` (
  `Datetime` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Year` varchar(45) NOT NULL,
  `Month` varchar(45) NOT NULL,
  `Day` varchar(45) NOT NULL,
  `MaxT` varchar(45) NOT NULL,
  `MinT` varchar(45) NOT NULL,
  `AvgT` varchar(45) NOT NULL,
  `Pcpn` varchar(45) NOT NULL,
  `Snow` varchar(45) NOT NULL,
  `SnowDepth` varchar(45) NOT NULL,
  `AvgTJan` varchar(45) NOT NULL,
  `AvgTFeb` varchar(45) NOT NULL,
  `AvgTMar` varchar(45) NOT NULL,
  `AvgTApr` varchar(45) NOT NULL,
  `AvgTMay` varchar(45) NOT NULL,
  `AvgTJun` varchar(45) NOT NULL,
  `AvgTJul` varchar(45) NOT NULL,
  `AvgTAug` varchar(45) NOT NULL,
  `AvgTSep` varchar(45) NOT NULL,
  `AvgTOct` varchar(45) NOT NULL,
  `AvgTNov` varchar(45) NOT NULL,
  `AvgTDec` varchar(45) NOT NULL,
  `AvgTJan1` varchar(45) NOT NULL,
  `TotPcpnJan` varchar(45) NOT NULL,
  `TotPcpnFeb` varchar(45) NOT NULL,
  `TotPcpnMar` varchar(45) NOT NULL,
  `TotPcpnApr` varchar(45) NOT NULL,
  `TotPcpnMay` varchar(45) NOT NULL,
  `TotPcpnJun` varchar(45) NOT NULL,
  `TotPcpnJul` varchar(45) NOT NULL,
  `TotPcpnAug` varchar(45) NOT NULL,
  `TotPcpnSep` varchar(45) NOT NULL,
  `TotPcpnOct` varchar(45) NOT NULL,
  `TotPcpnNov` varchar(45) NOT NULL,
  `TotPcpnDec` varchar(45) NOT NULL,
  `TotPcpnJan1` varchar(45) NOT NULL,
  `TotPcpnJul1` varchar(45) NOT NULL,
  `TotSnowJan` varchar(45) NOT NULL,
  `TotSnowFeb` varchar(45) NOT NULL,
  `TotSnowMar` varchar(45) NOT NULL,
  `TotSnowApr` varchar(45) NOT NULL,
  `TotSnowMay` varchar(45) NOT NULL,
  `TotSnowJun` varchar(45) NOT NULL,
  `TotSnowJul` varchar(45) NOT NULL,
  `TotSnowAug` varchar(45) NOT NULL,
  `TotSnowSep` varchar(45) NOT NULL,
  `TotSnowOct` varchar(45) NOT NULL,
  `TotSnowNov` varchar(45) NOT NULL,
  `TotSnowDec` varchar(45) NOT NULL,
  `TotSnowJan1` varchar(45) NOT NULL,
  `TotSnowJul1` varchar(45) NOT NULL,
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB AUTO_INCREMENT=20190112 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kcvg_monthly`
--

DROP TABLE IF EXISTS `kcvg_monthly`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kcvg_monthly` (
  `Datetime` int(10) unsigned NOT NULL,
  `Year` varchar(45) NOT NULL,
  `Month` varchar(45) NOT NULL,
  `Monthly_Temp_Avg` varchar(45) NOT NULL DEFAULT ' ',
  `Monthly_Precip_Total` varchar(45) NOT NULL DEFAULT ' ',
  `Monthly_Snow_Total` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kcvg_records`
--

DROP TABLE IF EXISTS `kcvg_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kcvg_records` (
  `Julian` int(11) NOT NULL,
  `Date` varchar(45) DEFAULT NULL,
  `Max1` int(11) DEFAULT NULL,
  `Max2` int(11) DEFAULT NULL,
  `Max3` int(11) DEFAULT NULL,
  `Max1Year` int(11) DEFAULT NULL,
  `Max2Year` int(11) DEFAULT NULL,
  `Max3Year` int(11) DEFAULT NULL,
  `Min1` int(11) DEFAULT NULL,
  `Min2` int(11) DEFAULT NULL,
  `Min3` int(11) DEFAULT NULL,
  `Min1Year` int(11) DEFAULT NULL,
  `Min2Year` int(11) DEFAULT NULL,
  `Min3Year` int(11) DEFAULT NULL,
  `LowMax1` int(11) DEFAULT NULL,
  `LowMax2` int(11) DEFAULT NULL,
  `LowMax3` int(11) DEFAULT NULL,
  `LowMax1Year` int(11) DEFAULT NULL,
  `LowMax2Year` int(11) DEFAULT NULL,
  `LowMax3Year` int(11) DEFAULT NULL,
  `HighMin1` int(11) DEFAULT NULL,
  `HighMin2` int(11) DEFAULT NULL,
  `HighMin3` int(11) DEFAULT NULL,
  `HighMin1Year` int(11) DEFAULT NULL,
  `HighMin2Year` int(11) DEFAULT NULL,
  `HighMin3Year` int(11) DEFAULT NULL,
  `PcpnMax1` float DEFAULT NULL,
  `PcpnMax2` float DEFAULT NULL,
  `PcpnMax3` float DEFAULT NULL,
  `PcpnMax1Year` int(11) DEFAULT NULL,
  `PcpnMax2Year` int(11) DEFAULT NULL,
  `PcpnMax3Year` int(11) DEFAULT NULL,
  PRIMARY KEY (`Julian`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kcvg_yearly`
--

DROP TABLE IF EXISTS `kcvg_yearly`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kcvg_yearly` (
  `Datetime` int(10) unsigned NOT NULL,
  `Year` varchar(45) NOT NULL,
  `Yearly_Temp_Avg` varchar(45) NOT NULL,
  `Yearly_Precip_Total` varchar(45) NOT NULL,
  `Yearly_Snow_Total` varchar(45) NOT NULL,
  `Yearly_Precip_Total_No_Missing` varchar(45) NOT NULL,
  `Yearly_Snow_Total_With_Missing` varchar(45) NOT NULL,
  PRIMARY KEY (`Datetime`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 PACK_KEYS=1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kday_daily`
--

DROP TABLE IF EXISTS `kday_daily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kday_daily` (
  `Datetime` int(10) unsigned NOT NULL,
  `Year` varchar(45) NOT NULL,
  `Month` varchar(45) NOT NULL,
  `Day` varchar(45) NOT NULL,
  `MaxT_Xmacis` varchar(45) NOT NULL DEFAULT ' ',
  `MinT_Xmacis` varchar(45) NOT NULL DEFAULT ' ',
  `Pcpn_Xmacis` varchar(45) NOT NULL DEFAULT ' ',
  `Snow_Xmacis` varchar(45) NOT NULL DEFAULT ' ',
  `SnowDepth_Xmacis` varchar(45) NOT NULL DEFAULT ' ',
  `MaxT_ncdc` varchar(45) NOT NULL DEFAULT ' ',
  `MinT_ncdc` varchar(45) NOT NULL DEFAULT ' ',
  `Pcpn_ncdc` varchar(45) NOT NULL DEFAULT ' ',
  `Snow_ncdc` varchar(45) NOT NULL DEFAULT ' ',
  `SnowDepth_ncdc` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kday_daily_xmacis`
--

DROP TABLE IF EXISTS `kday_daily_xmacis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kday_daily_xmacis` (
  `Datetime` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Year` varchar(45) NOT NULL,
  `Month` varchar(45) NOT NULL,
  `Day` varchar(45) NOT NULL,
  `MaxT` varchar(45) NOT NULL,
  `MinT` varchar(45) NOT NULL,
  `AvgT` varchar(45) NOT NULL,
  `Pcpn` varchar(45) NOT NULL,
  `Snow` varchar(45) NOT NULL,
  `SnowDepth` varchar(45) NOT NULL,
  `AvgTJan` varchar(45) NOT NULL,
  `AvgTFeb` varchar(45) NOT NULL,
  `AvgTMar` varchar(45) NOT NULL,
  `AvgTApr` varchar(45) NOT NULL,
  `AvgTMay` varchar(45) NOT NULL,
  `AvgTJun` varchar(45) NOT NULL,
  `AvgTJul` varchar(45) NOT NULL,
  `AvgTAug` varchar(45) NOT NULL,
  `AvgTSep` varchar(45) NOT NULL,
  `AvgTOct` varchar(45) NOT NULL,
  `AvgTNov` varchar(45) NOT NULL,
  `AvgTDec` varchar(45) NOT NULL,
  `AvgTJan1` varchar(45) NOT NULL,
  `TotPcpnJan` varchar(45) NOT NULL,
  `TotPcpnFeb` varchar(45) NOT NULL,
  `TotPcpnMar` varchar(45) NOT NULL,
  `TotPcpnApr` varchar(45) NOT NULL,
  `TotPcpnMay` varchar(45) NOT NULL,
  `TotPcpnJun` varchar(45) NOT NULL,
  `TotPcpnJul` varchar(45) NOT NULL,
  `TotPcpnAug` varchar(45) NOT NULL,
  `TotPcpnSep` varchar(45) NOT NULL,
  `TotPcpnOct` varchar(45) NOT NULL,
  `TotPcpnNov` varchar(45) NOT NULL,
  `TotPcpnDec` varchar(45) NOT NULL,
  `TotPcpnJan1` varchar(45) NOT NULL,
  `TotPcpnJul1` varchar(45) NOT NULL,
  `TotSnowJan` varchar(45) NOT NULL,
  `TotSnowFeb` varchar(45) NOT NULL,
  `TotSnowMar` varchar(45) NOT NULL,
  `TotSnowApr` varchar(45) NOT NULL,
  `TotSnowMay` varchar(45) NOT NULL,
  `TotSnowJun` varchar(45) NOT NULL,
  `TotSnowJul` varchar(45) NOT NULL,
  `TotSnowAug` varchar(45) NOT NULL,
  `TotSnowSep` varchar(45) NOT NULL,
  `TotSnowOct` varchar(45) NOT NULL,
  `TotSnowNov` varchar(45) NOT NULL,
  `TotSnowDec` varchar(45) NOT NULL,
  `TotSnowJan1` varchar(45) NOT NULL,
  `TotSnowJul1` varchar(45) NOT NULL,
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB AUTO_INCREMENT=20190112 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kday_monthly`
--

DROP TABLE IF EXISTS `kday_monthly`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kday_monthly` (
  `Datetime` int(10) unsigned NOT NULL,
  `Year` varchar(45) NOT NULL,
  `Month` varchar(45) NOT NULL,
  `Monthly_Temp_Avg` varchar(45) NOT NULL,
  `Monthly_Precip_Total` varchar(45) NOT NULL,
  `Monthly_Snow_Total` varchar(35) NOT NULL,
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kday_records`
--

DROP TABLE IF EXISTS `kday_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kday_records` (
  `Julian` int(11) NOT NULL,
  `Date` varchar(45) DEFAULT NULL,
  `Max1` int(11) DEFAULT NULL,
  `Max2` int(11) DEFAULT NULL,
  `Max3` int(11) DEFAULT NULL,
  `Max1Year` int(11) DEFAULT NULL,
  `Max2Year` int(11) DEFAULT NULL,
  `Max3Year` int(11) DEFAULT NULL,
  `Min1` int(11) DEFAULT NULL,
  `Min2` int(11) DEFAULT NULL,
  `Min3` int(11) DEFAULT NULL,
  `Min1Year` int(11) DEFAULT NULL,
  `Min2Year` int(11) DEFAULT NULL,
  `Min3Year` int(11) DEFAULT NULL,
  `LowMax1` int(11) DEFAULT NULL,
  `LowMax2` int(11) DEFAULT NULL,
  `LowMax3` int(11) DEFAULT NULL,
  `LowMax1Year` int(11) DEFAULT NULL,
  `LowMax2Year` int(11) DEFAULT NULL,
  `LowMax3Year` int(11) DEFAULT NULL,
  `HighMin1` int(11) DEFAULT NULL,
  `HighMin2` int(11) DEFAULT NULL,
  `HighMin3` int(11) DEFAULT NULL,
  `HighMin1Year` int(11) DEFAULT NULL,
  `HighMin2Year` int(11) DEFAULT NULL,
  `HighMin3Year` int(11) DEFAULT NULL,
  `PcpnMax1` float DEFAULT NULL,
  `PcpnMax2` float DEFAULT NULL,
  `PcpnMax3` float DEFAULT NULL,
  `PcpnMax1Year` int(11) DEFAULT NULL,
  `PcpnMax2Year` int(11) DEFAULT NULL,
  `PcpnMax3Year` int(11) DEFAULT NULL,
  PRIMARY KEY (`Julian`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kday_yearly`
--

DROP TABLE IF EXISTS `kday_yearly`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kday_yearly` (
  `Datetime` int(10) unsigned NOT NULL,
  `Year` varchar(45) NOT NULL,
  `Yearly_Temp_Avg` varchar(45) NOT NULL,
  `Yearly_Precip_Total` varchar(45) NOT NULL,
  `Yearly_Snow_Total` varchar(45) NOT NULL,
  `Yearly_Precip_Total_No_Missing` varchar(45) NOT NULL,
  `Yearly_Snow_Total_With_Missing` varchar(45) NOT NULL,
  PRIMARY KEY (`Datetime`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `snow_cmh`
--

DROP TABLE IF EXISTS `snow_cmh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `snow_cmh` (
  `Datetime` int(10) unsigned NOT NULL,
  `year_cmh` varchar(45) NOT NULL DEFAULT ' ',
  `month_cmh` varchar(45) NOT NULL DEFAULT ' ',
  `sum_cmh` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `snow_cvg`
--

DROP TABLE IF EXISTS `snow_cvg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `snow_cvg` (
  `Datetime` int(10) unsigned NOT NULL,
  `year_cvg` varchar(45) NOT NULL DEFAULT ' ',
  `month_cvg` varchar(45) NOT NULL DEFAULT ' ',
  `sum_cvg` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `snow_day`
--

DROP TABLE IF EXISTS `snow_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `snow_day` (
  `Datetime` int(10) unsigned NOT NULL,
  `year_day` varchar(45) NOT NULL DEFAULT ' ',
  `month_day` varchar(45) NOT NULL DEFAULT ' ',
  `sum_day` varchar(45) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`Datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-08-05 11:51:35

-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: lnmdb
-- ------------------------------------------------------
-- Server version	5.1.73

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
-- Table structure for table `certmgr`
--

DROP TABLE IF EXISTS `certmgr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `certmgr` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `commonname` varchar(20) DEFAULT NULL,
  `certtype` varchar(12) DEFAULT NULL,
  `organization` varchar(20) DEFAULT NULL,
  `expiration` varchar(20) DEFAULT NULL,
  `createdate` varchar(20) DEFAULT NULL,
  `safekey` varchar(10) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `commonname` (`commonname`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dnsrecord`
--

DROP TABLE IF EXISTS `dnsrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dnsrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(128) DEFAULT NULL,
  `dnstype` varchar(16) DEFAULT NULL,
  `data` varchar(1024) DEFAULT NULL,
  `pronum` int(2) DEFAULT NULL,
  `action` int(11) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `logrecord`
--

DROP TABLE IF EXISTS `logrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `objtime` datetime DEFAULT NULL,
  `objname` varchar(255) DEFAULT NULL,
  `objact` varchar(255) DEFAULT NULL,
  `objtext` varchar(255) DEFAULT NULL,
  `objhost` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1100 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `netiface`
--

DROP TABLE IF EXISTS `netiface`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `netiface` (
  `id` int(6) NOT NULL AUTO_INCREMENT,
  `ifacename` char(6) NOT NULL DEFAULT '',
  `ifacetype` varchar(10) DEFAULT NULL,
  `status` varchar(4) DEFAULT NULL,
  `ipaddr` char(15) DEFAULT NULL,
  `netmask` char(15) DEFAULT NULL,
  `gateway` char(15) DEFAULT NULL,
  `defaultgw` int(2) DEFAULT NULL,
  `username` char(24) DEFAULT NULL,
  `password` char(16) DEFAULT NULL,
  `mtu` int(5) DEFAULT '1500',
  `rxdata` int(20) DEFAULT NULL,
  `txdata` int(20) DEFAULT NULL,
  `extip` longtext,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=54 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ruleconfnat`
--

DROP TABLE IF EXISTS `ruleconfnat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ruleconfnat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rulename` varchar(255) DEFAULT NULL,
  `srcaddr` longtext,
  `dstmatch` int(11) DEFAULT '1',
  `dstaddr` longtext,
  `runaction` varchar(255) DEFAULT NULL,
  `runobject` varchar(255) DEFAULT NULL,
  `status` int(11) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ruleconfutm`
--

DROP TABLE IF EXISTS `ruleconfutm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ruleconfutm` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rulename` varchar(255) DEFAULT NULL,
  `pronum` int(6) DEFAULT NULL,
  `actzone` varchar(255) DEFAULT NULL,
  `srcaddr` longtext,
  `sproto` varchar(3) DEFAULT NULL,
  `sport` varchar(60) DEFAULT NULL,
  `dstaddr` longtext,
  `dproto` varchar(3) DEFAULT NULL,
  `dport` varchar(60) DEFAULT NULL,
  `runaction` varchar(255) DEFAULT NULL,
  `status` int(11) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sysattr`
--

DROP TABLE IF EXISTS `sysattr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sysattr` (
  `attr` varchar(64) NOT NULL DEFAULT '',
  `value` longtext,
  `status` int(2) DEFAULT '1',
  `servattr` varchar(24) DEFAULT 'sys' COMMENT '指定功能属性,默认系统属性',
  PRIMARY KEY (`attr`),
  UNIQUE KEY `attr` (`attr`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sysinfo`
--

DROP TABLE IF EXISTS `sysinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sysinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `info` text,
  `tim` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=48778 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sysroute`
--

DROP TABLE IF EXISTS `sysroute`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sysroute` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `type` varchar(8) DEFAULT NULL COMMENT '路由类型（主机路由、网络路由）',
  `dest` varchar(15) DEFAULT NULL COMMENT '目标地址',
  `netmask` varchar(15) DEFAULT NULL COMMENT '子网掩码',
  `gateway` varchar(15) DEFAULT NULL COMMENT '下一跳地址',
  `iface` varchar(10) DEFAULT NULL COMMENT '匹配接口',
  `fromtype` int(2) DEFAULT NULL COMMENT '路由来源（系统、用户定义）',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3881 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sysrouteadv`
--

DROP TABLE IF EXISTS `sysrouteadv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sysrouteadv` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rulename` varchar(16) DEFAULT NULL,
  `srcaddr` longtext,
  `destaddr` longtext,
  `pronum` int(11) DEFAULT NULL,
  `iface` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `username` varchar(50) NOT NULL DEFAULT '0',
  `passwd` varchar(50) NOT NULL DEFAULT '0',
  `policy` int(11) DEFAULT '0',
  `access` tinyint(4) DEFAULT '0',
  `adddate` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `status` tinyint(4) NOT NULL DEFAULT '1',
  `comment` varchar(20) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=54 DEFAULT CHARSET=utf8 COMMENT='ç”¨æˆ·è¡¨';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vpnpolicy`
--

DROP TABLE IF EXISTS `vpnpolicy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vpnpolicy` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL DEFAULT '0' COMMENT '部门名',
  `pushdns` longtext,
  `pushroute` longtext,
  `pushnoroute` longtext,
  `txlimit` int(10) DEFAULT NULL,
  `rxlimit` int(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=100040 DEFAULT CHARSET=utf8 COMMENT='部门表';
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-01-08 16:28:01
-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: lnmdb
-- ------------------------------------------------------
-- Server version	5.1.73

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
-- Dumping data for table `user`
--
-- WHERE:  username='admin'

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','zL+ckVsxUYQleCoYHt3BDA==',100033,1,'2018-09-26 01:00:06',1,'admin');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-01-08 16:28:01
-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: lnmdb
-- ------------------------------------------------------
-- Server version	5.1.73

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
-- Dumping data for table `sysattr`
--
-- WHERE:  servattr!='netiface'

LOCK TABLES `sysattr` WRITE;
/*!40000 ALTER TABLE `sysattr` DISABLE KEYS */;
INSERT INTO `sysattr` VALUES ('appversion','1.0.0',1,'sys'),('vpnprofile','<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<AnyConnectProfile xmlns=\"http://schemas.xmlsoap.org/encoding/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://schemas.xmlsoap.org/encoding/ AnyConnectProfile.xsd\">\r\n\r\n        <ClientInitialization>\r\n                <UseStartBeforeLogon UserControllable=\"false\">false</UseStartBeforeLogon>\r\n                <StrictCertificateTrust>false</StrictCertificateTrust>\r\n                <RestrictPreferenceCaching>false</RestrictPreferenceCaching>\r\n                <RestrictTunnelProtocols>IPSec</RestrictTunnelProtocols>\r\n                <BypassDownloader>true</BypassDownloader>\r\n                <WindowsVPNEstablishment>AllowRemoteUsers</WindowsVPNEstablishment>\r\n                <CertEnrollmentPin>pinAllowed</CertEnrollmentPin>\r\n                <CertificateMatch>\r\n                        <KeyUsage>\r\n                                <MatchKey>Digital_Signature</MatchKey>\r\n                        </KeyUsage>\r\n                        <ExtendedKeyUsage>\r\n                                <ExtendedMatchKey>ClientAuth</ExtendedMatchKey>\r\n                        </ExtendedKeyUsage>\r\n                </CertificateMatch>\r\n\r\n                <BackupServerList>\r\n                    <HostAddress>192.168.60.188:8833</HostAddress>\r\n                     <HostAddress>192.168.60.188:8833</HostAddress>\r\n                </BackupServerList>\r\n        </ClientInitialization>\r\n\r\n        <ServerList>\r\n                <HostEntry>\r\n                    <HostName>LnmOS.devel.com</HostName>\r\n                    <HostAddress>192.168.60.188:8833</HostAddress>\r\n                </HostEntry>\r\n        </ServerList>\r\n</AnyConnectProfile>',1,'sys'),('vpnrelay','tun1000',1,'vpnrelay'),('dnsconf','{\"dnsrelay\": \"1\", \"dnsrule\": \"1\", \"dnsport\": 53, \"dnslist\": \"8.8.8.8\\n8.8.4.4\", \"dnsproxy\": \"0\", \"dnsstatus\": 1}',1,'dnsmasq'),('vpnclient','{\"authtype\": \"2\", \"service\": \"off\"}',1,'openconnect'),('resData','{\"ResState\": \"True\", \"visitDay\": \"30\", \"ResInv\": \"60\", \"ResSaveDay\": \"1\"}',1,'sys'),('dhcpconf','{\"otime\": \"48\", \"getdns1\": \"8.8.8.8\", \"getdns2\": \"8.8.4.4\", \"startip\": \"192.168.200.100\", \"dhcplist\": \"F0:79:59:92:C9:92,192.168.0.87\", \"getgw\": \"192.168.200.1\", \"dhcpenable\": \"0\", \"stopip\": \"192.168.200.200\"}',1,'dnsmasq'),('vpnserver','{\"authtype\": \"3\", \"service\": \"off\"}',1,'ocserv');
/*!40000 ALTER TABLE `sysattr` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-01-08 16:28:01

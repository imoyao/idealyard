-- 测试使用，数据无意义
-- MySQL dump 10.13  Distrib 5.7.26, for linux-glibc2.12 (x86_64)
--
-- Host: localhost    Database: iyblog_dev
-- ------------------------------------------------------
-- Server version	5.7.26

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
-- Table structure for table `iy_article`
--

DROP TABLE IF EXISTS `iy_article`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iy_article` (
  `post_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `title` varchar(64) DEFAULT NULL COMMENT '文章标题',
  `identifier` int(11) DEFAULT NULL COMMENT '文章标识码',
  `author_id` int(11) DEFAULT NULL COMMENT '作者id',
  `body_id` int(11) DEFAULT NULL COMMENT '文章结构体id',
  `view_counts` int(11) DEFAULT NULL COMMENT '文章阅读数',
  `weight` int(11) DEFAULT NULL COMMENT '置顶功能',
  `category_id` int(11) DEFAULT NULL COMMENT '分类',
  `create_date` datetime DEFAULT NULL COMMENT '文章创建时间',
  `update_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '文章更新时间',
  PRIMARY KEY (`post_id`),
  UNIQUE KEY `identifier` (`identifier`),
  UNIQUE KEY `body_id` (`body_id`),
  KEY `author_id` (`author_id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `iy_article_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `iy_user` (`id`),
  CONSTRAINT `iy_article_ibfk_2` FOREIGN KEY (`body_id`) REFERENCES `iy_article_body` (`id`),
  CONSTRAINT `iy_article_ibfk_3` FOREIGN KEY (`category_id`) REFERENCES `iy_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iy_article`
--

LOCK TABLES `iy_article` WRITE;
/*!40000 ALTER TABLE `iy_article` DISABLE KEYS */;
INSERT INTO `iy_article` VALUES (1,'醉里挑灯看剑',19930126,1,1,200,1,1,'2018-02-01 14:47:19','2018-02-04 16:00:00'),(2,'明月几时有',19930127,1,2,99,1,1,'2018-05-01 14:47:19','2018-02-04 16:00:00'),(3,'床前明月光',19930128,1,3,32,1,1,'2018-07-13 14:47:19','2018-02-04 16:00:00'),(4,'下周回国',19930129,1,4,54,1,1,'2018-12-01 14:47:19','2018-02-04 16:00:00'),(5,'你说你妈呢',19930130,1,5,23,1,1,'2019-02-01 14:47:19','2018-02-04 16:00:00'),(6,'锦瑟无端2十弦',19930132,1,6,67,1,1,'2018-02-11 14:47:19','2018-02-04 16:00:00'),(7,'锦瑟无端30弦',199301546,1,7,88,1,1,'2018-06-01 14:47:19','2018-02-04 16:00:00'),(8,'锦瑟无端40弦',19930134,1,8,5,1,1,'2018-03-01 14:47:19','2018-02-04 16:00:00'),(9,'锦瑟无端23弦',19930156,1,9,765,1,1,'2018-03-01 14:47:19','2018-02-04 16:00:00'),(11,'锦瑟无端123弦',1993012126,1,11,668,1,1,'2018-03-01 14:47:19','2018-02-04 16:00:00'),(12,'锦瑟无端五弦',199303126,1,12,3,1,1,'2018-08-01 14:47:19','2018-02-04 16:00:00'),(13,'锦瑟无端十弦',199301246,1,13,567,1,1,'2018-02-23 14:47:19','2018-02-04 16:00:00'),(14,'锦瑟无端4弦',199301526,1,14,4,1,1,'2018-11-01 14:47:19','2018-02-04 16:00:00'),(15,'锦瑟无端18弦',199301626,1,15,6,1,1,'2017-02-01 14:47:19','2018-02-04 16:00:00'),(16,'锦瑟无端6弦',199301726,1,16,67,1,1,'2018-02-02 14:47:19','2018-02-04 16:00:00'),(17,'锦瑟无端34弦',199301286,1,17,34,1,1,'2011-12-04 14:47:19','2018-02-04 16:00:00'),(18,'锦瑟无端28弦',199301926,1,18,23,1,1,'2018-06-01 14:47:19','2018-02-04 16:00:00');
/*!40000 ALTER TABLE `iy_article` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `iy_article_body`
--

DROP TABLE IF EXISTS `iy_article_body`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iy_article_body` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `content_html` text COMMENT '文章的html',
  `content` text COMMENT '文章内容',
  `summary` varchar(1000) DEFAULT '你如今的气质里，藏着你走过的路、读过的书和爱过的人。' COMMENT '文章摘要',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iy_article_body`
--

LOCK TABLES `iy_article_body` WRITE;
/*!40000 ALTER TABLE `iy_article_body` DISABLE KEYS */;
INSERT INTO `iy_article_body` VALUES (1,'<h2>快速上手</h2>\n<p>本节将介绍如何在项目中使用 Element。</p>\n<h3>使用 Starter Kit</h3>\n<p>我们提供了通用的项目模板，你可以直接使用。对于 Laravel 用户，我们也准备了相应的模板，同样可以直接下载使用。</p>\n<p>如果不希望使用我们提供的模板，请继续阅读。</p>\n<h3>使用 vue-cli</h3>\n<p>我们还可以使用 vue-cli 初始化项目，命令如下：</p>\n<pre><code class=\"lang-language\">&gt; npm i -g vue-cli\n&gt; mkdir my-project &amp;&amp; cd my-project\n&gt; vue init webpack\n&gt; npm i &amp;&amp; npm i element-ui\n</code></pre>\n<h3>引入 Element</h3>\n<p>你可以引入整个 Element，或是根据需要仅引入部分组件。我们先介绍如何引入完整的 Element。</p>\n<h4>完整引入</h4>\n<p>在 main.js 中写入以下内容：</p>\n<pre><div class=\"hljs\"><code class=\"lang-javascript\"><span class=\"hljs-keyword\">import</span> Vue <span class=\"hljs-keyword\">from</span> <span class=\"hljs-string\">\'vue\'</span>\n<span class=\"hljs-keyword\">import</span> ElementUI <span class=\"hljs-keyword\">from</span> <span class=\"hljs-string\">\'element-ui\'</span>\n<span class=\"hljs-keyword\">import</span> <span class=\"hljs-string\">\'element-ui/lib/theme-chalk/index.css\'</span>\n<span class=\"hljs-keyword\">import</span> App <span class=\"hljs-keyword\">from</span> <span class=\"hljs-string\">\'./App.vue\'</span>\n\nVue.use(ElementUI)\n\n<span class=\"hljs-keyword\">new</span> Vue({\n  <span class=\"hljs-attr\">el</span>: <span class=\"hljs-string\">\'#app\'</span>,\n  <span class=\"hljs-attr\">render</span>: <span class=\"hljs-function\"><span class=\"hljs-params\">h</span> =&gt;</span> h(App)\n})\n\n</code></div></pre>\n<p>以上代码便完成了 Element 的引入。需要注意的是，样式文件需要单独引入。</p>\n<h4>按需引入</h4>\n<p>借助 babel-plugin-component，我们可以只引入需要的组件，以达到减小项目体积的目的。</p>\n<p>首先，安装 babel-plugin-component：</p>\n','## 快速上手\n\n本节将介绍如何在项目中使用 Element。\n\n### 使用 Starter Kit\n我们提供了通用的项目模板，你可以直接使用。对于 Laravel 用户，我们也准备了相应的模板，同样可以直接下载使用。\n\n如果不希望使用我们提供的模板，请继续阅读。\n\n### 使用 vue-cli\n\n我们还可以使用 vue-cli 初始化项目，命令如下：\n\n```language\n> npm i -g vue-cli\n> mkdir my-project && cd my-project\n> vue init webpack\n> npm i && npm i element-ui\n```\n\n### 引入 Element\n你可以引入整个 Element，或是根据需要仅引入部分组件。我们先介绍如何引入完整的 Element。\n\n#### 完整引入\n在 main.js 中写入以下内容：\n```javascript\nimport Vue from \'vue\'\nimport ElementUI from \'element-ui\'\nimport \'element-ui/lib/theme-chalk/index.css\'\nimport App from \'./App.vue\'\n\nVue.use(ElementUI)\n\nnew Vue({\n  el: \'#app\',\n  render: h => h(App)\n})\n\n```\n以上代码便完成了 Element 的引入。需要注意的是，样式文件需要单独引入。\n\n#### 按需引入\n借助 babel-plugin-component，我们可以只引入需要的组件，以达到减小项目体积的目的。\n\n首先，安装 babel-plugin-component：\n\n',''),(2,'html1111111','test',''),(3,'html1111111','test',''),(4,'html1111111','test',''),(5,'html1111111','test',''),(6,'html1111111','test',''),(7,'html1111111','test',''),(8,'html1111111','test',''),(9,'html1111111','test',''),(10,'html1111111','test',''),(11,'html1111111','test',''),(12,'html1111111','test',''),(13,'html1111111','test',''),(14,'html1111111','test',''),(15,'html1111111','test',''),(16,'html1111111','test',''),(17,'html1111111','test',''),(18,'html1111111','test',''),(19,'html1111111','test',''),(20,'html1111111','test','');
/*!40000 ALTER TABLE `iy_article_body` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `iy_category`
--

DROP TABLE IF EXISTS `iy_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iy_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `category_name` varchar(32) DEFAULT NULL COMMENT '分类名称',
  `description` varchar(255) DEFAULT NULL COMMENT '分类描述',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iy_category`
--

LOCK TABLES `iy_category` WRITE;
/*!40000 ALTER TABLE `iy_category` DISABLE KEYS */;
INSERT INTO `iy_category` VALUES (1,'前端',NULL),(2,'后端',NULL),(3,'生活',NULL),(4,'数据库',NULL),(5,'编程语言',NULL);
/*!40000 ALTER TABLE `iy_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `iy_friend`
--

DROP TABLE IF EXISTS `iy_friend`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iy_friend` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `friend_name` varchar(64) DEFAULT NULL COMMENT '好友名称',
  `description` varchar(255) DEFAULT NULL COMMENT '好友描述',
  `friend_link` varchar(64) DEFAULT NULL COMMENT '友链',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iy_friend`
--

LOCK TABLES `iy_friend` WRITE;
/*!40000 ALTER TABLE `iy_friend` DISABLE KEYS */;
/*!40000 ALTER TABLE `iy_friend` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `iy_post_tags`
--

DROP TABLE IF EXISTS `iy_post_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iy_post_tags` (
  `post_id` int(11) DEFAULT NULL,
  `tag_id` int(11) DEFAULT NULL,
  KEY `post_id` (`post_id`),
  KEY `tag_id` (`tag_id`),
  CONSTRAINT `iy_post_tags_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `iy_article` (`post_id`),
  CONSTRAINT `iy_post_tags_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `iy_tag` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iy_post_tags`
--

LOCK TABLES `iy_post_tags` WRITE;
/*!40000 ALTER TABLE `iy_post_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `iy_post_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `iy_syslog`
--

DROP TABLE IF EXISTS `iy_syslog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iy_syslog` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `op_ip` varchar(64) DEFAULT NULL COMMENT '操作者ip',
  `operator` varchar(64) DEFAULT NULL COMMENT '操作者',
  `op_module` varchar(255) DEFAULT NULL COMMENT '操作模块',
  `operation` varchar(64) DEFAULT NULL COMMENT '操作事件',
  `op_time` datetime DEFAULT NULL COMMENT '操作时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iy_syslog`
--

LOCK TABLES `iy_syslog` WRITE;
/*!40000 ALTER TABLE `iy_syslog` DISABLE KEYS */;
/*!40000 ALTER TABLE `iy_syslog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `iy_tag`
--

DROP TABLE IF EXISTS `iy_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iy_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `tag_name` varchar(24) DEFAULT NULL COMMENT '标签名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iy_tag`
--

LOCK TABLES `iy_tag` WRITE;
/*!40000 ALTER TABLE `iy_tag` DISABLE KEYS */;
INSERT INTO `iy_tag` VALUES (1,'原创'),(2,'Python'),(3,'影评'),(4,'阅读'),(5,'MySQL'),(6,'推荐');
/*!40000 ALTER TABLE `iy_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `iy_user`
--

DROP TABLE IF EXISTS `iy_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iy_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `username` varchar(64) DEFAULT NULL COMMENT '用户名',
  `name` varchar(32) DEFAULT NULL COMMENT '真实姓名',
  `password` varchar(128) DEFAULT NULL COMMENT '密码，加密保存',
  `email` varchar(120) DEFAULT NULL COMMENT '注册邮箱',
  `location` varchar(64) DEFAULT NULL COMMENT '居住地',
  `slogan` varchar(64) DEFAULT '唯有文字能担当此任，宣告生命曾经在场。' COMMENT 'Slogan',
  `create_date` datetime DEFAULT NULL COMMENT '用户创建时间',
  `last_login` datetime DEFAULT NULL COMMENT '最近登录时间',
  `confirmed` tinyint(1) DEFAULT NULL COMMENT '注册确认',
  `avatar_hash` varchar(32) DEFAULT NULL COMMENT '头像',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_iy_user_username` (`username`),
  UNIQUE KEY `ix_iy_user_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iy_user`
--

LOCK TABLES `iy_user` WRITE;
/*!40000 ALTER TABLE `iy_user` DISABLE KEYS */;
INSERT INTO `iy_user` VALUES (1,'imoyao','张牧志','$6$rounds=656000$tIs6tFIsFTmqLpUi$rD2UcO0T7VXsVGeUee11oY6HcxbqluGzAXdUWHCDCpTK8fvsMC5rW8R1ZVhyY912MUK19xcnSqrYp88eKsuBH1','emailme8@163.com','中国·北京','凡人皆需侍奉！','2018-01-22 17:14:49','2019-06-24 17:14:49',1,NULL);
/*!40000 ALTER TABLE `iy_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-06-28 22:40:35

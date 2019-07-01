# 设计表结构

https://zhangjia.io/852.html

## 引擎选择

目前广泛使用的是MyISAM和InnoDB两种引擎,InnoDB在MySQL 5.5后成为默认索引。

总体来讲，MyISAM适合`SELECT`密集型的表，而`InnoDB`适合INSERT和UPDATE密集型的表

## 用户表（user）
engine:MyISAM

| 字段名      | 字段类型        | 备注                      | default        |
| ---------- | ------------- | -------------------------- | ------------- |
| u_id         | int           | AUTO_INCREMENT,PRIMARY KEY | not NULL            |
| username   | varchar（20） |     unique                 | not NULL             |
| email      | varchar(30)   |                            | not NULL             |
| password   | char(128)     | hash                       | not NULL             |
| create_time | TIMESTAMP     |                            | now() |

- [x] 用户头像是否必要？

不需要头像


- [IP地址在数据库里面的存储方式](https://www.cnblogs.com/gomysql/p/4595621.html)
- [论IP地址在数据库中应该用何种形式存储](https://www.cnblogs.com/skynet/archive/2011/01/09/1931044.html)

### 查询示例

```sql
SELECT name FROM user WHERE ipaddress = inet_aton('127.0.0.1');
```
    
```python
import socket, struct
def ip2long(ip):  
    return struct.unpack("!L",socket.inet_aton(ip))[0]  
def long2ip(longip):  
    return socket.inet_ntoa(struct.pack('!L', longip))  
if __name__ == '__main__':  
    print('local ip address to long is %s'% ip2long('8.8.8.8'))  
    print('local ip address long to ip is %s'%long2ip(3756947712))  
    print('local ip address long to ip is %s'%long2ip(3756947967))  
   
```

[Which MySQL datatype use for store an IP address?](https://itsolutionstuff.com/post/which-mysql-datatype-use-for-store-an-ip-address)

Insert Data :
```sql
INSERT INTO `ip_addresses` (`ip_address`) VALUES (INET_ATON("127.0.0.1"));
```
Select Data :
```sql
SELECT id, INET_NTOA(`ip_address`) as ip FROM `ip_addresses`;
```
参见[Most efficient way to store IP Address in MySQL](https://stackoverflow.com/questions/2542011/most-efficient-way-to-store-ip-address-in-mysql)

如果存储的是 IPv6 和 IPv4 类型使用 `INET6_ATON()`方法(`MySQL5.6+`可用)；

[MySQL doc-function_inet6-aton](https://dev.mysql.com/doc/refman/5.6/en/miscellaneous-functions.html#function_inet6-aton)

```sql
SELECT INET_ATON('127.0.0.1');

+------------------------+
| INET_ATON('127.0.0.1') |
+------------------------+
|             2130706433 | 
+------------------------+
1 row in set (0.00 sec)


SELECT INET_NTOA('2130706433');

+-------------------------+
| INET_NTOA('2130706433') |
+-------------------------+
| 127.0.0.1               | 
+-------------------------+
1 row in set (0.02 sec)

```

**注意**：
1. `MySQL 5.7+` 以上版本原生支持`json`数据存储。
2. `info_data`需要在下方具体的*json数据*章节中设计及组装。

[MySQL JSON数据类型操作](https://segmentfault.com/a/1190000011580030)


## 操作日志表(opLog)

engine:InnoDB

| 字段名 | 字段类型  | 备注                     | default  |
| --------- | ------------- | -------------------------- | -------- |
| ol_id     | int           | AUTO_INCREMENT,PRIMARY KEY  | not NULL |
| user_id   | int           | foreign key(user_id) references user(u_id) |          |
| op_type   | tinyint(1)    | 增删改查                    |          |
| op_module | int           | 操作模块foreign key(user_id) references moduleInfo(m_id)                    |          |
| op_time   | TIMESTAMP     |                            |          |
| op_ip     | int(UNSIGNED) |                            |          |
| op_result | int           | 0--ok/1                    |          |

- [x] 是否不需要中英文分开记录两个表，只需要一个 字典 或 专门的表 记录操作的模块
用专门的表保存模块

## 模块信息表（moduleInfo）

| 字段名称 | 字段类型  | 备注                     | 默认值 |
| -------- | ------------- | -------------------------- | ------ |
| m_id     | int           | AUTO_INCREMENT,PRIMARY KEY |        |
| m_name   | varchar（20） | unique                     |        |


## 数据表

暂时手动，后期直接 source < xxx.sql

```sql
CREATE DATABASE iyblog_dev CHARSET=UTF8;

USE iyblog_dev
show tables;

# 用户初始化
INSERT INTO `iy_user` VALUES ('1', 'imoyao', '张牧志', '$6$rounds=656000$tIs6tFIsFTmqLpUi$rD2UcO0T7VXsVGeUee11oY6HcxbqluGzAXdUWHCDCpTK8fvsMC5rW8R1ZVhyY912MUK19xcnSqrYp88eKsuBH1', 'emailme8@163.com','中国·北京','凡人皆需侍奉！', '2018-01-22 17:14:49','2019-06-24 17:14:49', '1', null);
# 分类初始化

INSERT INTO `iy_category` VALUES ('1',  '前端', null);
INSERT INTO `iy_category` VALUES ('2',  '后端', null);
INSERT INTO `iy_category` VALUES ('3',  '生活', null);
INSERT INTO `iy_category` VALUES ('4',  '数据库', null);
INSERT INTO `iy_category` VALUES ('5',  '编程语言', null);

# 文章初始化
INSERT INTO `iy_article` VALUES ('1', '醉里挑灯看剑', '19930126','1', '1', '200', '1', '1','2018-02-01 14:47:19','2018-02-05');
INSERT INTO `iy_article` VALUES ('2', '明月几时有', '19930127','1', '2', '99', '1', '1','2018-05-01 14:47:19','2018-02-05');
INSERT INTO `iy_article` VALUES ('3', '床前明月光', '19930128','1', '3', '32', '1', '1','2018-07-13 14:47:19','2018-02-05');
INSERT INTO `iy_article` VALUES ('4', '下周回国', '19930129','1', '4', '54', '1', '1','2018-12-01 14:47:19','2018-02-05');
INSERT INTO `iy_article` VALUES ('5', '你说你妈呢', '19930130','1', '5', '23', '1', '1','2019-02-01 14:47:19','2018-02-05');
INSERT INTO `iy_article` VALUES ('6', '锦瑟无端2十弦', '19930132','1', '6', '67', '1', '1','2018-02-11 14:47:19','2018-02-05');
INSERT INTO `iy_article` VALUES ('7', '锦瑟无端30弦', '199301546','1', '7', '88', '1', '1','2018-06-01 14:47:19','2018-02-05');
INSERT INTO `iy_article` VALUES ('8', '锦瑟无端40弦', '19930134','1', '8', '5', '1', '1','2018-03-01 14:47:19','2018-02-05');
INSERT INTO `iy_article` VALUES ('9', '锦瑟无端23弦', '19930156','1', '9', '765', '1', '1','2018-03-01 14:47:19','2018-02-05');
INSERT INTO `iy_article` VALUES ('10', '锦瑟无端16弦', '19930126','1', '10', '2', '1', '1','2018-04-01 14:47:19','2018-02-05');
INSERT INTO `iy_article` VALUES ('11', '锦瑟无端123弦','1993012126', '1','11',  '668', '1', '1','2018-03-01 14:47:19','2018-02-05');
INSERT INTO `iy_article` VALUES ('12', '锦瑟无端五弦', '199303126','1','12',  '3', '1', '1','2018-08-01 14:47:19','2018-02-05');
INSERT INTO `iy_article` VALUES ('13', '锦瑟无端十弦','199301246', '1','13', '567', '1', '1','2018-02-23 14:47:19','2018-02-05');
INSERT INTO `iy_article` VALUES ('14', '锦瑟无端4弦', '199301526','1','14',  '4', '1', '1','2018-11-01 14:47:19','2018-02-05');
INSERT INTO `iy_article` VALUES ('15', '锦瑟无端18弦','199301626', '1','15',  '6', '1', '1','2017-02-01 14:47:19','2018-02-05');
INSERT INTO `iy_article` VALUES ('16', '锦瑟无端6弦', '199301726','1','16',  '67', '1', '1','2018-02-02 14:47:19','2018-02-05');
INSERT INTO `iy_article` VALUES ('17', '锦瑟无端34弦','199301286','1', '17',  '34', '1', '1','2011-12-04 14:47:19','2018-02-05');
INSERT INTO `iy_article` VALUES ('18', '锦瑟无端28弦','199301926', '1','18',  '23', '1', '1','2018-06-01 14:47:19','2018-02-05');
# 文章内容表
INSERT INTO `iy_article_body` VALUES ('1', '<h2>快速上手</h2>\n<p>本节将介绍如何在项目中使用 Element。</p>\n<h3>使用 Starter Kit</h3>\n<p>我们提供了通用的项目模板，你可以直接使用。对于 Laravel 用户，我们也准备了相应的模板，同样可以直接下载使用。</p>\n<p>如果不希望使用我们提供的模板，请继续阅读。</p>\n<h3>使用 vue-cli</h3>\n<p>我们还可以使用 vue-cli 初始化项目，命令如下：</p>\n<pre><code class=\"lang-language\">&gt; npm i -g vue-cli\n&gt; mkdir my-project &amp;&amp; cd my-project\n&gt; vue init webpack\n&gt; npm i &amp;&amp; npm i element-ui\n</code></pre>\n<h3>引入 Element</h3>\n<p>你可以引入整个 Element，或是根据需要仅引入部分组件。我们先介绍如何引入完整的 Element。</p>\n<h4>完整引入</h4>\n<p>在 main.js 中写入以下内容：</p>\n<pre><div class=\"hljs\"><code class=\"lang-javascript\"><span class=\"hljs-keyword\">import</span> Vue <span class=\"hljs-keyword\">from</span> <span class=\"hljs-string\">''vue''</span>\n<span class=\"hljs-keyword\">import</span> ElementUI <span class=\"hljs-keyword\">from</span> <span class=\"hljs-string\">''element-ui''</span>\n<span class=\"hljs-keyword\">import</span> <span class=\"hljs-string\">''element-ui/lib/theme-chalk/index.css''</span>\n<span class=\"hljs-keyword\">import</span> App <span class=\"hljs-keyword\">from</span> <span class=\"hljs-string\">''./App.vue''</span>\n\nVue.use(ElementUI)\n\n<span class=\"hljs-keyword\">new</span> Vue({\n  <span class=\"hljs-attr\">el</span>: <span class=\"hljs-string\">''#app''</span>,\n  <span class=\"hljs-attr\">render</span>: <span class=\"hljs-function\"><span class=\"hljs-params\">h</span> =&gt;</span> h(App)\n})\n\n</code></div></pre>\n<p>以上代码便完成了 Element 的引入。需要注意的是，样式文件需要单独引入。</p>\n<h4>按需引入</h4>\n<p>借助 babel-plugin-component，我们可以只引入需要的组件，以达到减小项目体积的目的。</p>\n<p>首先，安装 babel-plugin-component：</p>\n','## 快速上手\n\n本节将介绍如何在项目中使用 Element。\n\n### 使用 Starter Kit\n我们提供了通用的项目模板，你可以直接使用。对于 Laravel 用户，我们也准备了相应的模板，同样可以直接下载使用。\n\n如果不希望使用我们提供的模板，请继续阅读。\n\n### 使用 vue-cli\n\n我们还可以使用 vue-cli 初始化项目，命令如下：\n\n```language\n> npm i -g vue-cli\n> mkdir my-project && cd my-project\n> vue init webpack\n> npm i && npm i element-ui\n```\n\n### 引入 Element\n你可以引入整个 Element，或是根据需要仅引入部分组件。我们先介绍如何引入完整的 Element。\n\n#### 完整引入\n在 main.js 中写入以下内容：\n```javascript\nimport Vue from ''vue''\nimport ElementUI from ''element-ui''\nimport ''element-ui/lib/theme-chalk/index.css''\nimport App from ''./App.vue''\n\nVue.use(ElementUI)\n\nnew Vue({\n  el: ''#app'',\n  render: h => h(App)\n})\n\n```\n以上代码便完成了 Element 的引入。需要注意的是，样式文件需要单独引入。\n\n#### 按需引入\n借助 babel-plugin-component，我们可以只引入需要的组件，以达到减小项目体积的目的。\n\n首先，安装 babel-plugin-component：\n\n','');
INSERT INTO `iy_article_body` VALUES ('2', 'html1111111','test','');
INSERT INTO `iy_article_body` VALUES ('3', 'html1111111','test','');
INSERT INTO `iy_article_body` VALUES ('4', 'html1111111','test','');
INSERT INTO `iy_article_body` VALUES ('5', 'html1111111','test','');
INSERT INTO `iy_article_body` VALUES ('6', 'html1111111','test','');
INSERT INTO `iy_article_body` VALUES ('7', 'html1111111','test','');
INSERT INTO `iy_article_body` VALUES ('8', 'html1111111','test','');
INSERT INTO `iy_article_body` VALUES ('9', 'html1111111','test','');
INSERT INTO `iy_article_body` VALUES ('10', 'html1111111','test','');
INSERT INTO `iy_article_body` VALUES ('11', 'html1111111','test','');
INSERT INTO `iy_article_body` VALUES ('12', 'html1111111','test','');
INSERT INTO `iy_article_body` VALUES ('13', 'html1111111','test','');
INSERT INTO `iy_article_body` VALUES ('14', 'html1111111','test','');
INSERT INTO `iy_article_body` VALUES ('15', 'html1111111','test','');
INSERT INTO `iy_article_body` VALUES ('16', 'html1111111','test','');
INSERT INTO `iy_article_body` VALUES ('17', 'html1111111','test','');
INSERT INTO `iy_article_body` VALUES ('18', 'html1111111','test','');
INSERT INTO `iy_article_body` VALUES ('19', 'html1111111','test','');
INSERT INTO `iy_article_body` VALUES ('20', 'html1111111','test','');

```
# 设计表结构

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

# 用户初始化
INSERT INTO `iy_user` VALUES ('1', 'imoyao', '张牧志', '$6$rounds=656000$tIs6tFIsFTmqLpUi$rD2UcO0T7VXsVGeUee11oY6HcxbqluGzAXdUWHCDCpTK8fvsMC5rW8R1ZVhyY912MUK19xcnSqrYp88eKsuBH1', 'emailme8@163.com','中国·北京','凡人皆需侍奉！', '2018-01-22 17:14:49','2019-06-24 17:14:49', '1', null)

# 文章初始化


```
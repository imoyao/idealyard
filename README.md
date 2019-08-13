# IdealYard

使用 `Vue` 和 `Flask` 搭建前后端分离的 RESTful 个人博客。
## 前置条件  
### Python

3.6+

### MySQL

```bash
mysql  Ver 14.14 Distrib 5.7.26, for linux-glibc2.12 (x86_64) using  EditLine wrapper
```
username：root

password：111111

数据库：`iyblog_dev`
```sql
-- 如果想支持emoji，就设置utf8mb4编码。
CREATE DATABASE iyblog_dev CHARSET=utf8mb4;
```

也可以通过修改配置之后自行定义。

1. 进入当前目录之后，先通过pip安装pipenv管理包
```bash
pip install pipenv [--user]
```
2. 安装Python依赖
```bash
pipenv install 
```
3. 配置环境变量
```bash
cd back
vi .flaskenv
```
4. 配置个人敏感信息
如百度翻译API秘钥，密码等
```bash
vi .env
```
## docker 支持
pass

## 更多
开发模式配置及说明参见[更多文档](./document/)  
TODO:此处需要持续更新。
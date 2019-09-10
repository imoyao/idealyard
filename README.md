# IdealYard

使用 `Vue` 和 `Flask` 搭建前后端分离的 RESTful 个人博客。
## 前置条件  

### Python

3.6+

### MySQL

```bash
mysql  Ver 14.14 Distrib 5.7.26, for linux-glibc2.12 (x86_64) using  EditLine wrapper
```
### 创建数据库

开发模式数据库：`iyblog_dev`，此处可以在[此处](back/config.py)修改配置

```sql
CREATE USER 'USERNAME'@'localhost' IDENTIFIED BY 'PASSWORD';
CREATE DATABASE DATABASENAME CHARSET=utf8mb4;
grant all privileges on DATABASENAME.* to USERNAME@localhost identified by 'PASSWORD';
-- 如果需要支持emoji，则设置utf8mb4编码。否则使用utf-8编码即可
CREATE DATABASE DATABASENAME CHARSET=utf8mb4;
```
### 环境配置

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
    vi .flaskenv
    ```
4. 编辑[dot.env](https://github.com/imoyao/idealyard/blob/master/dot.env)文件,配置环境变量并重命名为`.env`

    ```bash
    vi dot.env
    mv dot.env .env
    ```
## docker 支持

pass

  
## TODO

因为时间关系，还有一些问题没有解决，详见[此处](./document/TODOlist.md)
如果有同学需要`PR`，可以参考此处已知未解决问题和`bug`单。

## 更多

开发模式配置及说明参见[更多文档](./document/deploy.md)

## 致谢
与其在别处仰望 不如在这里并肩。    
感谢 G 小姐[@Sabiner](https://github.com/Sabiner)的鼓励才会产生动手写个人博客的想法。一切缘起，都要从丘处机路过牛家村的那个下午说起……

![不试怎么知道做不到呢？](./document/src/img_20190910153859.jpg)

同时感谢[@LeiWong](https://github.com/LeiWong)在开发中遇到问题帮助寻找`bug`并解决问题时付出的时间。 
  
---
> A human being should be able to change a diaper, plan an invasion, butcher a hog, conn a ship, design a building, write a sonnet, balance accounts, build a wall, set a bone, comfort the dying, take orders, give orders, cooperate, act alone, solve equations, analyze a new problem, pitch manure, program a computer, cook a tasty meal, fight efficiently, die gallantly. Specialization is for insects.
>
>一个人应该能够换尿布，
策划战争，
杀猪，
开船，
设计房子，
写十四行诗，
结算账户，
砌墙，
接脱臼的骨头，
安慰濒死的人，
服从命令，
发布命令，
携手合作，
独立行动，
解数学方程，
分析新问题，
铲粪，
电脑编程，
做出可口的饭，
善打架，
勇敢地死去。
只有昆虫才专业化。

-- 罗伯特·安森·海因莱因  《时间足够你爱》
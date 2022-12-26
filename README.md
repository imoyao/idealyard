# IdealYard
[![LICENSE](https://img.shields.io/badge/license-Anti%20996-blue.svg)](https://github.com/996icu/996.ICU/blob/master/LICENSE)

使用 `Vue2` 和 `Flask` 搭建前后端分离的 RESTful 个人博客。

关于该项目的部分说明可在此处找到👉[About IdealYard](https://masantu.com/categories/Projects/IdealYard/)，如果没有找到需要的内容，请邮件或者 Issues 交流；

## ⚠ 注意
1. 该博客仅用于学习原理，前端页面并**未实现**响应式布局，暂时也没有精力去实现，博客内容也没有时间去打理。关于日常的记录博客主要在[别院牧志](https://imoyao.github.io/)之中更新。   

2. 如果你是 Flask 初学者，推荐一本国人书籍给大家《Flask Web开发实战：入门、进阶与原理解析》，本人也是该书的阅读者与受益者。同时建议多去这个网站看看：[HelloFlask - Flask资源集合地](http://helloflask.com/)

3. 由于服务器到期，本博客暂无演示功能，如果有同学部署上线并可以提供演示链接，则非常感谢。暂时请点击下方链接观看简单的功能演示。
[使用 Vue 和 Flask 搭建前后端分离的 RESTful 个人博客功能展示_哔哩哔哩 (゜-゜)つロ 干杯~-bilibili](https://www.bilibili.com/video/BV11v411v76q?zw)

4. 由于[此处](https://github.com/flask-restful/flask-restful/issues/883) 提到的原因，Flask-RESTful 已经不是一个很好的选择，可能[flask-restx](https://github.com/python-restx/flask-restx) 和 [Apiflask](https://github.com/greyli/apiflask) <国人开发>（注意：由于本框架正在活跃开发期内，使用时请慎重评估）  是一个更好的替代品。如果需要学习，也推荐迁移到维护更加积极的扩展上面去。

 注意区分扩展和框架的区别，参阅：[请不要把 Flask 和 FastAPI 放到一起比较 | 李辉](https://greyli.com/flask-fastapi/)
 > 既然「FastAPI 应该和基于 Flask 的 Web API 框架比较」，那么合适的比较对象有哪些？[Flask-RESTX](https://github.com/python-restx/flask-restx)、[Flask-Rebar](https://github.com/plangrid/flask-rebar)、[flask-apispec](https://github.com/jmcarp/flask-apispec)、[flask-smorest](https://github.com/marshmallow-code/flask-smorest)、[Flask-RESTful](https://github.com/flask-restful/flask-restful)、[APIFairy](https://github.com/miguelgrinberg/APIFairy) 这些虽然试图做成框架，但在具体实现上仍然是 Flask 扩展。

## 交流
1. 技术问题请尽量使用[Issues · imoyao/idealyard](https://github.com/imoyao/idealyard/issues)提问回馈社区，参阅：[Issue #15 · imoyao/idealyard](https://github.com/imoyao/idealyard/issues/15)
2. 在网友的提议下建立了 QQ 群，群号：613922612。但是请注意：该项目为单纯开源，本人并不靠此盈利（有自己的砖要搬），在可预见的未来也**没有可能**投入到为大家答疑解惑中去。所以该群的目的更多是建立一个小白之间互相交流的途径。如果可能，请在公开场合讨论你的问题而不是简单地抛出截图等待答案。

![QQ 群扫码关注](document/src/idealyard-qq-group.png)

 **注意**
 > 如非必要，请谨慎考虑是否加入！有部分同学加入后一句话不说又退群，这样申请加群然后又退群的操作会对我造成不必要的打扰。

3. 友善、友善、友善。网络一线牵，珍惜这段缘。请务必和善、诚恳地对待其他同学。

## 前置条件  

### Python

3.6+

### MySQL

```bash
mysql  Ver 14.14 Distrib 5.7.26, for linux-glibc2.12 (x86_64) using  EditLine wrapper
```
或者

### MariaDB
```bash
[root@python]# mysql --version
mysql  Ver 15.1 Distrib 5.5.64-MariaDB, for Linux (x86_64) using readline 5.1
```
### 创建数据库

开发模式数据库：`iyblog_dev`，可以在[此处](back/config.py)修改配置

```sql
CREATE USER 'USERNAME'@'localhost' IDENTIFIED BY 'PASSWORD';
-- 如果需要支持emoji，则设置utf8mb4编码。否则使用utf-8编码即可
CREATE DATABASE DATABASENAME CHARSET=utf8mb4;
grant all privileges on DATABASENAME.* to USERNAME@localhost identified by 'PASSWORD';
flush privileges;
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
    mv dot.env .env        # 参考 master 分支
    ```
### 前端

node和npm/yarn的安装和换源请网络搜索教程自行完成。

前端部署部分是以`npm`作为包管理工具进行演示的，如果使用`yarn`进行包管理，请自行修改（你都使用yarn了，肯定不会找不到`package.json`的。😉）

前端指令配置请参考`front/package.json`中的`scripts`章节。

#### 安装依赖
```shell
npm install
```
#### 开发模式

1. 修改前端文件`front/config/dev.env.js`中后端请求的地址和端口为实际api地址 
2. 启动前端
```shell
npm run dev
```
#### 生产模式

1. 切换目录
```bash
cd front
```
2. 设置`prod`环境`BASE_API`地址
```javascript
// /idealyard/front/config/prod.env.js
module.exports = {
  NODE_ENV: '"production"',
  BASE_API: '"http://192.168.116.21:5000/api"'  // TODO:修改为真实API地址
}
```
3. 设置`router`为`history`模式
```javascript
// path: front/src/router/index.js:16

const router = new VueRouter({
  // https://router.vuejs.org/zh/guide/essentials/history-mode.html#html5-history-%E6%A8%A1%E5%BC%8F
  // mode: 'history',
  routes: []
})
```
4. build文件
```bash
npm run build
```
请参阅`document/deploy.md` 文件了解更多。

## Docker 支持

pass

## TODO

因为时间关系，还有一些问题没有解决，详见[此处](./document/TODOlist.md)    
如果有同学需要`PR`，也可以参考此处已知未解决问题和`bug`单。

## 更多
与其在别处仰望,不如在这里并肩。 
开发模式配置及说明参见[更多文档](./document/deploy.md)

### 代码概览

目录结构和代码量统计参考[此处](./document/README.MD)  

### 前端概览    
![网站概览](document/src/overview.gif)  

![首页](document/src/overview.jpg)

![标签页](document/src/tags.jpg)

![重置密码](document/src/reset_password.jpg)

## 致谢   

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
只有昆虫才囿于一门。

-- 罗伯特·安森·海因莱因  《时间足够你爱》

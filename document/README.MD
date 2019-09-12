## 代码量
```bash
imoyao@local:~/iyblog$ cloc . --fullpath --not-match-d=/front/src/assets/
     153 text files.
     151 unique files.                                          
      33 files ignored.

github.com/AlDanial/cloc v 1.74  T=1.12 s (115.2 files/s, 10816.3 lines/s)
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Vuejs Component                 30            553            225           4170
Python                          48            540           1163           2332
JavaScript                      34            167            137           1336
Markdown                         9            120              0            551
SQL                              4             85            155            412
JSON                             1              0              0             82
INI                              1             11              0             34
Mako                             1              7              0             17
HTML                             1              0              1             15
-------------------------------------------------------------------------------
SUM:                           129           1483           1681           8949
-------------------------------------------------------------------------------

```
## 目录结构
```bash
imoyao@local:~/iyblog$ tree -L 3 -I "node_modules|*.pyc" 
```

```
.
├── back        # 后端代码
│   ├── api_1_0     # RESTful API
│   │   ├── archives.py
│   │   ├── auth.py
│   │   ├── books.py
│   │   ├── categories.py
│   │   ├── comments.py
│   │   ├── decorators.py
│   │   ├── errors.py
│   │   ├── __init__.py
│   │   ├── posts.py
│   │   ├── __pycache__
│   │   ├── tags.py
│   │   ├── uploads.py
│   │   ├── users.py
│   │   └── utils.py
│   ├── config.py
│   ├── controller      # view层
│   │   ├── archives.py
│   │   ├── categories.py
│   │   ├── __init__.py
│   │   ├── posts.py
│   │   ├── __pycache__
│   │   └── tags.py
│   ├── docs
│   │   ├── data.md
│   │   └── separate_frontend_and_backend.md
│   ├── exception.py
│   ├── flask.log
│   ├── __init__.py
│   ├── iyblog_data
│   │   ├── sql
│   │   └── test_data
│   ├── main
│   │   ├── errors.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   └── views.py
│   ├── mains.py
│   ├── models.py       # model 层
│   ├── __pycache__
│   ├── README.md
│   ├── requirements.txt
│   ├── runserver.py        # 程序入口
│   ├── setting.py
│   ├── src
│   │   └── sql
│   ├── static
│   │   └── images
│   └── utils
│       ├── date.py
│       ├── __init__.py
│       ├── __pycache__
│       └── text.py
├── document        # 个人记录文档
│   ├── etc
│   │   ├── dev_config.py
│   │   ├── nginx.conf
│   │   ├── readme.md
│   │   ├── supervisord.conf
│   │   └── unicorn.py
│   ├── README.MD
│   └── 微信截图_20190617154417.png
├── front       # 前端
│   ├── build
│   │   ├── build.js
│   │   ├── check-versions.js
│   │   ├── logo.png
│   │   ├── utils.js
│   │   ├── vue-loader.conf.js
│   │   ├── webpack.base.conf.js
│   │   ├── webpack.dev.conf.js
│   │   └── webpack.prod.conf.js
│   ├── config
│   │   ├── dev.env.js
│   │   ├── index.js
│   │   └── prod.env.js
│   ├── index.html
│   ├── package.json
│   ├── README.md
│   ├── src
│   │   ├── api
│   │   ├── App.vue
│   │   ├── assets
│   │   ├── components
│   │   ├── Home.vue
│   │   ├── main.js
│   │   ├── request
│   │   ├── router
│   │   ├── store
│   │   ├── utils
│   │   └── views
│   └── static
│       ├── category
│       ├── favicon.ico
│       ├── tag
│       ├── user
│       └── vedio
├── LICENSE
├── Pipfile
├── Pipfile.lock
├── README.md

```
## 数据库迁移
```bash
cd back
flask db init       # 第一次初始化时执行一次
flask db migrate -m 'add iy_article slug'       # 生成迁移脚本
flask db upgrade        # 执行迁移，更新数据库  降级回滚使用 flask db downgrade

```


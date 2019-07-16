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

可参考的一些项目

- [vue-admin](https://github.com/taylorchen709/vue-admin)
- [vue-element-admin](https://github.com/PanJiaChen/vue-element-admin)

## 安装环境依赖

### 后端
```shell
pip install -r requirments.txt 
```

## 启动服务

### 命令行启动
```shell
export FLASK_APP=runserver.py   
export FLASK_ENV=default        # 设置env
flask run --host=0.0.0.0        # 外部访问
```
### PyCharm启动

配置`Run/Debug Configuration`,如下
```shell
FLASK_APP = runserver.py           # default script path,if module name: FLASK_APP = runserver
FLASK_ENV = development
FLASK_DEBUG = 1
In folder XXX/idealyard/back
ssh://root@192.168.*.*:22/home/*/envs/*/bin/python -u -m flask run --host=0.0.0.0
```

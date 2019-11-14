# 安装记录及说明

## 有外网
或者本地源可用，直接使用pip管理所有依赖；建议使用`virtualenv`管理`Python`环境；
```bash
pip3 install -r requirements.txt
```
## 没有外网

### 安装Python3
```bash
# 可能需要安装
yum install gcc
yum install zlib* -y
yum install libffi-devel -y

tar -xzvf Python-3.6.9.tgz 
cd Python-3.6.9
mkdir -p /usr/local/python3 
./configure --prefix=/usr/local/python3 

make && make install
ln -s /usr/local/python3/bin/python3 /usr/bin/python3
```
```sh
which python3
/usr/bin/python3
```
```sh
python3 --version
Python 3.6.9
```
```shell
# pip3
ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
pip3 -V
pip 19.0.3 from /usr/local/python3/lib/python3.6/site-packages/pip (python 3.6)

# pipenv
pip3 install pipenv
ln -s /usr/local/python3/bin/pipenv /usr/bin/pipenv
```
### 安装 Celery

依次安装下面依赖，或者根据提示报错查找包安装
```bash
 pip3 install vine-1.3.0-py2.py3-none-any.whl 
 pip3 install amqp-2.5.0-py2.py3-none-any.whl 
 pip3 install kombu-4.6.3-py2.py3-none-any.whl 
 pip3 install celery-4.3.0-py2.py3-none-any.whl 

 tar -xzvf billiard-3.6.0.0.tar.gz 
 cd billiard-3.6.0.0
 python3 setup.py install

 pip3 install pytz-2019.1-py2.py3-none-any.whl 
 pip3 install celery-4.3.0-py2.py3-none-any.whl 

```
### 安装Flask

### 报错处理
```bash
c/_cffi_backend.c:2:20: fatal error: Python.h: No such file or directory
 #include <Python.h>
                    ^
compilation terminated.
error: command 'gcc' failed with exit status 1

yum install python-devel

```
## 配置 YUM 源

```bash
-bash-4.2# vi /etc/yum.repos.d/c7.repo 

[c7]
name=c7
baseurl=http://10.10.1.8/centos-7.6/
gpgcheck=0
enabled=1
[c7-epel]
name=c7-epel
baseurl=http://10.10.1.8/epel/7/x86_64/
gpgcheck=0
enabled=1
[c7-odsp]
name=c7-odsp
baseurl=http://10.10.1.8/odsp/5.0_new/
gpgcheck=0
enabled=1
```

## 安装数据库

版本要求
```bash
# -bash-4.2# mysql -V
mysql  Ver 15.1 Distrib 10.2.25-MariaDB, for Linux (x86_64) using readline 5.1

```
### 创建数据库及用户（可选）

pass

## 开放访问端口

**注意**：此处端口为API端口5000，假如你修改了端口，则此处应该做相应调整
```bash
# 查询
-bash-4.2# iptables -nL|grep 5000
# 开放指定端口
-bash-4.2# iptables -I INPUT -p tcp --dport 5000 -j ACCEPT
# 再次查询
-bash-4.2# iptables -nL|grep 5000
ACCEPT     tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:5000
```
CentOS7 使用`firewall-cmd`管理防火墙端口
```bash
firewall-cmd --query-port=5000/tcp      # no
firewall-cmd --add-port=5000/tcp --permanent
firewall-cmd --reload
firewall-cmd --query-port=5000/tcp  # yes
systemctl status firewall
systemctl status firewalld
systemctl restart firewalld
```
此处完成之后访问`http://SERVERIP:5000/`应该可以看到`This is Index Page.`的页面提示信息，表示接口应用访问正常。

前端端口8080同上，不作赘述。

TODO: 此处需要写进脚本或者SQL直接导入
```sql
insert into user values('1','admin','$6$rounds=656000$Ph.Ew29UyB5l/hdG$g2Jw/PcP5gkzwnj9k2AaglAHBu/d2Qs0xhGbp8JQnPVHYsr1mFTbNICY.NXmaiqdNrC4hiOQ.RCI.YgRU1f3w/')
```

## celery

### pip安装celery
略
添加软链接
```bash
-bash-4.2# ln -s /usr/local/python3/bin/celery /usr/bin/celery
```
### 使用celery

前置条件：保证消息队列（rabbitMQ/Redis）已经后台启动。
以redis作为backend为例：
```bash
-bash-4.2# redis-cli

127.0.0.1:6379> ping
PONG

```
执行`celery`必须有管理员权限
```bash
# run celery worker
celery -A celery_worker:celery worker --loglevel=DEBUG
# run celery beat for periodic tasks
celery -A celery_worker:celery beat --loglevel=INFO
# run flask app
env 'FLASK_APP=manage.py' flask run
```

## 部署
### 前端
1. 修改`PMMT/pmfrontend/src/api/index.js`中的api地址为部署机器的ip地址，如果需要，则修改响应port；
2. 修改`PMMT/pmfrontend/config/index.js`中`module.exports`的`build`配置，使释出文件路径到指定目录；
```bash
  build: {
    // Template for index.html
    index: path.resolve(__dirname, '../dist/index.html'),   # ../../dist/index.html 表示释出到项目根目录

    // Paths
    assetsRoot: path.resolve(__dirname, '../dist'),     # ../../dist
```
3. 运行`npm run build` 导出`dist`目录；
4. 如果是在开发机器上进行上述操作，则将`dist`打包并上传到部署机器的工作根目录；

### 后端
#### nginx子配置
```bash
$-bash-4.2# vi  /etc/nginx/conf.d/app.conf 
server {
    listen  82;     # 默认80端口，因为被我们`lighttpd`使用，所以此处修改为82，到时候访问时也需要指定端口
    server_name localhost;      # 必要时填写域名
    charset utf-8;
    access_log /var/log/pmmt/access.log;
    error_log /var/log/pmmt/error.log;
    client_max_body_size 100M;
    location / {
 	 root /usr/local/PMMT/dist;
	 try_files $uri $uri/ /index.html last;
         index index.html index.htm;
    }
    location /api {
        proxy_pass  http://127.0.0.1:5000;      # 代理端口
        proxy_http_version 1.1;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        proxy_read_timeout 300;
        send_timeout 300;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $http_host;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header X-Forwarded-Port $server_port;
        proxy_set_header X-Request-Start $msec;
    }
}
```
- 相关命令

```bash
nginx -s reload
systemctl start/stop/restart/status nginx
```
#### supervisor配置

- flask应用配置
    ```bash
    $-bash-4.2# vi /etc/supervisord.d/app.ini 
    ```
    ```bash
    [program:app]
    command=/usr/bin/gunicorn -c gun.py runserver:app
    directory=/usr/local/PMMT      
    startsecs=0
    stopwaitsecs=0
    autostart=true
    autorestart=true
    stderr_logfile=/var/log/pmmt/app_err.log
    stdout_logfile=/var/log/pmmt/app_out.log
    ```
- celery_work 配置
    ```bash
    -bash-4.2# cat /etc/supervisord.d/celery_work.ini 
    ```
    ```bash
    [program:celery_work]
    command=/usr/bin/celery -A celery_worker:celery worker -Q default,mail -c 10 -l info      # 按需配置 -Q后面跟消息队列
    directory=/usr/local/PMMT      
    startsecs=0
    stopwaitsecs=0
    autostart=true
    autorestart=true
    stderr_logfile=/var/log/celery/worker_err.log
    stdout_logfile=/var/log/celery/worker_out.log
    stopasgroup=true
    killasgroup=true
    ```
- celery_beat 定时任务配置

    ```bash
    -bash-4.2# cat /etc/supervisord.d/celery_beat.ini 
    ```
    ```bash
    [program:celery_beat]
    command=/usr/bin/celery -A celery_worker:celery beat -l info
    directory=/usr/local/PMMT      
    startsecs=0
    stopwaitsecs=0
    autostart=true
    autorestart=true
    stderr_logfile=/var/log/celery/beat_err.log
    stdout_logfile=/var/log/celery/beat_out.log
    stopasgroup=true
    killasgroup=true
    ```

**注意**：配置中的`command`应用路径最好使用绝对路径

- 相关命令

```bash
supervisord -c /etc/supervisord.conf

supervisorctl start all/APP_NAME
supervisorctl stop all/APP_NAME
supervisorctl restart all/APP_NAME
```
以上各种配置文件可参考[此处](../confs)
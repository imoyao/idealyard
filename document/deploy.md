## 前端

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
5. 上传服务器
压缩`dist`目录生成tar包并解压到前端目录（此处由用户自定义，或者根据配置文件默认放到前端目录中）
6. 解压并赋权
```bash
sudo unzip -d ./dist dist.zip       # 根据压缩包格式决定使用命令
sudo chown -R root:root dist        # 根据nginx中的配置确定
```

## 后端

## 安装依赖
```bash
pipenv install
```
or  
```bash
cd back
pip install -r requirements.txt
```
## 安装`nginx`
### Ubuntu 安装  
参考[此处](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04)       
```bash
sudo apt update
sudo apt install nginx
sudo ufw app list       # 防火墙设置
sudo ufw allow 'Nginx HTTP'
sudo ufw status
sudo ufw enable
sudo ufw status
systemctl status nginx      # 查看状态
```
### 配置
修改`confs/nginx/conf.d/app.conf`为你`build`之后`dist`目录所在路径。

```conf
location / {
 root /home/imoyao/iyblog/front/dist;       # 修改此处，按需修改为dist目录
 try_files $uri $uri/ /index.html last;
     index index.html index.htm;
 expires:30s;   # 缓存过期时间
}
```
### 相关命令

```bash
nginx -s reload
systemctl start/stop/restart/status nginx
```

## 安装supervisor
### pip
```bash
pip install supervisor
```
### Ubuntu

```bash
sudo apt-get install supervisor
```
### CentOS

```bash
yum install -y epel-release && yum install -y supervisor
```
### 配置
- 编辑配置
    ```bash
    [supervisord]
    logfile=/var/log/supervisor/supervisord.log ; (main log file;default $CWD/supervisord.log)
    pidfile=/var/run/supervisord.pid ; (supervisord pidfile;default supervisord.pid)
    childlogdir=/var/log/supervisor            ; ('AUTO' child log dir, default $TEMP)
    environment=BD_APP_ID='',foo='bar'                                          # TODO:此处根据实际配置环境变量
    ; the below section must remain in the config file for RPC
    ……
    ```
- 编辑子应用配置文件  
    ```bash
    vi /etc/supervisor/conf.d/app.conf
    ```
    写入  
    ```bash
    [program:app]
    command=/usr/bin/gunicorn -c gun.py runserver:app
    # 项目根目录路径
    directory=/home/imoyao/iyblog
    startsecs=0
    stopwaitsecs=0
    autostart=true
    autorestart=true
    stopasgroup=true
    killasgroup=true
    stderr_logfile=/var/log/app/app_err.log
    stdout_logfile=/var/log/app/app_out.log
    
    ```
**注意**：
- 上面的配置在`ubuntu`中以`.conf`结尾，在`CentOS`中以`.ini`结尾。

- 配置中的`command`应用路径最好使用绝对路径。

- 相关命令

    ```bash
    supervisord -c /etc/supervisord.conf  # Ubuntu:/etc/supervisor/supervisord.conf
    supervisorctl start all/APP_NAME
    supervisorctl stop all/APP_NAME
    supervisorctl restart all/APP_NAME
    ```
## 使用celery
执行`celery`必须有管理员权限
```bash
# run celery worker
celery -A celery_worker:celery worker --loglevel=DEBUG
# run celery beat for periodic tasks
celery -A celery_worker:celery beat --loglevel=INFO
```
前置条件：保证消息队列（rabbitMQ/Redis）已经后台启动。
以redis作为backend为例：
```bash
-bash-4.2# redis-cli

127.0.0.1:6379> ping
PONG
```
## 安装 redis
此处可以参考本人之前的一篇文章：[Linux 下如何安装 Redis？](https://imoyao.github.io/blog/2019-04-11/how-to-install-Redis-on-Linux/)  
`redisd` 所在目录
```bash
/etc/init.d/redisd
```
`6379.conf` 所在目录：
```bash
/etc/redis/6379.conf
```

## 数据库

### 导出数据库数据
```sql
mysqldump -h主机名 -P端口 -u用户名 -p密码 --databases 数据库名 | gzip > 文件名.sql.gz
```
### 导入数据库
```sql

```


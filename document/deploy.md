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
3. build文件
```bash
npm run build
```
## 后端
1. 安装依赖
```bash
pipenv install
```
or  
```bash
cd back
pip install -r requirements.txt
```
2. 安装`nginx`
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

```bash
location / {
 root /home/imoyao/iyblog/front/dist;       # 修改此处，按需修改为dist目录
 try_files $uri $uri/ /index.html last;
     index index.html index.htm;
 expires:30s;   # 缓存过期时间
}
```

3. 安装supervisor
### Ubuntu

```bash
sudo apt-get install supervisor
```
### CentOS

```bash
yum install supervisor
```
### 配置
编辑配置文件  
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

- 配置中的`command`应用路径最好使用绝对路径

- 相关命令

```bash
supervisord -c /etc/supervisord.conf
supervisorctl start all/APP_NAME
supervisorctl stop all/APP_NAME
supervisorctl restart all/APP_NAME
```

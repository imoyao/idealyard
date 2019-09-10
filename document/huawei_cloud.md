## 安装mysql
```bash
sudo apt-get update
sudo apt-get install mysql-server
```
## 安装Python3

```bash
sudo apt-get install python-software-properties
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:jonathonf/python-3.7
sudo apt-get update
sudo apt-get install python3.7
```
## 克隆代码

## 安装pipenv

### 换源
```bash
cd
mkdir .pip
vi pip.conf
```
copy下面内容
```bash
[global]
#index-url = http://mirrors.aliyun.com/pypi/simple/
index-url = https://pypi.mirrors.ustc.edu.cn/simple/
[install]
trusted-host = mirrors.aliyun.com
               pypi.python.org
	       pypi.mirrors.ustc.edu.cn
```
报错
```bash
Traceback (most recent call last):
  File "/usr/local/lib/python2.7/dist-packages/virtualenv.py", line 24, in <module>
    import distutils.spawn
ModuleNotFoundError: No module named 'distutils.spawn'

```
编辑`cat /etc/apt/sources.list`添加一下地址源

```bash
# deb cdrom:[Ubuntu 18.04 LTS _Bionic Beaver_ - Release amd64 (20180425.1)]/ bionic main restricted

# See http://help.ubuntu.com/community/UpgradeNotes for how to upgrade to
# newer versions of the distribution.
deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted
# deb-src http://cn.archive.ubuntu.com/ubuntu/ bionic main restricted

## Major bug fix updates produced after the final release of the
## distribution.
# deb-src http://cn.archive.ubuntu.com/ubuntu/ bionic-updates main restricted

## N.B. software from this repository is ENTIRELY UNSUPPORTED by the Ubuntu
## team. Also, please note that software in universe WILL NOT receive any
## review or updates from the Ubuntu security team.
deb http://mirrors.aliyun.com/ubuntu/ bionic universe
# deb-src http://cn.archive.ubuntu.com/ubuntu/ bionic universe
# deb-src http://cn.archive.ubuntu.com/ubuntu/ bionic-updates universe

## N.B. software from this repository is ENTIRELY UNSUPPORTED by the Ubuntu 
## team, and may not be under a free licence. Please satisfy yourself as to 
## your rights to use the software. Also, please note that software in 
## multiverse WILL NOT receive any review or updates from the Ubuntu
## security team.
deb http://mirrors.aliyun.com/ubuntu/ bionic multiverse
# deb-src http://cn.archive.ubuntu.com/ubuntu/ bionic multiverse
# deb-src http://cn.archive.ubuntu.com/ubuntu/ bionic-updates multiverse

## N.B. software from this repository may not have been tested as
## extensively as that contained in the main release, although it includes
## newer versions of some applications which may provide useful features.
## Also, please note that software in backports WILL NOT receive any review
## or updates from the Ubuntu security team.
# deb-src http://cn.archive.ubuntu.com/ubuntu/ bionic-backports main restricted universe multiverse

## Uncomment the following two lines to add software from Canonical's
## 'partner' repository.
## This software is not part of Ubuntu, but is offered by Canonical and the
## respective vendors as a service to Ubuntu users.
# deb http://archive.canonical.com/ubuntu bionic partner
# deb-src http://archive.canonical.com/ubuntu bionic partner

# deb-src http://security.ubuntu.com/ubuntu bionic-security main restricted
# deb-src http://security.ubuntu.com/ubuntu bionic-security universe
# deb-src http://security.ubuntu.com/ubuntu bionic-security multiverse
deb http://www.rabbitmq.com/debian/ testing main

```
```bash

cd idealyard
pip install pipenv -y

```
### 启服务测试
```shell
(iyblog) imoyao@python-iy:$ python runserver.py 
 * Serving Flask app "back" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 238-568-563
```
打开本地之后无法访问
需要在安全组中开放5000端口，参见此处[flask,无法通过浏览器访问公网ip](https://www.cnblogs.com/shiyuzuxia/p/9265134.html)    
```python
if __name__ == '__main__':
    app.run(host='192.168.0.108')       # 此处ip修改为内网ip地址
```
## 设置supervisor 开机自启

```
vi /etc/systemd/system/supervisord.service
```
```bash
[Unit]
Description=Supervisor daemon
Documentation=http://supervisord.org
After=network.target

[Service]
ExecStart=/usr/local/bin/supervisord -n -c /etc/supervisor/supervisord.conf     # 根据实际配置
ExecStop=/usr/local/bin/supervisorctl $OPTIONS shutdown
ExecReload=/usr/local/bin/supervisorctl $OPTIONS reload
KillMode=process
Restart=on-failure
RestartSec=42s[Unit]
Description=Supervisor daemon
Documentation=http://supervisord.org
After=network.target


[Install]
WantedBy=multi-user.target

```
执行
```bash
systemctl enable supervisord.service
```
此时重启，就会发现，supervisor已经启动了。
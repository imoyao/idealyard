# 用来保存 flask 相关的环境变量
FLASK_APP = 'runserver'
FLASK_DEBUG = False      # 开启DEBUG模式 **注意**：生产模式下必须关闭
FLASK_ENV = 'production'   # 配置工作模式（此处默认开发模式）
FLASK_CONFIG = 'production'        # 使用的配置环境（默认使用生产配置）
FLASK_HOST = '192.168.0.108'      # hw_cloud
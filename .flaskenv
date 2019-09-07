# 用来保存 flask 相关的环境变量
FLASK_APP = 'runserver'
FLASK_DEBUG = True      # 开启DEBUG模式 **注意**：生产模式下必须关闭
FLASK_ENV = 'development'   # 配置工作模式（此处默认开发模式）
FLASK_CONFIG = 'default'        # 使用的配置环境（默认使用开发配置）
FLASK_HOST = '192.168.0.108'      # hw_cloud
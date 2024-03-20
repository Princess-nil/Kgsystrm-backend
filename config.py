import os
from datetime import timedelta

SECRET_KEY = 'dasdsddasfas'

# 项目根路径
BASE_DIR = os.path.dirname(__file__)

# 数据库配置
DB_USERNAME = "root"
DB_PASSWORD = "2350770456zh"
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_DATABASE = "graph"

#session过期时间
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

DB_URI = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8mb4" % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
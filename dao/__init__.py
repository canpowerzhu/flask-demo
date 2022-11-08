# @Author  : kane.zhu
# @Time    : 2022/11/8 14:00
# @Software: PyCharm
# @Description:

from flask_sqlalchemy import SQLAlchemy
from settings.conf import PrdConfig
import pymysql
from flask import current_app
pymysql.install_as_MySQLdb()


db = SQLAlchemy()


class DatabaseConfig():
    # 连接的数据库 URI
    # mysql://用户名:密码@host:port/database
    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}:{}/{}'.format(PrdConfig.DB_USER, PrdConfig.DB_PASSWD, PrdConfig.DB_HOST,
                                                              PrdConfig.DB_PORT, PrdConfig.DB_DATABASE)
    # 是否追踪数据的修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 是否显示生成sql语句
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_RECYCLE = 200

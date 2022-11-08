# @Author  : kane.zhu
# @Time    : 2022/11/7 21:23
# @Software: PyCharm
# @Description:
from flask import Flask, Blueprint
from settings.conf import app_config


def create_app():
    app = Flask(__name__)
    app.config.from_object(app_config)

    from dao import db
    # db.init_app(app)

    # 注册管理user蓝图
    from src.user_bp.v1.user_crud import user_crud_bp
    app.register_blueprint(user_crud_bp)

    return app

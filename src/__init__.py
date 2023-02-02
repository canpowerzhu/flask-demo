# @Author  : kane.zhu
# @Time    : 2022/11/7 21:23
# @Software: PyCharm
# @Description:


from flask import Flask

from dao import DatabaseConfig

from src.user_bp.v1.user_crud import user_crud_bp
from src.aliyun_bp.v1.sts_main import sts_api_bp
from src.celery_bp.v1.celery_main import task_bp
from src.login_out_bp.v1.auth import login_out_bp





def create_app():
    app = Flask(__name__)
    app.config.from_object(DatabaseConfig)

    with app.app_context():
        from dao import db

        db.init_app(app)
        # 需要在db.create_all()
        # 所在的文件里面的顶部事先导入那些model
        db.create_all()

    # 注册
    app.register_blueprint(login_out_bp)
    app.register_blueprint(user_crud_bp)
    app.register_blueprint(sts_api_bp)
    app.register_blueprint(task_bp)
    app.secret_key = "affedasafafqwe"
    return app

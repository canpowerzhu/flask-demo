# @Author  : kane.zhu
# @Time    : 2022/11/7 21:23
# @Software: PyCharm
# @Description:


from flask import Flask,request,jsonify
from log_settings import logger
import uuid
from dao import DatabaseConfig
from src.aliyun_bp.v1.ali_mail import mail_ali_bp

from src.user_bp.v1.user_crud import user_crud_bp
from src.aliyun_bp.v1.sts_main import sts_api_bp
from src.celery_bp.v1.celery_main import task_bp
from src.login_out_bp.v1.auth import login_out_bp
from src.domain_bp.v1.name_domain import domain_name_bp
from src.aliyun_bp.v1.ali_domain import domain_ali_bp
from src.jenkins_bp.v1.jenkins_job import jenkins_ops_bp
from src.gitlab_bp.v1.gitlab_funcs import gitlab_bp
from dao import db





def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(DatabaseConfig)

    @app.before_request
    def add_trace_id():
        trace_id = request.headers.get('X-Trace-Id')
        if not trace_id:
            trace_id = str(uuid.uuid4())
        request.trace_id = trace_id

    @app.before_request
    def before():
        url = request.path
        # 明确白名单接口地址， 首页、登陆以及注册无需验证
        pass_list = ['/','/login','/signup']
        # 这里不做静态资源的限制
        if url in pass_list:
            pass
        else:
            return jsonify({"code":401,"message":"Full authentication is required to access this resource"})

    @app.after_request
    def add_trace_id_to_logs(response):
        logger.info('Trace ID in Flask after_request: {trace_id}', trace_id=request.trace_id)
        return response


    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)
    setup_app(app)
    return app


def setup_app(app):
    # Create tables if they do not exist already
    @app.before_first_request
    def create_tables():
        db.create_all()
    db.init_app(app)
    app.register_blueprint(login_out_bp)
    app.register_blueprint(user_crud_bp,url_prefix="/v1/user")
    app.register_blueprint(domain_name_bp,url_prefix="/v1/domain")
    app.register_blueprint(sts_api_bp,url_prefix="/v1/ali_cloud/sts")
    app.register_blueprint(domain_ali_bp,url_prefix="/v1/ali_cloud/domain")
    app.register_blueprint(task_bp,url_prefix="/v1/celery_kane")
    app.register_blueprint(jenkins_ops_bp,url_prefix="/v1/jenkins")
    app.register_blueprint(mail_ali_bp,url_prefix="/v1/ali_cloud/mail")
    app.register_blueprint(gitlab_bp,url_prefix="/v1/gitlab")